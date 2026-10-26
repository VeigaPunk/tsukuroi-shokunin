VERDICT: supports

Item C2-7 — mutation probe of the frozen C2 counter `tools/check-hook-order-r38.py` (sha256 `60e3635b37d5cd92f371800d8e5a22837b540e57c1c50a399bc973d4e21bd1a8`) against the committed entry at revision `1fe28e725be47364fc6033bf81ecabc66ee5fe62`. All five model mutants were **killed by the entry**: every mutant counter returns `result: FAIL, exit 1` on the committed entry, with the mismatch counts below. The counter discriminates the rules the entry claims, on this frozen capture.

## Method

- Pristine `tools/check-hook-order-r38.py` and `tools/_revision.py` copied to scratch `/fast/scratch/hyaku/tsukuroi-r38/C2MutCounter/`; copy fidelity verified:
  `sha256sum <lane>/tools/check-hook-order-r38.py <scratch>/check-hook-order-r38.py <lane>/tools/_revision.py <scratch>/_revision.py`
  → `60e3635b…1a8` for the counter (lane == scratch) and `fc861ec8…6de` for `_revision.py` (lane == scratch). The lane counter sha256 matches the declared `60e3635b…` in SCORECARD "Round 38 — declaration".
- Baseline (pristine counter): `python3 check-hook-order-r38.py --repo /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --revision 1fe28e725be47364fc6033bf81ecabc66ee5fe62` → `result: PASS, exit 0, rows_expected: 69, rows_matched: 69, mismatches: 0, extra_rows: 0, source_ok: 1, source_ids: [S208, S209, S210, S211, S212]` (receipt `baseline-pristine.json`). The baseline passes, so every mutant FAIL below is attributable to the mutation, not the harness.
- Each mutant is a minimal mutation of the expected-row model in the scratch copy (unified diffs kept as receipts); all mutants read the same frozen capture `.ufo/waves/round-38/frozen/hooks-capture/` and the same entry/SOURCES at `1fe28e7` via `git show`. "Killed" = the committed entry FAILs under the mutant model (`result: FAIL`, `exit: 1`).

## Results — all five killed

| Mutant | Mutation (pristine site) | result | exit | rows_matched | mismatches | extra_rows | verdict |
|---|---|---|---|---|---|---|---|
| M1 full-name byte sort incl. suffix | `hook_cmp_key` returns `name.encode()` (pristine `tools/check-hook-order-r38.py:59-60`) | FAIL | 1 | 63 | 6 | 6 | killed |
| M2 no tie rule | `alpm_cmp` returns 0 when one base is a prefix of the other (pristine `:63-70`, tie lines dropped) | FAIL | 1 | 63 | 6 | 6 | killed |
| M3 dirs walked first-to-last (/usr wins) | `for tag, sub in DIRS:` instead of `reversed(DIRS)` (pristine `:109`) | FAIL | 1 | 68 | 1 | 1 | killed |
| M4 position counted across both phases | one global counter `pos['__global__']` (pristine `:124,130-131`) | FAIL | 1 | 1 | 68 | 68 | killed |
| M5 ignore NeedsTargets | `needs = False` on the NeedsTargets key (pristine `:92-93`) | FAIL | 1 | 55 | 14 | 14 | killed |

Receipts: `M1-fullnamesort.json/.diff`, `M2-notierule.json/.diff`, `M3-usrfirst.json/.diff`, `M4-globalpos.json/.diff`, `M5-noneedstargets.json/.diff` under `.ufo/waves/round-38/w1/C2MutCounter/`.

## Why each mutation bites (observed)

