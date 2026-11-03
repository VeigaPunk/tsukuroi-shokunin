# Round 64 — lesson (canonical Linux/omp host, base `44fc183b`, declaration `2f3061ef`)

Draft skeleton written 2026-11-03T19:00Z by seat **S1Scribe** (scribe). **Draft, not landed text** —
the L1 (TsukuroiR64) integrates and finalizes. Every `<<<L1: …>>>` marker is a deliberate
placeholder the L1 fills after integration; nothing here is asserted as final.

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
  update-root-fs --new-root-dir=/new_root" (line 11, the `run_latehook()` body). Supporting located
  text: "run_latehook(){" (1 word, line 10). The late hook still passes `--new-root-dir=/new_root`;
  the code alone does not establish the impact of that path mismatch.

Used by `corpus/knowledge/mkinitcpio42-onrelease-r64.md` — C3's sourced ground.

### Candidates

| Candidate | Source | Decision |
|---|---|---|
| S279 — mkinitcpio v42.2 release notes (GitLab releases API) | `docs`, tier A | candidate for admission; the release body itself, fetched live 2026-11-03 |
| S280 — limine-entry-tool `btrfs-overlayfs` hook, master re-pin | `code`, tier A | candidate for admission; supersedes S021 (re-pin), fetched live 2026-11-03 |
| S281 — Arch plymouth `main` initcpio hook, re-pin | `code`, tier A | candidate for admission; supersedes S022 (re-pin), fetched live 2026-11-03 |
| CRLF criterion — a line-endings criterion for `corpus/QUALITY.md` | own-work (this lesson) | candidate for admission as criterion #97; see the R64-CRLF-HOST-DRIFT row's fix below |

### Admitted

<<<L1: fill after integration>>>

### Rejected

**None — stated explicitly:** no source was opened and rejected this round, and no lead was retired.
The three sources above were each fetched, quoted and carried into the register; the CRLF criterion
is a criterion candidate, not a source. (Sibling seats' own rejection counts, if any, are theirs to
state — this line covers the three S-rows and the criterion candidate listed above.)

### Spot-check result

`pending non-author verification`

### Census and gates

Census: `bash <fleet-root>/scripts/sources-census.sh validate --root <fleet-root> tsukuroi` — the
round-start receipt exits **1** with **E12 = 278** and 0 W04
(`.ufo/waves/round-64/before/census-start-receipt.txt`). The end receipt lands with the final
commit. **Predicate note for the L1:** the C1 after-predicate's stated W04 figure moves **42 → 44**
once S279–S281 are inserted — S280 re-pins the limine master hook URL (already carried by S021 and
S098) and S281 re-pins the plymouth `main` hook URL (already carried by S022), each in a **new
scope**, so each is one `W04` "duplicate url across scopes" warning (not the `E04` "within scope"
error). Verified in a read-only scratch rig (LF-normalized copy of the lane tree, rows inserted at
the S278 id position): `validate` rc **0**, **0 E-codes**, W04 **44**, rows **281**, tier.A 265 /
tier.B 5 / tier.C 11, status.mined 253 / queued 5 / rejected 23. The exit-0 and zero-E-code halves
of the predicate are unaffected; only the stated warning count changes. A second landing-order
constraint: the three rows carry `used-by corpus/knowledge/mkinitcpio42-onrelease-r64.md`, which
does not exist on disk yet, so the census reports **three `E11`** findings until the MK note lands —
the census **END** receipt must be taken after the note exists. (Both points were raised with
SC2Census and folded into `.ufo/waves/round-64/after/gates-recon.md`.)

Row shape at the work revision: S279 at the id position directly after S278, then S280, S281
(`awk -F'|'` NF 13 verified on all three; 0 malformed rows; no duplicate ids). Gates at the work
revision `<<<L1: fill after integration>>>`.

Assimilation: `<<<L1: fill after integration>>>`.

## Mistakes

