# Considerthese adoption draft — round 65 (L2 seat S2Considerthese, scribe)

Date: 2026-11-03 · Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` · base HEAD `37c74e27`
Execution class: READ-ONLY. This seat wrote **no** lane file other than this draft and its own
report/receipts. Every upstream fact below was opened and verified by this seat (read-only
`curl` / `git ls-remote` / `pacman -Q`), not taken from a prior round's prose.

---

## 1. The proposal selected

**`considerthese/2026-10-24.md:17` — "Upstream release watch"** (proposals only, not acted on).

Verbatim from the file:

> - **Upstream release watch.** The journalctl note exists because systemd 262 changed behavior.
>   I could watch the upstreams the corpus pins (systemd, pacman, btrfs-progs, the kernel) and flag
>   notes whose pinned version is behind the latest release, before a round trips over it.

**Why this one.** Round 64 already adopted the *Counter-attack scoreboard* (`2026-10-26.md:18`),
so that file is excluded by the item. Of the remaining 31 proposals across the seven files, the
upstream-release watch is the one whose ground **is** this round's ground: round 65's C1 is a
sourced note about what systemd **v262** requires of a UKI, and C2 instruments the initramfs/boot
plane. The corpus pins upstream versions by tag (systemd `v262`, btrfs-progs `v7.1`, Linux
`v7.2.11`/`v7.2`, man-pages `6.19`, mkinitcpio `v42.x`, pacman commit `54d9411`) and 212 of 281
S-rows declare `recheck: on-release` — a cadence that **nothing in the lane executes**. The
proposal asks for exactly the missing half: the comparison.

### Still-unimplemented — grep receipts

Scope: `corpus/ SKILL.md tools/` (the lane's own trees), at base HEAD `37c74e27`.

```
$ grep -rn -i -- 'upstream release watch' corpus/ SKILL.md tools/   -> 0 hit(s)
$ grep -rn -i -- 'upstream-release watch' corpus/ SKILL.md tools/   -> 1 hit(s)
    corpus/knowledge/pause-lift-gate-r24.md:90
$ grep -rn -i -- 'latest upstream'   corpus/ SKILL.md tools/         -> 0 hit(s)
$ grep -rn -i -- 'behind the latest' corpus/ SKILL.md tools/         -> 0 hit(s)
$ grep -rn -i -- 'newest upstream'   corpus/ SKILL.md tools/         -> 0 hit(s)
$ grep -rn -i -- 'upstream tag index' corpus/ SKILL.md tools/        -> 0 hit(s)
$ grep -rn -i -- 'release index'     corpus/ SKILL.md tools/         -> 0 hit(s)
$ grep -rn -i -- 'pinned version.*behind' corpus/ SKILL.md tools/   -> 0 hit(s)

$ grep -rln -iE 'releases/latest|kernel.org/releases|tags\?per_page|repository/tags' \
      tools/ corpus/ SKILL.md
    (no output; rc=1)   => no mechanism exists
```

The single `upstream-release watch` hit is **not** an implementation: it is a single open
sentence inside a P3 caveat of the round-24 pause-lift note ("The upstream-release watch for
removal of the compatibility symlink is still open") — one named artifact's watch, in prose, in a
note, with no comparison and no registry row.

No lane tool compares a pinned version to upstream:

```
$ for f in tools/check-recheck-commands.py tools/check-registry-coverage.py \
           tools/check-freshness-r17.py tools/check-cited-receipts-r62.py; do ... done
  tools/check-recheck-commands.py            no version-compare logic
  tools/check-registry-coverage.py            no version-compare logic
  tools/check-freshness-r17.py               no version-compare logic
  tools/check-cited-receipts-r62.py          no version-compare logic
