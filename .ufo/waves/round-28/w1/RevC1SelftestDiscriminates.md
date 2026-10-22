# RevC1SelftestDiscriminates — round-28 wave 1

Verdict: partly holds — 18 of the 19 round-28 selftest cases discriminate against the old counter at `dd94cb1f` (old fails them); `b2-sibling-path-not-pinned` is non-discriminating because git cannot resolve `x/./entry.md`, so the old counter refuses it for the unrelated reason `snapshot-missing`.

Method [obs]: exported `tools/check-adjacency-overlap.py` at `f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0` and `dd94cb1f` into `/fast/scratch/hyaku/tsuku28/RevC1SelftestDiscriminates/{new,old}/check.py`; imported both as modules; swapped the new module's global `evaluate` for a wrapper calling the OLD module's `evaluate` verbatim (old module globals left at dd94cb1f defaults — the dd94cb1f selftest declares `global PIN_PATH` but never assigns it, so its pin-bytes check only fires for the real `corpus/knowledge/userspace-oom-killers-r26.md`); ran the new `selftest()` byte-for-byte so every fixture construction, `want_exit` and `want_anchored` came from the committed code; `pass` in each observation is computed by the committed selftest against the new expectations. Driver: `/fast/scratch/hyaku/tsuku28/RevC1SelftestDiscriminates/driver.py`; raw output: `/fast/scratch/hyaku/tsuku28/RevC1SelftestDiscriminates/driver_out.json`.

## Findings

1. Old-counter verdicts on the 19 round-28 cases [obs, all from `driver_out.json`]:

   | case | want (exit,anchored) | old (exit,anchored) | old passes? |
   |---|---|---|---|
   | b1-extra-row-id | 1,0 | 0,6 | no — DISCRIMINATES |
   | b1-extra-row-id-space | 1,0 | 0,6 | no — DISCRIMINATES |
   | b1-non-string-id | 1,0 | 2,0 (crash) | no — DISCRIMINATES (see 4) |
   | b1-non-object-row | 1,0 | 0,6 | no — DISCRIMINATES |
   | b2-sibling-path-not-pinned | 1,5 | 1,5 | YES — NON-DISCRIMINATING (see 2) |
   | b2-snapshot-field-bogus | 1,5 | 0,6 | no — DISCRIMINATES |
   | b3-quote-line-on-heading | 1,5 | 0,6 | no — DISCRIMINATES |
   | b3-window-crosses-heading | 1,5 | 0,6 | no — DISCRIMINATES |
   | b4-short-sibling-quote | 1,5 | 0,6 | no — DISCRIMINATES |
   | b4-short-lane-quote | 1,5 | 0,6 | no — DISCRIMINATES |
   | b5-lane-under-ufo | 1,5 | 0,6 | no — DISCRIMINATES |
   | b5-lane-is-register | 1,5 | 0,6 | no — DISCRIMINATES |
   | b5-lane-is-sibling-snapshot | 1,5 | 0,6 | no — DISCRIMINATES |
   | b6-lane-gap-with-lane-side | 1,5 | 0,6 | no — DISCRIMINATES |
   | b6-two-lane-gap-rows | 1,5 | 0,6 | no — DISCRIMINATES |
   | b7-province-disagrees | 1,5 | 0,6 | no — DISCRIMINATES |
   | b7-province-row-in-fence | 1,5 | 0,6 | no — DISCRIMINATES |
   | pass-upper-case-digest | 0,6 | 1,5 (`snapshot-digest-mismatch`) | no — DISCRIMINATES |
   | pass-backticked-province-id | 0,6 | 1,5 (`province-row-missing`) | no — DISCRIMINATES |

   The two `pass-` cases discriminate in the false-positive direction: the old counter rejects inputs the new counter is designed to accept (old does a case-sensitive digest compare and cannot unwrap a backticked PROVINCE id cell; old `province_ids` at old/check.py:56-70 vs new `province_rows` at new/check.py:59-78).

2. `b2-sibling-path-not-pinned` (want 1,5; old 1,5, reason `snapshot-missing` on OV1) does NOT discriminate [obs]. The fixture sets `sibling_path='x/./entry.md'`; `git show HEAD:x/./entry.md` does not resolve (`fatal: ambiguous argument 'x/./entry.md'`, git refuses the literal path — verified directly), so the old counter refuses via `snapshot-missing`, an A-rule path lookup failure that predates B2. The B2 pin check `spath != PIN_PATH` never gets exercised on the old side for a different reason than intended — the case would pass any mutant that merely keeps file-existence checking. A discriminating B2 shape exists: with `sibling_path='x/other.md'` pointing at a committed non-pinned file, the old counter ACCEPTS (exit 0, anchored 6, all rows clean) while the new counter refuses (exit 1, anchored 0, `sibling-path-not-pinned` on all six rows) — verified in this run. Residual gap [inf]: the register-mutant battery must reach B2's `sibling-path-not-pinned` reason through a non-pinned path whose snapshot exists; the selftest case alone does not prove that.

3. `b1-non-string-id` discriminates only because the old counter CRASHES, not cleanly refuses [obs]: `TypeError: cannot use 'list' as a set element (unhashable type: 'list')` at the old check's `rid not in in_province` (old/check.py, province-membership test). It exits 2 with no `status`/`rows` output. That still fails the case, so it discriminates, but it also exposes that dd94cb1f's evaluate() is not exception-safe on a non-string id — a quality note on the old counter, not the new one.

4. Old-counter behaviour on the non-round-28 cases is the expected sanity [obs]: `clean`, `null-lane-gap-ok` and `sibling-unavailable-then-mismatch` all pass under old evaluate (0,6; sibling case exit [0,1] with `sibling-mismatch`), and all 13 old-rule refusal cases still refuse at the same (exit, anchored) — the swapped-evaluate harness is faithful; the 19 round-28 verdicts are not an artifact of fixture drift. Note the new fixture differs from the old selftest fixture (adds a `snapshot` field, a 4-word lane quote, a 3-column PROVINCE table, and extra lane files `.ufo/waves/x/report.md` / `corpus/knowledge/adjacency-x.md`); none of these perturb the old verdicts except as recorded above.

5. Net effect for the declared C1 claim [inf]: the selftest battery would emit a 19th-round-28-case "pass" (non-failure) under a mutant that reverts evaluate() to dd94cb1f semantics ONLY for `b2-sibling-path-not-pinned`; the other 18 cases plus the sibling cross-check flip under the old logic, so a wholesale revert is still caught 18 of 19 times on the new cases alone. The B2 refusal itself is landed and live — the new counter emits `sibling-path-not-pinned` (new/check.py, `reasons.append('sibling-path-not-pinned')`) — only the selftest witness for it is weak.

Scope: read=SCORECARD.md round-28 declaration, check-adjacency-overlap.py at f8e3a8f (377 lines) and dd94cb1f (290 lines); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-28/w1/RevC1SelftestDiscriminates.md, /fast/scratch/hyaku/tsuku28/RevC1SelftestDiscriminates/{new,old}/check.py + driver.py + driver_out.json; executed=`git show` exports, `python3 new/check.py --selftest` (36/36 pass, rc 0), `python3 driver.py` (old counter fails 18/19 round-28 cases), one variant-fixture eval pair, `git show` path-resolution probe
Model: not exposed
Installs: none
