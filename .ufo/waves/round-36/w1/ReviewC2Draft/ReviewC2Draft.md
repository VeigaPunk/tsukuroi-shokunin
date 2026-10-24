# ReviewC2Draft — round 36, wave w1

Reviewer seat: C2 note draft review. All times pasted from `date -u +%H:%M:%SZ`.
Evidence captured at 02:48Z–02:49Z. Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
(base/declaration `6d76fb20f6ecbc940e5c8fff36c74060c885e161`).

## Primary input status (BLOCKING dependency, recorded per wave rule)

The draft and both source seats are **absent** as of 02:47:39Z:

```
$ ls -laR .ufo/waves/round-36/w1
./ScribeC2Draft: total 0      (empty)
./SrcJournalctlMan: total 0   (empty)
./SrcSystemdNews: total 0     (empty)
./ReviewC2Draft (this seat)
```

- `ScribeC2Draft/journalctl-v262-field-filter-r36.md` — **absent**. No draft, no matrix output,
  no decision table, no consumer inventory supplied by the drafting seat.
- `SrcJournalctlMan.md` (S198 row work) and `SrcSystemdNews.md` (S024 re-open) — **absent**.
  I cannot verify the note's header trio against those rows; I verified against
  `corpus/SOURCES.md:30` (S024) and the live host myself instead.
- `ScoutRecon` seat (`swarm-registry.json` member `ScoutRecon`, axes `depth,C2,recon`) has **no
  directory and no artifact**; consumer inventory below is my own fallback grep.

Per the standing wave rule (no seat blocks on a sibling), the remaining review is delivered as
(a) the acceptance checklist derived from the declaration, and (b) findings from independent
live/source verification that any draft must satisfy. Nothing here is a verdict on unwritten bytes.

## Independent verification (runs I did, not the draft's)

Live host: `systemd 262 (262-1-arch)` (`journalctl --version`). Matrix receipt:
`matrix.out` (30 invocations, command+rc+first stderr line) and `matrix.sh` in this directory.
Source: `systemd/systemd@v262:src/journal/journalctl.c:958-960`; NEWS at tag
`v262`, lines 129-132.

### Verified rejection (exit 1, exact stderr line)

```
-F/--field= and -N/--fields cannot be combined with options that limit the journal.
```

Guard is `IN_SET(arg_action, ACTION_LIST_FIELDS, ACTION_LIST_FIELD_NAMES) && field_list_has_scope_options()`
→ `log_error_errno(SYNTHETIC_ERRNO(EINVAL), …)` (`journalctl.c:958-960`), so exit status 1.

Rejected with that line (rc=1): `--since`, `-S`, `--until`, `-b`, `-b -1`, `--boot=0`, `-k`,
`-u`, `-t`, `-p`, `--facility`, `-g`, `--grep`, `--cursor`, `--after-cursor`, `--user-unit`;
both for `-F <field>` and for `-N`. (So the enumeration is filters + boot/time/cursor selectors,
matching NEWS "unit, boot, time, cursor or grep filters".)

### NOT rejected (rc=0) — traps a draft is likely to get wrong

| Invocation | rc | First line of output | Note |
|---|---|---|---|
| `journalctl -F _TRANSPORT` | 0 | `stdout` (5 values) | baseline |
| `journalctl -F _TRANSPORT -n 1` | 0 | `stdout` (**1 value**) | `-n` silently truncates the field list |
| `journalctl -F _TRANSPORT --lines=2` | 0 | `stdout`,`journal` (2 values) | same |
| `journalctl -F _TRANSPORT -n 0` | 0 | (empty) | prints nothing |
| `journalctl -F _TRANSPORT -D /var/log/journal` | 0 | full list | `-D` is scope, not filter |
| `journalctl -F _TRANSPORT --file /var/log/journal/…/system.journal` | 0 | full list | `--file` with a real file is NOT rejected |
| `journalctl -F _TRANSPORT --root /` | 0 | full list | scope |
| `journalctl -F _TRANSPORT --system` / `--user` | 0 | list / list | scope |
| `journalctl -F _TRANSPORT --namespace=x` | 0 | `No journal files were found.` | scope |
| `journalctl -F _TRANSPORT --no-pager` / `-q` / `-o json` | 0 | list | non-limiting |

