# WEC Iron Lynx roster follow-up - 2026-07-18

## Scope

This pass audited the thin source roster for Team Qatar by Iron Lynx and then
ran a reverse current-employee search against the operating organisation,
Iron Lynx Motorsport Lab. MySearch/Exa was called through the local
`127.0.0.1:9874` proxy. Firecrawl reached the current #62 page but returned its
keyless rate-limit response, which was not treated as a negative result.

Only public static portraits were eligible. No video, video frame, reel, or
video thumbnail was searched or used.

## Projection audit

The Team Qatar source object contains four direct people, but the rendered #62
card also receives Matteo Selva and Fabio Michelon through their existing
`entry_number: 62` assignments in the Iron Lynx roster. Those two people were
not duplicated. The new records below remain at Iron Lynx team level because
their current profiles do not identify a specific #61 or #62 assignment.

## Added personnel

| Person | Published English role | Current evidence | Confidence |
| --- | --- | --- | --- |
| Lorenzo Bruni | `Performance Engineer` | Exact current profile says Iron Lynx Motorsport Lab from January 2026; headline also identifies performance and data engineering. | medium |
| Davide Noè | `Race and Performance Engineer, WEC / ELMS` | Exact current profile says Iron Lynx from January 2026 and explicitly states `Race and Performance Engineer for WEC and ELMS 2026`. | medium |
| Rubén Casanova | `Race Engineer and Strategist` | Exact current profile says Iron Lynx from January 2021 and explicitly lists WEC, ELMS, GT World Challenge Europe and IMSA. | medium |
| Giorgio Ferro | `Team Manager` | Exact current profile says Iron Lynx Team Manager from January 2023. This team-level role does not replace Alice Menin's #62 duty. | medium |

The Iron Lynx public company profile independently lists Rubén Casanova among
current employees and describes the organisation's active WEC and ELMS work.
MySearch was used for discovery; each adopted record retains its exact public
professional profile URL as evidence.

## Avatar decisions

The exact public profile images for Lorenzo Bruni, Rubén Casanova and Giorgio
Ferro were downloaded as 200 x 200 JPEG files. All three are clear,
single-person static photographs and were inspected together in a contact
sheet before being copied to `web/img/`.

Davide Noè's exact current profile image is a valid motorsport photograph, but
he is wearing a full-face helmet and his face cannot be identified at avatar
size. It was rejected rather than using an unhelpful image merely to reduce the
gap count.

## Result

Iron Lynx rises from seven to eleven source members. Three of the four new
people have verified local static portraits. Team Qatar's existing cross-entry
rows remain unique and no unsupported car assignment was introduced.
