# S198 — new SOURCES.md row (journalctl(1) at systemd 262)

## Max-id check (run before proposing the row)

```
$ grep -oE 'S[0-9]+' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md | sort -V | tail -1
S197
```

So **S198 is the next free id** — no collision. (Second check: `grep -cE '^\| S[0-9]+' corpus/SOURCES.md` → `197` registry rows, consistent.)

## Which URL was used (assignment required recording this)

**Primary: `https://man.archlinux.org/man/journalctl.1`** — native HTML, footer reads **`systemd 262.1`** (plus `Package version: 262.1-1`, `core/systemd`). It therefore satisfies the "footer must read systemd 262.x" test and **is** the source used for the anchored quotes.

Also fetched, as corroboration and as the upstream-pinned twin:
- `https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml` (raw upstream XML at the v262 tag)
- `https://raw.githubusercontent.com/systemd/systemd/v262.1/man/journalctl.xml` — **byte-identical** to the v262 XML (same sha256)
- `https://raw.githubusercontent.com/systemd/systemd/main/man/journalctl.xml` — **byte-identical** to the v262 XML at fetch time (same sha256)
- `https://man.archlinux.org/man/journalctl.1.txt` (plain-text rendering of the same 262.1 page)

## Fetched bytes (sha256)

| Artifact | Bytes | sha256 |
|---|---|---|
| `journalctl.1.arch.html` (man.archlinux.org, native HTML) | 65136 | `aaae4efa61ff9c56e6249feb2f4527db57f1a4beb0eac4ad1eeb111a4bbb83c2` |
| `journalctl.1.arch.txt` (same page, .txt rendering) | 50637 | `414c1f4755e73872e25c39eb3cf934a1643825d5ac95b2e35149fe39c43348c5` |
| `journalctl-v262.xml` (upstream tag v262) | 61619 | `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd` |

The upstream XML sha256 `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd` **matches the sha256 already recorded for S188** (`corpus/SOURCES.md:194`, tag v262 `man/journalctl.xml`) — the upstream blob is reproducible, and S198's man-page quotes agree with that already-mined blob.

Snapshots kept in this seat dir: `journalctl.1.arch.html`, `journalctl.1.arch.txt`, `journalctl-v262.xml`, `snapshot-arch-html-653-663.txt`, `snapshot-arch-txt-665-685.txt`, `snapshot-arch-footer.txt`.

## Footer / version evidence

`journalctl.1.arch.html:1095` → `<td class="foot-os">systemd 262.1</td>`
`journalctl.1.arch.html:1119` → `<dd>262.1-1</dd>` (package `core/systemd`)
`journalctl.1.arch.txt:1125` → `systemd 262.1                                                    JOURNALCTL(1)`
Arch HTML page foot-note also states conversion by `mandoc` (mandoc.bsd.lv) from the packaged man source.

## Located quotes (each ≤25 words) with location

1. **`-N`/`--fields` semantics** — `journalctl(1)` §COMMANDS, `-N, --fields` entry (arch HTML lines 653-657; .txt lines 669-673; upstream `man/journalctl.xml:891-897`, "Added in version 229"):
   > “Print all field names currently used in all entries of the journal.”

2. **`-F`/`--field=` semantics** — `journalctl(1)` §COMMANDS, `-F, --field=` entry (arch HTML lines 658-662; .txt lines 674-678; upstream `man/journalctl.xml:900-906`, "Added in version 195"):
   > “Print all possible data values the specified field can take in all entries of the journal.”

