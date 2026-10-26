# Round 40 — lesson (tsukuroi, hyaku run 8)

author: tsukuroi L1 (`TsukuroiR40`), 2026-10-26. Base `53b294a274656be6479aadf2ec2fee890ded77ce`. Claims, controls and
outcome: `SCORECARD.md` sections "Round 40 — declaration" and "Round 40 — measured outcome". Wave: one v2 wave `w1`,
65 seats (`.ufo/waves/round-40/w1-spec.json`, `w1-results.json`; reports in `.ufo/waves/round-40/w1/`). Seats are the
lane, not outside reviewers (LEARNING.md); this round's non-author closure is pending.

The round-39 Gate's "Spot-check: Non-author closure pending" (`corpus/lessons/round-39.md:61-64`) is answered by
`corpus/lessons/round-39-verifier-spotcheck.md`: its §3 re-opened the admits S216 and S214 and both sampled rejects
(the staged interpretive sentences `:22`, `:26-27` and the "independent confirmation" sentence `:59-61`) and agreed
with all four (`:121-147`); its §6 routed the seven debts dispositioned below.

## Gate

### New SOURCES rows (all opened 2026-10-26 by this round; each quote located with `grep -n` in the committed
snapshot `.ufo/waves/round-40/frozen/src/` or capture `.ufo/waves/round-40/frozen/hostcap/`)

