# Draft registry row for tools/probe-child-env-allowlist-r33.py

Status: draft only. Not applied to SKILL.md. Frozen predicate and probe bytes stay at 9c89ff4f093d07a6f92925518310ca6a7c8a2fa0.

Operative heading at that commit: `## Gate and probe registry — round32 superseding current rows` (SKILL.md:2756). It is the unique highest heading of the form the coverage gate selects. It has 47 data rows (SKILL.md:2766-2812) and does not name this probe.

The landing heading, same form, next number:

## Gate and probe registry — round33 superseding current rows

Copy the 47 data rows at SKILL.md:2766-2812 verbatim under a new header of the same eight columns. Do not edit those cells. Append this one row. A heading that omits `superseding current rows`, or a second heading with the same number, is not a selected table. A round33 table that does not repeat the 47 rows leaves those tools REGISTRY-ROW-MISSING, because the gate reads only the highest table.

| child-env-allowlist-r33 | probe | `python3 tools/probe-child-env-allowlist-r33.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--set claim\|regression] [--only <tool> ...]` | 0 when leaking is 0 and harness_errors is empty;1 when a pair leaks;2 on a harness error | none: no self-test mode; the five-target claim set and channels names, quiet and source are the measurement | R33 C1 probe v3 frozen at 9c89ff4f093d07a6f92925518310ca6a7c8a2fa0, sha256 c24f344b864a13ea4db2909bfa81de77f8f41bae35cd5e0949a88b28ab1e04cd; claim set 5 targets, channels names, quiet, source, 15 pairs; label leaking; `--set regression` is repair evidence, not the claim | private mkdtemp (default `/fast/scratch/hyaku` when that directory exists), bare clone and strace, removed at exit; refuses a scratch inside the lane | tsukuroi |

Cell notes, from the probe at that commit (not a second row):

- Kind `probe` requires verdict digits 0 and 2 as standalone numbers (`tools/check-registry-coverage.py` VERDICT_ZERO and VERDICT_TWO). Exit mapping is `tools/probe-child-env-allowlist-r33.py:102-103` and `:878`.
- The self-test cell must not contain `--selftest` or `--self-test`. The probe's argparse (`:760-765`) has no self-test flag. The twelve `--selftest` strings in the file are target argv and docstring text, not a mode of this probe.
- Entry and self-test cells name only `tools/probe-child-env-allowlist-r33.py`. A second `tools/` path in either cell is REGISTRY-ROW-AMBIGUOUS.
- The pipe in `claim|regression` is escaped so the row stays eight cells.
