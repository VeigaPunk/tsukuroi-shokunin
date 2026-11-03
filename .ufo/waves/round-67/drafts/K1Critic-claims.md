2026-11-03T21:53:52Z

# K1Critic — round 67 claim falsification (C1 depth, C2 calibration)

Seat K1Critic (critic, leaf). Lane base `5abc31d9`; declaration frozen at `071a55c9` (lane HEAD
`071a55c9c0fd`). Read-only lane work; the base gate was run exactly once with the item's prescribed
flags; no sandbox writes by this seat; no tool installs (item needs none). Frozen blobs
(`SCORECARD.md@071a55c9`, `corpus/SOURCES.md@071a55c9`, `tools/check-adjacency-anchors.py@5abc31d9`)
were snapshotted read-only into seat scratch `/fast/scratch/hyaku/tsukuroi-r67/K1Critic/` (deleted
before yield; every number below is reproduced verbatim here). Verdict legend: **SURVIVES** = the
declaration closes the attack; **FALSIFIED** = it does not; **NAMED-LIMIT** = gap real but
receipt-visible, smallest correction named.

---

## A1 — C1: S284 can sit directly after S283 with a URL that is not the v7.3 bytes — **FALSIFIED**

Attack: publish an S284 row whose URL does not serve the pinned v7.3 bytes and still meet every
declared predicate and counting command.

