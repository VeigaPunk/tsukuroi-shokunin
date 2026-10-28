ROW GR3 VERDICT: holds
SECTION SHA256: 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c

Critic seat R49CritGR3a, claim C1, row GR3 of `corpus/knowledge/btrfs-scrub-grounding-r45.md` at
`55c07cd3f8bff2e12117c34d57b4c618de74d85c`. I did not write the row and am not its author.

## Hash and provenance

- Extract (once): `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 55c07cd3:corpus/knowledge/btrfs-scrub-grounding-r45.md > entry.md` — 287 lines, `## GR3` at line 152, next `## ` at line 198.
- My convention: the section is lines 152-197 (the blank line before `## How this changes OS triage` included), `'\n'.join(lines[151:197])` with no extra trailing LF added. sha256 = `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c`. The counter's `row_extent` (tools/check-scrub-admission-r49.py:166-175) takes exactly `lines[i:j]`, and `section_hashes` (:178-187) hashes `'\n'.join` of that slice, so the blank separator is inside the hashed text and the text ends with the one LF it contributes; our conventions agree. `--section-hash` at the freeze prints the same hash (`structural_ok: 1`, `problems: []`). Dropping the blank line would give `17b19a53…` and adding an extra LF `0f15f71c…` — neither is the frozen value.
- Snapshot digests, all `sha256sum -c SHA256SUMS` OK in their directories:
  - S248 = `.ufo/waves/round-45/frozen/src/systemd.kill.xml`, sha256 `448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72` (SHA256SUMS line 3); fetched from `systemd/systemd` tag v262 (round-45 `FETCH.txt`).
  - S244 = `.ufo/waves/round-44/frozen/src/btrfs-scrub@.service`, `eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252` (SHA256SUMS line 4); 10 lines, no `KillMode=` and no `TimeoutStopSec=`.
  - S237 = `.ufo/waves/round-42/frozen/src/scrub.c`, `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` (SHA256SUMS line 1), 2231 lines; round-42 `FETCH.txt` pins it to btrfs-progs v7.1 `cmds/scrub.c`. It is not S242, the round-44 kernel `fs/btrfs/scrub.c` (`f347931b…`); GR3 disambiguates by writing "btrfs-progs".
  - S249 = `.ufo/waves/round-45/frozen/hostcap/capture.txt`, `f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70`, matching the hash in the seat text; its method script `capture.sh` sits beside it and writes only its output argument.

## Clause-by-clause

All 12 quotes are exact at their cited lines (programmatic comparison of each quoted string to the cited snapshot line: 12/12 `stripped_equal=True`): S244:9,10; S248:68,91,96,101,108,114,115; S237:421,1546,439. No quote sits on the wrong line and no citation points into a different function.

