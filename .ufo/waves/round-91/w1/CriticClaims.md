# CriticClaims — R91 w1 attack on the declaration

Seat: CriticClaims. Lane: tsukuroi-shokunin, measured at b516d6ae (working tree gate dfc63548…; see 9).
Axes under attack: operability (C1 surface: V1 visibility + U1 reporting) and depth (C2 entry).
Each item: severity / evidence / smallest safe correction. All forgeries live in
`.ufo/waves/round-91/w1/CriticClaims/gates/`; measured receipts in `.ufo/waves/round-91/w1/CriticClaims/`.

## Findings

**1. [falsifies] Declaration literal numbers do not bind to the frozen battery — QUALITY 104.**
Evidence — `SCORECARD.md:7627-7635` (Round 91 declaration, as committed at freeze d3b0987):
Instrument sha `8f0daee8…` is the **r90 battery's** sha
(`git show 40efa4ea:tools/limine-pin-battery-r90.py | sha256sum` → `8f0daee82b9d…`, matches);
"for each of the 78 families … 78 of 78 families … below 78/78" states 78.
Frozen battery at d3b0987 is 82 families (`FAMILY_ROSTER` 82 entries; battery selftest at HEAD:
`roster-literal PASS families_passed=82`, full `--selftest` 5/5 rc=0); freeze sha is `655ee8f3…`.
Delta check: `git diff d3b0987 HEAD -- tools/limine-pin-battery-r91.py` touches only
`fam_unverified_sorted` + `u1_ok` (no roster change: 82→82). Control receipts read 82
(`runs-canonical/K1-landed-gate.txt`: `families_passed 2/82`), measured receipts read 82/82.
So the declaration's Instrument sha and 78-count describe an instrument that was not frozen;
QUAL​​ITY 104 (every literal count binds to a committed receipt line; named inputs exist at the
freeze revision) fails on two numbers. Smallest correction: amend the declaration row in place to
`655ee8f3d0942e958cc853deb2d16abcd2d16ae2823ca6548f2a53991b4901b9`, `82 of 82`, `below 82/82`, with a
pointer to `FAMILY_ROSTER`/`run_battery` and the freeze manifest line; do not re-freeze the battery.

**2. [falsifies] K2 is a broken control, not a do-nothing — QUALITY 126(a).**
Evidence — `.ufo/waves/round-91/before/controls/gates/K2-landed-adapter.py:329-330` registers
`--tpm-present` twice (both `add_argument` lines present); every case crashes:
`argparse.ArgumentError: argument --tpm-present: conflicting option string`. By my count of both
committed receipts: canonical 984/984 `error:` cases, clone 984/984. QUALITY 126(a) requires a
forgery control to "reach a verdict for the reason it names"; rows that are `error:` are counted
separately, not as rejection evidence. K2 currently proves nothing about the adapter; it names packs
as rejected when the battery only saw a crash. (K1 is valid: 0 error cases, 2/82×3 in both layouts.)
Smallest correction: fix `make-controls.py` K2 patch to not duplicate `--tpm-present` (landed gate
already has it), regenerate K2, re-run both layouts, replace its receipt; count its real failure
families separately (N-style). Do not let the declaration cite K2 until then.

**3. [falsifies, cheap control] F3 reaches the target while skipping r91 work — the battery cannot see "no sort".**
Evidence — `gates/F3-unsorted.py` = HEAD `tools/check-limine-pins.py` with the single deletion
`unverified.sort()` → `# forgeries: no sort`. Run: `families_passed 82/82 verdict met` ×3 rc=0
(`.ufo/waves/round-91/w1/CriticClaims/F3.json`). Root cause in the frozen battery: `u1_ok()`
(tsukuroi-shokunin battery lines ~1672-1685) does `got_sorted = [int(x) for x in got_list]; return got_sorted == want and got_sorted == sorted(got_sorted)` — it sorts the gate's answer before comparing, so a gate that returns set-iteration order passes when the set already happens to sort. N08 demonstrated the same blind spot at freeze (its pre-fix reverse patch lost, `git diff d3b0987 HEAD -- .ufo/waves/round-91/before/controls/gates/INDEX.tsv` shows N08 expected killers widened) and was repaired in the flight path (commit `203b3872` "fix N04/N08/N10…, add unverified.sort()" + `1652b086` "strengthen…fix u1_ok"), but the HEAD tree still ships F3's met despite the repaired families reading the same `u1_ok` for other families — the repair covered only the family that draws order, not the general case. Smallest correction: freeze `u1_ok` to compare raw order (`[int(x) for x in got_list] == want` with `want` sorted) before any re-score, and add one committed control whose only defect is the missing sort (F3 itself, relabelled as that control), requiring it to read `unmet` 3/3.

