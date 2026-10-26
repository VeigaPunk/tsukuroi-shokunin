VERDICT: supports

# C2ExecRerun — item C2-16 (C2 after re-run)

Executed from the lane worktree at `f951f288483c1af0cef4afd458488b84cf7a2165` (lane `master` tip at dispatch).
Nothing in the lane was written except this report and the receipts directory `.ufo/waves/round-40/w1/C2ExecRerun/`.
No package/service/hook/sysfs/mount/boot change; no sudo; no git write in the lane; no signal to any process.

## 1. Tool bytes (claim: sha256 `d4a2bb94…7d9d`, frozen at `a447b67`)

```
$ sha256sum tools/check-exec-environment-r40.py
d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d  tools/check-exec-environment-r40.py
$ for r in a447b67… 53b294a2… bf23805… f951f28…; do printf '%s  ' $r; git show $r:tools/check-exec-environment-r40.py | sha256sum; done
a447b67b2502bae1e96fda341ae5ad32243ae524  d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d
bf2380503b8e4a5d33162026854b0b7b66d18b86  d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d
f951f288483c1af0cef4afd458488b84cf7a2165  d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d
$ git diff --stat a447b67 f951f28 -- tools/check-exec-environment-r40.py tools/_revision.py
(empty)
$ git log -1 --format='%H %ad %s' --date=iso-strict a447b67
a447b67… 2026-10-26T03:47:27-03:00 round-40: freeze C1/C2 counters, pinned sources, host capture, registry rows
```
Working-tree bytes = bytes at the declared freeze commit `a447b67` = bytes at the C2 implementation commit `bf23805` = bytes at the lane tip `f951f28`. The tool that ran is the tool that was frozen; `_revision.py` is unchanged over the same span. The after receipt itself records `tool_sha256: d4a2bb94…7d9d`, `tool_revision: a447b67…`, `argv: [tools/check-exec-environment-r40.py, --revision, bf23805…]` (`.ufo/waves/round-40/after/c2-after-bf23805.jsonl:1`).

## 2. Re-run at the three revisions

```
$ python3 tools/check-exec-environment-r40.py --revision bf23805…   -> exit 0, PASS
$ python3 tools/check-exec-environment-r40.py --revision f951f28…   -> exit 0, PASS
$ python3 tools/check-exec-environment-r40.py --revision 53b294a2…   -> exit 1, FAIL
```
Receipts: `w1/C2ExecRerun/exec-env-bf23805….json`, `exec-env-f951f28….json`, `exec-env-53b294a2….json` (stdout; both stderr files empty).
All three: `rules_verified=8, duplicate_rows=0, duplicate_headings=0, source_ok=1, counts_ok=2, novelty_base_hits=0`; derived `EX1=/`, `EX2=stdout+stderr: one socket; stdin: second socket`, `EX3=SHLVL=1 BASH_ENV=unset umask=0022`, `EX4=/usr/bin/bash` (`EX4_default=/bin/sh`), `EX5=tmp/alpm_XXXXXX/.INSTALL`, `EX6=sorted, deduplicated, one per line`, `EX7=could not satisfy dependencies`, `EX8=NoExtract`; host `hooks_total=69, hooks_needstargets=14, libalpm_usr_bin_bash=1`; all eight novelty tokens `0`.
Base differs exactly as declared: `entry_present=false, rules_verified=0, source_ok=0, counts_ok=0, result=FAIL, exit 1`.
The entry survives to the lane tip unchanged: `sha256(git show bf23805:corpus/knowledge/pacman-exec-environment-r40.md)` = `sha256(git show f951f28:…)` = `2230ccaf4037ccfcb8628b97f15fcff9eca86f9e5e37bee1c5392712ce21c9ef`; `git diff --stat bf23805 f951f28 -- corpus/SOURCES.md` is empty.

## 3. Field-by-field comparison with after/before receipts

