# Probe lineage audit — probe-child-env-allowlist r32 → r33 → r34, and the r36 draft check

Seat: tsukuroi-r36.RevProbeLineage · 2026-10-24 02:54:42Z (pasted from `date -u`)
Scope: read-only. Lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin.

## Snapshots audited

| File | VERSION | sha256 (head) | State |
|---|---|---|---|
| `tools/probe-child-env-allowlist-r32.py` | (none; v2) 430 ln | `d43f95ed8a740b71aac1ab412e769e011127eb4ae29646d12b2075a696cf0576` | working tree == HEAD == base 6d76fb20 (`git status` empty) |
| `tools/probe-child-env-allowlist-r33.py` | 3 | `c24f344b864a13ea4db2909bfa81de77f8f41bae35cd5e0949a88b28ab1e04cd` | same; sha matches SCORECARD round-33/34 references ("probe bytes at `9c89ff4f`") |
| `tools/probe-child-env-allowlist-r34.py` | 6 | `5d0d568901c0eeb1c301b3bf825a839d4f41af68bc51e4de40f0706f15d1aa92` | same; sha + VERSION match round-34 amendment-2 (SCORECARD:1459, commit 3457f28) |

Method: modules imported from file in an isolated python process (no main run); `PREDICATE`
clause-substring containment checks; 28 module constants compared by value across versions; AST
dumps (`ast.dump`) of 19 shared functions compared r33↔r34 and 11 shared functions r32↔r33; full
unified diffs saved beside this file (`diff-r32-r33.patch`, `diff-r33-r34.patch`); machine receipt
`verify-rules.txt`.

## Per-rule kept/dropped table

Legend: rule present in the row's version? ✔ present, ✖ absent, — channel not existing yet.
"Verbatim" = exact substring in the `PREDICATE` constant; "AST-=" = function AST-identical to the
previous version.

