VERDICT: defect-found

# C2-18 — QUALITY 10 sweep of every mention of the three GR terms

Base: `18389f44cf6ce414d7be205998b29c79fb0b490c` (freeze `ea6e0ee38d8066663bb0871b53bade14441eb304`).
Paths swept: `SKILL.md`, `corpus/README.md`, `PROVINCE.md`, `corpus/knowledge/**` at that revision, read through
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show/grep <REV>` — no working-tree read, no lane write.

Item terms: `memparse`, `suffix`, `dev-replace` / `device replace`, `KillSignal`, `systemctl stop`,
`scrub_speed_max` write semantics.

**Why defect-found.** Three mentions are contradicted by GR1-GR3 and one consequence is asserted flatly where GR3
leaves it undecided. All of them are in `SKILL.md`, the lane's operative decision table: its round-44 scrub section
still carries "(dev-replace.c:701-703,1265-1268, **unpinned**)" (`SKILL.md:4222`) and a Limits block saying
"SR9's systemd side is systemd.kill(5) inference; the SR7 replace side is an unpinned caller [inference]"
(`SKILL.md:4229-4230`). The round's append landed only in the round-44 entry (`btrfs-scrub-record-r44.md:153-161`);
`SKILL.md` has no round-45 block at all (`git show <REV>:SKILL.md | grep -nE '^#+ .*[Rr]ound-4[0-9]'` prints only
`3405`, `3680`, `3945` — round 40, 41, 42).

---

## 1. Commands run (paste, verbatim)

```bash
L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
REV=18389f44cf6ce414d7be205998b29c79fb0b490c
for p in 'memparse' 'suffix' 'dev.replace' 'device replace' 'KillSignal' 'systemctl stop' 'scrub_speed_max'; do
  git -C "$L" grep -n -i -E "$p" "$REV" -- SKILL.md corpus/README.md PROVINCE.md corpus/knowledge
