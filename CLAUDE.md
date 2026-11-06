# CLAUDE.md — NIKA Docs Repo Guide

This file is for LLM assistants working in this repository. It covers the docs structure, newsletter production workflow, and SEO guidance.

---

## Repo overview

This is a **Mintlify** documentation site for NIKA (The Spatial Computing Co.) at `docs.nikaplanet.com`. It is a Mintlify v3 app configured via `docs.json`. Pages are written in MDX. The site covers NIKA's product suite: NIKA Desktop, NIKA Planet (cloud GIS), NIKA Mobile, and NIKA GeoEngine.

**Key files:**
- `docs.json` — Mintlify config: navigation, theme, colours, integrations
- `CLAUDE.md` — this file
- `newsletter/` — email and LinkedIn newsletter drafts (gitignored, not part of the Mintlify build)
- `nika-planet/changelog.mdx` — the product changelog, in Mintlify `<Update>` format
- `nika-desktop/memory-core.mdx` — NIKA Memory Core (spatial knowledge base) feature docs

---

## Newsletter folder

All newsletter materials live in `newsletter/`. This directory is in `.gitignore` and is **not referenced in `docs.json` navigation**, so Mintlify never builds, indexes, or serves any files from it. You can safely add HTML, TXT, and script files here without affecting the docs site or its SEO. For linkedin newsletter purpose, include a LinkedIn post caption as .txt too, e.g.
```
March 2026 has been a productive month for NIKA products, including map legends, large vector tiling layer support and many more! 🗺️ 🗾 
Subscribe to our newsletter to get up-to-date with latest geo innovations.
```

---

## Design System

Before creating the content, fetch this design file, read its readme, and implement the relevant aspects of this company design. https://api.anthropic.com/v1/design/h/1RzZxy9Piu_qDuJEi4nwRQ

## Writing Sender.net HTML emails

### Hard constraints (enforce these every time)

1. **No SVG tags anywhere.** Sender.net's editor strips `<svg>` and shows an error. Any illustration, icon, or diagram must be built entirely with HTML `<div>`, `<table>`, and CSS. Use CSS `border-radius`, `background-color`, `border`, and absolute positioning to create shapes. Unicode characters (e.g. `⚙` for a gear) are fine.

2. **No inline SVG route lines or shape paths.** Even a small inline `<svg>` for a dashed polyline will break rendering. Replace with a CSS dashed border on a `<div>` instead.

3. **Unsubscribe link format.** Sender.net requires this exact Liquid tag pair — do not use any other format:
   ```html
   <a href="{{unsubscribe_link}}">{{unsubscribe_text}}</a>
   ```

4. **Subscriber personalisation.** To greet subscribers by first name, use Sender.net's Liquid syntax:
   ```html
   Hi {{ firstname | default: "there" }}!
   ```

5. **Multi-column layout must use HTML tables**, not CSS flexbox or grid. Email clients (especially Outlook) do not reliably support flexbox. Use `<table width="100%" cellpadding="0" cellspacing="0" border="0">` for any side-by-side layout.

6. **Absolute positioning for illustrations.** For HTML/CSS illustrations, use a `position:relative` outer `<div>` with a fixed `height` and `overflow:hidden`, and `position:absolute` children. This renders consistently across Gmail, Apple Mail, and Sender.net's preview. However, be aware that iPhone Mail may not render `background-color` on `<div>` elements reliably — use contrasting element colours (borders, text) so illustrations are legible even if background colours fail.

7. **All styles must be inline.** Use a `<style>` block in `<head>` for structural classes, but rely on inline `style=""` attributes for anything layout-critical. Many email clients strip `<style>` blocks.

### Brand identity (apply consistently)

| Element | Value |
|---|---|
| Brand name | **NIKA** (not NikaPlanet, not Nika Planet) |
| Tagline | The Spatial Computing Co. |
| Website | nikaplanet.com |
| Docs | docs.nikaplanet.com |
| Booking link | https://cal.com/lawrence-nika/nika-expert |
| Contact email | info@nikaplanet.com |
| LinkedIn | https://www.linkedin.com/in/xdl/ |

