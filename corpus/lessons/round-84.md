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
| S336 (new, docs/A) | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/kernel-parameters.txt, 2026-11-06, raw 6581-6582 | "at which the swap header is located, in <PAGE_SIZE> units (needed only for swap files)" (15 words) | ADMIT, HR1. |
| S337 (new, docs/A) | https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/ch-swapfile.rst, 2026-11-06, raw 127, 118, 13 | "that will print the device physical offset and the adjusted value for" (12 words) | ADMIT, HR2/HR3/HR4. |
| S338 (new, docs/A) | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/power/swsusp-and-swap-files.rst, 2026-11-06, raw 57-58, 61 | "the swap file has to be active (ie. be present in /proc/swaps) so that it can be used for suspending." (20 words) | ADMIT, HR5/HR6. |
| S339 (new, docs/A) | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-hibernate-resume.service.xml, 2026-11-06, raw 38 | "Internally, it works by writing the major:minor of selected device node to" (12 words) | ADMIT, HR7. |
| S340 (new, docs/A) | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/ABI/testing/sysfs-power, 2026-11-06, raw 307-308, 97-98 | "Using this sysfs file will override any values that were set using the kernel command line for disk offset." (19 words) | ADMIT, HR8/HR10. |
| S341 (new, code/A) | https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/install/resume, 2026-11-06, raw 11-12 | "if (( systemd_ver >= 255 )); then add_binary /usr/lib/systemd/systemd-hibernate-resume" (9 tokens) | ADMIT, HR9; host copies byte-identical. |
| S342 (new, code/A) | https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/subprocess.py, 2026-11-06, raw 398-400 (re-raise at 402) | "return p.wait(timeout=timeout) except: # Including KeyboardInterrupt, wait handled that. p.kill()" (10 tokens) | ADMIT as the correction source for the round-83 `call()` reject reason (Mistakes M1). |
| REJECTED: swsusp.rst swap-size advice | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/power/swsusp.rst, 2026-11-06, raw 382 | "Just prepare big enough swap partition." (6 words) | REJECTED, no row: it names no size rule and speaks of partitions; HR10 rests on the sysfs-power `image_size` definition. Flip: a sentence in the same file that bounds image size against free swap. |
| REJECTED: ArchWiki Power management/Suspend and hibernate, revision 887184 | https://wiki.archlinux.org/index.php?title=Power_management/Suspend_and_hibernate&action=raw&oldid=887184, 2026-11-06 | none: the response was an anti-bot interstitial ("Making sure you're not a bot!"), 7066 bytes, no wiki text | REJECTED, not opened as a source; not a fabrication, an unreachable body. Flip: a fetch that returns the wikitext. |

