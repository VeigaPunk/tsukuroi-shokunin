2026-11-03T18:45:01Z

# CritC23 — attack review of C2 (freshness drift register) and C3 (mkinitcpio-42 plane), round 64 / w1

Reviewed at lane HEAD `2f3061ef725abebd8cd157b778203f1cf5c0cb0c` (the frozen declaration commit).
Both drafts landed before this review: `after/drift-table-draft.md` (E2Probes, rev 18:39Z) and
`after/mk42-rows-draft.md` (E3Mk42, 18:41Z). Frozen predicate sources: `LOG.md` "Round 64 —
declaration" (C1 bullet at LOG.md:2731, C2 at 2742, C3 at 2754, "Frontier step:" at 2776) and the
matching `SCORECARD.md` table. Receipt: `$ git -C tsukuroi-shokunin rev-parse HEAD` →
`2f3061ef725abebd8cd157b778203f1cf5c0cb0c`, rc=0.

## 1. Do-nothing controls (SS9)

**C2 control — write no receipts.** Rows without committed receipts do not count (LOG control
sentence), so a control writing none produces no note, `grep -c '^| DR'` = 0 rows, 0 drift —
**control score 0 < 5 drift, FAILS the frozen counter → discriminative.** Anti-control-equivalence
proof that the real submission is not accidentally the control: every receipt path named in
drift-table-draft.md exists:

```
$ for f in p1-installed-count.txt p2-explicit-count.txt p3-foreign.txt p4-orphans.txt \
    p4b-orphans-clean.txt p5-dk.txt p6-user-manager-state.txt p6b-system-scope.txt \
    p7-failed-units.txt p7b-user-timers.txt p8-journal-err-entries.txt p8b-journal-line-count.txt \
    p9-retained-boots.txt p10-coredumps.txt p10b-coredump-derivation.txt p11-nvidia-smi.txt \
    p12-dkms.txt p13-syncdb-birth.txt p14-qu.txt p15-holds.txt p16-db-lck.txt p17-snapper.txt \
    p18-df.txt p19-pkg-cache.txt p20-census.txt p21-versions.txt; do [ -e "$B/$f" ] \
    && echo "EXISTS $f" || echo "MISSING $f"; done
→ EXISTS ×26, MISSING ×0, rc=0
```

Spot format check (stamp / `$ command` / output / rc): `p20-census.txt` opens
`2026-11-03T18:37:21Z`, `$ bash tools/tsukuroi-census.sh`, full plane output, `rc=1`; `p6-user-manager-state.txt`
opens `2026-11-03T18:37:20Z`, `$ systemctl --user is-system-running` → `degraded`, `rc=1`. PASS.

**C3 control — sourceless fixture.** Cannot add S279–S281 (census id/Gate checks demand
receipt-backed opened sources) nor counted MK rows (receipt-backed): control score **0 MK rows < 5,
SOURCES stays 278 < 281 → FAILS → discriminative.** Anti-control: every m-receipt named in
mk42-rows-draft.md exists:

```
$ for f in <30 named m-files: m1, m2-newroot-residue, m2e, m2g, m2h, m2i, m2j, m2k, m2l, m2n, m2q,
  m2r, m2s, m3, m4-hooks, m4b, m5, m7c, m7d, m7e-boot-minus2-structure, m8g, m8e, m9, m10a, m10b,
  m10d, m10e, m11, m11b, m12>; do [ -e ... ]; done
→ EXISTS ×30, MISSING ×0, rc=0
```

S-row candidates carry dated fetch receipts + sha256 (m10a/m10b/m10e/m11/m11b). PASS.

## 2. Stored-value fidelity (draft stored cells vs committed SKILL.md bytes)