**Colours:**
| Name | Hex | Usage |
|---|---|---|
| Dark teal | `#003646` | Header background, CTA button, version badges |
| Lime | `#c5ff5a` | Accent, CTA text, active indicators, NIKA wordmark |
| Muted blue | `#7fb8c8` | Subtitle text, section labels |
| Deep dark | `#001824` | Illustration backgrounds |
| Mid dark | `#001e2c` | Illustration blocks, secondary elements |
| Light grey | `#f0f4f4` | Email outer background, footer |

**Standard header block** (copy exactly into every email):
```html
<div style="background-color:#003646;padding:28px 40px 24px;">
  <div style="font-size:36px;font-weight:800;color:#c5ff5a;letter-spacing:0.06em;line-height:1;">NIKA</div>
  <div style="font-size:11px;color:#7fb8c8;letter-spacing:0.16em;text-transform:uppercase;margin-top:6px;">The Spatial Computing Co.</div>
</div>
```

**Standard footer block:**
```html
<div class="footer">
  <div class="footer-logo">NIKA</div>
  <p class="footer-text">
    You're receiving this because you're subscribed to NIKA product updates.<br/>
    <a href="{{unsubscribe_link}}">{{unsubscribe_text}}</a> &nbsp;·&nbsp; <a href="https://nikaplanet.com">nikaplanet.com</a>
  </p>
  <p class="footer-text" style="margin-top:10px;">NIKA &bull; The Spatial Computing Co.</p>
</div>
```

### Changelog content source

Pull changelog items from `nika-planet/changelog.mdx`. The format is Mintlify `<Update label="DATE" description="VERSION">`. For a given month's newsletter, include all `<Update>` entries from that calendar month. Each entry becomes an `update-item` block in the email.

For changelog images, the base URL is `https://docs.nikaplanet.com/` — prepend this to any image path found in the MDX (e.g. `/nika-planet/changelog-images/2026-03-24-1.jpg` → `https://docs.nikaplanet.com/nika-planet/changelog-images/2026-03-24-1.jpg`).

### Tag colour classes
```html
<span class="tag tag-new">New</span>        <!-- green -->
<span class="tag tag-improvement">Improvement</span>  <!-- blue -->
<span class="tag tag-fix">Fix</span>        <!-- yellow -->
```

### NIKA Memory Core / knowledge base programme
- **Do not use the product name "NIKA Memory Core" in email body copy.** Refer to it as "the knowledge base" or "a queryable, location-aware knowledge base".
- Link to the docs page: `https://docs.nikaplanet.com/nika-desktop/memory-core`
- Programme details: 30 organisation slots; first 5 teams get direct setup support and priority access.
- CTA label: **"Secure the slot →"**, link: `https://cal.com/lawrence-nika/nika-expert`

---

## Writing LinkedIn newsletter articles

LinkedIn's article editor **does not accept HTML**. Paste plain text only, then use the editor toolbar to apply formatting (bold, headings, bullets, links).

### Pasting into LinkedIn without losing formatting

LinkedIn's article editor strips all formatting when you paste from a `.txt` file or a plain text editor — you end up with a wall of unstyled Normal text and have to reformat everything by hand.

**The fix:** Create a `-copypaste.html` file alongside each article. This is a minimal styled HTML page (not a Sender.net email — no brand constraints apply) that the user opens in a browser and copies from. When rich text is pasted from a browser, LinkedIn preserves headings, bold, bullets, and links automatically.

**Workflow:**
1. Open the `-copypaste.html` file in Chrome or Safari
2. Press `Cmd+A` (Mac) / `Ctrl+A` (Windows) to select everything
3. Press `Cmd+C` / `Ctrl+C` to copy
4. Click into the LinkedIn article body and paste — formatting carries over
5. Set the article title separately in LinkedIn's Title field (it's a separate input above the body)

**How to write the copypaste HTML:**
- Use semantic tags only: `<h2>` for major headings (LinkedIn renders as "Heading"), `<h3>` for subheadings, `<p>` for body, `<strong>` for bold, `<em>` for italic, `<ul>/<li>` for bullets, `<a href="">` for links
- Include a yellow instructions box at the top (the user can ignore it or it gets stripped on paste)
- No brand colours, no email layout, no tables — this file is never sent anywhere, just opened locally as a paste source

**Naming convention:** `{month}-{year}-linkedin-copypaste.html` — e.g. `march-2026-linkedin-copypaste.html`

