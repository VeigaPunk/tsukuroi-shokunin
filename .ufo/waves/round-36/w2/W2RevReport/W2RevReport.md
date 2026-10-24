# W2RevReport — no-overclaim sweep of the L1 integration record (round 36, w2)

Seat: reviewer. Written 04:37:52Z (`date -u +%H:%M:%SZ` pasted at write time; the final
edit stamp is the file mtime). Read-only: no production file, no VCS command, no
pacman. Nothing installed this seat.

Scope read: `SCORECARD.md:1589-1759` (declaration + pre-freeze corrections) and
`LOG.md:1359-1377` (declaration, corrections+integration, freeze entries) at
`c052bb7d41ced49aa888817069afd804eccfecf1`; the committed record rows that commit
lands (`SKILL.md` round36 registry table, `corpus/README.md` round-36 row,
`corpus/knowledge/journalctl-v262-field-filter-r36.md`, the four `NoUpgrade` appends,
`corpus/lessons/round-36.md`); the five changed tools' current bytes; every round-36
probe receipt under `.ufo/waves/round-36/`; and all 50 wave-1/wave-2 seat report
directories that hold a `.md`.

Deliverable: **`overclaim.md`** in this directory — 28 per-claim verdicts
(VERIFIED / PARTIAL / FALSE / UNSUPPORTED) with the receipt or byte evidence for each.

## Findings, by severity

### HIGH

1. **Two committed record rows assert sensitivity results the only committed receipt
   contradicts.** `SKILL.md:3057` registry row (child-env-allowlist-r36, Self-test
   column) and `corpus/README.md:262` both say the sensitivity battery
   "claim/r33claim/regression at base 0, MutAttrgetterCopy/MutPathCopy mutants > 0" is
   *committed under `.ufo/waves/round-36/l1/`*. In that directory: no `regression`
   receipt at all; `sens-mutattr.jsonl` last line reads `"leaking": 0` (MutAttrgetterCopy
   = 0, not "> 0"); no MutPathCopy receipt anywhere in round 36 at write time.
   Evidence: `.ufo/waves/round-36/l1/` listing (6 receipts + 2 scripts),
   `sens-mutattr.jsonl:5`, `SKILL.md` diff at `c052bb7`, `corpus/README.md:262`.

2. **The wave-1 evidence ledger was never committed; the record says it was.**
   The declaration's order and the corrections item 6 framing say "the L1 commits every
   wave-1 control receipt" before the freeze. At HEAD:
   `git status --porcelain .ufo/waves/round-36/w1` → `?? .ufo/waves/round-36/w1/`;
   `git ls-files .ufo/waves/round-36/w1/ | wc -l` → 0. The freeze commit
   (`1e92680`) added only L1-authored `l1/*.jsonl`. Consequence: every wave-1 measured
   claim — gate baselines (`w1/ExecGateBaselines/*.jsonl`, 7 files), the probe drafts,
   the C2 matrix, the source snapshots — has no committed receipt, which is the exact
   class the round-35 spot-check routed as defect 1 (untracked lane evidence).

3. **The C1 before-value has no receipt, and the wave-2 seat dispatched to check it is
   handed a false premise.** The declaration says "before: at least one leaking pair on
   every one of the five targets". No committed `livefive` receipt exists. The only
   `"target_set": "livefive"` receipts are untracked wave-1 draft-probe runs
   (`w1/MutProbeDraft/*`, probe digests `544c5ded`, `36d2342c`, `ee0750ae`, `979995aa`),
   and they cover **two of five** targets — `tools/check-report-receipts.py` (3 pairs)
   and `tools/run-receipt.py` (3-4 pairs). There is no receipt at any probe generation
   for `check-revision-binding.py`, `score-census-handoff-r32.py` or
   `mutants-btrfs-space-r30.py` reading > 0. `w2-spec.json` seat `W2ReBefore` instructs:
   "confirm the committed before receipt under `.ufo/waves/round-36/l1/` matches your
   run's last line" — that receipt does not exist.

4. **The frozen kill rule is not applied, and one conjunct is never stated.**
   Corrections item 9 freezes: "any sensitivity conjunct fails (MutAttrgetterCopy and
   MutPathCopy each read above 0; claim/r33claim/regression sets at the base each read 0)
   — C1 is reported not verified." The freeze LOG entry (`LOG.md:1375-1377`) reports
   MutAttrgetterCopy = 0 and reinterprets it as an "invocation-coverage gap", states
   MutPathCopy as pending, and **never mentions the regression set** — no round-36
   `regression` receipt exists, and the nearest `regression` receipts are round-35 V6
   (`ExecV6Calibration/regression-v6.jsonl`, 22/33 leaking at revision `6b4561e4`).
   So the verdict text states two of the three conjunct classes' outcomes and draws no
   "not verified" verdict from its own rule. This is the calibration defect the seat is
   asked to check: the text is candid about the reading and silent about the conclusion.

