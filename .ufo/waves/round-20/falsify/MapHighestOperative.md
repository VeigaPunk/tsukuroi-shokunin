# MapHighestOperative — R20 C3 table-selection attack

## Finding

**The ordinary historical-row control is handled correctly, but table selection has a Markdown-context false-green.** The checker can treat an inert registry example inside a fenced code block as the unique highest operative table; its corrected `boot-chain-audit` row can therefore hide a live-`1 DEGRADED` row in the actual highest table. This is a fixable parser defect affecting **C3 calibration**; no C1/C2 impact is identified.

The contract says the unique highest-numbered complete registry table is operative and earlier tables are historical (`SKILL.md:1997–1999,2098,2118`); preregistered C3 expects a historical-only repair to remain red (`.ufo/waves/round-20/preregister.json:27,49–53`). The candidate does handle the straightforward case: `_operative_rows()` finds the maximum exact heading and refuses a duplicate highest number (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:137–150`), returns rows only from that selected section (`:151–183`), and `main()` supplies those rows—not historical rows—to `_audit_live_map()` (`:348,351–355`). The existing C3 selftest also checks corrected lower/legacy higher → fail and corrected higher/legacy lower → pass (`:592–613`).

The gap is that heading discovery applies `REGISTRY_HEADING.fullmatch()` to every source line without tracking Markdown fences (`:139–143`), and the selected section's registry-header/table scan likewise does not exclude fenced content (`:151–182`). Thus text that is not a Markdown heading/table can be elevated into the selected table. `_audit_live_map()` then validates that parsed row exactly (`:270–288`).

## Minimal adversarial fixture

Create a fixture repository with one regular `tools/boot-chain-audit.sh` blob containing `--selftest`, and this `SKILL.md` (use the exact eight-column header/separator; show only the relevant row):

````markdown
## Gate and probe registry — round19 superseding current rows
| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| boot-chain-audit | probe | bash tools/boot-chain-audit.sh --live | 0 CONSISTENT;1 DEGRADED;2 UNKNOWN | bash tools/boot-chain-audit.sh --selftest | fixture | read-only | fixture |

```markdown
## Gate and probe registry — round20 superseding current rows
| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| boot-chain-audit | probe | bash tools/boot-chain-audit.sh --live | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | bash tools/boot-chain-audit.sh --selftest | fixture | read-only | fixture |
```
````

**[INFERENCE — not run under the NO-EXEC boundary]** The current implementation sees the fenced `round20` heading as the unique maximum, parses its corrected row, and returns `audit_live_map_errors=0` / exit 0, although the actual top-level round19 row still advertises live `1 DEGRADED`. The fixture has only one tool and the selected row covers it, so this isolates the table-selection false-green rather than generic coverage.

## Smallest safe correction

Make `_operative_rows()` Markdown-fence-aware: ignore lines inside fenced code blocks when discovering registry headings, locating the required registry header, and collecting table rows. Add the fixture above as a negative control, asserting that the actual top-level round19 row governs and produces the preregistered `REGISTRY-AUDIT-LIVE-MAP` / exit 1; retain the existing real-highest-vs-historical controls and duplicate-highest could-not-evaluate behavior.

## Limits

Static source review only; no candidate command, selftest, build, or runtime was executed. This concerns the registry's finite C3 declaration only and makes no host or boot-safety claim.

Scope: executed=none
