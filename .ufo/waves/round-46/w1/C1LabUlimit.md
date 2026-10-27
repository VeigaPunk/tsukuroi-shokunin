VERDICT: falsifies

# C1-9 — descriptor edge cases of `tools/tsukuroi-census.sh --identity` (round 46, wave w1)

Hypothesis under test (seat item): `--identity` prints the true digests with `verified=yes` for every ordinary
invocation of a regular census file, and `unverifiable` otherwise, **never a wrong digest**.

Result: every *ordinary* invocation is correct (13/13 probe kinds) and every documented refusal is correct
(4/4), but the "never a wrong digest" clause is false. A parent-held descriptor ≥ 10 that resolves to the same
path — combined with a relink of that path after bash has opened the script — makes the line report another
inode's bytes with `verified=yes`. Reproduced 15/15 with a plain racer and 1/1 deterministically with `BASH_ENV`.

Subject: `tools/tsukuroi-census.sh` at `a44770491eb5ca15ce9f8b3207309d1af683ffaf`, exported to scratch,
`sha256=d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa md5=db08a606ce128da3839457372e91e220
bytes=209208 lines=3598`. Host: bash 5.3.20(1)-release, kernel 7.2.11-arch1-1, `/bin/sh -> bash`,
default `ulimit -n` 524288. All fixtures under `/fast/scratch/hyaku/tsukuroi-r46/C1LabUlimit/` (removed).

## The code under probe

`tools/tsukuroi-census.sh:3471-3476` — the descriptor search: fd 255 first, then the whole `/proc/$$/fd/*` glob,
numeric-suffix and `-ge 10` filters, `[ -f ]`, and the test `readlink -- "$p" = "$self_real"` whose **first**
match wins (`fdp=$p; break`). `:3480-3486` — sha256, md5, bytes, lines, then sha256 again; `verified=yes` when
all five parse and the two sha256 reads agree. Nothing checks *which* descriptor this is; the evidence for
"the executed bytes" is only the path string the link carries.

## Ordinary invocations — all correct (receipts/probe_all.log)

| probe | command | output | verdict |
|---|---|---|---|
| baseline | `bash census.sh --identity` (cwd) | `sha256=d925839c… md5=db08a606… bytes=209208 lines=3598 … verified=yes` | correct |
| from `/` | `bash /abs/…/census.sh --identity` | same | correct |
| relative, other cwd | `cd /fast/scratch/hyaku/tsukuroi-r46 && bash C1LabUlimit/census.sh --identity` | same | correct |
| `./` form | `bash ./census.sh --identity` | same | correct |
| `sh` | `sh census.sh --identity` (`/bin/sh` is bash 5.3.20 here) | same | correct |
| `bash -x` | `bash -x census.sh --identity 2>/dev/null` | same | correct |
| `env -i` | `env -i bash census.sh --identity` (PATH and `BASH` unset, `$BASH` is a bash-internal) | same | correct |
| symlink to file | `bash lk/link.sh --identity` | same | correct |
| hard link | `bash hl/b.sh --identity` (same inode, other name) | same | correct |
| symlinked *directory* | `bash sd/link/c.sh --identity` | same | correct |
| path with spaces | `bash "sp/cen sus copy.sh" --identity` | same | correct |
| path with a newline | `bash "$(printf 'sp/census\nnl.sh')" --identity` | same | correct |
| PATH lookup | `cd / && PATH=$S/pth:$PATH bash census.sh --identity` | same (bash rewrites `BASH_SOURCE[0]` to the file found by `find_path_file`, `shell.c:1592-1597`) | correct |
| stdin | `bash -s -- --identity < census.sh` | `sha256=unverifiable … verified=no` | unverifiable (documented) |
| process substitution | `bash <(cat census.sh) --identity` | `sha256=unverifiable … verified=no` | unverifiable (documented) |

`--identity --selftest` → rc 2, `tsukuroi-census: --identity takes no other argument` + usage (correct). Identity
mode wrote nothing: directory entry count before=1 after=1 (`probe_all.sh` step 19).

## Where the script descriptor lands (probe_fd.sh = census + one prepended `FDSCAN` line; `ls -l /proc/$$/fd` from inside)

`bash -c 'ulimit -n N; exec bash probe_fd.sh --identity'`:

| `ulimit -n` | script fd | identity |
|---|---|---|
| 1024 | 255 | verified=yes, correct |
| 64 | 63 | verified=yes, correct |
| 20 | 19 | verified=yes, correct |
| 16 | 15 | verified=yes, correct |
| 12 | 11 | verified=yes, correct |
| 11 | 10 | verified=yes, correct (the `-ge 10` floor sits exactly on the edge) |
| 10 | 9 | verified=no, all four fields `unverifiable` |
| 8 | 7 | verified=no, all four fields `unverifiable` |

This matches S250 `general.c:681-698` (`nfds = getdtablesize()`, capped at `HIGH_FD_MAX` 256 per
`general.h:252`, then `for (nfds--; check_new && nfds > 3; nfds--)` down to the first free descriptor), and the
entry's claim that a limit below 11 makes the identity `unverifiable` is exactly what happens. Descriptor 255
pre-occupied: `exec 255</dev/null` → script lands on **254** (`FDSCAN: … 254=/…/probe_fd.sh 255=/dev/null`) and
the line is still correct; 255+254 occupied → still correct. A parent fd 10 on `/dev/null`, on a pipe, or on a
directory is skipped (`[ -f ]` false) and the line stays correct.

