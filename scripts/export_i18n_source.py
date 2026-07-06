#!/usr/bin/env python3
"""Export translatable data-layer content into shard files for translation agents.

Outputs (data/i18n/work/):
  src_zh.part1.json / part2 / part3   id -> zh text (str) or list[str]
  src_en.json                          id -> en text/list (RE-study pivot: translate en -> target)

Id scheme mirrors web/index.html person ids so overlays bind at runtime:
  series-<seriesId>-<slug(team)>-<slug(name)>-<slug(roleKey)>   series person notes
  f1eng-<teamId>-<slug(person)>-<slug(roleKey)>                 f1 engineering person notes
  <engineer id>                                                 26-person RE study notes
  hl:<id>                                                       highlights list for that person
  role:<key>:<field>                                            trackside role fields
"""
import json, re, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "data" / "i18n" / "work"
WORK.mkdir(parents=True, exist_ok=True)

D = json.loads((ROOT / "web" / "data.json").read_text())


def slug(s):
    # mirror web/index.html slug(): NFKD, strip non [\w\s-], lower, spaces->dash
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = re.sub(r"[^\w\s-]", "", s, flags=re.ASCII)
    s = s.strip().lower()
    s = re.sub(r"\s+", "-", s)
    return s or "person"


def clean(t):
    return re.sub(r"\s+", " ", str(t or "")).strip()


items_zh = {}

# --- series people (compiled + enrichment, mirroring makeSeriesPeople) ---
spc = D.get("series_people_compiled") or D.get("series_people") or {}
enr = D.get("series_people_enrichment") or {}
def pkey(sid, team, name, rk):
    return f"{sid}|{team}|{name}|{rk or ''}"
emap = {pkey(p.get("series_id"), p.get("team_name"), p.get("name"), p.get("role_key")): p
        for p in enr.get("profiles", [])}
umap = {pkey(p.get("series_id"), p.get("team_name"), p.get("name"), p.get("role_key")): p
        for p in enr.get("unresolved", [])}
for sid, sd in (spc.get("series") or {}).items():
    for team in sd.get("teams", []):
        for m in team.get("members", []):
            if m.get("engineering_related") is False:
                continue
            k = pkey(sid, team.get("team_name"), m.get("name"), m.get("role_key"))
            e = emap.get(k, {})
            u = umap.get(k)
            if m.get("notes_zh"):
                parts = [m["notes_zh"]]
            else:
                parts = [e.get("career_summary_zh")]
                parts += [p.get("evidence_zh") for p in (m.get("public_profiles") or e.get("public_profiles") or [])]
                if u:
                    parts.append(u.get("note_zh"))
            text = "\n\n".join(clean(p) for p in parts if clean(p))
            if not text:
                continue
            pid = f"series-{sid}-{slug(team.get('team_name'))}-{slug(m.get('name'))}-{slug(m.get('role_key') or m.get('role'))}"
            items_zh[pid] = text

# --- f1 engineering people ---
fe = D.get("f1_public_engineering_people") or {}
for team_id, people in (fe.get("teams") or {}).items():
    for p in people:
        rk = p.get("role_key") or "engineering-adjacent"
        text = "\n\n".join(clean(x) for x in [p.get("career_summary_zh"), p.get("note_zh")] if clean(x))
        if not text:
            continue
        pid = f"f1eng-{team_id}-{slug(p.get('person'))}-{slug(rk)}"
        items_zh[pid] = text

# --- trackside roles ---
for r in (D.get("trackside_roles") or {}).get("hierarchy", []):
    key = r.get("key") or slug(r.get("title") or "")
    for field in ("summary_zh", "importance_zh", "seniority_zh", "difficulty_zh",
                  "path_position_zh", "difficulty_reason_zh", "typical_progression_zh"):
        v = clean(r.get(field))
        if v:
            items_zh[f"role:{key}:{field[:-3]}"] = v
scope = clean((D.get("trackside_roles") or {}).get("scope_note_zh"))
if scope:
    items_zh["role:_scope:note"] = scope

# --- RE-study 26 engineers: en pivot (notes + highlights) ---
items_en = {}
for e in D.get("engineers", []):
    if e.get("notes"):
        items_en[e["id"]] = clean(e["notes"])
    hl = [clean(x) for x in (e.get("highlights") or []) if clean(x)]
    if hl:
        items_en[f"hl:{e['id']}"] = hl

# --- shard zh into 3 roughly equal parts by char volume ---
entries = sorted(items_zh.items())
total = sum(len(str(v)) for _, v in entries)
target = total / 3
shards, cur, acc = [[], [], []], 0, 0
for k, v in entries:
    shards[cur].append((k, v))
    acc += len(str(v))
    if acc > target and cur < 2:
        cur += 1
        acc = 0
for i, sh in enumerate(shards, 1):
    p = WORK / f"src_zh.part{i}.json"
    p.write_text(json.dumps(dict(sh), ensure_ascii=False, indent=1))
    print(f"{p.name}: {len(sh)} items, {sum(len(str(v)) for _, v in sh)} chars")
(WORK / "src_en.json").write_text(json.dumps(items_en, ensure_ascii=False, indent=1))
print(f"src_en.json: {len(items_en)} items, {sum(len(str(v)) for v in items_en.values())} chars")
