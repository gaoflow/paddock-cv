# WEC Algarve Pro Racing roster follow-up - 2026-07-18

## Scope

This pass targeted the two least-covered 2026 Le Mans entrants in the current
dataset: Algarve Pro Racing and CrowdStrike Racing by APR. MySearch/Exa was
used through the local `127.0.0.1:9874` proxy, while MySearch/Firecrawl
extracted the current car records that reject direct `curl` requests.

Medium-confidence people are included when a current race record or exact
current professional profile binds the person to APR and a technical role.
Only public static images were considered. No video, video frame, reel, or
video thumbnail was searched or used.

## Added current car staff

| Person | Published English role | Evidence | Confidence |
| --- | --- | --- | --- |
| Dan Jones | `Data Acquisition / LMP2 Systems & Data Engineer, car #25` | The [2026 #25 record](https://www.24h-en-piste.com/en/AfficherDetails.php?Annee=2026&Numero=25&Type=Course) lists `Data acquisition`; his [exact current profile](https://uk.linkedin.com/in/dan-jones-67115a153) lists `Systems & Data Engineer - LMP2` at APR from December 2025. | high |
| Jesus Rios Rueda | `Chief Mechanic, car #25` | The current [#25 record](https://www.24h-en-piste.com/en/AfficherDetails.php?Annee=2026&Numero=25&Type=Course) lists `Chief mechanic`. The official [2025 ELMS Pit Stop Challenge list](https://storage.googleapis.com/doc-prod/_6dw84zezO1fiyC7-uZmkd1z.pdf) and its 2024 predecessor also list him as an APR mechanic. | medium |
| Mark Holton | `Chief Mechanic, car #4` | The current [#4 record](https://www.24h-en-piste.com/en/AfficherDetails.php?Annee=2026&Numero=4&Type=Course) lists `Chief mechanic`; APR car records from [2023](https://www.24h-en-piste.com/en/AfficherDetails.php?Annee=2023&Numero=45&Type=Course) and 2019 list the same name and role. | medium |
## Added team-level mechanics

| Person | Current profile role | Independent team evidence | Confidence |
| --- | --- | --- | --- |
| André Pitaça | [APR / Algarve Pro Racing Team Race mechanic](https://linkedin.com/in/andr%C3%A9-pita%C3%A7a-62475888), March 2024-present | Official 2025 ELMS list: APR #25 mechanic | medium |
| Fábio Pimenta | [Algarve Pro Racing Race Mechanic](https://pt.linkedin.com/in/frpmnt), July 2020-present | Official 2025 ELMS list: APR #20 mechanic | medium |
| Pablo Compagnucci Montejo | [Algarve Pro Racing LMP2 Freelance Motorsport Technician](https://linkedin.com/in/pablocompag), January 2022-present | Official 2024 and 2025 ELMS lists: APR #20 mechanic | medium |
| Alexandre Gary | [Algarve Pro Racing Race Mechanic](https://fr.linkedin.com/in/alexandre-gary-445149186), January 2026-present | Current profile specifies `LMP2 Second Mechanic Gunner` | medium |
| Adrian Pedrero | [Algarve Pro Racing Motorsport Mechanic](https://es.linkedin.com/in/adrian-pedrero-751973223), April 2023-present | Current profile and first-person posts bind APR, LMP2 and Le Mans work | medium |

These three records are team-level assignments. A current Le Mans car number
is not inferred from an earlier ELMS pit-stop list.

## Avatar decisions

- Pablo Compagnucci Montejo: adopted. His exact current professional profile
  exposes a clear 200 x 200 head-and-shoulders static portrait.
- Alexandre Gary: adopted with face-focused display framing. The exact current
  profile image is a single-person team work portrait with his face visible.
- Adrian Pedrero: adopted. The exact current profile exposes a clear 200 x 200
  single-person paddock selfie.
- Fábio Pimenta: adopted with face-focused display framing. The exact profile
  image is a 200 x 200 single-person paddock photograph; his face remains
  recognizable in the rendered detail dialog.
- André Pitaça: rejected. The exact-profile image is a dark helmeted work
  scene, and his face is not legible at 48 px or 96 px.
- Dan Jones, Jesus Rios Rueda, and Mark Holton: initials only.
  No attributable static portrait passed review; namesake and generic images
  were not substituted.

Georgiy Berezin remains held. The current #4 record is the only motorsport
identity result, while all exact-name profiles found belong to unrelated
retail, ice-hockey, or fencing namesakes. That is low rather than medium
confidence, so the name is not promoted into the roster.

All adopted files are local so the dashboard does not depend on expiring
signed CDN URLs. The four adopted portraits were rendered in the real central
profile dialog before release; the avatar and name bounds also retain a clear
gap rather than overlapping.
