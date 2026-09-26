# Brief: Site fixes for gabrielordonez.com

**Feature**: `001-site-fixes-for-gabrielordonez-com`

**Created**: 2026-09-25

## Input

The operator assessed `gogabrielordonez-github-io` and its site https://gabrielordonez.com and chose 12 finding(s) from the assessment to be done. Every idea below rests on a fact the gateway measured; the fact's own words are quoted. This brief is the input to `spec.md`: write the specification from it in the house style (Input, Decisions, Requirements as FR-###, Success criteria as SC-###, Out of scope).

## Ideas

### 1. Add Open Graph title, description, and image tags on the homepage so shared links show a preview card instead of a blank unfurl.

Advised by the assessment. Rests on `site.seo.og.home`: https://gabrielordonez.com/ has no Open Graph tags; a link to it shows no card.

### 2. Declare a canonical URL on the homepage, preferably https://gabrielordonez.com/, so search engines do not treat other paths as separate pages.

Advised by the assessment. Rests on `site.seo.canonical.home`: https://gabrielordonez.com/ declares no canonical URL.

### 3. Shorten the homepage meta description from 214 characters to about 150–160 so search snippets are not cut off.

Advised by the assessment. Rests on `site.seo.description.home`: https://gabrielordonez.com/ has a 214-character meta description; results cut at about 160.

### 4. Redirect index.html to / or give it a canonical pointing at the homepage so the two URLs stop competing in search.

Advised by the assessment. Rests on `site.seo.canonical.index-html`: https://gabrielordonez.com/index.html declares no canonical URL.

### 5. Only 8 pages rendered while 19 were skipped; fix crawl or render failures so project and blog URLs are actually reachable.

Advised by the assessment. Rests on `site.content.pages`: 8 page(s) rendered, 19 skipped.

### 6. Add Person or Organization and WebSite JSON-LD on the homepage so search engines receive structured data about you.

Advised by the assessment. Rests on `site.seo.jsonld.home`: https://gabrielordonez.com/ carries no JSON-LD; search engines are told nothing structured about the organisation.

### 7. Add Open Graph tags on index.html as well, or stop serving it as a duplicate of the homepage, so shares of that URL still get a card.

Advised by the assessment. Rests on `site.seo.og.index-html`: https://gabrielordonez.com/index.html has no Open Graph tags; a link to it shows no card.

### 8. You have 4 source files and no tests; add a few checks around critical scripts so regressions are caught before deploy.

Advised by the assessment. Rests on `code.files`: 4 source file(s) and 0 test file(s).

### 9. Add Open Graph tags on the blog index so the listing produces a title and image when shared.

Advised by the assessment. Rests on `site.seo.og.blog-html`: https://gabrielordonez.com/blog.html has no Open Graph tags; a link to it shows no card.

### 10. Add Open Graph tags on the RAG project page so portfolio links preview correctly when you share them.

Advised by the assessment. Rests on `site.seo.og.rag-project-html`: https://gabrielordonez.com/rag-project.html has no Open Graph tags; a link to it shows no card.

### 11. Add Open Graph tags on the RAG latency article so social and chat unfurls show a title and summary.

Advised by the assessment. Rests on `site.seo.og.blog-rag-latency-html`: https://gabrielordonez.com/blog/rag-latency.html has no Open Graph tags; a link to it shows no card.

### 12. Trim the index.html meta description to about 160 characters and keep it aligned with the homepage after you pick a canonical.

Advised by the assessment. Rests on `site.seo.description.index-html`: https://gabrielordonez.com/index.html has a 214-character meta description; results cut at about 160.

## Facts cited

- `site.seo.og.home` (parameter): https://gabrielordonez.com/ has no Open Graph tags; a link to it shows no card.
- `site.seo.canonical.home` (parameter): https://gabrielordonez.com/ declares no canonical URL.
- `site.seo.description.home` (parameter): https://gabrielordonez.com/ has a 214-character meta description; results cut at about 160.
- `site.seo.canonical.index-html` (parameter): https://gabrielordonez.com/index.html declares no canonical URL.
- `site.content.pages` (stock): 8 page(s) rendered, 19 skipped.
- `site.seo.jsonld.home` (parameter): https://gabrielordonez.com/ carries no JSON-LD; search engines are told nothing structured about the organisation.
- `site.seo.og.index-html` (parameter): https://gabrielordonez.com/index.html has no Open Graph tags; a link to it shows no card.
- `code.files` (stock): 4 source file(s) and 0 test file(s).
- `site.seo.og.blog-html` (parameter): https://gabrielordonez.com/blog.html has no Open Graph tags; a link to it shows no card.
- `site.seo.og.rag-project-html` (parameter): https://gabrielordonez.com/rag-project.html has no Open Graph tags; a link to it shows no card.
- `site.seo.og.blog-rag-latency-html` (parameter): https://gabrielordonez.com/blog/rag-latency.html has no Open Graph tags; a link to it shows no card.
- `site.seo.description.index-html` (parameter): https://gabrielordonez.com/index.html has a 214-character meta description; results cut at about 160.