| Rule / mechanism | r32 | r33 | r34 | Verdict |
|---|---|---|---|---|
| Injected-name clause (4 fixed + 8 generated, presence by `NAME=` prefix) | ✔ (predicate) | ✔ reworded "any name injected in that run" | ✔ verbatim r33 wording | **KEPT** (r32 wording generalized at r33, same rule; r33 wording byte-kept at r34) |
| Exact value-channel clause (`NAME=VALUE` for HOME, TMPDIR, XDG_CONFIG_HOME, PATH, LANG, TZ, TERM, USER, LOGNAME, SHELL) | — | ✔ | ✔ verbatim; `value_carriers` AST-= r33; `VALUE_NAMES` same | **KEPT** |
| Parity clause vs control A (rc, normalised stdout digest, git exec count) | ✔ | ✔ verbatim | ✔ verbatim; `parity` AST-= both hops | **KEPT** |
| Control A/B agreement + A ≥1 git child (harness rule) | ✔ | ✔ | ✔ (main hunks untouched) | **KEPT** |
| Source channel: ambient read / inheriting spawn / tracer strings / hiding constructs; amendment-2 `env=` shape, builder, alias, module rules | — | ✔ | ✔ `scan_module`, `_builder_findings`, `source_findings`, `_aliases`, `_bindings`, `_dotted`, `_contains_none` AST-= r33 | **KEPT** |
| `KEPT_GIT_SETTINGS` clause (git execve lacking GIT_CONFIG_NOSYSTEM=1 or GIT_CONFIG_GLOBAL=/dev/null) | — | ✔ (amendment 2 of r33) | ✔ verbatim; `KEPT_GIT_SETTINGS` same | **KEPT** |
| quiet channel | — | ✔ | ✔ (`CHANNELS` same r33→r34) | **KEPT** |
| Marker-script checks (bashenv.sh/env.sh writing `TSUKUROI_R33_*_RAN`, `bashenv_log_exists`, `bashenv_log_lines`) | ✔ (R32 markers) | ✔ (markers renamed R32→R33 by design; `make_inject_dir` AST-= r32) | ✔ byte-identical to r33 (markers, log fields, evidence wiring) | **KEPT** |
| Per-run fixture integrity (single `git archive` export at REV; fresh `copytree(symlinks=True)` per run into `wtree`, removed after) | ✔ | ✔ (`export_tree`, `is_git` AST-= r32) | ✔ (`export_tree`, `is_git`, `copytree` line untouched by diff) | **KEPT** — see finding F3 on the name "fixture byte-invariance" |
| execveat clause | ✖ | ✖ | ✔ **added** (round-34 amendment 2: `trace=execve,execveat`, `parse_trace` counts, predicate + evidence fields) | ADDITION, not a drop; **PRESENT** in r34 |
| Unparseable-record clause | ✖ (silent `argv,envp=[]`) | ✖ (same silent fallback) | ✔ **added** (`unparsed` counter, predicate "…or has an execve record the probe cannot parse", `unparsed_exec_records` field) | ADDITION, not a drop; **PRESENT** in r34 |
| Any-name ambient-value clause (`anyname_carriers`, TMPDIR equality + run-unique token containment) | ✖ | ✖ | ✔ **added** (round-34 amendment 2) | ADDITION |
| Base-parity clause (control A vs claim-base control; `git_argv_sha256` normalised git-argv multiset) | ✖ | ✖ | ✔ **added** (round-34 amendment 1; `base_parity`, `norm_arg`, `HEX_STR`, `TMP_COMPONENT`, `--base`, base-tree export) | ADDITION |
| fork-without-exec observation | ✖ as predicate clause | ✖ as predicate clause; static scan flags `fork`/`forkpty`/`fork_exec` aliases (`SPAWN_ANY`) | ✔ `SPAWN_ANY` byte-same r33→r34; runtime exclusion explicitly documented, see F1 | **KEPT** in its only existing form; never a predicate rule — not dropped, not silent (F1) |
| Target-set lineage | 11 `TARGETS` | same 11 → `REGRESSION_TARGETS` (set-equal ✔); 5 `CLAIM_TARGETS` | `R33_CLAIM_TARGETS` set-equal to r33 claim ✔; new 9-target claim set; new `r33claim` set | **KEPT** as regression / no-harm sets |

Predicate sentence integrity: r32 len 319, r33 len 799, r34 len 1331; each has zero interior
". " and a single terminal period (one sentence each). All 6 r33 clauses are verbatim substrings
of the r34 `PREDICATE`; the r32-only wordings are subsumed (name clause reworded at r33, parity
clause verbatim). Every r34 change to `PREDICATE` is additive (verified containment) — a
shortcut cannot pass r34 by a dropped r32/r33 clause.

Constants: 28/28 identical r33→r34 (incl. `SPAWN_*`, `HIDING_*`, `NAMED_INJECTED`,
`EXCLUDED_*`, `VALUE_NAMES`, `KEPT_GIT_SETTINGS`, markers, `CHANNELS`). r32→r33 diffs are
exactly: `EXCLUDED_EXACT` +`XDG_CONFIG_HOME` (additive strengthening, nothing removed),
marker-string versioning, `CHANNELS` additive.

## Findings

**F1 — fork-without-exec: never a probe rule; exclusion is loud, not silent (no defect in r34).**
The run channels of all three versions parse only `execve`/`execveat` records; a forked child that
never execs is invisible to them in every version, so there was no r32/r33 rule for r34 to drop.
The static source channel flags non-direct references to `fork`/`forkpty`/`fork_exec`
(`SPAWN_ANY`, byte-identical r33→r34). Round 34 handled the class explicitly: ReadRunChannels
reported fork-without-exec at 08:50:37Z, before amendment 2 (09:04:36Z) excluded it, and the L1
recorded the reason and the critic's "narrowing" judgement (base SCORECARD.md:1484, :1542);
the kill-rule reading states "Passing ambient data through argv, a file, a pipe or a fork without
exec is outside this claim" (:1465). Verdict: carried as a documented named limit, exactly as the
lineage requires. The bashenv/env marker scripts (fork+source observation evidence) are intact in
r34.

