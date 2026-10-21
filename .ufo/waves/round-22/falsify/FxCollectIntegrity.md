# FxCollectIntegrity — C3 transcript-digest/sourcecount falsification (round 22)

Target: `.ufo/waves/round-22/candidate/.ufo/waves/round-22/collect.py` (134 lines), declared digest
`3d720f6aa18b3b9f5e4ec0f5b3c82cb7d7becddf1d2b6a40bbccd3ca31a7a47a`.
Method: source-only reading of the bound paths. No import, execution, fixture run, hash recomputation,
subprocess or network access (NO-EXEC / NO-FETCH). The declared digest is accepted as given; it was
**not** recomputed here, so this report binds to the declared identity, not to a locally re-hashed byte string.
Lane bounds: leaf member — no subagent dispatch.

## 0. Claim under test, split

- **A (positive):** a transcript digest plus a "sourcecount" is *sufficient* evidence for the available-trace scope.
- **B (negative):** the same pair is *not* a provenance theorem.

Definitional gap [OBSERVED-SOURCE]: the token `sourcecount` appears in none of the bound files
(`collect.py`, `preregister.json`, `host-tool-boundary.json`, `seat-boundary-r22.json`,
`seat-boundary-r22.md`, `check-review-snapshots.py`). The only count-bearing outputs inside the bound
bytes are:

1. `collect.py`: printed `seats` / `complete` / `requests` and the per-seat `events` list (lines 114-116, 124-126);
2. `check-review-snapshots.py`: `distinct_source_files` / `pinned_reviews` / `total_reviews` (lines 125-128).

Both referents are attacked below. A claim using an undefined "sourcecount" cannot be reproduced literally.

## 1. Verdict

| Half | Verdict | Basis |
|---|---|---|
| B — not a provenance theorem | **HOLDS, understated** | F6: digest has no external root, no expected value, and lives in the same writable artifact it protects |
| A — sufficient for available-trace scope | **FALSIFIED as a sufficiency claim** | F1 crashes before any artifact; F2 silent undercount with `complete: true`; F3 parallel children lost/uncounted; F5 denominator is registry members only |
| sourcecount = `distinct_source_files` | **FALSIFIED as a verified-source count** | S1 counts manifest declarations before verification; S2 field omitted on CANNOT_EVALUATE; S3 no fixture pins it |
| sourcecount = collect `requests` | **FALSIFIED as a request count** | F3: wrapper counts 1, children never counted; F2: unmodeled content dropped; duplicate ids dropped with only a boolean |

Claim A survives only under the five unstated preconditions P1-P5 in §4. Nothing here widens the
round-22 host decision: no native preventive enforcement is claimed or implied.

## 2. Observed source anchors

| Anchor | Bytes | Fact |
|---|---|---|
| collect.py:20-33 | `projection()` | parallel branch tests raw name `tool in ('multi_tool_use.parallel', 'parallel')`; leaf branch strips `functions.` |
| collect.py:38-39 | `registry = json.loads(...)`; `index = {p.stem: p for p in transcripts.glob('*.jsonl')}` | seat universe is registry members; transcript mapping is filename stem, non-recursive |
| collect.py:50-52 | `raw = trace.read_bytes()` … `sha256(raw)`; `trace_bytes = len(raw)` | digest = SHA-256 of exactly the caller-selected bytes |
| collect.py:57-62 | `json.loads(line)` in `try: except (ValueError, UnicodeError)` | only parse errors are contained |
| collect.py:63-69 | `obj.get(...)`, `message.get('content', [])` | no `isinstance(obj, dict)` / `isinstance(message, dict)` / list guard |
| collect.py:73-77 | duplicate/missing `id` -> `parsed = False`; keep first | duplicate call silently dropped, only a boolean records it |
| collect.py:106-107 | `complete = parsed and (exit_seen or final or terminal_error)` | completeness = parseability + terminal metadata |
| collect.py:113-116 | `json.dumps(args, sort_keys=True, ensure_ascii=False, default=str).encode()` then `sha256` | argument digest; `encode()` is outside any `try` |
| collect.py:122-123 | `write_text(events.json)`, `write_text(settlement.json)` | writes happen only after the whole seat loop |
| collect.py:130-134 | `add_argument('transcripts', type=Path)` | transcripts root is an unvalidated caller path |
| check-review-snapshots.py:81 | `distinct = len({row["source"] for row in reviews})` | count taken from the manifest, before any read |
| check-review-snapshots.py:85-120 | read / hash / report-line checks | verification happens after the count, and failures do not decrement it |
| check-review-snapshots.py:125-128 | payload | `distinct_source_files` printed next to `pinned_reviews` |
| check-review-snapshots.py:234-235 | fixture assertion | only `total_reviews` / `pinned_reviews` are pinned |
| check-review-snapshots.py:258-272 | CANNOT_EVALUATE payloads | `distinct_source_files` key absent |
| `_revision.py:172-192` | `bind()` landed/pushed ancestry checks | review bytes are read from a landed commit; transcripts are not commit-bound at all |

