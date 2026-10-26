# Round 43 — lesson (tsukuroi, hyaku run 9)

author: tsukuroi L1 (`TsukuroiR43`), 2026-10-26. Base `6951ead90566b2d74f7c45b4efca29246badad64` — the lane tip at round
start as `jj-lane.sh state` printed it. Claims, controls and outcome: `SCORECARD.md` sections "Round 43 — declaration"
and "Round 43 — measured outcome". Waves: two v1 waves, `w1` (build + first falsifiers, 44 seats) and `w2` (falsify,
with the six counted C2 row verdicts); specs, dispatches and the orchestrator's results files are in
`.ufo/waves/round-43/`. Seats are the lane, not outside reviewers (LEARNING.md); this round's non-author closure is
pending.

The round-42 Gate's spot-check is answered by `corpus/lessons/round-42-verifier-spotcheck.md`: its §4 agreed with both
sampled admits (SC2, SC5 as narrowed) and both rejects; its §6 routed the five defects dispositioned below.

## Gate

### New SOURCES rows (opened 2026-10-26 by this round's L1; each quote located with `grep -n` in the pinned snapshot; drafted by wave-1 seat SrcGateS240, checked by the L1)

| Row | URL (access 2026-10-26) | Located quote (≤25 words) | Location |
|---|---|---|---|
| S240 | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/ioctl.c?h=v7.2.11 (raw `plain/…?h=v7.2.11`, byte-identical to https://raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/btrfs/ioctl.c; tag v7.2.11 peeled `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`) | "if (!capable(CAP_SYS_ADMIN))" / "return -EPERM;" — the first check in each of the three scrub handlers | `.ufo/waves/round-43/frozen/src/ioctl.c:3072-3073, 3120-3121, 3132-3133` (handlers open `:3066`, `:3118`, `:3126`; dispatch `:5582-5583`) |
| S241 | own-work capture `.ufo/waves/round-43/frozen/hostcap/` (`capture.sh`, run 2026-10-26T21:51:26Z, uid 1000) | "scrub_progress_ioctl devid=1 errno=EPERM (1)"; "uid 1000 euid_caps 0000000000000000"; "no stats available" | `.ufo/waves/round-43/frozen/hostcap/capture.txt:6, 2, 10` |

Snapshot digests: `.ufo/waves/round-43/frozen/src/SHA256SUMS` (ioctl.c `7b3488f2…4ba01`), fetch log `FETCH.txt`;
capture.txt `f7ecbe7c…c556`, capture.sh `77ffeecb…a1a9`. Live re-fetches by wave-1 seats `C2ExecLiveSources` and
`SrcGateS240` were byte-identical. The Arch kernel 7.2.11-arch1-1 applies one patch that touches no file under `fs/`
(`w1/C2ExecKernelPatch.md`), so S240 is the booted code.

### Re-opened row and rows touched old→new

| Row | URL (access 2026-10-26) | Located quote (≤25 words) | Location |
|---|---|---|---|
| S237 | https://github.com/kdave/btrfs-progs/blob/v7.1/cmds/scrub.c (raw re-fetched byte-identical, `w1/C2ExecLiveSources.md`) | "ret = rename(datafile_old, datafile_new);" | `.ufo/waves/round-42/frozen/src/scrub.c:534` |

Rows touched: **S237 `used-by`** `corpus/knowledge/btrfs-scrub-record-r42.md` → `corpus/knowledge/btrfs-scrub-record-r42.md,
corpus/knowledge/btrfs-scrub-record-r43.md` (status `mined` unchanged). S240 and S241 are new rows (`mined` at entry).

### Entry gate (C2) — per adopted sentence, the source line the L1 checked (QUALITY 91)

The draft at `717b716a` was read by six wave-1 seats (`w1/C2DraftRevSR1/3/6.md`, `w1/C2DraftCritSR1/3/6.md`, not
counted) and three mechanical checks (`w1/C2ExecCallGraph.md`, `C2ExecTailRepro.md`, `C2ExecKernelPatch.md`).
Integrated into the entry before wave 2, each against the pinned line (`sed -n <n>p` on the snapshot, observed text):

| Row | Change | Proposed by | Source line checked by the L1 |
|---|---|---|---|
| SR1 | scope "every update of the record file" (three call sites) | C2DraftCritSR1 F3 | scrub.c:1123, :1503, :1702 `scrub_write_progress(` (grep) |
| SR1 | "open mode argument 0600, subject to the umask" | C2DraftCritSR1 F2 | scrub.c:483 `fd = open(datafile, m, 0600);` |
| SR1 | "a writer process killed between the open and the rename (for example by SIGKILL; the progress thread itself disables cancellation…)" replaces "a killed writer" | C2DraftCritSR1 F1 | scrub.c:905 `pthread_setcancelstate(PTHREAD_CANCEL_DISABLE, &old);`, :917 open, :925 rename, :941 `…ENABLE…` |
| SR1 | "if that update's write and rename succeed" | C2DraftCritSR1 F4 | scrub.c:922-927 (`if (err) goto out1;` before and after the rename) |
| SR1 | [inference] kept; reproduction named | C2ExecTailRepro | harness compiled from scrub.c write path: final file = new record + byte-identical tail of the older `_tmp` (`w1/C2ExecTailRepro.md` §results) |
| SR3 | "thirteen counted progress fields … `last_physical`, `canceled`, `finished` from the new run, `t_resumed` from the new run's `t_start`" replaces "progress counters added" | C2DraftCritSR3 F3 | scrub.c:806-818 (13 `_SCRUB_SUM`), :819 `_SCRUB_COPY(dest, data, last_physical);`, :820-822 |
| SR3 | "record (`last_dev_scrub`)" replaces "last record" | C2DraftCritSR3 F5 | scrub.c:1427 `last_scrub = last_dev_scrub(past_scrubs, devid);` |
| SR3 | zero-counter sentence replaced ("a device without a `resumed` source, or one that resume skips … zero in a run's first record; under a fresh `start` every device") | C2DraftRevSR3 S3, C2DraftCritSR3 F2, C2ExecCallGraph D1 | scrub.c:803 `if (!data->resumed \|\| data->skip)`, :1402 `sp = calloc(…)`, :1435-1437 (`skip = 1`, `resumed = last_scrub`) |
| SR6 | scoped to `btrfs scrub status`; start's other readings named | C2DraftCritSR6 F1 | scrub.c:1946 (only assignment of `in_progress`), :1378-1379 and :1392 (start: record), :1474-1476 (start: socket) |
| SR6 | "device by device … 1 on the first call that returns 0, and 0 only after every call failed" replaces "once per device"; no claim that success means running | C2ExecCallGraph SR6, C2DraftCritSR6 F2 | scrub.c:1197-1205 |
| SR6 | "`capable(CAP_SYS_ADMIN)` … initial user namespace [inference]" | C2DraftCritSR6 F3 | ioctl.c:3132 `if (!capable(CAP_SYS_ADMIN))`; `capable()` not in the pinned file — marked [inference] |
| triage | default start still warns on first-record/mkdir failure | C2ExecCallGraph D2 | scrub.c:1336, :1507 `warning(…status recording disabled)` (ungated `warning()`, `common/messages.c:33-40` per the seat) |
| Limits | Arch kernel patch checked | C2ExecKernelPatch | PKGBUILD tag 7.2.11.arch1-1: one patch `linux-v7.2.11-arch1.patch.zst` sha256 `741d473c…`, no `fs/` file |

Rejected (wave-1 claim refused by the integrator): **"the device id is never emitted, so resume never engages for
self-written records"** (`w1/C2DraftCritSR3.md` F1). False: `scrub_writev` writes its formatted buffer itself
(scrub.c:782-792, `return scrub_write_buf(fd, buf, ret);`), so the devid digits follow the colon; the extra
`scrub_write_buf(fd, buf, ret)` at :869 writes 0 bytes. The harness of `w1/C2ExecTailRepro.md` parsed `devid=7` back
from a record written by that code. SR3's resume sentences stand.

Post-wave-2 narrowing (the counted read `w2/C2CritSR3.md` bound SR3 `partly`, item 6): SR3's "(`skip` set: its record
is finished, or it has no record)" became "(`skip` set: its record is finished and not canceled, or it has no
record)". Source line checked by the L1: scrub.c:1430-1431 `if (resume && last_scrub && (last_scrub->stats.canceled
|| !last_scrub->stats.finished))` resumes a canceled record even when it is finished; :1435-1437 (`else if (resume)
{ sp[i].skip = 1; …`) skips only the rest. The changed row is re-read by the counted residual reviewer `C2ResSR3`
(`.ufo/waves/round-43/residual/`), as the declared kill rule requires. Out-of-row observation from the same read,
not claimed: for a skipped device with no record the child copy-in at :1550 dereferences `sp[i].resumed->p`.

### Assimilation (`merge/tsukuroi/`) — evaluated, nothing adopted (`Assimilation: none`)

Read-only evaluation `w1/AsmGate.md`: quarantine slice 12 rows (`w1/AsmGate/quarantine-slice`, identical to the
round-41 slice), collision check with the 0-3-space pattern in `w1/AsmGate/`. Nearest staged match to this round's
surfaces: `initramfs-hook-api-r25.md` (boot-chain inputs) — **refused this round**: not adoptable as staged (needs id
renumbering against S242+, a QUALITY check block, quote-anchored pointers and a reworded sentence; flip: a round that
takes the boot-chain input surface as its claim and does that work). **Rejected:** `ext4-journal-guarantee-r32.md` —
outside this host's province (no ext4 mount: `findmnt -rno TARGET,FSTYPE` lists no `ext4` filesystem — its disk mounts are btrfs, vfat and xfs;
`PROVINCE.md` names no ext4); flip: an ext4 filesystem enters this host. The round-42 reject of
`btrfs-ioctl-surface-r27.md` P2/P3 stands (its lines 14 and 31-32 re-read unchanged, `w1/AsmGate.md` §6).

### considerthese — cross-note correction propagation map (`considerthese/2026-10-26.md`, proposal 5, read 2026-10-26)

Mined for the round-42 SC1/SC3 withdrawals and SC4/SC5 narrowings (`w1/ConsiderMap.md`, built at `717b716a`): 34
dependent sites in `corpus/knowledge`, `SKILL.md`, `corpus/README.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md` plus 6
adjacent ones; 4 restated a withdrawn or narrowed proposition with no pointer (`corpus/README.md:410`,
`PROVINCE.md:239-244`, `SKILL.md:3914`, `:3918`), and `PROVINCE.md:243-244` asserted the opposite of the record's
0600 mode. Closed by append-only pointers this round: `corpus/README.md` "Round-43 coverage note", `PROVINCE.md`
"Round-43 note" (corrects :243-244), `SKILL.md` "Scrub record re-grounded — round 43" (supersedes the round-42 table
rows resting on SC1 and SC3, the `running` row included, and reads the `scrub_speed_max` row with the SC5 narrowing), the
round-42 entry's header line 4, and this round's `LOG.md` entry. Open (route): no gate reads a correction pointer
(`git grep superseded-in-part -- tools` → nothing); the map is the checklist until one does.

### Spot-check

Pending the non-author closure. Candidates below.

## Mistakes

| ID | Class | Evidence | Captured-by | Fix (and how it is shown able to fail) |
|---|---|---|---|---|
| R43-SIB-PIN-UNREPORTED | scope | Round 42's report named mori's moved pin and no tameshi pin (`grep -c tameshi .ufo/reports/round-42/tsukuroi.md` → 0) while `w2/AdjMoriPin.md` §3 had found the live `tameshi-shokunin/corpus/knowledge/service-optin-protocol.md:153` pin moved by the same round (`round-42-verifier-spotcheck.md` N1) | QUALITY 69 (a moved sibling pin is replayed and recorded, not absorbed silently) | The round-43 report carries a pin sweep (wave-1 `AdjPins`): every sibling `path:line` into a file this round moved, base and tip lines, and the two round-42 handoffs restated. Able to fail: `grep -c tameshi <report>` → 0 on the round-42 report (red), ≥ 1 on this round's |
| R43-MORI-ARITH | number-drift | The round-42 mori handoff gave "+6" and "+3" for one pin without naming their referents (N2); measured: content at census `:1097` (`c8efaa3f`) → `:1103` (`6951ead9`), mori's pin `1100-1115` was already 3 high against the base content (`w1/AdjPins.md` §3) | QUALITY 21 (a reader line number needs its snapshot) | One sentence per coordinate naming its starting revision (this round's report handoff). Able to fail: applying "+3" to the base content line (1097 → 1100) misses the tip content (1103) |
| R43-VERDICT-JSON-UNBOUND | vacuous | The round-42 binding read a plain first line, so JSON outputs carrying `"verdict": "holds"` bound nothing (`C2RevSC1`, `C2RevSC4`; N3) | QUALITY 90 named no accepted serialization | The round-43 counter binds the JSON `verdict_line` field or the first non-blank line, plus the report's first line; the seat prompt names that one form. Able to fail: control C2-K13 (report first line differs) and C2-K6 (mention) FAIL with `verdicts_ok 2` |
| R43-CAP-HEADER-DUP | landing | The round-42 capabilities table repeats its header (`SCORECARD.md:2630`, `:2632`) | none — no criterion read a rendered table (now QUALITY 92) | The round-43 table carries one header row; QUALITY 92 states the rule. Able to fail: the heading-bounded count `awk '/^## Capabilities — current full evidence set \(round 42\)/{f=1;next} /^## /{f=0} f&&/^\| Capability \|/{n++} END{print n+0}' SCORECARD.md` prints 2 (red); the same for round 43 must print 1 |
| R43-CENSUS-PROBE-COORDS | reference-drift | `R42-C1-CLASS-UNSWEPT` names single-line probes at census `:931, :969, :1051, :1426, :1501` (true at `44766208`); at `6951ead9` they sit at `:934, :972, :1054, :1429, :1504` (`w1/ScribeLesson.md`) | QUALITY 21 | Cite readers by content (`$CAP_OUT` piped into `head -n1`) plus revision. Able to fail: `sed -n '931p;969p;1051p;1426p;1501p' tools/tsukuroi-census.sh \| grep -c 'head -n1'` → 0 at the base |
| R43-L1-SCRATCH-STRAY | scope | The L1 left pre-wave scratch files in the shared round root `/fast/scratch/hyaku/tsukuroi-r43/` (a pre-fix `hybrid.sh` copy carrying the fail-open, `n.c`, fetched sources) where seats work (`w1/SentMisroot.md` F2); a seat import left `tools/__pycache__/*.pyc` in the lane, hidden by `.gitignore` (F1) | ROUND-PROMPT §7 (scratch discipline: one dir per seat, delete on exit) | The L1 removed the strays before wave 2 and the `.pyc` files before landing; L1 scratch goes under `…/tsukuroi-r43/L1/`. Able to fail: `ls /fast/scratch/hyaku/tsukuroi-r43/*.sh` lists the stray (red at sweep time) |

## Round-42 routed defects — round-43 disposition

1. **R42-C2-REGROUND** — C2: `corpus/knowledge/btrfs-scrub-record-r43.md` SR1, SR3 (re-grounded SC1/SC3 text) and SR6
   (the running-state limit at the kernel source), counted wave-2 reads; the round-42 entry's header line 4 points
   there (a header-reading sweep sees it; counter conjunct `pointer_ok`).
2. **R42-CAP-HEADER-DUP** — the round-43 capabilities table has one header row (Mistakes row above).
3. **R42-ADJ-TAMESHI-UNREPORTED** — the round-43 report carries the tameshi handoff and restates mori's with named
   referents (`w1/AdjPins.md` §3-4). New: the tameshi pin's text means the round-5 selftest block, which starts at census
   `:2425` at the tip (a 56-line block, `w2/AdjFinal.md`), not `:921-976` (the round-42 handoff's arithmetic was right, its referent wrong).
4. **R42-C1-COUNTER-AMEND** — done: the boot-chain fail-open (C1), a counter that refuses to run without `--scratch`,
   cleans on SIGINT/SIGTERM, runs production-identity legs (uid/gid via subuid map + `setpriv`) with values drawn per
   run, and frozen gated controls (K3 uid, K4 env, K5 name). Not done, with reason: the census `:743` lookup's selftest
   case and the single-line probe readers — C1's declared surface is `tools/boot-chain-audit.sh` only (causal
   separability); they stay routed to a census-surface round.
5. **R42-VERDICT-FORM** — the C2 binding counts one declared form (JSON `verdict_line` or first line) anchored, plus
   the report's first line; the wave-2 seat prompts name that form. Recorded limits from wave 1: padded or
   blank-line-prefixed lines and a contradictory JSON `verdict` field beside `verdict_line` still bind
   (`w1/C2MutBinding.md`); wave 2 audits every counted output for such contradictions by hand.

No `corpus/lessons/operator-*.md` exists (`w1/ScoutR42Defects-2.md` §6).

## Sources census

Start: `tsukuroi ok`, exit 0, 40 W04, 239 rows (`.ufo/waves/round-43/before/sources-census-start.txt`).

End: see the report's Sources & frontier section and `.ufo/waves/round-43/after/sources-census-final.txt`.

## Spot-check candidates for the non-author closure

One admit: SR6 (S240 ioctl.c:3126-3133 against the host EPERM, S241 capture.txt:6). One reject: the wave-1 claim
"the device id is never emitted" (`w1/C2DraftCritSR3.md` F1) against scrub.c:782-792, or the staged
`ext4-journal-guarantee-r32.md` (out of province).
