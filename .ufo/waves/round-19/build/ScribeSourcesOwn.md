# ScribeSourcesOwn — round-19 own-work SOURCES rows S066–S069 (author-side draft)

Behavior: drafted four own-work rows (S066–S069) and four Gate-table source lines. No admission authority. No file outside the drafts and this report was written.

Draft: `.ufo/waves/round-19/build/drafts/ScribeSourcesOwn.rows.md`

Observed (read-only):
- [obs] Registry ends at S065 (`corpus/SOURCES.md:72`); S066 is the next free id.
- [obs] Line-1 script digests: r19 `f8f9d38d…` (`host-capture-r19.txt:1`), r19b `b66fa7b3…` (`host-capture-r19b.txt:1`), r19c `fc916fd3…` (`host-capture-r19c.txt:1`). Self-declared; not re-hashed [unk].
- [obs] /boot writes: 10 journal `Updated: /boot/limine.conf` events (`host-capture-r19c.txt:11-20`; `host-capture-r19.txt:562-563` count = 10). Eight are snapper-cleanup.service (ExecStopPost drop-in, `host-capture-r19.txt:256-260`), two are transient `limine-snapper-add-*` units.
- [obs] Two ALPM-SCRIPTLET writes: pacman.log 3015 and 3047 at `host-capture-r19.txt:578` and `:597`; same lines in r19b at `:1700` and `:1702`.
- [obs] Census: inbound 114, outbound 10 (`adjacency-pointers-r19.json:87-90`). The 10 outbound pointers cite 8 distinct siblings; all 8 snapshot directories exist.

Discrepancies with the brief:
- [obs] Hook content in r19b is `:1399-1508`, not `1399-1633`; `:1509-1633` are other greps. Drafted with `1399-1508`.
- [obs] Plugin `systemd-run` line is `:1183-1185`, inside the `:1093-1245` block (brief correct).

Gaps:
- [unk] Census JSON and `extract-adjacency-r19.py` digests are not recorded and were not computed (no EXEC-AUTHORIZED). S069 anchor carries this gap.
- [unk] Capture script digests were not re-verified against `capture-r19*.sh`.
- Used-by left as `—`, the existing placeholder convention (S013).

Tooling: none installed or updated.

Scope: executed=none
