# Append-block draft — target `corpus/knowledge/update-safety-v2.md`, site `:198`

Seat: `ScribeNoUpgrade` (round 36, wave 1, routed repair 4).
Target (lane-relative): `corpus/knowledge/update-safety-v2.md`
Site: line 198 (one table row in §5 "Pins and holds, re-run [observed]", heading at :193)
Base commit read: `6d76fb20f6ecbc940e5c8fff36c74060c885e161` (declaration); file digests below at `189d8a080ba8d508d5faab12cad9e688aee91dab`
Target sha256 at that commit: `caa747e657527c5c29ceb93bfcc86791b53277e85cfd9b82bc804c0ba0e6895d` (420 lines)

## Landing instruction (for the L1)

**Append at the END of the file**, in the same EOF append as the `:52` block (order between the two
blocks does not matter; each starts with its own `## ` heading). Do not edit the row. Evidence
(verified):

- Same r18 registry pressure as the `:52` site: 8 records on this path, baseline `842a5312...`,
  `NOTICE-HISTORY` requires the target bytes to start with the baseline bytes; a mid-file insert
  at 198 would break that and would also shift every later citation (`:244`, `:244-260`, `:357`).
- The block starts with a `## ` heading, so the operative steer-safe section
  (`## R18-RECHECK — steer-safe procedure`, `:412`, currently running to EOF) is terminated at the
  same place and its command scan is unchanged.

## Verbatim original (quoted; NOT to be rewritten)

> | any | `pacman-conf IgnorePkg` / `IgnoreGroup` / `NoUpgrade` / `NoExtract` | all empty rc=0 — no version pins |

The table's columns are `| source | probe | value |` and the section heading above it is
`## 5. Pins and holds, re-run [observed]` (`:193`). The defect is the value cell `all empty rc=0 —
no version pins`, read as the verdict for a four-directive probe of two classes.

## Append block (paste at EOF, verbatim)

```markdown
## R36-SUPERSESSION — §5 row: the `no version pins` verdict covers two directive classes (2026-10-24)

Appended in round 36 as routed repair 4 (`corpus/lessons/round-35-verifier-spotcheck.md` §6 item 4).
The row above is preserved unchanged; this block supersedes its value cell. Prior locus (`:198`),
verbatim:

> | any | `pacman-conf IgnorePkg` / `IgnoreGroup` / `NoUpgrade` / `NoExtract` | all empty rc=0 — no version pins |

Superseded as a classification by `corpus/knowledge/pacman-backup-files-r35.md`
(§ `[obs] NoUpgrade and NoExtract (S191, S195)`; S191 pacman `lib/libalpm/add.c` at 54d94116164b,
S195 pacman `doc/pacman.conf.5.asciidoc` at 54d94116164b): of the four probed directives,
`IgnorePkg` / `IgnoreGroup` are the version pins (S195 lines 102-109, "ignore any upgrades … when
performing a '--sysupgrade'") and `NoUpgrade` / `NoExtract` are file-extraction rules over package
archive paths (S195 lines 136-137 and 147-148; S191 lines 223-230, 302-304, 338-350). The reading
`all empty rc=0` is correct and unchanged.

Replacement value cell:

> all empty rc=0 — no version pins (`IgnorePkg`/`IgnoreGroup`) and no file-extraction rules
> (`NoUpgrade`/`NoExtract`)

Values stand: the four directives are empty on this host (re-measured 2026-10-23 by round-35
wave-1 `ExecHostPacnew`; re-measured read-only 2026-10-24T03:08:20Z; `/etc/pacman.conf` carries
only `HoldPkg = pacman glibc` at line 7).
```

## Block notes

- No line starts with `recheck:`, `source:` or `verified-at:`; the operative trio (`:364-366`) and
  operative `recheck:` line (`:366`) are unchanged.
- Heading unique in the file; not one of the registered `R18-FRESHNESS` headings and not one of the
  two `R1[78]-RECHECK — steer-safe procedure` headings.
