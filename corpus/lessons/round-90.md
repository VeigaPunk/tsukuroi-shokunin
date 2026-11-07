# Round 90 — lesson (tsukuroi)

author: TsukuroiR90 (L1). Pre-round tip `c0f91856a5cc4816ae5d075022f16dc6aef0593c`; freeze
`6511437e7d86d3f1e7e39a45df91ade1d8293612` (battery r90, 29 controls ×3 canonical, pinned v12.9.4 sources, host
receipt, S364, declaration); clone-layout control receipts `cd165cf29071cc1f61ae3a5194b65d25f298894e`; candidate
`ce89df93e5f576c5c236d4547299e9ea954e8853` (gate r90, registry row, R90-REG-1); C1 measured at `ce89df93`
(`587234994bbea98559daa5f92b01e7fe6f01a492` carries the receipts). Citations are by hash.

## Inputs read

Round-89 closure (MANIFEST `rounds[]` index 1471, `rejected-honest-stop`, the second in a row after r88 index 1461)
and `corpus/lessons/round-89-verifier-spotcheck.md` §5. Disposition of its routed defects:

| Routed | Disposition this round |
|---|---|
| 1 — successor counter for R89-R1 (constant gate name, `--runs 0` void, unlisted roster void, socket path, name-oracle control, six counter mutants) | Not this round's instrument: C1 moved back to the gate surface (no counter is used). The `--runs 0` class is mined below (M1, QUALITY 130) and closed in the r90 battery; the rest of R89-R1 stays routed (R90-R4). |
| 2 — `path =` decoy; families for containment, >1 MiB, panic-after-pin, empty resource/label, non-UTF-8 | Repaired inside the frozen r90 battery with one near-miss control each: KEY-SPACING `path =` (N24), LARGE-FILE (N25), NON-UTF8 (N26, killed by crash rows), PANIC-AFTER-PIN (N27); the empty resource name is enumerated in BAD-RESOURCE. PANIC-AFTER-PIN turned out to encode a Limine-false answer (M2). Containment (gate hardening, not Limine) and the empty label stay routed. |
| 3 — r89 counter docstring line 24 overstates the instrument | Not corrected this round (the counter is retired as an instrument, not edited); the statement stands as a falsified record in `tools/battery-discrimination-r89.py` and the r89 spot-check. Routed R90-R4. |
| 4 — C2 follow-ups R89-R5 (gate consequence `panic` for an efi `LP-MISSING`) and R89-R6 | R89-R5 is this round's C1 surface (rule R9). R89-R6 SR1-SR4 (volume layer, `tpm_present()`) are re-opened by the L1 and admitted as C2 rows TV1, TV5, TV7, TV8. |
| 5 — fleet helper author date | Fleet-owned; this report is committed once, after the last lane commit. |

## Gate

Sources opened 2026-11-06/07 (America/Sao_Paulo) by the L1: `git clone --depth 1 --branch v12.9.4
https://github.com/limine-bootloader/limine.git` (HEAD `8ad14430bc9f2c24679cda558981ef53e6e3b18c`; host runs limine
12.9.4-1) and `git clone --depth 1 --branch v262.1 --filter=blob:none --sparse https://github.com/systemd/systemd.git`
(HEAD `73612ea502d53baf9b0df4336cfc296a7ee0d524`; host runs systemd 262.1-1). Pinned copies:
`.ufo/waves/round-90/before/src/` (C1; five files `cmp`-identical to the r87/r89 pins) and
`.ufo/waves/round-90/after/src-c2/` (C2; `SHA256SUMS`, `URLS.txt`, `PROVENANCE.txt`).

