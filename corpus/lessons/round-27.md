# Round 27 — lesson (tsukuroi, attempt 1, 2026-10-22)

author: TsukuroiR27 (L1). Claim base `3beab8ddcf4ed2ae9fdf12eab6ac7f840c74e333`; declaration `db9eecfa876a865f799aa56856a780d299b4f067`; C1 counter `tools/check-kernel-taint.py` committed before any C1 data at `75f410c825a941f819717e4183bcc82f9c368469` (sha256 `bd307d33bd9d4960f2dd1dcf7f0921534937e98c9d4b5769fed0097da3c6e23a`, 46-case selftest PASS, receipt `.ufo/waves/round-27/kt-selftest.json`). The seven canonical protocol files are byte-identical to the digests recorded in the round-26 declaration.

Wave-1 note: all 23 scribe and executor seats of wave 1 died at spawn with "Error: No model selected." (the operator-owned route for those roles is down). They were not replaced or rerouted. The L1 opened every source below and drafted every row itself; no Gate row comes from a seat.

## Gate

Candidates considered: Linux v7.2 `Documentation/admin-guide/tainted-kernels.rst`, `kernel/panic.c`, `include/linux/panic.h`, `kernel/module/main.c`, `kernel/module/signing.c` and `Documentation/admin-guide/module-signing.rst`, all fetched by plain curl from raw.githubusercontent.com at tag v7.2 (the host runs 7.2.11-arch1-1). Every quote below was checked by the L1 as a whitespace-normalised substring of the committed snapshot under `.ufo/waves/round-27/sources/` (`/fast/scratch/hyaku/tsuku27/build_c1.py` exits non-zero on a miss), and its line is the first line of the match.

Admitted rows (all `mined`, tier A, opened 2026-10-22, recheck `on-release`, used-by `corpus/knowledge/kernel-taint-r27.md`): S140 to S145.

| Source | URL | Opened | Located quote (at most 25 words) | Location |
|---|---|---|---|---|
| S140 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/tainted-kernels.rst | 2026-10-22 | If that returns ``0``, the kernel is not tainted; any other number indicates the reasons why it is. | Documentation/admin-guide/tainted-kernels.rst line 51, entry row KT1 |
| S142 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/panic.h | 2026-10-22 | #define TAINT_OOT_MODULE 12 | include/linux/panic.h line 83, entry row KT1 |
| S142 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/panic.h | 2026-10-22 | #define TAINT_UNSIGNED_MODULE 13 | include/linux/panic.h line 84, entry row KT1 |
| S143 | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/module/main.c | 2026-10-22 | `if (!get_modinfo(info, "intree")) {` | kernel/module/main.c line 2575, entry row KT2 |
| S143 | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/module/main.c | 2026-10-22 | `pr_warn("%s: loading out-of-tree module taints kernel.\n",` | kernel/module/main.c line 2577, entry row KT2 |
| S140 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/tainted-kernels.rst | 2026-10-22 | `12) ``O`` if an externally-built ("out-of-tree") module has been loaded.` | Documentation/admin-guide/tainted-kernels.rst line 171, entry row KT2 |
| S145 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/module-signing.rst | 2026-10-22 | modules for which the key is not available and modules that are unsigned are permitted, but the kernel will be marked as being tainted | Documentation/admin-guide/module-signing.rst line 57, entry row KT3 |
| S144 | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/module/signing.c | 2026-10-22 | `reason = "module with unavailable key";` | kernel/module/signing.c line 107, entry row KT3 |
| S143 | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/module/main.c | 2026-10-22 | add_taint_module(mod, TAINT_UNSIGNED_MODULE, LOCKDEP_STILL_OK); | kernel/module/main.c line 2610, entry row KT3 |
| S143 | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/module/main.c | 2026-10-22 | __ATTR(taint, 0444, show_taint, NULL); | kernel/module/main.c line 1083, entry row KT4 |
| S143 | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/module/main.c | 2026-10-22 | set_bit(flag, &mod->taints); | kernel/module/main.c line 198, entry row KT4 |
| S140 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/tainted-kernels.rst | 2026-10-22 | Note the kernel will remain tainted even after you undo what caused the taint | Documentation/admin-guide/tainted-kernels.rst line 12, entry row KT5 |
| S141 | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/panic.c | 2026-10-22 | set_bit(flag, &tainted_mask); | kernel/panic.c line 959, entry row KT5 |
| S141 | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/panic.c | 2026-10-22 | add_taint(i, LOCKDEP_STILL_OK); | kernel/panic.c line 129, entry row KT5 |
| S140 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/tainted-kernels.rst | 2026-10-22 | That's why bug reports from tainted kernels will often be ignored by developers, hence try to reproduce problems with an untainted kernel. | Documentation/admin-guide/tainted-kernels.rst line 8, entry row KT6 |

Not registered: the dkms 3.4.4 signing documentation and the Arch `nvidia-open` 615.78.08-1 PKGBUILD (their source seats died at spawn and the L1 did not open them; KT4's owning-package facts come from the capture's `pacman -Q` and `pacman -Qo` lines, not from a source row). Flip: open them in a later round if a row needs DKMS key handling or the package layout. `tools/debugging/kernel-chktaint` and `Documentation/admin-guide/sysctl/kernel.rst` were not opened either.

Registry recheck log (old -> new): none. No existing row changed `status`, `recheck` or `used-by`.

Spot-check result: owed to the non-author closure; not self-granted.
