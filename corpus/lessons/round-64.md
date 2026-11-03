author: tsukuroi lane round 64 (L1 TsukuroiR64, seats named inline)

Shape: the lane is **back on the canonical Linux/omp host** (Arch, kernel 7.2.11) after the
r53–r63 Windows era; the Windows-only planes stay frozen this round and no Windows-era probe is
replayed. The standing L0 questions (`tsukuroi | round-53` fleet `.ufo/l0-questions.md:229`,
`| round-57` `:247`, `| round-60` `:253`) remain unanswered and are routed around, never treated as
answered. Claims (LOG.md "Round 64 — declaration", commit `2f3061ef`, written before any
after-measurement): **C1 operability** — the host-transition line-ending gate repair (the canonical
census exits rc 1 with 278 E12 because Windows-era tooling landed CRLF in `corpus/SOURCES.md`,
`SKILL.md`, `SCORECARD.md`); **C2 freshness** — the SKILL plane table's "Measured 2026-10-14"
snapshot re-measured after the host's upgrade cycle, via a drift register note (`DR*` rows) whose
live values are each receipted; **C3 depth (lowest tied axis 8, SOURCED)** — the mkinitcpio-42
on-release watch discharged: the corpus frontier bullet "Pending mkinitcpio 42 upgrade strands two
/new_root hooks … watch upstream btrfs-overlayfs / plymouth hooks on-release" has FIRED
(mkinitcpio 42.2-1 installed), and the v42.2 release notes were fetched live 2026-11-03 **before**
this declaration text was written — the r60/r61 disclosure order, not the r59 post-declaration order.

Round-start conformance receipts (all under `.ufo/waves/round-64/before/`): census start rc 1 with
**E12 = 278** and 0 W04 (`census-start-receipt.txt`); CRLF inventory `SCORECARD.md 4654/4701`,
`SKILL.md 5452/5489`, `corpus/SOURCES.md 381/381` lines CR (`crlf-inventory-receipt.txt`); the
line-endings guard absent at base (`guard-absent-receipt.txt`, `git cat-file -e 44fc183b:tools/check-line-endings-r64.py`
→ rc 128); stored SKILL snapshot values (`skill-snapshot-values.txt`); the C3 note absent
(`c3-note-absent-receipt.txt`).

## Gate

Source records for rows opened this round (CORPUS.md contract v1). The three rows and their Gate
quotes are drafted in `.ufo/waves/round-64/drafts/sources-rows-r64.md` (seat S1Scribe); each was
fetched live on **2026-11-03** and each carries a located quote of ≤ 25 words with its location.

- **S279** — mkinitcpio v42.2 release notes (GitLab releases API),
  https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/releases/v42.2 .
  Opened 2026-11-03 (live fetch, HTTP 200, 3905 bytes; raw JSON sha256
  `9ebec7b1c8a1fdccd246282fd868e36acbcc1805917d564b41a0a946516c0bc2`; release `v42.2`,
  `released_at 2026-10-01T07:10:00.872Z`; changelog commit
  `e5433c2e3cb8f80dc77708b01d841a7f4dc864a0`). Located quote (11 words, counted by `wc -w` before
  landing): "install/systemd includes systemd-tpm2-setup-early.service and systemd-pcrnvdone.service
  because of changes in systemd v262." (the `* install/systemd …` bullet under `Changes in hooks:` in
  the `description` body). Supporting located text: "They are required to initialize NvPCRs and to
  measure a separator into PCR 9." (14 words); "Note that this does not fix the issue of failing units
  with UKIs built by mkinitcpio itself." (17 words); "systemd v262 requires that the UKI must be
  signed with a PCR policy and there is still no solution for that without using ukify." (24 words).
  The page states the release's only hook change is systemd-side; it does **not** mention
  `/new_root`, and it does not establish any host-level consequence for this host's busybox hook
  chain — that is the MK note's measured plane, not this row's.
