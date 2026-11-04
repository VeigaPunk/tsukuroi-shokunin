# K1Critic — round 71 w1: falsification of C1 and C2 against the declaration's own receipts

Seat K1Critic (L2, wave w1). Frozen declaration: `SCORECARD.md` "Round 71 — declaration" at
`0fcfca315fbdf4ff6a47abeff08efa7fd27aa32e` (base `930d5530e5fbf91091245c044fef4888ecf12029`).
Lane tree untouched: no write, stage, commit or push in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
All git writes were in the sandbox clone `/fast/scratch/hyaku/tsukuroi-r71/K1Critic/clone`
(`git clone --shared`, checked out at `930d5530` and `0fcfca31`; one attack-fixture commit
`51d2357` inside the clone only). Scratch removed before yield. Tooling installed: none.

## 1. Receipts (a)–(f), re-run — 20 of 24 declared receipt rows reproduce, 4 do not

| Item | Replay | Observed | Verdict |
|---|---|---|---|
| (a) | `cd before/src && sha256sum -c SHA256SUMS` | 4/4 `OK`, rc 0 | reproduced |
| (a) provenance (extra, not counted) | `curl` each `SOURCES.json` URL at `h=v7.2.11`, sha256 | 4/4 blobs hash to the committed digests (`params.c` 923610d5…, `moduleparam.h` 220f2dac…, `main.c` e1e1a1c8…, `kernel-parameters.rst` 45587d8e…) | reproduced, upstream |
| (b) kernel | `uname -r` via `capture.sh` | `7.2.11-arch1-1` | reproduced |
| (b) modules/files | `ls -d /sys/module/*/parameters \| wc -l`; `ls /sys/module/*/parameters/* \| wc -l` | 136; 829 | reproduced |
| (b) nvidia_drm | capture lines | `color_pipeline/fbdev/modeset/vblank` all `-r--r--r--`, `modeset=Y` | reproduced |
| (b) nvidia / uvm | capture lines | `NVreg_*` all `-r--r--r--`; `nvidia_uvm` mixes `-rw-r--r--` and `-r--r--r--`; writable-parameter list empty | reproduced |
| (b) btrfs | `[ -e /sys/module/btrfs/parameters/read_policy ]` | absent (perm==0) | reproduced |
| (b) cmdline | `/proc/cmdline` | `resume=`, `zswap.enabled=1`, `rootflags=subvol=@`, no `mod.param` token | reproduced |
| (b) modprobe.d | `find … -maxdepth 1 -type f` | `/etc/modprobe.d` **3**, `/usr/lib/modprobe.d` **5** (README, bluetooth-usb, gsr-nvidia, nvidia-utils, systemd) | **D1: declaration says 4 under /usr/lib; its own committed host.txt lists 5** |
| (c) | `git grep -c -iE <tok> 930d5530 -- corpus SKILL.md PROVINCE.md \| wc -l` | `modprobe.d` 0, `kernel-parameters` 0, `module_blacklist` 0, `NVreg` 0, `module_param` 0, `kernel_param_ops` 0, `param_attr_store` 0, `sys/module` 9, `parameters/` 6; notes 88; six-note list unchanged | reproduced exactly |
| (d) | note/counter `cat-file -e 930d5530:…` | rc 128 / rc 128 | reproduced |
| (d) | `git show 930d5530:<note> \| grep -c '^| MP'` | 0 | reproduced |
| (d) | `git show 930d5530:tools/tsukuroi-census.sh \| grep -c R71-C2` | 0 | reproduced |
| (d) | same, `grep -cE 'case_timeout\|SELFTEST_CASE_TIMEOUT\|kill -TERM'` | 0 | reproduced |
| (d) | base selftest (clone at 930d5530) | `PASS (214 cases, 214 passed, 0 failed)` rc 0, 53 s | reproduced |
| (d) | `git show 930d5530:corpus/SOURCES.md \| grep -cE '^\| S[0-9]{3,}'` | 296 | reproduced |
| (d) | `git ls-tree -r 930d5530 corpus/knowledge/ \| grep -c '\.md$'` | 88 | reproduced |
| (d) | "canonical census validate rc 0" | **no entry point**: 0 `validate` occurrences in `tools/tsukuroi-census.sh` at base; the same unlabeled value was already flagged at round 70 (`.ufo/waves/round-70/w1/K1Critic.md:117`) | **D2: un-replayable, carried** |
| (e) counter pin | `sha256sum tools/count-mp-rows-r71.py` | `fa67d4de…48bc` | reproduced |
| (e) battery control | `python3 before/control/battery.py` | `[PASS] control: rc=0 want=0 met=1`; `MP_ROWS=6 MP_VERIFIED=6 MP_SOURCES=4 MP_SNAPSHOTS=4 MP_MALFORMED=0` | reproduced |
| (e) battery mutants | same run | 10 mutants, all `met=0` rc 1, `BATTERY cases=11 passed=11 failed=0` | **D3: declaration says 12 cases (1 control + 11 mutants); the artifact has 11 (1 + 10)** |
| (e) mutant-duplicate-id | battery output line | killed by `MP_ROWS=7` + `snapshot-reuse params.c=3`; **no `duplicate-id` and no `ids-not-contiguous` token** | **D4: the named channel is untested by the battery** (the clause itself works: a true MP2-twice fixture reads `duplicate-id` + `ids-not-contiguous`) |
| (f) selftest | clone at 930d5530, `--selftest` | `PASS (214 cases, 214 passed, 0 failed)` rc 0 | reproduced |
| (f) live census | clone at 930d5530 | `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=DEGRADED drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)` rc 1 | reproduced |
| (f) red-before | `TMPDIR=$S bash before/redbefore-timeout.sh` | `rc=124 elapsed=20s verdict_lines=0`; labels 0; tokens 0 | reproduced |

