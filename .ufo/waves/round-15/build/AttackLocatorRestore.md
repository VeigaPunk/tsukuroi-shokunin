# AttackLocatorRestore — critic, C1/depth

Target: `tools/check-locator-clarification.py`, sha256 `773e31d8…2015` (581 lines at the
final read; it was 536 lines at the first read, but `LOC_NUM`/`QLOC`/`locator_sites` at :31-35,90-91
were byte-identical in both). Verdict: **fixable defect, blocks the admit of "restored renderer
numbers fail"**. The selftest restore cases (:489-493) do fail on the number, not on a missing token:
the heading tokens stay and the expected set is exactly `{LOCATOR_UNQUALIFIED}`, count 1.
That credit is real. But both fixtures use the one weakest form, a bare `rendered lines 1266-1267`
with no qualifier. Any qualifier word next to the number makes the restore pass.

## Counterexamples (regexes copied verbatim from :31-35,80-91 into a scratch probe; tool not run)

| # | Restore site / string | LOC_NUM | flagged |
|---|---|---|---|
| A1 | MD15: `Source object: S046, https://man.archlinux.org/man/systemd.exec.5 § SANDBOXING > ProtectSystem=, rendered lines 1266-1267, page footer systemd 262.1.` (r14 sentence + URL) | hit | **no** (QLOC `man\.archlinux\.org`) |
| A2 | MD15: `Active locator: rendered lines 1272-1273 in the closure reader.` | hit | **no** (`reader`) |
| A3 | MD15/JSON replacement, one sentence: `…1266-1267 are withdrawn; the active locator is rendered lines 1272-1273.` | hit | **no** (`withdraw`) |
| A4 | MD15 frontmatter `source: … man.archlinux.org…, rendered lines 1266-1267;` | hit | **no** |
| A5 | MD15 QUALITY table cell `rendered lines 1266-1267` (period-free table merges with neighbouring rows that say "superseded") | hit | **no** |
| A6 | MD15 or JSON `location`: `lines1266-1267` (the verifier lesson's own form, :234), `at 1266-1267`, `line 1272`, `lines 1272—1273` (em dash), `lines 1266 to 1267`, `L1266-L1267`, U+2011 hyphen, `.txt render 1395-1396` | **miss** | **no** |
| J1 | JSON15 `location` with qualifier: `…, rendered lines 1272-1273 (closure reader)` | hit | yes (no QLOC on location; good) |
| J2 | JSON15 extra keys (`anchor`, `sources[].anchor` copying r14's shape, numeric `rendered_lines:[1266,1267]`), or LOCATOR `quote` | never read | **no**: there is no key-set check, and only `location`/`replacement` are scanned (:146,166) |
| J3 | JSON14 `r15_supersession.notices[R15-LOCATOR].active_locator = "SANDBOXING > ProtectSystem=, rendered lines 1272-1273"` | never read | **no** (:255-259 checks heading tokens only) |

Each of A1–A6, J2 and J3 restores a renderer number in **one** file while the other file stays clean.
I expect each to give PASS with count 2 [INFERENCE from the regex probe plus a static read of the
count logic at :332-345; the checker was not executed]. Controls: the baseline r14 bytes at
`0db618a` are flagged at all three real loci (MD:34 sentence, JSON `corrections[0].location`,
`sources[0].anchor`). So baseline identification holds, and the gate now requires the notice to name
both `corrections[0].location` and `sources[0].anchor` (:258).

## Why qualification cannot be the exemption (reopened 2026-10-20, curl, HTTP 200)

The same definition sits at four different line numbers depending on the reader:
- r14 reader: 1266-1267.
- Round-14 closure reader: 1270 and 1272–1273 (lesson :234-236).
- `https://man.archlinux.org/man/systemd.exec.5.txt` (sha256 `08d00c43…c751`, 5005 lines): `ProtectSystem=` at :1395, definition at :1396.
- The HTML (sha256 `26f9a182…5043`, 293394 B): `<i>ProtectSystem=</i>` at :1359, definition at :1360-1361.

Other facts from the reopen:
- Footer: `systemd 262.1` (HTML :4970, txt :5005).
- The exact quote occurs once in the .txt; `SANDBOXING` is at txt :1366.
- The HTML has no `id` containing sandbox or protect, so there is no stable URL fragment.
- No renderer identity is pinned by a digest, so naming the reader does not make a number reproducible.

ActiveRefs' notice adds a renderer rule: "Any future line number must name the reader or renderer"
(r14 JSON `r15_supersession.notices[0].renderer_rule`; same in the r14 MD R15 section). That rule
endorses A2. It contradicts the contract's "no renderer-dependent line number in new location"
and the instruction "Do NOT rely on bare reader line numbers".

## Impacted axes

- **depth:** the C1 claim that "restores fail" would be admitted on a vacuous predicate.
- **calibration:** a green selftest would overstate what the gate enforces.
- No other axis is touched.

## Smallest safe correction (one file: LocatorGate's checker)

1. **Zero-digit rule for locator fields, with no qualifier exemption.**
   - Scope: every JSON15 `location`; recursively, any key matching `location|anchor|active_locator|line|render` in JSON15 and in JSON14 `r15_supersession`; MD15 lines starting `source:`, `Location:`, `Active locator:` or `Source object:`.
   - Before testing, strip these allowed tokens: `systemd.exec(5)`, `systemd \d+(\.\d+)*`, ISO dates, `S\d{3}`, `R1\d`, the exact URL.
   - Any `\d` left over → `LOCATOR_UNQUALIFIED`.
2. **Number rule for prose (MD15 whole text, JSON15 `replacement`).** Drop the sentence-level QLOC exemption.
   - Match: `(?:\blines?|\bll\.|\bL)\s*\d{3,}` or `\b\d{3,5}\s*(?:[-\u2010-\u2015\u2212]|to)\s*L?\d{2,5}\b`, after first removing ISO dates and repo pointers `[\w./-]+\.(?:md|json|py|sh):\d+(?:-\d+)?`.
   - Allow only the exact `1266-1267` when a withdraw/supersed/"not a locator" word appears within its own clause (split on `;`).
   - Any other number fails. Current `LOC_NUM` also flags prose like "lines 233-239" (a repo-lesson pointer), so the pointer form needs this exemption.
3. **Exact key set** `{id, source_id, url, location, quote, replacement, supersedes}` per correction.
   Any extra key in a correction, or any top-level `sources`/`anchor` value, gets rule 1.
4. **Selftest additions:** one-file fixtures A1, A2, A3, A6 (`lines1266-1267`), J2 (`sources[0].anchor`) and J3.
   Each expects exactly `{LOCATOR_UNQUALIFIED}`, exit 1, count 1. Add PASS controls carrying a repo pointer `…spotcheck.md:233-239`, a date and footer `262.1`.
5. **Integration note for L1:** the renderer rule in the r14 notice should become "line numbers are not
   locators", or the gate will contradict it. LocatorEntry was advised: no 1270/1272-1273 in the new
   pair (cite the lesson pointer instead) and no extra JSON keys.

## Sources / limits

- Read: AGENTS.md; r14 verifier lesson :233-246; the checker at both sizes; r14 MD/JSON at HEAD and
  `0db618a`; working-tree notices; `check-source-scope-correction.py`; SOURCES S044/S046 rows.
- Scope boundary: the new r15 MD/JSON pair did not exist at review time. These findings are about
  the predicates, not about the delivered pair.
- Not run: the checker, its selftest, census, builds or formatters. I make no pass claim.
- The regex probe is research on copied literals. It does not execute the gate.
- Messages sent to the exact seats TsukuroiR15.LocatorGate and TsukuroiR15.LocatorEntry.
- Tools installed or updated: **none**. curl/sha256sum/grep wrote only `/tmp/alr-systemd.exec.5.{html,txt}`.
