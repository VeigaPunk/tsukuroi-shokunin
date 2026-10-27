VERDICT: defect-found

# C1-18 — safety review of `--identity` (round 46, C1, impl a4477049)

Probed file: `git show a44770491eb5ca15ce9f8b3207309d1af683ffaf:tools/tsukuroi-census.sh` —
sha256 `d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa`, 209 208 B, 3 598 lines.
Copied to `/fast/scratch/hyaku/tsukuroi-r46/C1SentSafety/census.sh` and probed there; the lane
worktree moved during the run (HEAD `b57740c2`, `tools/tsukuroi-census.sh` modified by another
seat), so every observation below is pinned to the `a4477049` blob, not the worktree. This seat
wrote no lane file, no fleet-root file, no PATH entry, ran no sudo, no service/sysfs/mount action;
bash 5.3.20(1), uid 1000.

**One reproducible defect (Low)**: `verified=yes` can name bytes the running bash did **not**
execute. Cause: the fd is matched by *path string* (`readlink` on the descriptor vs
`readlink -f "$SELF"`), and `$(…)` strips trailing newlines from both sides, so a script path
ending in a newline collapses onto a same-named neighbour. Everything else the item asks about
holds: no attacker bytes enter the line, no census-side hang on FIFO / socket / char device / huge
file inputs, no writes, and root handling is unchanged (there was never an EUID gate). A validated
one-line fix exists (§5).

## 1. What the code under review does (line numbers = a4477049)

- `tools/tsukuroi-census.sh:455` `SELF=${BASH_SOURCE[0]:-}` — empty for `bash -s`.
- `:3466-3491` `census_identity()`:
  - `:3469` `self_real=$(readlink -f -- "$SELF" 2>/dev/null || true)` — **command substitution
    strips every trailing newline** from the canonical path.
  - `:3470` `[ -n "$self_real" ] && [ -f "$self_real" ]` — the regular-file gate is applied to the
    *stripped* path.
  - `:3471-3475` scan `/proc/$$/fd/255` then `/proc/$$/fd/*`, keep fd ≥ 10 whose target is a
    regular file, and stop at the first descriptor whose `readlink` string **equals**
    `$self_real`. `readlink` here is *not* `-f`, so the comparison is a string equality, never an
    inode/device equality.
  - `:3479-3483` five reads of the matched descriptor: `sha256sum`, `md5sum`, `wc -c`, `wc -l`,
    `sha256sum` again (the second digest is the change-between-reads guard).
  - `:3484-3487` four fields must match `^[0-9a-f]{64}$`, `^[0-9a-f]{32}$`, `^[0-9]+$`,
    `^[0-9]+$`, and the two sha256 values must agree, else `unverifiable` / `verified=no`.
  - `:3489` the line is `version`/`sha256`/`md5`/`bytes`/`lines`/`planes`/`exit_map`/`verified`.
    **The script path is never printed.**
- `:3513-3519` `--identity` is dispatched before any host probe and requires `nargs == 1`
  (else exit 2).

## 2. Probe matrix (`/fast/scratch/hyaku/tsukuroi-r46/C1SentSafety/probes.sh`, log `probes-run1.log`)

