# W2RevNoUpgrade — NoUpgrade supersession sweep, independent review

Seat: `W2RevNoUpgrade` (round 36, wave 2, falsify). Written 2026-10-24T04:38:48Z
(`date -u +%H:%M:%SZ` at write time).
Change commit under review: `c052bb7d41ced49aa888817069afd804eccfecf1` (parent `1e926801`).
Declaration: `6d76fb20f6ecbc940e5c8fff36c74060c885e161`. Base read for digests: `189d8a080ba8d508d5faab12cad9e688aee91dab`.
No production file was edited; no VCS mutation was run; no pacman invocation was made.

## Verdict on the assigned claim

The four-part claim **holds as stated**, with one wording caveat and two record-keeping defects
that sit beside it (findings 1 and 2 below).

| Claim component | Verdict | Evidence |
|---|---|---|
| Four `.append.md` blocks present at `c052bb7` in the three target files | **holds** | Each draft's fenced block is byte-identical in the target: SKILL.md 40 lines starting line 3010 (= base EOF + 1), `update-safety-note.md` 38 lines at EOF, `update-safety-v2.md` 25 lines (`:52` block) followed by 24 lines (`:198` block) at EOF |
| Each block quotes the original verbatim | **holds** | Programmatic: `'> ' + original_line` for every site line appears contiguously in HEAD — SKILL.md:397-399, note:420-425, v2:52, v2:198 all `True` |
| Each block names `pacman-backup-files-r35.md` | **holds** | Occurrences inside the landed blocks: SKILL.md 2, note 2, v2 `:52` block 2, v2 `:198` block 1 |
| Originals not rewritten (append-only clean) | **holds** | `git diff --numstat 1e92680..c052bb7`: 0 deletions in all three files (SKILL.md +51/-0, note +38/-0, v2 +49/-0); `HEAD_bytes.startswith(base_bytes)` True for all three; the four original sites are byte-identical to `189d8a08` |
| Gate posture of the appends | **holds** | `check-appended-notices` PASS (97 records, 0 findings); `check-adjacency-anchors` PASS (DRIFTED 17 / RESOLVES 96 / UNRESOLVABLE 1, 0 findings); `check-knowledge-header` PASS (56/56 complete, 0 findings); `check-recheck-commands` PASS (3 files, 0 flagged) — all at `--revision c052bb7` |

Wording caveat: "in SKILL.md (EOF)" is true only in the sense that the block begins at the base
file's tail (line 3010, base last line 3009). It is **not** the final EOF: the round-36 registry
section `## Gate and probe registry — round36 superseding current rows` follows at `SKILL.md:3050`
and runs to line 3060. The property the block itself needed (the `NOTICE-HISTORY` prefix test) is
satisfied either way.

## Findings

### F1 — HIGH (adjacent to this sweep, same file and commit): the round-36 registry table truncates the operative registry; `check-registry-coverage` FAILs at the change commit

`SKILL.md:3050-3060` is a "superseding current rows" table with **2 rows**
(`child-env-allowlist-r36`, `host-census`). Every prior round's table of that exact heading form is
cumulative, and each one's prose says so:

- rows per round table: r25 35, r29 48, r33 48, r34 50, r35 52, **r36 2**;
- `SKILL.md:2946-2947` (r35): "Every round34 row is retained verbatim"; `SKILL.md:2885-2886` (r34)
  the same for r33; `SKILL.md:3051-3053` (r36) claims "Every round35 row is retained verbatim …
  marks the five live tools' child-environment builders as fixed-dict" — the table below carries no
  such row and none of the 52 round-35 rows.

Measured consequence, `python3 tools/check-registry-coverage.py --revision c052bb7d41ced49aa888817069afd804eccfecf1`:

```
exit=1  status FAIL  counts {findings: 51, missing: 51, registered: 2, rows_total: 2, tools_total: 53}
first: REGISTRY-ROW-MISSING tools/_revision.py "no operative row names this regular tools/ file"
```

Because the checker takes the highest-round table as operative, the change commit ships a registry
that covers 2 of 53 tools. This is not caused by the NoUpgrade appends (they add no pipe-prefixed
line), but it lands in the same file and commit and it contradicts the section's own prose.
Owner in the dispatch: the registry close-out seat (`W2ExecCensusEnd`, whose prompt says
"check-registry-coverage reads it — confirm its verdict"); recorded here because it is a red gate
at the revision this review is anchored to.

### F2 — MEDIUM: the residual loci are not recorded in any committed artifact at `c052bb7`

The claim says the residual loci are "recorded as not-in-routed-scope". At the change commit they
are recorded **only** in untracked wave-1 files:

- `git grep -n "outside the routed\|not in routed scope\|not-in-routed\|residual loci" c052bb7d` →
  **no hits** in `SKILL.md`, `SCORECARD.md`, `corpus/`, `.ufo/`;
- the record exists in `.ufo/waves/round-36/w1/ScribeNoUpgrade/ScribeNoUpgrade.md:130-137` and
  `residual-mentions.md`, and `.ufo/waves/round-36/w1/` is untracked (`git status`: `?? .ufo/waves/round-36/w1/`);
