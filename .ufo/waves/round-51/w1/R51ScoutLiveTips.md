VERDICT: no-finding

Item C3-A6, independent live-tip walk. Observed 2026-10-28T21:17:09Z. Pins and quotes are the ten `outbound` records in `2732ee6c06108c031c4d8043239b994e0504eb2f:corpus/knowledge/adjacency-anchors-r19.json` (schema `tsukuroi-adjacency-anchors-r19-v1`). Each sibling checkout is `/home/vgpnk/Projects/shokunin/<sibling>-shokunin`. Read-only. No tool installed. The counter's quote legs were opened only after the table below was fixed.

No sibling changed the sentence an OUT anchor cites. Every anchor is stale: the registry pin is an ancestor of the live tip, and `PROVINCE.md` differs. It is not drifted: the registry quote is a substring of the tip blob on exactly the declared `quote_line`, that full line is byte-identical to the pin, and no `diff -U0` hunk covers the line.

## Repo table

Commands and output: `.ufo/waves/round-51/w1/R51ScoutLiveTips/raw-git.txt`. `pin..HEAD` counts and `diff --stat` are that file. `merge-base --is-ancestor <pin> HEAD` exited 0 for all eight (same receipt). Pin sha256 is `git cat-file blob <pin>:PROVINCE.md | sha256sum` and matches `sibling_blob_sha256` in the registry. Tip sha256 is the same command on `HEAD:PROVINCE.md`.

| sibling | HEAD | pin | commits pin..HEAD | PROVINCE.md pin..HEAD | pin sha256 = registry | tip PROVINCE.md sha256 |
|---|---|---|---|---|---|---|
| mori | `325f7e639916fcbc77fa2ec7475951a1b86bb1cb` | `91940fa339e38006f8db5bd7d78bb6f037f4d016` | 503 | 362 insertions, 7 deletions | yes | `e1afa247f169a104a1fc459e7a50a5329e00f5fb79d11a6ae6cbd020bcfc353b` |
| kama | `7ee8cbdf160f8c945954e4737e7a2f797e3b2987` | `e75cf680b53484a61709ee1b2787d8dbc6419f74` | 400 | 108 insertions, 0 deletions | yes | `a60591b77ac8a8f0bd90f3436d75fc8cbe1fbab820d37e6f57b0e386c32a01a9` |
| kagi | `69b61db46be4ed955994f6f1d1cba522bc5f4e97` | `c2cab35bc92e57e39e5489bac3386db078345b3f` | 63 | 26 insertions, 5 deletions | yes | `5edd4f1b134d1cf3b4434239478e168bcc535e02fcfa31bc354dabec4650bb02` |
| mado | `3b55b6e91e40f455dd56b2985e4ffc087ada92d5` | `a4046a8216080d4004de3f268c62cf142095ac07` | 380 | 102 insertions, 0 deletions | yes | `9edb9c47c7a0f6ca46d8d5769116efbbc90795947f8bfabcdd1bc95de3fb78d0` |
| kumitate | `14057f3e3899180c95713bace088fb9c0d0046e3` | `1770305fae20826b39905a8251ddeca6b4957ac4` | 285 | 5 insertions, 3 deletions | yes | `b20bd05ffd41002806b05bc5e49a53301671d580a87ffd2e15b3c093a2196fdc` |
| kaidoku | `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9` | `d1d981d2cc041dda4656c5b01d2c8445d8d17124` | 373 | 273 insertions, 5 deletions | yes | `e15824daf5037036e84c0939b8b987c204a394b39cf9f02afe0cf42ef8fab98b` |
| revenger | `6defe31e4af9f7b3780b2942f1e4e325f6d53cbc` | `cf02419276e5dd8aafb6fe09d4e9aaa6bcb78c97` | 104 | 7 insertions, 1 deletion | yes | `6c3694f9d82bf27d7bbf72d00903251a046e5d47630cb3ce3e5e18f1ea497a9b` |
| tameshi | `8c20d5c351b39d51c8842bccf3ea8dc45171ccfb` | `01d586ddbc5fcd78659557c4e93a6ee8517b87d1` | 419 | 35 insertions, 0 deletions | yes | `b2875fe21f381d98551d5a4946af4fb547ceb6244ce6bef35885dbdf034c28be` |