| # | probe | observed | risk |
|---|---|---|---|
| P1 | `bash census.sh --identity` | one line, exit 0, `sha256=d925839c… bytes=209208 lines=3598 verified=yes` (matches `sha256sum`/`wc` of the file) | none |
| P2 | relative `./census.sh` | same fields, `verified=yes` | none |
| P3 | filename = `newline.sh\nTSUKUROI_CENSUS_IDENTITY: version=evil … verified=yes` | stdout was **one** line, the real identity; `forged_line_present=0` — the path is never echoed, so a newline in the path injects nothing | none |
| P4 | filename `we*ird[1]?%s%d%n\x.sh` | `verified=yes`, correct digests — every use of `$SELF` is quoted and `readlink` is called with `--` | none |
| P5 | `-lead.sh`, via absolute, `bash -- -lead.sh`, `./-lead.sh` | all `verified=yes`, correct digests | none |
| P6 | `trail.sh` + `"\n"` (no neighbour) | `readlink -f` printed the path **with** the newline; identity printed `unverifiable … verified=no` although bash executed that file | false negative, see §4 |
| P7 | exploited: `amb.sh\n` executed (inode 76051992, 209208 B) + decoy `amb.sh` (inode 76051994, 209247 B) + `255<amb.sh` | `sha256=9dd14d4c… bytes=209247 lines=3599 verified=yes` — **the decoy's digest, with `verified=yes`** | **defect, §3** |
| P7b | same files, fd 10 on the decoy, fd 255 free | `sha256=d925839c… bytes=209208 verified=yes` (fd 255 wins, correct) | none |
| P7c | same files, only `255<amb.sh` | decoy digest with `verified=yes` — no fd ≥ 10 is needed | defect, §3 |
| P8 | `PATH=fakebin:…` with shadowing `sha256sum`/`md5sum`/`wc` | `sha256=1111… md5=2222… bytes=999999 lines=4242 verified=yes` for a 209 208 B file | note, §6.1 |
| P9 | `VERSION=evil CENSUS_PLANES=evil=x TSUKUROI_ROOT_DIR=/no/such` and `env -i` | line unchanged — all fields assigned unconditionally, no env influence | none |
| P10 | inherited fd 30 = unix socket, fd 31 = FIFO, fd 10 = `/etc/hostname` | all skipped, `verified=yes` with the script's true digests, no hang | none — the `[ -f ]` gate holds |
| P11 | `--identity` with stdin `/dev/zero`, `/etc/hostname`, and `0<&-` | `verified=yes` in all three: identity mode never reads stdin | none |
| P12 | `bash <(cat census.sh) --identity` and `bash -s -- --identity < census.sh` | `unverifiable … verified=no` | none |
| P13 | `bash -c 'source census.sh --identity'` | `unverifiable … verified=no` (bash closes the sourced file) | none |
| P14 | FIFO at the script path, writer feeds the census | `unverifiable … verified=no`, exit 0 | none |
| P15 | FIFO at the script path, writer holds it open with zero bytes | `rc=124` (timeout), zero output: **bash** blocks opening the FIFO before any census code runs | not a census defect |
| P16 | symlink to `/dev/zero` at the script path | `rc=126`, `…zero.sh: cannot execute binary file`; identity never runs | not a census defect |
| P17 | symlink to the FIFO, writer present | `unverifiable … verified=no` | none |
| P18 | `/dev/null` as script; symlink loop as script | no output, `rc=0`; `rc=126 Too many levels of symbolic links` | none |
| P19 | 1 KiB / 64 MiB trailing comment blocks (`probes-run1.log`): `--identity` 24 / 164 ms on 1.2 MB / 67 MB; 4 GiB trailing hole bash never reads (`sparse4g.log`): `--identity` 10 676 ms vs `--help` 6 ms | cost linear in file size, 5 passes | note, §6.2 |
| P20 | `--identity` in an empty cwd; `strace -f -e trace=%file,write,unlink,rename,mkdir` | 0 files left; trace: writes only to fd 1, `openat` only of `/dev/tty` (bash) and `/dev/null` (from the `2>/dev/null` redirects); no `O_CREAT` on a real path, no `unlink`/`rename`/`mkdir` | none |
| P21 | uid/EUID | line carries no uid field (`grep -c uid` on it = 0); `git diff 2042117c a4477049 -- tools/tsukuroi-census.sh` has 0 `EUID`/`id -u` lines | see §7 |
| P24 | `bash -c '( . census.sh --identity )'` | `unverifiable` — `$$` inside a subshell is the outer pid and that shell holds no fd on the file | none |
| P25 | `bash -c 'exec 10<census.sh; ( . census.sh --identity )'` | `verified=yes`, correct bytes — the scanned descriptor belongs to the *outer* shell, not to bash's script fd | note, §6.4 |
| fix-validation | `bash census-fix.sh --identity --selftest` (patched copy) | `rc=2` | none |

No probe left a process behind (`pgrep -af C1SentSafety` empty after the FIFO runs).

## 3. Defect D46-C1-18a — `verified=yes` can name bytes bash did not execute

**Severity: Low. Contract violation, reproducible, not a privilege escalation.**

The C1 declaration promises the digests are "read through the script descriptor bash holds …
only when it resolves to the invoked file". `:3469` + `:3475` compare **path strings** after
`$(…)` has stripped trailing newlines, so `X\n` and `X` collapse to the same string, and any
regular file named `X` satisfies both `[ -f "$self_real" ]` (:3470) and the equality (:3475).

Reproduction (all paths under `/fast/scratch/hyaku/tsukuroi-r46/C1SentSafety/`; `C` = the
`a4477049` census bytes):