### Format of the `.txt` article files

Each file has:
```
TITLE:
[The article title — goes in LinkedIn's Title field]

BODY (paste from here):
[Everything below this line is pasted into the article body]
```

### Content conventions

- **Length:** 600–1,000 words. Technical + narrative mix. Open with a human observation or quote, then move to product content, then close with a CTA or thought.
- **Sections:** Use short all-caps labels as dividers (e.g. `---` + `What shipped in March`) — these can be formatted as headings in LinkedIn's editor.
- **Changelog items:** List version, brief heading, and 1–3 sentences per item. No HTML tags. Use plain text arrows (`→`) or line breaks for structure.
- **Links:** Write out full URLs in plain text. LinkedIn article editor allows hyperlinking text once pasted.
- **Tone:** Direct, grounded, technically confident. NIKA's voice doesn't hype — it describes precisely what changed and why it matters. Avoid marketing superlatives.
- **Byline:** End with a short 2-sentence author bio identifying NS as NIKA's founder.

### LinkedIn newsletter series setup
- Series name: **NIKA Product Updates** (or similar)
- Cadence: monthly, published after each batch of changelog items
- Publish on: Tuesday–Thursday, 8–10 AM in the audience's primary time zone
- After publishing: post about the newsletter on the company page and as a personal post from the founder account — LinkedIn personal accounts have much higher organic reach than company pages

---

## Mintlify build — does the `newsletter/` directory affect the site?

**No.** Mintlify only builds and serves pages that are explicitly listed in the `navigation` object in `docs.json`. The `newsletter/` folder is not referenced there. Even if it were committed and pushed, Mintlify would ignore every file in it. The `.gitignore` entry is belt-and-suspenders hygiene.

If you ever want to confirm: check that no path starting with `newsletter/` appears anywhere in `docs.json`.

---

## Improving Mintlify docs SEO

### What Mintlify handles automatically
- Sitemap at `/sitemap.xml` (pages in navigation only)
- `robots.txt`
- Meta tags from frontmatter (`title`, `description`)
- OpenGraph tags (`og:title`, `og:image`, `og:description`)
- LLM discovery files (`/llms.txt`, `/llms-full.txt`)
- Mobile-responsive layout

### docs.json additions to make

```json
{
  "seo": {
    "indexing": "all"
  },
  "integrations": {
    "googleAnalytics": {
      "measurementId": "G-XXXXXXXXXX"
    }
  }
}
```

Add `"indexing": "all"` to ensure all navigation pages are included. Add Google Analytics to track real search traffic, bounce rate, and which docs pages drive most visits.

### MDX page frontmatter — every page should have all three

```yaml
---
title: "Vector Tile Rendering for Large Geospatial Datasets — NIKA"
description: "How NIKA automatically converts large vector datasets into vector tiles for fast, scalable map rendering without manual processing."
"og:image": "https://docs.nikaplanet.com/images/og-default.png"
---
```

Rules:
- `title`: 50–60 characters. Lead with the specific feature or task, not the brand name. Target the long-tail keyword a GIS practitioner would actually search.
- `description`: 120–155 characters. One sentence describing what the page teaches or solves.
- `og:image`: Use a consistent default OG image across docs. Create one branded 1200×630px image and reference it everywhere until you have page-specific ones.
- Do **not** set `noindex: true` on any public-facing product page.

### Content strategy for ranking

Mintlify's technical SEO is solid out of the box. The ranking gap is almost entirely content. Focus on:

- **Problem-first titles:** "How to query spatial records within a radius in NIKA" outranks "Map Query API". Think: what would a GIS analyst or ecologist type into Google?
- **Heading hierarchy:** Use H2 for major sections, H3 for sub-steps. Put the target keyword in at least one H2.
- **Internal links with descriptive anchor text:** `[see the vector tile rendering guide](/nika-planet/nika-map)` not `[click here](/nika-planet/nika-map)`.
- **Long-tail keyword targets for NIKA specifically:** "biodiversity net gain habitat mapping software", "vector tile rendering GeoJSON", "spatial knowledge base for ecology firms", "GIS notebook Python cloud", "field survey data management ecology".
- **Changelog as SEO content:** The changelog page (`/nika-planet/changelog`) is a real SEO asset — each update entry adds long-tail content. Keep descriptions specific and keyword-rich (feature names, file formats, workflows mentioned by name).