done
# widened during the sweep, because the stale tags do not use the six words:
git -C "$L" grep -n -i -E 'unpinned|not pinned|systemd\.kill' "$REV" -- SKILL.md corpus/README.md PROVINCE.md corpus/knowledge
git -C "$L" grep -n -i 'EINPROGRESS' "$REV" -- SKILL.md corpus/README.md PROVINCE.md corpus/knowledge
git -C "$L" grep -n -i -E 'resumable|canceled|scrub resume|cancel' "$REV" -- SKILL.md PROVINCE.md corpus/README.md corpus/knowledge
```

Per-pattern hit counts at that revision (`git grep -c … | awk -F: '{s+=$NF} END{print s}'`):

| pattern | hits |
|---|---|
| `memparse` | 10 |
| `suffix` | 15 |
| `dev.replace` | 17 |
| `device replace` | 8 |
| `KillSignal` | 13 |
| `systemctl stop` | 2 |
| `scrub_speed_max` | 29 |
| `unpinned\|not pinned\|systemd\.kill` (added) | 16 |

**91 distinct `file:line` hits** over 13 files (`sort -u` of the union; receipt `union.txt`). Distribution:
`SKILL.md` 13, `corpus/README.md` 4, `PROVINCE.md` 3, `btrfs-scrub-record-r44.md` 19, `-r42.md` 5, `-r43.md` 1,
`btrfs-scrub-grounding-r45.md` 40 (the grounding entry itself), and one hit each in six other knowledge files, which
with 3 of the `SKILL.md` hits are the **9 out-of-sense hits** (`.hook`/version/selector "suffix", a documentation
"device replacement", `version-unpinned`; §2).

Full hit text: receipts `grep-*.txt` and `hits-compact.txt` (one line per hit, 96-char excerpt) in
`.ufo/waves/round-45/a2w1/C2ExecSweep/`. Excerpts of the load-bearing ones are quoted inline below.

---

## 2. Classification, hit by hit

Labels: **CONTRADICTED** (GR refutes the mention as written) · **NARROWED** (GR makes it conditional; not refuted) ·
**NOW GROUNDED** (the mention was `[inference]`/unpinned and GR pins it) · **UNTOUCHED** · **OUT OF SENSE**.

### 2.1 SKILL.md (13 hits)

| hit | term | class | why |
|---|---|---|---|
| `SKILL.md:4222` | dev-replace | **CONTRADICTED** | tag reads "(dev-replace.c:701-703,1265-1268, unpinned)". GR2 pins both sites: `dev-replace.c:701-703` = `ret = btrfs_scrub_dev(fs_info, src_device->devid, 0, … &dev_replace->scrub_progress, false, true);` and `:1265-1268` = the same call in `btrfs_dev_replace_kthread` (verified in `.ufo/waves/round-45/frozen/src/dev-replace.c`). Draft D1. |
| `SKILL.md:4225` | memparse + suffix + scrub_speed_max | **NOW GROUNDED**, under-inclusive | "writes parse with `memparse` (K/M/G suffixes, trailing whitespace skipped, else `-EINVAL`)". GR1's set is `K M G T P E` in either case, one letter, 1024 per step, on a base-0 parse (`010`=8, `0x10`=16); a bare newline writes 0 and clears the limit. Not false, but reads as a closed list. Draft D1. |
| `SKILL.md:4226` | KillSignal | **NOW GROUNDED + NARROWED** | the row's Reading cell says "a stopped scrub service cancels the scrub and **leaves a resumable record**". GR3 grounds the signal chain (SIGINT → SIGCONT → SIGKILL after `TimeoutStopUSec=5s`) but leaves the canceled-record write undecided inside that window (`btrfs-scrub-grounding-r45.md:102-104`, `:137-139`). Draft D1. |
| `SKILL.md:4229-4230` | `systemd.kill` + "unpinned" (added pattern) | **CONTRADICTED** | "SR9's systemd side is systemd.kill(5) inference; the SR7 replace side is an unpinned caller [inference]." GR3 pins the former at S248 (systemd v262 `man/systemd.kill.xml`, quoted lines 68/91/96/101/108/114) and the host values at S249 (`capture.txt:3-5`); GR2 pins the latter. Draft D1. |
| `SKILL.md:3918` | scrub_speed_max | UNTOUCHED | SC5 / btrfs-progs print path ("a failed read also prints 0"), read side only; GR1 is the kernel write parse. |
| `SKILL.md:4011` | scrub_speed_max | UNTOUCHED | SC5 narrowing of the printed value, read side. |
| `SKILL.md:4189` | scrub_speed_max | UNTOUCHED | census arm reads the value; no parse claim. |
| `SKILL.md:4201` | scrub_speed_max | UNTOUCHED | "reads a nonzero decimal; 0 = no limit"; the read is `sysfs_emit("%llu\n")` (S243 `sysfs.c:2028`) whatever was written, so GR1 does not change it. |
| `SKILL.md:2676` | device replacement | UNTOUCHED | btrfs-progs v7.1 documentation summary (sizing/repair); GR2 is the kernel copy path, a different statement. |
| `SKILL.md:3186`, `:3530` | suffix | OUT OF SENSE | `.hook` file-name suffix (ALPM hook order), unrelated sense. |
| `SKILL.md:2080` | pattern FP | OUT OF SENSE | adjacency-anchors gate row; matched "not pinned" in a counter description, not the scrub surface. |

### 2.2 corpus/README.md (4 hits)

| hit | term | class | why |
|---|---|---|---|
| `README.md:434` | memparse + device replace + KillSignal | **NOW GROUNDED** (index row) | "device replace runs through the same `btrfs_scrub_dev`" and "`memparse` write" and "`KillSignal=SIGINT` → the foreground `BTRFS_IOC_SCRUB_CANCEL`, a canceled record" — all three were `[inference]` in the entry this row indexes and are now pinned. The trailing "a canceled record" inherits GR3's 5 s caveat. Draft D3 folds the qualifier into the round-45 coverage row instead of editing this row. |
| `README.md:410` | scrub_speed_max | UNTOUCHED | round-42 index row, SC5 print/read side. |
| `README.md:433` | scrub_speed_max | UNTOUCHED | census arm contract: reads the value, never writes it. |
| `README.md:291` | suffix | OUT OF SENSE | pacman hook suffix-ignoring sort. |

### 2.3 PROVINCE.md (3 hits) — all UNTOUCHED

- `PROVINCE.md:242` — round-42 note, "the per-device `scrub_speed_max` limit": read-side summary of btrfs-progs.
- `PROVINCE.md:252` — "cannot be assumed to parse the record [inference: a record written by a root scrub under the
  usual umask is root-only]": a **different** inference (record parse/umask), not one of the three; GR1-GR3 do not
  touch it.
- `PROVINCE.md:269` — promotion note, "a nonzero decimal is a limit and is listed in `detail`; SR8": read side.
- No PROVINCE statement tags the replace caller, `memparse` or `KillSignal` as open, so this sweep requires **no
  PROVINCE append**. (Convention check: rounds 42/43/44 each appended a note at `:239`, `:246`, `:256`; the L1 may
  still want a line for symmetry — I assert no contradiction, not a missing note.)

### 2.4 corpus/knowledge/btrfs-scrub-record-r44.md (19 hits)

| hit | term | class | why |
|---|---|---|---|
| `:21-22` | dev-replace | **NOW GROUNDED** | SR7's `[inference for the replace side … not pinned]`; GR2 pins both call sites. Pointer **already present** at `:159-161` ("the replace caller of `btrfs_scrub_dev` in SR7 … rows GR2, GR1 and GR3" — order matches SR7→GR2, SR8→GR1, SR9→GR3). No new draft. |
| `:63` | memparse + suffix | **NOW GROUNDED** | SR8's `[inference: its definition in `lib/cmdline.c` is not pinned]`; same pointer at `:159-161`. No new draft. |
| `:97`, `:99-101` | KillSignal | **NOW GROUNDED + NARROWED** | ":97 The service runs `btrfs scrub start -B %f` with `KillSignal=SIGINT`" is unit text (S244:9-10) and stands. But ":99-101 … a SIGINT sent to it (the service's stop signal) cancels the running scrub, and a device whose scrub ioctl returns nonzero is recorded with `canceled` set, which `btrfs scrub resume` later takes up" states the record outcome flatly; GR3 leaves that write undecided inside the 5 s window. Draft D2. |
| `:150-151` | `systemctl stop` + `systemd.kill` | **NOW GROUNDED** | "SR9's systemd side … is systemd.kill(5) behaviour and is not pinned here [inference]"; GR3 pins it, pointer at `:159-161`. No new draft. |
| `:141` (with `:140-142`) | resumable | **NARROWED** | "Stopping a running scrub service cancels the scrub and leaves a canceled, resumable record (SR9, SR3)." The cancel is pinned (`scrub.c:417-424` handler, installed at `:1546` in the foreground start); the record write is not. Draft D2. |
| `:160` | memparse + KillSignal | n/a — this **is** the round-45 pointer | It grounds the three marks but adds no qualifier for `:101`/`:141`, which is why D2 is a second block, not an edit. |
| `:11`, `:31`, `:58`, `:60`, `:61`, `:62`, `:74`, `:76`, `:82`, `:84`, `:88`, `:115`, `:138` | mixed | UNTOUCHED | scope sentence, quotes (verified at their cited lines), host reading, and the SR8 triage bullet "0 means none. The limit is root's to set" — all consistent with GR1. |

### 2.5 Other knowledge files

| hit | term | class | why |
|---|---|---|---|
| `btrfs-scrub-record-r42.md:125,131,137,141,151` | scrub_speed_max | UNTOUCHED | SC5 is `btrfs scrub status`/`limit` print behaviour in btrfs-progs 6.6.3; GR1 is the kernel store. |
| `btrfs-scrub-record-r43.md:4` | scrub_speed_max | UNTOUCHED | `extended-by:` chain r42→r43→r44; the r44 entry now carries the round-45 pointer. |
| `btrfs-scrub-grounding-r45.md` (40 hits) | all | n/a — source of grounding | Its own statement at `:62-63` is examined in F-2 (finding against the row, not a doc pointer). |
| `btrfs-repair-r31.json:59` | device replace | UNTOUCHED | "How is a failing or missing btrfs device replaced, and what size must the target be?" — replace mechanics, not the scrub copy path. |
| `aur-risk-plane.md:443`, `package-state-plane.md:335`, `pacman-hook-order-r38.md:21`, `path-reconciliation-r23.md:36` | suffix | OUT OF SENSE | version suffix, `.hook` suffix, selector suffix. |

### 2.6 Adjacent greps (context only, outside the six families)

- `TimeoutStopSec` / `SIGTERM` / `SIGCONT` / `SIGKILL`: the lane's teardown rows (`SKILL.md:1105`,
  `kill-event-deep-r8.md:263`, `kill-oom-boundary-r33.md:17`, `oom-event-plane.md:352`) attribute 5 s to a **unit**
  drop-in (`/etc/systemd/system/user@.service.d/faster-shutdown.conf`); GR3's 5 s is the **sysconf** default
  `DefaultTimeoutStopSec=5s`. Both files exist on the host (`stat -c '%n %s'` → 28 B and 35 B, 2026-10-03) and a unit
  drop-in overrides the default, so the rows are **not contradictory**; no pointer.
- `PROVINCE.md:281` / `README.md:443` ("running, canceling, resuming or limiting a scrub … operator-owned"): untouched.

---

## 3. Findings

**F-1 (high — the defect).** `SKILL.md`, the file a triage reader uses, still tells the reader that two of the three
statements are unpinned: `:4222` "(dev-replace.c:701-703,1265-1268, unpinned)" and `:4229-4230` "SR9's systemd side is
systemd.kill(5) inference; the SR7 replace side is an unpinned caller [inference]". Both are false as of this round
(GR2, GR3) and the round-44 entry they summarize says so at `:159-161`. `SKILL.md` has no round-45 block.
*Sweep note on method:* the six named patterns do **not** reach `:4228-4230` — that block contains neither
`KillSignal` nor `dev-replace`/`device replace` — measured: `git show <REV>:SKILL.md | awk 'NR>=4228&&NR<=4230' |
grep -c -i -E 'memparse|suffix|dev.replace|device replace|KillSignal|systemctl stop|scrub_speed_max'` → **0**. It was
found by reading the enclosing section, and only the added pattern `unpinned|not pinned|systemd\.kill` catches the
second fragment. A QUALITY 10 sweep that stops at the six words reports a clean `SKILL.md` on the two most
load-bearing contradictions.

**F-2 (medium — row accuracy, routed to C2RevGR2 / C2CritGR2, not a doc pointer).** GR2's "So while a replace runs,
the scrub-start ioctl for **any device** of that filesystem returns `EINPROGRESS`" (`btrfs-scrub-grounding-r45.md:62-63`)
overstates the quantifier. In `scrub.c` the replace check at `:3147-3153` is reached only after three earlier refusals:
`:3120-3125` `-ENODEV` (unknown or missing device), `:3127-3135` `-EROFS` (non-writeable device, scrub path), and
`:3138-3144` `-EIO` for `BTRFS_DEV_STATE_REPLACE_TGT` — i.e. the **replace target device** answers `EIO`, not
`EINPROGRESS`. The operational conclusion holds for the source and for ordinary devices; the universal does not.
Tightening (suggestion only, for the row's author/verifier): "the scrub-start ioctl for a device of that filesystem
returns `EINPROGRESS` although no scrub was started, unless an earlier check refuses it first (`ENODEV` for a missing
device, `EROFS` for a non-writeable one, `EIO` for the replace target)".
No outer mention repeats the "any device" quantifier, so F-2 needs no appended pointer text.

**F-3 (medium).** Two sentence pairs assert the stop outcome flatly while GR3 leaves it undecided:
`SKILL.md:4226` "a stopped scrub service cancels the scrub and leaves a resumable record" and
`btrfs-scrub-record-r44.md:140-142` "leaves a canceled, resumable record (SR9, SR3)". GR3 itself
(`grounding-r45.md:102-104`, `:137-139`) says the write might not land before SIGKILL, and the round's own triage bullet
tells the reader to distrust a record without a `canceled` mark. Drafts D1/D2 qualify both.

**F-4 (low — registry).** `corpus/README.md` has append-only coverage notes for rounds 42 (`:406`), 43 (`:416`) and 44
(`:427`, table rows for `tsukuroi-census.sh` and `btrfs-scrub-record-r44.md`), but **no round-45 coverage note**:
`git grep -n 'corpus/knowledge/btrfs-scrub-grounding-r45' <REV> -- corpus/README.md PROVINCE.md SKILL.md` → **0 hits**
(measured), while the settled entry has two: `r44:161` (the append's pointer sentence) and the `used_by` cells of
`corpus/SOURCES.md:246-258`. So the new entry is reachable only from the round-44 entry and the source registry, never
from the index a reader browses. Draft D3.

**F-5 (low).** `SKILL.md:4225`'s "K/M/G suffixes" reads as a closed list; GR1's accepted set is `K M G T P E` (either
case, one letter) over a base-0 radix, which changes how a written value reads back (`010` → 8, `0x10` → 16). Not
false — under-inclusive in the one place the lane's decision table states write semantics. Draft D1.

**F-6 (informational — verified clean).** All 31 `**Quote.**` lines of the three GR rows hold verbatim at their cited
lines in the digest-checked snapshots (`SHA256SUMS` in `.ufo/waves/round-45/frozen/src/`), and the host capture matches
its declared digest: `sha256sum capture.txt` → `f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70`,
equal to `btrfs-scrub-grounding-r45.md:1`. Spot-verified in source, not only by digest: memparse suffix fallthrough and
`check_shl_overflow` (`cmdline.c:160-193`), base fixup (`vsprintf.c:86`, `kstrtox.c:29-33`), the store
(`sysfs.c:2040-2046`), both replace call sites (`dev-replace.c:700-703`, `:1265-1268`), the refusal (`scrub.c:3147-3153`),
the unit (`btrfs-scrub@.service:9-10`), systemd's order (`systemd.kill.xml:84-99,108-115`), and the btrfs-progs handler
(`round-42/frozen/src/scrub.c:416-424`, installed at `:1546` when `-B` suppresses `do_background`).

---

## 4. Drafts — exact appended text (append-only; no old row edited)

### D1 — `SKILL.md`, append after line 4230 (end of "Scrub record — round 44 rows")

```markdown
### Scrub record — round 45 grounding (appended 2026-10-27)

