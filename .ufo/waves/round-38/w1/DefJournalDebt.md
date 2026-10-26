VERDICT: supports — the round-37 correction's "the later action won" holds in **both** orders (source + live), so the claim is not falsified; but the note records only the `-F`-then-`--list-boots` direction and never states (i) that the losing command is silently discarded, (ii) that the *selected action* decides which validation guards fire, or (iii) that `--list-boots --merge` can be evaded by argument order. The append-only text at the end of this report records both behaviours with line citations. Separate defect found in the same note: the round-37 correction was appended twice (near-duplicate, lines 129-157 vs 158-185).

# Item D-3b (routed defect 3, depth debt)

## Scope and method

- Re-opened `https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl.c` on **2026-10-26** (HTTP 200, 47020 bytes, 1139 lines, sha256 `285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab`) — the same bytes the round-36 note pinned (`285b3d0c…d5d0ab`, `corpus/knowledge/journalctl-v262-field-filter-r36.md:3`).
- Also read at the same tag: `src/journal/journalctl-filter.c` (sha256 `480f7a03040c0ddc93b1b65c0b49d6f0e8a4a377ee1b94168655132dcfd72f48`, matches the note's `480f7a03…72f48`), `src/shared/options.h` (`f56c0cc6…`), `src/shared/options.c` (`110b3029…`), `man/journalctl.xml` (`d54bbede…`).
- Host binary measured: `journalctl --version` → `systemd 262 (262-1-arch)`. All commands were read-only (`--no-pager`, no `--sync`, no `--rotate`, no `--vacuum-*`, no `--flush`), no unit/package/sysfs/journal mutation.
- Reproducible matrix: `.ufo/waves/round-38/w1/DefJournalDebt/live-matrix.jsonl` (17 rows, each with argv, rc, stdout bytes, stdout sha256, stderr bytes, stderr text).
- **Digests are content-dependent.** The host journal grows and rotates, so absolute byte counts differ from the round-36 saved cells (the note's `541` bytes for `live_list_boots` is now `447`; its `2882` bytes for `-N` is now `2849`). The durable evidence is **sha256 equality between invocations**, not the byte counts. I name this explicitly so nobody reads my numbers as falsifying the round-36 observations.

## (a) Reverse order `--list-boots -F`: the later option wins, the earlier one is discarded

Source, verbatim (word counts ≤ 25 each), `journalctl.c`:

```
805:                 OPTION('F', "field", "FIELD", "List all values that a specified field takes"):
806:                         arg_action = ACTION_LIST_FIELDS;
807:                         r = free_and_strdup_warn(&arg_field, opts.arg);
808:                         if (r < 0)
809:                                 return r;
810:                         break;
```

```
812:                 OPTION_LONG("list-boots", NULL, "Show terse information about recorded boots"):
813:                         arg_action = ACTION_LIST_BOOTS;
814:                         break;
```

Both arms assign the same variable unconditionally; neither inspects the previous value. Precedence is therefore argv order, and ordering is structurally guaranteed, not incidental:

- `FOREACH_OPTION_OR_RETURN` is a plain sequential `for` over `option_parse(...)` — `options.h:255-259`, whose contract comment is "Iterate over options. Don't forget to handle errors (negative c!)" (`options.h:252`); `journalctl.c:385` uses it.
- `optind` advances monotonically; `shift_arg()` only compacts already-consumed tokens toward the front — "Move argv[source] before argv[target], shifting the arguments in between." (`options.c:38`), called only at `options.c:375`/`:377` with `positional_offset++`/`optind++`. `struct OptionParser`'s "argv array, possibly reordered" (`options.h:221`) therefore refers to consumed-positional compaction, not to option re-sequencing.
- **No action-conflict check exists.** The only "at most one"/"only one of" diagnostics in `parse_argv()` are for journal sources (`journalctl.c:935`, `-D/--file/-M/--root/--image`) and for `--since`/cursor (`journalctl.c:943`). Two commands are accepted in silence.

Observable behaviour (live, 2026-10-26). The losing command leaves **no trace**: stdout is byte-identical to the same argv with that command deleted.

| argv (`journalctl --no-pager …`) | rc | stdout | equals |
|---|---|---|---|
| `--list-boots -F PRIORITY` | 0 | 11 B, sha256 `cbfedf6a…91e20d` | **identical to `-F PRIORITY`** → field values printed, boot list never produced |
| `-F PRIORITY --list-boots` | 0 | 447 B, sha256 `e55209f6…889d0fa2` | **identical to `-b 0 --list-boots`** → boot table printed, field list never produced |
| `--list-boots -N` | 0 | 2849 B, sha256 `b07760c5…c9e3329cb` | **identical to `-N`** |
| `-F PRIORITY -N` | 0 | 2849 B, sha256 `b07760c5…c9e3329cb` | **identical to `-N`** (last field action wins within the same family) |
| `-b 0 --list-boots` | 0 | 447 B, sha256 `e55209f6…889d0fa2` | `-b 0` has no effect on the boot-table output |

So `--list-boots -F PRIORITY` prints the `PRIORITY` value list (`2 4 5 6 7 3` — journal order, **not** sorted; the note's `2 3 4 5 6 7` is its `sort -u` pipeline output, not raw `-F` output) and exits 0. The user asked for two different reports and got one, with no warning.

## (b) `--list-boots --merge`: an action-gated rejection that argument order can bypass

Source, verbatim, `journalctl.c`:

```
962:         if ((arg_boot || arg_action == ACTION_LIST_BOOTS) && arg_merge)
963:                 return log_error_errno(SYNTHETIC_ERRNO(EINVAL),
964:                                        "Using --boot or --list-boots with --merge is not supported.");
```

Observable behaviour: exit **1**, stdout **0 B**, stderr exactly `Using --boot or --list-boots with --merge is not supported.` (59 chars + newline = **60 bytes**), raised in `parse_argv()`, which returns before any journal open — `journalctl.c:1019-1020` (`r = parse_argv(argc, argv, &args); if (r <= 0) return r;`).

The guard has **two independent terms**; `arg_boot` alone suffices: `-b 0 --merge -n 1` (action `SHOW`) exits 1 with the merge message. And because the guard tests the *selected* action, the same three words can be an error or be silently dropped:

| argv (`journalctl --no-pager …`) | rc | stdout | stderr |
|---|---|---|---|
| `--list-boots --merge` | 1 | 0 B | 60 B merge message |
| `-b 0 --list-boots --merge` | 1 | 0 B | 60 B merge message |
| `-F PRIORITY --list-boots --merge` | 1 | 0 B | 60 B merge message (list-boots won the action) |
| `--list-boots -F PRIORITY --merge` | **0** | 11 B (field values) | — **`--merge` silently ignored** |
| `--list-boots -N --merge` | **0** | 2849 B (field names) | — **`--merge` silently ignored** |
| `--merge` | 0 | 63753114 B (measured once) | — |

That is the depth-debt core: `--list-boots --merge` is a **documented rejection** (`journalctl.c:962-964`) that any caller can defeat by writing `-F`/`-N` after `--list-boots`. The error message also never mentions `--merge`'s actual effect, and never names the command that was discarded.

## Guard order: the first satisfied guard decides the message

`journalctl.c:958-960` (field-list scope rejection) is evaluated **before** `:962-964` (merge). Measured: `-F PRIORITY -b 0 --merge` exits 1 with the **84-byte** `-F/--field= and -N/--fields cannot be combined with options that limit the journal.` line, not the merge line. Combined with (a), the same argv in the other order (`--list-boots -F PRIORITY -b 0`) also exits 1 with the field-list line — but `-F PRIORITY --list-boots -b 0` exits **0** (447 B boot table). Identical option multiset, three different outcomes, selected purely by argv order.

## Man page is silent on precedence

`man/journalctl.xml:886`, §Commands: "The following commands are understood. If none is specified the default is to display journal records:" — no statement that commands are mutually exclusive, that the last wins, or that mixing them is an error. Last-wins is implementation behaviour, not documented interface; a knowledge note that treats it as a contract overstates the source.

## Comparison with `corpus/knowledge/journalctl-v262-field-filter-r36.md`

| claim under test | verdict | evidence |
|---|---|---|
| "`-F` sets `arg_action = ACTION_LIST_FIELDS` at `journalctl.c:805-809`, then `--list-boots` replaces it with `ACTION_LIST_BOOTS` at `:812-814`" (`:148`, repeated at `:177`) | **holds** | fetched bytes: assignment at `:806`, `:813`; live `-F PRIORITY --list-boots` stdout sha256 == `-b 0 --list-boots` |
| "Therefore the result means the later action won" (`:148`) | **holds, in both orders** | reverse order gives the *other* command's output (`--list-boots -F PRIORITY` == plain `-F PRIORITY`) |
| "Predicate: 15 terms" (`:133-135`) | **holds** | `journalctl-filter.c:26-43` lists exactly 15 OR terms; file digest matches the note |
| decision-table row 44: `--list-boots`, `--merge` classified "not a limiter … WORK" (`:44`) | **true as written, misleading in combination** | `--merge -F PRIORITY` → rc 0 (table correct), but `--list-boots -F PRIORITY -b 0` → rc 1, so `--list-boots` does **not** exempt a later `-F` from the scope predicate |
| `-N` invariant: `-n 1 -N` output identical to plain `-N` (`:140`, sha `3480f2aa…`) | **shape holds; digest is stale** | today `-N`, `-n 1 -N` analog, `-F PRIORITY -N`, `--list-boots -N` all share sha256 `b07760c5…` and 2849 B — the *equality* is durable, the absolute digest is journal-content dependent |

Not covered by the note at all: the reverse order, the absence of an action-conflict diagnostic, the selected-action dependence of the guard set, the guard order (`:958` before `:962`), and the `--merge` bypass.

### Defect in the note itself: the round-37 correction is present twice

`corpus/knowledge/journalctl-v262-field-filter-r36.md` carries the heading "## Round 37 correction — predicate count, output states, action precedence and prior teaching" at **line 129** and again at **line 158**, with the same five subsections. The copies are not byte-identical: lines 129-157 vs 158-185 differ in one line only —

```
14c14
< | `journalctl --no-pager -n 1 -N` | accepted (exit 0); `-N` field-name output is unchanged from plain `-N` | …
---
> | `journalctl --no-pager -n 1 -N` | accepted (exit 0); field-name output is unchanged from plain `-N` | …
```

plus a trailing blank line (file is 185 lines; `sha256 dedb5c2f…1483b`). This is a stale-copy hazard: a future editor can update one copy and leave the other, and the two now disagree on whether the `-N` invariance statement is scoped to `-N`. Deleting the second copy is a lane edit, which is outside my read-only seat; I report it for the lane owner.

## Side observation (guard against a future misreading)

Raw `journalctl --no-pager -F PRIORITY` prints `2 4 5 6 7 3` — journal order, not ascending. The note's "Verified live here: exit 0, output `2 3 4 5 6 7`" (`:52-58`) is the output of its `jq | sort -u` pipeline and must not be cited as the raw `-F` order. Today's plain `-F PRIORITY` and `--list-boots -F PRIORITY` share stdout sha256 `cbfedf6a…91e20d` (11 B).

## Proposed append-only text (for `corpus/knowledge/journalctl-v262-field-filter-r36.md`, insert after line 185)

```markdown
## Round 38 addendum — precedence in both orders, and the `--list-boots --merge` guard

Re-opened `https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl.c` on 2026-10-26 (1139 lines, sha256 `285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab` — the bytes this note already pins), with `src/shared/options.h` (`f56c0cc6…`), `src/shared/options.c` (`110b3029…`) and `man/journalctl.xml` (`d54bbede…`) at the same tag. Host: `systemd 262 (262-1-arch)`. This addendum extends the round-37 correction above; it supersedes nothing in it. Every command below was read-only.

### (a) The losing command is silently discarded, in both orders

Both arms assign `arg_action` unconditionally inside one left-to-right parse loop: `-F/--field=` sets `ACTION_LIST_FIELDS` (`journalctl.c:805-810`, assignment at `:806`), `--list-boots` sets `ACTION_LIST_BOOTS` (`:812-814`, assignment at `:813`). `FOREACH_OPTION_OR_RETURN` is a sequential `for` over `option_parse(...)` (`options.h:255-259`), `optind` advances monotonically, and `shift_arg()` only compacts consumed tokens toward the front of `argv` (`options.c:34-42`, `:375-377`) — the option sequence is preserved, so the rightmost command survives.

No action-conflict diagnostic exists: the only "one of" checks in `parse_argv()` are for journal sources (`:935`) and `--since`/cursor (`:943`). The earlier command produces nothing at all; stdout is byte-identical to the same argv with that command removed.

| argv (`journalctl --no-pager …`) | rc | stdout | equals |
|---|---|---|---|
| `--list-boots -F PRIORITY` | 0 | 11 B, sha256 `cbfedf6a…91e20d` | `-F PRIORITY` — field values; boot list never printed |
| `-F PRIORITY --list-boots` | 0 | 447 B, sha256 `e55209f6…889d0fa2` | `-b 0 --list-boots` — boot table; field list never printed |
| `--list-boots -N` | 0 | 2849 B, sha256 `b07760c5…c9e3329cb` | `-N` |
| `-F PRIORITY -N` | 0 | 2849 B, sha256 `b07760c5…c9e3329cb` | `-N` |
| `-b 0 --list-boots` | 0 | 447 B, sha256 `e55209f6…889d0fa2` | plain `--list-boots` — `-b 0` has no effect on the boot table |

Absolute byte counts and sha256s are host-journal content (2026-10-26 snapshot), so they drift between rounds; the durable claim is the **equality** between an invocation and its one-command-stripped twin. Raw `-F PRIORITY` prints in journal order (`2 4 5 6 7 3`), not sorted — the sorted `2 3 4 5 6 7` in §Safe substitution is that pipeline's `sort -u`, not raw `-F` output.

### (b) `--list-boots --merge` rejects, and order can bypass the rejection

`if ((arg_boot || arg_action == ACTION_LIST_BOOTS) && arg_merge)` (`journalctl.c:962-964`) exits **1** with stderr `Using --boot or --list-boots with --merge is not supported.` (59 chars + newline = 60 bytes), 0 stdout bytes, raised in `parse_argv()` before any journal open (`journalctl.c:1019-1020`). `arg_boot` alone is sufficient: `-b 0 --merge -n 1` (action `SHOW`) rejects with the same line.

Because the guard tests the *selected* action, mixing a field action with `--list-boots` and `--merge` gives either an error or a silent no-op:

| argv (`journalctl --no-pager …`) | rc | stdout | stderr |
|---|---|---|---|
| `--list-boots --merge` | 1 | 0 B | 60 B merge message |
| `-F PRIORITY --list-boots --merge` | 1 | 0 B | 60 B merge message |
| `--list-boots -F PRIORITY --merge` | 0 | 11 B field values | — `--merge` silently ignored |
| `--list-boots -N --merge` | 0 | 2849 B field names | — `--merge` silently ignored |
| `--merge` | 0 | 63753114 B | — (measured once) |

So the string `--list-boots --merge` is a documented rejection (`:962-964`) that any caller defeats by placing `-F` or `-N` after `--list-boots`.

### Guard order decides which error is reported

The field-list scope guard (`:958-960`) precedes the merge guard (`:962-964`): `-F PRIORITY -b 0 --merge` yields the 84-byte `-F/--field= and -N/--fields cannot be combined with options that limit the journal.` line, not the merge line. With (a), one option multiset has three outcomes: `--list-boots -F PRIORITY -b 0` → rc 1 field-list line; `-F PRIORITY --list-boots -b 0` → rc 0 boot table; `-F PRIORITY -b 0 --merge` → rc 1 field-list line.

### The man page does not define precedence

`man/journalctl.xml:886` (§Commands): "The following commands are understood. If none is specified the default is to display journal records:" — nothing on mutual exclusion, on last-wins, or on mixing commands. Last-wins is implementation behaviour, not a documented contract. A caller that needs two reports must issue two `journalctl` invocations; an arm that wants merged output must verify `--merge` took effect, because a field action drops it without a message.

### Falsifier (round 38)

1. `journalctl --no-pager --list-boots -F PRIORITY` exits non-0, or its stdout differs from `journalctl --no-pager -F PRIORITY`.
2. `journalctl --no-pager -F PRIORITY --list-boots` stdout differs from `journalctl --no-pager -b 0 --list-boots`.
3. `journalctl --no-pager --list-boots --merge` exits 0, prints stdout, or its stderr is not the 60-byte merge line.
4. `journalctl --no-pager --list-boots -F PRIORITY --merge` exits non-0 (the bypass is order-sensitive).
5. `parse_argv()` at v262 gains an action-conflict diagnostic (today only `:935` and `:943` exist).
6. A later systemd documents command precedence; the "undocumented" clause here then becomes stale.

### Provenance (round 38)

Live matrix (17 rows: argv, rc, stdout bytes, stdout sha256, stderr bytes, stderr text): `.ufo/waves/round-38/w1/DefJournalDebt/live-matrix.jsonl`. Source excerpts: `.ufo/waves/round-38/w1/DefJournalDebt/journalctl.c-excerpt.txt`. File digests: `.ufo/waves/round-38/w1/DefJournalDebt/provenance.txt`.

### QUALITY note

1 (falsifiable): six conditions above. 2 (source): every claim is a `file:line` at the pinned tag plus an rc/byte/sha256 receipt. 3 (observation vs inference): the tables are executed observations; "no action-conflict diagnostic" is a source statement about the two "one of" checks at `:935` and `:943`, not an inference from silence. 7 (S-row, tier A): the v262 tag sources and `journalctl(1)`-derived `journalctl.xml`. Known limit: the merge-bypass asymmetry is shown on this host's systemd 262 build; no other build was tested.
```

## Findings

1. **Supported**: "the later action won" (`corpus/knowledge/journalctl-v262-field-filter-r36.md:148`, `:177`) is correct in both orders, and the cited line numbers resolve to the fetched bytes (`:806`, `:813`).
2. **Debt (depth)**: the note's model is one-directional. It never states that the earlier command is discarded silently, so a reader can carry away "`--list-boots` wins" instead of "rightmost wins", and the decision-table row at `:44` reads as if `--list-boots` is benign next to `-F` — `--list-boots -F PRIORITY -b 0` exits 1 (`live-matrix.jsonl`).
3. **Debt (depth)**: `--list-boots --merge` rejection (`journalctl.c:962-964`) is not order-robust; `--list-boots -F PRIORITY --merge` and `--list-boots -N --merge` exit 0 with `--merge` dropped. The guard set is action-selected, and the field-list guard shadows the merge guard.
4. **Defect (hygiene)**: the round-37 correction block is duplicated (`:129-157` and `:158-185`), and the copies already disagree by one edited line; they are not byte-identical.
5. **Provenance note**: the note's `541`-byte and `2882`-byte counts, and its `3480f2aa…` `-N` digest, are round-36 host-journal snapshots; today's values differ (447 B, 2849 B, `b07760c5…`) while the *equality* statements they support still hold. No falsification.

## What I did not do

- No lane file was touched (read-only seat); the draft above is text in this report, not applied to `corpus/knowledge/journalctl-v262-field-filter-r36.md`, and the duplicate-section deletion is left to the lane owner.
- No host mutation: no package/service/sysfs/journal counter change, no sudo, no `pacman` (host-wide pause respected). No tool was installed — `curl`, `journalctl` and `sha256sum` sufficed.
- Not tested: systemd versions other than this host's 262 build; `--vacuum-*`/`--rotate` actions (mutating), `--verify`, `--setup-keys` actions; whether `-r`/`-n` alter the boot-table row order beyond the man page's statement; varlink-mode parsing (`journalctl.c:332-378`) — its `FOREACH` uses the same sequential parser but was not exercised.
- Absolute byte counts and sha256 in the tables are 2026-10-26 snapshots of this host's journal and will drift; only the inter-invocation equalities are durable.

## Provenance / artifacts

- `journalctl.c` v262: 47020 B, 1139 lines, sha256 `285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab` — `.ufo/waves/round-38/w1/DefJournalDebt/provenance.txt`.
- `journalctl-filter.c` `480f7a03…72f48`; `options.h` `f56c0cc6…`; `options.c` `110b3029…`; `journalctl.xml` `d54bbede…` — same file.
- Excerpts with line numbers: `.ufo/waves/round-38/w1/DefJournalDebt/journalctl.c-excerpt.txt`.
- Live matrix: `.ufo/waves/round-38/w1/DefJournalDebt/live-matrix.jsonl`.
- Host: `systemd 262 (262-1-arch)`; all measurements read-only, no scratch left behind (`/fast/scratch/hyaku/tsukuroi-r38/DefJournalDebt` removed after receipts were copied).
