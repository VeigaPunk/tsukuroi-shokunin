# CN1Siblings — w1 report (connector: assimilation, considerthese, sibling overlap)

Seat CN1Siblings — L2 connector, tsukuroi-shokunin r64 (hyaku run 15), wave w1.
Full write-up with every command and output inline:
`.ufo/waves/round-64/after/connector-assimilation.md`.
Evidence files (separate, as required): `.ufo/waves/round-64/assimilation/reg-ids`,
`staged-ids`, `collisions`, plus `assim-receipt.txt` (the receipt copy of the scratch-only guard
fixture and the URL-keyed census; the scratch dir is deleted before this yield).

Read-only everywhere else. No package transaction, no service action, no mutating git/jj, no
sibling-repo write, no considerthese edit. Scratch
`/fast/scratch/hyaku/tsukuroi-r64/CN1Siblings` removed at yield.

## 1. SS10 id-collision check

Mandated commands run verbatim against the live registry and the staged package
(`/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md` — the repo is `shokuknow`;
`shokunow`/`shoknow` do not exist), rc=0 for each of the three:

| file | lines | range |
|---|---|---|
| `reg-ids` | **278** | S001–S278, contiguous, no gaps |
| `staged-ids` | **147** | S200–S346, contiguous, no gaps |
| `collisions` | **79** | exactly S200–S278 |

- **Collision count: 79** — the entire live tail from `S200` (the staged package's first id) to the
  registry's current end `S278`; 68 staged rows do not collide; 199 live rows are untouched.
- The collision is **genuine id drift, not duplicate content**: for all 79 colliding ids the staged
  row and the live row carry **different sources** (0/79 same; e.g. live `S200` = `mount(2)`,
  staged `S200` = `mkinitcpio(8)`; live `S201` = `fs/btrfs/ioctl.c`, staged `S201` =
  `alpm-hooks(5)`). Arithmetic renumbering is therefore not a valid fix.
- URL-keyed census of all 147 staged rows: **101 carry a source URL the live registry does not
  hold** (genuinely new material) and **46 duplicate a live URL under a different id** (e.g. staged
  `S279/S280/S281` = `errno(3)`, already live as `S202/S203/S204`). Re-staging without dropping
  those 46 would mint 46 new duplicate-url W04 rows.
- Trend: the same package was reported at 53 collisions (r48), 57 (r50/r52) and is now 79 —
  monotonically widening, because the lane keeps growing into the staged id space.

**Guard sanity: PASS.** A scratch fixture registry whose rows are indented by **2 spaces**,
including one id the staged set contains (`S300`), matched by the same `^ {0,3}\|` pattern, gives
`S001 S300 S999` from the grep and a **non-empty** fixture intersection (`S300` only). The
non-staged fixture ids (`S001`, `S999`) correctly do not fire, so the guard discriminates.
Window stated, not assumed: a **4-space** indented row is *not* matched (0 hits) — the pattern
covers indentation 0–3 only; both real files hold every row at indent 0 (measured 278/147 at
indent 0), so no live row is currently missed. Blind-spot probe: five staged ids (`S008`,
`S096`, `S097`, `S110`, `S111`) appear only inside cell prose, are correctly excluded as
non-row ids, and the live registry has zero such references.

**SS10 routing: mass id drift a read-only check cannot fix → L0 question filed, NOTHING adopted
from the package this round.** The L0 line drafted for the L1 to append (format
`tsukuroi | round-64 | <question>`) is in the connector write-up §1.6. It carries the headline
(147 staged rows, first id S200, 79 collisions), the 0/79 same-source finding, the
101-new/46-duplicate URL census, the warning that option (b) "ids continuing S279" would collide
with this round's own S279–S281 re-pins, and the three rulings to choose from (renumber-and-dedupe
campaign / re-stage only the 101 new-material rows / confirm quarantine). An L1-owned draft of the
same question already exists at `.ufo/waves/round-64/assimilation-l1/l0-draft-line.txt`
(read-only to me, not edited) and agrees on the headline; mine adds the three extra facts.

## 2. considerthese scan → one pick

All seven files read in full (2026-10-19, -20, -22, -23, -24, -25, -26). Every file's proposal
section is headed "proposals only, not acted on", so implementation evidence in
`corpus/ tools/ SKILL.md SCORECARD.md` decides; a 32-proposal evidence table is in the connector
write-up §2.

**Picked proposal: Counter-attack scoreboard** (`considerthese/2026-10-26.md`).

Drafted grounding line for the lesson:

> `considerthese/2026-10-26.md + 2026-11-03` — the prior state lacked it because the
> counter-attack scoreboard's last tallied row is round 50 (`SKILL.md` "Counter-attack scoreboard —
> rounds 40-41" and "— round 42 (continuation)"; `corpus/lessons/round-52.md` rows for rounds
> 38-50) while rounds 51 and 52 each fielded a mutant battery the ledger never counted (64 and 53
> wave files carrying KILLED/SURVIVED markers), no tool or gate re-reads the arms (`grep -rn "arms
> fielded" corpus/ SKILL.md` → 3 prose-table hits; `tools/` → 0), and the proposal's own question —
> are the hole's classes converging or only moving? — has had no new evidence for thirteen rounds.
> Round 64 supplies the first row since then, for a new class of frozen counter
> (`tools/check-line-endings-r64.py`: 5 mutants from the mutation-tester seat, plus the reviewer's
> edge attacks and the critic's do-nothing controls).

Why not the other two candidates named in the item:
- **Seat-harm incident log** — the ledger (r45 lesson, 10 incidents; r46 row) stopped after round
  46; rounds 47–63 carry zero rows. This round produced no seat-to-seat damage: the one
  lane-state event (the CRLF regression of `corpus/SOURCES.md`, measured by this seat at 18:47Z,
  repaired by the owning seat at ~18:56Z) is a stale-blob re-materialisation on a detached HEAD,
  not one seat damaging another. Logging it would need a taxonomy change, not a row.
- **Downstream patch-offset check** — real, but it is a different work item: the round-42 check
  answered "do Arch's packaging patches shift the line pins this lane cites" for pacman and
  btrfs-progs and never became a re-runnable tool (script still in a wave dir; `tools/` 0 hits).
  Its kernel-source instance is measured below and filed as a finding for the L1, not mined as this
  round's proposal.

## 3. Sibling overlap

- **No crossing.** C3's measurements are installed-file byte reads (`/usr/lib/initcpio/hooks/*`,
  `/usr/lib/initcpio/functions`), package versions (`pacman -Q` → mkinitcpio 42.2-1, plymouth
  26.134.222-3, limine-mkinitcpio-hook 1.40.0-2) and public-upstream `curl` comparisons — host
  OS/package diagnosis plus public-source comparison, which mori's cross-lane table
  (`mori-shokunin/PROVINCE.md:66`) attributes to tsukuroi. kaidoku
  (`PROVINCE.md:3-6, :50`) and revenger (`PROVINCE.md:3-7, :44`) both declare shipped-artifact
  reverse engineering; artifact internals (package-archive extraction, binary disassembly, UKI
  payload unpacking) would cross into their surface and ADJ-06 routes it to the integrator with
  "request an ownership ruling before any RE work" (`tsukuroi-shokunin/PROVINCE.md:51`). The
  kaidoku/revenger arbitration remains **unresolved**; both sibling declarations are also
  host-stale (revenger's header still carries Windows-era paths and "absent on this host"
  entries dated 2026-10-31) — flagged for the integrator, not claimed by this seat.
- **ADJ-04 boundary for the C2 memory/journal reads — attribution stays with mori.** tsukuroi
  keeps the OS finding and hands over capture time, boot/window, the exact counter/PSI command
  and exit, and the observed value, distinguishing presence, cumulative count and dated event;
  mori owns the kill/OOM catalog-ID and signal-11 coredump classification and the fleet
  attribution ("fleet attribution is its correlation, not tsukuroi's",
  `mori-shokunin/PROVINCE.md:24`). The C2 battery's journal-err count, `coredumpctl list` count
  and per-identifier breakdown are cumulative presence counts and are legitimate drift-register
  cells; they must not be converted into attribution ("the wave caused these"), must not sum the
  user and system scopes, and must not be merged with mori's MESSAGE_ID-scoped counts. The census's
  own `HANDOFF ADJ-04 mori …` lines carry `state=prepared` only (`PROVINCE.md:193`).

## 4. Findings for the L1 (not adopted by this seat)

1. **C3 re-pin targets are byte-identical upstream↔installed** — sha256 `de852646…` (plymouth) and
   `eeac1ed3…` (btrfs-overlayfs) match on both sides; `/new_root` sits at line 11 and line 4 in
   both. The S280/S281 line citations will be correct as written.
2. **A corpus-anchor defect the round-42 patch-offset check never covered.** 22 registry rows pin
   upstream kernel **v7.2** file:line anchors and 20 of them assert "for the host kernel 7.2.11"
   while the host runs `7.2.11-arch1-1`. Upstream v7.2 → v7.2.11 comparison over the twelve cited
   kernel files: `fs/btrfs/ioctl.c` +8 lines, `fs/btrfs/volumes.c` +4, `kernel/module/main.c` +16;
   the other nine are byte-identical. Two instances: **S201** anchors "create_snapshot, lines
   1178-1186" but those lines are inside `__btrfs_ioctl_snap_create` (def :1138), not
   `create_snapshot` (def :735, which contains no ownership check in v7.2 or v7.1), and the same
   9-line block sits at 1185-1193 in v7.2.11 (**+7**); **S132** anchors six `volumes.c` ranges that
   moved +4. Downstream: `mount-errno-contract-r37.md:3,19` repeats the "create_snapshot()"
   attribution, `storage-health-r26.md:23,37` cites the shifted line numbers. The L1 owns
   integration; row text is S1Scribe's scope.
3. **C1 collateral, measured not assumed:** at 18:47Z `corpus/SOURCES.md` was back to 381 CR lines
   (byte-identical to the committed `2f3061ef` blob; census rc 1, E12=278). The owning seat
   reported a repair at ~18:56Z; re-measured after that: all three files CR-lines = 0, census
   `rc 0`, E-codes 0, W04 = 42, verdict `tsukuroi ok`. No action taken by this seat.

## 5. Verdicts

| asked | verdict |
|---|---|
| collision count | **79** (staged 147, registry 278, span S200–S278); 0/79 same-source; 101 new-material / 46 live-duplicate by URL |
| guard-sanity result | **PASS** — 2-space-indented fixture row caught, fixture intersection non-empty (`S300`); window is 0–3 spaces (4-space row unmatched); both real files all rows at indent 0 |
| picked proposal | **Counter-attack scoreboard** (`considerthese/2026-10-26.md + 2026-11-03`), grounded line drafted |
| overlap verdict | **no crossing** (ADJ-06 boundary held); ADJ-04 attribution stays with mori |

Scratch deleted: `/fast/scratch/hyaku/tsukuroi-r64/CN1Siblings` (`rm -rf` at yield).
