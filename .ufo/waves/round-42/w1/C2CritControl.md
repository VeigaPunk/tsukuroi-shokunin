VERDICT: defect-found

# C2CritControl — attack on the verdict binding of tools/check-scrub-record-r42.py (item C2-8)

Counter under test: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-record-r42.py`,
sha256 `dbe933ec8c2cca491346da76bbc104aba8ff9e5486f4dcaf572e59df3680503f` (matches the declaration), read from
tree `a84fc9dec860f8bea516dff7ddfdc98223cdae52`. Every score below is a fixture clone under
`/fast/scratch/hyaku/tsukuroi-r42/C2CritControl/` (git clone --shared of the lane, origin removed,
`git rev-parse --show-toplevel` asserted equal to the clone) committed with the fixture identity, scored with
`--lane <clone> --revision <sha>`; receipts `w1/C2CritControl/<mutant>C.py.jsonl` (frozen counter),
`<mutant>C-rec.py.jsonl` (exactly the patch proposed in §4) and `<mutant>C-fix.py.jsonl` (that patch plus the
byte-equality guard §4 rejects). `w1/C2CritControl/mut.py` is the driver, `c2counter-rec.py` and
`c2counter-fix.py` the patched counters, `w1/C2CritControl/B*.jsonl` the baseline. The fixture clones were
removed after the receipts were copied (`/fast/scratch/hyaku/tsukuroi-r42/C2CritControl/`, gone; replay with
`mut.py` against a fresh clone). All scores were produced
with the entry scripted by the control runner's method (`scripted_entry` + registry flip), i.e. a tree whose
lexical checks pass by construction; the baseline B scores `PASS verdicts_ok=5` and, with the real default
sessions dir, `PASS transcripts_bound 0/10`, so the only variable between rows is the binding.

## 1. Bottom line

The binding is fail-closed on **every structural shape the item lists** (§5). It is not fail-closed on
**meaning**: it matches the verdict *string*, not an assertion, so a row counts `holds` from artifacts that
state the row is false. Two of the three ways to do that need **no forged orchestrator record at all** — an
honest critic that disputes the row while quoting the format line is counted as `holds`.

## 2. Holes, with severity

### D1 — mention counted as assertion (HIGH; reachable without any forgery)

`VERDICT_RE` (`tools/check-scrub-record-r42.py:66`) is unanchored: `r'ROW (SC\d) VERDICT: (holds|partly|fails)\b'`,
and the report test is a plain substring (`:134`, `line not in rep.decode(...)`). Any single occurrence anywhere
in the output plus any occurrence anywhere in the report binds.

Mutant M4 — reviewer of SC1 writes, in both results `output` and its report:

```
I cannot support this row. I do not write ROW SC1 VERDICT: holds: sentence 2 is false.
```

Observed: `M4C.py.jsonl` → `verdict=PASS verdicts_ok=5`, `per_row.SC1.verdicts={"rev":"holds","crit":"holds"}`,
exit 0. A seat that rejects the row is counted as a `holds` reader.
Mutant M4b (`Rejected. This row is not ROW SC1 VERDICT: holds.`, report plain) → also `PASS`
(`M4bC.py.jsonl`). Mutant M3 (`DISPUTED: ROW SC1 VERDICT: holds is false; sentence 2 is wrong.` as the whole
report) → `PASS` (`M3C.py.jsonl`).

Impact: the predicate can be satisfied by ten seats that each say "false". This is the item's own question —
"a row verdict counts without a real wave-2 seat reading `holds`" — answered yes, with no fabrication beyond
writing the report the seat was already told to write (`make-w2-spec.py` FMT asks for the line in the report
and in the final answer).

### D2 — the report's verdict may be self-contradictory (MEDIUM-HIGH; no forgery)

The counter checks only that the bound line *occurs* in the report; it never checks that the report's only
verdict line for that row is the bound one. Mutant M2 — report is

```
# C2RevSC1

ROW SC1 VERDICT: holds

