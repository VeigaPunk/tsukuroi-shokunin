VERDICT: supports

Item C2-8 — Does the lane already hold SR1/SR3/SR6 as verified knowledge at 6951ead? Is C2 a depth gain, and is the novelty conjunct honest?

# Verdict

C2 is a depth gain, and the novelty conjunct is honest. At base 6951ead, none of the five SR facts exists as verified knowledge: all five exist only (a) as uncounted, seat-written replacement text in the round-42 entry's appended "Corrections — round-42 wave 2" section — which that entry itself declares carries no counted verdict and must not be cited as a verified outcome — and (b) as an appended SKILL.md note that explicitly says the round-42 C2 claim did not verify and instructs reading those rows "through those corrections". The mechanism names the novelty conjunct scans (`scrub_resumed_stats`, `is_scrub_running_in_kernel`) occur nowhere at base; `O_TRUNC` occurs exactly once, inside the excluded corrections section. The frozen counter's novelty conjunct therefore measures exactly what the declaration claims: the facts are not held as verified anywhere outside the uncounted corrections it re-grounds.

# Evidence

All lane reads are `git show`/`git grep`/`git diff` at 6951ead90566b2d74f7c45b4efca29246badad64 (base) and 717b716a8943151ace8657e0ca23d7d9b8434f26 (implementation), read-only. Counter runs: `python3 tools/check-scrub-record-r43.py --lane <lane> --revision <rev>` (writes nothing; exit 1 = FAIL as expected pre-wave-2). Receipts: `.ufo/waves/round-43/w1/C2CritNovelty/{r42.md,r43.md,counter-at-base.json,counter-at-impl.json}`.

## 1. The five facts at base: uncounted corrections only, never verified rows

`corpus/knowledge/btrfs-scrub-record-r42.md` at base:
- :170 section header: "## Corrections — round-42 wave 2 (appended 2026-10-26 after the counted reads; **these carry no counted verdict**)".
- :173-175: "The round's C2 claim is therefore **not verified** … This entry **must not be cited as a verified C2 outcome**; the sentences below are withdrawn or narrowed, and each replacement is the seat's own text, **not re-read by a counted seat**."

Each of the five facts appears in that section, as candidate text, not as a verified row:
- Fact 1 (no O_TRUNC/leftover `_tmp`): r42.md:180-183 — "The `_tmp` is opened `O_WRONLY|O_CREAT` without `O_TRUNC` (scrub.c:517) and never deleted … a later, shorter record … leaves the tail of the older record inside the renamed file, and `btrfs scrub status` reports `invalid data on line …`". Note: the trailing-bytes consequence is stated there as fact, not marked inference; the new SR1 marks it `[inference from the open flags; not reproduced on this host]` (r43.md:25) — an epistemic improvement, not a regression.
- Fact 2 (resume counters/t_start carried): r42.md:184-186 — "On a resume the same code (`scrub_start(…, true)`, :1831-1834) writes a first record that already carries the interrupted record's counters, original start time and accumulated duration".
- Fact 3 (-B gating of recording errors): r42.md:187-191 — "all of them print only in foreground mode (`-B`; `do_print` false by default, :1249), and none changes the exit status, so a scrub whose recording failed exits 0".
- Fact 4 (CAP_SYS_ADMIN for scrub progress): r42.md:196-197 — "the probe `BTRFS_IOC_SCRUB_PROGRESS` needs `CAP_SYS_ADMIN` (this host, uid 1000: `EPERM`), so a caller the ioctl refuses can read `interrupted` while a scrub runs [inference; reachable only with a readable record]". Kernel-source grounding (S240) is absent at base; only the host errno was held.
- Fact 5 (unprivileged status never `running`): held at base only as the contrapositive inside the same correction (r42.md:196-197) and as the appended SKILL.md sentence below.

`SKILL.md` at base:
- :3947-3952 (appended after wave 2): "The scrub-record section above rests on `corpus/knowledge/btrfs-scrub-record-r42.md`, whose C2 claim did **not** verify … Read the `_tmp` and SC3/SC4 table rows through those corrections: a left-over `_tmp` can corrupt a later record (`invalid data on line …`), a resume does not write an all-zero record, a recording failure does not change the exit status, and `interrupted` can be read while a scrub runs by a caller the progress ioctl refuses." This is an instruction to read candidates, not a verified row; it restates the corrections, not a counted verdict.