Appended; the rows above and their Limits block stay as written. `corpus/knowledge/btrfs-scrub-grounding-r45.md`
pins the three inferences those rows carried, so read them with this block:

- The first row's tag "(dev-replace.c:701-703,1265-1268, unpinned)" is stale: the replace caller is pinned at S247
  `fs/btrfs/dev-replace.c:700-703` and `:1265-1268`, each call `btrfs_scrub_dev(..., false, true)` (row GR2).
- "K/M/G suffixes" in the `scrub_speed_max` row is not the whole set: GR1 pins one suffix letter from `K M G T P E`
  in either case, a 1024 step each, on a base-0 parse (`010` is 8, `0x10` is 16), with at least one digit before the
  letter; a bare newline writes 0 and clears the limit (S246 `lib/cmdline.c:147-193`, `lib/vsprintf.c:86`,
  `lib/kstrtox.c:29-33`; S243 `sysfs.c:2040-2046`).
- The stop-signal row's outcome is conditional: on this host `systemctl stop` sends SIGINT (`KillSignal=2`), then
  SIGCONT, then SIGKILL once `TimeoutStopUSec=5s` has passed, so a `canceled` record exists only if the start writes it
  inside that window — a record without a `canceled` mark after a stop is possible (row GR3; S248
  `man/systemd.kill.xml:68,91,96,101,108,114`; S249 `capture.txt:2-5`).
