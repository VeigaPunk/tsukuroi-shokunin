VERDICT: defect-found

# Item C1-R3 — review of the frozen counter `tools/check-scrub-admission-r47.py` (counter review pass 3)

Seat C1RevCounter3, tsukuroi lane round 47 wave w1. Reviewed artifact:
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-admission-r47.py` against its docstring (lines 1–35) and the C1 declaration row (`SCORECARD.md:3065`).

## Method

- Hash check: `git show 77e9e2b2e96b85d8f048ae2087e246a542b71611:tools/check-scrub-admission-r47.py | sha256sum` → `e20c322171db76f1d08b51066e602707516f62eccdf3f64ca8356c69767f023b`; lane-tip file sha256 identical (receipt `C1RevCounter3/counter-checks.txt`).
- Read the full counter (383 lines) and the GR1/GR2/GR3 rows of `corpus/knowledge/btrfs-scrub-grounding-r45.md`.
- Fixture scoring: `git clone -q --shared` of the lane into `/fast/scratch/hyaku/tsukuroi-r47/C1RevCounter3/fx.gKRHKR` (toplevel asserted, `git remote remove origin`), variants committed with `-c user.name=fixture -c user.email=fixture@invalid`, scored with the lane's frozen counter via `--lane <clone> --revision <sha>`; `TMPDIR=/fast/scratch/hyaku/tsukuroi-r47/C1RevCounter3`. Fixture base = lane tip `f6bc6d05` (the entry rows at that commit are the live rows). Full observed outputs: receipts `variant-results.json`, `variant-results-2.json`, `extra-probes.txt`.
- Battery cross-read: `.ufo/waves/round-47/controls/battery-summary-r47.jsonl` — 12/12 as expected, including C1-K0/K1/K22a/K23a/F1a/F1b/F2a/F3a and C1-K-pass.

## Consistency: predicate sentence in code, docstring, declaration, receipt labels

- Code: `PREDICATE` constant `tools/check-scrub-admission-r47.py:84`; applied verbatim at `:373` (`ok = structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and marks_ok == 3`).
- Docstring usage `:34–35` (command form, exit codes 0/1/2, one JSON line).
- Declaration: `SCORECARD.md:3065` — the same predicate string, and the F1/F2/F3/K22/K23 closures map to the structural/quotes/verdicts/marks legs exactly as coded (`:134–146` F1 extent, `:78`+`:370–371` F2 marks, `:99–105`+`:122–123` F3 in-band parse, `:229–236`+`:270–281` K22 entry quotes, `:288–292` K22 seat citations, `:344–352` K23 distinct bodies).
- Receipt labels: output JSON keys `structural_ok/quotes_ok/verdicts_ok/marks_ok/per_row/distinct_bodies/citation_problems` (`:376–378`) are the fields `controls/battery.py` records. Consistent.
- Snapshot table: all ten (sid,file) pins in `SNAPSHOTS` (`:45–70`) match the frozen `SHA256SUMS` files (round-42/src, round-44/src, round-45/src) and the direct digest of `round-45/frozen/hostcap/capture.txt` (receipt `counter-checks.txt`).

## Findings (severity order)

### F1 (medium) — the README admission mark is grantable to reversal text that `NEGATE_RE` does not name

`NEGATE_RE` (`:78`) lists `unadmitted|not admitted|never admitted|stay pending|stays pending`. The README leg (`:370–371`) grants the mark to any line containing both `btrfs-scrub-grounding-r45.md` and `admitted round 47` (`MARK_README`, `:77`) that does not match that list. A line negating the admission in other words earns it:

Fixture `v-negreadme-evasion` (driver1): README line `- btrfs-scrub-grounding-r45.md admitted round 47 by administrative error; reversed within the hour.` → observed `marks={'entry': True, 'readme': True, 'skill': True}`, `marks_ok=3`, verdict `PASS` (receipt `variant-results.json`). The line is negating text (the admission was reversed) and F2's docstring intent ("admission marks must not be grantable to negating text", `:11–12`) is violated. The entry (`:367`) and SKILL (`:368`) marks are exact-line and do reject negated forms (my `v-entrymark-neg-exact-line`: `marks={'entry': False, ...}`); the gap is the substring+blocklist README leg only. The battery's F2a writes the entry mark un-negated, so it never exercises this leg against the entry mark and only exercises `remains unadmitted` (caught) on the README.

### F2 (medium-low) — K23 is byte-equality only; whitespace-normalized identical bodies bind as distinct

`bodies` hashes `'\n'.join(lines[2:])` verbatim (`:348`); `distinct` compares those digests (`:352`). The declaration says "byte-identical" and the code implements exactly that — but two counted seats can submit the same analysis with per-line trailing whitespace and count as independent binders:

Fixture `v-wsdup2`: paired reviewer/critic reports identical except three trailing spaces on every body line → observed `row_ok=True, bound_on_current=2, distinct_bodies=True`, verdict `PASS` (receipt `variant-results-2.json`). Contrast `v-byte-dup-contrast` (byte-identical) → `distinct_bodies=False`, FAIL. A whitespace/`' '.split()`-normalized comparison would close it; as frozen, K23 stops verbatim copy-paste but not lightly-padded duplication.

### F3 (low) — a vacuous empty `**Quote.**` verifies

Quote verification is normalized containment (`norm(want) not in norm(got[line_no - 1])`, `:278`); the empty string is contained in every line. Fixture `v-emptyquote-vacuous`: GR1's 12 real quotes replaced by one `**Quote.** \`S243\` sysfs.c:2040: ""` → observed `GR1_quotes={'quotes': 1, 'ok': 1, 'bad': []}`, `quotes_ok=3`, verdict `PASS` (receipt `variant-results.json`). A row carrying no informational quoting at all passes the quotes leg. Degenerate (requires the entry author to write it), but it is an honest-reading hole in the leg the predicate counts.

