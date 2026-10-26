VERDICT: draft

# Item F-5 — "Probe lineage table": counter lineage of rounds 35-40

Source proposal: `considerthese/2026-10-25.md` (section "Self-improvement ideas", bullet "Probe lineage table"):
"Track every frozen probe/counter version (VERSION 1 to 7 for the child-env probe), its sha256, the round it was
frozen in, and the defect that retired it." The existing partial implementation is
`corpus/lessons/round-38.md:109-130` (child-env probe VERSION 1-8 plus three amendment digests). This item drafts the
missing half: the **claim counters** of rounds 35-40, each with the digest at the commit that first carried it, what
it measured, and the defect that retired or qualified it.

Deliverable: the exact append-only `SKILL.md` section is below, ready to append at the end of `SKILL.md` (current tip
`f951f28`, 3324 lines). Every digest in it was produced by the command stated in the section, in this lane, at
`f951f288483c1af0cef4afd458488b84cf7a2165`; the full command/observation log is
`.ufo/waves/round-40/w1/ConsiderLineage/sha-commands.txt`.

## Exact Markdown for `SKILL.md` (append at end of file)

````markdown

## Counter lineage — rounds 35-40

Appended 2026-10-26 (round-40 wave 1, seat ConsiderLineage; `considerthese/2026-10-25.md` proposal "Probe lineage
table", item F-5). Append-only: no earlier section, row or prose is changed. It complements
`corpus/lessons/round-38.md:109-130`, which holds the child-env probe's VERSION 1-8 lineage and its amendment digests,
with the claim counters of rounds 35-40 and with the digest-at-freeze-commit method.

Method, one row at a time, from the lane root:
`C=$(git -C <lane> log --diff-filter=A --format=%h -- <tool>)` names the commit that first carried the tool;
`git -C <lane> show $C:<tool> | sha256sum` gives the digest. A digest below is therefore the tool's bytes at the
commit that first carried it. Where the lane later froze different bytes (an amendment or an operative revision), the
row names those revisions and their digests as well, because a digest that is not the frozen one leaves the freeze
unverifiable (the round-37 routed defect).

A `git log --all -- <tool>` read also lists commits with empty descriptions that are **not** ancestors of `master`
(`git merge-base --is-ancestor` exits 1) and carry a blob byte-identical to a master commit's version of the same file
(measured: two such commits beside the round-40 pair, five beside `tools/check-btrfs-space-r30.py`; `689eeab` and
`a447b67` both hold `8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159` for the round-40 C1 counter). The
lineage below is the master ancestry, not the union of all refs; an extra hash there is a snapshot, not a divergence.

Scope: every claim counter frozen in rounds 35-40 — `tools/score-*-r3*.py`, `tools/check-*-r3*.py`,
`tools/probe-*-r3*.py`, the two round-40 counters — plus `tools/check-journalctl-v262-corrections.py`, a round-37
claim counter the globs do not match. The second table carries the eight r3\* files frozen in rounds 30-34, so a reader
who follows the globs finds them here instead of concluding they do not exist.

| # | Counter | Frozen in | First-carrying commit | sha256 at that commit | What it measured | Retired or qualified by |
|---|---|---|---|---|---|---|
| 1 | `tools/score-pacnew-arm-r35.py` | r35 | `6b4561e43e15c1cce038e390ad7d4691b0af4cc8` | `19d25d14f9ee6ad15c036c75f997f2fba7aa756779c9e3b70a0ff136297e0155` | VERSION 1: 24 fresh-seeded fixtures (`TSUKUROI_ETC_DIR` + `TSUKUROI_PACMAN_LOG`) against the census `DRIFT pacnew-plane` line — eight `name=integer` fields plus unchanged fixture bytes, modes and inode change times | Not retired by a verifier: met before any freeze by pre-freeze controls K08FixtureKeyed (keyed on name length) and K15FieldMutants (log reader without a pair check); bytes kept as the failed candidate — `SCORECARD.md:1526-1528`, `SKILL.md:3004` |
| 2 | `tools/score-pacnew-arm-r35b.py` | r35 | `7186722b8eba243439c6724766bdae2ef13c595c` | `7517af92e0c9308c10f04b90d05a699cfa56278a736ef975d97ba08fbd957dc1` | VERSION 2: 20 stub views, 3 namespace views and 1 live view, a correct control arm and 17 should-fail arms (fixture gate, cached live values, name-only pairing, gone by `[ -e ]`, FIFO dropped, word-split paths, date filter) | C1 not verified under the declared kill rule: W2TreeKeyed and W2LogKeyed met it before the change existed — `SCORECARD.md:1553`; unrepaired counter defects (battery misses the ctime check and the live view, arm-audit disagreements, live view compares totals only, receipt reason-string echo) — `SCORECARD.md:1556`; pinned historical, base parity FAILs after `52ffd65` — `SKILL.md:3149`, `SKILL.md:3313`, `corpus/lessons/round-39.md:91` |
| 3 | `tools/probe-child-env-allowlist-r36.py` | r36 | `1e926801195e304950e3eb9d2525ef8bbc245089` | `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a` | VERSION 7: the five live tools' child environments on `livefive` — leaking (target, channel) pairs over names, quiet, source and untraced channels, 15 predicate pairs | Retired by its own gaps: S1 clone-branch crash, S3 livefive vacuity, S4 `os.get_exec_path()` silence, parameter-named-`env` source rule — `corpus/lessons/round-36-verifier-spotcheck.md:55-56`, `:102`; the crash reproduced directly — `corpus/lessons/round-37-verifier-spotcheck.md:37`; the source-channel false positive also failed C1 at `c052bb7` — `SCORECARD.md:1823-1825` |
| 4 | `tools/probe-child-env-allowlist-r37.py` | r37 | `29b22df142efb5479333af9d57ecbd069462ba05` | `9aee085b45d7566d6ce398733c10d3d87ae29bce107c4bd13fcdffcb4854b064` | VERSION 8: the same five tools and 15 pairs with the four round-36 fixes, a direct (receipt-free) livefive mode plus the receipt wrapper | Live, not retired: the sensitivity conjunct is unmet (no committed per-fix V8 mutant receipt) — `corpus/lessons/round-37-verifier-spotcheck.md:39`; the only kill ran under V7 — `:40`; a name-level source set cannot see the ambient-PATH family — `:128`; the V8-mutant-per-fix duty is carried, not paid — `corpus/lessons/round-38.md:103` |
| 5 | `tools/check-journalctl-v262-corrections.py` | r37 | `543a7cee2c5119f42023aa72597ce452d4a060d5` | `29fa51da440cb516019ce0b5a5f8fa0efb3aaa4d3d0eea6b830966402fa636d5` (operative bytes `d621b71` = `6fb5b589e2ac2678013885e7cb0bcb290d83d1547e0e3389d9360f2a858fd0cc`) | Three correction clusters in `corpus/knowledge/journalctl-v262-field-filter-r36.md`: the 15-term predicate list, `-n -F` truncation vs unchanged `-n -N` output, and action replacement; plus its own selftest | Qualified, carried: no freeze sha and no kill rule, and amended twice after the change commit (`718cc8f`, `d621b71`) — `corpus/lessons/round-37-verifier-spotcheck.md:63`, `:126`; the rejection-line-verbatim assertion is owed — `corpus/lessons/round-38.md:101` |
| 6 | `tools/score-storage-arm-r38.py` | r38 | `7cbaeb6317cb9f7323d2619eec02db4e4da29449` | `e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218` | Ten built-in sysfs fixtures F01-F10, the live leg and six `PLANE` lines per run for the census STORAGE arm | Qualified by QUALITY 82: a fixture-gated arm scores v1 PASS 10 of 10 — `corpus/lessons/round-38.md:84`; usable only together with row 7 — `SKILL.md:3113`; fixture F06 encodes the superseded absent-root rule and FAILs 9 of 10 by construction after `49cc53c7` — `SKILL.md:3222-3224`, `SKILL.md:3314` |
| 7 | `tools/score-storage-arm-r38-q82.py` | r38 | `9c9bb6477951b3a52ac49ed83db4395765dfcf1a` | `a183ff580cb92cdd276a5720adb54336e7e247c9bd7c81058065e706d62d99e3` | Three per-run random production-path views inside `unshare -rm` with a random tree bind-mounted over `/sys/fs/btrfs`; predicate `ns_views_matched == VIEWS and ns_available == 1` | Qualified: R38-Q82-LEAK — four adversarial arms that read the view tree through leaked paths score 3 of 3 — `corpus/lessons/round-38.md:89`, `corpus/lessons/round-38-verifier-spotcheck.md:171`; repaired by round 39's stdin-filled tmpfs views — `corpus/lessons/round-39.md:86` |
| 8 | `tools/check-hook-order-r38.py` | r38 | `7cbaeb6317cb9f7323d2619eec02db4e4da29449` | `60e3635b37d5cd92f371800d8e5a22837b540e57c1c50a399bc973d4e21bd1a8` | 69 effective hooks from 70 files against the frozen capture: order rule HO1-HO7 (override, suffix-ignoring sort, phase position), AbortOnFail, NeedsTargets, Exec, on mined source rows | Qualified: a stripped entry citing only S212 still passes — `corpus/lessons/round-38-verifier-spotcheck.md:82`, `:176`; an S-id dropped from `source:` survives — `:177` (R38-C2-COUNTER-GAPS, `corpus/lessons/round-39.md:76`); the HO rows are judged per row, not by the counter — `SCORECARD.md:2172` |
| 9 | `tools/score-storage-hidden-r39.py` | r39 | `6a08925daa30767809eb13bb4b01448ff954d46a` | `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973` | Two hidden-root legs (`BLOCKED … detail=mounts:btrfs-without-sysfs`), three stdin-filled tmpfs production-path views, five fixtures, the live leg and six `PLANE` lines per run | Qualified: R39-FIXTURE-MONOCULTURE — every btrfs fixture the same literal string — `corpus/lessons/round-39.md:71`, `corpus/lessons/round-39-verifier-spotcheck.md:184`; the `views_matched == 3` conjunct reads 3 in every run (R39-VIEW-CONTROL-UNREACHABLE, `corpus/lessons/round-39.md:72`); the live leg ignores `census_exit` — `corpus/lessons/round-39-verifier-spotcheck.md:187`. These falsify sufficiency, not the landed arm — `:67` |
| 10 | `tools/check-transaction-order-r39.py` | r39 | `6a08925daa30767809eb13bb4b01448ff954d46a` | `f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e` | TO1-TO8: each quote at its cited line of the pinned libalpm snapshot on a mined `source:` row, no duplicate row or heading, two host counts, 0 `running` lines inside a commit phase | Retired for any re-claim, though its readings stood: R39-CONTENT-UNREAD — it reads `cells[2]` and `cells[3]` and never the rule cell, so `RULE NOT SUPPLIED` or the opposite still scores 8 of 8 — `corpus/lessons/round-39.md:70`; the closure re-derived the claim instead — `corpus/lessons/round-39-verifier-spotcheck.md:180-183` |
| 11 | `tools/score-selftest-literals-r40.py` | r40 | `a447b67b2502bae1e96fda341ae5ad32243ae524` | `8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159` | Nine frozen mutants M1-M9 applied as exact substring replacements to the census `run_selftest` mount-table arms, three neutral rewrites N1-N3 and a self-reference guard; predicate `baseline_pass == 1 and neutral_pass == 3 and mutants_applied == 9 and survivors == 0 and selfref == 5` | Live in round 40; no verifier spot-check yet. Pre-data qualification: the self-reading selftest control does not isolate the selfref guard (selfref 6, its own baseline fails) — `SCORECARD.md:2312-2314` |
| 12 | `tools/check-exec-environment-r40.py` | r40 | `a447b67b2502bae1e96fda341ae5ad32243ae524` | `d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d` | EX1-EX8 rule cells: source-derived value, frozen proposition tokens, no negation word, a 4-25 word quote at the cited snapshot lines on a new mined upstream row, two host values, zero base hits of the novelty tokens | Live in round 40; no verifier spot-check yet. Pre-data controls X-empty, X-false by negation and X-false by wrong values all FAIL it, 0 of 8 — `SCORECARD.md:2308-2311` |

Predecessors matched by the same globs, frozen in rounds 30-34 (the probe rows' full VERSION story is
`corpus/lessons/round-38.md:109-130`; the digests below are the first-carrying bytes, with the amendments named):

| # | Counter | Frozen in | First-carrying commit | sha256 at that commit | What it measured | Retired or qualified by |
|---|---|---|---|---|---|---|
| 13 | `tools/check-btrfs-space-r30.py` | r30 | `8fb2cef081787ccb52b38e9f74d95d2a480de18f` | `1bf7ee14467accac5281e6ebd881db24c8ab682066e9f50ddbb0fe76a931c079` (v2 `a3f1937` = `4953203d2b03fe5e5153441ba9fdc9193683e4b38f2613322a401616b6e55eba`) | Ten frozen btrfs space questions D01-D10, one row each: registry cells, snapshot path and digest, quote at its line, an integer in the evidence directory | v1 qualified, then replaced by v2 after a wave-1 fixture that cited a made-up S900 row and quoted the counter's own `ROWS` comments scored 10 of 10 — `corpus/lessons/round-30-verifier-spotcheck.md:58`, `:62`; the registry records "version 2 after the wave-1 attacks" — `SKILL.md:2667` |
| 14 | `tools/probe-git-env-residual-r30.py` | r30 | `8fb2cef081787ccb52b38e9f74d95d2a480de18f` | `c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c` | Eleven git-writing tools over three channels (path wrapper, user files, enclosing repo), 33 (tool, channel) pairs | Qualified: parity is exit code plus normalized stdout digest, so a hollow fix scores 0, and `LD_PRELOAD`/`PYTHONPATH` go unmeasured — `corpus/lessons/round-30-verifier-spotcheck.md:182-184` |
| 15 | `tools/check-btrfs-repair-r31.py` | r31 | `f4861f4d5c0d03ad769a74e0bcab61b5c6f0877c` | `4f69a109e9b56b3fcba0df5a3555f7ff833b6b04fff28176060efe82ebde5cb8` (env-fix `df66150` = `a6f330226b31c9dcae52ca297197290e958641b52ff9ef91c00c924846194a33`) | Eight frozen btrfs repair questions Q01-Q08, each one `new_sourced` row against six pinned btrfs-progs v7.1 snapshots | Not retired and C1 did not verify: the K6 scripted non-reader reaches 8 of 8 — `corpus/lessons/round-31-verifier-spotcheck.md:126` |
| 16 | `tools/probe-git-child-env-r31.py` | r31 | `f4861f4d5c0d03ad769a74e0bcab61b5c6f0877c` | `b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0` | Eleven frozen tools over three channels (loader env, child contract, dotgit pointer); parity is exit code, normalized stdout digest and git-exec count | Qualified: the contract is a deny-list, so `BASH_ENV`, `GCONV_PATH` and 36 more names still reach children; 7 probe mutants survive the battery and `dotgit-pointer` gave 2 spurious verdicts in 121 runs — `corpus/lessons/round-31-verifier-spotcheck.md:95-97` |
| 17 | `tools/score-census-handoff-r32.py` | r32 | `fe1ae02cdf60aca141abf70400a850c59f239576` | `b2edc66924157703609f2489a1dca1c96bb00d30778f4d1b46640f5c0d6caee9` (v2 `f28442c` = `d6a8f07a53b586ffc4d710200962b8d99a796e0daf91222b9711516cdef311b3`; v3 `44c8eee` = `f45136c3ac15af820ae2c26fc1e5561101bbebe65df39e40c9549d37430c1b4a`) | 24 seeded fixture scenarios plus two live views: the census `HANDOFF ADJ-04 mori` line (`class= value= kind= state=`) routed per scenario | Qualified: under frozen v3 the post-data K11 shortcut reaches 24 of 24, so C1 is unprovable-but-better — `corpus/lessons/round-32-verifier-spotcheck.md:96`; the file later produced a source-channel false positive and was repaired at `4b2d263` — `SCORECARD.md:1823-1825` |
| 18 | `tools/probe-child-env-allowlist-r32.py` | r32 | `fe1ae02cdf60aca141abf70400a850c59f239576` | `2521711bb4e60a42ddd7a4a026961b3ae4aadbe0cf9036251c96f382630853d5` (v2 `44c8eee` = `d43f95ed8a740b71aac1ab412e769e011127eb4ae29646d12b2075a696cf0576`) | Eleven frozen tools; four fixed names plus eight per-run random names (four of length 2-20, four of 21-200); parity by exit code, normalized stdout digest and git-exec count | v1 replaced by a pre-data amendment (a filter keyed on the 2-20 length range would keep longer unknown names) — `tools/probe-child-env-allowlist-r32.py:25-26`; v2's exclusion list was never injected, so 4 mutants survive — `corpus/lessons/round-32-verifier-spotcheck.md:139` |
| 19 | `tools/probe-child-env-allowlist-r33.py` | r33 | `c2e69f3e863ff3332e99eae5c419c286435ff123` | `f34c3b8831369baee6a2f9151f1ecf8839528302e50615970ad655d45da152d2` (v2 `965bc5d` = `38a405837f7aa0dc9bb4e04c0851e44f5f0d6ba8429e0683ba21f1f3f38d8864`; operative freeze `9c89ff4` = `c24f344b864a13ea4db2909bfa81de77f8f41bae35cd5e0949a88b28ab1e04cd`) | The r32 probe with a source channel hardened against indirect access; 5 targets, channels names, quiet and source, 15 pairs | Not retired by a defect: C1 verified under the operative bytes `c24f344b` — `corpus/lessons/round-33-verifier-spotcheck.md:130` — then superseded by a wider nine-target set; carried gap: `is_git` recognises only `/usr/bin/git` and `/usr/lib/git-core/` — `:182` |
| 20 | `tools/probe-child-env-allowlist-r34.py` | r34 | `6de666c427ba9aa6b4350561980bde8d0e7c261d` | `35a87374eb89239af841a015965518d63e40de7ac556041f1b0f366a993fa5a8` (V5 `15c9ac0` = `5231dbafc472ff42e041cbaad3f48dd8bd204d58b6ab22e497cf9372b23d6bfd`; V6 `3457f28` = `5d0d568901c0eeb1c301b3bf825a839d4f41af68bc51e4de40f0706f15d1aa92`) | The r33 probe widened to nine targets and 27 pairs, with a claim-base parity clause | Replaced pre-data twice (amendments 1 and 2) and the round broke its own freeze promise — `corpus/lessons/round-34-verifier-spotcheck.md:55-56`, `:69`; read-side gap owed: an untraced view and the two committed mutants (R34-COUNTER-READ-SIDE-GAPS) — `:184` |

Two defect classes recur, one per family. For the child-env probes the class is a **clean zero that is
indistinguishable from an unobserved zero** (`corpus/lessons/round-38.md:130`). For the claim counters of rounds 35-40
it is a **pass that a non-reading, single-literal or fixture-gated arm also reaches**: a rule cell never read
(R39-CONTENT-UNREAD), one mount-table literal in every fixture (R39-FIXTURE-MONOCULTURE), a citation set one row wide
(R38-C2-COUNTER-GAPS), a fixture-gated pass (R38-QUALITY-UNREAD) and a leaked view path (R38-Q82-LEAK). Both classes
end the same way: the number is evidence only for the observation key that produced it. Read a row with its key, and
before re-claiming on a counter, check that the "qualified by" condition behind it is either repaired in that counter
or declared as a named limit.
````

## Evidence the draft rests on (method, observed)

Method and command, executed at `f951f288483c1af0cef4afd458488b84cf7a2165` (lane HEAD at dispatch):

```
C=$(git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log --diff-filter=A --format=%h -- <tool>)
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show $C:<tool> | sha256sum
```

Observed for all 20 tools, plus the twelve amendment commits, in
`.ufo/waves/round-40/w1/ConsiderLineage/sha-commands.txt`. Two integrity results worth naming:

- All 20 tools' working-tree bytes equal `HEAD` bytes (20/20), so no counter listed in the draft has drifted since
  `a447b67`; the draft's digests are the live instrument bytes, not a stale copy.
- The first-carrying commit is not the operative freeze for two rows (r33: added `c2e69f3`, operative
  `9c89ff4` = `c24f344b…`; r34: added `6de666c` V4, operative V6 at `3457f28` = `5d0d5689…`). The draft prints both
  digests rather than the add-commit digest alone; the add-commit method named in the item would have reported a
  digest that never scored anything in those two rounds.
- `tools/check-journalctl-v262-corrections.py` (row 5) first landed at `543a7ce` = `29fa51da…`, then changed at
  `718cc8f` and `d621b71` = `6fb5b589…`, with no lane record stating the latter digest. That is the round-37 routed
  defect (`corpus/lessons/round-37-verifier-spotcheck.md:63`: "no freeze sha names its bytes") made concrete.
- The item's globs miss row 5 (`check-journalctl-v262-corrections.py` has no round suffix); it is a frozen round-37
  claim counter and is included.
- `git log --all -- <tool>` shows empty-description commits that are not ancestors of `master` and carry a blob
  byte-identical to a master commit's version of the same file: two beside the round-40 pair (`689eeab`, `a8f8df2`,
  `c0cb750`), two beside the round-39 pair (`374003d`, `5569c9c`, `b5593f8`), five beside
  `tools/check-btrfs-space-r30.py` (one per touching commit or two). `git merge-base --is-ancestor <h> master` exits 1
  for each, and `689eeab:tools/score-selftest-literals-r40.py` hashes `8b06de18…`, the same as `a447b67:…`, so they are
  jj/keep snapshots, not lineage. The peer seat ConsiderLineageVerify independently re-derived the master lineage (one
  commit per counter: `7cbaeb6` for the r38 pair, `6a08925` for the r39 pair, `a447b67` for the r40 pair) and reported
  `supports` (`.ufo/waves/round-40/w1/ConsiderLineageVerify.md`); I verified the non-master finding myself and added
  the footnote to the drafted section.