- **S280** — limine-entry-tool `btrfs-overlayfs` runtime hook, master branch, re-pinned,
  https://gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs .
  Opened 2026-11-03 by S1Scribe (live fetch, HTTP 200, 1519 bytes; raw bytes sha256
  `eeac1ed326f5c6fed2e47bbb596d76c9c4b0020be30c3b3c58f6b3a4fa093dcf`, `cmp` rc 0 against the
  installed `/usr/lib/initcpio/hooks/btrfs-overlayfs`, which `pacman -Qo` attributes to
  `limine-mkinitcpio-hook 1.40.0-2`). Located quote (1 word, counted by `wc -w` before landing):
  `root_mnt="/new_root"` (line 4, the `root_mnt` assignment inside `run_latehook()`). Supporting
  located text: "# Check: Is $root_mnt mounted on Btrfs?" (7 words, line 6); `echo "[OverlayFS
  setup] ${root_mnt} is a read-only Btrfs subvolume. Setting up OverlayFS..."` (12 words, line 21).
  The hook still names `/new_root`; the source alone does not establish the boot-level effect.
- **S281** — Arch plymouth packaging initcpio hook, `main` branch, re-pinned,
  https://gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/main/plymouth.initcpio_hook .
  Opened 2026-11-03 by S1Scribe (live fetch, HTTP 200, 336 bytes; raw bytes sha256
  `de852646e615e06d4125eb2e646d0528d1e349bd9e9877c08c5d32c43d288b6f`, `cmp` rc 0 against the
  installed `/usr/lib/initcpio/hooks/plymouth`, which `pacman -Qo` attributes to
  `plymouth 26.134.222-3`). Located quote (3 words, counted by `wc -w` before landing): "plymouth
  update-root-fs --new-root-dir=/new_root" (line 11, the `run_latehook()` body). Supporting
  located text: "run_latehook(){" (1 word, line 10). The late hook still passes `--new-root-dir=/new_root`;
  the code alone does not establish the impact of that path mismatch.

Used by `corpus/knowledge/mkinitcpio42-onrelease-r64.md` — C3's sourced ground.

### Candidates

| Candidate | Source | Decision |
|---|---|---|
| S279 — mkinitcpio v42.2 release notes (GitLab releases API) | `docs`, tier A | candidate for admission; the release body itself, fetched live 2026-11-03 |
| S280 — limine-entry-tool `btrfs-overlayfs` hook, master re-pin | `code`, tier A | candidate for admission; supersedes S021 (re-pin), fetched live 2026-11-03 |
| S281 — Arch plymouth `main` initcpio hook, re-pin | `code`, tier A | candidate for admission; supersedes S022 (re-pin), fetched live 2026-11-03 |
| CRLF criterion — a line-endings criterion for `corpus/QUALITY.md` | own-work (this lesson) | candidate for admission as a new criterion; see the R64-CRLF-HOST-DRIFT row's fix below |

### Admitted

- **S279, S280, S281 admitted** — all three ADMIT by the wave's pre-integration source reviewer
  (R2Sources, `.ufo/waves/round-64/after/review-sources.md`: live re-opens HTTP 200 ×3, pin
  freshness checked against S021's 2026-01-11 and S022's 2023-03-21 pins, host byte-identity
  `cmp` rc 0 ×2, row shape NF 13 ×3, all nine quotes ≤ 25 words by `printf '%s' | wc -w`, the
  census E04 supersedes-exemption proven live both directions at
  `scripts/sources-census.sh:647-649`). S280/S281 landed with the `opens: ` prefix stripped from
  their `teaches` cells (R2Sources' condition; house style: the cell opens `supersedes S0NN —`,
  matching the 25 existing re-pin rows; `opens:` occurred 0 times in the 278-row register).
- **The CRLF criterion admitted** into `corpus/QUALITY.md` (new criterion citing this lesson).

### Rejected

