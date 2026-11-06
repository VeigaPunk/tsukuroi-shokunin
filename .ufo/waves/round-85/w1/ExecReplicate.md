# ExecReplicate — round 85, wave w1: independent replication of C2 and of every freeze control

Seat: executor (leaf). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Lane revision measured: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master`
= `479d868b2fc8969a19a617cd55ced5c13edd84b6` (the C2 candidate commit; freeze commit `66374a4db963e5c655506e64cb0fea2d67ec9d0d` is its parent).
Measured bytes equal committed bytes (`git hash-object` == `git rev-parse HEAD:<path>`) for
`tools/check-hibernate-resume.py`, `tools/resume-gate-battery-r85.py`, `tools/resume-gate-battery-r84.py`
and all ten control scripts, so this replication judged the committed candidate, not a sibling's uncommitted copy.
Worktree also carries other seats' uncommitted work (`SKILL.md`, `corpus/SOURCES.md`,
`corpus/knowledge/hibernate-resume-plane-r84.md`, `corpus/knowledge/hibernation-availability-r85.{md,json}`,
`corpus/lessons/round-85.md`); none of it was read for a verdict beyond the gate/battery/control bytes above,
and none of it was touched.

**Verdict: C2 REPLICATED — 20/20 families, rc 0, in 5 of 5 consecutive runs; no control met; no KILL.**

## 1. Instrument identity (required precondition)

```
$ sha256sum tools/resume-gate-battery-r85.py
b30a7c1ed8fca5fa9c30fb3f4b221ccae11137f688bffc47844b16f0a117ba21  tools/resume-gate-battery-r85.py
```

Equals the frozen value `b30a7c1ed8fca5fa9c30fb3f4b221ccae11137f688bffc47844b16f0a117ba21`. Gate under test:
`88041b7509fc5824b036d45dd3416bfadbaeb17f0b702e15af0edd17944483e7  tools/check-hibernate-resume.py`.

Freeze manifest re-verified from `.ufo/waves/round-85/before`:

```
$ sha256sum -c freeze-manifest.sha256
host/facts-v2.json: OK
host/receipt.txt: OK
controls/k1-r84-gate.py: OK
controls/k2-schema-shim.py: OK
controls/k3a-r84-f1-signature.py: OK
controls/k3b-r84-f2-replay.py: OK
controls/k3c-r84-f4-firstfault.py: OK
controls/k3d-r84-f1-shim.py: OK
controls/k3e-r84-f4-shim.py: OK
controls/k4-const-healthy.py: OK
controls/k5-replay-v2.py: OK
controls/k6-substring-sniffer.py: OK
../../../../tools/resume-gate-battery-r85.py: OK
rc=0
```

Pinned inputs therefore byte-identical at measurement time; the control corpus I re-ran is the committed corpus,
not a re-authored one.

## 2. Candidate counting command, five runs

```
$ python3 tools/resume-gate-battery-r85.py --gate tools/check-hibernate-resume.py --out $S/cand-N.json
```

Each run in its own `TMPDIR` (`$S/t1..t5`), all five started concurrently. Raw JSON: `ExecReplicate/cand-{1..5}.json`.

| run | cases | families_passed | verdict | rc | order_head |
|---|---|---|---|---|---|
| 1 | 134 | **20/20** | met | 0 | `HR-SYSFS-DEVICE-MISMATCH, PREC-NO-RESUME-ARG, PREC-NO-RESUME-ARG, HR-NO-ACTIVE-SWAP, HR-SYSFS-OFFSET-MISMATCH` |
| 2 | 134 | **20/20** | met | 0 | `HR-OFFSET-MISSING, PREC-DECOYS, HR-NO-RESUME-ARG, MULTI-FAULT, MULTI-FAULT` |
| 3 | 134 | **20/20** | met | 0 | `HR-NORESUME-ARG, HR-HIBERNATE-DISABLED, HR-OFFSET-MISMATCH, MULTI-FAULT, HR-NO-ACTIVE-SWAP` |
| 4 | 134 | **20/20** | met | 0 | `HR-SWAP-TOO-SMALL, HR-SYSFS-DEVICE-MISMATCH, MULTI-FAULT, HR-HOOK-BEFORE-ENCRYPT, HR-HOOK-BEFORE-ENCRYPT` |
| 5 | 134 | **20/20** | met | 0 | `HR-OFFSET-MISMATCH, HR-SYSFS-OFFSET-MISMATCH, HR-NO-RESUME-ARG, HR-NO-ACTIVE-SWAP, HR-HOOK-BEFORE-ENCRYPT` |

All five `failed_families` arrays are empty; all five `order_head` tuples are pairwise distinct (five distinct
first-case names alone: `HR-SYSFS-DEVICE-MISMATCH`, `HR-OFFSET-MISSING`, `HR-NORESUME-ARG`, `HR-SWAP-TOO-SMALL`,
`HR-OFFSET-MISMATCH`), so the call order is genuinely re-shuffled per run and no position counter can answer.
Five runs exceed the declared three; the predicate holds in every one. Wall time for the five concurrent runs
6.05 s total, no case hit the 20 s bound.

## 3. Every freeze control re-run once, against the frozen receipt values

`controls-receipt.txt` values, left; my reading at `479d868b`, right.

| control | frozen | re-run | families | rc | match |
|---|---|---|---|---|---|
| K0 (absent path) | 0/20 | **0/20** | unmet | 1 | yes |
| K1 r84 gate (do-nothing) | 0/20 | **0/20** | unmet | 1 | yes |
| K2 schema shim | 13/20 | **13/20** | unmet | 1 | yes |
| K3a r84 f1 signature | 0/20 | **0/20** | unmet | 1 | yes |
| K3b r84 f2 replay | 0/20 | **0/20** | unmet | 1 | yes |
| K3c r84 f4 first-fault | 0/20 | **0/20** | unmet | 1 | yes |
| K3d r84 f1 shim | 13/20 | **13/20** | unmet | 1 | yes |
| K3e r84 f4 shim | 13/20 | **13/20** | unmet | 1 | yes |
| K4 const-HEALTHY | 2/20 | **2/20** | unmet | 1 | yes |
| K5 v2 order replay | 0/20 | **0/20** | unmet | 1 | yes |
| K6 substring sniffer | 14–15/20 | **15/20** | unmet | 1 | yes (top of the frozen band) |

Failed-family sets also reproduce the receipt exactly, control by control (e.g. K6: `HR-NORESUME-ARG`,
`MALFORMED`, `PREC-DECOYS`, `PREC-NO-RESUME-ARG`, `PREC-NOHIB`; K2/K3d/K3e: `HR-HIBERNATE-DISABLED`,
`HR-LOCKDOWN-BLOCKS`, `HR-NORESUME-ARG`, `MALFORMED`, `MULTI-FAULT`, `PREC-NO-RESUME-ARG`, `PREC-NOHIB`).

**No control is met.** Highest control reading is K6 at 15/20, five families short of the target; the strongest
schema-aware forger (K2, K3d, K3e) stops at 13/20. The battery therefore separates a schema shim from a
rule-implementing gate by 7 families and a substring sniffer by 5. **No KILL.**

K5 scratch counter: the run created the untracked file
`.ufo/waves/round-85/before/controls/.k5-counter` (it is not gitignored: `git check-ignore -v` rc 1). Removed it,
then proved the directory is back to committed content:

```
$ git status --porcelain -- .ufo/waves/round-85/before
(empty)
$ git ls-tree --name-only HEAD .ufo/waves/round-85/before/controls/ | wc -l
12
$ ls .ufo/waves/round-85/before/controls/ | wc -l
12
```

No other residue was created in the lane; nothing was added, committed or modified there.

## 4. Harm checks

`bash tools/tsukuroi-census.sh --selftest`:

```
TSUKUROI_CENSUS_SELFTEST: PASS (218 cases, 218 passed, 0 failed)
exit status 0
```

`python3 tools/check-hibernate-resume.py --live`, twice:

```
{"findings": [], "verdict": "HEALTHY"}   rc=0
{"findings": [], "verdict": "HEALTHY"}   rc=0
```

The live reading is consistent with the pinned host facts (`/sys/kernel/security/lockdown` =
`[none] integrity confidentiality`, cmdline has `resume=`/`resume_offset=` and neither `nohibernate` nor
`noresume`): HEALTHY is the correct reading, not a vacuous one, and the gate is stable across invocations.

## 5. Round-84 battery against the v2 gate (expected consequence, not a regression)

```
$ python3 tools/resume-gate-battery-r84.py --gate tools/check-hibernate-resume.py
families_passed: 1, families_total: 13, verdict: unmet, rc=1
```

1/13. Every resume-facts/1 case gets `CANNOT-EVALUATE` rc2 from the v2 gate; the only family left standing is
MALFORMED, whose expectation *is* `CANNOT-EVALUATE` rc2. This is the schema change working as declared — the
round-84 instrument is a resume-facts/1 instrument and the lane tip speaks resume-facts/2. It is not a
regression of a live instrument: the round-84 battery is not the C2 counting command, and the r85 battery at
the same tip reads 20/20. Recorded for the record so nobody reads the "1/13" as a fresh defect.

## 6. Independent probes beyond the required list

- **No path/name privilege.** `grep -n -E 'check-hibernate|hibernate-resume\.py|tools/'` over the battery: no
  match (rc 1). The gate is invoked only as `[sys.executable, gate, "--facts", p]` with
  `env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"}`, so the gate cannot see `TMPDIR`, the battery's path, or the
  caller's environment. Copying the gate byte-identically to `$S/decoy/zzz-other-name.py` and running the
  battery against it still reads `families_passed: 20, verdict: met, rc=0` — the verdict follows behaviour,
  not a name.
