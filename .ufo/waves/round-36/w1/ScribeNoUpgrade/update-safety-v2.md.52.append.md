# Append-block draft — target `corpus/knowledge/update-safety-v2.md`, site `:52`

Seat: `ScribeNoUpgrade` (round 36, wave 1, routed repair 4).
Target (lane-relative): `corpus/knowledge/update-safety-v2.md`
Site: line 52 (one table row in §1 "Re-run receipts — r2 pin vs v2 value")
Base commit read: `6d76fb20f6ecbc940e5c8fff36c74060c885e161` (declaration); file digests below at `189d8a080ba8d508d5faab12cad9e688aee91dab`
Target sha256 at that commit: `caa747e657527c5c29ceb93bfcc86791b53277e85cfd9b82bc804c0ba0e6895d` (420 lines)

## Landing instruction (for the L1)

**Append at the END of the file** (after the `## R18-RECHECK — steer-safe procedure` block, i.e.
after line 420). Do not edit the row. Evidence (verified):

- `corpus/knowledge/freshness-recheck-r18.json` has 8 records on this path, baseline
  `842a5312...`; `check-appended-notices.py` requires `target_bytes.startswith(base_bytes)`
  (`NOTICE-HISTORY`). At `189d8a08` the property holds (base 388 lines, target 420 lines, first
  differing offset = start of line 389). A mid-file insert breaks it.
- Line-number citations that a mid-file insert would corrupt: `update-safety-v3.md:103`
  (`update-safety-v2.md:244-260`), `corpus/lessons/round-16-verifier-spotcheck.md:53`
  (`update-safety-v2.md:244`), `plans/round-9.plan.md:25` and `plans/round-9-record-draft.md:59`
  (`update-safety-v2.md:24-25,33`), and this file's own `:357` (`:102,280`).
- **This file's last section is the operative steer-safe section** (`## R18-RECHECK — steer-safe
  procedure`, line 412) and it currently runs to EOF. The block below starts with a `## ` heading,
  which terminates that section at the same place (`check-recheck-commands.py` `section()`), so the
  steer-safe body and its command scan are unchanged. If the L1 lands both v2 blocks, land them one
  after the other; each block's `## ` heading terminates the previous section.

## Verbatim original (quoted; NOT to be rewritten)

> | 7 | pins | `IgnorePkg`/`IgnoreGroup`/`NoUpgrade`/`NoExtract` empty; `HoldPkg = pacman glibc` (`:208-216`) | identical (all four rc=0 empty; HoldPkg two lines) | same |

The table's columns are `| # | pin (r2) | r2 value (10:44–10:51 -03) | v2 value (18:19–18:26Z) | verdict |`,
so the defect is the **label** `pins` covering four directives of two classes; the two value cells
("identical (all four rc=0 empty…)") are correct and unchanged.

## Append block (paste at EOF, verbatim)

```markdown
## R36-SUPERSESSION — row 7 of the §1 receipts table: `pins` covers two directive classes (2026-10-24)

Appended in round 36 as routed repair 4 (`corpus/lessons/round-35-verifier-spotcheck.md` §6 item 4).
The row above is preserved unchanged; this block supersedes its label. Prior locus (`:52`),
verbatim:

> | 7 | pins | `IgnorePkg`/`IgnoreGroup`/`NoUpgrade`/`NoExtract` empty; `HoldPkg = pacman glibc` (`:208-216`) | identical (all four rc=0 empty; HoldPkg two lines) | same |

Superseded as a classification by `corpus/knowledge/pacman-backup-files-r35.md`
(§ `[obs] NoUpgrade and NoExtract (S191, S195)`; S191 pacman `lib/libalpm/add.c` at 54d94116164b,
S195 pacman `doc/pacman.conf.5.asciidoc` at 54d94116164b): `IgnorePkg` / `IgnoreGroup` are the
version pins ("Instructs pacman to ignore any upgrades for this package when performing a
'--sysupgrade'." — S195 lines 102-104) and `NoUpgrade` / `NoExtract` are file-extraction rules
("All files listed with a `NoUpgrade` directive will never be touched during a package
install/upgrade" — S195 lines 136-137; "All files listed with a `NoExtract` directive will never be
extracted from a package into the filesystem" — S195 lines 147-148).

Replacement row (the row as it reads under the corrected classification):

> | 7 | pins | `IgnorePkg`/`IgnoreGroup` empty (version pins) and `NoUpgrade`/`NoExtract` empty (file-extraction rules, not version pins); `HoldPkg = pacman glibc` (`:208-216`) | identical (all four rc=0 empty; HoldPkg two lines) | same |

The verdict `same` stands: the r2 and v2 readings are identical and all four directives are empty
on this host (re-measured 2026-10-23 by round-35 wave-1 `ExecHostPacnew`; re-measured read-only
2026-10-24T03:08:20Z). `corpus/knowledge/pacman-backup-files-r35.md:32` records the same: "the
values those entries recorded … stand".
```

## Block notes

- No line starts with `recheck:`, `source:` or `verified-at:`; the operative trio (`:364-366`) and
  the operative `recheck:` line (`:366`) are unchanged.
- The heading differs from the only registered heading for this path
  (`## R18-FRESHNESS — sibling current-use restatements (2026-10-20)`) and from both
  `## R1[78]-RECHECK — steer-safe procedure` headings.
- No `$ command` line; no backticked invocation of a forbidden binary.