**None — stated explicitly:** no source was opened and rejected this round, and no lead was
retired. The three sources above were each fetched, quoted and carried into the register; the CRLF
criterion is a criterion, not a source. (The wave's reviewer seats rejected nothing either:
R2Sources' three verdicts are ADMIT/ADMIT/ADMIT; no seat reported a rejected source.)

### Spot-check result

`pending non-author verification` — the round's non-author closure judge re-opens a sample of the
three new rows and re-runs the counting battery.

### Census and gates

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tsukuroi` — the round-start receipt exits **1** with **E12 = 278**
and 0 W04 (`.ufo/waves/round-64/before/census-start-receipt.txt`). Predicate note, disclosed before
landing: the C1 after-predicate's stated W04 figure moves **42 → 44** once S279–S281 are inserted —
S280 re-pins the limine master hook URL (already carried by S021 and S098) and S281 re-pins the
plymouth `main` hook URL (already carried by S022), each in a **new scope**, so each is one `W04`
"duplicate url across scopes" warning (not the `E04` "within scope" error). Verified in a read-only
scratch rig before landing (S1Scribe, LF-normalized copy, rows inserted at the S278 id position):
`validate` rc **0**, **0 E-codes**, W04 **44**, rows **281**. The exit-0 and zero-E-code halves of
the C1 predicate are unaffected; only the stated warning count changes, and the +2 is caused by
C3's rows (the claims stay causally separable). Landing-order constraint: the three rows carry
`used-by corpus/knowledge/mkinitcpio42-onrelease-r64.md`, so the census reports **three `E11`**
findings until the MK note exists — the census **END** receipt is taken after the note lands.

Row shape at the work revision: S279 at the id position directly after S278, then S280, S281
(`awk -F'|'` NF 13 verified on all three; 0 malformed rows; no duplicate ids). Gates at the work
revision: recorded in the round-64 measured-outcome section of `SCORECARD.md` and the receipts
commit.

Assimilation: **none adopted from `merge/tsukuroi/` this round** — the §10 id-collision check
(`.ufo/waves/round-64/assimilation/` + the L1's independent rerun
`.ufo/waves/round-64/assimilation-l1/`) shows the staged package's 147 rows start at S200 while the
live registry already holds S200–S278: **79 collisions**, and for all 79 the staged row and the
live row carry **different sources** (0/79 same — CN1Siblings), so arithmetic renumbering is not a
valid fix; 101 of 147 staged rows carry a URL the live registry does not hold, 46 duplicate a live
URL under a different id. Mass id drift a read-only check cannot fix → **L0 question filed**
(fleet `.ufo/l0-questions.md`, `tsukuroi | round-64`) and nothing adopted. The guard-sanity fixture
(indented-row proof) passed: a 2-space-indented `S200` row in a scratch registry is caught by the
0–3-space pattern (nonempty `collisions`); a 4-space row is not (documented pattern boundary; both
real files hold every row at indent 0). **considerthese (one proposal adopted):** the
**Counter-attack scoreboard** (`considerthese/2026-10-26.md`, "proposals only, not acted on") —
the scoreboard exists in `SKILL.md` ("Counter-attack scoreboard — rounds 40-41" and the round-42
continuation) but its last tallied row is round 50-era; rounds 51–63 fielded mutant batteries the
ledger never counted (CN1Siblings' evidence). This round resumes it: the r64 row (MT1Guard's
5-mutant battery against `check-line-endings-r64.py`, 5/5 killed by out-of-band detectors, 2
selftest-coverage gaps found and closed in-round) is appended to the scoreboard in `SKILL.md`,
citing `considerthese/2026-10-26.md` + 2026-11-03.

## Mistakes

- **R64-CRLF-HOST-DRIFT** (class: host-transition line-ending drift — Windows-era tooling converted
  LF corpus files to CRLF; the producing host's census tolerated CR, the canonical fleet's did not) —
  the Windows-era record tooling landed CRLF line endings in the lane's corpus and control files:
  `corpus/SOURCES.md` 381/381 lines CRLF, `SKILL.md` 5452/5489, `SCORECARD.md` 4654/4701 at the
  round-start inventory. The canonical census's `## Registry` heading match is CR-intolerant, so
  **one** CR in that heading makes the whole 278-row table read as outside-Registry and the census
  exits rc 1 with **278 E12** and 0 W04. The r63 closure judge saw exit 0 because the Windows
  fleet's census copy tolerated CR (MinGW gawk's default text-mode CRLF→LF input translation;
  RV1Origin, `.ufo/waves/round-64/after/revenger-crlf-origin.md`) — a host-specific pass the
  canonical fleet never reproduced. **Evidence**:
  `.ufo/waves/round-64/before/census-start-receipt.txt` (rc 1, 278 E12) +
  `.ufo/waves/round-64/before/crlf-inventory-receipt.txt` + blob archaeology (RV1Origin, per file:
  `SCORECARD.md` whole-file-converted at the r59 **declaration** commit `c5a33d08` (4178/4178 CR);
  `SKILL.md` and `corpus/SOURCES.md` whole-file-converted at the r59 **work** commit `2913b75d`;
  parent `81776bef` is 0 CR for all three; mechanism: a text-mode write handle translating every
  written `\n` to `\r\n`, not core.autocrlf (unset) and not an editor; zero `\r\r\n` across 475
  first-parent commits). **Captured-by:** none (no line-endings gate existed; the Windows fleet's
  census copy passed what the canonical fleet failed; the frozen manual census counters were blind
  to the class — NF is unchanged by CR, rows still count 278, malformed 0 — SC2Census
  `after/gates-recon.md`). **Fix:** C1 normalization (CR-strip; content bytes otherwise unchanged,
  proven by `git show <pre>:F | tr -d '\r' | cmp - F` ×3 + independent 0x0D byte counts, R1C1Rev)
  + `tools/check-line-endings-r64.py` guard (7-case selftest) + the new `corpus/QUALITY.md`
  criterion citing this lesson.
  - **Second instance, same wave (the durability lesson):** the worktree repair regressed three
    times during the wave (18:43:21Z, 18:44:30Z, 18:47:32Z — `corpus/SOURCES.md` re-materialised
    byte-identically to the committed CRLF blob, sha `2349bfda…`). Attribution: R1C1Rev cleared
    itself (its `checkout-index -f` ran against a scratch clone, `.ufo/waves/round-64/after/review-c1.md`
    §7); MT1Guard never touched the repo path (sha before == after); the reverter is unnamed —
    the mechanism class is any checkout/restore-class command against the uncommitted worktree
    while the index still holds the CRLF blobs (`git ls-files --eol`: i/crlf ×2, i/mixed ×1 at
    HEAD). The durable fix is the landing itself: once the normalized blobs are committed, the
    HEAD blob is LF and re-materialisation is harmless. Recorded as the same class, not a new one.
  - **Census default-mode silent zero (RV1Origin divergence 3):** the census's default
    (non-validate) mode reads a CRLF registry as **rows 0, rc 0** — an empty clean lane. Only
    `validate` mode catches the class. The round's standing command is the `validate` form; noted
    here so no later round trusts the default mode's silence.
