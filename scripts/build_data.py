#!/usr/bin/env python3
"""Consolidate per-team research JSON + Chinese i18n overlays into one dataset.

Reads:
  data/teams_2026.json        team order + colours
  data/research/<team>.json   the fan-out research output (English)
  data/i18n/<team>.zh.json    Chinese translation overlays (keyed by engineer id)
  data/i18n/glossary.json     canonical zh names for teams/drivers/archetypes/etc.

Emits web/data.json (+ web/data.js) with bilingual fields the dashboard renders:
people/team/driver/org/institution names are kept English + zh; all other display
text uses zh fields (falling back to English when a translation is missing).
"""
import datetime
import difflib
import json
import os
import pathlib
import copy
import re
import unicodedata
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
# Data directory is swappable so the public repo can run on sample fixtures:
#   F1E_DATA_DIR=data/sample python3 scripts/build_data.py
DATA = pathlib.Path(os.environ.get("F1E_DATA_DIR", ROOT / "data"))
RESEARCH = DATA / "research"
I18N = DATA / "i18n"
TEAMS_FILE = DATA / "teams_2026.json"
GLOSS = json.loads((I18N / "glossary.json").read_text())
TEAM_LOGOS_FILE = DATA / "team_logos.json"
TEAM_LOGOS = json.loads(TEAM_LOGOS_FILE.read_text()) if TEAM_LOGOS_FILE.exists() else {}
ROLES_FILE = DATA / "trackside_roles.json"
ROLES = json.loads(ROLES_FILE.read_text()) if ROLES_FILE.exists() else {}
SERIES_FILE = DATA / "series_engineering.json"
SERIES = json.loads(SERIES_FILE.read_text()) if SERIES_FILE.exists() else {}
F1_ROLE_TAXONOMY_FILE = DATA / "f1_role_taxonomy.json"
F1_ROLE_TAXONOMY = json.loads(F1_ROLE_TAXONOMY_FILE.read_text()) if F1_ROLE_TAXONOMY_FILE.exists() else {}
if F1_ROLE_TAXONOMY.get("role_templates"):
    SERIES.setdefault("f1_team_engineering", {})["role_templates"] = F1_ROLE_TAXONOMY["role_templates"]
    for series in SERIES.get("motorsport_series", []):
        if series.get("id") == "f1":
            series["role_ladder"] = [role["key"] for role in F1_ROLE_TAXONOMY["role_templates"]]
PHOTOS_FILE = DATA / "photos_merged.json"
PHOTOS = json.loads(PHOTOS_FILE.read_text()) if PHOTOS_FILE.exists() else {}
AGES_FILE = DATA / "ages.json"
AGES = json.loads(AGES_FILE.read_text()) if AGES_FILE.exists() else {}
SERIES_PEOPLE_FILE = DATA / "series_people.json"
SERIES_PEOPLE = json.loads(SERIES_PEOPLE_FILE.read_text()) if SERIES_PEOPLE_FILE.exists() else {}
SERIES_PEOPLE_ENRICHMENT_FILE = DATA / "series_people_enrichment.json"
SERIES_PEOPLE_ENRICHMENT = json.loads(SERIES_PEOPLE_ENRICHMENT_FILE.read_text()) if SERIES_PEOPLE_ENRICHMENT_FILE.exists() else {}
SERIES_ROSTERS_FILE = DATA / "series_rosters.json"
SERIES_ROSTERS = json.loads(SERIES_ROSTERS_FILE.read_text()) if SERIES_ROSTERS_FILE.exists() else {}
LEADER_PROFILES_FILE = DATA / "leader_profiles.json"
LEADER_PROFILES = json.loads(LEADER_PROFILES_FILE.read_text()) if LEADER_PROFILES_FILE.exists() else {}
LE_MANS_ENTRIES_FILE = DATA / "wec_le_mans_entries_2026.json"
LE_MANS_ENTRIES = json.loads(LE_MANS_ENTRIES_FILE.read_text()) if LE_MANS_ENTRIES_FILE.exists() else {}
F1_PUBLIC_ENGINEERING_FILE = DATA / "f1_public_engineering_people.json"
F1_PUBLIC_ENGINEERING = json.loads(F1_PUBLIC_ENGINEERING_FILE.read_text()) if F1_PUBLIC_ENGINEERING_FILE.exists() else {}
F1_PUBLIC_ENGINEERING_EXPANSION_FILE = DATA / "f1_public_engineering_people_expansion.json"
F1_PUBLIC_ENGINEERING_EXPANSION = json.loads(F1_PUBLIC_ENGINEERING_EXPANSION_FILE.read_text()) if F1_PUBLIC_ENGINEERING_EXPANSION_FILE.exists() else {}
for team_id, people in F1_PUBLIC_ENGINEERING_EXPANSION.get("teams", {}).items():
    F1_PUBLIC_ENGINEERING.setdefault("teams", {}).setdefault(team_id, []).extend(people)
