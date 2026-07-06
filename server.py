#!/usr/bin/env python3
"""Static frontend + SQLite-backed API for the motorsport engineering dashboard."""
import argparse
import hashlib
import html
import json
import mimetypes
import pathlib
import sqlite3
import subprocess
import sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, unquote, urlparse
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
WEB = ROOT / "web"
import os
DATA = pathlib.Path(os.environ.get("F1E_DATA_DIR", ROOT / "data"))
DB = DATA / "motorsport.db"
IMAGE_CACHE = DATA / "image_cache"
MAX_IMAGE_BYTES = 8 * 1024 * 1024
IMAGE_TIMEOUT_SECONDS = 12
_ALLOWED_IMAGE_URLS = None


def ensure_db():
    if DB.exists():
        return
    subprocess.run([sys.executable, str(ROOT / "scripts" / "seed_db.py")], check=True)


def read_payload():
    ensure_db()
    with sqlite3.connect(DB) as conn:
        row = conn.execute(
            "select json from dashboard_payload where id = 'dashboard'"
        ).fetchone()
    if not row:
        raise RuntimeError("dashboard payload not found in SQLite database")
    return json.loads(row[0])


def _is_remote_url(value):
    return isinstance(value, str) and urlparse(value).scheme in {"http", "https"}


def _collect_image_urls(value, urls):
    if isinstance(value, dict):
        for key in ("photo_url", "src_img", "logo_url"):
            candidate = value.get(key)
            if _is_remote_url(candidate):
                urls.add(candidate)
        for child in value.values():
            _collect_image_urls(child, urls)
    elif isinstance(value, list):
        for child in value:
            _collect_image_urls(child, urls)


def allowed_image_urls():
    global _ALLOWED_IMAGE_URLS
    if _ALLOWED_IMAGE_URLS is None:
        urls = set()
        _collect_image_urls(read_payload(), urls)
        _ALLOWED_IMAGE_URLS = urls
    return _ALLOWED_IMAGE_URLS


def cached_image_path(url):
    key = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return IMAGE_CACHE / f"{key}.bin", IMAGE_CACHE / f"{key}.json"


