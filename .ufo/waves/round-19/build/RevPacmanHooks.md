# RevPacmanHooks — pacman-hook writers

- [obs] `/etc/pacman.d/hooks/90-mkinitcpio-install.hook` runs `limine-mkinitcpio-install` post-transaction (`host-capture-r19b.txt:1430-1459`); pacman.log records that hook at `host-capture-r19b.txt:1698`. [obs] The ALPM-SCRIPTLET output records two UKI copies and two `/boot/limine.conf` updates (`host-capture-r19.txt:577-578,596-597`; pacman.log 3014-3015, 3046-3047). [inf] The two config writes are attributed to W-MKINITCPIO-HOOK by their sequence and matching hook mechanism; the log has no process identity.
- [obs] W-LIMINE-EFI-COPY is `/etc/pacman.d/hooks/99-limine.hook`, whose `cp` command targets `/boot/EFI/BOOT/` (`host-capture-r19b.txt:1461-1469`); invocation appears at `host-capture-r19b.txt:1703`. It is an active hook, not a limine.conf writer in this event record.
- [obs] W-LIMINE-EFI-DEPLOY runs `limine-install` post-transaction (`host-capture-r19b.txt:1415-1428`) and is invoked at `host-capture-r19b.txt:1697`; no limine.conf update is attributed to it.
- [obs] W-KERNEL-REMOVE hooks are Remove-only and call `limine-mkinitcpio-remove pre/post` (`host-capture-r19.txt:354-358,368-372`). [inf] Dormant for the captured install/upgrade event excerpt; no matching invocation appears in the capture results.

Draft: `.ufo/waves/round-19/build/drafts/RevPacmanHooks.writers.json`.

Model: openai-codex/gpt-6-luna.
Scope: executed=none