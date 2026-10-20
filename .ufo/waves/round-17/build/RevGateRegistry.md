# RevGateRegistry — SKILL.md gate-registry review (round 17)

[obs] SKILL.md read at baseline `6923fe0` (file unmodified); tools are mid-edit in the
worktree. `root-dac`/`measure` still admit `HEAD|4-64 hex`; locator, section-citations and
source-scope already admit only `7-64 hex` + `--branch`.

## A. Existing rows — edit in place (exact current fragments)

| Line | Exact current text | Required |
|---|---|---|
| 1737 | `--revision <commit>`; `2 could-not-evaluate` | `--revision <7–64 hex>` + `--branch <name>` (default `master`); exit 2 adds `E-REVISION-INVALID`, `E-REVISION-NOT-LANDED`, `E-REVISION-NOT-PUSHED`; JSON adds `branch`, `branch_tip`. Tool still admits "HEAD or 4-64 hex" (`check-root-dac-correction.py:27`). |
| 1778 | `--revision <commit>`; `2 could-not-evaluate (CLI/read/parse/internal errors)`; `selftest in memory without network` | Same entry/branch change and two codes. Tool is already hex-only (`:27`); selftest now uses a mktemp git sandbox (`:8`), so "in memory" is false. |
| 1818 | (REV = `HEAD` or 4–64 hex); verdict 2 lists "`E-CLI`, `E-REVISION-INVALID`, read/git/parse/internal"; `(21 fixture cases + 2 CLI cases = 23; exit 0 pass, 1 fail)`; `selftest in memory` | `REV = 7–64 hex` + `--branch`; add both NOT-* codes; replace the stale 23 tally with the landed gate's printed tally; selftest is "in-memory fixtures plus a throwaway mktemp git repo" (`:11`). |
| 1819 | (REV = `HEAD` or 4–64 hex); exit-2 clause "malformed JSON, schema/digest/observation mismatch, missing record or snapshot, `E-CLI`" | Same hex/branch change; add both NOT-* codes. Tool still admits "HEAD or 4-64 hex" (`:38`). |
| 1857 | `--revision <commit>`; `2 could-not-evaluate: CLI/git/read/parse errors`; "independent attack vectors `.ufo/waves/round-16/build/frozen-cases.json`" | `--revision <7–64 hex> [--branch <name>]`; add both NOT-* codes; replace the frozen-cases pin — that JSON is superseded by the shipped 43-case selftest (`frozen-cases.SUPERSEDED.md:1-8`). |

## B. Prose that must change

`SKILL.md:1825-1826`: exact current text "In tree mode it reports
`revision: worktree`; a comparable verdict names a commit via `--revision`." Required: state
that `--revision` accepts only 7–64 hex and must be an ancestor of `refs/heads/<branch>`
(and `refs/remotes/origin/<branch>` when present); only the locator gate has tree mode.
The Round-17 section must also say these five edited rows supersede their earlier cells,
otherwise two contradictory registries stand.

## C. New rows the round adds (Round-17 table; none of the five tools exists yet)

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope |
|---|---|---|---|---|---|---|
| boot-chain | gate | `python tools/check-boot-chain.py --revision <7–64 hex> [--branch master]` | 0 clean; 1 findings incl `BOOTCHAIN-MISSING`; 2 binding codes | `--selftest` (≥20 cases; record the printed tally) | schema `tsukuroi-boot-chain-v1`; capture `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt`; baseline `6923fe0…`; entry ids `linux`, `linux-lts`, `snapshot-2/linux`, `snapshot-2/linux-lts`, `snapshot-1/linux`, `efi-fallback`; five-verdict vocabulary; output `verdicted_kernel_entries` (C1 0→5) | none |
| freshness-r17 | gate | `python tools/check-freshness-r17.py --revision <7–64 hex> [--registry-from <7–64 hex>] [--branch master]` | 0 clean; 1 findings incl `STALE-UNFLAGGED`; 2 binding codes | `--selftest` (≥18) | schema `tsukuroi-freshness-recheck-v1`; registry `corpus/knowledge/freshness-recheck-r17.json`; record fields `id/path/baseline_quote/stale_reason/observed_now/capture_ref/capture_quote/notice_heading`; output `resolved_records` (C2) | none |
| revision-binding | measure | `python tools/check-revision-binding.py --tools-revision <7–64 hex>` | 0 iff `bound_tools` 5/5; 1 otherwise; 2 could-not-evaluate | `--selftest` with stub tools | five tool paths (locator, root-dac, section-citations, source-scope, measure); output `tools_revision`, `bound_tools`, `total:5`, `per_tool[]`; mktemp clone + detached unlanded commit | clone/`git show` reads only |
| seat-scope | gate | `python tools/check-seat-scope.py --revision <7–64 hex> [--branch master]` or `--worktree` | 0 clean; 1 `SCOPE-UNDECLARED`/`SCOPE-EXEC-UNAUTHORIZED`/`SCOPE-REPORT-MISSING`; 2 binding codes | `--selftest` (≥10) | QUALITY24 (`corpus/QUALITY.md:33`); demo `.ufo/waves/round-16/build` at `f871697aa0a8ed180771e62d99e3b9559fd5efd1` → exit 1, 64 `SCOPE-UNDECLARED` (commit object exists [obs]) | none |
| recheck-commands | gate | `python tools/check-recheck-commands.py --paths <knowledge files> --revision <7–64 hex> [--forbid <bin,…>]` | 0 clean/`RESOLVED`; 1 `RECHECK-FORBIDDEN-INVOCATION`; 2 binding codes | `--selftest` (≥10) | default forbid `pacman,checkupdates,yay,paru,mkinitcpio,limine-update`; resolution heading `## R17-RECHECK — steer-safe procedure`; pinned defect `corpus/knowledge/initramfs-v42-sysroot-recovery.md:3` (`pacman -Q mkinitcpio limine-mkinitcpio-hook plymouth`) | none |

## D. Could not verify

- Exact selftest tallies and finding ids: must be read from each landed tool, not the
  planned minimums. [unk]
- `freshness-recheck-r17.json` absent at review, so `resolved_records` N is unknown. [obs]
- `root-dac`/`measure` conversions not yet in the worktree. [obs]
- Line numbers shift after the Round-17 section is appended; cite headings, not numbers.

[inf] Registry edits are documentation-only and authorize no package, service or boot action.
[inf] Deviation: this seat used read-only bash/git/grep inspection, so the Scope line below
records it rather than claiming `none` (QUALITY24: record deviations, never approve them).

Scope: executed=ls,git-status,git-branch,git-rev-parse,git-for-each-ref,git-cat-file,sed,grep,cat,python3-json-read
