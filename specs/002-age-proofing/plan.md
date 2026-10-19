# Plan: Age-proofing on gabrielordonez.com

## Files

- `index.html`: the only source file that changes (the Education card, the last timeline item, the comment above the timeline).
- The spec-002 checks under `tests/` (the test author chooses file and harness). The project's check is `python3 tests/check_site.py`, so the spec-002 checks must run under that command.

## Approach

1. The test author writes checks for SC-001 to SC-003 from this spec, with 8e70efe as the SC-003 baseline. They fail on the current `index.html`.
2. The implementer edits `index.html`: removes ` | 2019` and ` | 2022`, replaces the `2003 – 2013` item with an undated `Earlier Career` item (existing markup classes kept, so the layout is unchanged), and deletes the comment.
3. An independent reviewer walks the spec against the tree at the exact commit and posts an inline `Review verdict:` on the PR.
4. Merging the PR to `main` publishes the site through GitHub Pages, so the merge is a CEO card. SC-004 is checked live after it.

## Testing

`python3 tests/check_site.py` (the spec-001 checks stay green) plus the spec-002 checks. SC-004 is a live fetch after the merge.
