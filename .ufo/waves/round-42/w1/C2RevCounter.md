VERDICT: defect-found

# C2-10 — code review of `tools/check-scrub-record-r42.py`

Reviewed bytes: `tools/check-scrub-record-r42.py` is byte-identical at a84fc9dec860f8bea516dff7ddfdc98223cdae52 (freeze) and f50c28d83e1832ecd7eba765caace531f45d6b27 (dispatch tip); `git show <rev>:tools/check-scrub-record-r42.py | sha256sum` → `dbe933ec8c2cca491346da76bbc104aba8ff9e5486f4dcaf572e59df3680503f` for both, matching the frozen digest. Line numbers below refer to this file (255 lines). Probe receipts: `.ufo/waves/round-42/w1/C2RevCounter/` (probes-output.txt, probes2-output.txt, grep-probes.txt, run-f50.jsonl, probes.py, probes2.py, counter-a84.py). No tools installed (system python3 3.14 / git only). Lane access was read-only (`git show`/`rev-parse`/`grep`/`ls-tree` only); all fixtures live in `/fast/scratch/hyaku/tsukuroi-r42/C2RevCounter/` (removed after receipts), committed with `-c user.name=fixture -c user.email=fixture@invalid` after a `rev-parse --show-toplevel` check.

## Run at f50c28d8 (required JSON)

Command: `python3 tools/check-scrub-record-r42.py --revision f50c28d83e1832ecd7eba765caace531f45d6b27` (lane default), observed exit=1. Full JSON in receipts `run-f50.jsonl`; key fields:

```
rows=5  quotes_ok=5  novelty_ok=5  host_ok=5  sources_ok=1  verdicts_ok=0
novelty_base_hits=0  snapshots_ok=true  capture_ok=true
transcripts_bound=0  transcripts_checked=0  verdict=FAIL
sources: {"S237": true, "S238": true}
per-row quotes good/in_window/bad: SC1 6/5/0  SC2 5/4/0  SC3 5/5/0  SC4 7/6/0  SC5 5/5/0
```

Reading: the only false conjunct is `verdicts_ok == 5` — no `w2-dispatch.json`/`w2-results.json`/`w2/*.md` exist at f50c28d8 (`git ls-tree f50c28d8 .ufo/waves/round-42` lists none), so every row's `verdicts` are null. All lexical legs pass, and the zeros are honest (below). This is the expected pre-wave-2 FAIL, not a defect.

## Verified sound

