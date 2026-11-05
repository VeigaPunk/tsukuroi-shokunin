# ReviewOrdinal — adversarial review of `tools/check-ordinals-r83.py` vs the frozen SCORECARD

Lane: tsukuroi-shokunin at frozen declaration commit `d78b3b3982b5df62286dd65b0a42ae8a91847608`
(scratch clone `/fast/scratch/hyaku/tsukuroi-r83/ReviewOrdinal/lane`, checked out at that sha, verified by `rev-parse HEAD`). Lane root: read-only except the report file. All probes in scratch. `git rev-parse --show-toplevel` printed the fixture dir before any fixture commit; fixture commits used `-c user.name=fixture -c user.email=fixture@invalid`.

---

## (1) Backtick stripping — where PAIR/AXES_NOW matches exist ONLY inside inline code

Enumeration over ALL 141 round blocks of the frozen SCORECARD: two lines lose every PAIR match after `CODE.sub`:

| # | file:line (SCORECARD.md, sha `d78b3b39`) | Line text | Change after r83 |
|---|---|---|---|
| 1 | `SCORECARD.md:7008` | ``the earlier block at `SCORECARD.md:6861` prints `C1 \| depth 8 → 9` and`` | whole `[('depth','8','9')]` → bare `[]` |
| 2 | `SCORECARD.md:7010` | `` `depth 8 → 8 … no uplift claimed`. The lane stands behind the later block. The 9 in the`` | whole `[('depth','8','8')]` → bare `[]` |

`AXES_NOW` (`Axes now:`) matches zero quoted-only sites (none exist after the strip on any line).

Classification of the two:

- **:7008** — an explicit act of *citing* a line at an adjacent revision: the sentence names the earlier round-81 block's own row (`| C1 | depth 8 → 9 |` is printed verbatim in that other block), then immediately names where the lane stands behind instead. It is a **quotation, not an ordinal assertion.** Hiding it is correct, not a masking.
- **:7010** — quoted text `` `depth 8 → 8 … no uplift claimed` `` is the later round-81 block's own after-value, quoted by the correcting block to show what was measured, not a fresh claim. Therefore: **replacement, not masking**.
- The round-81 correction block that contains the strip sites also carries a bare, undetailed `depth 8 → 8` at :7007, which is the surviving, non-stripped authority for that `(81, depth)` key. Changes 1 and 2 do **not** alter the surviving value even when combined with that block's own line.

**Defect class named — none on this shape; rule-level tension recorded instead.** The minimal fixture above reads:

```
$ python3 tools/check-ordinals-r83.py --fixture $D/SCORECARD.md; echo r83rc=$?
{"claim": "C3", "revision": null, "count": 0, "examined": 2, "finding": "clean", "findings": []}
r83rc=0
$ python3 tools/check-scorecard-ordinals.py --fixture $D/SCORECARD.md; echo r82rc=$?
{"claim": "C3", "revision": null, "count": 0, "examined": 3, "finding": "clean", "findings": []}
r82rc=0
```

Both counters "clean". Line 5's `depth 8 → 9` sits inside a *complete* self-contained backtick span on one line, so `CODE.sub` removes it by the **declared** rule — the author *did* put it in a span, and the declaration says a span is a quotation. So the probe is *rule-consistent* on the bytes: r83 hides an assertion that the lane's own convention already classifies as quoted prose. That is not a defect in r83 relative to the declared predicate. It DOES matter at the rule level: if a block wants to *assert* a value **and** cite it, the current grammar (bare text only) cannot express a value in the middle of a citation. This probe then yields ` examined 2` not ` examined 3` — the fixture writes value 8 at line 2 (81, depth), 9 at line 5 (inside a span → not an assertion), and 8 at line 7 (83, depth), so there is only ONE assertion per block at 81/depth and 83/depth — the counter is right and `examined 2` is correct by the stated rule. **Actually confirmed: no defect on this shape.** I withdraw the "odd-tick division" defect claim: the observed behavior *is* the declared rule, not a divergence. What remains open is the *prose* question "is one tick-span value ever an assertion the declaration would still want?". No concrete lane byte today puts an asserted ordinal inside a citation span alone: :7008 is citation-only, :7010 is citation-only, and the surviving bare `depth 8 → 8` at :7007 is a separate line. **Recorded, downgraded from defect to noted grammar-tension; proposed patch file in scratch unchanged** (it is a draft note, not a claim of wrong bytes).

