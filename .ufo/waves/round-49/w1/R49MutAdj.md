VERDICT: supports

# R49MutAdj — C2 (adjacency) counter, mutation probes 1–4

Item C2-B8. Detector under test: `tools/check-adjacency-table-r49.py` at the freeze
`55c07cd3f8bff2e12117c34d57b4c618de74d85c` (sha256
`17be2a11ac6254fb3f3b0fd529f26415301e2f7240bd69813442086ded5eddd7`; identical to the lane
worktree file, verified with `sha256sum`). Probes ran on scratch copies under
`/fast/scratch/hyaku/tsukuroi-r49/R49MutAdj/` with `--lane
/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`; no lane byte was written or mutated.

## Baseline (pristine detector must PASS before a mutant is meaningful)

Revision used for all probes: `32a855608aa3ebb19b0602a94cc33bcfda564a61` — the control-scored
revision named in `FROZEN.md` ("Control outcomes (scored at `32a85560`…)") and used by the
pre-data battery (`battery.py` line 19 `REV = os.environ.get('BATTERY_REV', FREEZE)`; receipts
record `"revision": "32a85560…"`).

```
$ python3 counter-frozen.py --lane <lane> --revision 32a85560… --province-file PROVINCE.frozen.md
{"adj_rows": 7, "linked_rows": 7, "bare_ranges": 0, "anchors_ok": 7, "registry_ok": 7,
 "anchors_checker_rc": 0, "verdict": "PASS"}   rc=0
```

`PROVINCE.md` is byte-identical at the freeze and at `32a85560` (`git diff 55c07cd..32a8556 --
PROVINCE.md` empty), so the same fixture text is being judged; only the registry row differs
(see observation O1).

## Mutants

Each mutant is a single-point edit of the frozen script (verified `py_compile` clean); each
fixture uses `--province-file` only — the real registry at `--revision` is kept, the real
`tools/check-adjacency-anchors.py` cross-check stays live (`anchors_checker_rc` 0 in every run).

| Mutant | Injection (frozen script line) | Fixture (single-cell edit of `PROVINCE.md`) | Pristine (rc, legs) | Mutant (rc, legs) | Verdict |
|---|---|---|---|---|---|
| M1 bare_ranges leg removed | L137 `bare += len(row_bare)` deleted | F1: ADJ-01 ownership cell `| `OUT-002` |` → `| `OUT-002`, `../mori-shokunin/PROVINCE.md:10-20` |` | rc 1, `bare_ranges 1` (rest 7) — problem `bare locator(s): ['PROVINCE.md:10-20']` | rc 0, `bare_ranges 0`, PASS | **killed** |
| M2 ADJ-class equality removed | L157–159 `if anc[1] != row_id:` block deleted | F2: ADJ-01 and ADJ-02 own each other's anchor (`OUT-003`/`OUT-002` swapped) | rc 1, `anchors_ok 5` (rest 7) — problems `OUT-003 points at 'ADJ-02', not ADJ-01` and the converse | rc 0, `anchors_ok 7`, PASS | **killed** |
| M3 quote word-count removed | L168 `if not quote or len(quote.split()) > 25:` → `if not quote:` | F3: OUT-002 quote grown to 27 words | rc 1, `anchors_ok 6` (rest 7) — problem `OUT-002 quote cell empty or over 25 words (27)` | rc 0, `anchors_ok 7`, PASS | **killed** |
| M4 registry leg removed | L171–181 registry lookup + blob-sha256/commit-format checks deleted | F4: extra valid anchor `OUT-011` (points at ADJ-01) added, ADJ-01 names `` `OUT-002`, `OUT-011` ``; registry has no `OUT-011` | rc 1, `registry_ok 6` (rest 7) — problem `OUT-011 absent from corpus/knowledge/adjacency-anchors-r19.json` | rc 0, `registry_ok 7`, PASS | **killed** |

4/4 killed; no survivor, so no coverage gap is claimed on these four legs. Each pristine failure
is attributable to the mutated leg alone (the other five legs stay at their passing values), and
the mutants are accepted only because that leg no longer bites.

Byte evidence (sha256, restored/unchanged):
`counter-frozen.py 17be2a11ac…` (never edited; all mutants are separate files) ·
`M1 35f083f808…` · `M2 a978b568b2…` · `M3 596ed0b5bd…` · `M4 37b5f1b8c8…`.
Full `diff -u` of every mutant: `mutants.diff`; driver: `probe.py`; raw records:
`probe-results.json`.

