# ScoutSources — round 100 wave w1 — the two SOURCES rows (S396 own-work, S397 docs)

Full row text and the Gate-quote block: `.ufo/waves/round-100/w1/ScoutSources/SOURCES-rows.md`.
Receipts: `.ufo/waves/round-100/w1/ScoutSources/receipts/`.
Seat dir written: `.ufo/waves/round-100/w1/ScoutSources/` only. `corpus/SOURCES.md`,
`corpus/lessons/`, `corpus/knowledge/`, `tools/`, `.ufo/plans/` and `.ufo/waves/round-100/before/`
were **not** edited by this seat.

Verdict: **findings** — the rows are landed and their anchors re-derive byte-for-byte, but three
text defects in the landed rows/lesson are routed below (§4). Nothing falsifies a measured claim.

## 0. Read first — instrument integrity

```bash
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
sha256sum -c .ufo/waves/round-100/before/instruments.sha256
```

All 17 manifest entries `OK`, exit 0 (receipt inline above; the two files this seat measures are
`tools/make-r100-bends.py` `7ccfe69e52604ec5bb8db423e377cf9f0eb468baf03d0ef7be77b3209654e695` and
`tools/check-registry-content-r100.py` `7a23a522871ab5dd33a94ae51b09c70ab182a0d2a53d7380f82bb11a13f3c2d2`).

Byte-level copies taken read-only from the freeze commit, into scratch:

```bash
SD=/fast/scratch/hyaku/tsukuroi-r100/ScoutSources
git show 743ce449:tools/make-r100-bends.py                 > $SD/gen.py
git show 743ce449:tools/check-registry-content-r100.py      > $SD/chk.py
git show 743ce449:.ufo/waves/round-100/before/controls/bends/N12-x-echo.py > $SD/b12.py
git show 743ce449:.ufo/waves/round-100/before/controls/bends/N13-y-echo.py > $SD/b13.py
sha256sum $SD/gen.py $SD/chk.py $SD/b12.py $SD/b13.py
```

```
7ccfe69e52604ec5bb8db423e377cf9f0eb468baf03d0ef7be77b3209654e695  gen.py
7a23a522871ab5dd33a94ae51b09c70ab182a0d2a53d7380f82bb11a13f3c2d2  chk.py
eb247e1646d1b421cf047f2b2edeb34423227b5ca056edcaf0712924b3f0331a  b12.py
e1e5916fad0ee545a0571c852ebf658269322a138e802bcff5e875ab868bebee  b13.py
```

Sizes 4471 / 38009 / 30409 / 30446 bytes — the sizes the landed rows and the knowledge entry name.

## 1. Id collision (the expected line "S395 is the current maximum" is TRUE at the freeze, FALSE at HEAD)

```bash
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
git show HEAD:corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -u | tail -3
# S397
# S398
# S5
git show 743ce449:corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -u | tail -3
# S394
# S395
# S5
```