Host capture: the rerun is byte-identical to the committed `host.txt` except its date line (`diff` after
dropping the date header = 0 lines), so D1 is a declaration-summary error, not a receipt error.

## 2. Defects (4)

1. **D1 — (b) misstates its own receipt.** Prose: "3 files under `/etc` and 4 under `/usr/lib`".
   Committed `host.txt` (and the live rerun) list **5** under `/usr/lib/modprobe.d`. The receipt is
   right; the summary is wrong. Impact: the host-facts paragraph the claim cites is off by one on a
   surface the note is about (modprobe.d vs the parameter plane).
2. **D2 — (d) carries an un-replayable value.** "canonical census validate rc 0" names no command and
   no tool; `tools/tsukuroi-census.sh` at base contains 0 `validate` occurrences. Round 70's K1Critic
   already recorded this exact value as unlabeled/unreplayable; round 71 re-committed it unchanged.
3. **D3 — (e) miscounts its battery.** Declaration: "12 cases: 1 well-formed control + 11 mutants".
   `control/battery.py` registers 1 control + 10 mutants; `battery.txt` prints `BATTERY cases=11`.
   The eleven `[PASS]` lines in the receipt are the 11 *total* cases.
4. **D4 — (e) the duplicate-id mutant tests the wrong channel.** The case appends a seventh row
   (`MP7`) and is killed by the row count and by `snapshot-reuse params.c=3`; the failure line never
   emits `duplicate-id`. The counter's duplicate-id clause is real (my MP1,MP2,MP2,MP4,MP5,MP6 fixture
   prints `duplicate-id` + `ids-not-contiguous`), so this is battery coverage debt, not a counter bug.

None of D1–D4 touches a claim's before-state; they are summary/coverage errors in the declaration's own
prose. They are not fatal to either claim.

## 3. Predicate channels — C1 6, C2 4 (7 demonstrated, 3 named)

### C1 `tools/count-mp-rows-r71.py` — can a note pass while stating what the snapshot does not say? Yes.

Demonstrated on the **real committed snapshots and the real registry row shape**, over committed bytes
(clone `51d2357`, which appends S297–S300 in the live 11-cell shape and writes the attack note):

```
$ python3 tools/count-mp-rows-r71.py --revision HEAD
MP_ROW ok MP1 source=S297 snapshot=params.c
…
MP_ROWS=6 MP_VERIFIED=6 MP_SOURCES=4 MP_SNAPSHOTS=4 MP_MALFORMED=0
MP_TARGET rows=6 verified=6 sources>=4 snapshots>=4 max_reuse=2 met=1     (rc 0)
```

MP1's statement: *"module_param_sysfs_setup never skips a kparam whose perm equals zero and an
invisible parameter always gets a sysfs file"*. The snapshot says the opposite — `params.c:709-710`
`if (kparam[i].perm == 0) continue;`. The row passes with `statement-grounding=6/11`.

| # | Channel | Counterexample (scratch fixture; same code path) | Clause that fails to close it |
|---|---|---|---|
| C1-1 | statement grounding is lexical, not entailment | the contradiction above: 6/11 shared tokens, met=1 | `statement-grounding` (≥6 shared non-stopword tokens, share ≥0.5) |
| C1-2 | token salad | `"return static struct const char unsigned define include void call arg line"` → 10/11, met=1 | same clause; generic C vocabulary grounds any claim-free statement |
| C1-3 | empty quote | `quote=""` → met=1 (empty string is a substring of every snapshot) | `quote-absent` / `quote-words`; no non-empty requirement |
| C1-4 | irrelevant quote | `quote="the"` → met=1; the quote is never tied to the statement | none — the quote check is location-only |
| C1-5 | rejected registry row | S297 marked `rejected` → met=1; the counter reads `cells[2]` (source) and `cells[6]` (anchor), never `cells[8]` (status). Live-adjacent: the registry's newest three rows S294–S296 are all `rejected` | `source-registered` / `source-not-bound` |
| C1-6 | multi-URL / substring binding (named) | `url not in regrow["source"]` and `snap_name not in regrow["anchor"]` are substring tests over whole cells; a row carrying several URLs/basenames binds any of them | `source-not-bound` / `anchor-not-bound` |

