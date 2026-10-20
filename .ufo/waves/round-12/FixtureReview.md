# FixtureReview — round-12 selftest architecture advice (seat: FixtureReview)

Scope: advise selftest cases that would kill `missing-root-probe` and `wrong-octal-bit` mutants of the
C1 root-metadata probe; keep the fixture root off real `/`; protect the existing 80-case baseline.
Repo: `tools/tsukuroi-census.sh` at HEAD `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`, 2402 lines, clean
tree apart from `.ufo/waves/round-12/`.

Method and limits (recorded):
- Static reads only. **No selftest, census, or mutant run** (contract: no tests mid-flight). Every
  "80" below is a static line count, not a measured run.
- Read-only host probes: `id -un` → `vgpnk`, `id -u` → `1000`; `stat -c '%a %U %G %n' / /tmp` →
  `555 root root /` and `1777 root root /tmp`; `readlink -f /usr/bin/find` → findutils 4.11.0-1
  (`find -printf` available). Shell `find`/`stat` in the tool shell are wrappers; the cited binaries are `/usr/bin/*`.
- Arithmetic-only tables (bash/python integer ops over mode values). No fixture was built.
- Installs/updates: none. No git mutation. Only this file written.
- Author-side seat evidence. Not independent verification.

## 1. Architecture facts (exact)

| # | Fact | Evidence |
|---|------|----------|
| A1 | Baseline = 80 case lines: 77 `check` + 3 `check_cli` (static grep `^\s+check(_cli)? '`). Consistent with the 74-case round-9 receipt plus the 6 S10-2 lines at 2312–2331. | `tools/tsukuroi-census.sh:1838–2331`; `corpus/knowledge/census-closeout-receipt-r10.md` §4 |
| A2 | Hermetic seam registry is a header comment listing every override; "every host path read in live mode has an override". A new root path must be added there. | `tools/tsukuroi-census.sh:294–308` |
| A3 | `check()` is the only place that sets the fixture env for every case: 23 `TSUKUROI_*` overrides (fixture seam plus 22 path/command seams), then `"${EXTRA_ENV[@]}"` last, so per-case overrides win. No root-path override exists yet. | `:1757–1809`, env block `:1763–1786`, `EXTRA_ENV` `:1787` |
| A4 | The only host-read guard is `grep -q 'host=fixture-host'`. Nothing detects other host reads. | `:1793` |
| A5 | `check_cli` runs with no fixture env, only for arms that exit before probes (`--bogus`, `--sample 0`, `--help`). Arg parse precedes all probes in `main`. | `:1811–1833`, `main` `:2336–2358` |
| A6 | `fx_hash` hashes `find -type f` content only (sha256). Directory entries, directory creation, and permission/owner bits are not in the zero-mutation proof. `fx_no_mutation` compares only this. | `:1748`, `:1750–1754`, call `:1807` |
| A7 | Cleanup is `trap 'rm -rf -- "${work:-}"' EXIT INT TERM` with no mode restore and no error capture. A `000` directory with children blocks `rm` as owner. | `:1574` |
| A8 | Legacy expectations are mostly prefix/`.*`-tolerant, so appended fields are safe. Two are not: the rollup `\)$` at `:2319`, and anchored prefixes such as `^PLANE update-safety: HEALTHY \(status=INERT; ` at `:2135`. Inserting a field mid-note or changing the rollup breaks them. | `:2135`, `:2319` |
| A9 | Root-mode census is absent at HEAD: no `stat -c %a` / root-path probe in the script. QUALITY #13 and lesson D3/MC3, D6 record it as debt. The two named mutant classes therefore have no target yet. | `corpus/QUALITY.md:17`; `corpus/lessons/round-1.md:40,43`; grep of `tools/tsukuroi-census.sh` |
| A10 | Mutant spec convention to reuse after landing: `@defect Dn \| … @old … @new …`, pinned by sha256, control selftest green first. | `corpus/knowledge/memory-arm-mutants-s8.md` §3, §7 |
| A11 | **Host `/` is `555 root root`** (measured this seat). The census runs as uid 1000, so `/` is a non-owner, owner-write-absent object on this host. A class-blind "owner-write absent → DEGRADED" rule would fire on the live host. | `stat` probe above; spec.json Planner prompt |

## 2. Kill analysis for the two mutant classes [unmeasured — no probe exists at HEAD]

