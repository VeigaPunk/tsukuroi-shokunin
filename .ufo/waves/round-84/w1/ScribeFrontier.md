# ScribeFrontier — round 84, wave w1 (scribe, drafts only)

Seat: SCRIBE. Mission: draft the corpus README append and the LOG.md entry for round 84. Drafts only; no
lane file edited.

Lane revision measured: `c6941adbcd972de8ad1b93ce5f796e16ea630858`
(`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master`, rc 0).

Drift observed after the read set was taken: master advanced to `f19e73f3aa9817e76044e4e43a343c6ca6d929df`
("round-84: registry rows — single tool per row, code-2 maps", `SKILL.md`, 3 lines changed). No file this
seat read changed, and both drafts name the advance. The working tree also shows `M corpus/lessons/round-84.md`,
a sibling seat's uncommitted edit, not this seat's.

Axes this seat serves: depth (exploratory C1, the plane's held rows) and freshness (what the corpus gains
that it did not hold at `64f45b79`). No ordinal is moved by a draft.

## Read set (all read-only)

- `git show 69915b86:SCORECARD.md | tail -80` — "Round 84 — declaration" and "Round 84 — C1 withdrawn as a
  measured claim, re-declared exploratory". Frozen predicates, targets, kill rules, instrument digests.
- `corpus/README.md` (845 lines): `## Quality`/coverage-map head, rounds 74-82 sections, `### Frontier
  (round-26 addition)` at :242 for the subsection shape, `## Frontier — round 83` at :834 for the tail style.
- `LOG.md` (3759 lines): round-82 and round-83 entries for the bold-lead paragraph style.
- `PROVINCE.md:1-45` — Core domain ("package state, systemd, drivers/firmware, boot health") and the owned
  surface table row "Initramfs v42 and boot recovery".
- `corpus/knowledge/hibernate-resume-plane-r84.md` and `.json`; `corpus/lessons/round-84.md` (56 lines, M1-M3);
  `corpus/QUALITY.md` rows 113-118; `corpus/SOURCES.md` rows S336-S342; `MANIFEST.json` (fleet root, read).
- `tools/check-hibernate-resume.py:1-140` (docstring rule set, `validate()`, `gate()`); `tools/resume-gate-battery-r84.py:1-60`
  (family list, target, 20 s, random bases); `.ufo/waves/round-84/before/host/{receipt.txt,facts.json}`;
  `.ufo/waves/round-84/before/controls/*`; `.ufo/waves/round-84/after/uki-initrd-contents.txt`.

## Gates run (verbatim; every unrun check is listed below as unrun)

1. `git rev-parse master` rc 0 -> `c6941adbcd972de8ad1b93ce5f796e16ea630858`.
2. Instrument bytes vs the frozen declaration, all four match:
   ```
   cb70d4357ebe2d50f360dbbc2079f3a35756a79fc785280cf9d4312268ac8309  tools/count-resume-rows-r84.py
   00310ac205f07f396bc4a7a0406f1c0d4baf74c7ab30e27245bbc89d8ce00964  tools/resume-gate-battery-r84.py
   cec27b9d19e4ac85ccaa513b94e37f568b51979c546133c3d4bc5f62cd6cea23  tools/capture-resume-facts-r84.py
   3d2e1cf58af1576924decb2280a38ba4225905e7de0af2b1c5df9362eccb4556  tools/check-hibernate-resume.py
   ```
   (the gate has no frozen digest: it is the candidate, not an instrument).
3. Pinned manifests: `sha256sum src/SHA256SUMS host/SHA256SUMS` rc 0 ->
   `5d1673de7f893f035cb2808e9579bcdd292339a32dad605c6e3a53d6561f7eef` and
   `4ca3e20939eadff71c190f5e2d27a5f453479d0133321ebd118eb7eef624fde6`, equal to the declaration. `src/`
   holds 8 snapshots, `src/SHA256SUMS` 8 lines, `src/URLS.txt` 9 lines.