```
cp C 'amb.sh'$'\n'                       # executed file: inode 76051992, 209208 B
{ cat C; printf '# decoy marker: not the executed bytes\n'; } > amb.sh   # neighbour: inode 76051994, 209247 B
bash 'amb.sh'$'\n' --identity 255<amb.sh
```
observed:
```
TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=9dd14d4c9a165912c52124469cae9c7e08cae99ac0d892dbc0f318c948e83d52 md5=d4da7de2d74cf1ad0015aa71271156bd bytes=209247 lines=3599 … verified=yes
```
`9dd14d4c…` / `bytes=209247` are the **decoy's** values; the file bash executed was
`sha256=d925839c… bytes=209208`. Control on the same two files with fd 255 left free prints the
executed file's digests (P7b), so the trigger is the first loop entry `:3471`
(`/proc/$$/fd/255`) or any inherited fd ≥ 10 whose target is the neighbour.

**Exploit path / trust boundary.** Whoever supplies the invocation supplies the path and the
descriptors — and that same party could print any line. The line's value is to a *reader* who did
not run it: `verified=yes` is meant to be evidence that the bytes hashed are the bytes executed.
After this probe it is evidence only if the path is free of a trailing newline. Practical reach is
narrow (a script path ending in `\n`, which only the invoker can create), which is why this is
Low and not a kill: the counted predicate is untouched (the counter uses ordinary paths, P1/P7b).

**Impact.** Forged provenance: a relayed `verified=yes` line can attest a file that was never
executed. It also means the mode's guarantee is a property of the *string* it was handed, not of
the descriptor — the exact confusion the "never a path on trust" comment (`:3462`) says the
mode avoids.

## 4. Defect D46-C1-18b — same cause, safe direction: a legitimate newline-terminated path is `unverifiable`

`bash 'trail.sh'$'\n' --identity` on a plain copy of the census prints
`sha256=unverifiable … verified=no` (P6), because the stripped `self_real` is `…/trail.sh`, which
does not exist, so `:3470` fails even though `readlink` itself printed the path with its newline
(`readlink -f prints: [/…/trail.sh]`). False negative, not a false positive — but the same
one-line fix removes it (§5). Note the asymmetry that *is* the defect: the `-f` test runs on the
stripped path, while the executed file is the unstripped one.

## 5. Smallest remediation — validated, not applied (this seat has review scope only)

Compare by device+inode with bash's builtin `test -ef` (follows symlinks, no external tool, no
newline stripping), and test `-f`/`-ef` against `$SELF` itself:

```diff
--- a/tools/tsukuroi-census.sh
+++ b/tools/tsukuroi-census.sh
@@ -3464,15 +3464,14 @@
 census_identity() {
-  local self_real fdp='' p sha md5 bytes lines sha2
+  local fdp='' p sha md5 bytes lines sha2
   local f_sha=unverifiable f_md5=unverifiable f_bytes=unverifiable f_lines=unverifiable verified=no
-  self_real=$(readlink -f -- "$SELF" 2>/dev/null || true)
-  if [ -n "$self_real" ] && [ -f "$self_real" ]; then
+  if [ -n "$SELF" ] && [ -f "$SELF" ]; then
     for p in "/proc/$$/fd/255" /proc/$$/fd/*; do
       case "${p##*/}" in '' | *[!0-9]*) continue ;; esac
       [ "${p##*/}" -ge 10 ] || continue
       [ -f "$p" ] || continue
-      if [ "$(readlink -- "$p" 2>/dev/null || true)" = "$self_real" ]; then fdp=$p; break; fi
+      if [ "$p" -ef "$SELF" ]; then fdp=$p; break; fi
     done
   fi
 ```

Validated on a scratch copy (`fix-validation.log`, `fix-validation2.log`, patch in
`C1SentSafety/proposed-fix.patch`): baseline/copy/symlink/stdin/replaced-after-open all behave as
the four `(R46-C1)` selftest cases require (baseline `verified=yes` with its own bytes, symlink
reports the target, stdin `unverifiable`, replaced-after-open `unverifiable`); `--identity
--selftest` still exits 2; and on fixtures rebuilt from the patched bytes
- `amb-fix.sh\n` + decoy + `255<decoy` → `sha256=819734bf… bytes=209090 verified=yes` = the
  **executed** file (the false positive is gone; `10<decoy` likewise);
- `trail-fix.sh\n` with no neighbour → `verified=yes` (the false negative is gone);
- `trail-fix.sh\n` + decoy + `255<decoy` → executed file.
It also drops one PATH dependency (`readlink`) from the identity path.

## 6. Notes (informational; no change required for the claim)

1. **Digest tools come from `PATH`.** Shadowing `sha256sum`/`md5sum`/`wc` yields
   `sha256=1111… md5=2222… bytes=999999 lines=4242 verified=yes` (P8). A party who controls `PATH`
   can run code anyway, so this is not a new capability — but it means the line is not evidence
   *against* a hostile environment. The frozen counter pins `PATH=/usr/bin:/bin`
   (`score-census-identity-r46.py`, `env = {...}`), so the PASS verdict is unaffected. Optional
   hardening: absolute `/usr/bin/{sha256sum,md5sum,wc}` or a `command -v` location check.
