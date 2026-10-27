VERDICT: draft

# Seat ConnFrontierFinal — item R-9: round-45 planned row (draft, refines w1/ConnFrontier.md)

Lane: tsukuroi-shokunin; round 44, wave w2. Basis: `SCORECARD.md:2746-2787` (round-44 declaration,
freeze `1d2afffe`, base `98020ece`, integrated tip under test `8eee79db`, working tip `3a1c6b5c`);
`.ufo/waves/round-44/w1/ConnFrontier.md` (w1 draft, written at tip `ff2c264a`);
`corpus/lessons/round-44.md` (routed/open items); `PROVINCE.md:256-279` (round-44 promotion);
w1 counter findings `w1/C2RevCounter.md` F1-F3 and `w1/C2MutBinding.md` F1/F4; live lane files read
at `3a1c6b5c`. Read-only: I ran no counter, census, audit or host command (planning seat); receipt:
`w2/ConnFrontierFinal/census-readers-and-counter-gaps-tip.txt` (grep/sed evidence only).

## 1. Verified anchors (evidence; all path:line at tip `3a1c6b5c`)

- Ordinals unchanged: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8;
  depth and adjacency tied lowest; saturation 9 / window 3; adjacency unclaimable — recipient-side
  acknowledgement/acceptance/closure is not lane-producible (`PROVINCE.md:77-79`; ADJ-06 unresolved
  `PROVINCE.md:51,79-80`; mori has no intake format for ADJ-04 `PROVINCE.md:193`; no sibling declares
  storage-integrity ownership).