### Cannot be classified by rc alone (require valid args / privileges)

`--invocation=deadbeef` → `Failed to parse invocation descriptor` (before the guard);
`--machine=x` → `Using the --machine= switch requires root privileges`; `--image=x` → loopback
setup failure; `--file /nonexistent` → `Failed to open files`. These must be marked
`unclassified [unk]` in any note, or re-tested with valid inputs — not asserted in either direction.

### Prior-state command (declaration) run at the base

```
$ grep -rl "cannot be combined with options that limit the journal" corpus/knowledge/ SKILL.md
(no output; rc=1)
$ git grep -l "cannot be combined with options that limit the journal" cefe752d -- corpus/knowledge SKILL.md
(no output; rc=1)
$ git grep -l "…" 6d76fb2 -- corpus/knowledge SKILL.md
(no output; rc=1)
```

So the declared "prints nothing at the base" holds for that literal string at both `cefe752d`
and `6d76fb2`. But the broader premise needs care — see finding B3.

## Findings

### BLOCKING (apply to any draft that lands)

- **B1 — `-n/--lines` must not be filed as "limiting/rejected" and must be covered as a silent
  truncator.** `journalctl -F _TRANSPORT -n 1` exits 0 and prints one value; `--lines=2` prints
  two. This is the most likely real-world consumer bug (a value list piped through a wrapper
  that leaves `-n` in place), and it is invisible under the rejection signature. A decision table
  whose only axis is "rejected vs allowed" is insufficient; it needs a third state
  "allowed, output silently altered" with this receipt. Evidence: `matrix.out` rows
  `-F -n 1`, `-F -n 0`, `-F --lines=2`; live re-run 02:48Z.
- **B2 — the matrix must separate scope options from filters and must not over-generalise.**
  `-D`, `--file` (valid path), `--root`, `--system`, `--user`, `--namespace` all exit 0 with
  `-F`. Any sentence of the form "`-F` cannot be combined with source-selection options" is
  false. The only universal sentence allowed is the literal quoted error string. The source
  predicate name to cite is `field_list_has_scope_options()` (`journalctl.c:958`).
- **B3 — S198/journalctl(1) does **not** document the rejection.** The rendered local
  `journalctl(1)` (systemd 262-1-arch, 761 lines) has only:
  `-N, --fields — Print all field names currently used in all entries of the journal.`
  and `-F, --field= — Print all possible data values the specified field can take in all entries
  of the journal.` (man lines 454-462). There is no "limit the journal" sentence in the page.
  A header trio that sources the *rejection line* to S198/man is a mis-citation. Correct
  attribution: rejection line + exit 1 = live capture (+ `journalctl.c:958-960`); S198 = option
  semantics only; S024 = the NEWS change statement.
- **B4 — the "Before:" premise of C2 is overstated.** `corpus/lessons/round-1.md:111` already
  records S024 with a NEWS commit pin and the exact NEWS quote:
  `"journalctl now rejects -F/--field together with filters such as unit, boot, time, cursor or grep filters."`
  (pin `a923ab5ed1481512be6fb52aaa5086d0fef6878f`). The declaration's "S024 (queued) asserts the
  fact without a pin" is contradicted by that row, and "no lane entry documents systemd 262's
  rejection" is false as written. What is genuinely missing is: the exact reject line, the exit
  code, the live flag matrix and consumer guidance. The note (and SCORECARD before-text, which
  only the L1 may change) must scope the gap that way and cite round-1.md:111.

### MINOR

- **M1 — S024 row hygiene.** `corpus/SOURCES.md:30` still carries `no commit pin claimed` and
  status `queued` while round-1.md:111 has pin `a923ab5e…`. The S024 re-open this round should
  reconcile the row (pin at `v262` tag, status promoted); otherwise the note cites a row whose
  declared provenance contradicts the lesson.