## Findings

1. **Appending this section moves two self-assessment checks, and the gate will go red unless the same commit updates
   the depth cell.** `tools/check-self-assessment.py:592-609` (K08) compares the depth row's stated `SKILL.md` line
   count with `skill_blob.count("\n")`, and (K09) compares its stated table-line count with the number of
   pipe-prefixed lines. Measured by appending the drafted block to a copy of the tip: 3324 → **3387** newlines
   (+63) and 887 → **911** pipe-prefixed lines (+24), so the last axes table's depth cell must restate both values in
   the appending commit or `check-self-assessment` reports 2 mismatches. This is a counted surface, not prose; the
   same trap already produced five K07-K11 reds at round 37's base (`SCORECARD.md:1958-1963`).
2. **The r35 family shows the failure mode first, then the repair:** `score-pacnew-arm-r35.py` (V1) was met by two
   controls that skip the work before any freeze (`SCORECARD.md:1526-1528`), and its successor V2 was again met by two
   controls before the change existed (`SCORECARD.md:1553`). Round 35 is the only round in the set where a claim
   counter was retired before being frozen, and its replacement then failed the round's own kill rule; no VERSION 3
   was made (`SCORECARD.md:1556`), so the pacnew arm was never certified.
3. **Rounds 39 and 40 are instrument-repair rounds whose defect was named by the previous closure**, with one
   exception: round-40 C1 repairs R39-FIXTURE-MONOCULTURE and round-39 C2 repairs R38-C2-COUNTER-GAPS
   (`corpus/lessons/round-39.md:76-88`), but round-39 C1 (row 9) is itself qualified by a defect its own lesson
   recorded (`corpus/lessons/round-39.md:71-72`), and round 40 did not take that row into its C1 — the round-40 C1
   changes only `run_selftest`, not `probe_storage_arm` (`SCORECARD.md:2303`). The round-39 counter's own fixture
   monoculture therefore stays open after round 40: the selftest fixtures vary, the counter's F01-F05 views do not
   (`tools/score-storage-hidden-r39.py:64`, one `M_BTRFS` literal).
