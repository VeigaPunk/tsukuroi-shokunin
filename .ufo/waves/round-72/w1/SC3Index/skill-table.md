### Decision table — the modprobe configuration surface (round 72)

Read-only decision table for an observed `modprobe.d` shape. Every row rests on a rule row of
`corpus/knowledge/modprobe-config-plane-r72.md` (MD1-MD6; sources S301-S303, kmod v34, host kmod 34.2);
the cross-reference MP5 belongs to `corpus/knowledge/module-parameter-plane-r71.md`. **No row authorizes a
write, a load or a blacklist change:** the lane reads paths, modes and names and records them; every
action named in a right-hand column is the operator's and is never executed, attempted or retried by this
lane. Fragment contents are not read — the table therefore never states which line is effective.

| # | Observed shape (read-only probe) | Verdict | Operator action | Rests on |
|---|---|---|---|---|
| T1 | The same `.conf` basename in two configuration directories, e.g. `nvidia.conf` under `/etc/modprobe.d` and under `/usr/lib/modprobe.d` | ONE COPY, HIGHER PRECEDENCE WINS: the first directory in SYNOPSIS order loads the name, and every later same-name file is ignored; the copies are not merged, and libkmod's sorted insertion would reject the duplicate anyway | Edit the higher-precedence copy (the `/etc` one here); the later copy is inert while the duplicate exists. Never assume both files contribute lines | MD1; MD3 |
| T2 | `/lib/modprobe.d` and `/usr/lib/modprobe.d` both appear in the directory list while `/lib` resolves to `/usr/lib` | ONE DIRECTORY BEHIND TWO PATHS: the second listing presents the same names, which the sorted filename list rejects as duplicates, so nothing is parsed twice; counting files per SYNOPSIS entry double-counts | Resolve the path (`readlink -f`) before counting or naming a fragment; edit the single real file | MD1; MD3 |
| T3 | An `install` line exists for a module name | COMMAND, NOT A LOAD: an install line makes modprobe run the configured shell command instead of inserting the module; under `-n` no command executes, and the planned line appears only when the show path is on (`-v` or `-D`) | Read the command before relying on a load (an operator-owned content read); the lane records that an install line exists, never what it says | MD5 |
| T4 | A `blacklist <name>` line exists and the same module is requested by its real name | ALIAS-ONLY SUPPRESSION: blacklist hides the module's internal aliases, so `modprobe <real-name>` still loads it; only `--use-blacklist` adds the unconditional probe flag | Decide the intent: alias suppression (leave the blacklist) versus load refusal (needs the kernel `module_blacklist=` route — MP5 of the r71 note — or an install command); both are operator-owned | MD6 |
| T5 | A `softdep <module> pre: <list> post: <list>` line exists | ORDER DECIDES WHICH FRAGMENT'S LINE SURVIVES: softdep lines are read in the same single lexicographic pass, and a later-ordered file partially replaces an earlier one; whether a given softdep is in force cannot be read from the surface without contents | Read the fragments, or have the operator run `modprobe -c` (which prints the parsed softdep entries); the lane records paths and names only | MD2; MD1 |
| T6 | The operator asks what `modprobe -n <name>` would do | DRY RUN SUPPRESSES EXECUTION: `-n` sets the dry-run flag; the remove path returns before `system()`, and the probe is called with the dry-run probe flag. Plan text is emitted through the same show path that `-v`/`-D` enable, so `-n` alone guarantees suppression, not a printed line for every action — and a plan line is not proof the action would succeed | The operator runs it; the lane records the no-execution contract and never executes modprobe | MD5 |
| T7 | `/proc/cmdline` carries a `module.parameter=value` token | PARSED AFTER THE FILES: the command line enters the same configuration object after every configuration file; the lane can state that order, not that the token overrides a file line | Record the token; if a specific value matters, the operator checks the parsed configuration (`modprobe -c`) and the running value under `/sys/module/<name>/parameters/` (MP6 of the r71 note) | MD4 |

Named limits, not table rows: the surface yields paths, modes and filenames, never contents, so no row
states an effective value or which of two fragments' lines wins in fact; `MODPROBE_OPTIONS` can alter the
directory list (the manual's NOTE) and the lane does not read it, so the SYNOPSIS order is the documented
default and not a measured per-invocation order; a blacklist refusal is a kernel load event (MP5), not
observable from the configuration surface; `weakdep` and `remove` are documented in the manual but are not
rule rows of the entry, so no row cites them as such; and the plan-printing channel is conditional —
`-n` sets only the dry-run flag (`modprobe.c:836-838`), `do_show` is set by `-D` (`:819-822`), and `SHOW`
returns early unless `do_show` is set or `verbose` exceeds the default (`:150`), so an empty `-n` output is
not an empty plan. The snapshot set carries no `libkmod-module.c`, so what the dry-run probe flag does to
an install command inside libkmod is named from the documented behaviour (MD5) and not read here.
