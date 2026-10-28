VERDICT: supports

# R49LabFd — C3-B8: real descriptor-band exhaustion probe

Bytes under test: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 55c07cd3f8bff2e12117c34d57b4c618de74d85c:tools/tsukuroi-census.sh`
→ sha256 `c66144d73da1ac376cfe756eab3a60340e18bce91d60abe24c444408b99a2e75` (`receipts/census-frozen.sha256`).
All line numbers below are lines of that blob. Lane working tree never opened for reading of content and never written;
the lane was only `git show`-ed.

Host: bash 5.3.20(1)-release, `ulimit -n` soft = hard = **524288**, `/proc/sys/fs/file-max` = 9223372036854775807, 32 CPUs.

## 1. Baseline descriptors actually available

```
bash -c 'ls /proc/self/fd | sort -n'   →  0 1 2 3 16 18
                                          band free   (no 240..249 present)
```
16/18 are `/dev/pts/0` descriptors inherited from the seat harness; 3 is the harness's
`/proc/<pid>/fd` dir link. Nothing in 240..249 is held, so the production band is fully free
on this host in a plain `bash -c` (probe A step 0).

## 2. Does bash permit `exec 240</dev/null`? Yes — and the whole band

```
exec 238..249 </dev/null  →  ok for every one of the twelve (probe A step 1)
/proc/self/fd after: 0 1 2 3 16 18 238 239 240 241 242 243 244 245 246 247 248 249
238 -> /dev/null … 249 -> /dev/null
```
Re-executing an already-held slot re-points it silently (`exec 240</dev/null` → ok,
`240 -> /dev/null`, probe A step 2), i.e. the resolver's `[ -e /proc/self/fd/$fdn ]` test,
not bash, is what protects a slot.

Ceiling measured: `exec 524287</dev/null` → ok; `exec 524288</dev/null`,
`700000`, `1000000`, `2147483646` → all refused. Bash's usable fd space is
`RLIMIT_NOFILE-1`, far above 249.

## 3. Error text when bash refuses a descriptor number

Two distinct failure texts, both captured:

| condition | stderr |
|---|---|
| fd number ≥ `RLIMIT_NOFILE` (slots free) — `ulimit -n 200; exec 240</dev/null` | `bash: line 1: 240: Bad file descriptor` |
| `RLIMIT_NOFILE` exhausted (EMFILE) — `ulimit -n 10`, fds 3..9 held | `bash: redirection error: cannot duplicate fd: Too many open files` then `bash: line 1: /dev/null: Too many open files` |

## 4. Does `ulimit -n` allow the band at all? Yes, with 523,000+ to spare

Soft = hard = 524288 ⇒ descriptors 240..249 are all creatable (§2). The band does **not**
depend on raising a limit.

## 5. The exhaustion path, executed — frozen resolver, verbatim, band unset

Probe A runs a copy of `selftest_base_dir()`; a normalized diff of the copy against the frozen
function (comments/whitespace stripped) leaves only the `ST_BASE_DIR=; ST_BASE_FD=; ST_BASE_ERR=`
one-line vs three-line assignment — semantically identical. To remove even that, the decisive
run `eval`s the frozen function straight out of the extracted blob
(`eval "$(sed -n '/^selftest_base_dir() {/,/^}$/p' census.frozen.sh)"`, function sha256
`4e23d81b44202f223016b57d8a56b6196f50152d3fcb90bde8eb210e812336ad`) after holding 238..249:

```
held: 0 1 2 3 16 18 238 239 240 241 242 243 244 245 246 247 248 249
SELFTEST_FD_BAND=<unset>          # production band 240..249
frozen resolver rc=1 err=fd-band dir=<empty> fd=<empty>
```
`selftest_base_dir()` (`tools/tsukuroi-census.sh`:2082 band default, :2089 first-free scan,
:2091 `ST_BASE_ERR=fd-band`, :2092 `alias-open`, :2096 `alias-not-dir`) selects the first free
slot and fails **only** when the whole band is occupied — exactly what was observed. Releasing
248/249 with 240..247 still held: `rc=0 ST_BASE_FD=248`,
`/proc/self/fd/248 -> …/dirty tmpdir`, `readlink -f` lands in the dirty TMPDIR (probe A step 4),
so the first-free selection and the in-TMPDIR alias both work.

End-to-end through the real script, 240..249 held by the caller, dirty TMPDIR:

```
rc=1
stdout: []
stderr: [selftest: fd band 240 241 242 243 244 245 246 247 248 249 exhausted (every descriptor
         already open), cannot alias TMPDIR </fast/scratch/…/dirty tmpdir>; no /tmp fallback (R49-C3)]
