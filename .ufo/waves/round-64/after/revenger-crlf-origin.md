# CRLF origin — mechanism archaeology over committed bytes (run 15, round 64, w1)

captured_utc=2026-11-03T19:07:05Z
Seat: RV1Origin (revenger). Read-only over git plumbing (`git show`/`cat-file`/`diff`/`ls-tree`,
`od`). No write to the lane tree outside this file. No mutating git/jj command run.
Scratch: `/fast/scratch/hyaku/tsukuroi-r64/RV1Origin/` (fixtures only; removed at exit).

Question: what mechanism, operating on the Windows host during rounds 59-63, converted
`corpus/SOURCES.md`, `SKILL.md` and `SCORECARD.md` from LF to CRLF?

**Answer in one sentence.** Not `core.autocrlf` and not an editor: the bytes are in the blobs
(`git cat-file` yields them; no `.gitattributes`, `core.autocrlf` unset at system/global/local), and
the pattern per file is a **whole-file byte rewriting of `LF`→`CRLF` first (every line, from line 1),
followed by appends whose new lines were CRLF** — the signature of a *text-mode* file handle on a
Windows host (`open(path,'w')` then `open(path,'a')` in CPython, `newline=None` ⇒ every `\n`
written becomes `\r\n`), interleaved with **byte-exact appends** that kept LF (shell `printf >>`,
binary mode), which is where the residual mixed regions come from.

---

## 1. Blob receipts — CR counts and first CR line at each boundary commit

```
$ git show <commit>:<file> | tr -cd '\r' | wc -c        # CR bytes in the blob
$ git show <commit>:<file> | wc -l                      # line count
```

| commit | file | lines | CR lines | first CR line | note |
|---|---|---|---|---|---|
| `81776bef` (c5a33d08^, r58 outcome) | SCORECARD.md | 4127 | 0 | — | all LF |
| | SKILL.md | 4886 | 0 | — | all LF |
| | corpus/SOURCES.md | 376 | 0 | — | all LF |
| | LOG.md | 2356 | 0 | — | all LF |
| `c5a33d08` (r59 **declaration**) | SCORECARD.md | 4178 | **4178** | **1** | whole file CRLF |
| | SKILL.md | 4886 | 0 | — | unchanged |
| | corpus/SOURCES.md | 376 | 0 | — | unchanged |
| | LOG.md | 2356 | 0 | — | unchanged |
| `2913b75d` (r59 **work**) | SCORECARD.md | 4178 | 4178 | 1 | unchanged since declaration |
| | SKILL.md | 5009 | **4990** | **1** | whole file CRLF except 19 LF tail lines |
| | corpus/SOURCES.md | 377 | **377** | **1** | whole file CRLF |
| `5dd83fa3` (r59 verifier spot-check) | SCORECARD.md | 4224 | 4178 | 1 | +46 appended **LF** lines (4179-4224) |
| | SKILL.md | 5009 | 5009 | 1 | repaired at `c4aa0f5c` (19 LF lines → CRLF) |
| | corpus/SOURCES.md | 377 | 377 | 1 | unchanged |
| `44fc183b` (r63 closure, the r64 base) | SCORECARD.md | 4701 | 4654 | 1 | 47 LF-only lines |
| | SKILL.md | 5490 | 5452 | 1 | 38 LF-only lines |
| | corpus/SOURCES.md | 381 | 381 | 1 | fully CRLF |
| `2f3061ef` (r64 declaration, this host) | SCORECARD.md | 4723 | **4723** | 1 | **re-CRLF'd whole file** (47 LF lines gone) |
| | SKILL.md | 5490 | 5452 | 1 | unchanged |
| | corpus/SOURCES.md | 381 | 381 | 1 | unchanged |

Commands (one representative run, full output):

```
$ git show --name-only --format='' <c> | while read -r f; do cr=$(git show "$c:$f" | tr -cd '\r' | wc -c); ...; done
=== c5a33d08
   CR=4178/4178  SCORECARD.md
=== 2913b75d
   CR=4990/5009  SKILL.md
   CR=377/377  corpus/SOURCES.md
=== 5dd83fa3      -- SCORECARD unchanged from 35c2748f
   CR=4178/4224  SCORECARD.md
```