---

## Cross-promoting the LinkedIn newsletter from Sender.net emails

Every HTML email should include a section (or at minimum a footer callout) that drives subscribers toward the LinkedIn company page and newsletter. This creates a two-way audience funnel: email readers become LinkedIn followers and newsletter subscribers, and vice versa.

### Redirect link convention

Rather than embedding a raw LinkedIn URL (which is long and ugly), use a Mintlify redirect so you control the destination and can track clicks. Add an entry to `docs.json` under the `redirects` key:

```json
"redirects": [
  { "source": "/linkedin", "destination": "https://www.linkedin.com/company/nikaplanet" },
  { "source": "/newsletter", "destination": "https://www.linkedin.com/newsletters/nika-product-updates-XXXXXXXXXX" }
]
```

This gives you clean, memorable links:
- LinkedIn company page → `https://docs.nikaplanet.com/linkedin`
- LinkedIn newsletter → `https://docs.nikaplanet.com/newsletter`

Replace `XXXXXXXXXX` with the numeric ID LinkedIn assigns when you create the newsletter series. Update `docs.json` once and all email links automatically follow.

### HTML block to add to every Sender.net email

Place this immediately above the footer, as the last section before `<!-- FOOTER -->`. It is a single-column callout using the standard section styling:

```html
<!-- LINKEDIN CALLOUT -->
<div style="background:#f8fafb;border-top:1px solid #eef0ee;padding:28px 40px;text-align:center;">
  <p style="margin:0 0 6px;font-size:12px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#7fb8c8;">Also on LinkedIn</p>
  <p style="margin:0 0 16px;font-size:14px;color:#374151;line-height:1.65;">
    We publish this newsletter on LinkedIn too — subscribe there to get future issues directly in your LinkedIn feed.
  </p>
  <table cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;">
    <tr>
      <td style="padding-right:10px;">
        <a href="https://docs.nikaplanet.com/newsletter"
           style="display:inline-block;background:#0a66c2;color:#ffffff;text-decoration:none;font-size:13px;font-weight:700;padding:10px 20px;border-radius:6px;letter-spacing:0.02em;">
          Subscribe on LinkedIn →
        </a>
      </td>
      <td>
        <a href="https://docs.nikaplanet.com/linkedin"
           style="display:inline-block;background:#ffffff;color:#003646;text-decoration:none;font-size:13px;font-weight:700;padding:10px 20px;border-radius:6px;border:1px solid #003646;letter-spacing:0.02em;">
          Follow NIKA
        </a>
      </td>
    </tr>
  </table>
</div>
```

Notes on this block:
- Uses LinkedIn blue (`#0a66c2`) for the primary CTA — intentional signal that this goes to LinkedIn, not a NIKA page.
- The `Follow NIKA` button uses the NIKA dark teal border style.
- Both links go through `docs.nikaplanet.com` redirects so you can update destinations without touching every past email template.
- No SVG, no flexbox — table layout, safe for all email clients.

### Minimal footer variant

If you want a lighter touch instead of a full section, add this single line inside the existing footer `<p class="footer-text">` block:

```html
<a href="https://docs.nikaplanet.com/newsletter">Subscribe on LinkedIn</a> &nbsp;·&nbsp;
<a href="https://docs.nikaplanet.com/linkedin">Follow us</a> &nbsp;·&nbsp;
```

Insert it before the existing unsubscribe link.

---

### Known Mintlify SEO limitations

| Gap | Workaround |
|---|---|
| No JSON-LD schema markup generated | Inject `<script type="application/ld+json">` manually in MDX frontmatter for high-value pages (landing, getting started) |
| Analytics UI is AI-chat-focused | Use Google Analytics 4 for proper traffic and SEO funnel data |
| No built-in link validation | Add a GitHub Action to check for broken internal links before deploy |
| Sitemap excludes access-controlled pages | Fine for public docs; just ensure all public pages are in `navigation` |

---

## OnlyMap JS pages track a released package — keep them in step

