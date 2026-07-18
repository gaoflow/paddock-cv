# WEC Akkodis ASP / Heart of Racing roster follow-up - 2026-07-18

## Scope

This pass revisited current 2026 Le Mans car staff and team-level personnel for
Akkodis ASP Team and Heart of Racing / Prodrive. Medium-confidence people are
included when an exact current professional profile closes the team and role
identity chain. Car-specific duties remain restricted to their entry number.

Only public static portraits were eligible. No video frame, video thumbnail or
extracted video image was adopted.

## Added people

| Person | Published English role | Evidence | Confidence |
| --- | --- | --- | --- |
| Edward Warnett | `Technical Director / Chief Race Engineer - AMR, car #23` | The [2026 #23 car record](https://www.24h-en-piste.com/en/AfficherDetails.php?Annee=2026&Numero=23&Type=Course) lists `Ed Warnet` as Technical director. His [exact professional profile](https://uk.linkedin.com/in/edward-warnett-44429086) gives the full spelling Edward Warnett and a current Prodrive `Chief Race Engineer` role responsible for AMR Vantage GT3 track performance and development. | high |
| Victor Derain | `Car Engineer / Track Engineer, car #87` | The [2026 #87 car record](https://www.24h-en-piste.com/en/AfficherDetails.php?Annee=2026&Numero=87&Type=Course) lists Victor Derain as Car engineer. The [2024 #87 record](https://www.24h-en-piste.com/en/AfficherDetails.php?Annee=2024&Numero=87&Type=Course) independently records the same person and car under Data acquisition, establishing continuity. | high |
| Bruno Ricard | `Mechanic, Akkodis ASP Team` | His [exact professional profile](https://www.linkedin.com/in/bruno-ricard-2b56374a) lists a current Akkodis ASP Team Mechanic role from February 2015. This is a team-level role; no car number is inferred. | medium |
| Johann Beganton | `Race Mechanic / Apprentice Competition Vehicle Technician` | His [exact professional profile](https://fr.linkedin.com/in/johann-beganton) uses the headline `Race mechanic` and lists a current Akkodis ASP Team `Apprenti technicien développeur véhicules de compétition` role from September 2024. This is a team-level role; no car number is inferred. | medium |

## Avatar decisions

Three exact-profile images were downloaded as 200 x 200 JPEG files, decoded,
assembled into a contact sheet and inspected at original resolution:

- Edward Warnett: clear single-person paddock portrait, face unobstructed.
- Bruno Ricard: clear single-person team portrait, face unobstructed.
- Johann Beganton: clear single-person working photograph with a recognizable
  side profile.

All three images are stored locally under `web/img/`; the signed CDN URLs are
not used by the dashboard. Edward Warnett's Instagram profile image was also
inspected in a real browser and rejected because it is a group image without a
position key. Victor Derain remains without an avatar because no static image
could be bound to him without person-position ambiguity.

## Tool state

MySearch was operational through `127.0.0.1:9874`. The old SOP command initially
failed before making a request because macOS system Python 3.9 does not support
`dataclass(slots=True)`. Running the same client with the installed Python 3.11
restored Tavily, Firecrawl and Exa access. Firecrawl then extracted the current
#23, #78 and #87 pages even though direct `curl` requests returned HTTP 403.

This failure was treated as a local client-runtime problem, not as a negative
search result.
