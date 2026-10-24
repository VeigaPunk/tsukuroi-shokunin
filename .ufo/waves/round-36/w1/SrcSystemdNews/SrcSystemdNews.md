# SrcSystemdNews — round 36, wave w1 — source open S024 (systemd NEWS, pinned)

Seat: `tsukuroi-r36.SrcSystemdNews` · lane repo: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
· base/declaration commit read: `6d76fb20f6ecbc940e5c8fff36c74060c885e161` · working tree HEAD at
write time: `189d8a080ba8d508d5faab12cad9e688aee91dab` (round-36 wave-1 spec commit).
Report written 2026-10-23; headings carry a `date -u +%H:%M:%SZ` stamp pasted at write time.

**Outcome in one line: the v262 tag DOES contain the journalctl `-F`/`-N` rejection entry; the
pin, the quote, the byte snapshot and a full 11-cell S024 row proposal are recorded below —
but the declaration's "exact rejection line" is NOT in NEWS, it lives in the v262 source and in
the shipped binary, and that divergence is reported as a finding.**

---

## 1. What was done

| step | command | outcome |
|---|---|---|
| read the declaration | `git -C … show 6d76fb20…:SCORECARD.md \| tail -90` | claim C2 text, counter/freeze/kill rules and the S024+S198 sourcing requirement read |
| host journalctl version | `journalctl --version \| head -1` | `systemd 262 (262-1-arch)` (see §2) |
| fetch the pinned source | `curl -sSL -o /tmp/NEWS-v262 https://raw.githubusercontent.com/systemd/systemd/v262/NEWS` | 1271752 bytes, sha256 `a494f038…a7657` |
| locate the entry | `grep -n "journalctl now rejects" /tmp/NEWS-v262` | line **129**; section `CHANGES WITH 262:` (line 3) → `Feature Removals and Incompatible Changes:` (line 26); entry lines 129–133 |
| byte snapshot | python slice of the fetched bytes | `news-v262-excerpt.txt`, sha256 `06e902b6…a312a`, byte range **[7492, 7869)** |
| discrepancy check | fetched `main/NEWS` too | entry present there as well (line 306); bytes differ; no substantive discrepancy — details in §5 |
| live host verification | `journalctl -F/-N` with each limiting option (read-only) | 19-row matrix in `live-flag-matrix.txt`; error string + exit 1 confirmed |
| source-level confirmation | fetched `src/journal/journalctl.c` and `src/journal/journalctl-filter.c` @ v262 | exact error string at `journalctl.c:960`; the limiting-option predicate at `journalctl-filter.c:26-43` |
| prior-state check | `grep -rl "cannot be combined with options that limit the journal" corpus/knowledge/ SKILL.md` | **no output** (exit 1) at the base tree — the C2 prior state holds |

No pacman transaction was run (host-wide pacman pause, orchestrator ruling 2026-10-20).
No tool was installed or upgraded: `curl`, `python3`, `grep`, `git` and `journalctl` were
already present and sufficient.

## 2. `journalctl --version` first line (verbatim)

```
systemd 262 (262-1-arch)
```

`pacman -Q systemd` → `systemd 262-1`; `pacman -Qo /usr/bin/journalctl` →
`/usr/bin/journalctl is owned by systemd 262-1`.
So the pinned `v262` tag is the release this host runs — the pin is not arbitrary.

## 3. Fetched bytes

**v262 tag (the pin):**

```
https://raw.githubusercontent.com/systemd/systemd/v262/NEWS
sha256  a494f0389edd09702a90d1540c7e21c0af5a4d29a4d020855ca3062d885a7657
size    1271752 bytes
blob    1329d035c6ea83a2cd74071e20adaec9ce346049   (contents API, ref=v262)
tag     refs/tags/v262 = 1f7dffaf714cc4488159c498b7a17cf34c5a96d5 (annotated tag object)
commit  8cc40e0c5e9234bf45084751ac53b1fbfe70b492  (tagger: Luca Boccassi, 2026-09-22T13:12:43Z)
```