2. **Cost is 5 full reads of the executed file, unbounded by how much bash executes.**
   `:3479-3483` reads the descriptor five times (`sha256sum`, `md5sum`, `wc -c`, `wc -l`,
   `sha256sum` again). Measured (`probes-run1.log` P19, `sparse4g.log`): 209 KB→18 ms, 1.2 MB→24 ms,
   67 MB→164 ms; a 4 GiB script whose `main` exits at byte 209 208 (`census + '\n' + 4 GiB hole +
   '\n'`) took `--identity` **10 676 ms** and printed `bytes=4294967297 verified=yes`, while
   `--help` on the same file took **6 ms** — bash reads only up to `main "$@"`, and the identity
   then re-reads everything ~5× (21.5 GB at ~2 GB/s here). The caller chose the file, so this is
   not a new capability, but it is size-proportional work with no cap; `wc -c` is redundant with
   `stat -Lc %s` on the same descriptor (~one pass saved). The second sha256 is a deliberate
   TOCTOU guard and should stay.
3. **Hangs exist only inside bash, never inside `census_identity`.** P15 (FIFO with a silent
   writer) and P16 (`/dev/zero`) block/fail at script open, before `--identity` runs; the census's
   own inputs are one regular descriptor, `readlink`, `stat`, and a `/proc` glob — none of which can
   block indefinitely. FIFO/socket/char-device *descriptors* are excluded by `[ -f ]` (:3474),
   and a FIFO/char device *at the script path* ends in `unverifiable` (P14/P17) rather than in a
   read of the device.
4. **`$$` semantics when sourced.** In a subshell `$$` is the outer shell's pid, so a sourced
   census scans the *outer* process's descriptors; P25 shows `verified=yes` when that shell happens
   to hold fd 10 on the file. Correct bytes in the tested case, but it confirms the scan is not
   tied to "the descriptor bash executes from" — the same weak spot as §3, and `-ef "$SELF"` narrows
   it to the right inode in every case probed.
5. **stderr can still carry caller bytes**, pre-existing and outside `--identity`: the unknown
   argument branch prints `printf '… unknown argument: %s\n' "$1"`, so a newline-bearing argument
   forges an extra *stderr* line (not the identity line, which prints nothing but its eight
   constant/regex-gated fields).

## 7. Root / EUID 0

There is no EUID gate at base or at impl: `grep -n EUID` on the `a4477049` file returns 6 hits,
all `root_euid=$EUID` annotations in the packages root-directory arm (`:884,906,915,926,931,941`),
which `--identity` never reaches (`:3513-3519` returns before any probe). The base/impl diff
touches only the `SELF` assignment (`:455`), the usage text, one comment, the selftest block and `main`
(`git diff` hunks `@@ -452`, `@@ -591`, `@@ -602`, `@@ -3381`, `@@ -3405`; 117 insertions,
4 deletions; 0 lines mentioning `EUID`/`id -u`). So "refuse/handle root as before" = unchanged,
and the identity line itself has no uid-dependent field (P21). **I did not execute anything as
root** (no sudo permitted), so the uid-0 *run* is reasoned from the diff and the absence of any
uid read in the path, not observed.

## 8. Not done

- No run as uid 0 (prohibited); no counter run (other seats own the counted verdicts; the identity
  predicate's four fixtures were reproduced here by hand instead).
- No multi-GB non-sparse file (only 67 MB ordinary + 4 GiB sparse); no FUSE/NFS/hung-mount path
  (the only way `readlink -f`/`stat` could block — needs control of a mount, i.e. more than the
  unprivileged attacker modelled here).
- No remediation applied: the lane is read-only for this seat; §5 is a proposal only.

## 9. Receipts

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-46/w1/C1SentSafety/`:
`probes.sh`, `probes-run1.log` (P0-P21), `final-probes.log` (P16 text, P22-P26),
`strace.txt` (P20 trace), `sparse4g.log` (4 GiB trailing-hole timing),
`fix-validation.log`, `fix-validation2.log`, `proposed-fix.patch`,
`fixtures-listing.txt`, `provenance.txt` (probed blob sha256, bash version, uid, lane HEAD).
No tool was installed or upgraded for this seat. Scratch
`/fast/scratch/hyaku/tsukuroi-r46/C1SentSafety/` was removed after the receipts were copied.
