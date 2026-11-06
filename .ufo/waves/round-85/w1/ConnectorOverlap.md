# ConnectorOverlap — sibling-overlap scan, hibernation availability (r85 w1)

Lane measured: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` master =
`479d868b2fc8969a19a617cd55ced5c13edd84b6` (candidate commit, current tip).
Read-only throughout. Nothing in the lane was written; the one proposed patch is appended
below and staged under `.ufo/waves/round-85/w1/ConnectorOverlap/`.

## 1. Scan performed

```text
for d in *-shokunin; do grep -rIliE 'lockdown|secure ?boot|nohibernate|hibernat|secretmem|memfd_secret|\bcxl\b' \
  "$d/corpus/knowledge" "$d/PROVINCE.md"; done
```
Exit 0. 21 lanes present; **5 lanes hit** (kaidoku 1 file, mado 1, mori 2, revenger 1, tsukuroi 13).
tsukuroi's own hits: 51 matching lines across 13 files.

## 2. Per-hit classification

| Lane | file:line | Hit (fragment) | Verdict |
|---|---|---|---|
| kaidoku | `corpus/knowledge/2026-10-13-r4-06-1password-asar.md:144` | "Navigation + window-open lockdown" | **Different question** — Electron `webPreferences` hardening. Name collision only. |
| kaidoku | same `:294` | "navigation lockdown, openExternal allowlist" | **Different question** (same row's evidence list). |
| mado | `corpus/knowledge/xdg-portal-routing-r12.md:60` | "`Lockdown` | GTK, second candidate | ... `org.freedesktop.impl.portal.Lockdown`" | **Different question** — XDG desktop-portal interface name; no kernel relation. |
| mori | `corpus/knowledge/uptime-win-r70.md:31` | "this count is NOT working-state time and includes sleep/hibernation time" | Adjacent, **consistent** (mori labels its counter biased; it does not claim power state). |
| mori | `corpus/knowledge/uptime-win-r70.md:40-43` | "No `boot id`, no sleep/hibernation split ... all stay unmeasured here" | **Inbound overlap, aligned**: mori refuses the split. |
| mori | `corpus/knowledge/workstate-win-r71.md:23,29,39` | "INCLUDES time asleep or hibernating"; "reflects only the time that the system is in the working state" | Adjacent, consistent. |
| mori | `corpus/knowledge/workstate-win-r71.md:56,78` | "no sleep/hibernation decomposition, no wake/sleep timestamps"; "diagnosing sleep/hibernation" in the refusal list | Adjacent, consistent. |
| mori | `corpus/knowledge/workstate-win-r71.md:64-66` | "Boundaries: writing power configuration, **diagnosing sleep/hibernation or boot state**, and anything preceding the current boot are **tsukuroi/operator ground**" | **Direct inbound overlap** — recipient-side declaration that this round's surface is tsukuroi's. Strongest single hit in the scan. |
| mori | `PROVINCE.md:13` | "systemd unit, driver/firmware and boot state (→ tsukuroi)" | **Inbound overlap, aligned** at province level. |
| revenger | `corpus/knowledge/round-73-re-resource-atlas.md:278` | "acceptance policy depends on kernel config (**lockdown**, sig_enforce), not on the file" | **Partial overlap** — revenger owns artifact-side signature acceptability; the host-side lockdown selection is tsukuroi's, and it is the *same* `enum lockdown_reason` mechanism as HA5. |
| tsukuroi | `corpus/knowledge/kernel-taint-r27.md:48` (KT3) | "…`return security_locked_down(LOCKDOWN_MODULE_SIGNATURE);` (line 124). **The lockdown state was not captured.**" | Lane-internal; the unknown this round's capture answers **for 2026-11-06 only** (see §4). |
| tsukuroi | `corpus/knowledge/root-dac-decision-r12.md:62` | "`/sys/kernel/security/lsm` = `capability,landlock,lockdown,yama,bpf`" | Lane-internal; **supports HA5** — the lockdown LSM is stacked, so the sysfs selection and the reason ordering are live mechanisms, not a missing-feature stub. |
| tsukuroi | `corpus/knowledge/systemd262-uki-pcr-r65.md:21` (SY2), `driver-firmware-plane.md:105`, `journal-boot-plane.md:300` | "Secure Boot disabled", "`SecureBoot-8be4df61-…` first data byte `0`" | Consistent with `[none]`; Secure Boot state is an **independent fact**, never a substitute for the lockdown-mode read (kernel auto-lock is a separate input). |
| tsukuroi | `corpus/knowledge/journal-boot-plane.md:251-252,402` | "sweep for actual hibernation events: `hibernation entry`/`hibernation exit` = 0 lines in the whole retained journal" | **The episode-attribution half of HA1** already exists here; HA1 covers availability, not episodes. |
| tsukuroi | `corpus/knowledge/windows-power-config-plane-r63.md:34-35` (PW3, PW4) | "available sleep states"; "`powercfg -q … HIBERNATEIDLE`" | **Different machine, same word.** PW3/PW4 are the Windows power plane; a future grep can conflate them with HA rows. No sibling owns Windows. |
| tsukuroi | `corpus/knowledge/adjacency-recheck-r66.md:65,69,79` | boot-credential plane adjacency text | Different question (credentials), consistent. |

`grep -ciE 'lockdown|hibernat' PROVINCE.md` → **0**, and `grep -niE 'resume|hibernat|availability|suspend|power' PROVINCE.md` → **0**. The r84 resume chain and the r85 availability surface are registered as a SKILL arm (`SKILL.md:5917-5919`, `hibernate-resume` and `resume-gate-battery-r85`) but **no PROVINCE.md Core row or section names them**. Last PROVINCE section is `## Round 76` (PROVINCE.md:555); rounds 77-85 appended nothing.