| Row | Source URL/path and opened date | Located quote (≤25 words) | Location | Decision |
|---|---|---|---|---|
| S219 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/meson_options.txt — opened 2026-10-26 (raw fetched 2026-10-26T06:52:42Z, sha256 `89e5b350…`) | “option('scriptlet-shell', type : 'string', value : '/bin/sh',” | meson_options.txt:17 (description :18) | admit, mined, tier A |
| S220 | https://gitlab.archlinux.org/archlinux/packaging/packages/pacman/-/blob/7.1.0.r9.g54d9411-3/PKGBUILD — opened 2026-10-26 (sha256 `32d40dfd…`) | “-Dscriptlet-shell=/usr/bin/bash \” | PKGBUILD:115 inside `build()` (meson call :110-117; `_git_patch_level_commit=54d9411…` :9; patch sources :52-55) | admit, mined, tier A |
| S221 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/util.c — opened 2026-10-26 (sha256 `381618b6…`, equal to S216's snapshot) | “/* bash sources $BASH_ENV when run non-interactively */” | `_alpm_run_chroot`, util.c:693 (chdir root :628, dup2 :665-667, chroot :679, `chdir("/")` :683, SHLVL :692, umask :695, execv :698, stdin end closed :722-726) | admit, mined, tier A; scope distinct from S216 (output logging) |
| S222 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/trans.c — opened 2026-10-26 (sha256 `637c1165…`) | “/* create a directory in $root/tmp/ for copying/extracting the scriptlet */” | `_alpm_runscriptlet`, trans.c:360 (shell and `-c` :357-358, `mkdtemp` :368, `.INSTALL` :375-377, command line :400-406, run :410, cleanup :412-420) | admit, mined, tier A; scope distinct from S210/S217 |
| S223 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/hook.c — opened 2026-10-26 (sha256 `99f1044b…`) | “/* hooks with multiple triggers could have duplicate matches */” | `_alpm_hook_run_hook`, hook.c:523 (feed :469-490, Depends error :513-514, `running` :653, trigger match :258-306) | admit, mined, tier A; scope distinct from S208 (run order) |
| S224 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/doc/alpm-hooks.5.asciidoc — opened 2026-10-26 (sha256 `2970cb35…`) | “Causes the list of matched trigger targets to be passed to the running hook on 'stdin'.” | `NeedsTargets`, alpm-hooks.5.asciidoc:92-93 (`Target` :61-67, `Depends` :83-85) | admit, mined, tier A; scope distinct from S209 (run order, AbortOnFail) |
| S225 | `.ufo/waves/round-40/frozen/hostcap/` (own-work) — opened 2026-10-26 | “# captured 2026-10-26T06:54:46Z host=plazir27 read-only by TsukuroiR40” | capture-meta.txt:1; MANIFEST.sha256 (sha256 `57888c10…`) over capture-meta.txt, libalpm-shell-strings.txt, hooks-needstargets.tsv | admit, mined, tier A, own-work |

Status/recheck/used-by changes to existing rows: none (S208, S209, S216, S217 are not cited by the new entry; the
new rows carry the new scopes, CORPUS.md rule 2).

### Assimilation — collision check, quarantine slice

Collision check (scratch `.ufo/waves/round-40/assimilation/`, commands of round prompt §10, run after S219–S225 were
written): registry ids 225 (`reg-ids`), staged ids 147 (`staged-ids`), collisions **26** (S200–S225, `collisions`).
Every colliding staged id names a different document than the lane row at that id (round-39 finding, unchanged), so any
future adoption is document-keyed from **S226**. Guard proof: a scratch registry with an indented `  | S219 |` row is
caught by the 0–3-space pattern (1 collision) and missed by the column-zero pattern (0) (`assimilation/guard-proof/`).
Quarantine slice: 12 rows (`assimilation/quarantine-slice`), unchanged from round 39; intersection with the documents
the round-40 entry cites: none adopted — no staged row, id or text enters the corpus this round.

### Assimilation (theme: pacman hook timing, `merge/tsukuroi/`, continued) — residual propositions re-grounded

Candidate `pacman-hook-timing-r25.md` (sha256 `e18c146e733d3cab4bcc82c2ba30b9a571791ec132f7988cd93481b079f09324`),
the propositions round 39 deferred (`corpus/lessons/round-39.md` Gate, "residual mechanism propositions").

| Staged proposition | Decision | Reason; flip condition |
|---|---|---|
| `NeedsTargets` passes the matched trigger targets on stdin (staged `:42-43`) | admit, re-grounded by EX6 (and S224) | hook.c:519-526 and :469-490 add what the staged line omits: the targets are sorted with `strcmp`, de-duplicated across triggers, one per line; a hook lacking the flag reads end-of-file (EX2). Flip: none needed. |
| A file extracted with `.pacnew` triggers on the original name (staged `:44-45`) | admit, re-grounded by EX8 | The trigger matches the package file-list name (hook.c:265-279) and hook.c never consults NoUpgrade. Flip: a libalpm revision whose trigger match reads the extracted name. |
| `.INSTALL` functions execute in the system root (`/`) (staged `:47`) | admit, re-grounded by EX1 | The child changes to `/` after the optional chroot (util.c:679-687). |
| … "so every path inside them must be absolute" (staged `:47-48`) | reject | Not a source statement and not implied: with the working directory at `/`, a relative path resolves from `/` (EX1). It is a style recommendation stated as a requirement. Flip: a pacman or PKGBUILD(5) sentence requiring absolute paths in scriptlets. |
| The shell interpreter is chosen globally by the distribution and cannot be selected per package (staged `:49-51`) | admit-with-correction, re-grounded by EX4 | It is the build-time option `scriptlet-shell` of the pacman build (S219 default `/bin/sh`; Arch sets `/usr/bin/bash`, S220), used as `SCRIPTLET_SHELL` for every scriptlet (trans.c:357, :410); "by the distribution" is correct only as "by whoever builds pacman". Flip: none. |

Assimilation result: four propositions admitted by re-grounding (one with correction), one inference rejected; no staged
row, id or text enters the corpus.

### Wave-1 additions to the registry (2026-10-26)

| Row | Source URL and opened date | Located quote (≤25 words) | Location | Decision |
|---|---|---|---|---|
| S226 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/doc/alpm-hooks.5.asciidoc — opened 2026-10-26 (snapshot sha256 `2970cb35…`; re-opened by seat C2CritEX8) | “When installing or upgrading a file that is extracted with a '.pacnew' extension, the original file name is used in triggering the hook.” | CAVEATS, alpm-hooks.5.asciidoc:126-127 (section :121-129) | admit, mined, tier A; scope (Path-trigger caveats) distinct from S209 and S224 |

Used-by changes logged old→new (CORPUS.md rule 2):
- **S208** used-by `corpus/knowledge/pacman-hook-order-r38.md, corpus/knowledge/pacman-transaction-order-r39.md, corpus/knowledge/boot-writers-r19.md` → the same plus `corpus/knowledge/pacman-exec-environment-r40.md` (EX7 correction cites hook.c:141-144).
- **S209** used-by `corpus/knowledge/pacman-hook-order-r38.md` → `corpus/knowledge/pacman-hook-order-r38.md, corpus/knowledge/pacman-exec-environment-r40.md` (EX7 correction cites alpm-hooks.5.asciidoc:87-89).

### Spot-check

Non-author closure pending. Suggested sample: admit S220 (re-open the Arch PKGBUILD at tag `7.1.0.r9.g54d9411-3`,
line 115) and the reject of the staged inference "so every path inside them must be absolute"
(`pacman-hook-timing-r25.md:47-48`) against util.c:679-687.

## Mistakes

| ID | Class | Evidence pointer | Captured-by | Fix, and how it is shown able to fail |
|---|---|---|---|---|
| R40-HOSTCELL-UNANCHORED | attribution | The EX5 host cell said "on this host `/tmp` is a tmpfs" (`corpus/knowledge/pacman-exec-environment-r40.md`, EX5 row, commit `bf238050`); `/tmp` is xfs on `/dev/nvme1n1p1` and the frozen capture S225 holds no `/tmp` fact (`.ufo/waves/round-40/w1/C2RevEX5.md` §3, receipt `C2RevEX5/host-tmp-fstype.txt`). The L1 wrote it from memory; the same class as R39-HOSTCELL-INFERRED-AS-SEEN one round earlier | QUALITY 2 and 3 — not applied to the host column, and the entry shipped without the `## QUALITY check` QUALITY 14 requires | The sentence is withdrawn append-only and the entry now carries its `## QUALITY check` with an observation/inference split per host cell. Shown able to fail: the seat's read-only `findmnt /tmp` / `stat -f -c %T /tmp` on the host contradicts the original sentence (receipt above); the same command is the check for any future host-cell fstype claim |
| R40-ANSWER-KEY | vacuous | Both new counters are passed by writers that read the counter's own constants instead of doing the claimed work: C2 by a token-list writer (rule cells = the frozen `TOKENS`, values = `derive_values`) and by affirmatively false rules without NEG words (`w1/C2CritControl.md`, `w1/C2CritXFalse.md`, receipts in their seat dirs, PASS 8/8); C1 by a one-line selftest prologue reading the arm with `declare -f`, `${0}` or `${BASH_ARGV0}` (`w1/C1CritControl.md`, C1-CHEAT-A/B/C, PASS survivors 0) and by a census missing one declared fixture (`w1/ConnClaims-5/c1-variant-4fixtures.json`) | QUALITY 87 (closes "reads nothing", not "reads only its own answer key") | QUALITY 88 (new): the predicate checks the declaration's named content parameters, and a control violating exactly one of them must fail. Shown able to fail: the two ConnClaims-5 receipts are such controls and both PASS the round-40 counters, so a counter built under 88 must refuse them |
| R40-CONTROL-OWN-BASELINE | vacuous | The pre-data control C1-K2 (self-reading selftest) failed its own baseline (`controls/controls.jsonl`, `baseline_pass 0`, `selfref 6`), so its FAIL did not show the selfref guard works; the wave then passed that guard three ways (row above) | QUALITY 72/73 (should-fail battery) — silent on a control that fails for a reason other than the one it names | Covered by QUALITY 88's "violates exactly one named parameter": a control's receipt must show every other conjunct green. Shown able to fail: C1-K2's row shows `baseline_pass 0` beside the conjunct it was meant to test |
| R40-HEADING-TIMES (round 39) | number-drift | Two round-39 headings state times later than their commits: SCORECARD `93fddb2c` (+20 min 29 s) and LOG `eeba342e` (+1 h 09 min 16 s) (round-39 closure §6.3; `w1/RoutedTimestamps.md`) | none — no check compares a stated heading time with its commit | Erratum appended to `LOG.md` and a pointer to `SCORECARD.md`; round-40 headings state no clock time. Shown able to fail: `.ufo/waves/round-40/w1/MistakeDateCheck/check_heading_dates.py --rev a6ca8171…` flags exactly the two headings and exits 1 (`MistakeDateCheck/a6ca817-full.txt`) |
| R40-TMP-MISROOT | landing | Seats ran `tools/check-self-assessment.py` without `TMPDIR`; each run extracted a 294 MB lane archive under `/tmp` holding round-40 wave files, and its child census selftest cannot inherit `TMPDIR` at all (`w1/SentScope.md` F1, F2) | round prompt §7.4 (no hardcoded `/tmp`) — the tool honours `TMPDIR` but the wave context did not name this tool | Routed to round 41: the tool takes `--scratch` and passes it to its census child. Not yet shown able to fail; no evidence cites a `/tmp` path (SentScope grep, 0 hits) |

## Round-39 routed defects — round-40 disposition

| # | Routed defect (r39 closure §6) | r40 disposition | Evidence |
|---|---|---|---|
| 1 | R39-CONTENT-UNREAD (C2 counter reads no rule) | partly fixed: the round-40 counter reads value, tokens and polarity, and X-empty / X-false controls FAIL it pre-data; the wave showed a token-list writer and non-negated false rules still pass (R40-ANSWER-KEY) | `controls/controls.jsonl` C2-K1, K2a, K2b; `w1/C2CritControl.md`, `w1/C2CritXFalse.md` |
| 2 | R39-FIXTURE-MONOCULTURE and the live-leg `census_exit` | fixtures varied in the selftest (C1); the one-literal arm is a frozen control (C1-K1, FAIL). The `census_exit 2` decision: it is the six-plane rollup produced by the counter's stripped environment (`systemctl --user` without `XDG_RUNTIME_DIR`), STORAGE is outside the rollup by contract, so ignoring it as a match input is correct; the round-39 counter docstring does not say so, recorded here | `w1/RoutedCensusExit.md` §5; census `:589-600`, `:3142-3147` |
| 3 | Future-dated timestamps | erratum appended (LOG, SCORECARD pointer) | `w1/RoutedTimestamps.md`; R40-HEADING-TIMES |
| 4 | Gates receipt 8th row | disclosure appended to `SCORECARD.md` | `w1/RoutedGatesRow.md` |
| 5 | Receipt-provenance wording | scoping correction appended to `SCORECARD.md`; round-40 claim receipts all carry run-receipt headers | `w1/RoutedProvenance.md` |
| 6 | Residual staged propositions | re-grounded by EX1, EX4, EX6, EX8; one inference rejected (Gate above) | `w1/AsmStagedResidual.md` |
| 7 | Lesson cross-reference | the paragraph at the top of this lesson | `w1/RevLessonXref.md` |

## considerthese — counter lineage (`considerthese/2026-10-25.md`, proposal "Probe lineage table")

Mined as an append-only `SKILL.md` section "Counter lineage — rounds 35-40" (20 rows, digest at the first-carrying
commit, the defect that retired or qualified each), drafted by seat ConsiderLineage and cross-checked by
ConsiderLineageVerify (`w1/ConsiderLineage.md`, `w1/ConsiderLineageVerify.md`). Lesson: across rounds 35-40 every claim
counter was later qualified by the same family — a pass that a non-reading, single-literal or answer-key arm also
reaches — so a counter's reading is evidence only for the key that produced it (QUALITY 88).

## Sources census

Round start (`.ufo/waves/round-40/before/sources-census-start.txt`): `tsukuroi ok`, exit 0, 218 rows. Round end:
`.ufo/waves/round-40/after/sources-census-final.txt`.
