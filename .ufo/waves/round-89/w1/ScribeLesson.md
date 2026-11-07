# ScribeLesson — round 89 w1, seat report (scribe)

Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, `git rev-parse master` =
`665408cc45a88ed49717e22f4593e8e6152ac665` (measured throughout; the pre-round tip `dfeaab29c42b56128ddee13f46019a453fca4185`
is cited as `dfeaab29`). Write scope honoured: this seat wrote **only** under `.ufo/waves/round-89/w1/ScribeLesson.md`
and `.ufo/waves/round-89/w1/ScribeLesson/`; no lane file was edited, no git/jj mutation ran, no subagent was spawned,
no `sudo`, and nothing was installed (tooling: none needed; no pacman/uv/npx/npm channel was used).

## Behaviour delivered

Four draft files for the L1 to integrate into `corpus/lessons/round-89.md` and `corpus/QUALITY.md`, plus five
receipts. Nothing is a claim of my own about C1 or C2; the only new claims are the verifications below.

| Artifact | Covers | Integration status found at the tip |
|---|---|---|
| `w1/ScribeLesson/gate-rows.md` | `## Gate` rows S361/S362/S363 with quotes re-read by this seat; anchor changes old→new for S350/S351/S353; a REJECT row with measured evidence | the L1's rows (`corpus/lessons/round-89.md:29-47`) already exist and agree; only the REJECT row is strengthened (from "not cloned by the L1" to a diffed trunk) |
| `w1/ScribeLesson/mistakes.md` | M1 (`R89-CORRECTION-SWEEP-UNFALSIFIABLE`) and M2 (`R89-CERTIFY-BY-DRAW`) in the r88 table shape | `corpus/lessons/round-89.md` has no `## Mistakes` section at the tip, and the landed README cites "lesson r89 M1" — the reference is dangling until M1 lands |
| `w1/ScribeLesson/quality-127-128.md` | 127 (sweep gradient) and 128 (discriminating element in every case) | **127 already exists in the working tree** (uncommitted, `corpus/QUALITY.md`, token `R88-CORRECTION-NOT-SWEPT`); the draft says do not add a second one. **128 exists nowhere** and is the live proposal |
| `w1/ScribeLesson/errata.md` | verification of the L1's Errata, plus the provenance of "1 of 8" (the seat's first batch) | `corpus/lessons/round-89.md:51-58` agrees with every pointer checked |
| `receipts/` | `m1-sweep.txt`, `m2-evidence.txt`, `quote-verification.txt`, `sources-anchor-diff.txt`, `trunk-vs-tag.txt`, `trunk/limine-trunk-common_protos_chainload.c` | — |

## Verifications run (verbatim, with exit codes)

1. **Every Gate quote, re-read in the pinned snapshot.** `receipts/quote-verification.txt` prints, per file, its
   `sha256` and the `sed` window the row cites. Spot values: chainload `316eb17df996f91252791b1351e8f88c027ceeb8535becc1a247d614d8b5e1a7`,
   panic.s2.c `0233d557db8fdf96918350a305cde91a8a4aca33216d2ac8c712cf47c79a3ff1`, uri.c `e06cac12…`,
   menu.c `628001e8…`, CONFIG.md `c9e8b670…`. S361 quote sits at raw **435**, S362 at raw **78**, S363 at receipt
   **line 4** (`29:  protocol: efi`), S350's `measured_boot` at 157-160, S353's at 1719-1730 — all as the rows say.

2. **M1 sweep, both directions** (`receipts/m1-sweep.txt`):
   ```
   $ git grep -n -F "returned HTTP 429, so PW5 rests" dfeaab29 -- corpus/README.md
   dfeaab29:corpus/README.md:978:  returned HTTP 429, so PW5 rests on the installed bytes (S360).
   rc=0
   $ git grep -n -F "returned HTTP 429, so PW5 rests" master
   rc=1                      # empty over the whole tracked tree
   ```
   Peer receipts agree from a second token: `.ufo/waves/round-89/w1/ExecLints.md` (2 hits at `dfeaab29`, 1 at HEAD,
   the spot-check's quote) and `.ufo/waves/round-89/after/m1-sweep.txt` (same gradient, exclusion pathspec
   `':!corpus/lessons/*-verifier-spotcheck.md'`).

