# ScoutSources — round 100 wave w1 — the two SOURCES rows (S396 own-work, S397 docs)

Full report: `.ufo/waves/round-100/w1/ScoutSources/report.md`.
Row text + Gate-quote block: `.ufo/waves/round-100/w1/ScoutSources/SOURCES-rows.md`.
Receipts: `.ufo/waves/round-100/w1/ScoutSources/receipts/`.

Verdict: **findings**. `corpus/SOURCES.md` was NOT edited by this seat.

## Id collision — S396 and S397 are already landed

At the freeze tip `743ce449` the maximum id was `S395` (`git show 743ce449:corpus/SOURCES.md |
grep -oE 'S[0-9]+' | sort -u | tail -3` → `S394 / S395 / S5`), so S396/S397 were indeed the next
free ids. But the L1's land commit **`c450cd68`** (parent `60b5636f`, the wave-w1 dispatch commit)
landed rows under **both** ids while this wave ran, so at scoring time they are occupied and
`S399`/`S400` are next free (`grep -c` → 0 each). **Do not land a second S396/S397** (ids are never
reused; a repeat is census `E03`). The landed rows are this seat's rows — same subjects, same
anchors, verified byte-for-byte below — so `SOURCES-rows.md` is their provenance/verification
record plus the corrections in §Findings.

## Anchors (byte level on the pinned bytes — QUALITY 141)

`sha256sum -c .ufo/waves/round-100/before/instruments.sha256` → 17 files `OK`, exit 0. The two
measured files, extracted read-only with `git show 743ce449:`:
`tools/make-r100-bends.py` sha256 `7ccfe69e…` (4471 B) and
`tools/check-registry-content-r100.py` sha256 `7a23a522…` (38009 B).

| site | byte | how measured |
|---|---|---|
| generator, N12 emission clause `"limine_version": ("999999998.9.9"` | **2615** | `grep -abo` |
| generator, N13 emission clause `"limine_version": ("12.999999998.4"` | **3365** | `grep -abo` |
| generator, N12 falsified value `"999999998.9.9" if` | **2634** | `grep -abo` |
| generator, N13 falsified value `"12.999999998.4" if` | **3384** | `grep -abo` |
| checker `def parse_label_set` | **12134** | `grep -abo` |
| checker `TOKEN` (definition) / `SEPARATORS` (definition) | **12025** / **12073** | `grep -abo` |
| checker `def variant_labels` (the `VARIANTS`-keys half of the set equality) | **11160** / 11164 | `grep -abo` |
| committed bend `N12-x-echo.py`, bent clause | **16931** | `grep -abo` |
| committed bend `N13-y-echo.py`, bent clause | **16931** | `grep -abo` |

Both committed bends differ from the unchanged gate `7d79ac29…` by exactly one `-`/`+` line pair
(`diff -u | grep -c '^[+-][^+-]'` → 2 per bend).

| external site | value |
|---|---|
| `https://docs.python.org/3/library/re.html` | HTTP **200**, 257722 bytes, sha256 `69d64759ed7e269bd617470594dfb8c7970b61fa4def81530a5ea2953d42493b`, byte-identical across two fetches (`cmp`) |
| "Last updated on Nov 08, 2026 (14:27 UTC)." | BYTE **257438** |
| `id="re.fullmatch"` | BYTE **111489** |
| fullmatch `dd` sentence (`If the whole <em>string</em> matches …`) | BYTE **112171** |
| `\b` word-boundary sentence (`Matches the empty string, but only at the beginning or end of a word.`, 14 words) | BYTE **69787** |
| in-set `\b` branch (`not a word boundary as outside a set`) | BYTE **39044** |

## Census (frozen command, before and after, re-derived)

```bash
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
```

* **BEFORE** (freeze tree `743ce449` extracted read-only with `git archive`): **395 rows, exit 0** —
  59 output lines, 57 W04 + 1 W01, **0 E-codes**.
* **AFTER** (HEAD `c450cd68`): **398 rows, exit 0** — the same 57 W04 + 1 W01, **0 E-codes**.

Receipts: `receipts/census-before-743ce449.txt`, `receipts/census-after-head.txt`,
`receipts/byte-anchors.txt`, `receipts/landed-rows-S396-S397.txt`.

## Findings for the L1 (routed; this seat may not edit `corpus/`)

1. **S396 pairs two different offset units.** "generator emission lines at BYTE 2615 (N12) and BYTE
   3384 (N13)" — 2615 is a *clause* start, 3384 is the *falsified value* 19 bytes inside the N13
   clause (whose start is 3365). Both are true offsets; the pairing is what is wrong, and QUALITY
   141 wants the unit named. Proposed wording (amendment slot, append-only) is in `SOURCES-rows.md`
   §2.1 — it names both units for both bends.
2. **The lesson's S397 located quote is not present at its own offset.**
   `corpus/lessons/round-100.md` prints "If the whole string matches the regular expression
   pattern, return a corresponding match object" (BYTE 112171); `bytes.find` of that string on the
   fetched bytes → **-1**. The page says "a corresponding **Match**" (the `re.Match` class); "match
   object" occurs elsewhere, at BYTE 57131 in an unrelated table cell. Replacement quotes, verbatim
   and ≤25 words: BYTE 69787 (14 words) and BYTE 112171 (13 words).
3. **S396's teaches cell says "exactly the family"** (singular) where the round's own measurement
   gives **two** families for the N12 bend (`EXPLICIT-VERSION-ECHO`, `REFUSAL-VERSIONS-9DIGIT`)
   and one for N13.

Scope: source anchors only — no gate/battery/checker run, no `corpus/` edit, two read-only
public-document fetches, `git show`/`git archive` only, no git/jj mutation anywhere. Scratch
`/fast/scratch/hyaku/tsukuroi-r100/ScoutSources` deleted before yield.

```json
{"seat":"ScoutSources","verdict":"findings","notes":"S396/S397 already landed by the L1 in c450cd68 (S399/S400 now free) - no new id to land; every landed anchor re-derives byte-exactly at 743ce449 (2615 / 3384 / 12134 / 12025 / 12073 / 11160; bends 16931, one -/+ line pair each). S397 external: HTTP 200, 257722 bytes, sha256 69d64759ed7e269b..., stable across two fetches, offsets 111489 / 112171 / 69787 / 257438 / 39044. Census frozen command: before 395 rows exit 0, after 398 rows exit 0, 57 W04 + 1 W01 both, 0 E-codes. Routed findings: S396 mixes two offset units (needs an amendment-slot wording change); the lesson's S397 quote is a paraphrase absent at BYTE 112171 and says 'match object' where the page says 'Match'; S396 teaches 'exactly the family' but N12 fails two families. corpus/ not edited."}
```