### 2a. `missing-root-probe`
Why the current 80 cannot kill it: no legacy case asserts any root field. Every legacy regex tolerates
an absent field (`.*`, or the rollup pattern at `:2319` which is unaffected by a note field).

Required cases:
- **R1 (healthy measured value):** default fixture root with a non-host mode. Assert the exact field, e.g.
  `root=/ mode=0751 owner=1000`. A deleted probe or a hard-coded `root=ok` fails the regex.
- **R2 (named-unknown path):** the probe is also deleted or skipped on the unreadable path. Assert
  `root=unknown` (or the chosen token) so deletion on the BLOCKED/unknown branch is caught too.
- **R3 (non-default value):** at least one case whose mode differs from the default. This kills a
  probe that returns a constant. R1 with the default alone does not.
- Every case asserts the field inside the note, not only the verdict, so a deleted probe that leaves the
  verdict unchanged still fails.

### 2b. `wrong-octal-bit`
Why verdict-only assertions are weak: a wrong-bit read gives the same verdict on many fixtures. The
evidence must carry the bits that were read.

Assert in every mode case: `mode=<oct> owner=<uid> class=<owner|other|…> w=<0|1>` (exact tokens).
Then the bit read is visible even when the verdict coincides.

Fixture matrix (base uid = fixture owner 1000 unless noted). Kill rationale is for the bit read
(decimal misparse of the mode string, or a neighbouring-bit mask typo):

| Case | Fixture mode, owner class | Expected write bit / verdict (per Planner contract) | Kills |
|------|---------------------------|----------------------------------------------------|-------|
| F0 default | 0751 | owner-w=1, HEALTHY | leak sentinel (host `/` is 555 owner 0); baseline |
| F1 | 0755 | owner-w=1, HEALTHY | group/other mask read as owner (0020 gives dec 16 vs oct 0; 0002 gives dec 2 vs oct 0) |
| F2 | 0555 | owner-w=0, DEGRADED | owner-w absence rule itself; decimal misparse of other-w (555 & 2 = 2 vs oct 0) |
| F3 | 0575 | owner-w=0, group-w=1, DEGRADED | group-w mask read in place of owner-w (only F3 separates it from F2) |
| F4 | 0557 | owner-w=0, other-w=1, DEGRADED | other-w mask read in place of owner-w |
| F5 | 0775 | owner-w=1, HEALTHY | decimal misparse of owner-w: 775 & 128 = 0 vs oct 128; 0755 does **not** kill this (both 128) |
| F6 | 0355 | owner-w=1, owner-r=0 | a probe reading 0400 (r) where 0200 (w) is meant |
| F7 | 1777 (sticky) / 2755 (setgid) | per decided rule for 4-digit modes | 4-digit parsing (`[ "$m" = 755 ]`, `${m:0:1}`, `$((m))` on `1777`) |

Notes on F1–F5 (arithmetic checked, not run): for mask 0200, 0755 and 0751 give the same answer in
decimal and octal, so they cannot kill a decimal misparse of owner-w; F5 is required for that. Mask
0002 on 0555 gives decimal 2 vs octal 0, so F2 kills a decimal misparse of other-w.

### 2c. Non-owner class (uses the uid seam)
Fixtures are owned by uid 1000, so an owner-class probe cannot be tested against a non-owner
object without privilege. Add a uid seam (`TSUKUROI_CENSUS_UID`, name proposed) and set it to a value
other than the fixture owner:
- **F8:** fixture 0755 with seam uid ≠ owner → non-owner class, other-w=0. Kills a class-blind probe.
- **F9:** fixture 0557 with seam uid ≠ owner → other-w=1 → non-owner verdict. Kills a probe that reads
  the owner bit for a non-owner.
No root privilege is needed. This mirrors the existing hostname-seam pattern and matches A11 on the host.

### 2d. Unreadable metadata (C1 unknown path)
- stat(2) needs search (x) on each path prefix; it does not need read on the final object
  [INFERENCE from POSIX stat(2); not re-read from a man page this seat]. A `000` target directory
  therefore still stats with mode `0000`; it does not produce a stat failure.
- Pair two cases so that "mode 0000 readable" and "metadata unreadable" are distinct:
  - **U1:** root fixture chmod 000 itself → stat succeeds → `mode=0000`, verdict per rule.
  - **U2:** create `$FX/locked/root`, then chmod 000 `$FX/locked`; seam points at `$FX/locked/root` →
    stat EACCES → the named unknown token, verdict per the decided rule (BLOCKED or explicit unknown).
