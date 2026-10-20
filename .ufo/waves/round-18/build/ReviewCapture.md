# ReviewCapture

## Verdict

- **SURVIVES — host-state read-only.** [obs] `capture-r18.sh:8-29` probes time, `/proc`, `/sys`, systemd state, package metadata/logs, configuration listings, DKMS status and mount state. No package/service/boot mutation or forbidden executable invocation appears. `run` executes the hard-coded probe strings (`capture-r18.sh:7`).
- **FAILS if “read-only” means the entire capture workflow makes no writes.** [obs] The recorded harness call (`l1-capture/harness-probe-capture.json:13`) runs `chmod +x capture-r18.sh` and redirects `>` to `host-capture-r18.txt`, overwriting/creating the local artifact. This does not show mutation of probed host state.
- **UNPROVEN — independent provenance.** [obs] The capture header asserts a script SHA-256 (`host-capture-r18.txt:1`); the harness excerpt records an invocation/result (`harness-probe-capture.json:13`) but explicitly says it is “not an exhaustive shell audit” (`:55`). Printed `$ command` lines are script output (`capture-r18.sh:7`), not an independent execution trace. [unk] Independent authenticity and binding to the stated baseline/prerequisite; no hash or revision comparison was performed.
- **UNPROVEN — downstream precision.** [obs] `capture-r18.sh:14` and `host-capture-r18.txt:24-25` count `ls` output lines other than `ALPM_DB_VERSION`; this supports 1,395 listed local-DB entries, not an independently verified `pacman -Q` package count. The log tail ends with `pacman -D --asexplicit` at 13:23:09 (`host-capture-r18.txt:63-65`); the last displayed `pacman -U` is at 13:23:08 (`:70-73`). The capture establishes the latest shown log event, not a package-install transaction at 13:23:09.

## Residual risk / verification gaps

[obs] `run` records only the overall `bash -c` status; semicolon/pipeline members have no separate statuses (`capture-r18.sh:7,12,14,21-22`). Command/output pairs are useful evidence, but not a full audit trace.

Scope: executed=none