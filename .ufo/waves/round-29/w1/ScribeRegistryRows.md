Done: the draft round-29 registry section is written at
`.ufo/waves/round-29/w1/ScribeRegistryRows/draft.md` and it passes
`tools/check-registry-coverage.py` only when it carries all 33 earlier rows verbatim plus the
two new rows; a two-row section fails that gate with 33 missing rows.

1. [obs] At the attacked revision the coverage gate is already red for exactly the two tools
   this ticket is about. Command (from the sandbox clone
   /fast/scratch/hyaku/tsukuroi-r29/ScribeRegistryRows/repo, inherited GIT_* unset):
   `python3 tools/check-registry-coverage.py --revision 81a061a67466c5e1be812814a895a4b5ed89b4ff --branch master`
   exited 1 with
   `"counts":{"findings":2,"missing":2,"registered":33,"rows_total":33,"tools_total":35}` and
   the two findings are `REGISTRY-ROW-MISSING` at `tools/check-owed-statements-r29.py` and
   `tools/probe-git-env-leak.py`. The tools/ inventory at that revision is 35 regular files
   (`git ls-tree -r --name-only <rev> -- tools/`, `__pycache__` excluded).

2. [obs] The gate requires exactly one operative row per regular tools/ file and treats every
   other tools/ file as missing (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-registry-coverage.py:287-294`).
   A round-29 table holding only the two new rows under the correct highest heading makes the
   gate select that table and report 33 missing rows. Fixture branch `fx-partial` in the clone,
   commit `1dff10577f7bbcd8710347f6cc13920cdc452a79`, same command with `--branch fx-partial`:
   exit 1, `"findings":33,"missing":33,"registered":2,"rows_total":2`.

3. [obs] The heading must keep the exact form `## Gate and probe registry — round<N> superseding
   current rows`; the gate's selector is that literal regex
   (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-registry-coverage.py:23-24`).
   A section headed `## Gate and probe registry — round29` (the short form this ticket names) is
   invisible to the selector: round28 stays operative and both new tools stay missing. Fixture
   branch `fx-bare`, commit `e95769afe6787595f918b2c14c5c7f8974726431`: exit 1,
   `"findings":2,"missing":2,"registered":33,"rows_total":33`, the same two
   `REGISTRY-ROW-MISSING` findings as in finding 1. The draft therefore uses the superseding
   form and states this trap in its preamble.

4. [obs] The drafted section (round28's 33 rows byte-for-byte, header and separator included,
   plus the two new rows appended, under `## Gate and probe registry — round29 superseding current
   rows`) passes structurally. Fixture branch `r29fixture`, commit
   `1191087a31fc24bdcdb616f95e5ce968eafc881c` (SKILL.md blob sha256
   `a1e9427b294e22cb58d06572094975745c55931a4549a76f1ccdd86e5af1a081`): the gate printed
   `"counts":{"findings":0,"missing":0,"registered":35,"rows_total":35,"tools_total":35}` and
   `"status":"PASS"`, exit 0; it also passes with `--audit-live-map`
   (`"audit_live_map_errors":0`, findings 0, exit 0). Byte equality of the 33 carried rows and
   of the two appended rows against the committed round28 table was checked element by element
   in memory before the fixture commit.

5. [obs] The two rows and the source of every cell. `owed-statements-r29` is kind gate, entry
   `python3 tools/check-owed-statements-r29.py --revision <REV> [--lane <repo>]`, verdict map
   0 marked / 1 unmarked or invalid / 2 could-not-evaluate, self-test `none: no self-test mode`,
   pinned cell the twelve frozen anchors O01-O12 with marker rules M1-M7 at base `16e9ab2a`,
   write scope committed Git reads only, owner `tsukuroi`; these come from
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-owed-statements-r29.py:1-36`
   (docstring) and `:204-207` (only `--revision` and `--lane` exist, so there is no self-test
   mode). `git-env-leak` is kind probe, entry
   `python3 tools/probe-git-env-leak.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]`,
   verdict map 0 no leak / 1 one target leaks / 2 harness error, self-test `none: no self-test
   mode`, pinned cell the eight frozen write-capable targets at base `16e9ab2a` with the canary
   fingerprint and exit-code-divergence rule, write scope private mkdtemp scratch with canary
   commits confined there, owner `tsukuroi`; these come from
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/probe-git-env-leak.py:1-30`
   (docstring) and `:96-99` (no `--selftest` argument).

6. [obs] Both rows satisfy every per-row rule the gate applies: eight cells; kind in
   gate/probe; the gate row publishes codes 0, 1 and 2 while the probe row publishes 0 and 2
   (`check-registry-coverage.py:243-271`); exactly one `tools/` path per row, so no
   `REGISTRY-ROW-AMBIGUOUS` and no `REGISTRY-ROW-ORPHAN`; and no `--self-?test` token in either
   self-test cell, so no `REGISTRY-SELFTEST-UNRESOLVED` lookup is attempted
   (`check-registry-coverage.py:277-287`). The phrase used is `self-test` with a single hyphen,
   which the flag regex does not match.

7. [inf] The PASS in finding 4 is structural coverage only. It shows one row per tool and
   well-formed cells; it does not show that the pinned-value prose in either row is true, nor
   that the two tools count what their docstrings claim. I did not run either new tool and did
   not re-derive any pinned value; the pinned cells are transcribed from the docstrings cited in
   finding 5.

8. [unk] Whether the integrator pastes the section verbatim into `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md`
   is outside this seat: I wrote no lane file. If the section is edited before landing, the
   counts in finding 4 no longer describe the landed bytes.

9. [obs] The draft is 21297 bytes at
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ScribeRegistryRows/draft.md`,
   sha256 `97282252469e1c78cd2786498d8ba3bfb4701c614bbea2631c9ef3eddfb2cf02`. Its embedded
   section is 18068 bytes, sha256
   `0480439a4e9b481a9e7689d6fa0c36104fbe084fe9aa8b4e9337a92bf9b560f3`, parses to 35 data rows
   with `host-census` first and `git-env-leak` last, and is byte-identical to the section tested
   in finding 4.

Scope: read=tools/check-registry-coverage.py, tools/check-owed-statements-r29.py, tools/probe-git-env-leak.py, tools/_revision.py, SKILL.md lines 2488-2531 and the gate's parsed rows, git ls-tree/ls-files metadata at 81a061a67466c5e1be812814a895a4b5ed89b4ff; wrote=.ufo/waves/round-29/w1/ScribeRegistryRows/draft.md, .ufo/waves/round-29/w1/ScribeRegistryRows.md, sandbox fixtures under /fast/scratch/hyaku/tsukuroi-r29/ScribeRegistryRows/repo; executed=git clone/checkout and read-only git reads in the lane, fixture commits in the sandbox clone with inherited GIT_* unset, python3 tools/check-registry-coverage.py --revision <REV> --branch <name> [--audit-live-map] five times
Model: opencode-go/deepseek-v4.1-flash
Installs: none