## 3. Consistency of HA5 against the lane's own lockdown mentions

Verified against the pinned snapshots, not quoted from the claim:

- `.ufo/waves/round-85/before/src/include_linux_security.h:127-158` — `LOCKDOWN_NONE, LOCKDOWN_MODULE_SIGNATURE(1), LOCKDOWN_DEV_MEM, LOCKDOWN_EFI_TEST, LOCKDOWN_KEXEC, LOCKDOWN_HIBERNATION(5), … LOCKDOWN_INTEGRITY_MAX`. `LOCKDOWN_HIBERNATION` precedes `LOCKDOWN_INTEGRITY_MAX`. HA5's ordering holds.
- `.ufo/waves/round-85/before/src/security_lockdown_lockdown.c:59-71` — `if (kernel_locked_down >= what) { … return -EPERM; }`. `integrity` mode therefore blocks `LOCKDOWN_HIBERNATION`; HA5's "`integrity` already blocks" holds.
- `.ufo/waves/round-85/before/src/kernel_power_hibernate.c:109-113` — the four-conjunct `hibernation_available()` exactly as HA1 states.

No contradiction with `kernel-taint-r27.md`, `root-dac-decision-r12.md`, `systemd262-uki-pcr-r65.md`, `driver-firmware-plane.md` or `journal-boot-plane.md`. Two precision caveats:

1. **KT3 is not retroactively resolved.** HA7's `[none]` is a 2026-11-06 reading; KT3's unknown is dated to the round-27 capture. Landing HA7 must not be cited as filling KT3's cell at r27 — only as "the same measurement, later".
2. **`r84`'s recheck trigger set is incomplete once availability is in the chain.** `corpus/knowledge/hibernate-resume-plane-r84.md:3` says "recheck … cadence 30d and on any kernel, btrfs-progs, mkinitcpio or swap-file change". A lockdown-mode change (`lockdown=integrity\|confidentiality` on the cmdline, or Secure Boot enabling the auto-lock) reverses availability with **none** of those four changing. Reported, not patched (lane file).

## 4. Host facts re-measured read-only (2026-11-06, this seat)

```text
$ cat /sys/kernel/security/lockdown
[none] integrity confidentiality          rc=0
$ cat /sys/kernel/security/lsm
capability,landlock,lockdown,yama,bpf
$ tr ' ' '\n' < /proc/cmdline | grep -cE '^(nohibernate|noresume|hibernate=)'
0
$ zgrep -E '^CONFIG_(SECRETMEM|HIBERNATION)=' /proc/config.gz
CONFIG_HIBERNATION=y
CONFIG_SECRETMEM=y
$ zgrep -iE 'cxl' /proc/config.gz | head -2
CONFIG_ACPI_APEI_EINJ_CXL=y
CONFIG_CXL_BUS=m
$ ls /dev/cxl /sys/bus/cxl
ls: cannot access '/dev/cxl': No such file or directory
ls: cannot access '/sys/bus/cxl': No such file or directory
$ python3 tools/check-hibernate-resume.py --live
{"findings": [], "verdict": "HEALTHY"}      rc=0
```

Two points HA8 should absorb and no current row states:

- **CXL is modular, not absent**: `CONFIG_CXL_BUS=m`, `CONFIG_CXL_MEM=m`. "This host has no CXL" is therefore *not* derivable from config; it is measured as "no cxl bus or device registered" (`/sys/bus/cxl`, `/dev/cxl` absent). An inference from `CONFIG_` would be wrong in the opposite direction on a host that merely has not modprobed it.
- **`secretmem` is enabled (`CONFIG_SECRETMEM=y`)**, so `secretmem_active()` is a live conjunct, not an inert one — and it has **no sysfs surface**. Of the four conjuncts, this is the only one the gate cannot read.

## 5. Second-order effect: what the gate's HEALTHY does and does not say

