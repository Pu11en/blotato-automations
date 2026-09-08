"""Original brief packaging, asset-bound reviews and export-only production requests."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import Request, build_opener
from urllib.error import URLError, HTTPError
from .core import Invalid, now, read, validate, digest, atomic, locked, load_run, identifier, https_url, ROOT
from .adapters import https_opener

CHECKS = ('product_identity','claims','typography','muted_clarity','audio_rights','media_metadata','pacing')


def tracking(url, campaign, content):
    https_url(url)
    p = urlsplit(url)
    values = {'utm_source':'pinterest','utm_medium':'organic_social','utm_campaign':identifier(campaign),'utm_content':identifier(content)}
    query = [(k,v) for k,v in parse_qsl(p.query,keep_blank_values=True) if k.lower() not in values]
    return urlunsplit((p.scheme,p.netloc,p.path,urlencode(query+list(values.items())),p.fragment))


def check_destination(url, allowed_hosts, opener=None):
    p = https_url(url)
    if p.hostname not in allowed_hosts:
        return {'status':'blocked','checked_at':now(),'url':url,'reason':'Host not allowlisted'}
    opener = opener or https_opener()
    try:
        with opener.open(Request(url,headers={'User-Agent':'Cinco-Pinterest-Research/1.0'}), timeout=20) as r:
            content_type = r.headers.get('Content-Type','')
            status = 'verified' if r.status == 200 and 'text/html' in content_type else 'blocked'
            # HTTP validation is separate from human confirmation of product availability.
            return {'status':status,'checked_at':now(),'url':url,'reason':'HTTP page check; confirm product availability during review'}
    except (HTTPError, URLError, TimeoutError, OSError):
        return {'status':'blocked','checked_at':now(),'url':url,'reason':'Destination unavailable or redirected; verify canonical URL'}


def assets_state(profile, asset_ids):
    assets = {x['id']:x for x in profile['assets']}
    states = []
    for key in asset_ids:
        if key not in assets:
            raise Invalid('Unknown product asset')
        asset = deepcopy(assets[key])
        actual = None
        if asset['path']:
            path = Path(asset['path'])
            if not path.is_absolute():
                path = ROOT / path
            if path.is_file():
                actual = digest(path.read_bytes())
        asset['actual_sha256'] = actual
        asset['ready'] = bool(asset['approved'] and asset['rights'] in ('owned','licensed') and asset['rights_evidence'] and actual and actual == asset['sha256'])
        states.append(asset)
    return states


def package(directory, brief_input, check_url=False):
    brief = deepcopy(validate('brief', brief_input))
    identifier(brief['candidate_id'])
    with locked(directory) as d:
        run = load_run(d)
        profile = validate('profile', read(d/'profile.json'))
        candidates = {c['id']:c for c in run['candidates']}
        if brief['candidate_id'] not in candidates or candidates[brief['candidate_id']]['status'] == 'excluded':
            raise Invalid('Select a ranked non-excluded candidate')
        c = candidates[brief['candidate_id']]
        if brief['keyword'] != c['keyword']:
            raise Invalid('Brief keyword must match candidate')
        product = next(x for x in profile['products'] if x['id'] == c['product_id'])
        if not set(brief['asset_ids']) <= set(product['asset_ids']) or not set(brief['claim_ids']) <= set(product['claim_ids']):
            raise Invalid('Claims/assets must belong to the selected product')
        last_end = 0
        for shot in brief['shots']:
            if shot['start'] != last_end or shot['end'] <= shot['start'] or not set(shot['asset_ids']) <= set(brief['asset_ids']):
                raise Invalid('Shots must be contiguous and use declared product assets')
            last_end = shot['end']
        if last_end != brief['duration_seconds']:
            raise Invalid('Storyboard must cover the declared duration')
        key = f"{c['id']}-v{brief['version']}"
        target = d/'briefs'/key
        bound = {'brief':brief,'candidate':c,'profile_hash':digest(profile)}
        content_hash = digest(bound)
        if (target/'brief.json').exists():
            existing = read(target/'brief.json')
            if existing['content_hash'] != content_hash:
                raise Invalid('Brief version is immutable; increment version for changes')
            return existing
        sources = [x for x in run['references'] if x['id'] in c['reference_ids']]
        destination = check_destination(c['destination'],profile['allowed_hosts']) if check_url else {'url':c['destination'],'status':'unverified','checked_at':None,'reason':'Live destination check pending'}
        claims = {x['id']:x for x in profile['claims']}
        if any(x not in claims for x in brief['claim_ids']):
            raise Invalid('Unknown claim')
        pack = {'schema_version':1,'experiment_id':c['id'],'version':brief['version'],'mode':run['mode'],
                'content_hash':content_hash,'brief':brief,'candidate':c,'destination':destination,
                'assets':assets_state(profile,brief['asset_ids']), 'claims':[claims[x] for x in brief['claim_ids']],
                'references':sources, 'profile_hash':digest(profile),
                'variants': [{'asset_id':f"{c['id']}-{fmt}-v{brief['version']}", 'format':fmt,
                'url':tracking(c['destination'],run['run_id'],f"{c['id']}-{fmt}-v{brief['version']}"),
                'width':1000,'height':1500} for fmt in ('static','video')],
                'review_state':'pending', 'paid_calls':0,'publish_calls':0}
        atomic(target/'brief.json',pack)
        atomic(target/'brief.md', markdown(pack))
        return pack


def markdown(pack):
    b=pack['brief']
    lines=[f"# {b['hook']}",'',f"Mode: **{pack['mode']}** · Opportunity: **{pack['candidate']['status']}** · Version {b['version']}",'',
           f"Audience: {b['audience']}",f"Keyword: {b['keyword']}",f"Destination: {pack['destination']['url']} ({pack['destination']['status']})",'',
           '## Static Pin',b['static_layout'],'','## Video',b['script'],'', '| Seconds | Visual | Overlay |','| --- | --- | --- |']
    for s in b['shots']:
        lines.append(f"| {s['start']}–{s['end']} | {s['visual'].replace('|','/')} | {s['overlay'].replace('|','/')} |")
    lines += ['',f"Audio: {b['audio']['choice']} — {b['audio']['direction']}",f"CTA: {b['cta']}",'',
              '## Product assets and claims','Use originals. Image approval is required before animation; final review must verify all spoken and written claims.']
    lines += [f"- Asset {x['id']}: {x['source_url']} — production ready: {x['ready']}" for x in pack['assets']]
    lines += [f"- Claim {x['id']}: {x['text']} — approved: {x['approved']}" for x in pack['claims']]
    lines += ['', '## Creative references (separate from production assets)']
    lines += [f"- {r['source_url']} — {r['rights']} — {r['creator'] or 'creator unknown'}" for r in pack['references']]
    if not pack['references']:lines += ['No reference Pins available; direction is exploratory.']
    lines += ['', '## Tracking links']+[f"- {v['format']}: {v['url']}" for v in pack['variants']]
    lines += ['', 'Status: pending human review. Zero paid generation or publishing calls.']
    return '\n'.join(lines)+'\n'


def current_binding(d, pack):
    profile = validate('profile', read(d/'profile.json'))
    assets = assets_state(profile,pack['brief']['asset_ids'])
    # Include on-disk content, not merely a declared digest.
    return digest({'pack':pack,'profile':profile,'assets':assets}), assets


def review(directory, brief_key, review_input):
    identifier(brief_key)
    with locked(directory) as d:
        path=d/'briefs'/brief_key
        pack=read(path/'brief.json')
        reviewer=review_input.get('reviewer')
        if not isinstance(reviewer,str) or not reviewer.strip() or not review_input.get('evidence'):
            raise Invalid('Review requires a named reviewer and review evidence')
        stage=review_input.get('stage')
        if stage not in ('image','final'):
            raise Invalid('Review stage must be image or final')
        checks=review_input.get('checks',{})
        if set(checks)!=set(CHECKS) or any(type(v) is not bool for v in checks.values()):
            raise Invalid('Review requires explicit booleans for every quality check')
        media=review_input.get('media_path')
        if not media or not Path(media).is_absolute() or not Path(media).is_file():
            raise Invalid('Review requires an existing absolute media path')
        binding,assets=current_binding(d,pack)
        blockers=[]
        if pack['profile_hash'] != digest(read(d/'profile.json')):blockers.append('Profile changed; create a new brief version')
        if not all(x['ready'] for x in assets):blockers.append('Original assets not approved or hash mismatch')
        if not all(x['approved'] for x in pack['claims']):blockers.append('Product facts need approval')
        if pack['brief']['audio']['choice']!='silence' and not pack['brief']['audio']['rights_evidence']:blockers.append('Audio rights evidence missing')
        if not all(checks.values()):blockers.append('Quality review failed')
        if review_input.get('decision')!='approved':blockers.append('Reviewer did not approve')
        if stage=='final':
            image=read(path/'review-image.json') if (path/'review-image.json').exists() else None
            if not valid_review(image,binding):blockers.append('Current image approval missing')
        result={'stage':stage,'decision':'rejected' if blockers else 'approved','blockers':blockers,'reviewer':reviewer,
                'evidence':review_input['evidence'],'checks':checks,'binding':binding,'reviewed_at':now(),
                'media_path':media,'media_sha256':digest(Path(media).read_bytes())}
        atomic(path/('review-'+stage+'.json'),result)
        return result


def valid_review(item,binding):
    if not item or item['decision']!='approved' or item['binding']!=binding:
        return False
    path=Path(item['media_path'])
    return path.is_file() and digest(path.read_bytes())==item['media_sha256']


def export(directory, brief_key, check_url=False):
    identifier(brief_key)
    with locked(directory) as d:
        path=d/'briefs'/brief_key
        pack=read(path/'brief.json')
        profile=read(d/'profile.json')
        binding,assets=current_binding(d,pack)
        destination=check_destination(pack['destination']['url'],profile['allowed_hosts']) if check_url else pack['destination']
        blockers=['Blotato runner handoff and explicit credit budget are required before paid generation',
                  'Publishing is manual and requires an explicitly authorized account']
        if pack['profile_hash'] != digest(profile):blockers.append('Profile changed; create a new brief version')
        if not all(c['approved'] for c in pack['claims']):blockers.append('Product claims require approval')
        for stage in ('image','final'):
            r=read(path/('review-'+stage+'.json')) if (path/('review-'+stage+'.json')).exists() else None
            if not valid_review(r,binding):blockers.append('Current '+stage+' approval missing or invalidated')
        if not all(a['ready'] for a in assets):blockers.append('Original assets need approval or files are missing/changed')
        if destination['status']!='verified':blockers.append('Destination has not passed a live check')
        elif (datetime.now(timezone.utc)-datetime.fromisoformat(destination['checked_at'])).total_seconds()>86400:
            blockers.append('Destination check is older than 24 hours')
        if pack['mode']=='fixture':blockers.append('Fixture output is demonstration-only')
        out={'schema_version':1,'contract':'pinterest-production-request-v1','mode':'export_only','binding':binding,
             'experiment_id':pack['experiment_id'],'brief':pack['brief'],'assets':assets,'claims':pack['claims'],
             'references':pack['references'],'variants':pack['variants'],'destination':destination,
             'image_approval_required_before_animation':True,'credit_ceiling':0,'paid_calls':0,'publish_calls':0,
             'blockers':blockers,'exported_at':now()}
        atomic(path/'production-request.json',out)
        return out
