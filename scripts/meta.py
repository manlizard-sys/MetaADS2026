"""Shared Meta Graph API helper. Token is read from .env only and never printed."""
import json, os, re, sys, pathlib, requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
API_VERSION = os.environ.get("META_API_VERSION", "v24.0")
GRAPH = f"https://graph.facebook.com/{API_VERSION}"


def _load_token():
    for line in (ROOT / ".env").read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("META_ACCESS_TOKEN="):
            return line.split("=", 1)[1].strip()
    sys.exit("META_ACCESS_TOKEN missing in .env")


TOKEN = _load_token()


def scrub(text):
    text = str(text).replace(TOKEN, "***")
    return re.sub(r"access_token=[^&\s\"']+", "access_token=***", text)


class MetaError(Exception):
    pass


def _handle(r):
    try:
        data = r.json()
    except ValueError:
        raise MetaError(scrub(f"HTTP {r.status_code}: {r.text[:500]}"))
    if "error" in data:
        e = data["error"]
        raise MetaError(scrub(json.dumps({k: e.get(k) for k in (
            "message", "type", "code", "error_subcode", "error_user_title",
            "error_user_msg", "fbtrace_id")}, indent=2)))
    return data


HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def _request(method, url, **kw):
    # Token travels only in the Authorization header; any transport error is scrubbed.
    try:
        return _handle(requests.request(method, url, headers=HEADERS, **kw))
    except requests.RequestException as e:
        raise MetaError(scrub(f"{type(e).__name__}: {e}")) from None


def _url(path):
    return path if path.startswith("https://") else f"{GRAPH}/{path.lstrip('/')}"


def get(path, **params):
    return _request("GET", _url(path), params=params, timeout=60)


def get_all(path, **params):
    out, data = [], get(path, **params)
    while True:
        out.extend(data.get("data", []))
        nxt = data.get("paging", {}).get("next")
        if not nxt:
            return out
        data = _request("GET", nxt, timeout=60)


def post(path, files=None, **params):
    params = {k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in params.items()}
    return _request("POST", _url(path), data=params, files=files, timeout=600)


def save_ids(**kv):
    p = BUILD / "ids.json"
    ids = json.loads(p.read_text()) if p.exists() else {}
    ids.update(kv)
    p.write_text(json.dumps(ids, indent=2))
    return ids
