VERDICT: supports

# SRC-N2 — GNU Bash manual, Redirections + exec: fd numbers ≥ 10 (live re-open, opener of record)

## 1. Fetch record

- URL: https://www.gnu.org/software/bash/manual/bash.html
- Access date (UTC): 2026-10-28
- Fetch: `curl -fsSL --max-time 60 -o bash.html https://www.gnu.org/software/bash/manual/bash.html` → success, 1,040,954 bytes (receipt: `w2/SScoutBashRedir/bash-manual-2026-10-28.html`; commands: `w2/SScoutBashRedir/commands.txt`)
- sha256 of fetched bytes: `78d0eefbe60cfe7345ffdafede7294f055b04e53bd520360ff699b24f81e2b4b`
- Document identity: `<title>Bash Reference Manual</title>`; "This is Edition 5.3, last updated 18 May 2025," (HTML line 9 and line 84). Host bash is `GNU bash, version 5.3.20(1)-release`, matching the edition.
- Freshness note: the same URL timed out from this host on 2026-10-27 (`.ufo/waves/round-46/w1/SrcGateNew.md:53`, `corpus/lessons/round-46.md:46`); this round's fetch is the first successful open of this URL in the lane.

## 2. Pinned-snapshot comparison

No pinned snapshot of `bash.html` exists anywhere in the lane or `.ufo`: `find .ufo -name '*bash*'` shows only S175's `bash.1` roff source (`.ufo/waves/round-32/w1/ScribeSrcBashEnv/bash.1`, `.../w2/RevSourcesRows/S175-bash.1`) and round-46's `frozen/src/{shell.c,general.c,general.h}` — no HTML manual bytes were ever obtained, so a byte-level `cmp` is impossible and there is no prior digest to compare against.

Byte-equivalent cross-check: S175's pinned `bash.1` (GNU Bash 5.3 doc/bash.1 at tag `bash-5.3`, sha256 `23f7bd15…d1971`) carries the identical caveat sentence — "Redirections using file descriptors greater than 9 should be used with care, as they may conflict with file descriptors the shell uses internally." (`S175-bash.1:4763-4765`) — and the identical `{varname}` paragraph (`S175-bash.1:4665-4680`) as the live HTML (§3 below). The live page is the same content, so the pinned roff corroborates the fetch. `man bash` is present on this host.

## 3. Located sentences (verbatim, ≤25 words; line numbers in the fetched HTML)

(a) Explicit fd number ≥ 10 via `exec` — grammar at `bash.html:3884`: `[n]<word`, with `bash.html:3881-3883`: "Redirecting input opens the file whose name results from the expansion of word for reading on file descriptor n". No upper bound on `n` is stated; the only fd>9 text is the caveat in (c). `exec`-only-redirections at `bash.html:3758-3759`: "When used with the `exec` builtin, redirections modify file handles in the current shell execution environment." and `bash.html:4863-4864`: "If command is not specified, redirections may be used to affect the current shell environment."

(b) `{varname}` allocation — `bash.html:3771-3773`: "the shell allocates a file descriptor greater than or equal to 10 and assigns it to {varname}." And for the close form `exec {var}<&-` used by the selftest case: `bash.html:3774-3778`: "If {varname} precedes `>&-` or `<&-`, the value of varname defines the file descriptor to close."

(c) The caveat — `bash.html:3859-3861`: "Redirections using file descriptors greater than 9 should be used with care, as they may conflict with file descriptors the shell uses internally."

## 4. Are fds 240–249 safe from bash internals?

