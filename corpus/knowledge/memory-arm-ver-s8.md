# VER-S8 — independent verification of the S7-2 memory arm + seat S8-1's mutant set

source: independent read-only work by the VER-S8 seat (the round-8 OOM-arm named verifier),
host `plazir27`, user `vgpnk`, non-root; own commands run 2026-10-14 19:11:12–19:22:48Z
(16:11–16:22 -03); scratch `/tmp/w8-ver/` (`poll.log`, `live-probes.txt`, `live-r7.out`,
`selftest-r7.out`, `arm-mutants.spec`, `s81.spec`, `arm-mutants2.spec`, `battery.sh`,
`battery-results.txt`, `gap-*.txt`, `sweep1/`, `sweep-s81/`, `sweep-m17/`). No file was
edited by this seat; the only writes are that scratch and this note. No transaction, no
install/upgrade/remove/restart, no cgroup/journal write, no external site, no root.
Claim tags: **[observed]** / **[inference]** / **[unknown]**.

Target of verification (polled for, per the assignment): the **round-7 memory-pressure arm of
lane S7-2** — the AUD-X7 gap (`LOG.md:170`, "S7-2's memory arm has no non-author
verification (AUD-X7) — queued") — as landed in `tools/tsukuroi-census.sh`; and the round-8
mutant-set artifact by seat **S8-1**, `corpus/knowledge/memory-arm-mutants-s8.md`, which
landed inside this seat's poll window (16:17:08 -03 / 19:17:08Z; md5
`a09e5604a9a818f38096569365d48823`, 181 `wc -l` / 182 as read — unterminated final line).

Pins (re-measured by this seat):

- **census revision**: md5 `e2c4558a3ae4ddd2eca67e8f4d64281c`, sha256
  `bba6cdf6f5b7a7372e43230821bb7c12aa64192266c549f39475c948803a4f55`, 1472 `wc -l`, 73 919 B,
  mtime 2026-10-14 15:33:21 -03; identical to the HEAD `aa136d6` blob
  (`git show HEAD:tools/tsukuroi-census.sh | sha256sum` equal). Unchanged through
  19:22:48Z; my poll (20 s sampling from 19:11:12Z) recorded no HEAD or census movement
  [observed].
- **tameshi's mutation runner**: sha256 `cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75`,
  1341 L — the same pin S8-1's note records; unchanged after all my runs [observed].
- no round-8 census revision and no `*baseline*` / `*.tsv` artifact existed at 19:22:48Z
  (`find` over the tree; `git status --porcelain` = 4 untracked sibling files only) [observed].

**Verdict: CONFIRMED — AUD-X7 is closed for the S7-2 memory arm as landed at `e2c4558a…`,
with coverage debt named, not smoothed. 0 live measurement claims refuted. The arm's 8
shipped cases have measured kill power (my independent replay of S8-1's 11-defect set
reproduced all 11 verdicts and all 11 mutant sha256s byte-for-byte). 9 clause sites stay
un-exercised by the 49-case suite (3 named by S8-1, 5 by me, 1 = the sibling S8-1 named
unmeasured); every one is detected by this seat's independent battery — coverage debt, not
silent gaps. The round-8 half of the plan's measure (the new `PLANE oom` watch + ≥2 baseline
rows re-executed by a non-author) is not verifiable at this pin: nothing has landed (owner:
arm seat).**

## 1. What the arm claims, re-measured (my run of the landed revision)

`bash tools/tsukuroi-census.sh` (my invocation, 2026-10-14T19:12:2xZ): rc=1 [observed]

```
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=139 (oom=1 io=70 gpu=0 other=68) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=4 nodes=6 pci_10de=2; mem=[DEGRADED] C1_kernel_oom=1 C2_sysd_oom=3 C3_sigkill=3; C4_sweep=190 C4_present=2[user.slice,user.slice/user-1000.slice] C4_local=0; C5_swap_fail=5922849 C5_swap_peak_pct=99% C5_pswp=72315769/94058025 C5_sock_throttled=67558; C6_psi_some_avg300=0.04 C6_psi_full_avg300=0.04 C6_psi_full_total_us=69186087 C6_avail_kb=19155736 C6_shmem_kb=6935768; guards=max/max oom.group=0; r6 vocab: oom-event-plane.md §8)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED)
```