**Earliest evidence line, per file.** SCORECARD.md: line **1** at `c5a33d08`. SKILL.md: line **1**
at `2913b75d`. corpus/SOURCES.md: line **1** at `2913b75d`. All three are whole-file conversions
(pattern **(a) whole-file**, first CR line = 1), *not* (b) an append whose new lines were CRLF
(that would leave the prefix LF and make the first CR line the first appended line), and not (c)
interleaving at the conversion commit.

```
$ git show 81776bef:SCORECARD.md | head -c 40 | od -c
0000000   #   t s u k u r o i - s h o k u n i n     342 200 224 ...
0000040   d  \n  \n   L   a   n   e                          <-- LF
$ git show c5a33d08:SCORECARD.md | head -c 40 | od -c
0000040   d  \r  \n  \r  \n   L   a   n                          <-- CRLF, line 1
$ git show c5a33d08:SKILL.md  | head -c 40 | od -c   ->  - - -  \n   n a m e ...
$ git show 2913b75d:SKILL.md  | head -c 40 | od -c   ->  - - -  \r  \n   n a m e ...
$ git show c5a33d08:corpus/SOURCES.md | head -c 40 | od -c  ->  ...  l e a r n s  \n  \n
$ git show 2913b75d:corpus/SOURCES.md | head -c 40 | od -c  ->  ...  l e a r n s  \r  \n  \r  \n
```

## 2. Byte-level reconstruction — the mechanism discriminator

The decisive test is whether the tip blob equals **CRLF-normalised(base) + appended bytes**
(whole-file text round trip) or **base bytes + appended bytes** (a byte append). Both were run
for every boundary.

```
$ python3 - <<'EOF'   # (full program in transcript; core test)
def crlf_all(b): return b.replace(b"\r\n",b"\n").replace(b"\r",b"\n").replace(b"\n",b"\r\n")
print(B.startswith(crlf_all(A)), B.startswith(A))
EOF
```

| commit | file | `CRLF(base)` is byte-prefix of tip | raw `base` is byte-prefix of tip | remainder |
|---|---|---|---|---|
| `c5a33d08` | SCORECARD.md | **True** | False | 51 lines, **51 CRLF / 0 LF** |
| `2913b75d` | SKILL.md | **True** | False | 123 lines, **104 CRLF / 19 LF** |
| `2913b75d` | corpus/SOURCES.md | (mid-file insert) | False | see below — exact reconstruction |
| `c4aa0f5c` | SKILL.md | **True** | False | 0 lines; 4990 CRLF → 5009 CRLF (the 19 LF lines converted), content delta 1/1 |
| `35c2748f` | SCORECARD.md | False | **True** | 46 lines, 0 CRLF / **46 LF** |
| `41c18296` | SCORECARD.md | False | **True** | 60 lines, **60 CRLF / 0 LF** |
| `dd994b92` | SCORECARD.md | False | True | 56 lines, 56 CRLF |
| `136bfb00` | SCORECARD.md | False | True | 61 lines, 60 CRLF / 1 LF |
| `541cdaea` | SCORECARD.md | False | True | 59 lines, 58 CRLF / 1 LF |
| `f47bb0aa` | SCORECARD.md | False | True | 20 lines, 19 CRLF / 1 LF |
| `e50973da` | SCORECARD.md | False | True | 60 lines, 60 CRLF |
| `f9eee551` | SCORECARD.md | False | True | 62 lines, 61 CRLF / 1 LF |
| `13b095a6` | SCORECARD.md | False | False (mid-file insert) | byte-exact insert, 47 LF lines preserved |
| `cdfd8b8c` | SCORECARD.md | False | True | 42 lines, 42 CRLF |
| `896e3c8b` | SCORECARD.md | False | True | 59 lines, 59 CRLF |
| `2f3061ef` | SCORECARD.md | **True** | False | 22 lines, 22 CRLF; the 47 LF lines became CRLF |
| `bef165c4` | SKILL.md | False | True | 143 lines, 106 CRLF / **37 LF** |
| `abb2a161` | SKILL.md | False | True | 113 lines, 113 CRLF |
| `f3f64812` | SKILL.md | False | True | 113 lines, 113 CRLF |
| `82f0e1a9` | SKILL.md | False | True | 112 lines, 111 CRLF / 1 LF |
| `bef165c4`..`82f0e1a9` | corpus/SOURCES.md | insert at id position | False | every commit reconstructs **exactly** as base with one line inserted |