At the freeze tip `743ce449` the maximum id is `S395`, so `S396`/`S397` were the next free ids — the
seat's expectation holds against the freeze. But the L1's land commit **`c450cd68`** ("round-100:
land — … SOURCES S396-S398", parent `60b5636f`, the wave-w1 dispatch commit) landed rows under
**both** ids while this wave ran, so at scoring time they are occupied and `S399`/`S400` are the
next unused ones.

Consequence for the L1: **do not land a second `S396` or `S397`** (ids are never reused; a repeated
id is census `E03`). The landed rows *are* this seat's rows — same subjects, same anchors, verified
byte-for-byte in §2 and §3. `SOURCES-rows.md` is therefore the provenance/verification record of
the landed pair plus the corrections in §4, not a fresh proposal.

## 2. S396 (own-work) — anchor re-derivation, byte level (QUALITY 141)

Full row text: `SOURCES-rows.md` §1. The row's anchor cell claims:

> generator emission lines at BYTE 2615 (N12) and BYTE 3384 (N13) of the 4471-byte file
> (sha256 7ccfe69e…); checker `def parse_label_set` at BYTE 12134 and `TOKEN`/`SEPARATORS` at
> BYTEs 12025/12073 of the 38009-byte file (sha256 7a23a522…), all at the round-100 freeze 743ce449

Commands (all in scratch, on the bytes above):

```bash
grep -abo '"limine_version": ("999999998.9.9"' gen.py
grep -abo '"limine_version": ("12.999999998.4"'   gen.py
grep -abo '"999999998.9.9" if' gen.py
grep -abo '"12.999999998.4" if'  gen.py
grep -abo 'def parse_label_set' chk.py
grep -abo 'TOKEN'       chk.py
grep -abo 'SEPARATORS'  chk.py
grep -abo 'variant_labels' chk.py
```

Raw output:

```
2615:"limine_version": ("999999998.9.9"
3365:"limine_version": ("12.999999998.4"
2634:"999999998.9.9" if
3384:"12.999999998.4" if
12134:def parse_label_set
12025:TOKEN
12657:TOKEN
12073:SEPARATORS
12567:SEPARATORS
11164:variant_labels
16978:variant_labels
17179:variant_labels
17196:variant_labels
```

Per-claim PASS/FAIL:

| the row's claim | measured | verdict |
|---|---|---|
| N12 emission line at BYTE 2615 | 2615 | **PASS** |
| N13 emission line at BYTE 3384 | 3384 lands 19 bytes inside the clause (clause start = 3365) | **PASS as an offset, FAIL as a pairing** — see §4.1 |
| `def parse_label_set` at BYTE 12134 | 12134 | **PASS** |
| `TOKEN` at BYTE 12025 | 12025 (the `TOKEN = re.compile(...)` definition; 12657 is the `TOKEN.fullmatch(part)` use) | **PASS** |
| `SEPARATORS` at BYTE 12073 | 12073 (the definition; 12567 is the use) | **PASS** |
| generator = 4471 bytes, sha256 `7ccfe69e…` | 4471 / `7ccfe69e52604ec5bb8db423e377cf9f0eb468baf03d0ef7be77b3209654e695` | **PASS** |
| checker = 38009 bytes, sha256 `7a23a522…` | 38009 / `7a23a522871ab5dd33a94ae51b09c70ab182a0d2a53d7380f82bb11a13f3c2d2` | **PASS** |
| the anchors are at the freeze `743ce449` | extracted with `git show 743ce449:` | **PASS** |

`variant_labels` (the function that derives the tool's `VARIANTS` keys, i.e. the other half of the
C2 set-equality) is at BYTE 11160 (`def variant_labels`) / 11164, with the binding-table use at
17179/17196 and the selftest-fixture use at 16978. The landed S396 anchor cell does **not** name
`variant_labels` — a coverage gap in the anchor, not a false statement (the row's scope says "how
one registry cell's N-label set is bound across separators", which `parse_label_set`/`TOKEN`/
`SEPARATORS` do carry).

Cross-check on the emitted bends (the same one-line clause, in the committed artefacts):

```bash
grep -abo '"limine_version": ("' b12.py ; grep -abo '"limine_version": ("' b13.py
diff -u gate.py b12.py | grep -c '^[+-][^+-]'   # gate.py = git show 743ce449:tools/check-limine-pins.py
diff -u gate.py b13.py | grep -c '^[+-][^+-]'
```

```
16931:"limine_version": ("
16931:"limine_version": ("
2
2
```

i.e. in both committed bends the bent clause sits at BYTE 16931 of the file, and each bend differs
from the unchanged gate `7d79ac29…` by exactly one `-`/`+` line pair (the `limine_version` line).

## 3. S397 (docs) — external fetch, HTTP status, length, digest, offsets

```bash
cd $SD
curl -sS -o re.html -w 'http_code=%{http_code}\nsize_download=%{size_download}\nurl_effective=%{url_effective}\n' \
  https://docs.python.org/3/library/re.html
```

Raw output:

```
http_code=200
size_download=257722
url_effective=https://docs.python.org/3/library/re.html
```

```
$ sha256sum re.html
69d64759ed7e269bd617470594dfb8c7970b61fa4def81530a5ea2953d42493b  re.html
$ curl -sS -o re2.html … ; sha256sum re2.html ; cmp re.html re2.html
69d64759ed7e269bd617470594dfb8c7970b61fa4def81530a5ea2953d42493b  re2.html
(cmp: identical — the page is byte-stable across two fetches)
```

The row claims "the 2026-11-08 fetch (257722 bytes, sha256 69d64759…)" → **PASS** (200 / 257722 /
`69d64759ed7e269b…`, both fetches identical).

"Last updated" line of the page, byte-located:

```
$ grep -abo 'Last updated' re.html
257438:Last updated
$ python3 -c "print(open('re.html','rb').read()[257438:257438+46])"
b'Last updated on Nov 08, 2026 (14:27 UTC).\n    \n'
```

The row's anchor claims, re-measured with `bytes.find` on the fetched bytes:

| the row's claim | measured | verdict |
|---|---|---|
| `id="re.fullmatch"` at BYTE 111489 | 111489 | **PASS** |
| "its sentence at BYTE 112171" | `bytes.find(b'If the whole <em>string</em> matches the regular expression <em>pattern</em>, return a')` → 112171 | **PASS on the offset**; the lesson's *quote text* at that offset is a paraphrase — §4.2 |
| the `\b` sentence at BYTE 69787 | `bytes.find(b'Matches the empty string, but only at the beginning or end of a word.')` → 69787, verbatim, 14 words | **PASS** |

The page's rendered sentence at 112171 (tags stripped) is:

> If the whole string matches the regular expression pattern, return a corresponding Match.  Return
> None if the string does not match the pattern; note that this is different from a zero-length match.

— "a corresponding **Match**" (the `re.Match` class), not "a corresponding match object". The
phrase "match object" does occur on the page, but at BYTE 57131, in an unrelated table cell
("when processing match object *m*").

## 4. Findings for the L1 (routed — this seat may not edit `corpus/`)

### 4.1 S396 pairs two different offset units without naming either (needs an amendment-slot wording change)

2615 is the start of the whole `"limine_version": ("…` clause; 3384 is the start of the falsified
value `"12.999999998.4" if`, 19 bytes inside the N13 clause whose start is 3365. The row presents
them as one kind of thing ("generator emission lines at BYTE … and BYTE …"). Both are true offsets
of true things and both point inside the N13 substitution, so no measured claim is falsified — but
a reader re-measuring N13 the way the row measures N12 lands on 3365, not 3384, and QUALITY 141
requires the unit to be named.

Proposed wording (append-only, in the round's amendment slot; the frozen `claims.json` sentence is
untouched — this is the SOURCES row's anchor cell):

> generator emission lines at BYTE 2615 (N12) and BYTE 3365 (N13), each the start of the
> `"limine_version": ("…` clause in the 4471-byte file (sha256 7ccfe69e…); the N12 falsified value
> `"999999998.9.9" if` at BYTE 2634 and the N13 falsified value `"12.999999998.4" if` at BYTE 3384;
> checker `def parse_label_set` at BYTE 12134, `TOKEN` at BYTE 12025 and `SEPARATORS` at BYTE 12073
> of the 38009-byte file (sha256 7a23a522…), all at the round-100 freeze 743ce449

### 4.2 The lesson's S397 located quote is not present at its own offset (routed)

`corpus/lessons/round-100.md`'s Gate block prints, for S397:

> `If the whole string matches the regular expression pattern, return a corresponding match object`
> (BYTE 112171, under `id="re.fullmatch"` at BYTE 111489)

```bash
python3 -c "print(open('re.html','rb').read().find(b'If the whole string matches the regular expression pattern, return a corresponding match object'))"
# -1   (not found)
```

The offset is right; the quoted string is a **paraphrase with a wrong tail** ("match object" where
the page writes "Match"), so it is not a located quote at all — it cannot be re-found at 112171 by
`bytes.find`/`grep -abo`. Replacement, verbatim in the fetched bytes and ≤25 words:
`Matches the empty string, but only at the beginning or end of a word.` (BYTE 69787, 14 words) and
`If the whole <em>string</em> matches the regular expression <em>pattern</em>, return a`
(BYTE 112171, 13 words).

Also in the same cell: the row's teaches sentence says "`\b` asserts a word boundary rather than a
literal character" without the source's in-set branch — the page says at BYTE 39044 that `\b`
inside a set is a backspace character, "not a word boundary as outside a set". The checker's own use
(`re.search(r"\bVARIANTS\b(.*)", cell)`, BYTE 19924) is outside a set, so the claim is true of the
instrument; QUALITY 66 (a teaches cell keeps every branch its quoted source states) wants the
branch named or the sentence scoped to "outside a character set".

### 4.3 S396's teaches cell says "exactly the family" where the measurement gives two families for N12

The round's own target is that the **N12** bend fails **two** families
(`EXPLICIT-VERSION-ECHO`, `REFUSAL-VERSIONS-9DIGIT`) and the **N13** bend one
(`REFUSAL-VERSIONS-9DIGIT-Y`) — the r99 battery sets `check_echo` on the X-cap family (BYTE 79015)
and on the explicit-echo family (BYTE 79893), and both send the `999999999.9.9` spelling. The
landed teaches cell reads "makes exactly the family that asserts that spelling fail" (singular),
which is wrong for the N12 half. Proposed: "makes exactly the families that assert that spelling
fail — two for the X-cap spelling, one for the Y-cap spelling".

### 4.4 Not defects, recorded for completeness

* `S397`'s `used-by` paths `corpus/knowledge/limine-echo-bends-r100.md` (5972 bytes) and
  `corpus/lessons/round-100.md` (7641 bytes) both exist on disk at HEAD, so census `E11` does not
  fire — confirmed by the clean `ok` line of the frozen census run.
* The `re.html` fetch is byte-stable across two fetches (`cmp` identical), so the row's digest is
  reproducible, not a one-off.
* The `recheck` value `180d` and `status mined` on both rows are contract-valid enums; `kind`
  `own-work`/`docs` and `tier A` are in the census enums.

## 5. Census — the frozen command, before and after

```bash
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --root /home/vgpnk/Projects/shokunin tsukuroi
```

**BEFORE-state, re-derived by this seat** (the freeze tree extracted read-only, not copied from the
L1's receipt):

```bash
git archive 743ce449 | tar -x -C $SD/beforestate
bash …/sources-census.sh validate --root $SD/beforestate $SD/beforestate > $SD/census-before-743ce449.txt
grep -cE '^\|[[:space:]]*S[0-9]{3,}' $SD/beforestate/corpus/SOURCES.md
```

```
59 lines total: 57 × W04, 1 × W01, 0 × E-code
beforestate	ok	/fast/scratch/hyaku/tsukuroi-r100/ScoutSources/beforestate/corpus/SOURCES.md
exit=0
395
```

→ **before-state: 395 rows, exit 0.** The tail matches the L1's receipt
(`.ufo/waves/round-100/before/census-before-after.txt`, BEFORE block: `S386` W04, `S387` W04, `ok`,
`exit=0`).

**AFTER-state (HEAD `c450cd68`):**

```
59 lines total: 57 × W04, 1 × W01, 0 × E-code
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
exit=0
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md
398
```

→ **after-state: 398 rows, exit 0**, zero E-codes; the warning profile is byte-identical to the
before-state's (the landing added no error and no new warning). Receipts:
`receipts/census-before-743ce449.txt`, `receipts/census-after-head.txt`.

Note on the L1's receipt: its BEFORE/AFTER blocks are **tail excerpts** of the same 59-line output
(3 lines and 2 lines respectively), not the whole output — the full command prints 57 W04 + 1 W01
every run. The exit codes (0) and the row counts (395 → 398) in it are correct.

## 6. Commands run (exact, in order)

```bash
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
sha256sum -c .ufo/waves/round-100/before/instruments.sha256
git rev-parse HEAD; git log --oneline -12 | cat
git show HEAD:corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -u | tail -3
git show 743ce449:corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -u | tail -3
git show HEAD:corpus/SOURCES.md | awk 'NR==407||NR==408' | awk -F'|' 'NF!=13{print "MALFORMED"}'
git show HEAD:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}'
git -C <scratch> archive 743ce449 | tar -x -C <scratch>/beforestate
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <scratch>/beforestate <scratch>/beforestate
git show 743ce449:tools/make-r100-bends.py > gen.py
git show 743ce449:tools/check-registry-content-r100.py > chk.py
git show 743ce449:.ufo/waves/round-100/before/controls/bends/N12-x-echo.py > b12.py
git show 743ce449:.ufo/waves/round-100/before/controls/bends/N13-y-echo.py > b13.py
git show 743ce449:tools/check-limine-pins.py > gate.py
sha256sum gen.py chk.py b12.py b13.py gate.py
grep -abo '"limine_version": ("999999998.9.9"' gen.py
grep -abo '"limine_version": ("12.999999998.4"'   gen.py
grep -abo '"999999998.9.9" if' gen.py
grep -abo '"12.999999998.4" if'  gen.py
grep -abo '# N12 (echo lies' gen.py; grep -abo '# N13 (echo lies' gen.py
grep -abo '"N12-x-echo": (' gen.py; grep -abo '"N13-y-echo": (' gen.py
grep -abo '"limine_version": ("' b12.py; grep -abo '"limine_version": ("' b13.py
diff -u gate.py b12.py | grep -c '^[+-][^+-]'
diff -u gate.py b13.py | grep -c '^[+-][^+-]'
grep -abo 'def parse_label_set' chk.py
grep -abo 'TOKEN' chk.py; grep -abo 'SEPARATORS' chk.py; grep -abo 'variant_labels' chk.py
grep -abo 'RC-BEND-SPAN' chk.py
curl -sS -o re.html -w 'http_code=%{http_code}\nsize_download=%{size_download}\nurl_effective=%{url_effective}\n' https://docs.python.org/3/library/re.html
curl -sS -o re2.html -w … https://docs.python.org/3/library/re.html
sha256sum re.html re2.html; cmp re.html re2.html
grep -abo 'Last updated' re.html
python3 (bytes.find on re.html: id="re.fullmatch"; the fullmatch dd sentence; the \b sentence; the in-set \b note; Last updated)
```

## 7. Scope note

Source anchors only. This seat did **not** re-run the gate, the r99 battery, the bends, the r100
checker or its selftest, and did not touch `corpus/`, `tools/`, `.ufo/plans/` or
`.ufo/waves/round-100/before/`. Two read-only public-document fetches (no credentials, no network
write, nothing quoted from the environment). `git show` / `git archive` only — no git or jj mutation
of any kind; no commit was made anywhere. Scratch
`/fast/scratch/hyaku/tsukuroi-r100/ScoutSources` deleted before yield.

Tools installed: none — no package needed to be added or upgraded for this seat's work.

```json
{"seat":"ScoutSources","verdict":"findings","notes":"Rows S396/S397 already landed by the L1 in c450cd68 (S399/S400 now free); no duplicate id to be landed. Every landed anchor re-derives byte-exactly at the freeze 743ce449: generator N12 clause BYTE 2615, N13 falsified-value BYTE 3384 (clause start 3365 - unit mismatch, routed 4.1); checker parse_label_set 12134, TOKEN 12025, SEPARATORS 12073, variant_labels 11160/11164/17179; bends' bent clause at BYTE 16931 in both committed bends, one -/+ line pair each vs the gate. S397 external: HTTP 200, 257722 bytes, sha256 69d64759ed7e269b... stable across two fetches, id=re.fullmatch 111489, fullmatch dd 112171, \\b sentence 69787, Last updated 257438. Census frozen command: before-state (743ce449 tree via git archive) 395 rows exit 0; after-state (HEAD) 398 rows exit 0, 57 W04 + 1 W01 both, zero E-codes. Findings routed: (4.1) S396 pairs two different offset units, needs an amendment-slot wording change; (4.2) the lesson's S397 quote is a paraphrase not present at BYTE 112171 (bytes.find -1) and says 'match object' where the page says 'Match'; (4.3) S396 teaches 'exactly the family' but N12 fails two families. corpus/ not edited."}
```
