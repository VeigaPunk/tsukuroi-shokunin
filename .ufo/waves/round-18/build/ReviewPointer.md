# ReviewPointer — read-only falsifier

Axis: operability / recheck-gate fail-closed behavior.

## High — FAILS

- **AUR pointer survives the falsifier.** [obs] `corpus/knowledge/aur-risk-plane.md:347` points at §7, but §7 is “Unknowns and out-of-reach” (`:287`); the explicit operator probe set is §6 (`:261-280`), including `pacman -Qm` (`:267`), `pacman -Si` and process-substitution `pacman -Qm` (`:269`), and `pacman -Qmdtq` (`:271`). The file ends at `:348`, with no R17/R18 steer-safe block. [inf] `tools/check-recheck-commands.py:303-305` scans only backtick spans in the last `recheck:` line; this pointer contains none, so `header_hits` is empty and `:332-340` reports it clean. Thus the gate does not follow the pointer or catch the forbidden probes.
- **Script indirection also survives.** [obs] The gate recurses into shell text only for `sh -c` (`tools/check-recheck-commands.py:210-233`); it does not inspect a script path. Census defaults `PACMAN` to `pacman` (`tools/tsukuroi-census.sh:351`) and invokes it at `:579`, `:594`, `:620`. Yet recheck lines call the script: `degraded-triage-r4.md:632`, `host-health-report-r3.md:575`, and `census-closeout-receipt-r10.md:189` (live census). [inf] These are false-clean candidates under the current parser.
- **Other pointer bypasses found:** `arch-news-gate-2026.md:3` routes to checks containing `pacman -Q/-Qm` at `:59`; `aur-risk-plane-ver-s6.md:139` routes to §§1–5 with package queries at `:23-29`; `aur-risk-plane-ver-s7.md:190` routes to a census and query battery at `:31,46-48`; `aur-drift-receipt-r9.md:254` routes to §6, whose re-derive commands include live census and direct queries at `:220-225`.

## Residual risk / verification gaps

[unk] This is a source-read falsifier, not an executed gate result. LSP is unavailable (`xd://lsp` is not mounted); grep was only a locator, with findings grounded in read source lines. Current bytes show no R18 repair; any future R18 mitigation remains unproven. No host probes or commands were run.

Scope: executed=none