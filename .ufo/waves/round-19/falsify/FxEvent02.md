# FxEvent02 — boot event batch 2/4 (EV-05, EV-06, EV-07) re-verification

## Attack
C2 depth claim (`corpus/knowledge/boot-writers-r19.json`, revision `8e5916360f2dfe7bc4eb4ba144081af555900116`): all 13 `Updated: /boot/limine.conf` events attributed to 7 named writer classes. This seat re-verifies batch 2/4: EV-05, EV-06, EV-07. Falsifiable axes: (1) citation accuracy — cited capture file/line exists and the quoted text is on that exact line; (2) attribute fidelity — timestamp, unit name, and the `Updated: /boot/limine.conf` marker on the line; (3) writer-class fidelity — the named class exists in `writers[]` and its `signature` section actually matches the capture line; (4) uniqueness — no other event id cites the same capture line; (5) count consistency — the knowledge entry's event table row count and declared total match the JSON event set and the host captures. A wrong line number, off-by-one timestamp, mismatched signature regex, double-assigned line, or a count that does not sum refutes the claim.

## Method
All reads against the attack revision via `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 8e5916360f2dfe7bc4eb4ba144081af555900116:<path>` (lane working copy is at `2fd1e6768f18`, ahead of the attack revision, so the working tree was not used as evidence). Then, with `python3` (read-only JSON/line checks):

1. Parse `corpus/knowledge/boot-writers-r19.json`; recompute sha256 of each of the 3 declared captures and compare with the manifest (`captures[]`).
2. For EV-05/06/07: extract the cited line from the cited capture; check `quote` is an exact prefix of the line, timestamp token, unit token, and presence of `Updated: /boot/limine.conf`.
3. Resolve each event's `writer` against `writers[]`; apply the class `signature` to the capture line: `journal-unit` values as literal substring, `journal-unit-regex` values as `re.search`.
4. Duplicate check: collect `(capture, line)` for all 13 events; verify 13 distinct keys and no other event id on EV-05/06/07's lines; additionally dedup all `Updated:` renderings across both captures by `(timestamp, pid)` to confirm the same host event is never assigned two ids.
5. Count consistency: count marker occurrences in `host-capture-r19b.txt` and `host-capture-r19c.txt`, distinguish event rows from probe-command echo lines and corroborating re-renders; parse the knowledge entry `corpus/knowledge/boot-writers-r19.md` event table (13 data rows) and cross-check EV-05..07 rows (time, capture ref, signature column, writer) against the JSON; read the prose count declaration.
6. Official gate in a fresh scratch clone pinned to the attack revision (no gate run in the live lane):
   `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsk-r19-fxevent02 && git -C /tmp/tsk-r19-fxevent02 checkout -q --detach 8e5916360f2dfe7bc4eb4ba144081af555900116 && cd /tmp/tsk-r19-fxevent02 && python3 tools/check-boot-writers.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116`
7. No tool installs were needed (no new tool installed/updated). No host probe, no pacman, no writes outside this report; scratch clone removed after the run.

## Verdict
- **EV-05: CONFIRM** (claim C2, batch 2/4)
- **EV-06: CONFIRM** (claim C2, batch 2/4)
- **EV-07: CONFIRM** (claim C2, batch 2/4)

All five axes hold for all three ids; no axis failed. Gate status `PASS` with `attributed_events=13, events_total=13, unattributed=0, writer_classes=7, findings=[]`.

## Evidence
Attack revision: `8e5916360f2dfe7bc4eb4ba144081af555900116` ("checkpoint(r19): retain developed verification evidence for resume; admission pending", 2026-10-20 19:33:13 -0300).

- **Capture integrity**: recomputed sha256 of all three captures matches the JSON manifest — `host-capture-r19.txt` `d060de16…`, `host-capture-r19b.txt` `c4cc08fe…`, `host-capture-r19c.txt` `669cada8…` (all `match=True`).
- **EV-05** — `8e591636:.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:12`:
  `2026-10-20T09:29:19 260715 limine-snapper- limine-snapper-add-2-260668.service /system.slice/limine-snapper-add-2-260668.service Updated: /boot/limine.conf`
  JSON quote is an exact prefix; timestamp `2026-10-20T09:29:19` ✓; unit `limine-snapper-add-2-260668.service` ✓; marker ✓. Writer `W-SNAPPER-PLUGIN` exists in `writers[]`; its `signature` = `{kind: journal-unit-regex, value: " limine-snapper-(add|delete|modify)-[0-9]+-[0-9]+\.service /system\.slice/limine-snapper-(add|delete|modify)-[0-9]+-[0-9]+\.service "}` → `re.search` on line 12 = True. Corroborated by `host-capture-r19b.txt:1635-1638` (window 09:27:00–09:31:30: `2026-10-20T09:29:19-03:00 … limine-snapper-sync[260715]: Updated: /boot/limine.conf`) and `host-capture-r19c.txt:42` (same event re-rendered).
