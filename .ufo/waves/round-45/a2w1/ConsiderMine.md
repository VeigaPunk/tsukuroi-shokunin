VERDICT: draft

# F-7 — `considerthese` proposal mined: **Seat-harm incident log** (rounds 37-44)

Seat: `ConsiderMine`, wave `a2w1` (round 45, hyaku run 9). Read 2026-10-27, 00:30-00:40 -03. Report path:
`.ufo/waves/round-45/a2w1/ConsiderMine.md`; receipts `.ufo/waves/round-45/a2w1/ConsiderMine/` (168 KiB total).
Nothing in the lane was created or edited except this report and that receipts directory; no counter was run
(two argparse refusals only); no host query beyond read-only `git status`, `stat`, `find`, `ls`, `grep`.

## 1. Proposal survey — which of the four is still unimplemented

Receipt `w45/ConsiderMine/proposal-survey.txt` (all `w45/` = `.ufo/waves/round-45/a2w1/`):

| Proposal | `SKILL.md` hits | `corpus/lessons/` files | Status |
|---|---|---|---|
| Counter-attack scoreboard | 3 (`SKILL.md:3833`, `:3835`, `:3935`) | 1 (`corpus/lessons/round-41.md:99`) | implemented (r40-42) |
| Downstream patch-offset check | 1 (`SKILL.md:3956`) | 2 (`round-42.md:53`, `round-42-verifier-spotcheck.md:178`) | implemented (r42) |
| Cross-note correction propagation map | 0 | 1 (`round-43.md:83`, "proposal 5, read 2026-10-26") | mined in r43 |
| **Seat-harm incident log** | **0** | **0** | **not landed** — this seat |
| Burst-aware reading | 0 | 0 | unimplemented, but it is a change to how a daily reflection is read; no round-45 surface grounds it |

`grep -ric seat-harm SKILL.md` → 0; `grep -ril seat-harm corpus/lessons/` → 0. One prior build exists as a wave
artifact only: `.ufo/waves/round-44/w1/ConsiderMine.md` (round-44 seat, `VERDICT: draft`) with
`.ufo/waves/round-44/w1/ConsiderMine/seat-harm.jsonl` (8 rows) and a 13-mutant checker. It was never adopted —
the grep above is the proof — so under the lane's own standard (`.ufo` wave files are not corpus) the proposal is
still unimplemented and the round-44 text is a draft to re-derive, not a landing to cite.

## 2. What this seat built

`w45/ConsiderMine/seat-harm.jsonl` — 10 rows, rounds 37-44, fields: round, id, id_basis, class, actor, harm,
cite, quote, landing, today, status_cite, status_quote, note, plus proof_red/proof_green for closed rows.
`w45/ConsiderMine/seat-harm-log.py` — checker + per-round tally (read-only; opens lane files only).
`w45/ConsiderMine/run-mutants.py` + `mutants/` — 15 single-field mutants.

```
$ python3 seat-harm-log.py --log seat-harm.jsonl --lane <lane>        # w45/ConsiderMine/run.txt, rc=0
round  incidents  (seat-harm ledger, window 37-44)
  37  1  R37-MISROOT-NOTE-DRAFT
  38  0
  39  1  R39-SEAT-PKILL
  40  1  R40-TMP-MISROOT
  41  2  R41-TMP-MISROOT-REPEAT,R41-CAPTURE-FIFO
  42  1  R42-C1-SCRATCH-FALLBACK-TMP
  43  1  R43-L1-SCRATCH-STRAY
  44  3  R44-L1-FLEET-ROOT-FIXTURE,R44-PYCACHE-RECUR,R44-COUNTER-FIFO-LEAK
classes: fleet-root-write=2, lane-pollution=1, process-leak=2, process-signal=1, scratch-tmp=3, shared-scratch-stray=1
harms:   fleet-repo=2, host-disk=3, host-process=2, lane-tree=2, other-seat-run=1, shared-round-root=1
today:   closed-able-to-fail=2, detector-only=2, open=5, rule-only=1
open:    R41-CAPTURE-FIFO,R42-C1-SCRATCH-FALLBACK-TMP,R43-L1-SCRATCH-STRAY,R44-PYCACHE-RECUR,R44-COUNTER-FIFO-LEAK
PASS: rows=10 findings=0
```

