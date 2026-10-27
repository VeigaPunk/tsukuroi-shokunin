VERDICT: defect-found

Seat C2MutBinding, round 44 wave w1, item C2-9 — verdict-binding attacks on
`tools/check-scrub-record-r44.py` beyond controls K13–K16. 2026-10-26.

# Surface under attack

`tools/check-scrub-record-r44.py` (frozen sha256 `c96aeda99fc53336c7a12c3a492a5745bfbca28e3334d2b98f0547532a4c8059`,
verified: `sha256sum` on the lane working file matches the SCORECARD freeze). A row verdict binds when
`check-scrub-record-r44.py:210` finds the dispatch task (name, agent) exactly once, `:212-213` exactly one results
entry for that (name, agent), `declared_line()` `:187-203` yields a line that fullmatches
`ROW SR<n> VERDICT: (holds|partly|fails)` for that row (`:216-218`; the regex is `:26-27`), and the committed report's
first line equals it (`:219-224`). JSON-object outputs take `verdict_line` from the parsed object (`:190-200`, with
the K16 guard `:198-199`); any other string takes its first line with `rstrip('\r')` (`:203`, report `:222`). The
header's contract wording is `:29-32`: "the output's FIRST line exactly — no leading blank line, no leading or
trailing whitespace", report "identical text as its first line (raw, no blank line before it, no padding)".

# Method

Shared clone `/fast/scratch/hyaku/tsukuroi-r44/C2MutBinding-2/clone` of the lane (`git clone -q --shared`, origin
removed, `git rev-parse --show-toplevel` asserted equal to the clone), mirroring
`.ufo/waves/round-44/controls/run_controls_c2.py:62-95` `records()`: per variant one commit on top of BASE
`98020ece0674e0b569ee23aed10ffbee355b248e` carrying the `c2-candidate/` surface plus forged `w2-dispatch.json`,
`w2-results.json` and `w2/<seat>.md` reports, committed with `-c user.name=fixture -c user.email=fixture@invalid`,
scored with `python3 tools/check-scrub-record-r44.py --lane <clone> --revision <sha> --sessions <empty dir>`.
Each variant changes one aspect of the SR7 reviewer (`C2RevSR7`) record; SR8/SR9 and the critic seats stay
well-formed. 22 runs, receipts (one jsonl each: meta + full counter JSON, with the per-variant commit sha) in
`.ufo/waves/round-44/w1/C2MutBinding/V*.jsonl`.

Baseline: pre-data battery `battery-summary-c2.jsonl:1` shows K3 (consistent forged records) PASS with
`verdicts_ok: 3` and K13/K14/K15/K16 FAIL with `verdicts_ok: 2`. My V0 (mirror of K3) reproduces PASS:
rev `e8e5e0ebcb1fd7ae3ef5ca0885fed1c7a72e4cbd`, `verdicts_ok=3`, `per_row.SR7.verdicts.rev=holds` — harness sane.
"Expected" below is the strict ideal: a contradictory or padded record must bind nothing.

# Results (21 attacks + V0)

| variant | attack | observed | verdict |
|---|---|---|---|
| V0 | none (sanity, mirrors K3) | binds holds, PASS, `verdicts_ok=3` | sane |
| V1a | CRLF line ends, text output + report | binds holds, PASS | tolerance (see F2) |
| V1b | trailing `\r` inside JSON `verdict_line` | unbound, FAIL, `verdicts_ok=2` | rejected |
| V2a | UTF-8 BOM starting the report | unbound, FAIL | rejected |
| V2b | UTF-8 BOM starting the text output | unbound, FAIL | rejected |
| V2c | UTF-8 BOM starting `w2-results.json` | binds holds, PASS | accepted (F3) |
| V3a | Cyrillic О U+041E in `ROW`, identical in output+report | unbound, FAIL | rejected |
| V3b | Cyrillic е U+0435 in the `verdict_line` key | unbound, FAIL | rejected |
| V4a | trailing ASCII spaces on the line (output+report) | unbound, FAIL | rejected |
| V4b | trailing NBSP U+00A0 on the line | unbound, FAIL | rejected |
| V5a | recorded output is a JSON array | unbound, FAIL | rejected |
| V5b | `w2-results.json` is a non-empty top-level array | crash, exit 1, no JSON line | fails closed (F4) |
| V6 | duplicate `verdict_line` keys, fails then holds | binds holds, PASS | **GAP (F1)** |
| V6b | duplicates + `"verdict": "holds"` (K16 guard met) | binds holds, PASS | **GAP (F1)** |
| V6c | duplicates, holds then fails, holds report | unbound (report mismatch), FAIL | rejected |
| V6c2 | duplicates, holds then fails, fails report | binds fails, SR7 `verdict_ok=false`, FAIL | last key controls |
| V7 | newline inside `verdict_line` | unbound, FAIL | rejected |
| V8 | SR7 verdict duplicated under role `critic` with `fails` | reviewer binds holds; stray ignored, PASS | sanctioned |
| V8b | SR7 duplicated under the same name+role with `fails` | unbound, FAIL | rejected |
| V9 | report first line matches, body says the opposite | binds holds, PASS | sanctioned |
| V10 | report is only the verdict line | binds holds, PASS | sanctioned |
| V11 | `holds\r\r\n` double-CR padding (output+report) | binds holds, PASS | padding accepted (F2) |

