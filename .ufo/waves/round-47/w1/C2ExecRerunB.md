VERDICT: supports

# Seat C2ExecRerunB — item C2-2 (independent-environment selftest re-run B)

Claim C2's declared target reproduces in an independent clone of the freeze revision, under
both requested locales, byte-for-byte: `PASS (164 cases, 164 passed, 0 failed)`, rc 0. No
divergence between the LC_ALL=C and LC_ALL=en_US.UTF-8 legs. Four divergences from the claim's
*prose* (not from its target) are named in §5; the most important is that a dirty TMPDIR now
relocates the fixture tree to `/tmp`, outside the caller's TMPDIR.

## 1. Environment

- Clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /fast/scratch/hyaku/tsukuroi-r47/C2ExecRerunB/clone`,
  `git remote remove origin`, `git checkout 77e9e2b2e96b85d8f048ae2087e246a542b71611`.
  `git -C <clone> rev-parse --show-toplevel` → `/fast/scratch/hyaku/tsukuroi-r47/C2ExecRerunB/clone`;
  `rev-parse HEAD` → `77e9e2b2e96b85d8f048ae2087e246a542b71611`.
- Tool bytes: `sha256sum <clone>/tools/tsukuroi-census.sh` →
  `adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41`, equal to
  `git -C <lane> show 77e9e2b2e96b85d8f048ae2087e246a542b71611:tools/tsukuroi-census.sh | sha256sum`
  and to the lane working-tree file (same digest). So the clone runs the freeze bytes.
- Second clone for the baseline comparison: `clone_base` at
  `916019057147d7e9ba6b137647b2cee26decf4b8` (census.sh sha256 `ac4e38ff99df044bf17410722b253965402afa1556fd105dde181e19e048f48e`).
- Spaced TMPDIRs used: `/fast/scratch/hyaku/tsukuroi-r47/C2ExecRerunB/tmp with space` (leg A),
  `.../tmp with space 2` (leg B), `.../tmp base space` (baseline), plus the verbatim frozen
  shape `.../frozen/t 2`. `HOME` was a scratch dir in every run.
- Locale: `locale -a | grep -i en_US` → `en_US.utf8`; `env -i LC_ALL=en_US.UTF-8 locale` prints
  `LC_CTYPE="en_US.UTF-8"` with no "cannot change locale" error, so the second leg was a real
  locale change, not a silent fallback.

## 2. The two required runs (rc + final line)

| Leg | Command (env) | rc | Final line |
|---|---|---|---|
| A | `env -i PATH=/usr/bin:/bin HOME=<h> LC_ALL=C TMPDIR="<scratch with a space>" bash <clone>/tools/tsukuroi-census.sh --selftest` | **0** | `TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)` |
| B | same with `LC_ALL=en_US.UTF-8`, TMPDIR=`.../tmp with space 2` | **0** | `TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)` |

Divergence between A and B: **none** — the two logs are byte-identical
(`md5sum` `2d22c691575dcddb0640ba74e821619d` for both, 15314 bytes, 167 lines).

Third, stronger leg — the claim's frozen counting command, verbatim, against the **lane** path
(`S=<scratch>; mkdir -p "$S/t 2"; env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$S/t 2" bash
<lane>/tools/tsukuroi-census.sh --selftest`): rc **0**, same final line, and the log is
byte-identical to legs A and B (same md5). The declared target is therefore reproduced exactly
as declared, from three independent directory layouts.

Label census in the passing log (`selftest-LC_ALL=C.log`):
`grep -c '^PASS '` → 164; `grep -c '^FAIL '` → 0; `grep -c 'R47-C2'` → 2 (both PASS, lines 165-166);
`grep -c 'R46-C1'` → 8 (all PASS, lines 157-164).

## 3. Baseline control (does the fix do anything?)

`clone_base` (9160190) with the **same spaced-TMPDIR shape**:

| Run | rc | Final line |
|---|---|---|
| base, `TMPDIR=".../tmp base space"` | **1** | `TSUKUROI_CENSUS_SELFTEST: FAIL (162 cases, 13 passed, 149 failed)` |
| base, space-free `TMPDIR=".../tmpnospace"` | **0** | `TSUKUROI_CENSUS_SELFTEST: PASS (162 cases, 162 passed, 0 failed)` |

So the space alone flips the base from 162/162 to 13 passed / 149 failed, and the freeze
revision repairs exactly that. The base failures are all of one shape, e.g.
`FAIL blocked: pacman db.lck: configured root not asserted at a field boundary (wanted
root_dir=/fast/scratch/.../tmp base space/tsukuroi-r3-2-selftest.3s9aCv/fx/blocked-lck/root;
possible live-root read)` — the fixture roots handed to the census as root overrides contain a
space and `root_locator_class` refuses them. The base also **passes all 8 (R46-C1) cases** under
the dirty TMPDIR, so the 149 failures are not an identity-path regression.

Case-name set comparison (base space-free 162 vs final 164), by `comm` on the `PASS|FAIL <area>:`
prefixes: 162 common, 0 dropped, 0 renamed, 2 added — exactly
`selftest: the fixture base classifies absolute even when TMPDIR contains a space (R47-C2)` and
`selftest: a space in a root override stays unsafe by design (R47-C2)` (census.sh:3477, :3481).

## 4. Claim kill rules re-measured (supplementary, cheap)

- **Live census, digits-stripped, base vs final**: byte-identical
  (`sed 's/[0-9]//g'` on both live outputs, `diff` empty; both rc 2, both
  `TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=BLOCKED drivers=DEGRADED journal=DEGRADED
  update-safety=BLOCKED oom=DEGRADED)` under `env -i`). Receipts `live-{base,final}-digits-stripped.txt`,
  identical sha256 `09547ccf…`.
- **`--identity` line shape unchanged**: base and final both print one line with the same fields
  in the same order (`version= sha256= md5= bytes= lines= planes= exit_map= verified=yes`), the
  same `planes=packages,systemd,drivers,journal,update-safety,oom` and the same
  `exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED`; only `sha256/md5/bytes/lines` differ, which is
  required because the file bytes changed (`bytes=210762 lines=3622` → `bytes=212252 lines=3644`).
- **Exit map unchanged**: identical string in both identity lines (above).
- **(R46-C1) cases**: 8 labelled cases, 8 PASS, 0 FAIL at both revisions. The declaration's
  "all six (R46-C1) cases still pass" is true but undercounts the labels: six are the
  `identity:` cases and two more `cli: --identity …` cases also carry the `(R46-C1)` tag.

## 5. Divergences named

1. **The fix bypasses the caller's TMPDIR when TMPDIR is dirty.** With a spaced TMPDIR the
   fixture base becomes `/tmp` (census.sh:2055-2059:
   `local st_base=${TMPDIR:-/tmp}; case "$st_base" in *[!A-Za-z0-9._/+-]*) st_base=/tmp ;; esac;
   work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")`). Direct evidence from the failing
   fixture paths inside my private-tmpfs run: `root_dir=/tmp/tsukuroi-r3-2-selftest.SIK1eN/fx/...`.
   Consequence: a caller who sets TMPDIR for quota/filesystem isolation gets writes in the shared
   `/tmp` instead; the two alternatives in item C2-R1 (fail fast, or a space-free subdir *under*
   TMPDIR) would not have this property. Safety is preserved (`mktemp -d` creates the tree 0700 —
   observed `drwx------`) and cleanup works (see 2 below), so this is an operability note, not a
   correctness defect against the declared target.