```

`check-recheck-commands.py` inspects a `recheck:` line for **forbidden binaries** (it forbids the
lane from re-authorizing a withheld action); it never asks whether the pinned version is still the
current one. `check-registry-coverage.py` checks that a file under `tools/` has a registry row.
Neither executes the cadence.

### Conflict, stated verbatim for the judge

Round 64's connector recorded the proposal as **not implemented but discharged**:

> `.ufo/waves/round-64/after/connector-assimilation.md:216` — "Upstream release watch
> (`2026-10-24.md`) | 0 hits | not implemented — *but* this round's C3 **is** that watch firing
> (mkinitcpio v42.2), so the round satisfies it directly"

That is a **one-artifact discharge**, and this seat measured it: round 64's C3 re-read
mkinitcpio's `v42` → `v42.2` point release because the corpus's own **frontier bullet** named that
artifact ("watch upstream `btrfs-overlayfs` / `plymouth` hooks on-release",
`corpus/README.md:38-39`), and `corpus/knowledge/mkinitcpio42-onrelease-r64.md` discharges exactly
that bullet. The proposal as written is not that bullet: it says to watch **the upstreams the
corpus pins** — systemd, pacman, btrfs-progs, the kernel — and flag **notes whose pinned version
is behind the latest release**. Round 64's C3 covered one of six pinned upstreams and compared one
artifact's content. Round 47's independent scan had already drawn the same line, in more detail:

> `.ufo/waves/round-47/w1/ConsGate.md:56-59` — "**Already covered? No.** The registry has a
> `recheck:` cadence column (`on-release` for S246-S248, `30d` S249, `180d` S252) and QUALITY
> criterion 8 requires the column to exist, but **nothing executes the watch** … What would land it:
> (1) a standing w1 scout seat that each round lists every `kind: code|docs` registry row, its
> pinned tag, the latest upstream release at read time, and the delta, reporting to the sources
> gate; (2) a QUALITY criterion making that sweep a named, receipted check (criterion 8's recheck
> column becomes measured, not just present); (3) a lesson row in `corpus/lessons/round-47.md`
> recording the first sweep's result. **A SOURCES row alone cannot land it** — the rows and
> cadences already exist; the watch mechanism is the missing half."

Round 49's and round 52's scans agree ("Open/N — No matching implementation record for watching
systemd/pacman/btrfs-progs/kernel releases and comparing all pinned-note versions",
`.ufo/waves/round-52/w1/R52ScoutConsider.md:38`). **This draft takes round 47's reading**: the
artifact watch is discharged, the registry-wide watch is not.

---

## 2. Grounding — the fact under the pointer, verified by this seat

The reflection is a pointer, not evidence, so this seat opened what it points at. The proposal
points at *the registry's pinned upstream versions*, so the grounding is: (a) enumerate the pins
mechanically from `corpus/SOURCES.md`; (b) fetch each upstream's current release/tag index
read-only; (c) report the delta; (d) re-fetch each cited artifact at **both** the pinned version
and the latest, and compare bytes.

### 2.1 The pin inventory (mechanical, from the 281 S-rows)

| pinned upstream | rows | S-ids |
|---|---|---|
| systemd `v262` | 17 | S072, S120, S121, S122, S123, S124, S126, S136, S137, S177, S184, S186, S187, S188, S189, S190, S199 |
| btrfs-progs `v7.1` | 15 | S128, S129, S130, S139, S152, S153, S154, S155, S157, S164, S165, S166, S167, S168, S169 |
| Linux `v7.2` (release tag) | 22 | S115–S119, S132, S133, S138, S140–S145, S148, S149, S156, S158, S182, S185, S201, S205 |
| Linux `v7.2.11` (stable point release) | 5 | S240, S242, S243, S246, S247 |
| mkinitcpio `v42.x` | 10 | S015, S016, S053, S054, S058, S094, S109, S279, S280, S281 |
| pacman commit `54d9411` | 23 | S208–S211, S213–S217, S219, S221–S224, S226, S228–S235 |
| man-pages `6.19` | 3 | S171, S176, S181 |

**95 of the 281 S-rows are pinned to an upstream version**; the remaining rows pin Arch
packaging, documentation or own-work captures, which a release-index watch does not cover.

### 2.2 The delta, measured 2026-11-03

| pinned | latest upstream at read time | endpoint | verdict |
|---|---|---|---|
| systemd `v262` | **`v262.1`** (published 2026-10-16T21:57:14Z) | `api.github.com/repos/systemd/systemd/releases/latest` | **BEHIND** |
| btrfs-progs `v7.1` | **`v7.3`** (commit `afdc3a65e33f`, 2026-10-23T17:09:57Z) | `api.github.com/repos/kdave/btrfs-progs/tags` | **BEHIND, 2 releases** |
| Linux `v7.2.11` | **`7.2.15`** in-line; `latest_stable` **`7.3.1`** | `www.kernel.org/releases.json` | **BEHIND** |
| Linux `v7.2` | **`7.2.15`** in-line; `latest_stable` **`7.3.1`** | same | **BEHIND** |
| man-pages `6.19` | **`6.20`** | `git.kernel.org/.../man-pages.git/refs/tags` | **BEHIND** |
| mkinitcpio `v42.x` | `v42.2` | GitLab releases API | current (round 64 C3) |
| pacman `54d9411` | tag `v7.1.0` (`208ff2b5`) | `git ls-remote --tags` | commit-pin, not a tag |

**5 of the 6 pinned tag/version families are behind their upstream.** The pacman pin is a
**commit** (2026-01-07, "libmakepkg: fix linting of xdata"), not a tag — a correct watch needs both
a tag set and a commit set, and must not report a commit pin as "behind".

### 2.3 Content drift at the cited artifacts — byte comparison, not token match

Every corpus-cited artifact was re-fetched at **both** versions and compared with `cmp`:

```
systemd v262 vs v262.1:      IDENTICAL  man/systemd.kill.xml
                             IDENTICAL  man/oomd.conf.xml
                             IDENTICAL  man/systemd.resource-control.xml
                             IDENTICAL  src/coredump/coredump-submit.c
                             IDENTICAL  src/shared/logs-show.c
