# CriticClaims — round 84, wave w1 (tsukuroi)

Lane revision measured: `master = f19e73f3aa9817e76044e4e43a343c6ca6d929df`.
Claims read at freeze `e0f42051bf9b01af5857c28562ca0247a8fef367`, candidate
`c6ee78b2d4184ace3c6d01116190729f0f7c2c31`, C1 re-declaration `69915b8603d9e443f2e1c0021d7c34509186bd9e`.
Commands were run from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`; battery and gate runs used
`TMPDIR=/fast/scratch/hyaku/tsukuroi-r84/CriticClaims`. Receipts (gate sources, battery JSON, crafted
documents, the proposed battery patch) are copied to
`.ufo/waves/round-84/w1/CriticClaims-receipts/` with `SHA256SUMS`. Nothing in the lane was
written; no `git`/`jj` mutation was run.

Axes in play: **operability** (C2) and **freshness/repair** (the lane's host-operability surface).
I attacked the C2 measurement, the chronology, the C1 re-declaration, and the operability-vs-bookkeeping
question.

## Verdict summary

| Item | Verdict | Basis |
|---|---|---|
| C2 against its **frozen predicate** (13/13 families on the committed host base + 5 unseeded random bases) | **met, reproducible** | candidate run exit 0, `families_passed 13`, 74 cases, 2.8 s; receipts `battery/battery-candidate.json` |
| C2 as the **claim sentence** ("implements the frozen eight-rule set") | **not established by the frozen instrument** | two gates that do not implement the rule set read **13/13** (`battery-f1.json`, `battery-f2.json`); a first-fault-only gate reads 13/13 (`battery-f4-firstfault.json`); see F-C2-1..3 |
| Target reachable by a correct independent implementation (r82 class) | **yes** | `battery-l-literal.json`: `families_passed 13`, exit 0, from a from-scratch literal implementation; near-miss reads 12/13 (`battery-n-nearmiss.json`) |
| Chronology: freeze contains instruments/inputs/controls and precedes the candidate | **holds** | ancestry exit 0, distance 1, declared sha256 = actual sha256, no instrument byte changed; see F-CH-1..2 |
| C1 re-declared exploratory | **allowed in form, but post-data reclassification** | F-C1-1 |
| C2 an operability move (new runnable arm), not bookkeeping | **yes** | `python3 tools/check-hibernate-resume.py --live` → `{"findings": [], "verdict": "HEALTHY"}`, exit 0, on this host |
| Any axis harmed by the landed bytes | **none found** | additive only: new gate, new entry, new SOURCES rows, QUALITY 118, lesson; frozen instruments byte-identical |

## C2 — measurements that reach 13/13 without the eight rules

### F-C2-1 (severity: high) — a gate that reads nothing reaches 13/13

**Claim.** The battery's expected answers form a deterministic sequence that depends only on the run
shape, not on the facts, so a gate can replay it without opening the `--facts` file. The freeze's
defence sentence — "generates five unseeded random host bases per run, so a candidate that memorises
fixtures or the committed host base cannot follow" (`SCORECARD.md:7158`) — covers base memorisation,
not schedule memorisation.

**Evidence.** The plan order is fixed at `tools/resume-gate-battery-r84.py:207-214`
(`POSITIVE`, `MALFORMED`, then `IDS` in list order, `FILE_ONLY` skipped), base order at `:195-198`
(`host` then `random0..4`; `random4` is always the partition base because `file_swap=(i % 5) != 4`),
74 calls. `f2-replay.py` (in the receipts) answers from a position counter keyed on the battery's PID
and never opens the facts file:

```
python3 tools/resume-gate-battery-r84.py --gate .../gates/f2-replay.py
EXIT:0
{'families_passed': 13, 'families_total': 13, 'verdict': 'met', 'failed_families': []}
```

It also passes with `--random 0` (prefix of the same sequence): exit 0, 13/13. This is the cheapest
control that skips the claimed work (prompt §9), and it meets the frozen target. Per §9, "if it meets
the target, the counter or target is wrong".

**Impacted axis.** Operability (the measurement that would credit the arm). The gate itself is not
implicated.

**Smallest safe correction.** Randomise position: after the plan is built, `rng.shuffle(plan)` before
the `for` at `:214` (one line; the rng is already unseeded per run). A content-based gate is unaffected,
a schedule replay has nothing to replay. A next-round re-freeze, not a rescue of this round — the r84
predicate is frozen and the candidate has already been counted.

### F-C2-2 (severity: high) — a signature gate with three rule clauses unimplemented reaches 13/13

**Claim.** The battery enumerates one single-fault case per finding ID per base; it never exercises
rule 1's "nothing else is evaluated", rule 2's antecedent (`resume_swapfile not null`), or the
conjunction of two findings. A gate can therefore pass while violating the rule set.

**Evidence.** `f1-signature.py` (44 lines) never reads `resume_swapfile` (`check-hibernate-resume.py:95`
is the frozen antecedent), has no rule-1 short-circuit (`check-hibernate-resume.py:87`), and maps
"no `resume_offset=` on the cmdline while `map_swapfile_offset` is set" to `HR-OFFSET-MISSING`
instead of the frozen rule 2 branch:

```
python3 tools/resume-gate-battery-r84.py --gate .../gates/f1-signature.py
EXIT:0
{'families_passed': 13, 'families_total': 13, 'verdict': 'met', 'failed_families': []}
```

On documents the battery never generates, F1 and the candidate disagree (verbatim, receipts
`doc-*.json`):

```
== multi                 (COW + hooks resume-before-encrypt)
  check-hibernate-resume.py: rc=1 {"findings": ["HR-HOOK-BEFORE-ENCRYPT", "HR-SWAPFILE-COW"], "verdict": "DEGRADED"}
  f1-signature.py:           rc=1 {"verdict": "DEGRADED", "findings": ["HR-HOOK-BEFORE-ENCRYPT", "HR-SWAPFILE-COW"]}
