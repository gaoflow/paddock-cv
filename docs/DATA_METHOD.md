# Data Methodology

This project treats education, career path, photo identity, and source traceability as first-class data. The UI should not imply that a person has no public background just because one search path failed.

Detailed Chinese operating rules for roster discovery and photo adoption live in
[SEARCH_LOGIC.md](SEARCH_LOGIC.md). That document is the working checklist for
MySearch / Firecrawl searches, LinkedIn public-snippet handling, medium-confidence
people, Instagram image downloads, and local photo verification.

## Research Cascade

For each series, team, department, role, and public person:

1. Official team or series page: current role, title, team affiliation, official image.
2. LinkedIn public result: profile URL, public snippet, education or job fragments visible without login.
3. University or alumni page: education, degree, course, projects, and career interviews.
4. F1 / FIA / championship official article: role changes, appointments, team structures.
5. Specialist motorsport media: captioned photos, department roles, career profiles.
6. Wikipedia / Wikidata: identity disambiguation, image candidates, structured education facts.
7. Image search only as a last step, and only when the image page or caption explicitly identifies the person.

## LinkedIn Handling

LinkedIn is an important source, but it is not a general bulk-data API for third-party member profiles.

- Official LinkedIn Profile API access is restricted and requires LinkedIn approval.
- Profile API calls require an authenticated access token and are for the authenticated member, subject to that member's privacy settings.
- Project data must not store Profile API data for other LinkedIn members unless a future approved workflow obtains valid consent.
- LinkedIn public search snippets can be stored as source evidence when visible without login.
- LinkedIn URLs are stored as source links and cross-checking leads, not as proof by themselves when a stronger official/university source exists.

LinkedIn source states:

- `profile_found`: public profile URL and visible snippet match the target identity.
- `snippet_only`: search/index snippet exposes limited facts, but no full public page is accessible.
- `false_positive_ignored`: a same-name profile was found but does not match the motorsport person.
- `blocked_or_login_required`: a profile probably exists but the content requires login.
- `searched_no_public_result`: searches were run and no reliable match was found.

## Photo Handling

Do not use a face image unless the source page, filename, caption, page title, or official profile unambiguously identifies the person.

Photo states:

- `confirmed_official`: team, series, FIA/F1, university, or person profile image.
- `confirmed_captioned_media`: editorial image with caption naming the person.
- `wikimedia_confirmed`: Wikimedia/Wikipedia page image for the same person.
- `group_or_driver_shared`: image is valid but includes a driver or group.
- `identity_ambiguous`: image exists but cannot be safely attributed.
- `searched_no_confirmed_photo`: searched but no safe photo found.

## Department Coverage

For F1, do not stop at named heads. Build from:

`Team -> department -> public role -> person -> education -> career -> source state`.

Core F1 departments to enumerate:

- Team management and technical leadership
- Race engineering and trackside operations
- Vehicle performance
- Strategy and race strategy
- Aerodynamics
- Design / chassis / mechanical design
- Simulation, modelling, simulator, and test
- Systems, controls, electronics, and software
- Power unit / powertrain integration
- Tyres, brakes, and trackside aero performance

If a department exists but no reliable public member name is found, keep it as an unresolved research gap in the database, not as homepage explanatory text.

## Database Rule

Every person row should preserve:

- current role and team
- education entries with school, degree, field, years, source type
- career entries with year range, organization, role, and category
- photo state and source
- LinkedIn state and URL when found
- unresolved gaps when search was attempted but not confirmed