| Candidate | URL, access date, location | Located quote (≤25 words) | Decision, reason and flip |
|---|---|---|---|
| S364 (new, code/A) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/lib/gterm.c, 2026-11-06, raw 620-630, 700-712 | "if ((bg_file = uri_open_optional(background_path, MEMMAP_BOOTLOADER_RECLAIMABLE," (raw 625) | ADMIT, C1 R6: the only source that makes wallpaper/term_font optional opens, so an invalid resource there is `skip`, not `panic`. Flip: a limine upgrade that opens them with `uri_open`. |
| S365 (new, code/A) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/lib/tpm.c, 2026-11-07, raw 68-115 | "return tcg2 != NULL \|\| cc != NULL;" (raw 114) | ADMIT, TV1: defines what `--tpm-present` stands for. Flip: as S364. |
| S366 (new, code/A) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/lib/part.s2.c, 2026-11-07, raw 575, 597-598, 1035-1061 | "&& strcasecmp(volume_index[i]->fslabel, fslabel) == 0) {" (raw 1056) | ADMIT, TV5/TV7/TV8. Flip: as S364. |
| S367 (new, code/A) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/fs/file.s2.c, 2026-11-07, raw 27-31 | "bool fs_get_guid(struct guid *guid, struct volume *part) {" (raw 27; body `return false;` raw 30) | ADMIT, TV5/TV6: no filesystem GUID is ever read, so the vfat serial cannot match. Flip: a release that implements `fs_get_guid`. |
| S368 (new, code/A) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/lib/bli.c, 2026-11-07, raw 92, 110-124 | "gRT->SetVariable(L\"LoaderDevicePartUUID\"," (raw 119) | ADMIT, TV2/TV8: Limine writes the boot partition GUID and no TPM variable. Flip: as S364. |
| S369 (new, code/A) | https://raw.githubusercontent.com/systemd/systemd/v262.1/src/boot/export-vars.c, 2026-11-07, raw 57-63 | "s = xasprintf(\"0x%08x\", active_pcr_banks);" (raw 61) | ADMIT, TV2/TV3: who writes `LoaderTpm2ActivePcrBanks` and in what format. Flip: a systemd release that changes the stub's export. |
| S370 (new, code/A) | https://raw.githubusercontent.com/systemd/systemd/v262.1/src/boot/measure.c, 2026-11-07, raw 153-183, 194-216 | "if (!capability.TPMPresentFlag)" (raw 177) | ADMIT, TV2/TV4: what a zero bank mask means. Flip: as S369. |
| S371 (new, own-work/A) | `.ufo/waves/round-90/after/host-c2-receipt.txt` (2026-11-07T00:02:54-03:00; `systemd-analyze has-tpm2` appended 00:47) and `.ufo/waves/round-90/before/host/receipt.txt` | "LoaderTpm2ActivePcrBanks attrs: 06 00 00 00 value:0x00000000" (host-c2-receipt line 3) | ADMIT, TV3/TV6/TV7/TV8/TV9 host values. Flip: any boot after a firmware TPM or disk change (recheck event). |
| S372 (new, spec/A) | https://www.trustedcomputinggroup.org/wp-content/uploads/EFI-Protocol-Specification-rev13-160330final.pdf, 2026-11-07, p. 29 §6.4.4 item 5 (L1 `curl`, sha256 `40a2568e…`, the same digest wave seat ScoutTPM recorded) | "If the platform does not have a TPM then the following values SHALL be returned:" (p. 29) | ADMIT, TV2: the normative meaning of a zero `ActivePcrBanks`, which systemd's code alone does not give. Flip: a later TCG revision that changes the no-TPM reply. |
| REJECTED (this round): ScoutTPM rows A2, A6, A7, A11, A12 (PicoEFI headers, systemd `efi-api.c`/`tpm2-util.c`, edk2 `UefiMultiPhase.h`); ScoutVolume SV rows beyond its findings 1-2 and its draft rows S373-S376 | `.ufo/waves/round-90/w1/ScoutTPM/proposed-sources.md`, `.ufo/waves/round-90/w1/ScoutVolume/proposed-sources.md` | — | NOT ADMITTED: not re-opened by the L1 this round (CORPUS.md rule 1); TV9 therefore states only the tool's output. `disk.s2.c` (ScoutTPM A13, ScoutVolume) was re-opened and admitted as S373. Flip: a round that opens them. |
| S373 (new, code/A) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/drivers/disk.s2.c, 2026-11-07, raw 986-988, 1004-1016 | "if (ret == NO_PARTITION)" (raw 1012) | ADMIT, TV5/TV8 corrections on wave seat ScoutVolume's findings 1-2: only a whole disk carries a GPT disk GUID; partition numbers keep slot gaps. Flip: as S364. |
| REJECTED: `hdd(1:1)` as this host's ESP (wave seat ConnectorOverlap §4 proposal) | Limine `volume_get_by_coord` drive index (`part.s2.c` 1064-1074) | — | REJECT for the entry: the drive index is Limine's firmware enumeration order, which Linux does not expose; three disks are present (`before/host/receipt.txt` 26-41). Flip: a Limine verbose boot log that names the index. |
| REJECTED: `systemctl --version` `+TPM2` as a TPM-presence signal (sibling capture, ConnectorOverlap §2) | mori-shokunin capture line 10 | — | REJECT: a compile-time feature list, not firmware state (TV1). |

