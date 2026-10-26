VERDICT: draft

# Seat ConnFrontier — item X-3: frontier state after round 43, and the round-44 planned row

Lane: tsukuroi-shokunin; round 43 wave w1. Basis: round-43 declaration
(`SCORECARD.md:2648-2684`, freeze `fe357001`), implementation `717b716a`, lane tip
`7d0ed1c2`. Receipts: `w1/ConnFrontier/s242-src.txt`, `w1/ConnFrontier/host-units.txt`.
Read-only: no lane file written except this report and the receipts; no counter, census or
audit run; no host mutation; nothing installed (host guard: no pacman, no service, no sudo).

## 1. Which frontier lines round 43 advances

Round 43 advances exactly one frontier line, and only its *knowledge* depth: the scrub-record
line of the storage-integrity frontier (`PROVINCE.md:154-176`, `corpus/README.md:241-243`).

- `corpus/knowledge/btrfs-scrub-record-r43.md` re-grounds the round-42-withdrawn SC1/SC3 as
  SR1/SR3 with counted reads, and adds SR6: an unprivileged census cannot learn running state —
  `BTRFS_IOC_SCRUB_PROGRESS` returns `-EPERM` before doing anything else without
  `CAP_SYS_ADMIN` (`S240` ioctl.c:3132-3133), and `btrfs scrub status`'s `in_progress`
  comes only from that ioctl (`S237` scrub.c:1946, 1200-1205), so an unprivileged status never
  prints `running`. This turns the round-42 SC4 narrowing's [inference] (a host errno alone)
  into kernel-grounded text, and adds the start/cancel ioctl gates (S240:3072, 3120).
- No frontier area moves to Core. No census arm reads the scrub record or NVMe SMART
  (`SCORECARD.md:2662` declares C2 depth only; the round-42 proposed arm
  (`w2/ConnRound43.md` §3 C1) was not taken). Adjacency is untouched and unclaimed.
- SR6 also tightens the promotion boundary itself: a future arm can read the record's
  absence/presence/stat and the timer unit state, but **running state is an elevation-gated
  reading** (row lines 121-122) — an honest arm must either omit `running` or report it
  unobservable. The wave-1 first falsifier `w1/C2DraftCritSR6.md` confirms the row's
  status-command claims line-for-line and flags three refinements: F1 (the "comes only from the
  kernel" sentence overreaches the CLI as a whole; the record-based `is_scrub_running_on_fs`
  (S237:1392) and the live progress socket (S237:1474-1479) are other running authorities), F2
  (the ioctl *success* direction is unpinned: `btrfs_scrub_progress`'s body is not in the
  frozen set), F3 (`capable()` resolves in the initial user namespace, [inference]). These
  falsifier findings are input to the round-44 depth row below (section 4, C2).

## 2. Which frontier lines stay open after round 43

1. **Scrub record → Core promotion.** Still no read-only census arm reads it. The promotion
   condition (`corpus/README.md:243`; R38 precedent `SCORECARD.md:2117` for the error counters)
   is met for the *readable subset*: the record directory stat/listing, the per-fsid record
   file stat, the `scrub_speed_max` sysfs read and the timer unit state are unprivileged-readable
   (section 4 C2, SR8/SR9); the record *content* (root-owned mode 0600, S237:483) and running
   state (SR6) are not. The round-42 note (`PROVINCE.md:239-244`) already established
   `btrfs scrub status /` runs unprivileged; what the arm can honestly read is now fully known.
2. **NVMe SMART/Health (SH5/SH6)** — no arm; needs privilege; second NVMe (xfs `/tmp`, `/fast`)
   stays unread.
3. **Root-DAC census-arm debt and the `errno:13` [inf] falsifier** (snapper-eacces-mechanism)
   — unchanged; the falsifier awaits the operator.
4. **Adjacency** — recipient-side replay, acknowledgement/acceptance and closure stay unverified;
   kaidoku/revenger shipped-artifact RE arbitration stays unresolved; mori intake format stays
   undeclared (ADJ-04 handoffs remain `state=prepared`). Adjacency axis (8) stays unclaimed and
   must not be harmed.