CURRENT_YEAR = datetime.date.today().year
OUT = ROOT / "web" / "data.json"


def get_birth_year(eid):
    rec = AGES.get(eid)
    if not rec:
        return None
    if rec.get("dob"):
        return datetime.date.fromisoformat(rec["dob"]).year
    if rec.get("birth_year"):
        return int(rec["birth_year"])
    return None


def compute_age(eid):
    """Return current year minus birth year, plus the source approximation flag."""
    year = get_birth_year(eid)
    if year is None:
        return None, False
    return CURRENT_YEAR - year, bool(AGES[eid].get("approx", "dob" not in AGES[eid]))

teams_meta = json.loads(TEAMS_FILE.read_text())


def _norm(s):
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower().strip()


_SENT_RUN = re.compile(r"[。！？；!?;](?:\s*[。！？；!?;])+")
_SPACE_BEFORE_MARK = re.compile(r"\s+([。！？；，、])")
_CLAUSE_SPLIT = re.compile(r"[。！？；，、,.!?;:：]+")


def clean_zh(text):
    """Tidy a Chinese note: collapse repeated sentence punctuation and stray spaces.

    Fixes the doubled-period bug ("。。") that appears when note fragments that
    already end in a sentence mark are concatenated with another mark.
    """
    if not text:
        return ""
    s = re.sub(r"\s+", " ", str(text)).strip()
    s = _SENT_RUN.sub(lambda m: m.group(0).strip()[-1], s)
    s = _SPACE_BEFORE_MARK.sub(r"\1", s)
    return s.strip()


def _note_norm(text):
    return "".join(
        ch.lower()
        for ch in unicodedata.normalize("NFKC", text or "")
        if ch.isalnum()
    )


def _note_clauses(text):
    clauses = []
    for clause in _CLAUSE_SPLIT.split(text or ""):
        norm = _note_norm(clause)
        if len(norm) >= 8:
            clauses.append(norm)
    return clauses


def _same_note_clause(a, b):
    if not a or not b:
        return False
    if a in b or b in a:
        return True
    if min(len(a), len(b)) < 12:
        return False
    return difflib.SequenceMatcher(None, a, b).ratio() >= 0.86


def _redundant_note(candidate, existing_notes):
    candidate_norm = _note_norm(candidate)
    existing_norms = [_note_norm(note) for note in existing_notes]
    if candidate_norm and any(candidate_norm in norm for norm in existing_norms):
        return True

    candidate_clauses = _note_clauses(candidate)
    if not candidate_clauses:
        return False
    existing_clauses = [
        clause
        for note in existing_notes
        for clause in _note_clauses(note)
    ]
    return all(
        any(_same_note_clause(candidate_clause, existing_clause) for existing_clause in existing_clauses)
        for candidate_clause in candidate_clauses
    )


def join_zh(parts):
    """Join note fragments into one clean string with single sentence breaks."""
    cleaned = []
    seen = set()
    for p in parts:
        p = clean_zh(p)
        if not p:
            continue
        if p[-1] not in "。！？!?；;":
            p += "。"
        if p in seen or _redundant_note(p, cleaned):
            continue
        seen.add(p)
        cleaned.append(p)
    return clean_zh("".join(cleaned))


LAST_CHECKED = "2026-06-22"  # date the external-profile lookups were last refreshed


