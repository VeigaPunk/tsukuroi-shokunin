# CensusScribeR — round-12 resumed: starting measurement design and source census histogram

Seat: `TsukuroiR12.CensusScribeR` (leaf, resumed wave). Author-side seat evidence only; not independent non-author verification.
Paths relative to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Lane writes: this file only. No edits to `tools/tsukuroi-census.sh`, `corpus/SOURCES.md`, `corpus/QUALITY.md`, knowledge, lessons, LOG/SCORECARD/README/SKILL, or old wave evidence.

## 1. Starting state (re-verified now)

| item | observation | command / exit |
|---|---|---|
| HEAD | `b76b5c377eaee3e3d8d47fdddde977828d05dbd5` | `git rev-parse HEAD` (0) |
| tracked census | `tools/tsukuroi-census.sh` worktree == HEAD, sha256 `1045244387ffcd5d3db481dd0d3d30e34097abc24744d954e791b81d28b20c11`, 2402 lines, `VERSION='census-v2'` | `git show HEAD:… \| sha256sum`, Python sha256 of worktree (equal) |
| worktree status | `M corpus/QUALITY.md`, `M corpus/SOURCES.md`, `?? .ufo/waves/round-12/`, `?? corpus/knowledge/root-dac-decision-r12.{json,md}`, `?? corpus/lessons/round-12.md` | `git status --short` (0) |
| C1 landed | **No.** Census blob unchanged; `root_mode` tokens in HEAD blob = 0; no C1 evidence file in resumed dir | Python static scan |
| sources worktree sha | `corpus/SOURCES.md` HEAD sha256 `3e06c2eb…259b2e2`; worktree sha256 `3b798e30…3f74cd` (modified by Sources seat, not by this lane) | Python sha256 (both read) |

Status of inherited `CensusScribe.md#3B4C`: its starting-HEAD, C1-absent, census-blob and verdict statements are **reproduced** in this pass (section 3). It remains historical; this file does not rewrite it.

## 2. Measurement design (frozen metrics for the C1 comparison)

| id | metric | method | baseline at HEAD (this pass) |
|---|---|---|---|
| M1 | verdict line + rc | `timeout 180 bash <HEAD copy>` read-only | `TSUKUROI_CENSUS: DEGRADED (...)`, rc=1 — reproduced |
| M2 | per-plane lines | same run, `PLANE <name>:` | 6 lines: packages DEGRADED, systemd HEALTHY, drivers DEGRADED, journal DEGRADED, update-safety DEGRADED, oom DEGRADED — reproduced |
| M3 | root-dir metadata arm count | static Python scan of blob for `stat -c` with `%a/%A/%U/%G`, `getfacl`, `lsattr`, `pacman -Qo/-Ql`, `root_mode` | **0** on all: `stat -c` lines = 6 (none with `%a`), `getfacl` 0, `lsattr` 0, `pacman -Qo/-Ql` 0, `root_mode` 0 |
| M4 | selftest case invocations | static Python count of call lines (definitions excluded) | **80** = 77 `check` + 3 `check_cli`; `check()` defined L1757, `check_cli()` defined L1811; first call L1838, last L2330 |
| M5 | source registry histogram | Python parse of table rows `^\| S\d{3} \|` | see §4 (HEAD and worktree) |
| M6 | root-mode discrimination probe | read-only `stat`, `getfacl -p`, `pacman -Qo /`, `findmnt`, `os.access` | see §5 |

C1 target (spec): M3 0 -> 1 and isolated 0755 / 0555 / unreadable discrimination. The blind spot is confirmed: the census has no probe of `/` mode while `/` is `555`.

Pass/fail for C1 must be read on its own `packages`-line token and its own arm verdict, not on the rollup. The rollup is already DEGRADED on this host (section 3), so a rollup-level comparison cannot show C1's effect.

## 3. Live baseline census (re-run once, read-only)

