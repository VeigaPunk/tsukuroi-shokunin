# RevBindSectionCitations — revision binding

[obs] Audit rows read: `.ufo/waves/hyaku/jj-w1/reports/JjAuditTsukuroi.md` R1 (HEAD = jj `@-`), R2 (no ancestry gate); pre-edit HEAD admission at `tools/check-section-citations.py:55`, help `:433`, git surface `:399/:408/:421`, pinned-BASE resolve `:758`.

[obs] Contract applied:
- `REV` → `^[0-9a-fA-F]{7,64}$` (`tools/check-section-citations.py:61`); `HEAD`, `@`, `@-`, ref names now E-REVISION-INVALID (exit 2).
- `BRANCH` grammar `:64`; `--branch` default master `:493`; JSON adds `branch` + `branch_tip` (`:394-397`).
- `git()` repo parameter `:405`; `ref_sha`/`is_ancestor`/`bind_revision` `:437-472` require the revision and pinned baseline `db68e62…` to be ancestors of `refs/heads/<branch>` and, when present, `refs/remotes/origin/<branch>` → E-REVISION-NOT-LANDED / E-REVISION-NOT-PUSHED (exit 2). Wired in main `:934`.
- All 38 fixture cases, finding ids and pinned baseline unchanged; the lone HEAD literal (`cli-both-modes`) now passes a sandbox-resolved hex. No worktree mode exists.

[obs] Selftest: before 43/43 PASS (baseline file in clone); after 61/61 PASS, rc 0. Nine new mktemp git sandbox vectors: HEAD/@-/ref/6-hex rejected, unlanded rejected, unpushed rejected, absent branch rejected, tip and ancestor accepted with `branch_tip`. Zero leftover `/tmp/section-citations-bind-*`.

[obs] Diff +208/−29, one file. Run from mktemp clone `/tmp/sc-selftest-BAWoJL` (lane clone + edited tool copy); no git write in the lane.

[unk] Revision-mode end-to-end (`--revision <tip>`) not run — outside EXEC-AUTHORIZED.

[inf] `SKILL.md:1857` and `.ufo/waves/round-16/build/frozen-cases.json:9` still document "HEAD or 4–64 hex"; `revision-delivered` now also needs pushed ancestry.

Scope: executed=git clone,cp,python3 tools/check-section-citations.py --selftest,git show,git diff,git status,git rev-parse --verify,grep,ls,python3 -c ast.parse,wc