Registry changes, old→new: S364-S373 absent → `mined` (opened 2026-11-06/07; recheck `on-release` for S364-S370 and S373,
`30d` for S371, `365d` for S372). No existing row's status changed; S351, S352, S353, S361, S362 are cited by the new entry and keep their
rows (used-by not widened this round: the census does not require it, and their anchors are unchanged).

Assimilation: none (no `merge/tsukuroi/` theme taken). considerthese: none fits — every proposal of the latest file
`considerthese/2026-10-26.md` is already adopted (QUALITY 103, 108, 110, 112, 115; wave seat ConnectorOverlap §3).

## Errata

- `corpus/knowledge/limine-pin-plane-r87.md` LP5 ("read from the first occurrence in the file") is too wide:
  Limine sees `hash_mismatch_panic` and `measured_boot` only in the global section unless the file's first line is
  an entry line (`config.c` raw 642-650). Erratum appended to that entry; carrier map
  `.ufo/waves/round-90/after/erratum-sweep.txt`: LP5 (md and json) — corrected by erratum; the r87, r88, r89 and r90
  battery docstrings (R6 "in the whole file") and r90 R10 — standing as falsified record in frozen instruments;
  `tools/check-limine-pins.py` (reads the key anywhere) — routed R90-R1; `SCORECARD.md` r90 declaration clause map
  "R10 whole file" — standing as declared (the declaration is frozen).

## Mistakes

| Class | Evidence pointer | Captured-by | Fix | Shown able to fail |
|---|---|---|---|---|
| **M1 `R89-EMPTY-RUNS-MET`** — an instrument's CLI accepts a degenerate count that empties its evidence set, so the verdict is vacuous | `7f3f30b3:tools/battery-discrimination-r89.py:275, 303, 307-308` (`--runs` with no floor, zero runs, `all()` over nothing → `verdict met` rc 0); `7f3f30b3:tools/limine-pin-battery-r89.py:1112, 1128, 1135` (rc 0, no output); filed by r89 CriticClaims (`.ufo/waves/round-89/w1/CriticClaims.md:104-113`) | none (QUALITY 116/126 do not cover the count's domain) | QUALITY 130; `tools/limine-pin-battery-r90.py` refuses `--runs < 1` with rc 2 (frozen bytes `8f0daee8…`) | yes: r89 battery and counter with `--runs 0` exit 0 (`verdict met` for the counter); r90 battery exits 2 with no verdict line (`.ufo/waves/round-90/w1/ScribeLesson/draft-mistakes.md`, commands; seat ScribeLesson, run in a clone) |
| **M2 `R90-VISIBILITY-WHOLE-FILE`** — a setting's visibility was read from the accessor (`config_get_value(NULL, …)` scans `config_addr`) without the write that cuts `config_addr` before the first entry line | r87 LP5; battery r87-r90 R6 "FIRST `hash_mismatch_panic` key line in the whole file"; r90 R10 and families MEASURED-IN-ENTRY, PANIC-AFTER-PIN (`tools/limine-pin-battery-r90.py` at `6511437e`); found by wave seat ReviewSource F1 | QUALITY 106 (read the pinned definition before freezing) — applied to the accessor, not to its caller's buffer | QUALITY 131; erratum on LP5; gate and battery correction routed (R90-R1) — not counted as a fix this round | red shown: `.ufo/waves/round-90/after/visibility-probe.txt` (fixture A: landed gate `halt`, global-only probe gate `menu`; fixture B: both `halt`); the corrected gate is next round's work |

## Routed to round 91

- **R90-R1** (ReviewSource F1): correct R6/R10 visibility — `hash_mismatch_panic` and `measured_boot` count only in
  the global section unless line 1 is an entry line (`config.c` 642-650) — in the gate and in a successor battery
  with one family per visibility boundary (QUALITY 131); MEASURED-IN-ENTRY and PANIC-AFTER-PIN are wrong as frozen.