4. C1 shape counter, `python3 tools/count-resume-rows-r84.py --revision 69915b86...` rc 0 ->
   `"verdict": "met", "counted": 10, "failed": 0, "distinct_snapshots": 6, "target_rows": 7, "target_snapshots": 4`,
   all ten rows `"reason": "ok"`. Reported as a provenance-shape reading only, per the withdrawal block.
5. New-ground negative, `git grep -c 'map-swapfile' 64f45b79 -- corpus/knowledge` rc 1, no output; the same
   revision's two mentions are `journal-boot-plane.md:62` and `systemd-user-plane.md:218`, both printing
   `resume_offset=3795013` only.
6. Frozen C2 controls read from the committed files: absent `families_passed: 0`, healthy `1`, allids `0`,
   basediff `0`, each `"families_total": 13, "target": 13, "verdict": "unmet"`.
7. Host observables used by the frontier draft:
   - `journalctl -b -g 'Image not found'` rc 0 -> `Nov 02 12:07:17 plazir27 kernel: PM: Image not found (code -22)`.
   - `journalctl --no-pager -g 'hibernation entry|hibernation exit'` -> two `-- Boot ... --` lines and `-- No entries --`.
   - Receipt anchors re-checked: `:40` `253:0`, `:44` `3795013`, `:52` `[platform] shutdown reboot suspend test_resume`,
     `:56` `12835467264`, `:79` `systemd 262 (262.1-1-arch)`, HOOKS `encrypt` at :71 before `resume` at :75.
8. Fleet `MANIFEST.json` `rounds[]` 1276/1297/1319 read: `round` 81/82/83, `type: closure`, `lane: tsukuroi`,
   `lanes: {tsukuroi: ok}` (total 1421 entries).

## Drafts

1. `.ufo/waves/round-84/w1/ScribeFrontier/readme-append.md` (5329 bytes)
   - Heading `## Round 84 — hibernate-resume plane`, a 3-column `| Note | Holds | Sources |` table with one
     row for `knowledge/hibernate-resume-plane-r84.md` and `.json` (HR1-HR10, host values, Limits) and
     `S336–S341; lessons/round-84.md Gate`.
   - Classification paragraph: deeper ground inside an existing PROVINCE area (Core boot health plus the
     owned "Initramfs v42 and boot recovery" surface), new ground in the corpus at `64f45b79`; C1 stated as
     exploratory (`unprovable-but-better` or `unprovable`, no ordinal move, the 10/10 counter earns nothing);
     C2 named as the round's measured claim with its 13-family target and the four control readings, and its
     outcome explicitly assigned to `SCORECARD.md`.
   - `### Frontier (round-84 addition)`: no resume exercised (with the `-22` lookup and the empty
     hibernation sweep as the only runtime trace), which writer set `/sys/power/resume`, the preconditions
     the gate does not read, `HR-OFFSET-MISMATCH` silent on a null `map_swapfile_offset`,
     `HR-SWAP-TOO-SMALL` as a bound, and the untouched round-82 swap-unit item.
2. `.ufo/waves/round-84/w1/ScribeFrontier/log-entry.md` (5432 bytes)
   - `## Round 84 — hibernate-resume gate and plane (fresh start, 2026-11-06)` with bold leads: Motivating
     evidence (r83 closure, MANIFEST 1276/1297/1319, the three procedural failures, the pre-round corpus
     gap), Freeze before data (`e0f42051`, three digests, 8 snapshots, host capture, four controls, C1
     selftest 12/12), C2 as declared (`c6ee78b2`, 8 rules, 11 IDs, 13 families, 5 random bases, 20 s,
     target 13/13), C1 as declared then withdrawn (`69915b86`, 10 rows, 10/10 shape reading, P1 control,
     `ReviewEntry`), Sources/lesson/registry (S336-S342, QUALITY 118, M1-M3, `c6941adb` registry repair),
     and Wave.
3. `.ufo/waves/round-84/w1/ScribeFrontier/proposal-entry-limits.md` (2382 bytes) - proposed patch for
   finding F1 below.

