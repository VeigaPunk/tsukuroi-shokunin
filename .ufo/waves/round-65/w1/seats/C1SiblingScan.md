# C1SiblingScan — round-65 sibling overlap scan (connector, w1)

**Seat:** C1SiblingScan (connector) · **item:** OVERLAP-SCAN · **execution class:** READ-ONLY
**Wave:** w1 (the round's only wave) · **lane:** tsukuroi, round 65 (hyaku run 15)

## What I did

Read-only scan of every sibling lane repo for a claim on round 65's new ground — C1 the
systemd v262 NvPCR/UKI requirement plane measured against this host's boot chain, and C2 the
initramfs census arm — plus a gate-impact measurement of C2 against the lane's own
cross-lane register.

Full per-sibling table, per-hit `file:line` list, ADJ-row reasoning, the proposed move and
its verification recipe are in
**`.ufo/waves/round-65/drafts/overlap-scan.md`** (written; the L1 asked for it there).
Machine receipts: **`.ufo/waves/round-65/w1/C1SiblingScan-receipts.txt`**.

Commands (all read-only; no mutating git anywhere in any lane repo):

```
ls -1 /home/vgpnk/Projects/shokunin/                       # sibling inventory
for s in mori kama kaidoku revenger tameshi kumitate kengaku kasegi kake kotoba \
         kotodama chousa tabi souji mado kagi; do
  git -C /home/vgpnk/Projects/shokunin/$s-shokunin rev-parse HEAD
  git -C …/$s-shokunin grep -niE 'nvpcr|ukify|systemd-stub|sign-initrd-pcrs|unified kernel image|\bUKI\b|tpm2-setup|PCR policy' \
      HEAD -- '*.md' '*.json' '*.py' '*.sh' ':(exclude).ufo/*'
  git -C …/$s-shokunin grep -niE 'initramfs|mkinitcpio' HEAD -- … ':(exclude).ufo/*'
  git -C …/$s-shokunin grep -niE '/EFI/Linux|omarchy_linux\.efi|/boot/EFI|/boot/vmlinuz|systemd-stub' HEAD -- …
done
git -C tsukuroi-shokunin show HEAD:PROVINCE.md | sed -n '8,14p;22p'
python3 tools/check-adjacency-anchors.py  --revision 37c74e27b29d979ee749caa622eb58f9bfe39ed4
python3 tools/check-adjacency-overlap.py --revision 37c74e27b29d979ee749caa622eb58f9bfe39ed4
git clone --shared <lane> /fast/scratch/hyaku/tsukuroi-r65/C1SiblingScan/laneclone   # private fixture
```

## Verdicts (summary; the table with pointers is in the draft)

**No sibling claims this round's ground.** Across 16 sibling repos (the 15 named plus the
two HOLD lanes' `PROVINCE.md`), tracked non-wave content, the UKI-family terms
(`nvpcr|ukify|systemd-stub|sign-initrd-pcrs|unified kernel image|\bUKI\b|tpm2-setup|PCR policy`)
score **0 hits everywhere** except one capture artifact in souji
(`census/round-43/waves/w1/R43connector01/scan-receipts.json:25` holds a *copy of
tsukuroi's own* `SKILL.md:48` row) — a capture, not a claim. The `initramfs|mkinitcpio`
family scores 13 in kotoba, 4 in souji (historical census fixtures), 3 in mado, 0 elsewhere.

- **kotoba — AGREES, owner tsukuroi.** The only sibling naming the C2 subject, and it
  *cedes* it: `kotoba/PROVINCE.md:78` (*"tsukuroi owns host package and initramfs hooks
  and OS state as read-only probes (PROVINCE.md:22)"*), `SKILL.md:14-15`, `SKILL.md:127`,
  `corpus/knowledge/hook-files-round59.md:20`, `corpus/knowledge/sibling-overlap-census-round74.md:33,35,42,103`,
  `corpus/lessons/round-74-verifier-spotcheck.md:83-84`. The lane side resolves at both the
  pin kotoba quotes (`8bd001f58bfd`) and at lane HEAD (`37c74e27`): `PROVINCE.md:22` is the
  `Initramfs v42 and boot recovery` row. → **INBOUND-RESOLVES**, owner tsukuroi.
- **mado — AGREES, owner tsukuroi.** `tools/mado-tripwire.py:264` puts `mkinitcpio` and
  `bootctl` in `HOST_MUTATION_BINS` — mado refuses to let an agent run them, the same
  direction C2's arm takes (no mkinitcpio/ukify/bootctl call, no privilege, no write).
- **mori — adjacent, not a claim.** `PROVINCE.md:13` refuses *"driver/firmware and boot
  state (→ tsukuroi)"*; `:66` names tsukuroi as owning *"host OS, package, systemd-unit,
  driver, firmware, and boot diagnosis"*. mori already routes C1's ground to tsukuroi.
  Pre-existing drift, not caused by this round: mori re-pinned its pointer to
  `../tsukuroi-shokunin/PROVINCE.md:8-14` in `af42101d` (round 30), while the lane's
  register row **IN-067** still records the older `…PROVINCE.md:21-24,35-44` with
  `found_line 8`, class `DRIFTED`. The lane's register lags mori's live pointer.
- **kaidoku / revenger** keep shipped-artifact RE (kaidoku `PROVINCE.md:3`; revenger
  `:4` incl. `firmware`, S252 UEFITool) — the C1 subject, but neither has read this host's
  boot chain (0 hits) and neither claims it. **ADJ-06 is a boundary, not a conflict.**
- **tameshi** names tsukuroi's census as a read-only primary surface
  (`PROVINCE.md:32`) — method ownership, ADJ-07, untouched by C2 as scoped.
- All others: **LANE-GAP** — nothing to reconcile.

## ADJ rows that govern

**ADJ-06** (kaidoku/revenger) — named as the boundary, **not triggered** by the landed
claims. C1 measures requirement text plus host state (`bootctl` fields, `pacman -Qo`
ownership, mkinitcpio drop-ins, hook inventory, `ukify` presence) and names no binary
internals; the draft note's boundary line says so, and SY5 holds *"whether the current UKIs
embed the four `.nvpcr` defs (needs a UKI content read)"* as an explicit unknown. C2 reads no
artifact bytes at all. **ADJ-07** (tameshi): not triggered; the census implementation and
its selftest stay in this repo (`PROVINCE.md:52`). **ADJ-04** (mori): not triggered — no
pressure/kill measurement; the note keeps pressure attribution with mori. **ADJ-02**
(kagi): not triggered — the C2 arm stats `/etc/mkinitcpio.conf` and never opens it
(`tools/tsukuroi-census.sh:417-420`). ADJ-01/03/05: not in scope.

## The one non-obvious move

**Land a one-field companion re-pin of the lane's own IN-109 anchor in the same commit as
the C2 census edit** — `corpus/knowledge/adjacency-anchors-r19.json` `inbound[].found_line`
for IN-109, plus the mirrored cell at `corpus/knowledge/adjacency-anchors-r19.md:204`.

Measured on a private `git clone --shared` of the lane (the lane repo was never written):

- lane HEAD `37c74e27`: `check-adjacency-anchors.py --revision 37c74e27…` → **PASS**,
  `inbound_total 114`, `inbound_classified 114`, `{RESOLVES 96, DRIFTED 17, UNRESOLVABLE 1}`,
  `outbound_portable 10`, `findings: []`.
- lane HEAD **+ the round-65 worktree census** (`fe15cc5d…`, +245 lines), committed in the
  scratch clone: the same gate goes **red** —
  `INBOUND-CLASSIFICATION-WRONG` at `…/adjacency-anchors-r19.json:inbound[108]`
  (*"found_line is not an occurrence of evidence_quote"*) — because the C2 arm moves the
  D14/D15 selftest case that IN-109's quote points at from census line `2683` to `2822`.
- re-pinning that single `found_line` to `2822` restores the HEAD counts exactly.

IN-109 is the one register row whose evidence quote lives *inside* the file C2 edits
(tameshi's `service-optin-protocol.md:153` → `tsukuroi-census.sh:915-970`), and the
register's own note already records this re-pin ritual for rounds 32, 38, 39 and 42. The
round-65 C2 predicate names only *"registry-coverage + knowledge-header gates PASS"*
(`SCORECARD.md:4799`), **not** the adjacency-anchors gate — so without the companion
re-pin a green C2 measurement still leaves a red adjacency gate in the lane's own register
at the round's tip.

**Axes:** adjacency (the round's tied-lowest, 8) improves — the lane's published
cross-lane register stays truthful about a sibling pointer into the file the round edits.
**No harm:** one integer in one JSON field plus one mirrored table cell; no counted value,
no sibling repo, no claim predicate, no sibling-facing text changes. **Risk (bounded):**
the number must be computed against the *landed* census bytes, not the current worktree
bytes — the C2 arm is still being edited, so `2683 → 2822` is today's worktree value and
will move again. Recipe: after landing the census edit, run
`grep -n "degraded: kernel ring class counts are evidence" tools/tsukuroi-census.sh` and
write the number it prints into both mirrors. **Verification:** re-run
`check-adjacency-anchors.py --revision <landed-census-commit>` (expect PASS,
`inbound_total 114`, `{RESOLVES 96, DRIFTED 17, UNRESOLVABLE 1}`) and
`check-adjacency-overlap.py --revision <landed-census-commit>` (measured PASS on the
C2-applied clone: `anchored_rows 6`, `expected_rows 6`, `status PASS`).

## Defects seen (reported, not absorbed)

1. **C2 selftest flakiness — belongs to the C2 executor seat.** The new case
   `initramfs: the arm changed a line other than INITRAMFS, so it is rollup input (R65-C2)`
   fails intermittently: `FAIL (177 cases, 176 passed, 1 failed)` on 3/3 fresh-TMPDIR runs
   in one batch, `PASS (177 cases, 177 passed, 0 failed)` on 3/3 in another, and PASS on
   later single runs. The differing lines are **memory-plane** values
   (`PLANE drivers: … C5_pswp=37405521/… C6_avail_kb=20797628 …` vs
   `C5_pswp=37405522/… C6_avail_kb=20852120 …`) — live `/proc` drift between the two runs,
   not a property of the C2 arm. The arm's `ENV_BASE` does stub
   `TSUKUROI_MEMINFO_FILE`/`TSUKUROI_PRESSURE_FILE`/`TSUKUROI_VMSTAT_FILE` to fixture
   paths (`tools/tsukuroi-census.sh:2500-2502`), so the fixture is not fully hermetic for
   those counters. Not finished: I did not capture the per-case differing-line set on a
   failing run (my instrumented clone writing to `TSUKUROI_DBG_DIR` never fired because
   the failure did not reproduce in four instrumented runs); the diff above comes from two
   identical fixture runs of my own harness and is the best-supported account, not a
   per-case capture.
2. **Lane register lag vs mori's live pointer** (IN-067, described above) — pre-existing,
   lane-side, not caused by round 65.
3. **Published mirror already behind the JSON** for IN-109: `adjacency-anchors-r19.md:204`
   shows `Found line 2277` while the JSON holds `2683`. The companion re-pin fixes both.
4. **Out of this round's ground, reported for another lane:** a misrooted sibling tree
   `/home/vgpnk/Projects/shokunin/kumitate-shokinin/kumitate-shokunin/.ufo/waves/round-69/w1/K69ExecBaseCounter.md`
   holds a **byte-divergent** copy of kumitate's tracked
   `.ufo/waves/round-69/w1/K69ExecBaseCounter.md` (sha256 `9295423f…` vs the tracked
   `d2ccc0ab…`, 4826 vs 4801 bytes; the copy carries an older wording of the same receipt).
   The fleet root `.gitignore:1` (`*-shokunin/`) hides it from git status, so it is invisible
   to a git-based sweep. That is souji's hygiene surface (stray/duplicate artifacts), not
   tsukuroi's; noted, not touched.

## Files written

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-65/drafts/overlap-scan.md`
  (the L1-requested per-sibling table + verdicts + exact pointers)
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-65/w1/C1SiblingScan.md`
  (this report)
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-65/w1/C1SiblingScan-receipts.txt`
  (machine receipts)

Nothing else was written: no sibling repo, no `LOG.md`/`SCORECARD.md`/`SKILL.md`/
`PROVINCE.md`/`corpus/SOURCES.md`/`corpus/knowledge/`, no `.ufo/state/`, no `MANIFEST.json`.
No mutating git ran in any lane repo; the only commits were inside private
`git clone --shared` scratch trees.

## Scratch-clean confirmation

Scratch root `/fast/scratch/hyaku/tsukuroi-r65/C1SiblingScan/` held five `git clone --shared`
fixture trees (`laneclone`, `laneclone2`, `laneclone3`, `laneclone4`, `laneclone5`, plus
`lanecloneH`), the `receipts.txt` receipt, and the TMPDIR probe directories. All receipts
were copied into `.ufo/waves/round-65/w1/C1SiblingScan-receipts.txt` **before** cleanup.
The scratch root is removed as the last step of this seat; `/tmp` holds no citable evidence
of mine (the only `/tmp` write was `reg_f33379c3.json`, a scratch-tree artifact copied
under the scratch root).
