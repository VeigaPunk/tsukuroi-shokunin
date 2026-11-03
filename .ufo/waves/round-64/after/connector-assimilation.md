# CN1Siblings — connector: assimilation (SS10), considerthese survey, sibling overlap

Seat CN1Siblings (L2 connector, tsukuroi r64 hyaku run 15, wave w1). Read-only everywhere except
this file, the three `$A` id-list files, and the w1 report path. Lane repo:
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Scratch (deleted before yield):
`/fast/scratch/hyaku/tsukuroi-r64/CN1Siblings`. Receipts: `.ufo/waves/round-64/assimilation/`
(`reg-ids`, `staged-ids`, `collisions`, `assim-receipt.txt`).

All commands below are read-only (`grep`, `comm`, `wc`, `awk`, `python3` over files, `curl` of
public upstream source, `pacman -Q`, `uname`). No package transaction, no service action, no
mutating git/jj anywhere, no write outside the paths named above.

---

## 1. SS10 id-collision check (assimilation contract, operator directive 2026-10-24)

### 1.1 The three mandated commands, verbatim

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
rc=0
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunnow/merge/tsukuroi/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
rc=0
$ comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
rc=0
```

Path note, verified not assumed: the staged package lives at
`/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md` (the repo is `shokuknow`; the
`shokunow`/`shoknow` spellings do not exist — `ls /home/vgpnk/Projects/` shows `shokuknow` and a
separate empty `shokunnow/` tree). The package file is 178472 B, mtime `2026-10-24 23:33:20 -0300`,
and `git -C /home/vgpnk/Projects/shokuknow status --porcelain merge/tsukuroi/SOURCES.append.md`
prints ` M` (modified, uncommitted in that repo).

### 1.2 Counts (the required numbers)

```
$ wc -l reg-ids staged-ids collisions
 278 .../.ufo/waves/round-64/assimilation/reg-ids
 147 .../.ufo/waves/round-64/assimilation/staged-ids
  79 .../.ufo/waves/round-64/assimilation/collisions
 504 total
```

- **live registry ids: 278** (`S001`…`S278`, contiguous, no gaps — verified by an awk contiguity
  scan that printed no gap line).
- **staged package ids: 147** (`S200`…`S346`, contiguous, no gaps).
- **collisions: 79** — exactly the block `S200`…`S278` (head `S200`, tail `S278`; a numeric
  contiguity scan shows one run from 200 to 278 inclusive = 79 ids).
- Non-colliding staged ids: 68 (`S279`…`S346`). Registry-only ids: 199 (`S001`…`S199`).

**Classification (the item's "LARGE"):** the collision count is **79**, i.e. 79 of the 147 staged
rows (54%) collide with live registry rows, and the colliding span is the *entire* live tail from
`S200` up to the registry's current end `S278`. The staged package's first id `S200` is exactly the
live registry's first post-`S199` id: the package was staged against a registry that ended at
`S199`, and the lane has since grown by 79 rows into the same id space.

### 1.3 The collision is real id drift, not a duplicate-content artifact

Every colliding id carries **different source material** on the two sides (0 of 79 are the same
row):

```
$ python3 (id -> first URL on each side, over the 79 colliding ids)
colliding ids: 79   same-source-on-both-sides: 0   different-source: 79
   S200 live  : https://man7.org/linux/man-pages/man2/mount.2.html
   S200 staged: https://man.archlinux.org/man/mkinitcpio.8
   S201 live  : https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/ioctl.c
   S201 staged: https://man.archlinux.org/man/alpm-hooks.5
```

Consequence for any adoption path: the package is not "79 rows that happen to be numbered the
same" — it is 79 *different* documents sharing ids with 79 live documents. Arithmetic renumbering
(`staged id + 79`) would be wrong in the general case, because the package is not a superset of
the live registry in id order.

### 1.4 URL-keyed material census of the whole package (what is actually new)

```
$ python3 (key every staged row by its source URL; compare against live registry URLs)
staged rows: 147
  colliding ids (same id in live registry): 79
    of which the staged URL already exists in live under another id: 12
    of which the staged URL is absent from live: 67
  non-colliding staged ids: 68
    of which the source URL already exists in live under another id: 34
    of which the source URL is absent from live (new material): 34
    new-material ids: S283 S284 S285 S289 S290 S291 S292 S294 S295 S297 S298 S300 S302 S303
                      S306 S311 S313 S315 S316 S321 S324 S325 S328 S329 S330 S334 S336 S339
                      S340 S342 S343 S344 S345 S346
    live-duplicate ids (would stay W04 after any renumber):
                      S279 S280 S281 S282 S286 S287 S288 S293 S296 S299 S301 S304 S305 S307
                      S308 S309 S310 S312 S314 S317 S318 S319 S320 S322 S323 S326 S327 S331
                      S332 S333 S335 S337 S338 S341
