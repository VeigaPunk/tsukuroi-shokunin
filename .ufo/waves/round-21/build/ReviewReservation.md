# ReviewReservation — predicate `reservation-before-dispatch` on pinned QUALITY.md

Axes: correctness of the ordering rule as specified; observability of grant-before-dispatch
evidence; append-only disclosure of the historical retroactive reservation; no fleet mutation.

## Reviewed bytes and binding

Reviewed-SHA256: aabd157d7651c1cca96560f5cf00ee8c665acb2be22a6b5d76239926ccbc67be
Predicate: reservation-before-dispatch

`preregister.json:58-60` declares SHA `aabd157d…` for the pinned primary bytes at
`.ufo/waves/round-21/snapshot/corpus/QUALITY.md`. Those bytes end at criterion 41 (R20-C2-ORACLE);
the live `corpus/QUALITY.md` is byte-identical through line 85 and appends criteria 42–44, where
criterion 42 (R21-REVIEW-BYTES / R21-RETRO-RESERVATION) is the only text governing this predicate.
Under NO-EXEC the digest is the preregistered declaration, not a recomputation by this seat.

## Observations

1. Reviewed-bytes scope. The reviewed text (criteria 1–41) contains no fleet-reservation rule.
   Criterion 31 is adjacent in form only — "Authorization added after delivery … does not clear the
   seat; the deviation stays recorded" (QUALITY.md:47-49) — but it binds seat execution class, not
   headroom grants. So the predicate has no operative clause inside the pinned bytes; the operative
   spec is appended criterion 42, outside the reviewed SHA. This is a binding observation, not a
   defect in the reviewed text: reviews bound to different byte sets cannot clear each other
   (criterion 38 pattern).

2. Grant-before-dispatch evidence, this round (`.ufo/waves/round-21/build/`). Five attempts, each
   with a grant artifact committed alongside its dispatch attempt:
   - `reservation.json` acquired 12:36:06.941Z, `dispatch_started: false`, bound by `refusal-01.json`
     (`"reservation":"reservation.json"`, `"payload":"dispatch.json"`, spawned 0 at job cap 100).
   - `reservation-02.json` 12:38:00.644Z (refusal-02), `reservation-03.json` 12:42:00.204Z
     (refusal-03), `reservation-04.json` 12:46:43.691Z with `routing_notice` (refusal-04);
     each carries `preregister_commit: c05af5c07a63…`.
   - `reservation-05.json` acquired 12:48:42.989Z; `spawn.json` `started_at` 12:48:50.577Z —
     grant precedes the successful dispatch by ≈7.6 s.
   Per-attempt acquisition satisfies criterion 42's "before each dispatch attempt"; refused calls
   spawned zero seats and retried the unchanged 64-seat payload per `refusal-01.json` policy and the
   `dispatch.json:746` note.

3. Grant content is more than a bare timestamp: each grant records fleet counters
   (`seats=64 live=… pending=… cap=240`), distinguishing an observed fleet state from a declared
   receipt — the criterion-42 distinction between a receipt-as-declaration and acquisition evidence.

4. Append-only disclosure of the historical defect. Round-20's retroactive acquisition is preserved
   as defect, never re-dated: `corpus/lessons/round-21.md:34` (R21-RETRO-RESERVATION, "none for event
   chronology … No timestamp-only artifact can backdate the old grant"), gate row `:14` ("A
   retroactive reservation proves pre-dispatch headroom — reject"), and `README.md:194` (retroactive
   build reservation stays a "historical process defect, not newly cleared"). Consistent with
   criteria 4/5 (append-only errata, kept rejections) and criterion 31's recorded-deviation pattern.

5. No fleet mutation. Ordering evidence consists of lane-local committed artifacts
   (`reservation*.json`, `refusal-*.json`, `dispatch.json`, `spawn.json`) plus the fleet's own grant
   text — reads of allocator state, not fleet rewrites; the seat contract's no-fleet-mutation bound
   is unviolated by the evidence form itself [inference: fleet-side write path not observable to a
   NO-EXEC leaf].

## Findings

F1 (low — evidence completeness, not ordering violation). `reservation-05.json` drops the
`dispatch_started` field present in `reservation.json` and carries no `attempt` number or payload
binding; grants 02–05 likewise lack `attempt`. Grant→attempt linkage currently rests on filename
convention plus refusal-side binding: all four refusals (`refusal-01…04.json`) bind `attempt`,
`payload`, `reservation` filename and `spawned:0` — the successful attempt, the one whose ordering
matters most, has no refusal and therefore the weakest in-file binding. Specification gap: the
grant artifact for attempt N should record `attempt`, the dispatch payload identity (e.g.,
`dispatch.json` SHA-256), and a post-grant `dispatch_started` assertion symmetric to
`reservation.json`.

F2 (low — spec completeness). Criterion 42 carries no explicit `Falsified by:` clause, unlike
criteria 31–33. A named finite control is needed for the ordering claim to be more than prose:
a checker that must reject (a) a grant whose `acquired_at` post-dates its attempt's
`spawn.started_at`, and (b) a grant missing the attempt/payload binding, before the wave's
reservation ordering counts as green. Without it, "commit current grant before dispatch output"
(lesson:34) is unenforced.

F3 (note — append-only disclosure spec). The criterion forbids backdating but does not name the
disclosure form. Specification: a retroactive acquisition is disclosed only as a named, dated
erratum record identifying the covered dispatch and both event times (grant, dispatch), retained as
red — satisfying criteria 4/5 — and never merged into or re-dated within the original dispatch
record. This round's handling (lesson Mistakes row + gate reject row + README defect sentence) is a
conforming instance.

## Residual risk and limits

- Ordering between grant and dispatch within the successful attempt rests on two timestamps
  (`reservation-05.acquired_at` vs `spawn.started_at`) generated by the same orchestrator host;
  commit chronology (`preregister_commit` embedded in grants 02–05) is the stronger anchor but is
  not embedded in `reservation.json`/`reservation-05.json` [limitation].
- SHA-256 bindings are preregistered declarations; this seat recomputed nothing (NO-EXEC).
- Refusal-02 also records a refused `sleep 180` scheduling command — an honest refusal artifact;
  the retry sleep itself is dispatch-adjacent, outside pure grant ordering [note].
- The round-20 LOG line cited by QUALITY:87 and lesson:34 was not re-read; the disclosure chain was
  verified through lesson, gate row and README only.

Scope: executed=none
