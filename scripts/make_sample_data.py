#!/usr/bin/env python3
"""Generate a 100% FICTIONAL sample dataset under data/sample/.

Purpose: the public repo must run out of the box without the private research
data. Every person, team, driver, university, and URL below is an obvious
placeholder — no real person's data appears here. Role keys/titles in the
trackside hierarchy and role templates are copied from the project methodology
(they describe jobs, not people).

Usage:
    python3 scripts/make_sample_data.py
    F1E_DATA_DIR=data/sample python3 scripts/build_data.py
    F1E_DATA_DIR=data/sample python3 scripts/seed_db.py

The generator is deterministic: same output every run, no randomness.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "sample"

GEN = "2026-01-01"          # fixed fictional "generated" date
EX = "https://example.com"  # every source URL points at example.com

# --------------------------------------------------------------------------
# Fictional grid: 3 teams, 2 drivers + 2 race engineers each.
# --------------------------------------------------------------------------
TEAMS = [
    {
        "id": "apex-gp", "name": "Apex GP", "name_zh": "示例车队·Apex", "color": "#FF6600",
        "seats": [("Sam Speedwell", "Alex Example"), ("Robin Apexley", "Jordan Sample")],
    },
    {
        "id": "example-racing", "name": "Example Racing", "name_zh": "示例车队·Example", "color": "#0044CC",
        "seats": [("Jamie Gridley", "Casey Placeholder"), ("Morgan Chicane", "Riley Fixture")],
    },
    {
        "id": "placeholder-motorsport", "name": "Placeholder Motorsport", "name_zh": "示例车队·Placeholder", "color": "#00A550",
        "seats": [("Taylor Hairpin", "Devon Mockford"), ("Quinn Slipstream", "Harper Stub")],
    },
]

# Fictional education/career building blocks reused across people.
UNIS = [
    ("Sampleton University", "示例大学（Sampleton）", "Motorsport Engineering"),
    ("Placeholder Institute of Technology", "示例理工学院（Placeholder）", "Mechanical Engineering"),
    ("Fictional Polytechnic", "示例职业技术学院（Fictional）", "Aerospace Engineering"),
]
ARCHETYPES = ["uni-junior-formula-to-f1", "data-eng-to-RE"]  # methodology keys


def slug(name):
    return name.lower().replace(" ", "-")


def edu(i):
    inst, inst_zh, field = UNIS[i % len(UNIS)]
    return (
        {"institution": inst, "degree": "MEng", "field": field, "years": "2006-2010"},
        {"institution_zh": inst_zh, "degree_zh": "工程硕士", "field_zh": "示例工程专业"},
    )


def career(team_name, i):
    """Two-step fictional ladder ending at the current fictional F1 team."""
    en = [
        {"from": "2011", "to": "2015", "org": "Demo Junior Formula Team", "role": "Data Engineer", "category": "F2"},
        {"from": "2016", "to": "present", "org": team_name, "role": "Race Engineer", "category": "F1"},
    ]
    zh = [
        {"org_zh": "示例初级方程式车队", "role_zh": "数据工程师", "category_zh": "F2"},
        {"org_zh": "", "role_zh": "赛车工程师", "category_zh": "F1"},
    ]
    return en, zh


def write(rel, obj):
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {path.relative_to(ROOT)}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # -- teams_2026.json ----------------------------------------------------
    write("teams_2026.json", {
        "season": 2026,
        "note": "FICTIONAL sample dataset — every team, driver and person is a placeholder.",
        "teams": [
            {"id": t["id"], "name": t["name"], "color": t["color"],
             "seats": [{"driver": d, "race_engineer": e} for d, e in t["seats"]]}
            for t in TEAMS
        ],
    })

    # -- i18n/glossary.json (required at import time by build_data.py) ------
    write("i18n/glossary.json", {
        "teams": {t["name"]: t["name_zh"] for t in TEAMS},
        "drivers": {d: f"示例车手 {d.split()[0]}" for t in TEAMS for d, _ in t["seats"]},
        "archetypes": {
            "uni-junior-formula-to-f1": "大学 → 初级方程式 → F1",
            "data-eng-to-RE": "数据工程师 → 赛车工程师",
        },
        "archetype_desc": {
            "uni-junior-formula-to-f1": "示例说明：工程学位后经初级方程式进入 F1。",
            "data-eng-to-RE": "示例说明：以数据工程师身份进队后晋升为赛车工程师。",
        },
        "categories": {"F1": "F1", "F2": "F2", "other": "其他"},
        "confidence": {"high": "高", "medium": "中", "low": "低"},
    })

    # -- research/<team>.json + i18n/<team>.zh.json --------------------------
    person_index = 0
    for t in TEAMS:
        engineers, zh_engineers = [], {}
        for driver, eng_name in t["seats"]:
            eid = slug(eng_name)
            e_edu, z_edu = edu(person_index)
            e_car, z_car = career(t["name"], person_index)
            engineers.append({
                "id": eid, "name": eng_name, "aka": [], "role": "Race Engineer",
                "team_2026": t["name"], "drivers_2026": [driver],
                "nationality": "Exampleland",
                "education": [e_edu], "career": e_car,
                "f1_debut_year": 2016, "years_to_race_engineer": 5,
                "route_archetype": ARCHETYPES[person_index % len(ARCHETYPES)],
                "highlights": ["Entirely fictional career for demo purposes."],
                "sources": [{"url": f"{EX}/profiles/{eid}", "type": "profile",
                             "title": f"{eng_name} - Example Profiles"}],
                "confidence": "high",
                "notes": "Fictional sample person; not a real individual.",
            })
            zh_engineers[eid] = {
                "name_zh": f"示例工程师 {eng_name.split()[0]}",
                "role_zh": "赛车工程师", "nationality_zh": "示例国",
                "education_zh": [z_edu], "career_zh": z_car,
                "highlights_zh": ["示例数据：完全虚构的履历。"],
                "notes_zh": "示例数据：虚构人物，仅用于演示。",
            }
            person_index += 1
        write(f"research/{t['id']}.json", {
            "team_id": t["id"], "team": t["name"], "engineers": engineers,
            "team_notes": "Fictional sample team.",
        })
        write(f"i18n/{t['id']}.zh.json", {
            "team_id": t["id"], "team_zh": t["name_zh"],
            "team_notes_zh": "示例数据：虚构车队。", "engineers": zh_engineers,
        })

    # -- trackside_roles.json (role titles = methodology; zh kept generic) --
    role_rows = [
        ("department", "Head / Director of Race Engineering", "赛事工程主管 / 总监", 92),
        ("car-lead", "Senior / Chief Race Engineer", "资深 / 首席赛车工程师", 90),
        ("car-lead", "Race Engineer", "赛车工程师", 88),
        ("car-support", "Performance Engineer", "性能工程师", 80),
        ("pit-wall", "Strategy Engineer / Strategist", "策略工程师 / 策略师", 78),
        ("factory-feed", "Simulation / Simulator Engineer", "仿真 / 模拟器工程师", 70),
    ]
    write("trackside_roles.json", {
        "last_verified": GEN,
        "scope_note": "Fictional sample: role hierarchy titles are methodology, examples are placeholders.",
        "scope_note_zh": "示例数据：岗位结构来自方法论，示例人名均为虚构。",
        "hierarchy": [
            {"level": lvl, "title": title, "title_zh": zh,
             "summary_zh": "示例岗位说明。", "typical_progression_zh": "示例晋升路径。",
             "seniority_zh": "示例层级", "importance_score": score, "importance_zh": "高",
             "difficulty_zh": "高", "difficulty_score": 3, "path_position_zh": "示例位置",
             "difficulty_reason_zh": "示例难度说明。", "examples": ["Alex Example"]}
            for lvl, title, zh, score in role_rows
        ],
        "sources": [{"title": "Example Motorsport Handbook", "url": f"{EX}/handbook/trackside-roles",
                     "note": "Placeholder source."}],
    })

    # -- series_engineering.json ---------------------------------------------
    role_templates = [
        ("technical-leadership", "Technical Director / CTO", "技术总监", 100),
        ("engineering-principal", "Team Principal with engineering authority", "具工程背景的领队", 96),
        ("race-engineer", "Race Engineer", "赛车工程师", 88),
        ("performance-engineer", "Performance Engineer", "性能工程师", 80),
        ("strategy-engineer", "Strategy Engineer", "策略工程师", 78),
    ]
    leaders = [  # (team, leader) — all fictional
        ("apex-gp", "Sidney Leadman"), ("example-racing", "Frankie Principal"),
        ("placeholder-motorsport", "Ash Overseer"),
    ]
    write("series_engineering.json", {
        "last_verified": GEN,
        "scope_note_zh": "示例数据：完全虚构的系列与人员。",
        "driver_pairing_status": [{
            "team_id": "apex-gp", "engineer_id": "alex-example", "driver": "Sam Speedwell",
            "status": "confirmed", "status_zh": "官方确认", "certainty": "high",
            "note_zh": "示例数据：虚构车队页面公开列名。",
        }],
        "f1_team_engineering": {
            "scope_note_zh": "示例数据。", "correction_note_zh": "",
            "role_templates": [
                {"key": k, "title": title, "title_zh": zh, "importance_score": score,
                 "seniority_zh": "示例层级", "difficulty_zh": "高",
                 "publicity_zh": "示例公开度", "why_zh": "示例岗位说明。"}
                for k, title, zh, score in role_templates
            ],
            "teams": [
                {"team_id": tid, "leadership": [{
                    "role_zh": "Team Principal", "person": leader,
                    "person_zh": f"示例领队 {leader.split()[0]}",
                    "engineering_background_zh": "是，示例工程背景",
                    "importance_score": 95, "note_zh": "示例数据：虚构领队履历。",
                }]}
                for tid, leader in leaders
            ],
        },
        "motorsport_series": [
            {"id": "f1", "name": "Formula 1", "name_zh": "一级方程式", "season_label": "2026",
             "public_engineer_names_zh": "示例说明。", "coverage_zh": "示例覆盖说明。",
             "teams": [], "classes": ["F1"],
             "role_ladder": ["race-engineer", "performance-engineer", "strategy-engineer"]},
            {"id": "sample-junior", "name": "Sample Junior Series", "name_zh": "示例初级方程式",
             "season_label": "2026", "public_engineer_names_zh": "示例说明。",
             "coverage_zh": "示例覆盖说明。", "teams": ["Demo Junior Team"],
             "classes": ["SJ"], "role_ladder": ["race-engineer"]},
            {"id": "wec-le-mans", "name": "Example Endurance Series", "name_zh": "示例耐力系列赛",
             "season_label": "2026", "public_engineer_names_zh": "示例说明。",
             "coverage_zh": "示例覆盖说明。", "teams": [], "classes": ["Hypercar"],
             "role_ladder": ["car-race-engineer"]},
        ],
        "series_role_definitions": [
            {"key": "team-technical-director", "title_zh": "车队技术总监", "importance_score": 92,
             "seniority_zh": "高级管理", "difficulty_zh": "极高", "why_zh": "示例岗位说明。"},
            {"key": "data-engineer", "title_zh": "数据工程师", "importance_score": 70,
             "seniority_zh": "工程师", "difficulty_zh": "中", "why_zh": "示例岗位说明。"},
        ],
        "sources": [{"title": "Example Motorsport News", "url": f"{EX}/news/engineering-structures"}],
    })

    # -- one fictional junior-series roster (series_people.json) -------------
    members = [
        {"name": "Charlie Demo", "role": "Team Principal", "role_key": "team-principal",
         "role_group_zh": "管理 / 车队领导", "engineering_related": True, "confidence": "high",
         "notes_zh": "示例数据：虚构车队官网列名。"},
        {"name": "Sasha Specimen", "role": "Race Engineer", "role_key": "race-engineer",
         "role_group_zh": "赛车工程师", "engineering_related": True, "confidence": "high",
         "notes_zh": "示例数据：虚构车队官网列名。"},
        {"name": "Lee Dummy", "role": "Data Engineer", "role_key": "data-engineer",
         "role_group_zh": "数据工程师", "engineering_related": True, "confidence": "medium",
         "notes_zh": "示例数据：虚构车队官网列名。"},
    ]
    write("series_people.json", {
        "generated": GEN, "method_zh": "示例数据：手工构造的虚构名册。",
        "series": {"sample-junior": {"teams": [{
            "series_id": "sample-junior", "team_name": "Demo Junior Team",
            "source_url": f"{EX}/teams/demo-junior-team",
            "source_title": "Demo Junior Team - Example Site", "members": members,
        }]}},
    })

    # -- enrichment: one enriched profile + one unresolved lookup ------------
    write("series_people_enrichment.json", {
        "generated": GEN, "method_zh": "示例数据：虚构的公开档案富化。",
        "profiles": [{
            "series_id": "sample-junior", "team_name": "Demo Junior Team",
            "name": "Sasha Specimen", "role_key": "race-engineer",
            "career_entries": [
                {"from": "2012", "to": "2018", "org": "Placeholder Racing Developments",
                 "org_zh": "示例赛车研发公司", "role": "Junior Data Engineer", "role_zh": "初级数据工程师",
                 "category": "other", "category_zh": "其他",
                 "source_url": f"{EX}/profiles/sasha-specimen",
                 "source_title": "Sasha Specimen - Example Profiles"},
                {"from": "2019", "to": "present", "org": "Demo Junior Team",
                 "org_zh": "示例初级方程式车队", "role": "Race Engineer", "role_zh": "赛车工程师",
                 "category": "F2", "category_zh": "F2",
                 "source_url": f"{EX}/profiles/sasha-specimen",
                 "source_title": "Sasha Specimen - Example Profiles"},
            ],
            "public_profiles": [{"type": "profile", "url": f"{EX}/profiles/sasha-specimen",
                                 "title": "Sasha Specimen - Example Profiles",
                                 "confidence": "high", "evidence_zh": "示例数据：占位证据说明。"}],
            "education_entries": [{"institution": "Sampleton University",
                                   "institution_zh": "示例大学（Sampleton）", "degree": "BEng",
                                   "degree_zh": "工程学士", "field": "Motorsport Engineering",
                                   "field_zh": "赛车工程", "years": "2008-2012",
                                   "source_url": f"{EX}/profiles/sasha-specimen",
                                   "source_title": "Sasha Specimen - Example Profiles"}],
            "career_summary_zh": "示例数据：虚构人物的占位履历摘要。",
        }],
        "unresolved": [{"series_id": "sample-junior", "team_name": "Demo Junior Team",
                        "name": "Lee Dummy", "role_key": "data-engineer",
                        "note_zh": "示例数据：未找到可信公开档案（占位）。"}],
    })

    # -- series_rosters.json --------------------------------------------------
    write("series_rosters.json", {
        "generated": GEN,
        "series": {"sample-junior": {
            "source_url": f"{EX}/series/sample-junior/teams",
            "teams": [{"team_name": "Demo Junior Team",
                       "drivers": [{"name": "Ren Rookie", "number": "1"},
                                   {"name": "Nova Novice", "number": "2"}],
                       "logo_url": ""}],
        }},
    })

    # -- leader_profiles.json --------------------------------------------------
    write("leader_profiles.json", {
        "generated": GEN, "method_zh": "示例数据：虚构领队档案。",
        "people": {
            leader: {
                "photo_url": "", "source_url": f"{EX}/team/{slug(leader)}",
                "source_title": f"{leader} - Example Team Site", "photo_credit": "",
                "confidence": "high",
                "education": [{"institution": "Fictional Polytechnic",
                               "institution_zh": "示例职业技术学院（Fictional）",
                               "degree": "MSc", "degree_zh": "理学硕士",
                               "field": "Aerospace Engineering", "field_zh": "航空航天工程",
                               "years": "", "source_url": f"{EX}/team/{slug(leader)}",
                               "source_title": f"{leader} - Example Team Site"}],
                "education_lookup": "profile_found",
            }
            for _, leader in leaders
        },
    })

    # -- f1_public_engineering_people.json ------------------------------------
    write("f1_public_engineering_people.json", {
        "last_verified": GEN, "scope_zh": "示例数据：虚构的公开工程人员。",
        "sources": [{"title": "Example Motorsport News", "url": f"{EX}/news/engineering-structures"}],
        "teams": {
            "apex-gp": [{
                "person": "Dana Aeroford", "person_zh": "示例总监 Dana",
                "role_key": "technical-leadership", "role": "Technical Director",
                "role_zh": "技术总监", "importance_score": 95,
                "career_summary_zh": "示例数据：虚构技术总监履历摘要。",
                "note_zh": "示例数据：虚构人物。", "photo_url": "",
                "education": [{"institution": "Placeholder Institute of Technology",
                               "institution_zh": "示例理工学院（Placeholder）", "degree": "PhD",
                               "degree_zh": "博士", "field": "Aerodynamics", "field_zh": "空气动力学",
                               "years": "", "source_url": f"{EX}/profiles/dana-aeroford",
                               "source_title": "Dana Aeroford - Example Profiles"}],
                "education_lookup": "profile_found",
                "career": [{"from": "2010", "to": "present", "org": "Apex GP", "org_zh": "示例车队·Apex",
                            "role": "Technical Director", "role_zh": "技术总监",
                            "category": "F1", "category_zh": "F1"}],
                "sources": [{"url": f"{EX}/profiles/dana-aeroford", "type": "profile",
                             "title": "Dana Aeroford - Example Profiles"}],
                "confidence": "high",
            }],
            "example-racing": [{
                "person": "Kit Strategos", "person_zh": "示例策略主管 Kit",
                "role_key": "strategy-engineer", "role": "Head of Strategy",
                "role_zh": "策略主管", "importance_score": 80,
                "career_summary_zh": "示例数据：虚构策略主管履历摘要。",
                "note_zh": "示例数据：虚构人物。", "photo_url": "",
                "education": [], "education_lookup": "not_researched", "career": [],
                "sources": [{"url": f"{EX}/profiles/kit-strategos", "type": "profile",
                             "title": "Kit Strategos - Example Profiles"}],
                "confidence": "medium",
            }],
        },
    })

    # -- wec_le_mans_entries_2026.json (one fictional endurance entry) --------
    write("wec_le_mans_entries_2026.json", {
        "generated": GEN, "source_title": "Example Endurance Series entry list",
        "source_url": f"{EX}/endurance/entry-list", "source_published": GEN,
        "scope_zh": "示例数据：虚构耐力赛报名表。",
        "entries": [{
            "id": "wec-le-mans:hypercar:001", "series_id": "wec-le-mans",
            "class_name": "Hypercar", "car_number": "001",
            "entrant": "Sample Endurance Team", "source_championship": "SES",
            "nationality": "EXA", "tyre": "S", "car": "Example Hypercar EX-1", "misc": "",
            "drivers": [{"name": "Pat Fictitious", "country": "EXA", "rating": "P"},
                        {"name": "Drew Notreal", "country": "EXA", "rating": "G"}],
        }],
        "class_counts": {"Hypercar": 1},
    })

    # -- photos / ages / logos / run logs (empty-ish placeholders) ------------
    write("photos_merged.json", {})  # no photos: dashboard falls back to initials
    write("ages.json", {
        "_note": "Fictional sample ages (dob invented). approx flag demo included.",
        "alex-example": {"dob": "1990-03-14"},
        "casey-placeholder": {"birth_year": 1985, "approx": True},
    })
    write("team_logos.json", {"source_url": f"{EX}/logos", "light_bg": [],
                              "invert_on_dark": [], "teams": {}})
    write("search_runs.json", {"runs": [{
        "id": "sample-run-001", "run_at": GEN, "query": "sample fixture search",
        "tool": "none", "providers": [], "result_count": 0,
        "notes_zh": "示例数据：占位搜索记录。",
    }]})
    write("lookup_runs.json", {"note": "Fictional sample fixture.", "runs": [{
        "id": "sample-lookup-001", "run_at": GEN, "run_type": "sample",
        "target": "sample fixture", "tool": "none", "provider": "none",
        "result_count": 0, "status": "ok", "notes_zh": "示例数据：占位查询记录。",
    }]})

    print("sample dataset complete: data/sample/")


if __name__ == "__main__":
    main()