Hermetic suite, my run: rc=0, `TSUKUROI_CENSUS_SELFTEST: PASS (49 cases, 49 passed, 0
failed)`, 49 `PASS` lines, 8 of them carrying `(S7-2)` [observed].

## 2. My own probes, the gate not used

| signal | my command (abridged) | my result (19:12:13–22Z) | arm line |
|---|---|---|---|
| C1 kernel OOM family | `journalctl -k -b -p err -o json --grep '<CLASS_OOM>'` | rc=0, **1** line (23:44:30.638238 `Out of memory: Killed process 1732581 (python3)`) | `C1_kernel_oom=1` |
| C2 attribution | `journalctl -b -o json --grep 'kernel OOM killer killed some processes'` | rc=0, **3** messages — 2 at 23:44:30 (`app-…scope`, `user@1000.service`), 1 at 13:10:59 (`user-1000.slice`) | `C2_sysd_oom=3` |
| C3 kill9/teardown | `journalctl -b -o json --grep "status=9/KILL\|Failed with result '(signal\|oom-kill)'"` | rc=0, **3** lines | `C3_sigkill=3` |
| C4 sweep | `find /sys/fs/cgroup -xdev \( -name memory.events -o -name memory.events.local \)`, awk nonzero `oom_kill` | **190** files; nonzero = **2** (`user.slice`, `user.slice/user-1000.slice`, each `oom_kill 1`); `.local` nonzero = 0 | `C4_sweep=190 C4_present=2[…] C4_local=0` |
| C5 swap fail | awk `fail` of slice `memory.swap.events` | **5 922 849** | = |
| C5 peak % | `memory.swap.peak` 36 744 949 760 B ÷ 1024 ÷ `SwapTotal` 35 917 176 kB | **99 %** | `C5_swap_peak_pct=99%` |
| C5 pswp/sock | `memory.stat` pswpin 72 315 769 / pswpout 94 058 025; `sock_throttled` 67 558 | same at 19:12:13Z | `C5_pswp=72315769/94058025 C5_sock_throttled=67558` |
| C6 PSI | `/proc/pressure/memory` some avg300 0.04 / full avg300 0.04, full total 69 151 811 µs | 19:12:13Z | arm read 69 186 087 µs at its later instant |
| C6 meminfo | `MemAvailable` 19 463 420 kB / `Shmem` 6 935 716 kB | 19:12:22Z | arm read 19 155 736 / 6 935 768 kB at its instant |
| guards | slice `memory.max`=max, `memory.high`=max, `oom.group`=0 | same | `guards=max/max oom.group=0` |

Live counters drift between instants (pswp/sock/PSI/meminfo all move); the readings agree
wherever taken at comparable instants, and where they differ the difference is the known
drift, not a disagreement [observation + inference].

## 3. S8-1's mutant set, re-run independently (transcribed from the note alone)

Method: spec transcribed by this seat from `memory-arm-mutants-s8.md` §3 — no S8-1 scratch
was read (their `/tmp/w8-tsukuroi-s81/` never accessed); run with tameshi's runner,
`--suite 'bash "$MUTANT" --selftest'`, target = the repo file (the runner never writes the
target; restore proof in §8). Headline verbatim from my run:

```
CONTROL: GREEN (exit=0 … pristine-sha256=bba6cdf6…)
MUTATE: DONE (target=memory-arm-ver-s8-replay defects=11 killed=8 survived=3 inconclusive=0 kill-rate=73%)
MUTATE_RESTORE: OK (target-sha256 before=bba6cdf6… after=bba6cdf6…)
```