1. **QUOTE_RE greediness with embedded double quotes — correct.** `"(.+)"\s*$` (line 64) is greedy, so a quote whose text contains `"` captures to the LAST quote on the line: probe `embedded dquotes clean end` → q=`#define SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"` (probes-output.txt). All 28 Quote lines of the real entry parse (`bad=0` everywhere in the run) and every captured text occurs on its named frozen line — 28/28 substring-verified independently of the counter (`quote lines=28 failing-substring=0`, probes-output.txt), spot-checked against `git show f50c28d8:.ufo/waves/round-42/frozen/src/scrub.c` lines 67/69/856 and `CHANGES:460` (grep-probes.txt). Missing/empty quotes, 2-digit ids, wrong file names → NO-MATCH → counted `bad` (fail closed).
2. **Novelty base grep — command form works, parse correct, 0 is honest.** The unusual `--` before the pattern (`git grep -c -F -- TOKEN BASE -- corpus/knowledge SKILL.md`, lines 169-170) behaves identically to the canonical form: control token `scrub` → both forms list the same four files with counts 5/1/20/15, rc=0 (grep-probes.txt). Per-file `-c` counts parse correctly via `rsplit(':', 1)` (line 171) and the sum across files is right. All five row tokens: rc=1, no output at base → `novelty_base_hits=0` is a real zero, not a parse artifact. S237-S239 are absent at base in `corpus/SOURCES.md` (`grep -c S237` on the base blob → 0).
3. **Registry parse vs CORPUS.md — aligned.** 11 cells matches the corpus shape (CORPUS.md census: "11 columns means NF=13"); `c[7]`/`c[8]`/`c[10]` = status/opened/used-by match the header `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` (corpus/SOURCES.md line 6 at f50c28d8); `^ {0,3}` matches the corpus convention "accepts 0–3 leading ASCII spaces" (CORPUS.md:152); `mined` + opened `2026-10-26` + used-by split on `[,;]` naming the entry match CORPUS.md:103-107 and the actual S237-S239 rows (corpus/SOURCES.md:246-248 at f50c28d8).
4. **`bound()` record shapes — match the orchestrator's real files.** Round-41 `residual-dispatch.json` has `taskCall.tasks[0] = {"agent": "reviewer", "name": "C2RevPA2c", ...}` and `residual-results.json` has `results[0] = {"agent": "reviewer", "name": "C2RevPA2c", "note": null, "output": "..."}` (`git show 87c4f7c6:…`) — exactly what `bound()` reads (lines 121-128).
5. **Residual path when consulted — correct.** partly + residual `holds` → row ok (V-L: SC2 verdicts `{"crit":"holds","residual":"holds","rev":"partly"}`, `verdict_ok=true`, verdict PASS); partly + residual `fails` → not ok (V-M: `verdict_ok=false`, FAIL); partly unanswered → not ok (battery K5, `verdicts_ok=4`); two verdict lines for the row in one output → unbound (V-D, fail closed). Battery K0-K5 behaved as declared (K3 PASS, others FAIL; battery-summary-c2.jsonl `should_fail_accepted=0`, `control_accepted=1`), run with counter_rev=tree_rev=a84fc9de (C2-K3.jsonl).
6. **Window check.** Inclusive bounds, ≥1 in-window quote required; a real-but-out-of-window quote counts in `good` only — observed SC1 6/5 (line 67 < 446), SC2 5/4 (line 69 < 826), SC4 7/6 (line 342 > 330), matching a manual recount. V-K: a row whose only quote is real but out-of-window → `quotes_ok=4` → FAIL.
7. **Exit codes.** PASS→0 (V-A), FAIL→1 (the f50c28d8 run), unresolvable revision→2 with `{"error": …}` (lines 77-79), missing `--revision`→2 (argparse).
8. **Snapshot/capture pins.** Independent sha256 of the three frozen files at f50c28d8 match SNAP (lines 48-51), CAPTURE (lines 52-53) and `frozen/src/SHA256SUMS`; capture.txt lines 1,5,6,7,8,9,10 are non-blank and match the entry's host readings (grep-probes.txt).
9. **Transcript scan layout.** Glob patterns (line 140) match the real sessions tree `<sessions>/<session-uid>/<Seat>.jsonl` (verified by listing `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/`); the scan is advisory, outside the predicate, per docstring lines 25-27.

## Defects

**D1 (moderate, permissive, latent) — snapshot integrity is reported but not in the predicate.** `snapshots_ok`/`capture_ok` are output (line 246) but the predicate (lines 240-241, 244-245) omits them, so a frozen snapshot that fails its pinned digest only fails the predicate if some quote cites that file. Demonstrated V-E: scripted entry quoting only scrub.c + `frozen/src/CHANGES` replaced by `corrupted\n` → verdict **PASS with `snapshots_ok=false`** (probes-output.txt). Not reachable on current data: the real entry cites CHANGES (SC5 quotes CHANGES:460/467/468), so a corrupted CHANGES → SC5 `bad>0` → FAIL; corrupted scrub.c → all quotes bad; corrupted capture.txt → `host_ok=0<3`. Flip: FAIL→PASS, only when the corrupted snapshot is uncited. The predicate sentence is frozen in the declaration, so this is a coverage gap for the L1 to note, not an implementation deviation from the frozen predicate.

**D2 (moderate, permissive, contrived) — a bound residual `fails` is unconsulted when no w2 `partly` exists.** Line 215 (`if 'partly' in vs:`) gates the residual lookup, so with vs=[holds,holds] a fully bound residual `C2RevSC<n>c` reading `fails` is never read and lines 217-218 accept the row — contradicting docstring line 22: "any bound `fails` makes the row not ok". Demonstrated V-B: bound residual seat with `ROW SC1 VERDICT: fails` + both w2 verdicts `holds` → `verdicts_ok=5`, verdict **PASS**. Flip: FAIL→PASS; trigger requires the orchestrator to dispatch a residual seat without a partly (process anomaly).

**D3 (minor, permissive) — host check verifies only the FIRST `capture.txt:N` per Host-reading line.** HOST_RE's lazy `.*?` (line 59) applied at lines 207-209. Demonstrated V-F: `**Host reading.** ok (capture.txt:1) and bogus (capture.txt:99999).` → `host_ok=5`, PASS. The real entry's multi-ref host readings leave later refs unchecked (SC1 names :6 then :5; SC3 names :8 then :7,:10,:6) — all verified honest today (capture.txt:5,7,10 exist, non-blank). Flip: permissive only (a fabricated later ref escapes).

