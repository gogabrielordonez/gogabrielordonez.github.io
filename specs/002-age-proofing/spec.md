# Feature Specification: Age-proofing on gabrielordonez.com

**Created**: 2026-10-18

**Status**: Approved (CEO, ask be87de01fc, "Go ahead", 2026-10-18)

## Why

Gabriel's CVs and LinkedIn deliberately omit graduation years and condense the roles before 2013 without dates. The live site contradicts them. On 2026-10-18 `index.html` on `main` (8e70efe, identical to the live page apart from Cloudflare's email obfuscation) shows:

- Education: `University of Barcelona | 2019` (line 656) and `University Canada West, Vancouver | 2022` (line 661).
- Experience: the last timeline item is dated `2003 – 2013` (line 495), titled `Previous Experience`, with `Ericsson | MSI Americas | Telefónica`.

Reference wording, `resume-ai-tpm.md`: `### Earlier Career` / `Solutions Architect & Project Lead — Ericsson · RF Engineering — MSI Americas, Telefónica`. No other page carries these items.

## Requirements

| ID | Description |
|---|---|
| FR-001 | The MS (University of Barcelona) and MBA (University Canada West, Vancouver) Education entries show degree and institution, and no year. The Bachelor entry is unchanged. |
| FR-002 | The timeline item dated `2003 – 2013` becomes an undated item headed `Earlier Career`, with no four-digit year and no year range. |
| FR-003 | The Earlier Career item names the same employers (Ericsson, MSI Americas, Telefónica) and both roles by the resume's names: `Solutions Architect & Project Lead` (Ericsson) and `RF Engineering` (MSI Americas, Telefónica). The existing one-line description under each role is kept. |
| FR-004 | Everything else on the page is unchanged: every other timeline item and its dates (2013 – 2015 to 2024 – Present), the About text (including "(2011)" and "2017"), metrics, case studies, projects, certifications, awards and footer. |
| FR-005 | The leftover developer comment above the timeline items (`<!-- Nokia/Ericsson/MSI ... I'll include Nokia and Ericsson. -->`, lines 478–480) is removed. |

## Success criteria

| ID | Description |
|---|---|
| SC-001 | In `index.html`, neither the Barcelona nor the Canada West Education entry contains a four-digit year; both still name their degree and institution. |
| SC-002 | `index.html` contains no `2003`; the Earlier Career item contains no four-digit year and names Ericsson, MSI Americas, Telefónica and both resume role names. |
| SC-003 | Outside the FR-001 entries, the Earlier Career item and the removed comment, `index.html` is identical to `index.html` at 8e70efe. |
| SC-004 | After the merge publishes the site, live `https://gabrielordonez.com/` shows no `| 2019`, `| 2022` or `2003 – 2013`, and shows `Earlier Career`. |

## Out of scope

- The About text's "(2011)" and "(2017)" and every date from 2013 onward.
- Any other page, the design, CSS and layout.
- LinkedIn and the CV files.
