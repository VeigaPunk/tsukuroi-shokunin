# ExecDrift — round 99, wave w1

Seat: ExecDrift (executor). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`,
pre-round tip `f107da3afe511f7db8cdc30235a992b774903158` (measurement date 2026-11-08).
Scope: the frontier census (BEFORE), the CORPUS.md §10 id-collision guard fail-leg proof, the
R99-D1 pointer sweep, and the r96 calibration re-run. No claim is scored by this seat.

Frozen instruments verified before any measurement (receipt `receipts/00-instruments-sha256.txt`):

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && sha256sum -c .ufo/waves/round-99/before/instruments.sha256
... 16 lines ...
.ufo/plans/round-99.md: OK
rc=0
```

No `make-r*-bends.py` and no campaign tool was executed. `/home/vgpnk/Projects/shokuknow` was
opened read-only (`grep -oE` on `merge/tsukuroi/SOURCES.append.md`); nothing there was written.

## 1. Census (BEFORE — the AFTER is the L1's, after this round's row lands)

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --root /home/vgpnk/Projects/shokunin tsukuroi
ta... W04 ... (57 duplicate-url warning lines)
tsukuroi	W01	S381 tierC mined used-by=corpus/knowledge/limine-r92-oracle-isolation.md, corpus/lessons/round-92.md
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
rc=0
```

| expected | measured | verdict |
|---|---|---|
| exit code | 0 | PASS |
| error rows | 0 (`E##` histogram empty) | PASS |
| warning rows | 58 = 1 W01 + 57 W04 | PASS |
| rows | 395 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`) | PASS |

Raw census output: `receipts/01-census-validate.txt`; histogram: `receipts/01b-census-summary.txt`.

Tree note (measured, raw in `receipts/08-sources-md-diff-vs-f107da3a.txt`): the working tree carries
**395** rows while `git show f107da3a:corpus/SOURCES.md` has **394**; `git diff f107da3a --
corpus/SOURCES.md` is exactly `1 file changed, 1 insertion(+)` (the S395 r99 battery row) and
`git status --porcelain corpus/SOURCES.md` reads ` M corpus/SOURCES.md` — i.e. the row is present
in the working tree but uncommitted at measurement time. The census above validates the tree as
found (rc 0).

## 2. Column-loop and the CORPUS.md §Census sub-commands

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0
```

All outputs in `receipts/02-census-subcommands.txt`:

| sub-command | output | verdict |
|---|---|---|
| rows (seat-spec regex `S[0-9]{3,}`) | 395 | PASS |
| rows (CORPUS v1 regex `S[0-9][0-9][0-9]+`, trailing `|` required) | 395 | PASS |
| rows with 0–3 leading spaces | 395 | PASS (no indented row in the real registry) |
| malformed rows, seat-spec `{3,}` regex | 0 | PASS |
| malformed rows, CORPUS v1 regex | 0 | PASS |
| tier histogram | `A=377 B=6 C=12` | recorded |
| status histogram | `mined=355 queued=7 rejected=33` | recorded |
| duplicate ids (`uniq -d`) | empty | PASS |
| enum violations / tier inflation | empty | PASS |
| mined rows with missing `used-by` paths | empty | PASS |

## 3. CORPUS.md §10 id-collision guard — shown able to fail

Scratch fixture (2-space-indented row; archived at `fixtures/register-indented.md`):

```
| id | source | ... | used-by |
|---|---|---|---|
  | S002 | Fixture source — https://example.invalid/indented-fixture | docs | A | ... | queued | 2026-11-08 | 90d | — |
```

Maintained parser accepts it (and the frozen manual census does not see it):

```
$ sources-census.sh validate --file <scratch>/register-indented.md
file	ok	<scratch>/register-indented.md
validate rc=0

$ grep -cE '^\|[[:space:]]*S[0-9]{3,}' fixtures/register-indented.md
0
```

Extractor legs against a staged-id file holding `S002`
(`receipts/06-collision-fixture-official.txt`):

```
# old column-zero extractor ids:        (none)
old_count=0
# new 0-3-leading-space extractor ids:  S002
new_count=1
# comm -12 old vs staged:               (empty)  old_collisions=0
# comm -12 new vs staged:               S002     new_collisions=1
```

The 0–3-leading-space guard catches what the column-zero extractor false-greens: the fail-leg is
nonempty (`S002`) exactly where the old extractor reads empty.

Real files, same recipe (`receipts/07-collision-real.txt`, counts `receipts/10-collision-counts.txt`):

| set | count | file |
|---|---|---|
| registry ids (`corpus/SOURCES.md`, 0–3 spaces) | 395 | `receipts/reg-ids-real.txt` |
| registry ids, column-zero comparison | 395 | — |
| staged ids (`/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md`) | 147 | `receipts/staged-ids-real.txt` |
| `comm -12` collisions | **147** (`S200`–`S346`) | `receipts/collisions-real.txt` |

