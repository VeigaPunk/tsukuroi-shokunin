# S024 — proposed `corpus/SOURCES.md` row (round 36, seat SrcSystemdNews)

Written 2026-10-23. Production files are **not** edited by this seat; the L1 lands this row.

## 1. What the pin changes

The base row (SOURCES.md:30) points at the **mutable** `main` branch and carries
`status | queued | ... | used-by | —`. Round 36 re-opens S024 **pinned to the systemd
`v262` tag** and mines it. The v262 tag is the release this host runs
(`journalctl --version` first line: `systemd 262 (262-1-arch)`; `pacman -Q systemd` →
`systemd 262-1`), so the pinned bytes are the ones the host's behavior derives from.

## 2. Fetch evidence (v262 tag)

| item | value |
|---|---|
| URL | `https://raw.githubusercontent.com/systemd/systemd/v262/NEWS` |
| sha256 of fetched bytes | `a494f0389edd09702a90d1540c7e21c0af5a4d29a4d020855ca3062d885a7657` |
| size | 1271752 bytes |
| git blob sha (via contents API, `ref=v262`) | `1329d035c6ea83a2cd74071e20adaec9ce346049` |
| annotated tag object | `1f7dffaf714cc4488159c498b7a17cf34c5a96d5` (`refs/tags/v262`) |
| tag → commit | `8cc40e0c5e9234bf45084751ac53b1fbfe70b492` (tagger Luca Boccassi, 2026-09-22T13:12:43Z) |
| byte snapshot (entry) | `.ufo/waves/round-36/w1/SrcSystemdNews/news-v262-excerpt.txt`, sha256 `06e902b652cdc496ec22ec6b0b5468cb079dccc1631efb55ca9eb40ee3ea312a` |
| full pinned copy | `.ufo/waves/round-36/w1/SrcSystemdNews/NEWS-v262.full` (same sha256 as fetched bytes) |

## 3. Located quote (≤25 words) and its location

> "journalctl now rejects -F/--field together with filters such as unit, boot, time, cursor or grep filters."

* Section: `CHANGES WITH 262:` (line 3) → subsection **`Feature Removals and Incompatible Changes:`** (line 26).
* Entry lines **129–133** of the v262 NEWS file; byte range **[7492, 7869)** (377 bytes).
* Entry start offset in file: 7492; file length 1271752.

The exact runtime rejection line asserted by the round-36 declaration is
`"-F/--field= and -N/--fields cannot be combined with options that limit the journal."`
That string is **not** in NEWS — it is the error text journalctl prints (see §5). NEWS
carries the prose statement of the change; the error signature comes from
`src/journal/journalctl.c` at v262 (line 960).

## 4. Discrepancy check against `main` (recorded because the base row is a `main` row)

The v262 tag **does** contain the entry — no discrepancy in substance. `main` was fetched
anyway for completeness:

| file | sha256 | size | entry at | section |
|---|---|---|---|---|
| `v262/NEWS` | `a494f038…a7657` | 1271752 | line 129 | `CHANGES WITH 262:` (line 3) |
| `main/NEWS` | `b9e7a6a2…04352` | 1281401 | line 306 | `CHANGES WITH 262:` (line 180); `main` opens with `CHANGES WITH 263 in spe:` (line 3) |

`main` blob sha `8978e23dace89367e3638e04ce52323f3e1b62c3` at commit
`0f0682b773b15ff350057a80763cd39d71d71f30` (2026-10-23T22:22:11Z). The `main` copy is
byte-different (it has the extra 263 section) — this is why the row is re-pinned rather
than left on `main`. The prose bullet is identical in both.

## 5. Supporting bytes for the note (secondary, same tag)

| artifact | sha256 | what it supports |
|---|---|---|
| `src/journal/journalctl.c` @ v262 | `285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab` | line 960: the exact rejection string; lines 958–959: the guard `IN_SET(arg_action, ACTION_LIST_FIELDS, ACTION_LIST_FIELD_NAMES) && field_list_has_scope_options()`; `SYNTHETIC_ERRNO(EINVAL)` → exit 1 |
| `src/journal/journalctl-filter.c` @ v262 | `480f7a03040c0ddc93b1b65c0b49d6f0e8a4a377ee1b94168655132dcfd72f48` | lines 26–43: `field_list_has_scope_options()` — the exact set of limiting options |
| `man/journalctl.xml` @ v262 | `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd` | lines 890–905: `-N/--fields` (added v229) and `-F/--field=` (added v195) — the man page does **not** document the 262 restriction |
| local `/usr/share/man/man1/journalctl.1.gz` (decompressed) | `1e737294f62ab090d9927f2c7b81c5b43216a841af0ae197dc599bb4bd62b54d` | footer `.TH "JOURNALCTL" "1" "" "systemd 262" "journalctl"` — the on-host man page is the systemd 262 one |

## 6. Proposed row (all 11 cells of the `## Registry` table)

Registry header (SOURCES.md:5) is
`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`.

Proposed replacement for SOURCES.md:30 (single line, pipe-delimited):

