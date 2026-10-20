## BootChainGate report — tools/check-boot-chain.py (created)

**Behaviour [obs].** Read-only gate for `corpus/knowledge/boot-chain-r17.{json,md}` at schema `tsukuroi-boot-chain-v2` (rewritten after L1's 13:2x schema swap; v1 DEGRADED-PREDICTED logic removed). Checks:

- Top-level shape: exact key set, `schema`, `captures` map == pinned 4 captures, non-empty `authority`/`superseded` strings, `verdict_rules` order/verdict table == the 6 recorded rules.
- Per entry: exact 18-key set + types; every `capture:line` evidence ref resolves (path must be in the captures map → `BOOTCHAIN-EVIDENCE-PATH`/`BOOTCHAIN-EVIDENCE-LINE`); cited lines witness `sha256`, `uname`, `rootflags`, `VERSION`, `init /sysroot refs N ; /new_root refs M`, `root_mnt="…"`, `--new-root-dir=…`; `b2sum_prefix` prefixes the entry's own `path:` #hash; `### <efi_path>` block agrees (sha/uname/VERSION/refs/hook bytes).
- Verdict re-derivation from the 6 ordered rules (booted image identified as the unique `/boot/EFI/Linux` block whose uname == `boot.running_kernel`); `verdicted_kernel_entries` counts derived==recorded and != NOT-A-KERNEL-ENTRY — expected 5 on the real corpus.
- Boot block evidence witnesses running_kernel, boot_start, cmdline_rootflags, loader_entry_selected. MD: `source:`/`verified-at:`/`recheck:` + 4 required headings + every entry id in `## Decision table`.
- Revision binding: 7–64 hex only; `<hex>^{commit}`; ancestor of `refs/heads/<branch>` (default master) → `E-REVISION-NOT-LANDED`; of `refs/remotes/origin/<branch>` when it exists → `E-REVISION-NOT-PUSHED`; `HEAD`/`@`/refs → `E-REVISION-INVALID`; `--branch` validated `E-BRANCH-INVALID`; JSON carries revision/branch/branch_tip.
- Missing files → `BOOTCHAIN-MISSING` (exit 1); malformed JSON → `E-JSON-PARSE` (exit 2).

**Selftest [obs]:** `python3 tools/check-boot-chain.py --selftest` in a mktemp clone of the lane → `PASS (53 cases, 53 passed, 0 failed)`, incl. wrong verdict, hash mismatch, missing evidence line, restored-defect BOOTED-OBSERVED-on-snapshot, and 5 real git binding vectors. Exit 0.

**Static real-data trace [inf]:** every cited line number and claimed string verified against the 4 capture files by grep; expected PASS at landing with verdicted 5. Not executed against real data (selftest-only authorization).

**Schema questions for L1 [unk]:** entry rootflags are not cited for `linux` (line 12 belongs to the entry evidence — ok) but `snapshot` entries rely on supplement cmdline lines — fine as long as captures stay as is; `image_new_root` has no literal witness check (emulation cites exist but string is `new_root -> sysroot`, not `symlink->sysroot`).

**Files changed:** `tools/check-boot-chain.py` (new, 1134 lines). No installs.

Scope: executed=mktemp -d, git clone --quiet /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/*/lane, cp tools/check-boot-chain.py, cd sandbox && python3 tools/check-boot-chain.py --selftest, plus repo-readonly git rev-parse/for-each-ref/status/ls-tree/grep/ls/wc/head/py_compile