The six pages under `onlymap/` restate the public surface of `@nika-js/onlymap`,
which releases often (seventeen releases between 0.8.0 and 0.10.9 in one month). The
core repo has no way to update this site, so the pages rot silently: they sat at 0.8.0
while the core shipped projected maps, shaded relief, geometry transforms, curved
labels, SVG export, print finishes, fallback frame sources and atlas paging — none of
which this site mentioned. A claim that "the docs were updated" is only true if
`git log -- onlymap/` says so.

**Which page restates what:**

| Page | Restates |
|---|---|
| `onlymap/overview.mdx` | the layer-type count and roster; every headline feature with its `<sup>new in X</sup>` tag; the Roadmap (anything shipped must LEAVE it) |
| `onlymap/authoring.mdx` | `<om-map>`/`<om-layer>` attributes, data sources, Cartographic Maps, Print Finishes, legends, exports, validation |
| `onlymap/cartographs.mdx` | the cartograph entry: frames and their sources, atlas, export, credit; **the CDN pin in its install snippet** |
| `onlymap/licensing-and-telemetry.mdx` | free-plan limits, the badge and `keep-badge`, the sheet credit |
| `onlymap/react-native.mdx`, `onlymap/remotion.mdx` | the two sibling packages, each with its own version |
| `geoengine/onlymap-fullstack.mdx`, `scripts/geoengine-docs/onlymap-demo.html` (re-run `build_diagrams.py` after editing) | the OnlyMap side of the NIKA GeoEngine pairing: **two more CDN pins**, plus the `COGLayer`/`ZarrLayer`, `refresh` and `OmMap.configureData` behaviour it describes (including that raster layers do not route through `configureData`) |

**The ritual, on every core release** (or when asked to "update the docs"):

1. Find what shipped: `git -C ../OmniMap log --oneline` is not enough — read
   `CHANGELOG.md` in the core repo from the version this site last documented
   forward. Every `### Added` bullet is a claim this site must make; every `### Changed`
   bullet may make a sentence here wrong; every `### Fixed` bullet is a workaround an
   author may have learned that they can now drop.
2. Touch every page in the table that restates the affected surface. Tag new
   capabilities `<sup>new in X.Y.Z</sup>`, the house convention.
3. Move the CDN pins in `onlymap/cartographs.mdx`, `geoengine/onlymap-fullstack.mdx` and
   `scripts/geoengine-docs/onlymap-demo.html` (then re-run `build_diagrams.py`) to the released version. A stale pin
   teaches the reader to install a version without the feature documented beside it.
4. Check mechanically, not from memory: `grep -rn "onlymap@0\." onlymap/ geoengine/ scripts/geoengine-docs/` must show only
   the current version (plus the historical "0.6.19 or later" note in the overview), and
   a grep for each new attribute or element name from the changelog must find at least
   one page.
5. Commit with the core version in the subject, e.g. `docs(onlymap): 0.10.9 — …`, so
   `git log -- onlymap/` is the record of what this site covers.

Source material is already written and verified in the core repo — `docs/*.md`,
`llms.txt`, `skills/onlymapjs/` — so condense from it rather than rewriting from memory.

---

## NIKA GeoEngine (Kubernetes) diagrams are generated

The SVGs in `images/geoengine/` (one light and one dark file per diagram) are built from
`scripts/geoengine-docs/diagrams.py`. Edit that file, then run
`python3 scripts/geoengine-docs/build_diagrams.py` from the repo root; never hand-edit the SVGs.
Pages embed them with plain `<img>` tags (`block dark:hidden` / `hidden dark:block`), so
they are server-rendered, cached across pages and cost no JavaScript. The only global CSS is
the ~2 KB `geoengine.css` (the overview title chip, the phone/desktop diagram swap and the chart slots);
keep it that small, because Mintlify inlines every root `.css` file into every page. The interactive charts on
`geoengine/observability.mdx` live in `snippets/geoengine/charts.jsx` and inject their own
styles only on that page. Mintlify does not serve `.html` files in production (they 404), so the
OnlyMap demo is embedded as an iframe `srcDoc` from the generated `snippets/geoengine/onlymap-demo.jsx`. "NIKA GeoEngine" is the Kubernetes product; the command-line tool is
"NIKA GeoEngine CLI" (pages under `nika-geoengine/` and `guides/custom-geoprocess-*`).
