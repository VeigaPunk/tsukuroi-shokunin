VERDICT: draft

# Seat ConnFrontier — item X-3: frontier state after round-44 C1/C2, and the round-45 planned row

Lane: tsukuroi-shokunin; round 44, wave w1. Basis: round-44 declaration (`SCORECARD.md:2746-…`,
freeze `1d2afffe`, base `98020ece`, implementation `7e081698`, lane tip `ff2c264a`); C1 after
receipt at `ab8aae16` (PASS); C2 draft entry SR7-SR9 landed at `7e081698` (counted verdicts are
bound only from wave 2, per the declaration). Read-only: I ran no counter, no census, no audit
(planning seat; heavy counters are running in wave-1 executor seats). Evidence below is `path:line`
at the tip or a quoted command/observation. Receipt: `w1/ConnFrontier/census-readers-tip.txt`.

## 1. Lane state at tip (evidence)

- Tip `ff2c264a`; working tree clean except the untracked w1 wave directory (git status).
- `tools/tsukuroi-census.sh` is 3396 lines; `probe_scrub_record` at `:1967-2040`; the header
  grammar for the new line at `:387`; nine `(R44-C1)` selftest cases at `:3229-3285` (132 → 141).
- The arm reads `/var/lib/btrfs` "by name and stat only, never content" (`:1996`), sysfs
  `scrub_speed_max` per devid (`:1985-1992`), and `timers.target.wants` links (`:2027-2031`).
  It never opens a record for reading and never issues an ioctl. Runs are socket-name counts, not
  state reads (`:2014-2016`).
- Top C1 frozen counter `tools/score-scrub-arm-r44.py`; C2 frozen counter `tools/check-scrub-record-r44.py`;
  counters for prior rounds (`check-scrub-record-r43.py`, `score-storage-arm-r38.py`/`-q82`,
  `score-storage-hidden-r39.py`, `score-size-invariance-r42.py`) are present and untouched.
- Round-44 declaration explicitly kept the census readers item routed: "item (3) (the census
  `:746` lookup case and the five single-line probe readers) stays routed"
  (`SCORECARD.md:2747-2749`).

## 2. Which frontier lines remain after round-44 C1 and C2 land

1. **Record content parse for a root reader — stays Frontier.** The round-44 C1 arm reads names and
   stat only, never content (`:1996`). What a root-credentialed reader would find in the file is
   specified only piecewise: the line grammar and field order (r42 SC2, held), the fold rules (r42
   SC4, narrowed), the write discipline and the tail consequence (r43 SR1, with the byte relation
   `final = new || old[len(new):]` reproduced in the round-43 harness seat C2ExecTailRepro), and the
   resume semantics (r43 SR3). Not yet pinned: the **reader-side validation boundary** (a line
   violating the grammar makes `btrfs scrub status` print `invalid data on line …`, S237:569-576,
   per the r42 corrections block), what a short-rewrite tail means to a reader (invalid-data lines,
   not extra devices), and the **content-only state matrix** a reader can compute without the ioctl.
2. **Running state — stays Frontier.** SR6 pins the gate: `BTRFS_IOC_SCRUB_PROGRESS` returns
   `EPERM` without `CAP_SYS_ADMIN` (S240; r43 SR6), and C1 counts progress sockets by name only.
   One mechanism boundary is unpinned: when a start process is live, the CLI reads the progress
   socket *before* the record (S237:1927-1940, r42 SC4 correction F3); that socket's visibility and
   protocol are the only non-ioctl running authority and are not yet source-pinned.
3. **NVMe SMART/Health — stays Frontier, and is not lane-claimable this round.** No census arm reads
   it (PROVINCE `:212-214` unchanged). Feasibility on this host: `smartctl` and `nvme` are installed,
   but `/dev/nvme0n1` is `brw-rw---- root:disk` and user `vgpnk` is not in the `disk` group; sudo is
   banned to seats; the second NVMe (xfs on `/tmp`, `/fast`) stays unread. So no read-only arm can
   obtain values; a coverage claim would be indistinguishable from an absent arm on the live host
   (constant BLOCKED, the R39 discrimination limit pattern) unless the operator grants a read
   allow-list first. Excluded from the planned row with reason.
4. **The census `:746` lookup case — open.** The foreign-baseline full read is at tip `:779`
   (`awk … '$1 == n && !f { print $2; f = 1 }'`; history `:740` base → `:743` first fix →
   `:746` round-43 tip → `:779` now). No selftest case drives `TSUKUROI_FOREIGN_BASELINE` past the
   pipe buffer: only the 16-row fixture (`:2262,2399-2432`) and absent-baseline (`:2727`) cases
   exist; the large-output cases (`:2465-2695`) cover `-Qkk/-Qu/-Sup/-Suu`, not this lookup. A
   revert to the round-42 `awk … exit` form would still pass the selftest.
