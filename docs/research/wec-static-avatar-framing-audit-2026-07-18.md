# WEC static-avatar framing audit - 2026-07-18

This pass revisited five named WEC staff records whose exact public
professional profiles expose non-placeholder static images. MySearch/Exa was
used for exact-profile discovery. A portrait was adopted only when the profile
also matched the person's current team or role and the face remained
recognizable in the dashboard's 48px card and 96px detail-dialog renderings.

## Decisions

| Person | Identity evidence | Browser result | Decision |
| --- | --- | --- | --- |
| Thibaut Jouet | Duqueine No 1 Car Mechanic LMP2 | Face recognizable; background is busy | Adopted with display framing |
| Flavien Caprera | Stellantis Motorsport Chef d'equipe | Face clear at both sizes | Adopted with display framing |
| Claudio Valentini | Peugeot Senior Performance Engineer | Head and shoulders clear in the dialog | Adopted with display framing |
| Benjamin Sagnes | Racing Spirit performance/strategy history | Person remains tiny after framing | Rejected; profile data retained |
| Fabio Michelon | Iron Lynx Capo officina | Circle shows mostly car and pit environment | Rejected; profile data retained |

The rejected candidates are deliberately kept without a photo. A correct but
unreadable environmental image is not treated as a usable avatar.

## Sources

- [Thibaut Jouet public professional profile](https://fr.linkedin.com/in/thibaut-jouet-4b0507171)
- [Flavien Caprera public professional profile](https://fr.linkedin.com/in/flavien-caprera-4ba470200)
- [Claudio Valentini public professional profile](https://it.linkedin.com/in/claudio-valentini-85616b183)
- [Benjamin Sagnes public professional profile](https://fr.linkedin.com/in/benjamin-sagnes-a766a7221)
- [Fabio Michelon public professional profile](https://it.linkedin.com/in/fabio-michelon-4b1621113)

No video search, video frame or video thumbnail was used. The three adopted
images are stored locally so the dashboard does not depend on expiring remote
image URLs.

## Verification

All five source images were decoded before review. The dashboard was rebuilt
and inspected in a real Chromium browser. Regression coverage locks the three
accepted local paths and their display positions; rejected candidates continue
to render initials instead of a misleading or unreadable image.
