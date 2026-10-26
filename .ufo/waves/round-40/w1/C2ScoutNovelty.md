VERDICT: supports (with scope notes) — C2's "new ground" holds for EX1, EX3, EX4, EX5, EX6, EX7's Depends half and EX8; EX2 (stdout+stderr merged) and the AbortOnFail half of EX7 are already held at base; EX8's NoExtract/NoUpgrade facts are held on the extraction side. No sibling lane covers any EX proposition.

Seat C2ScoutNovelty, item C2-17. Read-only; no pacman, no host mutation. Scratch dir `/fast/scratch/hyaku/tsukuroi-r40/C2ScoutNovelty/` created and removed. Tools installed: none.

## 0. Method and its limits

- Base: `git -C tsukuroi-shokunin grep … 53b294a274656be6479aadf2ec2fee890ded77ce -- corpus SKILL.md PROVINCE.md` (the pathspec includes `corpus/README.md`). The base has no `pacman-exec-environment-r40.md`, and its SOURCES.md has 0 rows S219-S225 (`git grep -E '^\| S(219|22[0-5]) '` → 0).
- Siblings: `git -C <lane> grep … HEAD`, all 20 other `*-shokunin` lanes (every file at HEAD, including `.ufo/` wave archives).
- Receipts: `.ufo/waves/round-40/w1/C2ScoutNovelty/` holds `sweep.sh`/`sweep-counts.txt` (first pass) and `sweep2.sh`/`sweep2-counts.txt` (second pass).
- Honesty note on pass 1 (`sweep.sh`): its regexes were case-insensitive and loose. The `alpm_[A-Za-z0-9]{6}|\.INSTALL` pattern matched ordinary words, so its counts (kama 1114, souji 47, tsukuroi 32) are noise. `BASH_ENV` in chousa (1223) is a campaign-dump count. Pass 1 counts are **not** evidence of coverage. Pass 2 (`sweep2.sh`) is case-sensitive with literal tokens, and every non-zero sibling hit was then opened.
- My own slip: one inspection grep used `util\.c`, which matches `shutil.copy`. I discarded those lines (kaidoku, kasegi, mori "libalpm" listings). Only the mado lines below are real libalpm hits.
- Semantic tools (`lsp`) are not applicable: the targets are prose and C snapshots, not a language-server project. This is a text sweep, not proof of semantics. Absence means "no literal hit", and I read the held rows for meaning (§2).

## 1. Literal-token hit counts (pass 2, tight patterns)

Command: `bash .ufo/waves/round-40/w1/C2ScoutNovelty/sweep2.sh` (output saved as `sweep2-counts.txt`). Counts are lines; siblings are summed over all files at HEAD.

