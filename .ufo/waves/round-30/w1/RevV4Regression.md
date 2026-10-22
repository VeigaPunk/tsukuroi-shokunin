# RevV4Regression — v4 counter reopen reproduction (round 30, wave 1)

Verdict: partly holds. Two of the four named shapes reopen exactly as the round-29 spot-check claimed (five-space list prefix, extra JSON metadata key); the empty-comment shape does NOT reopen in its literal `<!-->` form (both counters refuse it) while its closed-comment sibling DOES; the italic/unbalanced-asterisk id was never refused by v3 — both versions accept it.

1. [obs] Setup verified before any mutant ran. Counter bytes extracted with `git show <rev>:tools/check-owed-statements-r29.py`: v3 at `75257ea68b1b5c87b429a221bee4d1f8e5d7f54a` sha256 `1c37d49206e1e6656dd1c3115fb8fc2e594f6827d53b3830856a107678bf5891`; v4 at `8976ca92ec3c2e6a2aef07b7065a24ff84a1291b` sha256 `3516d57911f2af1e8ed9abacecc2254686757caf9e3029d0391d30975b461a2d` — both match the assigned digests. Baseline at `8976ca92` on the sandbox clone: v3 and v4 each report `marked: 12`, `unmarked: []`, exit 0. Evidence: `.ufo/waves/round-30/w1/RevV4Regression/baseline-8976ca92.v3.out`, `baseline-8976ca92.v4.out`, `counter-v3-1c37d492.py`, `counter-v4-3516d579.py`.

2. [obs] Method. Sandbox clone at `/fast/scratch/hyaku/tsukuroi-r30/RevV4Regression/repo` (cloned `--no-local`, checked out at `8976ca92`). Each mutant is one minimal one-line commit on its own branch off `8976ca92`, run as `python3 counter-<v>.py --revision <mutant-sha> --lane <sandbox>`; every sandbox git command ran under `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`. Commits, diffs and full outputs are committed-ready under `.ufo/waves/round-30/w1/RevV4Regression/` (`manifest.json`, `rvr-*.patch`, `<m>.v3.out`, `<m>.v4.out`, `v3-v4.diff`). Mutant commits (sandbox only, not in the lane): `0aaf5aac` (A1), `14d28515` (A2), `e0014721` (B), `62c7d013` (C), `9caf4ca1` (D1), `e9f16079` (D2).

3. Results table:

| shape | v3 marked | v4 marked | reopened |
|---|---|---|---|
| `<!-->` inside marker line (A1) | 11 | 11 | no — both refuse |
| `<!-- round-30 check -->` on marker line (A2, sibling variant) | 11 | 12 | yes |
| `-` + 5 spaces list prefix on marker line (B) | 11 | 12 | yes |
| `"status": "withdrawn"` extra JSON key (C) | 11 | 12 | yes |
| italic id `*[R29-OWED-O05]*` (D1) | 12 | 12 | no — v3 already accepts |
| unbalanced `*[R29-OWED-O05]` (D2) | 12 | 12 | no — v3 already accepts |

(Every unmarked line drops exactly the mutated item: O05 for A1/A2/B/D shapes, O09 for C; all other 11 items stay marked.)

4. [obs] N9 confirmed. Mutant `e0014721` turns the O05 marker into `-     [R29-OWED-O05] verdict: …`. v3 reports `M2 0 markers ([]), need exactly one in SKILL.md`; v4 marks it. Mechanism (v4 `MARKER_START`/`MD_MARKER`, file `counter-v4-3516d579.py` lines 125/122): `^ {0,3}(?:[-*+] +|\d{1,9}[.)] +)?` admits a bullet followed by one-or-more spaces; five spaces after `-` makes the line content an indented code block per CommonMark, so the marker is invisible to a markdown reader yet counted by v4.

