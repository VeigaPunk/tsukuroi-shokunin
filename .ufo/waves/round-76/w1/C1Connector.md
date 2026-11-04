# C1Connector — scoped findings

Verdict: **named conflict — mori already holds journald retention rules; mado has an archived-file vacuum rule in historical safety evidence.**
Unchecked: ownership arbitration, source-truth judgment and admission; none is inferred.

Full report and exhaustive 1,199-line hit table: `.ufo/waves/round-76/w1/C1Connector/report.md`.

Swept 20 sibling committed trees (21 directories including excluded tsukuroi): mori 1,138 hits, mado 37, kama 11, kumitate 7, tabi 6; other 15 no matches; no command errors. Exact per-repo command: `git -C <absolute-repo> grep -nE 'journald|SystemMaxUse|journalctl --vacuum|vacuum-size|journald.conf|journal storage' HEAD -- .`. Full report carries all observed HEAD pins and bounded negative-claim limitations.

Decisive evidence: mori `corpus/knowledge/journal-reach-r49.md` at `84c6cbc3b47c536a504aaee329c77897d389935e`, lines 14,24-39 state size/default/storage/vacuum rules; line 63 expressly refuses journald configuration ownership. Mado `SafetyService.md:73-74` at `1459cca11fb5d3956a6e9a128217852dd0c28cb9` states archived-file removal. Thus knowledge overlap exists, but daemon-configuration authority is not automatically contested. The frozen narrower phrase “this lane never held” is not disproved by sibling overlap.

Tsukuroi `PROVINCE.md:6-14` Core explicitly includes systemd and “journal/boot triage”; retention is not explicitly named. Placement within this broad Core is an inference, not an explicit frontier grant.

One proposal: prepare a pinned mori/integrator boundary packet distinguishing retention-as-evidence-reach from daemon-configuration diagnosis. Preserve every frozen JD row and predicate; cross-reference shared rules rather than silently deleting them or assigning authority. Axes: adjacency, C1 depth, siblings; C2 unchanged. Handoff remains proposed, not filed or accepted.

Risks: knowledge is not ownership; historical config is not current effective limit; row counts are not source-truth/novelty proofs. Main should compare frozen JD rows with pinned mori rules and obtain recipient/integrator acknowledgement before calling the boundary resolved. No tests/checkers/builds run, no installations, no scratch created, no sibling changes.
