# DecisionNewDependency — new requested package, installed dependency upgrade (round 15)

Seat `TsukuroiR15.DecisionNewDependency` · baseline `0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2` · report-only, read-only research; no docs edits, host queries, package/service/sudo/snapper action, child dispatch, tests or verification claimed. Tools installed/updated: **none**.

## Concrete decision row

| field | R15-DEC-NEW-PKG-TRANSITIVE |
|---|---|
| trigger | Every requested name is absent locally, but the fixed guard plan `pacman -Sp --print-format '%n %v' -- <pkgs>` lists ≥1 printed `%n` for which `pacman -Q <n>` succeeds. The installed printed name is a dependency pulled by resolution, a provides target, or a replacement — not necessarily a requested token. |
| required receipt | Exact argv; pacman's unpiped exit; full stdout/stderr; parsed `%n`/`%v` pairs; per-printed-name `pacman -Q` exit and local version; requested→printed mapping; `alpm_pkg_vercmp(printed %v, local)` class; context `pacman -Qu` count and sync-DB birth. A missing join ⇒ `CANNOT_EVALUATE` under `R15-PRINT-FAIL`, never a pass. |
| decision | `BLOCKED_FOR_AGENT_PACKAGE_ACTION`; reason `PARTIAL_UPGRADE_WOULD_UPGRADE_INSTALLED_DEPENDENCY`; `transaction_permitted=false`, `transaction_started=false`. **Same stop** as `R15-DEC-ALREADY-INSTALLED-NEWER`; "only a dependency" is not a lesser class. |
| non-clearance | An add-set of only absent names does not clear `-S`: installed-but-satisfying deps are not pulled, conflict removals are not printed, and the captured host has 413 pending upgrades against sync DBs born `2026-10-18T17:11:00Z` — S047's unsupported state. Round 15 executes no `-S` even on a clean plan. |
| epistemic | Unknown, not "safe": the print is an add-set preview, not a transaction certificate. |
| forbidden inference | Filtering the plan to requested names; "new requested package ⇒ not a partial upgrade"; "`--needed` prevents it"; "clean/empty dependency delta ⇒ safe"; "`-Sp` proves removals/conflicts absent"; "the plan now equals the commit state"; "use `-U`, a helper, `--assume-installed`, or relaxed flags instead". |

| branch | observed plan shape | classification | decision |
|---|---|---|---|
| N0 unusable plan | rc≠0, partial/malformed, or unexpected empty | `CANNOT_EVALUATE_PRINT_PLAN` | `BLOCKED_FOR_AGENT_PACKAGE_ACTION` |
| N1 all printed absent | every `pacman -Q %n` fails | `NEW_ONLY_ADD_SET` | blocked this round; state-level reason remains |
| N2 installed `%v > local` | dependency would upgrade | `TRANSITIVE_UPGRADE` | **same stop** |
| N3 installed `%v == local` | reinstall target (no `--needed`) | `TRANSITIVE_REINSTALL` | **same stop** |
| N4 installed `%v < local` | print hides a downgrade warning | `TRANSITIVE_DOWNGRADE` | **same stop** |
| N5 token absent, provider installed | provides resolution returns early | `PROVIDER_ALREADY_INSTALLED` | **same stop** as installed request |
| N6 unseen removal set | conflict/replaces handled only at commit | `UNSEEN_REMOVAL_SET` | blocked; no certification |

## Rule and mechanism

