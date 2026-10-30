ROW GR3 VERDICT: partly
SECTION SHA256: 0405f38a5783c49b6c078b118c9868543eb494b43f8b1c5e6c14284a123b9eac

Seat R52CritGR3c (critic, counted, row GR3, revision ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0). Entry extracted to /fast/scratch/hyaku/tsukuroi-r52/R52CritGR3c/entry.md (`git show ff9470ea:corpus/knowledge/btrfs-scrub-grounding-r45.md`, 447 lines). Receipts: .ufo/waves/round-52/w1/R52CritGR3c/digests.txt and lint-and-section-hash.txt.

Axes: C1 depth, clause-level grounding, citation fidelity, host provenance and boundary completeness. The smallest safe correction is to qualify the reset boundary; this review does not admit or integrate the row.

Checks run
- Section hash: `check-scrub-admission-r52.py --revision ff9470ea... --section-hash --no-base-check` prints GR3 0405f38a5783c49b6c078b118c9868543eb494b43f8b1c5e6c14284a123b9eac; matches the item.
- Snapshot digests (`sha256sum -c SHA256SUMS`, all OK): S237 = .ufo/waves/round-42/frozen/src/scrub.c (48df2e2f...); S244 = .ufo/waves/round-44/frozen/src/btrfs-scrub@.service (eaa7af92..., 10 lines); S248 = .ufo/waves/round-45/frozen/src/systemd.kill.xml (44832283...); S249 = .ufo/waves/round-45/frozen/hostcap/capture.txt (f5958a83...).
- Lint `lint-grounding-r51.py --revision ff9470ea...`: verdict PASS, lint_ok 3, GR3 quotes 25 / quote_bad 0, cites 28 / cite_bad 0, gap_ok 1.
- My own quote check: all 25 GR3 Quote rows match their cited lines after whitespace normalisation (0 content mismatches). Leading indentation differs on most rows; the lint strips it.

Clauses checked and supported as written
- systemd.kill.xml:108-109 and :84-85: KillSignal is the first step of stop; SIGTERM is the default (:112). Supported.
- btrfs-scrub@.service:9 `KillSignal=SIGINT`; lines 1-10 have no KillMode, SendSIGHUP or TimeoutStopSec. Supported.
- systemd.kill.xml:101 (control-group default), :86-87 (optional SIGHUP), :114-115 (SIGCONT, "always"), :91 and :96-97 (SIGKILL after TimeoutStopSec, FinalKillSignal, SendSIGKILL). Supported.
- scrub.c:1247 `bool do_background = true;`, :1292-1293 (`case 'B':` / `do_background = false;`), :1512 `if (do_background) {`. The only fork() in the file is at :1513. Supported.
- scrub.c:439, :442, :421, :1546 and :1710 are the quoted lines. :1546 is `scrub_handle_sigint_child(fdmnt);` and :1710 is `scrub_handle_sigint_child(-1);`. Only sigaction(SIGINT) sites are :433 and :443 (grep). A SIGINT before :1546 meets no cmds/scrub.c handler on the -B path. Supported.
- capture.txt:2-5 and host-btrfs-progs.txt:2-6, :4 (`SendSIGHUP=no`). The drop-in path in the row matches capture.txt:4 byte for byte.
- Inference marks at lines 253, 263 and 264 of the entry are genuinely undecided by the pinned bytes.

Defect D1 (makes the verdict partly): the reset-boundary description omits two error exits. This is a completeness defect, not a contradiction of the claimed SIGINT-to-cancel mechanism.
- Row text: "From scrub.c:1546 until scrub.c:1710 resets it, the start process has its SIGINT handler installed on the mount's descriptor (scrub.c:439, scrub.c:442)".
- Pinned bytes: scrub.c:1575 `goto out;` (after pthread_create of scrub_one_dev fails) and scrub.c:1592 `goto out;` (after pthread_create of the progress thread fails) both lie between :1546 and :1710 and skip the straight-line reset at scrub.c:1710. Both jump to `out:` at scrub.c:1712. On those two paths the handler stays installed when scrub_start returns (scrub.c:1761 returns scrub_start's result to the caller). Those paths are reachable only on thread-creation failure.
- Replacement text: replace "From `scrub.c:1546` until `scrub.c:1710` resets it, the start process has its SIGINT handler installed on the mount's descriptor (`scrub.c:439`, `:442`)" with "From `scrub.c:1546` the start process has its SIGINT handler installed on the mount's descriptor (`scrub.c:439`, `:442`); the reset at `scrub.c:1710` is the normal-path reset, and the error jumps `goto out` at `scrub.c:1575` and `:1592` skip it, so the handler stays installed when the function returns on those paths [inference: the process exits after that return; the caller's exit is not pinned here]."
- Impact on the stop clause: none on the normal path; the SIGINT-to-cancel mechanism and the SIGKILL timing are unaffected.

Non-blocking precision note (not counted as a defect)
- "(SR3)" in GR3 is not qualified by file. SR3 is defined in corpus/knowledge/btrfs-scrub-record-r43.md (line 52), not in r44. A parenthetical "(SR3 of btrfs-scrub-record-r43.md)" would make the row self-contained.

What I did not check
- I did not run any host command (systemctl, btrfs, pacman). Host claims rest on the round-45 capture.txt and the round-51 receipt host-btrfs-progs.txt, which I read but did not re-run. The receipt's sha256 at the frozen revision equals the worktree file.
- I did not verify the dispatcher's exit behaviour after cmd_scrub_start (scrub.c:1759-1761); the note in D1 is marked as inference for that reason.
- I did not check GR1 or GR2, the controls, or the other lanes.
- Disclosure: I read the uncounted round-51 pre-reads R51W1PreCritGR3a and R51W1PreCritGR3b to see which round-51 findings the amended row answers. I read no round-52 R52*GR* report. No admission mark was written.