def _linkedin_from(urls):
    for u in urls:
        if u and "linkedin.com" in u:
            return u
    return ""


def _photo_url_of(photo):
    if isinstance(photo, dict):
        return photo.get("src_img") or photo.get("local") or ""
    return ""


def build_external_profiles(teams_out, flat, series_people_compiled):
    """Consolidate one queryable external-profile row per public person.

    Pulls LinkedIn URL, photo, education/career counts and lookup status from
    every people source (F1 race engineers, leaders, F1 engineering staff, and
    other-series people) so downstream analysis queries the DB, not the web.
    """
    team_name = {t["id"]: t["name"] for t in teams_out}
    leader_team = {}
    for g in SERIES.get("f1_team_engineering", {}).get("teams", []):
        for l in g.get("leadership", []):
            leader_team[l.get("person")] = g.get("team_id")

    profiles = []

    def add(name, category, series_id, team, role, link_urls, photo, edu, career_len, lookup, extra_srcs=(), role_zh=""):
        edu_srcs = [e.get("source_url") for e in (edu or []) if e.get("source_url")]
        all_srcs = [u for u in list(link_urls) + list(extra_srcs) + edu_srcs if u]
        profiles.append({
            "name": name, "category": category, "series_id": series_id,
            "team": team, "role": role, "role_zh": role_zh or role,
            "linkedin_url": _linkedin_from(all_srcs),
            "relatedin_url": "",  # relatedin.com is Cloudflare-gated, unusable
            "photo_url": _photo_url_of(photo) if isinstance(photo, dict) else (photo or ""),
            "photo_status": "confirmed" if (photo) else "searched_no_confirmed_photo",
            "education_status": lookup or ("profile_found" if edu else "not_researched"),
            "education_count": len(edu or []),
            "career_count": career_len,
            "source_urls": sorted(set(all_srcs)),
            "last_checked": LAST_CHECKED,
        })

    for e in flat:
        srcs = [s.get("url") for s in e.get("sources", []) if s.get("url")]
        add(e["name"], "f1-race-engineer", "f1", team_name.get(e.get("team_id"), ""),
            e.get("role") or e.get("role_zh", ""), srcs, e.get("photo"),
            e.get("education"), len(e.get("career", [])), None,
            role_zh=e.get("role_zh", ""))

    for name, p in LEADER_PROFILES.get("people", {}).items():
        src = [p.get("source_url")] if p.get("source_url") else []
        add(name, "f1-leader", "f1", team_name.get(leader_team.get(name), ""),
            "管理 / 技术领导", src, p.get("photo_url"), p.get("education"), 0,
            p.get("education_lookup"))

    for tid, ppl in F1_PUBLIC_ENGINEERING.get("teams", {}).items():
        for p in ppl:
            srcs = [s.get("url") for s in p.get("sources", []) if s.get("url")]
            add(p.get("person"), "f1-engineering", "f1", team_name.get(tid, ""),
                p.get("role") or p.get("role_zh", ""), srcs, p.get("photo_url"),
                p.get("education"), len(p.get("career", [])), p.get("education_lookup"),
                role_zh=p.get("role_zh", ""))

    for sid, sd in (series_people_compiled.get("series") or {}).items():
        for team in sd.get("teams", []):
            for m in team.get("members", []):
                if m.get("engineering_related") is False:
                    continue
                pp_urls = [p.get("url") for p in m.get("public_profiles", []) if p.get("url")]
                srcs = [s.get("url") for s in m.get("sources", []) if s.get("url")]
                add(m.get("name"), "series-person", sid, team.get("team_name", ""),
                    m.get("role", "") or m.get("role_group_zh", ""), pp_urls + srcs,
                    m.get("photo"), m.get("education"), len(m.get("career", [])),
                    m.get("profile_lookup_status"), role_zh=m.get("role_group_zh", ""))

    return profiles


PAIRING_STATUS = {
    (s.get("engineer_id"), _norm(s.get("driver"))): s
    for s in SERIES.get("driver_pairing_status", [])
}
DRIVER_NORM = {_norm(k): v for k, v in GLOSS["drivers"].items()}


