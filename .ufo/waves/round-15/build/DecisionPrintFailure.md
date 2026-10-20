# DecisionPrintFailure — round 15

Seat TsukuroiR15.DecisionPrintFailure. Baseline `0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2`. Report-only: no docs edits, no host queries, no package/service/sudo/credential action, no child or labrat dispatch; tools installed/updated: none.

## Concrete decision fragment

Row for the agent package-request guard (`pacman -Sp --print-format '%n %v' <pkgs>`). It is the **precondition row**: no sibling request row may be evaluated unless this row returns `PLAN_EVALUABLE`.

| field | R15-PRINT-FAIL |
|---|---|
| trigger | The guard cannot yield a complete, parseable plan: tool absent or unexecutable (subprocess `ENOENT`/`EACCES`, shell 127/126), pacman's own exit ≠ 0, out-of-spec argv (no print mode: neither `-p`/`--print` nor the implying `--print-format`; or `-w`/`--downloadonly`, `--needed`, wrapper/alias), rc=0 with 0 lines for a non-empty request, malformed/partial lines, or any stderr error/warning that accounts for an absent requested target. |
| required receipt | Verbatim argv; resolved tool path and version; **pacman's own** exit (not a pipeline's); stdout bytes; stderr bytes (never discarded); requested tokens; parsed `%n`/`%v` pairs; requested-token → resolved-name mapping. Any missing field ⇒ `CANNOT_EVALUATE`. |
| decision | `BLOCKED_FOR_AGENT_PACKAGE_ACTION`, subreason `CANNOT_EVALUATE_PRINT_PLAN`. No `-S`, no relaxed flags, no substitute resolver; a repeat of the exact read-only guard after an operator-side fix is a new receipt, not a reinterpretation. |
| epistemic state | Unknown, not "unsafe" and not "safe". The action gate blocks in all failure branches; it does not assert package harm. |
| forbidden inference | Empty stdout = nothing to do/safe; a pipeline's rc = pacman's rc; absent from the plan = not installed; missing tool = nothing to install; `yay -Sp`/`checkupdates` = equivalent; drop print flags to "see the plan". |

| branch | receipt shape | classification |
|---|---|---|
| B0 tool absent/unexecutable | `ENOENT`/127 or `EACCES`/126, empty stdout, "command not found"/"permission denied" | `TOOL_ABSENT` |
| B1 resolution/DB error | pacman rc≠0: target not found, dependency failure, unreadable/missing sync DB, lock/refusal | `RESOLUTION_ERROR` |
| B2 download error | stderr retrieval/network failure on a claimed `-Sp` | `NOT_THE_GUARD` — pure `-Sp` does not download |
| B3 pipeline rc | `pacman … \| wc -l` rc=0, 0 lines | `PIPELINE_RC_FALSE_SAFE` |
| B4 unexpected empty | exact argv, non-empty request, rc=0, 0 lines | `UNEXPECTED_EMPTY` |
| B5 partial/malformed | rc=0, but a requested token has no mapped line, or a line is not exactly two non-empty fields | `PARTIAL_PLAN` |
| B6 contrast only | exact argv, rc=0, ≥1 valid line per mapped token, no stderr error (warnings recorded and consistent with present tokens) | `PLAN_EVALUABLE` (still no transaction this round) |