Snapshot copied into the seat directory: `NEWS-v262.full` (identical sha256 to the fetched
bytes), `news-v262-excerpt.txt` (the entry with surrounding context),
`news-v262-header.txt` (file head through `CHANGES WITH 262:`), `entry-v262.txt` (the 5 entry
lines alone).

## 4. Located quote (≤25 words) + location

> "journalctl now rejects -F/--field together with filters such as unit, boot, time, cursor or grep filters."

* Section: `CHANGES WITH 262:` (line 3) → **`Feature Removals and Incompatible Changes:`** (line 26).
* Lines **129–133**; byte range **[7492, 7869)** (377 bytes); file length 1271752.
* Continuation (same bullet): "Previously field listing used sd_journal_query_unique(), which
  cannot represent those filters, so the filters were silently ignored. Scripts relying on
  filtered field lists should be adjusted to query entries explicitly."

### Byte snapshot around the entry (`news-v262-excerpt.txt`, verbatim excerpt)

```
          recreated.

        * sd-event rate-limit timers, and thus manager timers such as
          StartLimitIntervalSec=, now use CLOCK_BOOTTIME instead of
          CLOCK_MONOTONIC. Time spent suspended therefore counts toward
          rate-limit expiry. After upgrade/reexecution, already-serialized
          rate-limit state from older managers may expire once earlier than it
          would have previously, because the stored timestamp is compared
          against the new clock base.

        * journalctl now rejects -F/--field together with filters such as
          unit, boot, time, cursor or grep filters. Previously field listing
          used sd_journal_query_unique(), which cannot represent those filters,
          so the filters were silently ignored. Scripts relying on filtered
          field lists should be adjusted to query entries explicitly.

        * The systemd-sysupdate binary has been moved back from bindir to
          libexecdir, as more breaking changes are forthcoming and it is thus
          again marked as experimental. It will be stabilized in a future
          release. The libexecdir path is the most compatible way to call it.
```

## 5. Discrepancy check — honest record

**The v262 tag's NEWS *does* carry the entry.** There is no "entry missing from v262"
discrepancy. The `main` branch was fetched anyway for completeness, and the differences are
recorded rather than glossed:

| file | sha256 | size | entry at | section head |
|---|---|---|---|---|
| `v262/NEWS` | `a494f0389edd09702a90d1540c7e21c0af5a4d29a4d020855ca3062d885a7657` | 1271752 | line 129 | `CHANGES WITH 262:` line 3 |
| `main/NEWS` | `b9e7a6a2314355be2d9a7d75f10ad40f1c4eb7c4fbad2a6e8fe245188a404352` | 1281401 | line 306 | `CHANGES WITH 262:` line 180 (main opens with `CHANGES WITH 263 in spe:` line 3) |
| `main` at round-1's claimed pin `a923ab5ed1481512be6fb52aaa5086d0fef6878f` | `fab017059d7cbcd05b6cdcfa8f65c31a034e53ee79b6e96fa6a1694c3341b78a` | — | line 265 | `CHANGES WITH 262:` line 139 |

The prose bullet is byte-identical across all three copies. The only differences are the
surrounding section offsets caused by the added `CHANGES WITH 263 in spe:` block on `main`.
`main` blob sha `8978e23dace89367e3638e04ce52323f3e1b62c3` at commit
`0f0682b773b15ff350057a80763cd39d71d71f30` (2026-10-23T22:22:11Z).

**Which bytes support the note:** the pinned `v262` NEWS lines 129–133 support the *prose
statement of the change*. The **exact rejection line and the exit code named in the round-36
declaration are not in NEWS at all** — they come from the v262 source and from the shipped
binary:

* `src/journal/journalctl.c` @ v262 (sha256 `285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab`),
  lines 958–960:
  ```c
  if (IN_SET(arg_action, ACTION_LIST_FIELDS, ACTION_LIST_FIELD_NAMES) && field_list_has_scope_options())
          return log_error_errno(SYNTHETIC_ERRNO(EINVAL),
                                 "-F/--field= and -N/--fields cannot be combined with options that limit the journal.");
  ```
