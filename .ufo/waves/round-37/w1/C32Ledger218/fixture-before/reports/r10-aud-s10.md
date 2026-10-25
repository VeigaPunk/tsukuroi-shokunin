# AUD-S10 — verdict table: the census self-sweep (2 mutants re-run) + the hardened census (selftest count, live run)

Lane AUD-S10 (round-10 wave, width 32), 2026-10-14. Write scope: **this file only** —
`reports/r10-aud-s10.md` is the lane's first `reports/` file (the sibling audit lanes'
convention: `tameshi:reports/r9-aud-t9.md`, `tabi:reports/r9-aud-b9.md`,
`mado:reports/r9-aud-m9.md`); nothing else in any repo was written, no commit, no
`git add`. Scratch `/tmp/w10-aud-s10/` (evidence kept). Host probes read-only: census
runs only, `md5sum`/`wc`/`stat`/`git show`/`cmp`/`diff`, two mutant sweeps on scratch
copies; no `pacman` transaction, no `-Sy`/`-Syu`, no service action, no root, no
external site; `db.lck` absent before/after every run (checked).

Task (verbatim): "audit the census self-sweep (2 mutants re-run from the pinned
revision) + the hardened census (selftest count, live 5-plane run). Verdict table; do
NOT edit."

Method: (i) re-hash every artifact and extract my own copies of the pinned census and
the pinned mutation service from each repo's git object store; (ii) re-materialize and
re-run 2 of the sweep's 10 mutants with the pinned service; (iii) re-run the hardened
census's selftest and live mode from the pinned revision; (iv) re-derive the S10-3
receipt's numbers, including its drift table and cross-probes, from raw captures;
(v) record the concurrent moves (the census and the service both moved in this window)
as observations, never as pins.

Tags: **[obs]** measured in my window with the command named · **[inf]** inference ·
**[unk]** unsettled, probe named. Line counts are `wc -l`; the census carries an
**unterminated final line** (`main "$@"`), so Read counts one more.

Audit window: 2026-10-14 20:55:38Z – 21:07Z (17:55–18:07 -03), host `plazir27`,
user `vgpnk` (non-root).

## 0. Audited bindings

| artifact | revision bound | size | note |
|---|---|---|---|
| lane HEAD | `fac745b2813980014125390ff63defe0420b16d7` ("probation round 9 (training r8): see LOG", 17:47:30 -03) | — | tree clean at my open; round-10 seats' files appeared during the window |
| census **pinned revision** (the sweep's and the receipt's target) | md5 `e32aac98c6b54f9d7fb8bc4f348cd467` · sha256 `c396662eeb5f435d841b0c1863903dba807aa9dcbc6a67b2439fdfb13670c650` | 2349 `wc -l` / 123 410 B | mtime 17:17:50.225952228 -03; `git show HEAD:tools/tsukuroi-census.sh` hashes equal; worktree == blob at 20:55:38Z |
| census **round-10 hardened revision** (in flight at close) | md5 `945c76fc6cc548e47b91c23a9637df75` · sha256 `1045244387ffcd5d3db481dd0d3d30e34097abc24744d954e791b81d28b20c11` | 2402 `wc -l` / 126 075 B | mtime 18:03:00.967 -03, `M`; == `/tmp/w10-tsukuroi-s102/census.hardened.sh`; **uncommitted** |
| S10-2 defect spec | md5 `48a3a388fe5ca587076b9ed5b89344fa` | 4 085 B / 10 defects | `s102.defects.spec` == `spec.copy` in every sweep dir |
| S10-2 sweep-before (live service) | 10 rows, 17:56:56–17:58:49 | evidence 11 files | `/tmp/w10-tsukuroi-s102/sweep-before/` |
| S10-2 sweep-before-frozen (pinned service) | 10 rows, 18:00:55–18:02:48 | same | service copy `mutate-and-run.cf41efaa.sh` (sha256 = the pin) |
| S10-2 sweep-after (on the hardened revision) | 10 rows, 18:03:56–18:05:54 | evidence 11 files | all KILLED |
| S10-2 sweep-covering (CLI cases) | 2 rows, 18:06:15–18:06:39 | evidence 3 files | S1/S2 KILLED |
| S10-3 receipt | md5 `c5041b5d03e38c774637f47a24304ca8` · sha256 `d7e10ada2e762adfc8a4451d863cc2194ca373c83a21681c4e03944729d0f1a2` | 183 `wc -l` / 15 506 B | `corpus/knowledge/census-closeout-receipt-r10.md`, mtime 17:54:47 -03; stable 17:5x–18:07Z |
| mutation service **pin** | sha256 `cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75` | 61 632 B | == `tameshi` HEAD blob `b8eb96e1:tools/mutate-and-run.sh`; the live path was **dirty and moving** in this window (§4) |

