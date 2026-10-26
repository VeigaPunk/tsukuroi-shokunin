VERDICT: defect-found

# C1-14 — adversarial review of the STORAGE line grammar (census @52ffd65)

Seat C1SentGrammar, round 38. Measured object: `probe_storage_arm` in
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh` at
52ffd65f868431f021b8615ab281efd87195eac6. Pinned bytes verified:
`git show 52ffd65:tools/tsukuroi-census.sh | sha256sum` =
`8e0084f67ad4783a980d5c2eaba453f51f1fc5d75408a1c9021a7249ac9aba1c`, equal to the
working-tree blob (`sha256sum tools/tsukuroi-census.sh`), and `git diff 52ffd65..HEAD --
tools/tsukuroi-census.sh` is empty.

Method: the pinned blob was copied out to scratch, each fixture tree built under
`/fast/scratch/hyaku/tsukuroi-r38/C1SentGrammar/cases/<case>/` and the census run as
`env -i PATH=/usr/bin:/bin LC_ALL=C TSUKUROI_BTRFS_SYSFS=<tree> bash census-52ffd65.sh`
(host probes are read-only; nothing was written outside scratch and the seat dir). Receipts:
`.ufo/waves/round-38/w1/C1SentGrammar/receipts.txt` (every case, STORAGE/PLANE/HANDOFF/rollup
lines with line numbers and counts) and `.ufo/waves/round-38/w1/C1SentGrammar/harness.sh`
(the reproducible driver). No tool was installed or upgraded.

## 1. The injection surface is one token: the devinfo entry basename

`probe_storage_arm` (1848-1887) validates the *filesystem* name against a lowercase-UUID
regex (1850, 1856) but echoes the *device* entry basename raw into `detail` at three places:

- 1861 `detail+="$fs8:${dev##*/}:unreadable,"`
- 1875 `detail+="$fs8:${dev##*/}:malformed,"`
- 1877 `nz=...; detail+=$ddet` where `ddet` is built as `"$fs8:${dev##*/}:$k=$v,"`

`$k` is whitelisted (`$keys`, 1851) and `$v` must match `^[0-9]+$` (1869), so the counter
*k/v* pair is safe. `$fs8` is safe (regex-constrained, see §3). The devid is not constrained
at all: `for dev in "$fsd"/devinfo/*` (1857) accepts any basename the tree contains.
The line is then composed at 1884-1885 and printed at 3008, **before** the rollup at 3018.

## 2. Concrete failing inputs (all executed)

### F1 — newline in a devid ⇒ arbitrary census lines (severity: contract break, forged pass)

`devinfo/$'1\nTSUKUROI_CENSUS: HEALTHY (packages=HEALTHY systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)'`:

```
11:STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=1 nonzero=0 detail=11111111:1
12:TSUKUROI_CENSUS: HEALTHY (packages=HEALTHY systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY):unreadable
13:TSUKUROI_CENSUS: BLOCKED (packages=DEGRADED systemd=BLOCKED drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)
```
2 rollup lines. The forged line is printed first, so the natural consumer idiom
`grep -m1 '^TSUKUROI_CENSUS:'` reads **HEALTHY** on a run whose real verdict is BLOCKED.

Same vector, two more shapes (receipts `case=nlplane`, `case=nlstorage`):
`devinfo/$'1\nPLANE packages: HEALTHY (fake)'` ⇒ 7 PLANE lines (grammar pins six),
and `devinfo/$'1\nSTORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0 x'`
⇒ **two fully well-formed STORAGE lines**, the second matching the frozen counter's own
`LINE_RE` (`tools/score-storage-arm-r38.py:54-57`, whose suffix is `(?: .*)?$`):

```
LINE_RE match: True | STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=1 nonzero=0 detail=11111111:1
LINE_RE match: True | STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0 x:unreadable
last-wins state = HEALTHY        (real state = BLOCKED)
```
This is the arm's own anti-claim inverted: the injected line is the exact "no btrfs
filesystem is mounted ⇒ 0/0/0" pass reading (header:363), on a tree that says BLOCKED.

### F2 — fake sibling-owned routing line

`devinfo/$'1\nHANDOFF ADJ-04 mori class=kill-events value=1 kind=dated-event state=prepared window=2026-01-01:00:00 source=journal-window x'`
is emitted as a third HANDOFF line and is accepted as a **compared** line by the round-32
counter (`tools/score-census-handoff-r32.py:509-520`, `parse_handoff`): observed
`parsed=True, class=kill-events, value=1` alongside the two real lines (value=138, value=5).
The one-line grammar is the only barrier between this arm and the HANDOFF contract.

### F3 — whitespace / metacharacters in a devid ⇒ token corruption (no new line)

| devid | observed STORAGE tail | effect |
|---|---|---|
| `1 2` | `detail=11111111:1 2:unreadable` | a space inside a structured field: a whitespace tokenizer sees a bare token `2:unreadable` after `detail=` |
| `$'1\tx'` | `detail=11111111:1<TAB>x:unreadable` | same, tab |
| `1=write_errs=99` | `detail=11111111:1=write_errs=99:unreadable` | forged-looking `key=value` inside the devid slot |
| `1:write_errs=99` (+ nonzero counters) | `detail=11111111:1:write_errs=99:write_errs=1` | four colon fields in a three-field triple; left-to-right readers attribute `write_errs=99` to the devid |
| `a,b` (+ nonzero) | `detail=11111111:a,b:write_errs=1` | `,` is the entry separator: reads as two entries, the second with an empty fsid8/devid |
| `1,` (+ nonzero) | `detail=11111111:1,:write_errs=1` | same split via the trailing-comma trim at 1885 |
| `$'1\x1b]0;PWNED\x07'` | `detail=11111111:1^[]0;PWNED^G:unreadable` | raw ANSI OSC in the line (terminal-title injection in any log viewer) |

Note the F3 rows are **accepted by the frozen v1 counter**: `parse()` returns the correct
`(state, filesystems, devices, nonzero)` and `six_planes_all=True` for the space, comma and
colon cases (LINE_RE's `(?: .*)?` swallows the broken tail). Only the newline rows fail it,
and only via the line-count check (`parse` requires `len(lines)==1`, exactly six PLANE lines
and exactly one rollup: `score-storage-arm-r38.py:164-170`). Frozen counters fail closed —
no false PASS — but nothing in them notices F3.

## 3. Inputs tried that hold (no corruption)

- Counter **values**: trailing word (`write_errs 5 junk`), `0x10`, `7;<text>`, glued
  `write_errs=0`, and a newline inside `error_stats` followed by `PLANE oom: HEALTHY (x)`
  all yield `nk=-1` ⇒ `detail=...:malformed`; the offending value is never echoed (1869-1876).
  Backslash escapes are inert (`read -r`).
- **Fsid name**: a directory named `$'11111111-...-555555555555\nPLANE oom: HEALTHY (x)'`
  is rejected by the regex — verified independently: bash `=~` gives NOMATCH both for a
  trailing newline and for newline-plus-text (glibc without REG_NEWLINE) — so the clean
  fixture reports `state=HEALTHY filesystems=0 devices=0 nonzero=0`. `features` is ignored
  as designed.
- **Glob metacharacters** in a devid (`*[a]?`) are harmless when the device is clean: no
  detail entry is emitted, the line is exactly `...filesystems=1 devices=1 nonzero=0`.
  (Iteration at 1857 is a quoted glob; expansion results are not word-split.)
- `state`, `filesystems`, `devices`, `nonzero` cannot be influenced by a name; only
  `detail` (and line count) can.
- Adjacent, non-grammar: an entry that is a symlink is followed (`[ -e ]`/`[ -f ]`), so a
  devid symlink to a file elsewhere is read — observed `detail=11111111:1:unreadable` for
  a symlink to `/etc/hostname`. Fixture-level only; not assessed further here.
- Adjacent coverage nit: a dot-prefixed devinfo entry (`.9`) is invisible to the glob
  while a numeric sibling exists (`devices=1`, HEALTHY) — kernel sysfs never emits one.

## 4. Is the risk real on a live host?

**No for the default path.** Live evidence: `/sys/fs/btrfs/` holds one lowercase-UUID
directory plus `features`; its `devinfo/` holds exactly `1`; `stat -c '%a %U:%G'` on the
root, `devinfo` and `devinfo/1` is `755 root:root`, and `error_stats` is `444 root:root`
(readable by uid 1000). devid directory names are created by the kernel in sysfs — an
unprivileged shell cannot create or rename an entry there — so a live host has no
user-controlled devid, and the census's default `TSUKUROI_BTRFS_SYSFS=/sys/fs/btrfs`
(446) cannot be fed a hostile name by an unprivileged user.

**Yes for every supplied tree.** `TSUKUROI_BTRFS_SYSFS` is an environment seam (446), and
the C1 pre-seat amendment's q82 arm deliberately runs the census against a tree bind-mounted
over `/sys/fs/btrfs` inside `unshare -rm` (`tools/score-storage-arm-r38-q82.py`, the
`unshare -rm sh -c ...` invocation). Any run whose tree the *reader* did not build can carry
a forged `TSUKUROI_CENSUS:` / `PLANE` / `STORAGE` line, and the forged rollup precedes the
real one. Severity: low as a live-host vuln (no privilege boundary crossed), medium as a
contract defect — header:350-354 states the arm "prints ONE line", and that invariant is
false for any tree with a non-numeric devinfo basename. The arm's six selftest cases
(2890-2922) contain no hostile name, and `check()` asserts with per-line `grep -qE`
(2091; the per-line `grep -qE` is at 2151), so even a `^STORAGE ...$` assertion is satisfied by an injected line: the test
harness cannot detect this class, and no case asserts "exactly one STORAGE line".

## 5. Smallest remediation (verdict-neutral, no new dependency)

The kernel's devid is a decimal device id (live: `1`; `corpus/knowledge/storage-health-r26.md:15`
writes the path as `devinfo/<devid>/error_stats`). Reject anything else and never echo a raw
basename. Replace the increment and the three devid appends at 1859/1861/1872/1875 with:

```bash
        nd=$((nd + 1)); devn=$((devn + 1)); f=$dev/error_stats
        # A devid is the kernel's decimal device id; any other basename is not a devid this
        # arm can name, and a raw directory basename is never echoed into a structured field
        # (a name containing a newline would otherwise forge a PLANE/STORAGE/rollup line).
        if ! [[ ${dev##*/} =~ ^[0-9]+$ ]]; then
          blocked=1; detail+="$fs8:-:unrecognized-devid,"; continue
        fi
        did=${dev##*/}
```
then use `$did` in place of `${dev##*/}` at 1861, 1875 and in the `ddet` append at 1872
(`ddet+="$fs8:$did:$k=$v,"`), and document in header:354 that `<devid>` is a decimal devid
and that `<reason>` is one of `unreadable|malformed|no-devinfo|unrecognized-devid`.

Add one selftest case next to 2890-2922 (keeps the "healthy rollup" stance: the STORAGE
line is verdict-neutral, the rollup stays HEALTHY):

```bash
  case_home='storage-hostile-name'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/btrfs/$sfs/devinfo/"$'1\nPLANE packages: HEALTHY (fake)'
  mkdir -p "$FX/btrfs/$sfs/devinfo/2 3"
  check 'hostile devinfo names forge no line; both entries are named, not echoed (R38-C1)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=2 nonzero=0 detail=11111111:-:unrecognized-devid$' \
    'ABSENT:^PLANE packages: HEALTHY \(fake\)'
```
and extend `check()` (2091) with a count assertion so "ONE line" is testable, e.g.
`[ "$(printf '%s\n' "$out" | grep -c '^STORAGE ')" -eq 1 ]` and the same for
`^TSUKUROI_CENSUS:` / `^PLANE `.

Adjacent doc defect, worth one line in the same edit: header:354 writes the detail list as
`[detail=<fsid8>:<devid>:<key>=<value>|<fsid8>:<devid>:<reason>,...]`, using `|` where the
code emits `,` between entries (1885) — the separator is unstated and the `|` reads as a
field separator.

## 6. What I did not do

- Did not run the frozen counters end-to-end (they build their own fixtures and have no
  injection fixture); instead I imported `score-storage-arm-r38.py`'s `parse()` and
  `score-census-handoff-r32.py`'s `parse_output()`/`parse_handoff()` and fed them the
  observed stdout — that is the evidence in §2.
- Did not exercise the q82 namespace path with a hostile tree (its tree is counter-built).
- Did not attempt any write to `/sys` or any host mutation; no sudo; no pacman.
