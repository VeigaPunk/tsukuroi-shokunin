# FxCorrection4

Axes: defect fidelity; capture scope; independent semantic enforcement.

**SURVIVES — correction fact.** The baseline sentence at `corpus/knowledge/boot-chain-r17.md:88-89` assigned mtime `09:26:22` to the history-copy citation B:115. Capture B:110-124 identifies B:115 as the `limine_history` copy (`09:29:18`) and B:124 under `/boot/EFI/Linux` as live `omarchy_linux.efi` (`09:26:22`). The correction at `boot-chain-r17.md:221-225` fixes that citation and preserves byte-identity: B:171 and B:219 both carry SHA-256 `2e9c9bdc…079fe8`; each file is 284439552 bytes (B:115,124). S051 (`corpus/SOURCES.md:57`) is a dated host capture, not a boot test.

B:59 is the complete pacman argv with 12 package names; B:82 is truncated at `linux-lts`. Separately, the fixed C1 checks compare both UKIs and installed files: `init` B:182/198/251 (`62fcc3a9…`); btrfs hook B:183/199/252 (`eeac1ed3…`); plymouth B:184/200/253 (`de852646…`).

**FAILS — medium, checker scope.** `--statement-corrections` independently fixes the CORR-04 metadata/notice and checks B:124/B:115 timestamps and filename prefixes (`tools/check-boot-chain.py:99-106,640-650`). It does **not** compare the byte-identity hashes at B:171/B:219; a mismatch there can pass this item while the fixed notice still asserts identity. The wrong-B:115 notice fixture expects CORR-04 unresolved (`1450-1459`). Baseline-without-notices fixture expects count 0, four named unresolved IDs and FAIL/code 1 (`1464-1467`, `PASS/FAIL/CANNOT=0/1/2` at 56); static expectation only, not run.

**Verification gaps.** No LSP device is exposed, so status/references/definition/diagnostics were unavailable; no execution or tests. Scope: executed=none