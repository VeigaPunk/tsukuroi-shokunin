# Round 84 — lesson (tsukuroi, fresh start)

author: TsukuroiR84 (L1). Freeze `e0f42051bf9b01af5857c28562ca0247a8fef367` precedes every candidate file.

## Fresh-start read

Read before declaring: MANIFEST `rounds[]` 1276/1297/1319 and the spot-checks for rounds 81 (`d5b3e134`),
82 (`a8598038`) and 83 (`64f45b79`). The three failures were procedural or instrumental, never numeric: r81
scored candidates before freezing; r82 froze a target its own recipes could not reach; r83 froze a battery a
fixture-path sniff passed in full. All three were also meta-rounds — the claimed surface was the lane's own
counters. This round returns to host ground (hibernate-resume, a surface no entry read) and freezes the
instruments with candidate-free controls first.

## Gate

Sources opened 2026-11-06 by the L1 (curl, HTTP 200 each; URLs in `.ufo/waves/round-84/before/src/URLS.txt`,
digests in `SHA256SUMS`). Quotes are verbatim at the cited raw lines of the pinned snapshot.

| Candidate | URL, access date, location | Located quote (≤25 words) | Decision, reason and flip |
|---|---|---|---|
| S336 (new, docs/A) | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/kernel-parameters.txt, 2026-11-06, raw 6581-6582 | "at which the swap header is located, in <PAGE_SIZE> units (needed only for swap files)" (14 words) | ADMIT, HR1. |
| S337 (new, docs/A) | https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/ch-swapfile.rst, 2026-11-06, raw 127, 118, 13 | "that will print the device physical offset and the adjusted value for" (12 words) | ADMIT, HR2/HR3/HR4. |
| S338 (new, docs/A) | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/power/swsusp-and-swap-files.rst, 2026-11-06, raw 57-58, 61 | "the swap file has to be active (ie. be present in /proc/swaps) so that it can be used for suspending." (20 words) | ADMIT, HR5/HR6. |
| S339 (new, docs/A) | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-hibernate-resume.service.xml, 2026-11-06, raw 38 | "Internally, it works by writing the major:minor of selected device node to" (12 words) | ADMIT, HR7. |
| S340 (new, docs/A) | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/ABI/testing/sysfs-power, 2026-11-06, raw 307-308, 97-98 | "Using this sysfs file will override any values that were set using the kernel command line for disk offset." (19 words) | ADMIT, HR8/HR10. |
| S341 (new, code/A) | https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/install/resume, 2026-11-06, raw 11-12 | "if (( systemd_ver >= 255 )); then add_binary /usr/lib/systemd/systemd-hibernate-resume" (8 tokens) | ADMIT, HR9; host copies byte-identical. |
| S342 (new, code/A) | https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/subprocess.py, 2026-11-06, raw 397-400 | "return p.wait(timeout=timeout) except: # Including KeyboardInterrupt, wait handled that. p.kill()" (11 tokens) | ADMIT as the correction source for the round-83 `call()` reject reason (Mistakes M1). |
| REJECTED: swsusp.rst swap-size advice | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/power/swsusp.rst, 2026-11-06, raw 382 | "Just prepare big enough swap partition." (6 words) | REJECTED, no row: it names no size rule and speaks of partitions; HR10 rests on the sysfs-power `image_size` definition. Flip: a sentence in the same file that bounds image size against free swap. |
| REJECTED: ArchWiki Power management/Suspend and hibernate, revision 887184 | https://wiki.archlinux.org/index.php?title=Power_management/Suspend_and_hibernate&action=raw&oldid=887184, 2026-11-06 | none: the response was an anti-bot interstitial ("Making sure you're not a bot!"), 7066 bytes, no wiki text | REJECTED, not opened as a source; not a fabrication, an unreachable body. Flip: a fetch that returns the wikitext. |

Round-83 correction (routed defect 1, appended, the round-83 row is not rewritten): the round-83 Gate row
"REJECTED negative: `call()` kills the child on timeout" gave the reason "behaviour reaches it only through
`Popen.wait`". That reason is false: CPython v3.14.8 `Lib/subprocess.py` raw 397-400 (S342) wraps
`p.wait(timeout=timeout)` in `except: p.kill(); raise`, so `call()` does kill the child on timeout. The
decision (no row) stays right because no admitted entry needed a `call()` row; the reason and the flip were
wrong. Corrected flip: source code at the host's version decides a tier-A behaviour claim; a docs-only sweep
cannot reject one.

Round-83 closure result (routed defect 4): the closure spot-check at `64f45b79` agreed on 5 of 6 Gate items
and disagreed on the `call()` reject reason; trend discernment `harmed`. Recorded here as received.

Routed defect 2: CriticClaims F1's named patch `proposal-battery-fixture-alias.md` was never committed; the
evidence that stands is the receipt `.ufo/waves/round-83/w1/CriticClaims-receipts/f1-v2-r82.json`, which this
lesson cites instead.

Registry changes (old → new): rows S336–S342 added (status none → `mined`, opened 2026-11-06, recheck
`on-release`; used-by: S336–S341 → `corpus/knowledge/hibernate-resume-plane-r84.md`, S342 →
`corpus/lessons/round-84.md`). No existing row touched. Collision check: highest id before was S335.

## Mistakes

| # | Class | Evidence | Captured-by | Fix |
|---|---|---|---|---|
| M1 | wrong reject reason from a docs-only sweep of a tier-A behaviour claim | `corpus/lessons/round-83.md` Gate row "REJECTED negative: `call()`…"; `round-83-verifier-spotcheck.md` §3 | none (QUALITY had no rule for reject reasons) | QUALITY 118: a reject reason about code behaviour cites the code at the host's version. Shown able to fail: the round-83 row cites only the docs page (fails 118); S342 at raw 397-400 is the passing form. |
| M2 | three consecutive rounds (81–83) claimed the lane's own instruments as the surface; each rejection fed the next meta-claim | MANIFEST 1276/1297/1319 verdicts; SCORECARD r81–r83 declarations | none | This round's claims sit on host ground; the counters are frozen instruments, not the claimed surface. The check that can fail: `grep -c 'corpus/knowledge/' <declaration>` naming a new host entry — r83's declaration names none. |