1. `-Sp` prepares the transaction and prints `alpm_trans_get_add` — the **full add-set** (explicit targets plus pulled dependencies), not the requested tokens (pacman source inspection, `AttackAllowedNewPackages.md` counterexample 3; not executed here).
2. Join on every printed `%n`: `pacman -Q <n>` succeeding means the transaction would act on an installed package; `%v` is the sync target version, so the action class needs `alpm_pkg_vercmp` against the local version.
3. Any installed printed name fails the guard's own "every listed package is not installed" clause. Without `-u`, that is a partial-upgrade shape under S047 — the same condition as an installed requested target.
4. Absence is weaker than presence: a satisfied installed dependency is not a target, conflict removals are absent from the print, `--needed` skips only `cmp == 0`, and a clean plan can still precede failure or removal. Print mode also sets `NOLOCK`/`NOCONFLICTS` and masks warnings (`AttackAllowedNewPackages.md` 3–4).
5. `--needed` is no rescue: an installed outdated dependency pulled by a constraint is not up-to-date, so it upgrades; S049 documents "Do not reinstall the targets that are already up-to-date." The observed libinput 1.31.3→1.32.0 upgrade under `--needed` is the explicit-target analogue (both names were requested; the transitive pull itself was not observed).
6. Under `R15-PRINT-FAIL` the guard argv is fixed; adding `--needed`/resolution flags creates a new receipt, not a cleaner pass. Round policy is stricter still: no transaction this round, clean plan or not.

## Evidence

- Guard clause, `/home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-15.md` §7: "proceed only if every listed package is not installed yet (`pacman -Q <name>` fails); otherwise do not install".
- S048 pacman(8), footer Pacman 7.1.0 / 2026-10-15: "Only print the targets instead of performing the actual operation (sync, remove or upgrade)." S047 ArchWiki System maintenance, oldid 885170: "That is why partial upgrades are not supported."
- S049 pacman(8), same URL: `--needed` = "Do not reinstall the targets that are already up-to-date."; `-u` = "Only package versions are used to find outdated packages; replacements are not checked here."
- Retained host snapshot `.ufo/waves/round-15/build/host-snapshot.json` (captured `2026-10-20T07:44:39Z`): 413 pending rows, DB birth `2026-10-18 14:11:00 -0300`; log 2429 `pacman -S --needed --noconfirm libinput libinput-tools`, 2432 `upgraded libinput (1.31.3-1 -> 1.32.0-1)`, 2436 `installed libinput-tools (1.32.0-1)`.
- `corpus/knowledge/update-safety-note.md:199-202`: `-Sp` printed an installed target (`nvidia-utils 610.57.04-1`), so installed names can appear in the add-set; `%s` is not a trustworthy size.
- Consistency: `R15-DEC-ALREADY-INSTALLED-NEWER` uses the identical decision string and transaction flags.

## Machine-readable row (advisory)

```json
{"id":"R15-DEC-NEW-PKG-TRANSITIVE",
 "applies_when":{"requested_names_installed":false,"resolved_add_set_contains_installed_name":true,
   "probe":"pacman -Sp --print-format '%n %v' -- <pkgs>","probe_executed":false},
 "join":"each printed %n: pacman -Q <n>; compare printed %v with local via alpm_pkg_vercmp",
 "classes":["TRANSITIVE_UPGRADE","TRANSITIVE_REINSTALL","TRANSITIVE_DOWNGRADE","PROVIDER_ALREADY_INSTALLED"],
 "decision":"BLOCKED_FOR_AGENT_PACKAGE_ACTION",
 "reason":"PARTIAL_UPGRADE_WOULD_UPGRADE_INSTALLED_DEPENDENCY",
 "same_stop_as":"R15-DEC-ALREADY-INSTALLED-NEWER",
 "transaction_permitted":false,"transaction_started":false,"clean_plan_clears":false,
 "source_ids":["S047","S048","S049"],
 "limits":["guard not executed; transitive pull source-inspected","add-set excludes removals/conflicts and lock",
   "no host health/ABI/causation verdict"]}
```

## Boundaries, limits and tools

- No `-Sp`, `-S`, `pacman` probe, host state query or package/service/sudo/snapper action ran. The snapshot is the only host observation and is stale by construction.
- Transitive dependency upgrade is source-inspection inference, not a measured transaction on this host; no ABI/UI/health/causation claim follows.
- Known blind spots: `%n %v` hides action kind and removals; `replaces` may evade `-Qu` (S049); no lock, so print/commit can race; mirrors/DBs can change between calls; unknown targets are not proof of absence.
- No checker/implementation written; this is advisory documentation, not enforcement, and makes no ordinal or axis claim. No test/build/lint/format/smoke run.
- Tools installed/updated: **none**. Child/labrat dispatch: **none**.