== nores-second-fault    (no resume= AND image_size > free swap)
  check-hibernate-resume.py: rc=1 {"findings": ["HR-NO-RESUME-ARG"], "verdict": "DEGRADED"}
  f1-signature.py:           rc=1 {"verdict": "DEGRADED", "findings": ["HR-NO-RESUME-ARG", "HR-SWAP-TOO-SMALL"]}
== partition-offset-no-map
  check-hibernate-resume.py: rc=0 {"findings": [], "verdict": "HEALTHY"}
  strict-mapfile.py:         rc=1 {"verdict": "DEGRADED", "findings": ["HR-OFFSET-MISSING"]}   # plausible misreading
```

The candidate is substantively correct on all three; the instrument cannot see the difference.
§9 forbids a universal clause unless the counting command enumerates the full set: the claim sentence
"implements the frozen eight-rule set" is stronger than what 13 single-fault families measure.

**Impacted axis.** Operability (claim credit), depth of the verification, not the tool.

**Smallest safe correction.** Add two families to the next freeze: `MULTI` (two perturbations, expected
sorted pair) and `RULE1-SHORT-CIRCUIT` (no `resume=` plus a second independent fault, expected exactly
`["HR-NO-RESUME-ARG"]`), plus one `PARTITION-OFFSET-NO-MAP` positive to pin rule 2's antecedent.
Exact code blocks: `CriticClaims-receipts/proposal-battery-r84.md`.

### F-C2-3 (severity: medium) — a first-fault-only gate reaches 13/13

**Claim.** Because every generated case carries exactly one fault, a gate that stops at the first
violated rule is indistinguishable from one that returns the full set.

**Evidence.**

```
python3 tools/resume-gate-battery-r84.py --gate .../gates/f4-firstfault.py
EXIT:0
{'families_passed': 13, 'families_total': 13, 'verdict': 'met', 'failed_families': []}
```

On `doc-multi.json` it returns `["HR-SWAPFILE-COW"]` where the candidate returns both findings
(verbatim above). Rule-set composition is unmeasured.

**Severity rationale.** Same class as F-C2-2; listed separately because the correction (the `MULTI`
family) is shared.

### F-C2-4 (severity: low) — the random legs are neutralised by a shape switch; only the host base still discriminates

**Claim.** "a candidate that memorises the committed host base cannot follow" is true only while the
memoriser is applied to random-shaped documents too. A two-line shape test (`"sys_power_disk" in f and
captured_at endswith "-01T00:00:00Z"`, both generator-only markers) switches the committed-base
memoriser on for the host base and a signature comparator on for the random bases.

**Evidence.** `f3-shape.py` scores **10/13**: it fails only `HR-NO-ACTIVE-SWAP`, `HR-NO-RESUME-HOOK`,
`MALFORMED` — exactly the three host-base families that the committed `c2-control-basediff.json`
already fails on the host (10/13 on host, 0-1/13 on each random base). All 61 random-base cases pass
under the switch. So the unseeded bases stop base memorisation on the random legs, but a shape test
removes that defence at zero domain cost; the 13 host-base cases are what remains, and a memoriser that
adds precedence for those three host families would reach 13/13. Severity low because F3 itself does
not reach 13/13 and because F-C2-1 already defeats the instrument more simply.

### F-C2-5 (severity: low) — rule 1's precedence over validation is pinned only for a non-string cmdline

**Claim.** The frozen text says type/schema errors are rc 2 and rule 1 says "nothing else is evaluated";
the battery exercises the conflict only through `cmdline-type` (cmdline becomes an int). A gate that
short-circuits on a *parseable* cmdline without `resume=` reaches 13/13; a missing-key document with
no `resume=` is never generated.

**Evidence.** `p2-rule1first.py` (rule 1 before *all* validation) scores 12/13 — the only
discriminator is the `cmdline-type` MALFORMED case (`cmdline` becomes an int and a naive rule-1-first
gate answers `HR-NO-RESUME-ARG` instead of rc 2):

```
p2-rule1first.py -> {'families_passed': 12, 'failed_families': ['MALFORMED']}
```

Move the short-circuit behind `isinstance(cmdline, str)` (`p3-rule1-guarded.py`) and it reads 13/13
while still returning exactly `["HR-NO-RESUME-ARG"]` on `doc-nores-second-fault.json`:

```
p3-rule1-guarded.py -> {'families_passed': 13, 'verdict': 'met', 'failed_families': []}
p3 --facts doc-nores-second-fault.json -> rc=1 {"verdict": "DEGRADED", "findings": ["HR-NO-RESUME-ARG"]}
```

No battery case combines a *missing key* with an absent `resume=`, so the missing-key half of the
precedence remains unmeasured.

**Smallest safe correction.** Pin precedence in one sentence in the battery docstring and add a
`MALFORMED` variant that combines a missing key with an absent `resume=`.

### F-C2-6 (severity: low) — the `--live` interface is frozen but unmeasured

The battery tests only `--facts`. I ran the frozen interface on the host (read-only; capture uses
`sudo -n` for `map-swapfile`/`lsattr`/`filefrag` reads):

```
python3 tools/check-hibernate-resume.py --live
{"findings": [], "verdict": "HEALTHY"}
LIVE-EXIT:0
```

It works today; the claim does not measure it. Not a defect in the gate, a gap in the predicate's
coverage of its own frozen interface.

## Chronology and freeze integrity

### F-CH-1 (severity: none) — the chronology holds

```
git merge-base --is-ancestor e0f42051... c6ee78b2...
freeze<->candidate ancestor EXIT:0
git rev-list --count e0f42051...c6ee78b2...
1
git log --format='%H ai=%ai ci=%ci %s' -5 master
f19e73f... ai=2026-11-06 15:58:15 ci=2026-11-06 15:58:15  round-84: registry rows — single tool per row, code-2 maps
c6941ad... ai=2026-11-06 15:57:36 ci=2026-11-06 15:57:36  round-84: register ... (repair)
69915b8... ai=2026-11-06 15:54:02 ci=2026-11-06 15:54:02  round-84: C1 withdrawn ... re-declared exploratory
c6ee78b... ai=2026-11-06 15:52:51 ci=2026-11-06 15:52:51  round-84: candidates — ...
e0f4205... ai=2026-11-05 05:39:34 ci=2026-11-06 15:48:26  round-84: freeze C1/C2 instruments, pinned inputs and controls
```

`git show --stat e0f4205` contains `tools/{capture,count,resume-gate}-*.py`, `.ufo/waves/round-84/before/{src,host,controls}`,
`census-before.txt` and the SCORECARD declaration; the candidate commit adds the entry, the gate,
SOURCES, the lesson, QUALITY 118 and `after/`.

Instrument bytes after the freeze:

```
git diff e0f4205 master -- tools/resume-gate-battery-r84.py tools/count-resume-rows-r84.py tools/capture-resume-facts-r84.py .ufo/waves/round-84/before/
 -> only .ufo/waves/round-84/before/src-lesson/cpython-subprocess.py (added) and tools/check-hibernate-resume.py (candidate)