5. **A named wave-1 source returned NO-GO for the freeze; the record carries no
   disposition.** `.ufo/waves/round-36/w1/CriticFreeze/freeze-checklist.md:138`:
   "**NO-GO for the freeze as currently specified.** B1–B7 are fixable before-freeze
   design/wording defects or unresolved required evidence." The corrections block cites
   CriticFreeze as a basis and addresses B2/B3/B7-shaped items (2-5) but records no
   disposition for B1 (a battery entry point whose result cannot be green if any
   conjunct fails), B4 (the selftest-sanitization false negative — precisely the
   MutAttrgetterCopy gap in finding 4), B5 or B6. Freezing against a live NO-GO is
   allowed; recording it as satisfied without naming the disposition is not.

6. **"16-term predicate" is wrong in both the committed note and the committed README
   row.** The predicate excerpt lists 15 terms
   (`.ufo/waves/round-36/w1/ScribeC2Draft/journalctl-filter-c-predicate.txt`:
   `arg_boot_filter` … `arg_pattern`), and the note's own decision table has 15 `arg_*`
   rows (`grep -c '^| \`arg'` → 15). `matrix-mini.json` `cell_count` = 54 checks out
   (6+29+4+15), so only the term count is wrong — in `corpus/knowledge/journalctl-v262-
   field-filter-r36.md:126` and `corpus/README.md:264,269`.

### MEDIUM

7. **Corrections item 6's "on final bytes" is false for two of its three readings.**
   The receipts carry three different probe digests: `dev-r33claim-final.jsonl`
   `0865d8a1…` (leaking 6), `final2`/`final3` `6ec9af2d…` (leaking 3), `final4`
   `a2a5acac…` (leaking 0). Only the last is on the frozen bytes.

8. **Stated measurement without receipt: "direct control 16.77 s"** (corrections item 4)
   occurs only in untracked `w1/ExecProbeR36/ExecProbeR36.md`.

9. **"the label 31 round-34 receipts carry"** (corrections item 3) has no derivation;
   a grep of `.ufo/waves/round-34/` for `"predicate_label": "leaking"` matches 100 files.
   The "31" may be a narrower set, but nothing in the lane defines it.

10. **Exit codes in the freeze receipts are unverifiable.** `dev-claim-final.jsonl` and
    `dev-r33claim-final4.jsonl` have no exit/timeout/finish field and no `.err` sibling;
    the LOG's "exit 0" cannot be checked from them. Contrast the round-33/34 runner
    receipts, which carry a `receipt_end` line with `exit_code`, `timed_out`,
    `finished_utc`.

11. **The corrections block's order names a commit that does not exist.** "Order
    amended: this corrections commit; the freeze commit; the change commit" — history is
    `1e92680` (freeze, carrying the corrections **LOG** entry) then `c052bb7` (change,
    carrying the corrections **SCORECARD** block). The block's own "landed, before any
    after-data seat scored" holds for seats (w2 dispatch file mtime 04:30:30Z, after
    both commits), but not for the two artifacts as one commit.

12. **Corrections item 7's line pointers read as append targets but are the superseded
    loci.** The appended blocks are at `SKILL.md:3010-3060`,
    `update-safety-note.md:556-582`, `update-safety-v2.md:427-454`; the named
    `SKILL.md:397-399`, `note:420-424`, `v2:52`, `v2:198` are the historical rows the
    appends supersede. The appends themselves are correct and append-only.

### LOW

13. `w1/CriticC2Shape/CriticC2Shape.md` cites its own deliverable as
    `.ufo/waves/round-36/w1/CriticC2Shape.md`, which does not exist (the file is at
    `w1/CriticC2Shape/CriticC2Shape.md`).
14. `corpus/lessons/round-36.md` as landed still says "This file is a proposal for the
    L1 to land; it is not the landed lesson", yet the change commit message counts it as
    "lesson". Its append-only sweep claim ("both sweeps print no removed line") names no
    receipt; the property itself holds for `c052bb7` (record files
    `SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/`: 452 insertions,
    0 deletions, `git show --numstat`).

## Honesty sweep — wave reports with result claims and no receipt

Method: for every seat directory under `w1/` and `w2/` holding a `.md` (50 directories
at 04:37Z), collect (a) machine-output files (`.json/.jsonl/.txt/.log/.csv/.err/.out`),
(b) lines asserting a result (`exit/rc/leaking/PASS/passed/verified/green/sha256`),
(c) every backticked lane path, tested for existence. 35 seat reports make result
claims; 8 have zero machine artifacts in the seat directory:

| Seat | result lines | flag |
|---|---|---|
| `w1/ScoutRecon` | 32 | **FLAG** — 32 live `rc=0`/`rc=1` journalctl readings recorded as a table (`inventory.md`), no raw capture in the seat dir. Re-runnable, but as written it is a measurement table without a receipt |
| `w1/ScoutSourcesEnv` | 2 | **FLAG (minor)** — installed CPython "3.14.8" and `/usr/lib/python3.14/subprocess.py:1911-1917` claimed with no capture in the seat dir |
| `w1/CriticFreeze` | 15 | **FLAG (finding 5)** — its NO-GO is the material assertion and no disposition exists in the record; its historical readings cite `round-34`/`round-35` receipts that do exist |
| `w1/ConnSiblings` | 15 | flag: cross-lane claims (20-sibling diff, `GIT_ENV_KEEP`) not checkable inside this lane; no capture |
| `w1/ScoutMori` | 4 | flag: mori-lane paths (`corpus/knowledge/audit-r11.md:203-204`, `journal-alarm-routing-r14.md`, `kernel-oom-line-attribution-r12.md:10-16`) are absent here — other lane, not a dangling citation in this lane |
| `w1/ConnReport` | 7 | not flagged: the report says "Not run: no probe, no child-env before/after, no journalctl live matrix, no build. An unrun check has not passed." |
| `w1/SimplifierProbe` | 16 | not flagged: conditional/counterfactual lines, no pass assertion |
| `w1/ExecPacnewDebtNote` | 5 | not flagged: requirement text, explicitly "not a passed independent oracle" |

Systemic flag on top of the table: **all 32 wave-1 seat directories are untracked**
(`git ls-files` = 0), so every wave-1 measured claim currently has no *committed*
receipt regardless of whether its seat wrote machine output — the strongest single
honesty finding (HIGH 2). No lane-path citation in a committed record file dangles
except the two uncommitted-evidence references already named: `corpus/README.md:269`
cites `.ufo/waves/round-36/w1/ScribeC2Draft/matrix-mini.json` (exists on disk,
untracked) — the same class as the round-35 tarball defect this round claims to repair.

## What checked out (so the sweep is not one-sided)

- Frozen probe bytes: `sha256sum` of `1e92680:tools/probe-child-env-allowlist-r36.py`
  and of HEAD both `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a`;
  `VERSION = 7`.
- Frozen predicate sentence: 1331 characters, identical to `PREDICATE` (programmatic
  compare, not eyeball).
- No ambient copy remains in the five tools: `grep -n "os.environ"` over all five
  returns nothing; the fixed-dict builders and the computed run-private settings are
  where the corrections say they are (`run-receipt.py:37-48`,
  `check-report-receipts.py:313-321`); `import re` replaced `__import__('re')`.
- `livefive` named limit is implemented as declared for the parity conjuncts
  (`:1153`, `:1256`), and the do-nothing control for livefive is `child_execs` (`:1155`).
- C2's central live claim reproduces read-only: `journalctl --version` = `systemd 262
  (262-1-arch)`; `journalctl -F _SYSTEMD_UNIT --since -1h` exits 1 with the 84-byte
  stderr line (83 chars + newline), text identical to the note.
- S199's pinned NEWS bytes hash to the row's `a494f038…a7657` (file untracked, see HIGH 2).
- The change commit is append-only on record files (`git show --stat`: record files all
  insertions; the 20 deletions are inside `tools/`).

## Residual risk

- [inf] I did not re-run the probe. Every "before > 0" statement is therefore
  unverified in both directions: absent receipt **and** absent re-measurement. The
  `W2ReBefore` seat is the only lane actor positioned to produce that number.
- [unk] Whether the missing `regression` base receipt is a deliberate scope cut: the
  kill rule names it, no record explains its absence at the base, and the only w2 seat
  that names the regression set is `W2ReAfter`, which runs it at `c052bb7` (the after
  state, "expect 0") — no seat re-measures regression at the base `6d76fb20`, which is
  the conjunct's wording.
- [inf] The round-34 `MutAttrgetterCopy/mutant-ordinary.json` proof is on a different
  detector (`detector_sha256 4048c876…`); a frozen-probe live-mode reading is the only
  thing that can convert it into a conjunct result.
- Cross-lane claims (`w1/ConnSiblings`, `w1/ScoutMori`) are outside this seat's read
  authority and were not checked.

## Verification gaps (method honesty)

- No `lsp` device is exposed in this seat's tool inventory, so no language server
  answered for these Python files: caller/definition checks were done by reading the
  exact builder functions and spawn sites, not by a semantic engine. The one grep-based
  claim (`os.environ` absence in the five tools) is a literal-text check and is stated
  as such; it is corroborated by reading each builder.
- Only committed receipts and on-disk artifacts were inspected; wave-1 seats still
  running or writing were read at the file state present at 04:37Z.
- No production file, lane VCS state, or other lane was modified by this seat.

## Pin note (lane moved while this seat ran)

Every record citation above is pinned to `c052bb7d41ced49aa888817069afd804eccfecf1`
bytes (the assigned change commit); the probe is byte-identical at the later HEAD
(`8d5fa7f`, wave-2 spec commit: `git show 8d5fa7f:tools/probe-child-env-allowlist-r36.py
| sha256sum` still `a2a5acac…`). Between the 04:37Z checks and 04:40:29Z the lane's HEAD
advanced to `8d5fa7f` and the worktree gained uncommitted `SCORECARD.md` (+56/-1) and
`SKILL.md` (+58/-5) edits by the L1. Those edits were not audited here (outside the
assigned commit); [inf] the five `SKILL.md` deletions are append-only-relevant if they
land, and if they touch the `child-env-allowlist-r36` row (still `SKILL.md:3057`) the
C-20 finding should be re-read against the new bytes.
