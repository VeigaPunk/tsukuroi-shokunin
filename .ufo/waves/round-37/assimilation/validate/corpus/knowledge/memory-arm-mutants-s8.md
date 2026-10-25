# Memory-arm (S7-2) mutation verification — seat S8-1

Round-8 execution note. Author: seat **S8-1** (this seat wrote no S7-2 code — the arm is
round 7's, lane S7-2). This is **evidence for** the arm's non-author verification, not a
substitute for it: the VER-S8 seat runs the non-author pass; this note supplies the
mutation proof that the round-7 memory arm's selftest cases have kill power, and records
what the sweep found honestly. **No gate edit was made** (no S7-2 case was found toothless;
§4).

## 1. What this closes and what it does not

- Closes the measuring half of AUD-X7's round-7 finding ("S7-2's memory arm has no
  non-author verification", `LOG.md` round-7 entry): the 8 memory-arm selftest cases
  (`tools/tsukuroi-census.sh:1350-1407`, labels `(S7-2)`) are now measured against injected
  defects — **8/8 own-case kills**, D2–D8 each uniquely (§4).
- Not closed here: the VER-S8 non-author pass itself; the three survivor findings in §5
  (coverage debt, deliberately **not** patched by this seat — its scope is verification).

## 2. Instruments and pins (all re-measured 2026-10-14T19:14–19:16Z)

| role | artifact | pin |
|---|---|---|
| mutation runner (tameshi, r7-1) | `tameshi-shokunin/tools/mutate-and-run.sh` | sha256 `cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75` (1341 L); own `--selftest` → `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS` rc 0 |
| target (tsukuroi gate) | `tools/tsukuroi-census.sh` | sha256 `bba6cdf6f5b7a7372e43230821bb7c12aa64192266c549f39475c948803a4f55` · md5 `e2c4558a3ae4ddd2eca67e8f4d64281c` · 1472 `wc -l` (unterminated final line) · 73919 B · = HEAD `aa136d6` blob (`git show HEAD:…` sha256 equal) |
| case set | the 8 `(S7-2)` cases | suite headline `TSUKUROI_CENSUS_SELFTEST: PASS (49 cases, 49 passed, 0 failed)` |

The runner was executed from tameshi's tree (read-only: its sha256 is unchanged after the
sweep, §6) against a byte copy of the gate under `/tmp/w8-tsukuroi-s81/`; the gate was
executed **only** in `--selftest` mode (fixtures, no live-path read).

## 3. Method and the re-runnable defect spec

Tameshi recipe (unchanged): pinned byte copy → one exact edit per defect, each `@old`
asserted to occur exactly once **before any suite run** → control run on the pristine (a red
control refuses the sweep) → per-defect suite run `bash "$MUTANT" --selftest` → per-defect
verdict plus the full evidence log per mutant → target sha256 before/after as the restore
proof. Scratch (ephemeral, `/tmp/w8-tsukuroi-s81/`) is transcribed here so the sweep can be
re-cut without this seat's filesystem:

```
@defect D1 | quiet path removed: any readable fixture degrades (owner: healthy-mem-quiet)
@old   elif [ "$deg" -gt 0 ] || [ -n "$unk" ]; then
@new   elif [ "$j_ok" -gt 0 ] || [ "$cg_ok" -gt 0 ]; then
@defect D2 | oom_kill value summed as an event count, not a presence flag (owner: degraded-mem-presence)
@old           present=$((present + 1))
@new           present=$((present + v))
@defect D3 | systemd attribution class C2 never measured, reported as clean 0 (owner: degraded-mem-classes)
@old       0) s_oom=$(nlines "$CAP_OUT"); j_ok=$((j_ok + 1)) ;;
@new       0) s_oom=0; j_ok=$((j_ok + 1)) ;;
@defect D4 | swap.peak vs SwapTotal without kB->B conversion, peak% inflated 1024x (owner: degraded-mem-swap)
@old       'BEGIN { printf "%d%%", (p / 1024 / t) * 100 }')
@new       'BEGIN { printf "%d%%", (p / t) * 100 }')
@defect D5 | memory.events.local merged into the .events presence count (owner: degraded-mem-local)
@old         *.local) localp=$((localp + 1)) ;;
@new         *.local) present=$((present + 1)) ;;
@defect D6 | unreadable PSI silently skipped, no named unknown (owner: degraded-mem-psi-unknown)
@old   else\n    unk="${unk}C6-psi "\n  fi
@new   else\n    :\n  fi
@defect D7 | missing slice treated as zero pressure, slice absence swallowed (owner: degraded-mem-slice-unknown)
@old   else\n    unk="${unk}C5-slice "\n  fi
@new   else\n    :\n  fi
@defect D8 | total unreadability degrades instead of blocking (owner: blocked-mem-unreadable)
@old   if [ "$j_ok" -eq 0 ] && [ "$cg_ok" -eq 0 ]; then\n    MEM_V=BLOCKED
@new   if [ "$j_ok" -eq 0 ] && [ "$cg_ok" -eq 0 ]; then\n    MEM_V=DEGRADED
@defect D9 | unreadable C1 journal probe counted as a clean zero (no owning case)
@old       *) unk="${unk}C1 " ;;
@new       *) k_oom=0; j_ok=$((j_ok + 1)) ;;
@defect D10 | unreadable meminfo is not named (C6-meminfo unknown dropped) (no owning case)
@old   [ -r "$MEMINFO_FILE" ] || unk="${unk}C6-meminfo "
@new   :
@defect D11 | unreadable swap.events is not named (C5-swap unknown dropped) (no owning case)
@old     [ -r "$slice/memory.swap.events" ] || unk="${unk}C5-swap "
@new     :
```

