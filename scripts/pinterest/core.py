"""Validated contracts and crash-safe, serialized local storage."""
import csv
import fcntl
import hashlib
import json
import os
import re
import tempfile
from contextlib import contextmanager
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / 'templates/pinterest/contracts.json'

CHECKER = FormatChecker()

@CHECKER.checks("date-time", raises=(ValueError, TypeError))
def valid_datetime(value):
    if not isinstance(value, str):
        return True
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return "T" in value and parsed.tzinfo is not None

@CHECKER.checks("date", raises=(ValueError, TypeError))
def valid_date(value):
    if not isinstance(value, str):
        return True
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)) and bool(date.fromisoformat(value))

@CHECKER.checks("uri", raises=(ValueError, TypeError))
def valid_uri(value):
    if not isinstance(value, str):
        return True
    return bool(urlparse(value).scheme and urlparse(value).netloc) and not any(c.isspace() for c in value)

class Invalid(ValueError):
    pass


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(value):
    raw = value if isinstance(value, bytes) else json.dumps(value, sort_keys=True, allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def validate(kind, value):
    schema = read(SCHEMAS)
    schema['$ref'] = '#/$defs/' + kind
    errors = sorted(Draft202012Validator(schema, format_checker=CHECKER).iter_errors(value), key=lambda e: str(e.path))
    if errors:
        e = errors[0]
        # Never include submitted values (they may contain credentials/customer details).
        raise Invalid(f'{kind}: invalid field {".".join(map(str, e.path)) or "root"} ({e.validator})')
    return value


def atomic(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = value if isinstance(value, str) else json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n'
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix='.' + path.name, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


@contextmanager
def locked(directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / '.lock').open('a') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield directory
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def load_run(directory):
    return validate('run', read(Path(directory) / 'run.json'))


def save_run(directory, run):
    validate('run', run)
    atomic(Path(directory) / 'run.json', run)


def snapshot(directory, value):
    key = digest(value)
    path = Path(directory) / 'snapshots' / (key + '.json')
    if not path.exists():
        atomic(path, value)
    return key


def identifier(text):
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,95}', text):
        raise Invalid('Invalid identifier')
    return text


def https_url(url):
    p = urlparse(url)
    if p.scheme != 'https' or not p.hostname or p.username or p.password or p.port not in (None, 443):
        raise Invalid('Expected a public HTTPS URL without credentials')
    return p


def pin_id(url):
    p = https_url(url)
    if p.hostname not in ('pinterest.com', 'www.pinterest.com'):
        raise Invalid('Expected a canonical Pinterest Pin URL')
    match = re.fullmatch(r'/pin/(\d+)/?', p.path)
    if not match:
        raise Invalid('Expected a numeric Pinterest Pin ID')
    return match.group(1)


def records(path):
    """CSV rows use JSON for nested cells; JSON input is an array of records."""
    path = Path(path)
    if path.suffix.lower() != '.csv':
        data = read(path)
        if not isinstance(data, list):
            raise Invalid('Import must be an array')
        return data
    with path.open(newline='') as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        for key, value in row.items():
            if value == '':
                row[key] = None
            elif value and (value[0] in '[{' or value in ('null', 'true', 'false') or key in ('schema_version', 'value', 'version')):
                try:
                    row[key] = json.loads(value)
                except ValueError:
                    raise Invalid('Invalid JSON cell in CSV') from None
    return rows