- `tools/tsukuroi-census.sh` is 3442 lines at tip; `probe_scrub_record` at `:1965`, SCRUB line emitted
  at `:2039`, grammar `:387`; nine `(R44-C1)` selftest cases at `:3232-3319` (selftest 148 cases at
  tip per the declaration's 132 -> 148 hardening note).
- **Census readers still routed** (item's named content). `corpus/lessons/round-44.md` §3 keeps item 3
  routed "planned for a census-surface round (round-45 planned row)"; the round-44 declaration
  (`SCORECARD.md:2750-2751`) kept it routed for causal separability. At tip the coordinates are:
  - foreign-baseline full read `:777` (`printf '%s\n' "$base_txt" | awk -v n="$nm" '$1 == n && !f
    { print $2; f = 1 }'`, comment "(round 42: an awk `exit` under pipefail killed the census on a
    large baseline)"); no selftest drives `TSUKUROI_FOREIGN_BASELINE` past the pipe buffer — only the
    16-row fixture (`:2402-2410`) and absent-baseline (`:2730`, `:2432-2434`) cases exist; the
    large-output cases (`:2468`, `:2674-2685`) cover `-Qkk/-Qu/-Sup/-Suu`, not this lookup.
  - five single-line probe readers `printf '%s\n' "$CAP_OUT" | head -n1 | …` at `:965`
    (is-system-running), `:1003` (show -p Result), `:1085` (nvidia-smi csv), `:1460`
    (is-active graphical.target), `:1535` (show -p ActiveState); plus the two selftest assert
    heads `grep … | head -n1` at `:2292`, `:2302`. (w1 draft's `:967/:1005/:1087/:1462/:1537`
    and `:2289/:2299` are stale by -2; the w1 draft's `:779` baseline coordinate is stale by -2
    after the timers-case commit `8eee79db` and registry commits.)
  - **Adjacent same-class site the named list misses** (the non-obvious extension): `:832`
    `holds=$(grep -hE '^[[:space:]]*HoldPkg' "$PACMAN_CONF_FILE" | head -n1 | sed … || true)` — a
    piped `head -n1` inside a probe path, the identical early-reader/SIGPIPE class; it is masked by
    `|| true` today and unguarded by any case. `:669` `mem_read` (`head -n1 -- "$1"` reading a FILE,
    not a produced stream), `:1025` (`head -n1` on `$DMESG_RESTRICT_FILE`), `:3370` (`head -n1` on
    `$HOSTNAME_FILE`) read files directly — no producer stream, no SIGPIPE; excluded.
- **C2 counter gaps (item's named content), all demonstrated in w1 and recorded open in the round-44
  lesson** (`corpus/lessons/round-44.md:55-59`):
  - *quote gate*: `tools/check-scrub-record-r44.py:287` `if src and 1 <= n <= len(src) and q in
    src[n - 1]` — bare substring containment of the `(.+)` quote text; replacing a quote with `"n"`
    kept `quotes_ok 3` (`w1/C2RevCounter.md` F1, `out-c5.json`). Together with `:290/:294` (one good
    quote must sit in *any* window of the key) a writer can satisfy the gate with one trivial
    in-window token per required file.
  - *last-dup-wins registry*: `:167-175` `rows[cells[0]] = cells` — any `^ {0,3}\|S\d{3,}\|` line
    with exactly 11 cells anywhere in SOURCES.md (incl. fenced blocks) participates; later duplicates
    silently overwrite. Appending a doctored S242 row flipped `sources_ok 1→0`; re-appending the
    original restored it (`w1/C2RevCounter.md` F2, `out-c6/c7.json`).
  - *baseless-repo vacuity*: `novelty_hits` ignores the git exit code (`:240-243`) and `reg_base` is
    `{}` when `show(BASE,'corpus/SOURCES.md')` returns None (`:267`), so in a repo without base
    history "novel"/"absent at base" are trivially true: an orphan repo returned exit 0 PASS
    (`w1/C2RevCounter.md` F3, `out-fx2.json`, rev `774732b4`).
  - *recorded, cheap to close in the same amendment* (C2MutBinding): F1 — duplicate `verdict_line`
    keys bind the last value (`json.loads` last-wins; demonstrated PASS at rev `40c8479c`); F4 —
    a top-level JSON array in `w2-results.json` crashes the counter with a traceback (fails closed,
    contract violation).
- **Frontier after round 44** (`PROVINCE.md:275-279`): still Frontier — record *content* (mode-0600
  root-written, `flock(LOCK_EX|LOCK_NB)`), the running state (`BTRFS_IOC_SCRUB_PROGRESS` needs
  CAP_SYS_ADMIN; SR6/SR7), and NVMe SMART/Health. NVMe SMART is **not lane-claimable**: `/dev/nvme0n1`
  is `brw-rw---- root:disk`, the seat user is not in `disk`, sudo is banned — a coverage arm would be
  constant BLOCKED, indistinguishable from a do-nothing arm on the live host (the R39 discrimination
  limit). Excluded from the planned row with reason.
- **Depth knowledge gaps for the r45 entry** (refining w1/ConnFrontier §2): the record-grammar
  consequences are piecewise-pinned — SC2 (line grammar, held), SC4 + r42 corrections block
  (`btrfs-scrub-record-r42.md:184` already records `invalid data on line …`, `:199` already records
  socket-first ordering), SR1 (write discipline + `final = new || old[len(new):]`, harness-reproduced),
  SR3 (resume), SR6/SR7 (ioctl gate). The *synthesized reader-side matrix* — what a record's bytes
  alone tell a root reader, and how invalid-data tail bytes present — has no single pinned row; the
  progress-socket's content protocol beyond "reads it first" (S237 `cmds/scrub.c` anchor
  `1925-1945`) is unpinned. Sources needed: S237, S240 (re-open, used-by gains the r45 entry), S245
  reused; no new source required unless the socket-protocol claim needs a wider S237 window — flagged
  as a freeze-time decision (freshness: re-fetch byte-identical).
- **Novelty-token risk**: r44's counter uses token hits at BASE for novelty; much of the grammar
  vocabulary already exists in r42/r43/r44 entries, so the r45 counter's `novelty_base_hits` tokens
  must be chosen against the actual base corpus (freeze-time check: `git grep -F <token> BASE --
  corpus/knowledge`).

## 2. Synthesis (the one move)

Keep the w1 draft's two-claim shape (depth + operability; adjacency unclaimable, coverage
privilege-gated) and fold the three named C2 counter gaps into the round-45 **depth claim's counter
specification** — the r43→r44 precedent is that each round's new sourced-depth counter closes the
recorded gaps of its predecessor (r44's counter added the K14/K15/K16 binding guards over r43's
recorded limits). A separate counter-amendment claim would share the operability axis with the
census-readers claim or invent a third claim on an axis already at 9; folding is causal-separable
(new file `tools/check-scrub-record-r45.py`, disjoint from `tools/tsukuroi-census.sh`). Two cheap
binding hardenings (dup-key rejection, record-file shape guard) ride the same amendment — recorded
open items, closed by design requirements, not by new claims.

## 3. Round-45 planned row — exact text

```
## Round 45 — declaration (planned row, draft)

Base: the round-44 measured tip (declared before the after-run). Ordinals at base: depth 8,
coverage 9, operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency are tied
lowest; C1 works depth; adjacency stays unclaimed — recipient-side acknowledgement, acceptance and
closure cannot be produced by this lane (`PROVINCE.md:77-79`), ADJ-06's recipient is unresolved
(`PROVINCE.md:51,79-80`), mori declares no intake format for ADJ-04 (`PROVINCE.md:193`), and no
sibling declares storage-integrity ownership — and must not be harmed. Saturation 9 / window 3
unchanged. This round discharges the routed census-readers debt (the foreign-baseline lookup case
and the five single-line probe readers; routed since round 42, kept routed by the round-44
declaration `SCORECARD.md:2750-2751` and `corpus/lessons/round-44.md` §3) on the operability axis,
and closes the remaining scrub-record knowledge gap — the reader-side content matrix — on the depth
axis. NVMe SMART stays Frontier: its reads need a privilege this lane does not have and may not
acquire (`/dev/nvme0n1` root:disk 660; no sudo); an operator-gated dependency, not a lane gap.

| Claim | Axis | Surface moved | Counter (frozen; sha256 named at freeze) | Before at base (expected) | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | depth (sourced: S237, S240 re-opened; S245 reused; no new source unless the socket-protocol window widens) | New entry `corpus/knowledge/btrfs-scrub-record-r45.md` rows RG1-RG3: RG1 the reader-side record grammar and its failure surface — every non-header line is `<uuid>:<devid>` plus the `|key:value` pairs of SC2 in order; a grammar-violating line makes `btrfs scrub status` print `invalid data on line …` (S237:569-576, first recorded in the r42 corrections block); a shorter successful rewrite leaves the old record's tail inside the renamed file (r43 SR1, `final = new \|\| old[len(new):]`), surfacing as invalid-data lines — a defect signal, never extra devices. RG2 the content-only state matrix a root reader can compute from record bytes alone without the ioctl — which status words/fields the record can and cannot attest, bounded by SR6/SR7 (`EPERM` without CAP_SYS_ADMIN; 0 only while `dev->scrub_ctx` is attached). RG3 the live-start signal path — while a start process is live, `btrfs scrub status` reads the `scrub.progress.<fsid>` socket before the record (S237:1925-1945, socket-first ordering already pinned in r42 SC4-correction F3) and what that socket's visibility/protocol bounds for a non-ioctl reader; plus an append-only `extended-by:` header pointer from `btrfs-scrub-record-r44.md` and SOURCES used-by edits | `python3 tools/check-scrub-record-r45.py --revision <REV> --sessions <DIR>`: r44 verdict-binding machinery carried over; NEW conjuncts closing the three recorded r44 counter gaps — (a) quote gate: every quoted line number must lie inside a declared window for its key AND quote text must be ≥N substantive chars of that line's bytes (K9-shift and gutted-quote controls must FAIL); (b) registry: S-id rows parsed only inside the SOURCES registry table (fenced blocks excluded), a duplicated id anywhere is fatal (dup-doctor controls must FAIL); (c) base vacuity: BASE must resolve as an ancestor of REV before any base-relative check runs, else exit 1 (orphan-repo control must FAIL) | `rows 0` at base (no r45 entry) → FAIL | rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1, verdicts_ok 3, novelty_base_hits 0, pointer_ok 1, snapshots_ok/capture_ok true; all three new gap conjuncts green on the candidate and red on their controls | any bound `fails` without a bound residual `holds`; `novelty_base_hits > 0`; any predecessor sourced counter (`check-scrub-record-r43.py`, `check-scrub-record-r44.py`) FAIL; S237/S240 re-fetch not byte-identical; entry appended to the r43/r44 file instead of a new file (frozen `rows == 3` breaks) |
| C2 | operability | `tools/tsukuroi-census.sh`: (a) a selftest case driving `TSUKUROI_FOREIGN_BASELINE` past the pipe buffer (~64 KiB, ≥2000 rows) asserting the packages plane still computes foreign additions/removals via the `:777` full-read form, so a revert to the round-42 `awk … exit` form fails the case (exit 141 precedent); (b) convert the five single-line probe readers (`printf '%s\n' "$CAP_OUT" \| head -n1 \| …` at `:965`, `:1003`, `:1085`, `:1460`, `:1537`), the same-class HoldPkg reader `grep … \| head -n1` at `:832`, and the two selftest assert heads (`:2292`, `:2302`) to full-read/here-string forms so no produced-stream early reader remains; file-read heads (`mem_read` `:669`, `:1025`, `:3370`) stay — they read files, not produced streams | `python3 tools/score-census-readers-r45.py --revision <REV> --scratch <DIR>`: lexical conjunct (no `producer \| head` early-reader regex hit in production probe paths, site list content-pinned), selftest PASS including the new large-baseline case, the `awk … exit` revert mutant killed | regex hits present at the named sites and no large-baseline case at base → FAIL | lexical clean, selftest PASS total grows by the new case(s), revert mutant FAILs the counter | a PLANE/SCRUB/STORAGE/DRIFT/TSUKUROI_CENSUS line shape or count changes; live exit code changes between base and measured; selftest regresses (148 cases minus the new additions, 0 failed); the counter runs without `--scratch` or leaves residue; predecessor counters `score-scrub-arm-r44.py`, `score-storage-arm-r38.py`/`-q82`, `score-storage-hidden-r39.py`, `score-size-invariance-r42.py`, `score-bootinputs-r43.py` FAIL |

Controls, scored with the frozen counters before any seat: C1 — K0 do-nothing base (rows 0; must
FAIL), K1 scripted writer, K2 line references shifted, K3 dropped source, K4 mention-not-assertion,
K5 padded verdict line, K6 contradictory JSON `verdict`, K7 no pointer, K8 gutted quote ("n" as
quote text), K9 doctored duplicate SOURCES row (used-by dropping the entry), K10 duplicate row
inside a fenced block, K11 duplicate `verdict_line` keys (fails-then-holds), K12 top-level-array
record file (each must FAIL); K13 orphan/no-base repo (must FAIL via the base-resolution gate);
only the candidate PASSes; K3 forged records PASS recorded as the standing limit. C2 — K0
do-nothing base (must FAIL), K1 the `awk … exit` revert variant (must FAIL), K2 a `| head` early
reader reintroduced at any named site (must FAIL), K3 the new selftest case removed (must FAIL),
K4 a file-read head converted (over-reach: lexical conjunct must not flag mem_read/HOSTNAME_FILE/
DMESG_RESTRICT_FILE; must PASS as a tolerated conversion or be scoped out by the pinned site list —
freeze-time decision); only the candidate PASSes. Battery lines: `should_fail_accepted 0,
control_accepted 1` for each counter.

Causal separability: C1 touches corpus/knowledge (new r45 entry), the r44 entry header pointer,
`corpus/SOURCES.md` used-by, frozen snapshots and `tools/check-scrub-record-r45.py` (new file);
C2 touches `tools/tsukuroi-census.sh` only (probe_packages baseline read, six reader call sites,
selftest). Neither counter reads the other's surface. No-harm: all six axes re-checked at the tip;
the r44 frozen counters, the storage-arm counters, the boot-inputs counter, the r43 sourced counter
and the census selftest still PASS.

Risks / second-order effects. (a) C1's rows are source-grounded with no live record on this host
(capture: `/var/lib/btrfs` absent); verdicts rest on pinned bytes plus wave-2 reads, same as
SR7-SR9. (b) RG3's socket-protocol claim may exceed S237's pinned window (1925-1945); widening the
anchor is a freeze-time decision needing a byte-identical re-fetch — never an unpinned quote.
(c) The r45 counter's novelty tokens must be chosen against the actual base corpus — most grammar
vocabulary already exists in r42-r44 entries; a lazy token set either vacuously passes or
impossibly fails. (d) C2's conversions touch long-lived probes; producers are small today so the
sites are latent, not live, defects — the claim's evidence is the regression guard + revert mutant,
not a demonstrated host failure; say so in the declaration. (e) The r44 C1 counter's recorded open
items (cached-live leg C1CritEvasion F1; understated channel set C1CritChannels) are deliberately
NOT folded: `score-scrub-arm-r44.py` is frozen and its amendment would land on the same census
surface as C2 — named here as the next candidate for a later counter-surface round.
```

## 4. Corrections to the w1 draft (`.ufo/waves/round-44/w1/ConnFrontier.md`)

1. **Coordinates**: all census line numbers updated to tip `3a1c6b5c` (`:746`→`:777`;
   `:967/:1005/:1087/:1462/:1537`→`:965/:1003/:1085/:1460/:1535`; assert heads `:2289/:2299`→`:2292/:2302`);
   the w1 draft's tip (`ff2c264a`, 3396 lines) predates the `8eee79db` timers-case commit and the
   registry/promotion commits (3442 lines).
2. **The three named C2 counter gaps are folded into C1's counter spec** (section 3, C1 counter
   column + controls K8-K13): the w1 draft did not carry them; the r43→r44 precedent shows gap
   closure belongs in the next round's new counter, never in a retro-edit of the frozen one.