Linux  v7.2.11 vs v7.2.15:   IDENTICAL  fs/btrfs/scrub.c, fs/btrfs/ioctl.c,
                             IDENTICAL  fs/btrfs/sysfs.c, fs/btrfs/dev-replace.c,
                             IDENTICAL  lib/cmdline.c
Linux  v7.2 vs v7.2.15:      IDENTICAL  (all three checked)
Linux  v7.2 vs v7.3.1:       DIFFERS    fs/btrfs/sysfs.c
                             DIFFERS    Documentation/admin-guide/cgroup-v2.rst
                             IDENTICAL  mm/oom_kill.c
man-pages 6.19 vs 6.20:      IDENTICAL  man/man5/proc_pid_environ.5,
                             IDENTICAL  man/man5/proc_pid_status.5,
                             IDENTICAL  man/man7/environ.7,
                             IDENTICAL  man/man8/ld.so.8
mkinitcpio v42 vs v42.2:     IDENTICAL  cmds/init (3318 bytes both)
```

**One line window moved.** btrfs-progs `v7.1` → `v7.3` `cmds/scrub.c`: eight of S237's nine cited
windows are unchanged, and one moved:

```
v7.1 67-70     -> v7.3 67-70       offset +0   UNCHANGED
v7.1 280-330   -> v7.3 280-330     offset +0   UNCHANGED
v7.1 446-535   -> v7.3 446-535     offset +0   UNCHANGED
v7.1 826-895   -> v7.3 826-895     offset +0   UNCHANGED
v7.1 1110-1125 -> v7.3 1110-1125   offset +0   UNCHANGED
v7.1 1186-1220 -> v7.3 1186-1220  offset +0   UNCHANGED
v7.1 1330-1340 -> v7.3 1330-1340  offset +0   UNCHANGED
v7.1 1498-1512 -> v7.3 1498-1512  offset +0   UNCHANGED
v7.1 1925-1945 -> v7.3 1927-1947  offset +2   *** WINDOW MOVED ***
```

And one corpus-quoted **literal** changed text while its line anchor survived:

```
corpus/knowledge/btrfs-scrub-record-r42.md:184  quotes scrub.c :569-576 ('invalid data on line ...')
btrfs-progs v7.1 scrub.c:571   warning("invalid data on line %d pos ")
btrfs-progs v7.3 scrub.c:571   warning("invalid data on line %d position ")
```

The line anchor (571 → 571) survives; the quoted text does not. A `v7.3` re-read of that quote
would **fail** a verbatim check. The corpus pins `v7.1`, so its quote is **correct at its pin** —
this is a trigger to re-read, not a defect in the corpus today.

### 2.4 The watch's live question, for this round's own claim

The round-65 C1 note is anchored on systemd **v262**'s release body (S282) and its `recheck:` line
reads "on-release — the next systemd release … re-fires the applicability watch (SY4 falsifier)"
(`.ufo/waves/round-65/drafts/note-systemd262-uki-pcr-r65.md:3`). The watch asks: **has the next
systemd release landed?** It has — `v262.1`, published 2026-10-16, eighteen days before this
round. So the trigger condition was already met when the note was drafted, and this seat can
report what the re-read finds:

- `v262.1`'s release body is 76 bytes: `**Full Changelog**: https://github.com/systemd/systemd/compare/v262...v262.1`
  — no TPM text at all.