3. **REJECT row measured** (`receipts/trunk-vs-tag.txt`):
   ```
   $ curl -sS -o trunk-chainload.c -w '%{http_code} %{size_download}' …/limine/trunk/common/protos/chainload.c
   200 18463          rc=0
   68d56ee4…  <trunk>      316eb17d…  <v12.9.4 pinned>
   grep -n "Failed to open image"  → trunk:450   pinned:435
   diff -u → 3 hunks
   ```
   Two hunks are behavioural: trunk roots the EFI file path with `\` and grows the UTF-16 buffer by one
   (`(original_path_chars + 2)`, `efi_file_path[0] = '\\'`), and clamps an extended-partition `sect_count` to the
   disk end. The host runs `limine 12.9.4-1` (`host/receipt.txt:18`).

4. **Anchor diff** (`receipts/sources-anchor-diff.txt`): S350 gains `157-160 (measured_boot)` + used-by; S351 gains
   `46-63`, `109-243`, `344-362`→`344-366`, `372-376` + used-by, **teaches unchanged**; S353 gains `1719-1730` +
   used-by; no status/opened/recheck changed on any row.

5. **Battery determinism of the reference gate** (one run, this seat's scratch, removed after):
   ```
   $ python3 tools/limine-pin-battery-r89.py --gate .ufo/waves/round-89/before/roster/pos-landed-gate-3ba37eb0.py --runs 1 --work $S/work
   families_passed 50/50 verdict met failed -          rc=0   (13.4 s wall)
   ```

6. **Errata pointers**: `MutBattery.md:23` "in 2 of 24 runs", `:113` "measured 2/24 runs", `:285` "CRLF 2/24 met",
   `:226-227` the 24-run paragraph, `:230-232` the 8-run first batch (`×1 met`) — so "1 of 8" is a sampling, not a
   miscount. "1 of 8" carriers: `SCORECARD.md:7451`, `corpus/lessons/round-88.md:115`, fleet
   `.ufo/reports/round-88/tsukuroi.md:66-67`. K1 controls: `grep -c N-g15-no-cr-strip` = canonical **1**, clone
   **0** → "once in six runs" is exact.

## Findings (file:line, no patch applied)

- **F1 — dangling reference in a landed file.** `corpus/README.md:976` says "(Corrected round 89; spot-check r88
  routed 1, lesson r89 M1.)" while `git ls-tree master corpus/lessons/round-89.md` is empty and
  `git ls-files --error-unmatch` exits non-zero: at the measured revision the cited lesson row does not exist.
  Resolves when M1 lands; if the L1 lands a different M-row id, the README line must change with it.
- **F2 — the correction commit carries no sweep** (`81f68d00`: `corpus/README.md` 7 lines changed, no sweep file;
  `git show --format= --name-only 81f68d00 | grep -iE 'sweep|companion'` → rc 1). QUALITY 108 asks for the companion
  map; the working-tree 127 now asks for the gradient; both post-date this commit, so the gap is honest, not a
  forged claim — but the round should land the map with the lesson.
- **F3 — residual drawn variants in the frozen battery** (`tools/limine-pin-battery-r89.py`): `:798` (CR inside a
  key, 3 keys), `:838` (empty path, 2 keys), `:727`/`:735` (optional key, 2), `:850` (6 forms over 2 keys),
  `:777-784` (panic-value blanks). The discriminating *clause* is present in every case (the r88 defects `:351`,
  `:821-829` are fixed), so this is coverage breadth, not certification-by-chance: no roster negative is left
  draw-dependent — the two key-set negatives, `m26` and `m27`, are caught every run by `fam_all_pin_keys`
  (`:659-671`) and `fam_optional_hash_format` (`:565-573`). A successor family that is key-specific would
  reintroduce the class; QUALITY has no barrier, hence the 128 draft.
- **F4 — latent mislabel**: `:840` records the expected key as the literal `"path"` while `:838` drew
  `path`/`kernel_path`. No verdict changes today (an `LP-MISSING` consequence is key-independent, `finish()`
  `:226-244`), but the same family's expectation would be computed from the wrong key if its status changed.
- **F5 — the fleet report's figure**: `.ufo/reports/round-88/tsukuroi.md:66-67` says "1 of the seat's 8 runs";
  the seat's own 24-run sample is 2 of 24 and its predicate-level consequence (7.4 %) is at `MutBattery.md:236`.
  The Errata draft keeps the superseded text in place and names the carriers.

## Out of scope / not done (unrun checks are not passes)

- I did **not** verify C1 (3/3, 62/62, 0 errors ×3) or C2's UF rows: executor/mutation seats own those; nothing here
  should be read as corroborating or contradicting the C1 receipt at `665408cc`.
- I did **not** run the counter: the reading at `665408cc` is the L1's C1 receipt and the counter is frozen; this
  seat's one instrument run was the battery on the reference gate (13.4 s, item 5). I did not run any
  roster gate, and did not measure the escape rates in F3 empirically — they are analytic (`(1-1/m)^4` per run,
  `1-[1-(1-m^-1)^4]^3` over three runs) and marked as such in the draft.
- I did **not** edit `corpus/README.md`, `corpus/QUALITY.md`, `corpus/lessons/round-89.md`, `corpus/SOURCES.md`,
  the battery, the counter or the roster; the L1 decides.
- I did **not** touch `/boot`, `/efi`, `/etc`, `/usr`, `/sys`, `/proc`; the host receipt used is the L1's committed
  one. No host fact is claimed beyond it.
- Working-tree state observed but not mine: `corpus/QUALITY.md` modified (the 127 insert), `corpus/lessons/round-89.md`
  and `.ufo/waves/round-89/after/m1-sweep.txt` untracked. Scratch `/fast/scratch/hyaku/tsukuroi-r89/ScribeLesson`
  removed after its receipts were copied (`/fast` 411 G free, 49 % used).

## Files

Report: `.ufo/waves/round-89/w1/ScribeLesson.md`
Drafts and receipts: `.ufo/waves/round-89/w1/ScribeLesson/` (`gate-rows.md`, `mistakes.md`, `quality-127-128.md`,
`errata.md`, `receipts/{m1-sweep,m2-evidence,quote-verification,sources-anchor-diff,trunk-vs-tag}.txt`,
`receipts/trunk/limine-trunk-common_protos_chainload.c`).
