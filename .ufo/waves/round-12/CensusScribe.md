# CensusScribe — round-12 starting measurement and source histogram

Scope: baseline only (no implementation, no tests, no git mutation). Paths relative to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Lane tools: Python stdlib parsing, `git show`, one read-only live census run, targeted read-only host probes. No installs, no sudo, no service/unit changes. Raw live census output was deleted after summarizing; only sanitized summaries below are retained.

## 1. Starting state and C1 output status

- Starting HEAD: `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`. `git status --short` at run time: only `?? .ufo/waves/round-12/`; no tracked modification (checked before and after the live run).
- Census blob at HEAD: `tools/tsukuroi-census.sh`, sha256 `1045244387ffcd5d3db481dd0d3d30e34097abc24744d954e791b81d28b20c11` (`git show HEAD:... | sha256sum`), 2402 newline-terminated lines, `VERSION='census-v2'` (line 323).
- **C1 output: absent.** `.ufo/waves/round-12/` contains only `dispatch.json`, `spec.json`, `swarm-registry.json` (plus this file). No C1 census diff, no C1 evidence file, and no tracked change to `tools/tsukuroi-census.sh` exists. The baseline below is therefore pre-edit by construction; any C1 result must be compared against section 3.

## 2. Measurement design (frozen baseline metrics)

| id | metric | method | baseline at HEAD |
|---|---|---|---|
| M1 | verdict line and rc | `bash <HEAD copy>` live, read-only | `TSUKUROI_CENSUS: DEGRADED ...`, rc=1 |
| M2 | per-plane verdicts (6 planes) | same run, `PLANE <name>:` lines | see §3 |
| M3 | root-directory metadata arm count | static count of `stat -c` format `%a/%A/%U/%G`, `getfacl`, `lsattr`, `pacman -Qo`/`-Ql` probe sites in the census | **0 sites** (static Python scan; `stat -c` sites = 6, all `%W`/`%Y` on sync dbs / offline.db) |
| M4 | selftest case rows (static, not executed here) | count of `check` / `check_cli` invocations | 80 (77 `case_home` + 3 `check_cli`) |
| M5 | source registry histogram | Python parse of `corpus/SOURCES.md` table at HEAD | §4 |
| M6 | root-mode discrimination probe (read-only) | `stat`, `getfacl -p`, `pacman -Qo /`, `findmnt /` | §5 |

Target for C1 (per the round-12 spec): M3 0 -> 1 and isolated 0755 / 0555 / unreadable discrimination. The baseline demonstrates the blind spot directly: the census has zero probe sites for the mode of `/`, while the host's `/` is in fact `555`.

## 3. Live baseline census (single run, read-only)

- Method: `git show HEAD:tools/tsukuroi-census.sh > /tmp/r12-census/census-HEAD.sh`; `sha256sum` equal to the HEAD blob; `bash -n` OK; then `timeout 180 bash /tmp/r12-census/census-HEAD.sh`. Wall 3.69 s, rc=1, stderr 0 bytes, stdout 8 lines. Header timestamp `2026-10-20T02:13:56Z` (UTC). No tests were run; the `--selftest` path was not invoked.
- Verdict: `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)`. Exit 1 = DEGRADED (worst plane wins).
- Sanitized plane summaries (counts only; names, versions and journal text omitted):
  - packages: DEGRADED. `pacman -Qkk` sample 8, rc=1, drift=2 within sample; foreign=16 (known=16, new=0, drift=0, gone=0) against baseline r6; holds declared; db.lck absent.
  - systemd: HEALTHY. scope=user running, failed=0, timers 2/2 scanned, timer_fail=0.
  - drivers: DEGRADED. kernel-ring err=37 classed as accepted noise floor; mem arm HEALTHY (C1=0, C2=0, C3=0, C5 swap fail=0, C6 PSI avg300=0.00); guards max/max.
  - journal: DEGRADED. boots=10, current=yes, target active; err=39 (coredump=0, kernel=37, other=2); failedhist=0; timer drift 0.
  - update-safety: DEGRADED (REQUIRES-PREP). candidate counts disagree inside the census (`qu=414`, `sup=430`, `disagree`); `-Suu` trap row reports 430; chan dbs=5, stamp 3d; offline.db absent.
  - oom: DEGRADED. window 10 boots; C1_kernel=1, killed_process=0; C2=16, C3=5 events, 7 clusters; baseline r8 known=0, new=7, missing=0, out_of_window=2.
- Raw output deleted after summarizing (`/tmp/r12-census/live-baseline.{out,err}`); `/tmp/r12-census/census-HEAD.sh` retained for re-run.
- Implication: the live rollup is already DEGRADED for reasons unrelated to root metadata. A C1 root-mode arm that degrades on this host will leave the rollup unchanged, so rollup-level comparison cannot show C1's effect; C1 must be judged on its own plane/arm line.

