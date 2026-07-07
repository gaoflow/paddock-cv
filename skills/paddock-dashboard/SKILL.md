---
name: paddock-dashboard
description: Build a Paddock-CV-style roster dashboard — an Apple-dark, single-file, dependency-free people directory with collapsible series sections, team cards, person rows, a full-page CV drawer with shareable hash links, and instant client-side search. Use when creating a team/people directory, org-chart browser, or any grouped-roster UI with per-person detail pages.
---

# Paddock dashboard: layout & search

The layout and search system behind [paddockcv.com](https://paddockcv.com)
(`web/index.html` in this repo — one HTML file, zero runtime dependencies).
Follow this skill to reproduce the pattern or extend this repo consistently.

## Layout system

### Page anatomy (top to bottom)

```
header.top            sticky 56px, rgba(0,0,0,.88) + backdrop blur, hairline bottom
  .logo               brand slashes + wordmark (16px / 600)
  .tabs               view switcher — text pills, active = filled pill (--s3)
  .langsel            language <select>, pill shaped
  .searchbox          pill input, right-aligned, "/" hint chip
.hero                 eyebrow (14px muted) → h1 clamp(34–56px)/600/-1px → sub (20px muted)
.seriesboard          one .rostersection per series
  .series-toggle      full-width button: chevron + h3 (24px/600) + mono meta line
  .rostergrid         3-up → 2-up (≤1080px) → 1-up (≤640px), 16px gap
    .rosterteam       the team card
footer                hairline top, muted small text
#drawer               full-page CV overlay (position:fixed; inset:0)
```

### Design tokens (Apple-dark)

```css
--canvas:#000; --s1:#161617; --s2:#1d1d1f; --s3:#272729; --carbon:#2a2a2c;
--hair:#2d2d2f; --hair2:#3d3d41;
--ink:#f5f5f7; --ink2:#d2d2d7; --ink3:#a1a1a6; --ink4:#86868b;
--accent:#2997ff;            /* the ONE interactive blue (focus: #0071e3) */
--a1..--a6                   /* data-coding hues: one clear color per series/route */
```

Rules that make it read "Apple": cards are `--s2` on black with **no borders**
(hierarchy comes from surface steps, hover = `--s3`); radius 18px for cards,
12px for rows/chips inside cards, 9999px for pills; type is the system stack
(SF Pro), headlines 600 with negative tracking, body 400; sentence case
everywhere — no letterspaced uppercase.

### Team card (`.rosterteam`)

```
.rosterhd   grid: [3px team-color mark] [logo] [name + drivers line]
.posblock   one per role slot:
  .postitle 12px/600 muted label with hairline underneath (bilingual: zh + en)
  .personrow | .unknownrow ("No name found" keeps empty slots honest)
```

Team identity carries the color system: every team has an official primary
color in the data (`t.color`). It drives the header mark, the person-row hover
tint, and the CV drawer stripe. Set it once per row as a CSS custom property:

```html
<div class="personrow" style="--tc:#FF8000">
```
```css
.personrow{--tc:var(--accent)}                     /* fallback */
.personrow:hover{background:color-mix(in srgb, var(--tc) 14%, var(--s2))}
.personrow::after{content:'›'; color:var(--tc); opacity:0}  /* affordance */
```

Team logos: colorful official marks render directly on the dark canvas;
near-black monochrome marks use a white variant on a rounded chip filled with
`color-mix(in srgb, <team color> 72%, #000)`. White-background source images
(no transparent version available) are rescued with
`filter:invert(1) hue-rotate(180deg); mix-blend-mode:screen` — never put a
background on that element (the filter would invert it too).

### Person row (`.personrow`)

48px circular avatar + name line (name 15px/500, zh suffix in `.zh` span with
a 6px gap — always a space between Latin and CJK) + role line (13.5px muted).
Avatars are `background-image` divs lazy-loaded by an IntersectionObserver;
photo-less people get initials on their team color. Serve small (~112px)
thumbnails for rows — browsers downscaling a large photo 8x look crunchy.

### CV drawer (`#p/<person-id>` hash routing)

Full-page overlay, not a modal: `position:fixed; inset:0; background:var(--canvas)`
with `opacity/transform` transition and `visibility 0s` on close (Playwright
counts `opacity:0` as visible — `visibility:hidden` is what actually hides it).

- Open pushes `#p/<id>` via `history.pushState`; boot + `popstate` call
  `openPersonFromHash()` — every CV is a shareable deep link.
- Header: 3px team-color stripe, 96px avatar (+ license credit), display name
  (clamp 30–44px/600), role, team · drivers, then fact chips (pills).
- Body grid: `minmax(0,1fr) 320px` — career timeline / route / highlights /
  notes in the main column, education + sources in the side rail. Timeline is
  a hairline rail with color-coded dots (`--a1..--a6` by category) + mono years.

## Search

One input filters everything, live, with zero index or library:

```js
rosterSearch.addEventListener("input", e => renderRosterBoard(e.target.value));
document.addEventListener("keydown", e => {          // "/" focuses search
  if (e.key === "/" && !/input|textarea|select/i.test(document.activeElement?.tagName || "")) {
    e.preventDefault(); rosterSearch.focus();
  }
});
```

- **Haystack, not fields**: each team card concatenates team name (en+zh),
  drivers, every member's name / zh name / nicknames / role strings, then does
  one lowercase `includes(query)`. Cheap, typo-tolerant enough, bilingual for
  free.
- **Filter at the card level**: a matching team keeps its whole card (context
  beats surgical row-filtering in a roster UI).
- **Re-render, don't toggle**: `renderRosterBoard(filter)` rebuilds section
  HTML from data on every keystroke — at ~500 people this is faster and less
  buggy than DOM show/hide bookkeeping.
- Collapsed sections stay collapsed; matches show per-series so users see
  *where* someone is, not just that they exist.

## Checklist when extending

1. New colored element on a person? Use `var(--tc)` (team color), not a new hue.
2. New label? Sentence case, `--ink4`, hairline under it — no uppercase tracking.
3. New surface? Next step on the ladder (`--s2` → `--s3`), never a border.
4. New person field? Add it to the search haystack too.
5. Mixed Latin + CJK string? Keep a space at the boundary (`cjks()` helper).
6. Test contract lives in `tests/` — update assertions when a design decision
   deliberately changes (logo variant, drawer layout), never delete them.
