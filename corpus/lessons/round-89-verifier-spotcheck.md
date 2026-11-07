# Round 89 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-06
lane-round: tsukuroi r89; pre-round tip `dfeaab29c42b56128ddee13f46019a453fca4185`, landed tip `7f3f30b3898adf77af1035608621ffdbbabaa9d9`
report: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-89/tsukuroi.md` (fleet commits `ea28e55b5c738e6c5bb1eda756f86f3180f1be8d`
author date 23:08:53 -03, commit date 23:15:41 -03; amendment `765cca05578aa91f46fcb870b54a71b835a368cf` author date 23:15:41 -03,
commit date 23:16:13 -03; both author `tsukuroi-shokunin`)
dispatch digest (copied from the mutable `.ufo/watchdog.log`):
`2026-11-06T21:41:53-03:00 launch tsukuroi round=89 pgid=1608150 driver=hyaku-inline attempt=1`;
`2026-11-06T23:16:33-03:00 complete tsukuroi round=89; hyaku-inline attempt=1`

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by the lane identity | `git log --format='%an %H %ad' -- .ufo/reports/round-89/tsukuroi.md` (fleet) | `tsukuroi-shokunin 765cca05…`, `tsukuroi-shokunin ea28e55b…` | pass |
| `SHONEN` heading, one line per box | read report §SHONEN; `grep -n '\[.\]' SHONEN.md` (lane) | 4 boxes in SHONEN.md, 4 report lines, all `[~]`, each with an evidence line | pass |
| Cited commits exist and are ancestors of `master` | `git rev-parse --verify <h>^{commit}`; `git merge-base --is-ancestor <h> master` for fba764ca, dddc82c6, 81f68d00, 665408cc, 96a582c8, 7f3f30b3, dfeaab29 | all resolve, all ancestors; `git log dfeaab29..7f3f30b3` = exactly the six commits of the report's table | pass |
| Lane pushed, nothing left over | `scripts/hyaku/jj-lane.sh state …/tsukuroi-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `branch=master local=remote=7f3f30b3… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `7f3f30b3…` | pass |
| Prompt carries the template contract | `diff <(sed -n 1,140p .ufo/prompts/tsukuroi-round-89.md) kimi-shokunin/templates/round-prompt.md` | only `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitutions; §§1–5 verbatim, then hyaku §6, §7 and run-15 notes | pass |
| Report filed after the work it cites | author/commit dates vs cited commits | first commit `ea28e55b` author date 23:08:53 precedes the cited `7f3f30b3` (23:15:01); its commit date (23:15:41) and the amendment `765cca05` (author 23:15:41) follow it. The report itself names the cause (`scripts/hyaku/fleet-commit.sh` keeps the jj change's creation time as author date) | conformance note (status-neutral); routed to the fleet-helper owner, not the lane (§5 item 5) |

Not a marker: the report cites six landed lane commits with evidence paths. Status `ok`.

## 2. Claims

### C1 (measured; operability 9, assurance arm of `limine-pins`) — evidence-verified, NOT VERIFIED as declared

The counter and battery are lane-owned gates; neither was executed here (§Gate standard, Closure consequence).
Committed evidence checked at `7f3f30b3`:

- Freeze integrity: `sha256sum -c .ufo/waves/round-89/before/freeze-manifest.sha256 --quiet` → rc 0, 76 lines;
  `git log dfeaab29..7f3f30b3 -- tools/limine-pin-battery-r89.py tools/battery-discrimination-r89.py` → `81f68d00`, `fba764ca`
  only; `sha256sum` → counter `c666323a…`, battery `3bae11e9…` = the digests in every run JSON.
- Roster: `jq '[.gates[]|.expect]|group_by(.)|…' roster-r89.json` → `{"met":3,"unmet":62}`, 65 gates. Matches.
- Tallies: `jq '[.runs[]|"\(.positives_ok)/\(.positives_total) \(.negatives_ok)/\(.negatives_total) e\(.error_rows)"]'` over
  `after/measured/c1-run-{81f68d00,96a582c8,canonical}.json` → 9 runs, each `3/3 62/62 e0`, verdict `met`. Matches the report.
- Battery selftest (evidence): `c1-receipt-81f68d00.txt` lines 4-15 → every case PASS, incl. `lie-verdict`, `lie-exit-code`,
  `lie-rc-field`, `lie-line`.
- Before (do-nothing, `before/controls/controls-summary.txt` lines 2, 8): r88 battery 3/3 with 46/46/45 of 62 (canonical) and
  46/46/46 (clone), rc 1; always-met 0/62, always-unmet 0/3, roster and fingerprint oracles 0/62 with 0 hits inside the
  counter and 65/65 correct, 65 hits outside (lines 15-16); crash 65 error rows rc 3. Matches.
- Instrument property: the counter docstring (`tools/battery-discrimination-r89.py` line 24) says "No source text, digest
  or file name of a roster gate is visible to the battery"; line 211 copies the gate as
  `os.path.join(gd, os.path.basename(gate["abs"]))`, so the gate runs under its roster file name and its argparse usage
  text carries that name back through the launcher. Forgery evidence: `after/forgeries/usage-oracle.py` (a name→label
  table, no rule evaluated); `jq` over `usage-oracle.json` → 3 runs `3/3 62/62 e0`, verdict `met`, and
  `[.runs[]|[.rows[]|select(.families_passed==999)]|length]` → `[65,65,65]` (every row answered by the name table).

Ruling: the 62/62 ×3 numbers verify, but the claim's predicate includes "the battery sees each gate only as an opaque
launcher", and a battery that tests no rule meets the same target on the frozen counter. The frozen instrument cannot
separate the candidate from a forgery, so C1 does not verify as declared → operability **unchanged** (no ordinal move was
claimed; r84/r88 precedent: a lane-disclosed falsified instrument is an honest stop). CriticClaims' patched counter
(`w1/CriticClaims/patched-full-run.json`: candidate 62/62, name oracle unmet) and MutBattery 16/19 are recorded, not
credited: they are not the frozen measure.

### C2 (exploratory; depth 8) — closure is the named non-author reviewer: **unprovable-but-better**

Prior state re-measured: `git grep -n -i 'boot_dispatch\|uri_hdd\|fslabel_dispatch\|allow_menu\|measured_boot' dfeaab29 -- corpus/knowledge`
→ 0 lines; at `7f3f30b3` → `limine-uri-failure-r89.{md,json}` only. `jq length` on the JSON → 8 (UF1–UF8). Knowledge `.md`
files 104 → 105.
Sources re-opened independently: `curl` of the S361 and S362 raw tag URLs → `cmp` byte-identical to
`.ufo/waves/round-89/before/src/` (and `sha256sum -c SHA256SUMS` there → 2 OK); `pacman -Q limine` → `12.9.4-1` (the tag is
the installed version).
Row checks against pinned bytes:
- UF1: `uri.c` 18-26 — `URI_ERROR` panics unless `optional_resource`; line 20 quote verbatim.
- UF2: `uri.c` 364 `URI_ERROR("Resource \`%s\` not valid.", resource);` verbatim.
- UF3: `uri.c` 220-222 PXE → `uri_tftp_dispatch`; 237-238 `volume_get_by_coord(boot_volume->is_optical, boot_volume->index, partition)` verbatim.
- UF4: `uri.c` 119 drive-omitted message verbatim.
- UF5/UF6: `chainload.c` 414-437 — `PATH` then `IMAGE_PATH`, `secure_boot_active` saved/cleared around `uri_open`, NULL →
  `panic(true, "efi: Failed to open image …")` at 435; the code comment matches. `menu.c` 1714-1717 forces
  `hash_mismatch_panic = true` under Secure Boot. Holds.
- UF7: `panic.s2.c` 24-28 clears `allow_menu` under `measured_boot`; 70-78 menu return gated on
  `efi_boot_services_exited == false && allow_menu`; 98 "System halted."; `menu.c` 1719-1728 measured boot = exactly `yes`
  or Secure Boot, forced off without `tpm_present()`; `config.c` 488-492 clears `secure_boot_active` on an empty config
  checksum. Holds, including the narrowing done on ScoutSources.
- UF8 is labelled `[inf]`, states that the firmware TPM protocol was not probed and nothing was booted — honest.
Reasons for `unprovable-but-better`: new ground (absence grep 0 → 2 files) answering the r88 routed R88-R5 question with
operator consequences (a missing UKI is a recoverable panic here; measured boot or enrolled Secure Boot would halt); every
`[src]` row re-derivable from tag-pinned bytes I re-opened; the host-specific consequences grounded in a committed
read-only receipt; four rows reworded and two narrowed on wave findings before admission. Not `improved`: an exploratory
claim has no counting predicate.

### Owned-axis harm

`git diff dfeaab29 7f3f30b3 -- SCORECARD.md` → three appended sections (declaration, measured outcome, addendum), no removed
line; "Axes now: depth8, coverage9, operability9, freshness9, calibration9, adjacency8 (unchanged)".
`git diff dfeaab29 7f3f30b3 -- corpus/knowledge | grep -c '^-[^-]'` → 0. SKILL.md: two registry rows added
(`limine-pin-battery-r89`, `battery-discrimination-r89`), nothing removed. Census:
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → rc 0, 52 W04 (all pre-existing
duplicate-URL warnings), `tsukuroi ok`; SOURCES rows 360 → 363 (`grep -c '^| S[0-9]'` at both tips). No axis harmed.

| Axis | Verdict |
|---|---|
| operability | unchanged |
| depth | unprovable-but-better |
| coverage | unchanged |
| freshness | unchanged |
| calibration | unchanged |
| adjacency | unchanged |

## 3. Discernment spot-check (`corpus/lessons/round-89.md` `## Gate`)

| Item | Gate decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S361 chainload.c (code/A) | ADMIT | `curl https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/protos/chainload.c` → `cmp` = pinned; `sed -n 435p` | agree | Line 435 reads exactly the Gate quote (13 words); it is the only source stating what an unopenable `path:` does to an `efi` entry, the protocol of all six host entries. |
| S362 panic.s2.c (code/A) | ADMIT | `curl …/v12.9.4/common/lib/panic.s2.c` → `cmp` = pinned; `sed -n 70,100p` | agree | Raw 78 is the Gate quote verbatim; 24-28 and 98 support the measured-boot halt. Turns the gate's word `panic` into what the operator sees. |
| Limine trunk as host-behaviour source | REJECT | `curl …/limine/trunk/common/lib/uri.c` (HTTP 200, 738 lines); `cmp` vs the v12.9.4 pin → differs; `grep -c -i blake3` trunk 1 vs tag 0; `pacman -Q limine` → 12.9.4-1 | agree | Trunk already diverges from the installed tag on the cited file (BLAKE3 present), so rows sourced from it would describe a bootloader this host does not run. |

SOURCES row re-opened: S362 (`corpus/SOURCES.md` line 373): URL resolves (re-fetched, byte-identical to the pinned
snapshot), anchors 18-29/70-86/87-100 resolve; the grounding ≤25-word quote is in the Gate table (raw 78, 13 words,
verified above); `teaches` paraphrase (20 words) matches the code.

## 4. Trend verdicts

- **expansion — unprovable-but-better.** One entry on uncovered ground (absence grep 0 → 2 files), 8 rows, +3 tier-A rows
  360 → 363; admission rests on the C2 exploratory ruling above.
- **quality — improved.** r88 routed 1 closed with a sweep receipt (`after/m1-sweep.txt`: superseded sentence present at
  `dfeaab29`, absent at `81f68d00`); r88 routed 3 filed as an erratum; QUALITY 127-129 added (6 lines), each with a
  receipt; entry rows reworded/narrowed on wave findings before admission; registry 142/142, headers 105/105 (evidence).
- **discernment — improved.** My spot-check agrees on two admits and one reject; the lane's own wave found the name leak
  and the L1 built and ran the forgery on the frozen counter rather than reading 62/62 as proof.

## 5. Routed defects (lane must fix next round)

1. C1 successor counter (R89-R1): run every gate under a constant name (`gate.py`) and strip argv-derived text, so no
   roster file name can reach the battery; count `--runs 0` as void; void on an unlisted roster file; make the
   AF_UNIX socket path independent of `--scratch` length (crash at > 45 bytes reads exit 1 = `unmet`); add a committed
   name/usage-oracle control and controls that kill the six surviving counter mutants (MutCounter) before any new 62/62.
2. Battery: certify `path =` deterministically (R89-R3 `KEY-SPACING` decoy) and add families for the clauses no family
   draws (R89-R4: containment, >1 MiB files, panic-after-pin, empty resource/label, non-UTF-8 configs).
3. Counter docstring line 24 overstates the instrument ("No … file name … visible"); correct it with the successor and
   sweep every mention (QUALITY 127).
4. C2 follow-ups stay routed in the lane's own lesson (R89-R5 gate consequence `panic` for `efi` `LP-MISSING`; R89-R6
   v12.9.5/6 drift and ScoutSources SR rows not admitted).
5. Fleet, not lane: `scripts/hyaku/fleet-commit.sh` keeps the jj change's creation time as the report's author date, so
   the first report commit again predates the lane commit it cites (r88 routed 4 recurs through the helper). Owner:
   operator/protocol lane (fleet helper); the lane's amendment `765cca05` is the correct workaround.

## 6. Notes for the operator

SHONEN: all four boxes are `[~]`; the "instructions executable without oral context" box still lacks a no-oral-context
retest and the counter has an undocumented scratch-length limit, so the set is not fully checkable by a non-author yet.
Promotion is operator-owned; nothing promoted here. L0 `tsukuroi | round-86 | HOST INCIDENT` remains open.