* `src/journal/journalctl-filter.c` @ v262 (sha256 `480f7a03040c0ddc93b1b65c0b49d6f0e8a4a377ee1b94168655132dcfd72f48`),
  lines 26–43 — the predicate itself:
  ```c
  bool field_list_has_scope_options(void) {
          return
                  arg_boot_filter ||
                  arg_invocation ||
                  arg_dmesg ||
                  arg_cursor ||
                  arg_after_cursor ||
                  arg_cursor_file ||
                  !strv_isempty(arg_system_units) ||
                  !strv_isempty(arg_user_units) ||
                  !strv_isempty(arg_syslog_identifier) ||
                  !strv_isempty(arg_exclude_identifier) ||
                  arg_priorities != 0 ||
                  !set_isempty(arg_facilities) ||
                  arg_since_set ||
                  arg_until_set ||
                  arg_pattern;
  }
  ```
* The shipped binary contains the string verbatim:
  `strings /usr/bin/journalctl | grep "cannot be combined"` →
  `-F/--field= and -N/--fields cannot be combined with options that limit the journal.`

## 6. Live host verification (read-only)

`journalctl --version` → `systemd 262 (262-1-arch)`. Every invocation below is a read-only
query; none writes to the journal.

* `-F _SYSTEMD_UNIT` alone → **exit 0**, field values printed.
* `-N` alone → **exit 0**, field names printed.
* Every limiting option combined with `-F`/`-N` → **exit 1**, stderr:
  `-F/--field= and -N/--fields cannot be combined with options that limit the journal.`

Full 19-row matrix in `live-flag-matrix.txt`. Summary:

| option | rc | stderr |
|---|---|---|
| `-F _SYSTEMD_UNIT` | 0 | — |
| `-N` | 0 | — |
| `-F … -u sshd.service` | 1 | rejection line |
| `-F … --user-unit=sshd.service` | 1 | rejection line |
| `-F … -b` / `-b0` | 1 | rejection line |
| `-F … --since=-1h` / `--until=-1h` | 1 | rejection line |
| `-F … --grep=foo` | 1 | rejection line |
| `-F … --cursor=x` / `--after-cursor=x` | 1 | rejection line |
| `-F … -p err` | 1 | rejection line |
| `-F … -t sshd` / `--identifier=sshd` | 1 | rejection line |
| `-F … -T sshd` (`--exclude-identifier`) | 1 | rejection line |
| `-F … --facility=daemon` | 1 | rejection line |
| `-F … -k` / `--dmesg` | 1 | rejection line |
| `-N -u sshd.service` | 1 | rejection line |
| `-F … -f` (follow) | 0 | — (follow is **not** in the predicate) |
| `-F … --merge`, `-F … --show-cursor` | 0 | — (not in the predicate) |