Re-grepped/re-read every anchor myself (raw reads, CRLF-aware): SKILL.md:44 (snapshot header
"Measured 2026-10-14 (notes: `corpus/knowledge/`)" ✓), :46 (1188 / 207 explicit / **16 foreign** /
3 orphans trio / `-Dk` clean — all verbatim ✓), :47 (both scopes `running`; 0 failed units
(`--failed` and `--all`); only `ai-usage.timer` … `Result=success` ✓), :48 (60 941 err lines but
only 238 entries ✓; "Coredumps this boot 198: godot 142 SIGABRT, node 47 …, typora 2,
`chrome_crashpad` 2, electron 1, bash 1 SIGSEGV" — endpoints verbatim, elision "(25+22), `grok-bot`
3 SIGBUS" marked with "…" ✓), :49 (610.57.04 active; stale `7.1.4-arch1-1` (tree gone; ls
/lib/modules = 7.2.3 only); `pacman -Qo` = `error: No package owns …/updates/dkms/nvidia.ko.zst` ✓),
:50 (sync dbs born 2026-10-11 12:54:13.542; `-Qu` empty **rc=1**; HoldPkg = pacman glibc; "no
`db.lck`." ✓), :100-102 (`pacman -Qm` = 16 foreign (3 explicit: android-apktool-bin,
obsidian-cli-inspector, omarchy-walker; the 13 `elephant-*` are its deps) ✓ across the line wrap),
:125-127 (851G / 1.8G; 8.6 G; 1568+1568 ✓), :152 (`systemctl is-system-running` named probe ✓),
:403 + :957 (snapper 0 configs ✓ both), :729 ("1188 installed, 207 explicit" ✓), :1210-1216 census
block (foreign=16 base=r6(16) at :1211; scope=user state=running failed=0 at :1212; smi=610.57.04 at
:1213; boots=13 at :1214; TSUKUROI_CENSUS rollup verbatim at :1216 ✓), :2366 ("over 6 retained
boots" ✓). **All 25 rows anchor-true; no wrong path:line found.**

Defect class (minor, transcription): three cells splice/trim stored text **without** ellipsis —
DR17's second fragment reorders SKILL.md:49 ("packages … installed 2026-10-11 16:14 (upgrade
610.43.03-3 → 610.57.04-1)" → "upgrade … installed 2026-10-11", silently dropping " 16:14");
DR18's head phrase "module tree pinned to `7.2.3`" is paraphrase (SKILL says the 7.1.4 tree is
gone and 7.2.3 is the only modules dir); DR19 drops "; TSUKUROI-4 re-derived" mid-parenthetical.
Quantities compared are faithful; the fix is cosmetic but required for the landed note to stay
audit-proof (quote verbatim or mark every elision "…" as DR7/DR14 already do).

Cross-checks that bind the two seats: E2 `p21-versions.txt` and E3 `m1-pkg-versions.txt` both
record `mkinitcpio 42.2-1` on the same host — consistent ✓.

## 3. Predicate integrity (rows counted by this seat, rules as frozen)

**C2** (frozen: `^| DR` rows ≥ 6; drift-verdict rows ≥ 5; six-plane live census line among probes;
per-probe receipts committed with-or-before the citing note; SKILL dated append-only erratum):
counted from the draft — **25 DR rows, 20 `drift`, 5 `match`, 0 `drift?`** → ≥6 ✓, ≥5 ✓ (no
narrowing; the margin is 20 vs 5). Six-plane census line present in `p20-census.txt`
(`TSUKUROI_CENSUS: DEGRADED (… oom=DEGRADED)`, six planes, live `err=5275`, `foreign=23`,
`boots=3`, `smi=615.78.08`, `chan=dbs=5` — all matching the rows that cite it) ✓. Row shape carries
plane / stored(verbatim+anchor) / live(value+receipt) / verdict for all 25 ✓. **No quiet narrowing
or widening found.** Notes: (a) the draft adds a third verdict label `drift?` — unused (0 rows), so
scoring is untouched; do not let the landed note use it to park a would-be-drift row. (b) DR7 calls
`drift` on a lower-bound-vs-lower-bound cache size (8.6 G ≥ vs 6.9 G-with-permission-denied) —
honestly caveated in-row and counter-independent (19 drift remain without it); acceptable.
(c) Commit-order (receipts with-or-before citing note) and the SKILL erratum are landing gates, not
draft-checkable — listed in §6.

