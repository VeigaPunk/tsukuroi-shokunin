## Module-parameter surface — decision table (round 71)

Read-only decision table for an observed `/sys/module/<name>/parameters/<p>` shape. Every row rests on a
rule row of `corpus/knowledge/module-parameter-plane-r71.md` (MP1-MP6; sources S297-S300, Linux stable
v7.2.11). **No row authorizes a write:** the lane reads and records; every write named in a right-hand
column is the operator's and is never executed, attempted or retried by this lane. Detection and report
only, as the province's `Refuses` line requires — no module internals, no reverse engineering.

| # | Observed shape (read-only probe) | Verdict | Operator action | Rests on |
|---|---|---|---|---|
| S1 | A `-r--r--r--` file whose value reads `Y` or `N`, e.g. `nvidia_drm/parameters/modeset` = `Y` | READ-ONLY PARAMETER, readable: `get` answered, the mode carries no write bit, and no store handler was registered | Record mode and value. A different value needs a command-line or modprobe route plus a reload, both operator-owned; never write the file | MP2 (visibility: MP1) |
| S2 | A `-rw-r--r--` file whose value is readable, while an unprivileged write returns `EACCES` | ROOT-WRITABLE PARAMETER: a store handler exists and the mode is the parameter's `perm`; the unprivileged refusal is the mode, not a missing handler | Record the mode. The write is the operator's; the lane never performs or retries it | MP2 |
| S3 | The named parameter file is absent while `/sys/module/<name>/` exists | INVISIBLE BY `perm == 0`: the parameter is declared but publishes no sysfs file, so absence is not emptiness (host case: `btrfs` `read_policy`) | Record `absent (perm 0)`; consult the declaration or the command-line route; do not report a missing or unknown parameter | MP1 |
| S4 | `/sys/module/<name>/` itself is absent | NOT LOADED: there is no parameters directory at all, so the parameter set cannot be enumerated from sysfs | Record the absence; loading or unloading is operator-owned and out of the lane's scope | MP1 |
| S5 | A read of a mode-`0444` file returns `EPERM` rather than `EACCES` | NO GET HANDLER: the mode is not readability, and `get` is optional, so a visible parameter can refuse every read | Record `EPERM` as a source-contract shape, not a permission fault; do not retry with privilege | MP3 |
| S6 | The kernel ring carries `<mod>: unknown parameter '<x>' ignored` | TYPO, LOAD SURVIVED: an unmatched name is warned and ignored, so a mistyped parameter silently did not take effect | Record the exact token and the module; correcting the route is operator-owned | MP4 |
| S7 | The kernel ring carries `<mod>: '<v>' invalid for parameter '<p>'` and the load was refused | VALUE REJECTED, LOAD FAILED: a known parameter's `set` returned a negative errno, which aborts the load, unlike S6 | Record the parameter and the value text; the correction is the operator's | MP3 (contrast: MP4) |
| S8 | The kernel ring carries `Module <name> is blacklisted` and the load was refused | BLACKLISTED: the check refuses the load before parameters matter, so no parameters directory ever appears | Record the name and the refusal; blacklist changes are operator-owned | MP5 |
| S9 | `/proc/cmdline` carries `mod.param=v`, or carries no `mod.` token while the loaded module holds the value | ROUTE: the command-line route is attributable by token presence; modprobe is the documented alternative, and built-in code reaches its parameters only from the command line | Record the route and the token; a modprobe fragment edit is operator-owned, and fragment contents are never read | MP6 |

Named limits, not table rows: a writable mode does not prove a store will be accepted — a parameter can
still refuse with `EPERM` through the source's unsafe-parameter check, which MP1-MP6 do not describe; the
value vocabulary (`Y`/`N`, a decimal, `(null)`) is what the source's `get` implementations print and is not
a claimed contract; and S4's premise is that the parameters path exists only for a name the kernel holds as
a module, which is MP1's subject rather than an additional rule.
