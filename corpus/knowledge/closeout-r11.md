# Closeout r11 — the arc, the standing cadence, and the elevation-gated register (S11-1)

source: synthesis of landed artifacts — every pin re-hashed in this seat's window
(2026-10-14 21:30:44Z – 21:37Z, host `plazir27`, user `vgpnk`, non-root) — plus this seat's
own executed read-only receipts: `bash tools/tsukuroi-census.sh --selftest` (×2, rc=0),
`bash tools/tsukuroi-census.sh` (×2, rc=1), `md5sum`/`sha256sum`/`wc`/`stat`, `git show`
`git log`/`git status`, `dkms status`, `snapper list-configs`, `ls -ld /.snapshots`,
`ls /boot` (rc=2 — privilege gate), `stat -c '%a %U:%G' /etc/crypttab` (shape only),
`dmesg` (denied — shape). Scratch `/tmp/w11-s11-1-tsukuroi/` (`hash-before.txt`,
`selftest.{out,err}`, `live.{out,err}`; ephemeral). No external site; no host mutation;
no `-Sy`/`-Syu`; no transaction; no service action; no root; secrets/session material
shape-only. **Write scope: this file only.**
verified-at: 2026-10-14 21:30:44Z – 21:37Z. **Every count/verdict is a capture; re-run,
never quote.**
recheck: §5.
Notation: `[obs]` measured · `[inf]` inference · `[unk]` unsettled, with the probe that
would settle it. Pins state their convention (`wc -l`; the census and `SKILL.md` carry an
**unterminated final line**, so a Read counts +1). Errata are append-only: a superseded
claim keeps its original text; the correction is an appended block.

## 0. What this note is, and the state it froze

**0.1 Scope.** The terminal closeout of the lane's training arc for the reader who remains
when the lanes stop: **the arc** (§1 — the plane count, the census's self-measurement, the
triage discipline), **the standing cadence** (§2 — when the operator should re-run), and
**the named debts** (§3 — the elevation-gated register first-class, the other classes named
so nothing hides behind it). It makes **no new host claim beyond its own executed
receipts** (each marked with this window). Sibling round-11 artifacts (the runbook and the
record set per `plans/round-11.plan.md`) are landing around and after this window; they are
**not cited as landed here** — the realized names govern, and this note claims nothing
about them.

**0.2 State at freeze [obs].** HEAD `af8adf1a2f5ea0be458ebc2144ca40ba4469e08`
("probation round 10 (training r9)"); `git status --short` = 0 lines at 21:30:44Z and again
after the last probe; the working gate equals the committed blob (`git show
HEAD:tools/tsukuroi-census.sh | md5sum` = the working-tree md5 below);
`/var/lib/pacman/db.lck` absent after every probe.

**0.3 The census at this freeze [obs].** md5 `945c76fc6cc548e47b91c23a9637df75` · sha256
`1045244387ffcd5d3db481dd0d3d30e34097abc24744d954e791b81d28b20c11` · 2402 `wc -l`
(Read 2403) · 126 075 B · mtime 2026-10-14 18:03:12 -03 · final line `main "$@"`,
unterminated. `VERSION='census-v2'` (`:323`) — **identity is by hash, not version string**;
`--identity` is **not landed** (D12: `usage()` `:439-452` lists `--selftest`, `--sample N`,
`--help` only; unknown argument → usage, exit 2). Six emitters `:2377-2382`, rollup `:2392`.
This seat's executed runs: selftest rc=0 verbatim
`TSUKUROI_CENSUS_SELFTEST: PASS (80 cases, 80 passed, 0 failed)`, wall 12.041 s; live rc=1
(two runs), header stamp of the capture below `2026-10-14T21:31:11Z`, wall 4.590 s (second,
timed run — concurrent 32 lanes [inf; r10 measured 2.770 s in a quieter window]);