```
$ python3 run-mutants.py                                              # w45/ConsiderMine/mutants/run.txt, rc=0
KILLED K01-cite-line-drift … K15-proof-green-names-old
killed=15/15 survived=none
```

Row contract (enforced, not decorative): `cite`/`status_cite` are lane-relative `path:line` (an absolute,
`/tmp` or `/fast/scratch` path is a finding); the quote must occur verbatim on that line; a `lesson` id must also
occur on its line; a `minted` id must be *absent* from `corpus/lessons/`; `closed-able-to-fail` is refused without
a red-shape and a green-shape cite in the same receipt. Mutants hit each check exactly once (K01-K12, K14, K15);
K13 was rewritten after its first form survived — the paraphrase `Signal only processes` is a literal prefix of the
guard sentence, so it bound nothing (recorded in `mutants/results.json`).

Population classified from: the 59 lesson-table ids of rounds 37-44 (`w45/ConsiderMine/scan-ids.txt`); rows that
name a harm to another party's surface are the 10 above.

## 3. Per-round tally, class, and whether the isolation fix landed

| Round | Id | Class | Harm | Evidence (lane bytes) | Landing | Today |
|---|---|---|---|---|---|---|
| 37 | `R37-MISROOT-NOTE-DRAFT` | fleet-root-write | fleet-repo | `corpus/lessons/round-37.md:102` | repair (quarantined copy) | detector-only |
| 39 | `R39-SEAT-PKILL` | process-signal | other-seat-run | `corpus/lessons/round-39.md:74` | none at landing | rule-only |
| 40 | `R40-TMP-MISROOT` | scratch-tmp | host-disk | `corpus/lessons/round-40.md:81` | routed → r41 | closed-able-to-fail |
| 41 | `R41-TMP-MISROOT-REPEAT` | scratch-tmp | host-disk | `corpus/lessons/round-41.md:80` | closed in r41 | closed-able-to-fail |
| 41 | `R41-CAPTURE-FIFO` | process-leak | host-process | `corpus/lessons/round-41.md:74` | line-scoped guard | **open** |
| 42 | `R42-C1-SCRATCH-FALLBACK-TMP` | scratch-tmp | host-disk | `corpus/lessons/round-42.md:79` | routed → convention only | **open** |
| 43 | `R43-L1-SCRATCH-STRAY` | shared-scratch-stray | shared-round-root, lane-tree | `corpus/lessons/round-43.md:108` | repair | **open** (both halves live) |
| 44 | `R44-L1-FLEET-ROOT-FIXTURE` | fleet-root-write | fleet-repo | `corpus/lessons/round-44.md:44`; `w1/C1ExecEdgeNames.md:246` | repair | detector-only |
| 44 | `R44-PYCACHE-RECUR` | lane-pollution | lane-tree | `.ufo/waves/round-44/w1/SentMisroot.md:22` | none (removal only) | **open** |
| 44 | `R44-COUNTER-FIFO-LEAK` | process-leak | host-process | `.ufo/waves/round-44/w1/SentMisroot.md:9`; `corpus/lessons/round-44-verifier-spotcheck.md:210` | none | **open** |

Two rows are new relative to the round-44 ledger: `R41-CAPTURE-FIFO` and `R44-COUNTER-FIFO-LEAK`, the process
leaks onto the shared host that the round-44 draft scoped out (it declared itself seat-to-seat only and listed
`R41-CAPTURE-FIFO` in its boundary paragraph). The third difference is an update, not a new row:
`R43-L1-SCRATCH-STRAY`'s shared-root half re-measured against the round-45 root.