**4. [falsifies, cheap control] F2/F2-oracle-import: importing the battery oracle is *legitimate* under the frozen predicate, and comes within 2 families of target.**
Evidence — `gates/F2-oracle-import.py` (18 lines): `importlib` loads `tools/limine-pin-battery-r91.py` as `bat91` and `tools/check-limine-pins.py` as `gate`; it executes the *gate's own* `check()` — i.e. no oracle is used. F2-oracle-replay (`gates/F2-oracle-replay.py`) goes the other way: it re-derives pins/on_panic/unverified by calling the battery's oracle primitives (`r1_key`, `resource_name`, `b2`, `VALID_RESOURCES`, `EFI_PROTOCOLS`) and `Case` semantics while skipping gate logic; also 80/82 in my runs (fails MEASURED-TPM0, SECUREBOOT, is unmet). Crucially, both read 80+/82 ×1 and at least one path overruns the cheapest possible forgery the spec asks about: no gate needs to import the battery *only for constants* to pass — the honest candidate already passes 82/82×3 at HEAD (candidate receipt, my run `families_passed 82/82` rc=0). The honest-import question is settled by the frozen predicate: the battery's `run_gate()` (lines ~1634-1655) runs the gate as a *subprocess* with cwd set to the fixture dir, reading only argv/stdout; CASE oracle methods (`want_unverified`, `r1_first_visible`, `r9_image_lines`, `r8_entries`) are executed inside the battery to build expectations, never handed to the gate. So an oracle import is a legitimate implementation of the frozen rules *iff* it reuses the source-backed constants (parse rules, resource set), which is exactly what "implements R1-R10/V1/U1" means — the battery's helpers *are* the frozen rule set; there is no epistemic channel that distinguishes "imported oracle" from "copied rule set". Smallest correction: record this as a note, not a kill rule: the declaration's "Separable" sentence is defensible, but the lane should list the oracle-import as a *legitimate* forgery control (passes only when it also implements the rules) — it does not reach 82/82×3, so it stays a non-control. No predicate change needed.

**5. [weakens] F1 (r90 gate + thin regex wrapper) reaches 74/82×1, capped by first-path and non-efi regex errors.**
Evidence — `gates/F1-regex-wrapper.py` (K1 source + one-patch: `unverified_image_lines` from a `path:`-without-`#` regex, `on_panic` from a whole-file `measured_boot: yes` regex, `LP-UNRESOLVED→LP-BAD-RESOURCE` relabel): run reads 74/82 (fails GLOBAL-VS-ENTRY, MEASURED-IN-ENTRY, NO-PAREN, PANIC-AFTER-PIN, UNHASHED-DECOYS, UNVERIFIED-IMAGE-PATH, UNVERIFIED-NON-EFI, UNVERIFIED-SORTED). The wrapper dies exactly where a genuine implementation must track R9 structure: first-`path`-else-`image_path` (UNVERIFIED-IMAGE-PATH), efi-only scoping (UNVERIFIED-NON-EFI), sorted order (UNVERIFIED-SORTED), and V1 global-section visibility (GLOBAL-VS-ENTRY, PANIC-AFTER-PIN, MEASURED-IN-ENTRY). No regex on raw lines survives those families — the wrapper would need to reimplement R1/R9, at which point it *is* the implementation. Smallest correction: none needed; F1 confirms the battery's anti-cheat bite on the claimed surface.

**6. [weakens] N01 and N10 are byte-identical gates — the "FIRST visible" clause has no independent control.**
Evidence — `sha256sum` of `.ufo/waves/round-91/before/controls/gates/N01-panic-whole-file.py` and
`N10-panic-first-anywhere.py` are both `7e158cd2e3249c7b4a6d31bf86fecb7a8e88f7388597fdc9e49774e5753f6489`
(`diff` reports identical). `make-controls.py` NEAR defines both with the same single patch
(`if in_global and key == "hash_mismatch_panic" …` → `if key == …`), so N10's disclosure
("FIRST visible in global section") is not actually implemented: there is no control that reads
`hash_mismatch_panic` whole-file-but-first-wins globally *with* correct global-section `hash_mismatch_panic` entry-label handling separated. QUALITY 125 clause-map conformance: the declaration's "each bends one r91 clause" needs 12 distinct bends; there are 11 gates, and N10 merely duplicates N01. Smallest correction: rewrite N10 to bend "FIRST" while keeping V1 scope (e.g. LAST-visible-wins globally, or first-over-whole-file minus the global-section cut) so it fails only under PANIC-GLOBAL-ONLY/GLOBAL-VS-ENTRY and passes when the clause is bent elsewhere.

**7. [weakens] QUALITY 125 clause map: R1–R8 carry no per-clause killer column in the declaration.**
Evidence — the declaration table names R1-R8/R4/R6/R7/R9/R10/V1/U1 in the Instrument line but lists only "R1-R8 (r87) with r90's R4/R6/R7/R9/R10 and the r91 visibility rule V1" with no clause→family table; QUALITY 125 requires one line per clause naming the certifying family or `uncertified`. V1/U1 are covered (N01/N02/N03/N04 + U1 five), R9/R10 are covered by r90 families, but R1–R8 are covered only implicitly by the 82-family roster. Smallest correction: append the clause table to the landing record (or a follow-up round lemma) with one line per clause; mark any genuinely uncertified clause `uncertified` and repeat the count in the verdict sentence, per QUALITY 125.

