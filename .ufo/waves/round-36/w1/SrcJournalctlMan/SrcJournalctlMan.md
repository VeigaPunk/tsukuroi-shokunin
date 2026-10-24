# SrcJournalctlMan — source open S198 (journalctl(1) at systemd 262)

**Seat:** `tsukuroi-r36.SrcJournalctlMan` · round 36, attempt 1, wave w1 · lane repo `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
**Write scope:** `.ufo/waves/round-36/w1/SrcJournalctlMan/` only. No production file (`tools/`, `corpus/`, `SCORECARD.md`, `LOG.md`, `SKILL.md`, `corpus/SOURCES.md`) was edited. No git/jj mutating command was run.
**Heading time:** `02:49:56Z` (pasted from `date -u +%H:%M:%SZ` at write time; UTC date at that moment is 2026-10-24 — the assignment fixes the row's `opened` field at 2026-10-23, which is the local date of the round and is used verbatim in the row).

## Behavior delivered

Opened `journalctl(1)` at systemd 262, anchored the `-N/--fields` and `-F/--field=` texts, established where the "cannot be combined" sentence does and does **not** live, verified the rejection live and read-only on this host, and produced the full S198 registry row.

## Gates run (all read-only; no product file touched)

| # | Gate | Result |
|---|---|---|
| G1 | `grep -oE 'S[0-9]+' corpus/SOURCES.md \| sort -V \| tail -1` | `S197` → **S198 is the next free id** (no collision) |
| G2 | `grep -cE '^\| S[0-9]+' corpus/SOURCES.md` | `197` registry rows — consistent with G1 |
| G3 | `https://man.archlinux.org/man/journalctl.1` HTTP 200, 65136 bytes, footer `systemd 262.1` | **pass** — served the required systemd 262.x, so the Arch HTML is the source used |
| G4 | `https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml` HTTP 200, 61619 bytes | fetched as corroboration; **byte-identical** to v262.1 and to `main` at fetch time (same sha256) |
| G5 | `grep -c -i 'cannot be combined'` in Arch HTML and in v262 XML | **0 and 0** → the man page at 262 does **not** carry the rejection sentence |
| G6 | `grep -c -i 'limit the journal'` in both | **0 and 0** (same conclusion, second phrasing) |
| G7 | `grep -n 'cannot be combined' src/journal/journalctl.c` (v262) | line 960 — the exact string lives in the **source**, not the man page |
| G8 | Live `journalctl -F _SYSTEMD_UNIT -b0` | stderr `-F/--field= and -N/--fields cannot be combined with options that limit the journal.`, **exit 1** |
| G9 | Live matrix over 17 limiting/non-limiting options for `-F`, 5 for `-N` | recorded in `live-matrix.txt` |
| G10 | `grep 'journalctl now rejects -F' NEWS` at tag v262 → hit at line 129; at tag v261 → **no hit** | the rejection is **v262-new** |
| G11 | `journalctl --list-fields` | exit 1, “unrecognized option” — `--list-fields` does not exist at 262 |

## Touched surfaces

Only this seat directory:

- `SrcJournalctlMan.md` (this report)
- `s198-row.md` — the full S198 row + all fetch/quote evidence
- `journalctl.1.arch.html` — byte snapshot, sha256 `aaae4efa61ff9c56e6249feb2f4527db57f1a4beb0eac4ad1eeb111a4bbb83c2` (65136 bytes)
- `journalctl.1.arch.txt` — plain-text rendering of the same 262.1 page, sha256 `414c1f4755e73872e25c39eb3cf934a1643825d5ac95b2e35149fe39c43348c5` (50637 bytes)
- `journalctl-v262.xml` — upstream v262 man source, sha256 `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd` (61619 bytes)
- `snapshot-arch-html-653-663.txt` — byte snapshot of the `-N`/`-F` COMMANDS entries (Arch HTML lines 653-663)
- `snapshot-arch-txt-665-685.txt` — the same region in the .txt rendering
- `snapshot-arch-footer.txt` — Arch HTML lines 1090-1125 (`foot-os systemd 262.1`, package `core/systemd` 262.1-1)
- `snapshot-news-v262-129-133.txt` — NEWS v262 prose announcement
- `snapshot-src-v262-journalctl-c-955-962.txt` — the exact rejection site in `src/journal/journalctl.c`
- `snapshot-src-v262-journalctl-filter-c-26-45.txt` — `field_list_has_scope_options()`, the option predicate
- `live-matrix.txt` — the live read-only matrix with exit codes