Exact reconstruction outputs:

```
1 SCORECARD c5a33d08: base normalized-to-CRLF is a byte prefix of tip: True | tail = b'\r\n## Round 59 \xe2\x80\x94 declaration (2026-11-01, base `c2e32b00\xe2\x80\xa6' | tail_lines= 51
2 SKILL 2913b75d: tip startswith CRLF(base): True | rest lines: 121
   rest: CRLF= 104  LF= 19
3 SOURCES 2913b75d: len conv lines= 376 tip lines= 377
   first differing index (0-based): 282
   reconstructed == tip: True
   inserted line: b'| S274 | Task Scheduler error and success constants \xe2\x80\x94 Microsoft Learn, Win32/taskschd (current ref'
4 SOURCES bef165c4: first diff idx(0-based)= 283  reconstructed==tip: True  inserted[:80]= b'| S275 | reg query \xe2\x80\x94 Microsoft Learn, Windows Commands (current reference) \xe2\x80\x94'
5 SCORECARD 2f3061ef: tip startswith CRLF(base): True | tail CRLF lines: 22
```

So: **SCORECARD at `c5a33d08`, SKILL at `2913b75d`, SOURCES at `2913b75d` and SKILL at `c4aa0f5c`
are whole-file text round trips** (base bytes survive only after CRLF-normalisation), while
**every later commit is a genuine byte append or a byte-exact mid-file insert** (raw base is a
byte prefix, or a one-line insertion reconstructs the tip exactly).

### 2b. The append-pattern boundaries, verbatim

Pure CRLF-in-new-lines append (`41c18296`, SCORECARD — base tail is the r59-outcome LF block):

```
$ python3 -c "... print('base_tail=',A[-46:], 'append_head=',B[len(A):][:70])"
41c18296 SCORECARD.md: base_tail=b'own\n  mapping is opened.\n- **retired:** none.\n'
    append_head=b'\r\n## Round 60 \xe2\x80\x94 declaration (2026-11-01, base `5dd83fa3` + carry-in '
```

Pure LF-in-new-lines append (`35c2748f`, SCORECARD — the round-59 measured outcome):

```
35c2748f SCORECARD.md: base_tail=b'mmit cites them (R58-DECLARED-COMMAND rule).\r\n'
    append_head=b'\n## Round 59 \xe2\x80\x94 measured outcome (2026-11-01, author-side; non-author'
