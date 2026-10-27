VERDICT: defect-found

# C1-10 — probe: does `--identity` ever print `verified=yes` with digests of bytes bash did not execute?

**Answer: yes.** Two deterministic reproducers, both on the implementation revision
a44770491eb5ca15ce9f8b3207309d1af683ffaf (`tools/tsukuroi-census.sh` sha256
`d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa`, 209208 bytes, 3598 lines).
The hypothesis in the item is falsified: the mode *does* print a `verified=yes` line whose
sha256/md5/bytes/lines describe a file the running bash never executed.

Seat: leaf, probe only. No lane file was written; nothing on the host was mutated; one installed
tool was not needed. All builds, copies and fixtures lived under
`/fast/scratch/hyaku/tsukuroi-r46/C1LabReplace/` and are removed at exit; the receipts named below
are the surviving copies under `.ufo/waves/round-46/w1/C1LabReplace/`.

## 0. Baseline (so the probes are anchored)

```
$ bash census-a4477049.sh --identity          # pristine copy, cwd = its own dir
TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa md5=db08a606ce128da3839457372e91e220 bytes=209208 lines=3598 planes=packages,systemd,drivers,journal,update-safety,oom exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED verified=yes
rc=0
```

Frozen counter on the implementation revision (one run, my seat, alone):

```
$ python3 tools/score-census-identity-r46.py --revision a4477049… --scratch /fast/scratch/…/s
{"census_sha256":"d925839c…","cli_ok":1,"identity_ok":1,"nowrite_ok":1,
 "selftest_pass":1,"selftest_r46":6,"symlink_ok":1,"tracks_ok":1,"unverifiable_ok":1,
 "verdict":"PASS", "detail":{"selftest":{"last":"TSUKUROI_CENSUS_SELFTEST: PASS (160 cases, 160 passed, 0 failed)"}}}
```

So the counted legs pass (receipt `counter-impl.json`); everything below is outside the frozen
predicate's coverage. Identity runtime measured at **0.017 / 0.026 / 0.021 s** vs **3.684 s** for the
live census (`probes6.log`, X3).

## 1. Item results, each with the exact output and the honesty judgement

`(a)` **replace by rename after bash opened it** — honest.

```
### A rename-replace at line 1 (decoy = census + one appended line)
rc=0
TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=unverifiable md5=unverifiable bytes=unverifiable lines=unverifiable planes=packages,systemd,drivers,journal,update-safety,oom exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED verified=no
== path now holds sha256 (decoy) ==
0afe2e17a14c02893512f17982c77d472033b6635f9127cc256236ea350d65a1  …/A/census.sh
```
Same result for `rm -f -- "$0"` (A2, `probes2.log`): `unverifiable` / `verified=no`, rc=0, one line.
Also confirmed from outside the process (X1b, `probes6.log`): an external `mv -f decoy census.sh`
1 s into a run → `verified=no`. The rename path is correctly covered.

`(b)` **in-place overwrite — the answer depends on which side of bash's read cursor the edit lands.**

(b.i) edit *ahead* of the cursor (identical-length rewrite at line 1, i.e. before bash has read the
`VERSION` line) — **honest**, bash executes the new bytes and the digests match them:

```
### P3  (probes4.log)
TSUKUROI_CENSUS_IDENTITY: version=decoy-v99 sha256=461b3da065295d616caaee001b3120ffa2cdda77e129429a1df2e2ea7441093b md5=e1b0db1bb23c3ac15e6f2f273b2e508e bytes=209238 lines=3599 … verified=yes
rc=0
== umask syscalls ==
2750329 umask(000)                      = 022
== file on disk ==
455:VERSION='decoy-v99'   453:umask 000    461b3da0…  census.sh
```

(b.ii) edit *behind* the cursor (identical-length rewrite placed after `umask 077`/`VERSION` have
been executed) — **DISHONEST**. This is the defect; reproducer
`repro-p1-inplace-edit.sh`:

```
$ ./repro-p1-inplace-edit.sh /fast/scratch/…/repro/p1 impl-a4477049.sh
built census.sh bytes=209238 decoy bytes=209238 same-length=True
--- run (strace records the umask(2) the executed bytes asked for) ---
TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=3142445b86cd408641c5def25ed4f3bb22aa01e38d9ce4bf9936b012c841a4c9 md5=748c3b38bafebbe7075ae0093148086b bytes=209238 lines=3599 planes=… verified=yes
rc=0
--- kernel saw:
2182913 umask(077)                      = 022
--- the file the identity hashed, after the run:
454:VERSION='decoy-v99'
452:umask 000
3142445b86cd408641c5def25ed4f3bb22aa01e38d9ce4bf9936b012c841a4c9  census.sh
3142445b86cd408641c5def25ed4f3bb22aa01e38d9ce4bf9936b012c841a4c9  decoy
bytes=209238 lines=3599
```
(The same script run against the lane *worktree* draft prints `bytes=210792 sha256=4be94d39… verified=yes`,
same mismatch — `repro-p1-draft-worktree.out`.)
The executed stream said `umask 077` (kernel witness `umask(077)`) and `VERSION=census-v2` (the
printed `version=` field); the hashed file says `umask 000` and `VERSION='decoy-v99'`. `verified=yes`
therefore names 209238 bytes whose two identifying statements never ran. Re-running the same now-edited
file prints the *same* sha256 with `version=decoy-v99` (P1b), so the earlier line is indistinguishable
from a genuine run of the decoy — a reader re-deriving provenance gets the wrong revision.

Same shape from a third-party writer (the realistic case: an in-place save/upgrade of the checkout
while the census runs) — X1, `probes6.log`:

```
### X1 external in-place rewrite during a 2 s window
rc=0
TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=cd98d9d8e8011fd3d62a43973c928a47cfd672521db5168745b5f298938e33af md5=edb61337241ef8945b1c5edfc3e6b70b bytes=209216 lines=3599 … verified=yes
== file on disk after the external rewrite == 454:VERSION='decoy-v99'  452:umask 000  cd98d9d8… census.sh == decoy
```

(b.iii) length-changing in-place overwrite (the literal "`cat decoy > census.sh` on the first line"
with a decoy of different size) — no false yes, but no line either: bash's parse offsets shift and it
dies before `main`:

```
### B1 in-place overwrite at line 1
rc=2
…/B1/census.sh: line 2: syntax error near unexpected token `('
```
With a shorter decoy (B3) bash continues misaligned and executes decoy/garbage without ever reaching
`--identity`:
```
### B3 short decoy overwrite at line 1
rc=0
…/B3/census.sh: line 2: ipefail: command not found
DECOY-TAIL
```
Honest in content (no false claim), but see §3.1: exit 0 with zero output is itself a contract hole.

`(c)` **truncate in place — the smallest dishonest line in the whole set.**

(c.i) truncate immediately before `main "$@"` → the entire 209 KB script executes (the line itself is
proof: only the full file defines `census_identity` and calls `main`), yet the fd now holds zero bytes:

```
$ ./repro-c2-truncate.sh /fast/scratch/…/repro/c2 impl-a4477049.sh
injected: : > "$0"   immediately before main "$@"
rc=0
stdout: TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 md5=d41d8cd98f00b204e9800998ecf8427e bytes=0 lines=0 planes=packages,systemd,drivers,journal,update-safety,oom exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED verified=yes
bytes left in census.sh: 0
sha256 of the empty string: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
CONTROL (same injection, truncating a different file):
TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=56799c9966e54c87bd1253df74ab87314737640f8d165b914d5692790055aa65 md5=b39213e8db5f7d70edff043d73ac0b99 bytes=209229 lines=3600 … verified=yes
```
**Dishonest**: `verified=yes`, `bytes=0`, `lines=0`, sha256 of the empty string — for a process that
executed 209 KB and could not have printed anything if it had not.

(c.ii) truncate at line 1 (`C1`) and `truncate -s 4096` at line 1 (`C3`) → rc=0, **no output at all**,
file left empty/4096 bytes (`probes2.log`). No false claim, but a silent success.

`(d)` **hard link invoked by the other name** — honest in every shape tested (`probes2.log` D1–D4):

| shape | output | honest? |
|---|---|---|
| D1: `ln census.sh alias.sh`; `bash alias.sh --identity` | `sha256=d925839c… bytes=209208 … verified=yes` | yes — `stat -c %i` shows one inode for both names |
| D2: alias invoked, sibling name `census.sh` rename-replaced mid-run | `sha256=48674ea3… bytes=209253 … verified=yes` | yes — the fd still resolves to the invoked inode, and 209253 is exactly the injected alias file that ran |
| D3: alias invoked, sibling name overwritten **in place** | `sha256=2ed5d072… bytes=209253 lines=3599 … verified=yes` while `grep '^VERSION='` on disk says `decoy-v99` | **no** — same defect as (b.ii), reached through the second name |
| D4: invoked name unlinked | `unverifiable` / `verified=no` | yes |

Boundary, not defect: a hard link has no "the invoked file" identity beyond the inode, so `verified=yes`
with the *same* digests for either name (D1) is the only correct answer.

`(e)` **bind mount — not probed, stated.** Mounts are forbidden in this seat outside a private
`unshare` namespace, and a bind mount would change nothing that (f) does not already settle: the
identity takes the same path (`readlink -f $SELF` vs `readlink /proc/$$/fd/N`) either way, and it
performs no write. I recorded this instead of guessing: `probes2.log` section (e).

`(f)` **read-only path — honest, and it writes nothing.** Two independent checks:

```
# F1: 0555 dir, 0444 file, unprivileged
TSUKUROI_CENSUS_IDENTITY: … sha256=d925839c… bytes=209208 lines=3598 … verified=yes
rc=0 ; dr-xr-xr-x 2 vgpnk vgpnk … /fast/scratch/…/F1 ; -r--r--r-- 1 vgpnk vgpnk 209208 census.sh
```
```
# genuinely read-only filesystem: bind mount remounted ro inside a private user namespace
findmnt: ro,nosuid,nodev,noatime,inode64,…
write attempt: …/ro/probe: Read-only file system
identity: TSUKUROI_CENSUS_IDENTITY: … sha256=d925839c… bytes=209208 lines=3598 … verified=yes
rc=0
```
Receipt `readonly-fs.out`. Syscall trace of a normal run (`trace-identity-f2.txt`) shows **no**
write-mode open, rename, unlink, truncate, mkdir or link on the script or the cwd — the only write-mode
opens are `/dev/null` and a failed `/dev/tty`; the five opens of the script are
`openat(AT_FDCWD, "/proc/<pid>/fd/255", O_RDONLY)` (sha, md5, wc -c, wc -l, sha again), matching
`tools/tsukuroi-census.sh:3479-3483`.

## 2. Why it happens (code path, with line numbers)

* `tools/tsukuroi-census.sh:3471-3477` chooses the descriptor by `readlink /proc/$$/fd/N == readlink -f $SELF`.
  An in-place rewrite keeps both the inode and the path, so the match stays true — there is no signal
  that the content changed after bash read it.
* `:3478-3486` then hashes that descriptor's **current** content; the only consistency check is
  `sha2 == sha` across the identity's own five reads (`:3483`). Nothing relates the hashed bytes to
  bash's consumed offset.
* bash reads the script on fd 255 in 8192-byte chunks and never rewinds (`trace-reads-255.txt`: 25
  reads of 8192, the single `lseek(255, 0, SEEK_CUR)` at line 14 is a position query). Bytes behind
  the cursor are executed once, from the old content; the identity hashes the new content. That is
  exactly the (b.i) vs (b.ii) asymmetry: an edit ahead of the cursor is honestly named because bash
  executes the new bytes (`umask(000)` in P3), an edit behind it is not (P1).

Coverage gap, for the record: the only reopen race the selftest tests is rename
(`tools/tsukuroi-census.sh:3440-3447`, label `(R46-C1)`), and the counter's `unverifiable_ok` leg is
stdin / process substitution / "replaced after open" by rename
(`tools/score-census-identity-r46.py:22-33`, `:199-215`). No case edits the file **in place**, which
is why `identity_ok … selftest_r46 = 6` can be 1/6 while the defect stands.

## 3. Edge findings (all measured, all with exact output in the receipts)

1. **Silent exit 0 with no identity line** (C1, C3, B2, B3): when the in-place edit removes the tail
   bash has not yet read, bash reaches EOF and exits 0 having printed *nothing*, while the usage text
   promises "`--identity` alone prints one TSUKUROI_CENSUS_IDENTITY line … exit 0"
   (`tools/tsukuroi-census.sh:605`). A wrapper that only checks the exit status reads this as success.
2. **The identity trusts the caller's tool resolution.** With `sha256sum`/`md5sum` exported as shell
   functions (`export -f`) the line becomes
   `sha256=0123456789abcdef… md5=0123… verified=yes` (P6), and a PATH-first fake `sha256sum` does the
   same while md5 stays genuine and the line still reads `verified=yes` (P7, `probes3.log`). Control
   without `export -f` prints the true digest (P6c). This is environment trust, not a bug in the fd
   logic, but it means "verified=yes" is only as strong as the caller's `PATH`/function namespace.
3. **`/dev/stdin` as the script path verifies honestly** (`bash /dev/stdin < census.sh --identity` →
   `sha256=d925839c… verified=yes`): the fd resolves to the real file and bash did execute those bytes.
   Contrast: `bash -s -- --identity < F` (selftest), `bash <(cat F)` and a FIFO-fed script all print
   `unverifiable` (`probes2.log` G8/G9). The stdin *label* is not what decides it; the descriptor is.
4. **Invocation shapes that keep verification**: `./census.sh` (G1), a path containing `..` (G2), a
   symlink chain (G3), `sh`/POSIX mode (G4), `bash -o posix` (G5), shebang with exec bit (H1), a
   caller-held extra fd 10 on the same file (J1), and a caller pre-setting fd 255 on a decoy before
   `exec bash census.sh` (J2 — bash re-ducks its own script onto 255, so the real file is hashed).
   Retargeting the symlink to a decoy (G6) verifies the decoy honestly (`version=decoy-v99`).
   `source ./census.sh` from `bash -c` (P4) is `unverifiable` — correct, since no script descriptor exists.
5. **`--identity` with a closed stdout** exits **1** (X4) — inside the census exit map that is
   `DEGRADED`, so a mis-piped reader sees a plane verdict rather than a usage error.
6. **Argument handling**: `--identity x` exits 2 (`unknown argument: x`) and `--identity --identity`
   exits 2 (`--identity takes no other argument`) — the contract "takes no other argument (exit 2)" holds.

## 4. Proposed guard (proposal, not implemented — leaf seat)

The cheapest fix that catches all of §1(b.ii), §1(c), D3 and X1 — a startup signature compared at hash
time, so any same-inode change of the file is `unverifiable`:

```sh
# near SELF, at the top of the file (before any probe):
SELF_SIG=$(stat -Lc '%d:%i:%s:%y' -- "${SELF:-/dev/null}" 2>/dev/null || true)
# in census_identity(), inside `if [ -n "$fdp" ]` and after the four reads:
[ -n "$SELF_SIG" ] && [ "$(stat -Lc '%d:%i:%s:%y' -- "$self_real" 2>/dev/null || true)" = "$SELF_SIG" ] \
  || { fdp=''; }
```
(`stat` is already a dependency of the live census, so no new tool enters the identity path. It does
not stop an attacker who also restores `mtime` with `touch -r`; it does stop every honest race —
writers, editors, `git checkout`, an in-place package upgrade.)

A deterministic selftest case for the same hole (must inject **after** the `VERSION` line; injecting at
line 1 executes the new bytes and is legitimately honest, see §1(b.i)):

```sh
  { printf '%s\n' 'cat -- "${0%/*}/decoy" > "$0"'; cat -- "$SELF"; } > "$idd/edit.sh"
  sed "s/^VERSION='census-v2'\$/VERSION='decoy-v99'/" "$idd/edit.sh" > "$idd/edit.decoy"
  id_out=$(cd "$idd" && R46_EDIT=… "$BASH" ./edit.sh --identity 2>&1); id_rc=$?
  id_check 'identity: an in-place rewrite behind the read cursor prints unverifiable (R46-C1)' \
    'sha256=unverifiable md5=unverifiable bytes=unverifiable lines=unverifiable' "$id_out" "$id_rc"
```
with the edit line placed after the `VERSION='census-v2'` line of the copy (the two `sed`/`cat` steps
above are illustrative; the essential invariant is *same length, edit behind the cursor*).

## 5. Repo-state observation (not a judgement, not mine to fix)

While I probed, the lane moved: HEAD went `a4477049` → `b57740c2` → **`61e06740`** ("C1 identity
hardening from wave w1 — O_CLOEXEC + unique-descriptor rule (C1LabUlimit wrong-digest reproducer) …").
The census bytes at `b57740c2` are identical to `a4477049` (`sha256 d925839c…`), so the implementation
revision the declaration scores is unchanged by that commit. `61e06740` is the hardening commit
(census `sha256 ac4e38ff…`, 210762 bytes, `impl-61e06740.sh` / `census-61e06740.sh`).

**The defect reproduces unchanged on `61e06740`** — the added `O_CLOEXEC`/single-hit descriptor rule
does not address in-place edits, because the descriptor is the *right* descriptor; only its content
changed:

```
$ ./repro-p1-inplace-edit.sh /fast/scratch/…/repro/p1b impl-61e06740.sh
built census.sh bytes=210792 decoy bytes=210792 same-length=True
TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=4be94d3907ca7755794b728e3dc6ef6f23928fe044e13be39b76d4fdb656087d md5=44e319081c7554690afc7651e5a43255 bytes=210792 lines=3623 … verified=yes
rc=0
--- kernel saw:  53705 umask(077)                        = 022
--- file on disk: 454:VERSION='decoy-v99'   452:umask 000
```
Receipts `repro-p1-61e06740.out` (pinned to the commit) and `repro-p1-draft-worktree.out` (the same
content run from the worktree before it was committed).

## 6. What I did not do

* Did not implement any fix (leaf seat; report only). §4 is a proposal.
* Did not probe a bind mount over the lane path or `/proc` (mount(2) only inside a private user
  namespace; the read-only question was answered with an ro remount instead, receipt `readonly-fs.out`).
* Did not deterministically trigger a write landing *between* the identity's own five reads. The code
  re-checks only `sha` (`:3483-3486`), so `md5`, `bytes` and `lines` could be read from a different
  version than `sha256`; that is **[INFERENCE]** from the code, not a measured line.
* Did not run the counter on any revision other than `a4477049` (one run, PASS, receipt
  `counter-impl.json`), and no census selftest beyond that counter run and the probes' own runs.
* No packages installed or upgraded; no sudo; no host service, unit, sysfs, mount-outside-unshare or
  lane/git mutation. Scratch `/fast/scratch/hyaku/tsukuroi-r46/C1LabReplace/` removed at exit.

## 7. Receipts (`.ufo/waves/round-46/w1/C1LabReplace/`)

| file | content |
|---|---|
| `repro-p1-inplace-edit.sh`, `repro-p1-a4477049.out`, `repro-p1-61e06740.out`, `repro-p1-draft-worktree.out` | the defect, §1(b.ii) and §5: same-inode rewrite behind the cursor, with the `umask(077)` kernel witness |
| `repro-c2-truncate.sh`, `repro-c2-a4477049.out`, `repro-c2-draft-worktree.out` | the smallest dishonest line, §1(c.i): empty file, `sha256=e3b0c442…`, `verified=yes` |
| `probes2.log` | the (a)–(k) matrix: rename/unlink/length-changing overwrite/truncate variants, hardlink D1–D4, read-only F1 + strace F2, invocation shapes G1–G9, shebang H1, fd cases J1–J2, CLI K1–K2 |
| `probes3.log` | P4–P7: `source`, stripped env, exported-function and PATH shadowing of the digest tools |
| `probes4.log` | P0–P4: the same-length edit asymmetry (ahead = honest, behind = defect) and the identical-bytes control |
| `probes6.log` | X1/X1b external writer (in place = defect, rename = `unverifiable`), identity vs census timing |
| `counter-impl.json` | frozen counter PASS on `a4477049` (identity_ok…selftest_r46 = 1, selftest 160/160) |
| `readonly-fs.out` | read-only filesystem run (proved read-only by a failing write) |
| `trace-identity-f2.txt` | no write-mode or mutating syscall; five `O_RDONLY` opens of `/proc/<pid>/fd/255` |
| `trace-p0-umask.txt` | `umask(077)` on the pristine census (the witness used in §1(b.ii)) |
| `trace-reads-255.txt` | bash's 8192-byte reads on fd 255, one `lseek(255,0,SEEK_CUR)`, no rewind |
| `census-a4477049.sh`, `census-61e06740.sh` | the exact census bytes probed: the implementation revision (`sha256 d925839c…`) and the landed hardening commit (`sha256 ac4e38ff…`) |