The binding chain (snapshot sha256 == row digest == map digest; map URL in the registry source cell;
basename in the anchor cell; quote verbatim; reuse ≤2) is sound. What is not closed is **substance**:
the note's rows are the only machine-read content, and none of the six channels is closed by the frozen
clauses. C1's headline ("states the kernel module-parameter surface") is therefore weaker than what the
counter establishes.

### C2 — can a case pass without the bound firing? Yes.

Do-nothing control (scratch copy of the base census; three no-op `ok` calls labelled `R71-C2`, **zero**
timeout machinery — no process group, no poll, no TERM/KILL):

```
$ TMPDIR=$S/tmp bash $S/census-do-nothing.sh --selftest | tail -1
TSUKUROI_CENSUS_SELFTEST: PASS (217 cases, 217 passed, 0 failed)      (rc 0, 46 s)
$ grep -c 'R71-C2' $S/census-do-nothing.sh        → 4   (one of them a comment)
$ grep -cE 'case_timeout|SELFTEST_CASE_TIMEOUT|kill -TERM' …  → 0
```

| # | Channel | Counterexample | Clause that fails to close it |
|---|---|---|---|
| C2-1 | do-nothing control reaches the declared target | the run above: labels 4 ≥ 3, N=217 ≥ 217, PASS, 46 s < 300 s | the counting command (`--selftest \| tail -1` + `grep -c R71-C2`) never executes a bound |
| C2-2 | label grep counts comments/dead code | one of the 4 `R71-C2` occurrences is a comment line | `grep -c 'R71-C2'` |
| C2-3 | self-check not tied to the case runner (named) | a bound implemented only for the self-check's own helper (main loop keeps `out=$(…)`) still prints PASS 217/217; the predicate cannot distinguish it | "a hermetic self-check case proves the bound fires" is prose, not a machine-checked clause |
| C2-4 | verdict neutrality not counted (named) | the claim says "never a verdict term", but the counting command never compares the rollup line/exit code with and without the harness (the R70 arm did carry an A/B neutrality case) | none in the counting command |

The external 300 s bound is sound: a hanging suite returns rc 124 and no `PASS` line. `N` counts `ok`
calls, not distinct case identities (a case can call `ok` twice) — folded into C2-1.

## 4. Claim sizing

- **C1: after-state re-derivable with ONE command over committed bytes — YES**, with one caveat.
  `python3 tools/count-mp-rows-r71.py --revision <REV>` reads the note, registry, `SOURCES.json` and
  every snapshot through `git -C <lane> show <REV>:…`; demonstrated at clone `51d2357` → `met=1` rc 0.
  Caveat: the counter script itself is executed from the worktree (its sha256 pin `fa67…` is the only
  binding), and the registry `296 → 300` half of the declared after-state needs a second command
  (`git show <REV>:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3,}'`).
- **C2: target a do-nothing control cannot reach — NO.** The control in §3 reaches every arm of the
  frozen target with zero timeout machinery. The claim's kill rule ("a R71-C2 case passes with the
  harness removed") does close it, but that mutation is not part of the counting command; the
  after-state must carry the mutation receipt or the claim is not established by the declared target.

## 5. Smallest safe corrections (next round; predicates are frozen, no substitution this round)

C1 (the declaration's own "planned (next round)" already opens this door):
1. require `quote` non-empty and ≥ 3 words (kills C1-3);
2. require ≥ 4 distinct non-stopword tokens shared between the **statement and the quote** (kills
   C1-1/C1-2/C1-4: the contradiction shares only "invisible" with its quote);
3. read the registry status cell (`cells[8]`) and require `mined` (kills C1-5);
4. require the URL to match exactly one snapshot and the anchor basename at a word boundary (kills C1-6).

C2:
1. add a mutation arm to the counting command: a scratch copy with the timeout path removed must print
   `FAIL` for the `R71-C2` self-check cases (kills C2-1/C2-3);
2. count distinct case labels, not `ok` calls;
3. add the R70-style A/B rollup neutrality case (kills C2-4).

## 6. What holds (calibration)

- All four snapshots are byte-identical to live upstream `git.kernel.org` at `h=v7.2.11` — provenance is
  stronger than the declaration asserts.
- The host capture is reproducible byte-for-byte (except its date line) and every figure except the
  modprobe.d summary is exact.
- The novelty sweep, the absence controls (bar the unlabeled value), the counter pin, the battery's 11
  cases, the 214-case baseline, the live DEGRADED rollup and the red-before all reproduce.
- Neither claim's before-state is falsified. C1's predicate cannot establish its headline; C2's target
  is not control-distinguishing. Both are fixable defects of the frozen instruments, not tradeoffs that
  force a rejection of the round's direction.