Independent uniqueness pre-check (own `python3` reader, same escape rules as the runner):
`DEFECTS=11 DUP_OR_ZERO=0` — every `@old` occurs exactly once in the pinned bytes.

Reproduce:

```
bash tameshi-shokunin/tools/mutate-and-run.sh \
  --target <byte copy of tsukuroi-census.sh @ bba6cdf6…> \
  --defects <spec above> --suite 'bash "$MUTANT" --selftest' \
  --label tsukuroi-census-s7-2-memory-arm --workdir <dir>
```

## 4. Result

Control and headline, verbatim from the run (`/tmp/w8-tsukuroi-s81/sweep/`, ephemeral):

```
CONTROL: GREEN (exit=0 duration-ms=5379 pristine-sha256=bba6cdf6…)
MUTATE_RESTORE: OK (target-sha256 before=bba6cdf6… after=bba6cdf6… pristine-sha256=bba6cdf6…)
MUTATE: DONE (target=tsukuroi-census-s7-2-memory-arm defects=11 killed=8 survived=3 inconclusive=0 kill-rate=73%)
```

| # | target line | injected defect | owning S7-2 case | verdict | failing cases | mutant sha256 (short) |
|---|---|---|---|---|---|---|
| D1 | `:797` | quiet path removed — any readable fixture degrades | healthy quiet | KILLED | 10 (owning + 9 legacy healthy) | `4c71f6c5…` |
| D2 | `:732` | `oom_kill` value summed as an event count | presence flag, not a count | KILLED | 1 — owning only | `51f70ab7…` |
| D3 | `:707` | C2 attribution never measured, reported as clean 0 | ring class + C1/C2/C3 together | KILLED | 1 — owning only | `5ef739ad…` |
| D4 | `:761` | kB→B conversion dropped, peak % inflated 1024× | swap anchors C5 | KILLED | 1 — owning only | `80f9bbb5…` |
| D5 | `:730` | `memory.events.local` merged into the `.events` count | `.local` reported separately | KILLED | 1 — owning only | `5e1aaa64…` |
| D6 | `:783` | unreadable PSI skipped, no named unknown | unreadable PSI is a named unknown | KILLED | 1 — owning only | `729e90c2…` |
| D7 | `:754` | missing slice read as zero pressure | slice anchors are a named unknown | KILLED | 1 — owning only | `4ef70513…` |
| D8 | `:796` | total unreadability degrades instead of blocking | no cgroup and no journal ⇒ BLOCKED | KILLED | 1 — owning only | `6ced6f50…` |
| D9 | `:703` | C1 probe error counted as a clean zero | — (none) | **SURVIVED** | 0 | `4b3609de…` |
| D10 | `:770` | unreadable meminfo not named | — (none) | **SURVIVED** | 0 | `bd27da6f…` |
| D11 | `:751` | unreadable `swap.events` not named | — (none) | **SURVIVED** | 0 | `4ff09ff1…` |

Reading: every one of the 8 round-7 memory-arm cases kills a defect of exactly its own
contract clause; for D2–D8 it is the **only** failing case out of 49 (attributed from the
pinned full logs, not from the tail). D1 is caught multiply — 10 cases go red, the owning
quiet case among them — so the quiet clause is over-determined, never unverified.
**No case is toothless.** That is the positive finding of this seat: the AUD-X7 gap closes
with kill power measured per case, not asserted.

## 5. The three survivors — coverage debt, named (honest treatment)

The survivors are the arm's fail-closed vocabulary for signals that are *absent or
unreadable while everything else looks fine*. No S7-2 case drives them, so a defect that
silently un-names such a signal passes all 49 cases:

