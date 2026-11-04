# Round 81 — mount-unit plane, gate-standard repair, provenance-header closure

Base `96ad75b84160da58efaee4997576ce718fd72e2b`. Declaration-only commit
`8023711867eaa788f68af09d7f29d24db749cca7`; the L1 scored candidate files before that
declaration, so this round is **not** a compliant pre-data freeze and the chronology
defect stays on the record (`SCORECARD.md` "Round 81 — declaration"). One v1 wave of
twelve seats (three executors, three scribes, one scout, one connector, one reviewer,
one critic, one mutation-tester, one sentinel); the L1 holds the planner role because
the validator forbids a spawned planner.

## Gate

Sources opened 2026-11-04. Both pinned v262 files were re-fetched live this round and
compared byte for byte with `.ufo/waves/round-81/before/src/` (`cmp` rc 0), and the
generator capture was reproduced byte for byte from the installed binary
(`w1/SentinelProbe/probe.txt`).

| Candidate | URL and location | Located quote (≤25 words) | Decision, reason, flip |
|---|---|---|---|
| S331 systemd.mount(5) v262 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.mount.xml, accessed 2026-11-04, SHA256 `afbf3be6…2394`, stripped lines 498-503 | "With nofail, this mount will be only wanted, not required, by local-fs.target or remote-fs.target." (14 words, :500-501) | ADMIT, docs/A, status mined. Teaches MT2 and, with :229-241, MT5. Scope is upstream v262, not the installed Arch build. |
| S331 (same snapshot), x-systemd.before= | same file, stripped :229-241 | "In the created mount unit, configures a Before= or After= dependency on another systemd unit, such as a mount unit." (20 words, :232-234) | ADMIT — the MT5 teaching: the documented way a `nofail` entry re-acquires ordering. |
| S332 own-work generator capture | `.ufo/waves/round-81/before/host/generator.txt`, header 2026-11-04T17:54:25-03:00, SHA256 `8e1bb73b…e4f8`, line 77 | "Options=rw,noatime,nosuid,nodev,logbsize=256k,nofail,x-systemd.before=local-fs.target" | ADMIT WITH CORRECTION, own-work/A, 30d. The row first said "four required mounts land in .requires" (lines 141-145 hold five) and "produced at boot"; both cells are corrected before the row's first commit, so no supersession row is needed. |
| systemd-fstab-generator.xml and fstab-generator.c (snapshots, `before/src/`) | `.ufo/waves/round-81/before/src/` | none quoted in the entry | NOT ADMITTED, no row: the entry names their digests in the JSON but no MT row or sentence cites them. Flip: a row plus a sentence citing them. |
| REJECTED reading of S331: "nofail guarantees no waiting even with an explicit Before=" | S331 stripped :229-241, :335-347; S332 :77 | — | REJECTED: the manual makes `x-systemd.before=` order a `nofail` mount before a target, and this host's `tmp.mount` carries `Before=local-fs.target` with `nofail` in `Options=`. Flip: a located v262 passage that makes `Before=` ineffective under `nofail`, or a boot measurement (none exists). |
| REJECTED adjacent page: ArchWiki "Fstab", https://wiki.archlinux.org/title/Fstab, opened 2026-11-04 | section "External devices" | "a disconnected external device with only nofail will make your boot take 90 seconds longer" (16 words); page banner "the nofail option does not work as described here" | REJECTED, no row: community page, no revision/oldid anchor, and the page's own banner marks the claim disputed. Flip: an oldid-pinned revision citing the v262 source for a boot wait, plus a host measurement. |

Registry changes (old → new): no existing row changed
(`git diff --numstat 96ad75b8 -- corpus/SOURCES.md` → `2 0`). S331 and S332 are new
rows: status none → mined, recheck none → on-release / 30d, used-by none →
`corpus/knowledge/mount-unit-fstab-plane-r81.md` (this lesson appended). Census rows
330 → 332; malformed 0 → 0; tier A 313 → 315.