5. **R39 namespace-discrimination limit** — a census that detects the fixture namespace and
   behaves honestly only there cannot be told apart on this host (live answer constant
   `HEALTHY 1/1/0`; no host-side injection authorized). Stays.
6. **mkinitcpio watch** — upstream may drop the `/new_root` compatibility symlink; recheck
   `tools/boot-chain-audit.sh --live` on every mkinitcpio release (r17 note). A standing watch,
   not claimable ground.

## 3. Weighing the remaining R42-C1-COUNTER-AMEND bullets

Source: `corpus/lessons/round-42-verifier-spotcheck.md:201-207`; the individual sites from
round-42 `w1/C1SweepSites.md`. Status after round 43:

| Bullet | Round-43 disposition | Remaining |
|---|---|---|
| 1 production-identity legs (uid 1000 via `setpriv`) with per-run fixture names | DONE in the new round-43 counter: `score-bootinputs-r43.py` runs the scored function at the caller's uid/gid via subuid map + `setpriv --reuid/--regid` (lines 84-87, 292), fixture content built inside the child namespace with per-run random names (`random.Random(os.urandom(16))`, line 289) | — |
| 2 frozen controls for the gated, data-gated and padding-filter arms | PARTIAL: `run_controls_c1.py` K3 uid-gated, K4 env-gated, K5 name-gated, K7 mount-table-gated cover the env/identity/name/mount channels of QUALITY 90 (`corpus/QUALITY.md:177`). Explicit **data-gated** (fix keyed on the fixture data value, e.g. the found path/hit content) and **padding-filter** (fix that pads/filters output so `grep -q` always matches) arms are **not present** in the battery | open (counter-hygiene; binds future counters) |
| 3 refuse without `--scratch`; fix SIGINT leak | `--scratch` required (line 240) — DONE. SIGINT/SIGTERM handler installed (lines 247-251) with cleanup in `finally` — the handler is present, but whether a SIGINT during a namespace subprocess is reaped (vs. orphaning the child) is unverified (I did not run a signal injection test) | SIGINT-reaping unverified |
| 4 selftest case for the `:743` lookup whose revert survives the selftest | NOT DONE. The code fix exists — `tools/tsukuroi-census.sh:746` now reads the foreign baseline with `awk '$1 == n && !f { print $2; f = 1 }'` (full read; comment cites the round-42 `exit` kill). But the selftest has no case driving an override baseline past the pipe buffer (existing foreign cases use a 16-row baseline, census lines 2288-2321), so restoring the `exit` form would still pass the selftest | open — C3 below |
| 5 `tools/boot-chain-audit.sh:480-487` fail-open with a red-before case | DONE (round-43 C1: helper `inputs_newer_than`; `R43-C1-*` selftest cases at 1232-1237; before/after receipts `.ufo/waves/round-43/before/c1-before.jsonl`, `after/c1-after-717b716.jsonl`) | — |
| 6 fix the single-line probe readers | NOT DONE: the single-line `printf … | head -n1 | …` assignments remain un-neutralised and unreachable (census :934, :972, :1054, :1429, :1504; C1SweepSites table lines 38, 41, 80) | open — C3 below |

## 4. Proposed round-44 planned row

**Synthesis (the one move).** Three claims on three distinct axes, worked from the round-43
frontier state: C1 (coverage) closes the cheapest true Frontier→Core promotion available — the
scrub-record arm over the subset SR6/SR8/SR9 prove readable — and is *made honest by* the depth
claim; C2 (depth, the tied-lowest axis) pins what the w1 falsifier proved unpinned (the ioctl
success direction, S242) and the read-surface matrix; C3 (operability) discharges the two
remaining R42-C1-COUNTER-AMEND bullets (4 and 6) with a red-before regression case. Adjacency
stays unclaimed (still lane-internally unreachable). Each claim has a do-nothing control that
fails under its frozen counter.