`git rev-parse --show-toplevel` for each repo printed that repo path (`raw-git.txt` lines 3, 27, 48, 70, 90, 109, 133, 153).

## Quote table

Substring and full-line check: `.ufo/waves/round-51/w1/R51ScoutLiveTips/quote-lines.txt`. Each quote occurs once in the pin blob and once in the tip blob, both times on the registry `quote_line`, and those two lines are equal. First hunk is `git diff -U0 <pin> HEAD -- PROVINCE.md` (`raw-git.txt`).

| id | sibling | quote_line | tip substring | line pin==tip | first hunk | hunk covers quote_line |
|---|---|---|---|---|---|---|
| OUT-001 | mori | 9 | yes | yes | `@@ -25 +25 @@` | no |
| OUT-005 | mori | 8 | yes | yes | `@@ -25 +25 @@` | no |
| OUT-007 | mori | 12 | yes | yes | `@@ -25 +25 @@` | no |
| OUT-002 | kama | 12 | yes | yes | `@@ -13,0 +14 @@` | no |
| OUT-003 | kagi | 3 | yes | yes | `@@ -45 +45 @@` | no |
| OUT-004 | mado | 6 | yes | yes | `@@ -19,0 +20,16 @@` | no |
| OUT-006 | kumitate | 3 | yes | yes | `@@ -20,3 +20,5 @@` | no |
| OUT-008 | kaidoku | 3 | yes | yes | `@@ -44 +44 @@` | no |
| OUT-009 | revenger | 3 | yes | yes | `@@ -8,0 +9,6 @@` | no |
| OUT-010 | tameshi | 7 | yes | yes | `@@ -83,0 +84,35 @@` | no |

Lines `quote_line-1` through `quote_line+2` are also identical on pin and tip for every id except kama line 14. Kama lines 12 and 13 match. Tip line 14 is an inserted table row, not a rewrite of the cited row: pin line 14 (`endpoint-drift detection + invocation history`) is tip line 15. The cited sentence is the line-12 cell `` `GET /v1/models` vs `--alias` vs the configured model id` ``, unchanged. The second kama hunk (`@@ -15,0 +17 @@`, `raw-git.txt:40`) is another insertion below that.

Drifted siblings: none.

## Post-walk read of the quote legs

Not used to classify the table. Frozen `2732ee6c06108c031c4d8043239b994e0504eb2f:tools/check-adjacency-table-r51.py` reuses round-50 `quote_at_pin_ok` and `live_quote_ok` (docstring lines 5-8; `run` copies them at lines 277-278). Its own `sibling_blob` (lines 78-81) and `bound_legs` (lines 116-128) read `PROVINCE.md` at the registry `sibling_commit`, not at `HEAD`.

Frozen `2732ee6c06108c031c4d8043239b994e0504eb2f:tools/check-adjacency-table-r50.py` (blob `ba0ed701a30af0b286ee9055040c3d80f956e7b9`), `content_legs` lines 112-167: `live_quote_ok` counts OUT ids named by ADJ rows whose displayed anchor-cell quote, after `str.strip('`')`, is a substring of `HEAD:PROVINCE.md` (lines 131 and 152-161). The docstring (lines 13-14) calls that "the locator still names a sentence that exists." That test does not require the surrounding line to be unchanged. On these tips the stricter line-and-hunk check still finds no rewritten cited sentence. This seat did not run either counter.

## Not done

Did not run `tools/check-adjacency-table-r51.py`. Did not parse the displayed anchor table, only the registry `quote` strings. Live HEADs are the checkouts at the observation time above.
