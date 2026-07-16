#!/usr/bin/env python3
"""Build the SQLite data layer for the motorsport engineering dashboard."""
import json
import pathlib
import re
import sqlite3
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
import os
DATA = pathlib.Path(os.environ.get("F1E_DATA_DIR", ROOT / "data"))
WEB_DATA = ROOT / "web" / "data.json"
DB = DATA / "motorsport.db"


def rebuild_payload():
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_data.py")], check=True)
    return json.loads(WEB_DATA.read_text())


def role_title_to_key(role):
    r = (role or "").lower()
    if "chief" in r or "senior" in r:
        return "chief-race-engineer"
    if "race engineer" in r:
        return "race-engineer"
    if "performance" in r:
        return "performance-engineer"
    if "strategy" in r:
        return "strategy-engineer"
    return "engineering-adjacent"


def slug(value):
    value = re.sub(r"[^\w\s-]", "", value or "", flags=re.UNICODE).strip().lower()
    return re.sub(r"\s+", "-", value) or "item"


def source_id(url):
    return "src:" + slug(url.replace("https://", "").replace("http://", ""))


def enrichment_key(series_id, team_name, name, role_key=""):
    return (series_id or "", slug(team_name), slug(name), role_key or "")


def insert_source(cur, source, default_type="web"):
    url = source.get("url") or source.get("source_url")
    if not url:
        return None
    sid = source_id(url)
    cur.execute(
        """
        insert or ignore into sources(id, url, title, source_type, publisher, retrieved_at, json)
        values(?, ?, ?, ?, ?, ?, ?)
        """,
        (
            sid,
            url,
            source.get("title") or source.get("source_title") or url,
            source.get("type") or default_type,
            source.get("publisher", ""),
            source.get("retrieved_at", ""),
            json.dumps(source, ensure_ascii=False),
        ),
    )
    return sid


def ensure_role(cur, key, title="", title_zh="", json_value=None):
    cur.execute(
        """
        insert or ignore into roles(id, title, title_zh, importance_score, seniority_zh, difficulty_zh, json)
        values(?, ?, ?, ?, ?, ?, ?)
        """,
        (
            key,
            title or key,
            title_zh or title or key,
            None,
            "",
            "",
            json.dumps(json_value or {"key": key, "title": title, "title_zh": title_zh}, ensure_ascii=False),
        ),
    )


def put_json(cur, table, key, value):
    cur.execute(
        f"insert into {table}(id, json) values(?, ?)",
        (key, json.dumps(value, ensure_ascii=False)),
    )