Every staged id collides (147/147): mass id drift; the package cannot be appended under CORPUS.md
rule 2 without a document-anchored renumber. Registry duplicate-id check: 0 (`uniq -d` empty).

## 4. R99-D1 pointer sweep at `f107da3a`

```
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin grep -n 'coverage-tip\|report-draft' \
    f107da3afe511f7db8cdc30235a992b774903158 -- .ufo SCORECARD.md LOG.md
... 18 producing files ...; rc=0
$ git cat-file -e f107da3afe511f7db8cdc30235a992b774903158:.ufo/waves/round-98/after/c2/coverage-tip.json
fatal: path '.ufo/waves/round-98/after/c2/coverage-tip.json' does not exist in 'f107da3afe...'
cat-file rc=128
```

Raw sweep: `receipts/03-pointer-sweep.txt`; classification: `receipts/09-pointer-classification.txt`.

Exactly **two** committed artifacts cite the non-existent
`.ufo/waves/round-98/after/c2/coverage-tip.json`:

1. `.ufo/waves/round-98/after/report-draft.md:110` — “`after/c2/`; `after/c2/coverage-tip.json`”
   (the draft is committed at `f107da3a`, `git cat-file -e` rc=0; the receipt it names is not).
2. `SCORECARD.md:7984` — “settled tip coverage `PASS 157/157 findings 0`
   (`after/c2/coverage-tip.json`)”.

All other `coverage-tip` hits are other rounds' own receipts that exist at `f107da3a`
(`.ufo/waves/round-93/after/registry-coverage-tip.json`, `.ufo/waves/round-97/w1/ExecGateHygiene/
receipts/04a-coverage-tip.txt`), and the `report-draft` hits outside round-98 are round-52/round-97
artifacts whose targets exist (`.ufo/waves/round-97/after/report-draft.md` rc=0). The fleet-repo
r98 report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-98/tsukuroi.md` contains neither token
(`grep` rc=1), so it does not cite the missing path.

Exact 18-file sweep list: see `receipts/09-pointer-classification.txt` (SCORECARD.md plus
round-52/92/93/97/98 `.ufo` files).

## 5. r96 calibration re-run against the r98 report and ledger

The checker accepts `--root/--report/--tsv` (usage confirmed), so it was run with the canonical
r98 report and the r98 falsification ledger:

```
$ python3 tools/check-r96-calibration.py \
    --root /home/vgpnk/Projects/shokunin/tsukuroi-shokunin \
    --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-98/tsukuroi.md \
    --tsv /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-98/claim-falsification.tsv
{
 "schema": "tsukuroi-r96-calibration-v1",
 "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
 "report": "/home/vgpnk/Projects/shokunin/.ufo/reports/round-98/tsukuroi.md",
 "findings": [],
 "unreadable": [],
 "status": "PASS"
}
rc=0
```

No refusal: `receipts/05-r96-calibration-r98.txt`.

## Acceptance accounting

| line | verdict |
|---|---|
| census command with rc, rows, warning/error counts | PASS — rc 0, 395 rows, 0 E, 58 W |
| all census sub-command outputs | PASS — `receipts/02-census-subcommands.txt` |
| collision guard fail-leg nonempty on indented scratch registry | PASS — `S002`, old extractor empty |
| real id counts + collision count | PASS — registry 395, staged 147, collisions 147 |
| pointer sweep file list + `git cat-file` rcs | PASS — rc 128 for the missing path; 2 citing artifacts |
| no campaign tool; shokuknow never written | PASS — only `grep -oE` read |
| calibration re-run | PASS — accepted args, `status PASS`, `findings []`, rc 0 |

Findings for the L1 (not claim failures): (a) the working tree has one uncommitted row (S395)
beyond `f107da3a` (394→395) and validates; (b) staged ids collide 147/147, so no assimilation
append is possible without a renumber; (c) the two artifacts above cite the missing round-98
receipt.

Receipts: `receipts/00-instruments-sha256.txt` … `receipts/10-collision-counts.txt`; fixtures:
`fixtures/register-indented.md`, `fixtures/staged-ids-indented.txt`,
`fixtures/old-ids-indented-fixture.txt`, `fixtures/collisions-indented-fixture.txt`.

{"seat":"ExecDrift","verdict":"findings","notes":"census rc0 395 rows 0E/58W (1 W01 + 57 W04; tree +1 uncommitted S395 vs f107da3a's 394); census subcommands all clean (0 malformed/dup/enum/missing-path); id-collision guard fail-leg proven (indented fixture validate rc0, old extractor 0 ids, 0-3-space extractor S002, comm -12 nonempty) and real files read registry 395 / staged 147 / collisions 147 (S200-S346); R99-D1 path .ufo/waves/round-98/after/c2/coverage-tip.json missing at f107da3a (cat-file rc128), cited by .ufo/waves/round-98/after/report-draft.md:110 and SCORECARD.md:7984; check-r96-calibration.py accepts --report/--tsv and reads PASS findings [] rc0; no campaign tool run and shokuknow read-only."}
