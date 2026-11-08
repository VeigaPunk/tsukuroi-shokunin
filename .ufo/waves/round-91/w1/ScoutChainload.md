# ScoutChainload — round 91 w1 — C2 sources, chainload half

Seat: ScoutChainload (scout, leaf). Lane axes: operability + freshness.
Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (branch `master`).
Lane revision measured: `git rev-parse master` → **`b516d6ae13ec0bba3ef89589ac1cac86f73a9632`**
(pre-round tip was `40efa4ea2862ab39da02430cada68f6dff230e86`; the lane has moved on since the
pre-round tip — the round-91 wave commits `d3b0987d`, `203b3872`, `1652b086`, `d6f674f8`, `b516d6ae`
are on `master` now). At the end of my seat the tip had advanced further to
`2d7e09e101996cc1ac5836c6d635f3f608453ac5` (other seats committing concurrently); every source
number I quote is anchored to the pinned snapshot files, not to a moving tip.
Working tree at my measurement time: `M SKILL.md`, `M corpus/SOURCES.md`, `M tools/check-limine-pins.py`
(another seat's in-flight edits; I did not touch them), plus untracked `.ufo/waves/round-91/w1*`.

Deliverables written (all inside my own wave dir, nothing else touched):
- `.ufo/waves/round-91/w1/ScoutChainload/proposed-rows.md` — 10 candidate rows CC1–CC10 for
  `corpus/knowledge/limine-unverified-image-r91.md`.
- `.ufo/waves/round-91/w1/ScoutChainload/proposed-sources.md` — SOURCES row drafts (TBD-A…TBD-E) plus
  anchor-extension proposals for the already-registered S374/S375/S376.
- `.ufo/waves/round-91/w1/ScoutChainload/urires-harness.c` + `.bin` — verbatim transcription of
  `uri_resolve` (uri.c 32-107) and its measured output.
- `.ufo/waves/round-91/w1/ScoutChainload/cfgcut-harness.c` + `.bin` — verbatim transcription of the
  `init_config` strip loop (config.c 527-552), the global cut (642-651), `config_get_entry` (686-722)
  and `config_get_value` (778-818), with 15 measured cases.
- `.ufo/waves/round-91/w1/ScoutChainload/clone-{chainload.c,config.c,uri.c}` — the clone files I read.

## Verdict per check

| check | verdict | evidence |
|---|---|---|
| pinned snapshot byte-identical to clone `v12.9.4` | **PASS** | `cmp` identical for `chainload.c`, `config.c`, `uri.c` (also `menu.c`, `panic.s2.c` vs `before/src`); clone HEAD `8ad14430bc9f2c24679cda558981ef53e6e3b18c`; sha256 match `after/src-c2/SHA256SUMS` |
| `chainload()` reads PATH then IMAGE_PATH from the entry body | **PASS** | chainload.c 415/417; body = `selected_menu_entry->body` (menu.c 2349→2460), copied at config.c 377-380 |
| shape-less value ⇒ boot-fatal panic of that entry | **PASS** | uri.c 48-49/61-62 silent false → uri.c 335-336 NULL → chainload.c 435 `panic(true, "efi: Failed to open image …")` |
| URI-shaped, `#`-less value ⇒ opens and boots with NO Limine digest check | **PASS** | uri.c 44/77-104 (hash stays NULL), 378-381, 483-488, 662-664 (no comparison); harness `boot():/EFI/BOOT/BOOTX64.EFI -> TRUE … hash=(NULL)` |
| an `efi` image path needs no hash even under Secure Boot | **PASS** | chainload.c 426-427/437 clears the flag around `uri_open`; the only missing-hash gate is uri.c 372-375 |
| a present-but-malformed `#hash` is a *different* panic | **PASS** | uri.c 89-91 / 97-99 `URI_ERROR("Blake2b hash must be 128 characters long")` — not "Failed to open image" |
| `unverified_image_lines` mixes a fatal shape with a silent one | **PASS** (observation, not a defect in the frozen rule) | frozen r91 gate `d3b0987d` on fixtures: `plainname.efi` and `boot()plainname.efi` both → `HEALTHY rc 0 pins [] unverified_image_lines [3]` |
| host: exactly one unhashed image line, line 72 | **PASS with a caveat** | receipt line 20 `72:path: boot():/EFI/BOOT/BOOTX64.EFI`; **caveat** below (CC9) |
| global-section cut / first-entry exception (config.c) | **PASS** | 15 harness cases; first-line entry header ⇒ whole file stays visible (53/56 bytes), global key after the entry body still found |

## The two findings the L1 should act on

**1. The C2 claim's framing needs one correction (CC2/CC3/CC6).** `unverified_image_lines` lumps
two shapes that behave completely differently at boot:
- no `(` / no `):/` → `uri_resolve` false **without a message** → `uri_open` NULL → **panic**
  `efi: Failed to open image with path ...` (menu return unless measured boot);
- URI-shaped but no `#` → opens fine, and because `hash == NULL` **no BLAKE2b comparison happens at
  all** (uri.c 378-381, 483-488, 662-664) → the image is executed with **no digest check by Limine**;
  under Secure Boot the only check is the firmware's `LoadImage` (chainload.c 423-425, 507).

The host's line 72 is the *second* shape. So the entry must not describe the host's fallback as a
panic case. And because U1 is a reporting contract (no verdict/status/consequence/rc change), the
gate is correct as frozen — the *entry* has to carry the distinction.

**2. The r91 host receipt's per-line capture is truncated at 140 columns (CC9).** Its six image-line
excerpts are all exactly 140 characters; the visible `#` fragments are 93 and 89 hex chars of a
required 128, and lines 50/56/64 lose their `#` entirely. The round-17 full capture (S051, lines
143/147/153, 230 chars each) shows those three DO carry `#` + 128-hex BLAKE2b pins at column ~160.
**Do not write that lines 50/56/64 lack a pin.** Only line 72 is genuinely unpinned. A fresh
read-only capture (e.g. `sudo -n grep -n -E '^\s*(protocol|path|image_path):' /boot/limine.conf`)
without a column cut would close this.

## Row/quote discipline

Every quote in `proposed-rows.md` is verbatim from the pinned snapshot with its raw line number; all
four quotes ≤ 25 words. `[src]`/`[obs]`/`[inf]` labels used per the seat spec. Statements are
labelled individually inside each row's text.

## Boundaries honoured

- Read-only everywhere; **no `sudo`**, no writes to `/boot`, `/efi`, `/etc`, `/usr`, `/var`, `/sys`,
  `/proc`; no `objcopy`/`strip`/`sbsign`/`ukify`/`patchelf`/`mkinitcpio`/`limine`/`pacman`/`snapper`/
  `bootctl`/`efibootmgr`; no sysctl change; no git/jj mutation in the lane or outside my fixtures.
- No lane file edited. No `MANIFEST.json`, `.ufo/state/`, `.ufo/watchdog.log`, `.scratch/`, sibling
  lane repos, `/home/vgpnk/Projects/shokuknow`, or `considerthese/` touched.
- No subagents dispatched (leaf). No model chosen. `agent://all` never messaged.
- Scratch used: `/fast/scratch/hyaku/tsukuroi-r91/ScoutChainload/` (created, used, then removed);
  fixtures only under `$S/work`; the wave dir holds the two harnesses and their binaries.
- Host facts came from the committed r91 receipt (read-only) plus the round-17 committed capture
  already in the repo; I did not re-read `/boot` (permission denied for this user anyway) — so the
  line-72 / 140-column findings are from the committed receipts, not from a fresh host read.

## Refused / not done

- Did not re-measure the live host (`/boot/limine.conf` is not readable by this user without sudo,
  which is forbidden): the host column rests on the committed receipts.
- Did not run the r91 battery or the C1 gate measurement: out of this seat's scope (C1 is measured by
  the C1 seats), and the frozen battery/battery digest are not mine to touch.
- Did not touch `corpus/knowledge/limine-unverified-image-r91.md` (the L1 writes it) or
  `corpus/SOURCES.md` (L1's call).

## Unresolved

- Whether the L1 wants the `common/menu.c` dispatch anchors (TBD-A) as a new registry row or as an
  extension of S353 — my recommendation is the extension; the id is the L1's.
- The exact full text of host conf lines 50/56/64 (beyond column 140) is not in any committed
  receipt; the round-17 capture is from 2026-10-20 and the hashes have since changed (the r91 receipt
  shows different hashes on lines 30/38). A fresh uncut capture would be needed to state today's
  values verbatim.