## Placeholder register (for the L1 to fill; none may be filled by this seat)

readme-append.md:
- `no resume was exercised` bullet: `<from ScoutHost: independent re-capture, and any retained-boot resume
  evidence beyond the -22 lookup>`.
- `which writer sets /sys/power/resume` bullet: `<from ScoutHost>`.
- `preconditions the gate does not read` bullet: `<from ScoutHost>`, with three named candidate surfaces
  (device node timing inside the initramfs, LUKS unlock ordering beyond HOOKS position, `/sys/power/disk`
  `[platform]`).
- C2 outcome is not stated at all; it stays with `SCORECARD.md`.

log-entry.md:
- `C2 ... Measured outcome: <from ExecBatteryC2 and SCORECARD.md>`.
- `Wave. <from the L1 at landing: seat count, settled seats, durable reports, attack share, residual call,
  dead seats>`.

Deliberate omissions: no 13/13, no wave counts, no seat deaths, no ordinal change is asserted anywhere; the
drafts contain only what files at the measured revision already print.

## Findings

- F1 (defect, entry, proposed patch not landed): `corpus/knowledge/hibernate-resume-plane-r84.md:50-52`
  enumerates only "no hibernation entry or exit" under Limits, while the boot-time image lookup is observed
  and logged on every retained boot (`PM: Image not found (code -22)`, `journal-boot-plane.md:64`,
  `:249-252`). This under-claims the available evidence and leaves the one runtime trace of the chain
  unmentioned. Patch: `ScribeFrontier/proposal-entry-limits.md` (one appended Limit bullet, nothing above
  rewritten).
- F2 (classification evidence, not a defect): "deeper ground inside an existing area" is supported by
  `PROVINCE.md:4` (Core includes boot health) and the owned surface row `PROVINCE.md:22` (Initramfs v42 and
  boot recovery: "inspect effective mkinitcpio drop-ins, hooks and recovery stages"), while new-corpus-ground
  is supported by the rc-1 grep at `64f45b79`. The drafts therefore say both, separately, and keep
  `PROVINCE.md` unchanged.
- F3 (reconfirmed, already declared): the C1 counter reads `met` on the committed entry and is a shape gate;
  its P1 control builds seven boilerplate rows and also reads `met` (`before/controls/c1-controls.txt`). The
  drafts state this and give the reading no credit.
- F4 (style constraint observed): README.md and LOG.md write no outcome for a claim whose measurement belongs
  to `SCORECARD.md` (round-82 instrument row precedent). Both drafts follow that split.

## Refused / out of scope

- No edit to `corpus/README.md`, `LOG.md`, `SCORECARD.md`, `MANIFEST.json`, `.ufo/state/`, or any lane file;
  the three artifacts above are drafts under the seat's own wave subdir.
- No `git add|commit|push|stash|checkout|switch|reset|pull`, no `jj` mutation; only `git rev-parse`, `git show`,
  `git log`, `git grep` were run.
- No host mutation: no hibernate, suspend, swapon/swapoff, sysctl, `/sys` or `/proc` write, no mkinitcpio, no
  pacman. `journalctl` and file reads only.
- Not run by this seat (owned elsewhere; unrun is not a pass): the C2 counting command
  (`ExecBatteryC2`), the gate `--live` run (`ReviewGate`), the per-row judgment (`ReviewEntry`), the mutation
  batteries (`MutGate`, `MutCounter`), and the independent host re-capture (`ScoutHost`).
- No tool installed or upgraded this round (tooling channel unused).

## Artifacts

- `.ufo/waves/round-84/w1/ScribeFrontier.md` (this report)
- `.ufo/waves/round-84/w1/ScribeFrontier/readme-append.md`
- `.ufo/waves/round-84/w1/ScribeFrontier/log-entry.md`
- `.ufo/waves/round-84/w1/ScribeFrontier/proposal-entry-limits.md`

Scratch: no scratch root was needed and none was created; every input read was already a committed lane or
fleet-root file, so no receipt required copying out and no `TMPDIR` was set.
