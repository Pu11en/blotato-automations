"""Idempotent cumulative snapshots. Never infer order attribution from posting time."""
from copy import deepcopy
from datetime import date, timedelta, datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from .core import Invalid, read, validate, digest, atomic, locked, load_run, identifier, pin_id, now, snapshot

METRICS = {'pinterest':{'impressions','saves','outbound_clicks'},'website':{'sessions','orders','revenue','refunds'},'costs':{'production_cost'}}
MONEY = {'revenue','refunds','production_cost'}


def register(directory, record):
    required={'asset_id','pin_url','published_date','account_id','authorization_reference'}
    if set(record)!=required or not all(isinstance(v,str) and v for v in record.values()):
        raise Invalid('Publication record requires asset, Pin URL, date, account and authorization reference')
    date.fromisoformat(record['published_date'])
    identifier(record['asset_id'])
    with locked(directory) as d:
        profile=read(d/'profile.json')
        if profile['accounts']['pinterest'] != record['account_id']:
            raise Invalid('Publication account is not the configured authorized account')
        packs=[read(p) for p in (d/'briefs').glob('*/brief.json')]
        matches=[(p,v) for p in packs for v in p['variants'] if v['asset_id']==record['asset_id']]
        if len(matches)!=1:
            raise Invalid('Unknown or ambiguous asset')
        item={**record,'experiment_id':matches[0][0]['experiment_id'],'format':matches[0][1]['format'],'pin_id':pin_id(record['pin_url'])}
        path=d/'publications.json'
        rows=read(path) if path.exists() else []
        for old in rows:
            if old['asset_id']==item['asset_id'] or old['pin_id']==item['pin_id']:
                if old==item:return item
                raise Invalid('Publication association is immutable; use a new asset version')
        atomic(path,rows+[item])
        return item


def import_results(directory, records):
    with locked(directory) as d:
        run=load_run(d)
        profile=validate('profile',read(d/'profile.json'))
        pub=read(d/'publications.json') if (d/'publications.json').exists() else []
        by_asset={p['asset_id']:p for p in pub}
        path=d/'results.json'
        database=read(path) if path.exists() else {'schema_version':1,'imports':[],'snapshots':{}}
        batch_hash=digest(records)
        if batch_hash in database['imports']:
            return {'status':'already_imported','rows':len(database['snapshots'])}
        staged=deepcopy(database)
        for original in records:
            row=deepcopy(validate('result',original))
            source=row['source']
            if row['metric'] not in METRICS[source]:raise Invalid('Metric does not belong to source')
            if profile['accounts'][source] is None or profile['accounts'][source]!=row['account_id']:
                raise Invalid('Analytics account/property does not match configured account')
            if row['mode']=='fixture' and run['mode']!='fixture':raise Invalid('Fixture metrics cannot enter a real run')
            try:ZoneInfo(row['timezone'])
            except ZoneInfoNotFoundError:raise Invalid('Unknown timezone') from None
            if row['timezone']!=profile['timezone']:raise Invalid('Timezone does not match experiment profile')
            if row['period']['start']>=row['period']['end']:raise Invalid('Result periods are start-inclusive/end-exclusive and must have positive duration')
            if datetime.fromisoformat(row['extracted_at'].replace('Z','+00:00')).date()<date.fromisoformat(row['period']['end']):
                raise Invalid('Extraction predates completed reporting window')
            if row['metric'] in MONEY and row['currency'] is None:raise Invalid('Monetary metric requires currency')
            if row['metric'] not in MONEY:
                if row['currency'] is not None:raise Invalid('Count metrics must not carry currency')
                if row['value'] is not None and row['value']!=int(row['value']):raise Invalid('Count metrics must be integers')
            if row['asset_id'] is None:
                if row['experiment_id'] is not None or row['pin_id'] is not None or source!='website':
                    raise Invalid('Unattributed rows must be website totals without experiment or Pin IDs')
            else:
                p=by_asset.get(row['asset_id'])
                if not p or p['experiment_id']!=row['experiment_id'] or p['pin_id']!=row['pin_id']:
                    raise Invalid('Metrics do not match a registered publication')
                if row['period']['start']!=p['published_date']:
                    raise Invalid('Import cumulative snapshots beginning on the publication date')
                if source=='website' and (row['attribution_model']!=profile['attribution']['model'] or row['attribution_window']!=profile['attribution']['window']):
                    raise Invalid('Website attribution differs from configured model/window')
            if source!='website' and (row['attribution_model']!='not_applicable' or row['attribution_window']!='not_applicable'):
                raise Invalid('Non-website sources must use not_applicable attribution')
            key=digest({k:row[k] for k in ('asset_id','experiment_id','source','account_id','metric','period','timezone','currency','attribution_model','attribution_window')})
            prior=staged['snapshots'].get(key)
            if prior:
                old_time=datetime.fromisoformat(prior['extracted_at'].replace('Z','+00:00'));new_time=datetime.fromisoformat(row['extracted_at'].replace('Z','+00:00'))
                if new_time<old_time:continue
                if new_time==old_time and prior['value']!=row['value']:raise Invalid('Conflicting values at the same extraction time')
            staged['snapshots'][key]={**row,'import_hash':batch_hash}
        staged['imports'].append(batch_hash)
        snapshot(d,records)
        atomic(path,staged)
        return {'status':'imported','rows':len(staged['snapshots'])}