- **R90-R2** (ReviewSource F2, ReviewGate F1): an efi image line that is not a pin (unhashed, empty or URI-less)
  still goes to `uri_open` and panics when unopenable (`chainload.c` 414-435); the gate reads such a conf HEALTHY.
  Decide between a reported `unverified_image_lines` field and a new status; patch draft
  `.ufo/waves/round-90/w1/ReviewGate/patch-F1-unverified-image-lines.diff`.
- **R90-R3** (CriticForgers G1-G3; ReviewGate F2-F4; ReviewSource F4/F5): battery roster gaps IMAGE-PATH-NOT-PIN,
  BLANK-IN-BODY, MEASURED-NON-YES; R8's text versus the battery's own oracle for a bare `/` line and `\v`/`\f` label
  ends (the gate and the oracle agree, the docstring does not); unreadable-conf output shape; a positive `$boot()`
  selftest case; `--runs 0` control in the next freeze (QUALITY 130 residual).
- **R90-R4**: the remainder of r89 routed 1 and 3 (counter successor and its docstring) — open only if a counter is
  used again.
- **R90-R5** (ScoutDrift): Arch carries limine 12.9.6-1 (the host runs 12.9.4-1; the local sync DB predates it).
  Between the pins and 12.9.6: R1's strip loop now removes blanks before CRLF (the r90 R1 text matches 12.9.6, not
  12.9.4 — the r89 R89-R2 finding from the other side), a conf whose first line is an entry has no global options
  since 12.9.5 (CONFIG.md and the v12.9.6 changelog say so), `guid()`/`fslabel()` retry after connecting all disks,
  and the R9 entry-body code moved (`config_get_entry` deleted; rule unchanged). Re-pin the rule set on the host
  upgrade and freeze the visibility families against the version the host runs.

## Wave w1 (13 seats; attack 6/13; 0 dead)

Shape: one v1 wave, 13 seats (executor 2, mutation-tester 2, critic 2, reviewer 2, scout 3, connector 1, scribe 1),
validated under `scripts/hyaku/ufo-wave-policy.json` (`.ufo/waves/round-90/w1-validate.err` empty), dispatched by the
orchestrator from `w1.ready` (marker `w1.ready.dispatched` 2026-11-06T23:50:50); all 13 reports present
(`w1-results.json`). The L1 holds the planner seat. No residual call.

- ExecReplicate: 73/73 ×3 clone and canonical at `ce89df93`; manifest 40/40; selftests 25/25 and 18/18.
- ExecLints: registry 143/143, headers 105/105, census rc 0, no hardcoded `/tmp`.
- MutGate: 26 of 29 held-out gate mutants killed; survivors m05 (`image_path` key case), m08 (LP-BAD-RESOURCE-only
  file rc 2), m20 (`.strip()` on the measured value) are roster gaps routed with R90-R3 (`w1/MutGate.md`).
- MutBattery: 21 of 43 battery mutants detected by the committed controls (`w1/MutBattery.md`).
- CriticForgers: docstring-only `base.py` met 73/73 ×3; 28 of 31 one-clause forgers killed (G1-G3 roster gaps).
- CriticClaims: oracle-import forgery 73/73 (channel unnamed), docstring post-pass 73/73, QUALITY 104/125/126 gaps,
  QUALITY 114 order deviation (disclosed draft), R9/R10 source-backed except the visibility point.
- ReviewSource: F1 visibility (C1 honest stop), F2 unhashed image lines, F3 `tpm.c` unpinned for C1 (pinned for C2),
  F4 R8 label, F5 wallpaper read globally.
- ReviewGate: F1 unhashed image lines, F2 label edge cases, F3 unreadable-conf shape, F4 selftest `$boot()` blind
  spot; N2 (indented entry lines) refuted by `config.c` 527-551, which strips leading blanks before `/` is tested.
- ScoutTPM: `--tpm-present 0`, TCG spec, `systemd-analyze has-tpm2`; A1/A7/A8 integrated as TV2/TV4/TV9.
- ScoutVolume: TV5/TV8 corrections (disk GUID arm, slot gaps); 50 000-text GUID round-trip harness.
- ScoutDrift: R90-R5; confirms the visibility divergence independently (its §3-B shape C).
- ConnectorOverlap: no sibling conflict; considerthese none fits; `hdd(1:1)` and `+TPM2` proposals rejected (Gate).
- ScribeLesson: M1 drafted with shown-able-to-fail receipts; QUALITY 130.
