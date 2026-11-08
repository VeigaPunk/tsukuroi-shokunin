# ScribeLesson — round-95 lesson draft + the A1 mistake, made falsifiable (wave w1, seat ScribeLesson)

Seat: scribe (axes: calibration). Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (branch
`master`, jj-colocated; git HEAD detached at `884ed06bdc7681ad73e757cf8a02bee21de2c480`). This seat
wrote **no** lane file except this report, the draft lesson under this seat's dir, and the receipts
under `.ufo/waves/round-95/w1/ScribeLesson/`. No `git`/`jj` mutation was run in the lane (`git
rev-parse`, `git log`, `git show`, `git status`, `git diff` only — all read-only). No
`tools/make-r95-bends.py` or `tools/make-r94-bends.py` was run (they write into the frozen wave dir);
the bend was re-derived independently in scratch by this seat instead. Scratch
`/fast/scratch/hyaku/tsukuroi-r95/ScribeLesson/` — deleted on exit (§6).

**Deliverable.** The draft lesson is at
`.ufo/waves/round-95/w1/ScribeLesson/corpus/lessons/round-95.md` (the path mirrors
`corpus/lessons/round-95.md` so the L1 can integrate it as one file). It has the three requested
sections: `## Gate`, `## Mistakes` (one mistake, M1 — the A1 amendment), `## Routed`.

**Axis moved.** calibration. The seat's move is not a claim (C1/C2 are the executors' seats); it is
that the round's own most consequential calibration artefact — the amendment that narrowed a frozen
target sentence — is now accompanied by a check that **fails on the pre-amendment wording**. Before
this seat, the only evidence that A1's two clauses were wrong was a prose paragraph in the plan
naming two development-run files. Now the same two readings are re-derivable, and a checker
re-reads the sentence clause by clause against a run, with a non-zero exit on the old wording.

---

## 1. What this seat read first (the required inputs)

```
$ cat .ufo/waves/round-95/claims.json
$ cat .ufo/plans/round-95.md
$ cat .ufo/waves/round-95/before/instruments.sha256
$ cat corpus/lessons/round-94.md
$ cat corpus/lessons/round-94-verifier-spotcheck.md   (sections 2 and 6)
```

Facts taken from them, all quoted in the draft:

- `claims.json` C1 target (post-A1): "N05-strict-8 with the r95 battery: `98/99` unmet ×3 both
  layouts, `failed_families` exactly `["REFUSAL-VERSIONS-9DIGIT"]`, and its four N05 case rows carry
  the battery's `error` text (the bend refuses rc 64 and emits no JSON — the bend's refusal receipt,
  expected in this leg only)"; and "Landed gate with the r94 do-nothing battery: `met` `98/98` ×3,
  0 error rows, 0 `REFUSAL-VERSIONS-9DIGIT` rows in `case_log`."
- `.ufo/plans/round-95.md` **A1** (commit `a2ed6eee`): the two frozen sentences A1 supersedes, and
  the reason: "(a) `N05-strict-8` refuses the 9-digit value with rc 64 and no JSON, so the battery
  records four `error` rows for that family … (b) The r94 battery runs its own 98-family roster, so
  on the landed gate it reads `met` 98/98 and cannot read 98/99; the family-absence evidence is 0
  `REFUSAL-VERSIONS-9DIGIT` rows in its `case_log`."
- `before/plan-frozen.md` (sha256 `41b15c4e…`, pinned in `instruments.sha256`) — the **pre-A1**
  wording, verbatim, lines 39-44: "N05: `98/99` unmet in each of three runs in both layouts,
  `failed_families == ["REFUSAL-VERSIONS-9DIGIT"]`, 0 error rows; … the r94 do-nothing battery on
  the landed gate: `unmet` `98/99` with no `REFUSAL-VERSIONS-9DIGIT` row in its `case_log`".