```

The **CRLF→LF switch inside SKILL.md at `2913b75d`** — the round-59 narrative section was
appended by a second writer after the CRLF rewrite:

```
$ git show 2913b75d:SKILL.md | sed -n '4989,4992p' | od -c | tail -8
0003240       |       t   s   u   k   u   r   o   i       |  \r  \n  \n
0003260   #   #       R   o   u   n   d       5   9     342 200 224
0003320   s   c   h   e   d   u   l   e   d   -   t   a   s   k ...
0003400   ,       2   0   2   6   -   1   1   -   0   1   )  \n
```

i.e. line 4990 ends `\r\n` and line 4991 (blank) + 4992 onward end `\n` — the 19 LF lines are
exactly lines 4991-5009, the appended "## Round 59" section. The same seam appears at `bef165c4`
(37 LF lines from line 5115 onward, "## Round 60 — registry read plane…").

## 3. Mechanism verdict per file

| file | pattern | mechanism | earliest evidence |
|---|---|---|---|
| **SCORECARD.md** | **whole-file** at `c5a33d08` (r59 *declaration*, not work): 4127 LF lines → 4178 lines, all CRLF, in one write (base is only recoverable as CRLF-normalised prefix) | **Windows text-mode write of the whole file**: CPython `open(p,'w')` with default `newline=None` translates every `\n` in the written string to `\r\n`, so a read-modify-write round trip converts the entire file. Not an append: an append-mode handle would leave lines 1..4127 LF. | line 1, blob `c5a33d08:SCORECARD.md` |
| **SKILL.md** | **whole-file** at `2913b75d` (r59 *work*): 4886 LF lines → CRLF, plus 104 CRLF new lines; then **19 LF new lines** from a second writer; repaired to all-CRLF at `c4aa0f5c` by another whole-file text round trip | same text-mode whole-file writer, then a **byte-exact appender** for the round-59 narrative (bash `printf >>`/binary mode) which preserved LF | line 1, blob `2913b75d:SKILL.md` |
| **corpus/SOURCES.md** | **whole-file** at `2913b75d`: 376 LF lines → 377 all-CRLF, with `S274` **inserted in id position** (line 283); every later round inserts exactly one row, byte-exact, EOL preserved | same text-mode whole-file writer taking a read → insert → write path (the insert makes a pure append impossible, so the same text-mode `write` also performed the EOL conversion) | line 1, blob `2913b75d:corpus/SOURCES.md` |

**Append-phase verdict.** From `35c2748f` onward the writers are byte-level: raw base is a byte
prefix and only the appended bytes carry EOLs. Those appended bytes were *authored* CRLF in most
commits (`41c18296`, `dd994b92`, `e50973da`, `cdfd8b8c`, `896e3c8b`, `abb2a161`, `f3f64812`) and
*authored* LF in three (`35c2748f` 46/46; the narrative tails of `2913b75d` 19/19 and `bef165c4`
37/143; plus single trailing LF lines in `136bfb00`, `541cdaea`, `f47bb0aa`, `f9eee551`,
`82f0e1a9`). The lane's own claim "record appends binary-mode byte-stable" (LOG.md:2462, 2687) is
therefore **true of the append mechanics and false of the appended bytes' EOL** — the appender was
byte-stable, but its input string already carried CRLF because it was composed through a
CRLF-emitting path.

### Ruled out, with the exact check

```
$ git config --get core.autocrlf ; git config --global --get core.autocrlf ; git config --system --get core.autocrlf
(empty; rc 1 each time)
$ git config --get-regexp 'core\.'
core.repositoryformatversion 0
core.filemode true
core.bare false
core.logallrefupdates true
$ git check-attr text eol -- SCORECARD.md SKILL.md corpus/SOURCES.md
SCORECARD.md: text: unspecified
SCORECARD.md: eol: unspecified
SKILL.md: text: unspecified ; SKILL.md: eol: unspecified
corpus/SOURCES.md: text: unspecified ; corpus/SOURCES.md: eol: unspecified
$ git ls-tree -r --name-only c5a33d08 | grep -c gitattributes
2          # both are fixture clones under .ufo/waves/, not lane-root attributes
```

- **`core.autocrlf` / smudge filter** — excluded: the CR bytes are *in the blobs* (`git cat-file`
  and `git show` both yield them; `git ls-files --eol` reports `i/crlf` for SCORECARD and SOURCES,
  `i/mixed` for SKILL, `i/lf` for LOG). A checkout filter would leave LF in the blob.
- **An editor "convert line endings" pass** — excluded: a one-shot conversion would leave no
  LF-remnant seams; the observed files carry contiguous LF regions that map exactly to
  individually-appended sections (§2b), and `c4aa0f5c` / `2f3061ef` each convert exactly the
  residual LF region and nothing else.
- **Double conversion (CRCRLF)** — excluded:

```
$ for every commit in `git log --first-parent 2f3061ef`: scan four files for b"\r\r\n"
commits scanned: 475 double-CR occurrences: 0
```

  so no writer ever round-tripped an already-CRLF file through Windows text mode twice; each
  conversion is a single pass.

## 4. Why the Windows-era census passed — the parser differential

**Observed.** The Windows-host census receipts report a clean lane while SOURCES.md was fully
CRLF:

```
$ git show 35c2748f:.ufo/waves/round-59/after/sources-census-end.txt | sed -n '1p;$p'
# sources-census END receipt, round 59 (2026-11-01) — command: bash scripts/sources-census.sh validate --root <fleet-root> tsukuroi; exit 0; 42 W04 warnings, 0 E-code findings; SOURCES 274 rows at end (S274 added inside Registry)
tsukuroi	ok	C:/Users/jpvei/.zcode/workspace/95b1ba4d-.../tsukuroi-shokunin/corpus/SOURCES.md
CENSUS_END_EXIT=0
$ git show 52d9ba1a:.ufo/waves/round-61/after/sources-census-end.txt | sed -n '1,5p'
sources-census validate --root <fleet-root> tsukuroi — round-61 END receipt (final tree 541cdaea)
captured_utc=2026-11-01T22:42:38Z
exit=0
W04_count=42
E_code_count=0
```

At `35c2748f` SOURCES.md is 377/377 CRLF; at `541cdaea` it is 379/379 CRLF. Both receipts show
42 W04 and **zero** E-code with `exit=0`.

**Reproduced on this host, same script, same bytes.** Copy of the HEAD blob plus a CR-stripped copy:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file SOURCES.crlf.md ; echo rc=$?
rc=1          E12-count=278   W04-count=0
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file SOURCES.lf.md   ; echo rc=$?
rc=1          E12-count=0     W04-count=42    (all findings are E11, a --file relative-dir artifact)
```

