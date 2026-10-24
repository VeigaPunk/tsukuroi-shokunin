# C2 shape attack — CriticC2Shape

Review target: C2 at declaration `6d76fb20f6ecbc940e5c8fff36c74060c885e161`, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:1623-1635,1658-1663`.

Axes: **depth** is the claim; **freshness** and **calibration** are the principal confounds; **operability** is the consumer-guidance harm risk. **Coverage** is not established by another note/source row; **adjacency** is outside this attack. Expansion, quality and discernment are learning trends, not additional axes.

This is an attack report, not admission, a claim verdict, an ordinal change, or the required non-author closure review. No production file, VCS state, routing or judge was changed or invoked.

## 1. Prior-state counting result and its strongest counterexample

Requested counting command, quoted verbatim:

```sh
grep -rl 'cannot be combined with options that limit the journal' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/ /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md
```

**The bounded absence holds at the specified commit:** I exported those committed paths with `git archive`, then searched the immutable export with the required specialized grep tool, case-sensitive and with ignore filtering disabled. Actual tool output:

```text
No matches found
```

The shell GNU grep command itself was not invoked: tool policy mandates the specialized search tool. Consequently there is no claimed GNU grep stdout/exit-code receipt. Exact preparation, search parameters, output and the one failed preparation attempt are persisted in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/CriticC2Shape/prior-state-count.txt`. The scratch directory is not the durable evidence pointer.

**Counterexample to treating that absence as novelty:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md:30`, both current and at the specified commit, already says:

> NEWS documents versioned behavior changes including v258 boot breakpoints and the v262 rejection of journalctl -F combined with filters

Its S024 anchor explicitly says:

> main branch fetched 2026-10-19 (mutable: main now opens with CHANGES WITH 263 in spe; no commit pin claimed)

Status is `queued`, with `used-by` `—`. That means an opened, unmined source, not an unopened lead and not an admitted operational note. The exact-signature search excludes this file entirely. A second, broader case-sensitive semantic sweep over the baseline knowledge directory, SKILL and SOURCES found S024's line as its only matching line; its pattern and scope are in the same evidence file.

**Impacted axes:** depth, calibration; freshness if a new pin is mislabeled new knowledge.

**Smallest safe correction:** preserve the declaration's explicit S024 qualification. Describe the before-state as lacking an *operational decision table*, not as never knowing the rejection. Do not use zero exact-string matches as proof that the mechanism is new. A newly quoted error line would satisfy that lexical distinction even if the note taught nothing else.

## 2. A real boundary the note must teach, not merely repeat

The measured binary identifies itself as `systemd 262 (262-1-arch)` (`journalctl --version`). Read-only counterexamples below are separately preserved in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/CriticC2Shape/observations.json`.

| Executed command, with `LC_ALL=C` | Observed result |
|---|---|
| `journalctl --no-pager -b -F SYSLOG_IDENTIFIER` | exit 1; exact declared rejection line |
| `journalctl --no-pager -b -N` | exit 1; same rejection line |
| `journalctl --no-pager -F TSUKUROI_R36_NONEXISTENT_FIELD -p err` | exit 1; same rejection line |
| same enumeration with `-k`, or with `--since=now` | each exit 1; same rejection line |
| same enumeration with `--boot=all` | exit 0; no output |
| same enumeration with `-n 0`, or with `-n 1` | each exit 0; no output |
| `journalctl --no-pager -F _BOOT_ID -n 0 \| wc -l` | 0; pipefail-protected pipeline exits 0 |
| `journalctl --no-pager -F _BOOT_ID -n 1 \| wc -l` | 1; pipefail-protected pipeline exits 0 |
| `journalctl --no-pager -N -n 0 \| wc -l` | **167**; pipefail-protected pipeline exits 0 |
| `journalctl --no-pager -F TSUKUROI_R36_NONEXISTENT_FIELD SYSLOG_IDENTIFIER=tsukuroi-r36-critic-no-match` | exit 1; **different** message: `Extraneous arguments starting with 'SYSLOG_IDENTIFIER=tsukuroi-r36-critic-no-match'` |

Exact shared rejection:

```text
-F/--field= and -N/--fields cannot be combined with options that limit the journal.
```

Thus an unqualified rule “all limiting options are rejected” is false. In particular, `-n` is accepted; `-N -n 0` still enumerates field names, while the corresponding tested `-F` counts differ with the bound. `--boot=all` also cannot be collapsed into the same matrix cell as `-b`. The absent-field runs prove parser acceptance only; the counted real-field/field-name runs supply the stronger contrast. The 167 count is a host capture, not a durable expected value. No journal bodies or boot-ID values are published.