| id | S8-1 verdict | my verdict | S8-1 sha (short) | my sha (short) | my failing-case count |
|---|---|---|---|---|---|
| D1 | KILLED | KILLED | `4c71f6c5` | `4c71f6c5` | 10 (incl. the owning quiet case) |
| D2 | KILLED | KILLED | `51f70ab7` | `51f70ab7` | 1 (owning only) |
| D3 | KILLED | KILLED | `5ef739ad` | `5ef739ad` | 1 |
| D4 | KILLED | KILLED | `80f9bbb5` | `80f9bbb5` | 1 |
| D5 | KILLED | KILLED | `5e1aaa64` | `5e1aaa64` | 1 |
| D6 | KILLED | KILLED | `729e90c2` | `729e90c2` | 1 |
| D7 | KILLED | KILLED | `4ef70513` | `4ef70513` | 1 |
| D8 | KILLED | KILLED | `6ced6f50` | `6ced6f50` | 1 |
| D9 | SURVIVED | SURVIVED | `4b3609de` | `4b3609de` | 0 |
| D10 | SURVIVED | SURVIVED | `bd27da6f` | `bd27da6f` | 0 |
| D11 | SURVIVED | SURVIVED | `4ff09ff1` | `4ff09ff1` | 0 |

All 11 mutant sha256s reproduce byte-for-byte; all 11 verdicts and the per-case attribution
reproduce (D2–D8 kill exactly their owning case; D1 kills 10, the owning quiet case among
them). Their §7.2 spot-check reproduces: the D2 evidence log carries exactly one `FAIL`, and
the captured plane line shows `C4_present=7` (the value-as-count defect) [observed].

## 4. My own complementary mutant set (16 defects, pre-registered)

Method: own spec `/tmp/w8-ver/arm-mutants.spec`, expectations written before the run
(`/tmp/w8-ver/manifest.md`: a predicted verdict per defect), same runner and suite, target =
the repo file. Result: **killed 11 / survived 5 / inconclusive 0 (69 %); control green;
restore OK**. Killed: M01 (C1 regex drops `oom_reaper`), M02 (presence flag accepts any
value), M03 (`.local` folded into `present`), M05 (swap-fail never degrades), M07 (unknown
never degrades), M08 (cgroup sweep cap 4000→1), M09 (swap pct arithmetic), M11 (C1 count
+1), M13/M14 (dispatcher misroutes C2/C3), M16 (sweep counter frozen). Prediction score
15/16: M01 was predicted SURVIVED and was killed — see §6 D1 for the mechanism.

Survivors (each is a clause with **no fixture driving it**):

| id | site (landed revision) | defect | why it survives |
|---|---|---|---|
| M04 | `:702` | `journalctl` rc=1 read as unknown instead of "0 entries" | no fixture sets an `oom-*.rc` to 1; the rc=1 path (the documented trap, `:695-697`) is unexercised |
| M06 | `:795` | BLOCKED condition `&&` → `\|\|` | no fixture has exactly one of journal/cgroup readable (quiet: both; blocked: neither) |
| M10 | `:756` | meminfo override ignored (hardcoded `/proc/meminfo`) | the swap fixture's `SwapTotal` equals the live host's value; the quiet peak is 0 (0 % either way) |
| M12 | `:801` | guards fields swapped (`$g_max/$g_high` → `$g_high/$g_max`) | every fixture sets `memory.max` and `memory.high` to the same token (`max`) |
| M15 | `:777` | PSI some-avg300 value read from `total` | no case asserts any C6 PSI value; only the C6-unknown path is asserted |

## 5. Independent fail-closed battery (15 cases, 0 failures on the control)

