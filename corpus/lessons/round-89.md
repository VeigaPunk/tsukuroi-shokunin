# Round 89 — lesson (tsukuroi)

author: TsukuroiR89 (L1). Pre-round tip `dfeaab29c42b56128ddee13f46019a453fca4185`; freeze
`fba764ca2a72dc2321f1c5d8cd228e92aa9382a9` (counter r89, 65-gate roster, roster probe, controls, host receipt,
declaration); control receipts `dddc82c6ac73d98a324477c3187eb14a78f36381` (both layouts, before any candidate score);
candidate `81f68d0053213400a5495b5fb5722c4dcb1cfc53` (battery r89, registry rows, entry UF1-UF8, S361-S363, README
correction); C1 measured at `81f68d00` from a clone (`665408cc…`). Citations are by hash.

## Inputs read

Round-88 closure (MANIFEST `rounds[]` tsukuroi r88, `rejected-honest-stop`) and
`corpus/lessons/round-88-verifier-spotcheck.md` §5. Disposition of its five routed defects:

| r88 defect | Disposition this round | Evidence |
|---|---|---|
| 1 README Round-88 Frontier contradicts the entry's corrected Limits | Corrected (README lines 977-981); mined as M1 below with a sweep receipt and QUALITY 127 | `corpus/README.md`; `.ufo/waves/round-89/w1/ExecLints/` |
| 2 C1 successor counter (mask every roster copy, error rows could-not-evaluate, deterministic CR) | This round's C1: `tools/battery-discrimination-r89.py` (opaque launcher, allowlist sandbox + preflight, exit 3 on any error row, manifest void, no `--roster`); battery r89 writes CRLF in every WHITESPACE-CRLF case | `SCORECARD.md` "Round 89 — declaration"; `.ufo/waves/round-89/before/controls/controls-summary.txt` |
| 3 Report text: CR flake is the seat's 2/24 | Erratum below; the r89 report cites 2/24 | this file, Errata |
| 4 Report author date earlier than the commits it cites | The r89 report is written after the last lane commit and committed at once | fleet commit of `.ufo/reports/round-89/tsukuroi.md` |
| 5 `hash_mismatch_panic.value` detector; r88 forger/mutant survivors as committed negatives | Roster negatives f01 f03 f06 f07 f08 f12 f14 f16 f18 f19, h01 h10 h11 h19 h20, m31 (value lie); selftest lie `panic-value` | `.ufo/waves/round-89/before/roster/roster-r89.json`; battery `--selftest` 15/15 |

Also read: the round-88 lesson's R88-R1..R6 (R88-R5's ReviewBattery F1/F3 is C2's ground; R88-R6 names C1 by its
surface, battery calibration).

## Gate

Sources opened 2026-11-06 (America/Sao_Paulo) ~21:50-22:05 by the L1: `git clone --depth 1 --branch v12.9.4
https://github.com/limine-bootloader/limine.git` (HEAD `8ad14430bc9f2c24679cda558981ef53e6e3b18c`) and the two raw
URLs with `curl` (HTTP 200, byte-identical to the clone: `.ufo/waves/round-89/before/src/fetch.txt`). The clone's
`uri.c`, `config.c`, `menu.c`, `CONFIG.md` are byte-identical to the round-87 pins (`cmp-r87-pins.txt`). The host
runs limine 12.9.4-1 (host receipt line 18).

| Candidate | URL, access date, location | Located quote (≤25 words) | Decision, reason and flip |
|---|---|---|---|
| S361 (new, code/A) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/protos/chainload.c, 2026-11-06, raw 414-437 | "panic(true, \"efi: Failed to open image with path `%s`. Is the path correct?\", image_path);" (raw 435) | ADMIT, UF5/UF6: the only source that says what an unopenable `path:` does to an `efi` entry, the protocol of all six host entries. Flip: a limine upgrade that changes `chainload()`'s failure path. |
| S362 (new, code/A) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/lib/panic.s2.c, 2026-11-06, raw 18-29, 70-100 | "print(\"Press a key to return to %s.\", booting_from_editor ? \"editor\" : \"menu\");" (raw 78) | ADMIT, UF7: turns the gate's consequence word `panic` into what the operator sees (menu return, or halt under measured boot). Flip: as S361. |
| S363 (new, own-work/A) | `.ufo/waves/round-89/before/host/receipt.txt`, captured 2026-11-06T21:52:29-03:00 (read-only `sudo -n grep`, `ls`, `od`, `pacman -Q`) | "29:  protocol: efi" (receipt line 4) | ADMIT, UF2/UF5/UF7/UF8 host values. Flip: any `/boot/limine.conf` rewrite (recheck 30d). |
| REJECTED: Limine trunk (`https://github.com/limine-bootloader/limine`, default branch) as the source for host behaviour | not cloned by the L1; the lane's rule is the installed tag (r87 entry Limits: trunk accepts BLAKE3 pins the host's 12.9.4 does not) | — | REJECT for rows: the host runs 12.9.4; trunk would describe a bootloader not installed. Flip: a host upgrade past 12.9.4 (then re-pin at that tag). Wave seat ScoutSources reports whether trunk changed the cited lines (advisory). |

