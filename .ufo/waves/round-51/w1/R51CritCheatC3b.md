VERDICT: defect-found

Seat R51CritCheatC3b, item C3-A3 (cheat claim C3 through input paths). Non-counted. Bytes under test: lane revision 2732ee6c06108c031c4d8043239b994e0504eb2f (FREEZE). `tools/check-adjacency-table-r51.py`, `tools/check-adjacency-table-r50.py`, `tools/check-adjacency-anchors.py` are byte-identical at 2732ee6c and at lane HEAD 6d051ef0 (checked with `git show <rev>:<path> | diff`). `tools/_revision.py` was hashed at 2732ee6c only. No lane file was written. Fixtures lived under /fast/scratch/hyaku/tsukuroi-r51/R51CritCheatC3b (removed after receipts were copied). Receipts: `.ufo/waves/round-51/w1/R51CritCheatC3b/` (JSON outputs, commands.txt, wrapper, sitecustomize, sum.py).

## 0. Baseline (real lane bytes)

`python3 tools/check-adjacency-table-r51.py --revision 2732ee6c…` prints PASS, rc 0, `adj_rows 7, bare_ranges 0, anchors_checker_rc 0, quote_at_pin_ok 9, live_quote_ok 9, display_bound_ok 10, digests_bound_ok 10, r50_blind 1`. Receipt: `R51CritCheatC3b/h4.json` (lane R, no override). The counter itself is reproducible at the freeze; the holes below are about what it accepts as input.

## 1. Which file is loaded (answers the item's question)

- The r51 counter loads r50 from ITS OWN directory, not from `--lane`: `_load_r50()` uses `os.path.join(HERE, 'check-adjacency-table-r50.py')` (r51 `tools/check-adjacency-table-r51.py:68-69`); the override child also runs `HERE` (`:222`, `:265`). `--lane` defaults to `dirname(HERE)` (`:302`).
- The anchors checker is run from `--lane`: r50 `checker = os.path.join(lane, CHECKER)` (`tools/check-adjacency-table-r50.py:352-353`).
- Evidence: `a1`=lane counter `--lane <fx>` with a bare locator in F5 → FAIL, `anchors_checker_rc 2`. `a3`= same with a stub checker printing PASS in `<fx>/tools` → `anchors_checker_rc 0`, still FAIL (bare 1): the checker copy alone does not rescue. `a4`= lane counter with a forged `<fx>/tools/check-adjacency-table-r50.py` printing passing legs → still FAIL (`bare_ranges 1`): the lane's r50 is what loads. `a5`= the fixture's own copy of r51 with that forged r50 → **PASS** on the same F5 bytes.

## 2. Does r50/r51 scrub the environment? No.

Every git call is `subprocess.run(['git', …])` with no `env=`: r50 `:84-85, :137, :152, :155`; r51 `:78-79` (inherits PATH, PYTHONPATH, GIT_*). The anchors checker does scrub: `env=clean_env()` (`check-adjacency-anchors.py:264, :459`), and `_revision.py:62-66` defines `clean_env()` = `PATH=/usr/bin:/bin`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`. The r50/r51 counters never import `_revision.py`.

## 3. Per-path results

| path | run | output | PASS printed? | still a measurement of the lane's real bytes? |
|---|---|---|---|---|
| (a) `--lane` = fixture, fixture's copy of r51 with a forged r50 (`a5`) | F5 = fixture commit with `` `../revenger-shokunin/PROVINCE.md:3-5` `` in ADJ-01 ownership cell; not landed in lane | rc 0 `PASS`; `bare_ranges 0`; real checker on F5 gives rc 2 | **yes** | **no**: the r50 legs were the forged copy's output, and the bytes measured are not the lane's F5 (bare 1, checker rc 2 in `a1`) |
| (a) forged checker only (`a3`) | `--lane` fixture | FAIL (`bare 1`), rc 0 | no | the checker leg alone is insufficient; r50 legs still real |
| (a) forged r50 loaded from lane (`a4`) | `--lane` fixture | FAIL | no | confirms r50 comes from the counter's own dir |
| (b) symlinked `--siblings-root` (`g1`) | symlink → fleet root | rc 3 OVERRIDE-NOT-MEASURED | no | yes (blocked). `g2` (trailing-slash spelling) also rc 3. `g3` with `--control` prints CONTROL-PASS, never PASS |
| (c) `--revision` fixture-only commit with `--lane` fixture (`b1`) | F6 = benign commit absent from lane; fixture's refs/heads/master and refs/remotes/origin/master set to F6 | rc 0 `PASS`, same JSON shape as lane (`b0`), revision differs | **yes** | **no**: `--lane` is not in the override guard (`r51:206-207`), and the PASS JSON names no lane path, branch tip or ancestry |
| (d) `PATH` prepended with a `git` wrapper that substitutes honest R bytes for F5 (`d1`) | F5 real bytes (`d0`) FAIL, bare 1 | rc 0 `PASS` | **yes** | **no**: the measured PROVINCE is R's bytes, not F5's. Checker unaffected (clean env) |
| (d) `PYTHONPATH` with a `sitecustomize.py` patching `subprocess.run` (`e1`; `e2` = same path, no forge env, FAIL) | as above | rc 0 `PASS` | **yes** | **no**, same as `d1`. Child r50 also picks it up (env inherited) |
| (d) `GIT_DIR` = fixture `.git` (`c1`, `c2`) | F6 | FAIL, `quote_at_pin_ok 0`, checker `CANNOT_EVALUATE` | no | fail-closed here: sibling pins do not resolve in fixture objects. But see the sibling primitive below |
| (d) `GIT_DIR` checker scrub probe | lane checker, F6 | identical `E-REVISION-INVALID` / CANNOT_EVALUATE with and without `GIT_DIR` | n/a | yes: the checker's clean env ignores GIT_DIR |
| (d) `GIT_CONFIG_*` textconv driver via `core.attributesFile` on the real lane | `git show` and `cat-file blob` | return the real bytes; only `git show --textconv` runs the driver | n/a | **not a hole** for the counter's reads (default `show` is not textconv-ed) |
| (d) replace refs | fixture `git replace R F5` (`i1`) | `show` returns F5 bytes → FAIL bare 1 | n/a | honoured by `show`; the lane has **0** replace refs (`for-each-ref refs/replace` empty). Reaching a repo with replace refs via GIT_DIR is [INFERENCE], not run |
| (e) `--no-base-check` with an unreachable base (`e2`) | fresh repo whose single root commit carries lane R's tree; BASE `c0ad548a` absent | rc 0 `PASS` on a lineage-free commit (`e1` without the flag: FAIL "base unreadable") | **yes** | the bytes are R's, but nothing binds the revision to the lane's history: `cat-file -e` checks existence, not ancestry (`r51:213`, `r50:233`), and the child always receives `--no-base-check` (`r51:223`) |
| (e) `--no-base-check` alone on the real lane (`h4`) | lane R | PASS, not flagged as an override | yes | yes (guard gap only: `a.no_base_check` is not in `overridden`, `r51:206-207`) |

Override guard otherwise holds: `--province-file`, `--skip-anchors-check` (`h1`, `h2`) → rc 3 OVERRIDE-NOT-MEASURED; `--control` on F5 (`h3`) → CONTROL-FAIL, never PASS.

## 4. Sibling-read primitive (not a full forgery)

With `GIT_DIR` set to a fixture, `git -C ../revenger-shokunin show <fixture commit>:PROVINCE.md` returns the fixture's bytes (prints `# FORGED SIBLING`); without the env it is `fatal`. So r50's sibling reads (`r50:137, :152, :155`) can be redirected to fixture objects. I did NOT build a complete quote-forgery chain (fixture sibling pins + forged checker copy + live tip). That chain is [INFERENCE] until run.