- **M1/M2** — the capture contains exactly three tie pairs (prefix-pair enumeration over the 69 unique names): `fontconfig.hook`/`fontconfig-32.hook`, `gio-querymodules.hook`/`gio-querymodules-32.hook`, `gio-remove-module-cache.hook`/`gio-remove-module-cache-32.hook`. libalpm order puts the shorter base first; a full-name byte sort flips all three because `-` (0x2d) sorts before `.` (0x2e), and M2's stable sort keeps capture-walk order, which also puts the `-32` file first (`sorted(iterdir())` in `usr-share-libalpm-hooks`). The entry at `1fe28e7` carries the alpm order — `corpus/knowledge/pacman-hook-order-r38.md:75-76` (PostTransaction 32 `fontconfig.hook`, 33 `fontconfig-32.hook`), `:79-80`, `:81-82` — so each flipped pair yields 2 mismatched rows: 6 mismatches, 6 extra (`M1-fullnamesort.json`, `M2-notierule.json` `missing_rows_first5`/`extra_rows_first5`). The entry's own HO1 row (`pacman-hook-order-r38.md:21`) names this exact discriminator: "a plain byte sort of full file names reverses all three pairs (`-` 0x2d sorts before `.` 0x2e)".
- **M3** — the only name present in both capture dirs is `90-mkinitcpio-install.hook` (`comm -12` of the two sorted dir listings). The two files differ in Exec and Targets (`diff etc-pacman.d-hooks/90-mkinitcpio-install.hook usr-share-libalpm-hooks/90-mkinitcpio-install.hook`: etc `Exec = /usr/share/libalpm/scripts/limine-mkinitcpio-install` vs usr `Exec = /usr/share/libalpm/scripts/mkinitcpio install`). Under usr-first the expected row becomes `(PostTransaction, 26, 90-mkinitcpio-install.hook, usr, no, yes, /usr/share/libalpm/scripts/mkinitcpio)` while the entry carries the etc row (`pacman-hook-order-r38.md:69`: dir `etc`, exec `limine-mkinitcpio-install`) → 1 mismatch, 1 extra (`M3-usrfirst.json`). The entry's HO2 row (`:22`) names this override as its discriminator.
- **M4** — no hook in the capture is masked (`for f in …*.hook; do grep -q '^\[Trigger\]' "$f" || echo masked; done` printed nothing), so all 69 rows carry phase positions; a single global counter shifts every row except the first row in name order (`10-glibc-locale-gen.hook`, phase pos 1 = global pos 1) → 68 mismatches, 68 extra, 1 matched (`M4-globalpos.json`).
- **M5** — 15 capture files carry `NeedsTargets` (`grep -l '^NeedsTargets' usr-share-libalpm-hooks/*.hook etc-pacman.d-hooks/*.hook | wc -l` → 15), collapsing to 14 unique rows because the cross-dir duplicate `90-mkinitcpio-install.hook` is one row; the entry says `needs=yes` for all 14 → 14 mismatches, 14 extra (`M5-noneedstargets.json` shows the no/yes pairs, e.g. `40-fontconfig-config.hook` expected `no` vs entry `yes`).

## Process note (mutant defect, fixed before verdict)

The first M4 edit used `pos['__global__']` without initializing the key: `KeyError: '__global__'` traceback, exit 1 — uncaught because `main` catches only `RevisionError/RuntimeError/OSError` (`tools/check-hook-order-r38.py:194`). That run is **not a verdict**; M4 was repaired by also mutating the init line to `{'__global__': 0}` and rerun. The verdict above is from the repaired mutant (`M4-globalpos.diff` contains both hunks, both inside `expected_rows`).

## Coverage statement

- All five assigned mutants killed; none survived, none inconclusive (baseline passed, so each FAIL is a true kill).
- Scope of this probe: the row-model arm of the counter (sort key, tie rule, dir-walk order, position counter, NeedsTargets). The `source_ok` arm and the capture-tamper arm were not mutated — not in this item's mutant list; those checks have not been run and have not passed here.
- One capture-dependence worth naming: M1/M2 bite only because the frozen capture contains three tie pairs, and M3 only because one name is duplicated across dirs. A capture without tie pairs or cross-dir duplicates would let M1/M2/M3 survive. On this frozen capture they are killed.

## Bounds

- Lane untouched except this report and the receipt dir `.ufo/waves/round-38/w1/C2MutCounter/`: no tracked lane file edited; counter runs are read-only (`git show` + capture reads). No `git add/commit/stash/checkout/reset/push`, no jj mutation, no pacman, no sudo, no host change, no service touched. No tool installs were needed (none performed).
- Scratch `/fast/scratch/hyaku/tsukuroi-r38/C2MutCounter/` removed after receipts were copied out (trap `rm -rf -- "$S"` EXIT).