5. **Single-line probe readers — open (routed since round 42).** Five `printf … | head -n1 | …`
   sites remain at tip `:967` (is-system-running), `:1005` (show -p Result), `:1087`
   (nvidia-smi csv), `:1462` (is-active graphical.target), `:1537` (show -p ActiveState); their
   producers are small today, so the sites are unreachable rather than live defects, but no
   regression guard exists and the R42-C1-COUNTER-AMEND item was explicitly routed to a census-surface
   round (round-43 lesson `:102-119`; round-44 declaration kept it routed). `tools/boot-chain-audit.sh`
   is fixed (helper `inputs_newer_than` at `:463`, R43-C1 cases at `:1231-1238`).

Nothing else is open on the storage frontier: the readable subset of the scrub record is now Core
(round-44 C1); the error counters are Core since 38; the R39 mount-table guard stands; the second
NVMe and the root-only record content/running state are privilege-gated, which is a host/operator
dependency, not a lane gap.

## 3. Why the round-45 planned row is two claims, not three

- Lowest axes at base: depth 8 and adjacency 8, tied (`SCORECARD.md` ordinals, unchanged through
  round 43 and re-stated in the round-44 declaration).
- **Adjacency stays unclaimable**: recipient-side acknowledgement/acceptance/closure cannot be
  produced by this lane (PROVINCE `:77-79`); ADJ-06's recipient is unresolved (PROVINCE
  `:51,79-80`); mori declares no intake format for ADJ-04 (PROVINCE `:193`); and no sibling owns
  storage integrity, so there is no handoff recipient for any new finding. Any adjacency claim would
  be vacuous or harmful.
- **Coverage (9) has no feasible move**: the only coverage ground left is NVMe SMART, which is
  privilege-gated (section 2.3). A "readability probe" arm would be a constant BLOCKED on the live
  host and cannot be told apart from a do-nothing arm except structurally — the weakest claim shape
  available, and it would collide with the round-44 C1 surface (census file) for no gain.
- The strongest remaining moves are therefore **depth** (the record-grammar gap, section 2.1/2.2)
  and **operability** (the two routed census-reader debts, section 2.4/2.5). These are distinct axes,
  disjoint files, and both have do-nothing controls that fail at base.

## 4. Round-45 planned row — exact text

