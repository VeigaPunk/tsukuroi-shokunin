VERDICT: draft

# ConnFrontier — Item X-3: frontier and round 41 (draft)

Assessment basis: round-40 declaration (`SCORECARD.md:2291-2321`, commit `758a4b0`), the frozen counters at
`a447b67b`, implementation commits `c707e356` (C1) and `bf238050` (C2), tip `f951f288` at dispatch. Round 40 is
mid-wave (no measured-outcome section exists yet; `git log` shows the three commits above plus the wave generator at
`f951f28`). "Advances" below means *the declared claims move the line*; admission is a separate, non-author-closure
step I did not run.

---

## 1. Round 40's declared claims, in frontier terms

- **C1 (operability)**: `--selftest` gains five mount-table fixtures varying device/mountpoint/options/subvolume/
  line position/fstype case plus an unlistable root with btrfs mounted, so the literal-keyed and guard arms of the
  round-39 STORAGE cross-check fail it (`SCORECARD.md:2303`; target `R39-FIXTURE-MONOCULTURE`). This is an
  **instrument repair** on the Core census gate — it changes the selftest and the counter, not the production
  probe and not any host surface (`probe_storage_arm` is explicitly NOT changed).
- **C2 (depth, sourced)**: EX1–EX8 of what a libalpm hook command / install scriptlet finds at start, on S219–S225,
  deepening the **Core update-safety plane** (`SCORECARD.md:2304`; entry header `corpus/knowledge/
  pacman-exec-environment-r40.md:1-4`: "Ground: the update-safety plane (`PROVINCE.md` Core)").
- The declaration explicitly takes **no adjacency claim**: "no adjacency claim (a sibling acknowledgement cannot be
  produced by this lane; adjacency stays unclaimed and is not harmed)" (`SCORECARD.md:2295-2296`).

## 2. Which frontier lines round 40 advances

**None of the named Frontier bullets (PROVINCE.md:75-80; corpus/README.md:28-42) is advanced by the declared
claims.** The two claims work held Core ground (census gate; update-safety plane) and repair counter defects; they do
not move a Frontier line to Core, close a recipient/arbitration gap, or open a new owned surface.