## 4. Findings

**F1. The fixes that hold are carried by a tool argument; the prose rules do not hold.** `R40`/`R41` (scratch-tmp)
were closed by a measured red/green pair on one receipt: old invocation 1153 absolute `/tmp` mkdir calls, new
invocation 2 and no census tree (`.ufo/waves/round-41/w1/RoutedSelfAssessScratch.md:54`, `:56`). `R39`
(process-signal) has only prose: the sentence "Signal only processes you started (by PID); never
`pkill`/`killall`" is on `.ufo/waves/round-45/make-a2w1-spec.py:39` and 7 other generators, but 0 in
`.ufo/waves/round-39/make-w1-spec.py` and 0 in `.ufo/waves/round-42/make-w2-spec.py` — 8 of the 11 spec files of
rounds 37-45 (`w45/ConsiderMine/guard-presence-all.txt`). No receipt shows a seat stopped by the rule, so it is
`rule-only`, not landed.

**F2. `R44-L1-FLEET-ROOT-FIXTURE` repeated `R37-MISROOT-NOTE-DRAFT` seven rounds later, with the guard sentence
already in the wave it was dispatched to.** The guard "never create files at the fleet root … is a misroot" is in
the round-44 spec generator (`.ufo/waves/round-44/make-w1-spec.py:35`; spec 21:04:47, fixture 21:08:59); the round-37
context survives only as the lesson's wording "wave context 'seat paths are absolute'" (`round-37.md:102`), so the
earliest surviving generator that carries the fleet-root sentence is round 44's. The case
that fired was not a redirect but `dev0 "$PWD/fx/…"` with cwd at the fleet root
(`.ufo/waves/round-44/w1/C1ExecEdgeNames.md:245-246`: "one hand-written fixture argument was `dev0
\"$PWD/fx/A2-uppercase-fsid-sysfs/sysfs\"`, which created"). The only detector remains `git status` at the fleet
root; today it lists one line, another lane's in-flight report (`w45/ConsiderMine/fleet-and-pycache.txt:2`
`?? .ufo/reports/round-45/kengaku.md`), no tsukuroi stray.

**F3. Correction: the round-44 ledger marks `R42-C1-SCRATCH-FALLBACK-TMP` `closed-able-to-fail`; the incident's own
site is unchanged.** `.ufo/waves/round-44/w1/ConsiderMine/seat-harm.jsonl:5` carries `"today":
"closed-able-to-fail"` citing a refusal receipt from the round-44/45 counters. The round-42 C1 counter still makes
the argument optional and falls back to the process default:

```
$ sed -n '296p;300p' tools/score-size-invariance-r42.py
    ap.add_argument('--scratch')
    parent = a.scratch or os.environ.get('TMPDIR') or None
```

With `--scratch` absent and `TMPDIR` unset, `tempfile.mkdtemp(dir=None)` builds under `/tmp`, i.e. the reported
defect. Newer counters do refuse — `python3 tools/score-census-readers-r45.py` → rc 2 "the following arguments
are required: --revision, --scratch"; `score-scrub-arm-r44.py` → rc 2 likewise (`w45/ConsiderMine/scratch-refusal.txt`)
— so the class is closed by convention for later counters only. This row is `open` in the ledger, not closed: a
fix may not be credited at a site it never touched.

**F4. A removal is not a fix, and a `.gitignore`d path is invisible to every `git status` sweep.**
`R43-L1-SCRATCH-STRAY`'s lane half was "fixed" by deleting `tools/__pycache__` (`corpus/lessons/round-43.md:108`:
"The L1 removed the strays before wave 2 and the `.pyc` files before landing"). Round 44 rebirthed three files; round
45 has six, three of them born in this round's waves (`w45/ConsiderMine/pycache-churn.txt`):

