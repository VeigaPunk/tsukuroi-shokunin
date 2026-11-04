# Source disposition Gate — Round 78

Axes: depth and operability. Opened by ScribeSources on **2026-11-04** using the read tool against both exact upstream URLs below; source bodies were returned. No package adoption, installation, promotion or host-state inference.

## S327 — admit as mined, code, tier A

URL: https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c

Located passage: `manager_determine_path_usage`, lines 91–135. Located excerpts below total fewer than 25 whitespace-delimited words:

- 119–120: `if (!endswith(de->d_name, ".journal") && !endswith(de->d_name, ".journal~"))`
- 123: `fstatat(dirfd(d), de->d_name, &st, AT_SYMLINK_NOFOLLOW)`
- 128: `if (!S_ISREG(st.st_mode))`
- 131: `*ret_used += (uint64_t) st.st_blocks * 512UL;`

The adjacent continues at 121, 125 and 129 exclude other suffixes, failed stats and nonregular entries. A symlink's own metadata is examined, not its target's, so a journal-suffixed symlink fails the regular-file predicate. Included files contribute allocated blocks times 512, not st_size; line 114 separately derives filesystem availability from f_bsize times f_bavail. The allocation sum is the support needed for U1–U6; no claim that this finite set covers every filesystem behavior or the installed Arch build.

Used-by: `corpus/knowledge/journald-path-usage-r78.md` and `corpus/lessons/round-78.md`. Recheck: on-release.

## S328 — reject for the scoped implementation claim, docs, tier A

URL: https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml

Located passage: --disk-usage entry, lines 941–948; prose at 944–945. Quote (16 words):

> This shows the sum of the disk usage of all archived and active journal files.

The manual supports broad disk-usage meaning, including active and archived journal files, but cannot by itself prove manager implementation. This located option description does not specify the suffix filter, no-follow stat, failed-stat handling or regular-file test. This is a scoped rejection, not a claim that the manual is false or that no other passage could exist.

Flip condition: reopen a located passage explicitly naming the `.journal`/`.journal~` suffix, `AT_SYMLINK_NOFOLLOW`, failed-stat skipping and `S_ISREG` predicates. S327 supplies implementation support now; the manual's general wording does not substitute for it.

Used-by: `corpus/lessons/round-78.md`. Recheck: on-release.

## Provenance and integration limits

`before/expected.json` supplied the inherited v262 SHA256 pins: manager `428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2`; manual `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd`. This seat reopened source text but did not independently hash downloaded bytes or retain full raw snapshots. Do not describe those pins as this seat's checksum execution evidence.

The live `corpus/SOURCES.md:338-339` already contained S327 and S328 when read. `rows.json` is an integration draft, not evidence of additions by this seat; do not append duplicate IDs. All existing registry rows remain untouched by this seat. L1 owns integration and any required canonical checks.
