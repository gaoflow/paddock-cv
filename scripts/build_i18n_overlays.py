#!/usr/bin/env python3
"""Merge translated content parts into per-locale overlay files served to the frontend.

Input : data/i18n/content/<locale>/part*.json   (flat id -> translated text/list)
Output: web/i18n/<locale>.json                  {persons:{id:{notes,highlights}}, roles:{key:{field:txt}}, scope_note}

Id conventions (see scripts/export_i18n_source.py):
  role:<key>:<field>  -> roles[key][field]
  role:_scope:note    -> scope_note
  hl:<person-id>      -> persons[id].highlights (list)
  <person-id>         -> persons[id].notes
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "i18n" / "content"
OUT = ROOT / "web" / "i18n"
OUT.mkdir(parents=True, exist_ok=True)

if not SRC.exists():
    print("no i18n content yet; nothing to do")
    raise SystemExit(0)

for locdir in sorted(SRC.iterdir()):
    if not locdir.is_dir():
        continue
    locale = locdir.name
    flat = {}
    for part in sorted(locdir.glob("part*.json")):
        try:
            flat.update(json.loads(part.read_text()))
        except Exception as err:  # a bad part must not kill the build
            print(f"WARN {part}: {err}")
    if not flat:
        continue
    overlay = {"persons": {}, "roles": {}, "scope_note": ""}
    for k, v in flat.items():
        if k == "role:_scope:note":
            overlay["scope_note"] = v
        elif k.startswith("role:"):
            _, key, field = k.split(":", 2)
            overlay["roles"].setdefault(key, {})[field] = v
        elif k.startswith("hl:"):
            pid = k[3:]
            overlay["persons"].setdefault(pid, {})["highlights"] = v if isinstance(v, list) else [v]
        else:
            overlay["persons"].setdefault(k, {})["notes"] = v
    out = OUT / f"{locale}.json"
    out.write_text(json.dumps(overlay, ensure_ascii=False, separators=(",", ":")))
    print(f"{out.relative_to(ROOT)}: {len(overlay['persons'])} persons, {len(overlay['roles'])} roles, {out.stat().st_size//1024}KB")