The pinned [v262 NEWS](https://raw.githubusercontent.com/systemd/systemd/v262/NEWS), `CHANGES WITH 262`, journalctl bullet, supplies the causal explanation, not merely the symptom:

> Previously field listing used sd_journal_query_unique(), which cannot represent those filters, so the filters were silently ignored.

The same bullet advises querying entries explicitly. The [v262 journalctl manual](https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml), `Commands` → `-N/--fields` and `-F/--field=`, distinguishes field **names** from field **values**. A proposed substitute must preserve that distinction.

**Impacted axes:** depth, operability, calibration.

**Smallest safe correction:** make the matrix a bounded set of actual tested argv, commands, signatures and exit codes; include allowed contrast rows and distinguish `-F` from `-N`. Do not infer an exhaustive parser rule from the diagnostic's wording. The above is an attack set, not the full matrix owed by C2.

## 3. Consumer guidance is where depth can become real—or cause harm

Observed local consumers already query entries, not field enumeration:

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh:1081-1096` uses filtered JSON for OOM/SIGKILL entry counts. These branches deliberately accept exit 1 as no matching entries for their existing `--grep` argv.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh:1400-1415` uses `-b -p err -o json`, treats a nonzero result as blocked, and separately tests whether the boot journal exists.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/coredump-count-unit-r34.md:93-105` already supplies boot/priority/MESSAGE_ID-filtered JSON with `--output-fields`.
- A case-sensitive specialized search of `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/` for `--field=`, `--fields`, and journalctl/JOURNALCTL `-F`/`-N` forms returned no matches. This is a bounded textual sweep, not a claim about dynamically constructed argv.

[inf] A future consumer that copies the OOM arm's “exit 1 means zero” rule into a rejected enumeration query could report query failure as no incidents. Conversely, removing boot/time/priority filters to make enumeration succeed would change the evidence population. Neither is demonstrated as a current census bug; C2 changes no tool and should not claim to repair one.

**Smallest safe correction:** identify the actual consumer and desired object: entry count, selected field values, or selected field names. Preserve the original selection when recommending explicit-entry JSON queries; `--output-fields` is projection, not `-F` enumeration. Explain query-error versus no-match handling. Do not call an arbitrary JSON pipeline universally equivalent: S188 already documents nulls, byte arrays and size limits, so field-value extraction needs appropriately scoped handling.

**Trade, not an acceptable fix:** gaining a shorter/working command by dropping the selection or converting query failure to a healthy zero would harm operability/calibration. The canonical judge must not treat that trade as an improvement. No such trade is established against a delivered note here.

## 4. Depth versus restatement, expansion and freshness repair

- **Restatement:** repeating “v262 rejects filtered `-F`” in a new file. S024 already teaches that proposition. An error quotation plus a new filename/source count alone does not establish a new causal account.
- **Freshness/provenance repair:** reopening mutable S024 at v262, saving source bytes/digest, and checking the installed binary. Useful, but it is not by itself depth or expanded coverage.
- **Depth:** a reader can distinguish the exact rejection and exit from a no-match result, understand why unique enumeration is not filtered entry selection, use the tested exceptions correctly, and select a semantically safe pattern for a named existing consumer. The error signature, actual matrix, mechanism and worked consumer decision are nonredundant ground missing from S024's one-line teaching. The declared design *can* supply this; delivery was not yet available to establish that it does.
- **Expansion:** requires an admitted entry on genuinely uncovered coverage-map ground, citing its map row and a mined source. Existing `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:10-11` already owns journal/boot triage; `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/README.md:8,12-13` already holds journal entry-counting ground. Another note or S198 row does not automatically establish expansion. Do not silently relabel this declared depth claim as coverage.

Framework evidence: `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:11-15,43-55`; `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md:31-50`; `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md:112-125`.

## 5. Provenance and duplicate-authority traps

S188 already registers the exact v262 `journalctl.xml` URL, scoped to JSON encoding, at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md:194`. A separately scoped S198 covering enumeration can add a needed proposition, but it is not an independent upstream authority. S190's rejected redundant threshold-code row at line 196 is a local precedent against counting duplicate authority as new evidence.

Reopening S024 at a pinned tag must not retroactively rewrite its historical `main` URL, anchor or opened field. The source contract permits in-place changes only to `status`, `recheck`, and `used-by`; corrections use a new superseding row. Smallest safe route: preserve S024's historical identity, record the pinned reopening and exact quote/snapshot in the lesson, and use an append-only superseding row if its immutable registry fields need correction. Explicitly scope S198 against S188.

**Impacted axes:** calibration, freshness, depth's source support. These are fixable evidence defects, not reasons to inflate the claim or relax the contract.

## 6. What the named non-author closure reviewer needs

1. The final landed C2 revision and the fixed predecessor; the actual note, SKILL rule, README row, source rows and round lesson—not only this proposal or signature search.
2. Source snapshots/digests and located quotes for the NEWS mechanism and manual semantics; live binary identity, exact argv, outputs and exits for both enumeration forms, with allowed controls and falsifiers. A source quotation must not be represented as a live observation.
3. A before→after comparison that explicitly acknowledges S024 and names the new operational decisions; a worked real-consumer substitution preserving scope, data shape and failure semantics; the note's applicable `## QUALITY check`.
4. An explicitly named outside/non-author reviewer, the reviewed commit, reasons the note is better, and the recorded exploratory judgment. The declaration's phrase “the named non-author closure reviewer” is not itself a name. The inspected declaration and wave registry supplied no actual closure-reviewer identity.
5. The outside spot-check's admit and reject decisions with reasons in the lesson. Neither this critic, the wave's `ReviewC2Draft` seat, nor another subagent dispatched by this lane substitutes for that outside reviewer: `AXES.md:47-50` and `LEARNING.md:42-50` explicitly exclude dispatched subagents.

The declared exploratory route remains the only route: no ordinal movement or measurable-proof shortcut follows from the prior-state grep. Whether the delivered note is genuinely better is reserved for that review and the canonical judge.

## Availability and scope

The inspected `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/ScribeC2Draft/`, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/SrcJournalctlMan/`, and `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/SrcSystemdNews/` directories were empty when opened. This is a dependency finding, not a claim that those seats failed or that later artifacts are absent. I did not wait or re-poll them. Final-note conformity and reviewer identity beyond the inspected declaration/registry remain [unk].

Executed: read/search operations, read-only git show/archive, scratch creation/export, scoped directory creation, `journalctl --version`, and the bounded read-only journalctl counterexamples recorded separately. No test suite, build, lint, gate, admission, integration, other model runtime or delegation was run. Tool installs/updates: none.

The requested outer `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/CriticC2Shape.md` is outside this seat's permitted write directory; the scoped companion `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/CriticC2Shape/CriticC2Shape.md` points to this full report instead.
