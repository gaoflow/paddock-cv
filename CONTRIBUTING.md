# Contributing to paddock-cv

Thanks for your interest. Two very different kinds of contribution are
welcome — read the right section.

## 1. Contributing people information (encouraged!)

**This is the most valuable thing you can contribute.** One person's search
reach is limited; if you know something the dataset is missing, please share
it — open a **GitHub Issue** using the *Person info* template (or any issue
titled `[person] Name — Team`):

- who: name, team, role, series/season
- what you know: career step, education, a photo that actually identifies
  them, a role change, a correction to something the live site shows
- **source link(s)** — the one hard requirement. Official team pages,
  editorial interviews, university alumni features, public LinkedIn profiles
  are all great. "I heard" is not usable; a URL is.

What happens next: the maintainer verifies it against the sourcing rules in
[docs/SEARCH_METHODOLOGY.md](docs/SEARCH_METHODOLOGY.md) and merges it into
the **private dataset** that powers [paddockcv.com](https://paddockcv.com).
Person data lives in issues and on the site — it is not stored in this
repository's files, which is why you contribute it via an issue rather
than a PR. Corrections and removal requests about anyone already on the
live site are handled the same way, with priority.

## 2. Contributing code & methodology (PRs)

- **Methodology improvements** — better source patterns, new identity-binding
  heuristics, sharper stop conditions. These live in `docs/`.
- **Pipeline fixes** — `scripts/*.py` correctness, portability, performance.
- **Dashboard fixes** — `web/index.html` (single file, no build step; keep it
  that way). UI translations live in the `I18N` dict in the same file.
- **Sample-data schema fixes** — keep `scripts/make_sample_data.py`
  structurally identical to what `build_data.py` expects.
- **Test coverage** — `tests/` asserts structure against the sample dataset.

Note that PRs should not add real-person data to the repo's *files* — the
repo ships only the fictional sample dataset (see the README data notice).
Real-person info goes through issues (§1) into the private dataset.

### Dev setup

```bash
python3 scripts/make_sample_data.py
F1E_DATA_DIR=data/sample python3 scripts/build_data.py
F1E_DATA_DIR=data/sample python3 scripts/seed_db.py
F1E_DATA_DIR=data/sample python3 server.py            # http://localhost:8000

# tests
npm install && npx playwright install chromium
npm test
```

Python is stdlib-only by design — don't add pip dependencies without a very
good reason. The frontend is one HTML file with no build step — likewise.

### PR checklist

- [ ] `npm test` passes against the sample dataset
- [ ] No absolute paths, usernames, or machine-specific config
- [ ] New behaviour covered by a test if it's testable
- [ ] Role taxonomy changes include a primary-source responsibility or careers link
- [ ] PR title describes the user-facing or research outcome

PRs run the public sample build and browser suite. Maintainer release PRs use
GitHub auto-merge: the `test` check must pass, then GitHub squash-merges the
branch and deletes it. Releases summarize substantive changes from the merged
PRs; timestamp-only and formatting-only churn is not part of the release process.

### Style

Match what's there. The codebase favours small, boring, readable code over
abstractions. One file per concern; comments only where the code can't speak.