| token | tsukuroi @ base | siblings with hits (lane count) |
|---|---|---|
| `alpm_XXXXXX` | 0 | none |
| `tmp/alpm_` | 0 | none |
| `scriptlet-shell` | 0 | none |
| `SCRIPTLET_SHELL` | 0 | none |
| `could not satisfy dependencies` | 0 | none |
| `unable to run hook` | 0 | none |
| `NeedsTargets` | 6 | none |
| `alpm-hooks` | 15 | none |
| `_alpm_run_chroot` | 4 | none |
| `SHLVL=` | 0 | (see `SHLVL` below) |
| `umask\(0022\)\|umask 0?022` | 0 | kaidoku 1, kama 1, kotoba 2, kumitate 3, mado 1, souji 4, tameshi 2 |
| `BASH_ENV` | 16 | chousa 1148, kagi 16, kaidoku 17, kasegi 1, kotoba 2, kumitate 13, mado 5, mori 8, souji 10, tabi 3, tameshi 27 |
| `SHLVL` (pass 1, base) | 0 | chousa 1, kaidoku 4, kama 2, kengaku 3, kumitate 4, mado 24, tameshi 3 |
| `NoExtract` (pass 1) | 40 | kama 2, tameshi 1 (the tameshi hit is outside the lines I opened; kama's two are the `pacman-conf` listing in `TsukuroiOverlap.md:15,37`) |

Zero at base for the four literals that carry the new proposition text: scriptlet shell, `alpm_XXXXXX`, `could not satisfy dependencies` and `SHLVL`. The same holds for `umask 0022` and for `chdir`/cwd of a hook or scriptlet.

What the non-zero tokens are:

- tsukuroi `NeedsTargets` (6): `SKILL.md:3162` (count 14 effective), `pacman-hook-order-r38.md` line 14 (header count), the table column `needs`, `round-38-verifier-spotcheck.md:74`, `round-39-verifier-spotcheck.md:191`, `round-39.md:56`. It is held only as a count and a column, never as stdin semantics.
- tsukuroi `BASH_ENV` (16): the child-env deny-list/allow-list work (`SKILL.md:2812` and four more rows of that tool, `lessons/round-31*.md`, `round-32.md:3,12,29,55`, S175 at `SOURCES.md:181`). S175 holds only "bash sources `$BASH_ENV` when started non-interactively". It does not hold that libalpm unsets it. That is adjacency, a supporting fact, not the proposition.
- sibling `BASH_ENV`/`SHLVL`/`umask 022`: about the sibling's own harness environments (`chousa` campaign dumps; `mado` `SentinelReaEnv.md:47`; `tabi`; `kumitate` `RedoDemoBwrapEnv.md:175-191`; `souji` `round-36/w1/reports/SentGateExec.md:147`). None is about libalpm children.
- sibling `libalpm` real hits (mado only): `round-15/w1/reports/AttackNoHarm.md:14` and `InputSafety.md:82` (the `systemd-hook` udev-reload script and `35-systemd-udev-reload.hook`), `round-16/w1/reports/QualityGround.md:18,24` (pacman `sync.c` `alpm_trans_get_add`, dependencies in the add list), `round-17`/`round-18`/`round-19` hook-file listings. Not about `_alpm_run_chroot`, scriptlet staging, stdin, env or `Depends`.

## 2. Per-proposition prior-coverage table (base `53b294a2`)

Held means the proposition (not just the topic) is stated, with a source line, in the base corpus.

| EX | proposition | held at base? | evidence | verdict |
|---|---|---|---|---|
| EX1 | cwd `/` in chroot child | no | grep of `chdir` and "working directory" over the pathspec has no hook/scriptlet hit. `round-39.md:56` names "scriptlet cwd `/` (`:47-48`)" as a **not-carried deferral** (flip: "a round-40 entry … states each with its line"). `round-39-verifier-spotcheck.md:191` repeats it | new ground, a named round-39 carry-over |
| EX2 | stdout+stderr merged on one socket | **half held** | `pacman-transaction-order-r39.md:78-80` (TO8 scope): "The child's stdout **and** stderr are both joined to the pipe whose lines become `[ALPM-SCRIPTLET]` (util.c:665-666)"; `SKILL.md:3288`, `:3319-3320` say the same | held: stdout+stderr merge. New: stdin is a second socket closed at once without an input callback (no base text) |
| EX3 | SHLVL=1 if unset, BASH_ENV removed, umask 0022, execv keeps the rest | no | zero literals for `SHLVL=`, libalpm `umask`, `unsetenv`. The corpus's BASH_ENV rows are about this lane's own tools | new ground; S175 (`SOURCES.md:181`) supports the *reason* ("bash sources $BASH_ENV when run non-interactively"), not the rule |
| EX4 | scriptlet shell `/usr/bin/bash` (Arch), upstream `/bin/sh` | no | 0 hits for `scriptlet-shell`, `SCRIPTLET_SHELL`, or an interpreter statement. `round-39.md:56` "global interpreter (`:49-51`)" is a deferral. TO4 (`pacman-transaction-order-r39.md:27`) holds only the *argument order* ($1 new, $2 old), not the shell | new ground; adjacent to TO4 |
| EX5 | `<root>/tmp/alpm_XXXXXX/.INSTALL` staged then removed | no | `alpm_XXXXXX`/`tmp/alpm_` 0. `.INSTALL` appears only as a package's vendor install script (`degraded-triage-r4.md:61`) and `%INSTALL%` in `aur-risk-plane.md:202` (a package-metadata fact, not libalpm staging) | new ground |
| EX6 | NeedsTargets: stdin, sorted, de-duplicated, one per line | no | `NeedsTargets` is held only as a count/column (see §1). `round-39.md:56` "`NeedsTargets`→stdin (`:42-43`)" is a deferral | new ground, a named round-39 carry-over |
| EX7a | `running` logged before Depends checked; unmet Depends skips the command | no | `could not satisfy dependencies` 0, `unable to run hook` 0. `round-39.md:53` says only "`Depends =` gates execution independently (`hook.c:509-517`)" (an owner-cell correction), a pointer, not the rule. S208's anchor (`hook.c:532-683`) covers the `running` line, but no row states the order | new ground, with the thin pointer in `round-39.md:53` |
| EX7b | an unmet-Depends failure aborts only a PreTransaction AbortOnFail hook | **held in form** | HO4 (`pacman-hook-order-r38.md:24`): "A PreTransaction hook's non-zero exit stops the transaction only when the hook carries `AbortOnFail`"; S209 (`SOURCES.md` S209 row): "PreTransaction-only scope of AbortOnFail". The Depends-failure path into the same abort (`hook.c:660-668`) is not stated | held ground as applied to non-zero exit: deeper ground; the Depends-failure route is the new part |
| EX8a | Path triggers match file-list names, relative to the root | no | no row; `alpm-hooks` mentions are S209 (`:38-39`, AbortOnFail) and the r39 flip text | new ground |
| EX8b | NoExtract skipped on install; NoUpgrade ignored so `.pacnew` still matches | **adjacent held** | `pacman-backup-files-r35.md:30-32` (`## [obs] NoUpgrade and NoExtract (S191, S195)`): NoExtract skips the member entirely, NoUpgrade turns an existing target into `.pacnew`. That is the extraction path (`add.c`), not trigger matching (`hook.c:258-279`). `round-39.md:56` lists ".pacnew trigger target (`:44-45`)" as a deferral | hook-trigger half is new; the underlying NoExtract/NoUpgrade semantics are held ground (r35), so EX8 is "deeper ground" on that fact |

Only the stdout+stderr merge half of EX2 and the AbortOnFail half of EX7 are restated. Held lines: `pacman-transaction-order-r39.md:78-80` (TO8 scope), `SKILL.md:3319-3320`, `pacman-hook-order-r38.md:24` (HO4). `QUALITY 68` (held ground is "deeper ground", not new) applies to those two clauses and to the NoExtract/`.pacnew` semantics inside EX8. It does not apply to the other proposition clauses.

## 3. Source-row duplication (adjacency within the lane)

The new rows re-mine four files already held under S208/S209/S216/S217/S210. The snapshot digests are identical:

- S221 util.c = S216: sha256 `381618b6…` (base `SOURCES.md:225` and `frozen/src/SHA256SUMS`).
- S222 trans.c = S217/S210: `637c1165…`.
- S223 hook.c = S208: `99f1044b…` (base `SOURCES.md:217`).
- S224 alpm-hooks.5 = S209: `2970cb35…`.

Same bytes, different anchors. S216's anchor is `_alpm_chroot_process_output` 521-528, `_alpm_run_chroot` line 610. S221's is 610-760. S208's anchor is 443-455, 532-683, 116-147. S223's is 258-306, 469-490, 507-530, 653. S209's is DESCRIPTION 34-39 and AbortOnFail 87-89. S224's is 61-67, 83-85, 91-93. `round-39.md:56` itself said these anchors "lie outside S209's declared anchor/scope cell, so stating them needs new rows (next free S219)". So the new rows are not redundant; they widen anchors of held snapshots. The honest label is "deeper ground on held snapshots with new anchors", not new sources. New bytes are S219 (`meson_options.txt`), S220 (`PKGBUILD`) and S225 (own-work capture).

## 4. Sibling adjacency summary

- No sibling lane states any EX proposition (0 hits for `alpm_XXXXXX`, `scriptlet-shell`, `could not satisfy dependencies`, `NeedsTargets`, `_alpm_run_chroot` across the 20 other lanes).
- `mado-shokunin` is the only adjacent lane, on hook *files* and a pacman source reading unrelated to the run environment. Those files are the systemd hook scripts and `35-systemd-udev-reload.hook` (`round-15/w1/reports/AttackNoHarm.md:14`) and a pacman upstream `sync.c` read (`round-16/w1/reports/QualityGround.md:18`). No coverage of EX1-EX8.
- `kama`/`kotoba`/`kumitate`/`souji`/`tameshi`/`kaidoku` hits on `umask 022`, `SHLVL`, `BASH_ENV` concern their own harness hygiene. They are adjacent in vocabulary only.

## 5. Proposed wording (for the C2 reviewer or the entry's boundary section)

1. Under EX2 add: "The merge of stdout and stderr is held at `pacman-transaction-order-r39.md:78-80` (TO8 scope); this row adds the stdin socket." That keeps the held half from reading as new.
2. Under EX7 add: "The AbortOnFail-only abort is held (HO4, `pacman-hook-order-r38.md:24`); this row adds the order of the `running` line against the Depends check and the Depends-failure path."
3. Under EX8 add: "NoExtract skipping and NoUpgrade-to-`.pacnew` in extraction are held (`pacman-backup-files-r35.md:30-32`); this row adds how a `Path` trigger treats them."
4. Optional: note in S221-S224 that the snapshots share bytes with S216/S217/S208/S209, to make the "deeper ground" status visible at the source table.

## 6. Not done

- No live reading of upstream pacman source beyond the pinned snapshots. The frozen files `.ufo/waves/round-40/frozen/src/{util.c,trans.c,hook.c,alpm-hooks.5.asciidoc,meson_options.txt,PKGBUILD}` were only hash-listed; I did not re-verify EX quotes against them (that is C2's counter and the reviewers' job).
- Sibling greps cover HEAD only, not other branches, reflog or untracked files.
- The sibling `NoExtract`, `SHLVL` and `umask` hit lists were opened only partly; every lane with a non-zero count was inspected for libalpm relevance in a sample (about 3 lines per lane for `SHLVL`, all lines for `NoExtract` in kama/tameshi/`umask`). A hit deeper in a large campaign dump could have been missed; none of the 13 sampled lanes' samples was about libalpm children.