```
2026-10-27 00:24:14|35103|tools/__pycache__/_revision.cpython-314.pyc
2026-10-27 00:31:48|33662|tools/__pycache__/check-scrub-grounding-r45.cpython-314.pyc
2026-10-27 00:35:26|25781|tools/__pycache__/score-census-readers-r45.cpython-314.pyc
pyc_count=6
```

`.gitignore:2 __pycache__/` hides all six from `git status` (the lane porcelain lists none of them), so only a
`find` over the worktree sees the class. The set also moves inside one wave: the 00:34:52 reading held 5
(`fleet-and-pycache.txt`), the 00:36:37 reading held 6 (`pycache-churn.txt`), and the extra file is timestamped
00:35:26 — a file born 00:25:49 had been removed before 00:34:52 and returned after. The count is a snapshot, not
a standing claim.

**F5. The shared round root is dirty again in round 45.** `R43` was rowed as a shared-root stray; the round-44 root
was clean; the round-45 root is not (`w45/ConsiderMine/round-root-strays.txt`):

```
2026-10-26 23:52:35.6953357230|198992|/fast/scratch/hyaku/tsukuroi-r45/base-census-r45.sh
2026-10-26 23:52:35.6979146350|202665|/fast/scratch/hyaku/tsukuroi-r45/impl-census-r45.sh
```