## Out of scope (deliberately not done)

- Did **not** append the S198 row to `corpus/SOURCES.md` — production file; the L1 lands it from `s198-row.md`.
- Did **not** write `corpus/knowledge/journalctl-v262-field-filter-r36.md` — not this seat's scope; the row's `used-by` names it.
- Did **not** edit `SCORECARD.md`/`LOG.md`/`SKILL.md`, did not commit, push, tag, or touch the lane index.
- Did **not** install any tool: `curl`, `grep`, `sort`, `sha256sum`, `tar`, `pacman -Q`, `journalctl` and `python3` already present and sufficient.
- Did **not** dispatch a subagent (leaf seat).
- Did **not** write anywhere outside the seat directory plus `/tmp` scratch (`/tmp/matrix.sh`, `/tmp/jctl_arch.*`, `/tmp/journalctl_v262.xml`, `/tmp/NEWS_v262`, `/tmp/sd262/`, `/tmp/systemd-v262.tar.gz`).

## Findings

**F1 — the man page does not contain the "cannot be combined" sentence; the source does.** `grep -c -i 'cannot be combined'` = 0 in `journalctl.1.arch.html` and 0 in `man/journalctl.xml` at tag v262 (and at v262.1 and `main`, which are byte-identical blobs). The exact string is in `src/journal/journalctl.c:960` (v262), inside the guard

```c
if (IN_SET(arg_action, ACTION_LIST_FIELDS, ACTION_LIST_FIELD_NAMES) && field_list_has_scope_options())
        return log_error_errno(SYNTHETIC_ERRNO(EINVAL),
                               "-F/--field= and -N/--fields cannot be combined with options that limit the journal.");
```

**Consequence for C2's sourcing (important, and it does not change the claim):** the declaration names S198 as "journalctl(1) at systemd 262" and puts the exact rejection line in the C2 after-state. As a *docs* source, journalctl(1) at 262 anchors the `-F`/`-N` **semantics** but cannot by itself evidence the **limiting-option interaction**. The row's `teaches` cell in `s198-row.md` is written to say exactly that, so the registry does not overstate the man page. The exact-string evidence for the rejection must be cited to the v262 source (`src/journal/journalctl.c`) and/or the v262 NEWS entry, and the live observation below, not to journalctl(1).

**F2 — the rejection sentence is v262-new, per upstream NEWS.** `NEWS` at tag v262, "CHANGES WITH 262", lines 129-133: “journalctl now rejects -F/--field together with filters such as unit, boot, time, cursor or grep filters.” The same grep on `NEWS` at tag v261 returns nothing → new in v262. This corroborates S024's queued assertion and gives it a **pinnable** anchor (S024's own URL is the mutable `main` branch; the v262 tag is the pin). S024 remains `queued`; this seat did not change it.

**F3 — exit code is 1, on stderr.** Verified live: `journalctl -F _SYSTEMD_UNIT -b0` → stdout empty, stderr = the rejection line, exit **1**. The source uses `SYNTHETIC_ERRNO(EINVAL)`, so the errno is EINVAL while the process exit status is 1 — the C2 note should state "exit status 1" and may mention EINVAL as the internal errno.

**F4 — live limiting-option matrix (read-only, this host `systemd 262 (262-1-arch)`, `pacman -Q systemd` → `systemd 262-1`).** Rejected with exit 1 for both `-F` and `-N`: `-b0`, `-b-1`, `-S today`, `-U today`, `--since=-1h`, `--until=now`, `-u <unit>`, `-t <ident>`, `-p <prio>`, `--cursor=<s>`, `-g <pattern>`. **Not** rejected (exit 0): no option at all, `-n 5`, `-f`, `-r`; `--directory=/tmp` fails earlier and differently (“No journal files were found.”, exit 0 here). The rejected set matches the v262 predicate `field_list_has_scope_options()` exactly: boot filter, invocation id, dmesg, cursor / after-cursor / cursor-file, system units, user units, syslog identifier, exclude identifier, priorities, facilities, since, until, pattern. Full table in `live-matrix.txt`.