3. **C2MutBinding F1/F4 added** as cheap design requirements of the same new counter (dup-key
   rejection via `object_pairs_hook`, record-file `isinstance(dict)` guard) — recorded open items
   (`corpus/lessons/round-44.md:57-58`), closed without a new claim.
4. **HoldPkg `:832` added** to C2's conversion surface: same `producer | head -n1` early-reader class
   as the five named sites; file-read heads explicitly excluded by mechanism (no produced stream).
5. **"Unpinned" claims narrowed**: the w1 draft's "not yet pinned" list partly overstates — the
   invalid-data consequence is already recorded (`btrfs-scrub-record-r42.md:184`) and socket-first
   ordering is pinned (`:199`, SC4-correction F3). RG1/RG3 are drafted as synthesis-and-boundary rows,
   not novelty-of-fact rows; the novelty-token risk is named in risks.
6. **r44 C1-counter open items named but not folded** (risk e): folding a second counter amendment
   into the operability claim would blur the surface and the axis.

## 5. What I did not do

- I did not run any counter, census selftest or host command; evidence is `grep`/`sed` reads at tip
  (receipt file). I did not freeze counter bytes or score K-batteries (L1 work; sha256 named at
  freeze). I did not fetch or re-fetch sources (byte-identity is freeze work). I did not read
  sibling lane files. No tools installed or updated; no lane tracked file written; only this report
  and `w2/ConnFrontierFinal/census-readers-and-counter-gaps-tip.txt`. Scratch
  `/fast/scratch/hyaku/tsukuroi-r44/ConnFrontierFinal/` removed after use.
