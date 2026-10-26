VERDICT: supports

# C2-9 — independent oracle over the frozen transaction capture (round 39, seat C2ExecLogOracle)

Item: recompute, from a parser written for this seat alone, the command windows, `transaction started`
count, `running` lines inside commit phases, `ALPM-SCRIPTLET` lines inside/outside commit phases, `removed`
lines and their transactions, and mixed remove+add transactions; compare with the entry's numbers
(86, 60, 0, 252 of 441, 28, 0 of 60); repeat on the live `/var/log/pacman.log` and report drift.

Entry under test: `corpus/knowledge/pacman-transaction-order-r39.md` (commit 4078eb2), host cells on lines
24–31. Capture: `.ufo/waves/round-39/frozen/txcapture/pacman.log`. Receipts in
`.ufo/waves/round-39/w1/C2ExecLogOracle/` (`oracle.py`, `oracle-capture.txt`, `oracle-live.txt`,
`drift.txt`, `windows.py`, `prehook.py`, `selftest.py`, `hashes.txt`).

## 1. Every declared number reproduces exactly

`python3 oracle.py frozen/txcapture/pacman.log` (receipt `oracle-capture.txt`; I wrote this parser from the
line grammar `[<ts>] [<TAG>] <msg>` before reading any of the counter's code, and import nothing from it):

| entry claim (entry line) | claimed | oracle | status |
|---|---|---|---|
| `[PACMAN] Running` windows (TO1, line 24) | 86 | 86 | match |
| `transaction started` (TO1) | 60 | 60 | match |
| `running '<hook>'` inside a commit phase (TO1) | 0 | 0 (of 295 total) | match |
| `[ALPM-SCRIPTLET]` outside every commit phase (TO8, line 31) | 252 | 252 | match |
| `[ALPM-SCRIPTLET]` total (TO8) | 441 | 441 | match |
| `removed` lines (TO2 line 25, TO7 line 30) | 28 | 28 | match |
| transactions mixing removed with installed/upgraded (TO2) | 0 of 60 | 0 of 60 | match |
| PreTransaction hook files whose owner the capture first installs, none run in that Pre phase (TO5, line 28) | 17, 0 | 17, 0 | match |

Whole-log census from the same parser: 3254 lines, 0 unparsed, 60 transactions all closed by
`transaction completed` (0 interrupted, 0 failed, 0 unclosed, 0 nested starts), 2260 package-add lines
(1437 `installed`, 821 `upgraded`, 2 `reinstalled`), 295 hook invocations over 49 distinct hooks.
Every `transaction started` sits inside a `[PACMAN] Running` window (0 orphans), and 0 `[ALPM] error` lines
exist in the capture.

A second, independently written state machine (`windows.py`, awk-style phase tracking in Python) returns the
same figures — `windows-out.txt`: `running_before_started(PRE)=59 running_after_completed(POST)=236
inside=0 no_window=0`, `scriptlet_by_phase {'commit': 189, 'post': 243, 'win': 9}`, `windows_with_commit=60
windows_total=86`; and a third pass in pure `awk` (`T=60 W=86 R=295 Rin=0 Rout=295 S=441 Sin=189 Sout=252
D=28 Din=28 W_in_commit=0`) agrees. 189 + 252 = 441 and 59 + 236 = 295, so the inside/outside split closes
arithmetically as well as by construction.

Structural detail the entry leaves implicit and the oracle supplies: the 86 windows contain exactly one
`transaction started` each for 60 of them (a bijection, not an aggregation), and the other 26 windows are
non-committing (`pacman -D`, `-Sc/-Scc`, `-Sy`, `-Sw`, plus two `-S --noconfirm` runs at
pacman.log:1413 and :2286) with zero `[ALPM]` lines each — so the 86/60 pair is consistent under both
readings ("all windows" and "windows that commit").

`removed` lines sit in exactly 7 transactions — opened at pacman.log:2122, 2389, 2456, 3128, 3134, 3154,
3249 — each with 0 `installed`/`upgraded` lines (1, 4, 2, 1, 14, 3, 3 removals). This is what makes TO2's
"0 of 60" and TO7's "never for upgrades" true in the same fact: no transaction in the capture contains both
a `removed` line and an add line, so no `removed` line can belong to an upgrade.

TO5's host clause reproduces independently (`prehook.py`, from `hook-when.tsv` + `hook-owners.tsv` +
first `installed <pkg>` line): 17 hooks have `When=PreTransaction` (of 70 hook files, 53 Post); all 17
owners are first seen in the capture as `installed` (e.g. `10-limine-snapper-lock.hook`/`limine-snapper-sync`
at pacman.log:1346, `60-mkinitcpio-remove.hook`/`mkinitcpio` at :245); 0 of the 17 ran before the
`transaction started` of their own first-install window; 10 of the 17 never ran at all in the capture and 7
ran elsewhere (49, 2, 1, 2, 2, 2, 1 times).