def fetch_image(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 F1EngineerDashboard/2.0",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=IMAGE_TIMEOUT_SECONDS) as resp:
        content_type = (resp.headers.get("Content-Type") or "").split(";", 1)[0].strip()
        data = resp.read(MAX_IMAGE_BYTES + 1)
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError("image is larger than cache limit")
    if content_type and not content_type.startswith("image/"):
        raise ValueError(f"upstream did not return an image: {content_type}")
    return data, content_type or "application/octet-stream"


def read_health():
    ensure_db()
    with sqlite3.connect(DB) as conn:
        generated = conn.execute(
            "select value from metadata where key = 'generated'"
        ).fetchone()
        counts = {
            "series": conn.execute("select count(*) from series").fetchone()[0],
            "teams": conn.execute("select count(*) from teams").fetchone()[0],
            "entries": conn.execute("select count(*) from entries").fetchone()[0],
            "people": conn.execute("select count(*) from people").fetchone()[0],
            "assignments": conn.execute("select count(*) from assignments").fetchone()[0],
            "sources": conn.execute("select count(*) from sources").fetchone()[0],
            "photos": conn.execute("select count(*) from photos where found = 1").fetchone()[0],
            "leadership_photos": conn.execute("select count(*) from photos where found = 1 and person_id like 'leader:%'").fetchone()[0],
            "series_people_photos": conn.execute(
                "select count(*) from photos where found = 1 and (person_id like 'f2:%' or person_id like 'formula-e:%' or person_id like 'wec-le-mans:%')"
            ).fetchone()[0],
            "linkedin_sources": conn.execute("select count(*) from sources where source_type = 'linkedin'").fetchone()[0],
            "profile_lookup_gaps": conn.execute("select count(*) from data_gaps where gap_type = 'public_profile_not_found'").fetchone()[0],
            "series_people_career_entries": conn.execute(
                "select count(*) from career_entries where person_id like 'f2:%' or person_id like 'formula-e:%' or person_id like 'wec-le-mans:%'"
            ).fetchone()[0],
            "data_gaps": conn.execute("select count(*) from data_gaps").fetchone()[0],
            "search_runs": conn.execute("select count(*) from search_runs").fetchone()[0],
            "external_profiles": conn.execute("select count(*) from external_profiles").fetchone()[0],
            "external_profiles_with_photo": conn.execute(
                "select count(*) from external_profiles where photo_url != ''"
            ).fetchone()[0],
            "external_profiles_with_linkedin": conn.execute(
                "select count(*) from external_profiles where linkedin_url != ''"
            ).fetchone()[0],
            "lookup_runs": conn.execute("select count(*) from lookup_runs").fetchone()[0],
        }
        le_mans_classes = dict(
            conn.execute(
                "select class_name, count(*) from entries where series_id = 'wec-le-mans' group by class_name"
            ).fetchall()
        )
        named_by_series = dict(
            conn.execute(
                "select series_id, count(*) from assignments where person_id is not null group by series_id"
            ).fetchall()
        )
    return {
        "ok": True,
        "database": str(DB),
        "generated": generated[0] if generated else None,
        "counts": counts,
        "le_mans_classes": le_mans_classes,
        "named_assignments_by_series": named_by_series,
    }


class Handler(SimpleHTTPRequestHandler):
    server_version = "F1EngineerDashboard/2.0"

    def _json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            try:
                self._json(200, read_health())
            except Exception as exc:
                self._json(500, {"ok": False, "error": str(exc)})
            return
        if parsed.path == "/api/dashboard":
            try:
                self._json(200, read_payload())
            except Exception as exc:
                self._json(500, {"ok": False, "error": str(exc)})
            return
        if parsed.path == "/api/image":
            self._image(parsed)
            return
        super().do_GET()

    def _image(self, parsed):
        query = parse_qs(parsed.query)
        url = (query.get("u") or [""])[0]
        initials = ((query.get("i") or ["?"])[0] or "?")[:4]
        if not _is_remote_url(url) or url not in allowed_image_urls():
            self._json(403, {"ok": False, "error": "image url is not allowed"})
            return

        IMAGE_CACHE.mkdir(parents=True, exist_ok=True)
        img_path, meta_path = cached_image_path(url)
        try:
            if img_path.exists() and meta_path.exists():
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                data = img_path.read_bytes()
                content_type = meta.get("content_type") or "application/octet-stream"
            else:
                data, content_type = fetch_image(url)
                tmp_path = img_path.with_suffix(".tmp")
                tmp_path.write_bytes(data)
                tmp_path.replace(img_path)
                meta_path.write_text(
                    json.dumps({"url": url, "content_type": content_type}, ensure_ascii=False),
                    encoding="utf-8",
                )
        except (OSError, ValueError, urllib.error.URLError, TimeoutError):
            self._image_placeholder(initials)
            return

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _image_placeholder(self, initials):
        label = html.escape(initials.upper())
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96">'
            '<rect width="96" height="96" rx="18" fill="#1c2635"/>'
            f'<text x="48" y="55" text-anchor="middle" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
            f'font-size="24" font-weight="800" fill="#dce5f0">{label}</text>'
            '</svg>'
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "image/svg+xml; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Image-Placeholder", "1")
        self.send_header("Content-Length", str(len(svg)))
        self.end_headers()
        self.wfile.write(svg)

    def translate_path(self, path):
        parsed = urlparse(path)
        rel = unquote(parsed.path).lstrip("/")
        if not rel:
            rel = "index.html"
        target = (WEB / rel).resolve()
        try:
            target.relative_to(WEB.resolve())
        except ValueError:
            return str(WEB / "index.html")
        return str(target)

    def end_headers(self):
        if self.path.startswith("/api/"):
            self.send_header("Access-Control-Allow-Origin", "*")
        else:
            parsed = urlparse(self.path)
            suffix = pathlib.Path(parsed.path).suffix.lower()
            if parsed.path.startswith("/img/") or suffix in {".webp", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico"}:
                self.send_header("Cache-Control", "no-store, max-age=0")
            elif suffix in {".js", ".json", ".html", ""}:
                self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

    def guess_type(self, path):
        if path.endswith(".js"):
            return "application/javascript"
        return mimetypes.guess_type(path)[0] or "application/octet-stream"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    ensure_db()
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"serving {WEB} with API on http://{args.host}:{args.port}", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