```

Totals: **101 staged rows carry a source URL the live registry does not hold** (67 colliding +
34 non-colliding) — that is the genuinely new material. **46 staged rows duplicate a live source
URL under a different id** (12 colliding + 34 non-colliding), e.g. the package's `S279/S280/S281`
are `errno(3)` rows whose URL the live registry already holds at `S202/S203/S204`. Re-staging
without dropping those 46 would mint 46 new duplicate-url rows — exactly the warning class the
census already emits today (`W04`, 42 instances at this tree).

### 1.5 Guard sanity (the S10 proven-guard duty) — PASS, with its window stated

Scratch fixture registry whose rows are indented by **2 spaces** and which includes one id the
staged set contains (`S300`):

```
$ cat fixture-registry.md
# fixture registry

| Id | Note |
|---|---|
  | S001 | fixture row, 2-space indented |
  | S300 | fixture row, 2-space indented, id present in staged set |
  | S999 | fixture row, 2-space indented, not in staged set |

$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' fixture-registry.md | grep -oE 'S[0-9]+' | sort
S001
S300
S999
rc=0
$ comm -12 fixture-reg-ids staged-ids
S300
rc=0        (fixture-collisions lines: 1 — NONEMPTY)
```

**Guard-sanity result: PASS.** The `^ {0,3}\|` pattern catches 2-space-indented rows, and the
intersection with the staged set is non-empty, so the same command pair that produced 79 live
collisions would have produced a collision on a 2-space-indented registry too. The fixture's
non-staged id `S999` correctly does not intersect, and `S001` (not in the staged set) correctly
does not either — so the guard is discriminating, not merely always-firing.

**The guard's window, stated rather than assumed.** A second fixture with a **4-space** indented
row is *not* matched:

```
$ cat fixture-indent4.md
| Id | Note |
|---|---|
    | S300 | four-space indented row, outside the 0-3 space window |

