VERDICT: defect-found

Seat R51CritCheatC2a — item C2-A1 (attack C2 `idiom_sites` by spelling). Non-counted wave-1 seat.

## Bytes under test
- `tools/tsukuroi-census.sh` at 2732ee6c06108c031c4d8043239b994e0504eb2f (via `git show`), must-match arm at line 2396: `    elif ! out_has 'host=fixture-host'; then`. `out_has` = `buf_has` (full-read awk, no early exit), defined at census lines 2230-2239.
- `tools/check-selftest-matcher-r51.py` at 2732ee6c, blob sha256 `3a9af76b4ecc06dcc502659708f2c80f6dbdae3f4cb379d50651f4c4efea30b9` (matches FROZEN-hashes.txt; working-tree copy not used). `IDIOM_RE` lines 59-62; `idiom_sites` lines 104-105; predicate lines 55-56.
- Base census `idiom_sites` = 0 (imported via importlib, `propose.py` / `results.json` field `base_idiom_sites`).

## Method
1. For 23 spellings (22 + control), replaced line 2396 once in a scratch copy of the census with `    elif ! <SPELL>; then`. All 23 mutants pass `bash -n`.
2. Scored each mutant with the frozen `idiom_sites`.
3. Measured hazard: `set -euo pipefail`; 200 KB buffer; host line first (worst case for early exit) and mid-buffer; 20 trials per spelling; count trials where the condition is false although the host line is present (a false miss = real SIGPIPE hazard).
4. Proposed a replacement leg and scored it on the real census and on all 23 mutants.
- Not run: the full counter / `--selftest` (no selftest-bearing command was needed for idiom spellings; cost budget kept). No mutant was run through the census harness itself.
- Tools installed: none.

## Results (measured, `receipts/results.json`, `receipts/table.md`)

| id | spelling | frozen idiom_sites | first-line false misses /20 | mid-buffer /20 | real hazard |
|---|---|---|---|---|---|
| C0 | control: printf \| grep -q | 1 | 20 | 20 | yes |
| S01 | producer through variable | 0 | 20 | 20 | yes |
| S02 | command printf | 0 | 20 | 20 | yes |
| S03 | builtin printf | 0 | 20 | 20 | yes |
| S04 | consumer in brace group | 0 | 20 | 20 | yes |
| S05 | process substitution `grep -q x <(printf ...)` | 0 | 0 | 0 | no (status not consumed) |
| S06 | grep -E -q | 0 | 20 | 20 | yes |
| S07 | grep --quiet (control) | 1 | 20 | 20 | yes |
| S08 | grep -m1 | 0 | 20 | 20 | yes |
| S09 | sed -n 1p then grep -q | 0 | 0 | 20* | no (*mid-buffer run is a semantic artifact: sed 1p only sees line 1) |
| S10 | awk match-exit | 0 | 20 | 20 | yes |
| S11 | read -r (probe form) | 0 | 20 | 20 | yes |
| S12 | head -c 64 then grep -q | 0 | 20 | 20 | yes |
| S13 | head --lines=1 then grep -q | 0 | 20 | 20 | yes |
| S14 | grep -e PAT -q | 0 | 20 | 20 | yes |
| S15 | /usr/bin/grep -q | 0 | 20 | 20 | yes |
| S16 | command grep -q | 0 | 20 | 20 | yes |
| S17 | subshell consumer `( grep -q x )` | 0 | 20 | 20 | yes |
| S18 | awk NR==1{exit} (probe form) | 0 | 20 | 20 | yes |
| S19 | grep -m 1 (spaced) | 0 | 20 | 20 | yes |
| S20 | echo producer, grep -E -q | 0 | 20 | 20 | yes |
| S21 | timeout 5 grep -q | 0 | 20 | 20 | yes |
| S22 | head -n 1 then grep -q (control) | 1 | 20 | 20 | yes |

Sensitivity: the control C0 fails 20/20 at 200 KB, so the trial design can see the hazard.

## Holes: real SIGPIPE hazards that score `idiom_sites` 0 (18 spellings)
Exact arm lines (as spelled in the scratch mutant of tools/tsukuroi-census.sh:2396; `receipts/lines.txt`):
- S01 `    elif ! { p=printf; "$p" '%s\n' "$out" | grep -q 'host=fixture-host'; }; then`
- S02 `    elif ! command printf '%s\n' "$out" | grep -q 'host=fixture-host'; then`
- S03 `    elif ! builtin printf '%s\n' "$out" | grep -q 'host=fixture-host'; then`
- S04 `    elif ! printf '%s\n' "$out" | { grep -q 'host=fixture-host'; }; then`
- S06 `    elif ! printf '%s\n' "$out" | grep -E -q 'host=fixture-host'; then`
- S08 `    elif ! printf '%s\n' "$out" | grep -m1 'host=fixture-host' >/dev/null; then`
- S10 `    elif ! printf '%s\n' "$out" | awk '/host=fixture-host/ { exit 0 } END { exit 1 }'; then`
- S11 `    elif ! printf '%s\n' "$out" | read -r _; then`
- S12 `    elif ! printf '%s\n' "$out" | head -c 64 | grep -q 'host=fixture-host'; then`
- S13 `    elif ! printf '%s\n' "$out" | head --lines=1 | grep -q 'host=fixture-host'; then`
- S14 `    elif ! printf '%s\n' "$out" | grep -e 'host=fixture-host' -q; then`
- S15 `    elif ! printf '%s\n' "$out" | /usr/bin/grep -q 'host=fixture-host'; then`
- S16 `    elif ! printf '%s\n' "$out" | command grep -q 'host=fixture-host'; then`
- S17 `    elif ! printf '%s\n' "$out" | ( grep -q 'host=fixture-host' ); then`
- S18 `    elif ! printf '%s\n' "$out" | awk 'NR==1{exit}'; then`
- S19 `    elif ! printf '%s\n' "$out" | grep -m 1 'host=fixture-host' >/dev/null; then`
- S20 `    elif ! echo "$out" | grep -E -q 'host=fixture-host'; then`
- S21 `    elif ! printf '%s\n' "$out" | timeout 5 grep -q 'host=fixture-host'; then`

