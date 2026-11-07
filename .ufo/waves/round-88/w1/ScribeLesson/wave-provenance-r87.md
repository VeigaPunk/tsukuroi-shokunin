## Wave provenance — round 87 w1 (`R87-WAVE-OUTPUT-NOT-DURABLE`, routed 4)

`.ufo/waves/round-87/w1-results.json:5` records `"seats": 12`; all twelve result entries carry `"output": null`
(first at `:8-12`), each with the same note: "orchestrator kernel restarted mid-wave; seat output was delivered to
the orchestrator session but not retained — read the seat report file in the wave dir" (`:11`). A count over the
file reads `seats 12 results 12 null_outputs 12` with one distinct note string (`python3`, this seat).

The wave's seat finals were therefore not written by the wave file. `.ufo/waves/round-87/w1/finals/` holds 13 files
— the 12 seat names in `w1-results.json` (some with numeric suffixes, e.g. `ExecLints-3.md`) plus `TsukuroiR87.md` —
all mtime 2026-11-06 20:23:39, and per the non-author spot-check they were recovered from the orchestrator's session
store after the restart (`corpus/lessons/round-87-verifier-spotcheck.md:139-141`).

Seat-written primary receipts exist for part of the wave. `ls .ufo/waves/round-87/w1/` lists seat dirs
`ConnectorOverlap CriticClaims ExecLints ExecReplicate MutBattery MutGate ReviewEntry ReviewGate ScribeLesson` and
top-level seat reports `ExecLints.md ExecReplicate.md MutBattery.md MutGate.md ReviewEntry.md ReviewGate.md
ScribeLesson.md`. Three seats — `CriticLimine`, `ScoutSources`, `ScoutRepair` — have neither a dir nor a top-level
report, so for those the only surviving output is the session-store `finals/` file. Their finals are quotable but
are not seat receipts.

Round-88 correction: every seat writes receipts to disk as it goes (`.ufo/waves/round-88/w1-spec.json:10`, context:
"Write your receipts to disk there as you go (round-87 lesson: seat output lost on a kernel restart)"), and this
round's wave evidence lives at `.ufo/waves/round-88/w1/<seat>/` plus `.ufo/waves/round-88/w1/<seat>.md`. The
round-88 lesson should cite seat receipt paths, and never a session store; where a seat's receipt is missing, the
lesson should say so instead of quoting a final as if the seat had written it.