Recursive diff of the embedded counter record (lines 2..n-1 of each `.jsonl`) against my three runs:
- `after/c2-after-bf23805.jsonl` vs my `bf23805` run: **1 differing field** — `.branch_tip` receipt `bf23805…` vs mine `f951f28…` (expected: the lane advanced after the receipt was taken). Every other field identical, including each of the 8 `rules[*].verified / reasons` lists (all `verified=true`, `reasons=[]`).
- `before/c2-before.jsonl` vs my `53b294a2` run: **1 differing field** — `.branch_tip`, same reason. `entry_present=false`, `rules={}`, `result=FAIL`, `exit=1` identical.
Both receipt headers carry `tool_sha256 d4a2bb94…7d9d`, `tool_revision a447b67…`, and matching `argv`; `receipt_end.exit_code` 0 (after) and 1 (before) match my observed exits.
Determinism: three runs at `bf23805` are byte-identical (`b68f7b08…440e`, `determinism-run2/3-bf23805.json`).

## 4. Independent checks of the values the counter derives (not taken on trust)

- Frozen snapshots: `sha256sum -c .ufo/waves/round-40/frozen/src/SHA256SUMS` → all six `OK`; `sha256sum -c .ufo/waves/round-40/frozen/hostcap/MANIFEST.sha256` → all three `OK`. Digests equal `SRC_SHA`/`CAP_MANIFEST_SHA` in `tools/check-exec-environment-r40.py:76-83`.
- Re-derived by hand from the pinned sources: `util.c:683 chdir("/")` (EX1), `util.c:666 dup2(child2parent_pipefd[HEAD], 2)` + `util.c:667 dup2(parent2child_pipefd[TAIL], 0)` + parent-side `close(parent2child_pipefd[HEAD])` at `util.c:722-725` (EX2), `util.c:692 setenv("SHLVL","1",0)` / `:694 unsetenv("BASH_ENV")` / `:695 umask(0022)` / `:698 execv` (EX3), `PKGBUILD:115 -Dscriptlet-shell=/usr/bin/bash` with `meson_options.txt:17 value : '/bin/sh'` (EX4), `trans.c:361-377 tmp/alpm_XXXXXX` + `/.INSTALL` + `01777` + `rmdir(tmpdir)` at `:417` (EX5), `hook.c:521 alpm_list_msort(…, strcmp)` + `:524 _alpm_strlist_dedup` + `:476 buf[len++] = '\n'` (EX6), `hook.c:513-515 "could not satisfy dependencies"` and `running` logged at `hook.c:653` **before** `_alpm_run_hook` at `:660` (EX7), `hook.c:271 alpm_option_match_noextract(…) == 0` with no `noupgrade` token in the file (EX8). Modulo the excerpted quotes this reproduces the counter's `derived` map exactly.
- Host values independently: `hooks-needstargets.tsv` has 69 rows, 14 with `needs_targets=1`; `libalpm-shell-strings.txt:1277` is `/usr/bin/bash`; `capture-meta.txt:2-4` records `pacman 7.1.0.r9.g54d9411-3` and `/usr/lib/libalpm.so.16.0.1` owned by that package — and on this host `pacman -Q pacman` → `7.1.0.r9.g54d9411-3`, `ls -l /usr/lib/libalpm.so.16.0.1` present. Entry EX6/EX4 host cells carry `14 of 69 effective hook files` and `/usr/lib/libalpm.so.16.0.1`.
- Registry: at `f951f28`, rows `S219`–`S224` are `code`/`docs`, `S225` `own-work`, all `status=mined`, `opened=2026-10-26`, `used_by=corpus/knowledge/pacman-exec-environment-r40.md`; none exist at the base `53b294a2` (`grep -c` = 0 there, and the entry file is absent at base).
- Quotes: an independently written checker extracted every curly quote from each EX row and located it inside the cited frozen lines — all eight found at the cited ranges (`util.c:677-687`, `util.c:659-668`, `util.c:688-698`, `PKGBUILD:113-115`, `trans.c:360-377`, `hook.c:519-526`, `hook.c:507-517`, `hook.c:258-279`); quote lengths 6–11 words; rule cells 35–59 words, all within the 4–25-word quote / ≥12-word rule constraints.
- I also read the eight rule cells against the source text: each states what the code does (order of `running` vs `Depends`, stdin/umask/SHLVL, scriptlet staging and cleanup warnings, NeedsTargets sort/dedup/one-per-line, NoExtract skip with NoUpgrade ignored). No contradiction found in the entry itself.

## 5. Non-vacuity of the PASS (mutations in a throwaway clone)