One partial, indirect effect: C1's fixture diversity removes the round-39 counter defect that let a literal-keyed or
guard arm pass on a monoculture fixture set, i.e. it hardens the *instrument* behind the round-39 "remaining limit"
(`PROVINCE.md:234-236` — a census that detects the counter's namespace cannot be told apart on this host). The limit
itself is untouched: nothing in C1 changes the live constant answer (`HEALTHY 1/1/0`) or adds a host-side injection,
which the lane forbids.

## 3. Which frontier lines stay open (all of them)

| Line | Status after round 40 | Evidence |
|---|---|---|
| F1 Recipient acknowledgement / independent replay of handoffs unverified; author-side replay not promotion evidence | open | `PROVINCE.md:77-78`; `corpus/README.md:30-32`; adjacency ceiling `SCORECARD.md:2273` ("recipient acknowledgement and independent replay are unverified") |
| F2 Kaidoku/revenger shipped-artifact RE ownership contested; integrator arbitrates | open | `PROVINCE.md:79-80`; `corpus/README.md:33-34`; R20-OUT009 clarification `PROVINCE.md:148-152` |
| F3 Boot: btrfs-overlayfs snapshot-boot path on a mkinitcpio 42.2 image untested; `/new_root` symlink watch | open | `corpus/README.md:38-39` (superseded pending-upgrade bullet) and round-24 notice `corpus/README.md:225-228`; round-17 watch `corpus/README.md:151-153` |
| F4 Storage integrity: scrub record (SH3/SH4) and NVMe SMART (SH5/SH6) still Frontier, no census arm; second NVMe device (`/tmp`,`/fast`, xfs) unread | open | `PROVINCE.md:212-214`; round-39 "Still Frontier, unchanged: the scrub record and NVMe SMART" `PROVINCE.md:234`; round-26 condition `PROVINCE.md:169-170` |
| F5 Storage: census honesty indistinguishable on this host (live answer constant); no host-side injection authorized | open (C1 hardens the instrument only) | `PROVINCE.md:234-236`; round-38 known limit `PROVINCE.md:217-218` closed *for the absent-root rule* by round 39 (C1 now makes the literal-keyed arms fail, but does not change the host-facing distinction) |
| Adjacent OV4/OV5 conflicts with mori (OOMRules= qualifier; earlyoom option) | recorded, unresolved — need mori action | `PROVINCE.md:187-189` |
| ADJ-04 census handoff line (`state=prepared`; round 32) | no state transition possible: mori declares no intake format | `PROVINCE.md:193` |

## 4. Why the round-41 lowest-axis claim should be depth, not adjacency

Depth and adjacency are tied lowest at 8 (`SCORECARD.md:2268,2273`). Every avenue that would move adjacency 8→9
requires an actor outside this lane or outside the province: a recipient-side acknowledgement/replay (F1), integrator
arbitration (F2), mori intake-format or conflict resolution (ADJ-04; OV4/OV5). The round-40 declaration's reason
stands — "a sibling acknowledgement cannot be produced by this lane" (`SCORECARD.md:2295`). A *self-producible*
adjacency claim (re-checking sibling pins, counting handoff lines) has been measured before and is freshness/quality
work, not a new adjacency move; a do-nothing control would reach the same counter. So the planned row works **depth**
as the lowest axis, and leaves adjacency declared-unchanged (no harm).

## 5. Best round-41 planned row (draft text)

```
## Round 41 — declaration (planned row, draft)

Base: the round-40 measured tip (declared before the after-run). Ordinals at base: depth 8, coverage 9,
operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency are tied lowest; saturation 9 /
window 3 unchanged. No adjacency claim is attempted (a sibling acknowledgement cannot be produced by this lane;
adjacency stays unclaimed and is not harmed). C1 works depth on the storage-integrity frontier (the lowest
axis); C2 works operability on a named carried ceiling (D12).

| Claim | Axis | Surface moved | Counter (frozen; sha256) | Before at base | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | depth (sourced) | `corpus/knowledge/storage-health-r26.md` gains an append-only section (rows SH7–SH10) pinning the scrub-record mechanics from the two unopened SOURCES leads (btrfs-progs 7.x release notes; ArchWiki Fwupd page — `SOURCES.md` "Leads (unopened)" line 322, round-26 clarification line 327): what `btrfs scrub status` reports per filesystem (running/finished, finished timestamp, duration, status code, data/error sums), where the per-filesystem record lives (`/var/lib/btrfs/scrub.status.*`), how the timer-run scrub writes it, and what a stale record means for a reading. No privileged host probe is claimed; the host cell stays `UNVERIFIED` like SH4 | `python3 tools/check-storage-scrub-r41.py --revision <REV>` (frozen; sha256 TBD): reads rule cells (source-derived value, frozen tokens, negation words, paraphrase), quote at cited lines, new mined rows S226–S230, novelty vs SH1–SH6 | entry absent; `rules_verified 0, source_ok 0, novelty_ok 0`, FAIL exit 1 | `rules_verified 4, source_ok 1, novelty_ok 1`, every quote resolves at its cited line, PASS exit 0 | do-nothing (base) fails; X-empty rule cells fail; rows citing only own-work fail; S210-style wrong-anchor row fails; duplicated rules block fails; a host-privilege or host-state claim fails |
| C2 | operability | The census lands `--identity` (closes the D12 ceiling carried since round 11 — "Ceiling: D12 `--identity` not landed (three-command re-derivation stands)", `SCORECARD.md:49`): `bash tools/tsukuroi-census.sh --identity` prints the measured revision by the same rule as the receipts (`git rev-parse HEAD`; `_revision.bind`) and exits 0; `--selftest` stays PASS with one new identity case | `python3 tools/check-census-identity-r41.py --revision <REV>` (frozen; sha256 TBD): exports the census at <REV> into a scratch clone, runs `--identity`, compares output to `git rev-parse HEAD` at <REV>, checks exit 0 and `--selftest` PASS | no `--identity` path; `identity_ok 0, selftest_pass 0`, FAIL exit 1 | `identity_ok 1, selftest_pass 1`, PASS exit 0 | do-nothing (base) fails; identity from a stale revision fails; nonzero exit fails; selftest regression fails; a variant that prints a constant string fails |

Controls, scored with the frozen counters before any seat (run_controls.py): per claim, do-nothing base,
X-empty (rule cells `RULE NOT SUPPLIED`), X-false (negation / wrong values), scripted writer (quote copied as
rule plus every frozen token), and the anti-loop shapes of rounds 30–33 (sourceless fixture; scripted
non-reader) — each must FAIL, only the candidate PASSes.

Causal separability: C1 touches the storage-health entry and `corpus/SOURCES.md`; C2 touches only the census
`--identity` path; neither counter reads the other's surface. No-harm: all six axes re-checked at the tip
(registry-coverage, knowledge-header, adjacency-anchors, section-citations, appended-notices, boot-writers,
recheck-commands, self-assessment gates PASS). Measured revision: the lane branch tip named in the round-41
outcome section, declared before the after-run.
```

Notes on the draft:
- **C1's surface is the storage-integrity frontier (F4), not Core**: it deepens `storage-health-r26.md` the same
  way round 27 deepened the driver plane from outside (`corpus/README.md:250-256`); it does not claim the
  round-26 Core-promotion condition (a census arm reading it) is met. It opens the two leads the round-26
  correction explicitly left unopened (`corpus/README.md:246-248`). It is do-nothing-proof: the rows and S226–S230
  do not exist at base, so the counter fails base (mirrors the round-40 C2 do-nothing control).
- **C2 is the oldest named operability ceiling** (D12, carried since round 11). It is do-nothing-proof: `--identity`
  does not exist at base. Axes are distinct (depth, operability). Saturation 9 does not waive the lowest-axis duty,
  which C1 discharges.
- An alternative depth candidate — pinning the btrfs-overlayfs snapshot-boot mechanism (F3) from the installed
  initcpio hook bytes + mkinitcpio 42.2 images — is viable but weaker: this host has no snapper config and no
  snapshot-boot entry (`systemd-user-plane.md:116`; `snapper list-configs` empty), so its host cell would bind to
  nothing and it would be a pure-source claim. The scrub-record C1 has a clearer boundary to the existing SH rows.
- A third claim on calibration was considered and dropped: the round-39 routed items (§6.3–6.5 of
  `corpus/lessons/round-39-verifier-spotcheck.md`) are already consumed by round-40 seats (Routed*), leaving no
  named calibration debt large enough to beat a do-nothing control.

## 6. What I did not do

- I did not run the C1/C2 counters or the census (planning seat; only reads).
- I did not read sibling lane files (only the citations inside lane files and the peer roster).
- Round-40 measured outcome and non-author closure do not exist yet; verdicts here are against the declaration.
