# Round 56 — lesson (Windows host, base `62b47771`; declaration `ebaf9856`, work `a4d88715`)

Shape: single-session inline round (no wave/AgentSwarm dispatch surface on this host; the L0
question `tsukuroi | round-53` stands unanswered and was routed around, never treated as answered;
the round-1 contested kaidoku/revenger scope question likewise stands). The four routed carry-ins
of the r55 closure landed first as repairs R1-R4 (not claims): R1 the r52 "58 seat files" counting
command (SCORECARD correction block), R2 the r55 Gate's explicit zero-rejections line, R3 scratch
hygiene, R4 the W04 watch count (42 both passes). Claims declared before any measurement
(SCORECARD "Round 56 — declaration"): C1 operability (census `--receipt` mode + recheck `--budget`),
C2 freshness (executable T1-T12 recheck pass), C3 depth (sourced config/failure plane). All probes
read-only or absence-refused; every repair operator-gated; receipts live in the lane tree, never
scratch. The FRESH-START ruled-out set (r50/r51/r52 re-spot-checked) is in the SCORECARD
declaration.

## Gate

Source records for rows opened this round (CORPUS.md contract v1):

- **S266** — Microsoft Learn, Windows Server commands reference, `sc.exe config`,
  https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/sc-config .
  Opened 2026-11-01 by the L1 (HTTP fetch of the live page). Located quote (22 words, counted by
  `wc -w` before landing): "A space is required between an option and its value (for example,
  type= own. If the space is omitted, the operation fails" — the page's own sentence drops its
  closing paren (recorded; same page-side-typo class as S265). Supporting located text: the
  start= value domain `{boot | system | auto | demand | disabled | delayed-auto}` (closed,
  six values), the error= domain, "There is no default for **binpath=**, and this string must be
  supplied", the S262-family sentence "Using **type= interact** by itself will generate an
  error", and the frontmatter identity (`git_commit_id 48fd05321fd0fe328b1977597b554d884ca5e35d`,
  `updated_at` 2026-02-16, `ms.date` 2018-06-05 — same doc build as S261/S262/S265). The tool's
  own usage text (receipt `t13-config-usage-gate.txt`) confirms the start= domain byte-for-byte
  and adds type= `userown|usershare`, which the page omits. Used by
  `corpus/knowledge/windows-services-config-plane-r56.md` — C3's sourced ground.
- **S267** — Microsoft Learn ARCHIVE, `Sc failure` (Windows Server 2012 R2 library),
  https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc742019(v=ws.11) .
  Opened 2026-11-01 by the L1 (HTTP fetch of the live page, located by web search after the
  current-reference URL returned 404 — the current Windows Server commands reference carries NO
  sc-failure page). Located quote (23 words, counted by `wc -w` before landing): "A space is
  required between an option and its value (for example, actions= restart). If the space is
  omitted, the operation will fail." Supporting located text: the syntax line (set semantics
  only — no query form), the actions= contract (up to three slash-separated actions
  run/restart/reboot with millisecond delays; requires reset=), "Not all services allow changes
  to their failure options", and the frontmatter identity (`is_archived: true`, `ms.date`
  2016-08-31, archive `git_commit_id 5327995ac358bee6eaf26e4214a7ac52b67607f1` — the same
  archive commit as S263/S264). Used by
  `corpus/knowledge/windows-services-config-plane-r56.md`.

Census: `bash <fleet-root>/scripts/sources-census.sh validate --root <fleet-root> tsukuroi` exit 0
at round start and round end (42 W04 warnings at BOTH passes — no growth: the two new rows carry
fresh URLs; no E-code either pass; receipts
`.ufo/waves/round-56/before/sources-census-start.txt` and
`.ufo/waves/round-56/after/sources-census-end.txt`).

