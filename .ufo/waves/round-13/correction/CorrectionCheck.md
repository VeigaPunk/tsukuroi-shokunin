# CorrectionCheck — round 13 scoped findings

## Axes

- **Depth only:** narrow executable conformance for R13-DAC-EXCLUSIVITY.
- Not source correctness, admission authority, host health or causal proof.

## Files changed

- `tools/check-root-dac-correction.py` (new, read-only gate; sole implementation write).
- This report.

No corpus, registry, source, fleet, sibling or LOG file was edited; no commit. No gate
invocation, `--selftest`, build, lint or repo test was executed; expectations are static
and L1 owns the single shipping run.

## Shape

- 375 lines total, ~260 evaluator/CLI; remainder is one compact in-memory fixture and
  13 cases. No 20KB prose/schema duplication.
- Predicates committed semantics, not full prose equality: historical site patterns,
  notice pointer, correction id, narrow/non-exhaustive scope, mechanism names/flags,
  private-namespace unknown, `S041`, fixture `executed_root_owned_fixture=false`,
  resolved-parent scope, strict exceptions, minimal headings/tables, and absence of the
  active old universal.
- Entry: tree by default or `--revision <HEAD|hex>`; both call `evaluate()`. Exit 0 clean,
  1 failed, 2 could-not-evaluate.
- Stable summary:
  `CHECK_ROOT_DAC_CORRECTION: <PASS|FAIL|CANNOT_EVALUATE> correction_count=<0|1> source=<tree|revision:sha> scope=narrow-conformance-not-semantic-proof findings=<n>`;
  `correction_count=1` only for a fully clean correction.
- Findings are `F <stable-id> site=<stable-site> detail=<bounded>`, no file payload.
- Revision hardening: `HEAD`/4–64 hex only, commit resolved before blob reads, argv
  list/no shell, inherited `GIT_*` stripped, optional locks disabled, no writes.
  `--selftest` is in memory.

## Predicates (not exact prose pins)

r12 history/supersession:
- The specific old pattern must remain at MD current-host and R13 sites and in JSON B2
  `limit`; absence is `R12-*-HISTORY-MISSING` (preservation failure).
- Exact MD heading; notice names current-host, worked-example, R13, B2 and
  decision-procedure sites, points to both r13 files, carries `R13-DAC-EXCLUSIVITY`,
  and scopes `ProtectSystem=no`/empty `ReadOnlyPaths=` without excluding B2.
- r12 JSON `superseded_by = corpus/knowledge/root-dac-correction-r13.json`; its notice
  names B2 interpretation/limit.
- If any supersession piece or r13 content check fails, the old statements are active:
  per-site `R12-*-EXCLUSIVE-*` plus `UNIT_READONLY_FALSE_UNIVERSAL`.

r13 MD:
- Title, corrected-claim, mechanisms, unknown-cause and QUALITY headings in order; two
  four-column tables; `source:` with `S041`.
- One plain-text block must carry all four mechanisms, `ProtectSystem=no` + empty
  `ReadOnlyPaths=` + "not excluded by", full-vs-strict with `except /dev/ /proc/ /sys/`,
  non-exhaustive language, and the unobserved/invisible private namespace.
- No active old universal and no affirmative general-correctness claim.

r13 JSON:
- `correction_id = R13-DAC-EXCLUSIVITY`; narrow scope stating it is not a proof of
  general semantic correctness.
- Exactly four `retained_alternatives`: `BindReadOnlyPaths=` true, `TemporaryFileSystem=`,
  `RootDirectory=` and `RootImage=` false; effects retain EROFS-indicator, no-tmpfs-default-RO,
  and not-intrinsically-RO semantics; `corrected_universal.source_ids` includes `S041`.
- `full_vs_strict` + exceptions retain full-not-root and strict exceptions.
- `unknowns.unit_private_namespace` is unobserved/invisible, not certain.
- `fixture_identity.executed_root_owned_fixture` is false; `ro_parent_scope` names the
  resolved parent and B4/EEXIST; non-exhaustive language is present.

## Expected red/green (not executed by this seat)

Baseline containing the r12 pair (declared baseline `9574a189…`):

```sh
python tools/check-root-dac-correction.py --revision 9574a189a758251da5957eee8ff0f38ba2d03c7f
```

Static expectation: exit 1, `correction_count=0`, `findings=9` — two MD active
exclusives, JSON B2-limit active, `UNIT_READONLY_FALSE_UNIVERSAL`,
`R12-MD-NOTICE-MISSING`, `R12-JSON-SUPERSEDED`, `R12-JSON-NOTICE`,
`R13-MD-MISSING`, `R13-JSON-MISSING`. The false sentences themselves are detected;
missing r13 is additional, not the sole reason.

Corrected tree or landed correction commit:

```sh
python tools/check-root-dac-correction.py
```

Static expectation: exit 0, `correction_count=1`, `findings=0`. A pre-r12 revision
without the pair correctly exits 2.

## Selftest (13 in-memory cases)

Baseline red; corrected green; sole-delta `remove-alternative`,
`rootdirectory-intrinsic-RO`, `tmpfs-default-RO`, `namespace-certain`,
`closed-list-restored`, `strict-drop`, `notice-missing`, `superseded-wrong`,
`malformed-r13-json`, `history-deleted`, `table-broken`. Assertions cover exit code,
required IDs and `correction_count`; fixtures/mutations are compact dictionaries and
lambdas, not copied 20KB files.

## Evidence anchors (read-only)

- Gate: `tools/check-root-dac-correction.py`.
- Correction: `corpus/knowledge/root-dac-correction-r13.json`; MD headings/sections.
- Historical sites: r12 MD lines 53/86 and JSON B2 `limit`; r12 notice heading and
  `superseded_by`.
- Contract: `corpus/QUALITY.md` #17/#18, `corpus/lessons/round-13.md` § Gate,
  `corpus/lessons/round-12-verifier-spotcheck.md` C2/routed defect 1.

## Limits

- Narrow conformance, not semantic/source truth or causal history.
- Predicates are intentionally shape-specific; future schema changes require updating
  the compact checks.
- Boundaries: no host, journal, service, package, registry or privileged surface touched.
- Tooling: none installed or upgraded.
