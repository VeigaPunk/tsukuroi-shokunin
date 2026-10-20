# CritWritersCircular — C2 /boot writer attribution

Verdict: direction sound; three required corrections before the gate is non-vacuous.

**1. Denominator — partially self-selected, fixable.** [obs] Journal side is honest: `journalctl -g "/boot/limine.conf"` is tag-agnostic, untruncated count 10 (host-capture-r19.txt:524-563; host-capture-r19b.txt:1685-1686). [obs] Pacman side: the captured tail itself contains a THIRD `Updated: /boot/limine.conf` event — pacman.log:2021, 2026-10-11 (host-capture-r19b.txt:1695), inside claim-scope bytes. `check-boot-writers.py` MUST enumerate `Updated:` lines itself and apply a stated window (≥2026-10-19T00:00, the journal sweep bound), else the denominator is ambiguous (12 vs 13) or hardcoded. [obs] Events duplicate across files (12:07:07 at r19.txt:446, r19.txt:548, r19c.txt:15); dedupe by (timestamp,pid,unit) or the count inflates past 12.

**2. Taxonomy is a posteriori — circularity risk real.** [obs] Writer classes read straight off observed `_SYSTEMD_UNIT` (r19c.txt:11-20). [inf] If classes = {observed units}, attribution is tautological. Fix: derive class regexes from mechanism bytes — drop-in `ExecStopPost=limine-snapper-sync` (r19.txt:256-260), plugin `--unit=limine-snapper-${op}-${SNAP_ID}-$$` (r19b.txt:1191-1195, matching `add-1-5846`/`add-2-260668`), hook `Exec=` (r19.txt:397, `running '90-mkinitcpio-install.hook'` r19b.txt:1698) — plus residual classes: limine-snapper-sync.service/watcher path (watcher live, inotifywait absent, r19b.txt:1645-1683), limine-snapper-restore (r19b.txt:1244-1245), limine-update, manual. Explicit UNATTRIBUTED bucket; unmatched unit → red.

**3. Empty prior (M030).** [obs] r17 already attributed: 12:07:07→snapper-cleanup/limine-snapper-sync (boot-chain-r17.md:34-36), snapshot-add (:29-31); r18 closure:206-208,271-273. `0→12` holds only if the metric is *mechanism-anchored* attribution. Rename to `mechanism_anchored_events`; honest before ≈3 name-level, 0 mechanism-anchored; red-before = gate red on baseline corpus bytes.

**4. Depth vs coverage — depth is correct.** Same surface already attributed name-level; the new layer is mechanism resolution. Guard: output MUST cite prior attributions (duplicate-authority risk) and keep the "events in captures" bound — silent writes unobservable (limine-update 09:26, r17:25-28; stat denied r19.txt:439-440).
Scope: executed=none