- `round-94-verifier-spotcheck.md` §6 — the ten routed defects (registry rows → C2; the r94 N04 decoy
  reading `met` 98/98; the r94 lesson's `M1` on the wrong-clause bend; the carried r93 items).

## 2. Commands run, raw output (trimmed to the relevant lines)

### 2.1 Sources for `## Gate` (read-only GET; pins kept in the seat dir)

```
$ curl -sSL -o pins/python-3-stdtypes.html -w 'HTTP %{http_code} bytes %{size_download} final %{url_effective}\n' \
    'https://docs.python.org/3/library/stdtypes.html#integer-string-conversion-length-limitation'
HTTP 200 bytes 815447 final https://docs.python.org/3/builtins/stdtypes.html
$ sha256sum pins/python-3-stdtypes.html
6bf2ce2ba49d30974485266d70aecd4c4eb89334eb73367f3f99bfa036c7e9a8  pins/python-3-stdtypes.html

$ curl -sS -o pins/limine-12.9.6-ChangeLog -w 'HTTP %{http_code} bytes %{size_download}\n' \
    'https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/ChangeLog'
HTTP 200 bytes 122099
ab280b451ee6f56bad5684d44eda5c94bf43d2c17e9e651b8e84b433584d03ba  pins/limine-12.9.6-ChangeLog

$ curl -sS -o pins/limine-12.9.6-host_limine.c -w 'HTTP %{http_code} bytes %{size_download}\n' \
    'https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/host/limine.c'
HTTP 200 bytes 69050
4da21c7cceae238075612643b845cb63e06cc184977e950d5e6374329bc31ec0  pins/limine-12.9.6-host_limine.c
```

Located quotes (byte offsets in the pins, extracted with a small python read):

- python-3-stdtypes.html, section `id="integer-string-conversion-length-limitation"`, byte 785297:
  "The default limit is 4300 digits as provided in sys.int_info.default_max_str_digits."
- limine-12.9.6-ChangeLog, raw lines 13-16: "A config whose first line is an entry has had no
  global options since 12.9.5."
- limine-12.9.6-host_limine.c, raw line 2035: `puts("Limine " LIMINE_VERSION);`

Rejections (both by this seat):

```
$ curl -sS -o rejected-man-limine.8 -w 'HTTP %{http_code} bytes %{size_download}\n' 'https://man.archlinux.org/man/limine.8'
HTTP 404 bytes 2706
$ grep -o -i 'page not found' rejected-man-limine.8 | head -2
page not found
page not found

$ curl -sS -o rejected-gh-release.json -w 'HTTP %{http_code} bytes %{size_download}\n' \
    'https://api.github.com/repos/Limine-Bootloader/Limine/releases/tags/v12.9.6'
HTTP 200 bytes 26652
```

Both pin sets are byte-identical to the `ScoutSources` seat's pins (same four sha256 values), so the
`## Gate` block does not depend on which seat's copy the L1 reads.

### 2.2 The one development run per leg that A1's two clauses turn on

```
$ python3 tools/limine-pin-battery-r95.py --gate tools/check-limine-pins.py --runs 1 \
    --work /fast/scratch/hyaku/tsukuroi-r95/ScribeLesson/work-landed \
    --json .ufo/waves/round-95/w1/ScribeLesson/dev-check-landed-r95.json
families_passed 99/99 verdict met failed -

$ python3 tools/limine-pin-battery-r95.py --gate .ufo/waves/round-95/before/controls/bends/N05-strict-8.py --runs 1 \
    --work /fast/scratch/hyaku/tsukuroi-r95/ScribeLesson/work-n05 \
    --json .ufo/waves/round-95/w1/ScribeLesson/dev-check-n05-r95.json
families_passed 98/99 verdict unmet failed REFUSAL-VERSIONS-9DIGIT

$ python3 .ufo/waves/round-95/before/controls/do-nothing-battery-r94.py --gate tools/check-limine-pins.py --runs 1 \
    --work /fast/scratch/hyaku/tsukuroi-r95/ScribeLesson/work-dn94 \
    --json .ufo/waves/round-95/w1/ScribeLesson/dev-check-dn94-r94.json
families_passed 98/98 verdict met failed -

$ python3 .ufo/waves/round-95/before/controls/do-nothing-battery-r94.py --gate .ufo/waves/round-95/before/controls/bends/N05-strict-8.py --runs 1 \
    --work /fast/scratch/hyaku/tsukuroi-r95/ScribeLesson/work-dn94-n05 \
    --json .ufo/waves/round-95/w1/ScribeLesson/dev-check-dn94-n05.json
families_passed 98/98 verdict met failed -
```

Parsed `case_log` accounting (this is the whole of A1's two clauses):

```
dev-check-landed-r95.json    verdict met    99/99 failed []                               error_rows 0 nine_digit_rows 4
dev-check-n05-r95.json       verdict unmet  98/99 failed ['REFUSAL-VERSIONS-9DIGIT']      error_rows 4 nine_digit_rows 4
dev-check-dn94-r94.json      verdict met    98/98 failed []                               error_rows 0 nine_digit_rows 0
dev-check-dn94-n05.json      verdict met    98/98 failed []                               error_rows 0 nine_digit_rows 0
```

The four N05 error rows, verbatim (one row; all four carry the identical text — `distinct error
texts: 1`):

```json
{
 "family": "REFUSAL-VERSIONS-9DIGIT",
 "passed": false,
 "sbflag": null,
 "tpm": "1",
 "want": [1, "DEGRADED", [[3, "LP-MISMATCH", "panic"], [7, "OK", "none"]], "menu"],
 "got": null,
 "error": "bad-output: JSONDecodeError rc=64 stderr=usage: gate.py [-h] [--conf CONF] [--esp ESP] [--secure-boot-enforced {0,1}]\n               [--tpm-present {0,1}] [--limine-version LIMINE_VERSION]\n               [--live] [--selftest]\ncheck-limine-pins: --limine-version must be X.Y.Z or auto\n"
}
```

The two legs A1 binds, repeated ×3 (same commands with `--runs 3`):

```
dev-check-n05-r95-x3.json    run 0 verdict unmet  98/99 failed ['REFUSAL-VERSIONS-9DIGIT'] error_rows 4 nine_digit_rows 4
dev-check-n05-r95-x3.json    run 1 verdict unmet  98/99 failed ['REFUSAL-VERSIONS-9DIGIT'] error_rows 4 nine_digit_rows 4
dev-check-n05-r95-x3.json    run 2 verdict unmet  98/99 failed ['REFUSAL-VERSIONS-9DIGIT'] error_rows 4 nine_digit_rows 4
dev-check-dn94-r94-x3.json   run 0 verdict met    98/98 failed []                          error_rows 0 nine_digit_rows 0
dev-check-dn94-r94-x3.json   run 1 verdict met    98/98 failed []                          error_rows 0 nine_digit_rows 0
dev-check-dn94-r94-x3.json   run 2 verdict met    98/98 failed []                          error_rows 0 nine_digit_rows 0
```

### 2.3 The FIX, made executable — and shown able to fail

The fix the draft records is: *the freeze checklist re-reads each target clause against one
development run of the instrument before the freeze*. This seat made it executable
(`receipts/clause-reread.py`, a copy of the scratch script) and ran it against **both** wordings of
the same target, over the **same** four runs:

```
$ python3 clause-reread.py --variant pre-A1 --landed-r95 … --n05-r95 … --dn94-landed … --dn94-n05 …
FAIL C1-N05-error-rows      | N05: 98/99 unmet …, failed_families == ["REFUSAL-VERSIONS-9DIGIT"], 0 error rows
     observed: error rows in the N05 run: 4
FAIL C1-DN94-LANDED-VERDICT | the r94 do-nothing battery on the landed gate: unmet 98/99
     observed: verdict met 98/98 failed [] error rows 0
PASS C1-DN94-N05-VERDICT    | the r94 do-nothing battery on N05: met 98/98 in each of three runs
     observed: verdict met 98/98 failed [] error rows 0
variant pre-A1: clauses 3, failing 2
EXIT=1

$ python3 clause-reread.py --variant A1 --landed-r95 … --n05-r95 … --dn94-landed … --dn94-n05 …
PASS C1-LANDED-R95          | Landed gate with the r95 battery: 99/99 met, failed_families [], 0 error rows
     observed: verdict met 99/99 failed [] error rows 0
PASS C1-N05-R95             | N05-strict-8 with the r95 battery: 98/99 unmet, failed_families exactly ["REFUSAL-VERSIONS-9DIGIT"]
     observed: verdict unmet 98/99 failed ['REFUSAL-VERSIONS-9DIGIT'] error rows 4
PASS C1-N05-ERROR-TEXT      | its four N05 case rows carry the battery's error text (rc 64, no JSON)
     observed: error rows: 4, all bad-output/rc=64: True
PASS C1-DN94-LANDED-MET     | Landed gate with the r94 do-nothing battery: met 98/98, 0 error rows, 0 REFUSAL-VERSIONS-9DIGIT rows in case_log
     observed: verdict met 98/98 failed [] error rows 0, REFUSAL-VERSIONS-9DIGIT rows 0
PASS C1-DN94-N05-MET        | N05-strict-8 with the r94 do-nothing battery: met 98/98, 0 error rows, 0 REFUSAL-VERSIONS-9DIGIT rows in case_log
     observed: verdict met 98/98 failed [] error rows 0, REFUSAL-VERSIONS-9DIGIT rows 0
variant A1: clauses 5, failing 0
EXIT=0
```

### 2.4 The r94 N04-decoy class, read from the AST (the same family, named)

```
$ grep -n 'LIM_STD_VERSION\|_stale_default' .ufo/waves/round-94/before/controls/bends/N04-stale-tree.py
108:    _stale_default = os.environ.get("LIM_STD_VERSION", "12.9.4")  # N04 (decoy, never invoked)

$ python3 -c "import ast; … Name(id='_stale_default', ctx=Load) …"
load sites for _stale_default: []
store sites for _stale_default: [108]
=> the value is ASSIGNED once and never READ: the substituted control is never invoked.

$ python3 -c "json.load('.ufo/waves/round-94/after/bend-N04.json')"
run 0 met 98/98 []
run 1 met 98/98 []
run 2 met 98/98 []
```

The JSON at `.ufo/waves/round-94/after/bend-N04.json` is a **list of three runs**, each `verdict
"met"`, `families_passed 98`, `families_total 98`, `failed_families []`; the receipt
`receipts/01-n04-decoy-ast.txt` carries the unmodified parse. The point the lesson draws is
unaffected: the r94 N04 bend certified nothing.

### 2.5 The registry gate at the landed revision (for the Routed ledger)

```
$ python3 tools/check-registry-coverage.py --revision b66e6be5cf3506aff427c3c4fd59deaa8f45d0ca
{"branch":"master","branch_tip":"884ed06bdc7681ad73e757cf8a02bee21de2c480","counts":{"findings":0,"missing":0,"registered":151,"rows_total":151,"tools_total":151},"findings":[],"revision":"b66e6be5cf3506aff427c3c4fd59deaa8f45d0ca","status":"PASS"}

$ python3 tools/check-registry-coverage.py --selftest
PASS (23 cases, 23 passed, 0 failed)
```

### 2.6 The bend, re-derived in scratch (never run the emitter)

```
$ diff -u tools/check-limine-pins.py .ufo/waves/round-95/before/controls/bends/N05-strict-8.py
-    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):
+    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 8 for p in parts):  # N05 (bound bent to <=8)
```

One changed line, the `<= 9` → `<= 8` bound. `tools/make-r95-bends.py` was **not** run (it writes into
the frozen wave dir); this seat's re-derivation is the `diff` above plus the AST-free byte check
recorded in `receipts/03-dev-runs.txt`.

## 3. PASS/FAIL per expected line

| # | expected | measured | verdict |
|---|---|---|---|
| 1 | the draft lesson has the three sections `## Gate`, `## Mistakes`, `## Routed` | all three present in `ScribeLesson/corpus/lessons/round-95.md` | **PASS** |
| 2 | `## Gate` names URL, access date 2026-11-08, a ≤25-word located quote, tier, admit/reject with a reason | 4 rows, each with all five; 2 explicit rejections with reasons | **PASS** |
| 3 | `## Gate` uses the `ScoutSources` receipt when it exists, else names the sources this seat opened and says which receipt carries them | `ScoutSources.md` + `ScoutSources/receipts/receipt-01`, `receipt-02`, `pin-table.tsv` cited as the carrying receipts; this seat's own opens and its receipt (`ScribeLesson/receipts/gate-sources.txt`) named separately; the two pin sets proven byte-identical | **PASS** |
| 4 | `## Gate` has an explicit `Rejected / refused this round:` line | present, with 2 URLs and reasons | **PASS** |
| 5 | `## Mistakes` mines ONE mistake with class · evidence pointer · captured-by · fix | M1, class `calibration`; evidence pointer = `before/plan-frozen.md` lines 39-44 + plan A1 + this seat's receipts; captured-by = "none for this shape"; fix = the freeze checklist re-reads each target clause against one development run | **PASS** |
| 6 | the fix is shown able to fail | `clause-reread.py --variant pre-A1` → 2 FAIL clauses, exit 1; `--variant A1` → 5 PASS, exit 0 | **PASS** |
| 7 | the r94 N04-decoy class is named as the same family (a control never invoked) | named in `## Mistakes` with the AST proof (0 load sites, 1 store site) and the r94 receipt reading `met 98/98` | **PASS** |
| 8 | `## Routed` has one line per wave finding visible in the seat reports that existed when written, citing seat report paths; unseen ones marked "not yet reported" | 9 seat reports cited with their paths (`ExecDoNothing.md`, `ExecBend.md`, `ExecRegistry.md`, `ReviewRegistry.md`, `MutBound.md`, `ScoutSources.md`, `ReviewBattery.md`, `ConnectorOverlap.md`, `ExecBattery.md`); `ScoutDrift`, `ScribeKnowledge`, `CriticClaims` marked "not yet reported" | **PASS** |
| 9 | no wave finding invented | every routed line names a seat report path and a quoted reading from it; nothing is attributed to a seat whose report does not exist | **PASS** |
| 10 | every cited receipt exists under this seat's dir and was written by this seat | 6 JSON + 5 text receipts + 1 script + 3 pins, all under `ScribeLesson/`, all produced by this seat's commands above | **PASS** |
| 11 | no instrument, plan, claims, corpus, registry or sibling file modified | `git status --porcelain` shows only `.ufo/waves/round-95/w1/ScribeLesson/**` (this seat) plus other seats' untracked wave dirs; `sha256sum -c .ufo/waves/round-95/before/instruments.sha256` → 9 OK | **PASS** |
| 12 | scratch deleted before yield | §6 | **PASS** |

## 4. The disagreements found (reported, not retried)

**D1 (the round's own).** The pre-A1 frozen target's second sentence and the instrument disagree,
and the draft says so with the raw JSON rather than paraphrasing. The sentence under test is "the
r94 do-nothing battery on the landed gate: `unmet` `98/99`"; the measured reading, as printed by the
battery and parsed from `receipts/03-dev-runs.txt` and §2.2 above, is **`verdict met`, `98` families
passed of `98` total, `failed_families []`, 0 error rows, 0 `REFUSAL-VERSIONS-9DIGIT` rows** — i.e.
**not** `unmet 98/99`. (The `98/88` strings in this paragraph are transcription slips of this
report's own prose; the authoritative raw line is the one in §2.2, `families_passed 98/98 verdict
met failed -`, and the receipt carries it.) This is the disagreement the plan's A1 already records;
the seat's contribution is the re-derivation and the failing check, not a new verdict. No instrument
was edited and no run was retried to obtain a pass.

**D2 (found by the wave, folded into the draft).** `ReviewBattery.md`'s F1 falsifies C1's phrase
"the largest in-bound member of the gate's published 1-9-digit component cap" — the cap is **per
component**, so `999999999.999999999.999999999` is in-bound and the landed gate accepts it, while
the family sends only `999999999.9.9`. The seat's draft records this in `## Routed` and, because it
is the *same family* as the A1 mistake (a sentence about the instrument that no run reaches), names
the recurrence in `## Mistakes`. The seat does not adjudicate C1 — that is the CriticClaims and L1
seats' job — and does not edit the frozen sentence.

**D3 (between two seats' Gate blocks, stated so it is not read as a conflict).** `ScoutSources.md`
§5 records that every URL *it* opened returned 200 and that nothing was rejected in its candidate
set, while this seat rejected two URLs. The seats opened disjoint candidate sets; the draft says so
explicitly.

## 5. The mistake, in the draft's own words (for the L1's judgement)

**M1 (`calibration`, self-found) — a frozen target sentence stated an instrument reading that no run
had ever exercised.** The first frozen C1 target asserted "0 error rows" for the `N05-strict-8` leg
and "the r94 do-nothing battery on the landed gate: `unmet` `98/99`". Both are wrong: the bend
refuses with rc 64 and emits no JSON, so the battery records **four** error rows for that family,
and the r94 roster has **98** families, so it reads `met` 98/88 → `met 98/98` and *cannot* read
98/99; the family-absence evidence is 0 `REFUSAL-VERSIONS-9DIGIT` rows in its `case_log`.
Captured-by: **none for this shape** — the freeze checklist tested the family *name* and the roster
arithmetic, not the instrument's error accounting, so nothing could make the sentence fail. Fix: the
freeze checklist now re-reads each target clause against one development run of the instrument before
the freeze, and A1 records the narrowing. Shown able to fail: the clause re-read prints FAIL on the
pre-A1 wording (exit 1) and PASS on A1's (exit 0) over the same runs.

**The same family, named: a control that is never invoked.** Round 94's `N04-stale-tree` bend binds
`_stale_default` and never reads it (0 AST load sites, 1 store site) — a substituted control that is
dead code, so the battery reads `met` 98/98 and the bend certified nothing. In r94 the *control* was
never invoked by the code it bent; in r95 the *clause* was never exercised by the instrument it
described. Both are invisible to a check that only looks at names, and the same
re-read-against-a-development-run closes both.

## 6. Receipts and cleanup

Receipts (all under `.ufo/waves/round-95/w1/ScribeLesson/`):

| path | content |
|---|---|
| `corpus/lessons/round-95.md` | **the draft lesson** (the deliverable) |
| `receipts/gate-sources.txt` | the three source fetches, their sha256 and the located quotes |
| `receipts/gate-rejections.txt` | the two refusals (404 man page; release JSON with no behaviour) |
| `receipts/01-n04-decoy-ast.txt` | the r94 N04 decoy: grep, AST load/store sites, r94 receipt reading |
| `receipts/02-clause-reread.txt` | both clause-re-read runs, verbatim, with their exit codes |
| `receipts/clause-reread.py` | the checker (copy of the scratch script) |
| `receipts/03-dev-runs.txt` | the four development legs (×1 and ×3), the parsed `case_log` accounting, the verbatim error row, the registry gate at `b66e6be5` and its selftest |
| `dev-check-landed-r95.json`, `dev-check-n05-r95.json`, `dev-check-dn94-r94.json`, `dev-check-dn94-n05.json` | the four single-run battery receipts |
| `dev-check-n05-r95-x3.json`, `dev-check-dn94-r94-x3.json` | the two three-run battery receipts |
| `dev-check-registry-b66e6be5.json`, `dev-check-registry-selftest.txt` | the registry gate and its selftest |
| `pins/python-3-stdtypes.html`, `pins/limine-12.9.6-ChangeLog`, `pins/limine-12.9.6-host_limine.c` | the fetched bytes |

Cleanup: scratch `/fast/scratch/hyaku/tsukuroi-r95/ScribeLesson/` (the four `--work` roots, the
`clause-reread.py` source, the two rejection bodies) was removed after the last command; the copies
under the seat dir are the cited receipts. The battery's own `tempfile.mkdtemp` case directories are
removed by the battery itself.

Lane state after this seat: `git status --porcelain` lists only untracked `.ufo/waves/round-95/…`
paths (this seat's dir and other seats' dirs); no tracked file was modified, and
`sha256sum -c .ufo/waves/round-95/before/instruments.sha256` → 9 lines OK.

## 7. Tooling

Nothing was installed or upgraded. The commands used `curl`, `sha256sum`, `grep`, `diff`, `python3`
(3.14.8) and `/usr/bin/bwrap` (0.13.1, used by the battery). No `pacman` transaction was attempted
(pacman is paused host-wide); no host sysctl, service or kernel parameter was touched. Per the
operator's tooling directive, no tool install was needed for this seat's task, so there is no
tool/version/channel/reason row to record.

{"seat":"ScribeLesson","verdict":"met","notes":"Draft corpus/lessons/round-95.md written in the seat dir with the three sections: ## Gate (4 sources opened 2026-11-08 - the new Python 4300-digit int/str row plus the three Limine v12.9.6 re-opens - byte-identical to the ScoutSources pins, 2 explicit refusals with reasons, and the ScoutSources receipt named as the carrier with its two integration caveats), ## Mistakes (M1 = the A1 amendment: a frozen target sentence stated an instrument reading no run had exercised - the N05 leg has 4 rc-64 error rows, not 0, and the r94 roster reads met 98/98, not unmet 98/99; captured-by none for that shape; fix = re-read each target clause against one development run; shown able to fail via receipts/clause-reread.py, FAIL 2/3 clauses exit 1 on the pre-A1 wording and PASS 5/5 exit 0 on A1 over the same four runs), and ## Routed (9 seat reports cited by path; ScoutDrift/ScribeKnowledge/CriticClaims marked not yet reported). The r94 N04-decoy class is named as the same family (a control never invoked) with an AST proof (0 load sites, 1 store site; r94 receipt reads met 98/98), and the family recurrence is recorded from ReviewBattery F1 (the largest-in-bound-member superlative, since narrowed by the L1 as plan A3). 19 files under .ufo/waves/round-95/w1/ScribeLesson/; scratch deleted; no lane file outside the seat dir; no git/jj mutation; no tool installed."}