- The `Changes in the TPM Subsystem:` section of `NEWS` is **byte-identical** between `v262` and
  `v262.1` (2139 bytes each, same section start at line 439). The `v262`→`v262.1` NEWS diff does
  not touch any TPM/NvPCR/UKI/PCR line.
- The five corpus-cited systemd files are byte-identical across the two tags.

So the honest first-sweep result for this round is: **the trigger fired, and the re-read returns
"no change to the proposition C1 rests on."** The corpus's SY1–SY5 rows are unaffected by `v262.1`.
That is a real result of the watch, and it is a *negative* one — the watch's value here is that it
is now measurable rather than assumed.

---

## 3. The adoption text

Vehicle: **a QUALITY criterion** plus the **lesson row it cites**. Round 47's scan named exactly
this pairing ("(2) a QUALITY criterion making that sweep a named, receipted check (criterion 8's
recheck column becomes measured, not just present); (3) a lesson row … recording the first sweep's
result"). A SOURCES row cannot carry it — round 47 wrote that plainly: "A SOURCES row alone cannot
land it — the rows and cadences already exist; the watch mechanism is the missing half." The
next free criterion number is **98** (`corpus/QUALITY.md` ends at 97, `corpus/QUALITY.md:190`).

### 3.1 `corpus/QUALITY.md` — proposed criterion 98

```markdown
98. **A pinned upstream version is compared with the upstream's current release at read time, and
the comparison is a recorded result rather than a declared cadence (R65-UPSTREAM-RELEASE-WATCH):**
a knowledge row whose `source:` names an upstream artifact by tag, release or commit is listed
with that pin, and the same round records the upstream's current release or tag at read time, the
delta between them, and — for the artifacts the row cites — whether the cited bytes or line
windows are unchanged at the newer version; the registry's `recheck: on-release` column is a
cadence, and a cadence that is never executed is not a recheck, so the sweep is the receipt and
the cadence is only its schedule. The sweep reports a pin delta as a **trigger to re-read**, never
as a defect in the pinned row: a row pinned at an older version stays correct at its pin, and a
re-read that finds the cited bytes and line windows unchanged is recorded as "no change to the
proposition" and discharges the trigger. A pin expressed as a commit is compared against the
upstream's tag set and its commit set, and is not reported as behind a release it never claimed.
Failing example (round 65): the corpus pins btrfs-progs `v7.1` on fifteen S-rows and systemd
`v262` on seventeen, while upstream `v7.3` (2026-10-23) and `v262.1` (2026-10-16) had both
shipped, and no lane row, tool or lesson recorded the comparison; 212 of 281 S-rows declare
`recheck: on-release` and none was ever executed, so "the corpus is on a current release" was a
cadence nobody ran. Lesson: `corpus/lessons/round-65.md`.
```

### 3.2 `corpus/lessons/round-65.md` — proposed lesson row