- tracking convention says it should be committed: `git ls-files .ufo/waves/round-35 | wc -l` = 1487,
  round-34 = 760, round-36 = 19.

The non-mutation itself is correct — `corpus/knowledge/degraded-triage-r4.md` is untouched by the
change commit (absent from its numstat) and the note's `:346` row is unchanged — so
"not-in-routed-scope" is factually right; what is missing at `c052bb7` is the recorded statement.

### F3 — LOW: the residual set is undercounted (3 loci measured, 2 named)

The seat's own report lists **three** class-A loci: `corpus/knowledge/update-safety-note.md:346`,
`corpus/knowledge/degraded-triage-r4.md:392`, and `update-safety-note.md:204` + `:212`
(`## 4. Pins and holds — measured, plus what `HoldPkg` does not mean [observed]` together with
`| any | `pacman-conf NoUpgrade` / `NoExtract` | **empty** |`). The wave-2 prompt and the claim
name only the first two. Verified still present at `c052bb7` (lines quoted above). A reader taking
the two-locus list leaves the note's own §4 heading/row unaccounted for, in the same file the
sweep appended to.

### F4 — OBSERVATION (not a defect): `check-self-assessment` is red at the change commit, and the K08 obligation is only in the untracked draft

`python3 tools/check-self-assessment.py --revision c052bb7d41ced49aa888817069afd804eccfecf1`
→ exit 1, K07 `stated 55 / observed 56` notes, K08 `3009 / 3060` SKILL.md lines, K09 `784 / 788`
pipe-prefixed lines, K10 `46 / 48` lesson files (all `stated_line: 1570`, the round-35 depth row).
K09's delta is the registry table's 4 pipe lines, not the NoUpgrade appends; the SKILL.md append
block explicitly owed K08 ("the round-36 axes depth row must state the new number"), and that
obligation currently exists only in the untracked draft (F2's tracking gap). Whether this gate is
one of the seven that must be green at the change commit is [unk] to this seat — the declaration
(`SCORECARD.md:1672`) names "the seven lane gates" without listing them.

### F5 — COSMETIC: no blank line before the appended heading pair in SKILL.md

`SKILL.md:3049` (block's last paragraph) → `:3050` (`## Gate and probe registry — round36 …`).
CommonMark still parses the ATX heading; no gate flagged it. Noted only because it is the seam
between the assigned append and the registry section of F1.

### F6 — WAVE-INTEGRITY (observed 2026-10-24T04:39:51Z; not this seat's edit): HEAD moved mid-review, and the in-flight registry repair writes a malformed table

At 04:20Z the worktree HEAD was `c052bb7` (detached); by 04:39:51Z `git rev-parse HEAD` returns
`8d5fa7fe27c336d602a463519e839e932d26301d` and `SKILL.md` is dirty with an uncommitted
`+54/-4` edit that expands the round-36 registry to the full operative set (this is the repair for
F1). Two things the L1 must fix before landing it:

1. The table is **malformed**: `SKILL.md:3056` is the `| Name | Kind | …` header, `:3057` is the
   `child-env-allowlist-r36` data row, `:3058` is the `|---|---|…` delimiter. GFM requires the
   delimiter row immediately after the header; with a data row in between the table does not
   parse. The `---` row should stay at 3057.
2. The prose was edited to "round36 **prepends** one probe row" while the table lists that probe
   first and then `host-census` — that is consistent, but the simultaneously deleted clause
   ("marks the five live tools' child-environment builders as fixed-dict") is the only sentence
   that carried the C1 marking in the registry; if no row now carries it, the C1 registry
   assertion is dropped rather than repaired [inf: I could not see a fixed-dict marking in the
   in-flight rows].

The claim verdict above is unaffected: every block check was re-run against the **commit bytes**
(`git show c052bb7:…`) after the HEAD move and all four blocks are still present verbatim
(`present_in_commit=True` ×4).

## Residual risk

- The four appends are correct and their gates pass; the risk they carry is that the SKILL.md
  depth-row line count (K08) is now stale in the operative round-35 row, and the obligation to fix
  it lives outside the commit.
- F1 means the *registry* contract of the same file is broken at the revision under review. If the
  outcome commit writes a round-36 depth row but keeps the 2-row table, `check-registry-coverage`
  will stay red.
- The third residual locus (F3) is a known, unfixed misclassification inside a file this sweep
  edited; the supersession text in that file does not cover it.

## Verification gaps (honest)

- **Unrun:** the census (`tools/tsukuroi-census.sh`), the C1 probe battery, and the seven-gate set
  as a whole — outside this seat's scope, owned by `W2ExecCensusEnd`/`W2ExecGates`.
- **Unrun:** `check-self-assessment`'s selftest; only the `--revision` run above was executed.
- **Semantic-caller checks:** `lsp` was not used — the changed artifacts are Markdown documents
  with no language server answering them, so all reference checks here are byte/line comparisons
  and the named tool runs; no grep output is presented as semantic proof of a caller contract.
- **Not re-measured:** host `/etc/pacman.conf` directives. The appends' value claims are
  `[inf]` from the committed text; this seat ran no pacman binary (host-wide pacman pause).

## Tooling

No tool was installed or upgraded in this seat.