```
## Round 44 — declaration (planned row, draft)

Base: the round-43 measured tip (declared before the after-run). Ordinals at base: depth 8,
coverage 9, operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency are tied
lowest; C2 works depth; adjacency stays unclaimed (a sibling acknowledgement cannot be produced
by this lane) and must not be harmed. Saturation 9 / window 3 unchanged. This round folds the
remaining R42-C1-COUNTER-AMEND bullets: the C3 counter refuses to run without --scratch, handles
SIGINT by reaping its own children, and its frozen pre-data controls include the data-gated and
padding-filter arms (QUALITY 90 channels) beside the env/uid/name/mount arms; the C2 binding is
the anchored declared-verdict form (QUALITY 90 second clause, R42-VERDICT-FORM).

| Claim | Axis | Surface moved | Counter (frozen; sha256 named at freeze) | Before at base (expected) | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | coverage | The scrub-record line of the storage-integrity frontier (`PROVINCE.md:212-214`, `corpus/README.md:243`) moves Frontier → Core for the unprivileged-readable subset: the census gains a verdict-neutral `STORAGE btrfs-scrub-record state=… filesystems=N records=N unreadable=N timers=N [detail=…]` line (`probe_scrub_record`, beside `probe_storage_arm`), which for each btrfs fsid the mount table lists (round-39 guard, `TSUKUROI_PROC_MOUNTS`) stats `/var/lib/btrfs` (absent → `records=0`, SH4 semantics), stats each `scrub.status.<fsid>` file, reads `devinfo/<devid>/scrub_speed_max`, and reads the `btrfs-scrub@*.timer` unit state; a present record whose content is unreadable (root mode 0600, S237:483) reads `state=BLOCKED detail=records:unreadable`, never HEALTHY; running state is never reported (SR6: elevation-gated, unobservable to the census) | counter: base census has no `STORAGE btrfs-scrub-record` line → FAIL | line present for every listed btrfs fsid; fixture matrix (absent dir, present-0600 record, present-readable record, dir-unreadable, no-mount) each maps to its declared state; census selftest still PASS | any change to existing census functions other than the new probe + its call site, or the census selftest regresses |
| C2 | depth (sourced) | `corpus/knowledge/btrfs-scrub-record-r43.md` gains append-only rows SR7-SR9: SR7 the kernel-side success direction — `btrfs_scrub_progress` (Linux v7.2.11 `fs/btrfs/scrub.c:3321-3335`, new source S242) returns 0 with the device's `scrub_ctx` stat only while a scrub runs on that devid, `-ENOTCONN` when the device is idle, `-ENODEV` for an unknown devid (closes the SR6 wave-1 falsifier F2; F1/F3 scoping notes appended); SR8 the read-surface permission matrix — `/var/lib/btrfs` created by `mkdir_p(…, 0777)` (S237:1335, 1160), record files opened mode 0600 (S237:483) and named `scrub.status.<fsid>`/`_tmp` (S237:446-470), `btrfs scrub status` distinguishes absent (exit 0, "no stats available", S241 capture.txt:8-10) from present-unreadable (warning "failed to open status file", S237:1931-1939, `!!err` at :1999); SR9 the timer surface — `btrfs-scrub@.service`/`.timer` (`ExecStart=/usr/bin/btrfs scrub start -B %f`, `ConditionPathIsMountPoint=%f`, `Nice=19`, `IOSchedulingClass=idle`, `KillSignal=SIGINT`, `OnCalendar=monthly`, `Persistent=true`; host unit files, receipt `host-units.txt`; template instance state queryable unprivileged, `is-enabled` = disabled on this host) | counter: entry rows absent at base → FAIL | per-row counted wave-2 verdicts `C2RevSR<n>`/`C2CritSR<n>` bound through w2-dispatch.json + w2-results.json (anchored first-line form); S237/S240/S241 pinned hashes unchanged; S242 (new) pinned; S243 = unit files pinned | any change to the r43/r42 entries other than the appended rows + header pointer, or a pinned source digest drifts |
| C3 | operability | `tools/tsukuroi-census.sh`: add a selftest case that drives the packages-plane foreign baseline through `TSUKUROI_FOREIGN_BASELINE` at > the pipe buffer (~64 KiB, ~2000 rows; C1SweepSites :24) and asserts the packages plane still computes (the `:746` full-read form), so that reverting to the round-42 `awk … exit` form fails the selftest (exit 141); convert the remaining single-line probe readers (`printf … | head -n1 | …` at :934, :972, :1054, :1429, :1504) and the selftest asserts to here-strings so no probe-buffer early reader remains | counter: base fails the lexical conjunct (early-reader regex hits) and lacks the large-baseline case; a revert mutant (restore `exit`) must FAIL the selftest case | lexical conjunct clean, large-baseline case present and PASSing in `--selftest`, revert mutant FAIL, census selftest PASS (case count grows), round-42 C1 counter and round-43 C1 counter still PASS at the tip | any function body other than the baseline read and the named single-line readers changes, or the round-42/43 C1 counters / census selftest regress |

Controls, scored with the frozen counters before any seat: C1 — do-nothing base census (no
STORAGE btrfs-scrub-record line; must FAIL), constant emitter, count-only reader (stats without
EACCES discrimination), presence-denial (ignores BLOCKED detail), fixture-gated arm, cached-live
arm, and a present-0600 fixture that must read BLOCKED (only the candidate PASSes). C2 —
do-nothing base, scripted writer (quotes copied from the row windows), line references shifted,
dropped source, S242 absent, mention-not-assertion report (must FAIL under the anchored binding);
only the candidate PASSes. C3 — do-nothing base plus the `awk … exit` revert variant (must
FAIL) and the early-reader regex hit (must FAIL); only the candidate PASSes. Expected battery
lines: `should_fail_accepted 0, control_accepted 1` for each counter.

Causal separability: C1 touches the census (new probe + call site) and the promotion paragraphs in
PROVINCE/README; C2 touches the r43/r42 knowledge entries and corpus/SOURCES.md (new S242/S243);
C3 touches census `probe_packages` (baseline read + single-line readers) and the selftest. C1 and
C3 share the census file but touch disjoint functions and are scored by independent counters;
neither counter reads the other's surface. No-harm: all six axes re-checked at the tip,
including `score-storage-arm-r38.py`, `score-storage-hidden-r39.py`, `check-scrub-record-r43.py`,
`score-bootinputs-r43.py`, `score-size-invariance-r42.py`, and the census selftest still PASS.
Measured revision: the lane branch tip named in the round-44 outcome section, declared before the
after-run.
```

