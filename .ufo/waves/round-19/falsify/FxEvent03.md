## Attack

Tested C2's EV-08 through EV-10 assignments. They are falsifiable by comparing each registry citation to its pinned capture line, checking that the line contains the stated timestamp, cleanup unit and `Updated: /boot/limine.conf`, resolving its writer and signature to the registry's writer class, and checking for repeated event-ID citations and disagreement with the markdown event count.

## Method

- Read committed sources and captures at revision `8e5916360f2dfe7bc4eb4ba144081af555900116` using read-only `git show`; independently parsed the pinned JSON, capture lines, and markdown table to compare event fields and duplicate `(capture, line)` references.
- Checked the three capture digests with `sha256sum`; all matched the digest recorded in the registry. Checked the capture files and registry/entry had no diff from the pinned revision.
- Ran the named gate: `python3 tools/check-boot-writers.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116`.

## Verdict

CONFIRM — C2, for the assigned EV-08 through EV-10 batch.

- EV-08: CONFIRM.
- EV-09: CONFIRM.
- EV-10: CONFIRM.

## Evidence

- The registry assigns EV-08 to `host-capture-r19c.txt:15`, with timestamp `2026-10-20T12:07:07`, unit `snapper-cleanup.service`, and writer `W-SNAPPER-CLEANUP` (`8e5916360f2dfe7bc4eb4ba144081af555900116:corpus/knowledge/boot-writers-r19.json:319-324`). The pinned capture line contains the timestamp, PID `4066545`, cleanup unit/cgroup, and `Updated: /boot/limine.conf` (`8e5916360f2dfe7bc4eb4ba144081af555900116:.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:15`).
- EV-09 cites `host-capture-r19c.txt:16`, timestamp `2026-10-20T13:07:10`, unit `snapper-cleanup.service`, writer `W-SNAPPER-CLEANUP` (`…:corpus/knowledge/boot-writers-r19.json:326-331`). That pinned line contains the timestamp, PID `1947334`, unit/cgroup, and the `Updated:` message (`…:.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:16`).
- EV-10 cites `host-capture-r19c.txt:17`, timestamp `2026-10-20T14:07:12`, unit `snapper-cleanup.service`, writer `W-SNAPPER-CLEANUP` (`…:corpus/knowledge/boot-writers-r19.json:333-338`). That pinned line contains the timestamp, PID `1670514`, unit/cgroup, and the `Updated:` message (`…:.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:17`).
- The writer class exists with `journal-unit` signature ` snapper-cleanup.service /system.slice/snapper-cleanup.service ` (`8e5916360f2dfe7bc4eb4ba144081af555900116:corpus/knowledge/boot-writers-r19.json:30-76, signature at lines 62-65). Its captured mechanism is the cleanup-service drop-in's `ExecStopPost=limine-snapper-sync`; the timer has `OnUnitActiveSec=1h` (`8e5916360f2dfe7bc4eb4ba144081af555900116:.ufo/waves/round-19/l1-capture/host-capture-r19.txt:227-228,256-260`).
- No event IDs share a `(capture, line)` citation; EV-08, EV-09, and EV-10 cite separate lines 15, 16, and 17. The independent pinned-blob check found 13 JSON events and 13 markdown table rows with matching IDs, times, citations and writers (`…:corpus/knowledge/boot-writers-r19.json:268-359`; `…:corpus/knowledge/boot-writers-r19.md:64-84`). The gate returned `status=PASS`, `events_total=13`, `attributed_events=13`, `unattributed=0`, exit 0 (command above).
- The capture digest for r19c is `669cada8c08e00cae06b1429f81f254a744f3a7a1d6fe684592fbe202dea298d` in the registry (`…:corpus/knowledge/boot-writers-r19.json:13-16`); the read-only `sha256sum` check returned that same digest for the pinned capture.

## Residual

This verifies that the captured journal records report `Updated: /boot/limine.conf`; it does not prove the file's content changed. The knowledge entry explicitly records that limitation (`8e5916360f2dfe7bc4eb4ba144081af555900116:corpus/knowledge/boot-writers-r19.md:97-100`). I did not inspect the live host or `/boot`; these findings concern the committed captures only.

Scope: executed=python3 tools/check-boot-writers.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116; sha256sum .ufo/waves/round-19/l1-capture/host-capture-r19.txt .ufo/waves/round-19/l1-capture/host-capture-r19b.txt .ufo/waves/round-19/l1-capture/host-capture-r19c.txt