```
PLANE packages: DEGRADED (… drift=2[1password-beta,1password-cli] … foreign=16(known=16 new=0 drift=0 gone=0) base=r6(16); pins=none; holds=pacman glibc; db.lck=absent)
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=1 timers_scanned=1 timer_fail=0 timer_unknown=0)
PLANE drivers: DEGRADED (… kerr=146 (oom=1 io=70 gpu=0 other=75) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 …)
PLANE journal: DEGRADED (boots=13 current=yes … err=1034 (coredump=752 kernel=146 other=136); failedhist=8[…])
PLANE update-safety: DEGRADED (status=UNKNOWN-UPSTREAM; … join=equal=1171 behind=0 ahead=1 … chan=dbs=4 fetch=3d stamp=36d; offline.db=present(stamp=85d birth=11d) … trap=-Suu:1[omarchy/1password-beta 8.12.42_32.BETA-1] …)
PLANE oom: HEALTHY (window=boots=13 2026-10-03..2026-10-14; … known=2[A, B] new=0 missing=0 …)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=HEALTHY)
```

(lines elided with `…` for width; the full capture is the scratch `live.out`; elision never
crosses a field this note cites). Plane-set consistency: **6 emitters == 6 rollup keys**
(D11, verified in this seat's runs).

**0.4 Premise delta, recorded not smoothed.** The dispatch frames the arc as "3→5 planes".
Measured, the **committed** gate went 3 → 4 → 6; the arc's "5" was real but transient and
**uncommitted**: S9-1's five-plane revision (`0f72f4cf…`, 2011 `wc -l`) lived in the
working tree for ~12 minutes before S9-2's oom plane made the gate six-plane
(`SKILL.md:1320-1323` and the addendum `:1347-1356`; `calibration-synthesis.md:1419`). So:
**3 (v1) → 4 (v2) → 5 (uncommitted, ~12 min) → 6 (committed r9b onward)** — the design arc
passed through five; no committed revision ever emitted five. The round-10 receipt set the
precedent for this move with its own "5 PLANE lines" premise against the realized six
(`census-closeout-receipt-r10.md` §0).

## 1. The arc

### 1.1 The instrument — prose to gate, three planes to six

Each row a landed pin; md5 prefixes (8 hex) re-derived by this seat from committed bytes
(`git show <commit>:tools/tsukuroi-census.sh | md5sum`), `wc -l` by the same route; plane
sets by the emitter labels in the same show; case counts are the landed declarations
(restated in `LOG.md`/`SCORECARD.md`/`SKILL.md`), the last one executed by this seat.

| revision | commit | md5 (8) | `wc -l` | planes | cases | landed as |
|---|---|---|---|---|---|---|
| census-v1 (r2) | `5f90645` | `7a3d3b94` | 743 | **3** (packages, systemd, drivers) | 17 | first executable gate; exit map 0/1/2 |
| census-v2 (r3) | `9bcd162` | `41953ee9` | 976 | **4** (+journal) | 26 | journal/boot plane joins the gate |
| hardened (r5) | `da95290` | `e9327046` | 1032 | 4 | 35 | 9 cases close the mutation-sweep defects |
| r7 arms | `aa136d6` | `e2c4558a` | 1472 | 4 | 49 | AUR watch + memory pressure **arms**, not planes |
| five-plane (r9, uncommitted) | — | `0f72f4cf` prefix (cited, addendum `:1349`) | 2011 | **5** (+update-safety) | — | working-tree only, superseded in ~12 min |
| r9b (r9 commit) | `fac745b` | `e32aac98` | 2349 | **6** (+oom) | 74 | the first committed revision carrying either carries both |
| r10 (HEAD) | `af8adf1` | `945c76fc` | 2402 | 6 | **80** | six `(S10-2)` cases close the sweep survivors |

Notes: the version string stayed `census-v2` across all revisions — **revision identity is
the hash**. The r10 case count reconciles in source as 77 `check '` declarations + 3
`check_cli` (3 + 3 of those = the six `(S10-2)` cases landed on the r9b base; executed
verbatim in `SKILL.md:1486-1491`). Ten round commits after the mint carry the arc (measured
`git log --oneline`: `55b2186` … `af8adf1`).

### 1.2 The corpus — three notes to twenty-three

- r1: three plane notes (`package-state-plane.md`, `systemd-user-plane.md`,
  `driver-firmware-plane.md`) + a `SKILL.md` distill (22 → 232 `wc -l`); the "5-plane"
  verdict table was **design** at r1, not gate output.
- r3: the e2e board over **five surfaces** (packages, systemd, drivers, journal,
  update-safety) — 20 finding→action pairs, 15-row unknowns register
  (`host-health-report-r3.md`).
- r10 end: **23** notes under `corpus/knowledge/` (`ls | wc -l` = 23 at this window; +this
  one = 24 when it lands); `SKILL.md` at 1569 `wc -l` / md5 `19d989b3…` (Read 1570) after
  11 revisions (22 → 232 → 444 → 543 → 543 → 706 → 837 → 983 → 1169 → 1374 → the r10
  append; the line arc is `SKILL.md` §3's own; `calibration-synthesis.md` §8 pins the
  1374 revision `d276ecea…` as the pre-append state).
- The classes the corpus now covers beyond the original five: the OOM/kill-event class
  (`oom-event-plane.md`, `kill-event-deep-r8.md`, the two memory-arm notes), the AUR risk
  class (`aur-risk-plane.md` + two verifier notes + the first drift receipt), boot-plane
  depth and timer semantics (`boot-plane.md`, `timer-drift-plane.md`), and the calibration
  ledger (`calibration-synthesis.md`).

### 1.3 The census self-measured

The distinguishing property of this lane's instrument: **it measures itself before it
measures the host**, and its failures are kept as receipts. Four mechanisms, each landed:

1. **`--selftest` executes the gate against hermetic fixtures** — zero-mutation asserted
   (fixture byte-unchanged), case count declared == executed (D3). Arc: 17 → 26 → 35 → 49 →
   74 → **80**; this seat executed the 80 case line above (rc=0, verbatim).
2. **Own-source mutation sweeps, two revisions, never conflated** (`SKILL.md:558-628`):
   r5 — the cross-author tameshi sweep on the own gate (23 defects, 13 killed by the own
   suite; its replay closed only 1/4 survivors — a hardening gap recorded, not smoothed);
   r10 — the gate's **own** sweep, target the r9b sha256 pin: 10 defects, 6/10 killed, the
   four survivors (H1 default `-Qkk` sample cap, H2 CLI exit map, H3 rollup field order,
   H4 update-safety `-Sup` fail-closed) covered by the six `(S10-2)` cases. The r10 sweep
   figures are the revision comment's **attestation**; its independent replay is owed
   (§3.2, D13).
3. **Counts move together** (D3) — the executed 80 equals the live restatements at
   `SKILL.md:1529`; the 17/26/35/49/63/74 lines stand as history.
4. **Zero mutation** (D8) — `git status` byte-identical before/after every probe;
   `db.lck` absent; live mode writes nothing (this seat's receipts above).

Behind it all: the **calibration ledger** (r10 S10-1, `calibration-synthesis.md`,
md5 `ed8dec89…`, 463 `wc -l`): the five-step correction loop — claim → re-measure → append
the divergence append-only → supersede the restatement → distil a rule or name the gap with
an owner — and the round table of mismeasures it caught (the 18/19 `-Qkk` split, the
unit-file count 136→133, the "0 unit failures" belief refuted in r4, the mtime→birth
correction). **A lane that cannot be wrong in a recorded way cannot be trusted when it is
right** — that is the arc's method, not a slogan: every row cites the artifact that caught
it.

### 1.4 The triage discipline (the reader's rules)

The operator-facing subset; the full executable set is D1–D13 at `SKILL.md:1426-1471`.

- **Vocabulary and rollup**: each plane emits `HEALTHY` | `DEGRADED` | `BLOCKED`; the
  rollup takes the worst plane; exit map 0/1/2 (usage errors 2). A `BLOCKED` arm is a
  **failed-closed reading, never a pass** (D1) — an unreadable probe is a finding.
- **Empty-proof** (D2): an empty result passes only with the scan itself measured.
- **Captures, not quotes** (D4): every count/verdict carries its time. The coredump class
  is the standing proof — one boot lineage reads 198 (r1) → 224 (r3) → 467 (r9 plan
  capture) → 523 (r10 receipt) → **752** (this window). None of these is a fact about
  today.
- **Traps printed** (D10): each plane names its own (line-vs-entry, birth-vs-mtime, `-Qu`
  shadowing, `%s` is not a size, pipeline rc).
- **Post-verdict contract** (`SKILL.md:508`): every `DEGRADED` finding carries its measured
  evidence and an **exact operator unblock** — the r3 report's 20 pairs and r4's P/D/J/U
  tables are the model (`degraded-triage-r4.md`).
- **Detection, never remediation** (`PROVINCE.md:16-17`): no install/upgrade/remove/
  restart, no elevation; boundaries are reported to owning lanes, never absorbed.
- **D13 — attested ≠ verified**: an author's suite is author evidence; a verifier named in
  a log row without a landed note is an attestation, not a verification
  (`calibration-synthesis.md:356-368`).

## 2. The standing cadence — when the operator should re-run

**The measured fact first**: no landed artifact prescribes a calendar interval for running
the gate [obs — the corpus's only "cadence" hits are the host's own systemd timer
definitions and per-note recheck sets]. The standing rule is the one the discipline already
proves: **capture-not-quote** (D4) — a stored verdict is a capture with a timestamp, never
a standing fact about the host. The gate is cheap and read-only (this window: live 4.590 s,
selftest 12.041 s; r10: 2.770 s / 12.121 s), so the cadence that follows is
**event-anchored, at decision points**, not scheduled:

1. **Before any package-wave decision.** Re-run the gate; then `-Qu`/`-Sup` — the
   update-safety table's own instruction: "re-run `-Qu`/`-Sup` **before** the upgrade"
   (`update-safety-v3.md:217`); the "as-of date" caveat stands (`:206`); the 36 d sync
   stamp in this window's line is a capture, not a property of the repos.
2. **After any elevation-gated remediation** (§3.1). The action pairs carry their own
   re-check: D2 "then re-check `dkms status`"; U3 verify `dkms status` for the new kernel
   before reboot; U6 root pre-verify before a wave; J4/U1 re-audit; U2 then re-run
   `-Qu`/`-Sup`; P2 root re-run "expected to clear". The r4 pending line is the model:
   the blocked rows are "operator-executable today … none was executed by this lane"
   (`degraded-triage-r4.md:586-587`).
3. **At any new boot, or after any event class fires.** The journal and oom planes report
   **windows**: `boots=13 current=yes`; the oom arm's sweep window
   `2026-10-03..2026-10-14` with `new=0`. A boot edge or a `new=`/coredump jump means the
   previous capture no longer describes the current window — re-count with the census
   command (J1's own wording, r3).
4. **On any gate revision change.** Re-hash first: a mismatch against the pinned identity
   means the instrument moved — **stop and re-measure** (`SKILL.md` §4; the r9 addendum
   `:1372-1375`). Then re-run `--selftest` (declared == executed, D3) and re-quote the live
   lines.
5. **At receipt time, for the watch class.** The watch model is a re-run against a fixed
   baseline; r9's re-run produced the first receipt — an **explicit no-drift**
   (`aur-drift-receipt-r9.md`; a real event would surface as `drift=[name(old->new)]` in
   the next re-run, `:169`). Whether a future re-run lands a real drift event is `[unk]`
   by design — the watch names it when it happens.

Re-run rules, restated: unpiped rcs only; an unreadable probe is `BLOCKED`; `git status`
before/after (zero mutation); `db.lck` absent after; every value a capture with a time.
**Not a cadence**: nothing here sets daily/weekly/monthly; if the operator wants a timed
schedule, the receipt model (each run leaves a timestamped receipt against the previous
baseline) is the landed pattern to copy — that choice is the operator's `[inf]`, no
artifact prescribes it.

## 3. The named debts

**3.1 The elevation-gated register** — findings whose next step requires an elevation the
lane never performs (detection-only, `PROVINCE.md:16-17`). Each row: finding → measured
evidence (this window where re-measured; otherwise the landing artifact) → elevation
action → owner artifact. **None was executed by this lane.**

| # | finding | measured evidence | elevation action | owner artifact |
|---|---|---|---|---|
| 1 | full-sweep `-Qkk` root delta | r3: 36 non-root artifact lines (32 failed-calc + 4 permission-denied); this window's bounded sample reports `nonroot_artifacts=0` — the delta is a full-sweep property | `sudo pacman -Qkk` (root view) | r3 P2/P3; `package-state-plane.md:222-223,291-292` |
| 2 | stale DKMS registration | **re-measured**: `nvidia/610.57.04, 7.1.4-arch1-1 … installed (Original modules exist) (Built modules are missing in the kernel modules folder)` beside the current 7.2.3-arch1-3 | `sudo dkms remove nvidia/610.57.04 -k 7.1.4-arch1-1` | r3 D2; `driver-firmware-plane.md` |
| 3 | `/boot` privilege gate | **re-measured**: `ls /boot` rc=2 non-root | `sudo ls /boot` + `sudo bootctl status` **before** a kernel/firmware/limine wave | r3 U6 |
| 4 | crypttab / LUKS dwell `[unk]` | **re-measured shape**: `/etc/crypttab` mode 600 root:root (never read) | operator probe of the LUKS/crypttab path; mechanism stays `[unknown]` | r3 J3; `journal-boot-plane.md`; `boot-plane.md:213` |
| 5 | stale mirror / upstream delta `[unk]` | this window's gate line: `stamp=36d`, `status=UNKNOWN-UPSTREAM` | `sudo pacman -Sy` then re-run `-Qu`/`-Sup` | r3 U2; `degraded-triage-r4.md:524` |
| 6 | alpm temp dirs (3) | r3 P5 | root inspect of the temp dirs | r3 P5 |
| 7 | `walker-restart.hook` root-exec surface | user-owned script run as root (r3) | kagi / operator review — reported, never absorbed | r3 U7 |
| 8 | no rollback net | **re-measured**: `snapper list-configs` header-only rc=0; `/.snapshots` absent | configure snapper + `SNAPPER_CONFIG_NAME` (or accept snapshot-less); re-audit | r3 J4/U1 |
| 9 | 1Password pair sample drift (census `DEGRADED`) | this window: `drift=2[1password-beta,1password-cli]`, `sample=8` | root-verify the setgid group surfaces; accept as vendor convention **or** reinstall both | r3 P1 |

Also in this class, by policy rather than by finding: **every state-changing verb** —
install, upgrade, remove, restart, `-Sy`/`-Syu` — is operator-only; the `-Syu` decision
table is recommendation-only (`update-safety-v3.md` §5), and the downgrade trap stands as a
rule (`omarchy/1password-beta … BETA-1`; never `-Suu`, never `-Syyu`; r3 U5 / this window's
`trap=-Suu:1[…]` row).

**3.2 Not elevation-gated — named so nothing hides behind the register.**

- **Verification debts (D13)**: the two planes r9 added still need non-author
  verification; the calibration ledger's rows; the six `(S10-2)` cases' covering claims and
  the r10 sweep's independent replay; tameshi's B7/B8/B9 survivors (no landed closure);
  the **post-append no-oral-context re-test** owed since r3 (`LOG.md:153-154`;
  `SHONEN.md` box 3 keeps the pre-fix tally).
- **Record debts**: `corpus/lessons/` = **0 files** at this window (the discernment loop's
  contracted home; no retro-fabrication — a Gate for closed rounds would invent decisions);
  `corpus/README.md` unchanged since r3 (md5 `98bd0066…`, 20 `wc -l`; rows stop at r3, no
  `## Frontier` heading, and its row `:13` still repeats the r4-refuted "0 unit failures in
  13 retained boots"); `SCORECARD.md` rows 16, 21 and 22 each mishandle an unescaped
  parenthesis — row 16 truncates at `boot plane (299 L`, row 21 loses the closing paren
  after `AUD-X7 gap closed`, row 22 truncates at `the calibration synthesis (measured-vs-believed`
  (all measured at this window) — repair preserves the original text verbatim; `LOG.md:172`'s
  "5-plane" wording and its AUD-X7 credit (closed in r8 by VER-S8, not by r9's
  update-safety arms) stay visible, corrected only by appended precision.
- **Host unknowns with owners, not elevation-gated**: the coredump storm (journal
  workstream + the godot/node/LOVE app lanes; 752 this window, dir state `[unk]`-moving);
  V8 heap-OOM class; the coredump dir count-up/size-down `[unk]`; the OOM-counter
  lifecycle Q2; r6 H1–H3; the E4–E8 errata on `oom-event-plane.md` (that note's owner
  applies them); the "20-min cap" item (integrator); the 18/19 sweep-summary split;
  `offline.db` coverage; the round-2 wave-1 errata merge; the `1password-beta` provenance
  formal decision; D12 (one-command identity) not landed — the re-derivation is the
  classic three commands (§5).

**3.3 What closes a debt.** The pattern the arc earned: a debt closes by **landing an
artifact at its owner** — a root run leaves a receipt, a verification leaves a note
(VER-S7/VER-S8 shape), a re-run leaves a drift receipt — never by being re-quoted. The r4
triage's blocked rows "operator-executable today; none was executed by this lane" and the
r9 drift receipt's explicit no-drift are the two halves of the model.

## 4. Unknowns and bounds

- `[unk]` the round-11 sibling artifacts (runbook, province/coverage rows, lesson, record
  set) — landing around/after this window; their realized names govern; this note cites
  none as landed. The probe: re-read the tree.
- `[unk]` the five-plane intermediate's exact lifetime — "~12 min" is the round-9
  addendum's own wording (`SKILL.md:1353`); the revision never committed, so it cannot be
  re-derived from history.
- `[unk]` this window's live wall (4.590 s vs r10's 2.770 s) — concurrent 32 lanes is
  `[inf]`; the settling probe is a timing in a quiet window.
- `[unk]` the coredump dir's shrink-while-count-grows mechanism (r10 observed 443 files /
  4.0 G against 484 / 3.5 G earlier; no retention reading was taken here).
- `[unk]` whether the training ladder ends at round 11 fleet-wide — the round-11 plan's
  own frame note leaves it to the dispatcher; this note claims nothing about siblings.
- Bounds: this note writes nothing else, opens no new ground, re-opens no deferred class,
  and is not a remediation trigger. Nothing in it was re-measured from memory.

## 5. Pins, receipts, recheck

**Pins** (re-hashed by this seat 2026-10-14 ~21:30–21:33Z; `wc -l`; `…` = elided hash
middle — full values in the scratch `pins` capture and the sibling artifacts). These are
captures of this window: **re-hash before quoting** (D5/D6) — round-11 siblings may land
after this freeze.

| artifact | md5 | lines |
|---|---|---|
| `tools/tsukuroi-census.sh` (HEAD, sha256 §0.3) | `945c76fc6cc548e47b91c23a9637df75` | 2402 · 126 075 B |
| `SKILL.md` (Read 1570) | `19d989b32fb0b4040254a2503d503854` | 1569 |
| `LOG.md` | `0c9b2f02375cca07998a6ff46a8cec6f` | 173 |
| `SCORECARD.md` | `52218ee5fcb240fa0bd9f64602ff169d` | 22 |
| `SHONEN.md` / `PROVINCE.md` | `9cf1d450685ae0ed0d15dee1b54e8fd5` / `f1722b163a5c433b003de362ab93ee11` | 51 / 19 |
| `corpus/README.md` (stale since r3) | `98bd00668e84f18cf6781718c4d09ea0` | 20 |
| `calibration-synthesis.md` (Read 464) | `ed8dec8938bf74647d28d630199aa7be` | 463 |
| `census-closeout-receipt-r10.md` | `c5041b5d03e38c774637f47a24304ca8` | 183 |
| `host-health-report-r3.md` / `degraded-triage-r4.md` | `98a0f263f801245f6069e57a9f72d4af` / `d57ae2d48e01777e1ef3c8c0ffb642c9` | 563 / 607 |
| `update-safety-v3.md` / `aur-drift-receipt-r9.md` | `2ac0c21db678c1c806d6de9e546daf2e` / `e7d6f70b65e4846ad7001b5a66e8ec73` | 387 / 248 |
| `journal-boot-plane.md` / `boot-plane.md` | `e5ca40dafc4d1d2a2158fded39067df6` / `e722b7a931858aa5ff1a89ce91cccca9` | 430 / 312 |
| `package-state-plane.md` / `systemd-user-plane.md` / `driver-firmware-plane.md` | `ef93f1b78b6a9e17e8c9d096e7852a02` / `af07a829cfd0307fbe970a2cdc054e18` / `518eda8f0f39f25ee95c715571a9cf95` | 323 / 265 / 256 |
| `kill-event-deep-r8.md` | `6685e1da443f5d368cd41584d2b9943e` | 340 |

**Recheck (read-only, no elevation, from the lane root):**

```bash
md5sum tools/tsukuroi-census.sh                  # expect 945c76fc… (a mismatch = re-read the SKILL addenda first)
bash tools/tsukuroi-census.sh --selftest         # expect rc=0, PASS (80 cases, 80 passed, 0 failed) at this pin
bash tools/tsukuroi-census.sh                    # expect rc=1, six PLANE lines == rollup keys, worst plane DEGRADED
git status --short                               # zero mutation; /var/lib/pacman/db.lck absent after
dkms status; snapper list-configs; ls /boot      # the §3.1 debt rows, re-measured shape
```

- This seat's receipts: `/tmp/w11-s11-1-tsukuroi/` (`hash-before.txt`, `selftest.{out,err}`,
  `live.{out,err}`; ephemeral).
- Errata for this note: append-only, below this line. (A later round's mismatch against
  §0.3's identity pin is a new block, never an edit.)
---

## T11-3 (append) — the final receipt: the six-leg regression at today's pins + the selftest

**Frame.** Lane T11-3, window 2026-10-14 21:33:44Z–21:36:32Z, host `plazir27`, user
`vgpnk`, non-root; every command below executed by this seat in this window. Read-only
on fleet trees — each leg is materialized from its repo's git object store
(`git show <rev>:<path>`) and the tool writes only its workdir; no host mutation, no
elevation, no external site, no live session; secrets/session material shape-only.
Receipts `/tmp/w11-t11-3-ev/` (`selftest.log`, `regression.log`, `pin-read.{sh,txt}`,
`context.txt`); workdir kept `/tmp/w11-t11-3-regression/` (six case dirs). **Write
scope: this append only.**

**Tool revision [obs].** tameshi `tools/mutate-and-run.sh` sha256
`75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` — re-hashed before
(21:33:44Z) and after (21:36:32Z) the run, equal; committed clean at tameshi HEAD
`606716f` ("probation round 10 (training r9): see LOG"); `git status --porcelain --`
the tool = 0 lines. `VERSION` = `r10-2`.

### 1. `--selftest` [obs]

- 21:33:44Z, rc=0, ~5 s; log 82 L; last two lines verbatim:
  `MUTATE_SELFTEST: 80/80 pass` / `VERDICT: PASS`; `grep -c '^PASS'` = 80.
- Hermetic: fixtures under the tool's own `/tmp/tameshi-r4-2-selftest.*`, removed on
  PASS — no retained copy by design (the claim rests on this log).

### 2. `--regression` at today's pins [obs]

- `bash tools/mutate-and-run.sh --regression --workdir /tmp/w11-t11-3-regression`;
  `REGRESSION_DATE 2026-10-14T21:33:55Z`; rc=0; wall 115 s (…21:35:50Z; 32-lane load
  [inf]); closing line verbatim:
  `REGRESSION: PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0 flips<=0)`.

| # | leg | pinned source (repo@rev) | mode | pin sha256 (8) | recorded rate | table |
|---|---|---|---|---|---|---|
| 1 | js-kimi-census | kumitate@`175de6ba` | 100644 | `83016d45` | 8/10 = 80 % | match=10/10 |
| 2 | bash-surface-census | kagi@`fecee874` | 100755 | `275d8294` | 8/10 = 80 % | match=10/10 |
| 3 | bash-tsukuroi-census | tsukuroi@`165307fe` | 100755 | `084951be` | 6/10 = 60 % | match=10/10 |
| 4 | bash-mado-verify | mado@`eead56b2` | 100755 | `d7edaab4` | 4/10 = 40 % | match=10/10 |
| 5 | bash-checklist-run | kagi@`fecee874` | 100755 | `7e5ec98b` | 7/15 = 47 % | match=15/15 |
| 6 | js-claims-check | kumitate@`175de6ba` | 100755 | `e9a21b44` | 7/10 = 70 % | match=10/10 |

- Each leg exact: `flips=0 inconclusive=0`, control green, `MUTATE_RESTORE: OK`
  (per-case `sweep.log`); full sha256 in the log's `REGRESSION_PIN` lines.
- **Today's-pin relation** (independent read this seat, 21:36:02Z, `pin-read.txt`):
  4 current · 2 stale — leg 3 pin `084951be…` vs live HEAD blob `10452443…`; leg 4 pin
  `d7edaab4…` vs live HEAD blob `93e43f8f…`; both recorded pins still ancestors of
  their repo HEADs; the six target paths read byte-clean on `git status --porcelain`
  (no uncommitted drift at the six targets). Stale cells cannot move a replay — the
  legs are git-materialized, and all six matched while two read stale.
- Cross-lane check: this seat's live blob for tsukuroi `tools/tsukuroi-census.sh`
  (`1045244387ffcd5d…`) equals §0.3's census sha256 — one revision, two lanes.

### 3. Spot-checks (three, re-runnable)

- **SC1 — the selftest line.** `grep -c '^PASS' /tmp/w11-t11-3-ev/selftest.log` → 80;
  `tail -2` → `MUTATE_SELFTEST: 80/80 pass` / `VERDICT: PASS`.
- **SC2 — the regression close.** `grep '^REGRESSION: ' /tmp/w11-t11-3-ev/regression.log`
  → the PASS line quoted above; rc 0 recorded at 21:35:50Z.
- **SC3 — pin materialization, independent route.**
  `git -C kagi-shokunin show fecee874:corpus/checklist-run.sh | sha256sum` →
  `7e5ec98b…` = leg 5's recorded pin = its `REGRESSION_PIN`; same route re-hashed legs
  1/3/4 → `83016d45…` / `084951be…` / `d7edaab4…`, all equal.

### 4. Unknowns

- `[unk]` the two stale pins' successor rows at the new live revisions (`10452443…`,
  `93e43f8f…`) are not in `fleet-kill-rate-ledger.md` as of this read (grep, 0 hits on
  both prefixes) — ledger owner's follow-on; this receipt measures, it appends no
  ledger row. Probe: re-read the ledger.
- `[unk]` the selftest's hermetic scratch is tool-managed and removed on PASS; no
  retained copy exists by design.
- `[unk]` sibling seats of round 11 (pin-read, runbook, records) — not cited as landed
  here; the realized files govern.
- `[inf]` the 115 s wall vs round-10's 81.7 s — 32-lane host load; a quiet-window
  timing is the settling probe.
- Bounds: the six-path `git status --porcelain` reads 0 lines (measured after the
  run); nothing above was re-measured from memory.

(appended by T11-3; append-only — later blocks go below, no edits above)
