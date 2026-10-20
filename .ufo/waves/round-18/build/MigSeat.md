# MigSeat — scoped result

Axes: shared-binding consistency; first-error determinism; seat-domain preservation.

[obs] Sandbox clone: `/tmp/tsukuroi-r18-migseat.1ZLu1f`, master at prerequisite `51dd9eeaa305539fa3cfc6ee275978dc18043b79`, origin removed. Sandbox-only commit: `6f0ef768de87bbf9dcba72676b3306d76c187451`. Changed only `tools/check-seat-scope.py` there; patch: `.ufo/waves/round-18/build/patches/MigSeat.patch`. No production lane file changed.
[obs] Initial `git checkout -b master 51dd9ee...` was rejected with `fatal: a branch named 'master' already exists`; `git branch -avv`/`git rev-parse HEAD` showed `master` at the requested prerequisite. Then checked out `master` and removed origin.

[obs] Checker imports shared `RevisionError`/`bind` (`/tmp/tsukuroi-r18-migseat.1ZLu1f/tools/check-seat-scope.py:33`); `collect` catches and maps one `RevisionError` to one existing `Cannot` (`:245-259`). Local REV/BRANCH regexes and binding helpers were removed. CLI syntax handling and worktree/domain evaluation remain; fixture subprocess copies include `_revision.py` (`:228-242`, `:268-311`, `:518-562`). Parser exposes only `--revision`, `--worktree`, `--selftest` (`:213-225`); this assigned checker has no `--registry-from` path.

[inf] Original selftest matrix implied 42 cases (not run pre-edit); post-edit `CHECK_SEAT_SCOPE_SELFTEST: PASS (52 cases, 52 passed, 0 failed)`. Shared result: `REVISION_SELFTEST: PASS (37 cases, 37 passed, 0 failed)`. New assertions cover invalid/missing branches, branch-before-revision and revision-before-missing-branch precedence, CLI single-finding output, and subprocess imports.

[obs] Judge output `artifact://83044:1`: this tool is `bound=true`, `consistent=true`, `shared=true`, `local_rev_regex=0`. Overall intermediate judge exits 1: 1/9 consistent, 8 remaining local regex copies. It also still observes the root-dac single-id probe returning both NOT-LANDED and NOT-PUSHED; that checker is outside the assigned path and remains a blocker for that separate expectation.

[unk] No LSP tool route was available. No tools installed.

Scope: executed=git clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsukuroi-r18-migseat.1ZLu1f; git checkout -b master 51dd9eeaa305539fa3cfc6ee275978dc18043b79 (rejected, branch existed); git checkout master; git remote remove origin; python3 tools/check-seat-scope.py --selftest; python3 tools/_revision.py --selftest; git add tools/check-seat-scope.py && git -c user.name='tsukuroi-shokunin' -c user.email='tsukuroi@shokunin.local' commit -m 'Share revision binding in seat scope checker'; python3 tools/check-revision-binding.py --tools-revision 6f0ef768de87bbf9dcba72676b3306d76c187451