1. Order KillSignal, then SIGCONT, then (after the timeout) SIGKILL — `systemd.kill.xml:84-87` ("Processes will first be terminated via SIGTERM (unless the signal to send is changed via KillSignal= or RestartKillSignal=)"), `:114-115` (SIGCONT "right after sending the signal specified in this setting"), `:89-98` (the timeout list item applies to `control-group`, `mixed`, `process`; "the termination request is repeated with the SIGKILL signal or the signal specified via FinalKillSignal= (unless this is disabled via the SendSIGKILL= option)"). The row's parenthetical names settings spelled on `:97-98`, one line past its exact `:96` quote; the CLAUSE is true in the pinned bytes.
2. `KillSignal=` is SIGINT rather than the SIGTERM default — `btrfs-scrub@.service:9` and `systemd.kill.xml:108-112` (first-step signal; "Defaults to SIGTERM."). `:112` is not quoted, but the clause is decided there.
3. No `KillMode=` means the default `control-group`, and every remaining process receives the signal — the unit file is 10 lines with no `KillMode=` (`btrfs-scrub@.service:1-10`); `systemd.kill.xml:101` ("Defaults to control-group."), `:64-66` (value list), `:68-70` ("all remaining processes in the control group of this unit will be killed on unit stop"). Host side: `capture.txt:3` reports `KillMode=control-group`, so the default and the effective value coincide; `capture.txt:7` (`unit_dropins` empty) rules out a unit-level override in the captured sweep.
4. Effective stop timeout 5 s — `capture.txt:4` (`/etc/systemd/system.conf.d/10-faster-shutdown.conf:2:DefaultTimeoutStopSec=5s`), `capture.txt:3` (`TimeoutStopUSec=5s`), `capture.txt:5` (`dropin_owner … none`, from `capture.sh`'s `/var/lib/pacman/local/*/files` sweep). The `[inference]` mark is placed on the reach to *every* system unit, which is the part `systemd-system.conf(5)` would decide and which is not pinned; the 5 s value itself is captured directly for this unit.
5. `-B` does not fork — `scrub.c:1247` (`do_background = true`), `:1292-1294` (`case 'B': do_background = false; do_wait = true; do_print = true;`), `:1743` (`OPTLINE("-B", "do not background")`), `:1512-1513` — the only `fork(` in the file is inside `if (do_background)`. The row cites `:1512`, the guard at the fork site; the option mapping is `:1292-1294`. `:1512`/`:1546`/`:439` is exactly the citation trio the round-46 gate records as the narrowed "-B handler install" ("Gate status — round 46" paragraph), so this is the vetted anchor, not an unreviewed gap.
6. The SIGINT handler acts on the mount descriptor — `scrub.c:1546` (`scrub_handle_sigint_child(fdmnt)`), `:1343` (`fdmnt = btrfs_open_mnt(path)`), `:436-444` (handler chosen at `:439`, `cancel_fd = fd` at `:442`, `sigaction(SIGINT, …)` at `:443`), `:417-424` (the handler issues `ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL)` at `:421`). The only two SIGINT `sigaction` sites in the file are `:433` (parent, `SIG_IGN`) and `:443`; with `-B` there is no fork, so `:443` is the live handler and it is installed at `:1546` before the scrub ioctls.
7. Canceled record not established — marked `[inference]` and consistent with SR3 (`corpus/knowledge/btrfs-scrub-record-r43.md:52ff`, `## SR3`: the record's `canceled` field comes from the new run, and a failed record write ends the progress thread), so a SIGKILL before that write leaves the last written record. I checked consistency, not the timing.
8. Host reading — `capture.txt:2` (systemd 262-1-arch), `:3` (`FragmentPath=/usr/lib/systemd/system/btrfs-scrub@.service` with `KillSignal=2 KillMode=control-group TimeoutStopUSec=5s FinalKillSignal=9 SendSIGKILL=yes`), `:4`, `:5`. `PKGBUILD:100` installs the unit to exactly that FragmentPath, so the host unit is the packaged one at that path.
9. Universal words — "every remaining process" restates the doc's "all remaining processes" (`:68`); "always send" is systemd's own wording (`:114`); no other only/never/exact word overreaches.
10. Ranges — GR3 cites no `a:b-c` line range at all, so no cited range can run into the following function.

## Defects

None found; no replacement text is owed. Two evidence-completeness notes, neither of which makes any clause false and therefore neither of which changes the verdict: (a) `FinalKillSignal=`/`SendSIGKILL=` are spelled on `systemd.kill.xml:97-98` while the quoted line ends at `:96` — adding a second Quote entry at `systemd.kill.xml:97` whose text is that line, `<varname>FinalKillSignal=</varname> (unless this is disabled via the <varname>SendSIGKILL=</varname>`, would make the parenthetical self-evidencing; (b) the `-B` mapping is at `scrub.c:1292-1294` while the citation is `:1512` — citing `scrub.c:1292-1294, :1512` would be tighter. Both existed in the same form in the round-46 bytes: GR3 at `b57740c2` is byte-identical to the freeze (same sha256 `43430a…`), and that revision was read `holds` by both residual seats after exactly this narrowing; at `a4477049` the diff is confined to the -B handler sentence, the `[inference]` mark and the `:1546`/`:439` quotes.

## Verified but not re-derived

- Exact quote equality and every cited `file:line` (programmatic, all 12).
- Digest equality of the four snapshot files and `sha256sum -c` in all three `src/` directories.
- Section hash by two routes (counter `--section-hash` and my own recomputation) and row extents.
- Cross-revision identity of GR3 (`b57740c2` == freeze) and the `a4477049` diff.

## Not done

- Did not run the full C1 counter, any census `--selftest`, or the C2/C3 counters (no cohort this seat; one selftest-bearing command at a time).
- Did not run `capture.sh`, `systemctl show/start/stop/cat`, or any live host probe; host claims were checked against the frozen capture only, so the installed unit's bytes are not digest-verified here (its path is, via `capture.txt:3` and `PKGBUILD:100`).
- Did not re-fetch the upstream URLs.
- Did not audit GR1 or GR2 (outside this seat; the item's GR2 hints did not apply to GR3).