**C3** (frozen: `^| MK` rows ≥ 5 covering MK1–MK5, every row receipted; SOURCES 278 → ≥ 281 with
S279 docs tier-A / S280 supersedes S021 / S281 supersedes S022; S279 directly after S278; 11
columns NF 13; Gate quotes ≤ 25 words `wc -w`; knowledge-header gate PASS at final tree; README
frontier-bullet discharge notice append-only): counted — **6 MK rows (≥5 ✓), every row citing
receipt paths that exist (30/30)**. Register position verified: the last S-row is S278 at
`corpus/SOURCES.md:287` (`$ sed -n` equivalent via raw read; row begins `| S278 | powercfg …`),
so "S279 directly after S278" holds by construction when appended ✓. S279–S281 source facts are
complete in the draft appendix (URLs, fetched 2026-11-03, released_at 2026-10-01, sha256
`eeac1ed3…93dcf` / `de852646…88b6f`, byte-identity to installed + tags) — but the rows themselves
are **not yet written** in the 11-column registry shape, so NF 13 / gate-quote checks are **open
landing gates**. Gate-quote budget pre-cleared: the two candidate quotes count **14** ("Busybox-based
init now uses /sysroot as the root mountpoint just like the systemd-based one") and **20** words
("To avoid issues (or to at least try to avoid them), /new_root will be kept as a symlink to
/sysroot") by `wc -w` — both ≤ 25 ✓ (the latter is quoted from pre-existing S095, not a new gate
quote). **Kill rule honored:** the installed hooks DO carry the residue and the prediction refutes
at mechanism level (m2s: overlay actually mounted) — the draft records the refutation as the
claim's outcome, exactly the frozen kill-rule branch; the "refuted at mechanism, `unk` at boot"
split is disclosed scoping with the operator discriminator named (snapshot boot; m8g receipts
"You are not in a snapshot." on boots 0/-1), **not a quiet narrowing** — the r1 falsifier
(line 32) required a v42 boot that still does not exist, and the draft says so.

## 4. New ground vs restatement (propositions diff: r1 note lines 9–14 and 32)

r1 propositions (verbatim re-read): pins `mkinitcpio 41.1-1`, `plymouth 26.134.222-2`,
`limine-mkinitcpio-hook 1.38.0-1.1`, `limine-snapper-sync 1.31.0-1.1`, `snapper 0.13.1-3` (line 9);
hook residue `btrfs-overlayfs:4`, `plymouth:11` as of 2026-10-19 (line 12); v42 init 0 vs v41 7
`/new_root` (line 13); `[inf]` silent-no-op **prediction** + Plymouth `[unk]` (line 14); falsifier
line 32 needs a v42-era boot, "operator-only discriminator", none performed.

- **MK1 — new ground.** Post-upgrade measured state (42.2-1 / 1.40.0-2 / 26.134.222-3 / 1.32.1-2 /
  0.13.2-1) + pacman.log upgrade timestamps; unknowable at r1.
- **MK2 — re-measurement + new ground.** The bare residue (lines 4/11) is r1-held ground honestly
  framed as "still", now re-measured with new owners; NEW: full-tree sweep = exactly 3 hits,
  including the `functions:1213` symlink constructor (absent from the 41.1-era tree r1 measured).
  Not restatement.
- **MK3 — new ground, the claim's core.** r1 explicitly could not test (line 32); the symlink
  mechanism did not exist installed at r1. Refutation receipts: m2i (v41 dir vs v42 symlink in
  functions), m2g (findmnt follows symlink rc=0, dangling control rc=1), m2s (namespace chroot,
  installed hook bytes verbatim, stubs disclosed in-receipt, `[OverlayFS setup]` reached, real
  findmnt reads `/sysroot FSTYPE = overlay`, marker writable). Boot level: m8e/m7c/m7d/m7e/m8g —
  0 marker hits in all three retained boots, none a snapshot boot → `unk`, correctly NOT read as
  refutation-confirmation.
- **MK4 — new evidence extending an r1 conclusion.** r1's R5 reasoned S002 non-applicability from
  HOOKS alone; MK4 adds measured `/etc/crypttab.initramfs` absence (m5, rc=2), systemd 262, and
  the v42.2 changeset (m11b: NvPCR/PCR-9 systemd-hook-only) — and preserves r1's "does not
  establish whether TPM hardware exists" caveat. The `omarchy_hooks.conf:1` HOOKS line matches r1's
  description; the `/etc/mkinitcpio.conf:51` systemd line is correctly exposed as a comment.
- **MK5 — new dated re-pin.** "Upstream as of 2026-11-03" changes by construction; byte-identity
  installed == master == tag is new measured state. NEW finding: the systemd-only
  `/usr/lib/limine/overlayfs-setup` variant naming `/sysroot` (m2l/m2k/m10d).
- **MK6 — verdict row.** Provenance to pre-existing register rows verified: S057 at
  `corpus/SOURCES.md:63`, S095 at `:101` (grep-confirmed) — the MR !482 quote is cited as
  pre-existing ground, not claimed as new. ✓

**r24-overlap disclosure (does not defeat the claim but must be cross-linked):** the register
already holds r24-era rows covering part of this ground — S058 (v42.2 init /sysroot), S094
(v42.2 functions symlink, sha256 `8ccfad02…777d` — the same hash m2i re-measures), S096 (plymouth
daemon chroot), S097 (plymouth hook at tag 26.134.222-3, `run_latehook` line 11), S098 (limine
master hook, sha256 `eeac1ed3…` identical to today's fetch, recheck **on-release**, teaches "only a
read-only snapshot boot exercises it"). Those rows were registered BEFORE the host upgraded
(anticipation); r64 measures the fired state (MK1 versions, MK3 boot receipts, MK4 crypttab) — the
plane is new measured ground, not a re-score. The landed note's source/used-by chains must link
S058/S094/S096/S097/S098 so their `used-by` columns gain the new note.

## 5. Axis naming

- **C2 — named-surface-ok.** "The SKILL decision-table snapshot re-measured after the host's
  upgrade cycle" names the surface (the 2026-10-14 snapshot column going stale on a live host),
  not a number; the DR rows serve that surface.
- **C3 — named-surface-ok.** "The mkinitcpio-42 on-release watch, discharged" is a NEW sourced
  plane: a pre-declared frontier bullet that FIRED, discharged with post-upgrade measured state and
  three new sourced rows. Held r1 ground is used as the comparison base (and r24 ground as
  provenance), never re-scored. See §4 for the overlap reasoning.

## 6. Required fixes (ordered; none changes a frozen predicate)

1. **E3 draft header miscite (fix before landing the note):** header says "claim C3,
   `LOG.md:2719-2742`" — the C3 bullet is **LOG.md:2754-2774** (C1 at 2731, C2 at 2742, "Frontier
   step:" at 2776; 2719-2742 covers the SOURCED-disclosure tail + C1 + C2-start). Grep receipts:
   `^- \*\*C[123] ` → 2731/2742/2754; `^Frontier step:` → 2776.
2. **S280/S281 supersession-chain hygiene (note author/L1, at S-row writing):** the register
   already holds an ACTIVE same-URL master pin between S021 and the new S280 — S098
   (SOURCES.md:104, status mined, recheck on-release, identical sha256 `eeac1ed3…`). Land S280
   stating the full chain (supersedes S021; refreshes/absorbs S098's on-release observation, same
   bytes) so one URL does not carry two live authorities. S281: S022 (main pin) → S281 (main
   re-pin) is clean; S097 is tag-scoped (`26.134.222-3` path) and stays distinct — say so in the
   teaches column. Add S058/S094/S096 to the note's source chain per §4.
3. **E2 landed note stored-cell verbatim discipline:** DR17 (splice + dropped " 16:14"), DR18
   (paraphrase head), DR19 (mid-parenthetical trim) — quote verbatim or mark elisions "…" (DR7/DR14
   pattern). Cosmetic; all compared quantities verified faithful.
4. **Landing gates to carry (not draft defects):** SKILL dated append-only erratum pointing at
   `host-drift-recheck-r64.md` (C2 predicate — absent from E2's integrator notes, drop-risk);
   receipts committed with-or-before the citing note (C2, r63 routed defect); README frontier-bullet
   discharge notice append-only (C3); knowledge-header gate PASS at final tree; S-rows in the
   11-column shape (awk NF 13) with Gate quotes ≤ 25 words by `wc -w` (candidates pre-counted 14
   and 20); S279 appended directly after S278 (SOURCES.md:287).

Non-blocking notes: `drift?` label unused (keep or drop; never park a drift row in it); DR7
lower-bound caveat acceptable; the m2* emulation series is one falsifiable-hypothesis labrat probe
campaign (scratch-contained `unshare -rm`, disclosed stubs, m16 documents precleanup) within the
executor allowance.

## Verdicts

- **C2: PASS with minor required fixes** (fix 3, gates in 4). Shape 25/20 against counters ≥6/≥5;
  all 26 receipts exist; stored anchors verified true; no predicate narrowing or widening.
- **C3: PASS with minor required fixes** (fixes 1, 2, gates in 4). Shape 6 MK rows vs ≥5; 30/30
  receipts exist; refutation recorded per the frozen kill rule; no restatement of r1 as new; no
  predicate change; sourced plane confirmed new.
- Both drafts proceed to L1 integration after the listed fixes. Neither claim's rule was altered;
  both do-nothing controls fail their counters as frozen (discriminative).
