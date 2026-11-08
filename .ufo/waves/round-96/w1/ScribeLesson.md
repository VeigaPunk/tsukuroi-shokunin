# ScribeLesson — round-96 lesson draft (wave w1, seat ScribeLesson)

Seat: scribe (axis: **calibration**). Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
(branch `master`, jj-colocated; git HEAD detached at
`a814f24dc31270bca4e8999ac3cd907ecd72f100`). Full report, receipts and the PASS/FAIL table:
`.ufo/waves/round-96/w1/ScribeLesson/report.md`. Receipts:
`.ufo/waves/round-96/w1/ScribeLesson/receipts/`. Draft lesson (the L1 integrates this file):
`.ufo/waves/round-96/w1/ScribeLesson/corpus/lessons/round-96.md`.

This seat wrote no lane file outside its own seat dir; no git/jj mutation was run (read-only
`rev-parse`, `log`, `show`, `status`, `diff`, `archive`); `tools/make-r96-bends.py` and
`tools/make-r95-bends.py` were not run (the N04 bend was re-derived from the frozen copy with the
frozen battery). Scratch `/fast/scratch/hyaku/tsukuroi-r96/ScribeLesson/` was deleted on exit.

## Deliverable

The draft lesson carries the four required sections:

- **`## Gate`** — 8 sources opened 2026-11-08 (URL, access date, ≤25-word located quote, byte
  offset, admit/reject with reason): the new **S390** admit ("The default value for
  sys.get_int_max_str_digits() when it is not otherwise explicitly configured.", raw byte 157851
  of the 280632-byte pin, sha256 `a7e00587…`), the S389 / S382-S384 / S386-S388 re-opens, and
  **3 refusals** with the observed status and body (`man.archlinux.org/man/limine.8` → HTTP 404,
  2706 bytes, title "Page not found — Arch manual pages"; the GitHub release API → HTTP 200,
  26652 bytes, `tag_name` v12.9.6, a 512-char body pointing at the ChangeLog and the signing key;
  `man.archlinux.org/man/limine.conf.5` → HTTP 404, 2725 bytes). The census before/after is
  recorded with its commands and exit codes: **389 rows → 390 rows, exit 0 both, 0 E-findings**,
  exactly one new row (S390, tier A), no row touched old→new in place.
- **`## Mistakes`** — 5 entries, each with class, evidence pointer, captured-by and fix:
  **R96-FRONTIER-NOT-SENT** (the r95 Frontier said the four-component shape was not sent;
  `REFUSAL_VERSIONS` carries `12.9.5.1` — the class was broadened, not first),
  **R96-N04-TWO-FAMILIES** (the bend fails `EXTRA-COMPONENT` *and* the pre-existing
  `REFUSAL-VERSIONS`; frozen after a development run), **R96-N02-ERRORROWS** (the r96 twin of the
  same class), **R96-REPORT-WORD-COUNT** (the routed r95 report-count miss: the r95 report says
  "four `falsifies-wording` rows", the committed ledger holds six), and **R96-S390-LOCATOR-BYTE**.
- **`## Routed`** — all seven r95 spot-check items with the receipt that carries each, plus the
  r94/r93 carry-forward, plus the two items this seat measured that no queue yet carries.
- **`## Relation to the r95 freeze manifest`** — the r95 manifest reads 2 FAILED (exactly the two
  files the r96 wording correction touched), the pinned bytes are re-derivable at `b8f878c8` to
  the byte, the edits are **docstring-only** (equal ASTs modulo docstrings), and the r96 manifest
  reads 17 × OK.

## Findings (this seat's own, both with a failing check)

1. **R96-FRONTIER-COUNTED-ONCE** — the landed README correction says the four-component class
   "was sampled once"; the r95 instrument sampled it **twice** (roster row `12.9.5.1` and the
   `--usage-check` leg `12.9.6.1`, which on the N04 bend reads `unmet` with
   `{'version': '12.9.6.1', 'want_rc': 64, 'rc': 0, 'ok': False}`). The blind leg is the family
   roster, not the instrument — the same roster-vs-instrument scope slip r95's A4 fixed for the
   r94 case, re-opened in the other direction.
