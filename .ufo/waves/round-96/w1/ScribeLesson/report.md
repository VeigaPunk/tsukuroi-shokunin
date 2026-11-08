# ScribeLesson — round-96 lesson draft, with the round's own corrections re-measured (wave w1)

Seat: scribe (axis: **calibration**). Lane
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (branch `master`, jj-colocated; git HEAD detached
at `a814f24dc31270bca4e8999ac3cd907ecd72f100`). This seat wrote **no** lane file except the draft
lesson under its own seat dir and the receipts under `.ufo/waves/round-96/w1/ScribeLesson/`. No
`git`/`jj` mutation was run (`rev-parse`, `log`, `show`, `status`, `diff`, `archive` only — all
read-only). `tools/make-r96-bends.py` and `tools/make-r95-bends.py` were **not** run (they write
into the frozen wave dir); the N04 bend was re-derived from the frozen copy with the frozen
battery instead. Scratch `/fast/scratch/hyaku/tsukuroi-r96/ScribeLesson/` — deleted on exit (§6).

**Deliverable.** The draft lesson is at
`.ufo/waves/round-96/w1/ScribeLesson/corpus/lessons/round-96.md` (the path mirrors
`corpus/lessons/round-96.md` so the L1 can integrate it as one file). It carries the four required
sections: `## Gate` (8 sources opened 2026-11-08 with URL, access date, ≤25-word located quote and
byte offset, 3 explicit refusals with the observed status/body, and the census before/after
commands with exit codes), `## Mistakes` (5 entries, each with class, evidence pointer,
captured-by and fix), `## Routed` (the seven r95 spot-check items, each with its receipt, plus the
r94/r93 carry-forward), and `## Relation to the r95 freeze manifest`.

**Axis moved.** calibration. This seat's move is not a claim — C1 and C2 belong to the executor
seats. It is that **two of the round's own corrections are themselves miscounted against the
bytes**, and both are now measured rather than asserted: the four-component class was sampled
**twice** by the r95 instrument (roster row `12.9.5.1` *and* the `--usage-check` leg `12.9.6.1`),
not "once" as the landed README says; and the round's own new registry row S390 cites a byte
(157653) that lands inside an HTML attribute rather than on the element or sentence it names, while
the sibling row S389's four bytes are exact. Both carry a **failing check** under this seat dir.

---

## 1. What this seat read first (the required inputs)

```
$ cat .ufo/waves/round-96/claims.json
$ cat .ufo/plans/round-96.md
$ cat .ufo/waves/round-96/before/instruments.sha256
$ sed -n '191,224p' corpus/lessons/round-95-verifier-spotcheck.md     # §6 routed defects
$ sed -n '139,140p' corpus/QUALITY.md
$ grep -n '^## Round 96' SCORECARD.md && sed -n '7905,7940p' SCORECARD.md
```

Facts taken from them, all carried into the draft with their commands: the frozen C1/C2 sentences
and kill rules; the seven r95 spot-check routed items and their dispositions; QUALITY 139 (the
numeric-bound rule, both legs) and 140 (the criterion that routed 2 owed, added this round); the
round-96 SCORECARD section (the void binding and the tip receipt); the r95 freeze manifest's nine
pins and the r96 manifest's seventeen.

## 2. The Gate — sources opened, admits and rejects

Commands (all run by this seat, 2026-11-08):

```
$ cd /fast/scratch/hyaku/tsukuroi-r96/ScribeLesson/pins
$ curl -sSL -o <pin> -w '%{http_code} %{size_download}' <url>      # 8 admits + 3 rejects
$ sha256sum <pin>
$ python3   # located-quote byte offsets: d.find(needle) on the raw fetched body
```