**F5 — `--list-fields` does not exist at systemd 262.** `journalctl --list-fields` → exit 1, “unrecognized option '--list-fields'”. The two field-listing actions at 262 are `-N`/`--fields` and `-F`/`--field=`. Any consumer guidance in the C2 note must not name `--list-fields` for a 262 host.

**F6 — the upstream v262 blob reproduces S188's recorded sha256.** `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd` is already recorded for S188's `man/journalctl.xml` at tag v262 (`corpus/SOURCES.md:194`); my fetch of the same URL reproduced it exactly, and the v262.1 and `main` blobs are byte-identical to it. So the upstream man source is a stable, already-mined artifact — the new S198 row adds the *Arch 262.1 rendered page* plus the `-F`/`-N` anchor, not a new upstream blob.

**F7 — dependency (recorded, not blocking).** The row's `used-by` target `corpus/knowledge/journalctl-v262-field-filter-r36.md` **does not exist yet** in the lane at this seat's write time (`test -f` → absent). The L1 must land that note (or retarget the row's `used-by`) for the registry to be self-consistent. S198's `status: mined` is honest regardless, since the mining happened here.

**F8 — no man-page sentence for the restriction, so the C2 note's "-F/-N and limiting options" wording must be anchored to source/NEWS/live, not to journalctl(1).** This is the same content as F1 but stated as an actionable instruction for the note author: cite `journalctl(1)` for what `-F`/`-N` do, and cite the v262 source + NEWS + the live run for the rejection.

## Honest limits of this seat's evidence

- The two man-page quotes and the byte snapshots are **observed** (fetched, hashed, line-located in this session).
- The rejection sentence as **runtime output** is **observed** (live, this host). Its presence in the v262 **source** is **observed** (fetched `journalctl.c`, line 960; sha256 `285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab`, and the same file extracted from the v262 tarball, sha256 `6aa77506c0644aa67f940a48e3d3a7368601f787e4f249139516d353f107bcab` for the tarball).
- The statement "the option set is exactly `field_list_has_scope_options()`" is an **[inf]** inference from reading the v262 predicate against the live matrix; the two lists agree on all 17 probed options, but the predicate was not exhaustively probed live (e.g. `--exclude-identifier`, `--facility`, `-u` on the *user* journal, `--invocation-id` were not individually exercised — several are in the predicate list, and `-t`/`-p`/`-g`/`-b`/`-S`/`-U`/`--cursor`/`-u` were).
- The `main`-branch blob was byte-identical to v262 **at fetch time only**; `main` is mutable and must not be cited as pinned.
- Host journalctl is the **packaged** 262.1-1 build, not upstream v262 as built by upstream CI; the observed stderr string matches the upstream source string exactly, so the packaged build carries the same guard.

## Artifact paths (all under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/SrcJournalctlMan/`)

```
SrcJournalctlMan.md                          this report
s198-row.md                                  the full S198 row + fetch/quote evidence
journalctl.1.arch.html                       byte snapshot (sha256 aaae4efa…83c2)
journalctl.1.arch.txt                        byte snapshot (sha256 414c1f47…48c5)
journalctl-v262.xml                          byte snapshot (sha256 d54bbede…bdd)
snapshot-arch-html-653-663.txt               -N/-F COMMANDS entries, Arch HTML
snapshot-arch-txt-665-685.txt                -N/-F COMMANDS entries, .txt
snapshot-arch-footer.txt                     footer: foot-os systemd 262.1, core/systemd 262.1-1
snapshot-news-v262-129-133.txt               NEWS v262 prose announcement
snapshot-src-v262-journalctl-c-955-962.txt   the exact rejection site in upstream source
snapshot-src-v262-journalctl-filter-c-26-45.txt   field_list_has_scope_options() predicate
live-matrix.txt                              live read-only option matrix with exit codes
```