ROW SC1 VERDICT: fails
```

with the output carrying exactly one `holds` line → `PASS verdicts_ok=5` (`M2C.py.jsonl`). The artifact a human
reads says both. The docstring's "must carry that identical line" (`:18-19`) is literally true and useless here.
Related and minor: the line need not stand alone — report `XROW SC1 VERDICT: holdsX` binds (`M6cC.py.jsonl`,
`PASS`); case (`M6a`) and doubled-space (`M6b`) variants are correctly rejected.

### D3 — "exactly one line" is "exactly one line for this row": one blob binds all ten seats (MEDIUM)

`hits` is filtered by row before the uniqueness test (`:129-131`), so an output may carry all five rows' lines.
Mutant M11 — every results `output` and every report file is the same 114-byte blob

```
ROW SC1 VERDICT: holds
ROW SC2 VERDICT: holds
ROW SC3 VERDICT: holds
ROW SC4 VERDICT: holds
ROW SC5 VERDICT: holds
```

→ `PASS verdicts_ok=5` (`M11C.py.jsonl`). Five rows and ten "independent" seats are satisfied by one string;
no per-seat artifact is required to differ. The docstring's "whose final output carries exactly one
`ROW SC<n> VERDICT: …` line" (`:18`) is false as written. Adding a byte-inequality guard is *not* safe: two
honest seats that write only the line produce identical bytes, and my `o1 != o2` guard broke exactly that case
on the M16 fixture (`M16C-fix.py.jsonl`, v_ok 4). This is the same limit the K3 control records ("committed
bytes cannot tell forged orchestrator files apart") extended to seat independence; it must be **stated**, not
coded.

### D4 — the transcript cross-check can never falsify a bound verdict, and a name-only file satisfies it (MEDIUM)

`tcount`/`tbound` are incremented only inside `if ln:` (`:220-222`), and `ln` exists only when `bound` already
succeeded — so `transcript_has` is evaluated exclusively on lines the predicate has already accepted. It cannot
downgrade anything; the docstring's "a cross-check against forged orchestrator files" (`:25-27`) is a capability
claim the code does not have.

Two scored demonstrations, both with the same forged records that already score PASS:

- M15 — a scratch `--sessions` root with one file per seat, named `<sid>/C2RevSC1.jsonl` … `C2CritSC5.jsonl`,
  whose entire content is the 114-byte blob (no session, no transcript, no round) → `PASS transcripts_bound 10/10`
  (`M15C.py.jsonl`, `M14C.py.jsonl` with a `{"role":"assistant",…}` wrapper). 114 bytes per seat makes the
  cross-check read 10/10.
- M15c — the same files one directory deeper (`<sid>/L1Parent/<name>.jsonl`, the layout real nested transcripts
  use, e.g. `~/.omp/agent/sessions/-Projects-shokunin/2026-10-25T06-15-52-413Z_…/L1Chousa47/L1Chousa47.SweepC1Corpus.jsonl`)
  → `transcripts_bound 0/10` (`M15cC.py.jsonl`). The glob `os.path.join(sessions, '*', name)` (`:139-141`) is
  one level deep, so a sub-orchestrated seat is invisible: 0/10 means "not found at that depth", not "forged".

Also: the glob has no round/date filter and the line text is round-invariant, so from round 43 on, a same-named
seat in any earlier round satisfies it for free (`find ~/.omp/agent/sessions -name 'C2RevSC*' -o -name 'C2CritSC*'`
→ 0 files today, which is why today's baseline is `0/10`).

Guard note: `make-w2-spec.py:72-73` asserts only `'VERDICT: holds' not in prompt/context`; a prompt that spelled
`ROW SC1 VERDICT: partly` passes that assert. This cannot create a PASS by itself (D4's code path), it only
corrupts the reported cross-check count on the `partly` path.

### D5 — a "seat" is a name string, not a dispatch body (LOW)

Mutant M13 — dispatch tasks reduced to `{"name": …, "agent": …}`, no `task` text → `PASS` (`M13C.py.jsonl`).
`bound` never looks at what the seat was asked, so "the seat must be a task of `w2-dispatch.json`" is satisfied
by a two-key object. Same family: duplicate dispatch entries for the same seat are tolerated (`M20`, PASS),
which is harmless.

### D6 — residual semantics: not revocable, and `verdicts_ok` overstates (LOW, tradeoff)

- M10 — an extra residual `C2RevSC1c` reading `fails` on a row whose two wave-2 seats read `holds` is never
  consulted (`resid` is resolved only when `'partly' in vs`, `:216-219`) → `PASS` (`M10C.py.jsonl`). Once both
  seats say holds, no later falsifier can demote the row.
- M16 — both seats `partly`, one residual `holds` → `PASS` with `verdicts_ok=5` (`M16C.py.jsonl`): a row with
  **zero** holds among its two wave-2 seats counts inside `verdicts_ok`. That matches the declared rule, but the
  receipt label "verdicts_ok == 5" will read as "five rows both-holds". Say what it counts.

## 3. What the binding does reject (confirmed fail-closed, no defect)

| mutant | shape | result |
|---|---|---|
| M1 | output carries `holds` and `fails` lines for the same row | `FAIL`, rev `None` (`M1C.py.jsonl`) |
| M1b | the same line twice in one output | `FAIL`, rev `None` (`M1bC.py.jsonl`) |
| M5 | right name, `agent: critic` in dispatch *and* results | `FAIL`, rev `None` (`M5C.py.jsonl`) |
| M6a / M6b | report line lower-cased / double space after colon | `FAIL` (`M6aC.py.jsonl`, `M6bC.py.jsonl`) |
| M7 | results `output: null` | `FAIL` (`M7C.py.jsonl`) |
| M8 | output word `Holds` | `FAIL` (`M8C.py.jsonl`) |
| M9 | reviewer `partly`, critic `fails`, residual `holds` | `FAIL` (`M9C.py.jsonl`) |
| M12 | shared blob + `ROW SC3 VERDICT: fails` in the SC3 output | `FAIL`, SC3 not ok (`M12C.py.jsonl`) |
| M17 | residual reads `partly` | `FAIL` (`M17C.py.jsonl`) |
| M18 | critic `fails`, reviewer `holds` | `FAIL` (`M18C.py.jsonl`) |
| M19 / M21 | dispatch without `taskCall.tasks` / empty results list | `FAIL`, `verdicts_ok=0`, no crash |
| M22 | output holds, report has no line | `FAIL` (`M22C.py.jsonl`) |
| M23 | output carries only another row's line | `FAIL` (`M23C.py.jsonl`) |

So the structural parse is sound; the defect is that it validates *strings present*, not *claims made*.

## 4. Smallest safe correction (D1 and the embedded-line part of D2), with cost

Two-line semantic change plus a report test; no new data source:

```python
-VERDICT_RE = re.compile(r'ROW (SC\d) VERDICT: (holds|partly|fails)\b')
+VERDICT_RE = re.compile(r'(?m)^ROW (SC\d) VERDICT: (holds|partly|fails)[ \t]*$')
+ANYV_RE = re.compile(r'(?m)^ROW (SC\d) VERDICT: (holds|partly|fails)\b')

