# CriticFreeze — round 78

Axes: depth (lowest tied 8), operability (9). No admission or outside verdict.

Full review: `.ufo/waves/round-78/w1/CriticFreeze/report.md`.
Exact-byte evidence and argv: `.ufo/waves/round-78/w1/CriticFreeze/attack-receipt.json`.
Reproducer: `.ufo/waves/round-78/w1/CriticFreeze/attack.py`.

## Counterexamples and classification

Three isolated C1 attacks each returned rc 0, `count=6 met=1 reason=finite-content-and-review`:
1. Fully fabricated ReviewUsage verdict plus fabricated unique reviewer-role orchestrator result. This is the **explicitly acknowledged complete-bundle authenticity limitation**, not a newly invented kill or guarantee.
2. That same bundle with a companion claiming symlinks are followed, apparent size is counted, directories count, and failed stats contribute size. Numeric success does not excuse this: such prose in the actual submission **would fire the frozen false-companion kill rule**.
3. A digest-bound verdict explaining falsely that AT_SYMLINK_NOFOLLOW follows symlinks and st_blocks is apparent byte length, with result output saying `I did not review this source.` The gate accepts matching bytes/identity fields, not narrative truth or reviewer authorship.

C2's frozen `_coverage` subfunction accepted a row advertising `python3 tools/measure-journal-usage-r78.py --invented-mode` with verdict digits 0/1/2: `findings=[]`. This is not a whole-checker success claim. A submitted false command still fires the frozen C2 kill rule. Existing-tool retention likewise requires independent base comparison; ordinary enumeration sees the candidate's tools, not an immutable baseline.

**Smallest safe correction:** do not amend counters, cases, target, pins or rules. Check actual companion/reviewer explanations against source, carry actual review bytes in the genuine orchestrator result, and inspect advertised registry commands/verdict maps and tool retention separately from numeric success.

## Source and baseline evidence

Reopened pinned manager :91–135 and journalctl documentation :941–978; checked S327/S328 literals. Both counters, expected.json and both source snapshots matched their frozen-commit and manifest SHA256 values. Independent source-predicate calculation gives U1–U6 **4096, 8192, 0, 0, 0, 0** (sum 12288). No upstream-source contradiction found. ScribeNote's available actual draft preserves the important source boundaries; no false explanation was found there. Final integrated review binding was not claimed.

Pre-seat controls already show do-nothing C1 **0/6, rc 1** and C2 **10 findings, rc 1**, so neither target can be met by inaction. C1 addresses depth, a tied-lowest axis; C2 alone cannot satisfy it. The two numeric claims read separate artifact families. No ordinal uplift or domain saturation inferred from these finite cases.

No production/results writes, git mutations, host changes, installs, clones, privileged probes or other judgment runtime. Private scratch removed; exact generated attack bytes and receipts retained in the seat directory. No final integrated candidate verification or outside verdict performed.
