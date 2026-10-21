# SysctlValueArgs — source-only findings

## Scope and confidence

Axis: C2 operability, supporting finite systemctl exec-log classification only. Inspected candidate: `/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py` (source snapshot tag `E248`). All candidate line citations below refer to that absolute path. No C1/C3 metric, integrated-revision result, host safety, or boot clearance is established.

**Answer:** Recognized value-taking options consume their arguments exactly once. Missing, empty, and dash-prefixed **separated** values are rejected. However, nonempty **inline** values receive no content validation, and nonempty separated values receive only a leading-dash check. Therefore blanket rejection of malformed values is not supported. I found no source-level mechanism by which these correctly recognized option values are subsequently rescanned as a mutating verb; this is not proof about arbitrary shell syntax or actual systemctl behavior.

Confidence: high for the explicit source branches; all example outcomes below are **[INFERENCE: static control-flow predictions, not executed results]**. No LSP device was exposed/permitted in this NO-EXEC seat; definitions and callers were traced by literal search and direct source inspection, not semantic-reference proof.

## Observed argument consumption

- The exact table contains `--property`, `-p`, `--type`, `-t`, `--state`, `--output`, `-o`, `--lines`, `-n`, `--host`, `-H`, `--machine`, `-M`, `--root`, and `--image` (`:283-285`). All use the same value branch (`:313-326`).
- `--flag=value`: the parser partitions once at the first `=` (`:309`), rejects an empty suffix (`:314-316`), advances one token (`:317`), and immediately continues (`:326`). Neither the suffix nor the next token is rescanned as that value.
- `--flag value` / `-p value`: the parser requires a following nonempty token not beginning with `-` (`:318-321`), advances two tokens (`:322`), and immediately continues (`:326`). End-of-input rejects (`:323-324`). Repeated options revisit this branch independently; there is no second shared increment after it.
- Attached `-H...` and `-M...` have an earlier prefix branch that advances exactly one token without inspecting the suffix (`:287,304-307`). Attached property/type/output/lines spellings have no corresponding prefix branch; for example, `-pId` is an unknown flag in this implementation (`:304-327`). This establishes a finite parser limitation, not a measured runtime compatibility failure.
- The first unconsumed positional token becomes the verb (`:328-330`); later positionals do not replace it. Options remain recognized after a verb until an explicit `--` (`:292-330`). An explicit `--` disables further option handling (`:294-297`). With no truthy verb, the final check uses `list-units` (`:331`).

## Malformed values: validation is structural, not semantic

The entire value branch is `:313-326`; it contains no numeric, property-name, type/state/output-enumeration, hostname, machine, path, or option-combination validation. Inline values are checked only for nonemptiness, unlike separated values.

| Inert example text | Predicted classifier result and reason |
|---|---|
| `systemctl show --property` | Reject: value absent (`:318-324`). |
| `systemctl show --property=` | Reject: empty inline suffix (`:314-316`). |
| `systemctl show --property ''` | Reject: empty separated token (`:319-321`); tokenizer preserves quoted empty arguments (`:190-198,209-210`). |
| `systemctl show --property --force` | Reject: separated value starts with `-` (`:319-321`). |
| `systemctl show --lines=not-a-number` | Accept: nonempty inline suffix, then allowed `show` (`:314-317,331`). No numeric check occurs. |
| `systemctl show --output=not-an-output-mode` | Accept for the same reason; output-mode membership is not checked. |
| `systemctl show --property=--force` | Accept: `--force` is opaque value text, not a separately parsed option (`:309,314-317,326`). **This does not itself demonstrate an effectful operation.** |

The same lack of domain validation applies to type/state and host/machine/root/image values because they share that branch (`:283-285,313-326`). Consequently, parser acceptance cannot establish that a value is meaningful to systemctl, that combined context options are compatible, or that a remote/image/path target is safe. Those remain outside this evidence.

## Effectful flags and verb scanning

Observed: `--now` and `--force` occur in neither option table (`:279-285`) and reach the rejection at `:327` when parsed as standalone options. Only the finite read verbs at `:276-278` survive the final membership check (`:331`). `--runtime` is now a non-value read flag (`:281,310-312`), so it does not consume a following verb; this inspected source differs from the older description in `.ufo/waves/round-20/build/ExecOptions.md:5`.

**[INFERENCE]** For every listed value-taking flag, a mutating verb remaining after its one required value is consumed is still the first positional verb and fails the read allowlist. Conversely, a word occupying the required value position is intentionally not a verb. A mutation-like word appearing only after a latched read verb is merely another positional operand to this classifier (`:313-331`). Neither situation alone proves a hidden mutation. Content that merely spells an effectful flag inside a value must not be equated with a separately parsed flag.

Call chain inspected: `simple_commands` supplies argument tokens after the identified command word (`:242-247`); `systemctl_violations` applies `_systemctl_read_only` only to command word `systemctl` and records rejection (`:342-345`); `assess_exec_log` scans `$ ` lines and adds the systemctl-specific findings unless a generic systemctl ban was explicitly supplied (`:658-667`); CLI `run` consumes these findings and reports their count (`:857-864,879-883`). These are source observations, not execution evidence.

## Existing evidence and remaining gaps

- Candidate read fixtures cover inline property/type/state, inline host/machine/root/image, and separated host (`:1469-1478`). Their aggregate declares `PASS` and zero exec violations (`:1489-1492`); this declaration was not exercised here.
- The malformed/effectful aggregate contains `status --property --force`, direct `--force`/`--now`, and a mutation following `--runtime` (`:1498-1513`). It does not provide a per-flag matrix for missing/empty/repeated values, inline malformed content, separated values for every flag, or short property/output/lines forms. Literal search of this candidate found no additional `_systemctl_read_only` callers beyond `:344`; no repository-wide semantic-reference completeness is claimed.
- A finite additional matrix could distinguish both value spellings, values before/after a read verb, repeated `-p`/`--property`, and each missing/empty/dash-value case. Whether malformed *domain* values should be rejected or merely left to systemctl needs an explicit contract; the current source implements only the structural boundary above.
- `.ufo/waves/round-20/preregister.json:55-65` specifies finite mutation/read/unknown-verb outcomes and expressly disclaims arbitrary shell equivalence, runtime enforcement, and current host/boot readiness. It does not specify full value-domain validation. This report therefore identifies the validation limit without treating it as evidence that the preregistered C2 metric changed or that a host operation is safe.

Only this report was written. No commands, tests, imports, builds, formatter/linter checks, host probes, external requests, or tool installations were performed. Boot images remain UNKNOWN; no clearance.

Scope: executed=none