**D4 (minor, permissive, contrived) — verdict binding is prefix-lax and the report check is substring.** VERDICT_RE's `\b` (line 60) accepts `holds-X` as `holds` (unit probe), and line 134 `line not in rep` is a substring test. Demonstrated V-C (`ROW SC1 VERDICT: holds-X` in results output and report → binds as holds, PASS) and V-J (report line `xROW SC1 VERDICT: holdsy` → binds, PASS). Flip: permissive, requires malformed authoring.

**D5 (minor, fail-closed, breaks the output contract) — `bound()` crashes on shape anomalies instead of returning None.** A non-dict element in `taskCall.tasks` → AttributeError at line 124 (V-G: exit 1, **no JSON line**, stderr traceback); a list-shaped results file → AttributeError at lines 122/126. Exit 1 is then indistinguishable from FAIL while docstring line 34 promises "one JSON line".

**D6 (minor, fail-closed) — `registry()` drops rows on edge cases.** Empty FIRST cell: line 103 `strip('|')` eats both leading pipes → 10 cells → dropped (unit probe `empty first cell` → keys=[]); any pipe inside a cell → len≠11 → dropped (V-H → `sources_ok=0` → FAIL; contract-consistent, CORPUS.md forbids pipes in cells); 4-space indent or backticked id → dropped. An empty LAST cell survives as an empty used-by cell → fails the ENTRY check. All fail closed (PASS→FAIL only); unreachable in compliant tables today.

**D7 (minor, fail-closed, authoring hazard) — QUOTE_RE rejects an honest quote with trailing annotation.** Line 64 `"\s*$`: appending ` (checked)` after the closing quote → NO-MATCH → `bad=1` (V-I → `quotes_ok=4` → FAIL). Greediness itself is correct (verified-sound 1); the entry format tolerates no annotation after the quote.

**D8 (minor, fail-open, unreachable today) — base-grep returncode ignored.** Lines 169-171 never check `p.returncode`: any grep failure contributes 0, silently satisfying `novelty_base_hits == 0`. Demonstrated: the same command with a bad rev → stderr `fatal: unable to parse object…`, rc=128, empty stdout → the counter adds 0. Reachable only where BASE is absent (e.g. a shallow fixture clone); the lane and `--shared` battery clones carry full history. Also, per frozen docstring line 11 the grep covers `corpus/knowledge` + `SKILL.md` but not `corpus/lessons` — verified latent only (no token hits at base in corpus/lessons; grep-probes.txt).

## Observations (no predicate flip)

- Extra `## SC6`+ sections are collected by `sections()` (unit probe `SC6-collected=True`) but never scored (loop iterates ROWS only, line 182) — an unreviewed extra row is invisible; duplicate `## SC1` headers merge their lines.
- Indented or mis-cased quote lines are invisible: not counted `good` nor `bad` (line 189 filter), and their sid never enters `cited`, so their registry row escapes `sources_ok`.
- `novelty_ok` is satisfied by the token anywhere in the row text (line 206), including quote/host lines; harmless because quotes are snapshot-verified.
- Substring occurrence (line 198) is the frozen spec ("whose text occurs on the named line", docstring line 8); a one-word fragment quote passes (unit probe `fragment quote` → MATCH q=`b`) — spec-level laxity for the L1; greediness mitigates by extending the capture to the last quote on the line.
- `transcripts_bound` is advisory (docstring lines 25-27); battery K3 shows forged committed records PASS with `transcripts_bound=0` — the declared limit "committed bytes cannot tell forged orchestrator files apart" stands.
- SC3's counter window (scrub.c 1186-1206, line 58) is narrower than the S237 registry anchor "1186-1220" (corpus/SOURCES.md:246) — stricter, fail-closed; no live impact (SC3's line-1200 quote is inside both).
- The counter takes no `--scratch` flag (lines 154-156) and performs only read-only git ops; I ran it in-lane.

## Not done

- No wave-2 records exist at f50c28d8, so the verdict-binding leg was exercised only with synthetic fixtures in my scratch clone (V-A..V-M), never against real wave-2 data.
- I did not audit the frozen snapshot contents (scrub.c/CHANGES) beyond the quoted lines, nor the capture.sh methodology (out of seat scope).
- I did not run the C1 counter or the census (other seats' items).