2. **Cleanup of the `/tmp` tree is by EXIT trap only, and only for that run's own dir.**
   census.sh:2062 `trap 'chmod -R u+rwx -- "${work:-}" …; rm -rf -- "${work:-}" …' EXIT INT TERM`.
   Verified: in a private `unshare -m` tmpfs `/tmp`, the run leaves **0 entries** behind
   (`private tmp after: 0 entries`) for both the spaced and the space-free TMPDIR. On the shared
   host `/tmp` I observed transient `/tmp/tsukuroi-r3-2-selftest.*` trees during concurrent
   sibling seats' in-flight runs (e.g. `C2CritTMP/run-dirty.log:167` records
   `INST_WORK_DIR: /tmp/tsukuroi-r3-2-selftest.9g7bVR`); I could not attribute every observed
   residue dir to a specific seat, and I removed nothing outside my own scratch.
3. **The selftest is not root-clean, and that is unrelated to this fix.** Under
   `unshare -m -r` (euid 0 in the namespace) the run reports
   `FAIL (164 cases, 159 passed, 5 failed)`: `R35-C1` unreadable-dir, two `R38-W1`/`R40-C1`
   unlistable-sysfs-root and two `R44-C1` unreadable-record/dir cases. Control: the **same five**
   fail in that namespace with a *space-free* TMPDIR, and outside the namespace uid 1000 cannot
   read a `chmod 000` dir while namespace-root can (`euid=0 … READABLE`). So the cause is DAC
   bypass by euid 0, not the R47-C2 edit. Anyone re-running the selftest as real root should
   expect those five.
