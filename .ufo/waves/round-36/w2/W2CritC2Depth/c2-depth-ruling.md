# C2 depth ruling — critic recommendation

## Closure recommendation

**Correction-needed exploratory depth, not expansion and not merely a duplicate.** The closure reviewer should not endorse all of C2's advertised details at change commit `c052bb7d41ced49aa888817069afd804eccfecf1` without the narrow corrections below. After those corrections, there is a defensible case for `unprovable-but-better` **depth**: the note makes a previously recorded NEWS warning operationally discriminable. It does not discover the rejection, add a new owned surface, demonstrate a new tool capability, or justify an ordinal move.

This is an advisory attack, not the canonical judgment, admission, or the required outside non-author review. The declaration at `SCORECARD.md:1623-1635` selects the exploratory route. A named outside reviewer must record the final reasons; this dispatched leaf cannot supply that authority. No saturation conclusion follows.

Axes: **depth** is primary; **calibration** is affected by novelty and completeness overclaims; **operability** by misleading accepted-command/output classifications. **Freshness** benefits from source pinning, but pinning alone is not depth. **Coverage** and **adjacency** have no demonstrated gain here. Expansion is a learning trend, not a seventh axis.

## Evidence identities

All lane paths below resolve beneath `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/`:

- `note`: `corpus/knowledge/journalctl-v262-field-filter-r36.md`, reviewed SHA-256 `0077b6cf7e81ef243997fe5bd8559f5e21569290f271b2f60cb0cd1b57a8a8bf`.
- `matrix`: `.ufo/waves/round-36/w1/ScribeC2Draft/matrix-mini.json`, SHA-256 `acd9b6334aa102287ed1592351c1757df545f1b92d6aed25aea3301399f9dcd8`.
- `filter.c`: `.ufo/waves/round-36/w1/SrcSystemdNews/journalctl-filter.v262.c`, SHA-256 `480f7a03040c0ddc93b1b65c0b49d6f0e8a4a377ee1b94168655132dcfd72f48`.
- `journalctl.c`: `.ufo/waves/round-36/w1/SrcSystemdNews/journalctl.v262.c`, SHA-256 `285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab`.
- `NEWS`: `.ufo/waves/round-36/w1/SrcSystemdNews/NEWS-v262.full`, SHA-256 `a494f0389edd09702a90d1540c7e21c0af5a4d29a4d020855ca3062d885a7657`.

A read-only diff of freeze `1e926801195e304950e3eb9d2525ef8bbc245089` to the change commit shows the 127-line note added, together with S198/S199 and the README appendix. Baseline comparisons below independently used a `git archive` export of declaration commit `6d76fb20f6ecbc940e5c8fff36c74060c885e161`, not an assumed pre-change worktree. Search parameters/results and selected observed cells are retained in `evidence.json` alongside this report.

## 1. Strongest counterexample to novelty: S024 already teaches the rejection

`corpus/SOURCES.md:30`, S024, already teaches the v262 rejection of `journalctl -F` combined with filters. Its status is `queued`, not unopened; lack of a used-by note does not erase its teaching.

More decisively, **`corpus/lessons/round-1.md:111` already records**:

> journalctl now rejects -F/--field together with filters such as unit, boot, time, cursor or grep filters.

That line carries the historical NEWS commit string `a923ab5ed1481512be6fb52aaa5086d0fef6878f`. However, **the same lesson at lines 127-129 says S006/S024 pins that did not reproduce were stripped before first commit**, and the registry explicitly claims no S024 pin. Thus the lesson proves the warning was held; it does **not** establish a presently reproducible immutable source pin. Neither ignoring the lesson nor upgrading its withdrawn pin is safe provenance.

The note's lines 88/96 say no lane entry documented the rejection/behaviour. That is too broad. Its exact-error-string search excludes both the registry and lessons, and lexical absence could not establish semantic novelty anyway.

