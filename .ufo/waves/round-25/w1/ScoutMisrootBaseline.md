# Scout: misroot baseline (round 25, wave 1)

Verdict: the fleet root working tree is byte-identical to the L1 baseline taken at 10:09Z, so round 25 wave 1 introduced no new fleet-root path; there are zero plain `??` untracked entries, six intent-to-add paths and three gitignored misroot directories, and none of the nine names tsukuroi round 25.

## 1. Porcelain matches the baseline byte for byte

[obs] `git -C /home/vgpnk/Projects/shokunin status --porcelain` produces 17 lines. Diffing it against the baseline is empty:

```
diff /fast/scratch/hyaku/tsukuroi-r25/fleet-porcelain-before.txt \
     /fast/scratch/hyaku/tsukuroi-r25/ScoutMisrootBaseline_porcelain-now.txt
=> IDENTICAL
```

[obs] The baseline file's own mtime is 2026-10-22 07:09:46 -0300, that is 10:09:46Z, which is the capture the L1 describes as 10:15Z. Both files hold 17 lines: eleven tracked modifications (ten `.ufo/state/*.report-baseline` plus `.ufo/watchdog.log`) and six intent-to-add entries. All eleven modifications are state files, not misroot, and all eleven are unchanged from the baseline.

[obs] Fleet repo HEAD at the time of this reading is `f1a75c9`, `2026-10-22T07:19:21-03:00 round-25: kama report` (`git log -1`).

## 2. There are no plain untracked entries at all

[obs] `git status --porcelain | grep -c '^??'` exits 0 and prints `0`. Every untracked file carries the intent-to-add flag, shown as ` A` in porcelain column two.

[obs] `git ls-files -s` on all six returns the empty-blob object id, which is the intent-to-add signature:

```
100644 e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 0	write
100644 e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 0	.scratch/goal-20261022-hyaku-12h.md
100644 e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 0	.ufo/state/kotoba.report-baseline
100644 e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 0	.ufo/state/kotodama.report-baseline
100644 e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 0	.ufo/state/revenger.report-baseline
100644 e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 0	scripts/hyaku/__pycache__/append-closure.cpython-314.pyc
```

[obs] Real content exists only in the worktree: `git diff --stat -- write` reports `write | 1 +`, while `git diff --cached --stat -- write` is empty.

[inf] Some session ran an intent-to-add sweep (`git add -N` or equivalent) over the fleet root, which is why these six files appear in porcelain as ` A` rather than `??`. The flag records no content, so nothing about them is committed yet.

[obs] `git check-ignore -v` exits 1 for `write`, `.scratch/goal-20261022-hyaku-12h.md`, the pyc and `.ufo/state/kotoba.report-baseline`, confirming none of them is ignored; they are visible precisely because nothing hides them.

## 3. Every untracked fleet-root path, with a round-25 content verdict

Round-25 test used: `grep -a -i -c -E 'tsukuroi|round[ -]?25|r25' <path>`, where exit 1 means no match.

