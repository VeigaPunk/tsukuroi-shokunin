# FxCrossScope — falsify: cross-lane boundary and no-harm (round 21)

Seat: TsukuroiR21.FxCrossScope (connector, falsify wave). Fresh attack seat, not a build resume.
Candidate revision `0a14952b59d20179e1c813af58befaecd6992a17`; primary file `.ufo/waves/round-21/candidate/PROVINCE.md`.

Reviewed-SHA256: a296da872e83731f7f7a7737662988558ebb97e4399681a1099fab4a259b7a79
Predicate: no-host-authority-no-sibling-award
Lane bounds: leaf member — no subagent dispatch.

The digest above is the one given at dispatch, which also appears in `candidate-files.json`. I did not recompute it, because this seat is NO-EXEC. "Observation" below means I read the frozen bytes with read/grep only. "Prediction" means what the source implies would happen if it were run. Nothing was executed.

## Verdict

**The predicate holds for the round-21 candidate.** No falsifier was found in the round-21 delta.

- PROVINCE.md carries no round-21 edit, no host authority and no new sibling ownership award.
- None of the nine revision consumers in the new target-type matrix can spawn anything except `git`.
- Both shell tools with live host modes keep every host read behind a fixture branch in `--selftest`.

I found two residual items and both are older than round 21. One is a round-19 wording over-award at OUT-001. The other is a coverage gap: the C3 receipts bind the snapshot copy of PROVINCE, not the production file. I also found one mechanical invariant that makes "no province edit" enforceable rather than just promised (see I1).

## Axes

- **adjacency (8):** sibling ownership language in PROVINCE.
- **operability (9):** whether the C2 matrix and the selftests stay host-free.
- **calibration (9):** whether C3 receipts actually bind the bytes the round claims.

No ordinal movement is proposed.

## Observations (source reads of frozen snapshots)

1. **PROVINCE is unchanged by declared digest.** `preregister.json` snapshots `.ufo/waves/round-21/snapshot/PROVINCE.md` with sha256 `a296da87…a79`, written 2026-10-21T12:34:30Z before candidate output. `candidate-files.json` lists `candidate/PROVINCE.md` at revision 0a14952 with the same sha256. The candidate text ends at the `## R20 ownership clarification — OUT-009` section and has no R21 heading.
   - Lesson `corpus/lessons/round-21.md` says "PROVINCE remains unchanged" and "No province ownership-award proposal is integrated". It also declines connector suggestions for a sibling ownership paragraph and a broadened ADJ-07 trigger.
   - `selector-contract-r21.md:7` says the entry does not "award disputed sibling ownership".
2. **PROVINCE contains no host authority.** Core says "all read-only probes". Refuses says "Never installs, upgrades, or removes packages; never restarts services. Detection and report; the operator remediates."
   - The initramfs row says "never rebuild or boot". The snapper row says "never attempt restore/config changes".
   - Round 12 says "no mode repair, service restart, subvolume creation, boot or package transaction is authorized by a finding". R20-OUT009 says "No configuration, service, package, boot or sibling-file write is authorized."
   - The update-safety surface is limited to "what an -Syu would touch". The operator tooling directive routes `-Syu` through this gate, but that does not turn the gate into an approval authority. The gate is a report.
3. **PROVINCE contains no boot-readiness or package-recovery inference.** Nothing in PROVINCE grades a boot image or declares a package recovery.
   - SKILL R21 (`SKILL.md:2125`) says "No host or package/service/boot action follows any result".
   - The boot-chain-audit registry row (`SKILL.md:2140`) says "not operator clearance" and "live reads only when separately authorized".
   - The update-recheck row says "COUNTED/ABSENT observation, not health clearance". `measure-update-recheck.py:8-10` says "never a safety pass … no health, repair, causality or upgrade-clearance verdict".
4. **The C2 consumers spawn only `git`.** I enumerated every `subprocess.run` call across the 17 `tools/*.py`.
   - Production paths in all nine consumers call only `git`: locator-clarification, root-dac-correction, section-citations, source-scope-correction, measure-update-recheck, boot-chain, freshness-r17, recheck-commands, seat-scope.
   - The only non-git spawns are `sys.executable` re-running a copied tool inside a mktemp fixture during selftest. These are at freshness:508, root-dac:459, source-scope:473, measure:537 and seat-scope:539.
   - All host-command strings in these files are data, not calls. That covers `pacman -Qu`, `systemctl`, `journalctl`, `/boot/...`, `sudo …` and `~/.cache/yay`. Examples: measure-update-recheck parses a committed snapshot (`:12-13` "No host-state command is executed: the snapshot is data"), recheck-commands lints text, and boot-chain compares captured lines.
   - No Python tool executes `tsukuroi-census.sh` or `boot-chain-audit.sh`. Those names appear only as registry or fixture strings, in check-registry-coverage:35-36,302 and check-recheck-commands:1337,1363.