Own fixtures + expectations (`/tmp/w8-ver/battery.sh`, `/tmp/w8-ver/battery-results.txt`),
built by extracting the author's own dispatcher and `fx_default` from the pinned revision
(the fixture *shape* is the author's; the *cases* are mine). All 15 cases passed against the
control. Cases include the paths the shipped suite does not drive:

- **B3** all three journal greps exit rc=1 → the arm reads 0 and stays HEALTHY (the M04
  semantics, verified independently).
- **B4** rc=3 → `unknown=[C1 C2 C3]`, DEGRADED, never a pass.
- **B5 (B5b in the results file)** no cgroup + journal unreadable → BLOCKED (rc=2).
- **B6** `oom 5` (non-kill counter) nonzero → C4 stays 0 (presence flag is `oom_kill`, not
  `oom`/`oom_group_kill`).
- **B7** swap peak 99 % with `fail=0` → printed, verdict-neutral (peak is not a meter).
- **B8** meminfo unreadable → `unknown=[C6-meminfo]`, DEGRADED.
- **B11** peak vs a fixture `SwapTotal` that differs from the live host → the pct must come
  from the override (97 %).
- **B12** `memory.high=123456789` → `guards=max/123456789` (field order pinned).
- **B13** fixture PSI with distinct avg300 and total → the avg300 field is asserted.
- **B14** `memory.swap.events` unreadable while the slice exists → `unknown=[C5-swap]`.
- **B15** the sibling `memory.stat` unreadable → `unknown=[C5-stat]` (S8-1's note names this
  sibling **unmeasured**; this seat measured it).

Battery vs the survivors — each is detected by at least one of my cases, so the debt is
suite coverage, not undetectable semantics [observed]:

| survivor | caught by (my battery on that mutant) |
|---|---|
| M01 | B4, B5, B9 (the mutant breaks the C1 route/count) |
| M04 | B3 (rc=1 read as unknown → DEGRADED where HEALTHY is required) |
| M06 | B4 (mixed readability → BLOCKED where DEGRADED is required) |
| M10 | B11 |
| M12 | B12 |
| M15 | B13 |
| D9 (S8-1) | B4, B5 |
| D10 (S8-1) | B8 |
| D11 (S8-1) | B14 |
| **M17** (my supplementary defect, `:752`, `C5-stat` unknown dropped) | **B15**; M17 itself **SURVIVED** the shipped suite (1-defect sweep, own spec `arm-mutants2.spec`) |

M17 is the measurement S8-1's §5 explicitly left open ("named as unmeasured, not assumed
equal"): the C5-stat sibling is a survivor too, and it is caught by B15 [observed].

## 6. Deltas the verifier found (kept, not smoothed)

- **D1 — my prediction error on M01, and why it matters.** I predicted M01 (dropping
  `oom_reaper` from `CLASS_OOM`) would survive; it was killed. Mechanism [observed]: the
  suite's stub dispatcher routes the C1 probe by the literal pattern `*--grep*oom_reaper*`
  (`:971`), so removing the token from the regex changes which fixture file the C1 command
  reads — the kill is a routing coupling, not a semantic assertion. The stub never filters by
  the grep pattern at all, so regex *semantics* are only indirectly covered [inference].
  Recorded as a prediction error, not smoothed.
- **D2 — consolidated coverage debt: 9 clause sites un-exercised by the 49-case suite.**
  S8-1's D9/D10/D11, my M04/M06/M10/M12/M15, and M17 (above). The 8 shipped S7-2 cases have
  measured kill power for the clauses they own (S8-1's sweep + my replay agree exactly); the
  debt is the un-owned clauses, and every one is detectable by a case built from the arm's
  own vocabulary [observation + inference].
- **D3 — the round-8 arm has not landed at this pin.** The plan proposes (a) the OOM plane as
  the census's next plane line and (b) new-vs-baseline rows; at 19:22:48Z the census is
  unchanged, no `*baseline*`/`*.tsv` exists, and the landed S7-2 arm's C1 is boot-scoped
  (`-b`) where the plan proposes a retained-window scan. The plan's ≥2-baseline-rows
  spot-check is therefore unverifiable by this seat; it is carried, owner: arm seat
  [observation for the state; inference for ownership].
- **D4 — method delta vs S8-1.** Their sweep ran against a byte copy under
  `/tmp/w8-tsukuroi-s81/`; mine targeted the repo file directly (the runner never writes the
  target) — identical mutant bytes prove the same instrument outcome either way [observed].

## 7. Not re-verified by this seat

- The live host's *unreadable* states (probe errors, missing slice files): forcing them
  read-only is not possible; my battery used hermetic fixtures, and the arm's own live
  unknowns are state/timing-dependent [unknown].
- The other planes' arms (packages/systemd/journal, and the non-mem part of drivers) were
  exercised only as the suite's 41 non-S7-2 cases; my sweep touched the memory-arm code, its
  regex constants and the selftest dispatcher — not the rest of the gate.
- The cgroup counter-lifecycle model Q2 and event-B's H1–H3 readings stay `oom-event-plane.md`'s
  carried unknowns; the presence-flag rule is the response, and I verified only that the arm
  applies it (B6).
- Whether S8-1's run produced the same per-case attribution as mine is [inference] — their
  scratch was not read; my run's attribution derives from identical mutant bytes.

## 8. Mutation statement

Every command above is a read or a run on `/tmp` copies: `journalctl`, `find`/`awk`/`cat`
over `/sys/fs/cgroup` and `/proc`, `pacman`-free, one live gate run (writes nothing) and
hermetic `--selftest` runs (fixtures under `mktemp -d`). The runner writes only its
`--workdir` under `/tmp/w8-ver/`. Receipts: `git status --porcelain` at 19:22:48Z shows the
same 4 untracked sibling files the tree gained during the window (`memory-arm-mutants-s8.md`,
`update-safety-v3.md`, `plans/round-8-record-draft.md`, `plans/round-9.plan.md` — none written
by this seat; the tree was clean at 19:10 before they landed); the census md5 is
`e2c4558a…` and tameshi's runner sha256 `cf41efaa…` after every run; all three of my sweeps
report `MUTATE_RESTORE: OK` with target sha256 before = after `bba6cdf6…` [observed]. The only
writes by this seat are `/tmp/w8-ver/*` and this note.

## 9. Unknowns [unknown]

- Whether any of the 9 un-exercised clause sites can be reached on the live host (state- and
  timing-dependent; not forced read-only here).
- Whether a later round-8 seat lands the new `PLANE oom` watch / baseline inside this round,
  superseding this pin — a moved gate is never re-interpreted against these specs; the specs
  must be re-cut (`.old`-string count assertions fail closed).
- Re-cut reproducibility: M17 was swept once; its kill power under a different case set is
  [unknown].
- Whether the round's record quotes this note's verdict for AUD-X7 closure or adds the
  round-8 arm's rows — the record's call, not this seat's.

## Errata (append-only)

- 2026-10-14 19:23Z — this note landed while sibling round-8 artifacts were still appearing
  (the 4 untracked files above; `update-safety-v3.md` mtime 19:18:23Z). The census pin and all
  measurements above are unaffected; recorded so a later reader does not read concurrent lane
  movement as drift by this seat. [observation]
- 2026-10-14 19:23Z — the poll for S8-1 (20 s sampling, `/tmp/w8-ver/poll.log`) recorded no
  HEAD or census change from 19:11:12Z; S8-1's artifact landed at 19:17:08Z and was picked up
  by tree inspection. The 30-min poll window cap was not exhausted when this note was
  written; a later census change voids the pins above by design. [observation]
- 2026-10-14 19:30Z — a further sibling artifact landed during the poll window,
  `corpus/knowledge/kill-event-deep-r8.md` (seat S8-2, md5 `6685e1da443f5d368cd41584d2b9943e`,
  340 `wc -l`); the census stayed at `e2c4558a…` (19:29:18Z). Read by this seat as a
  cross-read only: its F3 counter map (non-zero `oom_kill` only at `user.slice` and
  `user-1000.slice`, each 1; `.local` 0) and its event-B counts agree with this note's §2
  probes [observation]. No round-8 census revision or baseline exists as of 19:29Z.
- 2026-10-14 19:40Z — poll window closed: the full 30 minutes (19:11:12Z → 19:41Z) recorded
  **no HEAD and no census change** (`/tmp/w8-ver/poll.log` carries only its start line); the
  round-8 census revision / baseline had not landed; the sibling artifacts that did land in
  the window were note-family only (`memory-arm-mutants-s8.md`, `update-safety-v3.md`,
  `kill-event-deep-r8.md`, `plans/round-8-record-draft.md`, `plans/round-9.plan.md`).
  All pins above therefore stand for the closing revision of this window [observation].