tools/resume-gate-battery-r84.py  freeze=00310ac2...0964  tip=00310ac2...0964
tools/count-resume-rows-r84.py    freeze=cb70d435...8309  tip=cb70d435...8309
tools/capture-resume-facts-r84.py freeze=cec27b9d...cea23 tip=cec27b9d...cea23
src/SHA256SUMS  = 5d1673de7f893f035cb2808e9579bcdd292339a32dad605c6e3a53d6561f7eef (declared)
host/SHA256SUMS = 4ca3e20939eadff71c190f5e2d27a5f453479d0133321ebd118eb7eef624fde6 (declared)
sha256sum -c SHA256SUMS (host) -> receipt.txt: OK, facts.json: OK, exit 0
sha256sum -c SHA256SUMS (src)  -> exit 0
```

The freeze precedes the candidate by exactly one commit and no C1/C2 instrument byte changed.

### F-CH-2 (severity: low) — the freeze's author date is stale, and `before/` is not byte-frozen

The freeze's author date is `2026-11-05 05:39:34`, identical to its parent's committer date, 34 h
before its own committer date; anyone reading author dates sees the freeze authored before the round-83
verifier commit. Commit-graph order is correct, so this is cosmetic — but it is exactly the field a
spot-check reads first.

Second: `.ufo/waves/round-84/before/src-lesson/cpython-subprocess.py` (S342's pinned snapshot) was
committed with the *candidate* (`c6ee78b`), not with the freeze. It is not a C1/C2 input, so the
declaration's instrument/input freeze holds for C1/C2; but "the freeze commit contains the pinned
inputs" is false for the lesson's input, and a `before/` tree that grows after the freeze is a weak
pin. Smallest safe correction: state `src-lesson/` as a post-freeze, disclosed lesson input in the
SCORECARD withdrawal block, or move it under `corpus/lessons/` evidence rather than `before/`.

## C1 — exploratory re-declaration

### F-C1-1 (severity: medium) — the reclassification happens after the candidate was counted, and it removes the falsifiable condition

**Claim.** §2 item 8 permits at most one exploratory claim: taste-bound, no counting command, verified
only by a named non-author `unprovable-but-better` judgment, its axis score unchanged. The C1
declaration at the freeze was a **measured** claim (counted ≥ 7 rows, kill rule, counting command);
the withdrawal block appended at `69915b86` reclassifies it after the candidate commit and after the
L1 found that the frozen counter's own positive control P1 (junk rows from random spans) reads `met`.
That is disclosed, reasoned, and it does not edit the frozen predicate (verified: the `SCORECARD.md`
diff of `69915b86` against `c6ee78b` is append-only, 23 added lines, no removed line). In form it is
allowed. In effect it converts a claim that failed its do-nothing test into a claim with no target:
the only remaining failure mode is the reviewer declining. §9's "never narrow a target after landing"
is not literally broken (no target was amended), but its purpose is.

**Evidence.**

```
git show --stat 69915b86  -> SCORECARD.md | 23 +++++++++++++++++++++++ (only)
git diff c6ee78b 69915b86 -- SCORECARD.md -> only "+" lines at EOF
python3 tools/count-resume-rows-r84.py --root .
{"verdict": "met", "counted": 10, "failed": 0, "distinct_snapshots": 6, ...}   (exit 0)
ctrl P1 in .ufo/waves/round-84/before/controls/c1-controls.txt: "P1-random-valid-rows-met", counted 7, verdict "met" (three runs)
```

**Why it is not a scoped narrowing of this round's claim.** The round still declares C2 as its
measured claim; C1 is reported as exploratory and earns no ordinal. The admission path is intact if
and only if the wave's named non-author reviewer judges HR1-HR10 per row with reasons, and the report
does not cite the 10/10 as evidence.

**Impacted axis.** Depth (claim credit). No axis harm from the entry itself.

**Smallest safe correction.** (a) In the round report, present C1 as exploratory-pending-review and
never as "10/10"; (b) require the reviewer's per-row reasons in the wave receipt (the prompt's
`unprovable-but-better` path already demands this); (c) for the next freeze, apply §9's skip-work rule
to every positive control, not only to the claim's own counter — the lesson's M3 already says this.

### F-C1-2 (severity: none) — the entry's cited spans check out on the pinned snapshots

I spot-checked every row's cited raw line against the pinned `before/src/` files; each supports its
statement:

| Row | Span | Text found |
|---|---|---|
| HR1 | kernel-parameters.txt:6581-6582 | "given by \"resume=\" at which the swap header is located, in <PAGE_SIZE> units (needed only for swap files)." |
| HR2 | ch-swapfile.rst:127 | "that will print the device physical offset and the adjusted value for" (+ :128 "the value is divided by page size") |
| HR3 | ch-swapfile.rst:118 | "The value is the physical offset on the device. Note that **this is not the same" (+ :119 "value that filefrag prints as physical offset!") |
| HR4 | ch-swapfile.rst:13 | "swapfile - must be NODATACOW (i.e. also NODATASUM, no compression)" |
| HR5 | swsusp-and-swap-files.rst:57-58 | "the swap file has to be active (ie. be present in /proc/swaps)" |
| HR6 | swsusp-and-swap-files.rst:61 | "the location of its header need not be the same as before. Thus every time" |
| HR7 | systemd-hibernate-resume.service.xml:38 | "Internally, it works by writing the major:minor of selected device node to" (+ :39 "/sys/power/resume") |
| HR8 | sysfs-power:307-308 | "Using this sysfs file will override any values that were set using the kernel command line for disk offset." |
| HR9 | mkinitcpio-install-resume:11-12 | "if (( systemd_ver >= 255 )); then / add_binary /usr/lib/systemd/systemd-hibernate-resume" |
| HR10 | sysfs-power:97-98 | "as an upper limit of the image size, in bytes." |

Host-side evidence also verifies: the two mkinitcpio snapshots are byte-identical to
`/usr/lib/initcpio/{hooks,install}/resume` (sha256 `3cf8144c…` / `207d0eb3…`, `diff` empty), the birth
time is really `2026-10-03 17:45:33 -0300` (`stat -c %W` = 1791060333), the UKI evidence lists
`usr/lib/systemd/systemd-hibernate-resume`, and the pre-round tip holds **no** `map-swapfile` mention
(`git grep -l -i map-swapfile 64f45b7 -- corpus/knowledge` → exit 1) while printing
`resume_offset=3795013` twice (`journal-boot-plane.md:62`, `systemd-user-plane.md:218`). The "novel
resolution path / prior state lacked it" part of the exploratory declaration is therefore true; the
per-row taste judgment remains the named reviewer's, not mine.

## C2 — operability move or bookkeeping? Axis harm?

C2 is a genuine new runnable arm: a standalone read-only gate that (i) gates a `resume-facts/1`
document, (ii) can capture and gate the live host (`--live` returned HEALTHY rc 0 above), (iii) names
eleven actionable findings, and (iv) is registered in the lane's tool registry (`c6941adb`, `f19e73f`).
It is not bookkeeping and not a re-labelled ordinal move (operability stays 9 by declaration).

Axis harm: none found. The round's bytes are additive — the three frozen C1/C2 instruments are
byte-identical to the freeze, no existing tool or entry was edited, SOURCES changes are new rows
(`S336`-`S342`), QUALITY gains one rule (`118`), and the lesson is a new file (M1-M3). The only harm is to
**claim admission**: an admitted "measured" C2 would credit the arm on an instrument that a do-nothing
and a signature-only gate both reach in full marks.

## What the canonical judge should weigh

- C2's **gate** is correct on everything I could construct independently (literal reimplementation
  13/13; crafted multi-fault, rule-1, and rule-2-antecendent documents all match the candidate).
- C2's **measurement** is not. The frozen battery accepts a gate that opens nothing (F-C2-1) and a
  gate with three rule clauses unimplemented (F-C2-2, F-C2-3). Under §9 ("if it meets the target, the
  counter or target is wrong"), the honest disposition for r84 is **C2 not verified as stated** — the
  instrument defect is fixable in a next-round re-freeze (shuffle the plan; add `MULTI`,
  `RULE1-SHORT-CIRCUIT`, `PARTITION-OFFSET-NO-MAP`; pin rule-1 precedence), and the target must not
  be re-declared after data.
- C1 is honestly disclosed as exploratory but is a post-data reclassification; admit only through the
  named non-author per-row judgment, never through the counter.

## Refusals / limits

- No hibernate, suspend, `swapon`/`swapoff`, `/sys` or `/proc` write, sysctl, mkinitcpio, limine or
  pacman was run; `sudo -n` was used only by the candidate's own read-only capture through `--live`.
- No `git add|commit|push|stash|checkout|switch|reset|pull`, no `jj` mutation, no sibling lane, no
  model choice, no subagent.
- I did not judge, admit, or land anything: the proposals are for the L1 / next freeze.
