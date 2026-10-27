VERDICT: draft

# Seat ConnFinalQuality — item R-8: ONE QUALITY criterion from the named wave-1 findings

Inputs read (all absolute, read-only): `w1/C1CritEvasion.md` (F1 live-leg cache, F3 unenforced kill rule, V1–V10 battery), `w1/C2RevCounter.md` (F1 substring quote, F2 last-dup-wins registry, F3–F7), `w1/C2MutBinding.md` (F1 duplicate `verdict_line`, F2 CR-run, F3 BOM, F4 array crash, V0–V11 battery), `w1/C2CritControl.md` (controls X and Y). Verified in-lane: `tools/check-scrub-record-r44.py` at :167-175 (`registry`), :190-203 (`declared_line`), :216-224 (`bound`), :287 (`q in src[n-1]`); `tools/score-scrub-arm-r44.py` :47-50 (channel doc), :445 (`live_model`), :593-605 (L leg); `corpus/QUALITY.md` criteria 45, 72-73, 79-91; `SCORECARD.md` round-44 declaration. No counter was run (read-only seat); every mutant result below is quoted from committed w1 receipts named in those reports.

## 1. The five named findings are one defect class: an unwitnessed projection

Each gate reads its input through a **normalizing map** that is weaker than the contract or claim it serves, and the battery holds no input where the raw bytes are contract-forbidden while the normalized view is contract-clean — so PASS binds the projection, not the artifact:

| Finding | Normalizing map | Contract it under-reads | Demonstrated surplus |
|---|---|---|---|
| C2MutBinding F1 | `json.loads` keeps last duplicate key (`:190`); the K16 guard `:198-199` sees only the `verdict` key, not earlier `verdict_line` values | declared line "exactly", "no contradictory" record | V6 binds `holds` while raw bytes carry `verdict_line: fails` then `holds`; PASS |
| C2MutBinding F2/F3 | `rstrip('\r')` on the text/report paths (`:203`, `:222`); `json.loads` on *bytes* strips BOM (`:182`) | "no leading or trailing whitespace", "no padding" | `holds\r\r\n` binds; BOM'd `w2-results.json` binds — while the same bytes on the JSON path/report are refused (asymmetric tolerance) |
| C2RevCounter F2 | `rows[cells[0]] = cells` last-wins (`:175`), incl. rows inside fences | registry row S### is unique | appending a doctored S242 duplicate flips `sources_ok 1→0`; re-appending the true row restores it — either direction silently rewrites the scored registry |
| C2RevCounter F1 | `q in src[n-1]` substring containment (`:287`) | "occurs on its named line" | SR8 quote text `"n"` still counts `good`, `bad 0` |
| C2CritControl X/Y | props = token containment in statement cell; quotes = containment in cited line; nothing reads *direction* | the declared claim is sourced **depth** | SR7 statement asserting the exact inverse of its own quotes PASSes; SR8 write-path claim quoted by attr-macro lines PASSes |
| C1CritEvasion F1 | live leg compares output line to `live_model()` (`:593-605`) — output-agreement, not read | "the census reads `/var/lib/btrfs`, sysfs, timer links" | V1–V5 emit the constant on the live host behind a gate (mount table, statfs, script path, cwd, uid_map) + `TSUKUROI_SCRUB_DIR` selftest gate: PASS 16/16, `live_agree 1` |
| C1CritEvasion F3 | no map at all — the declared kill rule "arm writes a file in live mode" has no check in the counter | declared kill rules | declared but uninstrumented; delegated in prose only |

Adjacent findings deliberately excluded from the criterion's load-bearing set (kept honest): C2RevCounter F3 (baseless-repo vacuity — a *premise* defect, not a projection), F4/F5/F6/F7 (brittleness/info), C2MutBinding F4 (crashes closed).

## 2. What existing criteria already capture — and the uncovered remainder