-    line = hits[0].group(0)
-    rep = show(lane, rev, f'{WAVE}/{wave}/{name}.md')
-    if rep is None or line not in rep.decode(errors='replace'):
-        return None, None
-    return hits[0].group(2), line
+    line = hits[0].group(0).strip()
+    rep = show(lane, rev, f'{WAVE}/{wave}/{name}.md')
+    if rep is None:
+        return None, None
+    rl = [x.strip() for x in rep.decode(errors='replace').splitlines()]
+    if line not in rl:                       # the line, as a line of its own
+        return None, None
+    words = {m.group(2) for m in ANYV_RE.finditer('\n'.join(rl)) if m.group(1) == row}
+    if len(words) != 1:                      # no second, contradictory verdict line
+        return None, None
```

Verified exactly as written, arity unchanged (`w1/C2CritControl/c2counter-rec.py`, receipts `*C-rec.py.jsonl`):
baseline B still `PASS` (v_ok 5, `BC-rec.py.jsonl`); M2, M3, M4, M4b, M6c flip `PASS → FAIL` (`M2/M3/M4/M4b/M6c`
`C-rec.py.jsonl`); every fail-closed control above stays `FAIL`; M11 stays `PASS` (`M11C-rec.py.jsonl`) — D3 is
untouched, as intended. The receipts also carry `c2counter-fix.py` / `*C-fix.py.jsonl`: that is this patch plus a
`rev_output != crit_output` guard run only to test whether D3 can be coded away; it cannot (M16 breaks), so it
is **not** part of the recommendation.

Costs, in order of importance:

1. The counter is frozen at `dbe933ec…`; the patch changes its sha256, so it must be re-declared/re-frozen.
2. The pre-data control battery must be re-scored: `controls/run_controls_c2.py:86` writes
   `output: f'done. ROW {row} VERDICT: {v}'` — prefixed text that the anchored regex rejects. Mutant M30 is
   exactly that K3 fixture shape: `PASS` under the frozen counter (`M30C.py.jsonl`, matching
   `controls/C2-K3.jsonl` exit 0) and `FAIL verdicts_ok=0` under the corrected one (`M30C-rec.py.jsonl`,
   `M30C-fix.py.jsonl`).
   K0-K5 would have to be re-run with the `\n` added.
3. It does not touch D3/D4/D5: one blob still binds ten seats, `transcripts_bound` still cannot falsify.

Cheaper alternative that needs **no** re-freeze: keep the counter and close D1/D2 by discipline at the source.
`make-w2-spec.py` already emits "Write that line once in the report and once in the final answer, nowhere else"
(FMT, `make-w2-spec.py:66-69`); it is not yet built into `w2-spec.json` (no such file in the tree), so the
sentence can still be hardened to "the line must be the first line of your report and a line of its own in the
final answer; never quote another seat's or your own verdict line inside prose". That closes D1 for compliant
seats but not for a seat that disputes the row *and* writes the line — and the counter cannot tell the
difference. If the intent is that a disputing seat must not count as holds, only §4's patch does it.

If D3/D4 are accepted, the docstring must stop claiming more than the code does — proposed replacement text
for `:17-27`:

> A row verdict counts only through the orchestrator's records committed at the revision: the seat must be a
> task of `w2-dispatch.json` (`taskCall.tasks`, name and agent role), have a `w2-results.json` entry with the
> same name and role, whose final output carries exactly one line `ROW SC<n> VERDICT: <holds|partly|fails>`
> on a line of its own, and the committed report `.ufo/waves/round-42/w2/<name>.md` must carry that line as a
> line of its own and no other verdict line for the same row. Limit: these are committed bytes. The counter
> cannot tell a seat from a copy of a text: a single five-line blob used as every output and every report binds
> all ten seats (control M11), and none of it is distinguishable from a real wave. `transcripts_bound` is
> reported for the record only: it counts a seat-named file under the sessions root that contains the line, so
> a planted file satisfies it and a nested (sub-orchestrated) transcript is invisible to the glob. It is not
> evidence that a seat read anything, and it is not part of the predicate.

## 5. Not done / limits of this report

- No wave-2 records exist at the tip (`w2-dispatch.json`, `w2-results.json`, `w2/`, `residual/` are all absent
  from `87c4f7c6`), so nothing here scores real wave-2 data; every verdict above is a fixture score.
- I did not touch the lane (no tracked write, no git mutation), the fleet repo, `~/.omp/agent/sessions`
  (all session demonstrations use a scratch `--sessions` dir), or the host.
- I did not re-run the K0-K5 battery (it is the L1's to re-score after any re-freeze).
- I did not evaluate the lexical planes (quotes/novelty/host/registry); other seats own them. Note only that
  `sources_ok == 1` and `host_ok >= 3` are separate conjuncts I left alone.