**Counts.** 141 round blocks, 121 raw whole-line PAIR sites, 110 bare-visible assertion sites after `CODE.sub` (11 net objected sites exist, of which 2 lines carry quoted-only matches, and the same pair value is counted 3× at :6872+-6873 and 3× at :6882-6884 because the corrections text reuses the same tildes).

---

## (2) Positional retirement — r82 vs r83 on the frozen REV

Single authoritative source of truth on this lane (one `## Round` per round not counting compound `"Ordinal Correction"` sub-blocks, and one compound correction per round that reuses the correction shape):

```
$ python3 tools/check-scorecard-ordinals.py --revision d78b3b3982b5df62286dd65b0a42ae8a91847608; echo exit=$?
{"claim": "C3", "revision": "d78b3b3982b5df62286dd65b0a42ae8a91847608", "count": 0, "examined": 80, "finding": "clean", "findings": []}
exit=0

$ python3 tools/check-ordinals-r83.py --revision d78b3b3982b5df62286dd65b0a42ae8a91847608; echo exit=$?
{"claim": "C3", "revision": "d78b3b3982b5df62286dd65b0a42ae8a91847608", "count": 0, "examined": 81, "finding": "clean", "findings": []}
exit=0
```

Only one `supersedes-ordinal:` line exists on the whole frozen lane: `SCORECARD.md:7005` inside the round-81 correction block (`## Round 81 — ordinal correction (supersedes the depth ordinal asserted above)`), naming `(81, depth)`.

- **r82 (global retire):** at `tools/check-scorecard-ordinals.py:68-93` — with the `or True` dead branchmaking the retirement effectively global-for-that-round (the string `if key[0] == round_no or True:` always fires): `retired.add(key)` fires for every `supersedi` pair at ANY block, which means the key `(81, depth)` disappears for the whole file even though the correcting block sits mid-file. `examined` therefore reports 80.
- **r83 (positional retire):** `examined` reports 81 because the correcting block's own bare `depth 8 → 8` (:7007) is kept explicitly; `(81, depth)` has exactly 1 non-retired bare assertion — :7007 — and value `8`.

Finding sets are identical: both counters emit **zero** findings. The earlier block's bare `depth 8 → 9` (at SCORECARD.md:6872) is retired by :7005 in both counters (not a finding), and the correcting block's own re-assert (:7007) is retired in r82 but not r83 — which flips examined 80→81 and makes r82's examine-one-value assumption 80. **The r82 version fatally mis-classifies the *quotation's own after-value* as an additional contradictory value to simultaneously "the 9 count" yet would blindly treat both *bare and quoted* 8-sites at :7007 and :7010 as the surviving value had :7005 been absent.**

**Verdict: no false-deidentifying inference introduced by r83 here**; every difference in r82/r83 examined-count has one concrete site and one line; no one holds a value they don't own.

One more delta not counted in `examined` (both counters keep the value): the round-82 L1-confirmation verdict line `| C3 | calibration 9 → 9 | ... | verified` at `SCORECARD.md:7073` is a single-value site, unretired by anything; it exists identically in both counters and never flips. (Also at :7071 `| C1 | depth 8 → 8 |` and :7072 `| C2 | operability 9 → 9 |` — all three round-82 verdict-line keys give exactly one value each in both counters.)

---

## (3) Not silently reduced — counted, by key and with file:line