84 s after `w1.ready` (23:51:41), in the root every seat works from (31 directory entries including the root,
measured 00:34:52, `round-root-strays.txt`). Actor unattributed: the
pair are exported census copies (`#!/usr/bin/env bash` header), i.e. an L1-style pre-wave export or a seat's
comparison harness. I did not remove them (not mine; repair is the L1's).

**F6. `R44-COUNTER-FIFO-LEAK` is a counter/tooling leak, not a production-reader defect, and it is still open.**
A seat's gated probe variant ran `grep -ls '^scrub status:1$' "$SCRUB_DIR"/scrub.*`; a FIFO matching `scrub.*`
blocked `grep`/`head`, the counter's 1200 s timeout killed only the direct child, and 8 processes plus a private
mount namespace survived with cwd in a deleted directory (`.ufo/waves/round-44/w1/SentMisroot.md:9-16`: "8 hung
processes", "no host harm, but the namespace is leaked and unreaped"). No host mount landed. The production reader
already type-guards (`tools/tsukuroi-census.sh:2004` `if [ -L "$e" ] || [ ! -f "$e" ] … record:not-regular`, with
`mkfifo` in the `scrub-wrong-types` case at `:3279`), so the durable defect is the un-reaped process group, which
`corpus/lessons/round-44-verifier-spotcheck.md:210` still lists under "Still open from the lane's own routing: …
the orphaned w1 `grep` on a fixture FIFO". The round-44 counter-mount/process leak the orchestrator tracks in its
own run-state notes is cited here only from the lane file above, never from `.scratch`.

## 5. Exact proposed text — lesson section for `corpus/lessons/round-45.md`

```markdown
### considerthese — seat-harm incident log (`considerthese/2026-10-26.md`, proposal "Seat-harm incident log")

Mined: "Seat-to-seat damage on the shared host (pkill, `/tmp` misroot, the round-37 fleet-root misroot) is now a
recurring class separate from seat loss. A running tally per round would show whether isolation fixes are actually
landing." Ten incidents over rounds 37-44, each row bound to the lane bytes carrying it: the checker refuses a row
whose `cite` is absolute or `{/tmp,/fast/scratch}`-rooted, whose quote is not on its line verbatim, whose `lesson`
id is absent from that line, whose `minted` id already occurs in `corpus/lessons/`, or whose `closed-able-to-fail`
state lacks a red-shape and a green-shape cite in one receipt. Receipts: `.ufo/waves/round-45/a2w1/ConsiderMine/`
(`seat-harm.jsonl`, `seat-harm-log.py`, `run-mutants.py`, 15 single-field mutants, `killed=15/15 survived=none`).
A round-44 wave had built an eight-row version of this ledger as a wave file
(`.ufo/waves/round-44/w1/ConsiderMine.md`); it was never adopted (`grep -ric seat-harm SKILL.md` → 0,
`grep -ril seat-harm corpus/lessons/` → 0), so this section re-derives the rows instead of citing it, and adds the
two process leaks the draft left out of scope.

| Round | Incidents | Ids |
|---|---|---|
| 37 | 1 | `R37-MISROOT-NOTE-DRAFT` |
| 38 | 0 | — |
| 39 | 1 | `R39-SEAT-PKILL` |
| 40 | 1 | `R40-TMP-MISROOT` |
| 41 | 2 | `R41-TMP-MISROOT-REPEAT`, `R41-CAPTURE-FIFO` |
| 42 | 1 | `R42-C1-SCRATCH-FALLBACK-TMP` |
| 43 | 1 | `R43-L1-SCRATCH-STRAY` |
| 44 | 3 | `R44-L1-FLEET-ROOT-FIXTURE`, `R44-PYCACHE-RECUR`, `R44-COUNTER-FIFO-LEAK` |

| Class (n) | Landed as | Today | Deciding evidence |
|---|---|---|---|
| `fleet-root-write` (2) | repair ×2 | detector-only | `git status` at the fleet root is red while the tree exists and clean after quarantine (`round-37.md:102`, `round-44.md:44`); no rule stopped either write |
| `process-signal` (1) | none | rule-only | the sentence is in 8 of 11 wave-spec generators of rounds 37-45 and 0 in the round-39 one (`make-a2w1-spec.py:39`; `guard-presence-all.txt`); no receipt shows it firing |
| `scratch-tmp` (3) | routed ×2, closed ×1 | closed ×2 / open ×1 | old 1153 vs new 2 absolute `/tmp` mkdir calls (`round-41/w1/RoutedSelfAssessScratch.md:54`, `:56`); the round-42 counter still takes `--scratch` optionally and falls back (`tools/score-size-invariance-r42.py:296`, `:300`) |
| `process-leak` (2) | line-scoped guard ×1 | open | `round-41.md:74` guards one injected line; the class recurred as the counter's un-reaped process group (`round-44-verifier-spotcheck.md:210`) |
| `shared-scratch-stray` (1) | repair | open | round-44 root clean, round-45 root carries `base-census-r45.sh` + `impl-census-r45.sh` at top level (`round-root-strays.txt`) |
| `lane-pollution` (1) | none (removal only) | open | 6 `tools/__pycache__/*.pyc`, 3 born during round 45, invisible to `git status` (`.gitignore:2`) (`pycache-churn.txt`) |

Reading: the classes that stopped recurring are the ones whose fix is a tool argument or a per-seat path; the prose
rules did not stop theirs, and a removal did not stop `lane-pollution`. `R44-L1-FLEET-ROOT-FIXTURE` repeated
`R37-MISROOT-NOTE-DRAFT` seven rounds later while its own wave context already read "never create files at the fleet root … is
a misroot" (spec 21:04:47, misroot 21:08:59) — and the case that fired (`dev0 "$PWD/fx/…"` with cwd at the fleet root) is the one the sentence's
redirect example does not name. `R42-C1-SCRATCH-FALLBACK-TMP` was marked closed while its own counter still fell
back, which is the failure mode a tally must catch: a fix credited at a site it never touched. Rule: a seat-harm
fix counts as landed only when the incident's own site refuses the old shape and a receipt shows red before green;
prose is `rule-only`, a removal is not a fix, and the sweep must read ignored paths and the shared round root, not
only `git status`. Open: no gate reads this ledger — `git grep -l seat-harm -- tools SKILL.md corpus` exits 1 with no hits
(`ledger-gates.txt`) — so it is a checklist until one does.
```

## 6. Boundaries and what was not done

- **Excluded, with reason** (not a silent filter): `R42-BATTERY-SUMMARY-COLLISION`
  (`corpus/lessons/round-42.md:77`) — the actor is the round's own control runners and the loss was the same
  agent's artifact, no other party's surface; `R42-COUNTER-SIGINT-LEAK` (`round-42.md:80`) — residue inside the
  counter's own run root, no other seat's run; `R37-SEAT-REPORT-COUNT`, `R43-SIB-PIN-UNREPORTED`,
  `R43-MORI-ARITH`, `R44-W1-UNREPORTED-SEATS` — record/count/delivery defects, no harm to a shared surface
  (`round-37.md:103`, `round-43.md:103-104`, `round-44.md:45`; round 44's own spot-check routes D7's six untracked
  files as landing debt, `round-44-verifier-spotcheck.md:196`); `R42-HERESTRING-TEMPFILE`, `R41-PIPEFAIL-SIGPIPE`, `R44-C2-CONTROL-K17-CATCH` — counter defects.
- **Not observed, therefore not claimed.** (a) No receipt shows the `process-signal` rule stopping a seat; it stays
  `rule-only`. (b) The round-45 round-root copies and the `.pyc` writers are unattributed; I recorded timestamps
  and bytes, not owners. (c) The checker binds quotes and paths, not meaning: `today` is a judgment defended by
  `status_cite`, and the red/green numeric comparison on the scratch receipt is human-read. (d) The tally counts
  disclosures; an incident no seat disclosed and no lesson recorded is invisible to it. (e) The ledger is bound to
  the working tree, not to a revision.
- **Not done.** No C1/C2 counter, census or selftest run (the two `--scratch` refusals are argparse exits, rc 2,
  before any work); no host mutation, no service/unit/timer/sysfs/mount action, no sudo, no signalling; I did not
  delete the round-root copies, the `.pyc` files or any other seat's scratch; no tool was installed. Scratch
  `/fast/scratch/hyaku/tsukuroi-r45/ConsiderMine/` held only the refusal captures (copied into
  `scratch-refusal.txt`) and was removed at exit.

## 7. Artifacts

All under `.ufo/waves/round-45/a2w1/ConsiderMine/`; sha256 (first 16), sizes from `du -sb .` = 171663 B:

| File | sha256 (16) | Purpose |
|---|---|---|
| `seat-harm.jsonl` | `52b6dd0b45e57d2a` | 10 rows, rounds 37-44 |
| `seat-harm-log.py` | `ec0a60748ee12b31` | checker + per-round tally |
| `run-mutants.py` | `8c11d8f8e8664b21` | mutant driver |
| `mutants/` (16 jsonl + `results.json` + `run.txt`) | `2c12cdb46195ceed` (run.txt) | 15 mutants, all killed |
| `run.txt` | `d5694e7ea1a75d03` | baseline tally, `PASS: rows=10 findings=0` |
| `proposal-survey.txt` | `feb19dfceb21793d` | the four-keyword survey |
| `guard-presence.txt`, `guard-presence-all.txt` | `9b54d022f5b98a41`, `eb86fe73111a7239` | rule presence per wave spec |
| `fleet-and-pycache.txt`, `pycache-churn.txt` | `64978015b8fb022d`, `70cb6aa3946b492c` | fleet sweep, `.pyc` readings |
| `round-root-strays.txt` | `778c542db751bda1` | the two round-45 root copies |
| `scratch-refusal.txt` | `372c41ab01a40755` | rc 2 refusals and the round-42 fallback |
| `census-fifo-guard.txt` | `5d370cf007d27dc4` | production type guards, `mkfifo` selftest |
| `scan-ids.txt` | `9203c3aba21d5c2f` | 59 lesson ids classified from |
| `ledger-gates.txt` | `9c7ab24a380cfedb` | no lane gate reads the ledger (`git grep` rc 1) |
