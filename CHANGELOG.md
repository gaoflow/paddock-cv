# Changelog

All notable public changes to Paddock CV are recorded here. The compiled
real-person dataset remains private; entries below describe public code,
methodology, schema and interface changes.

## [1.1.7] - 2026-07-18

### Added

- An AF Corse held-staff follow-up documenting four car-specific management,
  engineering, and mechanic additions plus two verified static portraits.

### Changed

- Full professional names are now retained when current race records use a
  shortened form, with role-title differences preserved in provenance notes.

## [1.1.6] - 2026-07-18

### Added

- A held-engineer follow-up documenting three medium-confidence WEC car-staff
  additions and two visually verified static portraits.

### Changed

- Expanded the namesake audit for a Manthey chief mechanic and recorded the
  exact local MySearch/Exa route used for profile and avatar discovery.

## [1.1.5] - 2026-07-18

### Added

- A WEC car-staff follow-up documenting three medium-confidence technical and
  sporting staff additions across 13 Autosport and Vista AF Corse.

### Changed

- Expanded namesake rejection notes for professional-profile and avatar
  candidates, including explicit evidence for keeping two single-source names
  on hold.

## [1.1.4] - 2026-07-18

### Added

- A source-level WEC follow-up documenting two newly verified car-specific
  technical staff records and one corrected static-avatar decision.

### Changed

- Avatar review now treats decoded initial tiles as placeholders even when an
  image search returns them as JPEG profile images.
- Corrected an earlier vehicle-only classification after the exact Iron Lynx
  profile image was downloaded and visually inspected again.

## [1.1.3] - 2026-07-18

### Added

- A WEC static-avatar audit recording three adopted portraits and two
  candidates rejected after real-browser card and dialog inspection.

### Changed

- Portrait acceptance now requires recognizable rendering at both dashboard
  avatar sizes; exact identity alone is insufficient for an environmental
  photograph with a very small subject.

## [1.1.2] - 2026-07-18

### Added

- A source-by-source Alpine Endurance Team roster audit documenting four
  verified 2026 Le Mans staff records, two car-specific assignments and four
  visually checked public static portraits.

### Changed

- Corrected three misspelled names inherited from the #35/#36 race sheets by
  cross-checking exact current professional profiles.
- Added regression coverage that prevents #35 and #36 personnel from being
  displayed on the wrong Alpine entry.

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

[1.1.7]: https://github.com/gaoflow/paddock-cv/releases/tag/v1.1.7
[1.1.6]: https://github.com/gaoflow/paddock-cv/releases/tag/v1.1.6
[1.1.5]: https://github.com/gaoflow/paddock-cv/releases/tag/v1.1.5
[1.1.4]: https://github.com/gaoflow/paddock-cv/releases/tag/v1.1.4
[1.1.3]: https://github.com/gaoflow/paddock-cv/releases/tag/v1.1.3
[1.1.2]: https://github.com/gaoflow/paddock-cv/releases/tag/v1.1.2
[1.1.1]: https://github.com/gaoflow/paddock-cv/releases/tag/v1.1.1
[1.1.0]: https://github.com/gaoflow/paddock-cv/releases/tag/v1.1.0
[1.0.0]: https://github.com/gaoflow/paddock-cv/releases/tag/v1.0.0