| # | Absolute path | Kind | Size / mtime | Names tsukuroi round 25? |
|---|---|---|---|---|
| 1 | `/home/vgpnk/Projects/shokunin/write` | file, intent-to-add | 25 B, 2026-10-21T22:52:50Z | No. grep match count 0, exit 1 |
| 2 | `/home/vgpnk/Projects/shokunin/.scratch/goal-20261022-hyaku-12h.md` | file, intent-to-add | 17367 B, 2026-10-22T07:54:00Z | No, as asked. It does name tsukuroi r24, see below |
| 3 | `/home/vgpnk/Projects/shokunin/scripts/hyaku/__pycache__/append-closure.cpython-314.pyc` | file, intent-to-add | 10738 B, 2026-10-22T08:01:42Z | No. match count 0, exit 1 |
| 4 | `/home/vgpnk/Projects/shokunin/.ufo/state/kotoba.report-baseline` | file, intent-to-add | 1 line | No. match count 0, exit 1 |
| 5 | `/home/vgpnk/Projects/shokunin/.ufo/state/kotodama.report-baseline` | file, intent-to-add | 1 line | No. match count 0, exit 1 |
| 6 | `/home/vgpnk/Projects/shokunin/.ufo/state/revenger.report-baseline` | file, intent-to-add | 1 line | No. match count 0, exit 1 |
| 7 | `/home/vgpnk/Projects/shokunin/bash: ` | directory, ignored | 2026-10-18T17:01:47Z | No, 1 file inside, match count 0 |
| 8 | `/home/vgpnk/Projects/shokunin/mori-shokukin/` | directory tree, ignored | 2026-10-21T12:53:32Z | No, contains no files |
| 9 | `/home/vgpnk/Projects/shokunin/tameshi-shokukin/` | directory tree, ignored | 2026-10-21T05:50:33Z | No, contains no files |

### 3a. `write` is a tool-shaped misroot, and it predates round 25

[obs] `hexdump -C write` shows exactly 25 bytes with no trailing newline, the ASCII `agent://U100N079H334f935b` ending in byte `62`.

[obs] Its mtime is 2026-10-21 19:52:50 -0300, that is 2026-10-21T22:52:50Z. The round-25 baseline was taken 2026-10-22T10:09:46Z, so the file is 11 hours 17 minutes older than this round's first capture and cannot be a round-25 product.

[inf] The name and payload together are the signature of a peer message written through the file-writing tool instead of the messaging tool: a seat supplied the literal string `write` as the path and one `agent://` address as the content, so the artifact landed in the process working directory, which was the fleet root.

[obs] No other tool-shaped filename exists anywhere in the fleet repo. A `find` over the whole tree, with `.git` pruned, for files named `write`, `edit`, `read`, `task`, `wait`, `grep`, `glob`, `eval` or `bash` returned exactly one hit, `./write`, in 119.77 seconds.

[obs] The fleet root contains no `tsukuroi`-shaped misroot: the top-level directory list holds `tsukuroi-shokunin` once, with a real `.git`, and no typo variant.

### 3b. The goal file names tsukuroi r24, not round 25

[obs] `.scratch/goal-20261022-hyaku-12h.md:86-87` reads `... This applies to kaidoku r25, kotoba r48, mori r24, / tameshi r25, tsukuroi r24, kake r28 and kotodama r51 ...`, and line 103 reads `| B5 | tsukuroi (r24) | Host operability. Owns the update-safety gate behind the host-wide pacman pause. |`. The token `r25` occurs there only for kaidoku (99), tameshi (104) and kama (106).

[obs] The file is the binding contract for the 12-hour hyaku session and legitimately lives under `.scratch/`; being untracked is its normal state, not a misplacement.

[inf] The goal file is one round stale with respect to tsukuroi, since it schedules tsukuroi r24 while the lane is now in round 25. That is a scheduling record, not a misroot, and it is outside this ticket's question.

### 3c. The three `.ufo/state` baselines record zero bytes

[obs] Each of the three new lanes' baseline files holds one line: `49 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, `51 e3b0...855` and `62 e3b0...855`. The digest `e3b0c442...b855` is the SHA-256 of the empty string.

[inf] Those three lanes (kotoba, kotodama, revenger) were registered with an empty report baseline, so their first report comparison starts from nothing. Worth knowing, but a registration-time property, not this round's.

## 4. Three misroot directories are hidden behind the ignore rule

[obs] `/home/vgpnk/Projects/shokunin/.gitignore:1` is `*-shokunin/`. Because that pattern matches any path component ending in `-shokunin`, it hides these three trees, which never appear in plain porcelain: `git status --porcelain --ignored=matching -uall` lists them as

```
!! "bash: /home/vgpnk/Projects/shokunin/souji-shokunin/"
!! tameshi-shokukin/tameshi-shokunin/
```

