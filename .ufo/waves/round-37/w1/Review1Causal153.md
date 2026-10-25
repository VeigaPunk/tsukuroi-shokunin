# Review1Causal153 — adversarial review of the round-37 declaration (item 1/4)

Seat: Review1Causal153 (reviewer, L2, tsukuroi r37 w1). Date: 2026-10-25. Read-only review; no
lane file touched; no tool installs (none needed: git/python3/curl present; RULES.md read;
pacman unused per host pause). Object reviewed: `SCORECARD.md` "Round 37 — declaration,
pre-freeze candidate" (SCORECARD.md:1857-1948) and "Round 37 — pre-freeze C3 correction"
(SCORECARD.md:1950-1974), against fleet `PROTOCOL.md`, `AXES.md`, `CORPUS.md`, `MISSION.md`,
`LEARNING.md`. Every check below was executed first-hand this round. Lane state moved during
review (HEAD `0e5f70f` → `d621b71`); each observation names its hash.

## Findings (by severity)

### F1 — HIGH — C3 (calibration): the frozen after-value is not separable and was already falsified by the round's own pipeline

The correction freezes the predicate `mismatches == 0 && checked == 27 && exit == 0` "at the
measured round-37 branch-tip revision" and asserts separability via "each claim verifies without
the others" (SCORECARD.md:1942-1944 context; the C3 correction carries the predicate at
SCORECARD.md:1963-1966). But K07–K11 of `tools/check-self-assessment.py` measure live tree
counts (knowledge .md count, SKILL.md newlines, SKILL pipe lines, lessons file count,
corpus/README.md lines) at the given revision — exactly the surfaces the declaration's own
remaining order appends to ("SOURCES rows, lesson skeleton, registry rows" in the change commit;
"the measured outcome, lesson, SOURCES/README/SKILL rows and report" after wave 2,
SCORECARD.md:1944-1948).

Observed this round:
- Base `564db0b614b2914de5452f9ebd537a0653ae1de5`: `checked: 27, mismatches: 5, status: FAIL,
  exit 1` — K07 55≠56, K08 3009≠3110, K09 784≠839, K10 46≠49, K11 256≠269. The declaration's
  before-value is honest and reproduced exactly.
- At `0e5f70f` (during this review): `mismatches: 0, PASS, declaring_round 37`.
- At `543a7ce` (three commits later: assimilation `8936643`, C2 correction+counter `543a7ce`):
  `mismatches: 5, FAIL` — K07 56≠58, K08 3110≠3111, K09 839≠840, K10 49≠50, K11 269≠282.
- Re-measured at final tip `d621b71`: still `checked: 27, mismatches: 5, FAIL`.

AXES.md requires "Claims must be **causally separable** — each verifiable without the others
having landed". C3's after-value exists only at tips that exclude the other claims' artifacts; it
flipped 0→5 twice before wave 2 even dispatched, caused by the round's own declared commits. As
declared, the claim is satisfiable only by an undeclared re-correction loop after every counted
file append — the single "append-only correction of the five current self-assessment count
cells" (SCORECARD.md:1960-1962) cannot hold at "the measured round-37 branch-tip revision".

### F2 — HIGH — C1 (operability): the declared sourced-claim rows are unsatisfiable — id collision, duplicate, and false recency

SCORECARD.md:1903-1904: "C1's probe note cites a strace(1) row opened this round (S200-strace)
plus the probe's own-work row (S201-probe), both opened and mined in-round."

Observed at tip `d621b71` (corpus/SOURCES.md, landed in `8936643`): **S200 = mount(2) man page;
S201 = Btrfs fs/btrfs/ioctl.c**. CORPUS.md §SOURCES v1 fixes the id as "the **next unused**;
**never reused**" — max id at the declaration base was S199 (verified: HEAD~4 registry ends
S197/S198/S199; base registry 199 rows). S200/S201 can therefore name exactly one source pair,
and the assimilation consumed them first. Additionally:
- A strace source row already exists: **S173** (strace v7.2 `doc/strace.1.in`, tier A, round 31)
  — a new strace row this round is a duplicate, and "opened this round" is false for it.
- No `probe-child-env` own-work row exists anywhere in the registry, and C1's target
  `tools/probe-child-env-allowlist-r37.py` is not yet landed, so its own-work row cannot exist
  yet either.

C1's sourced-claim evidence sentence cannot be executed as declared: both named ids are taken by
other sources, one named source is already rowed, and the recency claim is false on both counts.

### F3 — MEDIUM — C2 (depth): the corrected predicate's decisive source has no provenance row, and the counter has no declared kill rule

