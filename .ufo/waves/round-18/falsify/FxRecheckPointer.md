# FxRecheckPointer — round 18

Axis: operability / fail-closed recheck-pointer resolution.

## High — FAILS

- The new regression's baseline red is accidental, not proof that the referenced probe set is checked. The immutable migration patch defines §6 with `pacman -Qm` and §7 with an explanatory `pacman -T` mention (`.ufo/waves/round-18/build/patches/MigRecheck.patch:486-498`); `pointer-aur-347-red` expects one hit for the §7 pointer (`:560-568`). In the actual source, the recheck line calls §7 a “probe set” (`corpus/knowledge/aur-risk-plane.md:347`), while executable operator probes are in §6 (`:261-280`) and §7 is “Unknowns and out-of-reach” (`:287-311`).
- The implementation resolves only the numbered heading and inspects commands inside that section: `follow_pointers` resolves `§7`, then scans only its span (`tools/check-recheck-commands.py:417-438`); `section_commands` treats backticks/fenced lines as commands (`:288-309`). It never reaches §6 from this pointer. The current apparent red comes from §7:309’s inline `pacman -T`, an explanatory statement, not the referenced probe set. If that incidental mention is removed/rewritten, the existing logic records no hit or unresolved pointer and can report clean despite the unsafe §6 probes.
- Required fix: fail closed when a pointer’s claimed procedure is not actually resolved (or repair the pointer to the explicit §6 procedure); add a regression with unsafe commands only in §6 and harmless/non-command §7 content. Preserve a separate R18 test that proves the appended file-read procedure resolves safely. The R18 append is present at `aur-risk-plane.md:431-446` and is statically file-read-only; runtime red/green was not exercised here.

## Residual risk / verification gaps

The migration report records 80 selftests passing (`.ufo/waves/round-18/build/MigRecheck.md:18`), but its AUR fixture does not distinguish §6 from the incidental §7 mention. No LSP device is mounted (`xd://lsp` returned “No such tool”); evidence is literal artifact/source reading, not semantic LSP proof. No tests or commands were run.

Scope: executed=none