**8. [weakens] QUALITY 104 second half: the freeze manifest under-covers its own input set — the battery is not in it.**
Evidence — `.ufo/waves/round-91/before/freeze-manifest.sha256` has 13 lines (census-start, K1 gate, host receipt, new-ground-sweep, src/*×9); it omits `tools/limine-pin-battery-r91.py` itself (`sha256sum -c` passes trivially), and it was *not* regenerated after commits `203b3872`/`1652b086` changed the battery's `u1_ok`/family text (HEAD battery `655ee8f3…` ≠ freeze battery `a7cb92f4…`). The declaration's kill rule says "void if the battery bytes or the freeze manifest differ from …/freeze-manifest.sha256" — the manifest does not contain the battery, so the check is vacuous for the instrument. Smallest correction: recompute a manifest that includes `tools/limine-pin-battery-r91.py` + `tools/check-limine-pins.py` (draft) + freeze battery sha line, and amend the kill rule to check both; archive the mismatch as a finding.

**9. [note] Candidate-draft hash: `candidate-draft.py` == K1 (no V1/U1), the genuine candidate is HEAD `tools/check-limine-pins.py`.**
Evidence — `sha256sum .ufo/waves/round-91/before/controls/candidate-draft.py` = `4780da83…` = `K1-landed-gate.py`; `grep in_global|unverified candidate-draft.py` prints nothing. But `git show d3b0987:tools/check-limine-pins.py` does have V1/U1 lines (`in_global` 148/156/165/167, `unverified` 179-251, sha `679d4f0e…`). The declaration text "candidate gate is drafted alongside the battery…committed here as candidate-draft.py" is therefore misleading: what is committed as candidate-draft is *K1 itself*, and the actual V1/U1 gate was committed into `tools/check-limine-pins.py` at the same freeze revision. QUALITY 114 (instrument frozen with red controls *before any candidate is authored/run/scored*) is **not** violated in substance (no candidate score exists at freeze; controls are committed at d3b0987), but the artifact is mislabelled: a reader cannot tell which file is the candidate. Smallest correction: rename or annotate candidate-draft.py ("K1 copy; candidate = tools/check-limine-pins.py at d3b0987, sha 679d4f0e…") in the landing record.

**10. [note] Uncommitted working-tree gate drift over HEAD.**
Evidence — `git diff HEAD -- tools/check-limine-pins.py` shows uncommitted changes (docstring S374-376 claim, `sanitize()` on panic/measured values, removed dead `if first_entry != 1: pass`). HEAD battery = working tree (`655ee8f3`). The candidate I ran (82/82) is the *working-tree* file (`62bb06c9…`), not the committed HEAD (`dfc63548…`); both pass, but the lane tip judges "at the landed tip". Smallest correction: commit or discard the drift before scoring; record which sha the verdict reads.

**11. [note] C1/C2 separable; C2 subject evaluation pending (no entry-verified claim to attack).**
Evidence — declaration sentence "the battery reads only the gate's JSON; the entry is judged on its rows and sources" is accurate: `check()` never reads `corpus/knowledge/limine-unverified-image-r91.md`, and the entry exists at `45ae6518` (post-freeze) not at freeze (consistent with "opens this round"). Entry row-claims (uri.c silent-fail, SB-unhashed cleared by chainload, first-path-wins, empty-path blocks) are consistent with the battery's U1 frozen rules and the pinned sources; I did not re-open every cited line (would need src-c2 re-pin check), so this is a [note], not a falsification. The disclosed pre-freeze "candidate draft" is neutralised by item 9: there was no scored draft at freeze, so no predicate contamination. R9/R10 are source-backed except the one visibility point the lane already disclosed and repaired (V1 = the r91 fix of the r90 M2 finding).

**12. [note] Controls' per-run numbers confirmed against receipts; clone layout identical.**
Evidence — my recount of both `summary-*.txt` payloads matches the committed JSON: K1 2/2/2, N01 81/81/81, N02 80/80/80, N03 81/81/81, N04 78/78/78, N05 2/2/2, N06 6/6/6, N07 76/76/76, N08 78/78/78, N09 78/78/78, N10 81/81/81 — canonical and clone identical (12 JSON files each), every N control killed by its named family in all 3 runs in both layouts except where item 6 shows the name is a duplicate. Error rows are separated in the summaries (`error_cases` column reads 984 only for K2; item 2), satisfying QUALITY 126(a)'s counting-separately half.

Report: .ufo/waves/round-91/w1/CriticClaims.md
Scope: executed=none