def gd(name):  # driver English -> Chinese, accent-insensitive
    return GLOSS["drivers"].get(name) or DRIVER_NORM.get(_norm(name), "")


def _key_part(value):
    return re.sub(r"\s+", " ", _norm(value).replace("-", " ")).strip()


def profile_key(series_id, team_name, name, role_key=""):
    return (_key_part(series_id), _key_part(team_name), _key_part(name), _key_part(role_key))


def compile_series_people(raw, enrichment, series_catalog):
    compiled = copy.deepcopy(raw or {})
    series_by_id = {s.get("id"): s for s in series_catalog or []}
    enriched_by_key = {
        profile_key(p.get("series_id"), p.get("team_name"), p.get("name"), p.get("role_key")): p
        for p in (enrichment or {}).get("profiles", [])
    }
    unresolved_by_key = {
        profile_key(p.get("series_id"), p.get("team_name"), p.get("name"), p.get("role_key")): p
        for p in (enrichment or {}).get("unresolved", [])
    }
    stats = {"named_people": 0, "career_compiled": 0, "profile_found": 0, "profile_gaps": 0}
    for series_id, series_data in (compiled.get("series") or {}).items():
        series_meta = series_by_id.get(series_id, {})
        series_name = series_meta.get("name") or series_id
        series_zh = series_meta.get("name_zh") or series_name
        for team in series_data.get("teams", []):
            official_source = {
                "url": team.get("source_url"),
                "title": team.get("source_title") or team.get("source_url"),
                "type": "official",
            } if team.get("source_url") else None
            for member in team.get("members", []):
                role_key = member.get("role_key") or _key_part(member.get("role"))
                member["role_en"] = member.get("role_en") or member.get("role", "")
                key = profile_key(series_id, team.get("team_name"), member.get("name"), role_key)
                enriched = enriched_by_key.get(key, {})
                unresolved = unresolved_by_key.get(key, {})
                member_photo = member.get("photo") if isinstance(member.get("photo"), dict) else {}
                enriched_photo = enriched.get("photo") if isinstance(enriched.get("photo"), dict) else {}
                if enriched_photo and not member_photo.get("local"):
                    member["photo"] = enriched.get("photo")
                stats["named_people"] += 1
                public_profiles = enriched.get("public_profiles", [])
                if public_profiles:
                    stats["profile_found"] += 1
                if unresolved:
                    stats["profile_gaps"] += 1

                official_role = {
                    "from": "2026",
                    "to": "present",
                    "org": team.get("team_name", ""),
                    "org_zh": team.get("team_name", ""),
                    "role": member.get("role", ""),
                    "role_zh": f"当前岗位：{member.get('role_group_zh') or member.get('role') or '岗位'}。",
                    "category": series_name,
                    "category_zh": series_zh,
                    "source_type": "official_team_page",
                }
                entries = []
                for item in enriched.get("career_entries", []):
                    row = dict(item)
                    row.setdefault("org_zh", row.get("org", ""))
                    row.setdefault("category_zh", series_zh)
                    row.setdefault("source_type", "public_profile")
                    entries.append(row)
                if entries:
                    # use the real (LinkedIn-sourced) ladder; keep a current-role anchor
                    # only if the sourced ladder doesn't already cover the present role.
                    has_current = any(
                        str(r.get("to", "")).lower() in ("present", "current", "2026", "now", "至今", "现在")
                        for r in entries
                    )
                    career = entries if has_current else [official_role] + entries
                else:
                    career = [official_role]
                member["career"] = career
                stats["career_compiled"] += 1

                education = []
                for item in enriched.get("education_entries", []):
                    row = dict(item)
                    row.setdefault("institution_zh", row.get("institution", ""))
                    row.setdefault("degree_zh", row.get("degree", ""))
                    row.setdefault("field_zh", row.get("field", ""))
                    education.append(row)
                member["education"] = education

                profile_sources = [
                    {"url": p.get("url"), "title": p.get("title") or p.get("url"), "type": p.get("type") or "profile"}
                    for p in public_profiles
                    if p.get("url")
                ]
                notes = [
                    member.get("notes_zh"),
                    enriched.get("career_summary_zh"),
                    *(p.get("evidence_zh") for p in public_profiles if p.get("evidence_zh")),
                    unresolved.get("note_zh"),
                ]
                if not any(notes):
                    notes.append("已记录当前岗位；详细履历待补充。")
                member["public_profiles"] = public_profiles
                member["profile_lookup_status"] = (
                    "no_trusted_result" if unresolved else "profile_found" if public_profiles else "not_enriched_yet"
                )
                member["profile_lookup_note_zh"] = unresolved.get("note_zh", "")
                first_note = next((n for n in notes if n), "")
                member["career_summary_zh"] = clean_zh(
                    enriched.get("career_summary_zh") or member.get("career_summary_zh") or first_note
                )
                member["notes_zh"] = join_zh(notes)
                member["sources"] = ([official_source] if official_source else []) + profile_sources
                member["career_detail_level"] = "enriched_public_profile" if public_profiles else "official_current_role"
    compiled["profile_pipeline_stats"] = stats
    compiled["enrichment_method_zh"] = (enrichment or {}).get("method_zh", "")
    return compiled


