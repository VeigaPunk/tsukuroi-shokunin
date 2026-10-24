# SimplifierProbe — dead-weight audit, r36 successor probe vs tools/probe-child-env-allowlist-r34.py

Written 2026-10-23T02:55:28Z (`date -u`, pasted at write time). Read-only seat; the shared tree
was not modified. No installs.

## 0. Dependency finding (primary input absent)

`.ufo/waves/round-36/w1/ExecProbeR36/` does not exist; no r36 draft probe is on disk anywhere
under `.ufo/waves/round-36/` (only `swarm-registry.json`, `ScribeC2Draft/`, `SrcJournalctlMan/`,
`SrcSystemdNews/` at 02:41Z). Per the standing wave rule this audit is therefore of **r34 itself**
(`tools/probe-child-env-allowlist-r34.py`, working tree bytes = committed tip bytes, sha256
`5d0d568901c0eeb1c301b3bf825a839d4f41af68bc51e4de40f0706f15d1aa92`, VERSION 6), plus the exact
list of what the successor must add. ExecProbeR36 (or whoever writes the draft) should read
§2–§4 here before writing a line.

## 1. The four declared additions (SCORECARD.md:1637-1645 at the declaration commit, LOG.md:1361)

The r36 counter is "the round-34 probe … plus" exactly four things:

1. **This paragraph** — the declaration's counter paragraph becomes the probe's round-36 docstring
   paragraph, and the `PREDICATE` constant is rewritten to the declaration's frozen sentence
   (`leaking_pairs` label). r34 already enforces the docstring↔constant coupling with
   `assert PREDICATE in ' '.join(__doc__.split())` (`probe-child-env-allowlist-r34.py:213`); the
   successor must keep that assert so the three texts (declaration, docstring, constant, receipts)
   stay one sentence. The summary key `leaking_pairs` already exists in r34's output — no rename.
2. **VERSION 5** — **stale, needs an L1 erratum before freeze** (§5, finding F1). The on-disk/committed
   r34 is VERSION 6 (`5d0d5689…`, LOG.md:1321 "VERSION 6, `5d0d5689…`"); the declaration's
   "(tools/probe-child-env-allowlist-r34.py, VERSION 4)" names a round-34 intermediate
   (`35a87374…`, per round-34 spot-check §2). A successor printed as `probe_version: 5` would be
   numerically *below* its own predecessor and collide with r34's historical V5 (`5231dbaf…`).
   The successor should be **VERSION 7**; the freeze text should say so via an appended correction.
3. **The `livefive` set** — 5 targets: `check-revision-binding.py`, `check-report-receipts.py`,
   `score-census-handoff-r32.py`, `mutants-btrfs-space-r30.py`, `run-receipt.py`. Not mechanical:
   each target needs per-target argv and a viability rule (§4) — three of the five are not runnable
   under r34's default harness assumptions (`--selftest` of check-report-receipts starts no git
   child; `--selftest` of check-revision-binding exceeded 45 min against a 1200 s per-run limit,
   both excluded at r34 per the r34 docstring; `mutants-btrfs-space-r30` starts no git child at
   all, by its own docstring `mutants-btrfs-space-r30.py:8`).
4. **Untraced view + normalisation fixes** — repaying round-34 routed defect 3: (a) an untraced
   observation of child environments, scored against the committed `MutAttrgetterCopy` and
   `MutPathCopy` mutants (both committed at `.ufo/waves/round-34/w2/MutAttrgetterCopy/`,
   `MutPathCopy/` — `variant.patch`/`mutant.patch` + receipts; reuse those patches, do not
   re-derive) each reading above 0, with `claim`/`r33claim`/`regression` at base each 0; and
   (b) normalisation for short hashes, fixture paths and `GIT_CEILING_DIRECTORIES`/`$HOME`-derived
   values.

§4 lists two requirements the four additions imply but do not name; if they are skipped the
declared after-value is arithmetically unreachable.