## 3. Counterexamples

### F1 — one malformed line destroys the wave artifact before any digest is available [OBSERVED-SOURCE, high confidence]

`collect.py:59` contains `json.loads` errors only. Lines 63, 65, 78 call `obj.get(...)` with no dict
guard, so a record line that is valid JSON but not an object (`null`, `[]`, `3`, `"x"`) raises
`AttributeError`; `message` being a scalar raises the same at 66-67; `content: null` raises `TypeError`
at 69 because `message.get('content', [])` returns `None` and line 69 iterates it. A lone surrogate in
arguments survives parsing and raises `UnicodeEncodeError` at 113, also outside any `try`.

Because both writes sit after the entire seat loop (122-123), one such line aborts the process with no
`events.json` and no `settlement.json` for **every** seat, not only the malformed one. The failure mode
is a traceback, not the structured could-not-evaluate that the seat-boundary markdown requires
("Mark incomplete trace coverage could-not-evaluate, not zero activity"). Consumers either fail on a
missing file or, worse, read a previous run's unreplaced file as current.

### F2 — unmodeled content shape yields `complete: true` with zero counted requests [OBSERVED-SOURCE, high confidence in behaviour; recorder-shape likelihood unknown]

If `message['content']` is a non-null non-list (a single unwrapped object, or a string), line 69
iterates keys/characters, line 70 rejects each, and `parsed` is never touched. An unwrapped tool-call
object is therefore invisible: `events` stays empty, `final_text` (91) is truthy because no dict
element is seen, a `stopReason` of `stop` makes `final` true (93), and the settlement row reads
`completed` with `complete: true` and zero requests. No finding, no coverage marker.

### F3 — parallel wrapper: children never counted; prefixed wrapper loses even the child projections [OBSERVED-SOURCE, high confidence]

`order` is fed only by top-level call ids (76-77, 85-87); children of `tool_uses` are never added.
`'requests': sum(len(r['events']))` (125) therefore counts *dispatches*: a wrapper with N read/grep
children counts 1. In addition, line 23 tests the raw name while line 31 strips `functions.` only for
leaves, so a recorded `functions.multi_tool_use.parallel` falls through both branches and projects to
`{}` at 33, silently discarding every child path. A recorded `functions.read` keeps its path. The
asymmetry is internal to the file; line 31 is itself evidence that prefixed names are expected.

### F4 — seat attribution is filename identity only [OBSERVED-SOURCE, high confidence]

`index` (39) maps `agentId` to `p.stem`; nothing checks the trace's own session/agent identity, and the
glob is non-recursive. A renamed file, a shared transcript root across waves, or a trace stored one
directory down is respectively accepted as that seat, aliased across waves, or reported
"registered transcript unavailable" (47). The digest then faithfully attests whatever bytes the name
resolved to, so digest integrity and seat attribution are independent, and only the first is provided.

### F5 — denominator is registry members, not the declared population [OBSERVED-SOURCE, high confidence]

The loop is `for name, member in registry['members'].items()` (41). The C3 bound in `preregister.json`
requires accounting for "every declared seat". A seat declared but never written into
`swarm-registry.json` produces no row at all, and the printed `seats` count shrinks silently; there is no
cross-check against any declared list. Settlement also has three outcome values (98/100/102) while the
seat-boundary markdown requires four classes, and absent-dead versus absent-unresolved are the same
`'unknown'` row with identical fields (45, 49). The distinction must be supplied by an input outside
this artifact, or the four-way partition is underdetermined.

### F6 — the digest is a content checksum, not provenance [OBSERVED-SOURCE, high confidence]

The digest is over bytes read from an arbitrary caller path (`--transcripts`, 132); there is no expected
digest parameter, no signature, no monotonic recorder, and no path field in the output to re-locate the
hashed file. The digest is written into the same writable wave directory (122-123) that the transcript
tree sits beside, so an actor able to rewrite a transcript can rewrite its digest in the same pass;
nothing external binds the pair. Structurally, the artifact cannot rise above available-trace scope.

### S1 — `distinct_source_files` counts declarations, not verified sources [OBSERVED-SOURCE, high confidence]

`distinct` is computed at 81, before any read. A manifest with three distinct sources whose bytes all
mismatch produces `status: FAIL`, `pinned_reviews: 0`, and still `distinct_source_files: 3`. The same
holds for read failures and missing reports. Read as "sources verified", the field overstates; the
payload's `scope` string disclaims reading proof, but not that this number is verified.

### S2 — the count field is absent exactly when evaluation is inconclusive [OBSERVED-SOURCE, high confidence]

`evaluate` always returns the key (125-128), but `main`'s manifest-path, revision and read failures emit
payloads without it (258-260, 268-272). A consumer indexing the field fails on the inconclusive paths;
a consumer treating absence as zero cannot distinguish "no sources" from "could not evaluate". Two
different CANNOT_EVALUATE shapes exist in one tool.

### S3 — no fixture pins the source count [OBSERVED-SOURCE, high confidence]