plus, at depth one, no entry for `mori-shokukin/` because that tree contains no file whose path ends in `-shokunin`.

[obs] Directory one, `/home/vgpnk/Projects/shokunin/bash: `, is a directory whose name ends with a space; `cat -A` renders the top-level name as `bash: $`. Its only file is a 10139-byte regular file at `bash: /home/vgpnk/Projects/shokunin/souji-shokunin/tests/tools/souji-verify.sh: No such file or directory`, so the file name itself embeds a bash error message. Its first lines are a JSON object with `"seat": "S54"`, `"kind": "adversarial"`, `"round": 4`, `"lane": "souji-shokunin"`, that is a souji-shokunin round-4 adversarial seat fixture, not tsukuroi. mtime 2026-10-18T17:01:47Z.

[obs] Directory two, `/home/vgpnk/Projects/shokunin/mori-shokukin/`, is a typo of `mori-shokunin`. It contains only empty directories down to `mori-shokukin/.ufo/waves/round-21/build`. mtime 2026-10-21T12:53:32Z.

[obs] Directory three, `/home/vgpnk/Projects/shokunin/tameshi-shokukin/`, is a typo of `tameshi-shokunin`. It contains only empty directories: `tameshi-shokukin/.ufo/waves/round-18/w1` and the doubly nested `tameshi-shokukin/tameshi-shokunin/.ufo/waves/round-19/w1`. mtimes 2026-10-20T19:39Z and 2026-10-21T05:50Z.

[obs] `find` over those three trees returns exactly one file in total, the fixture JSON above.

[inf] The `bash: ` tree is the residue of a command whose stderr text was used as a directory path, and the two `-shokukin` trees are the residue of a lane checkout run from a mistyped working directory; all three come from rounds 18, 19 and 21 or earlier, and none is a round-25 artifact. Nothing was moved or deleted, per the ticket.

## 5. Structural blind spot worth recording

[inf] Because of `.gitignore:1`, the fleet repo cannot see any path inside a lane repository. A misroot write that targets a lane directory, for example a file named `write` landing in the tsukuroi clone instead of its seat directory, would be invisible to fleet porcelain and to any baseline built from it. This baseline therefore proves absence at the fleet root and says nothing about paths inside lane repositories.

[obs] Nothing in the evidence indicates such a lane-internal misroot for tsukuroi in this round; this is a limit of the instrument, not a finding of damage.

## 6. Unknowns

[unk] Which session ran the intent-to-add sweep, and when. Establishing it would need reflog or shell history, which this ticket did not ask for and which the lane bounds restrict.
[unk] Whether the peer address `U100N079H334f935b` in `/home/vgpnk/Projects/shokunin/write` still resolves. That peer identity is not on this round's roster.
[unk] Whether the three ignored misroot trees are intended to be reclaimed by the operator. Reclaiming them is a host and VCS write, so it belongs to the L1 or the operator, never to this seat.

Scope: read=fleet repo porcelain status, baseline at /fast/scratch/hyaku/tsukuroi-r25/fleet-porcelain-before.txt, the six intent-to-add fleet-root paths and their first lines, .gitignore, the ignored-path listing, and the three misroot directory trees at the fleet root; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/ScoutMisrootBaseline.md plus scratch copies /fast/scratch/hyaku/tsukuroi-r25/ScoutMisrootBaseline_porcelain-now.txt and /fast/scratch/hyaku/tsukuroi-r25/ScoutMisrootBaseline_toplevel-dirs.txt; executed=git status --porcelain, git status --porcelain -uall, git status --porcelain --ignored=matching -uall, git ls-files -s, git diff, git check-ignore, git rev-parse, git log, stat, find, ls, head, grep, diff, cat, hexdump, strings, wc, sed
Model: opencode-go/deepseek-v4.1-flash
Installs: none