```
| S024 | systemd NEWS at the v262 tag — https://raw.githubusercontent.com/systemd/systemd/v262/NEWS | docs | A | systemd 258-262 changes relevant to boot recovery and journal tooling, pinned to the release this host runs (systemd 262-1) | CHANGES WITH 258 through CHANGES WITH 262 at tag v262 (annotated tag object 1f7dffaf714cc4488159c498b7a17cf34c5a96d5 → commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492); the journalctl -F/-N entry is lines 129-133 under "CHANGES WITH 262:" > "Feature Removals and Incompatible Changes:" (line 26), byte range [7492, 7869); raw bytes SHA-256 a494f0389edd09702a90d1540c7e21c0af5a4d29a4d020855ca3062d885a7657 (1271752 bytes); NEWS blob sha 1329d035c6ea83a2cd74071e20adaec9ce346049; snapshot .ufo/waves/round-36/w1/SrcSystemdNews/NEWS-v262.full; fetched 2026-10-23. The earlier mutable-main anchor is superseded: main now opens with "CHANGES WITH 263 in spe:" (sha256 b9e7a6a2...) and carries the same bullet at line 306 | NEWS documents versioned behavior changes including v258 boot breakpoints and the v262 rejection of journalctl -F/--field together with filters such as unit, boot, time, cursor or grep filters, because field listing used sd_journal_query_unique() and silently ignored those filters; the shipped error signature and exit code are not stated in NEWS and come from the v262 source (src/journal/journalctl.c:960, EINVAL → exit 1) | mined | 2026-10-19 | on-release | corpus/knowledge/journalctl-v262-field-filter-r36.md |
```

### Cell-by-cell deltas from the base row

| cell | base (SOURCES.md:30) | proposed | why |
|---|---|---|---|
| id | `S024` | `S024` (unchanged) | re-open of the same source, not a new row |
| source | `systemd NEWS — https://raw.githubusercontent.com/systemd/systemd/main/NEWS` | `systemd NEWS at the v262 tag — https://raw.githubusercontent.com/systemd/systemd/v262/NEWS` | the base is a mutable branch; the claim is about the release the host runs |
| kind | `docs` | `docs` | unchanged |
| tier | `A` | `A` | unchanged (upstream project source) |
| scope | `systemd 258-262 changes relevant to boot recovery and journal tooling` | `…, pinned to the release this host runs (systemd 262-1)` | scope now names the pin |
| anchor | `CHANGES WITH 258 through CHANGES WITH 262; main branch fetched 2026-10-19 (mutable: main now opens with CHANGES WITH 263 in spe; no commit pin claimed)` | tag object + commit + blob + entry lines/bytes + sha256 + snapshot path + fetch date + explicit supersession note of the mutable-main anchor | the base anchor is self-declared unpinned; the round-36 note needs a reproducible anchor |
| teaches | `NEWS documents versioned behavior changes including v258 boot breakpoints and the v262 rejection of journalctl -F combined with filters` | the same, expanded with the reason (sd_journal_query_unique() cannot represent the filters) and with the explicit statement that the error signature/exit code come from the v262 source, not NEWS | keeps NEWS-scoped teaching separate from source-scoped facts |
| status | `queued` | `mined` | the entry is now located, pinned and quoted |
| opened | `2026-10-19` | `2026-10-19` (unchanged — first-open date; re-open is 2026-10-23) | the row was first opened 2026-10-19; changing it would lose the original open |
| recheck | `on-release` | `on-release` | unchanged |
| used-by | `—` | `corpus/knowledge/journalctl-v262-field-filter-r36.md` | the round-36 C2 note is the consumer |

### Anchor naming the v262 tag — the literal form used

`v262` (annotated tag `1f7dffaf714cc4488159c498b7a17cf34c5a96d5` → commit
`8cc40e0c5e9234bf45084751ac53b1fbfe70b492`), raw bytes sha256
`a494f0389edd09702a90d1540c7e21c0af5a4d29a4d020855ca3062d885a7657`.

### used-by naming the note — the literal form used

`corpus/knowledge/journalctl-v262-field-filter-r36.md`

## 7. Prior-state check for the counting command named in the declaration

```
$ grep -rl "cannot be combined with options that limit the journal" corpus/knowledge/ SKILL.md
(no output; exit 1)
```

Confirmed at the base commit `6d76fb20f6ecbc940e5c8fff36c74060c885e161` working tree:
no lane entry documents the rejection line yet. (Note: the round-36 knowledge note file
does not exist in the tree at this seat's write time — the L1 lands it from another seat's
output. This seat does not create it.)

## 8. Dependency note (not blocking)

The declaration names **S198** (journalctl(1) at systemd 262) as the second C2 source row.
S198's row content is not this seat's deliverable, but the evidence it needs is in this
seat's directory and is quoted in §5 above: the local systemd 262 man page
(`.TH "JOURNALCTL" "1" "" "systemd 262"`), `man/journalctl.xml` @ v262 (sha256
`d54bbede…`), and the upstream `https://man.archlinux.org/man/journalctl.1` copy
(sha256 `aaae4efa61ff9c56e6249feb2f4527db57f1a4beb0eac4ad1eeb111a4bbb83c2`, HTML; its
`-N`/`-F` text says "Added in version 229"/"Added in version 195" and does **not** mention
the 262 restriction).
