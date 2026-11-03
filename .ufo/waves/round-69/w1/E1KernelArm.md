2026-11-03T20:30Z — Seat E1KernelArm (executor), round 69 w1, item E1KernelArm: C2 census kernel arm implementation and selftest. No tool installs (wave items need none; none made).

## Built

`probe_kernel_arm` + one `KERNEL_LINE` in `tools/tsukuroi-census.sh` (sandbox clone @ 920a9eea3c5c5400567be0e96141014f338973df), emitted exactly once after the INITRAMFS line, before the rollup. Header contract paragraph + override-list entry + seam variables (`KERNEL_OSRELEASE`, `KERNEL_MODULES`, `KERNEL_TAINTED` from `TSUKUROI_KERNEL_OSRELEASE` / `TSUKUROI_KERNEL_MODULES` / `TSUKUROI_KERNEL_TAINTED`) + fixture stub `-Qo` verb + `fx_default`/`base_env` kernel seams follow the R65 initramfs pattern (`local LC_ALL=C`, `cap` wrapper, `have` unused here, verdict-neutral by construction — no rollup/exit/verdict variable touched).

Field contract as declared: `KERNEL kernel-plane release=<uts> pkg=<name> pkgver=<ver> modules_tree=PRESENT|ABSENT|UNKNOWN tainted=<int|UNKNOWN> taint_bits=<csv|none|UNKNOWN> pending=NO|YES|UNKNOWN unreadable=<n>` + optional ` detail=`. Taint letters embedded exactly as pinned S288 (`tk-v7211.rst`, sha256 727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 — re-verified on the committed snapshot): `PFSRMBUDAWCIOELKXTNJ` for bits 0-19 (12=O, 13=E, 14=L).

## Named semantic choices (where the declaration left room)

- **Multi-owner `pacman -Qo`**: live host answers with BOTH `linux 7.2.11.arch1-1` and `linux-headers 7.2.11.arch1-1` for `/usr/lib/modules/7.2.11-arch1-1`. The arm reports the FIRST ` is owned by ` line in pacman's own order and flags `detail=qo:multi-owner` when more than one owner line exists; never merges, never guesses.
- **Bits above 19** (case e): the 0-19 table is closed — any value > 1048575 reads `taint_bits=UNKNOWN` + `detail=tainted:bits-outside-closed-table`; the raw integer still prints in `tainted=`, so nothing is dropped, only not decoded.
- **`pending` mapping**: pkgver's last `.` replaced by `-` (`7.2.11.arch1-1` -> `7.2.11-arch1-1`) vs release; UNKNOWN when pkg or release unknown or pkgver has no arch dot.
- **ABSENT modules tree**: no `-Qo` is attempted (nothing to own) -> `pkg=UNKNOWN pkgver=UNKNOWN pending=UNKNOWN detail=modules:absent`.
- `-Qo` rc!=0 -> `qo:failed`; output with no ` is owned by ` -> `qo:unowned`; tail not exactly `<name> <version>` -> `qo:shape`; in all three `pkg=UNKNOWN pkgver=UNKNOWN`.

## Evidence (all run in sandbox /fast/scratch/hyaku/tsukuroi-r69/E1KernelArm/clone; full receipts in probes/)

- Base control: `$ bash tools/tsukuroi-census.sh --selftest` -> rc=0, `TSUKUROI_CENSUS_SELFTEST: PASS (177 cases, 177 passed, 0 failed)` (matches declared control 177).
- Patched: `$ bash tools/tsukuroi-census.sh --selftest` -> rc=0, `TSUKUROI_CENSUS_SELFTEST: PASS (192 cases, 192 passed, 0 failed)`; 15 R69-C2 cases (healthy; osrelease absent/empty/unreadable; tainted 0-padded/12288/1048576/unparsable; modtree absent; qo failed/unowned/shape/multi; A/B neutrality; field-order shape).
- Live: `$ bash tools/tsukuroi-census.sh` -> rc=1, `KERNEL kernel-plane release=7.2.11-arch1-1 pkg=linux pkgver=7.2.11.arch1-1 modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=NO unreadable=0 detail=qo:multi-owner`; rollup `TSUKUROI_CENSUS: DEGRADED (...)` (live host's own verdict; neutrality pinned by the A/B case).
- `$ bash tools/tsukuroi-census.sh | grep -c '^KERNEL kernel-plane'` -> 1 (rc=0).
- `$ grep -c 'KERNEL kernel-plane' tools/tsukuroi-census.sh` -> 16 (header contract line + 13 case regexes + shape literal + multi-owner fixture comment context; enumerated in counts.txt).
- `$ git status --porcelain` -> ` M tools/tsukuroi-census.sh` only tracked change + my four untracked receipt files (removed with scratch). E1_CLONE_CLEAN=yes.

## Files written (exclusive surfaces)

- .ufo/waves/round-69/drafts/c2/tsukuroi-census.sh (byte-identical to the sandbox patched file, verified `diff -q`)
- .ufo/waves/round-69/drafts/c2/census-kernel-arm.diff (`git diff` vs 920a9eea)
- .ufo/waves/round-69/probes/E1KernelArm/{selftest.txt,live.txt,counts.txt}
- this report. Lane working tree untouched; no commits anywhere; pre-existing drafts/c2/count-kr-rows-r69.py (C1 seat) untouched.

## Risks / notes for the L1

- `KERNEL_LINE` is a new global set unconditionally by `probe_kernel_arm` before its printf — same shape as `INITRAMFS_LINE`.
- The two non-neutral-looking details on the live line (`qo:multi-owner`, DEGRADED rollup) are host facts, not arm defects; the A/B case proves rollup/exit/non-KERNEL-line-count invariance with arm inputs present vs absent.
- Hermeticity: every R69-C2 case runs with `TSUKUROI_PACMAN` = fixture stub, kernel seams under `$FX`; non-kernel cases inherit the healthy fixture defaults (one extra stub `-Qo` per run, rc 0 path).
- Scratch /fast/scratch/hyaku/tsukuroi-r69/E1KernelArm/ deleted after this report was written.
