# Tasks: Age-proofing on gabrielordonez.com

- [ ] T001 [tests] Write the spec-002 checks for SC-001, SC-002 and SC-003 (baseline 8e70efe), run by `python3 tests/check_site.py`. Red on the current `index.html`. Serves FR-001, FR-002, FR-003, FR-004, FR-005, SC-001, SC-002, SC-003.
- [ ] T002 [impl] Edit `index.html` as FR-001, FR-002, FR-003 and FR-005 say, changing nothing else (FR-004). Turns T001 green; the spec-001 checks stay green. Serves FR-001, FR-002, FR-003, FR-004, FR-005.
- [ ] T003 [review] Walk spec 002 against the tree at the PR head, run the check, call `cq_converge`, and post an inline `Review verdict:` comment on that head.
- [ ] T004 [lead] Open the PR; on review's APPROVE, bring the CEO the merge card (merging publishes the site). After the merge, check SC-004 on the live site. Serves SC-004.