The routed correction (round-36 verifier spot-check §6 item 2, `corpus/lessons/round-36-verifier-spotcheck.md:65,103`) is factually **correct**: I opened
`https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl-filter.c` on
2026-10-25T19:22:24Z and counted `field_list_has_scope_options()` — **exactly 15 OR terms**
(`arg_boot_filter`, `arg_invocation`, `arg_dmesg`, `arg_cursor`, `arg_after_cursor`,
`arg_cursor_file`, `arg_system_units`, `arg_user_units`, `arg_syslog_identifier`,
`arg_exclude_identifier`, `arg_priorities`, `arg_facilities`, `arg_since_set`, `arg_until_set`,
`arg_pattern`), matching the note's corrected table (`journalctl-v262-field-filter-r36.md:133-135`).
Located quote (function head, line 26): "bool field_list_has_scope_options(void) { return
arg_boot_filter || … arg_pattern; }".

The defect: that file is the correction's ground truth, yet it has **no SOURCES row**
(`grep filter.c` over the HEAD registry = 0 hits; the note cites it only by inline sha256 at
`journalctl-v262-field-filter-r36.md:2-3`). CORPUS.md kaika rule: "when the source is external,
`source:` cites its `S###` row in `corpus/SOURCES.md` alongside the URL and anchor"; SOURCES
rule 1: "Write it only after opening the source in the round that writes the row." The
declaration's C2 section declares no sourced rows at all (contrast C1's S200/S201 sentence and
the assimilation's row list, SCORECARD.md:1938). Secondary: C2's counter
`tools/check-journalctl-v262-corrections.py` has a real do-nothing control (exit 1 on the
uncorrected base) but **no declared kill rule or should-fail battery** — a checker dropping any
one of its three assertions still reads after-exit-0 undetected. It was also amended twice after
first landing (`718cc8f`, `d621b71`) with no freeze rule naming its bytes, unlike C1's named
sha256 freeze.

### F4 — MEDIUM — assimilation: the declaration's entry names and row-id enumeration are both false against the landed state

SCORECARD.md:1936-1938 declares THREE entries — `errno-name-discrimination-r25.md`,
`mount-errno-contract-r26.md`, `errno-contract-variance-r37.md` — and "rows
S204/S205/S214/S220/S279–S282/S286/S287 appended". Observed landed in `8936643`:
- **Two** knowledge notes, under different names: `corpus/knowledge/mount-errno-contract-r37.md`
  and `corpus/knowledge/errno-contract-variance-r37.md` (`errno-name-discrimination-r25.md` does
  not exist);
- rows **S200–S207 contiguous** (mount(2), btrfs ioctl.c, errno(3) ×3, errno-base.h, two
  own-work captures) — execution is next-unused compliant, but only S204/S205 intersect the
  declared list; S214/S220/S279–S282/S286/S287 do not exist, and six landed rows are unlisted.
The staged-id manifold `.ufo/waves/round-37/assimilation/staged-ids` (147 ids, S200–S346)
matches neither. The declaration's assimilation evidence sentence is not a countable predicate
over the state it governs.

## What verified clean (calibration positives)

- C3 before-value honest (reproduced exactly, above). C1's S1 anchor honest:
  `tools/probe-child-env-allowlist-r36.py:497-499` raises `RuntimeError('cannot create local
  master branch')` as declared.
- Axis fit per AXES.md: C1 operability (runnable probe), C2 depth (correction-complete note),
  C3 calibration ("SCORECARD entries match observed repo state") — all three genuine; distinct
  axes; lowest-axis duty (depth/adjacency tied at 8, saturation 9/window 3 correctly computed as
  not waiving) covered by C2.
- Assimilation theme is documented on the coverage map (`corpus/README.md:271-275`, "Round 37 —
  errno discrimination on existing snapshot and journal ground"); SOURCES execution was
  append-only and next-unused compliant even though the declaration mis-enumerated it.

## Residual risks / verification gaps

- Wave 2 not dispatched at review close; C1's probe V8 and kill-rule receipts are unlanded, so
  C1 is unverifiable either way yet.
- C1's kill rule is under-specified: the sensitivity conjunct ("the committed mutant probes …
  each read above 0 under the frozen probe", SCORECARD.md:1940-1941) has no declared counting
  command, target battery, or receipt format; and a skip-fix variant reading `leaking` 0 on the
  *clean* livefive battery is the expected reading of any correct probe, so the firing condition
  needs the mutant-battery reading defined or it can fire on non-defective variants.
- Active change window: HEAD advanced `0e5f70f`→`d621b71` and `LOG.md` /
  `tools/check-journalctl-v262-corrections.py` were uncommitted-modified at close; a later
  re-correction may restore mismatches 0 at a future tip — F1 is about the declaration's stated
  predicate/order, not about eventual recovery.
- PROVINCE.md itself contains no errno ground; the theme's fit rests on the corpus/README.md
  coverage map (acceptable per LEARNING.md, noted for completeness).
