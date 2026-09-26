# Feature Specification: Site fixes for gabrielordonez.com

**Feature Branch**: `001-site-fixes-for-gabrielordonez-com`

**Created**: 2026-09-25

**Status**: Draft

## Input

These are the ideas and the facts they rest on. The fact's own words are quoted.

1. **OG tags on homepage** — Rests on `site.seo.og.home`: https://gabrielordonez.com/ has no Open Graph tags; a link to it shows no card.
2. **Canonical URL on homepage** — Rests on `site.seo.canonical.home`: https://gabrielordonez.com/ declares no canonical URL.
3. **Shorten homepage meta description** — Rests on `site.seo.description.home`: https://gabrielordonez.com/ has a 214-character meta description; results cut at about 160.
4. **Canonical URL on index.html** — Rests on `site.seo.canonical.index-html`: https://gabrielordonez.com/index.html declares no canonical URL.
5. **Fix crawl/render failures** — Rests on `site.content.pages`: 8 page(s) rendered, 19 skipped.
6. **JSON-LD on homepage** — Rests on `site.seo.jsonld.home`: https://gabrielordonez.com/ carries no JSON-LD; search engines are told nothing structured about the organisation.
7. **OG tags on index.html** — Rests on `site.seo.og.index-html`: https://gabrielordonez.com/index.html has no Open Graph tags; a link to it shows no card.
8. **Add tests** — Rests on `code.files`: 4 source file(s) and 0 test file(s).
9. **OG tags on blog index** — Rests on `site.seo.og.blog-html`: https://gabrielordonez.com/blog.html has no Open Graph tags; a link to it shows no card.
10. **OG tags on RAG project page** — Rests on `site.seo.og.rag-project-html`: https://gabrielordonez.com/rag-project.html has no Open Graph tags; a link to it shows no card.
11. **OG tags on RAG latency article** — Rests on `site.seo.og.blog-rag-latency-html`: https://gabrielordonez.com/blog/rag-latency.html has no Open Graph tags; a link to it shows no card.
12. **Trim index.html meta description** — Rests on `site.seo.description.index-html`: https://gabrielordonez.com/index.html has a 214-character meta description; results cut at about 160.

## Decisions