SERIES_PEOPLE_COMPILED = compile_series_people(
    SERIES_PEOPLE,
    SERIES_PEOPLE_ENRICHMENT,
    SERIES.get("motorsport_series", []),
)


teams_out, flat = [], []
for t in teams_meta["teams"]:
    tid = t["id"]
    rf = RESEARCH / f"{tid}.json"
    zf = I18N / f"{tid}.zh.json"

    team_zh = GLOSS["teams"].get(t["name"], "")
    team_notes_zh = ""
    zmap = {}
    if zf.exists():
        zd = json.loads(zf.read_text())
        team_zh = zd.get("team_zh") or team_zh
        team_notes_zh = clean_zh(zd.get("team_notes_zh", ""))
        zmap = zd.get("engineers", {})

    engineers, team_notes = [], ""
    if rf.exists():
        rd = json.loads(rf.read_text())
        engineers = rd.get("engineers", [])
        team_notes = rd.get("team_notes", "")

    drivers, drivers_zh = [], []
    for e in engineers:
        e["team_id"] = tid
        e["team_color"] = t["color"]
        e["team_zh"] = team_zh
        e["photo"] = PHOTOS.get(e["id"])
        e["birth_year"] = get_birth_year(e["id"])
        e["age"], e["age_approx"] = compute_age(e["id"])

        a = e.get("route_archetype", "unknown")
        e["archetype_label_zh"] = GLOSS["archetypes"].get(a, a)
        e["archetype_desc_zh"] = GLOSS["archetype_desc"].get(a, "")
        e["confidence_zh"] = GLOSS["confidence"].get(e.get("confidence", ""), e.get("confidence", ""))
        e["drivers_zh"] = [gd(d) for d in e.get("drivers_2026", [])]
        statuses = []
        for d in e.get("drivers_2026", []):
            s = PAIRING_STATUS.get((e["id"], _norm(d)))
            if s:
                statuses.append(s)
        if statuses:
            e["pairing_status"] = statuses[0].get("status", "")
            e["pairing_status_zh"] = statuses[0].get("status_zh", "")
            e["pairing_status_certainty"] = statuses[0].get("certainty", "")
            e["pairing_note_zh"] = statuses[0].get("note_zh", "")

        z = zmap.get(e["id"], {})
        e["name_zh"] = z.get("name_zh", "")
        e["role_zh"] = z.get("role_zh", "")
        e["nationality_zh"] = z.get("nationality_zh", "")
        e["highlights_zh"] = [clean_zh(h) for h in z.get("highlights_zh", []) if clean_zh(h)]
        e["notes_zh"] = clean_zh(z.get("notes_zh", ""))

        edu_zh = z.get("education_zh", [])
        for i, ed in enumerate(e.get("education", [])):
            zz = edu_zh[i] if i < len(edu_zh) else {}
            ed["institution_zh"] = zz.get("institution_zh", "")
            ed["degree_zh"] = zz.get("degree_zh", "")
            ed["field_zh"] = zz.get("field_zh", "")

        car_zh = z.get("career_zh", [])
        for i, c in enumerate(e.get("career", [])):
            zz = car_zh[i] if i < len(car_zh) else {}
            c["org_zh"] = zz.get("org_zh", "")
            c["role_zh"] = zz.get("role_zh", "")
            c["category_zh"] = zz.get("category_zh") or GLOSS["categories"].get(c.get("category", ""), c.get("category", ""))

        for d in e.get("drivers_2026", []):
            if d not in drivers:
                drivers.append(d)
                drivers_zh.append(gd(d))
        flat.append(e)

    logo_light_list = TEAM_LOGOS.get("light_bg")
    logo_invert_list = TEAM_LOGOS.get("invert_on_dark") or []
    logo_url = (TEAM_LOGOS.get("teams") or {}).get(tid, "")
    logo_light = (tid in logo_light_list) if logo_light_list is not None else bool(logo_url)
    teams_out.append({
        "id": tid, "name": t["name"], "name_zh": team_zh, "color": t["color"],
        "logo_url": logo_url,
        "logo_light": logo_light,
        "logo_invert": tid in logo_invert_list,
        "drivers": drivers, "drivers_zh": drivers_zh,
        "engineers": engineers, "team_notes": team_notes, "team_notes_zh": team_notes_zh,
    })