- **EV-06** — `8e591636:.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:13`:
  `2026-10-20T10:07:03 6567 limine-snapper- snapper-cleanup.service /system.slice/snapper-cleanup.service Updated: /boot/limine.conf`
  Timestamp/unit/marker ✓. Writer `W-SNAPPER-CLEANUP` exists; `signature` = `{kind: journal-unit, value: " snapper-cleanup.service /system.slice/snapper-cleanup.service "}` → literal substring match = True. Corroborated by `host-capture-r19b.txt:1641` (`2026-10-20T10:07:03-03:00 … limine-snapper-sync[6567]: Updated: /boot/limine.conf`, window `-u snapper-cleanup.service -u limine-snapper-sync.service`).
- **EV-07** — `8e591636:.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:14`:
  `2026-10-20T11:07:04 1135802 limine-snapper- snapper-cleanup.service /system.slice/snapper-cleanup.service Updated: /boot/limine.conf`
  Timestamp/unit/marker ✓; writer and signature literal match = True. (Period ~1h spacing to EV-06/08 matches the `OnUnitActiveSec=1h` cleanup timer declared in the writer's trigger.)
- **Uniqueness**: 13 events → 13 distinct `(capture, line)` keys, zero duplicates. Lines `r19c:12/13/14` are cited only by EV-05/06/07 respectively. Corroborating renderings (`r19b:1638`→EV-05, `r19b:1641`→EV-06, `r19c:25`→EV-02, `r19c:42`→EV-05) carry **no** event id — `(timestamp, pid)` dedup across both captures yields exactly 13 distinct host events, none double-assigned.
- **Count consistency**: `host-capture-r19b.txt:1685-1686` — host-side `journalctl … -t limine-snapper-sync | grep -c "Updated: /boot/limine.conf"` since 2026-10-19 → **10**, equal to the 10 journal rows `r19c:11-20` (all ten end in exactly `Updated: /boot/limine.conf`; the r19c probe filter accepts any `/boot/limine.conf` MESSAGE, but no non-`Updated` message entered the event set). `r19b:1688-1702` (pacman.log grep) contains exactly 3 ALPM `Updated:` rows — pacman.log lines 2021, 3015, 3047 → `r19b:1695/1700/1702` = EV-01/03/04. 10 + 3 = 13. Knowledge entry `8e591636:corpus/knowledge/boot-writers-r19.md` event table has exactly 13 data rows EV-01..EV-13; EV-05/06/07 rows match the JSON on time, capture ref (`host-capture-r19c.txt:12/13/14`), signature column, and writer; prose declares "Count: 13 attributed events = 10 journal rows (r19c:11-20) + 3 pacman.log ALPM rows".
- **Gate** (fresh clone at the attack revision): `python3 tools/check-boot-writers.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116` →
  `{"branch":"master","branch_tip":"2fd1e6768f187be8c5e837af6286c3736953fcff","counts":{"attributed_events":13,"events_total":13,"unattributed":0,"writer_classes":7,"writers_with_events":3},"findings":[],"revision":"8e5916360f2dfe7bc4eb4ba144081af555900116","status":"PASS"}`

## Residual
- Timezone presentation: r19c-derived rows (EV-02, EV-05..13) are naive local time in JSON/md (no `-03:00`), while EV-01/03/04 carry offsets; naive values equal the `-03:00` short-iso renders in the same captures (e.g. `r19c:11` 09:03:03 = `r19c:25` 09:03:03-03:00). Presentation only, no instant discrepancy.
- My md/JSON cross-checker flagged EV-01/03/04 `table_time_match=False` — checker artifact: pacman.log lines embed a line-number prefix (`2021:[2026-10-11T16:16:36-0300] …`), so first-token extraction fails; the md times are correct against line content. Not a defect, and outside this batch.
- Writer `mechanism_refs` lines and `sources` (S066–S076) were not re-verified — the attack item scopes the writer check to existence + signature section; signature sections all match.
- Gate reports `writers_with_events=3` (W-MKINITCPIO-HOOK, W-SNAPPER-PLUGIN, W-SNAPPER-CLEANUP); the other 4 classes attribute none of the 13 events, consistent with the entry (e.g. W-WATCHER declared "dormant on this host"). Whether 7-class attribution overstates coverage is a claim-level question outside batch 2/4.
- Only captures committed at the attack revision were used; no /boot access (host-safety rule observed).

Scope: executed=git -C <lane> log -1 --format='%H %ci %s' 8e5916360f2dfe7bc4eb4ba144081af555900116; git -C <lane> cat-file -t <rev>:tools/check-boot-writers.py; git -C <lane> show <rev>:corpus/knowledge/boot-writers-r19.json; git -C <lane> show <rev>:{host-capture-r19.txt,host-capture-r19b.txt,host-capture-r19c.txt}; git -C <lane> show <rev>:corpus/knowledge/boot-writers-r19.md; git -C <lane> rev-parse --short=12 HEAD; git clone --no-hardlinks <lane> /tmp/tsk-r19-fxevent02 && git -C /tmp/tsk-r19-fxevent02 checkout -q --detach 8e5916360f2dfe7bc4eb4ba144081af555900116 && python3 tools/check-boot-writers.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116; python3 (read-only JSON/line/sha256/regex checks over the above); rm -rf /tmp/tsk-r19-fxevent02; write .ufo/waves/round-19/falsify/FxEvent02.md