**Risks / second-order effects.** (a) C1's live line on this host is `records=0` (no
`/var/lib/btrfs`, `scrub_status_exit 0`, S241 capture.txt:7-10), so the live value cannot show
the BLOCKED branch; the fixture matrix carries it (mirrors the round-43 C1's namespace-evidence
pattern). (b) C2's SR7 must not restate SR6's overreach: it is scoped to `cmd_scrub_status` and
the ioctl success direction, with F1/F3 notes appended (per `w1/C2DraftCritSR6.md` F1-F3). (c)
C3 is the only claim with a pre-existing fix; its novelty is the regression guard — the counter's
do-nothing control is the missing case, and the revert mutant proves the case bites. (d) The
SIGINT-reaping behavior of the round-43 counter remains unverified; C3's counter should both
handle SIGINT and reap its children (report under `--scratch` hygiene, not as a scored claim).

## 5. What I did not do

- I did not run the C1/C2 counters, the census selftest, `boot-chain-audit.sh`, or any signal-injection test (planning seat; read-only queries only).
- I did not freeze counter bytes or score K-batteries (L1 work).
- I did not verify the Arch kernel patches `fs/btrfs/ioctl.c` or `fs/btrfs/scrub.c` (the same limit SR6 records at row lines 126-128; S242 carries the same caveat).
- I did not read sibling lane files; only lane-internal files.
- No tools installed or upgraded.