- Under root, DAC is bypassed: U2 would stat successfully and fail loudly, not pass silently. Add a
  precondition message for `id -u` = 0 so the failure is explained.
- Cleanup: the trap must `chmod -R u+rwx -- "$work"` (or equivalent) before `rm -rf`, otherwise `rm`
  cannot descend into `locked/` (needs w+x on `locked`) and `/tmp/tsukuroi-r3-2-selftest.*` leaks.
  Trap at `:1574` does not do this.

## 3. Fixture root must not be real `/`
1. Add a root-path seam (name proposed `TSUKUROI_ROOT_PATH`, default `/`) and list it in the
   seam registry at `:294–308`.
2. Set it in `check()`'s env block before `"${EXTRA_ENV[@]}"` (`:1763–1787`), pointing at `$FX/root`
   (created by `fx_default`). Case overrides then still work (U2).
3. Sentinel: default fixture root mode 0751, owner uid 1000. Host `/` is 555 owner 0. Any leak produces
   `mode=0555 owner=0`, which fails R1/F0 exact-token assertions. This needs no production guard.
4. `check_cli` stays fixture-free. It must not gain a probe before the arg parse.
5. Optional stronger guard (not required): in fixture mode, a root path equal to `/` yields BLOCKED. This
   adds production-visible test logic; prefer the sentinel.

## 4. Protecting the 80-case baseline
- Add only. Do not edit any existing `check`/`check_cli` line (`:1838–2331`). Insert the new block
  before the summary at `:2333`. A static protection check: `git diff` over the selftest region should
  show additions only, with no changed legacy label or regex line.
- Keep the rollup unchanged (`:2319` is `$`-anchored). Root data goes into the packages or
  update-safety note suffix, not into a new rollup field and not mid-note (`:2135` prefix).
- `fx_default` gains the root fixture (0751 owned 1000). Every legacy case must still read HEALTHY on
  the packages plane. Verify by reasoning that 0751 is HEALTHY under the owner rule, and confirm
  that rule before landing.
- Extend `fx_hash` to include directory entries and modes, for example
  `find "$1" -printf '%p %m %U %G %y\n' | LC_ALL=C sort` with the existing content hash. Findutils
  4.11.0 supports `-printf`. Redirect stderr from `find` (the `000` directory will print permission
  errors, and the before/after hashes will be equal, so no false pass results).
- Expected count after landing: 80 + N, printed by the summary at `:2333`. A decrease means a legacy case
  was lost. Parent should compare the label set before and after.

## 5. Risks and decisions the parent must settle before cases can be written
1. **Contradiction in the Planner contract:** "without changing six-plane rollup" vs "owner-write
   absence DEGRADED". If the packages plane goes DEGRADED, the rollup changes. Cases cannot pin
   either until one reading is chosen. (spec.json Planner prompt.)
2. **Undefined verdicts:** non-owner class, world-writable (other-w), sticky (1777), setgid (2755).
   F7–F9 need these. Without decisions the cases would encode guesses.
3. **Live host `/` = 555 root:root (A11).** Under a class-blind owner-write rule, the live census will
   read DEGRADED on this host. Expected behaviour must be stated, not discovered at landing.
4. **Mutation kill power is unmeasured.** No probe exists at HEAD, so `missing-root-probe` and
   `wrong-octal-bit` cannot be run now. Post-landing, re-cut `@old` strings (A10) and run the sweep
   with a pristine control. Parent runs it once after integration.
5. **Root execution:** unreadable cases fail loudly under root (U2 stat succeeds). Document that the
   selftest is expected to run non-root.
6. **Trap and fixture cleanup** (A7, §2d) must land with U2, or `/tmp` leaks.

## 6. Verification gaps
- No selftest, mutant, or census execution this seat (contract). All kill claims are design-level and
  unmeasured.
- The decimal/octal table is integer arithmetic only. It shows where a misparse is invisible on
  particular modes; it does not show the landed probe's behaviour.
- stat(2) EACCES semantics for U2 are from POSIX/standard Unix semantics, not re-read from a man
  page in this repo. Label: [INFERENCE].
- 80 is a static line count. It has not been measured by running `--selftest` in this round.
- Nothing here is independent non-author verification.