The only count assertion in `selftest` is `total_reviews` / `pinned_reviews` for
`read-failed-retains-missing` (234-235). No case asserts `distinct_source_files`, and no case exercises
duplicate sources sharing one path. The seat-boundary markdown's own QUALITY line requires fixed
negative fixtures before an improvement counts, so the source-count metric is unpinned by the artifact
that would justify it.

### S4 — asymmetric anchors when the two halves are combined [OBSERVED-SOURCE, high confidence]

`check-review-snapshots.py` reads manifest, sources and reports from a landed revision
(`_revision.bind`, `git_read`), which is a genuine external pin for those bytes. `collect.py` reads
transcripts from an unbound directory. A combined "digest + sourcecount" claim therefore inherits the
weaker half for every seat-attribution question, and even the commit-pinned half has no chronology
binding (report and source are read from the same commit; `_revision` checks landing, not sequence).
Neither half observes reading, command bodies, or effects.

## 4. Bounded reason claim A holds

Claim A is defensible only when all of the following are true, and none is asserted by the code:

- P1: every seat of the declared population is present in `registry['members']` (F5);
- P2: every trace is `<agentId>.jsonl` directly under the caller root (F4);
- P3: every line is a JSON object; every `message` is an object; every `content` is a list (F1, F2);
- P4: argument values encode under UTF-8 without lone surrogates (F1);
- P5: tool names are consistently prefixed or unprefixed, and callers treat `requests` as dispatch
      count, not leaf-request or operation count (F3).

Under P1-P5, `events` derives solely from the hashed bytes, `complete` is exactly
`parsed and (exit_seen or final or terminal_error)`, `trace_bytes` binds length, and the coverage strings
(107, 119, 121) correctly limit the result to recorded requests and observed terminal metadata.
That is the entire defensible content of claim A. Claim B needs no precondition: no input or output in
`collect.py` can express an external commitment.

## 5. Expected fixture verdict vs observed runtime

No fixture bytes for `collect.py` exist in this seat's bound read paths, and the `check-review-snapshots`
fixtures do not cover the source count, so the expected column is derived from source only. Nothing was run.

| Hypothetical fixture | Expected verdict from source reading | Observed runtime |
|---|---|---|
| trace containing a `null` line | abort before 122-123; no events.json/settlement.json; traceback, no finding | none |
| assistant `content` as one unwrapped toolCall object; `stopReason: stop` | `complete: true`, `requests: 0`, outcome `completed` | none |
| `multi_tool_use.parallel` with 3 children | 1 event; children projected but not counted | none |
| `functions.multi_tool_use.parallel` with 3 children | 1 event with `args: {}`; no child paths, no flag | none |
| registry missing one declared seat | no row; `seats` equals registry size only | none |
| 2 reviews / 1 source / tampered source bytes | `FAIL`, `pinned_reviews: 0`, `distinct_source_files: 1` | none |
| invalid `--manifest` path | CANNOT_EVALUATE payload without `distinct_source_files` | none |
| any re-hash of the target to confirm the declared digest | would require execution | none |

## 6. Consequence for C2/C3, without overreach

- C3 (cohort accounting) consumes `settlement.json`: it can report completed/failed/unknown, but the
  four-way partition in the preregister needs a discriminator this artifact does not carry (F5).
  Registry-membership also replaces the declared denominator silently, so accounting is conditional on
  an input the collector never validates.
- C2 (request audit) consumes `events.json`: F1 can remove it entirely, F2/F3 can understate the request
  surface with no marker, and F4 makes seat attribution filename-based. The audit remains post-hoc
  detection and evidence; nothing in this analysis supports calling it enforcement.
- The candidate's prose is calibrated: coverage strings at 107/119/121 and 128 already disclaim effects,
  reading, chronology and universal completeness. The defect is in field semantics (`complete`,
  `requests`, `distinct_source_files`) and in failure containment, not in the stated caveats.
- Duplicate-id calls are dropped from the count (73-75) with only `complete: false` (106) and no drop
  magnitude; never-started calls are retained with `start_line: null` (114-116), which is correct for
  auditing proposed requests but means the count is neither operations nor executed requests.

## 7. Remaining unknowns

- `tools/check-seat-bindings.py` and `tools/check-review-cohort.py` (declared in `preregister.json` but
  not bound to this seat) — whether they expand parallel children, treat `complete` as coverage, or
  recover dead/unresolved from the review manifest.
- The producer of `swarm-registry.json` and whether registry membership equals the declared population.
- The actual recorder's transcript shape: `content` always a list, flat directory, and name prefixing.
  F1/F2/F3 severity depends on these.
- Provider semantics for `stopReason`/`errorMessage` (line 90 gating): an error with `stopReason: stop`
  plus text is classified `completed`.
- Whether the candidate bytes hash to the declared digest: not checkable under NO-EXEC.

## Receipt

Reviewed-SHA256: 3d720f6aa18b3b9f5e4ec0f5b3c82cb7d7becddf1d2b6a40bbccd3ca31a7a47a
Predicate: r22-fxcollectintegrity
Scope: executed=none