- Limits block: the fragments "SR9's systemd side is systemd.kill(5) inference" and "the SR7 replace side is an
  unpinned caller [inference]" are superseded — both sides are pinned now (GR3, GR2).
```

### D2 — `corpus/knowledge/btrfs-scrub-record-r44.md`, append after line 161

Counted-counter safety, checked because `tools/check-scrub-grounding-r45.py:399-400` derives `pointer_ok` from
`sections(text, r'^## (Round-45)\b.*$')` on this file: `sections` uses `out.setdefault(cur, [])` (`:160-173`), so a
second `## Round-45 …` heading **extends** the same bucket instead of replacing it, and the existing `:161` sentence
keeps `pointer_ok == 1`. Editing or renaming the existing "## Round-45 grounding and gate status" heading's body — as
opposed to appending below it — would flip that leg to 0. D2 appends; it does not touch `:153-161`.

```markdown
## Round-45 qualification — the stop outcome (appended 2026-10-27, C2 sweep)

Appended; nothing above is rewritten, and the grounding it points at is `corpus/knowledge/btrfs-scrub-grounding-r45.md`
row GR3. The block above grounds SR9's systemd side; it does not qualify the outcome sentence at `:99-101` or the
triage bullet at `:140-142`. On this host `systemctl stop btrfs-scrub@<instance>.service` is SIGINT
(`KillSignal=2`), then SIGCONT, then SIGKILL once `TimeoutStopUSec=5s` has passed (GR3; S248
`systemd.kill.xml:68,91,96,101,108,114`; S249 `capture.txt:3-5`). The SIGINT handler issues
`BTRFS_IOC_SCRUB_CANCEL` (S237 `scrub.c:416-424`, installed in the foreground start at `:1546`), but whether the start
then writes its `canceled` record before the SIGKILL is not established [inference]. "Leaves a canceled, resumable
record" therefore holds for a start that finishes that write inside the window; otherwise the record stands as it was
last written during the run, and `btrfs scrub resume` sees whatever that record says.
```