out = {
    "season": 2026,
    "generated": "2026-06-22",
    "asset_version": str(max(
        p.stat().st_mtime_ns
        for p in (
            SERIES_PEOPLE_FILE,
            SERIES_PEOPLE_ENRICHMENT_FILE,
            F1_ROLE_TAXONOMY_FILE,
            PHOTOS_FILE,
            F1_PUBLIC_ENGINEERING_FILE,
            F1_PUBLIC_ENGINEERING_EXPANSION_FILE,
            LEADER_PROFILES_FILE,
        )
        if p.exists()
    )),
    "subject": "Race engineers of the 2026 F1 grid — CV / career-path study, plus trackside engineering role map",
    "team_count": len(teams_out),
    "engineer_count": len(flat),
    "trackside_roles": ROLES,
    "series_engineering": SERIES,
    "series_people": SERIES_PEOPLE,
    "series_people_compiled": SERIES_PEOPLE_COMPILED,
    "series_people_enrichment": SERIES_PEOPLE_ENRICHMENT,
    "series_rosters": SERIES_ROSTERS,
    "team_logos": TEAM_LOGOS,
    "f1_public_engineering_people": F1_PUBLIC_ENGINEERING,
    "leader_profiles": LEADER_PROFILES,
    "series_entries": {
        "wec-le-mans": LE_MANS_ENTRIES,
    },
    "motorsport_series": SERIES.get("motorsport_series", []),
    "f1_team_engineering": SERIES.get("f1_team_engineering", {}),
    "teams": teams_out,
    "engineers": flat,
    "external_profiles": build_external_profiles(teams_out, flat, SERIES_PEOPLE_COMPILED),
}
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2))
(ROOT / "web" / "data.js").write_text("window.F1DATA = " + json.dumps(out, ensure_ascii=False) + ";\n")
print(f"wrote {OUT} (+ data.js) — {len(teams_out)} teams, {len(flat)} engineers")

# zh coverage sanity
missing_name = [e["name"] for e in flat if not e.get("name_zh")]
missing_role = [e["name"] for e in flat if not e.get("role_zh")]
print("missing name_zh:", missing_name or "none")
print("missing role_zh:", missing_role or "none")
arche = Counter(e.get("route_archetype", "unknown") for e in flat)
print("route archetypes:", dict(arche))
with_photo = [e["id"] for e in flat if e.get("photo")]
print(f"photos: {len(with_photo)}/{len(flat)}")
print("no photo:", [e["id"] for e in flat if not e.get("photo")] or "none")
with_age = [e["id"] for e in flat if e.get("age") is not None]
print(f"ages: {len(with_age)}/{len(flat)}")
print("no age:", [e["id"] for e in flat if e.get("age") is None] or "none")

# publish per-locale data-content overlays (web/i18n/<locale>.json)
import subprocess, sys as _sys
subprocess.run([_sys.executable, str(ROOT / "scripts" / "build_i18n_overlays.py")], check=False)
