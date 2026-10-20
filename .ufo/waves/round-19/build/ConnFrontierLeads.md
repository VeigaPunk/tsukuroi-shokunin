# ConnFrontierLeads

Model: Grok 4.7. Author-side only. Axes: C2 depth, Frontier. C1 and C3 untouched. No install.

**Evidence.** [obs] GitLab issues API `state=all`: page 1 iids 18–1, page 2 `[]`. [obs] No description contains `ExecStopPost`. [obs] #4 https://gitlab.com/Zesko/limine-snapper-sync/-/issues/4 "Snapper automatic cleanup blocked by limine-snapper-watcher"; quote (19 words): "conflict when both the cleanup process and limine-snapper-sync v1 try to access a snapper CLI at the same time". Notes API and project search API: HTTP 401; HTML thread has no ExecStopPost and no hourly claim. [obs] Closer cites 754090077de4b5e9de8f09a870ae7301d56dec13, message "Skip sync when cleanup is active"; diff adds `ExecStopPost=limine-snapper-sync --no-force-save`. [obs] CHANGELOG 1.12.0: "Sync runs afterward. (#4)". [obs] Master `limine-snapper-override.conf` (blob 58480985895d77d93326a08e67d7919d27f66997) is `ExecStopPost=limine-snapper-sync` and matches `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:258-260`. [obs] Eight `Updated: /boot/limine.conf` lines under `snapper-cleanup.service`: `host-capture-r19c.txt:13-20`. Hour is snapper's timer, `host-capture-r19.txt:223-228`. [obs] S033 four issues: GitHub `"ExecStopPost=limine-snapper-sync"` total_count 0. #6683 and #11100 report cleanup/service failure, not a conf rewrite.

**Counts.** GitLab: identified 18, screened 18, included 0, excluded 18. S033: identified 4, screened 4, included 0, excluded 4.

**Move.** Do not add a row. The eight hourly writes are the #4 fix's packaged ExecStopPost (intended post-cleanup sync), not a filed bug. Next frontier source is that drop-in plus changelog 1.12.0 and commit 75409007, not an issue.

**Risks.** [inf] "Sync runs afterward" does not name `limine.conf`; the journal line does. [unk] Whether each hourly "Updated" changed bytes. [obs] 75409007 still passed `--no-force-save` and used `limine-override.conf`; host matches current master, not that first diff. [unk] A note behind the 401 was not read; the opened HTML thread does not contain it.

**Verification.** Diff the three Exec lines to `host-capture-r19.txt:258-260`. No host probe. Search-log draft: `.ufo/waves/round-19/build/drafts/ConnFrontierLeads.searchlog.md`.

Scope: executed=none