- **Q45** (R21-TYPE-PROVENANCE) already demands "fixed decision gates reject duplicate JSON members" — but it scopes to decision-table gates; the verdict-binding record and the SOURCES registry are outside its text. C2MutBinding F1 and C2RevCounter F2 are the same mechanism on new surfaces.
- **Q82** (R32-FIXTURE-GATEABLE) already demands "a cached-live variant" — and the r44 battery's K7 was exactly that; it read below target only because it lacked the selftest branch. What no criterion names: detection channels *compose across legs*. V1 is the conjunction of a namespace-visible channel (watched ⇒ real logic) with the selftest's own `TSUKUROI_SCRUB_DIR` channel — per-channel arms passed the battery, the composed arm passes the counter.
- **Q87/Q88** (R39-CONTENT-UNREAD / R40-CLAIM-PARAMETERS) demand a says-the-opposite control and per-named-parameter checks — but only for parameters the *declaration names*. X/Y's "statement direction" was never a named parameter; the declaration's blanket "shape gates" disclosure covers it loosely, but discloses no *specific* unwitnessed dimension and pairs none with a mutant.
- **Q90** (R42-OBSERVED-CHANNEL) demands per-channel arms and open-channel disclosure — the declaration does name the three open channels — but says nothing about the normalizing *parse* defects (dup keys, substring, rstrip, BOM) and nothing about composites.

Uncovered remainder, therefore: **for every normalizing map a gate applies, the battery needs the discriminating pair (raw-forbidden × projection-clean), or the map's dropped dimension must be disclosed by name as an open surface.** One criterion covers all five findings without widening any declared claim.

## 3. Proposed criterion (exact text)

```
93. **A gate scores what its projection keeps, so every normalisation it performs carries a discriminating pair or a named disclosure (R44-PROJECTION-SURPLUS):** wherever a frozen counter parses its input through a map weaker than the contract it enforces — `json.loads` last-duplicate-wins, `rstrip`/BOM-tolerant first lines, a registry keyed `id → last row seen`, a quote tested by substring containment, a proposition tested by token containment, a behavioural leg scored by output agreement — the pre-data battery carries, per such map, a case whose raw bytes are forbidden by the declared contract while the normalised view is clean, and it must fail; a map with no such case makes the counter's PASS a fact about the projection, and the declaration names each still-open dropped dimension (channel composition across legs included) exactly as it names open channels, never subsumed under a generic "shape gate" label. A declared kill rule with no instrumented check is reported unenforced, not enforced. Failing examples: `w1/C2MutBinding` V6 — `{"verdict_line": "…fails", …, "verdict_line": "…holds"}` binds `holds`, PASS; `w1/C2RevCounter` — quote text `"n"` on a labelled line keeps `bad 0`, and a doctored appended S242 row flips `sources_ok`; `w1/C1CritEvasion` V1 — mount-table gate plus `TSUKUROI_SCRUB_DIR` selftest gate answers the live host from the constant, PASS; `w1/C2CritControl` X — the SR7 statement inverted against its own quotes keeps every token and PASSes. Lesson: `corpus/lessons/round-44.md` (to be recorded).
```

## 4. Why this and not one criterion per finding

Per-finding criteria (dup-key rejection, min quote length, composed-channel arms, statement-direction witness) would each be real but narrower than the mistake: the round-44 batteries failed not on *which* maps were weak but on having **no member that exercises the difference** between raw bytes and projection. The criterion is cheap to satisfy — enumerate the maps (finite, readable in the counter source), and for each either add one mutant or write one disclosure line — and it harms no axis: coverage/depth claims are unchanged; only their *reported* verification scope tightens (discernment, the seat's axis). It composes with, not duplicates, Q45/Q82/Q87/Q88/Q90: those name particular maps and parameter sets; this names the obligation over maps not yet enumerated.

## 5. Boundary kept explicit

- Does **not** require semantic (non-lexical) checks the counter family cannot express: direction/agreement may be *disclosed* (as the declaration already does at "shape gates") provided the battery's demonstrating member (X-style inverse, Y-style hollow quote) exists so the limit is measured, not asserted.
- The transcripts leg (`transcripts_bound`) is already reported outside the predicate — already conforming to this criterion's disclose-or-witness rule; noted as the model the other maps should follow.

## 6. Scope

Read-only seat: no counter runs, no fixtures built, no installs, no lane writes beyond this report; no scratch fixtures created (scratch dir `/fast/scratch/hyaku/tsukuroi-r44/ConnFinalQuality/` used only as cwd). All quoted mutant outcomes are from committed w1 receipts: `w1/C2MutBinding/V*.jsonl`, `w1/C2RevCounter/out-*.json`, `w1/C1CritEvasion/score-V*.json`, `w1/C2CritControl/missing-controls.json`.
