VERDICT: supports

# Seat ConnRound43 — item F-23: round-43 planned row (draft, exact text)

Connector synthesis across the wave-1 frontier draft (`w1/ConnFrontier.md`) and the four open routed items
named by this item. Basis: round-42 declaration freeze `a84fc9dec860f8bea516dff7ddfdc98223cdae52`, base
`c8efaa3f120834541f8de1e5e0367e8d1593bae6`, dispatch tip `78abb8b5cdc9da511b4fc523e661517a68dd33d3`,
lane HEAD `a968393c` at my run. Every evidence line below is in my receipt
`w2/ConnRound43/evidence.txt` (sha256 `f32f728f26a66e140368a6645114d276581daabc8d166b1998227924e5ea772a`).
Read-only: no lane file was written except this report and the receipt; no counter, census, or audit was run;
no host mutation; no tools installed. The one proposed move is the planned row in §3 — one bounded proposal.

## 1. What the four routed items establish (evidence)

1. **boot-chain-audit.sh:480-487 pipefail fail-open (routed, un-fixed).** The function prints `1` iff
   `find /etc/fstab … /usr/lib/modules -newermt "@$btime" -print -quit 2>/dev/null | grep -q .` matches
   (`tools/boot-chain-audit.sh:480-487`, pipefail at `:139` `set -uo pipefail`). `find` exits 1 when any start
   point is missing, `-quit` returns that status, and pipefail propagates it past the `grep -q .` match, so the
   `if` takes the else and prints `0`. `newer=$(boot_inputs_newer)` (`:749`) feeds the `booted=1` gate
   (`:761`, `[ "$newer" = 0 ]`): verdict rule 2 BOOTED-OBSERVED is awarded while a boot-chain input IS newer
   than boot start — a fail-open on the lane's own freshness guard. Reproduced by wave-1
   `w1/C1SweepSites.md:67,:75,:82`; routed as "Not fixed here (routed)" in `SKILL.md:3891`. Reachable on hosts
   where any of `/etc/crypttab`, `/etc/mkinitcpio.conf.d`, `/etc/default/limine`,
   `/etc/limine-snapper-sync.conf` is absent; fixture mode bypasses the code so no selftest covers it
   (`w1/C1SweepSites.md:75`).
2. **C1 counter's observed-channel gaps (QUALITY 90).** The frozen predicate of
   `tools/score-size-invariance-r42.py` is `cases == 10 and invariant == 10 and ns_invariant == 3 and
   selftest_pass == 1 and default_equal == 1` (`:43`). Its three production-path legs run inside `unshare -rm`
   (`:283`) — uid 0 inside the namespace — with the fixed sample names `alpha beta gamma delta`
   (`:175-179,:278`); view-gated fixes (gated on `TSUKUROI_FIXTURE`-or-uid-0, or on those four names) pass the
   full predicate while the production path still reads DEGRADED where BLOCKED is due
   (`w1/C1CritNsView.md:1,:43-45`). The production-identity separation (uid 1000 via subuid mapping +
   `setpriv`, measured working on this host, `w1/C1CritNsView.md:67`) exists only as wave evidence — wave-2
   `w2/C1FinalProdIdentity.md` re-confirmed it at the dispatch tip — not as part of the frozen predicate.
   QUALITY 90 (`corpus/QUALITY.md:177`, R42-OBSERVED-CHANNEL) therefore names these channels open: a leg
   offered as "a view the code cannot tell from production" must run at production identity with per-run
   fixture values, **or** be named an override-free leg with channels reported open.
3. **C2 binding's unanchored match (QUALITY 90, second clause).**
   `VERDICT_RE = re.compile(r'ROW (SC\d) VERDICT: (holds|partly|fails)\b')` (`tools/check-scrub-record-r42.py:66`)
   is unanchored and the report test is a plain substring (`:134`), so a critic's sentence that quotes the line
   in order to dispute the row counts as `holds` — scored PASS by wave-1 `w1/C2CritControl.md` D1 (mutants
   M3/M4/M4b). A verified anchored patch (arity unchanged, baseline still PASS, D1/D2 mutants flip to FAIL) is
   `w1/C2CritControl.md:4` (`§4`, receipts `*C-rec.py.jsonl`). Its cost: the counter must be re-frozen and the
   K0-K5 battery re-scored (`run_controls_c2.py:86` writes a prefixed output line the anchored regex rejects —
   mutant M30). QUALITY 90's second clause states the rule for round 43: a verdict binding counts a line only
   where it is the declared verdict line (anchored, a line of its own), never a substring a disputing sentence
   may quote.