`corpus/README.md` at base (:410) and `PROVINCE.md` at base (:239-243) describe the round-42 SC1-SC5 *claims* (the withdrawn text), not the corrected facts; neither holds any of the five facts as verified.

## 2. Token scan at base (replicated the counter's `novelty_hits` exactly)

`git grep -n -F -- <token> 6951ead -- corpus/knowledge SKILL.md`:
- `O_TRUNC`: exactly one hit — `btrfs-scrub-record-r42.md:180`, inside the corrections section (heading at :170). The counter excludes hits at `num >= corr_from` where `corr_from` is the corrections heading line, so 0 counted hits.
- `scrub_resumed_stats`: 0 hits anywhere in corpus/knowledge + SKILL.md.
- `is_scrub_running_in_kernel`: 0 hits anywhere in corpus/knowledge + SKILL.md.
- Same tokens also absent from `corpus/lessons` and `corpus/plans` at base (`git grep` over both: no output).

Other `CAP_SYS_ADMIN` hits at base (degraded-triage-r4.md:324,522,627; snapper-eacces-mechanism.md:10,14,26,53,130; mount-errno-contract-r37.md:15; kernel-taint-r27.json:170; freshness-recheck-r17.json:337) concern systemd unit capability bounding, `mount(2)`, and the tainted-sysfs write — none states the scrub-progress ioctl gate, so SR6's specific claim is not held anywhere at base.

## 3. Frozen counter evaluates the novelty conjunct as the declaration frames it

- At base: `rows=0, pointer_ok=0` → FAIL; `novelty_base_hits=0` (counter-at-base.json).
- At 717b716a: `rows=3, quotes_ok=3, props_ok=3, host_ok=3, sources_ok=1, novelty_base_hits=0 (SR1/SR3/SR6 each 0), pointer_ok=1`; `verdicts_ok=0` because no wave-2 seats are bound yet — expected at wave 1; the binding completes in wave 2 (counter-at-impl.json). The counter's docstring (:35-37) documents the exclusion: novelty tokens are scanned "outside the round-42 entry's appended `## Corrections — round-42 wave 2` section (the uncounted text these rows re-ground)".

## 4. What C2 adds beyond the base candidates (the depth gain)

- Verification status: the three rows become quote-bound, digest-checked rows (S237 scrub.c re-opened; S240 Linux v7.2.11 `fs/btrfs/ioctl.c` new; S241 host capture new) judged by counted wave-2 seats — the r42 replacements were explicitly never read by a counted seat (r42.md:173-175).
- S240 is genuinely new verification detail: `ioctl.c:3132-3133` "if (!capable(CAP_SYS_ADMIN)) return -EPERM;" (`r43.md:102-104`) grounds fact 4 in the kernel source, replacing the base's host-errno-only statement; the declaration marks "depth (sourced: S240 opened this round)" (SCORECARD.md:2662).
- SR1 adds the unlink-socket analysis ("its three `unlink` calls all name the progress socket path", scrub.c:1485, r43.md:22,41) absent from the base correction, and relabels the trailing-bytes consequence [inference].
- `pointer_ok`: the implementation adds a supersession pointer in the r42 header ("superseded-in-part: round 43 — SC1 and SC3 … are not a verified outcome", r42 header diff at 717b716a), so a header-reading sweep sees the supersession.

## 5. Novelty conjunct honesty

The conjunct asserts token absence outside the corrections; it does not claim the facts were never stated. That matches the base state and the declaration's own framing ("C2 re-grounds the withdrawn SC1/SC3 text (R42-C2-REGROUND)", SCORECARD.md:2653; "re-grounds those three points as rows", r43.md:9-13). Limit to record: the conjunct is token-based; it does not require the new text to differ from the corrections (a verbatim restatement would still pass novelty). Depth therefore rests on verification status rather than text novelty — which is precisely the declared epistemic move (QUALITY 91 R42-ADOPTED-UNREAD: proposed text is a candidate, never evidence).

# What I did not do

No privileged ioctls, no `capture.sh`, no scrub commands, no git/jj mutation, no lane file writes outside the report and receipts. The counter runs are read-only; exit 1 at both revisions is the expected FAIL state (pre-wave-2 binding at 717b716a, absent entry at base), not a harness error.