**F2 — the r36 draft is absent (dependency finding).**
`.ufo/waves/round-36/w1/ExecProbeR36/` does not exist (w1 contains only `swarm-registry.json`,
`ScribeC2Draft/`, `SrcJournalctlMan/`, `SrcSystemdNews/` at audit time). `swarm-registry.json`
registers `ExecProbeR36` with `"agentId": null` — registered spawn, nothing delivered yet. The
declared four-additions audit (exactly: VERSION 5 paragraph naming round 36 and the debt
repayment; `livefive` set; untraced view; normalisation fixes) could not be executed; nor the
one-sentence PREDICATE comparison. Sibling seats (ExecBeforeDesign, CriticClaimShape,
MutProbeDraft, SimplifierProbe, ExecV6NormCheck) each declared the same dependency-absent
fallback, so the wave is consistent.

**F3 — "fixture byte-invariance" does not name any rule in r32/r33/r34 (naming gap, no regression).**
No occurrence of "invarian"/"fixture" as a rule in any of the three probe files, and none in the
base SCORECARD. The structural guarantee that exists — one `git archive` export at REV, each run
getting a fresh `copytree(symlinks=True)` of it (`export_tree`, `is_git` AST-identical across all
three; the copytree line untouched by the r33→r34 diff) — is kept. If the ticket's phrase means a
distinct assertion, it exists in none of the three versions, so nothing was dropped. Round-35's
"normalisation fixes for … fixture paths" (SCORECARD:1522) is r36-draft scope, not an existing
probe rule.

**F4 — the round-36 declaration contains no predicate sentence (dangling reference).**
Base SCORECARD.md:1620-1621: "The probe is the counter; its frozen predicate label is
`leaking_pairs`, the same sentence in this declaration, the probe's `PREDICATE` constant and every
receipt." Grep for "leaking when" over the base SCORECARD: last match is the round-34 predicate
(line 1461); the round-36 section (1589→end) has none. So "the same sentence in this declaration"
has no antecedent — the sentence to freeze is not stated in the declaration [inf: the intended
sentence is most plausibly the round-34 predicate, extended only by the declared r36 additions].
Checkable requirement that survives: the r36 `PREDICATE` must be one sentence (r34's is —
verified) and must contain every r32/r33/r34 clause (verified for r34).

**F5 — VERSION numbering inconsistency for the draft.**
The declaration says the r36 counter is "the round-34 probe (`tools/probe-child-env-allowlist-r34.py`,
VERSION 4) plus this paragraph, VERSION 5 …" (SCORECARD:1637-1640). The file it names is
VERSION 6 (round-34 amendments 1 and 2 bumped 4→5→6 pre-data; commits 15c9ac0, 3457f28;
SCORECARD:1449, :1461). A draft that literally sets `VERSION = 5` would move the counter's version
backwards from the bytes it starts from. The draft author / L1 should resolve this (either
VERSION 7, or record the declaration's "(VERSION 4)" as loose wording) before the freeze commit
names the probe bytes. Flagged, not decided — outside this seat's scope.

## Verdict

No rule from r32 or r33 was silently dropped by r34. The r33→r34 diff (+146/−14 lines, 18 hunks)
contains only: the round-34 header paragraph, target sets (claim → 9 tools; + `r33claim`), VERSION
3→6, the declared amendment clauses (base parity; any-name value; execveat; unparseable), their
mechanics, and the additive summary key `base`. All 19 shared functions are AST-identical; all 28
shared constants byte-equal; every r33 predicate clause survives verbatim; exit-code contract and
`predicate_label` unchanged. The r32→r33 hop likewise drops nothing (11 shared functions
AST-identical; only additive channels/clauses plus the intended `EXCLUDED_EXACT` strengthening and
marker renaming). The r36 draft could not be audited because it does not exist yet (F2); the
audit it must pass is fully specified above, including the two declaration-side defects the draft
will collide with (F4, F5).