- **R64-CRLF-HOST-DRIFT** (class: host-transition line-ending drift — Windows-era tooling converted
  LF corpus files to CRLF; the producing host's census tolerated CR, the canonical fleet's did not) —
  the Windows-era record tooling landed CRLF line endings in the lane's corpus and control files:
  `corpus/SOURCES.md` 381/381 lines CRLF, `SKILL.md` 5452/5489, `SCORECARD.md` 4654/4701. The
  canonical census's `## Registry` heading match is CR-intolerant, so **one** CR in that heading
  makes the whole 278-row table read as outside-Registry and the census exits rc 1 with **278 E12**
  and 0 W04. The r63 closure judge saw exit 0 because the Windows fleet's census copy tolerated CR —
  a host-specific pass the canonical fleet never reproduced. **Evidence**:
  `.ufo/waves/round-64/before/census-start-receipt.txt` (rc 1, 278 E12) +
  `.ufo/waves/round-64/before/crlf-inventory-receipt.txt` (SOURCES 381/381, SKILL 5452/5489,
  SCORECARD 4654/4701 lines CRLF) + blob archaeology: the parent of the round-59 work commit,
  `c5a33d08`, is 100% LF for `corpus/SOURCES.md` and `SKILL.md`; the round-59 work commit
  `2913b75d` (2026-11-01, Windows host) is the first CR commit for those two files. **Captured-by:**
  none (no line-endings gate existed; the Windows fleet's census copy passed what the canonical
  fleet failed). **Fix:** C1 normalization (CR-strip; content bytes otherwise unchanged, proven by
  `git show <pre>:F | tr -d '\r' | cmp - F`) + `tools/check-line-endings-r64.py` guard with selftest +
  a new QUALITY.md criterion candidate (cite this lesson; mark `<<<L1: finalize criterion wording>>>`).

  **Scribe's archaeology note (for the L1, flagged — one nuance, not a change):** the "parent is 100%
  LF" statement holds for `corpus/SOURCES.md` and `SKILL.md`, but **not** for `SCORECARD.md`. Measured
  from the lane's own git objects (`git show <c>:F | grep -c $'\r'` over `81776bef` → `c5a33d08` →
  `2913b75d`): at `81776bef` (the r58 carry-in) all three files are 0 CR; at `c5a33d08` (the r59
  **declaration** commit) `SCORECARD.md` is already 4178/4178 CR while `corpus/SOURCES.md` and
  `SKILL.md` are still 0 CR; at `2913b75d` (the r59 **work** commit) all three are CRLF
  (`SOURCES.md` 377/377, `SKILL.md` 4990/5009, `SCORECARD.md` 4178/4178). So the first CR commit for
  `SCORECARD.md` is the round-59 **declaration** commit `c5a33d08`, one commit earlier than the
  round-59 **work** commit `2913b75d` that first carried CR in `corpus/SOURCES.md` and `SKILL.md`.
  The class, the file set, the fix and the counts are unchanged; only the "which commit first carried
  CR in SCORECARD.md" detail is refined. The L1 may state it per-file (recommended, as above) or
  keep the round-level phrasing; the scribe did not change the declared text.

## No-further-mistakes sweep

<<<L1: paste the sweep command here>>>

The sweep re-reads the round's files against the declared predicates before the outcome commit: the
counting battery (row count 281, S279 at the id position directly after S278, NF 13 on every
registry row, 0 duplicate ids, the three Gate quote word counts), the census end receipt (rc 0,
0 E-codes, W04 44), the knowledge-header gate at the work revision, the registry-coverage gate, the
line-endings guard (`--check` rc 0 over the lane tree and `--selftest` PASS), the guard's mutant
kill, and the protected surfaces (PROVINCE, SHONEN, AGENTS, QUALITY — no round-64 writes outside
the named surfaces). The command and its receipt land with the outcome commit.

## Correction (appended round 64, if the closure finds one)

<<<L1: fill after integration>>>
