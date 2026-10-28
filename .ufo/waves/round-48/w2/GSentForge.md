VERDICT: defect-found

# C2-S1 — can a seat that was never spawned be bound? (bind-forging attempt)

Sandbox: `/fast/scratch/hyaku/tsukuroi-r48/GSentForge/sbx`, `git clone --shared` of the lane,
`--detach ae99f021b76f8eb1c8805d32d80644464afb1ff6`; `git rev-parse --show-toplevel` printed
`/fast/scratch/hyaku/tsukuroi-r48/GSentForge/sbx` before every commit; every commit ran with
`-c user.name=fixture -c user.email=fixture@invalid`. All 18 counted seats, both JSON files, all
three marks and (in the §6 attacks) the rows themselves were written **only** inside that clone. The lane was never written, and
nothing outside the sandbox was touched.

| attack | frozen C2 counter | my `check-wave-provenance.py` |
|---|---|---|
| fabricate dispatch+results+18 reports+3 marks (no spawn) | **PASS** | PASS — the documented limit |
| …with content-free bodies that admit they read nothing | **PASS** | PASS |
| …with one real quoted line per seat (the cost floor) | **PASS** | PASS |
| rewrite a grounding row, re-attest 6 seats | **PASS** | **FIND** (P10) |
| revert GR2 to the r47-rejected wording, re-attest | **PASS** | **FIND** (P10) |
| `partly` dissent + zero its own hash line | **PASS** | **FIND** (P5) |
| `partly` dissent, untouched (control) | FAIL | PASS |
| traversal / symlink / duplicate-key / symlinked wave dir | FAIL (closed) | n/a |