5. **The C2 judge stays inside a disposable clone.** `target_type_measure` (check-revision-binding.py:739-780) runs one read-only `bind()` against the lane, then calls `git clone --no-hardlinks --no-tags` into a `TemporaryDirectory`. `prepare()` removes origin and recreates only the tracking ref. Each consumer runs with `cwd=sandbox`, and its `ROOT` resolves from `sandbox/tools`, so its Git reads target the clone.
   - All tag and ref fixtures are created and deleted inside the sandbox (`:684-736`).
   - The docstring (`:49-53`) says plainly that this is not OS isolation. Consumers keep user-level filesystem and network authority.
6. **Every selftest is fixture-isolated.** The registry (`SKILL.md:2131-2151`) has exactly 19 rows, matching the 19 tool files in `candidate-files.json`.
   - **Python selftests:** they build private mktemp Git repos or in-memory fixtures. Every `_revision` importer sets `sys.dont_write_bytecode = True`, so importing writes no `tools/__pycache__` into the lane.
   - **`boot-chain-audit.sh --selftest`:** it sets `BOOTCHAIN_FIXTURE` (`:886`). Every host primitive branches on `fixture_mode` first: stage_image, sha256, b2sum, image_identity, uname, extract, snapshot_ro, mtime, btime, boot_inputs_newer and loader_entries (`:249-506`). `--live` refuses while the fixture is set, refuses as root, and is required explicitly; without a mode flag the script exits 2 (`:1243-1265`).
   - **`tsukuroi-census.sh --selftest`:** every `check()` run overrides each host binary and path with fixture stubs or files (`:1917-1944`). It also asserts `host=fixture-host` and the fixture root to detect live reads, and asserts the fixture tree is byte-unchanged. `check_cli` runs only `--help` and `--sample 0`, which exit before any probe.

## Predictions (not observed; nothing was run)

- **P1.** `check-revision-binding.py --tools-revision 0a14952… --object-target-types` should cause no host-state reads. Its only writes should be in `/tmp/tsukuroi-target-types-*`, which is removed afterwards.
- **P2.** If any PROVINCE append were adopted this round, `check-adjacency-anchors.py --revision <REV> --ownership-corrections` would return `OWNERSHIP-CORRECTION-INVALID` with the message "the OUT-009 clarification is not an exact append after the baseline". The code at `:189-193` requires PROVINCE to equal the R20 baseline plus exactly the OUT-009 suffix.

## Invariants

- **I1. "No province edit" is enforced mechanically, not just promised.** The R20 C1 gate requires PROVINCE = `OWNERSHIP_BASELINE` (`0cbc34dd…`) prefix plus the exact OUT-009 suffix (adjacency-anchors:174-193).
  - Any round-21 province paragraph would regress R20's measured `ownership_corrections` 1 into could-not-evaluate. That is an adjacency harm. Build connector ConnBoundary's proposed R21-GATE-BOUNDARY append is one such paragraph, so declining it was required for no-harm, not optional.
- **I2. Consumers stay off the host by code review, not by sandboxing.** C2 consumers must spawn only `git`, plus `sys.executable` on a copied tool during selftest. The judge confines Git writes but grants no OS isolation.
- **I3. Live modes require an explicit flag; selftests take the fixture branch.**
  - `boot-chain-audit.sh` needs `--live` and refuses when `BOOTCHAIN_FIXTURE` is set or when running as root.
  - `tsukuroi-census.sh` with no arguments **is** live mode (`main`, `:2632-2652`). "Separately authorized" therefore depends on the caller never omitting `--selftest`. No in-repo Python caller invokes it.
- **I4. Selftest writes land in `/tmp`, not in the lane.** The phrase "selftests run in clone only" must be read as "invoked from a disposable clone, with writes only in mktemp".
  - The census selftest writes to a fixed `/tmp/tsukuroi-r3-2-selftest.*` path and ignores `TMPDIR` (`:1713`). The audit and Python selftests use `TMPDIR` via mktemp.
  - SKILL's "selftest private clones" wording for root-dac, source-scope, locator, update-recheck, section-citations, boot-chain and freshness is imprecise. These selftests create fresh `git init` repositories (root-dac adds a bare origin); they are not clones of the lane.
- **I5. Boot-readiness, package-recovery and operator-clearance verdicts stay out of every round-21 metric.** C1 counts decisions, C2 counts consumer behaviour on Git object classes, and C3 counts declared receipts.

## Contradictions and residual risks (stated, not scored)

