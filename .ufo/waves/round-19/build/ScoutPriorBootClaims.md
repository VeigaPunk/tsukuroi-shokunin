# C2 corpus sweep — prior /boot-writer claims

Model: commandcode/deepseek-v4.1-flash. Paths from lane root; K=corpus/knowledge, C=.ufo/waves/round-19/l1-capture, A/B/D=host-capture-r19/r19b/r19c.txt. C=confirmed, R=refined, X=contradicted, †=append supporting note (never rewrite).

Sweep (grep tool; matched lines) over K: `limine\.conf` 6; `limine_history` 8; `Updated:` 2; `ExecStopPost` 0; `snapper-cleanup` 3; `limine-snapper-sync` 66; `99-limine\.hook` 5; `limine-mkinitcpio-install` 3. SKILL.md: combined patterns 2 (1874,1940); writer-language 1 (1878); `/boot writer`-class 0.

1. `K/boot-chain-r17.md:29-31` [inf] sync made limine_history copies 09:29:18 — C [obs] `D:23-24,39-41` (`Copied:`). † [inf]→[obs].
2. `K/boot-chain-r17.md:34-36` 12:07:07 cleanup write — C+R: drop-in `ExecStopPost=limine-snapper-sync` (`A:256-260`), hourly timer (`A:221-231`), 10 events 09:03–17:07 (`D:11-20`; `B:1686` count=10). †
3. `K/boot-chain-r17.json:112` same attribution — C+R identically. †
4. `K/update-safety-note.md:226-228` hook rebuilds initramfs — C (`B:1457-1459`)+R: writes limine.conf; [inf] limine-entry-tool does it (script grep only BOOT_PATH, `B:1509-1511`; `B:1516,1524`; `A:576-598`, pacman.log 3015/3047; `B:1699-1702`). †
5. `K/update-safety-note.md:81-82,229-231` 99-limine.hook copies EFI binaries — C (`B:1469`); no limine.conf write.
6. `K/update-safety-note.md:216` three operator hooks — C (`A:263-280`).
7. `K/degraded-triage-r4.md:366-370,621` hook Exec/Target — C (`B:1389-1470`).
8. `K/boot-chain-r17.md:124-126` pruning limits — C (`A:419,428`).
9. `K/journal-boot-plane.md:141-145` watcher/sync config logs — not a /boot-writer claim; R: watcher lacks inotifywait, falls back to plugin (`B:1645`).
10. `SKILL.md:1874-1878` tool reads limine.conf, never writes /boot — consistent; no host-writer claim.

No X found [obs]; `ExecStopPost` absent from K, so the mechanism was unrecorded (R not X). [unk] direct sync-service writes outside plugin/ExecStopPost; limine.conf mtime unreadable non-root (`A:439-440`). Stray read-only `ls` was run inadvertently; item is NO-EXEC.

Scope: executed=ls