### F4 (low, diagnostic) — a citation failure is also reported as `distinct_bodies: False`

`bodies` only grows for seats whose citations resolve (`:344–348`), and `distinct` requires `len(bodies) == len(on_cur)` (`:352`). Fixture `v-nonpinned2`: one bound seat citing `btrfs-scrub-grounding-r45.md:16` → observed `citations_ok=False` with the true reason in `citation_problems=['R47RevGR1a: btrfs-scrub-grounding-r45.md not a pinned snapshot file']`, but simultaneously `distinct_bodies=False` (receipt `variant-results-2.json`). A reader of `distinct_bodies` alone misdiagnoses a K23 duplicate where the failure is K22. The true reason is in-band, so this is attribution noise, not a binding hole.

### F5 (low, observation) — a results entry's status is not checked

`bind` requires exactly one results entry by name+agent (`:197–201`) but never reads its `ok`/status field. Fixture `v-results-okfalse`: all results entries `"ok": false` → verdict `PASS` (receipt `variant-results.json`). The docstring promises only a spawn/results presence check, so this is in-scope-but-unstated; flagging so the L1 knows a seat whose task failed still counts as spawned if a conforming report exists.

## Verified-sound legs (fixtures score the holes the battery does not cover)

Every one of these binds as the docstring/declaration says; each carries an observed fixture result (receipts `variant-results*.json`, `extra-probes.txt`):

| Probe | Counter logic | Observed |
|---|---|---|
| Orphan report, no dispatch entry (`v-nospawn-no-dispatch`) | exactly-one dispatch across all waves `:181–194` | `dispatched 0 times`; row FAIL |
| Same seat twice in one dispatch (`v-duplicateseat`) | `:191` | `dispatched 2 times`; FAIL |
| Same seat in two waves (`v-wave2` accidental: real tracked `w1-dispatch.json` + added `v2-dispatch.json`) | `:181–194` | waves_seen `['v2','w1']`, seat binds in neither; FAIL — see notes |
| Dispatch with duplicate JSON keys (`v-dupkeys-dispatch`) | `no_dups`+`object_pairs_hook` `:99–105`,`:122–123` | one-line stdout, `dispatched 0 times`, `verdicts_ok=0`; in-band, no crash (F3) |
| Wrong agent role in dispatch (`v-agentmismatch`) | `:194–195` | `agent critic != reviewer`; FAIL |
| Verdict on stale pre-amendment bytes (`v-stalehash-old-bytes`) | hash must equal current section hash `:343–350` | stale seat binds (`detail` set) but `bound_on_current=1`; row FAIL — a verdict cannot bind to unread bytes |
| Single bound seat per row (`v-quorum1-single-seat`) | `len(on_cur) >= 2` `:350`,`:354` | `bound_on_current=1`; all rows FAIL — no quorum-by-one |
| Report cites a non-pinned file (`v-nonpinned2`) | `CITE_RE` `:83`, `verify_citation` `:241–247`, `report_citations_ok` `:288–292` | row FAIL; every `file:line` token in a report body must resolve to a pinned snapshot file |
| Body line contradicting the verdict (`v-contradict`, `extra-probes.txt`) | `ANY_VERDICT_RE` scan `:217–220` | `contradicting line ROW GR1 VERDICT: fails`; seat unbound |
| Digest-moved snapshot (`v-movedsnap-digest-break`) | snapshots cached only on digest match `:229–236` | `snapshot absent or digest moved` for both S243 sysfs.c quotes; `quotes_ok=1`; FAIL — a moved/edited snapshot cannot slip a pin |
| Quote naming a wrong pinned pair (`v-quotehop-wrong-file`) | cache keyed `(sid, file)`; quote keyed by its own sid/fname `:270–275` | `(S243, scrub.c)` → `snapshot absent or digest moved`; FAIL — no wrong-file verification |
| Inner `## ` header inside a row (`v-h2inner`; battery F1a/F1b) | `row_extent` `:134–146` | `structural_ok=0`, problem in-band; duplicated/absent next header also fails closed |
| Byte-identical bound reports (`v-byte-dup-contrast`; battery K23a) | `:348`,`:352` | `distinct_bodies=False`; FAIL |
| Negated entry gate line (`v-entrymark-neg-exact-line`) | exact-line entry mark `:367` | `marks.entry=False`, `marks_ok=2`; FAIL — battery F2a never tests the entry mark |
| Wave-name independence (`v-wave2b-name-independent`) | wave scan by suffix `:167–174` | single dispatch under another name → `waves_seen=['v2']`, verdict PASS; no hardcoded wave name |
| Exit codes | docstring `:35`; `main`/`run` `:302–311`,`:379–380` | observed rc 0 (PASS), 1 (FAIL) across variants; `--revision deadbeef` → rc 2, `{"error": "cannot resolve deadbeef"}` |