| URL | status | bytes | sha256 (16) | verdict |
|---|---|---|---|---|
| https://docs.python.org/3/library/sys.html#sys.int_info.default_max_str_digits | 200 | 280632 | `a7e005875e4152bc` | **admit** → S390 (new) |
| https://docs.python.org/3.15/library/stdtypes.html#integer-string-conversion-length-limitation | 200 | 815447 | `6bf2ce2ba49d3097` | **admit** (re-open) → S389 |
| https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/common/lib/config.c | 200 | 23351 | `a940acae3a0a9c4d` | **admit** (re-open) → S382 |
| https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/ChangeLog | 200 | 121313 | `d2e08cc4a4bffc4b` | **admit** (re-open) → S383 |
| https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/host/limine.c | 200 | 69050 | `4da21c7cceae2380` | **admit** (re-open) → S384 |
| https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/common/lib/config.c | 200 | 23351 | `a940acae3a0a9c4d` | **admit** (re-open) → S386 (byte-identical to S382's) |
| https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/ChangeLog | 200 | 122099 | `ab280b451ee6f56b` | **admit** (re-open) → S387 |
| https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/host/limine.c | 200 | 69050 | `4da21c7cceae2380` | **admit** (re-open) → S388 (byte-identical to S384's) |
| https://man.archlinux.org/man/limine.8 | **404** | 2706 | `e0ad4429a6597299` | **REJECT** |
| https://api.github.com/repos/Limine-Bootloader/Limine/releases/tags/v12.9.6 | 200 | 26652 | `b3f81a021cf090a2` | **REJECT** as a row |
| https://man.archlinux.org/man/limine.conf.5 | **404** | 2725 | `542ba6f649941080` | **REJECT** |

Raw bodies and the per-reject reasoning: `receipts/05-gate-rejections.txt`. Located quotes with
byte offsets: `receipts/02-gate-located-quotes.txt`. Digests: `receipts/01-gate-sources.sha256.txt`
(the fetched bytes are under `ScribeLesson/pins/`).

- **Admit (S390):** "The default value for sys.get_int_max_str_digits() when it is not otherwise
  explicitly configured." — raw byte **157851** of the 280632-byte pin. The configured default of
  CPython's decimal-conversion limit; it states no Limine behaviour.
- **Admit (S389 re-open):** "The default limit is 4300 digits as provided in
  sys.int_info.default_max_str_digits." — raw byte **785297** of the 815447-byte pin, byte-identical
  to the r95 pin.
- **Reject 1:** `man.archlinux.org/man/limine.8` → HTTP 404, `<title>Page not found — Arch manual
  pages</title>`; no such page, nothing to admit.
- **Reject 2:** the GitHub release API → HTTP 200, `tag_name` `v12.9.6`, body 512 chars whose first
  sentence is "Changelog can be found [here](…/blob/v12.9.6/ChangeLog)." and whose rest is the
  tarball-signature text. It states no Limine behaviour: a wave-directory locator, never a row.
- **Reject 3:** `man.archlinux.org/man/limine.conf.5` → HTTP 404, 2725 bytes.

### The census, before and after

```
$ git archive 73c47107 | tar -x -C <scratch>/pre73c
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census   --file <scratch>/pre73c/corpus/SOURCES.md
file  rows 389   (tier.A 371, tier.B 6, tier.C 12; mined 351, queued 5, rejected 33)   exit 0
$ bash .../sources-census.sh validate --file <scratch>/pre73c/corpus/SOURCES.md
exit 0   E-findings 0   W-findings 58   lines 59

$ git rev-parse HEAD    # a814f24dc31270bca4e8999ac3cd907ecd72f100
$ bash .../sources-census.sh census --root /home/vgpnk/Projects/shokunin tsukuroi
tsukuroi  rows 390  (tier.A 372, tier.B 6, tier.C 12; mined 352, queued 5, rejected 33)   exit 0
$ bash .../sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
exit 0   E-findings 0   W-findings 58   lines 59
```

Row count from the committed blobs
(`git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}'`): `73c47107` → **389**,
`38adc4ed` → **389**, `59cbfe2f` → **390**. One row added: **S390** (tier A). Rows touched
old→new in place: **none**. Full output: `receipts/06-census-before-after.txt`,
`receipts/census-validate-pre.txt`, `receipts/census-validate-after.txt`.

## 3. The two findings this seat measured

### 3a. R96-FRONTIER-COUNTED-ONCE — the round's own correction undercounts the class

The landed README correction reads "the class was sampled once, and r96 broadens it"
(`corpus/README.md:1163`). Measured: the r95 instrument sampled the four-component shape **twice**.

```
$ grep -n 'REFUSAL_VERSIONS = ' tools/limine-pin-battery-r95.py
1643:REFUSAL_VERSIONS = ("12.9", "12.9.5.1", "abc", "", " 12.9.5", "12.9.5 ", "+12.9.5", "12..5",
$ sed -n '2300,2301p' tools/limine-pin-battery-r95.py
        cases = [("12.9", 64), ("abc", 64), ("12.9.6.1", 64), ("", 64), ("9" * 5000 + ".0.0", 64),

$ python3 .ufo/waves/round-96/before/controls/do-nothing-battery-r95.py \
      --gate .ufo/waves/round-96/before/controls/bends/N04-extra-components.py --usage-check
verdict unmet
failing cases 1 [{'version': '12.9.6.1', 'want_rc': 64, 'rc': 0, 'ok': False}]
```

The usage leg is **not** blind to the bend — it sends `12.9.6.1` and expects rc 64, and the bent
gate answers rc 0. The blind leg is the **family roster**, not the instrument. Receipt:
`receipts/10-r95-usage-check-leg.txt`.

### 3b. R96-S390-LOCATOR-BYTE — the round's new registry row cites a byte that does not resolve

The S390 row's `anchor` cell reads "`sys.int_info.default_max_str_digits` attribute, byte 157653 of
the 2026-11-08 pin (sha256 `a7e00587…`)"; the same byte is bound to the quoted sentence in
`corpus/knowledge/limine-bound-per-component-r96.md:19` and in the integrated
`corpus/lessons/round-96.md`. Measured on that exact pin:

```
  <dt> opening tag of the attribute              byte 157495
  id="sys.int_info.default_max_str_digits"       byte 157525
  byte 157653 as cited  ->  b' class="sig-name descname"><span class="pre">default'
  visible name `default_max_str_digits`         byte 157698
  start of the quoted sentence                   byte 157851
```

The sibling row S389 cites four bytes and **all four are exact** (780197 → `<section id=…>`;
780256 → `<span id="int-max-str-digits">`; 785297 → "The default limit is 4300 digits"; 782228 →
"When an operation would exceed the limit,"), so the convention is unambiguous. **157653 is the
start of nothing it names.**

The check, and its failure:

```
$ python3 .ufo/waves/round-96/w1/ScribeLesson/receipts/check-s390-locator.py --pins <pins>
S389 byte 780197 -> measured 780197  PASS  <section id="integer-string-conversion-length-limitation">
S389 byte 780256 -> measured 780256  PASS  <span id="int-max-str-digits">
S389 byte 785297 -> measured 785297  PASS  the `4300` sentence
S389 byte 782228 -> measured 782228  PASS  the ValueError sentence
S390 byte 157653 -> measured 157525  FAIL  the `sys.int_info.default_max_str_digits` attribute
     bytes at the cited offset: b' class="sig-name descname"><span class="pre">def'
locators 5, failing 1
exit=1
```

Receipts: `receipts/03-s390-locator-byte.txt`, `receipts/check-s390-locator.py`.

## 4. The two required mistakes, re-derived

```
$ python3 tools/limine-pin-battery-r96.py --gate .ufo/waves/round-96/before/controls/bends/N04-extra-components.py \
      --runs 1 --work <scratch> --json <out>
verdict unmet   families_passed 101/103   cases 412
failed_families ['EXTRA-COMPONENT', 'REFUSAL-VERSIONS']   error rows 0

$ the frozen pre-freeze dev run, .ufo/waves/round-96/before/dev/N04-extra-components.json
verdict unmet   families_passed 101/103   cases 412
failed_families ['EXTRA-COMPONENT', 'REFUSAL-VERSIONS']   error rows 0

$ grep -c 'falsifies-wording' .ufo/waves/round-95/claim-falsification.tsv   ->  6
$ grep -c 'falsifies-number' .ufo/waves/round-95/claim-falsification.tsv   ->  1
$ grep -c ''             .ufo/waves/round-95/claim-falsification.tsv       ->  21
$ sed -n '219p' /home/vgpnk/Projects/shokunin/.ufo/reports/round-95/tsukuroi.md
the artifact column; the four `falsifies-wording` rows point at A2/A3/A4 and the one
```

The r95 report's "four" against the ledger's six is the routed r95 report-count miss; the r96
checker reads it as F6 at the landed tree. Receipt: `receipts/04-mistakes-evidence.txt`.

## 5. C1's blindness legs and C2's six classes, measured by this seat

```
$ python3 .ufo/waves/round-96/before/controls/do-nothing-battery-r95.py --gate tools/check-limine-pins.py --runs 1 --work <scratch> --json <out>
verdict met   families_passed 99/99   failed_families []   cases 396   error rows 0   exit 0
  roster carries EXPLICIT-VERSION-ECHO / -ERA / REFUSAL-VERSIONS-9DIGIT-Y / EXTRA-COMPONENT : False (all four)

$ ... do-nothing-battery-r95.py --gate .ufo/waves/round-96/before/controls/bends/N04-extra-components.py --runs 1 --work <scratch> --json <out>
verdict unmet   families_passed 98/99   failed_families ['REFUSAL-VERSIONS']   cases 396   error rows 0   exit 1
```

Receipt: `receipts/07-do-nothing-blindness.txt`.

```
$ python3 tools/check-r96-calibration.py --selftest
clean PASS · F1 PASS · F2 PASS · F3 PASS · F4 PASS · F5 PASS · F6 PASS · selftest PASS 7/7   exit 0

$ python3 tools/check-r96-calibration.py --root <scratch>/pre73c --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-95/tsukuroi.md --tsv .ufo/waves/round-95/claim-falsification.tsv
status FAIL   exit 1
F1 QUALITY.md has no criterion 140
F2 receipt .ufo/waves/round-96/before/r95-registry-gate.sha256 missing
F2 SCORECARD.md has no Round 96 section
F3 tools/limine-pin-battery-r95.py still says largest in-bound
F3 tools/make-r95-bends.py does not say boundary member
F3 lesson does not relate the r95 freeze manifest to the edits
F4 README does not scope the sentence to the r94 family roster
F5 tip receipt .ufo/waves/round-96/before/c2-tip-b8f878c8.json missing
F6 report states no falsifies-wording count
F6 report states no falsifies-number count

$ python3 tools/check-r96-calibration.py --root .
status PASS   findings []   unreadable []   exit 0
```

All six classes F1-F6 are present before, and the landed tree reads 0 findings. Receipt:
`receipts/08-c2-calibration.txt`.

## 6. The r95 freeze manifest relation (measured, not asserted)

```
$ sha256sum -c .ufo/waves/round-95/before/instruments.sha256
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r95.py: FAILED
tools/make-r95-bends.py: FAILED
... (the other seven lines: OK)
sha256sum: WARNING: 2 computed checksum(s) did NOT match
exit=1

$ git show b8f878c8:tools/limine-pin-battery-r95.py | sha256sum
a51dca18d3c7641664a2f64476a7abc2bb14ff1133772f109ac73490828b9ebb  -     # == the r95 manifest line
$ git show b8f878c8:tools/make-r95-bends.py | sha256sum
57669e190e3e695956c0c4bca4302050daef62dd1b3ce8f9d7f98b869ba97554  -     # == the r95 manifest line
$ git show b8f878c8:tools/check-limine-pins.py | sha256sum
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  -     # == the r95 manifest line

$ python3   # ast.parse both versions, strip leading docstrings, ast.dump
tools/limine-pin-battery-r95.py ast_equal_modulo_docstrings: True
tools/make-r95-bends.py ast_equal_modulo_docstrings: True

$ sha256sum -c .ufo/waves/round-96/before/instruments.sha256
17 lines OK   0 FAILED   exit 0
```

The r95 manifest's two failures are exactly the two files the r96 wording correction touched, the
pinned bytes are re-derivable at `b8f878c8` to the byte, and the edits are docstring-only (equal
ASTs modulo docstrings). Receipt: `receipts/09-r95-freeze-manifest-relation.txt`.

## 7. PASS/FAIL per expected line

| expected line | verdict | receipt |
|---|---|---|
| Gate: ≥1 admit with URL, access date 2026-11-08, ≤25-word located quote, admit reason | **PASS** (8 admits) | `receipts/01`, `receipts/02` |
| Gate: ≥1 reject with the observed status/body | **PASS** (3 rejects) | `receipts/05` |
| Gate: the census before/after commands and exit codes | **PASS** (389 → 390, exit 0 both, 0 E) | `receipts/06` |
| Mistake R96-FRONTIER-NOT-SENT: class, evidence pointer, captured-by, fix | **PASS** | `receipts/04` §(a), `receipts/10` |
| Mistake R96-N04-TWO-FAMILIES: class, evidence pointer, captured-by, fix | **PASS** | `receipts/04` §(b) |
| Mistake: the routed r95 report-count miss | **PASS** (6 vs "four") | `receipts/04` §(c) |
| Routed: the spot-check's items and how r96 treats them | **PASS** (all 7) | `receipts/11` |
| Relation to the r95 freeze manifest: the r96 docstring edits vs the b8f878c8 pins | **PASS** | `receipts/09` |
| Every number carries its command | **PASS** | throughout the draft |

## 8. Out of scope (not this seat's to do)

- The L1 integrates the draft; this seat wrote **no** `corpus/`, `tools/`, `SKILL.md`, `SCORECARD.md`,
  `LOG.md` or `.ufo/plans/` byte, and did not touch `claims.json`, `before/`, or any sibling lane.
- The r96 claim-falsification ledger `.ufo/waves/round-96/claim-falsification.tsv` and the r96
  fleet report do not exist yet; F6 therefore cannot be exercised against them, and the after-state
  reading above is the no-report reading (`status PASS`, `findings []`). This is disclosed, not a
  defect: the L1 files both.
- The S390 anchor correction and the README "sampled once" correction are **proposals** here — the
  L1 owns `corpus/SOURCES.md`, `corpus/README.md` and `corpus/lessons/round-96.md`, and this seat
  has not edited any of them.
- The r93 probe-grammar half (routed 5) stays open: `EXTRA_COMPONENT_VALUES` are flag values
  (`tools/limine-pin-battery-r96.py:1720`), not the probe answer `Limine 12.9.6.1`.

## 9. Tooling

Nothing was installed or upgraded. The commands used `curl`, `sha256sum`, `grep`, `sed`, `awk`,
`diff`, `git` (read-only) and `python3` 3.14.8. No `pacman` transaction was attempted (pacman is
paused host-wide); no host sysctl, service or kernel parameter was touched. Per the operator's
tooling directive, no tool install was needed for this seat's task, so there is no
tool/version/channel/reason row to record.

**Cleanup**: scratch `/fast/scratch/hyaku/tsukuroi-r96/ScribeLesson/` (the three `--work` roots, the
pre-round archive, the fetched pins and the rejection bodies) was removed after the last command;
the copies under the seat dir are the cited receipts. The battery's own `tempfile.mkdtemp` case
directories are removed by the battery itself.

Lane state after this seat: `git status --porcelain` lists only untracked `.ufo/waves/round-96/…`
paths (this seat's dir and other seats' dirs); no tracked file was modified by this seat, and
`sha256sum -c .ufo/waves/round-96/before/instruments.sha256` reads 17 × OK.

## 10. Addendum — the r96 report and ledger landed after §5; F6 re-measured end to end

The r96 fleet report (`.ufo/reports/round-96/tsukuroi.md`) and the r96 ledger
(`.ufo/waves/round-96/claim-falsification.tsv`) landed at 08:05, after this seat's earlier
readings. The routed r95 report-count miss can therefore be closed end to end, and it was
(`receipts/12-f6-end-to-end.txt`):

```
$ awk -F'\t' 'NF>1{c[$3]++} END{for(k in c) print k, c[k]}' .ufo/waves/round-96/claim-falsification.tsv
neutral 7
falsifies-number 1
falsifies-wording 3
rows: 11

$ grep -n 'falsifies-wording' /home/vgpnk/Projects/shokunin/.ufo/reports/round-96/tsukuroi.md
64:  rows — 3 falsifies-wording rows and 1 falsifies-number row, plus 7 neutral — covering both claims

$ python3 tools/check-r96-calibration.py --root . \
      --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-96/tsukuroi.md \
      --tsv .ufo/waves/round-96/claim-falsification.tsv
status PASS   findings []   unreadable []   exit 0
```

And the r95 report still fails F6 against the same checker, for a **second** reason worth
recording: F6's regex is `(\d+)\s+.?falsifies-wording` — a *numeral* — and the r95 sentence spells
the count as the **word** "four", so the checker cannot bind a count at all
("report states no falsifies-wording count"). The routed defect was not only a wrong number but an
**unbindable** one: a report that writes its counts in words passes no check at all.

This supersedes the §8 disclosure that the r96 ledger and report did not yet exist; the no-report
reading in `receipts/08-c2-calibration.txt` remains the earlier measurement and is kept as the
record of the tree at that time.

## 11. Addendum — both findings closed by the L1 at `8fdb05e1`

The L1 committed both corrections while this seat was finishing:

```
$ git show 8fdb05e1 --stat | head -12
8fdb05e1 round-96: S390 locator byte corrected (157851 sentence / 157525 id),
                   README counted-twice correction, integrated lesson (Gate/Mistakes/Routed/scoreboard),
                   SCORECARD measured rows
 corpus/README.md                                       |  3 +-
 corpus/SOURCES.md                                      |  2 +-
 corpus/knowledge/limine-bound-per-component-r96.md     |  4 +-
 corpus/lessons/round-96.md                             | 185 ++++++++----------
```

**The S390 anchor cell, as landed:**

```
$ python3 -c "for l in open('corpus/SOURCES.md'): ... print(c[6].strip(), c[7].strip())"
anchor cell: `sys.int_info.default_max_str_digits` attribute (id at byte 157525; quoted sentence at byte 157851) of the 2026-11-08 pin (sha256 a7e00587…)
quote cell : The default value for sys.get_int_max_str_digits() when it is not otherwise explicitly configured.
```

**The README sentence, as landed** (`git show 8fdb05e1 -- corpus/README.md`):

```
-the class was sampled once, and r96 broadens it.
+the class reached the r95 instrument twice (the roster's `12.9.5.1` row and the `--usage-check` value
+`12.9.6.1`), and r96 broadens it a third time.
```

**The check, in both readings** (`receipts/13-locator-check-both-readings.txt`):

```
$ python3 .ufo/waves/round-96/w1/ScribeLesson/receipts/check-s390-locator.py --pins .../ScribeLesson/pins --row old
S390 byte 157653 -> measured 157525  FAIL   locators 5, failing 1   exit 1
$ python3 ... --row new
S390 byte 157525 -> measured 157525  PASS   locators 5, failing 0   exit 0
```

Same script, same pins, only the byte the row cites. The defect stays re-derivable and the
correction is now checkable — a check that can fail and can pass.

**Still open for r97 (a rule, not a defect):** nothing in the lane checks a *byte* locator. The
census (E01-E12) validates row shape; QUALITY 21 asks for a stable fragment; the four bytes in
S389 and the two in the corrected S390 were never machine-checked. `check-s390-locator.py` is a
two-row prototype of the registry-wide check that would catch the next one before it lands.

**Lane state at this seat's exit:** `git status --porcelain` shows only untracked
`.ufo/waves/round-96/…` paths — this seat's own two paths and the other seats' paths. No tracked
file was modified by this seat; `sha256sum -c .ufo/waves/round-96/before/instruments.sha256` reads
17 × OK.
{"seat": "ScribeLesson", "verdict": "findings", "notes": "Draft corpus/lessons/round-96.md written in the seat dir with the four required sections. ## Gate: 8 sources opened 2026-11-08 (new S390 admit - the CPython sys.int_info default, quote at raw byte 157851 of the 280632-byte pin sha256 a7e00587...; the S389 and S382-S384/S386-S388 re-opens) plus 3 explicit refusals with the observed status and body (man.archlinux.org/man/limine.8 HTTP 404 2706 bytes; api.github.com release tag v12.9.6 HTTP 200 26652 bytes with a 512-char body that states no Limine behaviour; man.archlinux.org/man/limine.conf.5 HTTP 404 2725 bytes); the census before/after is recorded with its commands and exit codes (389 rows -> 390 rows, exit 0 both, 0 E-findings, one new row S390 tier A, no row touched old->new). ## Mistakes: 5 entries, each with class, evidence pointer, captured-by and fix - R96-FRONTIER-NOT-SENT (REFUSAL_VERSIONS carries 12.9.5.1, so the class was broadened not first), R96-N04-TWO-FAMILIES (the bend reads unmet 101/103 with failed_families ['EXTRA-COMPONENT','REFUSAL-VERSIONS'], 0 error rows, measured twice: my own run and the frozen before/dev run), R96-N02-ERRORROWS (the r96 twin; A3 narrows the clause), R96-REPORT-WORD-COUNT (the routed r95 miss: the r95 filed report says 'four falsifies-wording rows', the committed ledger holds 6), R96-S390-LOCATOR-BYTE. ## Routed: all seven r95 spot-check items with the receipt for each, plus the r94/r93 carry-forward. ## Relation to the r95 freeze manifest: the r95 manifest reads 2 FAILED (exactly the two files the r96 wording correction touched), the pinned bytes are re-derivable at b8f878c8 to the byte, the edits are docstring-only (equal ASTs modulo docstrings), and the r96 manifest reads 17 OK. TWO FINDINGS, both now CLOSED by the L1 at 8fdb05e1 (the S390 anchor cell now cites the id at byte 157525 and the quoted sentence at byte 157851; the README sentence now says the class reached the r95 instrument twice - the roster row 12.9.5.1 and the --usage-check value 12.9.6.1 - and r96 broadens it a third time). The check receipts/check-s390-locator.py reads --row old = FAIL exit 1 and --row new = PASS exit 0, same script and same pins. Still open for r97 as a RULE: nothing in the lane checks a byte locator. The findings were: (1) R96-FRONTIER-COUNTED-ONCE - the landed README correction says the four-component class 'was sampled once', but the r95 instrument sampled it twice (roster row 12.9.5.1 and the --usage-check leg 12.9.6.1, which on the N04 bend reads unmet with {'version':'12.9.6.1','want_rc':64,'rc':0,'ok':False}); the blind leg is the family roster, not the instrument. (2) R96-S390-LOCATOR-BYTE - the round's own new registry row cites byte 157653 for the attribute, which lands inside the opening tag <span class=\"sig-name descname\">; the id= is at 157525, the visible name at 157698 and the quoted sentence at 157851, while the sibling row S389's four bytes are all exact; receipts/check-s390-locator.py prints 'S390 byte 157653 -> measured 157525 FAIL' and 'locators 5, failing 1', exit 1. Also measured by this seat: the r96 fleet report and ledger landed at 08:05, so the routed r95 report-count miss is closed end to end - the committed r96 ledger holds 3 falsifies-wording / 1 falsifies-number / 7 neutral over 11 rows, the filed r96 report states exactly that, and the checker reads status PASS findings [] exit 0; the r95 report still fails F6 twice, and for a second reason - F6's regex binds a NUMERAL while the r95 sentence spells the count as the word 'four', so the routed defect was an unbindable number, not only a wrong one. C2 selftest PASS 7/7, C2 before = status FAIL with all of F1-F6, C2 after = status PASS findings [], the do-nothing battery reads met 99/99 on the landed gate and unmet 98/99 with ['REFUSAL-VERSIONS'] on N04. ADDENDUM: the r96 fleet report and the r96 ledger landed after the earlier readings, so the routed r95 report-count miss is closed end to end - the committed r96 ledger holds 3 falsifies-wording / 1 falsifies-number / 7 neutral over 11 rows, the filed r96 report states exactly that, and the checker reads status PASS findings [] exit 0 against the landed tree. The r95 report still fails F6 twice, and for a second reason worth recording: F6's regex binds a NUMERAL and the r95 sentence spells the count as the word 'four', so the checker cannot bind a count at all - the routed defect was an unbindable number, not only a wrong one. No tool installed or upgraded; no pacman transaction; no git/jj mutation; scratch deleted."}
