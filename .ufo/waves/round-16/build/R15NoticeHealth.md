# R15 notice fields — host-health-report-r3.md

[obs] Baseline db68e62: `## R15-UPDATE-STATE (2026-10-20) — current-use supersession` (578) through EOF 599; 38589 bytes, final newline; no R16 heading exists.

Fields whose meanings must remain unchanged:

1. 580-581 history clause: 2026-10-14 bytes preserved/historical; old `§1 verdict-board row 5` (581) stays baseline-detectable.
2. 581-584 supersession scope: only board row 5 and §2.5 arm composition are capture-only/non-current; R16 retargets the citation to `## 0. Verdict board`, not the claim.
3. 586-588 current-use authority: `partial-upgrade-recheck-r15.md`/`.json`, schema `tsukuroi-partial-upgrade-recheck-v1`.
4. 588-590 snapshot binding: `host-snapshot.json`, captured 2026-10-20T07:44:39Z, SHA256 `b101f3747827cefd0ed604c14b669267ec0fcc1b6c2fbe6e486be0cdbbc6ea81`.
5. 591-594 observations: `pacman -Qu` exit 0, 413 rows, sync DB 2026-10-18T17:11:00Z, libinput 1.32.0-1, mkinitcpio 41.1-1/42.2-1 pending, decision `BLOCKED_FOR_AGENT_PACKAGE_ACTION`.
6. 596-599 authorization: no agent package/service action; operator-only assessment; news gate; `/new_root` hooks untested; no repair claimed.

Anchors: heading (23) unique; row_key `| 5 | update-safety |` and quote "`-Syu` now `INERT`" only line 31 (notice text spans 581-582). `§1` also 262/425; §2.5 correct (299). Keys 572-575; entry MD, not this notice, opens source:/verified-at:/recheck:.

Limits: static bytes; digest not recomputed; no host probes; append-only correction not yet implemented.
