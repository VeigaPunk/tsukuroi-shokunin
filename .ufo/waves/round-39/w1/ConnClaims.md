VERDICT: defect-found

Seat: ConnClaims-3 (tsukuroi lane, round 39, wave 1). Item X-1 — cross-claim pattern finding.
Read-only on lane content; no host mutation; no installs needed (all evidence via `grep`/`sed`/`read`).
Report: `.ufo/waves/round-39/w1/ConnClaims.md`; receipts: `.ufo/waves/round-39/w1/ConnClaims/evidence.txt`.

# The one pattern across the three anchors

C1 (r39), C2 TO8 and the round-38 lesson are the same rule stated on three surfaces:
**no absence and no tag graduates to a fact without a second witness that can fail.**

- C1: an absent `/sys/fs/btrfs` root was read as "no btrfs mounted" → HEALTHY 0/0/0 (the
  false all-clear). Round 39 adds the witness: the mount table
  (`tools/tsukuroi-census.sh:1903-1916` — btrfs mount without sysfs →
  `BLOCKED detail=mounts:btrfs-without-sysfs`; unreadable table → `mounts:unreadable`; a root
  with fsid entries never reads the table).
- C2 TO8: the `ALPM-SCRIPTLET` log tag was readable as "an install scriptlet ran"; the witness
  that separates the readings is the transaction phase boundary (`transaction started` /
  `transaction completed`): 252 of 441 tag lines lie outside every commit phase and are hook
  output (`corpus/knowledge/pacman-transaction-order-r39.md:34`).
- Round-38 lesson: "a clean zero that is indistinguishable from an unobserved zero"
  (`corpus/lessons/round-38.md:130`) — pass condition "measured 0" while the observation key
  is narrower than the channel space, "so a leaking control reports a clean 0 and the number
  reads as evidence" (:130).

Surveyed for other instances: all six census planes + the storage/DRIFT arms of
`tools/tsukuroi-census.sh`, `SKILL.md` (decision table :33-135, journal block :488+, OOM block
:1080+), and all 84 files of `corpus/knowledge/`.

# Findings — live instances of the class (not covered by any declared conjunct)

## F1. packages plane: a clean `-Qkk` over a FIXED 8-name prefix reads as the plane's pass

- `tools/tsukuroi-census.sh:673` — `mapfile -t names < <(printf '%s\n' "$CAP_OUT" | grep -v … | head -n "$SAMPLE_N")`
  over `pacman -Qq` output. `pacman -Qq` is alphabetical, so the "sample" is the same first 8
  names every run (deterministic prefix, not a sample). The two live gate runs printed the
  identical set: `sample=8(1password-beta,1password-cli,7zip,aalib,abseil-cpp,acl,adwaita-cursors,adwaita-fonts)`
  (`SKILL.md:301` and `SKILL.md:881`).
- `tools/tsukuroi-census.sh:652` — `PKG_V=HEALTHY` up front; drift comes only from those 8
  packages (`:695-702`); nothing else can move the packages plane to DEGRADED except the
  foreign arm. So `drift=0` over the prefix → plane pass, while 1180 of 1188 installed
  packages are structurally never observed by the gate.