## 1. Verdict table

**Self-sweep rows (S)** — S10-2's mutation arc, `/tmp/w10-tsukuroi-s102/`:

| # | check | scope / method | result | verdict |
|---|---|---|---|---|
| S1 | target binding | sha256 of the seat's `census.pristine.sh`, `sweep-before/pristine…`, `sweep-before-frozen/pristine…` vs the pin | all three = `c396662e…`; my own `git show fac745b:tools/tsukuroi-census.sh` = `c396662e…` | **PASS** |
| S2 | mutant identity column | recompute sha256 of all 10 mutant files in `sweep-before` vs `results.tsv` | **10/10 match** (K1 `a199fc4b…` … H4 `625b266a…`) | **PASS** |
| S3 | **K4 re-run from the pinned revision** | my materialization from the pinned bytes + pinned service; `--suite 'bash "$MUTANT" --selftest'` | **KILLED**, exit 1, 11 138 ms; failing case `blocked: oom watch — window unreadable (S9-2): plane evidence missing: '^PLANE oom: BLOCKED \(window unreadable: journalctl --list-boots rc=4'`; suite `FAIL (74 cases, 73 passed, 1 failed)`; matches the record | **PASS** |
| S4 | **H4 re-run from the pinned revision** | same | **SURVIVED**, exit 0, 11 099 ms; suite `PASS (74 cases, 74 passed, 0 failed)`; matches the record | **PASS** |
| S5 | re-run provenance | `cmp` my mutants vs the seat's | K4/H4 **byte-identical**; K4 diff vs pinned = 1 line (`:1036` `OOM_V=BLOCKED`→`DEGRADED`); H4 = 2 lines (`:1381-1382`) | **PASS** |
| S6 | evidence invariance | `cmp` control/K4/H4 outputs across seat sweep-before, seat frozen sweep, my sweep | **all byte-identical** (control `604818b2…`, K4 `c8b8c788…`, H4 `604818b2…`) | **PASS** |
| S7 | verdict tables, before vs before-frozen | field compare on id/verdict/exit/sha | **10/10 rows match** (K1–K6 KILLED, H1–H4 SURVIVED) | **PASS** |
| S8 | post-hardening proof | my run of the hardened revision's selftest; my re-run of H4 on it | selftest `PASS (80 cases, 80 passed, 0 failed)`, rc 0, stderr empty; **H4 KILLED** on the hardened revision, failing case = the **new** covering case `blocked: update-safety -Sup unreadable fails closed (S10-2): exit 1 wanted 2`; seat's `sweep-after` = 10/10 KILLED; `sweep-covering` S1/S2 KILLED | **PASS** |
| S9 | service revision **during** sweep-before | see §4; the seat's own hardening comment says "10 defects, **two tool revisions**"; the first sweep's evidence files are suite outputs only (no `MUTATE_TOOL` line in them) | the executed revision per mutant is **[unk]**; the declared pin is honored by my re-run and by the seat's frozen re-sweep, which reproduce every verdict | **noted** (finding, disclosed and remedied) |
| S10 | audit scope | mutants actually re-run by this lane | 2/10 pre-hardening (K4, H4 — assigned); 1/10 post-hardening (H4); the other 17 rows are identity-verified only | **noted** (scope) |

**Hardened-census rows (C)** — the S10-3 receipt, round-9 landed revision:

| # | check | scope / method | result | verdict |
|---|---|---|---|---|
| C1 | census revision binding | my re-hash vs receipt §2 | md5/sha256/2349/123 410 B all equal; = HEAD blob | **PASS** |
| C2 | selftest count | my run `bash tools/tsukuroi-census.sh --selftest` (20:55:4xZ) | rc=0 in ~11.5 s; 74 `PASS` lines; terminal line `TSUKUROI_CENSUS_SELFTEST: PASS (74 cases, 74 passed, 0 failed)`; stderr 0 B; == `SKILL.md:1359` and `:1373` restatements (grep -n) | **PASS** |
| C3 | **live run** | my two runs 20:55:58Z / 20:56:01Z, unpiped, stdout/stderr separate | rc=1 both; **six** `PLANE` lines; rollup `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=HEALTHY)`; stderr 0 B; plane-name set == rollup-key set, **6/6 SET-MATCH** (extract both, sort, compare); exit map consistent (crown = worst plane = DEGRADED) | **PASS** — with the dispatch's "5-plane" premise **stale** against the realized 6 (delta matches the receipt's §0; see §3) |
| C4 | zero mutation | census md5 before/after all runs; `git status --porcelain`; `ls /var/lib/pacman/db.lck` | hash unchanged; status unchanged (bar the seats' own files); `db.lck` absent | **PASS** |
| C5 | receipt §6 drift table | re-read the seat's raw captures `live.out` vs `live2.out` (77 s apart) | `diff` = exactly 2 lines (header stamp + drivers line); of §6's six field readings, **four moved** (`C6_avail_kb` 18 329 696→17 676 964; `C6_psi_full_total_us` 72 681 373→72 758 668; `C5_pswp` 74 576 915→74 576 965; `C6_shmem_kb` 8 573 292→8 577 692), two held (`err` 798, `coredump` 523, 0/0); all table cells reproduce byte-exactly from the captures | **PASS** (minor: §1's "identical line-for-line except the six fields" is imprecise — four moved, and the header timestamp line differs too) |
| C6 | receipt §7 cross-probes | re-run from my shell | `journalctl --list-boots --no-pager \| wc -l` = **14** (= 13 boots + header); `pacman -Qm \| wc -l` = **16**; `stat -c '%w %n' /var/lib/pacman/sync/*.db` → core/extra/multilib/omarchy birth `2026-10-11 12:54:13.542054496 -0300` (4 dbs), `offline.db` `2026-10-03 17:41:33.994891750 -0300` — all agree with §7 | **PASS** (minor arithmetic nit: §7 row 3 states "3 d 7 h 58 m" and "11 d 3 h 11 m"; recomputed against the §0 window end 20:52:37Z: **3 d 4 h 58 m** and **11 d 0 h 11 m** — the -0300 birth stamps were read as UTC (+3 h); both floors, 3 d and 11 d, are unchanged) |
| C7 | receipt stability | md5 at 17:5xZ and 18:07Z | `c5041b5d…` / 183 / 15 506 B both times; the scribe's draft recorded earlier sizes (15 176 B → 15 313 B) — the file **was moving before my binding**; my binding is the close read | **noted** |
| C8 | §5 zero-mutation corroboration | seat's raw scratch | `live.err`, `live2.err`, `selftest.err` all 0 B; `live.rc` reads `live rc=1`; my own status/db.lck checks in C4 | **PASS** |
| A1 | audit did not edit | `git status --porcelain` at close | ` M SKILL.md`, ` M tools/tsukuroi-census.sh`, `?? corpus/knowledge/calibration-synthesis.md`, `?? census-closeout-receipt-r10.md`, `?? plans/round-10-record-draft.md`, `?? plans/round-11.plan.md` — all other seats'; this lane wrote only this file; audited artifacts re-hash identical | **PASS** |

Aggregate: **the two re-run mutants reproduce their recorded verdicts byte-for-byte
from the pinned revision with the pinned service; the hardened census's selftest count
(74) and live run (six planes, `DEGRADED`, rc 1) reproduce; every number I re-derived
holds, with two minor receipt-level nits (§1 wording, §7 arithmetic) that change no
conclusion.** The one substantive finding is the service-revision split inside the
first sweep (§4) — disclosed by the seat itself and remedied by its frozen re-sweep.

## 2. The 2 mutants re-run (method → result)

- Pinned inputs, extracted from git object stores (never from a moving worktree):
  `git -C tsukuroi-shokunin show fac745b:tools/tsukuroi-census.sh` → sha256
  `c396662e…` (my copy `/tmp/w10-aud-s10/census.pristine.sh`);
  `git -C tameshi-shokunin show b8eb96e1:tools/mutate-and-run.sh` → sha256
  `cf41efaa…` (my copy `/tmp/w10-aud-s10/mutate-and-run.sh`).
- Spec: the K4 and H4 blocks extracted **verbatim** from the seat's `spec.copy`
  (md5 `48a3a388…`) → `/tmp/w10-aud-s10/audit.defects.spec`; the tool's own
  `count==1` assertion on each `@old` passed, so both edits bind the pinned bytes.
- Invocation (20:59:33Z): `bash mutate-and-run.sh --target …/census.pristine.sh
  --defects …/audit.defects.spec --suite 'bash "$MUTANT" --selftest' --workdir
  /tmp/w10-aud-s10/sweep`. Tool-provenance line captured:
  `MUTATE_TOOL: … sha256=cf41efaa…`; `MUTATE_TARGET: … sha256=c396662e… bytes=123410`.
- Result: `CONTROL: GREEN (11089 ms, 74/74)`; **K4 KILLED** (11 138 ms, suite 73/74,
  the oom-window BLOCKED case is the one that bites); **H4 SURVIVED** (11 099 ms,
  suite 74/74); `MUTATE_RESTORE: OK` (target sha before = after = pristine);
  `kill-rate=50% (1/2)`.
- Comparison: my produced mutants are **byte-identical** to the seat's
  (`ee60ec0a…` / `625b266a…`), and the suite outputs (`K4.out`, `H4.out`,
  `control.out`) are byte-identical to the seat's raw evidence in both of its
  sweeps — the record's K4/H4 verdicts are exactly reproduced, not merely similar.

## 3. The hardened census (S10-3 receipt) — my re-derivation

- The receipt's headline claim reproduces on my own runs against the pinned
  revision: six `PLANE` lines, `DEGRADED`, rc 1, both times; `--selftest`
  `PASS (74 cases, 74 passed, 0 failed)`, rc 0.
- The dispatch premise "5 PLANE lines" is **stale against the realized gate**
  (six emitters, `tools/tsukuroi-census.sh:2324-2329`; rollup `:2339`). My
  measurement agrees with the receipt's §0 delta, and with the stale wording it
  cites in `LOG.md` (last line) and `SCORECARD.md:21` (the row is also truncated
  mid-parenthesis before `wave-9 32-lane (…`). Neither file was repaired by me.
- Counts-move-together: the executed count (74) equals both live restatements
  (`SKILL.md:1359`, `:1373`) and the receipt §3; the history lines (`:1197` 63,
  `:1314` 63) stand as history.
- The 74-case suite's determinism is proven across three independent runs in this
  window: the seat's two sweeps and mine produced byte-identical `control.out`.

## 4. The service revision inside sweep-before — finding, disclosed

Timeline, all [obs] (mtime of the live service path and of the sweep's evidence):

- 17:56:56 seat control run → 17:58:49 last mutant of `sweep-before` (10 rows).
- `tameshi-shokunin/tools/mutate-and-run.sh` live-path mtimes: **17:58:19.2**
  (sha256 `5807fd38…` when read), **17:58:47.9** (`77e40aae…`), 18:00:00.9
  (`75ed934d…`) — i.e. the live service file was being rewritten **during** the
  sweep's window (tameshi's own round-10 seat T10-2, per the tool header's r10-2
  attribution). The committed pin is `cf41efaa…` (= tameshi HEAD `b8eb96e1`'s blob).
- The seat's own hardening comment in the census diff states the case plainly:
  "Pre-hardening sweep via the tameshi service (target pin c396662e…, 10 defects,
  **two tool revisions**)".
- Remedy, observed live: at ~18:00:46 the seat created
  `/tmp/w10-tsukuroi-s102/mutate-and-run.cf41efaa.sh` (sha256 = the pin) and re-ran
  all 10 mutants against it (`sweep-before-frozen`, 18:00:55–18:02:48) — verdict
  table identical to the first sweep (S7).
- What no artifact proves: which live revision executed which mutant in
  `sweep-before` — its per-mutant evidence is suite output, so no `MUTATE_TOOL`
  line was captured **[unk]**. What repairs re-derivability: the frozen re-sweep
  plus my pinned re-run (S3–S6) — both reproduce every overlap verdict.
- My re-run used the declared pin only; the intermediate dirty revisions were
  never committed to tameshi and are not relied on anywhere in this report.

## 5. The round-10 hardening (in flight at my close)

- After the pre-hardening sweep, S10-2 hardened the census: working-tree revision
  md5 `945c76fc…` / sha256 `10452443…`, 2402 `wc -l` / 126 075 B, `M`, mtime
  18:03:00 -03; **== its scratch `census.hardened.sh`** [obs]. The diff adds a
  `check_cli` helper and covering selftest cases for the sweep's four survivors
  (H1 sample cap, H2 CLI, H3 rollup order, H4 `-Sup` fail-closed), two of which
  (the CLI pair) are proven by the `sweep-covering` mutants S1/S2 (both KILLED).
- My runs of that revision: `--selftest` → rc 0, `PASS (80 cases, 80 passed, 0
  failed)`, stderr empty (74 → 80 cases); live → rc 1, six `PLANE` lines, the same
  rollup. My post-hardening H4 re-run → **KILLED** with the new covering case
  named (S8).
- **Not a landed revision**: it was uncommitted at my close and may move further;
  my rows bind to `945c76fc…` only. If it lands differently, every claim about
  "the round-10 hardened census" must be re-hashed and re-run.

## 6. Unknowns register

1. **S10-2's landed record**: no note/receipt for the self-sweep existed in the
   tree at my close (21:07Z) — this audit binds the scratch artifacts plus the
   in-tree hardening diff. If a landed note carries different pins, re-bind [unk;
   probe: read it and re-hash].
2. **Executed service revision per mutant in `sweep-before`** [unk]; probe: a
   `MUTATE_TOOL` capture per sweep invocation (the tool prints one; the seat's
   evidence files do not carry it). The frozen re-sweep and my re-run supply the
   pinned-service results in the meantime.
3. **Coverage of this audit**: 2/10 pre-hardening mutants re-run by me (as
   assigned), 1/10 post-hardening; the remaining rows are identity-verified only
   (S2). No full re-sweep by a non-author exists yet.
4. The census (and its round-10 hardening) may keep moving; the hardened revision
   is uncommitted, and the `SKILL.md` append was landing as I closed (` M
   SKILL.md`).
5. tameshi's live service keeps moving (three rewrites observed); my service pin
   is the HEAD blob `cf41efaa…` only.
6. The receipt's own carried [unk]s — the transient selftest temp-dir attribution,
   the "5-plane" wording repair, the `corpus/README.md` indexing — are carried,
   not settled here.
7. **Naming**: the round-10 record draft calls the ten-round synthesis "the
   self-sweep" (`plans/round-10-record-draft.md:8`, `:400`; the note landed as
   `corpus/knowledge/calibration-synthesis.md`, md5 `ed8dec89…`, 463 `wc -l`).
   This audit binds the assignment's "census self-sweep (2 mutants…)" to the
   census **mutation** sweep (S10-2's arc), which is the only read that contains
   mutants. The synthesis note itself is **outside this audit's scope**.
8. The dispatch's "5-plane" premise — stale vs the realized six; the repair call
   belongs to the record/scribe seats (§3).

## 7. What this is not

- Not a remediation and not a host-health review: every live value quoted here is
  a capture with a timestamp, not a standing fact.
- Not the non-author verification of the two planes round 9 added (their D13
  contract verification is another seat's product; this lane re-ran gates and
  mutants only).
- Not the acceptance of round 10: it audits the two named subjects at the named
  revisions; the round's other artifacts (synthesis, record, SKILL append,
  README/SCORECARD repairs) are not audited here.
- Not a commit: the L1 owns every commit; this file is the lane's only write.