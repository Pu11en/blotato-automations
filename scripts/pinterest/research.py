"""Evidence import and explainable ranking. Creative judgment is explicit input."""
from copy import deepcopy
from pathlib import Path
from .core import Invalid, now, digest, validate, read, atomic, locked, snapshot, load_run, save_run, pin_id, identifier, ROOT
from . import adapters


def collect(directory, profile_path, mode='manual', signals=(), references=(), live=False):
    profile = validate('profile', read(profile_path))
    if live and mode != 'live':
        raise Invalid('Live collection requires live mode')
    with locked(directory) as d:
        if (d/'run.json').exists():
            run = load_run(d)
            if run['profile_hash'] != digest(profile) or run['mode'] != mode:
                raise Invalid('Profile/mode changed; use a new run directory')
        else:
            run = {'schema_version':1,'run_id':identifier(d.name),'brand':profile['brand'],'region':profile['region'],
                   'created_at':now(),'profile_hash':digest(profile),'mode':mode,'queries':profile['queries'],
                   'sources':{},'signals':[],'references':[],'candidates':[], 'paid_calls':0,'publish_calls':0,
                   'dependency_revisions':read(ROOT/'templates/pinterest/dependencies.json')['revisions']}
            atomic(d/'profile.json', profile)
        incoming_signals, incoming_refs = list(signals), list(references)
        for kind, rows in [('signal', incoming_signals), ('reference', incoming_refs)]:
            for item in rows:
                validate(kind, item)
                if item['mode'] == 'fixture' and mode != 'fixture':
                    raise Invalid('Fixture evidence cannot enter a real run')
                if kind == 'signal' and item['region'] != run['region']:
                    raise Invalid('Signal region does not match run')
        if live:
            for query in profile['queries']:
                for name in ('opencli', 'trends'):
                    key = name + ':' + query
                    if key in run['sources']:
                        continue  # Resume never repeats a request; use a new run for a fresh snapshot.
                    checkpoint = d/'checkpoints'/(digest(key)+'.json')
                    if checkpoint.exists():
                        cached = read(checkpoint)
                    else:
                        cached = {'signals':[], 'references':[]}
                        try:
                            if name == 'opencli':
                                raw = adapters.opencli('search-pins', query)
                                cached['references'] = adapters.references(raw, query)
                            else:
                                raw, cached['signals'] = adapters.fetch_trends(profile['region'], query)
                            snapshot(d, raw)
                            cached['source'] = {'status':'available','reason':'Read completed','checked_at':now()}
                        except adapters.Unavailable as e:
                            cached['source'] = {'status':'unavailable','reason':str(e),'checked_at':now()}
                        atomic(checkpoint,cached)
                    incoming_refs.extend(cached['references'])
                    incoming_signals.extend(cached['signals'])
                    run['sources'][key] = cached['source']
        # Manual snapshot is a record of submitted evidence, not a claim we fetched its source.
        if signals or references:
            snapshot(d, {'signals':list(signals),'references':list(references)})
            run['sources']['manual_import'] = {'status':'available','reason':'User/agent-supplied evidence; source hashes retained','checked_at':now()}
        by_id = {x['id']:x for x in run['signals']}
        for item in incoming_signals:
            if item['observation_period']['start'] > item['observation_period']['end']:
                raise Invalid('Reversed observation period')
            if item['id'] in by_id and by_id[item['id']] != item:
                raise Invalid('Signal ID collision; use a new ID for a new observation')
            by_id[item['id']] = item
        run['signals'] = list(by_id.values())
        by_id = {x['id']:x for x in run['references']}
        for original in incoming_refs:
            item = deepcopy(original)
            item['id'] = pin_id(item['source_url'])
            item['source_url'] = 'https://www.pinterest.com/pin/' + item['id'] + '/'
            if item['rights'] != 'reference_only' and not item['rights_evidence']:
                raise Invalid('Reusable media requires rights evidence')
            if item['id'] in by_id:
                old = by_id[item['id']]
                item['queries'] = sorted(set(old['queries'] + item['queries']))
            by_id[item['id']] = item
        if len(by_id) > 50:
            raise Invalid('Pilot is limited to 50 unique reference Pins')
        run['references'] = list(by_id.values())
        save_run(d, run)
        write_report(d, run)
        return run