- The header discloses the bound (`tools/tsukuroi-census.sh:87` "bounded sample of
  `pacman -Qq` (SAMPLE_N=8, default)", `:102-104` "The sample is bounded on purpose… belongs
  to the operator checklist") and the note prints `sample=8(names)` — so this is a
  declared trade, not a hidden one. But it is exactly the lesson's shape: the observation key
  (8 fixed names) is narrower than the channel space (all installed packages), and the plane's
  clean zero "reads as evidence" of package integrity.
- Witness that would separate the readings: the full `-Qkk` sweep (~17 s warm, the operator
  checklist step `SKILL.md:104`), or a rotating/random sample so the observed key moves across
  the space. Same shape, already disclosed inline: journal arm 5's `armed=` count is over the
  scanned subset only, bounded by `TIMER_SCAN_MAX` (`tools/tsukuroi-census.sh:1480-1491`,
  `timers_enabled=te timers_scanned=ts` printed at `:1506`).

## F2. journal plane arm 4: `failedhist` is computed over a REPLACED corpus when the err stream is empty

- Arm 4 is documented as "journal-derived from the same err stream" (`tools/tsukuroi-census.sh:262-265`
  header; `:1469-1470` "journal-derived: units that failed earlier … still named").
- But when the err stream is empty, arm 3's no-data guard **overwrites the shared capture
  buffer**: `:1447-1448` runs `cap "$JOURNALCTL" -b -n 1 -o json` (one arbitrary-priority
  entry) and `:1451` blocks correctly on 0 lines. Control then reaches `:1472`:
  `fh_n=$(printf '%s\n' "$CAP_OUT" | grep -cE …CLASS_FAILED…)` — now grepping that ONE
  arbitrary entry, not the err stream.
- Effect: the number printed as `failedhist=$fh_n` ("failed services HISTORY this boot",
  `:1506`) has a stated corpus (the err stream) ≠ its actual corpus (the last journal entry,
  any priority). A spurious `CLASS_FAILED` match in that one line yields `failedhist=1` →
  journal plane DEGRADED on a wrong corpus. The failure direction is toward DEGRADED (a false
  alarm, not a false pass), and it requires the single most-recent line to match, so blast
  radius is small — but it is a live wrong-corpus count in the same gate that just shipped the
  C1 absent-root fix.
- Witness that would separate the readings: derive `fh_n` from its own
  `journalctl -b -p err -o json` capture (grep -c over an empty capture is honestly 0),
  independent of arm 3's emptiness probe.

# Findings — the class carried honestly (absence admitted as unknown, witness named)

- `corpus/knowledge/timer-drift-plane.md:183` (decision row 5): `Δ<P` with no manager-start and
  no transaction in the window is classified "early — external activation (or unknown)";
  "indistinguishable from an early timer fire at default log level [unk]"; the discriminator
  (`journalctl --user -u <service>` around the fire; `InvocationID`) is named, and the sharper
  one (`systemd.log_level=debug`) is gated as a mutation (§9 U2). Rows 6/8/10 (:184, :187,
  :188) likewise carry "0 occurrences — class defined, unobserved", "failing case unobserved",
  "no suspend event exists in the retained journal ⇒ counterfactual [unk]".
- `corpus/knowledge/journalctl-v262-field-filter-r36.md:84-90`: `cap()` merges stderr into
  stdout (`tools/tsukuroi-census.sh:579`) and the grep arms accept rc 1 as "0 entries"
  (`:1247-1251`); measured there: a `--grep` + `-F` rejection line folded into the captured
  output is "counted as one journal line… the same count from a completely different cause".
  Unsolved in `cap()` today; prospective, with the witness named (stderr separation or a
  rejection-line assertion before counting).
- `corpus/knowledge/pacman-transaction-order-r39.md:49` states the class inside C2 itself
  (TO5: the capture "cannot separate 'the hook file was absent' from 'its triggers did not
  match'"), and `:26` (TO2) reads "0 of 60 transactions both remove and add" as "no host
  instance yet", not as proof of absence.

# The same class, already solved in the lane (controls — the witness vocabulary to reuse)

Census guards (all in `tools/tsukuroi-census.sh`):

| site | line | absence/tag | witness that separates |
|---|---|---|---|
| drivers ring | :1018-1037 | `kerr=0` | ring must be non-empty (dmesg / `journalctl -k -b`) — "an empty ring cannot be told apart from a clean one" |
| journal err stream | :1447-1453 | `err=0` | journal holds ≥1 entry this boot (`-b -n 1` probe) |
| oom window | :1258-1273 | empty scans | `--list-boots` measured first; "empty is not a clean window"; `out_of_window` is a coverage fact, never a health fact (header :238-240) |
| storage arm (C1 fix) | :1903-1916 | absent sysfs root | mount table (`TSUKUROI_PROC_MOUNTS`) |
| foreign baseline | :801, :719-722 | `foreign` watch | absent/unreadable baseline → DEGRADED, "never HEALTHY off a missing baseline" |
| systemd `failed=0` | :947 | clean zero of current failed units | second witness in-plane: journal arm 4 `failedhist` names units failed-and-reset earlier this boot (:1469-1481) |
| update-safety log | :1684 | no refresh line in tail | printed as `none-in-window(last N lines)` — "a statement about the window, never about the host" (header :223-225) |

Knowledge entries that carry the same guard (each states the absence→fact gap and its witness):

- `corpus/knowledge/coredump-count-unit-r34.md` — the census `coredump=N` counts entries
  under the `systemd-coredump` identifier; on this host 1365/1621 are "terminated abnormally
  **without generating a coredump**" and 4 are handler errors. The identifier tag is not the
  event; witness = `MESSAGE_ID=fc2e22bc…` + the summary wording + `--all` for oversized
  messages. (`SKILL.md` row R32-H2's each-entry clause is superseded in its each-entry part.)
- `corpus/knowledge/pacman-backup-files-r35.md:36` — "an absent `.pacsave` is not proof that
  the file was unmodified": when the MD5 cannot be computed, `cmp` is 0 and no save is made
  (S192 :536-575). Witness = the `filehash NULL` branch.
- `corpus/knowledge/kernel-taint-r27.md` (KT2 wave-2 correction) — "out-of-tree" had been read
  from the **absence** of the `intree` modinfo tag while the capture never read that tag; the
  kernel tests only the missing tag. Witness = `modinfo -F intree <module>`.
- `corpus/knowledge/errno-contract-variance-r37.md:25` — "An empty retained search is not
  evidence that the mechanism was repaired: it says only that the old log evidence is no
  longer present in the measured window."
- `corpus/knowledge/memory-pressure-r25.md:110` — "A zero difference is not proof of no stall."
- `corpus/knowledge/timer-drift-plane.md:186` (row 7b) — "never classify on `infinity` alone".
- `corpus/knowledge/arch-news-gate-2026.md:23` — "`pacman -Qm` means absent from configured
  sync repositories, not proof of AUR origin".
- `corpus/knowledge/root-dac-decision-r12.md:60` — `findmnt` rc 1 = "not a mountpoint, not
  proof of path absence".
- `corpus/knowledge/pacnew-plane.md:14` — a permission-denied sweep "is therefore not proof
  that no matching files exist below unreadable locations".
- `corpus/knowledge/calibration-synthesis.md:262-266` — the worked example refuting round 3's
  "zero unit-activation failures" by re-reading the journal.
- `corpus/knowledge/seat-boundary-r22.md:24` — "Clean accounting is never a clean strict
  receipt verdict."

# Proposed move (one, bounded)

Route F1 and F2 as next-round debt on the census gate — not as findings against the round-39
conjuncts (they are outside both frozen predicates; no kill rule fires). Both sit in the same
plane family C1 just repaired, and the lane's own routing rule for outside-conjunct findings
is debt, not downgrade (`R38-CLOSURE-DISAGREEMENT`, `corpus/lessons/round-38.md` Mistakes;
SCORECARD round-38 outcome routing). Concretely, a round-40 seat (or the L1 note seat) can:

- F2: derive `failedhist` from its own err-stream capture (one-line change, selftest case
  "err-empty ⇒ failedhist=0 with an arbitrary last line that matches CLASS_FAILED").
- F1: print the bound in the verdict word itself (e.g. `packages=HEALTHY(sample-prefix=8/1188)`)
  or rotate the sample; the witness already exists (full sweep, `SKILL.md:104`).

Why this move and not an edit now: the census bytes are what every round-39 seat's evidence
quotes; a mid-round mutation would repeat the freeze-breach class the lesson records
(r34 VERSION 4/5 amendments, `round-34-verifier-spotcheck.md:55-56`). The pattern finding
itself is the deliverable; the fix belongs to the next declaration's conjuncts.

Affected axes: operability (C1's plane gains two routed, witnessed readings — no harm to the
frozen C1/C2 predicates) and depth (the TO8/tag reading now has a named sibling class with a
reuse-ready witness table). No other axis touched.

# Risks

- F1 is a declared design trade (the bound is printed in the note and header); grading it as a
  defect overstates it. I grade it "structural, disclosed" — the finding is that the pass WORD
  does not carry the bound, not that the bound is hidden.
- F2's trigger requires the single most-recent journal entry to match `CLASS_FAILED` while the
  err stream is empty; I did not construct a runtime reproduction (live journal mutation is
  out of bounds; a namespace fixture run was not necessary to establish the corpus swap —
  the code path is read directly).
- The journalctl-v262 `cap()` exposure is prospective; no current arm passes `-F`/`-N`.

# Verification

- Read: `tools/tsukuroi-census.sh` (all planes + storage arm), `SKILL.md:33-135`,
  `corpus/lessons/round-38.md` (:130 defect sentence), `corpus/knowledge/` entries cited above
  (84 files listed; pattern greps over all of them for "read as / not proof / indistinguishable
  / unobserved").
- Commands run (receipts in `.ufo/waves/round-39/w1/ConnClaims/evidence.txt`): grep/sed line
  pinning on the census (all file:line cites above were re-derived against the working tree,
  tip `2e1c2a40` per dispatch); dedupe grep over `.ufo/waves/round-39/w1/` — no sibling report
  covers the failedhist corpus swap or the fixed-prefix sample.
- Not run: the frozen counters (`tools/score-storage-hidden-r39.py`,
  `tools/check-transaction-order-r39.py`) — my item is pattern finding, not re-scoring; live
  journal/census runs (read-only evidence sufficed; live counts drift anyway per the header's
  own rule).
- TO rows: none judged by this seat, so no `TO<n>:` verdict lines (the kill-rule trailer binds
  seats that judge TO rows; this seat judged census/SKILL/knowledge surfaces only).
- No tools installed; no host mutation; scratch `/fast/scratch/hyaku/tsukuroi-r39/ConnClaims-3`
  used only for TMPDIR and removed.