1. The canonical URL for the site shall be `https://gabrielordonez.com/`.
2. `index.html` shall canonicalise to `/` rather than be redirected, so existing links to `index.html` still resolve.
3. Open Graph tags added across pages shall follow the [Open Graph protocol](https://ogp.me/) with at minimum `og:title`, `og:description`, and `og:image`.
4. JSON-LD on the homepage shall use `Person` and `WebSite` schemas from schema.org.
5. The project is a static site (no server-side rendering), so all changes shall be applied at build time or directly in static HTML / templates.

## Requirements

| ID | Description | Traces to |
|---|---|---|---|
| FR-01 | Add `og:title`, `og:description`, and `og:image` meta tags to the homepage (`index.html` served at `/`). `og:title` must match the page's `<title>`. `og:description` must match the page's `<meta name="description">` (shortened per FR-03). `og:image` must be `https://gabrielordonez.com/og-image.jpg` (or an existing image asset at that URL). | Idea 1, fact `site.seo.og.home` |
| FR-02 | Declare a `<link rel="canonical" href="https://gabrielordonez.com/" />` on the homepage. | Idea 2, fact `site.seo.canonical.home` |
| FR-03 | Shorten the homepage `<meta name="description">` to between 150 and 160 characters. | Idea 3, fact `site.seo.description.home` |
| FR-04 | On `index.html`, declare a `<link rel="canonical" href="https://gabrielordonez.com/" />`. Must not redirect. | Idea 4, fact `site.seo.canonical.index-html` |
| FR-05 | Make these URLs reachable and return HTTP 200 with the page content: `https://gabrielordonez.com/`, `https://gabrielordonez.com/index.html`, `https://gabrielordonez.com/blog.html`, `https://gabrielordonez.com/rag-project.html`, `https://gabrielordonez.com/blog/rag-latency.html`, `https://gabrielordonez.com/blog/llm-trust.html`, `https://gabrielordonez.com/blog/ai-theory-practice.html`, `https://gabrielordonez.com/genai-search-project.html`, `https://gabrielordonez.com/llm-eval-project.html`. This requirement covers only existing pages (from the brief and the skipped-page inventory); it does not require creating new pages or changing hosting configuration. | Idea 5, fact `site.content.pages` |
| FR-06 | Embed JSON-LD structured data with `Person` and `WebSite` schemas on the homepage. The `Person` object must include `name` ("Gabriel Ordonez") and `url` ("https://gabrielordonez.com/"). The `WebSite` object must include `name` ("Gabriel Ordonez") and `url` ("https://gabrielordonez.com/"). | Idea 6, fact `site.seo.jsonld.home` |
| FR-07 | Add `og:title`, `og:description`, and `og:image` meta tags to `index.html`. Values must match FR-01 (identical to homepage). | Idea 7, fact `site.seo.og.index-html` |
| FR-08 | The canonical `<link>` is present on both `/` and `/index.html` with `href="https://gabrielordonez.com/"`. Each page that adds OG tags (FR-01, FR-07, FR-09, FR-10, FR-11) has the three required OG tags. Each meta description (homepage and `index.html`) is 150–160 characters. The homepage JSON-LD contains `@type` values `Person` and `WebSite`. These assertions must be verified against the source or built HTML. | Idea 8, fact `code.files` |
| FR-09 | Add `og:title`, `og:description`, and `og:image` meta tags to `blog.html`. `og:title` must match the page's `<title>`. `og:description` must match the page's `<meta name="description">`. `og:image` must be `https://gabrielordonez.com/og-image.jpg`. | Idea 9, fact `site.seo.og.blog-html` |
| FR-10 | Add `og:title`, `og:description`, and `og:image` meta tags to `rag-project.html`. `og:title` must match the page's `<title>`. `og:description` must match the page's `<meta name="description">`. `og:image` must be `https://gabrielordonez.com/og-image.jpg`. | Idea 10, fact `site.seo.og.rag-project-html` |
| FR-11 | Add `og:title`, `og:description`, and `og:image` meta tags to `blog/rag-latency.html`. `og:title` must match the page's `<title>`. `og:description` must match the page's `<meta name="description">`. `og:image` must be `https://gabrielordonez.com/og-image.jpg`. | Idea 11, fact `site.seo.og.blog-rag-latency-html` |
| FR-12 | Shorten the `index.html` meta description to between 150 and 160 characters and keep it identical to the homepage meta description. | Idea 12, fact `site.seo.description.index-html` |

## Success criteria

| ID | Description |
|---|---|---|
| SC-01 | A shared link to `https://gabrielordonez.com/` renders a card with title, description, and image on major platforms (Twitter, LinkedIn, Slack). |
| SC-02 | `https://gabrielordonez.com/` advertises a canonical URL of `https://gabrielordonez.com/`. |
| SC-03 | The homepage meta description is between 150 and 160 characters. |
| SC-04 | `https://gabrielordonez.com/index.html` advertises `<link rel="canonical" href="https://gabrielordonez.com/" />` and is not redirected. |
| SC-05 | Each URL in FR-05 returns HTTP 200 with page content (verified by crawl or manual check). |
| SC-06 | The homepage HTML contains JSON-LD with `Person` and `WebSite` schemas, each with `name` and `url` as specified in FR-06. |
| SC-07 | A shared link to `https://gabrielordonez.com/index.html` renders a card with title, description, and image. |
| SC-08 | The canonical `<link>` is present on `/` and `/index.html` with `href="https://gabrielordonez.com/"`. Each OG-tagged page has `og:title`, `og:description`, and `og:image`. Meta descriptions on homepage and `index.html` are 150–160 characters. Homepage JSON-LD contains `Person` and `WebSite` with `name` and `url`. These are verified by inspecting source or built HTML. |
| SC-09 | A shared link to `https://gabrielordonez.com/blog.html` renders a card with title, description, and image. |
| SC-10 | A shared link to `https://gabrielordonez.com/rag-project.html` renders a card with title, description, and image. |
| SC-11 | A shared link to `https://gabrielordonez.com/blog/rag-latency.html` renders a card with title, description, and image. |
| SC-12 | The `index.html` meta description is between 150 and 160 characters and is identical to the homepage meta description. |

## Out of scope

- Server-side redirects (the site is static; any redirect must be implemented via HTML canonical or static hosting configuration).
- Changes to site design, layout, or content beyond the meta tags, structured data, and fixes needed to make the URLs in FR-05 reachable.
- Adding new pages, blog posts, or projects that do not already exist in the repository.
- Performance optimisation unrelated to crawl/render failures.
- HTTPS, DNS, or hosting infrastructure changes.
