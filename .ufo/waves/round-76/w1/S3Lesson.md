# S3Lesson — scoped report

Verdict: assigned draft complete; integration and judgment unclaimed. Axes: freshness/C2 and lesson auditability; no ordinal changes claimed.

## Behavior and touched surfaces

Wrote the full draft at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-76/w1/S3Lesson/round-76.md`, with Gate, Search log, Mistakes, all C2 repair-token blocks, round-76 correction propagation map, and explicitly requested L1 attack/owed placeholders. The draft is not `corpus/lessons/round-76.md`; no corpus/product file was edited.

Binding written before deep work: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-76/w1/S3Lesson/binding.md`. Copied original receipts into that same seat directory: `host.txt`, `recheck-r75-at-tip.txt`, `census-start.txt`. Source provenance remains the frozen `before/src/SOURCES.json`, `SHA256SUMS` and declaration `SCORECARD.md:6244-6318` at the specified declaration commit. Working-tree carrier positions are explicitly distinguished from final revision bindings.

## Gates and evidence

No instrument, selftest, verifier, census, source digest check or host probe was rerun. No additional runtime, delegation, install, privilege, git mutation, commit or publication occurred. Read `godspeed` and `agent-self-evaluation` skills. Reproduction commands in the draft are marked not run/expected; they are not execution evidence.

Observed from existing receipts only:
- `before/recheck-r75-at-tip.txt:5-11`: producer labels `count-jt-rows-r75.py --revision bd0acc44` and `check-r74-routed-r75.py --revision bd0acc44`; outputs respectively `JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1` and `ROUTED_STALE=0 ROUTED_OK=4/4`, each `rc=0`.
- `before/host.txt:7-68`: `systemd-analyze cat-config systemd/journald.conf` includes size.conf with SystemMaxUse=256M/RuntimeMaxUse=64M; `journalctl --disk-usage` reads 148.6M. Both commands have rc=0 in the original receipt.
- `before/census-start.txt:47`: `tsukuroi ok`; assignment supplies round-start exit 0. The receipt does not itself record the producer command or exit header. No exact command has been invented.
- Gate quotes were located by source reads: journald.conf.xml:87, journald-config.c:26, journald-manager.c:170, journalctl.xml:944. Each is shorter than 25 words.
- `corpus/lessons/round-75.md:55-80` lists the five mistake rows; :135-143 carries the two owed rows. The draft gives a section-aware reproduction command without running it.
- E5MarkerAudit's `markers.txt:2-8` records seven regular carried files absent at base; this does not establish final committed tracking.

## Findings and verbatim conflict

The requested R76-JD-CONFIG-DRIFT row distinguishes write-time sweep from absent recheck cadence and routes the fix to QUALITY 109 plus the three appended carrier errata.

Additional located discrepancy, recorded as R76-JD-CLAMP-WORDING without adjudication:

Declaration: “used space plus the smaller of free space and `keep_free`”.

Pinned `journald-manager.c:168`: `avail = LESS_BY(vfs_avail, metrics->keep_free);`

Pinned `journald-manager.c:170`: `space->limit = CLAMP(vfs_used + avail, metrics->min_use, metrics->max_use);`

No frozen claim, route, instrument or judgment was changed. L1/source reviewers/canonical judge must dispose of this discrepancy explicitly; the draft does not imply that a token pass resolves it.

The propagation map includes journal-boot-plane, degraded-triage-r4, boot-plane, README and the additional historical oom-event-plane carrier. A targeted case-insensitive SKILL search returned no matching retention/defaults-only claim, so no fictitious SKILL location was supplied. This was bounded search, not exhaustive semantic proof.

Known provenance limit: size.conf birth time appears in the assignment/declaration and appended carrier errata, but `before/host.txt` has no birth-stat command. The draft attributes it accordingly.

## Exact shell commands exercised

All returned successfully with no output:

1. `mkdir -p /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-76/w1/S3Lesson`
2. `mkdir -p "${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tsukuroi-r76/S3Lesson"`
3. `cp /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-76/before/host.txt /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-76/before/recheck-r75-at-tip.txt /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-76/before/census-start.txt /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-76/w1/S3Lesson/`
4. `rm -r -- "${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tsukuroi-r76/S3Lesson"`

Scratch was created empty and removed; no temporary-producing driver was invoked, so there was no TMPDIR-bearing runtime command. Remaining reads/searches/writes are tool calls recorded in the seat transcript; they do not imply shell execution. No tool install/update occurred.

## Out of scope and integration gate

L1 copies the draft to the corpus, incorporates final attack-seat reports, supplies committed marker/census/claim receipts, and runs the frozen checker against the integrated revision. This seat intentionally did not run verification or infer committed closure from concurrent working-tree edits. The requested attack/owed placeholders are integration fields, not a hidden assertion that those reports were read.

## Self-evaluation (not an external gate)

Accuracy 4/5: located quotations and attributed receipts; final committed state and birth-stat provenance remain outside observed evidence. Completeness 4/5: all requested draft sections present; final attack/owed integration is explicitly assigned to L1. Clarity 4/5: evidence versus expected commands is explicit; the draft is necessarily lengthy. Actionability 4/5: ready draft and reproduction commands supplied; canonical conflict disposition remains external. Conciseness 4/5: repeated path/receipt detail preserves auditability but could be shortened after integration. Mean 4.0. Highest-impact improvements: integrate final attack evidence; attach final revision/producer receipts; preserve explicit adjudication of the clamp conflict. Expected user agreement: appropriate for a draft-only scribe seat, not an admission report.