The declared C1 counting commands (SCORECARD `Round 67 — declaration`, C1 row, col "counting
command") are, in full: `git cat-file -e <rev>:corpus/knowledge/btrfs-scrub-limit-revert-r67.md`;
`git show <rev>:…note… | grep -cE '^\| SL[0-9]+ \|'`; `git show <rev>:corpus/SOURCES.md | grep -cE
'^\| S[0-9]{3,}'`; "the S284 line-number awk check"; "census validate at round end". **Every one of
them is repository-text-level; none fetches the URL the S284/S285 row carries.** The kill rule
("the v7.3 revert-after-all-devices block is absent from the re-fetched bytes → honest stop, no row
lands") re-fetches the *fetched source*, not the *published row's URL*.

$ curl -fsSL https://raw.githubusercontent.com/osandov/btrfs-progs/v7.3/cmds/scrub.c | sha256sum
  curl: (22) The requested URL returned error: 404   [curl rc 22; stream empty]
  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  -   [sha256 of empty input, rc 0]
$ curl -fsSL https://raw.githubusercontent.com/kdave/btrfs-progs/v7.3/cmds/scrub.c | sha256sum   [rc 0]
  b58942ccaff74cf2300f5d25b99624ba8e9cfcb59eda5897639f1928b277d528  -
$ curl -fsSL https://raw.githubusercontent.com/kdave/btrfs-progs/v7.3/CHANGES | sha256sum   [rc 0]
  5046bac1def81247a02d7442807a6d495de2caafbc1a7194637ef03ea958a249  -
$ curl -fsSL https://raw.githubusercontent.com/kdave/btrfs-progs/master/cmds/scrub.c | sha256sum   [rc 0]
  b58942ccaff74cf2300f5d25b99624ba8e9cfcb59eda5897639f1928b277d528  -

Observed: a plausible wrong URL (`osandov/…`, wrong mirror) serves **nothing (404)** while every
declared counter would still pass a row citing it; the real source is `kdave/btrfs-progs`
(`before/src/FETCH.txt:2-3`); and `master` currently serves **byte-identical** scrub.c, so even a
`master` URL is indistinguishable today and will drift later, undetected. The pins themselves are
genuine — the gap is counter-only, not content:

$ sha256sum …/round-67/before/src/scrub.c …/round-67/before/src/CHANGES   [rc 0]
  b58942ccaff74cf2300f5d25b99624ba8e9cfcb59eda5897639f1928b277d528  scrub.c
  5046bac1def81247a02d7442807a6d495de2caafbc1a7194637ef03ea958a249  CHANGES
$ sha256sum …/round-42/frozen/src/scrub.c   [rc 0]
  48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801  scrub.c
[scrub.c@v7.3 :1636-1652] post-results loop `/* Revert to the older scrub limits. */` after ALL
devices — matches declared v7.3 scrub.c:1640-1649. [scrub.c@v7.1 :1590-1608] revert inside the
per-device loop, before `skip`/`pthread_join` — matches declared v7.1 ~1594-1604.

Minimal extra check (name + command):
$ curl -fsSL "$(git show <rev>:corpus/SOURCES.md | awk -F'— ' '/^\| S284 /{split($2,a," "); print a[1]}')" | sha256sum
  → must equal b58942ccaff74cf2300f5d25b99624ba8e9cfcb59eda5897639f1928b277d528
  (same for S285 → 5046bac1def81247a02d7442807a6d495de2caafbc1a7194637ef03ea958a249).
Smallest safe correction: make that URL↔pin sha256 equality a C1 counting command at landing (or
extend the kill rule to require it). Precedent: round-66 measured outcome already records
"**C1 sourcing is not counted (critic K1, C1 Attack 2)** — a note with `source: S999` passes"; this
is the row-side half of the same defect class.

## A2 — C1: is depth the right axis for an inert-applicability sourced entry? — **SURVIVES (verdict: improved; ordinal 8→8)**

Read `.ufo/waves/round-67/probes/e1-applicability.md` (present at read time, 2026-11-03T21:50:21Z;
raw receipts `e1-g1..g5`). Its verdict line: "**APPLICABILITY: No** — v7.3's revert-after-all-devices
ordering cannot change any scrub on this host" (one device devid 1; `scrub_speed_max = 0` =
unlimited, so the revert is a no-op write of 0; no scrub running or recorded, monthly
`btrfs-scrub@-.timer` disabled; installed btrfs-progs is 7.1-1 with the old ordering).

AXES.md defines depth as "Verifiable technical detail — decision tables with real thresholds, named
error signatures, cited sources"; it nowhere requires local effect. The lane's own convention is
explicit in the round-66 measured outcome (SCORECARD@071a55c9:4956): C1 depth SOURCED—S283 landed
**improved** with CB4 reading the host option as *inert* ("Host applicability is measured, not
decided"), axis verdict "**depth ordinal 8 → 8 — no uplift claimed (lane convention: a sourced entry
does not by itself lift the ordinal; `SCORECARD.md:962` precedent)**".

Verdict: **improved** — the entry converts the QUALITY-98 watch firing into sourced, line-pinned
technical detail; inert applicability is measured *inside* the entry (planned SL4), exactly as r66
did; ordinal stays 8→8. One carry-forward: the probe's own "**Unverified assumption**" (Arch
`btrfs-progs 7.1-1` backport not excludable; gitlab.archlinux.org unreachable from allowed GET
hosts) belongs in SL4 as a named limit, not silently dropped.

## A3 — C2: does the base gate skip the live check without `--siblings-root`? — **SURVIVES (no)**

Verified on the exact base blob (`git diff 5abc31d9 071a55c9 -- tools/check-adjacency-anchors.py`
→ empty, rc 0; `git status --porcelain -- tools/check-adjacency-anchors.py` → empty, rc 0), citing
`5abc31d9` lines:

- `:28`  `DEFAULT_SIBLINGS_ROOT = "/home/vgpnk/Projects/shokunin"`
- `:813-814`  `parser.add_argument("--siblings-root", default=DEFAULT_SIBLINGS_ROOT, …)`
- `:856-857`  `main()` passes `args.siblings_root` into `evaluate(...)` — from the CLI it is never None
- `:467`  `evaluate(..., siblings_root=None, …)` — only the *Python-level* default is None
- `:647-652`  `if siblings_root is not None:` → live check runs; `live_digest is None` → record
  silently **uncounted** (no finding), which is C2's real declared before-state
- `:447-465`  `_live_object_hash` returns None on absent repo / unresolvable commit / git failure

Omitting the flag therefore **cannot** skip the live check; the argparse default substitutes the
fleet root. Measured (base tool, prescribed invocation):

$ python3 …/tsukuroi-shokunin/tools/check-adjacency-anchors.py --revision 5abc31d995f53d8bd7283fab78fa6d4a51e97ea6 --siblings-root /home/vgpnk/Projects/shokunin
  {"status": "PASS", … "live_object_checked": 10, "live_object_match": 10, … "findings": []}  rc=0

The trivial-PASS route that *does* exist — passing a bogus `--siblings-root` so every record is
uncounted (PASS with `live_object_checked` 0) — is closed by the frozen predicates themselves: the
honest base must show **10 of 10** and the mutant **9 of 10**; a bogus root shows 0 and fails both.

## A4 — C2: could the after FAIL be met by an unrelated failure? — **NAMED-LIMIT**

Every finding id the base tool can emit that sets `status=FAIL` (`_finding(` call sites `:153, 184,
543, 549, 556, 575, 580, 584, 591, 600, 615, 624, 628, 635, 642, 659, 669, 673, 677, 687, 692, 702,
712, 721, 725, 753, 756, 760`; the only non-literal emitter is `_emit_cannot`, CANNOT path, `:819`):

OUTBOUND-FIELDS, OUTBOUND-ID, OUTBOUND-DUPLICATE, OUTBOUND-PROPOSITION-TOO-LONG,
OUTBOUND-CENSUS-UNKNOWN, OUTBOUND-POINTER-MISMATCH, ANCHOR-SNAPSHOT-TAMPERED, ANCHOR-HEADING-MISSING,
ANCHOR-QUOTE-MISSING, ANCHOR-QUOTE-TOO-LONG, ANCHOR-POINTER-MISSING, ANCHOR-UNPUBLISHED,
OUTBOUND-CENSUS-INCOMPLETE, INBOUND-DUPLICATE, CENSUS-INCOMPLETE, INBOUND-CENSUS-UNKNOWN,
INBOUND-FIELDS, INBOUND-POINTER-MISMATCH, INBOUND-QUOTE-TOO-LONG, INBOUND-RELIED-ON-TOO-LONG,
INBOUND-CLASSIFICATION-WRONG, INBOUND-UNPUBLISHED — plus, only with `--ownership-corrections`:
OWNERSHIP-CORRECTION-MISSING, OWNERSHIP-CORRECTION-INVALID. (22 + 2 ids.)
`E-*` RevisionError ids (E-REGISTRY-SCHEMA, E-CENSUS-MISSING, E-CENSUS-UNSAFE, E-CENSUS-SCHEMA,
E-SNAPSHOT-UNSAFE, E-SNAPSHOT-UTF8, E-REGISTRY-PARSE, E-OBJECT-UNSAFE, E-OWNERSHIP-BASELINE, E-CLI,
E-REGISTRY-PATH, E-REGISTRY-MISSING, E-REGISTRY-UNSAFE, E-INTERNAL, E-REVISION-INVALID, E-GIT)
yield `CANNOT_EVALUATE` (exit 2), **not** FAIL.

Measured closure: `probes/e2-mutant-patched.json` — patched tool on the mutant:
`status FAIL`, `findings` = **exactly** `[{"id": "ANCHOR-LIVE-OBJECT-UNRESOLVED", … outbound[9]}]`,
`live_object_checked` 9, rc 1; and the before-receipt `e2-mutant-base.json` has `findings: []`, so no
unrelated failure co-fires in the measured scenario. Kill rule's false-positive direction is
measured under the **patched** tool: `e2-absent-sibling.txt/.json` (sibs tree without
`kagi-shokunin`) → `status PASS`, `findings []`, `live_object_checked 9` — absent repo does **not**
fire the new id.

Residual: the frozen predicate text says "status FAIL **with finding** ANCHOR-LIVE-OBJECT-UNRESOLVED"
— it does not freeze "findings == exactly [that id] and live_object_checked == 9", so a hypothetical
co-firing unrelated id would not violate the letter (it would be visible in the JSON receipt).
Smallest correction: freeze the exact findings-set and `live_object_checked 9` in the C2 counting
command. By-design limit to keep on record: the live check stays best-effort for absent repos (PASS
with checked<10 remains reachable *by design*; the kill rule names it).

## A5 — C2: is calibration the honest axis for a gate-overreach fix? — **SURVIVES (yes)**

AXES.md (fleet root, `The six axes`): calibration = "**Self-assessment quality: gaps named honestly,
confidence graded, overreach caught**"; signal column: "**SHONEN.md/SCORECARD entries match observed
repo state**". The base gate's PASS is precisely an overreach: it reports `status PASS` with no
finding while a live verification it claims silently did not happen for unresolvable commits
(`:647-652` uncount path; measured before: PASS 9/10, `probes/e2-mutant-base.json`). The fix makes
the gate's verdict carry the gap (FAIL + named id) instead of claiming coverage it does not have —
"overreach caught" verbatim. Not freshness (no lane claim is being re-verified against a live
surface) and not depth (the move is the gate's self-report honesty, not added technical detail).
Verdict: calibration is the honest axis; improved at claim level, ordinal 9→9 (0) per the lane's
no-uplift convention.

## A6 — predicate text vs counter behaviour — **NAMED-LIMIT (one mismatch, C1)**

- **C1 (the mismatch):** the "SOURCED — S284, S285" predicate asserts the rows name the pinned v7.3
  bytes, but no declared counting command connects a row's URL to those bytes (A1; wrong URL passes
  all counters — demonstrated above). Same defect class as the already-recorded r66 finding
  "C1 sourcing is not counted". Correction: URL↔pin sha256 equality as a counting command.
- C1 note-absence: `git cat-file -e 5abc31d9:…btrfs-scrub-limit-revert-r67.md` → rc **128** ✓
  (also absent at 071a55c9; snapshot rc 128).
- C1 SOURCES **283** rows at base ✓ (`awk '/^\| S[0-9]{3} \|/' → S_ROWS=283`); S283 is the last row.
- C1 `awk -F'|' NF == 13` ✓ — S265–S283 all measure NF=13 (`awk -F'|' '/^\| S2[6-8][0-9] /{print NF}'`).
  [Critic self-correction: my first probe printed 119 because it omitted `-F'|'` and counted words;
  the frozen check is sound.]
- C2 before **PASS 9/10** = `e2-mutant-base.json` ✓; after **FAIL + exactly ANCHOR-LIVE-OBJECT-UNRESOLVED**
  = `e2-mutant-patched.json` (rc 1) ✓; honest base **PASS 10/10** = `e2-honest-base.json` (base tool)
  and `e2-honest-patched.json` (patched) ✓; `--selftest` **PASS 25 → 26 cases, 0 failed**, rc 0
  (`e2-selftest.txt`) ✓; absent sibling **PASS, no finding** (`e2-absent-sibling.json`) ✓.
  No C2 text-vs-behaviour mismatch beyond A4's exact-set nit.

---

**Seat hygiene:** scratch `/fast/scratch/hyaku/tsukuroi-r67/K1Critic/` (frozen-blob snapshots only)
deleted before yield; no installs; no pacman/systemctl/host writes; no sandbox writes; no commits.