The counts invert exactly against the Windows receipts (278 E12 / 0 W04 here vs 0 E12 / 42 W04
there), and **278 is exactly the S-row count** of the file:

```
$ git show 2f3061ef:corpus/SOURCES.md | grep -cE "^\| *S[0-9]{3,} *\|"
278
```

**Mechanism.** `scripts/sources-census.sh` detects the registry section in gawk:

```
$ sed -n '608,613p' /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
      if (line ~ /^ {0,3}##[ \t]/) {
        sub(/^ {0,3}/,"",line)
        in_registry=(trim(substr(line,3))=="Registry")
```

and `trim()` strips **only space and tab**:

```
$ sed -n '581p' /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
    function trim(s) { gsub(/^[ \t]+|[ \t]+$/,"",s); return s }
```

On GNU/Linux gawk, `$0` keeps the CR (verified):

```
$ printf '## Registry\r\n' | gawk '{printf "len=%d last_byte_index_cr=%d\n", length($0), index($0,"\r")}'
len=12 last_byte_index_cr=12
$ printf '## Registry\r\n' | gawk 'function trim(s){gsub(/^[ \t]+|[ \t]+$/,"",s);return s}{printf "heading_match=%d\n", (trim(substr($0,3))=="Registry")}'
heading_match=0
```

so `trim("Registry\r") == "Registry"` is **false**, `in_registry` stays 0 for the rest of the file,
and every `| S… |` row falls into the `if (!in_registry)` arm — which is exactly the E12 emitter
(one E12 per row-shaped line, 278 of them) while `rows++` is never reached (hence W04 = 0).

On MinGW gawk the CR never reaches `$0`. The gawk manual bundled on this host states the default
in §B.3.1.3 *Using gawk on PC Operating Systems*:

```
Under MS-Windows, 'gawk' (and many other text programs) silently translates end-of-line
'\r\n' to '\n' on input and '\n' to '\r\n' on output.  A special 'BINMODE' variable
allows control over these translations ...
   • If 'BINMODE' is '"r"' or one, then binary mode is set on read (i.e., no translations on reads).
```

and the census never sets it:

```
$ grep -n "BINMODE" /home/vgpnk/Projects/shokunin/scripts/sources-census.sh ; echo "rc=$?"
rc=1
```

⇒ default text mode on the Windows build: `## Registry\r\n` arrived at awk as `## Registry\n`,
`trim(substr(line,3))=="Registry"` matched, the registry parsed normally, 42 W04 appeared and no
E12. **[obs]** the manual's text-mode default; **[inf]** that the Windows-host gawk binary in the
r59-r63 path was the MinGW build — forced by the receipts themselves, since the same script over
the same CRLF bytes gives a 278-E12 flood here and a clean 0-E12 there, and no other input
difference exists (the receipt's `ok` line names the lane's own SOURCES.md).

Sanity check on the discriminating fixture (one registry row, 9 lines):

```
$ bash scripts/sources-census.sh validate --file crlf.md ; echo rc=$?
file	E12	S001 row outside Registry section
rc=1
$ bash scripts/sources-census.sh validate --file lf.md ; echo rc=$?
file	W03	S001 mined but unused
file	ok	/fast/scratch/hyaku/tsukuroi-r64/RV1Origin/fx/lf.md
rc=0
```

**Corollary — the secondary arm is CR-tolerant.** `usedby_findings()` runs in bash and trims with
`[[:space:]]` globs (`trim_cell`, line 531-536), which eats the CR; the E11 count is therefore
identical on both copies (435 / 435 in the runs above), while the gawk arm diverges (E12 278 vs 0,
W04 0 vs 42). The failure is localised to the gawk record-splitting path, not to the file.