`D=$(mktemp -d /fast/scratch/hyaku/tsukuroi-r40/C2ExecRerun/fx2.XXXXXX); git clone -q --shared <lane> "$D"; git -C "$D" remote remove origin` (toplevel verified `= $D`, identity `fixture@shokunin.local`), variants committed on the clone's `master`, counter run as `--repo "$D" --revision <clone sha>`:

| tag | mutation | observed |
|---|---|---|
| M0 | none (unmutated clone at `f951f28`) | exit 0, PASS, 8/8 — output byte-identical to my lane `f951f28` run (`be4e0e9f…c7a`) |
| M1 | EX1 rule: "starts in **no** working directory … parent **never** changes" | exit 1, FAIL, 7/8, reason `rule carries negation word 'no'` |
| M2 | EX5 value cell `.INSTALL` → `.INSTALL.sh` | exit 1, FAIL, 7/8, reason `value … != derived 'tmp/alpm_XXXXXX/.INSTALL'` |
| M3 | one byte appended to `frozen/src/util.c` (manifest untouched) | exit 2, `frozen input: snapshot util.c sha256 be93cf49… != 381618b6…` |
| M4 | one byte changed in `frozen/hostcap/hooks-needstargets.tsv` | exit 2, `frozen input: capture file hooks-needstargets.tsv mismatch` |
| M5 | EX7 order reversed: "`running …` log line is written **after** the hook's `Depends` are checked" | **exit 0, PASS, 8/8** |
| M6 | EX2 streams split: "stdout and stderr are **split onto separate sockets** … the two streams arrive apart" | **exit 0, PASS, 8/8** |

Receipts `w1/C2ExecRerun/mut2-M0..M4*.json`, `mut3-M5*.json`, `mut3-M6*.json`.

Finding (residual, counter-side — the entry is not affected): the frozen predicate tests token presence, a negation-word list, length and quote presence; it cannot distinguish a rule's **orientation/partition**. M5 and M6 state the opposite of `hook.c:653,660` and `util.c:665-666` yet verify 8/8, because "after", "split" and "apart" are not in `NEG` (`tools/check-exec-environment-r40.py:106`) and the frozen tokens survive the reversal. So a PASS attests "rule cell carries the propositions and no negation word", not "the rule cell is true"; the truth of EX1–EX8 rests on the reading, which I re-did above and found correct. If the declaration is to be read as "the counter proves the rule is right", that reading is falsified; as written ("carries the rule … negative facts and conditions are worded affirmatively") it holds. Optional wording for the counter docstring / scorecard, if the L1 wants the limit recorded:

> "The polarity test is a negation-word list: a rule cell that reverses a relation without a negation word (e.g. `after` for `before`, `split` for `merged`) still verifies. ORDER- and PARTITION-bearing rows (EX2, EX7) are therefore checked for presence and quote, and their direction rests on the cited lines, not on the counter."

## 6. Round-39 counter no-harm

```
$ python3 tools/check-transaction-order-r39.py --revision f951f28…
{"counter": "check-transaction-order-r39", …, "host": {"windows": 86, "transactions_started": 60,
 "scriptlet_tag_outside_commit": 252, "scriptlet_tag_total": 441, "running_inside_commit": 0},
 "rules_verified": 8, "source_ok": 1, "counts_ok": 2, "oracle_violations": 0, "result": "PASS", "exit": 0}
```
exit 0 — still PASS at the lane tip. Receipt `w1/C2ExecRerun/r39-no-harm-f951f28.json`.

## 7. Not done / limits

- Did not run the C1 census selftest or the C1 literals counter (not this item; also CPU-shared).
- Did not re-fetch upstream pacman/Arch sources; provenance is the pinned snapshot, whose digests I did verify.
- Did not audit the round-39 entry beyond the no-harm run.
- `--revision HEAD` is refused by design (`E-REVISION-INVALID revision: 7-64 hex commit required`); anyone re-running must pass a hex commit — my first harness pass hit this and its outputs were discarded, not reported.
- No tool installs were needed; nothing was upgraded.

Receipt index with digests: `.ufo/waves/round-40/w1/C2ExecRerun/SHA256SUMS.local`. Scratch `/fast/scratch/hyaku/tsukuroi-r40/C2ExecRerun/` removed after copying these files.
