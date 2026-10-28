VERDICT: supports

Independent walk of `PROVINCE.md` at freeze `55c07cd3f8bff2e12117c34d57b4c618de74d85c` and base `6256760d1382ce4ce20fcba830d4b2912cfbf12b`. Mapping was built from those two blobs before the counter was opened. The counter's `BARE` pattern was read only afterwards, to see which nine strings the "9 bare ranges" claim means. The counter script was not executed. Sibling blobs were not re-read; quote specificity is judged from the quote cell alone.

## ADJ-01..07 ownership cells (freeze)

Source: `git show 55c07cd3f8bff2e12117c34d57b4c618de74d85c:PROVINCE.md` lines 46-52. Column is **Ownership source**.

| ID | Ownership cell |
|---|---|
| ADJ-01 | `OUT-002` |
| ADJ-02 | `OUT-003` |
| ADJ-03 | `OUT-004` |
| ADJ-04 | `OUT-005` |
| ADJ-05 | `OUT-006`, `OUT-007` |
| ADJ-06 | `OUT-008`, `OUT-009` |
| ADJ-07 | `OUT-010` |

No `*.md:N` token remains in those seven cells.

## OUT rows and ADJ class (freeze, lines 121-130)

| Anchor | ADJ row cell | Quote |
|---|---|---|
| OUT-001 | Core | independently labeled user/system journals, plus cgroup `memory.events` and the explicit same-boot journal window after a retained anchor; |
| OUT-002 | ADJ-01 | `GET /v1/models` vs `--alias` vs the configured model id |
| OUT-003 | ADJ-02 | **Domain:** secrets & vault ops — the-janitor flows, credential hygiene evidence |
| OUT-004 | ADJ-03 | **Owns (surfaces):** `~/.config/hypr/` (hyprland.conf, keybinds, rules, |
| OUT-005 | ADJ-04 | kill/OOM-related catalog-ID records and signal-11 coredump records |
| OUT-006 | ADJ-05 | **Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime |
| OUT-007 | ADJ-05 | **Refuses:** dispatch and orchestration mechanism (→ kumitate); OS package, |
| OUT-008 | ADJ-06 | **Domain:** reverse engineering of shipped artifacts with REA on this Linux |
| OUT-009 | ADJ-06 | Owns: reverse engineering of shipped artifacts |
| OUT-010 | ADJ-07 | **Owns:** the method, documented from the fleet's existing gates |

## Mapping (ADJ class → OUT ids whose class cell equals that class)

| ADJ class | Anchors with matching class cell | ≥1 match |
|---|---|---|
| ADJ-01 | OUT-002 | yes |
| ADJ-02 | OUT-003 | yes |
| ADJ-03 | OUT-004 | yes |
| ADJ-04 | OUT-005 | yes |
| ADJ-05 | OUT-006, OUT-007 | yes |
| ADJ-06 | OUT-008, OUT-009 | yes |
| ADJ-07 | OUT-010 | yes |

Each ownership cell names exactly those anchors and no others. OUT-001 is class Core and is not named by any ADJ-01..07 ownership cell. Every ADJ class has at least one anchor whose class matches.

## Nine bare ranges at base

Command (ownership cells only; pattern is the counter's `BARE` = `[A-Za-z0-9_.-]+\.md:\d+(?:-\d+)?`):

```
python3 -c '… git show 6256760d1382ce4ce20fcba830d4b2912cfbf12b:PROVINCE.md …'
```

Observed `bare_n 9`, `whole-file BARE 15`. The nine ownership-cell match strings, in order:

1. `PROVINCE.md:3-24` (line 46, ADJ-01)
2. `PROVINCE.md:3-6` (line 47, ADJ-02)
3. `PROVINCE.md:3-16` (line 48, ADJ-03)
4. `PROVINCE.md:3-16` (line 49, ADJ-04)
5. `PROVINCE.md:3-6` (line 50, ADJ-05)
6. `PROVINCE.md:12-16` (line 50, ADJ-05)
7. `PROVINCE.md:3-6` (line 51, ADJ-06)
8. `PROVINCE.md:3-7` (line 51, ADJ-06)
9. `PROVINCE.md:3-18` (line 52, ADJ-07)

Full locator strings on those same cells (regex `\.\./[A-Za-z0-9_.-]+/PROVINCE\.md:[0-9][0-9,\-]*`), also nine:

1. `../kama-shokunin/PROVINCE.md:3-24`
2. `../kagi-shokunin/PROVINCE.md:3-6,10-17,32-34,54`
3. `../mado-shokunin/PROVINCE.md:3-16`
4. `../mori-shokunin/PROVINCE.md:3-16`
5. `../kumitate-shokunin/PROVINCE.md:3-6`
6. `../mori-shokunin/PROVINCE.md:12-16`
7. `../kaidoku-shokunin/PROVINCE.md:3-6,88-100`
8. `../revenger-shokunin/PROVINCE.md:3-7,19-25`
9. `../tameshi-shokunin/PROVINCE.md:3-18`

The claim "9 bare ranges at base" holds for ownership cells. It does not hold for the whole file: the same `BARE` regex returns 15 hits (the nine above, plus `PROVINCE.md:6-16` at line 33, `PROVINCE.md:26` at line 166, `PROVINCE.md:66` at line 185, `SKILL.md:1097-1107` at line 197, `README.md:243` at line 260, `README.md:315` at line 285). An independent `../…/PROVINCE.md:` scan of the whole base file, done before opening the counter, found 11 locators (the nine, plus lines 33 and 166).

`BARE` stops at the first `N` or `N-M`. Comma tails inside three cells are not extra hits: kagi `10-17`, `32-34`, `54`; kaidoku `88-100`; revenger `19-25`. Splitting those tails yields 14 range atoms inside the 9 locator strings. That is a property of the regex, not a missing locator. Freeze ownership cells: `BARE` count 0.

## Weakest anchor

**OUT-010** (ADJ-07). Quote: "**Owns:** the method, documented from the fleet's existing gates" (`PROVINCE.md:130` at the freeze). The ADJ-07 trigger is "A census blind spot raises a reusable verification/mutation-testing question" (`PROVINCE.md:52`). The quote shares no content word with that trigger: it does not say census, verification, mutation, or testing. "the method" and "gates" name a role only after the proposition supplies "verification/mutation-testing". Every other ADJ-linked quote names the class's distinctive object in the quote itself (`model id`, `credential`, `hyprland.conf`/`keybinds`, `kill/OOM`/`signal-11`, `task/hub`/`orchestration`/`dispatch`, `reverse engineering of shipped artifacts`).

Runner-up, not chosen: OUT-004's quote is a cut-off Hyprland path and never says rendering, menu, or idle, but `hyprland.conf` and `keybinds` still pick out ADJ-03's desktop-configuration surface. OUT-003's quote is a secrets/vault banner and does not say permission or auth-flow, but it does say `credential`.

## Not done

Did not run `tools/check-adjacency-table-r49.py`. Did not check quotes against pinned sibling blobs, word-count ≤25, or registry sha256.