- **No fixture sniffing in the gate.** `grep -n -E 'random[0-9]|/tmp|TMPDIR|fixture|battery|resume-gate'` over
  `tools/check-hibernate-resume.py`: no match (rc 1).
- **Determinism.** Same committed `host/facts-v2.json` twice →
  `{"findings": [], "verdict": "HEALTHY"}` rc 0 both times, byte-identical outputs.
- **Schema discrimination.** The same document downgraded to `resume-facts/1` and with `lockdown` removed →
  `{"error": "schema", "findings": [], "verdict": "CANNOT-EVALUATE"}` rc 2, i.e. the v2 gate refuses the v1
  document rather than answering it (which is exactly the K1 do-nothing failure mode inverted).

## 7. Axes

- **operability**: no change claimed by this seat; the replication supports C2's 20/20 met at the landed tip
  and shows the instrument is live-clean (HEALTHY rc0 twice) and that the census self-test still passes 218/218.
- **freshness**: nothing refused; measurements taken at `479d868b` against inputs that verify against the freeze
  manifest.

## 8. Risks, refusals, notes

- K6 sits at the top of its frozen 14–15 band (15 in my run). Five families of margin is thin but declarative:
  K6 cannot exceed 16 without also getting MALFORMED/POSITIVE right, which a substring sniffer does not.
- K5's `.k5-counter` is a known, non-gitignored residue of the committed control; it was cleaned. A future
  wave running K5 should expect to clean it again (the control is frozen, so this is a property of the receipted
  control, not a defect I may patch).
- No lane file was edited, no git/jj mutation, no host mutation (`sudo -n` was not needed), no subagents spawned.
- Tooling: nothing installed or upgraded in this seat.

## Evidence files

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-85/w1/ExecReplicate/`
`cand-{1..5}.json`, `ctrl-{K0,k1,k2,k3a,k3b,k3c,k3d,k3e,k4,k5,k6}-*.json`, `summary.json`.
