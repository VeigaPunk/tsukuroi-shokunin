# NoticeHealth — host-health-report-r3 U1 and banner notice drafts

Behavior: six freshness records (`R18-FRESH-NoticeHealth-01..06`) for `corpus/knowledge/host-health-report-r3.md`, one heading `## R18-FRESHNESS — host-health U1 and R15 banner current-use (2026-10-20)`. Drafts only; no production file touched.

Drafts: `.ufo/waves/round-18/build/drafts/NoticeHealth.append.txt`, `.ufo/waves/round-18/build/drafts/NoticeHealth.records.json`.

Findings:
- [obs] U1 (`host-health-report-r3.md:301-306`) rests on a 2026-10-14 11:45 header-only `snapper list-configs`. R18 lists `home` and `root` (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:76-77`) and `SNAPPER_CONFIGS="root home"` (`:80`). Snapshot presence and rollback were not observed.
- [obs] Banner `:591-594`: R18 ran no `pacman -Qu`, so the pending count is UNKNOWN (neither 413 nor zero).
- [obs] Local DB lists `mkinitcpio-42.2-1` (`:34`); no 41.1 entry in `:27-38`. Pending state of 42.2-1 is UNKNOWN.
- [obs] Later `pacman -U` transactions at 09:31:03 (`:72`) and 13:23:08 (`:73`). R17 full `-Syu` at 09:15:30 (`.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:59`).
- [unk] libinput state was not re-observed; the banner statement is not restated as current.
- Historical bytes preserved; notice clears no package, reboot, or snapshot-boot status.

Checks (read-only, in-memory):
- All six `baseline_quote` strings occur exactly once in `842a5312` host-health bytes; `notice_heading` absent there.
- Each `now` and `capture_ref` appears in the append block; each `capture_quote` is a substring of its cited line (six pass).
- `S060` row exists in `corpus/SOURCES.md`; R18 capture is committed at `51dd9ee` (`git ls-files`, `git log`).

Not done: notice gate run (BuildNoticeGate's job); U2–U8 and J4 untouched; the R15 BLOCKED decision is not cleared. The lead must add a separator when concatenating the append block.

Installs/updates: none.

Scope: executed=git show 842a5312b704b5cda10fd80ec1fdee5fb381ba97:corpus/knowledge/host-health-report-r3.md; git ls-files --error-unmatch and git log -1 on round-18/round-17 captures (read-only); python substring and line-quote checks; wrote the two draft files and this report only.
