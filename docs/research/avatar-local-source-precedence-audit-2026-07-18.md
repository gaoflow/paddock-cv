# Avatar local-source precedence audit - 2026-07-18

## Problem

The production image materializer reported ten unavailable remote images on
every deployment. The frontend already preferred `photo.local`, so these people
were not actually falling back to initials, but the deployment process still
retried expired RocketReach, Instagram and Facebook `src_img` URLs stored as
provenance beside the verified local files.

This produced misleading `unavailable (render as initials)` output, unnecessary
network requests and stale remote cache entries.

## Affected records

| Person | Series / team | Verified local asset |
| --- | --- | --- |
| Miguel Angel Galvez Chicon | WEC / Team Qatar By Iron Lynx | `miguel-angel-galvez-chicon-rocketreach.jpg` |
| Alvaro Formoso Cruz | F2 / Campos Racing | `alvaro-formoso-cruz-public-profile.jpg` |
| Ben Scott | Formula E / Envision Racing | `ben-scott-envision-racing-third-party-people-directory.jpg` |
| Loup-Brann Licata | F2 / PREMA Racing | `loup-brann-licata-prema-rocketreach.jpg` |
| Justine Peutat | F2 / ART Grand Prix | `justine-peutat-instagram.jpg` |
| Thomas Owezareck | F2 / MP Motorsport | `thomas-owezareck-mp-instagram.jpg` |
| Ivan Rodriguez Bonet | F2 / PREMA Racing | `ivan-rodriguez-bonet-instagram.jpg` |
| Charlaine Robert Fondeville | WEC / Akkodis ASP Team | `charlaine-robert-fondeville-instagram.jpg` |
| Oier Bañuelos Arteagoitia | F2 / DAMS Lucas Oil | `oier-banuelos-dams-facebook.jpg` |
| Checco Ravera | WEC / Vista AF Corse | `checco-ravera-facebook.jpg` |

All ten files exist in `web/img`, decode as JPEG images and were reviewed in a
contact sheet. Each contains a visible person and none is a placeholder or a
broken payload.

## Fix

`scripts/materialize_imgcache.py` now checks whether a dictionary's `local`
path resolves to a real file under `web/`. When it does, the sibling remote
`src_img` remains in the data as provenance but becomes an alias to that local
file. The URL is excluded from the remote materialization queue, and any
duplicate payload occurrence that only contains `src_img` resolves through the
same local alias.

Remote images without a local file and all remote logos continue to be cached
as before. A regression test walks the generated payload and proves that no
remote `src_img` paired with an existing local file is returned by
`payload_urls()`.

## Result

The ten expired URLs no longer enter the remote image cache or generate failed
network requests. `imgmap.js` points them directly to the verified local
full-size images and their generated 112-pixel thumbnails.
