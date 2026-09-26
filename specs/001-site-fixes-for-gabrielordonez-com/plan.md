# Plan: Site fixes for gabrielordonez.com

## Epics

| Epic | Scope | Depends on |
|---|---|---|
| E1 – Meta tags & canonical | Shorten meta descriptions on `index.html` (both `/` and `/index.html`). Add `<link rel="canonical">` on `/` and `/index.html` both pointing to `/`. | — |
| E2 – Open Graph tags | Add `og:title`, `og:description`, `og:image` to every public page: `/`, `index.html`, `blog.html`, `rag-project.html`, `blog/rag-latency.html`. | E1 (OG description must match the shortened meta description) |
| E3 – JSON-LD structured data | Embed `Person` and `WebSite` schemas on `/`. | — |
| E4 – Crawl/render fixes | Diagnose why 19 of 27 URLs were skipped. Fix broken internal links, missing files, or server errors so the 9 known reachable URLs (spec FR-05) return HTTP 200. | E1, E2, E3 (rebuild after source changes), E5 (verify deploy) |
| E5 – Verification | Write source-level assertions (canonical present, OG tags present, meta description length, JSON-LD types) that pass against built HTML. | E1, E2, E3 |

## Phases

### Phase 0 — Foundation (input read, plan written)

**Artifacts produced**

| Artifact | File |
|---|---|
| Plan (this file) | `specs/001-site-fixes-for-gabrielordonez-com/plan.md` |

### Phase 1 — Source changes

**E1 – Meta tags & canonical**

1. Edit `index.html`:
   - Shorten `<meta name="description">` from 214 chars to 150–160 chars (keep identical for both `/` and `/index.html` treatments — the same file serves both).
   - Add `<link rel="canonical" href="https://gabrielordonez.com/" />` in `<head>`.

Affected file: `index.html`.

**E2 – Open Graph tags**

1. In `index.html`: add `og:title` (matches `<title>`), `og:description` (matches shortened description), `og:image` (`https://gabrielordonez.com/og-image.jpg`).
2. In `blog.html`: add same three OG tags, matching that page's `<title>` and `<meta name="description">`.
3. In `rag-project.html`: add same three OG tags, matching that page's `<title>` and `<meta name="description">`.
4. In `blog/rag-latency.html`: add same three OG tags, matching that page's `<title>` and `<meta name="description">`.

Affected files: `index.html`, `blog.html`, `rag-project.html`, `blog/rag-latency.html`.

**E3 – JSON-LD structured data**

1. In `index.html` `<head>`, embed a `<script type="application/ld+json">` block containing:
   - `@type: Person` with `name: "Gabriel Ordonez"`, `url: "https://gabrielordonez.com/"`
   - `@type: WebSite` with `name: "Gabriel Ordonez"`, `url: "https://gabrielordonez.com/"`

Affected file: `index.html`.

### Phase 2 — Crawl/render diagnosis (implement after source changes)

1. Manually `curl` or open each URL in FR-05 to confirm HTTP 200.
2. For any that fail, trace the link graph: find what internal links point to the broken URL and fix them, or create the missing file.
3. If the issue is hosting configuration (e.g. GitHub Pages not serving a path), document the fix; hosting config changes are out of scope for this repo.

### Phase 3 — Verification

1. Write a shell script or Node script that:
   - Reads each built HTML file.
   - Asserts canonical `<link>` present on `/` and `/index.html`.
   - Asserts `og:title`, `og:description`, `og:image` on each OG-tagged page.
   - Asserts meta description length is 150–160 on homepage and `index.html`.
   - Asserts JSON-LD contains `Person` and `WebSite` with expected `name` and `url`.

No test runner dependency — simple assertions that exit 0 on pass.

## Risks

- The meta description content itself: the spec says "shorten to 150–160 chars" but does not prescribe the new text. The implementor must reword without losing meaning. A draft should be reviewed.
- Crawl/render failures (E4) may reveal missing pages or broken links that require creation of new files, which touches the out-of-scope boundary. If a page referenced by the site does not exist at all, the implementor should flag it rather than create it.
- No `og:image` asset exists at `https://gabrielordonez.com/og-image.jpg` — the implementor should create a minimal 1200×630 PNG or use an existing image asset.
