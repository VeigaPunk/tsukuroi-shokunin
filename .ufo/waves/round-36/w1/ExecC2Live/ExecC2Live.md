# ExecC2Live — C2 journalctl v262 live verification

## Result

On this host, `journalctl --version` first line was `systemd 262 (262-1-arch)`. The limiting-option behavior is live-confirmed read-only: field mode rejects limiting selectors with exit 1, no stdout, 84 stderr bytes, and the exact diagnostic:

> `-F/--field= and -N/--fields cannot be combined with options that limit the journal.`

The plain `journalctl --no-pager -F PRIORITY` query succeeded (exit 0, stderr 0; stdout tail `5, 6, 2, 4, 7, 3`). The requested `-F` cases with `-b`, `-p err`, `--since`, or `-u` all rejected with the exact diagnostic. `journalctl --list-boots` showed `-1` exists, so the previous-boot matrix cell was run and rejected too.

Important `-N` syntax qualification: the two requested forms `-N PRIORITY,MESSAGE` and `-N PRIORITY` both fail as extraneous positional arguments (stderr 54 and 46 bytes respectively), not as limit-conflict cases. A correct no-argument `journalctl --no-pager -N` succeeds; `journalctl --no-pager -b 0 -N` rejects with the exact 84-byte limit-conflict diagnostic. Extra controls show `--quiet` and `-o json` alone work with `-F`, while `-p err` alone rejects; thus the `-b` matrix cells containing `--quiet`/`-o json` do not establish those options as the cause.

## Lane sweep

The recursive `.py`/`.sh` `journalctl` search plus direct `JOURNALCTL` call-site review found no fixed `-F`, `--field`, `-N` or `--fields` invocation. All 12 executable census call sites in `tools/tsukuroi-census.sh` use other journal modes and are outside this field-list incompatibility; their exact line, flag set and structural verdict are in `matrix.md`. The three live wrapper branches in `tools/score-census-handoff-r32.py:713,715,717` pass caller arguments through dynamically; the census callers reviewed do not supply `-F/-N`. Other grep hits were fixture, stub, setup or lint text, not live calls. Source-call verdicts are structural; those call sites were not separately run during this matrix capture.

## Retained evidence

- `matrix.json` — machine-readable version, boot availability, requested matrix and controls, with argv, stdout tails/byte and line counts, stderr byte counts/tails, exit codes and verdicts.
- `matrix.md` — readable matrix, exact rejection diagnostic, valid `-N` controls, and complete tool invocation sweep with file:line and flag sets.

The declaration's C2 statement is confirmed against the live v262 behavior, with the `-N` argument-shape caveat explicitly retained. No production tools, corpus, scorecard, or source registry files were changed. No package, service, or privileged action was taken.

## Risks and blockers

No blocker for the assigned live-verification deliverable. The specified `-N` matrix cells are malformed for testing the limit rejection; the extra valid `-N` controls resolve that gap. The lane-call sweep establishes absence of a field-list conflict, not live success of every unrelated journal command. No package/tool installation was performed.