# Findings

**F1 — GAP: a duplicate-`verdict_line` record binds the last value.** V6 commits the SR7 reviewer output exactly
`{"verdict_line": "ROW SR7 VERDICT: fails", "row": "SR7", "verdict_line": "ROW SR7 VERDICT: holds"}` with a report
whose first line is `ROW SR7 VERDICT: holds`. Observed at rev `40c8479c995d068e1a93144d53e5287c572fd114`: exit 0,
`per_row.SR7.verdicts.rev=holds`, `verdicts_ok=3`, overall PASS. `json.loads` (`:190`) keeps the last duplicate key,
so the K16 contradiction guard (`:198-199`) sees only `holds`; V6b shows even an explicit `"verdict": "holds"` key
satisfies it. V6c2 (key order reversed plus a `fails` report) binds `fails` — the last duplicate key fully controls
the bound word, so a broken or compromised record writer can flip a `fails` into a bound `holds` while the committed
bytes declare both. The raw record is contradictory; per the item rule ("accepting a contradictory record is a
counter gap") this is the gap. Context: RFC 8259 §4 names SHOULD be unique, and CPython and jq both keep the last
value, so downstream tooling sees the same word — the contradiction is visible only in the raw bytes. Minimal fix:
parse with an `object_pairs_hook` (or pre-scan) that refuses duplicate keys in `declared_line`/`load_json`, so such
a record binds nothing.

**F2 — minor: CR-run padding binds on the text path.** `:203` and `:222` apply `rstrip('\r')`, which strips any
number of CRs: V1a (`holds\r\n`) and V11 (`holds\r\r\n`) both bind, PASS. The header `:29-32` promises the first
line "exactly — no leading or trailing whitespace" and "identical text ... no padding"; `holds\r` is neither. The
JSON path is strict — the same trailing `\r` inside `verdict_line` unbinds (V1b) — so the two declared-line paths
disagree on identical padding.

**F3 — minor: a BOM on record files is accepted, on reports/outputs rejected.** V2c prefixes `w2-results.json`
with `EF BB BF`: observed PASS with all three rows bound — `json.loads` on *bytes* (`:182`) auto-detects
`utf-8-sig` and silently strips the BOM — while the same BOM on the report (V2a) or the text output (V2b) unbinds.
Asymmetric tolerance for the same byte prefix; a BOM'd record file is scored as if clean.

**F4 — robustness: record files typed as arrays crash the counter (fails closed).** V5b writes a non-empty
top-level JSON array to `w2-results.json`: `res = load_json(...) or {}` (`:208`) keeps the truthy list and
`res.get('results')` (`:212`) raises `AttributeError: 'list' object has no attribute 'get'` (receipt `V5b.jsonl`);
dispatch is symmetric at `:207`/`:209`. Exit 1 with a traceback and no JSON line, violating the documented output
contract ("Output: one JSON line", header) — but it cannot falsify, so this is a robustness defect, not a binding
gap. An array as the recorded *output* is properly rejected via the first-line path (V5a).

**Sanctioned by the frozen contract (observed, not gaps):** V8 — a results entry for `C2RevSR7` under role
`critic` is ignored; seat identity is the (name, agent) pair (`:212`), while a same-identity duplicate (V8b) or a
duplicated dispatch task (`:210`) is fatal. V9 — a report whose body argues `fails` binds its `holds` first line;
the binding surface is the first line by contract `:30-32` (K13/K6 already cover the opening line; the body is out
of contract by design). V10 — a report consisting of only the line satisfies "identical text as its first line".

**Rejected, fail-closed:** V1b, V2a, V2b, V3a, V3b, V4a, V4b, V5a, V6c, V7, V8b — each unbinds the attacked seat
(`verdicts_ok` drops to 2, overall FAIL). Notably V3a: the output line and report first line are byte-identical
homoglyphs, so the equality check passes and the ASCII `VERDICT_RE` fullmatch (`:216`) is the load-bearing guard.

# Which bind (the item's question)

CRLF text lines (V1a), CR-run padding (V11), BOM'd record files (V2c), duplicate-key contradictory records (V6,
V6b), body-contradicted reports (V9), only-line reports (V10), stray-role duplicates (V8). Of these, only V6/V6b
accept a contradictory record — that is the one counter gap. Everything else either binds because the frozen
contract says so (V9, V10, V8) or fails closed.

# Scope and what was not run

No C1 counter runs; no live wave-2 records exist (wave 1 produces no counted verdicts), so every leg is a forged
surface by construction. `residual-dispatch.json`/`residual-results.json` were not separately attacked — they flow
through the same `bound()` (`:206-225`), so F1–F4 apply verbatim (code-read, not executed). The transcripts leg was
pointed at an empty `--sessions` dir, exactly like the controls battery (`run_controls_c2.py:205`), so
`transcripts_bound=0` throughout. No tool installs or updates were performed (none needed).

# Restoration

Every write was inside `/fast/scratch/hyaku/tsukuroi-r44/C2MutBinding-2/` plus my report and receipts. Lane check
before scratch removal: `git status --porcelain | grep -c '^ M'` → `0` (no tracked lane file modified); the only
untracked additions under the wave dir are `.ufo/waves/round-44/w1/C2MutBinding/` (22 receipts, 92K) and this
report. Scratch dir removed after receipt copy (verified by the failing `ls` below, run after deletion).