**Smallest correction:** acknowledge both S024 and the round-1 quote; describe the actual gap as the absent runtime signature, exit status, exact parser boundary, contrasting output behaviours and preventive consumer analysis. Preserve S024's historical row; S199's explicit supersession is appropriate.

**Impacted axes:** depth, calibration; freshness if repinning is mislabeled new knowledge.

## 2. What actually goes beyond the held warning

An immutable baseline search over `corpus/knowledge/` and `SKILL.md` found no matches for the action/predicate names, `filtered field`, `field list`, `limit the journal`, or `sd_journal_query_unique`. A separate baseline journalctl-enumeration search over `corpus/`, `SKILL.md` and `PROVINCE.md` found only S024 and the round-1 quote. This is bounded evidence, not proof against every imaginable paraphrase.

| Proposed new ground | Comparison with prior local material | Finding |
|---|---|---|
| Exact runtime stderr plus exit 1; distinction from extraneous arguments | The prior quote contains neither the runtime sentence nor an exit status. `note:11-17`, `journalctl.c:953-960`, and matrix `core_boot0` supply them. | Substantive new diagnostic detail. Source errno EINVAL is not itself the process exit number. |
| Both `-F` values and `-N` names enter the guard | Prior NEWS quote names `-F`; `journalctl.c:958` explicitly tests both actions. S198 explains their distinct objects. | Genuine refinement, not another quotation of S024. |
| Exact limiting predicate and allowed contrasts | Prior quote gives examples, not an exhaustive predicate or exceptions. `filter.c:26-43` supplies the boundary. | New operational mechanism detail, but the advertised term count is wrong (below). |
| `-n` accepted-but-output-altered behaviour | No earlier matching treatment located. The matrix contains a strong `-F`/`-N` contrast. | New evidence exists, but the delivered decision table under-expresses it (below). |
| Source selectors remain usable | Matrix cells for `--root /`, `-D /var/log/journal`, `--user`, `--system`, `--namespace=x`, and `--boot=all` distinguish source selection from the rejected terms. | Useful new boundary; evidence is the tested argv, not a universal success guarantee for nonexistent/inaccessible sources. |
| Filtered JSON substitution | Earlier `boot-plane.md:269-278` and `coredump-count-unit-r34.md:93-105` already use filtered JSON with `--output-fields`. NEWS:133 gives the explicit-entry remedy. | Newly explained application to field enumeration, not a newly invented query method or executable capability. |

The note's consumer section also honestly says no lane tool currently uses `-F`/`-N` (`note:84`). Its census hazard is prospective, not a repaired shipped defect.

S198 (`SOURCES.md:205`) explicitly does **not** source the rejection sentence; it sources option semantics. S199 (`:206`) repins the same NEWS teaching plus its remedy, not an independent authority. S188 (`:194`) already registers the v262 manual XML with the same `d54bbede…a1edbdd` digest that S198 names. Different scope is useful; another source id is not another upstream authority.

## 3. Counterexample: the predicate has 15 terms, not 16

`filter.c:28-42` contains **15 OR operands**:

`arg_boot_filter`, `arg_invocation`, `arg_dmesg`, `arg_cursor`, `arg_after_cursor`, `arg_cursor_file`, system units, user units, syslog identifiers, excluded identifiers, priorities, facilities, since, until, and pattern.

The note's own rows 25-39 correctly enumerate those 15. But `note:126` and `corpus/README.md:264,269` advertise a **16-term** predicate. The action test in `journalctl.c:958` is an outer conjunct, not a sixteenth term of `field_list_has_scope_options()`.

**Smallest correction:** change the predicate count to 15 in every active companion claim. Do not invent an extra row to preserve the number. This is a fixable precision defect, not evidence that the whole mechanism is duplicated.

**Impacted axes:** depth, calibration.

## 4. Counterexample: the claimed `-n` third state is not actually decision-tabled