TO3's cited log pair is exact: pacman.log:123 `[ALPM] installed systemd (261.1-1)` and :124
`[ALPM-SCRIPTLET] Initializing machine ID from random generator.`

## 2. The oracle is sensitive, not vacuous (negative controls)

`selftest.py` (receipt `selftest-out.txt`) builds a fixture log with hand-known answers and then mutates the
capture four ways:

- fixture (3 windows, 2 transactions, 1 hook run inside a commit, 2 removals in one mixed transaction):
  every asserted value matches — `FIXTURE self-test PASS`.
- inject one `[ALPM] running` line right after the first `transaction started`: `R_in 1` (base 0), `S_in`
  unchanged 189, `R` total 296 (base 295) — the inside/outside classifier is not stuck at zero.
- rename all 60 `transaction completed` to `transaction interrupted`: closers flip to
  `{'transaction interrupted': 60}`, `S_out` stays 252 (all three closers are recognised, so the split is
  insensitive to which terminator a transaction used).
- delete one `[PACMAN] Running` line: `W 85` (base 86), `T` unchanged 60 — windows are counted per line,
  not inferred from transactions.
- delete the first `transaction completed`: `R_in 13` (base 0), `S_in 215` (base 189), one merged phase —
  losing a terminator is loudly visible rather than silently absorbed.
  `SENSITIVITY PASS`.

I also corrected two of my own initially wrong fixture expectations (scriptlet 5→4, inside 2→1) against the
parser's output rather than the reverse; the fixture contains 4 scriptlet lines, 1 of them inside a commit.

## 3. Live host log drift since the capture: none, and the capture is genuine

`drift.txt` + `oracle-live.txt`:

- `sha256sum /var/log/pacman.log` = `0845c1df31fcccd1b629f3b5c8190c037a572bbfbd6d9e11f81be635b1a4fc67` = the
  capture's own digest and the digest on the capture's `MANIFEST.sha256` line; `cmp` → `CMP_IDENTICAL`;
  both 3254 lines / 252016 bytes.
- `sha256sum -c MANIFEST.sha256` in the capture dir → `pacman.log: OK`, `hook-owners.tsv: OK`,
  `hook-when.tsv: OK`, and `sha256sum MANIFEST.sha256` = `cb5cb4f4…c1bb4`, exactly the manifest digest the
  entry's front matter pins.
