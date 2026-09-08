"""Bounded GET-only adapters; errors never contain response bodies or credentials."""
import json
import os
import re
import shutil
import ssl
import certifi
import subprocess
import time
from datetime import date, datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, build_opener, HTTPRedirectHandler, HTTPSHandler
from .core import Invalid, now, digest, validate, https_url, pin_id, read, ROOT

class Unavailable(RuntimeError):
    pass

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def https_opener():
    # Use an explicit, pinned CA bundle rather than a missing macOS Python store.
    return build_opener(NoRedirect(), HTTPSHandler(context=ssl.create_default_context(cafile=certifi.where())))


def get_json(url, token, opener=None, sleep=time.sleep):
    # Fixed provider only: never forward an OAuth token to another host or redirect.
    if https_url(url).hostname != 'api.pinterest.com':
        raise Invalid('Unexpected API hostname')
    opener = opener or https_opener()
    for attempt in range(3):
        try:
            with opener.open(Request(url, headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/json'}), timeout=20) as r:
                raw = r.read(2_000_001)
                if len(raw) > 2_000_000:
                    raise Unavailable('Response exceeded size limit')
                return json.loads(raw)
        except HTTPError as e:
            if e.code in (401, 403):
                raise Unavailable(f'API access unavailable (HTTP {e.code})') from None
            if e.code == 429 or 500 <= e.code < 600:
                wait = e.headers.get('Retry-After', '')
                try:
                    delay = float(wait) if wait.isdigit() else max(0, (parsedate_to_datetime(wait)-datetime.now(timezone.utc)).total_seconds()) if wait else 2 ** attempt
                except (ValueError, TypeError, OverflowError):
                    delay = 2 ** attempt
                if attempt < 2 and delay <= 30:
                    sleep(delay)
                    continue
            raise Unavailable(f'API unavailable (HTTP {e.code})') from None
        except (URLError, TimeoutError, OSError, ValueError):
            raise Unavailable('Network or response decoding unavailable') from None


def trends(raw, region, query, source_url, mode='live'):
    if not isinstance(raw, dict) or not isinstance(raw.get('trends'), list):
        raise Unavailable('Unsupported Trends response; use manual evidence import')
    output = []
    for item in raw['trends']:
        if not isinstance(item, dict) or not isinstance(item.get('keyword'), str):
            raise Unavailable('Unsupported Trends item')
        series = item.get('time_series') or {}
        if not isinstance(series, dict):
            raise Unavailable('Unsupported Trends time series')
        # Official TimeSeries is date-keyed; validate rather than silently dropping fields.
        dates = sorted(series)
        today = date.today().isoformat()
        signal = {'schema_version':1, 'id': 'trend-' + digest([region, item['keyword'], raw])[:16],
                  'source_url':source_url, 'source_type':'pinterest_trends', 'retrieved_at':now(),
                  'mode':mode, 'region':region, 'query':item['keyword'],
                  'observation_period': {'start':dates[0] if dates else today, 'end':dates[-1] if dates else today},
                  'metric_definition':'Weekly relative search index, per-keyword normalization; growth is provider percent change. 10001 means greater than 10000%. Dates are week-ending dates. Requested filter: ' + query,
                  'unit':'normalized_index_0_100', 'normalization':'per_keyword', 'time_series':series,
                  'growth':{x:item.get('pct_growth_' + x) for x in ('wow','mom','yoy')},
                  'availability':'available', 'snapshot_hash':digest(raw)}
        try:
            validate('signal', signal)
        except Invalid:
            raise Unavailable('Unsupported Trends values; use manual evidence import') from None
        output.append(signal)
    return output


def fetch_trends(region, query):
    if region != 'US':
        raise Unavailable('Only US is verified against the pinned schema; use manual import for other regions')
    token = os.getenv('PINTEREST_ACCESS_TOKEN')
    if not token:
        raise Unavailable('PINTEREST_ACCESS_TOKEN not configured; manual import available')
    url = 'https://api.pinterest.com/v5/trends/keywords/US/top/growing?' + urlencode({'include_keywords':query, 'limit':10, 'normalize_against_group':'false'})
    raw = get_json(url, token)
    return raw, trends(raw, region, query, url)


def opencli(operation, argument, limit=10, runner=subprocess.run, sleep=time.sleep):
    if operation not in ('search-pins', 'pin', 'board-pins'):
        raise Invalid('Only read-only Pin search/detail/board operations are allowed')
    if not isinstance(argument, str) or not argument.strip() or argument.startswith('-') or len(argument) > 200:
        raise Invalid('Invalid collector argument')
    if operation == 'pin' and not re.fullmatch(r'\d+', argument):
        raise Invalid('Pin detail requires a numeric ID')
    if not 1 <= limit <= 10:
        raise Invalid('Pilot limit must be 1–10')
    binary = os.getenv('PINTEREST_OPENCLI_BIN') or shutil.which('opencli')
    if not binary:
        raise Unavailable('OpenCLI not installed; manual reference import available')
    args = [binary, 'pinterest', operation, argument, '-f', 'json']
    if operation != 'pin':
        args += ['--limit', str(limit)]
    for attempt in range(3):
        try:
            result = runner(args, capture_output=True, text=True, timeout=45)
        except (OSError, subprocess.TimeoutExpired):
            raise Unavailable('OpenCLI unavailable or timed out') from None
        if result.returncode:
            error = result.stderr.lower()
            if ('429' in error or 'rate limit' in error) and attempt < 2:
                sleep(2 ** attempt)
                continue
            raise Unavailable('OpenCLI read failed; check browser bridge and access locally')
        try:
            data = json.loads(result.stdout)
            if not isinstance(data, list):
                raise ValueError()
            return data[:limit]
        except ValueError:
            raise Unavailable('Unsupported OpenCLI JSON response') from None


def references(raw, query, mode='live'):
    output = []
    for row in raw:
        if not isinstance(row, dict) or not isinstance(row.get('pinId'), str) or not row['pinId'].isdigit():
            raise Unavailable('Unsupported OpenCLI Pin record')
        url = 'https://www.pinterest.com/pin/' + row['pinId'] + '/'
        item = {'schema_version':1,'id':row['pinId'],'source_url':url,'creator':row.get('pinner') or None,
                'destination':row.get('link') or None,'retrieved_at':now(),'mode':mode,'queries':[query],
                'title':row.get('title') or '', 'observations':[], 'media_url':row.get('imageUrl') or None,
                'rights':'reference_only','rights_evidence':None,'snapshot_hash':digest(raw)}
        try:
            validate('reference', item)
        except Invalid:
            raise Unavailable('Unsupported OpenCLI metadata') from None
        output.append(item)
    return output


def doctor():
    binary = os.getenv('PINTEREST_OPENCLI_BIN') or shutil.which('opencli')
    return {'checked_at':now(), 'opencli': {'status':'unverified' if binary else 'unavailable',
            'reason':'Browser connection needs a live read test' if binary else 'Not installed'},
            'pinterest_trends':{'status':'unverified' if os.getenv('PINTEREST_ACCESS_TOKEN') else 'unavailable',
            'reason':'Entitlement needs a live read test' if os.getenv('PINTEREST_ACCESS_TOKEN') else 'Token not configured'},
            'manual_import':'available', 'paid_calls':0,'publish_calls':0,
            'dependencies':read(ROOT / 'templates/pinterest/dependencies.json')}