4. **Scrub-record census arm as Frontier→Core.** The promotion condition is written and unmet:
   `corpus/README.md:243` ("becomes Core only after a read-only census arm reads it"), `PROVINCE.md:212-214`
   ("Still Frontier … no census arm reads them"), the entry's own Limits
   (`corpus/knowledge/btrfs-scrub-record-r42.md:149-150`). The R38 coverage precedent
   (`SCORECARD.md:2117`) is the template: a verdict-neutral census arm promotes the storage-integrity line,
   declared on the **coverage** axis. Round 42 confirmed the permission facts the arm needs: record content is
   root-readable only (SC1; `scrub.c:483` `open(…, 0600)`, entry line 33), while the directory, file stat and
   `scrub_speed_max` are unprivileged-readable (`capture.txt:9`; my host re-read: `/var/lib/btrfs` absent,
   `btrfs-scrub@.timer` disabled, `scrub_speed_max` 0). SC6/SC7 source facts verified read-only on the host:
   `/usr/include/linux/btrfs.h:190,1194-1195` (`BTRFS_IOC_SCRUB_PROGRESS`,
   `struct btrfs_ioctl_scrub_args`); `/usr/lib/systemd/system/btrfs-scrub@.service`
   (`ExecStart=/usr/bin/btrfs scrub start -B %f`, `ConditionPathIsMountPoint=%f`, `Nice=19`,
   `IOSchedulingClass=idle`, `KillSignal=SIGINT`) and `btrfs-scrub@.timer` (`OnCalendar=monthly`,
   `Persistent=true`).

## 2. Synthesis — why this row, these axes, this shape

- **Three claims on three distinct axes; the lowest axis is worked.** At base, depth 8 and adjacency 8 are tied
  lowest (`SCORECARD.md:2567`). Adjacency stays unclaimed: every move needs an actor outside the lane (F1/F2
  recipient or integrator action, mori intake format), and the round-40/41 reasoning stands
  (`SCORECARD.md:2295-2296,2458-2459`; `w1/ConnFrontier.md:4`). Depth is the self-producible lowest axis, so
  C2 works depth. C1 works coverage (the scrub-record Frontier→Core promotion, R38 precedent). C3 works
  operability on the routed boot-chain fail-open — the same claim shape as round 42's C1 (a routed early-reader
  defect fixed under a frozen counter), not the round-41-dropped freshness *recheck* of boot-chain-audit (that
  was procedural; this is a demonstrated fail-open with a live verdict effect).
- **QUALITY 90 is folded into the counters, not claimed.** Mirroring round 42's fold of QUALITY 89
  (`SCORECARD.md:2564-2567`): C1's production legs run at production identity (the measured subuid+`setpriv`
  mapping) with per-run fixture values, or are named override-free legs with channels reported open; C2's
  verdict binding is the anchored variant (the `w1/C2CritControl.md:4` patch shape). This discharges both
  routed counter items without spending a claim on instrumentation.
- **One frontier line, two honest moves.** C1 (coverage) and C2 (depth) both work the F4 scrub-record line —
  the census arm promotes the unprivileged-readable subset; the depth rows state why the rest (record content,
  running state, SMART) stays Frontier. C3 works the F3 boot line and is causally separate.
- **Each claim has a do-nothing control that fails** (§3 controls paragraph), scored with the frozen counters
  before any seat, per QUALITY 73/80.

## 3. Round-43 planned row — exact text