- **R64-DECLARATION-STALE-PRIOR** (class: declaration framing stale against the target note's own
  errata AND the coverage map's own discharge notice) — the round-64 declaration froze C3's framing
  as "the r1 note's [inf] prediction … is testable NOW on this host" and "the watch … has FIRED",
  implying the prediction was untested and the watch undischarged; in fact the lane had already
  **withdrawn** that prediction in the r1 note's own `## R17-SYMLINK` erratum (2026-10-20,
  `initramfs-v42-sysroot-recovery.md:83-89`) after round-17's typed UKI extraction found
  `new_root -> sysroot` in every 42.2 image, had already **emulated both hooks in a user
  namespace** ("both hooks resolve (namespace emulation; not boot-tested)"), and had already
  **superseded the frontier bullet itself** in `corpus/README.md` ("The Frontier bullet above … is
  superseded for this host: the upgrade ran on 2026-10-20 and 42.x keeps `/new_root` as a symlink
  to `/sysroot`" — `corpus/README.md:147-155`). The declaration was written from the frontier
  bullet without re-reading the target note's errata or the README notice that supersedes it.
  **Evidence:** `corpus/knowledge/initramfs-v42-sysroot-recovery.md:83-89`,
  `corpus/README.md:147-155`, and the pacman.log upgrade line (2026-10-20T09:16,
  `probes/mk42/m12-pacman-log-upgrades.txt`) vs the declaration text (LOG.md "Round 64 —
  declaration", C3 bullet); the landed note (`mkinitcpio42-onrelease-r64.md` MK3/MK6) and the
  README's round-64 notice carry the precedence disclosure. **Captured-by:** none — the
  declaration discipline checks claims against the corpus's *held* ground but had no step "re-read
  the target note's own errata and the README's notices about it before freezing". **Fix:** the
  landed note discloses precedence (the refutation was first recorded 2026-10-20; this round's
  contribution is the post-upgrade measured state, the positive end-to-end demonstration, the
  `hook:14` by-design gate identification, the applicability matrix, and the dated upstream
  re-pins); new QUALITY criterion 97 (below) requires the target-note errata re-read before a
  declaration freezes a "first test" framing; the round's trend verdicts score the move as
  re-measurement (quality-class), not new coverage.
- **R64-SELFTEST-COVERAGE-GAP** (class: gate selftest blind to its own exit contract) —
  MT1Guard's 5-mutant battery killed all five mutants, but **M3 (exit-inversion) and M5
  (guard-set-shrink) survived the tool's own `--selftest`** (PASS 5/5): the five fixture cases call
  `check_paths()` and inspect violations, never a return code, and never exercise the canonical
  `is_guarded()` membership the default set is built from
  (`.ufo/waves/round-64/after/mutation/mutation-report.txt`). **Evidence:** the mutation report's
  structural proof (`check_paths()` refs 5, `is_guarded` refs 0, `report(` refs 0 in
  run_selftest) + the two `selftest_result: SURVIVED` rows. **Captured-by:** the mutation battery
  itself (the seat's out-of-band D2/D3 detectors caught what the selftest could not). **Fix:**
  cases 6 (`exit-code-contract`: `main(["--check", dirty]) == 1`, `main(["--check", clean]) == 0`)
  and 7 (`tools-python-is-guarded`: `is_guarded("tools/x.py")` true, nested `tools/subdir/x.py`
  false, `corpus/.ufo/…` not allowlisted) added to `run_selftest` — selftest now **7 cases, 7
  passed**; able-to-fail proven: the same M3/M5 patches re-applied to the updated tool make the
  selftest FAIL (rc 1, the named case fails) while the pristine control passes
  (`.ufo/waves/round-64/after/c1-selftest-coverage-fix.txt`).
- **R64-JJ-ST-WITHOUT-IGNORE-WC** (class: L1 protocol slip — read-only jj without
  `--ignore-working-copy`) — the L1 ran `jj st` bare in the lane repo mid-round (diagnosing the
  SOURCES.md regression), which snapshots the working copy; the round contract requires read-only
  jj only with `--ignore-working-copy`. **Evidence:** this lesson's authoring record; the `jj op
  log` entry (args `jj op log … / jj st`). **Captured-by:** the round contract itself (the rule
  was known and misapplied under diagnostic pressure). **Fix:** disclosure here; no state damage
  found (the snapshot absorbed the worktree as-is; the helper's own commit flow is unaffected —
  verified by the round's landing commits succeeding). Standing reminder to self: every jj
  invocation outside the helper carries `--ignore-working-copy`.

## No-further-mistakes sweep

Command and output land with the receipts commit (the sweep runs after the work commit, before the
outcome commit): the counting battery re-run (registry rows 281, S279 at the id position directly
after S278, NF 13 on every registry row, 0 duplicate ids, the Gate quote word counts), the census
end receipt (rc 0, 0 E-codes, W04 44), the knowledge-header gate at the work revision, the
registry-coverage gate (100/100/0), the line-endings guard (`--check` rc 0, `--selftest` PASS 7
cases), the guard's mutant kill, the cited-receipts gate `--round 64`, the scorecard-uniqueness
gate, and the protected-surface check (PROVINCE.md, SHONEN.md, AGENTS.md carry no round-64 writes).

## Correction (appended round 64, if the closure finds one)

None at landing time; corrections land as appended blocks per the contract if the non-author
closure finds one.
