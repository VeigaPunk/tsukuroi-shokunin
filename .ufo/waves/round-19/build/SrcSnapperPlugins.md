# SrcSnapperPlugins — C2 web source (snapper plugin mechanism)

[obs] `https://man.archlinux.org/man/snapper.8` plus `.8.en` and `.8.txt` failed ECONNRESET on 2026-10-20; `https://snapper.io/` failed ERR_TLS_CERT_ALTNAME_INVALID. Opened the linked project docs instead: `raw.githubusercontent.com/openSUSE/snapper/gh-pages/manpages/snapper.html:997-1051` (§PLUGINS, anchor `#plugins`).

[obs] Version-pinned man-page source, tag v0.13.2 (annotated tag `183a120…` → commit `43475845a712bc2327cec2ed641063df406705de`, tagger 2026-09-07): `doc/snapper.xml.in:893-1004` §PLUGINS (`refsect1 id='plugins'`). Quote, 15 words, one wrap normalized (XML:895-896, HTML:999-1000): “snapper can execute external scripts after certain actions. Scripts have to be placed in /usr/lib/snapper/plugins.” The action list defines `create-snapshot-post <subvolume> <fstype> <snapshot-number>` (XML:932-935) plus delete/modify-snapshot-post, set-read-only-*, set-default-snapshot-* and rollback-post. Man-page date 2026-01-02; Arch `extra` snapper 0.13.2-1, build 2026-09-16 (`https://archlinux.org/packages/extra/x86_64/snapper/json/`).

[obs] The contract matches the installed plugin's positional reads: `.ufo/waves/round-19/l1-capture/host-capture-r19b.txt:1103-1105` (`$1` ACTION, `$2` SUBVOLUME, `$4` SNAP_ID) against documented `subvolume, fstype, snapshot-number`; dispatch at `:1227-1244`; root-subvolume filter `:1111`.

[obs] Contract caveat: “It is undefined whether the plugins are called from the client (snapper) or server (snapperd)” (XML:1002-1003) — attribution must not assume the snapper client as parent process.

[inf] Draft row S066 (next free after `corpus/SOURCES.md:72` S065) written at `.ufo/waves/round-19/build/drafts/SrcSnapperPlugins.row.md`; kind docs, tier A, teaches the plugin contract. It grounds the trigger mechanism, not any particular `/boot` write.

[unk] Byte-identity of the Arch-rendered `snapper.8` (0.13.2-1) with upstream v0.13.2 §PLUGINS is unverified: man.archlinux.org was unreachable and `/usr/share/man/man8/snapper.8.gz` could not be decompressed by this seat's read/grep tools (returned file metadata only).

Substitute-doc search counts: identified 6, screened 6, included 2 (v0.13.2 XML, rendered gh-pages HTML), excluded 4 (3 ECONNRESET, 1 TLS altname). The man page does contain plugin text, so no upstream-docs fallback was required. Answering model: commandcode/deepseek/deepseek-v4.1-flash.

Scope: executed=none