Report-path traversal: not possible as coded. The report path is `f'{WAVES}/{wave}/{seat}.md'` (`:202`) where `wave` comes from `ls-tree` child names of `.ufo/waves/round-47` (`:167–174`, no `/` possible in a tree entry name; `.`/`..` are not valid git path components) and `seat` is one of the eight fixed f-strings from `universe()` (`:60–66`). There is no seat-name regex to spoof: dispatch matching is exact equality `t.get('name') == seat` (`:184`), so near-miss names never bind.

## Notes for the L1 and counted seats (behavior, not counter defects)

1. **K22 strictness for counted seats**: any token matching `file.ext:digit` anywhere in a report body — including citations of the entry itself, `SCORECARD.md`, the counter, or `file:line` strings inside pasted command output — must resolve to a pinned snapshot file and line, or the seat fails and the row fails (`:83`,`:288–292`). Counted seats should cite only the ten pinned snapshot files.
2. **Stale-verdict asymmetry**: a bound `fails` on any section hash blocks the row (`any_fails`, `:351`), but a bound `partly` on stale bytes does not block (`:354–355` counts only `on_cur`); amendment-flow consequence, not a bug.
3. **Dual-dispatch unbindability**: a seat name appearing in two committed wave dispatches binds in neither (`dispatched 2 times`, `:191`). This is what makes re-dispatch safe against double-counting, but it also means a re-run wave must use fresh seat names (as the Res/Res2 sizing intends) — re-dispatching the same name is fatal for that seat.
4. **h3 headings inside a row do not trip F1**: `startswith('## ')` (`:144`) requires a space as the third character, so `### x` is allowed inside the counted extent. That is the letter of F1 ("any other `## ` line"), and row extent is header-equality based (`:135–142`), so a stray h3 neither re-bounds the row nor fails closed. Battery F1a probes only h2.
5. **Deep nesting**: battery F3a (200 000-deep JSON) passes as expected with a single-line in-band failure; my `v-dupkeys` adds a second malformed-JSON class with the same in-band behavior.

## Residual risk and verification gaps

- I scored variants at fixture base `f6bc6d05` (lane tip at review time); the counter is revision-parameterized, so results transfer to any `--revision`, but I did not re-score against a hypothetical future w2 amendment composition beyond the dual-dispatch probe.
- Quorum is 2 of 8 universe seats (`:354`); the remaining six may abstain silently. That is the declared sizing ("every committed round-47 wave's seats count"), not a hole, but a row can pass with only two bound seats — worth stating in the closure report.
- F2/F3/F4/F5 above are frozen-counter behaviors; fixing them requires an amendment round (re-freeze). None is exploitable without write access to `corpus/README.md` (F1) or collusion between two counted seats (F2).
- Not exercised: `--section-hash` failure paths (used read-only for hashes), non-UTF-8 report bytes (decode-guard at `:207–209` read analytically), >2 amendment rounds (Res2 generation sized but not probed).
- The census selftest and C2 items are out of this seat's scope and were not run (the one-time serialization rule was respected; all my counter runs are light git operations, one at a time).

## Proposed text

No amendment text drafted here (this seat reports findings; amendment wording belongs to the L1 if round 48 re-freezes). If the L1 wants one-line fixes for the record: F1 → extend the README leg to require the line to not also match `reversed|rescinded|vacated|withdrawn|error`; F2 → compare whitespace-normalized bodies; F3 → reject empty quote text; F4 → compute `distinct` over `on_cur` seats only when `citations_ok`; F5 → require `r.get('ok') is not False` on the results entry.