$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' fixture-indent4.md | grep -oE 'S[0-9]+' | sort
(no output)
$ wc -l fixture4-ids
0
```

So the mandated pattern detects indentation 0–3 only. Measured indent census of the two real
files: every row is at indent **0** (registry `278 0`; staged `147 0`), so no live row is
currently missed by that window — the limitation is stated for future shape changes, not a current
defect.

**Blind-spot probe (ids present but not row-leading).** The pattern is anchored to a row-leading
id; ids appearing only inside prose cells are correctly excluded:

```
$ comm -23 (all S-ids in the staged file) (row-leading staged ids)
S008
S096
S097
S110
S111
rc=0
$ comm -23 (all S-ids in the registry) (row-leading registry ids) | wc -l
0
```

The five staged ids appear inside cells of rows `S200` (`S008` mention) and `S211`
(`S096, S097, S110, S111` — "the lane's existing plymouth rows … remain current"). They are
references, not registry rows, and must not be treated as staged ids. The live registry contains
zero such references.

### 1.6 SS10 routing and the L0 line

Mass id drift is not fixable by a read-only check: renumbering 147 rows by document (URL-anchored,
not arithmetic) is a multi-round editorial campaign, and this round's claims C1/C2/C3 are frozen
before any after-measurement. **SS10 routing therefore applies: an L0 question is filed and
NOTHING is adopted from the staged package this round.** The lane's own record already carries the
same verdict for the same package in earlier rounds — `SCORECARD.md:3094` ("53 id collisions
S200-S252 … nothing is appended from it"), `SCORECARD.md:3218` (57), `SCORECARD.md:3271` (57) —
so the drift is monotonically widening and the quarantine is the standing, correct state.

**L0 line drafted for the L1 to append** (format `tsukuroi | round-64 | <question>`):

```
tsukuroi | round-64 | The staged corpus-expansion-1 package merge/tsukuroi/SOURCES.append.md (147 rows, ids S200-S346, staged 2026-10-24) collides with the live registry's S200-S278: 79 ids, and every one of the 79 carries a different source document on the two sides (0 of 79 are the same row), so arithmetic renumbering is not a valid fix. A URL-keyed census shows 101 of the 147 staged rows carry a source URL the registry does not hold (genuinely new material) and 46 duplicate a live URL under another id (e.g. staged S279/S280/S281 = errno(3), already live as S202/S203/S204), so re-staging without dropping those 46 would mint 46 new duplicate-url W04 rows. Rule the adoption path: (a) authorize a dedicated multi-round renumber-and-dedupe campaign keyed by source URL, (b) authorize re-staging only the 101 new-material rows against the current registry (ids continuing S279, which this round's own S279-S281 re-pins will occupy), or (c) confirm the package stays quarantined. Until ruled, tsukuroi adopts nothing from merge/tsukuroi per the SS10 mass-id-drift routing; the guard check itself passes (2-space-indented fixture row caught; the 0-3 space window misses 4-space rows, and both real files hold every row at indent 0). Evidence: .ufo/waves/round-64/assimilation/{reg-ids,staged-ids,collisions,assim-receipt.txt}.
```

(An L1-owned draft of the same L0 question already exists at
`.ufo/waves/round-64/assimilation-l1/l0-draft-line.txt` — read-only to this seat, not edited. It
agrees with this seat on the headline: 147 staged rows, first id `S200`, 79 collisions, and it
offers the same three options (a)/(b)/(c); this draft adds the 0/79 same-source finding, the
101-new / 46-duplicate URL census, and the `S279-S281` occupancy warning for option (b).)

---

## 2. considerthese scan — all seven files read, implementation evidence checked

All seven files read in full: `2026-10-19.md`, `2026-10-20.md`, `2026-10-22.md`, `2026-10-23.md`,
`2026-10-24.md`, `2026-10-25.md`, `2026-10-26.md`. Every file's proposal section is headed
"Self-improvement ideas (proposals only, not acted on)" — so *as written* all 32 proposals across
the seven files are still marked proposed, and the honest test is repository evidence.

Implementation-evidence grep across `corpus/`, `tools/`, `SKILL.md`, `SCORECARD.md` for each
proposal's name/idea (counts are hits in those four trees):

| proposal (file) | repo evidence | status |
|---|---|---|
| Counter-attack scoreboard (`2026-10-26.md`) | `SKILL.md:3833` (rounds 40-41), `SKILL.md:3935` (round 42 continuation), `corpus/lessons/round-41.md:99`, `corpus/lessons/round-52.md:64-102` (rounds 38-50 table) | **partially implemented; ledger stale** |
| Seat-harm incident log (`2026-10-26.md`) | `corpus/lessons/round-45.md:124-166` (10 incidents, rounds 37-44), `corpus/lessons/round-46.md:73` (R46-SEAT-WROTE-LANE-FILES) | implemented once; **no rows for rounds 47-63** |
| Downstream patch-offset check (`2026-10-26.md`) | `corpus/lessons/round-42.md:53-58`, notes in `corpus/knowledge/{pacman-hook-order-r38.md:159, pacman-transaction-order-r39.md:87, alpm-package-anatomy-r41.md:104}` | implemented for pacman/btrfs-progs **only**; never re-run; kernel source rows never checked |
| Burst-aware reading (`2026-10-26.md`) | 1 hit | not implemented (out of scope for this round) |
| Cross-note correction propagation map (`2026-10-26.md`) | 11 hits | mined in round 43 |
| Upstream release watch (`2026-10-24.md`) | 0 hits | not implemented — *but* this round's C3 **is** that watch firing (mkinitcpio v42.2), so the round satisfies it directly |
| Routed-debt carry-over check (`2026-10-24.md`) | 1 hit | not implemented |
| Seat-loss tally (`2026-10-24.md`) | 0 hits | not implemented |
| Live-harm flag for env changes (`2026-10-24.md`) | 1 hit | not implemented (round-36 subject, closed) |
| Claim-arc length (`2026-10-24.md`) | 0 hits | not implemented |
| Probe lineage table (`2026-10-25.md`) | 4 hits | partially implemented |
| Evidence-weight watch (`2026-10-25.md`) | 2 hits | partially implemented |
| Quiet-day mode / next-round pickup sheet (`2026-10-25.md`) | 0 hits | not implemented |
| Missed-run catch-up, scope-violation trend line, receipt-first verification, volume-aware reading (`2026-10-22.md`) | 0 / 1 / 0 / 0 hits | not implemented |
| Verified-rate ledger, round-velocity table, late-evidence contradiction watch, env allow-list drift check, coverage-frontier map (`2026-10-23.md`) | 8 / 0 / 4 / 0 / 0 hits | partly implemented |
| Author-versus-verifier calibration ledger, daily source-quote sampling, signal-first review path, waived-obligation tracker (`2026-10-20.md`) | 4 / 0 / 0 / 0 hits | mostly not implemented |
| Daily pin-integrity check, promotion-debt ledger, stagnation watch, cross-lane receipt watch, draft-PR awareness (`2026-10-19.md`) | 0 / 0 / 57 (`saturation`, unrelated) / 0 / 0 hits | not implemented |

### 2.1 The one proposal that best fits THIS round: **Counter-attack scoreboard**

Grounding line the lesson will cite:

```
considerthese/2026-10-26.md + 2026-11-03 — the prior state lacked it because the scoreboard's
last tallied row is round 50 (SKILL.md "Counter-attack scoreboard — rounds 40-41" and "— round 42
(continuation)", corpus/lessons/round-52.md rows for rounds 38-50) even though rounds 51 and 52
each fielded a mutant battery that the ledger never counted (64 and 53 wave files carrying
KILLED/SURVIVED markers), no tool or gate re-reads the arms (grep -rn "arms fielded" corpus/ SKILL.md
-> 3 hits, all prose tables; tools/ -> 0), and the proposal's own question — are the hole's classes
converging or only moving? — has therefore been unanswered since round 50.
```

Why this proposal and not the other two named in the item:

- **Counter-attack scoreboard — fits the round's own seat mix.** This wave fields a dedicated
  mutation-tester seat (`MT1Guard`: five named mutants M1-M5 against the new frozen counter
  `tools/check-line-endings-r64.py`, each scored KILLED/SURVIVED with a named missing selftest case),
  a reviewer seat attacking the same counter's edges (`R1C1Rev`: allowlisted-path, symlink-into-
  `.ufo/`, empty/binary file), a critic seat running do-nothing controls (`CritC23`), and a source
  reviewer (`R2Sources`). The scoreboard's schema — *counter, round, arms fielded, arms that reached
  PASS, class that beat it* — is precisely the shape of what those seats produce. The lane's own
  r52 pattern read is the payoff: "the classes move, they do not disappear", r46-r50 every new
  admission/matcher counter beaten by "a liar or a forged bundle". Round 64 adds a *new class of
  counter* (a byte-level line-ending guard with a selftest) to that series, which is exactly the
  data the next table row needs.
- **Seat-harm incident log — nothing in this round to log.** The ledger stopped at round 46
  (rounds 47-63: zero seat-harm rows; the r45 lesson itself notes "no gate reads this ledger").
  This round's wave produced no seat-to-seat damage event: the one lane-state event (a CRLF
  regression of `corpus/SOURCES.md`, measured by this seat at 18:47Z and repaired by the owning
  seat at ~18:56Z) is a stale-blob re-materialisation on a detached HEAD, not one seat damaging
  another. Logging it would need a taxonomy change, not a row.
- **Downstream patch-offset check — real, but it belongs to a different lane of work.** The
  round-42 check answered "does Arch's packaging patch shift the upstream line pins this lane
  cites" for pacman and btrfs-progs. It was never extended to the *kernel-source* rows, and it
  never became a re-runnable tool (the script stays in a wave directory,
  `.ufo/waves/round-42/w1/ConsiderPatchOffset/patch-offset.py`; `tools/` has 0 hits). This seat
  measured the kernel-side instance read-only while doing this item's overlap work, and it is
  reported in §3.3 below as a finding for the L1 — but as a *corpus-anchor* correction, not as this
  round's mined proposal.

### 2.2 The draft grounding line, formatted as the lesson will cite it

`considerthese/2026-10-26.md + 2026-11-03` — "the prior state lacked it because the counter-attack
scoreboard's last tallied row is round 50 while rounds 51 and 52 each fielded an untallied mutant
battery, so the proposal's own question (converging or moving the hole?) has had no new evidence
for thirteen rounds; round 64 supplies the first row since then, for a new class of frozen counter
(`tools/check-line-endings-r64.py`: 5 mutants from the mutation-tester seat, plus the reviewer's
edge attacks and the critic's do-nothing controls)."

---

## 3. Sibling overlap

### 3.1 kaidoku / revenger declared ownership (headers only, read-only)

- `kaidoku-shokunin/PROVINCE.md:3-6` — "**Domain:** reverse engineering of shipped artifacts with
  REA on this Linux host — native ELF through the Ghidra 12.1.4 provider, Electron/ASAR/JavaScript
  bundles, archives and packages; evidence-first static analysis…". Its surface table includes an
  "Archive/package inventory" row (`:50`) covering the pacman `.pkg.tar.zst` cache, per-file
  `.MTREE` sha256, and `pacman -Qkk` verify.
- `revenger-shokunin/PROVINCE.md:3-7` — "Owns: reverse engineering of shipped artifacts — native
  binaries, managed assemblies, Electron/JavaScript packages, Android APKs, archives, firmware,
  browser/Electron runtime evidence — using the REA skill and its toolset". `:44` refuses
  "live-target execution beyond the declared target and lifecycle"; it also refuses
  "harness/evidence auditing (harness-integrity, gate-evidence, rlm-dispatch)".

**Overlap verdict for this round's C3 measurements: NO crossing.** The C3 measurements are
(a) reads of installed *text* files under `/usr/lib/initcpio/hooks/` and
`/usr/lib/initcpio/functions`, (b) installed package *versions* (`pacman -Q mkinitcpio plymouth
limine-mkinitcpio-hook`), and (c) byte comparison against public upstream source fetched by
`curl`. None of these inspect artifact internals, binary semantics, or package-archive contents;
they are host OS/package diagnosis plus public-source comparison, which this lane owns
(mori-shokunin/PROVINCE.md:66 records "tsukuroi | Owns host OS, package, systemd-unit, driver,
firmware, and boot diagnosis"). Two boundaries to hold explicitly:

1. **ADJ-06 boundary (the crossing that must not happen).** The moment a C3 step moves from the
   installed file's *bytes* to the *artifact's internals* — extracting a package archive
   (`.pkg.tar.zst`), disassembling the shipped `plymouth`/`limine` binaries, or unpacking a UKI
   initramfs to inspect payloads — it enters the surface kaidoku and revenger both declare, and
   ADJ-06 routes it to "protocol integrator — kaidoku/revenger ownership unresolved" with the
   standing instruction "Request an ownership ruling before any RE work; do not invoke a target or
   forward raw cores" (tsukuroi PROVINCE.md:51). No such step occurred this round; the measured
   comparison stayed at file-bytes level.
2. **The sibling declarations are themselves stale on this host.** revenger's PROVINCE header
   still carries Windows-era host facts (`C:/Users/jpvei/tools/ghidra_12.1.4_PUBLIC`,
   "absent on this host, 2026-10-31" for ghidra/ida/binwalk/pwntools, `D:/Projects` non-existent)
   and a `rea` 6.8.0 pin dated 2026-10-31; kaidoku's header describes a Linux host with Ghidra
   12.1.4 at `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`. The lane's own ADJ-06 row and the
   round-19 anchor correction (`PROVINCE.md:152`) both record that the kaidoku/revenger arbitration
   is **unresolved** and that the integrator owns the ruling. Observation for the integrator, not a
   claim: whichever sibling owns the mechanism, the current declarations disagree about which host
   and which RE surface is live, and the round-64 C3 work did not need either of them.

### 3.2 ADJ-04 boundary for the C2 memory/journal reads — attribution stays with mori

Per `tsukuroi-shokunin/PROVINCE.md:49` (ADJ-04) and `:125` (OUT-005), and
`mori-shokunin/PROVINCE.md:24,37,66`:

- tsukuroi keeps the **OS finding** on its journal and oom planes and hands over: capture time,
  boot/window, the exact counter or PSI command and its exit, and the observed value — explicitly
  "distinguish presence, cumulative count and dated event. Request correlation, not a claim that a
  wave caused OOM".
- **mori owns** kill/OOM catalog-ID records and signal-11 coredump classification from separately
  labelled user/system journals, and "fleet attribution is its correlation, not tsukuroi's".
- The two counting bases differ and are not interchangeable: mori's counts use MESSAGE_ID per
  journal scope, tsukuroi's census counts by message text and SYSLOG_IDENTIFIER over the boot
  window — and mori's scope labels are "never summed" (`mori-shokunin/PROVINCE.md:24`).

Applied to this round's C2 battery (`E2Probes` probes p8/p10 and `SC1Host`'s recon): the journal
err-entry count, the `coredumpctl list` count and the per-identifier breakdown are **cumulative
counts of presence**, and they are legitimate drift-register cells (stored "238 err entries" vs
live; stored "198 coredump entries" vs live). What tsukuroi must not do in the drift register is
convert them into attribution: no "the wave caused these entries", no summing the user and system
scopes, no merging its own text/SYSLOG_IDENTIFIER count with mori's MESSAGE_ID count. The lane's
census keeps this honest already by printing `HANDOFF ADJ-04 mori …` lines with `state=prepared`
only — prepared, not reported, acknowledged, accepted or resolved (`PROVINCE.md:193`), and mori
declares no intake format for them.

### 3.3 A related measurement made while checking overlap (not a C3 claim — a corpus-anchor finding)

While checking whether this round's C3 measurements touch a sibling's surface, this seat also
checked the *corpus anchor* form of the C3 re-pins and found two things the L1 should see. Both
are read-only measurements, both are stated as findings, neither is adopted here.

**(a) The C3 re-pin targets are byte-identical between installed and upstream.** The two files
C3 re-pins (S280 limine master `btrfs-overlayfs`, S281 plymouth `main`) match their installed
copies exactly:

```
$ sha256sum up-plymouth.txt up-btrfs-overlayfs.txt /usr/lib/initcpio/hooks/plymouth /usr/lib/initcpio/hooks/btrfs-overlayfs
de852646e615e06d4125eb2e646d0528d1e349bd9e9877c08c5d32c43d288b6f  up-plymouth.txt
eeac1ed326f5c6fed2e47bbb596d76c9c4b0020be30c3b3c58f6b3a4fa093dcf  up-btrfs-overlayfs.txt
de852646e615e06d4125eb2e646d0528d1e349bd9e9877c08c5d32c43d288b6f  /usr/lib/initcpio/hooks/plymouth
eeac1ed326f5c6fed2e47bbb596d76c9c4b0020be30c3b3c58f6b3a4fa093dcf  /usr/lib/initcpio/hooks/btrfs-overlayfs
$ diff up-plymouth.txt /usr/lib/initcpio/hooks/plymouth            -> IDENTICAL
$ diff up-btrfs-overlayfs.txt /usr/lib/initcpio/hooks/btrfs-overlayfs -> IDENTICAL
$ grep -n '/new_root' up-plymouth.txt up-btrfs-overlayfs.txt
up-plymouth.txt:11:  plymouth update-root-fs --new-root-dir=/new_root
up-btrfs-overlayfs.txt:4:	root_mnt="/new_root"
```

The `/new_root` line numbers the re-pin rows will cite (11 and 4) are the same upstream and
installed. `pacman -Q mkinitcpio plymouth limine-mkinitcpio-hook` → `mkinitcpio 42.2-1`,
`plymouth 26.134.222-3`, `limine-mkinitcpio-hook 1.40.0-2`.

**(b) A corpus-anchor defect the round-42 patch-offset check never covered.** The registry pins
22 rows to upstream kernel **v7.2** file:line anchors, and 20 of those rows assert "for the host
kernel 7.2.11" in their scope cell. The host runs `uname -r` = `7.2.11-arch1-1`
(`pacman -Qi linux` → `7.2.11.arch1-1`). Comparing upstream v7.2 against upstream v7.2.11 for the
twelve kernel files the registry cites:

```
fs/btrfs/ioctl.c:          DRIFT (v7.2 5670 lines -> v7.2.11 5678 lines, delta 8)
fs/btrfs/volumes.c:        DRIFT (v7.2 8976 -> 8980, delta 4)
kernel/module/main.c:      DRIFT (v7.2 3988 -> 4004, delta 16)
fs/btrfs/sysfs.c:          SAME   fs/btrfs/block-rsv.c: SAME   mm/oom_kill.c: SAME
kernel/sched/psi.c:        SAME   include/linux/psi.h: SAME   include/linux/panic.h: SAME
kernel/panic.c:            SAME   kernel/module/signing.c: SAME
include/uapi/asm-generic/errno-base.h: SAME
```

Two concrete instances:

- **S201** (`corpus/SOURCES.md:210`) anchors "create_snapshot, lines 1178-1186, kernel tag v7.2".
  Two defects in one cell: (i) at v7.2 lines 1178-1186 lie inside `__btrfs_ioctl_snap_create`
  (def at :1138), **not** inside `create_snapshot` (def at :735) — the quoted EPERM/EXDEV
  ownership block is in the ioctl wrapper, and `create_snapshot` contains no
  `inode_owner_or_capable` / "own subvolumes only" text at all (checked over the whole function
  body, v7.2 and v7.1); (ii) at v7.2.11 that identical 9-line block sits at 1185-1193, a **+7 line
  shift** (`diff` of the two ranges: identical). The downstream consumer
  `corpus/knowledge/mount-errno-contract-r37.md:3,19` repeats the "create_snapshot()" attribution.
- **S132** (`corpus/SOURCES.md:138`) anchors six `fs/btrfs/volumes.c` ranges (8186-8227, 8290-8348,
  8351-8354, 8422-8436, 8438-8456, 8458-8495) at tag v7.2 while its scope says "for the host
  kernel 7.2.11"; the file grew by 4 lines before those anchors in v7.2.11 (v7.2:8186
  `static int btrfs_device_init_dev_stats(` = v7.2.11:8190). Downstream consumer
  `corpus/knowledge/storage-health-r26.md:23,37` cites those line numbers verbatim.

This is the r42 proposal's exact question in a surface it never examined (kernel sources rather
than Arch-packaged pacman/btrfs-progs), and it is directly load-bearing for the round's own C2
freshness claim about the host's kernel upgrade. **It is filed here as a finding for the L1; this
seat adopts nothing and edits no corpus file** (row text is S1Scribe's scope; the L1 integrates).

---

## 4. Report summary

- **Collision count: 79** (staged `S200`–`S346` = 147 rows; live registry `S001`–`S278` = 278
  rows; colliding span `S200`–`S278`; 68 staged rows do not collide). 0 of the 79 colliding ids
  carry the same source on both sides — genuine id drift. URL-keyed: 101 staged rows are new
  material, 46 duplicate a live URL under another id.
- **Guard-sanity result: PASS** — a 2-space-indented fixture row (`S300`, present in the staged
  set) is caught and the fixture intersection is non-empty (`S300`); the non-staged fixture ids
  correctly do not fire. The pattern's window is 0–3 spaces (a 4-space row is not matched); both
  real files hold every row at indent 0, so nothing is currently missed.
- **Picked proposal: Counter-attack scoreboard** (`considerthese/2026-10-26.md + 2026-11-03`) —
  the wave fields exactly the arms its schema counts (MT1Guard's 5 mutants, R1C1Rev's edge attacks,
  CritC23's controls), and the ledger's last row is round 50.
- **Overlap verdict: no crossing.** C3's measurements stay at installed-file bytes + package
  versions + public upstream source; artifact-internals RE would cross into the unresolved
  kaidoku/revenger ADJ-06 question and must be routed to the integrator (and both sibling
  declarations are themselves host-stale). ADJ-04: attribution stays with mori — tsukuroi keeps
  the OS counts as presence/cumulative counts and requests correlation; it does not attribute.
- **C1 collateral observation (not this seat's work, no action taken here):** at 18:47Z this seat
  measured `corpus/SOURCES.md` back to 381 CR lines (byte-identical to the committed `2f3061ef`
  blob), census `rc 1` with E12=278; the owning seat reported a repair at ~18:56Z. Re-measured
  after that report: `corpus/SOURCES.md`, `SKILL.md`, `SCORECARD.md` all CR-lines = 0, census
  `rc 0`, E-codes 0, W04 = 42, verdict `tsukuroi ok`.