```
(`receipts/exhausted-band-e2e.stderr`, `.stdout` is 0 bytes). This is the print site at
`tools/tsukuroi-census.sh`:2115-2116; it fires *before* `mktemp` (:2125), so no fixture tree is
built and no `/tmp` fallback is taken — the exhaustion contract of C3 is real, not just a string.

Independent re-check of the C3 text legs on the frozen blob: stale comment
`builds a /tmp fixture tree` → **0** occurrences; `fd band` → 6; `ST_BASE_ERR=fd-band` → 2;
`fd band %s exhausted` → 1.

## 6. Can the census's own fixtures ever exhaust the band? No. Peak is 8 descriptors

`sampler.py` ran `bash census.frozen.sh --selftest` (clean TMPDIR under my scratch) and sampled
`/proc/<pid>/fd` for the census process and every descendant (~10 ms cadence, 2,620 process
samples, 80.4 s wall):

```
selftest_rc 0   summary: TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)
peak_fds_one_process 8
peak_cmd  /bin/bash …/census.frozen.sh
peak_fd_list [0, 1, 2, 3, 4, 10, 63, 255]
fd_numbers_ge_100_seen [255]
```
255 is bash's own script descriptor (the one `--identity` reads, comment :2074/:2130); 10 is the
fixture band the comment at :2070 describes; nothing else is high. The R49-C3 case adds exactly
two more (`exec 240<&0`, `exec 241<&0`, :3581, released at :3596-3597), so the selftest's worst
self-inflicted high-water mark is **≤ 10 of 524,288**, i.e. 230 idle slots below the band's first
member. Honest bound: the 10 ms sampler can miss sub-10 ms windows, so the 240/241 hold itself was
not sampled — it is counted analytically from the two `exec` lines, which is exact.

Normal `--selftest` at the freeze therefore **cannot** reach `fd band … exhausted`; only an
inherited/held band can, which is precisely the case C3 now names.

## 7. Caveats that size the diagnostic (not falsifications of C3)

1. **A caller holding 240 or 241 turns the selftest red, not green.** With only 240/241 held by
   the caller (band otherwise free, clean TMPDIR), the full run ends
   `FAIL selftest: could not reserve the 240/241 probe descriptors for the fd-band case (R49-C3)` /
   `TSUKUROI_CENSUS_SELFTEST: FAIL (167 cases, 166 passed, 1 failed)`, rc 1
   (`receipts/selftest-with-240-241-held.grep`; held.out:169). The band is *not* exhausted here —
   the proving case just cannot reserve its two fixed numbers (:3580-3581 guard,
   :3599 `bad` branch). Suggest, if the L1 wants it hardened: pick the first two free band members
   and set `SELFTEST_FD_BAND` to those two instead of the hard-wired 240/241.
2. **`RLIMIT_NOFILE` < 241 never shows the named message.** `ulimit -n 200`, band free, dirty
   TMPDIR: the scan finds 240 free → `exec 240<…` fails with
   `bash: line 1: 240: Bad file descriptor` → `ST_BASE_ERR=alias-open`, and the script prints the
   generic `selftest: TMPDIR <…> cannot host the fixture tree (alias-open; no /tmp fallback, R48-C2)`.
   That class is honest (it is not exhaustion) but is unnamed as a rlimit problem; a distinct
   class would say more.
3. **The resolver never widens past 240..249** even when lower descriptors are free — deliberate
   per :2070-2076 (auto-allocated fds start at 10 and fixtures `exec 10<…`), so a fully occupied
   band is a hard failure with no secondary band. The wording "every descriptor already open"
   means the band members, which the message prints explicitly.
4. Message-class note: the diagnostic interpolates `${SELFTEST_FD_BAND:-…}` so a narrowed band is
   reported as narrowed, and it reports `TMPDIR` unquoted inside `<>`.

## 8. What I did not do

- Did not run `tools/check-fd-band-r49.py` (that counter belongs to the counted C3 seat; my item is
  the bounded bash probe). I did independently observe its `band_ok` facts: 167/167 PASS and a
  `PASS selftest: exhausted fd band fails the base resolver and names err=fd-band (R49-C3)` line.
- Did not measure production-mode (non-`--selftest`) peak descriptors, and did not re-run the
  selftest under a dirty outer TMPDIR through the real script (the alias path was exercised
  directly in §5 instead).
- No lane write, no git/jj mutation anywhere, no `/tmp` write; `/tmp` observed only.

## 9. Receipts and scratch

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-49/w1/R49LabFd/`:
`probe-a-fd-band-exhaustion.out`, `probe_a.sh`, `sampler.py` (prints its JSON to stdout),
`exhausted-band-e2e.stderr`, `exhausted-band-e2e.stdout` (0 bytes),
`selftest-with-240-241-held.grep`, `census-frozen.sha256`.
Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49LabFd/` removed at the end of the seat.
No tools installed (nothing needed: bash + python3 + /proc were sufficient).
