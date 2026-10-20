# BootAuditTool — tools/boot-chain-audit.sh (round 17)

**Landed:** `tools/boot-chain-audit.sh` (bash, read-only; `--live|--selftest|--help`).

**Behaviour** — `--live` reads limine.conf via `sudo -n cat`, copies each `boot():/…` UKI via `sudo -n cat` into a mode-700 mktemp tree, then hashes, objcopies and extracts (`lsinitcpio -x`) unprivileged on the copy. Paths validated by `^boot\(\):/[A-Za-z0-9._/-]+(#[0-9a-f]{128})?$`, `..` rejected; refuses root; one image at a time in a subshell cd'd into its own mktemp dir; guarded rm only inside owned trees. Emits 17-column TSV (adds `image_new_root`, `selected`), counts, then `TSUKUROI_BOOTCHAIN: CONSISTENT|DEGRADED|UNKNOWN` (0/1/2; DEGRADED reserved, unemitted under v2).

Verdicts implement schema v2: NOT-A-KERNEL-ENTRY, BOOTED-OBSERVED (efivar-selected, mtime < boot start, no newer /etc+/usr input), UNTESTED (rules 3/6), PATH-ALIASED-EMULATED (`/new_root` symlink→sysroot), CONSISTENT-PRE42 (directory). Snapshot or selected entries landing on rule 6 force UNKNOWN.

**Evidence** [obs]: `corpus/knowledge/boot-chain-r17.json:26-56` (verdict_rules); `.ufo/waves/round-17/l1-capture/supplement-capture.txt:113-115` (LoaderEntrySelected `Omarchy.linux`, LimineLastBootedEntry `Omarchy/linux`); `l1-capture/overlay-emulation.txt:5,40-48` (`new_root -> sysroot`; findmnt resolves; overlay lands); `/usr/lib/initcpio/functions:1212-1213` (`ln -s sysroot "$buildroot/new_root"`).

**Selftest** [obs]: `bash -n` rc 0; `--selftest` in a mktemp copy: `TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=44 failed=0` — includes `$(touch canary)` conf leaving no canary, guarded-rm outsider refusal, `..` rejection.

**Unverified** [unk]: `--live` never run (forbidden). Unprivileged `stat` on the 0700 ESP fails, so BOOTED-OBSERVED is unreachable here; the selected entry resolves to PATH-ALIASED-EMULATED while its `selected` column stays true.

**Risks** [inf]: efivar menu-path matching joins the `/`-stack with `.` or `/`; a limine naming change would match nothing (stderr warning only when no efivar is readable). b2 mismatch is reported, never a verdict input.

Scope: executed=bash -n, bash --selftest, bash (syntax/help/refusal and sourced debug copies), mktemp, cp, rm -rf, sed -i (debug copies only), ls, cat, sed, awk, grep, wc, paste, tail, tr