2. **R96-S390-LOCATOR-BYTE** — the round's own new registry row cites byte 157653 for
   "`sys.int_info.default_max_str_digits` attribute"; that byte lands inside the opening tag
   `<span class="sig-name descname">`. The `id=` is at 157525, the visible name at 157698 and the
   quoted sentence at 157851. The sibling row S389's four bytes are all exact, so the convention is
   unambiguous. `receipts/check-s390-locator.py` prints `S390 byte 157653 -> measured 157525 FAIL`
   and `locators 5, failing 1`, **exit 1**.

Neither is written to the lane by this seat: `corpus/SOURCES.md`, `corpus/README.md` and
`corpus/lessons/round-96.md` are the L1's files.

## Numbers (each with its command; full raw output in the receipts)

| claim | command | observed |
|---|---|---|
| census before | `sources-census.sh census --file <pre73c>/corpus/SOURCES.md` | rows 389, exit 0 |
| census after | `sources-census.sh census --root /home/vgpnk/Projects/shokunin tsukuroi` | rows 390, exit 0 |
| N04 bend, two families | `limine-pin-battery-r96.py --gate .../bends/N04-extra-components.py --runs 1 --work <scratch> --json <out>` | `unmet 101/103`, `['EXTRA-COMPONENT','REFUSAL-VERSIONS']`, 0 error rows |
| r95 ledger counts | `grep -c 'falsifies-wording' .ufo/waves/round-95/claim-falsification.tsv` | 6 (the r95 report says "four") |
| C2 before | `check-r96-calibration.py --root <pre73c> --report <r95 report> --tsv <r95 tsv>` | `status FAIL`, exit 1, all of F1-F6 present |
| C2 after | `check-r96-calibration.py --root .` | `status PASS`, `findings []`, exit 0 |
| C2 selftest | `check-r96-calibration.py --selftest` | `PASS 7/7`, exit 0 |
| do-nothing blindness | `do-nothing-battery-r95.py --gate <landed|N04> --runs 1` | landed `met 99/99`; N04 `unmet 98/99`, `['REFUSAL-VERSIONS']` |
| r95 manifest | `sha256sum -c .ufo/waves/round-95/before/instruments.sha256` | 2 FAILED, exit 1 |
| r96 manifest | `sha256sum -c .ufo/waves/round-96/before/instruments.sha256` | 17 OK, exit 0 |

## Tooling

None installed or upgraded. `curl`, `sha256sum`, `grep`, `sed`, `awk`, `diff`, read-only `git` and
`python3` 3.14.8 only. No `pacman` transaction (pacman is paused host-wide); no host sysctl,
service or kernel parameter touched.
## Addendum — the routed r95 report-count miss, closed end to end

The r96 fleet report and the r96 ledger landed at 08:05, after this seat's earlier readings. The
routed r95 miss can therefore be closed end to end, and it was
(`receipts/12-f6-end-to-end.txt`):

```
$ awk -F'\t' 'NF>1{c[$3]++} END{for(k in c) print k, c[k]}' .ufo/waves/round-96/claim-falsification.tsv
neutral 7 / falsifies-number 1 / falsifies-wording 3     (11 rows)
$ grep -n 'falsifies-wording' /home/vgpnk/Projects/shokunin/.ufo/reports/round-96/tsukuroi.md
64:  rows — 3 falsifies-wording rows and 1 falsifies-number row, plus 7 neutral — covering both claims
$ python3 tools/check-r96-calibration.py --root . --report <r96 report> --tsv .ufo/waves/round-96/claim-falsification.tsv
status PASS   findings []   unreadable []   exit 0
```