- **R1. OUT-001 is a pre-existing over-award (round 19, not introduced in round 21).** Its proposition reads "Mori owns kill/OOM and cgroup memory evidence".
  - The pinned mori declaration lists those surfaces as **read-only probes** and refuses OS state: "mori reads journal and cgroup events as fleet evidence and reports them, never owning OS state" (`round-19/l1-capture/siblings/mori/91940fa339e3/PROVINCE.md:6-15`).
  - Tsukuroi's own census reads the same counters as OS evidence, the cgroup `memory.events` oom_kill presence flags (`tsukuroi-census.sh:1052-1078`). PROVINCE's ADJ preamble says "Shared evidence is not shared ownership", and ADJ-04 retains "OS memory, journal and boot diagnosis" for tsukuroi.
  - The section disclaimer and the Limits paragraph keep this from being a formal award. Still, the proposition column states evidence ownership in tsukuroi's own voice, the same pattern R20 corrected for OUT-009 only.
  - ConnBoundary already raised OUT-010. OUT-001 is sharper because tsukuroi measures the same evidence class.
- **R2. C3 hashes the snapshot copy, not production PROVINCE.** `check-review-snapshots.py:59-61` hashes `row["source"]`, which is `.ufo/waves/round-21/{snapshot,candidate}/PROVINCE.md`, not production `PROVINCE.md`.
  - A later production edit would leave every PROVINCE receipt green while it bound stale bytes. Today I1 covers the gap. C3 alone does not.
- **R3. Minor selftest hermeticity gap (census).** `check()` does not override `TSUKUROI_VERCMP`, so the host's `vercmp` from PATH runs on fixture version strings (`:384,1609-1632`). This is a pure version comparator with no host-state read and no write. It only makes selftest results depend on whether `vercmp` is installed.
- **R4. Some selftest subprocesses inherit the caller's GIT_* environment.** freshness:508, source-scope:473 and measure:537 pass no `env=clean_env()` (`GIT_*` variables are inherited). The child tools' own Git calls are cleaned by `_revision.clean_env` or `isolate=True`, so I predict no host or lane effect. Selftest-only.

## Proposed move (one, bounded; for L1, not applied, not for round 21)

Make no change in round 21; I1 makes any province edit harmful to the R20 metric. Record R1 as an open falsifier for a later round.

That later round could add an attributed-reading correction for OUT-001, modelled on R20-OUT009. It would:
- read OUT-001 as mori's own declaration of read-only fleet-evidence probes, not a tsukuroi award;
- state that the census reads the same counters as OS evidence (shared evidence, not shared ownership).

It would need to land together with an updated adjacency-anchors baseline and suffix pin, so that I1 stays exact rather than being loosened. Affected axes: adjacency (clarity gain) and calibration (the fixture must fail on missing, altered and award-rewrite mutants). Risk: changing PROVINCE outside a preregistered claim would repeat the drift that I1 guards against.

## Verification for L1 (not run by this seat)

- `python3 tools/check-adjacency-anchors.py --revision 0a14952b59d20179e1c813af58befaecd6992a17 --ownership-corrections` → expect exit 0 and `ownership_corrections` 1. This confirms I1 and an unchanged PROVINCE.
- `sha256sum PROVINCE.md` at the measured revision, compared against `a296da87…a79`. This closes R2 for this round.
- `python3 tools/check-revision-binding.py --tools-revision <REV> --object-target-types`, run under a process or file audit if one is authorized. This tests P1.
- A grep of `tools/*.py` for `subprocess.run([` callees other than `git` and `sys.executable`. Expect the same set listed in observation 4.

## Limits

- Auxiliary snapshot dependencies I read, none of them hashed by me:
  - all 19 `candidate/tools/*`;
  - `candidate/SKILL.md`, `candidate/SCORECARD.md`, `candidate/corpus/lessons/round-21.md` and `candidate/corpus/knowledge/selector-contract-r21.md`, all through `candidate-files.json`;
  - `round-21/preregister.json`, `reviews.json`, `falsify-reviews.json` and `build/ConnBoundary.md`;
  - pinned sibling snapshots `round-19/l1-capture/siblings/{mori/91940fa339e3,mado/a4046a821608,tameshi/01d586ddbc5f}/PROVINCE.md`.
- I did not read moving production or draft files for any verdict.
- Digest equality comes from declared manifests, not from a hash I computed.
- Source review cannot rule out a host effect in a path I did not trace. I traced every `subprocess.run` call in the Python tools and every host primitive in `boot-chain-audit.sh`, plus the census selftest harness. I did not trace every census live probe body, because live mode is out of selftest scope.
- No tools were installed or upgraded, and none were needed.
- I make no claim of non-author closure, outside promotion or admission.

Scope: executed=none
