# ScribeC2Draft — round 36, wave w1 — C2 note draft (journalctl v262 field/filter rejection)

Seat: `tsukuroi-r36.ScribeC2Draft` · lane repo `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
· base/declaration commit `6d76fb20f6ecbc940e5c8fff36c74060c885e161` · write scope: this seat dir only.
Report heading time `02:58:02Z` (pasted from `date -u +%H:%M:%SZ`).

## Behavior delivered

Drafted `journalctl-v262-field-filter-r36.md` (127 lines, under the 150-line bound) into this
seat dir for the L1 to land at `corpus/knowledge/`. It carries every element the assignment
named: title; `source:` citing S024 (pinned v262 NEWS) and S198 (`journalctl(1)` at 262);
`verified-at: 2026-10-23`; `recheck: on-release (systemd major bump; re-run the matrix
commands)`; the exact rejection line with its exit code; a 26-row decision table
(limiting-option → reject/work → evidence pointer); a consumer section naming every
`journalctl` invocation in `tools/` with its verdict; a six-item falsifier; `[inf]`/`[unk]`
marks; and the prior-state sentence with its counting command and pasted output.

I ran the core matrix myself (six cells as specified) plus 29 extended cells, merged the
`ExecC2Live` peer matrix's 4 extra cells (re-run rather than transcribed), and backfilled 15
`live_*` cells so **every** decision-table row names a cell. Total 54 cells in
`matrix-mini.json`, all with exit code, stderr bytes, stderr text, stdout bytes and stdout
sha256. Cell-name integrity was machine-checked: every `core_*`/`ext_*`/`live_*`/`merged_*`
token referenced in the note exists in the JSON (0 missing), and no cell claims `REJECT`
without the rejection line present or `OK` with a non-zero exit.

## Gates (run in a scratch clone, never the lane)

Sandbox: `mktemp -d` clone of the lane, note copied into `corpus/knowledge/`, committed in the
scratch repo only, `refs/remotes/origin/master` pointed at that commit so the shared
`tools/_revision.py` binding resolves. No lane commit, no lane index write, no VCS mutation
in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.

| gate | result |
|---|---|
| `tools/check-knowledge-header.py` | **PASS**, 0 findings, 56 notes (source/verified-at/recheck all present at column 0; ISO date; `on-release` cadence) |
| `tools/check-recheck-commands.py` | **PASS**, 0 findings, 56 files / 81 invocations (my `recheck:` line names no forbidden binary and carries no backticked command) |
| `tools/check-source-scope-correction.py` | **PASS**, 0 findings, 2 corrections |
| `tools/check-boot-chain.py` | **PASS**, 0 findings, 6 entries |

The L1 must re-run the seven lane gates at the first commit carrying the C1 change, per the
declaration; these four are the note-shape gates and they pass on the draft.

## Host verification (read-only; no package, service or boot action)

Host: `systemd 262 (262-1-arch)`, `pacman -Q systemd` = `systemd 262-1`,
`/usr/bin/journalctl` 110016 bytes dated 2026-09-22. Journal readable as uid 1000; boots
`-4…0` present.

Exact rejection line, 84 stderr bytes including newline, **exit 1**:

```
-F/--field= and -N/--fields cannot be combined with options that limit the journal.
```

Matrix shape: 54 cells, each recording `argv`, exit code, stderr bytes, stderr text,
stdout bytes, stdout sha256. `matrix-mini.json` is self-describing (`core_cells` names the
six required ones; `peer_crosscheck` and `backfill_note` record the merge).

## Findings

**F1 — the exact rejection line is NOT in systemd NEWS, and NOT in `journalctl(1)`.** S024's
v262 NEWS entry (`NEWS:129-133`) states the change only in prose: "journalctl now rejects
-F/--field together with filters such as unit, boot, time, cursor or grep filters." The exact
string is the runtime error at `src/journal/journalctl.c:958-960` (v262). The man page at 262
carries neither sentence: `grep -c -i 'cannot be combined'` = 0 in the Arch 262.1 HTML
(sha256 `aaae4efa…`) and 0 in `man/journalctl.xml` at tag `v262`. The note therefore attributes
the string and exit code to the source and the shipped binary, not to NEWS or the man page —
this was independently confirmed by `SrcSystemdNews` over IRC at 02:5xZ. S024 supports the
behaviour statement; S198 supports the `-F`/`-N` semantics only. **Any reading of the
declaration that expects the string in NEWS would overstate its source.**

**F2 — the limiting set is exactly the 16-term `field_list_has_scope_options()` predicate.**
From `src/journal/journalctl-filter.c:26-43` at tag v262 (sha256 `480f7a03…72f48`): boot
filter, invocation, dmesg, cursor, after-cursor, cursor-file, system units, user units,
syslog identifier, exclude identifier, priorities, facilities, since, until, pattern. Each
term was separately confirmed live. `--follow`, `--merge`, `--show-cursor`, `--reverse`,
`--all`, `--output-fields`, `--quiet`, `--root`, `-D`, `--file`, `--user`, `--system`,
`--namespace`, `--lines` are **not** limiters; `--boot=all` also works because it sets no
boot filter.

**F3 — `-N`/`--fields` takes NO argument at 262.** It lists every field name in use (167 on
this host). So `journalctl --no-pager -N PRIORITY,MESSAGE` fails with
`Extraneous arguments starting with 'PRIORITY,MESSAGE'` (exit 1, 54 stderr bytes) — **not**
with the scope rejection. The L1's `gen-w1-spec.py:67` wave spec lists `-N PRIORITY,MESSAGE`
as a matrix cell; that cell as written cannot exercise the rejection. `SrcSystemdNews` and
`ExecC2Live` independently hit the same result.

**F4 — the census has a latent silent-miscount path.** `tools/tsukuroi-census.sh:541-546`
(`cap()`) captures with `2>&1`, so stderr joins stdout; the grep arms at `:1247-1251` accept
rc 1 as "0 entries". Measured: a `--grep` no-match run yields the sentinel `-- No entries --`
(1 line, rc 1); a `--grep` run that also carried `-F` yields the rejection sentence (1 line,
rc 1) — the same count from a different cause. No shipped arm uses `-F`, so this is a hazard
about a hypothetical future arm, marked as such in the note. Not a claim of a current defect.

**F5 — no lane tool uses `-F` or `-N`.** `grep -rn journalctl tools/` returns 43 hits across
4 files (`tsukuroi-census.sh`, `score-census-handoff-r32.py`, `check-boot-chain.py`,
`check-source-scope-correction.py`); every real invocation is a `-F`-free `--output=json` /
`--list-boots` / `--grep` form. Two of the four files only mention the word in a docstring or
a regex. The lane is not exposed today.

**F6 — the fixture stubs would not catch a `-F` regression.** Both `journalctl` fixture stubs
(`tsukuroi-census.sh:1883-1900`, `score-census-handoff-r32.py:150-165`) dispatch on argument
substrings and fall through to a `*)` default that returns `journal-all.json`. A `-F`
invocation would silently get the wrong fixture rather than an error.

**F7 — peer matrix cross-check passed.** `ExecC2Live/matrix.json` (10 cells + controls)
appeared at 02:58Z, after my matrix. All 6 overlapping cells agree on exit code and stderr
byte count. Its 4 peer-only cells were re-run here and recorded as `merged_*` cells rather
than transcribed. Its control `journalctl --no-pager -N` exits 0 with 167 field names.

**F8 — `--quiet` does not exempt.** `--quiet -b 0 -F PRIORITY` still rejects (84 stderr
bytes, exit 1), as expected from the predicate: `--quiet` is not in it and the limiter is.

## Prior state (pasted)

At base `6d76fb20f6ecbc940e5c8fff36c74060c885e161`:

```
$ grep -rl "cannot be combined with options that limit the journal" corpus/knowledge/ SKILL.md
$ echo $?
1
```

No output, exit 1. Re-run in the working tree: same. A whole-repo `git grep` at the base finds
exactly one hit, `SCORECARD.md:1632` — the declaration's own C2 prior-state counting command.
The declaration named the string; no entry documented the behaviour.

## Touched surfaces

Seat dir only: `.ufo/waves/round-36/w1/ScribeC2Draft/`

| file | content |
|---|---|
| `ScribeC2Draft.md` | this report |
| `journalctl-v262-field-filter-r36.md` | the note draft for `corpus/knowledge/` (127 lines) |
| `matrix-mini.json` | 39 live cells, peer-merge record, version/pacman facts |
| `news-v262-excerpt.txt` | v262 NEWS lines 125-133 snapshot (sha256 `b7c0df0d…`) |
| `journalctl-filter-c-predicate.txt` | `field_list_has_scope_options()` lines 26-44 (sha256 `28b65c28…`) |
| `journalctl-c-callsite.txt` | the guard and rejection lines 955-962 (sha256 `a21927a4…`) |

Scratch only: `/tmp/tmp.wapwBS6Pqf/lane` (gate sandbox), `/tmp/systemd-v262.tar.gz`,
`/tmp/v262_*`, `/tmp/extra_matrix.json`, `/tmp/extra2.json`, `/tmp/subs.json`, `/tmp/haz.sh`.

## Out of scope (not done, by design)

- Did NOT edit any production file: `tools/`, `corpus/`, `SCORECARD.md`, `LOG.md`, `SKILL.md`,
  `corpus/SOURCES.md`. The L1 lands the note and the S024/S198 rows from the source seats.
- Did NOT write `s024-row.md` or `s198-row.md` — those belong to `SrcSystemdNews` and
  `SrcJournalctlMan`, both of which delivered them in their own seat dirs.
- Did NOT run git add/commit/push/jj in the lane repo; the scratch clone was outside it.
- Did NOT run the pacman binary in any form (host-wide pause, orchestrator ruling 2026-10-20).
  `pacman -Q systemd` output was quoted from `SrcSystemdNews`'s execution and from the earlier
  read; my own host facts come from `systemctl --version`, `journalctl --version` and the
  binary listing.
- Did NOT install or upgrade any tool: `curl`, `python3`, `jq`, `grep`, `git`, `systemctl`,
  `journalctl` were already present and sufficient. No tooling record to file.
- Did NOT dispatch a subagent (leaf seat).

## Known limits

- The matrix is a single-host, single-version observation at 2026-10-23. The note's falsifier
  encodes the re-run; the `on-release` cadence is the trigger.
- The census hazard (F4) is a replication of the census's own counting expression against
  hypothetical argv, not an execution of a lane arm.
- Every decision-table row now names a cell in `matrix-mini.json`, so no row rests on
  session-only observation. The 15 `live_*` cells were backfilled after the first draft for
  exactly that reason; `ext_*` cells the table does not cite remain in the matrix as the wider
  sweep and are not part of any claim.
- `-N`-alone and `-F`-alone control values (field names / field values) are recorded, but the
  note does not tabulate their contents; it only relies on their exit 0.
- The peer `ExecC2Live` matrix could be revised after 02:58Z; only the revision read at merge
  time is covered (see the F7 finding and the note's `[unk]` bullet).