## 4. Source census histogram (HEAD `corpus/SOURCES.md`, Python-parsed)

- Registry rows: 34 (S001–S034), all with 11 columns (`id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by`), zero column-count mismatches; all `opened` = 2026-10-19.
- Tier: A 31, B 1 (S023), C 2 (S030, S033).
- Status: mined 26, queued 5, rejected 3.
- Kind: docs 24, code 5, dataset 1, tool 2, own-work 2.
- Tier x status: A/mined 25; A/queued 5; A/rejected 1 (S029); B/mined 1; C/rejected 2 (S030, S033).
- Tier-C rows: 2, both rejected; none is support (QUALITY #7 satisfied by count).
- `used-by` empty (`—`): 8 rows = the 5 queued rows (S006, S012, S013, S018, S024) plus rejected S029, S030, S033.
- `recheck = on-release`: 15 rows. Recheck `90d`/`180d` for the remainder.

Risks in the registry relevant to C1:
- S031 (own-work, census) pins "current lane HEAD 9b70381" and "Comments 286-300 and CLI help 441-446". Starting HEAD is `b76b5c3`; the anchors match HEAD line ranges (help block 439-452) but the pinned revision is stale. Any C1 line shift will break S031 anchors, and QUALITY #10 requires the sweep.

## 5. Root-directory metadata probes (read-only, targeted)

| probe | observation |
|---|---|
| `stat -c '%a %U:%G %F %n' /` | `555 root:root directory /` |
| `getfacl -p -- /` | base entries only (`user::r-x group::r-x other::r-x`); no extended ACL |
| `pacman -Qo /` | `error: No package owns /`, rc=1 (unowned: `pacman -Qkk` cannot judge `/`) |
| `findmnt -n -o TARGET,FSTYPE,OPTIONS /` | btrfs `rw` (subvol `/@`): the mount is writable, so `555` is a DAC mode, not a read-only mount |
| `pacman` local db `filesystem-2025.10.12-1/mtree` (gz-decoded, Python) | 136 entries, 0 root `.` entries (consistent with the unowned-`/` observation) |
| `systemctl cat limine-snapper-sync.service` (read-only) | `User=root`, `CapabilityBoundingSet=CAP_SYS_ADMIN` |

Discrimination note for C1 design (not a test run): the three observable classes needed (0755 / 0555 / unreadable) map to `stat %a`, `getfacl` presence and `stat`/`lstat` failure; the probes above show each is available unprivileged for `/`. The `/` 555 observation is a DAC-bit fact and does not establish the EACCES cause (that belongs to the C2 matrix; this lane does not claim it).

## 6. Risks and open items

- R1 (C1 operability): the census has 0 root-mode sites (M3). Adding the arm turns a silent blind spot into an explicit line; with `/` at 555 the arm will report DEGRADED on this host, which the rollup already shows as DEGRADED. Fixtures must cover 0755 PASS, 0555 DEGRADED and unreadable BLOCKED/UNKNOWN; the rollup-only check cannot distinguish them on the live host.
- R2 (doc drift): the census header says "four-plane" / "four owned host planes" (lines 2, 7) while the code emits six `PLANE` lines (M2). A C1 landing must sweep the header and SKILL/LOG mentions, or the claim surface stays internally inconsistent.
- R3 (pre-existing census disagreement, not C1-owned): update-safety reports `qu=414` against `sup=430` in the same run; the census keeps the larger count and degrades. Flagged for the owner; not changed here.
- R4 (provenance): `snapper-eacces-mechanism.md` records the `/` 555 observation and the missing `pacman -Qo /` owner from 2026-10-19; this lane re-observed both (§5) rather than reusing the note. The EACCES mechanism itself stays `[inf]` in this file.
- R5: the live verdict includes journal and package-derived lines. Only counts are retained here; raw output was not written to the repository.

## 7. Tools, installs, verification

- Installs/upgrades: none. Used existing `/usr/bin/getfacl` (acl package, already present), `pacman`, `findmnt`, `systemctl`, `stat`, `bash`, and Python stdlib.
- Commands run and exit codes: `git show HEAD:tools/tsukuroi-census.sh | sha256sum` (0); `bash -n` on the copy (0); `timeout 180 bash census-HEAD.sh` (1, DEGRADED); `stat -c` on `/` (0); `getfacl -p -- /` (0); `pacman -Qo /` (1, unowned); `findmnt` (0); `systemctl cat limine-snapper-sync.service` (0); `git status --short` (0).
- Not run: `--selftest`, any build, lint, or formatter (per assignment; parent runs checks once after integration).
- Independence: this is author-side seat evidence; it is not independent non-author verification.

## 8. Root-mode red-before gate (C1 D6 proof) and `--file` probe

Gate script (temp, not in repo): `/tmp/r12-census/root_mode_gate.py` (978 bytes; stdlib only). It runs the census once via `timeout 180 bash CENSUS`, parses stdout, and counts `\broot_mode=` tokens in the single `PLANE packages:` line. Only counts and exit codes are printed, never the plane line. Gate exit 0 iff count == 1; otherwise exit 1. Census rc is printed separately and is not the gate. If the packages line is missing or duplicated, it prints `UNASSESSABLE` and exits 1.

Recommended command (inline, no tmpfs dependency; run once at closure against the tree under review). The `-c` payload is byte-identical to the source file below; this was checked by a non-executing `shlex` parse, and the census itself was not re-run for this change. Observed red at line 91 came from the same logic run from the temp file.

````
python3 -c '#!/usr/bin/env python3
# root_mode_gate.py CENSUS_SH
# Runs the census once, read-only, and counts `root_mode=` tokens in the single
# `PLANE packages:` line. Prints only counts and exit codes (never the plane line).
# Gate: exit 0 iff exactly one root_mode= token; exit 1 otherwise.
# The census'\''s own exit status is printed separately and is NOT the gate.
import re
import subprocess
import sys

if len(sys.argv) != 2:
    print('\''usage: root_mode_gate.py CENSUS_SH'\'', file=sys.stderr)
    sys.exit(2)
census = sys.argv[1]
p = subprocess.run(['\''timeout'\'', '\''180'\'', '\''bash'\'', census], capture_output=True, text=True)
pk = [ln for ln in p.stdout.splitlines() if ln.startswith('\''PLANE packages:'\'')]
if len(pk) != 1:
    print(f'\''root_mode_count=UNASSESSABLE packages_lines={len(pk)}'\'')
    print(f'\''census_rc={p.returncode}'\'')
    sys.exit(1)
count = len(re.findall(r'\''\broot_mode='\'', pk[0]))
print(f'\''root_mode_count={count}'\'')
print(f'\''census_rc={p.returncode}'\'')
sys.exit(0 if count == 1 else 1)
' tools/tsukuroi-census.sh
````

Observed (before):

- `repo census == HEAD` printed; sha256 `1045244387ffcd5d3db481dd0d3d30e34097abc24744d954e791b81d28b20c11`.
- `root_mode_count=0`, `census_rc=1` (DEGRADED), `gate_exit=1`. This is the red-before state for the D6 proof: the same command must exit 0 after the parent lands the C1 arm, with exactly one `root_mode=` token on the packages line.
- Raw census output was written to a temp file and deleted after the count.
- `git status --short` after the run: only `?? .ufo/waves/round-12/`.

Source snapshot and CLI probe:

- The census CLI does NOT support `--file`. Probe: `bash /tmp/r12-census/census-HEAD.sh --file /tmp/r12-census/SOURCES-HEAD.md` gives rc=2, stderr `tsukuroi-census: unknown argument: --file` (usage arm, exits before any probe). The census reads no source registry at all, so no historical SOURCES input path exists.
- Historical SOURCES baseline kept as a temp snapshot without touching the registry: `git show HEAD:corpus/SOURCES.md > /tmp/r12-census/SOURCES-HEAD.md`, sha256 `3e06c2ebb36f5feaf84978238a9bd36d76a2313c017a0f9916fbc0bf0259b2e2` (matches `git show HEAD:corpus/SOURCES.md | sha256sum`). `corpus/SOURCES.md` was not edited.
- Earlier §4 histogram was parsed from this same HEAD blob (34 rows).

Exact source of the gate (`/tmp/r12-census/root_mode_gate.py`, 978 bytes, sha256 `7fca52e83c19b509…`; the inline payload above is this text, shell-quoted):

````python
#!/usr/bin/env python3
# root_mode_gate.py CENSUS_SH
# Runs the census once, read-only, and counts `root_mode=` tokens in the single
# `PLANE packages:` line. Prints only counts and exit codes (never the plane line).
# Gate: exit 0 iff exactly one root_mode= token; exit 1 otherwise.
# The census's own exit status is printed separately and is NOT the gate.
import re
import subprocess
import sys

if len(sys.argv) != 2:
    print('usage: root_mode_gate.py CENSUS_SH', file=sys.stderr)
    sys.exit(2)
census = sys.argv[1]
p = subprocess.run(['timeout', '180', 'bash', census], capture_output=True, text=True)
pk = [ln for ln in p.stdout.splitlines() if ln.startswith('PLANE packages:')]
if len(pk) != 1:
    print(f'root_mode_count=UNASSESSABLE packages_lines={len(pk)}')
    print(f'census_rc={p.returncode}')
    sys.exit(1)
count = len(re.findall(r'\broot_mode=', pk[0]))
print(f'root_mode_count={count}')
print(f'census_rc={p.returncode}')
sys.exit(0 if count == 1 else 1)
````