- Extracted HEAD copy: `git show HEAD:tools/tsukuroi-census.sh > /tmp/r12-census-resumed/census-HEAD.sh` (sha256 matches section 1; `bash -n` rc=0).
- Run: `timeout 180 bash /tmp/r12-census-resumed/census-HEAD.sh` -> **rc=1**, stderr 0 bytes, stdout 8 lines, wall ~4.33 s (the tool's own timing).
- Verdict: `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)` — same as inherited run.
- Raw stdout/stderr deleted after the header and plane-name check. Only the plane identities and verdicts above are retained. Counts inside the planes were not re-derived in this pass (inherited §3 counts are historical, not re-observed here).
- `root_mode` token count on the packages line was **not** re-counted live in this pass (the output was deleted before counting; the inherited gate value 0 is historical). Static evidence (0 `root_mode` tokens in the HEAD blob) is consistent with it.
- No `--selftest` invoked. No test, build, lint, formatter, or install run.

## 4. Source census histogram (Python-parsed)

Two parses: starting HEAD blob (inherited baseline) and current worktree (modified by Sources seat; reported, not edited here).

| measure | HEAD (`b76b5c3`) | worktree (current, Sources seat in progress) |
|---|---|---|
| sha256 | `3e06c2eb…259b2e2` | `3b798e30…3f74cd` |
| rows S-id | 34 (S001–S034) | 37 (S001–S037; new S035, S036, S037) |
| column count | all 11 | all 11 |
| tier | A 31, B 1, C 2 | A 32, B 1, C 4 |
| status | mined 26, queued 5, rejected 3 | mined 26, queued 6, rejected 5 |
| kind | docs 24, code 5, tool 2, own-work 2, dataset 1 | docs 25, code 5, tool 2, own-work 2, community 2, dataset 1 |
| tier × status | A/mined 25, A/queued 5, A/rejected 1, B/mined 1, C/rejected 2 | A/mined 25, A/queued 6, A/rejected 1, B/mined 1, C/rejected 4 |
| `used-by` empty | 8: S006, S012, S013, S018, S024, S029, S030, S033 | 11: the 8 above + S035, S036, S037 |
| recheck | on-release 15, 180d 10, 90d 9 | on-release 16, 90d 11, 180d 10 |
| opened | all 2026-10-19 | all 2026-10-19 |

Correction to inherited §4: the inherited histogram is correct **for HEAD only**. It is stale for the current worktree (three added rows). The inherited note's `used-by`/recheck counts apply to HEAD, not to the live file.

Tier-C check (QUALITY #7 style, count only): HEAD tier-C rows = 2, both rejected, none support. Worktree tier-C rows = 4, all rejected (S030, S033, S036, S037). Tier-C rows support nothing; no claim in this file depends on them.

## 5. Root-directory metadata probes (read-only, targeted, re-run)

| probe | observation | exit |
|---|---|---|
| `stat -c '%a %U:%G %F %n' /` | `555 root:root directory /` | 0 |
| `getfacl -p -- /` | owner root, group root, base entries `user::r-x group::r-x` (first 5 lines inspected; no named ACL lines seen) | 0 |
| `pacman -Qo /` | no owner (`error: No package owns /` in inherited run; rc re-observed = 1) | 1 |
| `findmnt -n -o TARGET,FSTYPE,OPTIONS /` | btrfs `rw,…,subvol=/@` — writable mount | 0 (inherited) |
| Python `os.stat('/')` | mode `0o555`, uid 0, gid 0 | — |
| Python `os.access('/', W_OK)` | False (DAC: user cannot write to `/`) | — |
| Python `os.listdir('/')` | succeeds (readable/listable) | — |
| `systemctl cat limine-snapper-sync.service` | not re-run in this pass (inherited `User=root`, `CapabilityBoundingSet=CAP_SYS_ADMIN`) | not run |
| `--file` CLI probe | not re-run (inherited rc=2 `unknown argument: --file`) | not run |

Discrimination note for C1 (design only, not a test): the three classes (0755 / 0555 / unreadable) map to `stat %a`, the `getfacl` presence check, and `stat`/`lstat` failure. Each is unprivileged for `/`. The `555` observation is a DAC-bit fact; it does **not** establish the EACCES cause (that belongs to C2 and stays `[inference]` here).

## 6. Reuse / reject / correct (against inherited CensusScribe.md#3B4C)

| inherited claim | status now |
|---|---|
| starting HEAD `b76b5c3…` | **reused** (re-verified) |
| census blob sha `1045…c11`, 2402 lines, `census-v2` | **reused** (re-verified by sha256 both sides) |
| C1 output absent | **reused** (still true: no tracked census change, no C1 evidence) |
| live verdict DEGRADED rc=1, 6 plane lines | **reused** (reproduced this pass) |
| M3 = 0 root-mode sites | **reused** (static recount) |
| selftest 80 = 77 case_home + 3 check_cli | **corrected**: 77 are `check` calls, 3 are `check_cli`; `case_home` is a variable set in each block, not a call form. Total 80 unchanged. |
| source histogram 34 rows / tier A31 B1 C2 / status 26-5-3 | **reused for HEAD only**; **corrected for live tree**: worktree now 37 rows (see §4) |
| `used-by` empty = 8 | **reused for HEAD**; live tree has 11 |
| `/` 555 root:root, `pacman -Qo /` unowned, btrfs rw | **reused** (re-observed) |
| `--file` rc=2 | **not re-run here** (inherited observation, marked historical) |
| S031 anchors "HEAD 9b70381 / lines 286-300, 441-446" stale | **not re-verified in this pass**; the inherited claim that anchors shift is carried as a risk, not re-checked |

Nothing in the inherited file is rejected outright.

## 7. Risks

- R1 (C1 operability): the census has 0 root-mode sites (M3). Adding the arm turns a silent blind spot into an explicit line. With `/` at 555 the arm will report on this host; the rollup already shows DEGRADED, so the rollup cannot show C1's effect. Fixtures must cover 0755 PASS, 0555 DEGRADED and unreadable BLOCKED/UNKNOWN; the live host can only exercise the 555 branch.
- R2 (doc drift): census header says "four-plane" / "four owned host planes" (lines 2, 7; also 25, 283, 2305 contain "four") while the code emits six `PLANE` lines. A C1 landing must sweep the header and SKILL/LOG mentions, or the claim surface stays inconsistent.
- R3 (pre-existing, not C1-owned): update-safety disagreement `qu=414` vs `sup=430` inside the census run (inherited; not re-run for counts in this pass). Flagged to owner; not changed here.
- R4 (provenance drift): the source registry changed under this lane (three added rows, worktree sha differs from HEAD). Any histogram cited after this point must name which tree it parsed.
- R5: the live verdict includes journal- and package-derived lines; only plane identities and verdicts are retained here. No raw config, credential, argv, or journal body is stored.
- R6 (C2 boundary): the `/` 555 fact is not an EACCES cause. Keep the mechanism `[inference]` until C2's matrix grounds it.

## 8. Commands run and exit codes (this pass)

| command | exit |
|---|---|
| `git rev-parse HEAD` | 0 |
| `git status --short` | 0 |
| `git show HEAD:tools/tsukuroi-census.sh` + Python sha256 (blob and worktree) | 0 |
| `git show HEAD:corpus/SOURCES.md` + Python sha256 and parse (HEAD, worktree) | 0 |
| Python static scan of census blob (stat/getfacl/lsattr/pacman/root_mode/PLANE/check counts/VERSION/four) | 0 |
| `bash -n` on extracted HEAD copy | 0 |
| `timeout 180 bash census-HEAD.sh` (live, read-only) | 1 (DEGRADED), stderr 0 bytes |
| `sha256sum census-HEAD.sh` | 0 |
| `stat -c '%a %U:%G %F %n' /` | 0 |
| `getfacl -p -- /` | 0 |
| `pacman -Qo /` | 1 (no owner) |
| `findmnt -n -o TARGET,FSTYPE,OPTIONS /` | 0 |
| Python `os.stat`, `os.access`, `os.listdir` on `/` | 0 (read-only) |

Not run: `--selftest`, any build, lint, formatter, test, package operation, installer, `sudo`, service or unit change, `systemctl cat` (inherited only), `--file` probe (inherited only).

Installs / upgrades: none. Tools used already present: bash, git, Python stdlib, coreutils `stat`, `getfacl` (acl), `pacman`, `findmnt`, `timeout`. `bc` was absent and was not installed; wall time taken from the census's own report.

Temporary artifacts: `/tmp/r12-census-resumed/census-HEAD.sh` (HEAD copy, read-only use). Raw census output deleted.

## 9. Handoff

- Starting HEAD and missing C1 output: confirmed. C1 is not yet landed; the gate's red-before state (`root_mode_count=0`) stands.
- For the parent's single post-integration check: rerun the inherited gate command once against the landed tree (expect `root_mode_count=1` on the packages line, and the verdict may remain DEGRADED because the live host is DEGRADED for other reasons). Judge C1 on its own line.
- Histogram for the final registry: parse the worktree after the Sources seat finishes, not the HEAD blob.