```
## Round 45 — declaration (planned row, draft)

Base: the round-44 measured tip (declared before the after-run). Ordinals at base: depth 8, coverage 9,
operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency are tied lowest; C1 works
depth; adjacency stays unclaimed — recipient-side acknowledgement, acceptance and closure cannot be
produced by this lane (`PROVINCE.md:77-79`), ADJ-06's recipient is unresolved (`PROVINCE.md:51,79-80`),
mori declares no intake format for ADJ-04 (`PROVINCE.md:193`), and no sibling declares storage-integrity
ownership — and must not be harmed. Saturation 9 / window 3 unchanged. This round discharges the routed
round-42 item (3) (the census `:746` lookup case and the five single-line probe readers; kept routed by
the round-44 declaration) on the operability axis, and closes the remaining knowledge gap on the
scrub-record frontier line — the record file's content grammar for a root reader — on the depth axis.
NVMe SMART stays Frontier: the reads need a privilege this lane does not have and may not acquire
(`/dev/nvme0n1` root:disk 660; user not in `disk`; no sudo); it is an operator-gated dependency, not a
lane gap.

| Claim | Axis | Surface moved | Counter (frozen; sha256 named at freeze) | Before at base (expected) | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | depth (sourced; S237/S245 reused, no new source opened) | New entry `corpus/knowledge/btrfs-scrub-record-r45.md` rows RG1-RG3: RG1 the reader-side record grammar — every non-header line is `<uuid>:<devid>` plus the `|key:value` pairs of SC2 in order; a line violating the grammar makes `btrfs scrub status` print `invalid data on line …` (S237:569-576); a shorter successful rewrite leaves the old record's tail bytes inside the renamed file (SR1; relation `final = new || old[len(new):]`, harness-reproduced in the round-43 C2ExecTailRepro), and those bytes surface as invalid-data lines — not as extra devices — so a root reader must treat them as a defect signal, not a device; RG2 the content-only state matrix a root reader can compute without the ioctl (absent / unreadable / per-device finished / canceled / invalid-tail) versus the ioctl-gated `running` (SR6), including the live-start progress socket as the only other running authority (S237:1927-1940) and its visibility; RG3 the mapping of RG1/RG2 onto the round-44 census arm's verdict fields (records/tmp/sockets/unreadable/orphan) as the promotion-ready grammar for a future privileged content reader | `python3 tools/check-scrub-record-r45.py --revision <REV>` | no r45 entry at base (rows 0) → FAIL | rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 (wave-2 bound) and pointer_ok == 1 (pointer to the r44 entry) | a PLANE/STORAGE/SCRUB line or the census exit code changes on the live host between base and the measured revision; a frozen predecessor storage counter FAILs where it PASSes at base |
| C2 | operability | `tools/tsukuroi-census.sh`: (a) add a selftest case driving `TSUKUROI_FOREIGN_BASELINE` past the pipe buffer (~64 KiB, ≥2000 rows) asserting the packages plane still computes with the `:779` full-read form, so restoring the round-42 `awk … exit` form fails the case (exit 141); (b) convert the five single-line probe readers (`printf '%s\n' "$CAP_OUT" | head -n1 | …` at `:967`, `:1005`, `:1087`, `:1462`, `:1537`) and the two run-selftest assert heads (`:2289`, `:2299`) to full-read/here-string forms so no probe-buffer early reader remains | `python3 tools/score-census-readers-r45.py --revision <REV> --scratch <DIR>` | regex hits present at the five sites and no large-baseline case → FAIL | lexical conjunct clean (no `| head -n1` regex hit in production probe paths), selftest PASS including the new case, the `awk … exit` revert mutant FAILs (exit 141), neutral on the six PLANE lines | a PLANE line or the census exit code changes on the live host between base and the measured revision; the arm creates a file in live mode |

Controls, scored with the frozen counters before any seat: C1 — K0 do-nothing base (rows 0; must
FAIL), K1 scripted writer (quotes copied from the row windows), K2 line references shifted, K3
dropped source, K4 mention-not-assertion report, K5 padded verdict line, K6 contradictory JSON
`verdict` field, K7 no pointer (each must FAIL under the anchored binding; only the candidate PASSes).
C2 — K0 do-nothing base (must FAIL), K1 the `awk … exit` revert variant (must FAIL), K2 a
`| head -n1` reader reintroduced at any of the five sites (must FAIL), K3 the new case removed (must
FAIL); only the candidate PASSes. Battery lines: `should_fail_accepted 0, control_accepted 1` for
each counter.

Causal separability: C1 touches corpus/knowledge only (new r45 entry, r44 header pointer, SOURCES
used-by); C2 touches tools/tsukuroi-census.sh only (probe_packages baseline read, five reader call
sites, selftest) — disjoint surfaces, independent counters, no shared file. No-harm: all six axes
re-checked at the tip, including `score-scrub-arm-r44.py`, `check-scrub-record-r44.py`,
`score-storage-arm-r38.py`/`-q82`, `score-storage-hidden-r39.py`, `score-size-invariance-r42.py`,
`check-scrub-record-r43.py` and the census selftest still PASS.

Risks / second-order effects. (a) C1's rows are source-grounded with no live record on this host
(capture.txt:6-10); verdicts rest on the pinned bytes plus the wave-2 reads — the same constraint
SR7-SR9 already carry; the harness-reproduced tail relation is the only runtime evidence. (b) RG2
must not restate SR6: it refines the boundary (ioctl vs progress socket) and must keep the EPERM
result intact; a contradictory finding is reported, not smoothed. (c) C2's conversion touches
long-lived probes; the lexical conjunct and the revert mutant pin the exact before/after forms, and
the five producers are small, so the conversion is behavior-neutral full reads. (d) Neither claim
acquires privilege or performs a host action.
```

## 5. Risk trace for the one move

- Runtime: C2's full-read conversions add no observable latency (five one-line producers); the new
  selftest case is hermetic under `--selftest` fixtures.
- Contract: C1 writes a new knowledge entry only; C2 changes no line grammar — the `SCRUB`/
  `STORAGE`/`PLANE` shapes and the rollup stay byte-identical, so the frozen predecessor counters
  and the r44 counters keep passing (no-harm conjunct).
- Substrate: C1 stays source-grounded (S237/S245), never touching the live record (absent here);
  C2 touches only the census's own probe internals.
- Verification: C1 verdicts are wave-2-bound (a wave-1 seat must not count them); C2 is fully
  testable in wave 1 (selftest + lexical conjunct + revert mutant). The do-nothing controls for
  both fail at base: no r45 entry exists today, and the five `| head -n1` sites plus the missing
  large-baseline case are present today.

## 6. What I did not do

- I did not run the C1/C2 counters, the census selftest, `boot-chain-audit.sh`, or any
  signal-injection test (planning seat; read-only queries only; heavy counters run in wave-1
  executor seats).
- I did not freeze counter bytes, score K-batteries, or verify the r44 C2 verdicts (L1/wave-2
  work; verdicts are wave-2-bound by the declaration).
- I did not attempt any privileged read (no sudo), did not open `/dev/nvme0n1`, and made no host
  mutation. Scratch: no scratch dir needed (no fixture was built); nothing to remove.
- No tools installed or upgraded; no sibling lane files read.