Both rows are uncommitted first-appends, so their cells were corrected in place
before the first commit instead of by a `supersedes` row (CORPUS rule 2 protects
committed rows; no committed row held these ids — `git log -S S331 -- corpus/SOURCES.md`
is empty). Corrections, old → new: S331 `teaches` "the x-systemd.* dependency options
attach to the created mount unit only" → "the x-systemd.requires/wants and
x-systemd.before/after options attach … (wanted-by/required-by carry no such
sentence)", because the "always applies to the created mount unit only" sentence
exists only under those two options (stripped :210-212, :246-248); S331 `anchor`
`nofail :498-503` → `:498-504` (the ordering sentence runs to :502-503);
S332 `teaches` "only the /tmp entry carries the Before=" → "of the two nofail entries
only /tmp … (the five required mounts carry Before= from DefaultDependencies)",
because six generated units carry `Before=local-fs.target` (capture :9, :24, :55,
:70, :85, :100); S332 `anchor` gains `pinned at lane commit 80237118` beside the
timestamp. Seats' audit pointers: `w1/ScribeSources.md` V-S331-1/2, V-S332-2/3/4.

Non-author spot-check: pending (the round's closure owns it).

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| **R81-CITED-LINES-STRIPPED** — every MT row and the S331 anchor cite numbers that index the tag-stripped XML, not the file: 707 raw lines become 703 because the DOCTYPE (raw 2-3) and a `<ulink>` (raw 84-85) each swallow a newline, so every cited range is two lines early and MT1/MT4 fall outside their cited window in raw coordinates | `w1/ExecRows/findings.json` F4; `w1/ScoutSurface/contradictions.md` C4; raw spans MT1 135-138, MT2 502-503, MT3 486-487, MT4 491-492, MT5 234-236, MT6 339-341, MT7 198-201, MT8 259-260 | **none** — R5 locates quotes in the stripped list and cannot see the raw file; the entry called the anchors "v262 upstream lines" | Disclosed this round in the entry's Limits and in S331's anchor cell; next round the counter must strip tags per line (preserving line count) and add a selftest case carrying a multi-line tag |
| **R81-WRONG-UNIT-LEG** — MT5's measured leg cited S332 :99-100, which is `var-log.mount`'s default `Before=`, not the `x-systemd.before=` effect on `tmp.mount`; the prose cited "S332 :35-47 vs :95-107" where :95-107 is also `var-log.mount` | `w1/ScribeEntry/audit.md` D4/D5; `w1/ExecRows/findings.json` F3; capture blocks fast 35-47, tmp 64-77 (`Before=` at 70, `Options=` at 77), var-log 94-107 | **none** — R7 is substring-only and cannot tell which unit a range belongs to | Leg re-pointed to `tmp.mount` :69-70 and the prose to :64-77 vs :35-47 before landing; routed: R7 needs a unit-header check |
| **R81-COUNT-NO-COMMAND** — "six local file systems; four are required" contradicted the entry's own list of five and `/etc/fstab` (nine non-comment rows: seven local mount points, five required, two `nofail`, plus swap and `/dev/shm`); S332's `teaches` cell repeated "four required mounts" against capture lines 141-145 | `w1/ScribeEntry/audit.md` D1; `w1/ExecRows/findings.json` F1; `.ufo/waves/round-81/after/host-fstab-20261104.txt` | **none** — CORPUS's "a count carries its command" is not mechanical | Prose and S332 both corrected to five/six-of-seven and cited to the fstab capture before landing |
| **R81-OPTIONS-CLAIM** — "the generated `Options=` line … drops the `x-systemd.*` tokens" is false: `tmp.mount` keeps `x-systemd.before=local-fs.target`; only `x-systemd.device-timeout=` is consumed into the `.device.d` drop-in | `w1/SentinelProbe.md` (falsifier fires, `tmp.mount` Options at capture :77); `w1/ExecRows/findings.json` F2 | the sentinel falsifier the wave ran; the author's own trial did not test the token class | Sentence narrowed to the one consumed token, with the mechanism named from `fstab-generator.c` (`write_options` is fed the device-timeout filter only) |
| **R81-BOOT-TIMING** — "measured on this boot" and "up to ten seconds" were unmeasured: the generator files were regenerated 2026-11-04 17:34:49 after the 2026-11-02 12:07 boot, and the 10 s `JobRunningTimeoutUSec` sits on the by-uuid alias while the kernel device unit the mount requires reports `1min 30s` | `w1/ScribeEntry/audit.md` D3/D6; `w1/ScoutSurface.md` C3 | **none** — the declaration's Limits said "no boot test" but the prose did not carry the limit | Regeneration time and the unknown cause stated; the delay marked [INFERENCE] with both timeout values named |
| **R81-STALE-DIGEST** — the entry cited the `/etc/fstab` capture as sha256 `a265a504…de35`; the committed capture hashes `9effc73c38e7047f3f7fbbcfff363f82421afeda4647cbf122646de077c56d3d` | `corpus/knowledge/mount-unit-fstab-plane-r81.md:31`; `sha256sum .ufo/waves/round-81/after/host-fstab-20261104.txt`; `w1/ScribeEntry/audit.md` D9 | **none** — no gate hashes a receipt path quoted in prose; C1's R4 hashes only the `before/src` manifest | Digest recomputed and corrected before landing; routed: a cited-receipt digest check |
| **R81-UNMARKED-INFERENCE** — "filtered at mount time, so the kernel view is clean" was stated as fact although no pinned snapshot holds the filter | `corpus/knowledge/mount-unit-fstab-plane-r81.md:67-69` (now marked `[INFERENCE]`); `SKILL.md:6182` | none — CORPUS's observation/inference separation is prose discipline, not a gate | Marked `[INFERENCE]` in both the entry and the SKILL row before landing |
| **R80-C2-REGISTRY-NAME** (mined from the round-80 closure) — round 80's C2 synthesised `check-transaction-order-r39`; the committed row is `transaction-order-r39`, so the repaired real row stayed uncounted | `corpus/lessons/round-80-verifier-spotcheck.md` Routed defects 1; `corpus/lessons/round-80.md` | QUALITY 111, written after that miss, so it was not in force at the round-80 freeze | This round's declaration keeps the literal registry rows in `before/actual-registry-identities.json` and invents no filename-derived label |

## Seat harm

From `w1-results.json` (12 seats, 12 settled). No process trace or seat disclosure
of a seat-to-seat incident was observed. Two attack seats, `ReviewRows` and
`CriticFreeze`, returned after their first message with no report file and no error
text; the settlement attributes nothing to a sibling seat, so the cause stays `[unk]`
and is not attributed by timing.

| Round | Harmed seat | Causing seat | Evidence class | Effect | Fix |
|---|---|---|---|---|---|
| 81 | none observed | — | wave settlement (`w1-results.json`) | no kill signal, scratch collision or shared-file collision reported by any seat | none needed |
| 81 | `ReviewRows`, `CriticFreeze` (dead) | `[unk]` | seat output only: a first-turn preamble and no report; no provider error captured | both attack seats produced no falsification; no attack credit claimed | none in-round; a dead seat stays dead in the evidence |

## Wave outcome

Twelve seats dispatched as one v1 wave; ten durable reports, two dead attack seats,
residual 0. Attack share by role is 1/12 (the mutation-tester); the two designated
attack seats died at their first turn, so the ≥25 % attack-role share is **not met**
and is reported as a protocol deviation rather than papered over. Falsification was
carried by non-attack seats: the sentinel probe fired the `Options=` falsifier, the
executor's row re-derivation found the coordinate drift and two prose contradictions,
the scribe's prose audit produced 15 defects, and the scout's live-surface sweep found
three contradictions. The mutation seat killed 7 of 26 single-clause mutants across
the two new instruments (C1 3/18, C2 4/8) and named 17 behaviour-bearing survivors as
coverage debt.

## Limits

- C1's counter verifies quote location, digests and row shape; it is not semantic
  entailment, and its selftest leaves 13 clauses unguarded.
- C2's frozen table is a finite behavioural battery over six cases; a case-aware
  forger, or a `--selftest` that prints the expected token, survives case A.
- C3's gate reads the last column-0 `verified-at:` line; the appends carry a date
  supported by this round's own `sha256sum -c` runs, not by a re-fetch of the
  round-71/72 upstream tags.
