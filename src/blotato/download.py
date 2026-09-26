"""Bounded downloads of generated media.

By the time we download, the credits are already spent, so this has to fail
loudly and quickly rather than hang: a socket timeout, a byte ceiling, and a
filename derived from the URL's *path* (not its query string).
"""
from __future__ import annotations

import urllib.request
from pathlib import Path
from urllib.parse import unquote, urlsplit

USER_AGENT = "blotato-automations/0.1 (+repo:blotato-automations)"
CHUNK_SIZE = 1 << 20
DEFAULT_TIMEOUT = 60.0
DEFAULT_MAX_BYTES = 512 * 1024 * 1024

# Only extensions we are willing to write to disk from a remote URL.
KNOWN_EXTENSIONS = frozenset(
    {".jpg", ".jpeg", ".png", ".webp", ".gif", ".mp4", ".mov", ".webm", ".m4v", ".mp3", ".wav"}
)


class DownloadTooLarge(RuntimeError):
    pass


def extension_for(url: str, *, fallback: str) -> str:
    """The file extension implied by a URL, ignoring any query string.

    ``.../out.jpg?token=abc`` must not produce ``.jpg?token=abc``, and a URL
    with no extension at all (``.../render?id=9``) must not produce an
    extensionless file.
    """
    suffix = Path(unquote(urlsplit(url).path)).suffix.lower()
    return suffix if suffix in KNOWN_EXTENSIONS else fallback


def download(
    url: str,
    dest: Path,
    *,
    timeout: float = DEFAULT_TIMEOUT,
    max_bytes: int = DEFAULT_MAX_BYTES,
) -> int:
    """Stream `url` to `dest`. Returns bytes written.

    Leaves no partial file behind on failure, so a caller that retries does
    not checksum a truncated download.
    """
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"user-agent": USER_AGENT})
    written = 0
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response, dest.open("wb") as handle:
            while True:
                chunk = response.read(CHUNK_SIZE)
                if not chunk:
                    break
                written += len(chunk)
                if written > max_bytes:
                    raise DownloadTooLarge(
                        f"{url} exceeded the {max_bytes}-byte download ceiling"
                    )
                handle.write(chunk)
    except BaseException:
        dest.unlink(missing_ok=True)
        raise
    return written