5. [obs] N20-core confirmed. Mutant `62c7d013` adds `"status": "withdrawn"` to the O09 `corrections_r29` object. v3: `M2 JSON marker keys are not exactly basis,field,id,now,row,verdict,withdrawn_text`. v4: `ok: true`. v4's `JSON_META` set admits `status` and never inspects its value, so a marker reading "withdrawn" is still counted. [inf] A genuinely withdrawn correction would inflate the marked count.

6. [obs + refuted] The literal empty comment `<!-->` does NOT reopen. Mutant `0aaf5aac` puts `<!-->` inside the marker line; both v3 and v4 report `M2 0 markers` — `marked: 11` each. `<!--.*?-->` cannot match `<!-->`: after `<!--` the pattern needs the literal three bytes `-->`, and only `>` remains; `re.sub(r'<!--.*?-->', '', '<!-->')` returns `<!-->` unchanged (verified in the same interpreter run as the mutant prep). The spotcheck's stated mechanism ("`<!-->`, stripped by `<!--.*?-->`", citing v4 lines 130 and 186) is wrong for that instance. [obs] The family it named does reopen: `14d28515` appends the closed comment `<!-- round-30 check -->` to the marker line — v3 hides the whole line (`M2 0 markers`, 11) while v4 strips the comment and counts the marker (12). [inf] Battery consequence: a fixture using exactly `<!-->` would be refused by v4 and never expose the gap; the fixture needs a closed `<!-- … -->` form, e.g. `<!---->` or `<!-- x -->`.

7. [obs + refuted] The italic/unbalanced-asterisk id was never refused by v3. Mutants `9caf4ca1` (`*[R29-OWED-O05]*`) and `e9f16079` (`*[R29-OWED-O05]`) both produce `marked: 12` under v3 AND v4 (exit 0). The `\**` token bracketing the id is byte-identical in v3's and v4's `MARKER_START` and `MD_MARKER` (`v3-v4.diff` shows no change there). There is no reopen to reproduce; the routed-defect premise that v3 refused this shape is mistaken. [inf] The underlying risk the spotcheck flagged is still real and worse than stated: emphasis-wrapped ids are accepted by every version, so an italic id marker counts without ever rendering as a marker.

8. [obs] Remaining v4 deltas (`v3-v4.diff`) not exercised by these mutants: `* `, `+ ` and `N.`/`N)` list prefixes follow the same `[-*+] +` / `\d{1,9}[.)] +` token as finding 4 [inf: they reopen the same way]; moved-unique path citations in `basis_ok`; the JSON census now requires `"id": "R29-OWED-<id>"` (a tightening); capitalised verdict now reported as M4 (a tightening). [obs] No landed marker at `8976ca92` uses any reopened shape — baseline is 12/12 clean for both counters.

9. [inf] Carrier choice caveat: mutants used the O05 markdown marker (SKILL.md:2320) and the O09 JSON object (storage-health-r26.json:326); `live_lines`/`MARKER_START`/`MD_MARKER`/`JSON_KEYS` are shared across all six target files, so the same openings apply to every markdown item and both JSON files. [unk] Whether a standalone `<!-->` line (rather than inline) behaves identically was not run as a separate commit; the code path is the same (`live_lines` comment state), so the expected result is identical refusal by both.

Evidence index: `.ufo/waves/round-30/w1/RevV4Regression/` — `manifest.json`, six `rvr-*.patch`, six `*.v3.out`/`*.v4.out` pairs, two `baseline-*.out`, `counter-v3-1c37d492.py`, `counter-v4-3516d579.py`, `v3-v4.diff`. Sandbox with the six mutant branches: `/fast/scratch/hyaku/tsukuroi-r30/RevV4Regression/repo`.

Scope: read=lane lessons/spotcheck + counters v3/v4 via git show + sandbox files; wrote=.ufo/waves/round-30/w1/RevV4Regression/ (manifest, patches, outputs, counter copies, v3-v4.diff) and this report; executed=git clone/checkout/add/commit/diff/log in sandbox under env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE; python3 runs of counter v3/v4 and regex pre-checks; no lane-repo writes
Model: devin/swe-2
Installs: none
