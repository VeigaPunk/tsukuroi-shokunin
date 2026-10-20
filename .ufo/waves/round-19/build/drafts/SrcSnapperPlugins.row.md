# SrcSnapperPlugins — draft SOURCES row (round 19, C2 web source)

Draft only; not landed. Next free id confirmed after `corpus/SOURCES.md:72` (S065); registry after landing: 66 rows (S001–S066).

| id | title — url | kind | tier | teaches | anchor | claim | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S066 | snapper(8) PLUGINS — https://raw.githubusercontent.com/openSUSE/snapper/v0.13.2/doc/snapper.xml.in (rendered: https://raw.githubusercontent.com/openSUSE/snapper/gh-pages/manpages/snapper.html) | docs | A | Snapper's documented plugin contract: plugin directory, action-as-first-argument, and the post-action verbs that the installed limine-snapper-sync plugin dispatches on; scoped to the contract, not to any host write or plugin run | §PLUGINS, `refsect1 id='plugins'`, v0.13.2 `doc/snapper.xml.in:893-1004`; rendered gh-pages `manpages/snapper.html:997-1051` (`#plugins`, section head through the create-snapshot-post entry); action list at XML:932-935 (`create-snapshot-post <subvolume> <fstype> <snapshot-number>`); v0.13.2 tag commit `43475845a712bc2327cec2ed641063df406705de` (tagger 2026-09-07), man-page date 2026-01-02; Arch `extra` 0.13.2-1 build 2026-09-16 | “snapper can execute external scripts after certain actions. Scripts have to be placed in /usr/lib/snapper/plugins.” (15 words; one wrap normalized, XML:895-896 / HTML:999-1000) — the page defines create-, delete- and modify-snapshot-post with positional arguments subvolume, fstype, snapshot-number, so the plugin's `$1`/`$2`/`$4` reads match the documented order; it does not establish that any plugin wrote `/boot` at a given time | queued | 2026-10-20 | on-release | tools/check-boot-writers.py (planned C2 attribution source) |

## Opened-URL trail

| URL | Result |
|---|---|
| https://man.archlinux.org/man/snapper.8 | failed: ECONNRESET (socket closed) |
| https://man.archlinux.org/man/snapper.8.en | failed: ECONNRESET |
| https://man.archlinux.org/man/snapper.8.txt | failed: ECONNRESET |
| https://snapper.io/ | failed: ERR_TLS_CERT_ALTNAME_INVALID |
| https://raw.githubusercontent.com/openSUSE/snapper/v0.13.2/doc/snapper.xml.in | opened (man-page source, version-pinned) |
| https://raw.githubusercontent.com/openSUSE/snapper/gh-pages/manpages/snapper.html | opened (rendered page, `#plugins`) |
| https://api.github.com/repos/openSUSE/snapper/git/refs/tags/v0.13.2 and `/git/tags/183a120a15b127ee28c319432f0a44f9f7f17203` | opened (tag → commit pin) |
| https://archlinux.org/packages/extra/x86_64/snapper/json/ | opened (version 0.13.2-1, build 2026-09-16) |

Search counts (substitute-doc route, since man.archlinux.org was unopenable): identified 6, screened 6, included 2 (v0.13.2 XML, rendered gh-pages HTML), excluded 4 (3 ECONNRESET, 1 TLS altname). The man page does contain plugin text, so no upstream-docs fallback was needed.

## Scope limits

- The row documents the plugin **contract**; C2 attribution of `/boot/limine.conf` writes still needs the installed plugin file (`.ufo/waves/round-19/l1-capture/host-capture-r19b.txt:1093-1244`) and the journal/ALPM events.
- Man page caveat: “It is undefined whether the plugins are called from the client (snapper) or server (snapperd)” (XML:1002-1003), so a writer attribution must not assume the `snapper` client process as parent.
- [unk] Byte-identity of the Arch-rendered `snapper.8` (package 0.13.2-1) with upstream v0.13.2 §PLUGINS was not verified: man.archlinux.org was unreachable and the installed `/usr/share/man/man8/snapper.8.gz` could not be decompressed with this seat's read/grep tools (gz shown as file metadata only).