```
## Round 43 — declaration (planned row, draft)

Base: the round-42 measured tip (declared before the after-run). Ordinals at base: depth 8, coverage 9,
operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency are tied lowest. If the round-42
measured outcome moves depth to 9, ordinals are re-derived at declaration (adjacency becomes sole lowest,
still lane-internally unreachable; the depth claim below remains the strongest self-producible move). No
adjacency claim is attempted (a sibling acknowledgement cannot be produced by this lane; adjacency stays
unclaimed and is not harmed). Saturation 9 / window 3 unchanged. This round folds QUALITY 90
(R42-OBSERVED-CHANNEL) into its counters: C1's production-path legs run at production identity (uid 1000 via
the measured subuid+setpriv mapping) with fixture values drawn per run, or are named override-free legs with
their channels reported open; C2's verdict binding counts an anchored declared-verdict line only, never a
substring a disputing sentence may quote. C1 works coverage on the storage-integrity frontier's scrub-record
line (promotion condition corpus/README.md:243, PROVINCE.md:212-214, R38 precedent SCORECARD.md:2117); C2
works depth (the lowest axis) on the same line; C3 works operability on the routed boot-chain fail-open
(round-42 wave-1 C1SweepSites; SKILL.md round-42 counters section "Not fixed here (routed)").

| Claim | Axis | Surface moved | Counter (frozen; sha256 named at freeze) | Before at base (expected) | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | coverage | The scrub record (btrfs scrub status, /var/lib/btrfs/scrub.status.*, btrfs-scrub@.timer; SH3/SH4) moves Frontier → Core for the unprivileged-readable subset: the census gains a verdict-neutral `STORAGE btrfs-scrub-record state=… filesystems=N records=N unreadable=N speed_limits=N [detail=…]` line (probe_scrub_record, beside probe_storage_arm), which for each btrfs fsid the mount table lists (round-39 guard, override TSUKUROI_PROC_MOUNTS) reads /var/lib/btrfs (absent → records=0, SC3 semantics: never "never scrubbed"), stats each scrub.status.<fsid> file, and reads devinfo/<devid>/scrub_speed_max per device; a present record whose content is unreadable (SC1 mode 0600 root) reads state=BLOCKED detail=records:unreadable, never HEALTHY and never "never scrubbed". The NVMe SMART line, the record's content, and the running state stay Frontier (SC6 privilege ground). PROVINCE/README promotion paragraphs updated for the subset | frozen successor of the r38 arm counter + the r42 invariance leg discipline (bytes and sha256 named at freeze): fixtures matched against the counter's own unprivileged reads of /var/lib/btrfs and /sys/fs/btrfs in a private unshare -rm view whose content is created inside the child namespace (QUALITY 85), the production legs at production identity (QUALITY 90); per-run tokens; per-run fixture values | base census prints no `STORAGE btrfs-scrub-record` line; fixtures_matched 0/N, live_match 0, FAIL | PASS iff every declared fixture matches and the live line's fields equal the counter's own unprivileged reads, at the implementation commit and at the tip; the no-harm conjunct: the census --selftest at the measured revision is PASS with 0 failed | any fixture mismatches; the live fields differ from the counter's own reading; any run prints other than the declared PLANE set and one rollup; the census --selftest is not PASS; a diff hunk outside the declared census surfaces (probe function + its selftest cases + the promotion paragraphs) |
| C2 | depth (sourced) | corpus/knowledge/btrfs-scrub-record-r42.md gains append-only rows SC6–SC8: SC6 the kernel-side running-state API — BTRFS_IOC_SCRUB_PROGRESS is an ioctl on an fd of the filesystem (/usr/include/linux/btrfs.h:190 struct btrfs_ioctl_scrub_args, :1194-1195 the _IOWR define), so an unprivileged census cannot read running state (grounds SC3's "running state from the kernel ioctl"); SC7 the shipped btrfs-scrub@.service/.timer units — ExecStart=/usr/bin/btrfs scrub start -B %f, ConditionPathIsMountPoint=%f, Nice=19, IOSchedulingClass=idle, KillSignal=SIGINT (↔ S237 scrub.c:437-444 handler), OnCalendar=monthly, Persistent=true — what a scheduled scrub runs and how a stop writes the record; SC8 the host cell (timer disabled, no record dir, scrub_speed_max 0) restated against SC3/SC7. New corpus/SOURCES.md rows pinned, upstream kind for SC6/SC7, digest-checked snapshots | frozen successor of check-scrub-record-r42.py with the QUALITY 90 anchored binding (w1/C2CritControl.md §4 patch shape: line-anchored VERDICT_RE + no-second-contradictory-line report test): per row a quote on its named line of a digest-pinned snapshot with at least one quote inside the row's frozen source window, the row's frozen token (absent at base), a host line naming an existing line of the pinned capture, registry rows new/mined/used-by, and per-row non-author verdicts bound through the wave dispatch + results records + committed reports whose verdict line is an anchored line of its own | entry at base: SC6–SC8 absent, rows 5, FAIL | PASS iff rows == 8 and quotes_ok == 8 and novelty_ok == 8 and host_ok >= declared and sources_ok == 1 and novelty_base_hits == 0 and the bound per-row verdicts read holds (a partly needing a bound residual holds), at the tip | predicate false; any bound verdict reads fails; a partly without a bound residual holds; a report whose verdict line for a row occurs only inside a disputing sentence (mention, not assertion) binds nothing — the anchored binding must reject it |
| C3 | operability | tools/boot-chain-audit.sh:480-487: `find … -newermt "@$btime" -print -quit 2>/dev/null | grep -q .` reads FALSE under set -uo pipefail (:139) whenever find exits 1 on a missing start point, so boot_inputs_newer prints 0 and verdict rule 2 BOOTED-OBSERVED (:761 gate on newer==0) is awarded while a boot-chain input IS newer than boot start; the round fixes the reader (capture find's output, test non-empty; find's error status no longer masks a match) — the routed defect, same class as R41-CENSUS-PIPEFAIL-692 | frozen counter (new): runs the revision's boot_inputs_newer in a private unshare -rm view with the eight start points bound from per-run scratch content (QUALITY 85/90: content created inside the child namespace, production identity), cases: {one start point absent + one input newer → must print 1; all present + one newer → 1; none newer → 0}, compared to a reference find | base tool in the absent-plus-newer view prints 0 (BOOTED-OBSERVED reachable while newer), FAIL | PASS iff the fixed tool prints 1 whenever any start point newer than btime exists even with another start point absent, and prints 0 only when no input is newer, at the implementation commit and at the tip | the do-nothing base prints 0 in the absent-plus-newer view; an error-masking variant (|| true on the find position while still testing grep's match) reads the same as base; any hunk outside boot_inputs_newer and its selftest |

Controls, scored with the frozen counters before any seat: C1 — do-nothing base census (no arm; must FAIL: no
STORAGE btrfs-scrub-record line), constant emitter, count-only reader (stats without EACCES discrimination),
presence-denial (ignores the BLOCKED detail), fixture-gated fix (only under TSUKUROI_* / uid 0), cached-live,
and a 0600-record arm that must read BLOCKED (only the candidate PASSes); plus the QUALITY 90 per-channel
variants (uid-gated, name-gated, mount-table-gated) each FAIL. C2 — do-nothing base, scripted writer (quotes
copied from the row windows), line references shifted, dropped source, and a mention-not-assertion report (the
verdict line quoted inside a disputing sentence; must FAIL under the anchored binding) each FAIL; only the
candidate PASSes. C3 — do-nothing base plus the error-masking variant (must FAIL); only the candidate PASSes.
Expected battery lines: should_fail_accepted 0, control_accepted 1 for each counter; battery committed with
the freeze per QUALITY 73.

Causal separability: C1 touches the census (+ the promotion paragraphs in PROVINCE/README); C2 touches the
knowledge entry and corpus/SOURCES.md; C3 touches tools/boot-chain-audit.sh (boot_inputs_newer + selftest).
No counter reads another claim's surface; C1 reuses the round-39 mount-table guard and the r42 leg discipline
without changing them; C3 does not touch the census. No-harm: all six axes re-checked at the tip, including
score-storage-arm-r38.py, score-storage-hidden-r39.py, check-scrub-record-r42.py, the round-42 census
selftest, and the round-42 frozen counters still PASS at the tip. Measured revision: the lane branch tip named
in the round-43 outcome section, declared before the after-run.
```

