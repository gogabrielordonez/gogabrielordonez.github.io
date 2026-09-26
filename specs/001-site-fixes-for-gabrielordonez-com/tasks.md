# Tasks: Site fixes for gabrielordonez.com

Each task is checked by `tests/check_site.py` (the check with the same id).
A ticked task whose check fails turns the project's check red.

## Phase 1 — Homepage (`index.html`)

- [ ] T001 Shorten the `index.html` meta description to 150–160 characters; `/` and `/index.html` are the same file (FR-03, FR-12)
- [ ] T002 Add `<link rel="canonical" href="https://gabrielordonez.com/" />` to the `<head>` of `index.html` (FR-02, FR-04)
- [ ] T003 Add `og:title` to `index.html`, equal to its `<title>` (FR-01, FR-07)
- [x] T004 Add `og:description` to `index.html`, equal to its meta description (FR-01, FR-07)
- [x] T005 Create the link-preview card: `og-image.html` at the repository root, a 1200×1200 page in the site's colours with "Gabriel Ordonez", the title from `<title>` and "gabrielordonez.com" centred vertically; render it with `qlmanage -t -s 1200 -o . og-image.html`, crop the centre with `sips -c 630 1200 og-image.html.png --out og-card.png`, convert with `sips -s format jpeg -s formatOptions 85 og-card.png --out og-image.jpg`, delete the two PNGs, and look at the result (FR-01)
- [x] T006 Add `og:image` with value `https://gabrielordonez.com/og-image.jpg` to `index.html` (FR-01, FR-07)

## Phase 2 — Other pages

- [x] T007 Add `og:title`, `og:description` and `og:image` to `blog.html`, equal to its `<title>`, its meta description and the shared image (FR-09)
- [x] T008 Add `og:title`, `og:description` and `og:image` to `rag-project.html`, the same way (FR-10)
- [ ] T009 Add `og:title`, `og:description` and `og:image` to `blog/rag-latency.html`, the same way (FR-11)
- [ ] T010 Add a `<script type="application/ld+json">` to `index.html` with a `Person` and a `WebSite`, each with `name` "Gabriel Ordonez" and `url` "https://gabrielordonez.com/" (FR-06)

## Phase 3 — Reachability and verification

- [ ] T011 Make every FR-05 page exist, carry a `<title>` and be tracked by git, so GitHub Pages serves it; `blog/ai-theory-practice.html` is on disk and not tracked (FR-05)
- [ ] T012 Run `python3 tests/check_site.py --all` and make it pass (FR-08)
