VERDICT: supports

## C1-12 — axis fit, reachability, sizing

**Axis fit:** supports operability. This is not merely making the command execute: it corrects whether the already-running boot-chain gate reports the stated condition. At the base, `boot_inputs_newer` runs `find … | grep -q .` under `pipefail` (base source `tools/boot-chain-audit.sh:480-487`); a missing operand can make `find` exit nonzero despite a matching line, causing the `if` to choose 0. That false “no newer inputs” value permits the `booted` assignment only when `newer=0` (`tools/boot-chain-audit.sh:758-773`), after which `verdict_for` emits `BOOTED-OBSERVED` for `booted=1` (`:624-634`). The current helper instead decides from captured find output (`:463-475`), preserving a detected match despite find's status. This directly improves the check's declared output semantics, not just internal robustness.

**Reachability on this host:** the hazard is reachable. `pacman -Qo` was run against all eight production start points. Output:

```
error: openai-chatgpt: missing required signature
error: No package owns /etc/default/grub
error: No package owns /etc/kernel/cmdline
/etc/crypttab is owned by filesystem 2025.10.12-1
/etc/limine-snapper-sync.conf is owned by limine-snapper-sync 1.32.1-2
/etc/mkinitcpio.conf is owned by mkinitcpio 42.2-1
/usr/lib/initcpio/ is owned by btrfs-progs 7.1-1
/usr/lib/initcpio/ is owned by limine-mkinitcpio-hook 1.40.0-2
/usr/lib/initcpio/ is owned by mkinitcpio 42.2-1
/usr/lib/initcpio/ is owned by mkinitcpio-busybox 1.36.1-1
/usr/lib/initcpio/ is owned by plymouth 26.134.222-3
/usr/lib/modules/ is owned by linux 7.2.11.arch1-1
/usr/lib/modules/ is owned by linux-headers 7.2.11.arch1-1
/usr/lib/modules/ is owned by linux-lts 6.18.57-2
/usr/lib/modules/ is owned by linux-lts-headers 6.18.57-2
/etc/fstab is owned by filesystem 2025.10.12-1
```

The checked set is `/etc/fstab`, `/etc/crypttab`, `/etc/mkinitcpio.conf`, `/etc/mkinitcpio.conf.d`, `/etc/default/limine`, `/etc/limine-snapper-sync.conf`, `/usr/lib/initcpio`, `/usr/lib/modules` (`boot-chain-audit.sh:494-496`). Of these, `/etc/crypttab` and `/etc/limine-snapper-sync.conf` are present and package-owned on this host; no absence is established for either here. The attempted query was `pacman -Qo` on every listed path. Its combined command returned 2 because pacman printed a missing-signature error and reported no owner for `/etc/default/grub` and `/etc/kernel/cmdline`, which are not members of the eight-point set. Thus this invocation does **not** establish whether `/etc/mkinitcpio.conf.d` or `/etc/default/limine` exist/are optional; `pacman -Qo` is ownership evidence, not a universal existence test. The direct source and case design do establish that the implementation treats any missing start point as possible: selftests explicitly call the helper with a missing path and a deeper existing path (`candidate-boot-chain-audit.sh:1225-1237`).

**Verdict change:** yes, the narrow condition changes at the production predicate when one start point is missing and a *different* reachable input is newer. For `/etc/crypttab` missing and `/usr/lib/modules/<newer-file>` present, `find` can print the newer file while reporting the missing operand; under the base pipeline and `set -o pipefail`, the pipeline status is false, so `boot_inputs_newer` returns 0. The helper's `hit=$(find ...)` retains the matching output, so it returns 1 (`boot-chain-audit.sh:463-475,494-496`; base source `tools/boot-chain-audit.sh:480-487`). Then the actual audit's `newer=0` condition is no longer met (`:758-773`), hence it cannot set `booted=1`, and `verdict_for` cannot return `BOOTED-OBSERVED` by that route (`:631-634`). This conclusion is grounded in the cited code and the exact failure mechanism; I did not run the two-revision private-namespace end-to-end audit in this seat. The static `verdict_for` function itself does not inspect paths or change between revisions; it receives the changed `booted` input. That distinction matters: the defect is in supplying the predicate, not in verdict precedence.

**Sizing / do-nothing control:** the fix is appropriately bounded to a small helper, its call site, and targeted selftests; the frozen counter also requires all 16 production-path cases and the independent live agreement plus selftest conditions (`tools/score-bootinputs-r43.py:10-33,331-335`). A do-nothing base control cannot satisfy the target: the base pipeline demonstrably contains the fail-open, while the new regression cases include `R43-C1-missing-start-point-deep-newer` expected 1 (`candidate-boot-chain-audit.sh:1225-1237`). Counter evidence available in the declared pre-data battery likewise shows a no-fix variant K6 failed with 12/16 correct, while K7 is the declared passing mount-table-gated control (`controls/C1-K6.jsonl:1-2`; task context specifies K7 PASS). This supports a meaningful, non-token target rather than merely adding tests or accepting a no-op. I did not independently rerun the counter or audit. The optional-path premise is plausible and relevant, but the specific example “crypttab absent without LUKS” remains a general scenario, not a state observed on this host.

## Smallest safe correction

Keep the fix as scoped: make the helper's result depend on whether `find` emitted a match, not on its aggregate exit status, while retaining all eight start points and the current boot verdict contract. Do not remove optional paths or alter `verdict_for`; add/retain an end-to-end missing-start-plus-newer test if not already covered by independent reproduction.