The observed matrix matches `field_list_has_scope_options()` exactly: `-f/--follow`,
`--merge` and `--show-cursor` are *not* limiting options and therefore do not trigger the
rejection. Exit code is 1 (the CLI's generic `EINVAL` failure path), **not** a
`log_error_errno` errno number.

## 7. Proposed S024 row — 11 cells, complete

Full text, cell-by-cell deltas and the literal anchor/used-by forms are in
**`s024-row.md`** (same directory). Summary of the proposed row:

* **id** `S024` (unchanged — a re-open, not a new row)
* **source** `systemd NEWS at the v262 tag — https://raw.githubusercontent.com/systemd/systemd/v262/NEWS`
  (was: the mutable `main` branch)
* **kind** `docs` · **tier** `A` (unchanged)
* **scope** `systemd 258-262 changes relevant to boot recovery and journal tooling, pinned to the release this host runs (systemd 262-1)`
* **anchor** names the v262 tag: `v262` (annotated tag `1f7dffaf…a96d5` → commit `8cc40e0c…b492`), raw bytes sha256 `a494f038…a7657` (1271752 bytes), NEWS blob sha `1329d035…6049`, entry lines 129–133 under `CHANGES WITH 262:` > `Feature Removals and Incompatible Changes:` (line 26), byte range [7492, 7869), snapshot path, fetch date, and an explicit supersession note for the old mutable-main anchor
* **teaches** the v262 prose bullet and its reason (`sd_journal_query_unique()` cannot represent those filters), and states explicitly that the error signature and exit code are **not** in NEWS and come from the v262 source
* **status** `queued` → **`mined`**
* **opened** `2026-10-19` (unchanged — the original first-open date; the re-open is 2026-10-23 and is recorded in the anchor)
* **recheck** `on-release` (unchanged)
* **used-by** `corpus/knowledge/journalctl-v262-field-filter-r36.md`

## 8. Files written (all inside the seat directory; nothing else touched)

| file | what it is |
|---|---|
| `.ufo/waves/round-36/w1/SrcSystemdNews/SrcSystemdNews.md` | this report |
| `.ufo/waves/round-36/w1/SrcSystemdNews/s024-row.md` | the proposed 11-cell S024 row, cell-by-cell deltas, anchor and used-by literal forms |
| `.ufo/waves/round-36/w1/SrcSystemdNews/NEWS-v262.full` | full pinned NEWS bytes (sha256 `a494f038…a7657`) |
| `.ufo/waves/round-36/w1/SrcSystemdNews/news-v262-excerpt.txt` | byte snapshot around the entry (sha256 `06e902b6…a312a`) |
| `.ufo/waves/round-36/w1/SrcSystemdNews/news-v262-header.txt` | file head through `CHANGES WITH 262:` |
| `.ufo/waves/round-36/w1/SrcSystemdNews/entry-v262.txt` | the 5 entry lines alone |
| `.ufo/waves/round-36/w1/SrcSystemdNews/journalctl.v262.c` | `src/journal/journalctl.c` @ v262 (sha256 `285b3d0c…0ab`) |
| `.ufo/waves/round-36/w1/SrcSystemdNews/journalctl-filter.v262.c` | `src/journal/journalctl-filter.c` @ v262 (sha256 `480f7a03…f48`) |
| `.ufo/waves/round-36/w1/SrcSystemdNews/journalctl.v262.xml` | `man/journalctl.xml` @ v262 (sha256 `d54bbede…bdd`) |
| `.ufo/waves/round-36/w1/SrcSystemdNews/journalctl.1.local-manpage` | decompressed on-host `journalctl(1)`, footer `systemd 262` (sha256 `1e737294…b54d`) |
| `.ufo/waves/round-36/w1/SrcSystemdNews/live-flag-matrix.txt` | the 19-row live matrix with exit codes and stderr |

## 9. Findings for the L1 / the Rust judge

1. **The declaration's "exact rejection line" is not a NEWS quote.** The declaration says
   C2's note must carry "the exact rejection line (`-F/--field= and -N/--fields cannot be
   combined with options that limit the journal.`)". That string appears in **no** NEWS
   revision — v262, `main` and the round-1 pin `a923ab5…` all carry only the prose bullet
   ("journalctl now rejects -F/--field together with filters such as unit, boot, time,
   cursor or grep filters."). The exact string and the exit code are supported by
   `src/journal/journalctl.c` @ v262 lines 958–960 and by the shipped binary. The note must
   attribute the exact line to the source/binary, not to NEWS, or the note overstates its
   primary source. **Reported verbatim as a conflict, not silently reconciled.**
2. **The exact limiting-option set is now known** (not guessed): the 16 conditions of
   `field_list_has_scope_options()` — boot filter, invocation, dmesg, cursor, after-cursor,
   cursor-file, system units, user units, syslog identifier, exclude identifier, priorities,
   facilities, since, until, pattern. `--follow`, `--merge` and `--show-cursor` are **not**
   limiting. The live matrix agrees with this on all 19 probed invocations.
3. **The man page does not document the restriction.** `man/journalctl.xml` @ v262 lines
   890–905 still only say "Print all field names currently used in all entries of the
   journal." (added v229) and "Print all possible data values the specified field can take
   in all entries of the journal." (added v195). The on-host `journalctl(1)` (footer
   `systemd 262`) is the same. `https://man.archlinux.org/man/journalctl.1` (sha256
   `aaae4efa…83c2`) likewise has no mention. So a note that cites the man page for the
   restriction would be unsupported — the restriction is NEWS- and source-only.