def report(directory, days=7):
    if days not in (7,14,30):raise Invalid('Checkpoint must be 7, 14 or 30 days')
    with locked(directory) as d:
        run=load_run(d)
        pubs=read(d/'publications.json') if (d/'publications.json').exists() else []
        database=read(d/'results.json') if (d/'results.json').exists() else {'snapshots':{}}
        rows=list(database['snapshots'].values())
        results=[]
        for p in pubs:
            end=(date.fromisoformat(p['published_date'])+timedelta(days=days)).isoformat()
            matching=[r for r in rows if r['asset_id']==p['asset_id'] and r['period']=={'start':p['published_date'],'end':end}]
            counts={metric:next((r['value'] for r in matching if r['metric']==metric),None) for metric in ('impressions','saves','outbound_clicks','sessions','orders')}
            currency_groups={}
            for r in matching:
                if r['metric'] in MONEY:currency_groups.setdefault(r['currency'],{})[r['metric']]=r['value']
            for values in currency_groups.values():
                rev,refund=values.get('revenue'),values.get('refunds')
                values['net_attributed_revenue']=rev-refund if rev is not None and refund is not None else None
            def ratio(n,d):return n/d if n is not None and d is not None and d>0 else None
            results.append({'asset_id':p['asset_id'],'format':p['format'],'period':{'start':p['published_date'],'end':end},
                            'metrics':counts,'outbound_ctr':ratio(counts['outbound_clicks'],counts['impressions']),
                            'purchase_conversion':ratio(counts['orders'],counts['sessions']), 'money_by_currency':currency_groups,
                            'assessment':'insufficient evidence' if not counts['impressions'] or not counts['sessions'] or counts['orders'] is None else 'descriptive result; repeat the experiment before claiming a winner',
                            'attribution':sorted(set((r['attribution_model']+' / '+r['attribution_window']) for r in matching if r['source']=='website'))})
        output={'schema_version':1,'mode':run['mode'],'checkpoint_days':days,'generated_at':now(),'experiments':results,
                'unattributed_snapshots':[r for r in rows if r['asset_id'] is None],
                'comparison':'Same post age only; organic exposure is not randomized. No automatic winner.',
                'next_test':'Repeat the same product/promise with one changed opening; use clicks and attributed purchases to assess it.' if results else 'No published experiments recorded; export a reviewed brief first.',
                'notes':['Windows are start-inclusive/end-exclusive.','Cumulative windows are never added together.','Revenue is not profit. Missing refunds make net revenue unknown.','Currencies remain separate. Missing metrics remain null.']}
        atomic(d/f'results-{days}d.json',output)
        lines=['# Pinterest experiment results','',f"Mode: **{run['mode']}** · Checkpoint: {days} days",'',output['comparison'],'',
               '| Asset | Impressions | Outbound clicks | Sessions | Orders | Assessment |','| --- | --- | --- | --- | --- | --- |']
        for r in results:
            m=r['metrics'];val=lambda k:'unknown' if m[k] is None else str(m[k])
            lines.append(f"| {r['asset_id']} | {val('impressions')} | {val('outbound_clicks')} | {val('sessions')} | {val('orders')} | {r['assessment']} |")
            lines.append('')
        lines+=['',output['next_test'],'']+['- '+x for x in output['notes']]
        for r in results:lines += ['',r['asset_id']+': '+str(r['money_by_currency']), 'Attribution: '+str(r['attribution'])]
        lines+=['',f"Unattributed snapshots retained separately: {len(output['unattributed_snapshots'])}"]
        atomic(d/f'results-{days}d.md','\n'.join(lines)+'\n')
        return output