- **D9 `:703`** (`*) unk="${unk}C1 "`): a `journalctl` probe returning rc ≥ 2 is counted as a
  clean zero and the journal side stays alive (`j_ok` incremented) — a fail-open in the
  arm's own sense ("an unreadable signal is a named unknown"). No case sets
  `oom-kernel.rc`/`oom-attrib.rc`/`oom-sigkill.rc` ≥ 2 (`oom-*.rc` is written exactly once
  in the selftest, `:1054-1056`, always `0`).
- **D10 `:770`** (`[ -r "$MEMINFO_FILE" ] || unk="${unk}C6-meminfo "`): no case points
  `TSUKUROI_MEMINFO_FILE` at an unreadable path, so the `C6-meminfo` unknown is unverified.
- **D11 `:751`** (`[ -r "$slice/memory.swap.events" ] || unk="${unk}C5-swap "`): no case makes
  the slice's files unreadable while the slice exists, so `C5-swap` is unverified. Its
  sibling on `:752` (`C5-stat`) is the same class and was **not probed** by this sweep —
  named as unmeasured, not assumed equal.

The missing case shapes are the arm's own rule restated: probe-error → named unknown with
the class tag, discovered via the existing `EXTRA_ENV` overrides plus an rc file
(`oom-kernel.rc := 2`), and an unreadable meminfo / swap.events fixture. They are **not
added here**: the assignment's scope is gate selftest verification only, and none of the
existing cases is toothless. Carry to the arm's next turn.

## 6. Zero mutation, and what this note does not claim

- Target: `MUTATE_RESTORE: OK` — sha256 identical before and after (the runner writes only
  fresh copies; the pinned pristine is kept in the evidence dir).
- tsukuroi tree: the gate's md5 is `e2c4558a…` before and after; `git status --short` shows
  only two untracked round-8/9 drafts by other seats (`plans/round-8-record-draft.md`,
  `plans/round-9.plan.md`) — no tracked file moved.
- tameshi tree: clean (`git status --short` empty), tool sha256 `cf41efaa…` unchanged —
  the runner was used read-only.
- No live-path run was made: every execution was `--selftest` (fixture-only). No cgroup,
  journal, unit or service was touched; no external site was contacted.
- Not claimed: that this sweep is the arm's non-author verification (that is VER-S8's seat);
  that the three survivor sites are unreachable on a live host (they are *unexercised by
  the 49-case suite*, measured); that a survivor's kill power would stay zero under a
  different case set.

## 7. Spot-checks

1. **Control**: `bash <pristine> --selftest` → rc 0, `TSUKUROI_CENSUS_SELFTEST: PASS (49
   cases, 49 passed, 0 failed)`, 49 `PASS` lines, 8 of them `(S7-2)`.
2. **Attribution is per-case, not inferred from the exit code**: the D2 evidence log
   contains exactly one `FAIL` line — the presence-flag case — and the captured plane line
   shows `C4_present=7` (the value-as-count defect), while the same mutant's other 48 cases
   pass.
3. **Zero mutation**: `md5sum tools/tsukuroi-census.sh` → `e2c4558a…` and `git status
   --short` for the two repos as in §6, after the sweep.
4. **Independent uniqueness**: the `precheck.py` reader (not the runner's parser) reports
   `DEFECTS=11 DUP_OR_ZERO=0` against the pinned bytes.

## 8. Unknowns

- Whether the three survivor sites are reachable on the live host is **[unknown]** — a probe
  error is state/timing dependent, and this seat ran no live path.
- The `:752` `C5-stat` sibling mutant is **[unmeasured]** (predicted same verdict as D11;
  prediction is not a result).
- Re-cut reproducibility on a **moved** gate: the spec's `@old` strings were verified
  against `bba6cdf6…` only; if a later seat edits `probe_mem_arm`, the spec must be re-cut
  (the tameshi rule: a moved pin is never re-interpreted).
- Whether VER-S8's independent pass reproduces these mutant shas is **[pending]** — the
  spec is transcribed in §3 so it can be re-run from this note alone.

## Contract keys (appended 2026-10-19, fleet round 1)
source: own-work — tameshi mutation runner against a pinned temporary copy of `tools/tsukuroi-census.sh`, control selftest and defect spec, 2026-10-14; S031 `tools/tsukuroi-census.sh`.
verified-at: 2026-10-14 (the mutation-runner/gate measurements recorded in §§2–7).
recheck: on-release; procedure: §3 mutation spec against its exact pinned revision and §7 pristine control; re-cut `@old` strings if the gate moves.