Commands per probe (identical shape, one run each side):

```
python3 counter-frozen.py --lane <lane> --revision 32a85560… --province-file F<n>.md
python3 M<n>.py          --lane <lane> --revision 32a85560… --province-file F<n>.md
```

## `--skip-anchors-check`: which leg, and do the controls rely on it?

The flag disables exactly one leg, `anchors_checker_rc` — the subprocess cross-check
`tools/check-adjacency-anchors.py --revision <REV>` (frozen script L185–192). With the flag,
`checker_rc` is left at `-1`; the predicate term `checker_rc == 0` (L198–199) is *not* relaxed.
Consequence: a run with `--skip-anchors-check` can never PASS — the printed
`anchors_checker_rc: -1` alone fails the predicate and the exit status. The flag is therefore
"omit the cross-check", not "pass without it", and cannot be used to launder a PASS.

Control dependence: the four C2 negative controls were recorded with the flag
(`battery-summary-r49-c2.jsonl`, K0–K3 `"anchors_checker_rc": -1`), and the pass control runs it
live (K-pass `0`). I re-ran the four negative fixtures with the leg **enabled** at
`32a85560` (real checker rc 0, so the leg could not have caused the failure):

```
K0-base          rc 1  bare 9, linked 0, anchors 0, registry 0, checker 0
K1-ranges-kept   rc 1  bare 9,            anchors 7, registry 7, checker 0
K2-OUT-099       rc 1  bare 0,            anchors 6, registry 6, checker 0
K3-all-OUT-001   rc 1  bare 0,            anchors 1, registry 7, checker 0
```

All four still FAIL on their intended legs with the skipped leg at 0 ⇒ **no control relies on
that leg** for its verdict. (Sanity note for future batteries: because skipping forces
`checker_rc = -1`, any fixture run with the flag is FAIL by construction, so a FAIL expectation
is only meaningful together with a named non-checker leg violation — which all four have.)

## Observation O1 (not a mutation finding): the predicate does NOT hold at the freeze sha

Running the pristine counter at `--revision 55c07cd3…` (the freeze, as every seat is told to read
bytes) returns **FAIL, rc 1**, with `adj_rows 7, linked_rows 7, bare_ranges 0, anchors_ok 7,
registry_ok 7` and only `anchors_checker_rc 1`.

Cause: the frozen registry row IN-109 still pins `found_line 2642`, while the census at the same
revision carries the quote at line 2660:

```
$ git show 55c07cd…:corpus/knowledge/adjacency-anchors-r19.json \
    | python3 -c "import json,sys;print([x['found_line'] for x in json.load(sys.stdin)['inbound'] if x['id']=='IN-109'])"
[2642]
$ git show 55c07cd…:tools/tsukuroi-census.sh | grep -n "kernel ring class counts are evidence"
2660:  check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED \
$ python3 tools/check-adjacency-anchors.py --revision 55c07cd…
… "findings": [{"id": "INBOUND-CLASSIFICATION-WRONG", "site": "corpus/knowledge/adjacency-anchors-r19.json:inbound[108]",
                "detail": "classification DRIFTED is inconsistent: found_line is not an occurrence of evidence_quote …"}], "status": "FAIL"
```

The census is byte-identical at `55c07cd` and `32a85560` (`git diff --stat` empty); the repin
(`found_line 2642 → 2660`) landed in `32a85560` ("round-49: w1 spec …; IN-109 repin 2642->2660"),
after the freeze. At `32a85560` and at the lane tip `d7cfc27` the checker is PASS/rc 0
(`{"status": "PASS", …, "live_object_match": 10}`, rc 0). This matches `FROZEN.md`'s
"scored at `32a85560`" and "the measurement is the live integrated revision", but it means a seat
that runs the C2 command verbatim with `<REV>` = the freeze sha gets FAIL on a leg unrelated to
C2's surface. L1 should score C2 at `32a85560` (the integrated revision), not at `55c07cd`, and
should not file this as a C2 surface regression.

## Not done / limits

- I did not run `--selftest` (this counter has none) and did not mutate the other legs
  (anchor cell count, heading regex, `adj_rows`/`linked_rows` counting); those were outside the
  four assigned probes.
- I did not exercise `--registry-file` (the item required `--province-file` only and the real
  registry).
- No tooling installed or upgraded; no pacman transaction.
- Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49MutAdj/` removed after copying receipts; the lane
  worktree was never written (`git status` shows only other seats' wave files and a pre-existing
  `M corpus/SOURCES.md`, neither mine).