From the page itself: the caveat is generic — it warns, but names no number, so the page alone does not clear 240-249. The relevant internal descriptor is the script descriptor: bash reads the script it executes from a high fd, documented in this lane by S250 (`SOURCES.md` row S250): "bash opens the script and moves it to the highest free descriptor below 256 (close-on-exec)". Empirically that is fd 255 on this host (`bash w.sh` → `[ -e /proc/self/fd/255 ]` true in-process, absent from `ls /proc/self/fd/` in exec'd children — close-on-exec confirmed; transcript `w2/SScoutBashRedir/fd-tests-transcript.txt`). The resolver's band 240-249 sits below that and above the `{var}` allocation floor of 10.

Remaining conflict paths, measured:

- An `exec N<file` on an already-occupied N silently repoints it — the manual's real hazard. The resolver guards: `for fdn in 240..249; do [ -e "/proc/self/fd/$fdn" ] || break; done; [ -e ... ] && return 1` (`tools/tsukuroi-census.sh:2079-2083` at the freeze) skips every occupied number, including a script fd that landed in-band (e.g. when 250-255 are inherited occupied).
- `{var}`-allocation and other transient internal fds start at the lowest free ≥ 10 (empirical: `exec {v}</etc/hostname` → `v=10`; `v=10 w=11` for two) and reach 240 only if ~230 lower fds are already held — outside the selftest's usage.
- `exec 255<&-` mid-script does not fault the running script on this host (`t.sh` → `after-close-255 ok`, rc=0), but the resolver never touches 255.

Assessment: 240-249 is not guaranteed safe by the manual alone — the caveat applies — but the only documented high internal descriptor is the script fd (≤255, empirically 255, close-on-exec), and the resolver's `/proc/self/fd/<n>` occupancy probe makes the band collision-safe in the observed implementation. Support for `exec ${fdn}<"$base"` (frozen blob lines 2083-2086) and `exec {ST_BASE_FD}<&-` / `exec {r48_fd}<&-` (lines 3551, 3549) is direct.

## 5. Empirical corroboration (all in scratch `/fast/scratch/hyaku/tsukuroi-r48/SScoutBashRedir/fdtest`, transcript in wave dir)

- `bash -c 'exec 240</etc/hostname; ls -l /proc/self/fd/240; exec 240<&-'` → `240 -> /etc/hostname`, `closed-ok` (explicit fd ≥ 10 open/close).
- `bash -c 'exec {v}</etc/hostname; echo $v; exec {v}<&-'` → `v=10` (lowest free ≥ 10, per manual).
- `bash -c 'exec 240<DIR; ls /proc/self/fd/240/sub'` → lists `file` (a directory opened `O_RDONLY` on 240 resolves through the proc alias — the exact mechanism `ST_BASE_DIR=/proc/self/fd/$fdn` relies on).
- `bash w.sh` (script that tests itself) → `fd255: present in-process`; `fdinfo/255` absent in children; `exec 255<&-` inside a script → rc=0.
- Holding 240-254 then running a script → the script fd still lands at 255, invisible to exec'd children.

## 6. URL registration check

`git grep "gnu.org/software/bash" ae99f021` — hits are `shell.c`'s home-page printf, round-46 fetch-failure records, and this item's spec text; no `SOURCES.md` row registers `bash.html`. Closest existing row: S175 = the `doc/bash.1` roff *source* of the same manual (distinct artifact: tagged roff vs rendered HTML page; not a duplicate). Also absent: the 53 staged assimilation ids S200-S252 collide only by number, not by URL.

## 7. Draft SOURCES row (11-column schema `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`)

Provisional id `S253` (next free after S252; note SRC-N1 may also draft S253 — the L1 renumbers one):

```
| S253 | GNU Bash Reference Manual, Redirections — https://www.gnu.org/software/bash/manual/bash.html | docs | A | Explicit fd numbers in redirections, `{varname}` descriptor allocation, and the fd>9 caveat behind the census selftest's 240-249 fd-alias band | Edition 5.3 (18 May 2025); fetched 2026-10-28, sha256 78d0eefbe60cfe7345ffdafede7294f055b04e53bd520360ff699b24f81e2b4b; raw HTML lines 3881-3884, 3771-3778, 3859-3861, 4863-4864 | `[n]<word` opens word on descriptor n with exec; {varname} allocates a descriptor ≥ 10 and `exec {v}<&-` closes the descriptor named by the variable's value; descriptors above 9 "may conflict with file descriptors the shell uses internally" — the shell's own script fd sits at the highest free descriptor below 256 (S250) | mined | 2026-10-28 | on-release | corpus/lessons/round-48.md |
```

`used-by` mirrors S252 (`corpus/lessons/round-47.md`); the exact consumer file is the L1's round-48 lesson — adjust at integration if it lands elsewhere.

## 8. Caveats and what I did not do

- The `>`9 caveat is verbatim; nothing in the page binds 255. The 255 answer comes from S250 (already admitted, pinned) plus this host's empirical check — both cited, not the fetched page.
- I did not re-run the census selftest or the C1 counter (out of scope, one-selftest cost discipline).
- No prior `bash.html` digest exists to diff against; the equivalence check used pinned S175 `bash.1` text instead.