### D3 — `corpus/README.md`, append after line 452 (document end)

```markdown
## Round-45 coverage note (appended 2026-10-27)

Append-only; the coverage map, the Frontier bullets and the round-38 to round-44 notes above stay as written.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/btrfs-scrub-grounding-r45.md` | Grounds the three round-44 `[inference]` marks: GR1 the `scrub_speed_max` write parse (`memparse`: one letter of `K M G T P E`, 1024 per step, base-0 radix, bare newline = 0 = no limit); GR2 the device replace's two `btrfs_scrub_dev(..., false, true)` call sites and the `EINPROGRESS` a scrub start gets while a replace runs; GR3 systemd v262's stop sequence for the packaged service (SIGINT from `KillSignal=`, SIGCONT, SIGKILL after `TimeoutStopUSec=5s`), with the `canceled` write inside that window left undecided | S246-S249; `.ufo/waves/round-45/frozen/src/SHA256SUMS` and `hostcap/capture.txt` (sha256 `f5958a83…`); `tools/check-scrub-grounding-r45.py --revision <REV>` |

Frontier: nothing moves. The round-44 promotion (the unprivileged record-directory view is Core) stands; the record's
content, the running state and NVMe SMART/Health stay Frontier, and running, canceling, resuming or limiting a scrub
stay operator-owned (`:443-444`). The three row verdicts bind only from the counted reviewer and critic seats of wave
a2w1 (`SCORECARD.md` "Round 45 — attempt-2 rebinding").
```

### No draft needed (stated, with reason)

`r44:21-22`, `r44:63`, `r44:150-151` — the mention is grounded and the pointer already exists at `r44:159-161`, whose
SR7/SR8/SR9 → GR2/GR1/GR3 mapping is correct. `r44:101`/`:141` are not covered by that block, hence D2.
`README.md:434` is a summary that is now true; D3 carries its qualifier rather than editing the row.
`PROVINCE.md` needs no append (no stale mention; see §2.3).

---

## 5. Retained evidence

In `.ufo/waves/round-45/a2w1/C2ExecSweep/`:

| file | content |
|---|---|
| `grep-memparse.txt`, `grep-suffix.txt`, `grep-dev_replace.txt`, `grep-device_replace.txt`, `grep-KillSignal.txt`, `grep-systemctl_stop.txt`, `grep-scrub_speed_max.txt`, `grep-systemd__kill.txt`, `grep-unpinned_not_pinned_is_inference_inference.txt` | full `git grep -n` output per pattern at `18389f44…`, each with its command line and count footer |
| `hits-compact.txt` | every hit, `file:line: <96-char excerpt>`, grouped by pattern |
| `union.txt` | the de-duplicated `file:line` set (91) used for the counts |
| `skill-4228-4230.txt` | `SKILL.md:4228-4230` verbatim, the block the six patterns miss (F-1) |

Source facts re-read in this seat (all under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/`):