4. **`-F`/`-N` combined with `--grep` is the trap for scripts** and is exactly what NEWS
   warns about: before 262 the filters were *silently ignored* (no error, wrong output).
   Scripts that relied on the old silent behaviour now get exit 1 — a behaviour change from
   "wrong but exit 0" to "explicit failure". The lane's own consumers do not use `-F`/`-N`
   (grep over `tools/`, `corpus/`, `SKILL.md` finds only `journalctl -k`, `--list-boots`,
   `--grep`, `-b`, `-p err`, `-o json` forms in `tools/tsukuroi-census.sh`,
   `tools/score-census-handoff-r32.py`, `tools/check-boot-chain.py`,
   `tools/check-source-scope-correction.py` — **no** `-F`/`-N` use), so the note's consumer
   guidance is defensive, not a live repair. [inf — inference from the grep, which is a
   filename+pattern search, not a full AST scan.]
5. **S024's base anchor is self-admittedly unpinned** ("main branch fetched 2026-10-19 …
   no commit pin claimed"). The v262 tag supplies a reproducible pin whose commit
   (`8cc40e0c5e9234bf45084751ac53b1fbfe70b492`) is the release this host runs. The
   round-1 lesson row (`corpus/lessons/round-1.md:111`) already cites a `main` commit
   (`a923ab5ed1481512be6fb52aaa5086d0fef6878f`, dated 2026-10-19, "sd-varlink-idl: add
   SD_VARLINK_EXPERIMENTAL marker (#44287)") — **verified live**: that commit exists and its
   NEWS carries the same bullet at line 265, so the round-1 pin reproduces. The proposed
   S024 row supersedes it with the release tag rather than the moving branch.
6. **S198 (journalctl(1) at systemd 262) evidence is in this seat's directory** but the row
   itself is not this seat's deliverable. The on-host man page footer
   `.TH "JOURNALCTL" "1" "" "systemd 262" "journalctl"` and the v262 `man/journalctl.xml`
   bytes are the supports. Recorded as a dependency for the owning seat, not blocking.
7. **C2 prior state confirmed**: `grep -rl "cannot be combined with options that limit the
   journal" corpus/knowledge/ SKILL.md` prints nothing at the base tree
   (`6d76fb20…`), and no `corpus/knowledge/journalctl-v262-field-filter-r36.md` exists yet.
   This seat does not create that note — the L1 lands it from the drafting seat's output.

## 10. Out of scope (deliberately not done)

* No production file was edited: `corpus/SOURCES.md`, `SKILL.md`, `corpus/README.md`,
  `corpus/lessons/`, `tools/` are untouched. All writes are inside
  `.ufo/waves/round-36/w1/SrcSystemdNews/` (plus `/tmp` scratch).
* No git mutation: no `add`/`commit`/`push`, no `jj`, the lane index was never touched.
  Only read-only `git show`/`rev-parse`/`log`/`grep` were run.
* No pacman transaction (host-wide pause in force).
* No `corpus/knowledge/journalctl-v262-field-filter-r36.md` was authored — that is another
  seat's deliverable; this seat supplies its sources.
* The `## Paths` and `## Search log` sections of `corpus/SOURCES.md` were not amended; the
  L1 may want to add a search-log line recording the round-36 re-open of S024 (the row's
  `opened` cell stays `2026-10-19`; the re-open date is carried in the anchor).
