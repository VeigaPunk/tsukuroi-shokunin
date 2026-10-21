# FxRevBootTable — does `//linux` actually satisfy rule 2 (BOOTED-OBSERVED) at the captured state?

Round-19 FALSIFY wave, recovery attempt 2. Attacked revision: `8e5916360f2dfe7bc4eb4ba144081af555900116`.
Claim under attack: **BOOTED-OBSERVED for `//linux`** (decision table `corpus/knowledge/boot-chain-r17.md:69`; machine twin `boot-chain-r17.json:76-77`), consumed by the round-17 registry and re-exported by round-19 C1/C3 surfaces.

## Attack

Rule 2 is falsifiable per leg (`boot-chain-r17.json:33-34`):

> "if": "selected_this_boot is true (firmware LoaderEntrySelected names the entry), the image sha256 equals the file that booted (file mtime before boot start), and none of the nine boot-input paths swept at boot-chain-capture.txt:256 is newer than boot start (/boot is outside that sweep; the limine.conf path hash is checked instead)" → BOOTED-OBSERVED (json:34)

Same wording in prose (`boot-chain-r17.md:76-78`). Each leg is independently recomputable from `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt` (B:) and `supplement-capture.txt` (S:). The question: is BOOTED-OBSERVED earned from these captures, or merely assigned?

## Method

Exact commands (all read-only; no writes outside this report):

1. Byte-bind evidence to the attacked revision:
   - `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse HEAD` → `2fd1e6768f187be8c5e837af6286c3736953fcff` (lane has moved on; binding is to the attacked commit, not HEAD).
   - `git show 8e591636…:.ufo/waves/round-17/l1-capture/boot-chain-capture.txt | sha256sum` = `1a05ec2a…` = `sha256sum` of the worktree file (identical). Same for `supplement-capture.txt` (`8604310b…`) and `corpus/knowledge/boot-chain-r17.md` (`4e5018ca…`). All reads below are therefore of the attacked revision's bytes.
2. Read B: and S: in full; anchor every cited line with numbered grep; read `boot-chain-r17.json` ranges 14-63 and 114-153 and grep its rule/entry anchors.
3. Recompute each rule-2 leg from the captured values (arithmetic below); compare post-boot mtimes in `/boot` against the boot-start anchor; check the in-repo record for any prior explanation of every post-boot `/boot` mtime.

No tools installed (none needed); no host probe; `/boot` read only through the committed captures.

## Verdict

**CONFIRM — claim `BOOTED-OBSERVED //linux` (`boot-chain-r17.json:77`, `boot-chain-r17.md:69`) is earned under rule 2 as landed (`json:33`), not merely assigned.** Every operative leg recomputes TRUE from the captures at the attacked revision. The earn is scoped, not unconditional: it holds (a) over the rule's own nine-path `/etc`+`/usr` input set, (b) with boot start = `09:57:09` (journal anchor), (c) as an mtime-based identity whose byte-identity leg is [inf], and (d) with the rule's disclosed `/boot` substitution doing real work, because `/boot` itself contains two post-boot mtimes. No rule-named input is missing, so the INCONCLUSIVE trigger does not fire; the two `/boot` residuals are outside the asked `/etc`+`/usr` scope and are listed under Residual.

## Recomputed predicate

| # | Rule-2 leg (json:33) | Capture evidence | Recomputation |
|---|---|---|---|
| 1 | `selected_this_boot` | `LoaderEntrySelected-…: Omarchy.linux` (S:113); `LoaderInfo-…: Limine 12.9.3` (S:114); `LimineLastBootedEntry-…: Omarchy/linux` (S:115) | Firmware names the `linux` entry inside `/+Omarchy` (S:26, S:30). Its cmdline (S:35) equals `/proc/cmdline` (B:12) verbatim incl. `rootflags=subvol=@`; the live root mount is `subvol=/@` (B:14); `uname -r` 7.2.11-arch1-1 (B:5) equals the image's uname (B:173). **HOLD** |
| 2 | image sha = booted file, mtime < boot start | `/boot/EFI/Linux/omarchy_linux.efi` mtime `2026-10-20 09:26:22` (B:124); boot 0 start `Tue 2026-10-20 09:57:09 -03` (B:10) | 09:26:22 < 09:57:09 by **30 min 47 s**. sha256 `2e9c9bdc…` (B:171) equals the 09:29:18 history copy (B:219); b2sum `822299bb…` (B:172) equals the entry's `path:` `#` hash (S:34). Loader binaries pre-boot: `limine_x64.efi` 09:18:12 (S:92), `BOOTX64.EFI` 09:18:24 (S:85), byte-identical pair (S:94-95). **HOLD** as mtime; byte-identity to what firmware read stays [inf] — no capture hashes the running image (in-repo H3 agrees: `.ufo/waves/round-17/build/BootChainJsonAudit.md:17`) |
| 3 | none of the nine `/etc`+`/usr` inputs newer than boot | full-depth sweep, appended 12:53:51 (B:255): 9 paths (B:256) → `0` (B:257); `58674` files under the three trees (B:258). First attempt B:157-158 was `-maxdepth 1` (annotation B:255) | **0 newer** among all nine. Newest named input with a captured mtime: `/etc/fstab` installed 09:48:47 (B:97) — **8 min 22 s** before boot; `/etc/default/limine` + `/etc/limine-snapper-sync.conf` 09:19:40 (B:83-84); the 09:15:30 transaction (B:59, B:82) carried mkinitcpio/linux/systemd (upgrade lines within B:44-53). `/etc/crypttab` has no captured mtime event anywhere; it is bounded `< 09:57:09` only by the sweep. **HOLD** |
| 4 | `/boot` substitute: limine.conf path hash = image b2sum | S:34 suffix `822299bb…e8024` = B:172 (verbatim) | **HOLD** for the current file. Note the substitution is needed: `limine.conf` mtime is `12:07:06` (B:106), i.e. **2 h 09 min 57 s after** boot start, written by limine-snapper-sync at 12:07:07 (S:121); the pre-12:07 config content is uncaptured (`limine.conf.old` is 09:03:02, B:107) |

