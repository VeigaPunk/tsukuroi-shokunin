VERDICT: supports

Item C2-15 (round-38 routed defect 4) — seat C2RevS217, 2026-10-26.
I AGREE with the declared claim: S217 is a rule-2-compliant correction row superseding
S210's anchor; every line number S217 cites is exact against the frozen trans.c snapshot,
which is byte-identical to upstream pacman 54d9411; and S210's bytes are unchanged between
base 0eff65b21bb81195ee06c96a83afbd7a07e52eef and tip 2e1c2a40c13dc52e155d89e72f3fdd560db7399a.

## A. S217 satisfies CORPUS rule 2 (correction = new row, teaches opens `supersedes S<id> —`)
- Rule text, /home/vgpnk/Projects/shokunin/CORPUS.md:116-118: "2. **Append-only.** Only
  `status`, `recheck` and `used-by` change in place, and each change is logged old→new in
  the round lesson. A correction is a new row whose `teaches` opens `supersedes S0NN —`."
- Row S217 at tsukuroi-shokunin/corpus/SOURCES.md:226; `teaches` is the 7th column per the
  table header at corpus/SOURCES.md:3. S217's teaches opens exactly
  `supersedes S210 — the commit function is ...` (byte extract:
  .ufo/waves/round-39/w1/C2RevS217/S217.at-tip.txt) — required form present (row id,
  em-dash, space).
- S217 is NEW, not an in-place rewrite: `git show 0eff65b…:corpus/SOURCES.md | grep -c
  '^| S217 |'` → 0; same against 2e1c2a4… → 1 (receipts.log R6). The only commit touching
  corpus/SOURCES.md in 0eff65b..2e1c2a4 is 4078eb23 "round-39: C2 libalpm transaction
  order entry; SOURCES S213-S218 (S217 supersedes S210 anchor)"; merge-base --is-ancestor
  confirms base ≤ 4078eb23 ≤ tip (receipts.log R6).
- No competing supersession: `supersedes S210` matches only corpus/SOURCES.md:226 (S217).

## B. Anchor and line numbers vs .ufo/waves/round-39/frozen/src/trans.c
- Snapshot identity: sha256(frozen/src/trans.c) = 637c1165790ddd1c9d80bb0bfed9d85b1f5baa9
  b8e5a2e323243c5764ac4ed07 = frozen/src/SHA256SUMS:5 = the "snapshot sha256" cited in BOTH
  the S210 anchor (corpus/SOURCES.md:219) and the S217 anchor (corpus/SOURCES.md:226).
  Upstream cross-check: fetched
  https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/trans.c on
  2026-10-26 → sha256 637c1165… identical (receipts.log R2), so the frozen lines ARE the
  pinned commit's lines.
- `alpm_trans_commit` line 167: frozen trans.c:167 is
  `int SYMEXPORT alpm_trans_commit(alpm_handle_t *handle, alpm_list_t **data)` — exact.
  `grep -n 'trans_commit'` over the file returns only line 167 (receipts.log R3), so
  `_alpm_trans_commit` — the symbol S210's anchor names — does not exist anywhere in the
  snapshot; S217's teaches statement ("the commit function is `alpm_trans_commit`
  (trans.c:167), not `_alpm_trans_commit` as the S210 anchor says") is true of the file.
- Pre phase lines 201-204: trans.c:201-204 is exactly the `ALPM_HOOK_PRE_TRANSACTION` run
  block (`_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION)` at 202, `RET_ERR(...,
  ALPM_ERR_TRANS_HOOK_FAILED, -1)` at 203) — receipts.log R4.
- `transaction started` line 208: trans.c:208 is
  `alpm_logaction(handle, ALPM_CALLER_PREFIX, "transaction started\n");` — exact.
- `transaction completed` and Post phase lines 232-239: within trans.c:232-239 sit
  ALPM_EVENT_TRANSACTION_DONE (233-234), `alpm_logaction(..., "transaction completed\n")`
  (235) and `_alpm_hook_run(handle, ALPM_HOOK_POST_TRANSACTION)` (237-239) — both named
  items inside the cited range (the block's closing brace is 240; the range contains
  everything it names — noted as an observation, not a defect).
- teaches ordering claim holds on the same lines: Pre hook run (202) precedes the
  `transaction started` log (208); Post hook run (238) follows the `transaction completed`
  log (235).
- S210's stale anchor, for the record: corpus/SOURCES.md:219 anchor reads
  "`_alpm_trans_commit` lines 201-240" — the named symbol does not exist in the snapshot
  (R3), though lines 201-240 do fall inside `alpm_trans_commit` (spans 167-245). S217's
  correction states exactly this mismatch. Per rule 2 the stale S210 row itself stays
  untouched — verified in C.

## C. S210 bytes unchanged 0eff65b → 2e1c2a4
- Extracted the single `^| S210 |` line from each commit's corpus/SOURCES.md blob:
  `cmp` clean, sha256 of both extracts =
  1304b670b03f36515cc2d4de6df9129d141ca4f989ecbe57d2105dce3c544caa (receipts.log R5).
  Exactly one S210 row in each blob (grep -c → 1, 1); row still present at tip, not deleted.
- Working-tree agreement: lane corpus/SOURCES.md:219 is byte-identical to the tip-blob
  S210 line (cmp clean, receipts.log R5).

## Not done / limits
- Did not judge the truth of TO1-TO8 rule text in
  corpus/knowledge/pacman-transaction-order-r39.md — other seats' scope; this item is the
  SOURCES row form, the trans.c anchor lines, and S210 byte stability. No `TO<n>:` lines
  accordingly (no TO row judged).
- Byte comparison is between the two named commits (base, dispatch tip); I did not audit
  other working-tree differences beyond the S210/S217 lines.
- No tools installed or upgraded (none needed); no host or lane mutation; all scratch
  under /fast/scratch/hyaku/tsukuroi-r39/C2RevS217 (removed after receipts were copied).

## Receipts
.ufo/waves/round-39/w1/C2RevS217/: S210.base, S210.tip, S210.at-tip.txt, S217.at-tip.txt,
upstream-trans.c-54d9411, receipts.log (R1-R8: snapshot/upstream sha, trans.c:160-245
numbered dump, blob extraction + cmp + sha256, git log and merge-base outputs, row extracts).