Registry changes, old→new: S361, S362, S363 absent → `mined` (opened 2026-11-06; recheck `on-release`,
`on-release`, `30d`). S350 anchor gains `157-160 (measured_boot)`; used-by gains `corpus/knowledge/limine-uri-failure-r89.md`.
S351 anchor `… 28-104 (uri_resolve: last #, 128 hex), 301-319 …, 344-362 (resource dispatch), …` → adds `46-63 silent
false on no ( or no ):/`, `109-243 (dispatchers; boot(N) = partition N on the boot drive)`, `344-366 (… unknown
resource not valid)`, `372-376 (Secure Boot no-hash rule)`; used-by gains the r89 entry. S353 anchor `1711-1717` →
adds `1719-1730 (measured_boot …)`; used-by gains the r89 entry. No status or recheck of an existing row changed.
S351/S353/S350 re-opened this round in the tag clone (byte-identical), so their `opened` stays 2026-11-06.

Assimilation: none (no `merge/tsukuroi/` theme fits the Limine URI-failure surface; nothing adopted).
considerthese: latest file `considerthese/2026-10-26.md`, not mined this round.

## Errata

- **R88 report and lesson, "1 of 8 runs"** (`SCORECARD.md:7451`, `corpus/lessons/round-88.md:115`, fleet
  `.ufo/reports/round-88/tsukuroi.md`; not edited): the r88 seat measured the CR flake as **2 of 24** runs
  (`.ufo/waves/round-88/w1/MutBattery.md` lines 23 and 113: "in 2 of 24 runs", "measured 2/24 runs"; line 285
  "CRLF 2/24 met"). The analytic rate 0.4⁴ ≈ 2.6 % stands. In this round's freeze controls the r88 battery let
  `N-g15-no-cr-strip` escape once in six runs (canonical layout run 3,
  `.ufo/waves/round-89/before/controls/receipts-canonical/K1-r88-battery.receipt.txt`).

## Mistakes

| # | Class | Evidence | Captured-by | Fix |
|---|---|---|---|---|
| M1 | a correction landed in the entry's Limits but not in the README frontier bullet that stated the same fact (`R88-CORRECTION-NOT-SWEPT`) | `dfeaab29:corpus/README.md:977-978` ("`limine-install`'s body … is unread; the upstream tag copies … returned HTTP 429") against `corpus/knowledge/limine-pin-writers-r88.md:58-62` (corrected at r88 `35ca9e7e`); non-author spot-check r88 §5 item 1 | the r88 non-author spot-check; no lane criterion (QUALITY 108 names companions but no falsifiable sweep) | Bullet corrected (`corpus/README.md:977-981`, candidate `81f68d00`); QUALITY 127; sweep receipt `.ufo/waves/round-89/after/m1-sweep.txt` shown able to fail (hit at `dfeaab29`, rc 1 at `81f68d00`); second-token sweeps by wave seats ExecLints and ScribeLesson (`w1/ScribeLesson/receipts/m1-sweep.txt`) agree |
| M2 | a battery family certified its clause by a random draw, so a deviant gate could read `met` in a run (`R89-CERTIFY-BY-DRAW`, the R88-R2 class again) | first r89 candidate (uncommitted bytes `fae9c65b…`): `KEY-EQUALS` drew `path =` with p 0.5, `N-h01` escaped run 2 (`.ufo/waves/round-89/after/dev/README.txt`, `cand1-canonical-unmet-h01.json`) | the candidate's own first counter score (before commit); no criterion | `KEY-EQUALS` writes `path=` in every case (`tools/limine-pin-battery-r89.py:821-830`); QUALITY 128; 10-run determinism probe on 19 negatives, each killed 10/10 (`after/robustness-r89-negatives.txt`). Erratum: the dev README's "the blank-before-'=' variant is KEY-SPACING's ground already" is false — KEY-SPACING puts blanks before ':' only; a gate accepting `path =` reads `met` on the r89 battery (wave seat CriticClaims §6, `w1/CriticClaims/mut2-frozen.json`); patch routed (R89-R3) |
| M3 | the r89 counter's docstring promised "No source text, digest or file name of a roster gate is visible to the battery … closes it by construction", while the gate ran under its roster file name and its argparse usage line returns that name; no committed control queried that channel (`R89-NAME-CHANNEL-UNCONTROLLED`; same family as r88 M2 "promise in docstring, not in code") | `tools/battery-discrimination-r89.py:20-26` (promise), `:211` (`gate_path = os.path.join(gd, os.path.basename(gate["abs"]))`); wave seats ExecIsolation (b) and CriticClaims §2-a (name oracle 3/3, 62/62 `met`, 1 run); L1 usage oracle `.ufo/waves/round-89/after/forgeries/usage-oracle.receipt.txt` (3 runs, 65 hits each, `verdict met` rc 0) | QUALITY 126's isolation sentence clause ("backed by a control that would read the target if the mask were absent") — met only for the byte/source channel; the argv/stderr channel had no control | QUALITY 129 (one control per channel, shown able to fail by the usage-oracle receipt against CriticClaims' `patch-01-counter.patch`, name oracle 0/3, 62/62 `unmet`); successor counter routed (R89-R1). C1 does not verify (SCORECARD measured outcome) |

The r88 battery's rule text R1 also mis-states Limine for CRLF files (wave seat ReviewBattery F1): `config.c` 530-538
removes a blank run only when it is directly followed by `\n`, so blanks before `\r\n` survive the single pass and a
hash or `hash_mismatch_panic` value written with trailing blanks on a CRLF line reads differently in Limine (hash
length ≠ 128 → panic; `no ` → panic). Every roster positive and the landed gate implement the idealised rule, and
`WHITESPACE-CRLF` now exercises it every case. Routed as R89-R2 with the gate; not mined as a fixed mistake here
because no fix was shown able to fail this round.
