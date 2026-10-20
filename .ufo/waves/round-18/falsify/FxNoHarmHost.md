# FxNoHarmHost — no-harm attack: R18 capture scripts/tools/clones (read-only seat)

Axes: host-write vectors (pacman/service/boot/sudo); local-artifact vs host-state separation; execution-evidence honesty; selftest hermeticity. All reads at working tree with `.git/HEAD` = `68a8ae035fde33360cbbe21dc92ca0eacf0a5b33`.

**Verdict: SURVIVES code-level for every audited artifact; no FAILS. Round-wide executed absence UNPROVEN by design.**

1. `.ufo/waves/round-18/l1-capture/capture-r18.sh` (43 lines): 21 fixed probes, all reads — `cat /proc|/sys`, `systemctl is-active/is-enabled/show`, `ls/stat/wc/tail/grep` over /var/lib/pacman, /var/log, /etc/snapper, /usr/share/pacman, `dkms status`, findmnt. Zero forbidden binaries, no sudo, no /boot, no writes (`run()`: printf + `bash -c` only).
2. Harness invocation (`harness-probe-capture.json` record `e6ad937b`): `{ … } > host-capture-r18.txt; chmod +x capture-r18.sh` — lane-local artifact writes (content + mode bit), not host state. Output log shows exactly those 21 probes with rc.
3. `measure/run.py`: `git clone --no-hardlinks` → tempdir, origin removed, checkout TIP; git writes clone-local; `PYTHONDONTWRITEBYTECODE=1`; outputs to `measure/`. One out-of-lane exec: `scripts/sources-census.sh validate` — read-only, stdout-only (writes only via `--out`; conf parsed textually; sourcing canary selftest). `measure/census-start.txt` is that output (S038–S058 W04, `ok`, exit=0), NOT a live census — no pacman.
4. `tools/*.py`: subprocess = git read/plumbing + temp-repo selftests; shutil confined to own tempdirs; all `_revision` importers set `sys.dont_write_bytecode` before import (e.g. check-boot-chain.py:53, check-root-dac-correction.py:28) — no `tools/__pycache__` lane mutation.
5. `tools/boot-chain-audit.sh`: sudo only `sudo -n stat -c %Y` (:256,:258) and `sudo -n cat` redirected into `$WORK` (:257,:1277); `guarded_rm` validates confinement before chmod/rm (:152-163; selftest refuses /etc/passwd :973); `work_path` refuses `..`/absolute (:190-197). No pacman/systemctl/mkinitcpio execution; `--live` was not invoked this round (run.py runs `--selftest` only) — but executing it would be a host probe under seat rules.
6. `tools/tsukuroi-census.sh`: query verbs only; selftest dispatches before any live probe (:2632-2635), /tmp fixture with zero-mutation asserts.

UNPROVEN: (a) absence of pacman/sudo/service/boot actions beyond the one harness-bound wrapper — lesson's "Host safety read-only throughout" outruns its evidence (acknowledged wrapper limit); (b) tracked mode bit vs post-`chmod +x` tree, and script sha256 `bfe32ba3…` vs committed bytes — needs execution, not run; (c) sibling falsify clones not audited (owner seats); (d) lsp device unavailable → text-grep fallback used.

No tools installed.

Scope: executed=none