4. **Two counters are live and unverified at this dispatch** (rows 11 and 12). Their rows are written as "live in
   round 40; no verifier spot-check yet" and their only negative evidence is the pre-data control line
   (`SCORECARD.md:2306-2314`). They must be re-read after the round-40 closure and amended append-only, not rewritten.
5. **Rows 2, 6 and 9 are pinned historical instruments with named windows** (`SKILL.md:3149`, `:3222-3224`, `:3313`,
   `:3314`). The lineage table now states the window in the same cell as the digest, so a reader cannot take a
   post-window reading as a regression. The two historical windows are inclusive at the named commit
   (`SKILL.md:3303-3305`).
6. **No lineage row is a "pass" without a key.** Every row in the draft carries either a verifier finding or a
   counter-internal gap; there is no round in 35-40 whose claim counter was retired only by a newer round's taste.

## Measured impact of the drafted section

The drafted block appended verbatim to `SKILL.md` at `f951f28` (simulated on a copy, no lane write): total newlines
3324 → 3387 (+63), pipe-prefixed lines 887 → 911 (+24). Both are read by `check-self-assessment` K08 and K09
(`tools/check-self-assessment.py:592-609`) against the last axes table's depth cell, so the appending commit must
restate the two counts there (finding 1).

## What I did not do

- I did not run any counter, probe, census or selftest. Every digest is a pure function of committed bytes; every
  defect line is a citation to a committed verifier file or SCORECARD section. No claim in the draft rests on a fresh
  measurement of a host surface.
- I did not append the section to `SKILL.md` (the lane is read-only for this seat), and I did not test how the two
  tables render; the pipe count in finding 1 is the check I ran instead.
- I did not re-score the round-40 controls or the round-40 claims; the two r40 rows are labelled live, not verified.
- I did not create a scratch directory, clone, fixture or mutant; nothing was built, installed or removed.