- Live log mtime `2026-10-25 13:12:06.981386572 -0300`, last line `[2026-10-25T13:12:06-0300]`; the capture
  was taken `2026-10-26T05:42:12Z` (= 02:42:12 -0300, the copy's mtime in `capture-meta.txt`).
- Oracle on the live path returns identical counts (`IDENTICAL_COUNTS`): 0 new windows, 0 new transactions,
  0 new scriptlet lines, 0 new `removed` lines, 0 new lines of any kind — no pacman run has happened since
  the capture, so there is no drift to report.

The frozen source snapshots also verify: `sha256sum -c SHA256SUMS` in `.ufo/waves/round-39/frozen/src/` →
`add.c hook.c remove.c sync.c trans.c util.c: OK`.

## 4. Counter cross-check, and the host numbers the counter does not test

Running the frozen counter read-only at the entry commit
(`python3 tools/check-transaction-order-r39.py --revision 4078eb236c7c67f343c76956c587d0a356e0bf5c`) returns
`result: PASS, exit 0`, `rules_verified 8, duplicate_rows 0, duplicate_headings 0, source_ok 1, counts_ok 2,
oracle_violations 0`, and a host block identical to mine: `windows 86, transactions_started 60,
scriptlet_tag_outside_commit 252, scriptlet_tag_total 441, running_inside_commit 0`.

Coverage gap I can now state precisely: `counts_ok` tests only two substrings — the TO1 cell's
"60 transactions" and the TO8 cell's "252 of 441" (`tools/check-transaction-order-r39.py:222-226`); it never
looks at the 86, at TO2's "(0 of 60)", TO5's "17" or TO7's "28". Those four unchecked host numbers are the
ones this oracle recomputed from scratch, and all four hold. Likewise the counter's quote test proves a 4–25
word quote sits inside the cited lines (`:210-219`), not that the rule is true — consistent with the
declared kill rule, and it is why the rows below were read at source rather than trusted.

## 5. TO rows read at the cited lines (host log + pinned source)

No row is contradicted by the capture, and each cited quote is present at the cited lines in the frozen
snapshots (spot-located with `grep -n -F` and read in context). One wording caveat is recorded in §6.

TO1: holds — trans.c:201-208 (Pre hook at :202, `transaction started` at :208), Post at trans.c:238
TO2: holds — sync.c:1340-1354 (`_alpm_remove_packages(handle, 0)` :1345 before `_alpm_upgrade_packages` :1354)
TO3: holds — add.c:466-474 pre scriptlet, extraction at add.c:560, log verbs add.c:616-631, post add.c:638-645
TO4: holds — add.c:470-474 (`newpkg->version, oldpkg ? oldpkg->version : NULL, 1)`)
TO5: holds — hook.c:540 loop, `opendir(path)` at hook.c:554 inside it
TO6: holds — add.c:677-690 (`commit_single_pkg` failure → `STATE_INTERRUPTED`, `skip_ldconfig = 1`, single `_alpm_ldconfig` after the loop)
TO7: holds — remove.c:699-733 (`pre_remove` :711, `removed %s (%s)` :722, `post_remove` :731; both guarded on `!newpkg`)
TO8: holds — util.c:521-528 (`alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line);` :527)

## 6. Findings that qualify the entry (non-falsifying)

1. TO3 host cell, second clause — "a pre-scriptlet's output precedes the line" (entry line 26) — is not
   verifiable from the capture: `[ALPM-SCRIPTLET]` lines carry only the child's line
   (util.c:521-528 passes `line`, no package or scriptlet name), so no log line can be attributed to a
   package's pre- vs post-scriptlet. The clause is true by source order (add.c:466-474 before :616-631), and
   the first clause's citation (pacman.log:123-124) is exact, but as written the host column states more than
   the log can show. Precision note, not a contradiction.
2. TO6's host cell is a conditional with no host instance in this capture: 0 of 60 transactions closed by
   `transaction interrupted` or `transaction failed`, and 0 `[ALPM] error` lines — the skip-ldconfig/no-Post
   path is untested here.
3. TO1's "every Pre `running` line of a window precedes its `transaction started` line" is stronger than the
   counter checks and is exactly true on this log: 59 hook invocations occur before a window's
   `transaction started`, 236 after its `transaction completed`, 0 inside, 0 outside any window.

## 7. What I did not do

- Did not read or import `tools/check-transaction-order-r39.py`'s counting code before writing `oracle.py`;
  I ran it afterwards only to compare emitted numbers, and read `:210-226` afterwards to state the
  `counts_ok` coverage gap.
- Did not judge which staged `pacman-hook-timing-r25.md` propositions the entry admits, corrects or rejects
  (that is the Gate's business), did not verify `corpus/SOURCES.md` row status, and did not re-validate the
  hook-order entry HO1–HO7.
- Did not run any pacman/hook/mount/service action; the host was read-only throughout and the live log was
  only hashed and parsed.
- No tools installed or upgraded (host pacman transactions are paused per the directive; nothing was
  needed). No scratch left behind: `/fast/scratch/hyaku/tsukuroi-r39/C2ExecLogOracle/` was removed after
  its receipts were copied into the seat dir.

Risks: the capture is a single host's log, so TO2 and TO6 have no host instance and TO5 is consistency, not
proof (the entry says so itself in Boundaries); the manifest and source digests are intact, so those limits
are the entry's, not the receipts'.