`tools/check-hibernate-resume.py:10-20` models three availability rules (HR-HIBERNATE-DISABLED, HR-LOCKDOWN-BLOCKS, HR-NORESUME-ARG); `availability()` at `:99-120` reads only the cmdline tokens and the lockdown string. `hibernation_available()` has four conjuncts, and the gate reads neither `secretmem_active()` nor `cxl_mem_active()` — one of which (secretmem) is compiled in here.

A witness outside the gate exists and is named by the landed C1 entry (`corpus/knowledge/hibernation-availability-r85.md:33,58`):
`hibernate.c:1168-1169` `if (!hibernation_available()) return sysfs_emit(buf, "[disabled]\n");` is the
`disk_show` path, so `/sys/power/disk` is the kernel's own verdict on the whole conjunction.

```text
$ cat /sys/power/disk
[platform] shutdown reboot suspend test_resume
```

Not `[disabled]` ⇒ **the kernel itself reports hibernation available on this host**, secretmem and CXL
included, so the gate's `HEALTHY` is corroborated for this capture rather than merely asserted. The
residual risk is structural, not present: a live or future secretmem mapping would leave the gate at
`HEALTHY` while the witness flips to `[disabled]` — the gate is blind to one conjunct, not wrong now.

This stays a **scope** statement, not a defect claim, and it must not be repaired by adding a finding:
C2's predicate compares the exact `(rc, verdict, sorted findings)` tuple per case, so any new finding
or verdict token mid-round would break the declared 20/20 target. The carriers are the entry's HA8 text
and the gate's docstring scope line.

## 6. Proposed moves (bounded; L1 decides)

Move: **append one PROVINCE section registering the availability surface and three adjacency rows, and leave the frozen ADJ-01..07 table untouched.** Full patch text: `.ufo/waves/round-85/w1/ConnectorOverlap/proposed-province-r85.md`.

Proof the shape is inert, run in a `git clone --shared` of the lane at
`/fast/scratch/hyaku/tsukuroi-r85/ConnectorOverlap/lane` (commit `f2797a3b20ceae…` = base,
`0478fdb624ac…` = base + appended ADJ-08 row):

```text
check-adjacency-table-r50.py --revision <rev> --lane <clone>
  base: adj_rows 7, linked_rows 7, bare_ranges 0, anchors_ok 7
  appended: adj_rows 7, linked_rows 7, bare_ranges 0, anchors_ok 7
check-adjacency-table-r51.py --revision <rev> --lane <clone> --control
  base:     adj_exact 1, adj_rows 7, bare_all 0, anchor_rows_exact 1
  appended: adj_exact 1, adj_rows 7, bare_all 0, anchor_rows_exact 1
check-adjacency-anchors.py --revision <rev>
  both revisions: CANNOT_EVALUATE, 1 finding (clone lacks sibling repos; identical pre/post)
```

`ADJ_ROW = re.compile(r'^\|\s*(ADJ-0\d)\s*\|')` (`check-adjacency-table-r50.py:69`) is applied
**within** the `## Adjacent — finding-to-owner handoffs` section, so an appended section's
`ADJ-08` is not counted and `adj_exact`/`adj_rows == 7` survive. Adding rows *inside* the
ADJ-01..07 table would break `check-adjacency-table-r49/r50/r51` (`adj_rows == 7` is the
predicate) — that is the trap this move avoids.

### Row 1 (recommended, strongest evidence) — ADJ-08, sleep/hibernation episode attribution

| Field | Value |
|---|---|
| Trigger | A working-state, idle or uptime figure must be split by sleep/hibernation, or an episode must be confirmed/denied |
| Tsukuroi retains | HA1-HA8 availability facts, `hibernate-resume` gate findings, and the journal sweep `corpus/knowledge/journal-boot-plane.md:251-252,402` |
| Recipient | mori |
| Evidence | mori `corpus/knowledge/workstate-win-r71.md:64-66` @ `7765969c79e6` — "diagnosing sleep/hibernation or boot state … are tsukuroi/operator ground"; `uptime-win-r70.md:40-43` — "no sleep/hibernation split … stay unmeasured here"; `PROVINCE.md:13` |
| Ownership source | mori's own declaration (recipient-side), not a tsukuroi grant — re-read live; pins drift |

### Row 2 — ADJ-09, one lockdown selection decides two refusals

