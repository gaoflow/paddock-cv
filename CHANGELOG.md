# Changelog

All notable public changes to Paddock CV are recorded here. The compiled
real-person dataset remains private; entries below describe public code,
methodology, schema and interface changes.

## [1.1.1] - 2026-07-18

### Changed

- Person details now use native modal-dialog semantics with an accessible
  title, initial close-button focus and keyboard focus containment.
- Opening a profile locks background scrolling and removes the underlying
  dashboard from keyboard interaction; closing restores both state and focus.
- Mobile regression coverage now verifies that profile dialogs remain within
  the viewport margins.

## [1.1.0] - 2026-07-16

### Added

- A primary-source-backed taxonomy of 26 F1 engineering role families.
- Machine-readable sample taxonomy in `data/sample/f1_role_taxonomy.json`.
- A dedicated `birth_year` field in the SQLite people table; displayed ages
  are calculated from the current calendar year during each data build.
- Research guidance for team aliases, title aliases, department reverse
  searches, confidence handling and MySearch-assisted discovery.
- Public regression coverage for the expanded role taxonomy.

### Changed

- F1 team cards show only publicly identified people instead of presenting
  unresolved research cells as unnamed incumbents.
- Technical leadership, design, aerodynamics, performance, simulation,
  controls, tyres and reliability are rendered as distinct career domains.
- Person details no longer repeat entry-route analysis or summary fact tags;
  age remains visible when a sourced birth year is available.
- Public release contributions now use checked, auto-merged pull requests.

## [1.0.0] - 2026-07-06

- Initial public release of the five-series career-path dashboard.
- Fictional sample dataset, SQLite seed layer and Playwright regression suite.
- Research, sourcing, identity-binding and data-publication methodology.

[1.1.1]: https://github.com/gaoflow/paddock-cv/releases/tag/v1.1.1
[1.1.0]: https://github.com/gaoflow/paddock-cv/releases/tag/v1.1.0
[1.0.0]: https://github.com/gaoflow/paddock-cv/releases/tag/v1.0.0