def main():
    payload = rebuild_payload()
    DB.parent.mkdir(parents=True, exist_ok=True)
    if DB.exists():
        DB.unlink()

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.executescript(
        """
        pragma foreign_keys = on;

        create table metadata(
          key text primary key,
          value text not null
        );

        create table dashboard_payload(
          id text primary key,
          json text not null,
          generated_at text not null
        );

        create table series(
          id text primary key,
          name text not null,
          name_zh text,
          season_label text,
          public_engineer_names_zh text,
          coverage_zh text,
          json text not null
        );

        create table teams(
          id text primary key,
          series_id text not null,
          source_team_id text,
          name text not null,
          name_zh text,
          color text,
          drivers_json text,
          json text not null
        );

        create table entries(
          id text primary key,
          series_id text not null,
          team_id text,
          class_name text,
          car_number text,
          entrant text,
          car text,
          source_championship text,
          nationality text,
          tyre text,
          misc text,
          drivers_json text,
          source_url text,
          json text not null
        );

        create table people(
          id text primary key,
          name text not null,
          name_zh text,
          nationality text,
          nationality_zh text,
          birth_year integer,
          json text not null
        );

        create table education_entries(
          id text primary key,
          person_id text not null,
          seq integer not null,
          institution text,
          institution_zh text,
          degree text,
          degree_zh text,
          field text,
          field_zh text,
          years text,
          json text not null
        );

        create table career_entries(
          id text primary key,
          person_id text not null,
          seq integer not null,
          year_from text,
          year_to text,
          org text,
          org_zh text,
          role text,
          role_zh text,
          category text,
          category_zh text,
          json text not null
        );

        create table roles(
          id text primary key,
          title text,
          title_zh text,
          importance_score integer,
          seniority_zh text,
          difficulty_zh text,
          json text not null
        );

        create table assignments(
          id text primary key,
          series_id text not null,
          team_id text,
          person_id text,
          role_id text,
          title text,
          title_zh text,
          driver text,
          driver_zh text,
          status text,
          status_zh text,
          importance_score integer,
          public_status_zh text,
          note_zh text,
          json text not null
        );

        create table sources(
          id text primary key,
          url text not null unique,
          title text,
          source_type text,
          publisher text,
          retrieved_at text,
          json text not null
        );

        create table person_sources(
          person_id text not null,
          source_id text not null,
          relation text,
          confidence text,
          primary key(person_id, source_id, relation)
        );

        create table assignment_sources(
          assignment_id text not null,
          source_id text not null,
          relation text,
          primary key(assignment_id, source_id, relation)
        );

        create table entry_sources(
          entry_id text not null,
          source_id text not null,
          relation text,
          primary key(entry_id, source_id, relation)
        );

        create table photos(
          person_id text primary key,
          found integer not null,
          local_path text,
          source_image_url text,
          source_page_url text,
          credit text,
          license text,
          notes text,
          json text not null
        );

        create table data_gaps(
          id text primary key,
          series_id text,
          team_id text,
          entry_id text,
          gap_type text not null,
          severity text not null,
          status text not null,
          note_zh text not null,
          source_id text,
          json text not null
        );

        create table search_runs(
          id text primary key,
          query text not null,
          tool text,
          providers_json text,
          run_at text,
          result_count integer,
          notes_zh text,
          json text not null
        );

        create table raw_json(
          id text primary key,
          json text not null
        );

        create table external_profiles(
          id integer primary key autoincrement,
          name text not null,
          category text,
          series_id text,
          team text,
          role text,
          linkedin_url text,
          relatedin_url text,
          photo_url text,
          photo_status text,
          education_status text,
          education_count integer,
          career_count integer,
          source_urls text,
          last_checked text,
          json text not null
        );

        create table lookup_runs(
          id text primary key,
          run_at text,
          run_type text,
          target text,
          tool text,
          provider text,
          result_count integer,
          status text,
          notes_zh text,
          json text not null
        );

        create index idx_teams_series on teams(series_id);
        create index idx_entries_series_class on entries(series_id, class_name);
        create index idx_entries_entrant on entries(entrant);
        create index idx_people_name on people(name);
        create index idx_assignments_series_team on assignments(series_id, team_id);
        create index idx_assignments_person on assignments(person_id);
        create index idx_assignments_role on assignments(role_id);
        create index idx_career_person on career_entries(person_id, seq);
        create index idx_education_person on education_entries(person_id, seq);
        create index idx_data_gaps_scope on data_gaps(series_id, team_id, entry_id, gap_type);
        create index idx_extprofiles_name on external_profiles(name);
        create index idx_extprofiles_scope on external_profiles(series_id, team, category);
        create index idx_extprofiles_linkedin on external_profiles(linkedin_url);
        create index idx_lookup_runs_type on lookup_runs(run_type, run_at);
        """
    )

    cur.execute("insert into metadata(key, value) values(?, ?)", ("generated", payload["generated"]))
    cur.execute(
        "insert into dashboard_payload(id, json, generated_at) values(?, ?, ?)",
        ("dashboard", json.dumps(payload, ensure_ascii=False), payload["generated"]),
    )

    track_roles = payload.get("trackside_roles", {}).get("hierarchy", [])
    for r in track_roles:
        key = r.get("title", "").lower().replace(" / ", "-").replace(" ", "-")
        cur.execute(
            """
            insert into roles(id, title, title_zh, importance_score, seniority_zh, difficulty_zh, json)
            values(?, ?, ?, ?, ?, ?, ?)
            """,
            (
                key,
                r.get("title"),
                r.get("title_zh"),
                r.get("importance_score"),
                r.get("seniority_zh"),
                r.get("difficulty_zh"),
                json.dumps(r, ensure_ascii=False),
            ),
        )

    series_defs = payload.get("series_engineering", {}).get("series_role_definitions", [])
    for r in series_defs:
        cur.execute(
            """
            insert or replace into roles(id, title, title_zh, importance_score, seniority_zh, difficulty_zh, json)
            values(?, ?, ?, ?, ?, ?, ?)
            """,
            (
                r.get("key"),
                r.get("title"),
                r.get("title_zh"),
                r.get("importance_score"),
                r.get("seniority_zh"),
                r.get("difficulty_zh"),
                json.dumps(r, ensure_ascii=False),
            ),
        )
    for r in payload.get("f1_team_engineering", {}).get("role_templates", []):
        cur.execute(
            """
            insert or replace into roles(id, title, title_zh, importance_score, seniority_zh, difficulty_zh, json)
            values(?, ?, ?, ?, ?, ?, ?)
            """,
            (
                r.get("key"),
                r.get("title"),
                r.get("title_zh"),
                r.get("importance_score"),
                r.get("seniority_zh"),
                r.get("difficulty_zh"),
                json.dumps(r, ensure_ascii=False),
            ),
        )

    for s in payload.get("motorsport_series", []):
        cur.execute(
            """
            insert into series(id, name, name_zh, season_label, public_engineer_names_zh, coverage_zh, json)
            values(?, ?, ?, ?, ?, ?, ?)
            """,
            (
                s["id"],
                s.get("name"),
                s.get("name_zh"),
                s.get("season_label"),
                s.get("public_engineer_names_zh"),
                s.get("coverage_zh"),
                json.dumps(s, ensure_ascii=False),
            ),
        )
        for name in s.get("teams", []):
            tid = f"{s['id']}:{name.lower().replace(' ', '-').replace('/', '-')}"
            cur.execute(
                """
                insert or ignore into teams(id, series_id, source_team_id, name, name_zh, color, drivers_json, json)
                values(?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (tid, s["id"], None, name, "", "", "[]", json.dumps({"name": name}, ensure_ascii=False)),
            )

    for t in payload.get("teams", []):
        team_pk = f"f1:{t['id']}"
        cur.execute(
            """
            insert or replace into teams(id, series_id, source_team_id, name, name_zh, color, drivers_json, json)
            values(?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                team_pk,
                "f1",
                t["id"],
                t.get("name"),
                t.get("name_zh"),
                t.get("color"),
                json.dumps(t.get("drivers", []), ensure_ascii=False),
                json.dumps(t, ensure_ascii=False),
            ),
        )
        for e in t.get("engineers", []):
            cur.execute(
                """
                insert or replace into people(id, name, name_zh, nationality, nationality_zh, birth_year, json)
                values(?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    e["id"],
                    e.get("name"),
                    e.get("name_zh"),
                    e.get("nationality"),
                    e.get("nationality_zh"),
                    e.get("birth_year"),
                    json.dumps(e, ensure_ascii=False),
                ),
            )
            for idx, ed in enumerate(e.get("education", [])):
                cur.execute(
                    """
                    insert into education_entries(
                      id, person_id, seq, institution, institution_zh, degree, degree_zh,
                      field, field_zh, years, json
                    )
                    values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        f"{e['id']}:edu:{idx}",
                        e["id"],
                        idx,
                        ed.get("institution"),
                        ed.get("institution_zh"),
                        ed.get("degree"),
                        ed.get("degree_zh"),
                        ed.get("field"),
                        ed.get("field_zh"),
                        ed.get("years"),
                        json.dumps(ed, ensure_ascii=False),
                    ),
                )
            for idx, c in enumerate(e.get("career", [])):
                cur.execute(
                    """
                    insert into career_entries(
                      id, person_id, seq, year_from, year_to, org, org_zh, role,
                      role_zh, category, category_zh, json
                    )
                    values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        f"{e['id']}:career:{idx}",
                        e["id"],
                        idx,
                        c.get("from"),
                        c.get("to"),
                        c.get("org"),
                        c.get("org_zh"),
                        c.get("role"),
                        c.get("role_zh"),
                        c.get("category"),
                        c.get("category_zh"),
                        json.dumps(c, ensure_ascii=False),
                    ),
                )
            for s in e.get("sources", []):
                sid = insert_source(cur, s)
                if sid:
                    cur.execute(
                        "insert or ignore into person_sources(person_id, source_id, relation, confidence) values(?, ?, ?, ?)",
                        (e["id"], sid, "profile", e.get("confidence", "")),
                    )
            photo = e.get("photo") or {}
            cur.execute(
                """
                insert or replace into photos(
                  person_id, found, local_path, source_image_url, source_page_url,
                  credit, license, notes, json
                )
                values(?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    e["id"],
                    1 if photo.get("found") else 0,
                    photo.get("local", ""),
                    photo.get("src_img", ""),
                    photo.get("src_page", ""),
                    photo.get("credit", ""),
                    photo.get("license", ""),
                    photo.get("notes", ""),
                    json.dumps(photo, ensure_ascii=False),
                ),
            )
            role_id = role_title_to_key(e.get("role"))
            drivers = e.get("drivers_2026") or [""]
            drivers_zh = e.get("drivers_zh") or ["" for _ in drivers]
            for idx, driver in enumerate(drivers):
                driver_zh = drivers_zh[idx] if idx < len(drivers_zh) else ""
                aid = f"f1:{t['id']}:{e['id']}:{idx}"
                cur.execute(
                    """
                    insert into assignments(
                      id, series_id, team_id, person_id, role_id, title, title_zh,
                      driver, driver_zh, status, status_zh, importance_score,
                      public_status_zh, note_zh, json
                    )
                    values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        aid,
                        "f1",
                        team_pk,
                        e["id"],
                        role_id,
                        e.get("role"),
                        e.get("role_zh"),
                        driver,
                        driver_zh,
                        e.get("pairing_status", "fixed"),
                        e.get("pairing_status_zh", "公开命名"),
                        84 if role_id == "race-engineer" else 88 if role_id == "chief-race-engineer" else 60,
                        "公开命名",
                        e.get("pairing_note_zh", ""),
                        json.dumps(e, ensure_ascii=False),
                    ),
                )
                for s in e.get("sources", []):
                    sid = insert_source(cur, s)
                    if sid:
                        cur.execute(
                            "insert or ignore into assignment_sources(assignment_id, source_id, relation) values(?, ?, ?)",
                            (aid, sid, "driver-engineer-pairing"),
                        )

    f1_team_engineering = payload.get("f1_team_engineering", {})
    leader_profiles = (payload.get("leader_profiles", {}) or {}).get("people", {})
    team_meta = {t["id"]: t for t in payload.get("teams", [])}
    f1_source_ids = [
        sid for sid in (
            insert_source(cur, s)
            for s in payload.get("series_engineering", {}).get("sources", [])
        )
        if sid
    ]
    for t in f1_team_engineering.get("teams", []):
        source_team_id = t.get("team_id")
        team_pk = f"f1:{source_team_id}"
        for idx, leader in enumerate(t.get("leadership", [])):
            profile = leader_profiles.get(leader.get("person"), {})
            pid = f"leader:{source_team_id}:{leader.get('person', '').lower().replace(' ', '-')}"
            aid = f"f1:{source_team_id}:leader:{idx}"
            cur.execute(
                """
                insert or replace into people(id, name, name_zh, nationality, nationality_zh, birth_year, json)
                values(?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    pid,
                    leader.get("person"),
                    leader.get("person_zh"),
                    "",
                    "",
                    profile.get("birth_year"),
                    json.dumps(leader, ensure_ascii=False),
                ),
            )
            if profile.get("photo_url"):
                cur.execute(
                    """
                    insert or replace into photos(
                      person_id, found, local_path, source_image_url, source_page_url,
                      credit, license, notes, json
                    )
                    values(?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        pid,
                        1,
                        "",
                        profile.get("photo_url", ""),
                        profile.get("source_url", ""),
                        profile.get("photo_credit", ""),
                        "",
                        "F1 leadership profile image",
                        json.dumps(profile, ensure_ascii=False),
                    ),
                )
            if profile.get("source_url"):
                sid = insert_source(
                    cur,
                    {
                        "url": profile.get("source_url"),
                        "title": profile.get("source_title"),
                        "type": "leadership_profile_photo",
                        "publisher": profile.get("photo_credit", ""),
                    },
                    "leadership_profile_photo",
                )
                if sid:
                    cur.execute(
                        "insert or ignore into person_sources(person_id, source_id, relation, confidence) values(?, ?, ?, ?)",
                        (pid, sid, "leadership-photo-profile", profile.get("confidence", "medium")),
                    )
            for sid in f1_source_ids:
                cur.execute(
                    "insert or ignore into person_sources(person_id, source_id, relation, confidence) values(?, ?, ?, ?)",
                    (pid, sid, "leadership-background", "medium"),
                )
            cur.execute(
                """
                insert into assignments(
                  id, series_id, team_id, person_id, role_id, title, title_zh,
                  driver, driver_zh, status, status_zh, importance_score,
                  public_status_zh, note_zh, json
                )
                values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    aid,
                    "f1",
                    team_pk,
                    pid,
                    "engineering-principal",
                    leader.get("role_zh"),
                    leader.get("role_zh"),
                    "",
                    "",
                    "named",
                    leader.get("engineering_background_zh"),
                    leader.get("importance_score"),
                    "公开命名",
                    leader.get("note_zh"),
                    json.dumps(leader, ensure_ascii=False),
                ),
            )
            for sid in f1_source_ids:
                cur.execute(
                    "insert or ignore into assignment_sources(assignment_id, source_id, relation) values(?, ?, ?)",
                    (aid, sid, "leadership-role"),
                )

        public_engineering = payload.get("f1_public_engineering_people", {})
        public_engineering_sources = [
            sid for sid in (
                insert_source(cur, s)
                for s in public_engineering.get("sources", [])
            )
            if sid
        ]
        for idx, person in enumerate((public_engineering.get("teams", {}) or {}).get(source_team_id, [])):
            role_id = person.get("role_key") or role_title_to_key(person.get("role"))
            pid = f"f1eng:{source_team_id}:{slug(person.get('person', ''))}:{slug(role_id)}"
            aid = f"f1:{source_team_id}:public-engineering:{idx}:{slug(role_id)}"
            person_json = dict(person)
            person_json["team_id"] = source_team_id
            person_json["series_id"] = "f1"
            cur.execute(
                """
                insert or replace into people(id, name, name_zh, nationality, nationality_zh, birth_year, json)
                values(?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    pid,
                    person.get("person"),
                    person.get("person_zh", ""),
                    person.get("nationality", ""),
                    person.get("nationality_zh", ""),
                    person.get("birth_year"),
                    json.dumps(person_json, ensure_ascii=False),
                ),
            )
            current_career = {
                "from": person.get("from", "公开履历"),
                "to": "2026",
                "org": team_meta.get(source_team_id, {}).get("name", ""),
                "org_zh": team_meta.get(source_team_id, {}).get("name_zh", ""),
                "role": person.get("role", ""),
                "role_zh": person.get("career_summary_zh") or person.get("note_zh") or person.get("role_zh", ""),
                "category": "F1",
                "category_zh": "F1",
            }
            for cidx, career in enumerate(person.get("career") or [current_career]):
                cur.execute(
                    """
                    insert into career_entries(
                      id, person_id, seq, year_from, year_to, org, org_zh, role,
                      role_zh, category, category_zh, json
                    )
                    values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        f"{pid}:career:{cidx}",
                        pid,
                        cidx,
                        career.get("from"),
                        career.get("to"),
                        career.get("org"),
                        career.get("org_zh"),
                        career.get("role"),
                        career.get("role_zh"),
                        career.get("category"),
                        career.get("category_zh"),
                        json.dumps(career, ensure_ascii=False),
                    ),
                )
            if person.get("photo_url"):
                cur.execute(
                    """
                    insert or replace into photos(
                      person_id, found, local_path, source_image_url, source_page_url,
                      credit, license, notes, json
                    )
                    values(?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        pid,
                        1,
                        "",
                        person.get("photo_url", ""),
                        person.get("photo_source_url", ""),
                        person.get("photo_credit", ""),
                        "",
                        "F1 public engineering profile image",
                        json.dumps(person, ensure_ascii=False),
                    ),
                )
            source_ids = [
                sid for sid in (
                    insert_source(cur, s)
                    for s in person.get("sources", [])
                )
                if sid
            ] or public_engineering_sources
            for sid in source_ids:
                cur.execute(
                    "insert or ignore into person_sources(person_id, source_id, relation, confidence) values(?, ?, ?, ?)",
                    (pid, sid, "public-engineering-profile", person.get("confidence", "high")),
                )
            cur.execute(
                """
                insert into assignments(
                  id, series_id, team_id, person_id, role_id, title, title_zh,
                  driver, driver_zh, status, status_zh, importance_score,
                  public_status_zh, note_zh, json
                )
                values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    aid,
                    "f1",
                    team_pk,
                    pid,
                    role_id,
                    person.get("role"),
                    person.get("role_zh"),
                    "",
                    "",
                    "named",
                    "公开命名",
                    person.get("importance_score"),
                    "公开命名",
                    person.get("note_zh") or person.get("career_summary_zh", ""),
                    json.dumps(person_json, ensure_ascii=False),
                ),
            )
            for sid in source_ids:
                cur.execute(
                    "insert or ignore into assignment_sources(assignment_id, source_id, relation) values(?, ?, ?)",
                    (aid, sid, "public-engineering-role"),
                )

        for tmpl in f1_team_engineering.get("role_templates", []):
            if tmpl["key"] in {"technical-leadership", "engineering-principal", "race-engineer"}:
                continue
            aid = f"f1:{source_team_id}:slot:{tmpl['key']}"
            note = f"{team_meta.get(source_team_id, {}).get('name_zh') or source_team_id} 存在该工程职能；未找到完整公开姓名名单。"
            cur.execute(
                """
                insert into assignments(
                  id, series_id, team_id, person_id, role_id, title, title_zh,
                  driver, driver_zh, status, status_zh, importance_score,
                  public_status_zh, note_zh, json
                )
                values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    aid,
                    "f1",
                    team_pk,
                    None,
                    tmpl["key"],
                    tmpl.get("title"),
                    tmpl.get("title_zh"),
                    "",
                    "",
                    "role_exists_name_not_public",
                    "岗位存在，姓名未完整公开",
                    tmpl.get("importance_score"),
                    tmpl.get("publicity_zh"),
                    note,
                    json.dumps(tmpl, ensure_ascii=False),
                ),
            )

    series_entries = payload.get("series_entries", {}).get("wec-le-mans", {})
    le_mans_source_id = insert_source(
        cur,
        {
            "url": series_entries.get("source_url"),
            "title": series_entries.get("source_title"),
            "type": "official_entry_list",
            "retrieved_at": payload.get("generated", ""),
        },
        "official_entry_list",
    ) if series_entries else None
    for entry in series_entries.get("entries", []):
        team_slug = slug(entry.get("entrant", ""))
        team_pk = f"wec-le-mans:{team_slug}"
        cur.execute(
            """
            insert or ignore into teams(id, series_id, source_team_id, name, name_zh, color, drivers_json, json)
            values(?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                team_pk,
                "wec-le-mans",
                team_slug,
                entry.get("entrant"),
                "",
                "",
                json.dumps([d.get("name") for d in entry.get("drivers", [])], ensure_ascii=False),
                json.dumps({"name": entry.get("entrant"), "source": "Le Mans entry list"}, ensure_ascii=False),
            ),
        )
        cur.execute(
            """
            insert or replace into entries(
              id, series_id, team_id, class_name, car_number, entrant, car,
              source_championship, nationality, tyre, misc, drivers_json, source_url, json
            )
            values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry["id"],
                entry["series_id"],
                team_pk,
                entry.get("class_name"),
                entry.get("car_number"),
                entry.get("entrant"),
                entry.get("car"),
                entry.get("source_championship"),
                entry.get("nationality"),
                entry.get("tyre"),
                entry.get("misc"),
                json.dumps(entry.get("drivers", []), ensure_ascii=False),
                entry.get("source_url"),
                json.dumps(entry, ensure_ascii=False),
            ),
        )
        if le_mans_source_id:
            cur.execute(
                "insert or ignore into entry_sources(entry_id, source_id, relation) values(?, ?, ?)",
                (entry["id"], le_mans_source_id, "official-entry-list"),
            )
        for role_key in ["car-race-engineer", "strategy-engineer", "performance-data-engineer", "systems-energy-engineer", "tyre-fuel-stint-engineer"]:
            ensure_role(cur, role_key)
            aid = f"{entry['id']}:slot:{role_key}"
            cur.execute(
                """
                insert or ignore into assignments(
                  id, series_id, team_id, person_id, role_id, title, title_zh,
                  driver, driver_zh, status, status_zh, importance_score,
                  public_status_zh, note_zh, json
                )
                values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    aid,
                    entry["series_id"],
                    team_pk,
                    None,
                    role_key,
                    role_key,
                    role_key,
                    "",
                    "",
                    "role_exists_name_not_public",
                    "岗位存在，姓名未完整公开",
                    None,
                    "未完整公开",
                    f"{entry.get('class_name')} #{entry.get('car_number')} {entry.get('entrant')} 的工程岗位存在，但官方 entry list 不公开完整工程师名单。",
                    json.dumps(entry, ensure_ascii=False),
                ),
            )
        gap_id = f"{entry['id']}:gap:engineering-roster"
        cur.execute(
            """
            insert or replace into data_gaps(
              id, series_id, team_id, entry_id, gap_type, severity, status,
              note_zh, source_id, json
            )
            values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                gap_id,
                entry["series_id"],
                team_pk,
                entry["id"],
                "named_engineering_roster_missing",
                "medium",
                "known_publication_gap",
                "Le Mans 官方 entry list 公开车号、组别、车辆和车手，但不公开完整单车工程师名单；可核验姓名出现时再逐 entry 补充。",
                le_mans_source_id,
                json.dumps(entry, ensure_ascii=False),
            ),
        )

    series_people = payload.get("series_people_compiled") or payload.get("series_people", {})
    series_people_enrichment = payload.get("series_people_enrichment", {}) or {}
    enrichment_by_person = {
        enrichment_key(p.get("series_id"), p.get("team_name"), p.get("name"), p.get("role_key")): p
        for p in series_people_enrichment.get("profiles", [])
    }
    unresolved_by_person = {
        enrichment_key(p.get("series_id"), p.get("team_name"), p.get("name"), p.get("role_key")): p
        for p in series_people_enrichment.get("unresolved", [])
    }
    for series_id, series_data in (series_people.get("series") or {}).items():
        for team in series_data.get("teams", []):
            team_name = team.get("team_name", "")
            team_pk = f"{series_id}:{slug(team_name)}"
            cur.execute(
                """
                insert or ignore into teams(id, series_id, source_team_id, name, name_zh, color, drivers_json, json)
                values(?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (team_pk, series_id, slug(team_name), team_name, "", "", "[]", json.dumps(team, ensure_ascii=False)),
            )
            src = insert_source(
                cur,
                {"url": team.get("source_url"), "title": team.get("source_title"), "type": "official_team_page"},
                "official_team_page",
            )
            for member in team.get("members", []):
                if not member.get("engineering_related", True):
                    continue
                pid = f"{series_id}:{slug(team_name)}:{slug(member.get('name'))}"
                role_id = member.get("role_key") or slug(member.get("role"))
                enriched = enrichment_by_person.get(enrichment_key(series_id, team_name, member.get("name"), role_id), {})
                unresolved = unresolved_by_person.get(enrichment_key(series_id, team_name, member.get("name"), role_id), {})
                ensure_role(cur, role_id, member.get("role"), member.get("role_group_zh"), member)
                person_json = {
                    **member,
                    "public_profiles": enriched.get("public_profiles", []),
                    "profile_lookup_status": "no_trusted_result" if unresolved else "profile_found" if enriched.get("public_profiles") else "not_enriched_yet",
                    "profile_lookup_note_zh": unresolved.get("note_zh", ""),
                    "career_summary_enriched_zh": enriched.get("career_summary_zh", ""),
                    "id": pid,
                    "series_id": series_id,
                    "team_name": team_name,
                    "source_url": team.get("source_url"),
                    "source_title": team.get("source_title"),
                }
                cur.execute(
                    """
                    insert or replace into people(id, name, name_zh, nationality, nationality_zh, birth_year, json)
                    values(?, ?, ?, ?, ?, ?, ?)
                    """,
                    (pid, member.get("name"), "", "", "", member.get("birth_year"), json.dumps(person_json, ensure_ascii=False)),
                )
                if src:
                    cur.execute(
                        "insert or ignore into person_sources(person_id, source_id, relation, confidence) values(?, ?, ?, ?)",
                        (pid, src, "series-public-team-member", member.get("confidence", "high")),
                    )
                photo = member.get("photo") or enriched.get("photo") or {}
                if photo.get("found"):
                    cur.execute(
                        """
                        insert or replace into photos(
                          person_id, found, local_path, source_image_url, source_page_url,
                          credit, license, notes, json
                        )
                        values(?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            pid,
                            1,
                            photo.get("local", ""),
                            photo.get("src_img", ""),
                            photo.get("src_page", ""),
                            photo.get("credit", ""),
                            photo.get("license", ""),
                            photo.get("provenance", ""),
                            json.dumps(photo, ensure_ascii=False),
                        ),
                    )
                    psid = insert_source(
                        cur,
                        {
                            "url": photo.get("src_page"),
                            "title": photo.get("credit") or photo.get("src_page"),
                            "type": photo.get("provenance") or "profile_photo",
                            "publisher": photo.get("credit", ""),
                        },
                        photo.get("provenance") or "profile_photo",
                    )
                    if psid:
                        cur.execute(
                            "insert or ignore into person_sources(person_id, source_id, relation, confidence) values(?, ?, ?, ?)",
                            (pid, psid, "profile-photo", photo.get("confidence", "medium")),
                        )
                for profile in enriched.get("public_profiles", []):
                    psid = insert_source(
                        cur,
                        {
                            "url": profile.get("url"),
                            "title": profile.get("title"),
                            "type": profile.get("type") or "profile",
                            "publisher": "LinkedIn" if profile.get("type") == "linkedin" else "",
                        },
                        profile.get("type") or "profile",
                    )
                    if psid:
                        cur.execute(
                            "insert or ignore into person_sources(person_id, source_id, relation, confidence) values(?, ?, ?, ?)",
                            (pid, psid, "public-career-profile", profile.get("confidence", "medium")),
                        )
                for seq, ed in enumerate(member.get("education", [])):
                    cur.execute(
                        """
                        insert or replace into education_entries(
                          id, person_id, seq, institution, institution_zh,
                          degree, degree_zh, field, field_zh, years, json
                        )
                        values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            f"{pid}:edu:{seq}",
                            pid,
                            seq,
                            ed.get("institution", ""),
                            ed.get("institution_zh", ""),
                            ed.get("degree", ""),
                            ed.get("degree_zh", ""),
                            ed.get("field", ""),
                            ed.get("field_zh", ""),
                            ed.get("years", ""),
                            json.dumps(ed, ensure_ascii=False),
                        ),
                    )
                for seq, c in enumerate(member.get("career", [])):
                    cur.execute(
                        """
                        insert or replace into career_entries(
                          id, person_id, seq, year_from, year_to,
                          org, org_zh, role, role_zh, category, category_zh, json
                        )
                        values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            f"{pid}:career:{seq}",
                            pid,
                            seq,
                            c.get("from", ""),
                            c.get("to", ""),
                            c.get("org", ""),
                            c.get("org_zh", ""),
                            c.get("role", ""),
                            c.get("role_zh", ""),
                            c.get("category", ""),
                            c.get("category_zh", ""),
                            json.dumps(c, ensure_ascii=False),
                        ),
                    )
                entry_id = None
                if series_id == "wec-le-mans" and member.get("entry_number"):
                    row = cur.execute(
                        "select id from entries where series_id = ? and car_number = ?",
                        (series_id, member.get("entry_number")),
                    ).fetchone()
                    entry_id = row[0] if row else None
                aid_scope = entry_id or team_pk
                aid = f"{aid_scope}:person:{slug(member.get('name'))}:{role_id}"
                cur.execute(
                    """
                    insert or replace into assignments(
                      id, series_id, team_id, person_id, role_id, title, title_zh,
                      driver, driver_zh, status, status_zh, importance_score,
                      public_status_zh, note_zh, json
                    )
                    values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        aid,
                        series_id,
                        team_pk,
                        pid,
                        role_id,
                        member.get("role"),
                        member.get("role_group_zh") or member.get("role"),
                        "",
                        "",
                        "named",
                        "已列名",
                        None,
                        "已列名",
                        member.get("notes_zh", ""),
                        json.dumps(person_json, ensure_ascii=False),
                    ),
                )
                if src:
                    cur.execute(
                        "insert or ignore into assignment_sources(assignment_id, source_id, relation) values(?, ?, ?)",
                        (aid, src, "public-role"),
                    )
                for profile in enriched.get("public_profiles", []):
                    if not profile.get("url"):
                        continue
                    cur.execute(
                        "insert or ignore into assignment_sources(assignment_id, source_id, relation) values(?, ?, ?)",
                        (aid, source_id(profile["url"]), "public-career-profile"),
                    )
                if unresolved:
                    gap_id = f"profile-gap:{series_id}:{slug(team_name)}:{slug(member.get('name'))}:{role_id}"
                    cur.execute(
                        """
                        insert or replace into data_gaps(
                          id, series_id, team_id, entry_id, gap_type, severity, status,
                          note_zh, source_id, json
                        )
                        values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            gap_id,
                            series_id,
                            team_pk,
                            None,
                            "public_profile_not_found",
                            "low",
                            "searched_no_trusted_result",
                            unresolved.get("note_zh", ""),
                            None,
                            json.dumps(unresolved, ensure_ascii=False),
                        ),
                    )

    search_runs_file = DATA / "search_runs.json"
    if search_runs_file.exists():
        for item in json.loads(search_runs_file.read_text()).get("runs", []):
            cur.execute(
                """
                insert or replace into search_runs(id, query, tool, providers_json, run_at, result_count, notes_zh, json)
                values(?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item["id"],
                    item.get("query", ""),
                    item.get("tool", ""),
                    json.dumps(item.get("providers", []), ensure_ascii=False),
                    item.get("run_at", ""),
                    item.get("result_count"),
                    item.get("notes_zh", ""),
                    json.dumps(item, ensure_ascii=False),
                ),
            )

    for p in payload.get("external_profiles", []):
        cur.execute(
            """
            insert into external_profiles(
              name, category, series_id, team, role, linkedin_url, relatedin_url,
              photo_url, photo_status, education_status, education_count, career_count,
              source_urls, last_checked, json)
            values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                p.get("name", ""),
                p.get("category", ""),
                p.get("series_id", ""),
                p.get("team", ""),
                p.get("role", ""),
                p.get("linkedin_url", ""),
                p.get("relatedin_url", ""),
                p.get("photo_url", ""),
                p.get("photo_status", ""),
                p.get("education_status", ""),
                p.get("education_count"),
                p.get("career_count"),
                json.dumps(p.get("source_urls", []), ensure_ascii=False),
                p.get("last_checked", ""),
                json.dumps(p, ensure_ascii=False),
            ),
        )

    lookup_runs_file = DATA / "lookup_runs.json"
    if lookup_runs_file.exists():
        for item in json.loads(lookup_runs_file.read_text()).get("runs", []):
            cur.execute(
                """
                insert or replace into lookup_runs(
                  id, run_at, run_type, target, tool, provider, result_count, status, notes_zh, json)
                values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item["id"],
                    item.get("run_at", ""),
                    item.get("run_type", ""),
                    item.get("target", ""),
                    item.get("tool", ""),
                    item.get("provider", ""),
                    item.get("result_count"),
                    item.get("status", ""),
                    item.get("notes_zh", ""),
                    json.dumps(item, ensure_ascii=False),
                ),
            )

    put_json(cur, "raw_json", "series_engineering", payload.get("series_engineering", {}))
    put_json(cur, "raw_json", "trackside_roles", payload.get("trackside_roles", {}))
    put_json(cur, "raw_json", "series_people", payload.get("series_people", {}))
    put_json(cur, "raw_json", "series_people_compiled", payload.get("series_people_compiled", {}))
    put_json(cur, "raw_json", "series_people_enrichment", payload.get("series_people_enrichment", {}))
    put_json(cur, "raw_json", "series_rosters", payload.get("series_rosters", {}))
    put_json(cur, "raw_json", "leader_profiles", payload.get("leader_profiles", {}))
    put_json(cur, "raw_json", "series_entries", payload.get("series_entries", {}))

    conn.commit()
    conn.close()
    print(f"wrote {DB}")


if __name__ == "__main__":
    main()