Headline: **yes.** The frozen C2 counter
(`tools/check-scrub-admission-r48.py` @ae99f021) admits a whole fabricated wave — dispatch,
results, 18 reports, three marks — with no orchestrator having spawned anything, and it also admits
a rewrite of the grounding rows themselves. The documented limit ("committed bytes cannot prove who
spawned a seat") is real, but it is not the whole story: the counter does not read the frozen row
record, does not read the wave registry or the ready markers, and does not read report content. A
cheap committed-bytes check closes the row-rewrite hole outright and detects most of the forgery
shapes; the spawn-authorship residue stays out-of-band.

## Axes

- **C2 (depth gate)** — the axis under attack. Two distinct failures: false admission of a
  never-spawned cohort, and false admission of *changed bytes* (rows edited after freeze).
- **security** — authority confusion: `{wave}-dispatch.json`, `{wave}-results.json` and
  `{wave}/<seat>.md` are all authored by the same principal (the L1) that is being checked.
  Self-attestation is being counted as attestation by a third party.
- **depth (of the fix)** — a fix that only blesses more files would repeat the same error. The
  cheap fix must anchor to a record the L1 wrote *before* it knew the answer (the freeze record,
  the pre-data controls) or to a signal the L1 cannot author (the harness roster).

## 1. What the frozen counter actually reads

`tools/check-scrub-admission-r48.py` (@ae99f021), read through `git show`:

- `dispatches()` — line 162-164: reads exactly `.ufo/waves/round-48/w2-dispatch.json`.
- `bind()` — line 185: reads `.ufo/waves/round-48/w2-results.json`, then `{wave}/{seat}.md`.
- `snapshots()` / CITE map — lines 46-66: the only digest pins in the file are the *source
  snapshots* (.ufo/waves/round-4{2,3,4,5}/frozen/src/*), never the grounding entry.
- `grep -n "registry\|ready\|swarm-\|agentId"` over the frozen file → **no match**. The counter
  never opens `w2/swarm-registry.json`, `w2.ready`, or `w2.ready.dispatched`.
- `grep -n "gr-section-hashes\|FROZEN.md\|fe77ac76"` → **no match**. The frozen record
  `.ufo/waves/round-48/frozen/gr-section-hashes.json` (@ae99f021, contents GR1 `fe77ac76…9ca8`,
  GR2 `e0b391e1…52ce`, GR3 `43430a14…c32c`; also mirrored in `frozen/FROZEN.md` line 13) is
  committed at freeze and **never consulted**.

Consequence: every hash the counter compares is *recomputed from the bytes at `--revision`*. A row
whose text was rewritten after freeze yields a new hash, and the seats that quote that new hash are
consistent with each other. Self-consistency passes; the freeze is not enforced.

## 2. The forgery, cheapest first

Receipt: `forgeB-counter.json`, `forgeB-provenance.json`; builder `forge.py`.
`python3 tools/check-scrub-admission-r48.py --lane ./sbx --revision HEAD` →

```
{"structural_ok": 1, "quotes_ok": 3, "verdicts_ok": 3, "marks_ok": 3, "verdict": "PASS"}
per_row credited: GR1 6, GR2 6, GR3 6 ; distinct_bodies: all true
```

Cost of the forgery that clears it:

1. `w2-dispatch.json` with `taskCall.tasks` naming the 18 seats with their roles, plus
   `registry.members` and honest `counts` (a 12-line dict comprehension).
2. `w2-results.json` with one entry per seat, `output` = a JSON string containing
   `report`/`row`/`verdict`/`section_sha256`. Nothing checks that the value is the *delivered*
   output; the frozen counter only requires the entry to exist with the right `name`/`agent`.
3. 18 report files whose first two lines are the row hash and `holds`, and a body ≥300 bytes with one
   file:line citation whose number is inside a pinned snapshot.
4. The three marks: `## Gate status — round 48 (GR1-GR3 admitted)` in the entry,
   `## Scrub grounding — round 48 admission` in `SKILL.md`, and a README line containing both
   `btrfs-scrub-grounding-r45.md` and `admitted round 48` and no negation.

The bare version without registry/counts/JSON outputs fails (`forgeA-counter.json`, legs
`verdicts_ok:0`, findings P1/P2/P3/P6/P7 in `forgeA-provenance.json`). So the counter has *some*
shape teeth; they cost about ten minutes to satisfy.

## 3. Content is not read at all — the bodies may be open nonsense

`absurd.py` → `absurd-counter.json`. Bodies that say, verbatim, "I did not read any source … these
four lines exist, therefore the row holds … I am asserting this without opening them", each with a
unique filler sentence so K23 (distinct bodies) is satisfied and the citations point at real line
numbers →

```
{"structural_ok":1,"quotes_ok":3,"verdicts_ok":3,"marks_ok":3,"verdict":"PASS"}
credited: GR1 6, GR2 6, GR3 6
```

Without the unique filler, the same nonsense bodies are rejected by K23 alone (`verdicts_ok: 0`) —
so distinctness, not substance, is what the counter is measuring.

**Entry-level quotes are checked properly** (`quote_legs`, `QUOTE_RE`, normalized containment): a
bogus `**Quote.**` line fails `quotes_ok`. That is the one place the counter reads text against
bytes.

**Cost floor for a body that clears everything**: one real quoted line plus one citation to that
line plus ~300 bytes of prose (`quote_cite.py` → `quote-cite-counter.json` → PASS). Under 300 bytes
the seat earns nothing (`report_citations_ok` → "report body under 300 bytes"), so the floor is
real but trivially met: `onequote.py` → `onequote-counter.json` also PASSes.

## 4. Path and encoding tricks — all fail closed (good)

`tricks.py` → `tricks-summary.json` (each trick starts from tip `b727535`, mutates, commits, runs
the frozen counter; baseline T0 PASSes with 6 credited seats):

| trick | result | mechanism |
|---|---|---|
| T1 seat named `../w1/R48RevGR1a`, report parked in `w1/` | seat unbound ("no report w2/R48RevGR1a.md"); `git show HEAD:.ufo/waves/round-48/w2/../w1/R48RevGR1a.md` → **exit 128** | `bind()` builds `{wave}/{seat}.md` from the seat string but `show()` is `git show`, which normalizes and then refuses the traversal — the report is not reachable |
| T2 report is a relative symlink to a sibling report | "report too short" (the blob is the symlink text) | `git show` returns the link target, not the content |
| T3 report is an absolute symlink to `/etc/hostname` | "report too short" | same; no host file is ever read |
| T4 report only in `w1/` | "no report w2/R48RevGR1a.md" | fixed path |
| T5 `w2/` itself replaced by a symlink to `w2-alt` | `verdicts_ok: 0`, whole wave FAIL | `git show` treats the symlink as a blob |
| T6 duplicate `"wave"` key in the dispatch | "dispatched 0 times", FAIL | `no_dups` object hook raises `DupKey`, `load_obj` returns None, every seat unbinds — fails closed, and `main()` catches it in-band |
| T7 seat dispatched twice | seat unbound ("dispatched 2 times"), **row still PASS, 5 credited** | `len(hits) != 1` |
| T8 results `agent` disagrees with dispatch | seat unbound, **row still PASS, 5 credited** | exact-one-entry + role equality |
| T9 two results entries for one seat | seat unbound, **row still PASS, 5 credited** | same |
| T10 CRLF report | seat unbound (line 1 is `ROW GR1 VERDICT: holds\r`), **row still PASS, 5 credited** | `fullmatch` |

So: no traversal, no symlink, no cross-wave file, no duplicate-key or duplicate-entry confusion.
The path layer is sound. **T7-T10 are seat-scoped, not row-scoped**: the row still PASSes on the
remaining five credited seats, so a single mangled seat is silently absorbed. That is by design
(≥3 seats) but it means the counter has no notion of "the cohort the orchestrator dispatched".

## 5. Negative laundering — the A2 rule is real but has a bypass

`launder.py`, `launder2.py` → `launder-summary.json`, `launder2-summary.json`.

| probe | frozen counter |
|---|---|
| L1 `fails` on the current hash | **FAIL** — `blocking: [R48RevGR1a]` (A2 holds) |
| L8 `fails` + correct hash + 20-byte body | **FAIL** — A2 blocks regardless of citation credit |
| L9 `fails` + correct hash + unresolvable `nosuchfile.c:1` | **FAIL** — a citation slip never launders a negative |
| L7 `fails` + stale/zeroed hash line | **FAIL** — but via `any_fails: true`, not via `blocking` (`blocking: []`); the word `fails` is hash-independent |
| **L2/L5** `fails` + a duplicate dispatch entry for that seat | **PASS**, 5 credited, `blocking: []` |
| **L3** `fails` + results `agent` flipped to `critic` | **PASS**, 5 credited, `blocking: []` |
| **L6** `fails`, then the report emptied | **PASS**, 5 credited, `blocking: []` |
| **O1** report blanked + results `output` reduced to `{"report":…,"row":"GR1"}` | **PASS**, no finding anywhere |

Mechanism: A2 blocks only a seat that *binds* (`bind()` returns a verdict) and whose hash equals
the current one. Anything that makes `bind()` return `None` — a second dispatch entry, a role
mismatch, a second results entry, an empty report — removes the dissent from the blocking set while
the row still clears `>=3 credited`. `unbound_for_citation` is informational only.

**The cheapest version needs no dispatch edit at all** (`hash-launder-summary.json`,
`verify-matrix.json`):

| probe | frozen counter |
|---|---|
| `partly` on the current hash (control) | **FAIL**, `blocking: [R48RevGR1a]` |
| **`partly`, then its own `SECTION SHA256:` line replaced with 64 zeros** | **PASS**, `blocking: []`, 5 credited |
| `fails`, then the same 64-zero hash line | FAIL — but only because `any_fails` is hash-independent |

So one character-level edit to a single report line defuses a `partly`. The `fails` word is the only
verdict with hash-independent teeth, and `partly` — the verdict that closed rounds 47 and 46 — is
blocking only while its hash line is intact.

**Severity: high.** This is the exact failure mode the round was created to prevent. r47 closed
`rejected-honest-stop` because a counted critic read GR2 `partly`. At this revision:

- corrupting that critic's `SECTION SHA256:` line → PASS;
- dispatching that critic twice → PASS;
- flipping its results `agent` to `critic` (so the seat no longer matches its dispatch role) → PASS;
- emptying its report → PASS (`L6`);
- blanking report + verdict-free results output → PASS with no finding anywhere (`O1`).

Five small edits, five admissions of the thing the round exists to refuse. Note also that the
`fails`-with-stale-hash probe still FAILs through `any_fails`, so the asymmetry is one-directional:
a `fails` cannot be laundered this way, a `partly` can.

## 6. Row rewriting — the freeze is not enforced (most damaging)

`rowwarp.py` → `rowwarp-summary.json`, `rowwarp-counter.json`.
Insert two lines of prose into GR1, recompute the section hash, rewrite the hash line of the six
GR1 seats, commit. The frozen counter:

```
{"verdict":"PASS","structural_ok":1,"quotes_ok":3,"verdicts_ok":3,"marks_ok":3}
GR1: 6 credited, 12/12 quotes ok, row_ok true
hash_before fe77ac76…9ca8 → hash_after 8a28fad0…dd8f
"fe77ac76…9ca8" appears in the counter output: false
```

`compose.py` → `compose-summary.json`. All three rows replaced with statements the pinned sources
**contradict** ("the unmount suspend path cancels the scrub", "KillMode is set to none", "parsed by
an unreviewed shell wrapper"), each with one `**Quote.**` line that does verify, and 18 content-free
bodies that say so in plain words:

```
{"counter":"PASS","legs":{"structural_ok":1,"quotes_ok":3,"verdicts_ok":3,"marks_ok":3},
 credited {"GR1":6,"GR2":6,"GR3":6},
 hashes_now GR1 5ebfb4d5… GR2 f8b1b424… GR3 844368c3…,
 frozen_record_says GR1 fe77ac76… GR2 e0b391e1… GR3 43430a14…}
```

`revert_gr2.py` → `revert-gr2-summary.json`. The single most damaging revert: put GR2 back to the
wording round 47 rejected — "the unmount suspend path calls `btrfs_scrub_cancel`" — recompute, and
re-attest. **PASS, 6 credited on GR2.** The pinned source refutes it: the
`btrfs_dev_replace_suspend_for_unmount` body at `dev-replace.c:1171-1195` only sets
`BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED` and never calls the cancel helper; the only
`btrfs_scrub_cancel` calls in that file are at `dev-replace.c:1111` and `dev-replace.c:1144`, both
inside `btrfs_dev_replace_cancel`, not in the suspend path.

The admission gate therefore certifies "some cohort agreed on some bytes at the measured revision",
not "the cohort the orchestrator spawned agreed on the bytes that were frozen".

## 7. What detects it from committed bytes

Candidate check: `check-wave-provenance.py` (in this wave dir). Eight hard checks (P1-P7, P9, P10)
plus two soft ones. **Calibration first** — it must pass a real committed wave:

`python3 check-wave-provenance.py --lane <lane> --revision HEAD --round 47 --wave w1` →
`{"verdict":"PASS","findings":[],"soft":39}` (`genuine-r47-w1.json`). P1 counts, P2 identity,
P3 JSON outputs, P4 report paths (62 of 64 declare a path; all 62 normalize to their own
`w1/<seat>.md`; the other 2 declare none and are soft, not findings), P5 claim binding, P6 dispatch
added before every report (65 artifacts checked, dispatch commit `e31070a9`), P7 ready + spawn map,
P9, and P10 (no freeze record for r47 → skipped) all pass on the genuine wave.

Against the forgeries:

| build | frozen counter | this check |
|---|---|---|
| A: bare forge | FAIL | FIND (P1,P2,P3,P6,P7) |
| B: faithful forge | PASS | **PASS** — the documented limit |
| B + absurd bodies | PASS | PASS |
| B + one quoted line | PASS | PASS |
| T7 duplicate dispatch entry | PASS | FIND (P1,P2,P9) |
| T8 role mismatch | PASS | FIND (P2) |
| T9 duplicate results entry | PASS | FIND (P1,P2) |
| T10 CRLF report | PASS | **PASS** — still undetected (205-byte report is short but P4/P5 only inspect declared claims; nothing compares size) |
| L2/L3/L6 launder | PASS | FIND (P1/P2/P5) |
| O1 blanked seat | PASS | **PASS** — still undetected |
| O3 deleted negative, coherent counts | PASS | FIND (P9) |
| post-hoc roster deletion (separate commit) | PASS | FIND (P9) `late-edit-summary.json` |
| GR1 rewritten, re-attested | PASS | FIND (P5,P10) `rowwarp-provenance.json` |
| `partly` + zeroed own hash | PASS | FIND (P5) |
| `partly` on the current hash (control) | FAIL | PASS — correctly no finding on a well-formed negative |

P10 is the one that matters most and is the cheapest: read the freeze record the L1 already
committed and compare its three hashes to the recomputed ones. It is 12 lines, it needs no new data,
and it closes §6 completely. P9 (the dispatch file must not be edited after the first counted report
lands) catches roster surgery and costs one `git log -1 -- <dispatch>` per seat.

Two honest negatives:

- **O1 is not caught by any committed-bytes check I found.** Blanking a report and reducing the
  results output to a verdict-free object leaves a wave that is internally perfect: the seat simply
  never bound. The counter cannot distinguish "never spawned" from "spawned badly", and neither can
  any signature over these files. Only the spawn record or the harness roster can.
- **P8 (task text) and P5 (claim binding) are self-attestation too.** A forger who writes the
  results `output` by hand satisfies them, as `forge.py` shows. They raise the cost, not the bar.

Cheap out-of-band check that does decide it: the harness answers for every agent it knows.
`history://R48GhostSeatZq` → `Unknown agent: R48GhostSeatZq`; `history://R48RevGR1a` → transcript
present; `agent://R48RevGR1a` → the delivered output. An L1 that never dispatched a seat cannot
produce a transcript, so "every dispatched seat has a transcript whose final output contains the
bytes it claims to have delivered" is a decidable check at merge time — the L1 can run it, a
reviewer cannot (`receipts/ghost-probe.txt`). It is not a committed-bytes check and should not be
described as one.

## 8. Answers to the item's questions

1. **Can a seat that was never spawned be bound?** Yes, at a cost of ~10 minutes and ~200 lines of
   JSON; `forgeB-counter.json` is a PASS with no orchestrator involved. The documented limit is
   confirmed, and it is broader than "authorship": the counter also accepts rewritten rows.
2. **Is the frozen counter's `verdicts_ok` sensitive to dissent?** Only while the dissent binds.
   Three one-line edits (duplicate dispatch entry, role flip, empty report) make it vanish while
   the row still passes. This is worse than the documented limit because it needs no forgery of a
   positive — only the removal of a negative.
3. **Do path tricks work?** No. Traversal, relative and absolute symlinks, a symlinked wave
   directory, a duplicate JSON key, duplicate dispatch/results entries, and CRLF all fail closed,
   either seat-scoped or wave-scoped. That layer is well built.
4. **What cheap committed-bytes check detects it?** P10 (frozen-record comparison) closes row
   rewriting completely; P9 (dispatch not edited after the first report) closes roster surgery;
   P1/P2/P5 close the launder variants. All three are small, need no new data, and pass the genuine
   round-47 wave unchanged.

## 9. Smallest remediation (proposed text, not applied — I hold no lane write)

Append to the frozen counter as a new fail-closed leg, before the verdicts loop:

```python
    # F4 (round-48 w2/GSentForge): the admitted bytes must be the frozen bytes. The freeze
    # record is committed before any seat runs; a row whose section hash moved after the freeze
    # is a redesign, not an admission, whatever the seats say.
    frz = load_obj(lane, rev, f'{WAVES}/frozen/gr-section-hashes.json')
    frozen_ok = 1
    if not isinstance(frz, dict):
        frozen_ok = 0
        problems.append('frozen/gr-section-hashes.json unreadable')
    else:
        for row in ROWS:
            if hashes.get(row) != frz.get(row):
                frozen_ok = 0
                problems.append(f'{row}: section hash {hashes.get(row)} != frozen {frz.get(row)}')
```

and add `and frozen_ok == 1` to `ok` and to `PREDICATE`. Verified cost on the genuine bytes at
`ae99f021`: the record's three values equal the counter's three values exactly
(`--section-hash` output above), so the leg is 1 at freeze and 0 on `compose`/`revert_gr2`/`rowwarp`.

Second, fail-closed on dissenting-seat disappearance — replace the `blocking` computation with a
rule that a seat whose dispatch or results entry is not exactly one, or whose report is unreadable,
is a **negative** rather than an absent seat *when the same seat name appears in the dispatch at
all*:

```python
        # A4: a seat that is dispatched but does not bind is a defect, never an absence.
        broken = [n for n, s in seats.items()
                  if s['verdict'] is None and s['detail'] not in ('not dispatched',)]
        blocking = [n for n, s in seats.items()
                    if s['verdict'] in ('partly', 'fails') and s['hash'] == cur] + broken
```

This turns L2/L3/L6/O1/T7-T10 from silently-absorbed into row-blocking, and needs no new data.

## 10. Not done / limits of this seat

- I did not run the census or any C1 counter; out of scope for this item.
- Mismatch noted and left open: `forgeB`'s 18 reports are ~20-24 added lines each and
  `w2-results.json` is 116 lines — the whole forgery is **518 inserted lines across 22 files**
  (`git show --stat b727535a`), i.e. small enough to review by eye at merge time. I did not test
  whether a reviewer reading the diff would notice; that is a human-factor question, not a
  committed-bytes check.
- I did not test a forgery against the *live* w2 bytes under `/home/vgpnk/Projects/shokunin/
  tsukuroi-shokunin/.ufo/waves/round-48/w2/` (mutable working tree, not bytes under test). All
  measurements are against `ae99f021` and fixture tips derived from it.
- I did not attempt to defeat the harness roster check; a seat with the ability to write
  `history://` transcripts would need the harness, which is out of the lane's threat model here.
- The receipts bundle in this directory is the full raw output; the numbers quoted above are
  copied from those files verbatim.
- No tool installs were needed (python3 3.14, git 2.x already present); nothing was installed,
  upgraded, or paused.