The note defines only `REJECT` and `WORK` at line 21. It groups `-n` with ordinary WORK options at line 41, then says it limits how much is printed at line 48. That prose partly acknowledges truncation, but does not distinguish the two enumeration objects. README:265/269 overstates this as a delivered third state.

The saved matrix already supplies the missing distinction; these are **recorded wave-1 observations, not my live reruns**:

| Cell | Recorded result |
|---|---|
| `core_plain`: `-F PRIORITY` | exit 0, 12 stdout bytes, six values |
| `ext_lines1_F`: `-n 1 -F PRIORITY` | exit 0, 2 stdout bytes, one value (`5`) |
| `ext_plain_N`: `-N` | exit 0, 2882 stdout bytes |
| `ext_lines1_N`: `-n 1 -N` | exit 0, 2882 stdout bytes, **identical stdout SHA-256** to plain `-N` |

Thus accepted does not mean a complete value list, and `-n` does not have the same observed effect for `-F` and `-N`.

**Smallest correction:** table `-F FIELD -n 1` as **accepted, value list truncated**; separately table the tested `-N -n 1` as accepted with unchanged field-name output. Keep the host captures distinct from universal expected counts. Existing receipts suffice for this correction.

**Impacted axes:** depth, operability, calibration.

## 5. Counterexample: action replacement is not successful field enumeration

`note:44` calls `--list-boots` WORK. Matrix `live_list_boots` uses:

`journalctl --no-pager -F PRIORITY --list-boots`

It exits 0 but produces **541** stdout bytes, not the plain field list's 12. `journalctl.c:805-814` explains why: `-F` assigns `ACTION_LIST_FIELDS`, then `--list-boots` assigns `ACTION_LIST_BOOTS`. The guard at :958 no longer applies because field listing is no longer the selected action.

The same distinction applies to action flags mixed into the allowed list (`--disk-usage`, `--header`, `--sync`; assignments at :824-825, :877-878, :856-857). The saved `--sync -F PRIORITY` cell places `-F` last, so it does not demonstrate that arbitrary orderings combining those flags are read-only. [inf] Reversing that order selects the sync action under the inspected parser.

The table's exit-0 observation is not fabricated, but it is insufficient evidence that both requested operations work together.

**Smallest correction:** separate **action overwritten / last action selected** from genuine accepted field-enumeration scope selectors. Preserve exact argv order. Describe the scope list as “not rejected by this guard,” not as blanket success or output-preservation guidance.

**Impacted axes:** depth, operability, calibration.

## Why depth, not expansion

Journal/boot triage is already Core (`PROVINCE.md:10-11`), and S024 already held this versioned warning. The new useful work is stronger technical detail inside that surface: recognized failure signature, parser boundary, output-sensitive exceptions, and application to existing consumer conventions. That fits the depth definition, not uncovered coverage-map ground.

The protocol's axes/trend definitions agree: `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:11-22` maps depth to verifiable technical detail and quality, while `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md:31-35` requires uncovered mapped ground for expansion. A new filename or S-row cannot supply that ground.

**Requested closure disposition:** reject the “new rejection discovery/new expansion” rationale; withhold an unqualified endorsement of the landed note's advertised 16-term/third-state/WORK shape; after the factual corrections, consider exploratory depth on the nonredundant operational distinctions above, with reasons from the required named outside reviewer. No ordinal credit is supported.

These are fixable defects, not an unavoidable tradeoff. Treating misleading success/output guidance as harmless merely because other details deepen the note would instead trade operability/calibration for depth; the canonical no-axis-harm rule cannot be bypassed that way.

## Scope and verification limits

Performed: static reads/searches; read-only Git show/diff/archive; scratch export; SHA-256 capture; scoped report writes. No live journalctl command, gate, test suite, build, formatter, production edit, mutating VCS command, delegation, admission, or other runtime was invoked. The live numbers above are independently inspected **saved evidence**, not newly exercised verification. No tool was installed or updated. No required artifact was absent; final outside-reviewer identity/decision is not established by this leaf.