def rank(directory, assessments):
    with locked(directory) as d:
        run = load_run(d)
        profile = validate('profile', read(d/'profile.json'))
        products = {x['id']:x for x in profile['products']}
        signals = {x['id']:x for x in run['signals']}
        refs = {x['id']:x for x in run['references']}
        ranked = []
        seen = set()
        for original in assessments:
            c = deepcopy(validate('candidate_input', original))
            identifier(c['id'])
            if c['id'] in seen:
                raise Invalid('Duplicate candidate ID')
            seen.add(c['id'])
            if c['product_id'] not in products or any(x not in signals for x in c['signal_ids']) or any(x not in refs for x in c['reference_ids']):
                raise Invalid('Unknown product or evidence ID')
            product = products[c['product_id']]
            if any(signals[x]['query'].casefold() != c['keyword'].casefold() for x in c['signal_ids']):
                raise Invalid('Demand evidence must match the candidate keyword')
            measured = [signals[x] for x in c['signal_ids'] if signals[x]['source_type'] != 'editorial' and (signals[x]['time_series'] or any(v is not None for v in signals[x]['growth'].values()))]
            c['missing_evidence'] = []
            if not measured:
                c['scores']['demand_evidence'] = {'value':0,'reason':'No measured demand evidence for this keyword'}
                c['missing_evidence'].append('Measured Pinterest demand unavailable; concept is exploratory')
            if not c['reference_ids']:
                c['missing_evidence'].append('No reference Pins reviewed')
            if not product['verified_at']:
                c['missing_evidence'].append('Product destination requires a fresh check')
            c['status'] = 'qualified' if measured and c['reference_ids'] and product['verified_at'] else 'exploratory'
            if not c['scores']['product_fit']['value'] or not c['scores']['shopping_intent']['value']:
                c['status'] = 'excluded'
            c['total'] = sum(v['value'] for v in c['scores'].values())
            c['destination'] = product['url']
            c['destination_checked_at'] = product['verified_at']
            ranked.append(validate('candidate', c))
        order = {'qualified':0,'exploratory':1,'excluded':2}
        run['candidates'] = sorted(ranked, key=lambda c:(order[c['status']],-c['total'],c['id']))
        snapshot(d, assessments)
        save_run(d, run)
        write_report(d, run)
        return run['candidates']


def write_report(d, run):
    lines = ['# Pinterest research report', '', f"Mode: **{run['mode']}** · Region: {run['region']} · Collected: {run['created_at']}",
             '', 'Scores prioritize creative review; they do not predict clicks or sales. Public Pins provide inspiration, not competitor conversion data.', '', '## Source availability', '']
    for name, item in run['sources'].items():
        lines.append(f"- {name}: **{item['status']}** — {item['reason']}")
    lines += ['', '## Shortlist', '']
    selected = [c for c in run['candidates'] if c['status'] != 'excluded'][:3]
    lines.append(f"{sum(c['status']=='qualified' for c in selected)} qualified; {sum(c['status']=='exploratory' for c in selected)} exploratory. Missing evidence is not filled with guesses.")
    for c in selected:
        lines += ['',f"### {c['id']} — {c['status']} ({c['total']}/10)", c['rationale'],f"Product: {c['destination']}"]
        lines += [f"- {k}: {v['value']}/2 — {v['reason']}" for k,v in c['scores'].items()]
        lines += ['- Missing: '+x for x in c['missing_evidence']]
        lines += ['- Evidence IDs: '+', '.join(c['signal_ids']+c['reference_ids'])]
    lines += ['', '## Demand evidence', '']
    for s in run['signals']:
        lines += [f"- {s['id']} | {s['query']} | {s['source_url']} | {s['retrieved_at']}",
                  f"  Period {s['observation_period']}; {s['metric_definition']}; unit={s['unit']}; growth={s['growth']}; series={s['time_series']}"]
    lines += ['', '## Reference Pins', '']
    for r in run['references']:
        lines += [f"- {r['source_url']} — {r['title']} — creator: {r['creator'] or 'unknown'} — {r['rights']}"]
        lines += ['  '+x for x in r['observations']]
    lines += ['', 'Paid calls: 0. Publishing calls: 0.']
    atomic(Path(d)/'report.md', '\n'.join(lines)+'\n')
