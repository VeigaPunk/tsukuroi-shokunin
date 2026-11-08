# S395 candidate — SOURCES row (contract v1, CORPUS.md § "SOURCES.md — where a shokunin learns")

Draft only. `corpus/SOURCES.md` was NOT edited by this seat. Column order is the contract v1 order:
`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.

## 0. ID collision — read this first

**`S395` is already taken in the working tree.** `corpus/SOURCES.md` line 406 (working tree, uncommitted
at this seat's measurement) already carries an `S395` row for this round's subject; `git show
HEAD:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S395[[:space:]]*\|'` → **0** (it is new in the
round's uncommitted tree, landed by the round's own scribe seat).

I re-measured every anchor the existing row claims and **all of them reproduce byte-exactly**:

| existing row's anchor claim | my independent byte measurement | verdict |
|---|---|---|
| `def meta_ok` at BYTE 99305 (line 2179) | 99305 / line 2179 | agrees |
| echo assertion at BYTE 99430 (line 2181) | 99430 / line 2181 | agrees |
| era assertion at BYTE 99523 (line 2183) | 99523 / line 2183 | agrees |
| five `c.check_echo = True` sites (79015, 79893, 81666, 83173, 84390) | 79015, 79893, 81666, 83173, 84390 | agrees |
| five `c.check_era = True` sites (79039, 80414, 81690, 83197, 84414) | 79039, 80414, 81690, 83197, 84414 | agrees |
| the two new `LIE_KINDS` members at BYTE 108455 (line 2370) | `"limine-version"` 108455, `"visibility-era"` 108473, both line 2370 | agrees (the second member's own offset 108473 is not named in the row) |
| gate emits the asserted fields at BYTEs 16931 and 17037 | 16931 / 17037, lines 316 / 318, MAIN return | agrees |

So the existing `S395` row is **grounded**: every offset in its anchor cell was reproduced on the
pinned bytes with `bytes.find` / `grep -abo`. Nothing in this seat's findings falsifies it.

**Decision for the L1:** do **not** land a second row with id `S395` (ids are never reused, contract
v1). The row already in the tree is correct. This seat's candidate is therefore written in two
parts: (a) the **candidate as specified** for the round, for the L1 to take as-is *if* it wants a
wider scope than the landed row — in which case it must take a **new id (S396)**, not S395 — and
(b) a **suggested append-only correction** to the landed `S395`'s anchor cell, which is NOT
append-only-safe under contract v1 rule 2 (only `status`, `recheck`, `used-by` change in place),
so the correction must be a superseding row, again under a new id.

## 1. The candidate row (as specified by this seat's brief)

If the round wants a row whose scope is *the gate's reported metadata AND the battery's assertions
on it* — wider than the landed S395's battery-only scope — it takes the next unused id **S396**:

```
| S396 | tsukuroi limine-pins gate and the r99 battery's assertions on it (`tools/check-limine-pins.py` + `tools/limine-pin-battery-r99.py`, own-work) | own-work | A | the gate's reported metadata (`limine_version`, `limine_version_source`, `visibility_era`) and the battery's assertions on it | the gate's MAIN return emits `"limine_version"` at BYTE 16931 and `"visibility_era"` at BYTE 17037 (lines 316/318), the CANNOT-EVALUATE early return's copies at BYTE 11230 / 11344 (lines 200/202), gate sha256 7d79ac29…; the battery's `def meta_ok` at BYTE 99305 (line 2179), echo assertion at BYTE 99430, era assertion at BYTE 99523, battery sha256 c2e8c8fc… | A family certifies a reported field only if it reads that field on its own cases: a case whose pins are right but whose `limine_version` or `visibility_era` is wrong must read unmet, and the battery's selftest needs a lie kind per field or an assertion removal is invisible. | queued | 2026-11-08 | 180d | — |
```

(If this row is landed as `S396` it must open with `supersedes S395 — ` in `teaches`, per contract
v1 rule 2, and S395's `status`/`used-by` move to `queued` / `—` with the old→new logged in the
round lesson. This seat does not make that choice; it is the L1's.)

### Anchor-by-anchor groundings for the candidate (each ≤25 words)

| anchor | located quote (≤25 words) | byte | line |
|---|---|---|---|
| gate MAIN return, `limine_version` | `"limine_version": limine_version,` | 16931 | 316 |
| gate MAIN return, `visibility_era` | `"visibility_era": "12.9.5+" if era_b else "pre-12.9.5",` | 17037 | 318 |
| gate early (CANNOT-EVALUATE) return, `limine_version` | `"limine_version": limine_version,` | 11230 | 200 |
| gate early (CANNOT-EVALUATE) return, `visibility_era` | `"visibility_era": "12.9.5+" if era_b else "pre-12.9.5",` | 11344 | 202 |
| battery `meta_ok` definition | `def meta_ok(c, got):` | 99305 | 2179 |
| battery echo assertion | `if c.check_echo and not (got[8] == c.version and got[9] == "flag"):` | 99430 | 2181 |
| battery era assertion | `if c.check_era and got[10] != ("12.9.5+" if c.era_b() else "pre-12.9.5"):` | 99523 | 2183 |
| battery X-cap family echo site | `c.check_echo = True` | 79015 | 1775 |
| battery X-cap family era site | `c.check_era = True` | 79039 | 1776 |
| battery Y-cap family echo site | `c.check_echo = True` | 81666 | 1817 |
| battery Y-cap family era site | `c.check_era = True` | 81690 | 1818 |
| battery new lie kind `limine-version` | `"limine-version", "visibility-era")` | 108455 | 2370 |
| battery new lie kind `visibility-era` | `"limine-version", "visibility-era")` | 108473 | 2370 |

Word counts of every quote above: 3–12 words, all under the 25-word cap.

### Grounding of the `teaches` sentence (one grounded learner benefit)

The `teaches` sentence has two halves, each grounded on the bytes above:

1. *"a family certifies a reported field only if it reads that field on its own cases"* — grounded
   on the ten `c.check_echo = True` / `c.check_era = True` sites (the battery's own opt-in switches)
   and on `meta_ok`'s two assertion lines, which are the only code that reads `got[8]`/`got[9]`
   (`limine_version`, `limine_version_source`) and `got[10]` (`visibility_era`) — the tuple indices
   are read from the gate's JSON at battery lines 2172-2173.
2. *"the battery's selftest needs a lie kind per field or an assertion removal is invisible"* —
   grounded on `LIE_KINDS` at BYTE 108277 (line 2369): the r98 battery's tuple has 12 members, none
   of them `limine-version`/`visibility-era`; the r99 battery's tuple has 14, with the two new
   members at BYTE 108455 / 108473 (line 2370), and the lie-application branches at BYTE 107815
   (line 2356) / 107920 (line 2359).

## 2. Re-open of the lane's existing EXTERNAL row S392

`https://docs.python.org/3/library/functions.html#int` — **re-open, identical, no drift.**
Measured: HTTP 200 after the 301 to `https://docs.python.org/3/builtins/functions.html`;
331022 bytes; sha256 `d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7` — the
r98 pin's digest and length exactly. The three pinned offsets re-measured on the fetched bytes:
`have leading zeros, be surrounded by whitespace` at **157767**, `id="int"` at **153202**,
`disallows leading zeros` at **159315** — the row's three offsets, unchanged.

Receipt: `receipts/04-s392-reopen-and-config-reject.txt`.

## 3. Rejection candidate for the Gate block

`https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md` — **reject.**
HTTP 200, 27609 bytes, sha256 `f44f3a19133cb3dc14d6d8b402ed585feb98a36bc4b263c37aa92f621f603763`
(byte-identical to the r98 measurement). `grep -c` for `limine_version` → **0**, `visibility_era` →
**0**, `echo` → **0**, `version` → **0**. The page documents Limine's config keys and values, not
the gate's JSON report fields; it grounds none of this round's propositions. A rejection is
evidence of taste and is kept as a rejected row, not a mined one.

Receipt: `receipts/04-s392-reopen-and-config-reject.txt`.