4. **Declaration wording `failed 13/162`.** The measured base line is
   `FAIL (162 cases, 13 passed, 149 failed)`: 13 is the *passed* count, 149 is the failed count.
   The round-47 battery control agrees (`battery-summary-r47.jsonl`: "C2-K0 do-nothing (base
   census, space TMPDIR)" → `FAIL (162 cases, 13 passed, 149 failed)`), and the fix's own code
   comment says "must not turn 149 cases red" (census.sh:2054). The number 13 is right; the word
   "failed" inverts it. Suggested wording: "passed 13 of 162 at base (149 failed)".

## 6. What I did not do

- Did not run the round-46 identity counter (`score-census-identity-r46.py`) — that is item
  C2-K5's seat; I only re-measured its (R46-C1) label legs from the selftest log.
- Did not mutation-test the fix (items C2-4/C2-5) or review its design (C2-R1).
- Did not touch any tracked lane file, any git/jj state, the fleet repo, PATH dirs, or the host;
  no package/service/sysfs/scrub action was taken, and no `btrfs`/`systemctl` mutating command
  was run. Only read-only host queries (`locale`, `ls`, `stat`, `find`, `unshare` with a private
  tmpfs mount, and the census's own read-only probes).
- No tool was installed or upgraded (no install was needed; pacman is paused host-wide).

## 7. Receipts (in `.ufo/waves/round-47/w1/C2ExecRerunB/`)

| File | sha256 | Content |
|---|---|---|
| `selftest-LC_ALL=C.log` | `f8c8acfba89b45f4a5c015d1da0f0d33b610f620b0734026bd56dae6a12eb51c` | leg A, 167 lines, rc 0 |
| `selftest-LC_ALL=en_US.UTF-8.log` | `f8c8acfba89b45f4a5c015d1da0f0d33b610f620b0734026bd56dae6a12eb51c` | leg B, byte-identical to A |
| `selftest-frozen-counting-command.log` | `f8c8acfba89b45f4a5c015d1da0f0d33b610f620b0734026bd56dae6a12eb51c` | frozen command verbatim vs the lane path |
| `baseline-rev-selftest-spaced-TMPDIR.log` | `4aba0cc43ec961637eac386ef3fe0583975e7b9f8143696d885e891b9f213d8d` | base 9160190, dirty TMPDIR, rc 1 |
| `baseline-rev-selftest-plain-TMPDIR.log` | `2e6f5f7acd25d0bc28fb41bcb360032e50f0974e77bf520e066008a243cf7a0e` | base 9160190, clean TMPDIR, rc 0 |
| `live-final.txt` | `c5622b9d31869aeb1045b8999d981dc38e366e215c1770ce47c88cac86987cd5` | live census at the freeze revision |
| `live-base-digits-stripped.txt` / `live-final-digits-stripped.txt` | `09547ccfb23be73533042b2db6adf6d07fc77e08bf48f487ce311b5fe5612d1a` (both) | kill-rule comparison, identical |
| `namespace-private-tmpfs-run.log` | `ff2e5585cb9660cdedc79239413496f06b273379083fd667e91629916af322e7` | private tmpfs `/tmp`, spaced TMPDIR, 5 DAC-bypass failures |
| `namespace-private-tmpfs-control-spaceless.log` | `b4d75b065d85a8577ffd687d2afeea721f8a57ad7e49c738b709b8a92e69c842` | same namespace, space-free TMPDIR — same 5 failures |

Scratch `/fast/scratch/hyaku/tsukuroi-r47/C2ExecRerunB` held the clones and logs; the receipt
copies above are the evidence of record.