## The item's own scenario (rename over the path BEFORE exec) — correct

`exec 10<"$P"` (old inode), then `mv -f decoy P`, then `exec bash P --identity`: the parent's fd 10 reads
`…/P.sh (deleted)`, bash opens the *decoy* and executes it, and the line names the decoy
(`sha256=67d3aedd… bytes=209235`) — the bytes that actually ran. Correct.

## Falsification — a descriptor ≥10 makes the line name bytes that did not run

Both variants use the same `$SELF`-path design; the difference from the item's scenario is only *when* the path
is relinked: after bash opened the script instead of before exec.

### A. Deterministic (`BASH_ENV`, no timer), receipts/adversarial.log

Executed file `P.sh` = census copy, `sha256=d925839c…bytes=209208`. Decoy inode = census + a prepended
`printf "DECOY_EXECUTED\n" >&2` line, `sha256=c3dad0bc…bytes=209252`.

```
BASH_ENV:
  exec 10<"$R46_Q"
  trap '[ -n "$R46_ARMED" ] || { R46_ARMED=1; mv -f -- "$R46_Q" "$R46_P"; … }' DEBUG
```
Run (`R46_Q=… BASH_ENV=… bash P.sh --identity`):

```
FDLINKS:255=/…/fx3/P.sh (deleted) 10=/…/fx3/P.sh
TSUKUROI_CENSUS_IDENTITY: … sha256=c3dad0bc… bytes=209252 lines=3601 … verified=yes
```

`DECOY_EXECUTED` never printed, and the same decoy prints `DECOY_EXECUTED` plus its own `c3dad0bc…` line when it
is really the executed file (control in the receipt). So the executed bytes were `d925839c…` and the reported
bytes were `c3dad0bc…`, with `verified=yes`. **WRONG digest.**

Why it works: `run_startup_files()` (`S250 shell.c:722`) runs **before** `open_shell_script()`
(`S250 shell.c:779`), so `BASH_ENV` can create the extra descriptor, and the `DEBUG` trap fires on the first
script command — after `open()` (`shell.c:1586`) and `move_to_high_fd()` (`shell.c:1700`) but long before
`main` reaches `census_identity`. The relink leaves bash's script fd named `P.sh (deleted)` (no match) while the
inherited fd 10 now names `P.sh` (match).

### B. No `BASH_ENV`, plain racer, 15/15 WRONG

Parent: `exec 10<decoy; exec bash P --identity`. Racer: poll `/proc/$pid/fd/255` until it resolves to `P`, then
`mv -f decoy P`.

```
SUMMARY wrong=15 correct=0 unverifiable=0 executed_decoy=0 of 15
```

Every run printed `sha256=c3dad0bc… … verified=yes` for a process whose executed file was `d925839c…`
(`saw_fd255=1` in all 15: the relink happened after the script descriptor existed).

### Candidate fix (proposed, not verified here)

Discriminate by the flag bash sets and a shell redirection cannot: `SET_CLOSE_ON_EXEC (default_buffered_input)`
(`S250 shell.c:1703`, applied after `move_to_high_fd`, which `dup2`s and therefore clears any inherited
FD_CLOEXEC). Measured on this host:

```
fd255 flags: 02100000      # O_CLOEXEC | O_LARGEFILE
fd10  flags: 0100000       # O_LARGEFILE only (exec 10<…)
```

Requiring bit `02000000` in `/proc/$$/fdinfo/<n>` for the matched descriptor would reject both variants above
while keeping every ordinary case (the script fd always carries it). A weaker alternative — take the *highest*
matching descriptor, not the lexicographically first — does **not** fix either variant: in both, the only
matching descriptor left is the attacker's. I did not edit the census; the fix is for the owning seat.

## What I did not do

- No counter run (neither `score-census-identity-r46.py` nor the selftest): out of scope for a probe seat and
  the wave forbids build/lint/test runs; the C1 counter's `nowrite_ok`/`selftest_pass` fields are unverified here.
- `sh` probe only exercises bash in POSIX mode (`/bin/sh -> bash` on this host); a dash host is untested.
- Did not test patched-bash behaviour beyond 5.3.20; the pinned source is the bash-5.3 tag.
- Did not attempt a wrong digest with only *unprivileged in-script* means: the selftest's own `repl.sh` form
  (script relinks its own path) stays `unverifiable`, because then no descriptor matches — the parent-held
  descriptor is required.
- The adversarial cases need a cooperative parent (`BASH_ENV` or a racer); an ordinary operator invocation is
  unaffected, so the practical impact is low and the defect is in the safety *claim*, not in the common path.

## Receipts

- `.ufo/waves/round-46/w1/C1LabUlimit/probe_all.log` — full output of every probe (13 ordinary invocation kinds, 8-point
  ulimit sweep with fd scan, fd-255/254/10 parents, `BASH_ENV` variants, item scenario, stdin, process
  substitution, CLI, write check).
- `.ufo/waves/round-46/w1/C1LabUlimit/probe_all.sh` — the driver that produced it.
- `.ufo/waves/round-46/w1/C1LabUlimit/adversarial.log` — the deterministic `BASH_ENV` case with `FDLINKS`, the
  decoy-executed control, the 15-run racer summary, and the `fdinfo` flag comparison.
