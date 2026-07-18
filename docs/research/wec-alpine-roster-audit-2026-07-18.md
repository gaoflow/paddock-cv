# Alpine Endurance Team roster audit - 2026-07-18

This pass audited the public 2026 Le Mans team sheets for Alpine A424 cars
#35 and #36. It used car-number-specific race records as the assignment source,
then resolved each name against an exact public professional profile. Medium
confidence records are included when the race assignment and professional
identity agree.

## Adopted records

| Person | Current public role | Car scope | Decision |
| --- | --- | --- | --- |
| Giuseppe Bizzoca | Team Manager / Deputy CEO | Team | Added; race-sheet spelling `Giuseppe Bizoun` corrected. |
| Arnaud Pouzineau | Chief Mechanic / Car Chief | #35 | Added; race-sheet spelling `Arnaud Pouzinem` corrected. |
| Lucas Planchenault | Data Acquisition Engineer | #35 | Added; race-sheet spelling `Luca Planchessault` corrected. |
| Matthieu Mégy | Chief Mechanic / Car Chief | #36 | Added from matching race-sheet and current Car Chief evidence. |

David Ladouce was already present, but his display-only `assignment` value did
not restrict him to a Le Mans entry. The source record now also carries
`entry_number: "35"`, which prevents him from appearing on car #36.

## Sources

- [2026 Le Mans Alpine A424 #35 team sheet](https://24h-en-piste.com/en/AfficherDetails.php?Annee=2026&Numero=35&Type=Course)
- [2026 Le Mans Alpine A424 #36 team sheet](https://24h-en-piste.com/en/AfficherDetails.php?Annee=2026&Numero=36&Type=Course)
- [Giuseppe Bizzoca public professional profile](https://fr.linkedin.com/in/giuseppe-bizzoca-b82a2165)
- [Arnaud Pouzineau public professional profile](https://fr.linkedin.com/in/arnaud-pouzineau-558310183)
- [Lucas Planchenault public professional profile](https://fr.linkedin.com/in/lucasplanchenault/en)
- [Matthieu Mégy public professional profile](https://fr.linkedin.com/in/matthieu-m%C3%A9gy-606604210)

MySearch/Exa was used to discover and compare the exact profiles. Four
non-placeholder static profile images were downloaded and visually checked
before adoption. No video, video frame, thumbnail, ambiguous group image or
same-name candidate was used.

## Verification

The generated JSON and SQLite database were rebuilt. Regression coverage now
asserts the #35/#36 entry boundaries and the four local portrait paths. A real
browser render was captured for both Alpine entry cards to confirm that the
portraits load and remain recognizable.
