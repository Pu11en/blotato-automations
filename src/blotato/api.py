"""Blotato HTTP client using only the standard library.

Only the endpoints this skill actually uses. All logging and persistence
must run responses through blotato_run.sanitize before writing them.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Optional

BASE_URL = "https://backend.blotato.com"
API_KEY_HEADER = "blotato-api-key"
USER_AGENT = "blotato-brand-content/0.1 (+repo:blotato-automations)"


class BlotatoHttpError(RuntimeError):
    def __init__(self, status: int, body: Any, req_id: Optional[str] = None):
        super().__init__(f"blotato http {status}: {body!r}")
        self.status = status
        self.body = body
        self.req_id = req_id


def _request(
    method: str,
    path: str,
    *,
    api_key: str,
    body: Optional[dict] = None,
    timeout: float = 30.0,
) -> dict:
    url = f"{BASE_URL}{path}"
    data: Optional[bytes] = None
    headers = {
        API_KEY_HEADER: api_key,
        "user-agent": USER_AGENT,
        "accept": "application/json",
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["content-type"] = "application/json"

    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            payload = json.loads(raw)
        except Exception:
            payload = raw.decode("utf-8", errors="replace")
        raise BlotatoHttpError(e.code, payload, getattr(payload, "get", lambda k: None)("reqId") if isinstance(payload, dict) else None) from None
    if not raw:
        return {}
    return json.loads(raw)


def get_credits(api_key: str) -> dict:
    return _request("GET", "/v2/credits", api_key=api_key)


def list_templates(api_key: str) -> dict:
    return _request(
        "GET", "/v2/videos/templates?fields=id,name,description,inputs", api_key=api_key
    )


def upload_media(api_key: str, public_url: str) -> dict:
    """POST /v2/media -> returns a hosted media URL usable in template inputs."""
    return _request("POST", "/v2/media", api_key=api_key, body={"url": public_url})


def create_presigned_upload(api_key: str, filename: str) -> dict:
    return _request(
        "POST", "/v2/media/uploads", api_key=api_key, body={"filename": filename}
    )


def put_file_to_presigned_url(presigned_url: str, path, content_type: str) -> None:
    with open(path, "rb") as handle:
        data = handle.read()
    req = urllib.request.Request(
        presigned_url,
        data=data,
        method="PUT",
        headers={"content-type": content_type, "user-agent": USER_AGENT},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        resp.read()


def create_video_from_template(
    api_key: str,
    *,
    template_id: str,
    inputs: dict,
    title: Optional[str] = None,
    render: bool = True,
) -> dict:
    body: dict = {"templateId": template_id, "inputs": inputs, "render": render}
    if title:
        body["title"] = title
    return _request("POST", "/v2/videos/from-templates", api_key=api_key, body=body)


def get_video_creation(api_key: str, video_id: str) -> dict:
    return _request("GET", f"/v2/videos/creations/{video_id}", api_key=api_key)


def delete_video(api_key: str, video_id: str) -> dict:
    return _request("DELETE", f"/v2/videos/{video_id}", api_key=api_key)
