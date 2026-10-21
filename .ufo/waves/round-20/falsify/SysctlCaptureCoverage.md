# R20 systemctl retained-capture coverage

## Scope and evidence

Compared the R17–R19 captures cited by round-20 build reports with the bound execscope candidate `/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py` and its source fixtures. The final measurement source checks only the R19, R19b, and R19c captures (`.ufo/waves/round-20/measure/run.py:95-98`); the classifier assesses only lines beginning `$ ` (`candidate:654-668`). R17/R18 parity is therefore encoded in fixtures, not a final capture check.

The candidate’s finite read verb set includes `list-dependencies` and all read verbs seen in the cited captures (`candidate:276-278`); its option sets include the observed `--reverse`, `--no-pager`, `--failed`, `--wait`, and `-p` forms (`:279-285`). The parser keeps the first non-option token as the verb and defaults a missing verb to `list-units` (`:289-331`).

## Capture comparison

| Retained evidence | Comparison with candidate table and fixtures |
|---|---|
| R17 `fresh-capture.txt:47` (`is-enabled` over four units) | `is-enabled` is in the read table (`candidate:278`), but no positive fixture in the complete systemctl fixture block (`:1457-1513`) exercises `is-enabled`. This is a fixture gap, not an unsupported table verb. |
| R17 `fresh-capture.txt:52` (`is-system-running; systemctl --failed --no-legend \| wc -l`) | Both segments are represented: the no-verb `--failed --no-legend` form is explicitly in the read fixture at `candidate:1475`, and `is-system-running --wait` at `:1476`. The default-to-`list-units` path is at `:331`. |
| R18 `host-capture-r18.txt:16` (`is-active; is-enabled`) | The `is-active` control is present at `candidate:1473`; `is-enabled` is again tabled but untested (see above). |
| R18 `host-capture-r18.txt:20` (`show … -p … -p … --no-pager`) | `show` and value-taking `-p`/`--no-pager` are recognized (`candidate:276-285,308-331`), but the fixture uses one `--property=Id` at `:1470-1472` and plain `show` at `:1481`. Repeated short `-p` options with trailing `--no-pager` are not fixture-pinned. |
| R19 `host-capture-r19.txt:153,191,208,215,220,262` (`cat`, `list-unit-files`, `show`, `list-dependencies`, `cat`, `list-timers`) | Every observed verb is in the current table. The exact dependency command at `:215` has an exact clean-control fixture at `candidate:1484`; this resolves the omission described by older build reports. Other fixture forms are close but not exact: `cat` uses one unit and omits `--no-pager` (`:1480`); `list-unit-files` tests `--type=timer` rather than the captured two unit-file patterns (`:1477`); `show` does not repeat `-p`; `list-timers` tests `--all` but not the captured quoted pattern plus `--no-pager` (`:1479,1482`). These are fixture gaps for exact capture syntax, not table-level unsupported verbs/options. |
| R19b `host-capture-r19b.txt:13,183,206` | The `$ ` command is `cat -n` on a README (`:13`); the `systemctl enable --now` strings at `:183,206` are README lines printed by that command, not direct `$ systemctl` invocations. The classifier’s `$ `-line boundary (`candidate:658-663`) keeps them inert. |
| R19c `host-capture-r19c.txt:22,38` and `:32` | The `$ ` commands at `:22,38` are journalctl/grep/sed/cut pipelines; the `systemctl` text in the grep pattern is not a command word. Separately, output line `:32` records a historical `COMMAND=/usr/bin/systemctl enable --now snapper-timeline.timer snapper-cleanup.timer`. That is captured evidence of an effectful form, but it is output of the journal pipeline, not a `$ ` invocation for this classifier. |

## Findings

1. **No unsupported observed read verb remains in the inspected candidate table.** In particular, current candidate lines `276-282` include `list-dependencies` and `--reverse`, and fixture `:1484` matches the retained R19 command exactly. The contrary missing-`list-dependencies` findings in `build/ExecReadOnly.md:5`, `build/ExecMutating.md:7-9`, and `build/ExecUnknown.md:29-41` describe a different/earlier candidate state. The current fixture also contains all four user-scoped read controls at `:1480-1483`, contrary to the earlier `ExecReadOnly.md:7` gap.

2. **Observed `is-enabled` reads lack a fixture.** The R17/R18 captures contain `is-enabled` (`round-17/l1-capture/fresh-capture.txt:47`; `round-18/l1-capture/host-capture-r18.txt:16`); the table admits it (`candidate:278`), but the current fixture block `:1457-1513` has no `is-enabled` read. Add a clean control if exact retained-read coverage is required.

3. **The captured effectful `enable --now` form lacks a combined negative fixture.** R19c records it at `host-capture-r19c.txt:32`. Candidate mutation controls cover `restart`, bare `enable`, and `daemon-reload` (`:1457-1465`); the ambiguous/effectful block separately tests `status --now`, bare user `enable`, and `--runtime restart show` (`:1498-1513`), but not `enable --now`. The classifier is source-inferred to reject the observed command when supplied as an inert `$ sudo /usr/bin/systemctl enable --now …` fixture because `enable` is not a read verb and `--now` is not an allowed read option (`:276-285,308-331`); that inference is not a test result. `build/ExecUnknown.md:130-133` also explicitly names an `enable --now` negative expectation.

4. **Two further mutation controls named by the build review are absent.** `build/ExecMutating.md:13-21` calls for `kill` and `set-property` negative controls; candidate fixtures `:1457-1513` contain neither. The finite allowlist should reject these as non-read verbs (`:276-278,328-331`), but the forms are not fixture-tested. The candidate’s mutation assertions are aggregate cases, not isolated per-command outcomes (`:1462-1465,1509-1513`).

5. **The older `--runtime` finding does not match the inspected candidate.** `build/ExecOptions.md:3-9` says `--runtime` is value-taking and can hide `restart`; current candidate puts it in `SYSTEMCTL_READ_FLAGS`, not `SYSTEMCTL_VALUE_FLAGS` (`:279-285`), and includes `$ systemctl --runtime restart show …` in its negative fixture (`:1505`, aggregate expectation `:1509-1513`). This is a stale report against the current source snapshot, not a reproduced gap.

## Limits and remaining unknowns

These findings distinguish source/fixture contents from executed outcomes. No candidate fixture, test, measurement, command, host probe, or external request was run. The available tool surface exposed no LSP device/server, so references and caller links were traced from source lines, not semantic LSP results. The finite classifier is bounded to `$ ` command text and the existing parser; a clean classification does not establish shell equivalence or runtime enforcement. No host or boot-safety claim is made; boot images remain UNKNOWN.

Scope: executed=none