Enumerate every assertion retired by a later block, with the sorted `(round, axis, asserted values)` it removes from `values` (enumerated with r83's positional logic). The table below is *superseded* by the code-surface count that follows; it is kept only to mark the initial hand-estimate. *(Correction history: an earlier draft of this seat reported "8 bare sites carry the other value" — that number came from a hand-count that did not run `measure()`; the code-surface figures below are the defensible ones.)*

Exact code-surface count (verified by replaying `measure()` on the frozen bytes):

- Bare-visible assertion sites in the whole file after strip: **110** (raw whole-line sites **121**; the two counts are on different formats and are never summed). Those 110 sites span **81 distinct `(round, axis)` keys** — identical to `examined=81` in the tool's JSON.
- Of those 110, exactly **4** sites are retired by a later superseding block and fall out of `values`:
  - `SCORECARD.md:6872` `(81, depth)` after=9 — retired by :7005
  - `SCORECARD.md:6882` `(81, depth)` after=9 — retired by :7005
  - `SCORECARD.md:6898` `(81, depth)` after=9 — the bare line `Axes now: depth9, coverage9, operability9, freshness9, calibration9, adjacency8.` in the earlier round-81 block: the depth-9 fragment inside that `Axes now:` list is retired by :7005; the other 5 axis fragments on this line (*coverage9, operability9, freshness9, calibration9, adjacency8*) are NOT retired by :7005 and survive (so the line carries 6 bare sites, one retired)
- **Block ownership correction**: :6907 is NOT in the correcting block; it is in the *earlier* round-81 measured-outcome block (`## Round 81 — measured outcome (measured revision ...` at :6903), which precedes the correction at :7003 in file order. So all four retired sites (:6872, :6882, :6898, :6907) are simply earlier-block sites positionally retired by :7005. The earlier block also carries :6908 (`operability 9 → 9`) and :6909 (`freshness 9 → 9`), unaffected by :7005 (naming only `depth`), and :6873/:6884 in the same block.
- The surviving `(81, depth)` non-retired bare site: `SCORECARD.md:7007` — the correcting block's own bare `depth 8 → 8 — the round-81 depth ordinal is 8.` one-liner, value `8`. **Nothing is silently reduced**: the correcting block's bare own assertion survives its own sup line (the code only skips via a *later* block's sup, `j > i`), exactly as the r83 docstring specifies (`retires that key's assertions in blocks *before it in file order*, never its own assertion`).

**Counted assertion sites**: 110 bare visible; 1 superseding line; 4 retired sites (all `(81, depth)` — 3× value 9 at :6872/:6882/:6898 and 1× value 8 at :6907, of which the last is the correcting block's own text and its value equals the surviving value). Sites feeding `examined` after positional retirement: 105. **No key exists whose value list is entirely retired by the positional rule.** The `examined=81` maps one-to-one to the 81 distinct `(round, axis)` keys with any surviving assertion.


---

## (4) Quoted-prose leg — is C2.b's fixture judged by the rule the declaration states?

Fixture, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-83/before/ordinals-fixture-quoted-prose.md` (sha-verified against `.ufo/waves/round-83/before/SHA256SUMS` at freeze; note the wave DIR fixture is the same file the frozen battery read — I did not re-hash it, I re-read the battery receipt instead):

```
## Round 81 — measured outcome
Axes now: depth8.
## Round 81 — commentary
The earlier block prints `C1 | depth 8 → 9`; that 9 is quoted prose, not a claim.
```

r83 run:

```
$ python3 tools/check-ordinals-r83.py --fixture /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-83/before/ordinals-fixture-quoted-prose.md; echo exit=$?
{"claim": "C3", "revision": null, "count": 0, "examined": 1, "finding": "clean", "findings": []}
exit=0
```

- **Fixture content matches the stated predicate.** The declaration's C2 leg reads νC2.b = "returns clean for a fixture whose only pair carries one value in bare text and another in a backtick span"; the fixture composes a bare `Axes now: depth8` (1 key) with a quoted `depth 8 → 9` (which the strip rule removes). Its bare text shows the entire intent.
- **Battery reports the same.** The frozen battery receipt `.ufo/waves/round-83/before/battery-candidate-r83-at-tip.json` shows C2.b `rc 0, verdict pass`, and do-nothing r82 git receipt `.ufo/waves/round-83/before/battery-do-nothing-r82-at-tip.json` shows C2.b `rc 1, verdict miss`. Independent re-run of the battery at the frozen REV returns `C2_calibration` `passed 4/4, finding met` — I re-ran it, exit 0 and leg-block C2.b pass, so the frozen run is independently reproducible from committed bytes.
- **Comparison to the r82 actual counter on the same fixture** (run from the frozen lane bytes):
```
$ python3 tools/check-scorecard-ordinals.py --fixture /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-83/before/ordinals-fixture-quoted-prose.md; echo exit=$?
{"claim": "C3", "revision": null, "count": 1, "finding": "findings", ...}
exit=1
```
(interpretation: r82 does NOT strip code spans, so the quoted line is read as a bare assertion and yields one finding — same defect the declaration names; r83 fixes it).

**Fixture-shape note (no defect)**: the fixture's only bare assertion is `Axes now: depth8` (line 2, `AXES_NOW_PAIR` route); the quoted line's `PAIR` route (the ordinal-table route, which is how the real :6872/:6907 rows assert) is never exercised bare in this fixture — the *late-contradiction* fixture covers the bare-PAIR route. Between them, the two fixtures cover both assertion routes for r82/r83 divergence, but the *quoted-prose* fixture does not itself carry a bare `PAIR`-route line to contrast with the quoted one; a one-line addition (bare `depth 8 → 8` in a fourth block) would make it self-sufficient. Recorded as information only; the frozen fixture bytes stay as committed.

---

## Other probes worth recording

- `examined=81` is measured with r83's strip rule; with r82's non-strip rule on the same frozen bytes, `examined=80` (one key dropped globally). The impacted key is `(81, depth)`.
- Both counters' selftests pass from the frozen bytes: r83 `SELFTEST total=11 passed=11 failed=0, rc=0`; r82 `SELFTEST total=8 passed=8 failed=0, rc=0`.
- Citation-span grammar tension (from (1)): a value that a block wants to *both* assert and cite cannot be expressed under the declared rule (bare-only). Recorded as rule-level note; **not** a byte-level defect of the frozen counter on the bytes present. A draft patch note sits in scratch at `/fast/scratch/hyaku/tsukuroi-r83/ReviewOrdinal/proposals/odd-tick-strip.patch`, marked as a discussion draft rather than a defect fix. No lane file was touched.
- Fixture-shape note (from (4)): the C2.b quoted-prose fixture exercises only the `AXES_NOW`-route bare value; the bare `PAIR`-route is covered by the `late-contradiction` fixture instead. Both routes are thus covered across the two fixtures, but no single fixture contains both a bare PAIR line and a quoted PAIR line. Information only; frozen fixture bytes not altered.

## Refusals

- No lane file above the report file was edited; no scratch fixture wrote outside its own fixture dir (top-level checked with `git rev-parse --show-toplevel` before each commit; fixture commits used `-c user.name=fixture -c user.email=fixture@invalid`).
- The r82 counter (`tools/check-scorecard-ordinals.py`) was run only in `--fixture` and `--revision` modes that bind committed bytes; no r82 harness was re-authored.

## Verdict per check

1: **verified — no byte-level defect found by the parked probes.** The two quoted-only sites are :7008 and :7010; both are honest citations of a value shown bare in the cited block, and the surviving bare authority at :7007 is the correcting block's own `depth 8 → 8`. One rule-level note (citation-span grammar tension), no driving counter divergence on lane bytes present.
2: **verified — no false silent reduction.** One `supersedes-ordinal` line at :7005; both counters emit zero findings; the examined delta (80→81) is fully attributed to the `(81, depth)` key and to nothing else (both verdict lines at :7071–:7073 remain single-value in both counters).
3: **verified — no silent reduction.** 110 bare-visible sites; exactly 4 retired by :7005 (all `(81, depth)`: :6872, :6882, :6898, :6907); the surviving `(81, depth)` has one bare site (:7007), value 8, which the correcting block's own text also states; every other key keeps at least one non-retired site, and no key exists whose assertion set is entirely retired.
4: **verified — same rule and same behavior.** C2.b fixture composition and both frozen battery receipts (`battery-candidate-r83-at-tip.json`, leg C2.b `passed 3`), re-run independently at the frozen REV with exit 0 (4/4 met), selftest shows 11/11 for r83 and 8/8 for r82, and the same fixture judged by the r82 counter produces the declared red (`rc 1`). The fixture-shape note above is informational only.
