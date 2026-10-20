# SrcEntryToolUpstream — C2 SOURCES row draft

Assigned by: SrcEntryToolUpstream (C2 web source). No registry write; integrator
(ScribeSourcesOwn) assigns the concrete id. Placeholder `S0NN`; next free id at
baseline 452a0546 is **S066** (`corpus/SOURCES.md` ends at S065,
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md:72`).

## Row (11-column contract)

| S0NN | limine-entry-tool 1.40.0 README — https://gitlab.com/Zesko/limine-entry-tool/-/raw/1.40.0/README.md | docs | A | Upstream statements that Arch dracut/mkinitcpio hook packages manage kernel installation and removal through limine-entry-tool, and that limine.conf is the entry file the tool rewrites and backs up; not the installed hook/script contents and not any specific host transaction | Tag 1.40.0 (tags list https://gitlab.com/Zesko/limine-entry-tool/-/tags, dated 2026-09-27T11:19:52+02:00); `### Arch Linux` line 258, `## Description` line 17, `### Post-hooks` line 552, `## Installation` line 225; accessed 2026-10-20 | The Arch hook packages provide hooks that automatically manage kernel installation and removal using `limine-entry-tool`; the tool generates entries only at `$ESP_PATH/limine.conf`, backs it up before saving, and its post-hooks run after kernel management and limine.conf updates | mined | 2026-10-20 | on-release | corpus/lessons/round-19.md |

## Provenance for the round-19 lesson `## Gate` table

- **url_opened**: https://gitlab.com/Zesko/limine-entry-tool/-/raw/1.40.0/README.md
- **tags_list**: https://gitlab.com/Zesko/limine-entry-tool/-/tags
- **tag**: `1.40.0`, tag date `2026-09-27T11:19:52+02:00`
- **heading**: `### Arch Linux` (README line 250)
- **quote**:
  > These packages provide hooks to automatically manage kernel installation and removal using `limine-entry-tool`.
- **quote_line**: 258
- **quote_words**: 13 (whitespace-token count; <=25)
- **revision pin**: tag, not branch; raw tag URL reproduces the quote. Body sha256 not computed by this NO-EXEC seat.

### Supporting quotes from the same tag (anchor only)

- line 17, under `## Description`:
  > It generates, updates, and removes boot entries with periodic `limine.conf` backups. (12 words)
- line 225, under `## Installation`:
  > This tool generates boot entries only at `$ESP_PATH/limine.conf` and does not touch any other Limine config locations. (17 words)
- line 552, under `### Post-hooks`:
  > Executable files in `/etc/boot/hooks/post.d/` are executed **after** kernel management and `limine.conf` updates. (12 words)
- line 598, under `### Integrity`:
  > Automatic Limine configuration checksum updates and enrollment into the Limine binary after kernel management (15 words)

## Installed-version corroboration

`limine-mkinitcpio-hook-1.40.0-2` is the installed package
(`.ufo/waves/round-19/l1-capture/host-capture-r19.txt:10`), its `%VERSION%` is
`1.40.0-2` and its `%URL%` is `https://gitlab.com/Zesko/limine-entry-tool`
(`host-capture-r19.txt:147-151`). The installed README
(`/usr/share/doc/limine-entry-tool/README.md`) shows the same heading line numbers
(`## Description` 14, `## Requirements` 212, `## Installation` 221, `### Arch Linux`
250, `## Configuration` 341) in `host-capture-r19b.txt:1513-1596`, consistent with
the tag body.

## Limits (must survive integration)

- The README never uses the phrase "pacman transaction"; its transaction link is
  indirect: the two AUR packages are pacman packages whose hooks call
  `limine-entry-tool` on kernel install/removal (line 258), and post-hooks run after
  "kernel management and `limine.conf` updates" (line 552).
- The hook file that performs a specific `/boot/limine.conf` write is host evidence,
  not this README: `/usr/share/libalpm/hooks/90-limine-mkinitcpio-install` via
  `/etc/pacman.d/hooks/90-mkinitcpio-install.hook` (`host-capture-r19.txt:346-409`).
  Keep that attribution in C2's host rows, not in this row's `teaches`.
- `used-by` `corpus/lessons/round-19.md` does not exist until the round lesson lands;
  the integrator must land it (or repoint) before the SOURCES used-by census.
