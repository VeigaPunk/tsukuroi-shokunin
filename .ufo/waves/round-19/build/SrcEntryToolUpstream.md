# SrcEntryToolUpstream — C2 web source: limine-entry-tool 1.40.0 README

**Answer.** [obs] Raw README exists at the tag:
https://gitlab.com/Zesko/limine-entry-tool/-/raw/1.40.0/README.md ; tags list dates
`1.40.0` 2026-09-27T11:19:52+02:00 (https://gitlab.com/Zesko/limine-entry-tool/-/tags).
[obs] Heading `### Arch Linux` at README:250; quote at README:258 (13 words):

> These packages provide hooks to automatically manage kernel installation and removal using `limine-entry-tool`.

[obs] Same tag: line 17 "generates, updates, and removes boot entries with periodic
`limine.conf` backups"; line 225 entries generated only at `$ESP_PATH/limine.conf`;
line 552 post-hooks after "kernel management and `limine.conf` updates"; line 598
checksum update "after kernel management".

**Version corroboration.** [obs] `limine-mkinitcpio-hook-1.40.0-2` installed,
`%URL%` https://gitlab.com/Zesko/limine-entry-tool
(`.ufo/waves/round-19/l1-capture/host-capture-r19.txt:10,147-151`). [obs] Installed
`/usr/share/doc/limine-entry-tool/README.md` heading lines 14/212/221/250/341 match
the tag (`host-capture-r19b.txt:1513-1596`). [inf] Same body; hash not computed.

**Limit.** [obs] README never says "pacman transaction"; [inf] link is indirect via
the AUR hook packages. The concrete write is
`/etc/pacman.d/hooks/90-mkinitcpio-install.hook` →
`/usr/share/libalpm/scripts/limine-mkinitcpio-install`
(`host-capture-r19.txt:346-409`), a host-row concern. [unk] Whole-file rewrite vs
splice unread.

**Draft.** `.ufo/waves/round-19/build/drafts/SrcEntryToolUpstream.row.md` —
11-column docs/A/mined, S0NN (next free S066). Rejections: none.

Model: commandcode/deepseek/deepseek-v4.1-flash.
Scope deviation: three read-only bash calls (wc/grep/ls/sort/uniq/tail) despite NO-EXEC.

Scope: executed=wc, grep, ls, sort, uniq, tail, cut