**Corollary — census mode fails silently.** In default (non-`validate`) mode the CRLF copy reports
`rows 0 / FLEET rows 0 …` and `rc=0`:

```
$ bash scripts/sources-census.sh --file SOURCES.crlf.md | head -3
file	rows	0
FLEET	rows	0
FLEET	tier.A	0
```

versus `rows 278` for the LF copy. A consumer invoking census mode without `validate` reads a
CRLF registry as an *empty, clean* lane.

## 5. Divergences from the frozen C1 origin statement (round-64 declaration, `2f3061ef`)

The declaration states: *"origin at round-59 work `2913b75d` (parent `c5a33d08` is 100 % LF)"*.
Committed bytes falsify that for one of the three files and qualify it for the class:

1. **SCORECARD.md was already 100 % CRLF at `c5a33d08`** — the r59 **declaration**, 48 minutes
   before `2913b75d` (`81776bef` SCORECARD CR=0 → `c5a33d08` CR=4178/4178; content delta 51
   insertions / 0 deletions under `git diff --ignore-cr-at-eol`). So `c5a33d08` is 100 % LF only
   for SKILL.md and corpus/SOURCES.md. SCORECARD's origin commit is `c5a33d08`.
   *(Independently measured by seat SC2Census; filed there as F6 — agreement recorded.)*
2. **The class is not Windows-only.** At `2f3061ef` (the round-64 declaration, committed on this
   Linux host) SCORECARD.md was written whole-file again and its 47 residual LF-only lines
   (4179-4225, 4539 at `44fc183b`) came out CRLF: `CRLF(base)` is again a byte prefix of the tip,
   +22 lines all CRLF, content delta 22/0 under `--ignore-cr-at-eol`. The writer is therefore not
   the OS newline default; it is a writer that *emits CRLF explicitly* (`newline='\r\n'`, an
   explicit `'\r\n'.join`, or an EOL-preserving edit path keyed on the file's dominant EOL).
   Consequence for C1: stripping CR without changing the writer leaves the repair to be undone by
   the next declaration-class write. This is the mechanism behind SC2Census's "worktree SOURCES.md
   reverted to CRLF" observation (byte-identical to the `2f3061ef` blob).
3. **The 19-line and 46-line LF regions are not noise** — they are the exact footprints of the
   byte-mode appender, and they are what `c4aa0f5c` (SKILL 4990→5009 CRLF, content delta 1/1) and
   `35c2748f` created.

## 6. Confidence

- Whole-file vs append classification per commit/file: **high** — byte-exact reconstruction
  (`tip == CRLF(base) + tail`, and `tip == base with one line inserted`) succeeds or fails
  unambiguously for every boundary listed; no judgement call involved.
- Windows text-mode handle as the conversion mechanism: **high** for the *class* (blob-resident
  CR, whole-file conversion from line 1, zero double-CR across 475 commits, no attributes, no
  autocrlf, content invariant modulo CR); **medium** on the exact call site (CPython
  `open(p,'w')`/`'a'` is the best fit for a Python-tooled lane — the tools are Python and the r59
  probe receipts themselves show the same CRLF-from-Python-print signature per
  `corpus/lessons/round-54.md`'s `R54-CRLF-FIXTURE`; the alternatives — PowerShell `Out-File`,
  a Windows editor save, MSYS `sed -i` — produce indistinguishable bytes here, so the *writer
  identity* is [inf] while the *writer behaviour* is [obs]).
- Windows gawk text-mode default as the census-pass reason: **high** — the library manual's own
  wording, the absent `BINMODE`, the exact count inversion (278 ↔ 0 E12; 0 ↔ 42 W04; 278 = the
  S-row count), and the CR-in-`$0` measurement on Linux gawk.
- Which machine authored `2f3061ef`'s SCORECARD write: **unresolved [unk]** — the commit's
  declaration runs Linux-path receipts (`/home/vgpnk/...` census command in
  `.ufo/waves/round-64/before/census-start-receipt.txt`) and LOG.md is appended LF-clean in the
  same commit, yet SCORECARD comes back fully CRLF; both "explicit-CRLF writer on Linux" and "a
  Windows-side write carried into a Linux commit" remain open. Either way the divergence in §5.2
  holds.