Round-83 correction (routed defect 1, appended, the round-83 row is not rewritten): the round-83 Gate row
"REJECTED negative: `call()` kills the child on timeout" gave the reason "behaviour reaches it only through
`Popen.wait`". That reason is false: CPython v3.14.8 `Lib/subprocess.py` raw 398-402 (S342) wraps
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
| M1 | wrong reject reason from a docs-only sweep of a tier-A behaviour claim | `corpus/lessons/round-83.md` Gate row "REJECTED negative: `call()`…"; `round-83-verifier-spotcheck.md` §3 | none (QUALITY had no rule for reject reasons) | QUALITY 118: a reject reason about code behaviour cites the code at the host's version. Shown able to fail: the round-83 row cites only the docs page (fails 118); S342 at raw 398-402 is the passing form. |
| M2 | three consecutive rounds (81–83) claimed the lane's own instruments as the surface; each rejection fed the next meta-claim | MANIFEST 1276/1297/1319 verdicts; SCORECARD r81–r83 declarations | none | This round's claims sit on host ground; the counters are frozen instruments, not the claimed surface. The check that can fail: `grep -c 'corpus/knowledge/' <declaration>` naming a new host entry — r83's declaration names none. |
| M3 | a positive control that needs no domain work met the frozen target and was read as a passing selftest case | `before/controls/c1-controls.txt` P1 (`met`, three runs) committed in freeze `e0f42051`; SCORECARD "C1 withdrawn as a measured claim" (`69915b86`) | prompt §9 "build the cheapest control that skips the claimed work … if it meets the target, the counter or target is wrong" — existed, not applied: the L1 classed P1 as a counter-health case, not as a skip-work control | Before a freeze, every positive control is also read as a skip-work control: if it needs no domain work and reads `met`, the counter is a shape gate and the claim cannot rest on it. Shown able to fail: P1 itself (junk rows → `met`). C1 was withdrawn before any seat ran rather than re-predicated after data. |
| M4 | a battery whose case order is fixed per run lets a gate replay the expected answers without reading the input; one-fault-per-case families never exercise rule composition | `.ufo/waves/round-84/w1/CriticClaims.md` F-C2-1 (`f2-replay.py`, never opens `--facts`, 13/13 exit 0), F-C2-2 (`f1-signature.py`, three rule clauses unimplemented, 13/13), F-C2-3 (first-fault-only, 13/13); MutGate M14/M16/M20/M21 survive | QUALITY 117 (b) covers fixture-path sniffs, not schedule replay; prompt §9 skip-work control — the L1 built base-memorising and blanket controls but no order-replaying one | QUALITY 119. Shown able to fail: `f2-replay.py` against the frozen battery (13/13, the red) versus the same gate once the plan is shuffled per run (critic's proposal, `CriticClaims-receipts/proposal-battery-r84.md`). |

## Seat harm

| Harmed seat | Causing seat | Evidence class | Effect |
|---|---|---|---|
| none observed | — | seat reports and scratch roots under `/fast/scratch/hyaku/tsukuroi-r84/` | no kill signal, collision or out-of-tree write reported by any seat |

## Counter-attack scoreboard (QUALITY 115)

| Counter | Arms fielded | Killed | Survived (class) |
|---|---|---|---|
| `resume-gate-battery-r84` (as a discriminator of gates) | MutGate 22 single-point gate mutants; CriticClaims forgers F1 signature, F2 schedule replay, F3 shape switch, F4 first-fault | 16 mutants; F3 (10/13) | mutants M12 (`<` → `<=` boundary), M14 (first vs last token), M16 (no rule-1 short-circuit), M20, M21 (multi-swap), M22 (bool type); forgers F1, F2, F4 at 13/13 — classes: order replay, single-fault-only families, unexercised boundary and multi-swap |
| `count-resume-rows-r84` (provenance shape) | MutCounter 20 single-point mutants; ExecProvenanceC1 junk entries | 8 mutants | 12 (10 selftest gaps: bytes-vs-manifest, quote length bounds, https check, duplicate-id, statement floor, `failed == 0`, snapshot floor flaky; 2 equivalent); junk entries read `met` by design — the known limit that withdrew C1 as a measured claim |

## Routed to the next round (declare before data)

- Re-freeze the C2 battery before any claim on it: shuffle the plan per run; add families `MULTI` (two faults,
  sorted pair), `RULE1-SHORT-CIRCUIT` (no `resume=` plus a second fault), `PARTITION-OFFSET-NO-MAP` (positive),
  a boundary case `free == image_size`, a multi-swap base and a duplicate-token cmdline; run the four r84 forgers
  (`.ufo/waves/round-84/w1/CriticClaims-receipts/gates/`) as committed controls before freeze.
- Battery wording (ExecBatteryC2 D1/D2, ExecCleanRoomGate §5): state nullable keys as required-but-nullable;
  un-nest `swaps empty → HR-NO-ACTIVE-SWAP` from rule 2's file-swap clause; state first-versus-last token.
- C1 counter selftest gaps (MutCounter): a case per surviving clause, if the counter is reused.
- Capture script `tools/capture-resume-facts-r84.py`: record failed probes itself (ReviewGate F1); the gate's
  `--live` path now fails closed on any non-zero probe rc (landed this round as a repair).
- Freeze commit author date: the jj helper stamped the freeze `e0f42051` with its parent's author date
  (CriticClaims F-CH-2); commit-graph order is the chronology evidence, not author dates.

## Wave corrections to the Gate (applied at landing)

- ScoutSources re-fetched all nine URLs live: byte-identical to every pin (`.ufo/waves/round-84/w1/ScoutSources.md` §1);
  every HR quote and host value re-located (§2, §3).
- D1: S339 anchor `36-50 (Description)` excluded the section title; now `31-51 (Description section), 38`.
- D2: S342's `teaches` cell says "then re-raises", but the cited range ended at `p.kill()` (400); the `raise` is
  raw 402. Anchor now `388-402 (def call), 398-400, 402 (re-raise)`; the Gate row cites `398-400`, the minimal
  span of its quote.
- D3: three token counts in the Gate table were off by one (S336 15 words, S341 9 tokens, S342 10 tokens);
  relabelled. The same habit exists in earlier lessons (round-83 :18, round-81 :25) and is left as filed.
- ReviewEntry disagreed with the L1 on HR4 (mount option asserted without a receipt) and HR9 (writer
  attribution); both reworded. Its remark that this initramfs is systemd-based is not adopted: the effective
  HOOKS (`before/host/receipt.txt` :60-75) carry `base`, `udev`, `encrypt` and no `systemd`.

## Verdicts

| Claim | Axis | Verdict | Basis |
|---|---|---|---|
| C1 (exploratory, sourced S336–S341) | depth 8 | `unprovable-but-better` (reviewer ReviewEntry, non-author) | `w1/ReviewEntry/verdict.json`: 8 supports, 2 partial, 0 does-not-support, with reasons; no ordinal move |
| C2 (measured) | operability 9 | NOT VERIFIED | candidate 13/13 on the frozen battery, but forgers F1 (signature), F2 (order replay, opens nothing) and F4 (first-fault) also 13/13 (`w1/CriticClaims.md`); prompt §9 |

Not admitted: C2 does not verify. No axis harmed (`w1/CriticClaims.md` "Axis harm: none found"; registry gate 4 → 0 findings).