The r95 report still fails F6 twice — and for a **second** reason worth recording: F6's regex
binds a **numeral** and the r95 sentence spells the count as the **word** "four", so the checker
cannot bind a count at all ("report states no falsifies-wording count"). The routed defect was not
only a wrong number but an **unbindable** one.
{"seat": "ScribeLesson", "verdict": "findings", "notes": "Draft corpus/lessons/round-96.md written in the seat dir with the four required sections. ## Gate: 8 sources opened 2026-11-08 (new S390 admit - the CPython sys.int_info default, quote at raw byte 157851 of the 280632-byte pin sha256 a7e00587...; the S389 and S382-S384/S386-S388 re-opens) plus 3 explicit refusals with the observed status and body (man.archlinux.org/man/limine.8 HTTP 404 2706 bytes; api.github.com release tag v12.9.6 HTTP 200 26652 bytes with a 512-char body that states no Limine behaviour; man.archlinux.org/man/limine.conf.5 HTTP 404 2725 bytes); the census before/after is recorded with its commands and exit codes (389 rows -> 390 rows, exit 0 both, 0 E-findings, one new row S390 tier A, no row touched old->new). ## Mistakes: 5 entries, each with class, evidence pointer, captured-by and fix - R96-FRONTIER-NOT-SENT (REFUSAL_VERSIONS carries 12.9.5.1, so the class was broadened not first), R96-N04-TWO-FAMILIES (the bend reads unmet 101/103 with failed_families ['EXTRA-COMPONENT','REFUSAL-VERSIONS'], 0 error rows, measured twice: my own run and the frozen before/dev run), R96-N02-ERRORROWS (the r96 twin; A3 narrows the clause), R96-REPORT-WORD-COUNT (the routed r95 miss: the r95 filed report says 'four falsifies-wording rows', the committed ledger holds 6), R96-S390-LOCATOR-BYTE. ## Routed: all seven r95 spot-check items with the receipt for each, plus the r94/r93 carry-forward. ## Relation to the r95 freeze manifest: the r95 manifest reads 2 FAILED (exactly the two files the r96 wording correction touched), the pinned bytes are re-derivable at b8f878c8 to the byte, the edits are docstring-only (equal ASTs modulo docstrings), and the r96 manifest reads 17 OK. TWO FINDINGS, both now CLOSED by the L1 at 8fdb05e1 (the S390 anchor cell now cites the id at byte 157525 and the quoted sentence at byte 157851; the README sentence now says the class reached the r95 instrument twice - the roster row 12.9.5.1 and the --usage-check value 12.9.6.1 - and r96 broadens it a third time). The check receipts/check-s390-locator.py reads --row old = FAIL exit 1 and --row new = PASS exit 0, same script and same pins. Still open for r97 as a RULE: nothing in the lane checks a byte locator. The findings were: (1) R96-FRONTIER-COUNTED-ONCE - the landed README correction says the four-component class 'was sampled once', but the r95 instrument sampled it twice (roster row 12.9.5.1 and the --usage-check leg 12.9.6.1, which on the N04 bend reads unmet with {'version':'12.9.6.1','want_rc':64,'rc':0,'ok':False}); the blind leg is the family roster, not the instrument. (2) R96-S390-LOCATOR-BYTE - the round's own new registry row cites byte 157653 for the attribute, which lands inside the opening tag <span class=\"sig-name descname\">; the id= is at 157525, the visible name at 157698 and the quoted sentence at 157851, while the sibling row S389's four bytes are all exact; receipts/check-s390-locator.py prints 'S390 byte 157653 -> measured 157525 FAIL' and 'locators 5, failing 1', exit 1. Also measured by this seat: the r96 fleet report and ledger landed at 08:05, so the routed r95 report-count miss is closed end to end - the committed r96 ledger holds 3 falsifies-wording / 1 falsifies-number / 7 neutral over 11 rows, the filed r96 report states exactly that, and the checker reads status PASS findings [] exit 0; the r95 report still fails F6 twice, and for a second reason - F6's regex binds a NUMERAL while the r95 sentence spells the count as the word 'four', so the routed defect was an unbindable number, not only a wrong one. C2 selftest PASS 7/7, C2 before = status FAIL with all of F1-F6, C2 after = status PASS findings [], the do-nothing battery reads met 99/99 on the landed gate and unmet 98/99 with ['REFUSAL-VERSIONS'] on N04. No tool installed or upgraded; no pacman transaction; no git/jj mutation; scratch deleted."}
