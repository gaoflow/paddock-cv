# WEC Racing Team Turkey by TF follow-up - 2026-07-18

## Scope

This pass audited the current 2026 Le Mans #34 Racing Team Turkey by TF staff
table against the source roster. Direct HTML extraction was used after
Firecrawl returned its keyless rate-limit response. The failure was not treated
as a negative search result.

Only public static portraits were eligible. No video, video frame, reel, or
video thumbnail was searched or used.

## Added person

| Person | Published English role | Evidence | Confidence |
| --- | --- | --- | --- |
| Jonathan Lynn | `Technical Director / Sporting Director, car #34` | The [current #34 record](https://www.24h-en-piste.com/en/AfficherDetails.php?Type=Course&Annee=2026&Numero=34) writes `John O’Lynn`. Jonathan Lynn's exact current profile says he leads TF Sport's engineering department as Sporting Director / Race Engineer across WEC, ELMS and ALMS; the #33 record uses the full Jonathan Lynn spelling. The source variation is preserved without creating a duplicate person. | medium |

Jonathan Lynn reuses the existing locally stored profile portrait whose public
post author identity, current TF Sport role announcement, download, and visual
inspection were already verified.

## Existing assignment validated

Chris Gregory was already projected from the TF Sport source member into the
#34 card through the shared `33 / 34` entry mapping. The current #34 record
directly lists him as Chief mechanic; the #33 record repeats the duty, 2018,
2019 and 2025 TF Sport Le Mans records establish continuity, and
[BAM Motorsport Management](https://bammotorsportmanagement.com/faceoff-racing-by-florian-kaltenbach/)
credits him as TF Sport 1st Mechanic. This pass adds team-specific profile
evidence but deliberately does not create a second Chris Gregory row.

## Avatar recheck

- Rob Courtneidge: the exact public Instagram avatar remains a dark, blurred
  100 x 100 image that does not work at dashboard size.
- Blake Adamson: the exact current TF Sport profile still exposes the platform
  default avatar. A current personal post image could not be downloaded from
  its signed URL and did not establish a person-position key.
- Chris Gregory: the exact-name LinkedIn result belongs to a US construction
  operations executive. Motorsport results show cars, drivers, or production
  credits without an attributable clear portrait.

All three candidates were rejected. No namesake or ambiguous group photograph
was assigned merely to reduce the visible gap count.

## Result

Racing Team Turkey by TF rises from five to six displayed people. Its verified
portrait count rises from two to three by correctly reusing Jonathan Lynn's
existing local portrait in the #34 context. The final Playwright browser check
showed exactly one Jonathan Lynn and one Chris Gregory row, with the local
portrait loaded in the centered profile modal.