Boundary checks:

- **Boot-start anchor spread.** `uptime -s` = `2026-10-20 09:57:08` (B:6) vs journalctl boot-0 start `09:57:09` (B:10); the JSON bakes in `09:57:09` (`json:12`). The sweep threshold is the later reading, so a file with mtime in `09:57:08–09:57:09` would be newer than a 09:57:08 boot yet unflagged. No captured file falls in that window (nearest post-boot mtime anywhere in `/boot`: 09:57:10). One-second soundness gap, no observed occupant.
- **Everything else in `/boot` is pre-boot.** `EFI/` 2026-10-03 (B:105), `432d02b5…/` 09:03:02 (B:103), `amd-ucode.img` 2026-09-17 (B:104), `limine.conf.old` 09:03:02 (B:107), `EFI/Linux` dir 09:26:22 (B:122), history copies 09:29:18 (B:115-118).
- **Post-boot `/boot` mtimes at the captured state — exactly two:** `limine.conf` 12:07:06 (B:106, writer attributed: S:121) and `loader/` **09:57:10** (B:108) — 1 s after the journal boot start, before an interactive LUKS unlock could plausibly complete, writer [unk] (the capture's sudo window ends 09:58, B:75, and contains no loader-writing command), contents never captured.

## Evidence

- Captures (byte-bound to `8e591636…`, sha256 above): B:5-6, B:10-14 (boot start, cmdline, root mount); B:44-53, B:59, B:69-74, B:75, B:82-85, B:94, B:97 (transaction, UKI builds, sudo window, config installs); B:98-108 (`/boot` listing incl. B:106 `limine.conf` 12:07:06, B:108 `loader` 09:57:10); B:115-125 (history copies, `EFI/Linux` mtimes); B:157-158, B:255-258 (sweeps); B:171-175, B:219-220 (image facts).
- S:7 (`default_entry: 2`), S:26, S:30, S:34-35 (`//linux` block), S:85, S:92, S:94-95 (loader binaries), S:112-115 (efivars), S:118-121 (12:07:07 writer).
- Claim text: `corpus/knowledge/boot-chain-r17.md:69` (table row), `:76-78` (rules), `:86-93` (booted-image paragraph, incl. the `/boot`-exclusion disclosure), `:135-136` (falsifier); `boot-chain-r17.json:12, 14, 33-34, 59-62, 76-77`.
- Prior in-repo flags of the two `/boot` residuals (corroboration, not my finding): `.ufo/waves/round-17/build/CritDefaultEntryProof.md:10` (`/boot/loader` 09:57:10 anomaly, [unk]); `.ufo/waves/round-17/build/RevCaptureConsistency.md:7` (B2: both post-boot mtimes, sweeps exclude `/boot`); `.ufo/waves/round-17/build/BootChainJsonAudit.md:16` (H2); `.ufo/waves/round-17/falsify/FxBootedObserved.md:14` (`/boot/loader` listed unverified).

## Residual

1. `/boot/loader` (B:108): mtime 09:57:10 postdates boot start; contents never captured in any r17 file; writer unattributed. Whether Limine consults `/boot/loader/limine.conf` is not verifiable from in-repo sources (curl outside S070-S076 not authorized for this seat); `corpus/knowledge/journal-boot-plane.md:300` records an earlier-round `bootctl` probe failing to open `/boot/loader/loader.conf` — shape evidence only, and pre-dating r17. Outside rule-2's scope by the rule's own text (json:33), so it does not overturn CONFIRM, but "no newer boot-chain input" is only proven for `/etc`+`/usr`, never for `/boot`.
2. Boot-start anchor: 1 s spread between B:6 and B:10; the sweep uses the later (weaker) value. [unk] whether any swept path held a file with mtime in `09:57:08–09:57:09` at 12:53:51 — the sweep cannot express that question.
3. Byte identity of the booted image is [inf]: mtime + history-copy equality + cmdline/uname/rootflags agreement; no capture hashes the running kernel's UKI (H3, `BootChainJsonAudit.md:17`).
4. B:256's literal text contains `<same three trees>` (paraphrase), so `58674` (B:258) is not verbatim-reproducible from the printed command; accepted as captured output, flagged already as RevCaptureConsistency B2.
5. Pre-12:07 `limine.conf` content is uncaptured, so the config Limine actually parsed at 09:57:09 is not byte-attested; immaterial to legs 1-2, material only to next-boot prediction (outside this seat).

Scope: executed=cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && git rev-parse HEAD && git show 8e5916360f2dfe7bc4eb4ba144081af555900116:.ufo/waves/round-17/l1-capture/boot-chain-capture.txt | sha256sum && sha256sum .ufo/waves/round-17/l1-capture/boot-chain-capture.txt && git show 8e5916360f2dfe7bc4eb4ba144081af555900116:.ufo/waves/round-17/l1-capture/supplement-capture.txt | sha256sum && sha256sum .ufo/waves/round-17/l1-capture/supplement-capture.txt && git show 8e5916360f2dfe7bc4eb4ba144081af555900116:corpus/knowledge/boot-chain-r17.md | sha256sum && sha256sum corpus/knowledge/boot-chain-r17.md