- **M2 — decision-table shape vs the 150-line cap.** Peer notes run 53-135 lines
  (`coredump-count-unit-r34.md` 120, `storage-health-r26.md` 135). A one-row-per-option matrix
  over ~30 options plus mechanism prose will exceed 150. Recommend three grouped tables
  (rejected / allowed-but-altered / allowed-or-unclassified) with one receipt line each.
- **M3 — honesty marks required.** `--machine`, `--image`, `--invocation` (valid args), and
  root-only paths could not be classified here; the note must mark them `[unk]` or test them with
  valid inputs. Also mark the negative fact "journalctl(1) v262 does not document the
  restriction" explicitly — it is a citation of absence and must say so.
- **M4 — consumer inventory is thin; do not invent consumers.** Lane-wide search
  (`tools/`, `corpus/`, `SKILL.md`) finds **zero** invocations combining `journalctl` with
  `-F`/`--field`/`-N`/`--fields`; the only hits are the SCORECARD/SOURCES prose and
  `corpus/lessons/round-1.md:111`. The census journal arm uses `journalctl -b -p err -o json`
  (`tools/tsukuroi-census.sh:1403-1410` per `coredump-count-unit-r34.md`), which the -F/-N guard
  does not touch. So the note's "safe substitution patterns for the lane's journal consumers"
  must be framed as guidance for future arms (and for ad-hoc operator use), not as a fix to an
  existing broken caller. If ScoutRecon later produces a non-empty inventory, that supersedes
  this fallback and the mismatch is then a draft defect.
- **M5 — substitution patterns should preserve the rejection's intent.** NEWS gives the reason:
  field listing previously used `sd_journal_query_unique()`, "which cannot represent those
  filters, so the filters were silently ignored" (v262 NEWS:129-132). Safe patterns are:
  filter the *values* in the shell (`journalctl -F FIELD | grep -x VALUE`), or derive values from
  a filtered entry stream (`journalctl --since … -o json | jq -r .FIELD | sort -u`). Patterns
  that reinstate silent ignoring (e.g. appending `|| true` and treating empty output as "no
  values") must be called out as unsafe.

## Acceptance checklist for the landed note (declaration-derived)

1. Header trio `source:` / `verified-at:` / `recheck:` present; `verified-at` is the live date
   (2026-10-23, host `systemd 262 (262-1-arch)`); `recheck: on-release` (systemd) per S024/S198;
   the `source:` line names S024 **and** S198 and does not attribute the rejection line to the man page.
2. Mechanism: the exact reject line, exit 1, `EINVAL`, guard `field_list_has_scope_options()`
   at `journalctl.c:958-960`, and the NEWS rationale (silent-ignore replacement).
3. Matrix: every rejection claim backed by a command+exit+stderr receipt existing in the matrix
   file; allowed-but-altered (`-n`, `--lines`) separated from allowed (`-D`, `--file`, `--root`,
   `--system`, `--user`, `--namespace`, `--no-pager`, `-o`); unclassified marked `[unk]`.
4. Decision table rows map 1:1 to matrix rows; no row asserted from inference.
5. Consumer inventory matches ScoutRecon (or an explicit "none today; preventive guidance" with
   the grep command and rc).
6. Honesty marks on unrun/root-required cases; no universal clause beyond the literal quoted
   error string.
7. ≤150 lines (target ~110-135, matching peer notes), falsifier section present, and the
   prior-state grep receipt reproduced verbatim (rc=1).
8. Registry rows: S198 added to `SOURCES.md`; S024 re-opened at the `v262` pin with its status
   reconciled against `corpus/lessons/round-1.md:111`.

## Residual risk / verification gaps

- I could not review the draft, its decision table, or its consumer inventory — all absent
  (ScribeC2Draft, SrcJournalctlMan, SrcSystemdNews empty; ScoutRecon missing). Any defect in
  those bytes is outside what this review can see.
- `--machine`, `--image`, `--invocation` with valid arguments, and root-only journal paths were
  not exercised (no root shell used; `--image` requires a real image): classification `[unk]`.
- `-D`/`--file` acceptance was tested read-only on this host's journal; behaviour with
  `--merge`/remote journals was not tested.
- Tooling: no installs; all checks used preinstalled `journalctl`, `man`, `git`, `python3`.