3. **The “cannot be combined” sentence — NOT in the man page.** It is the runtime rejection string from the v262 **source**, `src/journal/journalctl.c:958-960`:
   > “-F/--field= and -N/--fields cannot be combined with options that limit the journal.”

   Verified: `grep -c -i 'cannot be combined'` → **0** in `journalctl.1.arch.html`, **0** in `journalctl-v262.xml`; `grep -c -i 'limit the journal'` → **0** in both. The man page at systemd 262 documents what `-F`/`-N` *do* but does **not** document the restriction.

   The upstream **NEWS** at tag v262 states the same change in prose (`NEWS:129-133`, "CHANGES WITH 262", Feature Removals and Incompatible Changes):
   > “journalctl now rejects -F/--field together with filters such as unit, boot, time, cursor or grep filters.”

   NEWS at tag v261 does **not** contain that line → the change is v262-new (verified by grep on `NEWS_v261`: no hit).

## Live read-only verification on this host (secondary evidence, for the note's matrix)

Host: `journalctl --version` → `systemd 262 (262-1-arch)`; `pacman -Q systemd` → `systemd 262-1`. Rejection message goes to **stderr**, exit code **1**. Matrix in `live-matrix.txt` (this dir); script `/tmp/matrix.sh`.

Rejection triggered (exit 1) by: `-b0`, `-b-1`, `-S today`, `-U today`, `--since=-1h`, `--until=now`, `-u <unit>`, `-t <ident>`, `-p <prio>`, `--cursor=<s>`, `-g <pattern>` — for both `-F` and `-N`.
Not rejected (exit 0): no option, `-n 5`, `-f`, `-r`, `--directory=/tmp` (its own "No journal files were found." error).

The option set matches the v262 source predicate `field_list_has_scope_options()` (`src/journal/journalctl-filter.c:26-43`): boot filter, invocation id, dmesg, cursor/after-cursor/cursor-file, system & user units, syslog identifier & exclude identifier, priorities, facilities, since, until, pattern.

Note: `journalctl --list-fields` does **not** exist at systemd 262 (exit 1, “unrecognized option '--list-fields'”); the field-listing actions are `-N`/`--fields` and `-F`/`--field=`.

---

## The full SOURCES.md row (id S198)

> Row only — the L1 appends it to `corpus/SOURCES.md`; this seat does not edit production files.

```
| S198 | journalctl(1) at systemd 262 — https://man.archlinux.org/man/journalctl.1 (footer "systemd 262.1"); upstream twin https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml | docs | A | The -F/--field= and -N/--fields semantics and their limiting-option interaction at systemd 262 | journalctl(1) §COMMANDS, "-N, --fields" and "-F, --field=" entries (Arch HTML lines 653-662, .txt lines 669-678; upstream man/journalctl.xml lines 891-906); footer/foot-os "systemd 262.1", package core/systemd 262.1-1; SHA-256 aaae4efa61ff9c56e6249feb2f4527db57f1a4beb0eac4ad1eeb111a4bbb83c2 (Arch HTML), d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd (upstream v262 XML, identical to the v262.1 and main blobs at fetch time); snapshots .ufo/waves/round-36/w1/SrcJournalctlMan/journalctl.1.arch.html, .ufo/waves/round-36/w1/SrcJournalctlMan/journalctl-v262.xml | The man page documents that -N/--fields prints all field names in journal entries and -F/--field= prints all possible values of a field, and it carries no "cannot be combined" sentence at all: the restriction is a v262 runtime rejection whose exact string lives in src/journal/journalctl.c (v262) and whose prose announcement lives in NEWS (v262, CHANGES WITH 262); the man page therefore grounds -F/-N semantics but does not by itself evidence the limiting-option interaction, which must be cited from the source/NEWS or observed live | mined | 2026-10-23 | on-release | corpus/knowledge/journalctl-v262-field-filter-r36.md |
```

Field-by-field against the assignment spec:
- **id** `S198` (max existing id verified as `S197`)
- **kind** `docs`
- **tier** `A`
- **scope** the `-F`/`-N` semantics and limiting-option interaction at systemd 262
- **status** `mined`
- **opened** `2026-10-23`
- **recheck** `on-release`
- **used-by** the new note `corpus/knowledge/journalctl-v262-field-filter-r36.md` (file not yet present in the lane at this seat's write time — see findings)