```markdown
### considerthese — upstream release watch (`considerthese/2026-10-24.md`, proposal "Upstream release watch", 2026-11-03)

Mined by wave seat S2Considerthese (`w1/S2Considerthese.md`; receipt `w1/S2Considerthese-receipts.txt`).
Proposal: "I could watch the upstreams the corpus pins (systemd, pacman, btrfs-progs, the kernel)
and flag notes whose pinned version is behind the latest release, before a round trips over it."

**Still unimplemented at base `37c74e27`.** `grep -rn -i` over `corpus/ SKILL.md tools/` returns 0
hits for "upstream release watch", "latest upstream", "behind the latest", "newest upstream",
"upstream tag index", "release index" and "pinned version.*behind"; the single
"upstream-release watch" hit (`corpus/knowledge/pause-lift-gate-r24.md:90`) is one open sentence
in a P3 caveat, not a mechanism. `grep -rln -iE 'releases/latest|kernel.org/releases|tags?per_page|repository/tags'`
over `tools/ corpus/ SKILL.md` returns nothing (rc=1). Round 47's independent scan reached the same
verdict and named the missing half ("Already covered? No … nothing executes the watch … A SOURCES
row alone cannot land it", `.ufo/waves/round-47/w1/ConsGate.md:56-59`); rounds 49 and 52 agree
("Open/N", `.ufo/waves/round-52/w1/R52ScoutConsider.md:38`). Round 64's C3 discharged the
**artifact** watch the corpus frontier bullet named (mkinitcpio `v42` → `v42.2`,
`corpus/knowledge/mkinitcpio42-onrelease-r64.md`); it did not execute the registry-wide
comparison this proposal describes (`.ufo/waves/round-64/after/connector-assimilation.md:216`).

**First sweep, measured 2026-11-03 (read-only).** The registry's 281 S-rows carry 212
`recheck: on-release` cadences and **0 executed**. The pins, by mechanical URL pattern, and the
upstream's current release at read time: systemd `v262` (17 rows) → **`v262.1`** (2026-10-16);
btrfs-progs `v7.1` (15 rows) → **`v7.3`** (2026-10-23, two releases); Linux `v7.2.11` (5 rows) and
`v7.2` (22 rows) → **`7.2.15`** in-line with `latest_stable` **`7.3.1`**; man-pages `6.19`
(3 rows) → **`6.20`**; mkinitcpio `v42.x` (10 rows) → `v42.2`, current; pacman commit `54d9411`
(23 rows) → tag `v7.1.0`, a commit pin that no release comparison settles. Five of the six pinned
families are behind their upstream.

**Content drift, byte comparison.** Every cited artifact was re-fetched at its pin and at the
newer version. Unchanged: systemd `v262`/`v262.1` (5 files), Linux `v7.2.11`/`v7.2.15` (5 files),
Linux `v7.2`/`v7.2.15` (3 files), man-pages `6.19`/`6.20` (4 files), mkinitcpio `v42`/`v42.2`
(`cmds/init`, 3318 bytes both). Changed: Linux `v7.2`/`v7.3.1` (`fs/btrfs/sysfs.c`,
`Documentation/admin-guide/cgroup-v2.rst`), and btrfs-progs `v7.1`→`v7.3` `cmds/scrub.c`, where
eight of S237's nine cited windows hold and **one moved** (`v7.1` 1925-1945 → `v7.3` 1927-1947,
offset +2) and the literal quoted at `corpus/knowledge/btrfs-scrub-record-r42.md:184` changed text
(`"invalid data on line %d pos "` → `"invalid data on line %d position "`) while its line anchor
(571) held.

**This round's own claim, re-read.** C1's note is anchored on systemd `v262` and its `recheck:`
line makes "the next systemd release" a trigger; `v262.1` shipped 2026-10-16, so the trigger had
already fired. The re-read returns **no change to the proposition**: `v262.1`'s release body is a
76-byte changelog link with no TPM text, and `NEWS`'s `Changes in the TPM Subsystem:` section is
byte-identical between the two tags (2139 bytes, same section start at line 439). SY1–SY5 stand.
A watch that fires and reports "nothing moved" is a result; a cadence nobody runs is not.

**Rule taken.** A pin delta is a **trigger to re-read**, never a defect in the pinned row and never
a re-score: a row pinned at an older version stays correct at its pin, and the sweep's receipt
records the delta, the byte comparison, and the verdict ("no change to the proposition"). QUALITY
98 makes the sweep a named, receipted check, so criterion 8's `recheck:` column becomes measured
rather than merely present. No new capability is claimed: this round's C2 remains the census arm,
and no tool, registry row or corpus entry is changed by this lesson.
```

### 3.3 What this draft does **not** ask for

- **No new SOURCES row.** Round 47: the rows and cadences already exist; the mechanism is the
  missing half. A row would not land the proposal.
- **No new tool.** This seat is READ-ONLY and the sweep is a *reading* procedure over the public
  release indexes; QUALITY 98 asks that a future round record the result, not that this round
  ship a checker. The receipt in `w1/S2Considerthese-receipts.txt` is the wave evidence, as in
  rounds 38/39/41/43/46.
- **No re-score and no re-pin.** The corpus pins are correct at their pins; nothing here claims a
  stale row, and no axis moves.

---

## 4. Full sweep receipt

Every command, count and file above is reproduced verbatim in
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-65/w1/S2Considerthese-receipts.txt`
(109 lines, copied out of scratch before cleanup).