Rejections this round: **0 — stated explicitly**: both new rows are admits; no `SOURCES.md` row
was opened-then-rejected in round 56 (no row quota, CORPUS contract v1 rule 4). The
current-reference sc-failure URL returned 404 BEFORE S267's archive page was located — a lead
that never became a row, not a rejection of an opened source (recorded inside S267's anchor).

Assimilation: `considerthese/` mined (latest 2026-10-26; the five self-improvement ideas are
aggregator/wave-class or Linux-host-class on this host, and the cross-note correction propagation
map was partially applied in r54 — none clears this round's bar; nothing adopted). The shokuknow
register is not reachable from this host. Assimilation: none — shokuknow unreachable.

## Mistakes

- **R56-STALE-DRAFT-REVERT** (class: a working file on this host reverted to a pre-commit draft;
  the committed tree was authoritative) — the ON-DISK `tools/recheck-drift-r54.sh` lacked the
  committed `> "$receipt"` write line (disk mtime Oct 31 21:08; the line is in every commit since
  r54's `f24ca241`): with `--receipt` the script printed the receipt to stdout and never wrote
  the file. Captured-by: this round's full-tree plumbing sweep, run after the redirect was found
  missing — `git ls-tree -r --name-only HEAD | grep -v "^\.ufo/waves/" | while IFS= read -r p; do
  git show "HEAD:$p" | cmp -s - "$p" || echo "STALE: $p"; done` → exactly two files differed
  (both r54-session tools; everything else byte-clean, r53-r55 waves included). Fix: the r56 edit
  restores the write and adds an exit-2 write-failure path; on this host the worktree/index views
  are UNTRUSTED (`git status`/`git diff` worktree comparisons showed the two existing files
  simultaneously as staged-deleted and untracked) — diffs that matter are tree-to-tree
  (`git show <rev>:<path>`), and the sweep command above is the repeatable capture.
- **R56-RECEIPT-FLAG-UNEXERCISED** (class: a registered flag whose write path was never
  exercised) — recheck-drift-r54's `--receipt` was registered in r54 and its row claimed it
  "writes one lane-tree file", but no round ever ran it, so the lost write line stayed invisible.
  Captured-by: C1's D7 receipt run this round — the first real `--receipt` call, which would have
  produced an empty file. Fix: a flag's registry claim should name its first EXERCISING use; C1's
  predicate requires the receipt's byte content (header keys + the D7 line), not the flag's
  existence; the r56 receipts are that first use for both tools.
- **R56-UGREP-LEADINGSLASH** (class: MSYS path conversion mangles a grep pattern that begins
  with `/`) — `grep -cE "/R52(Crit|Rev)GR[^/]*\.md$"` failed with `invalid option
  -(Crit|Rev)GR…` because MSYS rewrote the leading-slash ARGUMENT into a Windows path (the same
  class as r54 T1, biting the analyst's own counting one-liner; this host's grep is ugrep, r55
  lesson). Captured-by: the immediate ugrep error this round, kept in the shell transcript.
  Fix: spell counting patterns without the leading slash (anchor on the filename body) or set
  `MSYS_NO_PATHCONV=1` inside the command; the 58-count command in the SCORECARD correction
  block is spelled that way.
- **R56-USAGE-GATE-ASSUMED-ABSENCE** (class: a probe designed from the ASSUMED failure order of
  a tool) — the first T14/T15 design assumed `sc config <nonexistent>` would reach OpenService
  and refuse by absence; the tool prints its USAGE block and exits rc 103 because
  option-validation precedes OpenService. Captured-by: the probe's own receipts
  (`t13-config-usage-gate.txt`/`t14-failure-usage-gate.txt`, rc 103 with full usage text). Fix:
  the probes were redesigned with an option spelled (absence-refused, rc 36) and the wrong
  assumption became T13 — a real signature (rc 103 means "missing option", never "service
  missing") — instead of a silently reinterpreted result.
- **R56-COPY-RUNS-OUT-OF-TREE** (class: a tool copy executed outside its tree reads the wrong
  parent) — the before-battery ran a SCRATCH COPY of the base recheck script to test `--budget`;
  the script `cd`s to `dirname/..`, so from scratch its register/PROVINCE reads missed and drift
  lines fired by construction (rc 1 misread as a flag rejection). Captured-by: the before-receipt
  correction appended before the outcome commit (the honest before-evidence is the grep=0 at
  base; the copied-run rc is an artifact of the harness). Fix: a self-anchoring script must be
  exercised in place (or its cd anchor made explicit); before-proofs that copy tools out of the
  tree must account for the anchor, or use plumbing greps as the evidence instead.

Sweep that found no further mistakes this round: before the outcome commit the round's files were
re-read against the declared predicates (C1's receipt headers re-checked key by key; the C2
receipt's 12 lines re-read against the two planes' rows; C3's four rows re-read for citation and
column count; the SOURCES table re-run through the malformed-row awk; the two Gate quotes
re-counted with `wc -w`; the uniqueness gate re-run on the appended SCORECARD). The five mistakes
above are the complete defect set observed this round.