## 4. Risks and second-order effects

- **C1 arm vs the lane's read-only rule.** The arm reads `/var/lib/btrfs` and sysfs only; on this host both are
  absent/empty, so the live line is `records=0`. The arm is verdict-neutral by construction (a missing record is
  a gap in evidence, SC3). No census run writes; counter scratch lives under `--scratch` per the r42 counters.
- **C2 re-freeze cost.** The anchored binding changes the counter's sha256; the K-battery must be re-scored
  with `\n`-terminated output lines (`w1/C2CritControl.md:4` cost item 2, scored: prefixed-output K3 fixture M30
  fails under the anchored regex). Budgeted in the row (battery re-committed at freeze).
- **C3 reachability on this host.** All eight start points exist here today (`w1/C1SweepSites.md:75`), so the
  live audit cannot show the fail-open; the counter's private-namespace view is the evidence. This mirrors how
  the r42 C1 counter proves a defect the live host's clean data does not show.
- **D3-class limit carried honestly.** One blob still binds all C2 seats, and `transcripts_bound` cannot
  falsify a bound verdict (`w1/C2CritControl.md` D3/D4); the anchored binding closes mention-as-assertion (D1)
  and the contradictory-report line (D2) only. The C2 row text says what the binding counts, per the C2CritControl
  §4 proposed docstring.
- **Interaction with the R42-C1 residual.** The mid-line `error:` token (`w1/C1ExecLiveLarge.md:4`) touches the
  packages plane only; the C1 arm and C3 fix do not interact with it. It remains a candidate future operability
  item, deliberately not in this row (bounded proposal).
- **Axis harm check.** No claim touches adjacency, freshness, calibration, or saturation/window; the row is
  no-harm by construction, with the six-axis re-check named as a kill-rule conjunct.

## 5. What I did not do

- I did not run the C1/C2 counters, the census selftest, or boot-chain-audit.sh (planning seat; read-only
  queries and file reads only; the host is loaded and sibling seats own those runs).
- I did not freeze any counter bytes or re-score the K-battery (L1 work at round-43 declaration).
- I did not read sibling lane files; citations inside lane files only.
- Round-42 wave-2 is in flight; ordinals at the round-43 base are declared per the round-42 measured outcome
  with the branch note in the row text.
- No tools installed or upgraded (nothing was needed).
