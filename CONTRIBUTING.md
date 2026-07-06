# Contributing to paddock-cv

Thanks for your interest. Ground rules first, then the practical bits.

## The one hard rule

**Never submit real people's personal data to this repository.** No real
names, career histories, photos, LinkedIn URLs, or datasets built from them —
not in code, not in fixtures, not in issues. The public repo runs exclusively
on the fictional sample dataset. PRs that add real-person data will be closed
and the commits scrubbed.

If you believe content already in this repo identifies a real person
inappropriately, open an issue titled `[removal]` or email the maintainer —
it will be handled with priority.

## What contributions are welcome

- **Methodology improvements** — better source patterns, new identity-binding
  heuristics, sharper stop conditions. These live in `docs/`.
- **Pipeline fixes** — `scripts/*.py` correctness, portability, performance.
- **Dashboard fixes** — `web/index.html` (single file, no build step; keep it
  that way). UI translations live in the `I18N` dict in the same file.
- **Sample-data schema fixes** — keep `scripts/make_sample_data.py`
  structurally identical to what `build_data.py` expects.
- **Test coverage** — `tests/` asserts structure against the sample dataset,
  never real names.

## Dev setup

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

## PR checklist

- [ ] `npm test` passes against the sample dataset
- [ ] No real-person data anywhere in the diff
- [ ] No absolute paths, usernames, or machine-specific config
- [ ] New behaviour covered by a test if it's testable

## Style

Match what's there. The codebase favours small, boring, readable code over
abstractions. One file per concern; comments only where the code can't speak.