## 5. Holes and the smallest rule per hole

- **H1 `--lane` unbound (a, c).** Rule: add `a.lane != CANON_LANE` to `overridden` (`r51:206`), where `CANON_LANE` is the canonical lane path; bind the revision with `_revision.bind(CANON_LANE, rev, 'master')` and print `lane`, bound `sha`, `master_tip`, `origin_tip` in the JSON. Run the anchors checker from `CANON_LANE`, not `--lane` (`r50:352`).
- **H2 loaded copies are unfrozen (a iii–v).** `FROZEN-hashes.txt` pins only the r51 counter (`3d09a8e9…`). Not pinned: r50 `d571adc9562b…`, anchors checker `a4f500ef680d…`, `_revision.py` `fc861ec8a4f2…` (all computed from 2732ee6c). Rule: load r50 and the checker only from `CANON_LANE`; add those three hashes to `FROZEN-hashes.txt`; refuse (exit 2) on mismatch before measuring.
- **H3 environment inherited (d).** Rule: every `subprocess.run(['git', …])` in r50 and r51 becomes `env=clean_env()` with `/usr/bin/git`; add `GIT_NO_REPLACE_OBJECTS=1` to that env; the child is run as `[sys.executable, '-I', …]`; the counter exits CANNOT (rc 2) if `PYTHONPATH` or any `GIT_*` is set without `--control`.
- **H4 base is existence, not ancestry; child always skips it (e).** Rule: replace `cat-file -e BASE` (`r51:213`, `r50:233`) with `merge-base --is-ancestor BASE rev` in `CANON_LANE`; delete `--no-base-check` from the child call (`r51:223`) and from the public CLI (`r51:306`), or make it control-only.
- **H5 guard list incomplete (h4); temp files contradict docstring.** Rule: add `a.no_base_check` to `overridden` until H4 lands; r51 creates `NamedTemporaryFile` in `TMPDIR` (`r51:249, :252`) while its docstring says "Writes nothing". Either correct the docstring or pass a scratch dir in.

Keep as is: the symlink/`--siblings-root` string comparison (`r51:206-207`): (b) is blocked and only `--control` gets through, with CONTROL-PASS. The checker's `clean_env()` (`check-adjacency-anchors.py:264, :459`): this is the one leg that resisted GIT_DIR; extend the same scrub to r50/r51.

Suggested controls for the w2 battery (each must FAIL or CONTROL-*, never PASS, after the fix): fixture lane with fixture-only landing (`b1`); forged loader copy (`a5`); PATH wrapper (`d1`); PYTHONPATH shim (`e1`); unrelated root with `--no-base-check` (`e2`).

## 6. What I did not run

- No complete sibling-forgery chain (GIT_DIR + fixture sibling pins + forged checker copy). Only the read primitive (§4).
- GIT_REPLACE_REF_BASE and GIT_OBJECT_DIRECTORY/ALTERNATES: not run. Replace refs tested only inside a fixture repo.
- No selftest, scorer or battery run (out of item scope).
- Checked `_revision.py` only at 2732ee6c, not at HEAD.

## 7. Tooling

None installed. No pacman, no uv, no npm. No lane, sibling or fleet-root write. Scratch directory removed after receipts were copied.
