# ScribeWritersSkill — R19 C2 SKILL addition (report)

Draft: `.ufo/waves/round-19/build/drafts/ScribeWritersSkill.append.md` (append-only section `## R19 — expected /boot writers (decision table)`; 7,715 B). Nothing else was written.

## Behavior
- Decision table `| Signature seen | Writer | Expected when | Action |` with 7 writer classes W1-W7 (W1 cleanup stop, W2 snapper-create plugin, W3 delete/modify plugin, W4 watcher, W5 mkinitcpio hook, W6 deploy hooks, W7 restore hook). Counts: W1=8 (`r19c:13-20`), W2=2 (`r19c:11-12`), W5=2 (`r19:578`, `r19:597`), total 12 with the 10 journal events (`r19c:11-20`).
- Error list E1-E6, and a 5-step read-only checklist with no sudo, no limine-update, and no package-manager binary.

## Corrections to the assignment
- **Lock skip is misattributed.** `/run/limine-snapper-cleanup.lock` is checked only by the watcher (`r19b:1373-1374`). The snapper plugin (`r19b:1160-1169`) and the cleanup `ExecStopPost` (`r19:260`) have no lock check. The draft's E6 says this. [obs]
- **Watcher is in fallback on this host.** `inotifywait` is absent; the watcher exits 0 (`r19b:1365-1367`; journal `r19b:1645`, `1683`). W4 is expected-silent. [obs]
- **Knowledge entry absent.** `corpus/knowledge/boot-writers-r19.md` does not exist (glob, no match). The draft cites it as absent. [obs]
- **"Seven writer classes" not enumerated in the Goal.** I derived the seven above. [inf]
- **Script literal.** `limine-mkinitcpio-install` contains no literal `limine.conf`/`Updated`/`Copied` (`r19b:1509-1510`). Attribution of those strings to limine-entry-tool is [inf].

## Findings
- 2026-10-20 09:03:03–09:08:04 `snapper-cleanup.service` run has no limine line (`r19c:46-57`). Unexplained [unk].
- A third ALPM `Updated` exists at 2026-10-11 16:16:36 (`r19b:1694-1695`; pacman.log 2021), outside the round window. [obs]
- Earlier-window `limine-snapper-delete-*` units: none in captures. Whether a delete occurred is [unk].

## Tooling
No tool installed or updated.

## Open
Knowledge entry `boot-writers-r19.md` (owner: knowledge seat). Checklist commands were not executed; step 2 is adapted from `r19b:1688`.

Scope: executed=none