Why they slip: the frozen `IDIOM_RE` (matcher:59-62) requires the producer to be a literal `printf|echo|cat` directly after a statement anchor, and the consumer to be `grep` with `-q` immediately after `grep` (or `--quiet/--silent`) or `head -n1/-1/-n1`. Each hole breaks one of those: a variable command word (S01), a `command`/`builtin` prefix (S02, S03, S16), a brace or subshell consumer (S04, S17), a `-q` after the pattern or `-E` before it (S06, S14, S20), a `/usr/bin/` or `timeout` wrapper (S15, S21), `-m`/`--max-count` (S08, S19), `head -c`/`--lines` (S12, S13), and bare `read`/`awk ... exit` (S10, S11, S18).

Not holes (harmless, not counted): S05 (no pipe; the producer's status is not checked), S09 (sed -n 1p reads all input; no SIGPIPE on printf).

## Proposed closing leg (behavioural-free, regex; replaces nothing, adds one counted term)
Verified in scratch: census at 2732ee6c = 0 hits; every hazardous spelling above = 1 hit; harmless S05 = 0; S09 = 1 (harmless false positive, not in census).

Exact text to add next to `IDIOM_RE` in tools/check-selftest-matcher-r51.py (for the L1 pre-w2 amendment):
```python
# producer: printf/echo/cat (optionally command/builtin/exec, /usr/bin/) of an expansion, OR a variable as the command word
PROD2 = re.compile(
    r'(?:^|[;&!]|(?<!<)[({]|\$\(|\b(?:if|elif|then|do|while|until)\b)\s*!?\s*'
    r'(?:(?:(?:command|builtin|exec)\s+)?(?:/(?:usr/)?bin/)?(?:printf|echo|cat)\b[^|]*\$'
    r'|"?\$\{?[A-Za-z_][A-Za-z0-9_]*\}?"?\s)')
# early-exit consumer anywhere after the pipe
CONS2 = re.compile(
    r'\bgrep\b[^|]*\s-[A-Za-z]*[qm]|\bgrep\b[^|]*--(?:quiet|silent|max-count)|\bhead\b|\bread\b'
    r'|\bawk\b(?:(?!END)[^|])*\bexit\b|\bsed\b[^|]*[;\s\'"{]q\b')
PIPE2 = re.compile(r'(?<!\|)\|(?!\|)')

def idiom_pipe_sites(text):
    """Lines where a variable-expanding producer is piped into an early-exit consumer.
    Exempt: process substitution `< <(...)` (status unused) and pipelines whose status is discarded `|| true`."""
    n = 0
    for raw in text.split('\n'):
        ln = strip_comment(raw)
        if re.search(r'\|\|\s*true\)*\s*$', ln):
            continue
        if any(PROD2.search(ln[:m.start()]) and CONS2.search(ln[m.end():]) for m in PIPE2.finditer(ln)):
            n += 1
    return n
```
Predicate change: add `and idiom_pipe_sites == 0` (and report `idiom_pipe_sites` in the JSON). Census at 2732ee6c scores 0 under this leg (checked by `propose.py`; receipts show `census_new_hits: []`).

Why the exemptions are not new holes: both exemptions remove a pipeline whose failure cannot abort the census or flip a branch (`|| true` discards status; `< <( )` status is not read). A `printf | head` in an `if` condition or an assignment without `|| true` is still flagged.

Census lines that a producer-agnostic leg would wrongly flag (why the leg narrows to variable producers): tools/tsukuroi-census.sh:716, :1006, :1540 (`mapfile ... < <(printf ... | ... | head ...)`), :1826 (`x=$(printf ... | head -n6 ... || true)`), :1205 (`done < <(find ... | LC_ALL=C sort | head -n 4000)`). The `< <(`/`|| true` exemptions cover them; all are harmless by status.

## Named limits (not closed by this leg)
- Function producers: `emit() { printf '%s\n' "$1"; }; emit "$out" | grep -q x` (not measured here; same mechanism, not flagged by PROD2).
- Multi-line pipelines split across a `\` continuation (the matcher is per line; census line 841 and 3495 already show this shape).
- `|| true` in a condition is exempt by design (it is a different defect, not an abort).
- Eval, aliases, and `$(...)` wrappers around the whole pipe are outside any lexical leg.

## Receipts
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-51/w1/R51CritCheatC2a/`: `results.json` (23 mutants, idiom_sites, hazard counts), `table.md`, `lines.txt` (exact spelled lines), `attack.py`, `propose.py` (PROD2/CONS2 test, census 0), `extra.py` + `extra_out.txt` (added spellings: no-space pipes, `-Fq`, `-F -e x -q`, awk exit-before-END vs END, discarded status). Scratch path /fast/scratch/hyaku/tsukuroi-r51/R51CritCheatC2a removed after copying.
- Census scratch copy sha256 (git-show bytes of 2732ee6 tools/tsukuroi-census.sh): aeda2cbcdcc4b08b09fefcddc237da7c0d8ee903aaf063a1578452081e0245dc.

## Operability note
One bash call failed once with "Working directory does not exist" for the scratch cwd; re-running with absolute paths succeeded. No lane file, fleet file, or PATH directory written. No git mutation.