## 2. Dead weight in r34 — carried rules/channels with no firing surface on livefive ∪ base sets

Method: full read of the 1014-line r34; construct grep over all 30 targets of the four sets that
survive into r36 (livefive 5, claim 9, r33claim 5, regression 11) for every hiding-module import,
ambient-bytes read, inheriting spawn, spawn alias, hiding call, getattr-on-os, and trace-string;
cross-checked against the committed clause-attribution receipts of
`.ufo/waves/round-35/w1/ExecV6Calibration/` (all 48 pairs of r33claim+regression attributed per
clause) and the round-34 claim receipts (27/27 before, 0/27 after). The only true (non-`re.compile`
false-positive) construct hit in the whole 30-target universe is `__import__('re')` at
`mutants-btrfs-space-r30.py:145` — see §4. No lsp server was needed: no code-symbol deletion is
proposed; every module function in r34 is called from `main()`. Non-firing is proven by
receipts + corpus grep, which is the applicable evidence for data-literal rule rows.

| Carried rule/channel | Firing surface today | Keep? and the valid reason it is still carried |
|---|---|---|
| `environb`/`getenvb` in `OS_AMBIENT` (`:448`) | zero — no target touches bytes environ (grep over all 30: no match) | **Keep.** Name-completeness of the ambient-read rule (one token from `os.environ`); dropping forks the frozen rule text that r33→r34 byte-identity vouches for. |
| `HIDING_MODULES` — all 24 names (`posix`, `nt`, `importlib`, `ctypes`, `inspect`, `builtins`, `gc`, `asyncio`, `pty`, `multiprocessing`, `concurrent`, `_posixsubprocess`, `webbrowser`, `platform`, `pydoc`, `cffi`, `distutils`, `runpy`, `code`, `codeop`, `pickle`, `marshal`, `types`, `zipimport`, `:470-476`) | zero — no target imports any of them (grep: no match) | **Keep.** This is amendment 2's only defense against "start a process or run code outside the spawn calls this scan reads" (e.g. `pty.fork()`); the livefive set is *new* surface that may import them tomorrow. Zero scan cost. |
| `SPAWN_ANY` exotic aliases (`fork`, `forkpty`, `posix_spawn`, `create_subprocess_*`, `exec*`/`spawn*` non-`e` forms, `:455-468`) | zero bare references in any target | **Keep.** The bare-reference ("spawn alias") rule is exactly what kills a re-exec mutant (`MutPythonReexecInherit` was killed in r34); removing aliases reopens the hole amendment 2 closed. |
| `execveat` + unparseable-execve tripwires (`parse_trace`, `:247-289`) | never fired in any committed receipt (ExecV6Calibration: `execveat` 0, `unparsed_exec_records` 0 on all 48 pairs) | **Keep.** Runtime-dependent (glibc `posix_spawn` can lower to `execveat`), so "cannot fire" is unprovable; cost ~0; frozen-lineage. Record as a named never-fired limit, not a deletion. |
| `GCONV_PATH`/`PERL5OPT` fixed injections (execution never observed) | fire only by NAME-presence (no marker channel); that fires on every ambient-copy builder — i.e. on all five livefive targets at before | **Keep.** Their purpose is name-presence sensitivity, not execution; both reach children of all five before-state tools. |
| `BASH_ENV`/`ENV` marker execution channel (`bashenv_log_exists/lines`) | genuinely live: `score-census-handoff-r32.py:489` spawns `/usr/bin/bash` with the copied ambient env; `run-receipt.py:94` spawns `['bash', tool]` for `.sh` tools; `check-self-assessment.py` spawns bash (ExecV6Calibration §3a) | **Keep.** The only channel that distinguishes "name carried" from "code actually executed"; it is the before-signal for the census tool's bash child. |
| `KEPT_GIT_SETTINGS` git clause (`:214-215`) | per-target dead on `mutants-btrfs-space-r30` (no git children, docstring `:8`); live at before on the other four (score-census's bare git spawns `:438`, `:843` inherit the probe's hermetic ambient and lack both settings) | **Keep.** Uniform cross-target predicate; this is the clause that catches a content-free `env={}` builder (amendment 2's stated purpose). The per-target non-firing is a fact to record, not a fork to make. |
| `HIDING_STRINGS` `environ`/`getenv` + `TRACE_STRINGS` | zero non-docstring hits in all 30 targets (all "environment" occurrences live in module docstrings, which the scan exempts — checked the five livefive files individually) | **Keep.** Tripwire for indirect string-built lookups; zero cost; source channels are receipt-proven clean on regression/r33claim. |
| `--set r33claim`/`regression`/`claim` sets | all live (required green in the same run by the declaration) | **Keep** — these are the calibration harness, not dead weight. |
| `--only`/`--scratch`/`--base` flags, `is_git()` limited to `/usr/bin/git` + `/usr/lib/git-core/` | mechanics | **Keep.** `is_git()` narrowness is already routed carried debt (round-34 spot-check §6 item 9); the five livefive tools spawn `git` PATH-resolved, which resolves to `/usr/bin/git`, so it does not bite this set. |

**Bottom line: r34 carries no deletable rule for the r36 target universe.** Everything that looks
dead is either (a) alias/tripwire closure whose value is conditional on future targets, (b)
name-completeness, or (c) frozen-lineage comparability (the r34 docstring's "predicate, label,
channels, scan rules and run mechanics are byte-identical" is the round-over-round evidence chain;
every row above is inside that frozen text).

## 3. Not dead weight — the opposite: over-firing r34 mechanisms the successor MUST change

These are the two clauses the calibration receipts prove broken; they are the real content of
declared addition 4(b):

1. **Base-parity clause (r34 amendment 1) is structurally unsalvageable by normalisation.**
   ExecV6Calibration §2b measured it firing **with `--base == --revision`** (8/15 on r33claim,
   byte-identical trees): the compared git-argv digests embed per-run randomness (4–7-hex
   `--disambiguate=` prefixes brute-forced by `_revision.py:384-391`, `mkdtemp` fixture leaves,
   `mkdtemp` scratch dirs outside the probe root). Normalisation cannot fix a comparison against
   per-run noise. The successor needs a structural change — run-against-run stability instead of
   base-against-claim, or per-target stability evidence — and a fresh pre-data amendment, exactly
   as ExecV6Calibration §5.4 routes. Without it, "claim/r33claim/regression each read 0 in the
   same run" (a declared sensitivity conjunct) is unreachable: V6 reads 8/15 and 22/33 there.
2. **Any-name value clause (r34 amendment 2) misfires on derived fences.** Nine regression
   targets fire `EXACT-TMPDIR` on `GIT_CEILING_DIRECTORIES` = dirname of a `TemporaryDirectory`
   under the run TMPDIR (ExecV6Calibration §3a, with the construct lines named per tool). The
   declaration *retains* `GIT_CEILING_DIRECTORIES` (to the run's scratch parent) and private
   `HOME`/`XDG_CONFIG_HOME` in the after-state of `check-report-receipts.py` and `run-receipt.py`
   — both currently derive those values from `os.path.dirname(os.path.abspath(temp_dir))`
   (`check-report-receipts.py:321`) and `tempfile` dirs. So without a derived-value exclusion in
   the token set, **the declared after-state of 2 of the 5 livefive targets reads >0 by
   construction**. The normalisation fix must add these tool-derived values (and the ceiling
   name) to the run's exclusion set, while keeping true ambient copies leaking — the untraced
   view + the two mutants are the sensitivity proof that the exclusion did not go too far.
3. **Normalisation gaps named by the declaration are real and receipted**: short hashes
   (`HEX`/`HEX_STR` match only 40/64, `_revision.py` emits 4–7-hex), fixture leaves under the
   run tree (`check-boot-writers.py:675` mkdtemp suffix), and scratch outside the probe root
   (`mutants-owed-statements-r29-v4shapes.py:32` uses `/fast/scratch/hyaku` directly).

## 4. What the livefive set forces (implied by additions, not spelled out; route to ExecC1Design/MutProbeDraft)

1. **`mutants-btrfs-space-r30` starts no git child, ever** (`:8` "No git is run"; its only spawn is
   `sys.executable` at `:363`). r34's harness rule `control run started no git child` → harness
   error would put it in `harness_errors`, violating "after: `harness_errors` empty, exit 0" on all
   five. The livefive set needs a per-target viability rule (e.g. ≥1 child exec instead of ≥1 git
   exec for this target) — decided as a pre-data amendment, before any seat scores.
2. **`check-report-receipts --selftest` starts no git child and `check-revision-binding --selftest`
   exceeded the 1200 s limit** (both excluded at r34 for exactly these reasons). The set must pick
   per-target argv (a real `--report/--lane/--revision` run for the former; a bounded fixture mode
   for the latter) and the TIMEOUT/viability consequences that follow. [inf] Both tools'
   non-selftest modes spawn PATH-resolved `git`, which also makes an untraced stub-git wrapper
   viable for the whole set (all five spawn `git` or `bash`/`python3` via PATH or absolute paths —
   a stub-dir `git` shim that dumps its environ is the cheapest untraced channel; `sys.executable`
   children bypass PATH and stay strace-only [inf]).
3. **`score-census-handoff-r32.py` has two bare inheriting git spawns** (`:438-440` `git archive`,
   `:842-844` `git rev-parse`, no `env=`). The r34 source scan flags `inheriting-spawn … without
   env` — these fire at before and **keep firing after** unless the C1 change gives them fixed
   dicts. The claim text "builds every child environment from a fixed dict" already covers them;
   this is the concrete hunk list the change must include (plus `:786` `os.environ.items()` minus
   `TSUKUROI_*`, the actual ambient copy).
4. **`mutants-btrfs-space-r30.py:145` uses `__import__('re')`** inside the F10 mutant lambda — the
   only true hiding-construct hit in the 30-target universe, so the source channel leaks on this
   target permanently, before *and* after, until rewritten. Behavior-preserving fix, using the
   file's own `:295`/`:303` idiom: module-level `import re` (the file has none at top level) and
   `re.sub(...)` in the lambda. Like r34's two locator/citations hunks, this is scan-compliance
   rewrite, not allow-list work — the L1 should disclose it as such in the C1 diff.
5. **Reuse the committed mutants**: `.ufo/waves/round-34/w2/MutAttrgetterCopy/` and `MutPathCopy/`
   (tracked files: `variant.patch`, `mutant.patch`, `mutant-claim.jsonl`, `ordinary` receipts).
   The untraced view's sensitivity gate is "each reads above 0" — apply those patches to exported
   trees at the after revision, do not invent new mutants (a new mutant would need its own
   pre-freeze justification).

## 5. Import/refactor vs copy — verdict: **copy is safer; do not extract a shared module this round**

- **Import is not even available**: `probe-child-env-allowlist-r34` is hyphen-named; loading it
  needs `importlib` — which sits on the probe's own `HIDING_MODULES` denylist. A successor that
  loads its predecessor via importlib legitimises exactly the construct the scan exists to reject,
  and sets a precedent that weakens every future source-channel finding ("your own probe imports
  that way").
- **Receipt discipline pins one file**: the frozen counter is named by `probe_sha256` of a single
  file in every receipt and by sha256 in the LOG freeze entry. A lib+CLI split doubles the
  frozen-bytes surface and breaks the r33→r34→r36 byte-identity lineage that is the only
  comparability evidence between counter generations (round-34 spot-check verified lineage by
  exact sha256 per VERSION).
- **The successor changes the frozen text anyway** (PREDICATE + docstring assert, VERSION, set,
  untraced view, normalisation), so the shared surface would be the run mechanics and scan engine
  — precisely the parts whose byte-identity across rounds is cited as evidence. A partial import
  would make "byte-identical rules" unverifiable without a third artifact.
- **Editing r34 to expose internals is out of scope**: r34 is a production tool; this round's
  write scope is the new probe, and the freeze rule forbids touching the r34 bytes the controls
  scored.
- If dedup is ever wanted, the honest path is a *later* round: introduce `tools/_child_env_probe_lib.py`
  together with a new-generation probe and re-base r34's lineage comparison in that round's own
  declaration. Not under a freeze that names r34's bytes.

## 6. Recommendations (keep/drop/refactor) and risk

- **Keep** every r34 rule/channel in the successor (§2 table) — zero deletions found; the carried
  non-firing rows get one sentence each in the successor docstring's named-limits paragraph
  (mirroring how r34 documents its known limits), so the dead surface is *declared* dead instead
  of silently carried.
- **Change** (pre-data amendments, before any seat scores the after value): base-parity clause →
  run-against-run or per-target stability; any-name clause → exclude tool-derived ceiling/HOME
  values; extend HEX normalisation to 4–7-hex and tree-local fixture leaves.
- **Add** per-target livefive argv + viability rules (§4.1–4.2), the untraced stub channel scored
  against the two committed mutant patches, and VERSION 7 with an erratum correcting the
  declaration's "VERSION 4"/"VERSION 5" wording (F1 below).
- **Rewrite** `mutants-btrfs-space-r30.py:145` to a plain import as part of the C1 change, disclosed
  as scan-compliance (§4.4).

Findings for the L1:
- **F1 (freeze-text defect, fix before freeze):** SCORECARD:1637 says the r34 probe is "VERSION 4"
  and the successor "VERSION 5"; committed r34 is VERSION 6 (`5d0d5689…`, LOG.md:1321; round-34
  spot-check §2 gives the per-VERSION hashes). Successor should be VERSION 7; append a correction
  row. Cheap now, a freeze breach later.
- **F2:** three of five livefive targets are non-viable under r34's default harness assumptions
  (§4.1–4.2) — the livefive set addition must carry per-target args and a viability amendment, or
  the declared "`harness_errors` empty" after-value is impossible.
- **F3:** the after-value is unreachable without the two structural counter repairs of §3, on
  receipted evidence (ExecV6Calibration: 8/15 and 22/33 under V6, 8/15 even at base == claim);
  "normalisation fixes" alone (declaration wording) under-covers the base-parity half.
- **F4:** one livefive target leaks in the source channel independent of env (`__import__('re')`,
  §4.4) — the C1 diff must include that rewrite or the claim cannot verify.

Risk of this audit's keep verdict: low — it recommends *no* deletions, only declared-limits
documentation plus the receipted repairs. Risk of skipping §3/§4: the round burns its after-battery
on harness errors and guaranteed-leaking derived fences, i.e. a second `unprovable-but-better`
stop like round 34's.

## Artefacts

- This file: `.ufo/waves/round-36/w1/SimplifierProbe/SimplifierProbe.md` (copy:
  `simplification.md` in the same directory).
- Evidence read, nothing produced by me needs committing: `tools/probe-child-env-allowlist-r34.py`
  (full, sha256 `5d0d5689…1aa92`); `SCORECARD.md` declaration at `6d76fb20…`; `LOG.md:1321,1345,1361`;
  `corpus/lessons/round-34-verifier-spotcheck.md` (§2, §6 items 1–3, 9);
  `.ufo/waves/round-35/w1/ExecV6Calibration.md` (+ receipts dir);
  `.ufo/waves/round-34/w2/Mut{Attrgetter,Path}Copy/` (tracked, via `git ls-files`);
  construct grep over the 30 target files (livefive 5, claim 9, r33claim 5, regression 11).