Receipt shape (reuses the wave snapshot's `command`/`exit`/`stdout`/`stderr` keys):
`{"command":"pacman -Sp --print-format '%n %v' -- pkg","tool":"/usr/bin/pacman","exit":1,"stdout":"","stderr":"error: target not found: pkg","requested":["pkg"],"parsed":[],"mapping":{},"decision":"BLOCKED_FOR_AGENT_PACKAGE_ACTION","reason":"CANNOT_EVALUATE_PRINT_PLAN:RESOLUTION_ERROR"}`

## Evidence

- pacman(8), local installed page, footer `Pacman 7.1.0  2026-05-06`, OPTIONS: `-p, --print` = “Only print the targets instead of performing the actual operation (sync, remove or upgrade).” `--print-format` = “Specify a printf-like format to control the output of the --print operation.” and “Implies --print.” (so the guard's explicit `-p` is redundant, not load-bearing) `-w, --downloadonly` = “Retrieve all packages from the server, but do not install/upgrade anything.” `--needed` = “Do not reinstall the targets that are already up-to-date.” Hence the guard is print-only; the option set's only normal route to an empty plan is `--needed` skipping up-to-date targets, which the guard does not use [inference from the option text].
- Measured installed-target behavior: `corpus/knowledge/update-safety-note.md:199-202` records `pacman -Sp --print-format '%r/%n %v %s' nvidia-utils` → `extra/nvidia-utils 610.57.04-1 0`; `driver-firmware-plane.md:73` shows that package as installed. So on this host/version an explicit installed target printed rather than vanishing [observed, one package]. Generalizing to every target is [inference]; the row does not depend on it, since B4 stays blocked either way. (The note's other lesson: `%s` printed `0`, so output fields must be validated, not trusted.)
- Established repo precedent: `tools/tsukuroi-census.sh:1518-1524` maps `pacman -Sup --print-format` rc≠0 to `BLOCKED` with “candidate set not confirmable”; selftest case `:2484-2486` pins exit 2 / `BLOCKED` for `sup=rc=1`. This is the same fail-closed move applied to the requested-target plan.
- Pipeline-rc trap: `SKILL.md:1239-1242` requires `-Qu` **unpiped** and treats “any other shape” as unreadable → `BLOCKED`, “never INERT — the pipeline-rc trap made executable”. `pacman … | wc -l` with pacman absent or failing yields `$?`=0 and 0 lines while `${PIPESTATUS[0]}`=127 or pacman's error code: the canonical false-safe.
- Empty ≠ current: `corpus/knowledge/update-safety-note.md` §2 — “`-Qu` empty proves 'nothing newer than a 36-day-old snapshot', not 'fully current.'” A plan lists transaction actions, not installed-package state (`%v` is the target version only; the plan does not carry the installed version); even B6 requires a separate installed-inventory join.
- Wave state: `host-snapshot.json` (captured `2026-10-20T07:44:39Z`) has probes `package_versions`, `pending_updates`, `sync_metadata`, `libinput_log`, `boot_hook_mentions` — **no `-Sp` probe**. `ScribeClaims.md` F5: “No dry run was executed here.” The wave therefore holds no plan receipt; the guard is unevaluated, and the fixed decision is blocked regardless of fresh counts.

## Recommendations for L1

1. Make R15-PRINT-FAIL the precondition for every other request row: without B6, do not reach installed/new-dependency/foreign/count verdicts.
2. Record argv, not a reconstructed command; require the format as one argv element (`%n %v`) and use `--` before package names (a terminator, not a resolution flag); any extra resolution/download flag is a new, uninterpreted receipt.
3. Capture with argv execution (`shell=False`) or verified `pipefail`/`PIPESTATUS`; never pipe the guard before capture (`wc`, `head`, `grep`), never `2>/dev/null`, and record tool absence as `ENOENT` rather than empty output.
4. Collapse B0–B5 to the same decision; do not rank them as different safety degrees. Unknown neither clears nor condemns the package.
5. Leave the `--needed`-empty case to DecisionAlreadyCurrent, installed-newer to DecisionAlreadyInstalled, transitive upgrades to DecisionNewDependency, and foreign targets to DecisionForeignPackage; this row only gates their evidence.
6. Treat a download error on a claimed `-Sp` as a protocol deviation (non-guard invocation), not a package-resolution fact; preserve it for the incident packet.
7. Cite pacman(8) by OPTIONS headings plus footer, not rendered line numbers, per the R15 locator discipline.

## Sources, limits, tools

- Sources read: local pacman(8) page (Pacman 7.1.0, 2026-05-06) via `man -P cat 8 pacman` — a static documentation read, not a host state probe; `corpus/knowledge/update-safety-note.md`; `SKILL.md`; `tools/tsukuroi-census.sh` (implementation and selftest fixtures); `corpus/SOURCES.md` row S010 (partial-upgrade doctrine context, not reopened); wave `host-snapshot.json`, `ScribeClaims.md`, `spec.json`/`dispatch.json` context.
- S048 URL (`https://man.archlinux.org/man/pacman.8`) was **not** reopened by this seat. SourceRegistry owns S048; re-verify the quoted option text and footer against that URL before landing the row. This report supplies quote/date as a lead, not as S048 evidence.
- Limits: no `pacman`, `-Sp`, `-Qu`, `--version`, package, service, snapper or sudo command ran. No failure fixture was executed; the rc taxonomy is deliberately not claimed (the rendered page text I read has no EXIT STATUS section — bounded string search, not an exhaustive absence claim). Error strings are locale/version-dependent and advisory; rc and output shape are authoritative. The zero-line-success anomaly is argued from the option semantics plus one measured installed-target invocation, not from an executed negative. Wrapper identity and pacman 7.1.0 edge cases are untested. No checker or executable was written; this fragment is documentation, not enforcement, and makes no ordinal claim.
- Tools installed/updated: none. No package changes, upgrades, downgrades, removals, service restarts, snapper queries or daemon activation.