```
round-45/frozen/src/cmdline.c:147,156,159,160-187,189-193
round-45/frozen/src/vsprintf.c:86
round-45/frozen/src/kstrtox.c:26-40
round-45/frozen/src/dev-replace.c:700-703, 1259-1268
round-45/frozen/src/systemd.kill.xml:60-119
round-44/frozen/src/scrub.c:3081, 3118-3155
round-44/frozen/src/sysfs.c:2028, 2031-2049
round-44/frozen/src/btrfs-scrub@.service:1-10
round-42/frozen/src/scrub.c:412-444, 1512-1546
round-45/frozen/hostcap/capture.txt:1-9 (sha256 f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70)
```

Host reads (read-only, unprivileged): `stat -c '%n %s %y' /etc/systemd/system/user@.service.d/faster-shutdown.conf
/etc/systemd/system.conf.d/10-faster-shutdown.conf` → both present (28 B, 35 B). No unit, sysfs, package or mount
state touched; `pacman` not run; nothing written under the fleet root or any PATH.

Tools installed or upgraded: **none** (no need arose).

---

## 6. What I did not do

- I did not run `tools/check-scrub-grounding-r45.py`, `tools/score-census-readers-r45.py`, the census selftest or any
  gate: my item is a read sweep, and the counters are other seats' instruments. Every claim above comes from `git grep`,
  `git show` and direct reads of the frozen snapshots.
- I did not judge the three row verdicts (that is C2RevGR1-3 / C2CritGR1-3); F-2 is flagged **to** those seats and its
  suggested wording is not applied anywhere.
- I did not edit any lane file, including `SKILL.md`, `README.md` and `r44`: all three drafts are proposals for the L1.
- I did not test a `scrub_speed_max` write, start/stop a unit, or read a record's content (host guard).
