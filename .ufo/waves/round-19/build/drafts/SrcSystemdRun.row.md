# SOURCES row draft — systemd-run(1) transient unit naming and collection

Provisional id: **S066** (next free id in `corpus/SOURCES.md`, which ends at S065; L1 reassigns if
another round-19 row claims it first). kind `docs`, tier `A`.

## Row (append to the registry table)

| S066 | systemd-run(1) — https://man.archlinux.org/man/systemd-run.1 | docs | A | The `--unit=` naming of a transient `.service` unit and the `--collect` unloading semantics used by the snapper plugin's detached sync invocation; not evidence that any particular transient unit ran or wrote `/boot` | § DESCRIPTION first paragraph; § OPTIONS > `--unit=`, `-u`; § OPTIONS > `-G`, `--collect`; systemd 262 (installed page `.TH "SYSTEMD-RUN" "1" "" "systemd 262"`). man.archlinux.org returned ECONNRESET on four request forms this session; text verified at pinned https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-run.xml:64-65,130-131,545 and in `/usr/share/man/man1/systemd-run.1.gz` | `--unit=` makes systemd-run create the transient unit under the given name instead of an automatically generated one; `--collect` unloads that unit after it completes even if it failed, so a finished transient unit is expected absent from later unit listings | mined | 2026-10-20 | on-release | corpus/knowledge/boot-writers-r19.md (drafted by ScribeWritersEntry) |

## Required quote(s)

The item asked for one exact <=25-word quote showing systemd-run creates a transient service unit
with the given name. The man page splits the two halves across sections, so both exact sentences
are recorded rather than a spliced non-quote.

1. Creation (21 words) — § DESCRIPTION, XML lines 64-65:
   > systemd-run may be used to create and start a transient .service or .scope unit and run the specified COMMAND in it.
2. Naming (10 words) — § OPTIONS > `--unit=`, `-u`, XML lines 130-131:
   > Use this unit name instead of an automatically generated one.
3. Collection (11 words) — § OPTIONS > `-G`, `--collect`, XML line 545:
   > Unload the transient unit after it completed, even if it failed.

Quotes are the rendered plain-text sentences (roff uses line breaks and `\&.service` escapes;
bold/italic markers removed). `--unit=` and `--collect` are both documented as added in version 206
and 236 respectively (XML 133 and 562).

## Version and access record

- Intended source: `https://man.archlinux.org/man/systemd-run.1` (named by the item).
- Attempted and failed with `ECONNRESET` this session: `systemd-run.1`, `systemd-run.1.en`,
  `systemd-run.1.txt`, `extra/systemd/systemd-run.1.en`, `systemd-run.1/` (five forms, no body
  returned). This is a transport failure, not a 404, and is not treated as absence.
- Verified instead, word for word, at the pinned upstream tag `v262`:
  `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-run.xml:64-65,130-131,545`
  (fetched, text/plain) and the installed man page `/usr/share/man/man1/systemd-run.1.gz`
  (`.TH "SYSTEMD-RUN" "1" "" "systemd 262"`). Also read the freedesktop `latest` render
  (`https://www.freedesktop.org/software/systemd/man/latest/systemd-run.html`, header
  `systemd 262`), which carries the same three sentences.
- Version recorded: **systemd 262** (v262 tag and installed page). The Arch render's own footer
  string was not observed, so it is not claimed.

## C2 relevance (author note, not part of the registry row)

- `host-capture-r19b.txt:1184-1188` shows the snapper plugin invoking
  `systemd-run --unit="limine-snapper-${op}-${SNAP_ID}-$$" ... --quiet --collect`.
- `host-capture-r19c.txt:14-15` shows journal `_SYSTEMD_UNIT` values
  `limine-snapper-add-1-5846.service` and `limine-snapper-add-2-260668.service`, matching the
  plugin's `${op}-${SNAP_ID}-$$` pattern (op `add`, SNAP_ID 1 and 2, PIDs 5846 and 5846/260668).
- [inf] `--collect` means a finished transient unit is unloaded after completion, so such a unit
  may be absent from later unit listings even though its journal records remain. This row supplies the
  naming/collection mechanism only; it does not by itself prove the writer or that a write occurred.