| Field | Value |
|---|---|
| Trigger | A signed-module load refusal (nvidia DKMS) or a hibernation refusal is attributed to kernel lockdown |
| Tsukuroi retains | The live `/sys/kernel/security/lockdown` selection (`[none]`), the reason ordering (`LOCKDOWN_MODULE_SIGNATURE`=1, `LOCKDOWN_HIBERNATION`=5 < `LOCKDOWN_INTEGRITY_MAX`) |
| Recipient | revenger (ADJ-06 route) for artifact-side signature acceptability |
| Evidence | revenger `corpus/knowledge/round-73-re-resource-atlas.md:278` @ `654d09298960` — "acceptance policy depends on kernel config (lockdown, sig_enforce), not on the file"; tsukuroi `kernel-taint-r27.md:48` (KT3 unknown); this round's `[none]` + `--live` HEALTHY rc 0 |
| Ownership source | `OUT-008`/`OUT-009` anchors (unresolved kaidoku/revenger arbitration still governs) |

### Row 3 (method, not repair) — ADJ-10, a gate verdict that omits its own entry's witness

| Field | Value |
|---|---|
| Trigger | A gate returns HEALTHY over a rule set narrower than the predicate it names, while the lane's own knowledge entry names a host witness the gate does not read (`/sys/power/disk` `[disabled]` for the two unread conjuncts) |
| Tsukuroi retains | The gate, its rule set, and the measured host facts (`CONFIG_SECRETMEM=y`; no `/sys/bus/cxl`; witness not `[disabled]`) |
| Recipient | tameshi (ADJ-07 route) — ask for method advice only |
| Evidence | `tools/check-hibernate-resume.py:10-20` and `:99-120` (three rules) vs `hibernate.c:109-113` (four conjuncts) and `:1168-1169` (the witness); `corpus/knowledge/hibernation-availability-r85.md:33,58`; `--live` tuple above |
| Ownership source | `OUT-010` |

Explicitly **no behavior change** is proposed under ADJ-10: a new finding/verdict token would
break C2's exact-tuple predicate. The question is "how should a gate scope a verdict over
terms it cannot read", which is tameshi's ground, not a repair of this gate.

## 7. Defect found in the adjacency register (pre-existing, not this round's)

`python3 tools/check-adjacency-anchors.py --revision 479d868b2fc8969a19a617cd55ced5c13edd84b6`
→ `status: FAIL`, one finding:

```json
{"detail": "classification DRIFTED is inconsistent: found_line is not an occurrence of evidence_quote (or empty quote requires line 0)",
 "id": "INBOUND-CLASSIFICATION-WRONG", "site": "corpus/knowledge/adjacency-anchors-r19.json:inbound[108]"}
```

Record `IN-109` (tameshi `corpus/knowledge/service-optin-protocol.md:153` → `tools/tsukuroi-census.sh:915-970`)
pins `found_line: 2822`; the quote now sits at `tools/tsukuroi-census.sh:3214`:

```text
$ grep -n "kernel ring class counts are evidence" tools/tsukuroi-census.sh
3214:  check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED \
```

Proposed one-field patch (append a note, do not rewrite history): set
`inbound[108].found_line` to `3214` and append to its `note`: "Round 85 (ConnectorOverlap):
census growth moved the case 2822 → 3214; quote re-located at 479d868." Any PROVINCE change
this round lands on this red base, so the L1 should either apply it or state the base is red.

## 8. Axes

- **adjacency**: improved — the surface gets a PROVINCE registration plus three rows with live, pinned sibling evidence; no existing row changed; checkers proven inert (§6).
- **operability, depth, freshness, contract**: unchanged. No gate behavior, battery input, predicate, or host state was touched; the only executable runs were read-only.

## 9. Risks

1. Rows 1-3 cite sibling knowledge files at today's tips (`7765969c…`, `654d0929…`, `61990f3d…`); unlike the OUT anchors they have **no** blob-sha pins, so they will read DRIFTED on the next sibling commit. The section must say so, or it repeats IN-109's failure mode.
2. Row 2 must not be read as resolving KT3 retroactively (§3 caveat 1).
3. Row 3 must not be routed as a defect; a "fix" would break C2's target.
4. Appending to PROVINCE.md is safe only as a **new section**; editing the ADJ-01..07 table breaks three frozen counters (§6).
5. `.ufo/waves/round-85/before/src/` holds four snapped files, not the tree: `cxl_mem_active()`'s own definition is not in the pin, so "modular CXL" rests on `/proc/config.gz` + sysfs absence, not on a pinned source line.

## Verification

```text
python3 tools/check-adjacency-table-r51.py --revision <NEW-TIP>   # expect adj_exact 1, adj_rows 7, bare_all 0
python3 tools/check-adjacency-table-r50.py --revision <NEW-TIP>   # expect adj_rows 7, linked_rows 7, bare_ranges 0, anchors_ok 7
python3 tools/check-adjacency-anchors.py --revision <NEW-TIP>     # expect no *new* finding vs the one below
python3 tools/resume-gate-battery-r85.py --gate tools/check-hibernate-resume.py   # unchanged: 20/20 in 3 runs
```

Scratch `/fast/scratch/hyaku/tsukuroi-r85/ConnectorOverlap/` removed before exit.
