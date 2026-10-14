# Round-6 record — DRAFT (scribe prep, seat SCR-S6)

Status: **draft, pre-landing.** This file is the scribe's working skeleton for the
round-6 `LOG.md` entry and for the round's artifact families (foreign/AUR-risk
register + census baseline extension). It is not the record; the record is the
append-only `LOG.md` entry written after every round-6 artifact has landed
(`AGENTS.md:3`). Every number below is a draft-time capture with its command and
time; the host is live (coredump storm, timers, sibling lanes), so re-run, never
quote.

Draft seat: SCR-S6. Draft window: 2026-10-14 17:38:20–17:4xZ (14:38–14:4x -03),
host `plazir27`, user `vgpnk` (non-root). Write scope: this file only. Scratch:
`/tmp/w6-tsukuroi-scr-s/` (ephemeral). All probes read-only; no
install/upgrade/remove/restart verb was run (`PROVINCE.md:16-17`); `yay` was
only asked for `--version`, no yay transaction verb.

Tags used throughout: [observed] = measured now, command named; [inference] =
join from measurements; [unknown] = named gap with owner.

Round state at draft time [observed]: HEAD `da95290` (probation round 5);
`git status --short` empty (clean tree); **no round-6 artifact has landed yet**
— `corpus/knowledge/foreign-aur-risk-plane.md` absent, no baseline file, census
untouched (`e9327046b05b5c71e07fe511ad7e82dd`, 1032 lines). Sibling round-6
scratch dirs are live under `/tmp/w6-tsukuroi-s62`, `/tmp/w6-tsukuroi-s63`,
`/tmp/w6-tsukuroi-auds6` (listed shape-only, 14:39Z) — the work is concurrent;
this draft's job is to have the fills ready when the artifacts land.

## 1. Plan anchor and the round's measure

`plans/round-6.plan.md` (md5 `81a9be07fecfbf2af7540ea958143d3a`, 2506 B, 38
lines, mtime 2026-10-14 14:05:40 -03; committed in `da95290`; only revision seen
— no worktree/committed split like round 5):

> Axis move: coverage (the foreign/AUR-risk plane) + freshness (per-package
> provenance re-measured from live state and logs, never quoted).
> Claim: the lane's owned surface "foreign/AUR census" (`PROVINCE.md:6-7`) —
> counted by the gate but never measured per package — becomes a plane: all 16
> foreign packages … get a provenance + risk register
> (`corpus/knowledge/foreign-aur-risk-plane.md`) with at least these two
> measured classes and their operator actions: (i) **offline-exile** …; (ii)
> **AUR-local** … The register lands P4's owed "record the accepted baseline"
> as a machine-readable baseline the census reads, so the packages plane
> reports `foreign=` as known-vs-new instead of a bare count — fail-closed: a
> baseline entry can hide neither a new foreign package nor a version change —
> with selftest fixtures; SKILL.md's package/update-safety rows gain the
> foreign-risk rule.
> Anti-claim: … `unknown-provenance` row with the exact operator probe — never
> a guessed channel; no ELF/linkage internals (`readelf`/`ldd`) … the baseline
> splits the count but must not raise a DEGRADED verdict to HEALTHY.
> Measure: register rows = the live foreign count (16 at draft); census
> selftest green incl. ≥3 new baseline fixtures (hit / new / version-drift);
> every class cites its probe (date + command); zero host mutation.

**Plan anchors re-resolved at draft time [observed]** — against the settled
1032-line census revision (`md5 e9327046…`):

- foreign count arm `tools/tsukuroi-census.sh:303-306` (`cap "$PACMAN" -Qm` →
  `foreign_n`), verdict arm `:325` (`foreign_n != '0'` → `PKG_V=DEGRADED`);
  the plan's `:303-325` bracket is exact.
- `degraded-foreign` fixture `:820-822` — three bare-name lines in `$FX/pm`,
  pattern `^PLANE packages: DEGRADED .*foreign=3`.

Interpretation to check when the artifacts land:

- **Register.** One row per live foreign package (16 at draft, §3), each with
  class, channel/db evidence, install date, validation, update path, risk,
  operator action, and the exact recheck command. Both plan-named classes must
  appear; the `unknown-provenance` arm must be present **as a rule**, even if no
  row currently needs it (the anti-claim is a rule, not a row).
- **Baseline.** Machine-readable, committed, read by the census; the packages
  note switches from bare `foreign=16` to known-vs-new (realized format to be
  quoted from the landed revision); fail-closed in both directions (new
  package, version change); never raises a verdict.
- **Selftest.** ≥3 new baseline fixtures (hit / new / version-drift) and the
  executed post-count line quoted (`PASS (35+N cases, …)`); the existing 35
  cases must stay green.
- **SKILL sync.** Package row (`SKILL.md:41`) and the plane-semantics DEGRADED
  bullet (`SKILL.md:318`, "accepted baseline is an operator question") plus any
  selftest-count restatement (`SKILL.md:468-469,519-520,600-601,686-687`) move
  with the landed revision; a stale count is an executor-sufficiency finding,
  not a footnote.

## 2. Draft-time baseline receipts (this seat, read-only)

Gate, re-run 2026-10-14 17:38:33Z (raw captures `/tmp/w6-tsukuroi-scr-s/`):

```bash
bash tools/tsukuroi-census.sh --selftest   # 17:38:31Z, rc=0
bash tools/tsukuroi-census.sh              # 17:38:33Z, rc=1
```

Selftest last line verbatim: `TSUKUROI_CENSUS_SELFTEST: PASS (35 cases, 35
passed, 0 failed)`. Live run verbatim:

```
tsukuroi-census census-v2 — host=plazir27 — 2026-10-14T17:38:33Z — read-only
PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=8(1password-beta,1password-cli,7zip,aalib,abseil-cpp,acl,adwaita-cursors,adwaita-fonts) drift=2[1password-beta,1password-cli] backup_diffs=0 nonroot_artifacts=0; foreign=16; pins=none; holds=pacman glibc; db.lck=absent)
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=1 timers_scanned=1 timer_fail=0 timer_unknown=0)
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=139 (oom=1 io=70 gpu=0 other=68) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=4 nodes=6 pci_10de=2)
PLANE journal: DEGRADED (boots=13 current=yes target=graphical.target:active err=432 (coredump=269 kernel=139 other=24); failedhist=8[...]; timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 timer_unknown=0)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED)
```

The packages plane note is exactly where the baseline lands; the journal/
drivers counts are live-storm captures (round-5 draft saw err=427 at 17:02Z;
this draft sees 432) and are the record's drift caveat, not disagreement.

Artifact pins, hashed 2026-10-14 17:38Z:

| artifact | md5 | lines |
|---|---|---|
| `tools/tsukuroi-census.sh` (round-5 hardened revision) | `e9327046b05b5c71e07fe511ad7e82dd` | 1032 |
| `SKILL.md` | `60ae9bcc6f94413c0507ec63cb14899a` | 706 |
| `LOG.md` / `SCORECARD.md` / `SHONEN.md` | `a3cfa972…` / `30de3424…` / `9cf1d450…` | 168 / 17 / 51 |
| `PROVINCE.md` / `AGENTS.md` | `f1722b163a5c433b003de362ab93ee11` / `390017cff803cc8798dd3b51d48a82f0` | 19 / 6 |
| `corpus/README.md` | `98bd00668e84f18cf6781718c4d09ea0` | 20 |
| `plans/round-6.plan.md` | `81a9be07fecfbf2af7540ea958143d3a` | 38 |
| `corpus/knowledge/timer-drift-plane.md` (r5) | `fc0760c8070c9387ff5334f0f8c645cc` | 333 |
| `corpus/knowledge/boot-plane.md` (r4) | `e722b7a931858aa5ff1a89ce91cccca9` | — |
| `corpus/knowledge/degraded-triage-r4.md` (r4) | `d57ae2d48e01777e1ef3c8c0ffb642c9` | — |
| `corpus/knowledge/package-state-plane.md` | `ef93f1b78b6a9e17e8c9d096e7852a02` | — |
| `corpus/knowledge/journal-boot-plane.md` | `e5ca40dafc4d1d2a2158fded39067df6` | — |
| `corpus/knowledge/systemd-user-plane.md` | `af07a829cfd0307fbe970a2cdc054e18` | — |
| `corpus/knowledge/driver-firmware-plane.md` | `518eda8f0f39f25ee95c715571a9cf95` | — |
| `corpus/knowledge/update-safety-note.md` | `5cc3067fec33d261d8bff6a5c7e8ac48` | — |
| `corpus/knowledge/host-health-report-r3.md` | `98a0f263f801245f6069e57a9f72d4af` | — |
| `corpus/knowledge/executor-test-sufficiency.md` | `4b2c1d3612db7db1477da92aaec39862` | — |

All hashes are of committed bytes (clean tree) — nothing in this table can have
drifted under the draft except by a sibling lane landing (re-check at entry).

**Foreign-set freshness anchor [observed].** `pacman -Qm` (17:38:21Z, 424 B) is
**byte-identical** (`diff` rc=0) to the round-1 capture `/tmp/tsukuroi-foreign.txt`
(09:54Z): the 16 name+version lines have not moved in ~7 h 44 min. The register
therefore describes a stable set, not a moving one — the freshness claim is
about re-measuring, not about drift. Sibling shape, 14:38–14:41Z: lane s62's
`foreign.qm` is byte-identical to this seat's capture (`diff` rc=0) and that
lane is building signature/receipt evidence (`signer.pub`, `verify.log`,
`chain.tsv`, `receipt.tsv` — names only, contents not read by this seat); s63
carried only an unrelated OOM table. If the signature evidence lands, the
register may cite it — two lanes' tables must not be merged.

Eligibility probes, all 16, 17:38–17:41Z:

- `pacman -Q | wc -l` = 1188; `pacman -Qe | wc -l` = 207; `pacman -Qm | wc -l` = 16.
- `pacman -Si <pkg>` → rc=1 for all 16 (absent from every **configured** sync
  db); capture `/tmp/w6-tsukuroi-scr-s/si-absence.out`.
- `pacman -T $(awk '{print $1}' foreign.list)` → rc=0, empty output (all
  declared dependencies satisfied).
- targeted `pacman -Qkk android-apktool-bin obsidian-cli-inspector
  omarchy-walker elephant` → rc=0, `0 altered` on each (the register's packages
  are swept clean today).
- `pacman -Qu` (no pipeline) → rc=1, 0 lines (nothing pending).

**Method trap re-confirmed live, this seat.** `pacman -Qu | head` reported
`rc=0` — that rc is `head`'s, not pacman's; without the pipe pacman answers
rc=1/empty. Same for `pacman -Qkk … | tail`. The record must not carry any
pipelined rc as a measurement (`journal-boot-plane.md` method lesson "pipelines
hide rc", re-proven at 17:39Z).

## 3. Provenance evidence (the register's raw material, measured)

### 3.1 The 16 rows

`pacman -Qi` fields + `/var/log/pacman.log` install lines + `bsdtar -tf
/var/lib/pacman/sync/offline.db`, 17:38–17:41Z:

| package | version | install date | reason | Validated By | class (proposed) |
|---|---|---|---|---|---|
| `elephant` + 12 `elephant-*` | 2.21.0-1 | 2026-10-03 17:44:26 | dep of `omarchy-walker` | SHA-256 Sum + Signature | offline-exile |
| `omarchy-walker` | 1.0.0-2 | 2026-10-03 17:44:26 | explicit | SHA-256 Sum + Signature | offline-exile |
| `android-apktool-bin` | 3.0.3-1 | 2026-10-13 13:52:59 | explicit | None | AUR-local |
| `obsidian-cli-inspector` | 1.0.3-1 | 2026-10-13 16:21:20 | explicit | None | AUR-local |

Counts: 3 explicit / 13 dependency — matches the plan's "3 explicit + 13
omarchy-walker deps" [observed]. The plan's two install timestamps are exact
(pacman.log `:2093`, `:2100`).

### 3.2 offline-exile channel evidence (14 rows)

- `/var/log/pacman.log` lines `1096-1110`: the 13 `elephant-*` + `omarchy-walker`
  all installed in one transaction at `2026-10-03T17:44:26-0300` (line 1099 in
  between is `wl-clipboard`, unrelated).
- `bsdtar -tf /var/lib/pacman/sync/offline.db` (world-readable, `-rw-r--r--`;
  2550 entries, list in scratch) contains exactly `elephant-2.21.0-1/…` (all
  13), `omarchy-walker-1.0.0-2/…`, and `walker-2.16.2-1/…` — the same versions
  that landed that day [observed].
- `offline.db` birth `2026-10-03 17:41:33.994891750 -0300`, mtime `2026-07-20
  21:11:36` (upstream stamp, copied); `grep -c offline /etc/pacman.conf` = 0 —
  the db is **not a configured repo** and cannot be queried (`pacman -Sl
  offline` → repo not found; already in `package-state-plane.md:82-84`).
- The 10-03 install line is a plain `pacman -S --noconfirm --needed … omarchy-walker …`
  (log `:484`) — a `-S` cannot install from an unregistered db, and the four
  configured dbs (`core/extra/multilib/omarchy`) all have birth 2026-10-11
  12:54:13.542054496, i.e. **after** 10-03 [observed, this seat 17:42Z:
  `stat -c '%w' /var/lib/pacman/sync/{core,extra,multilib,omarchy}.db` — all
  four birth `2026-10-11 12:54:13.542054496 -0300`; `offline.db` birth
  `2026-10-03 17:41:33.994891750 -0300`].
- **Chain [inference, named as such]:** at install time a repo served by
  `offline.db` must have been registered (the installer's own pacman config,
  replaced afterwards — the current config has no such stanza), and the 14
  packages carry signature validation because that repo's `SigLevel` required
  it. Direct proof (the installer's historical pacman.conf, or a log naming
  the db) is **not available read-only** → the register's "channel was
  offline.db" line must read as [inference] with this evidence chain, not as a
  probe result. The exact operator probe that would settle it: the installer
  media's `/etc/pacman.conf` (or its logs), which this lane cannot reach.
- Update path: none. The 14 are absent from all four configured dbs
  (`pacman -Si` rc=1) and from the omarchy channel listing (`pacman -Sl
  omarchy | grep -E 'elephant|omarchy-walker'` → no rows; only `walker`,
  `walker-debug`, `yay`, `yay-debug` matched the wider grep) [observed].

### 3.3 Exposure chain `omarchy-walker → walker` [observed]

- `walker` 2.16.2-1 came from the same 10-03 transaction (log `:1095`); it is
  **not** foreign today because the omarchy channel now carries it:
  `pacman -Sl omarchy` → `omarchy walker 2.17.0-1 [installed]`.
- `walker` was upgraded `2.16.2-1 → 2.17.0-1` at `2026-10-11T16:14:39-0300`
  (log `:1943`); install date matches (`pacman -Qi walker`).
- `omarchy-walker` stayed at `1.0.0-2` (built 2025-11-21, installed 10-03) —
  so one silent `walker` move has already happened beneath a frozen meta
  package; a second is possible on any `-Syu` of the omarchy channel.
- Whether `omarchy-walker` 1.0.0-2's expectations still hold at walker 2.17.0-1
  is a linkage/binary question → **out of province** (no `readelf`/`ldd` per
  the plan's anti-claim); if the register needs it, the row reads `out of
  reach` and the question is reported to kaidoku/revenger.

### 3.4 AUR-local evidence (2 rows)

- Exact invocations in `/var/log/pacman.log` [observed]:
  - `:2092` `[PACMAN] Running 'pacman -U --needed --noconfirm --config
    /etc/pacman.conf -- /home/vgpnk/.cache/yay/android-apktool-bin/android-apktool-bin-3.0.3-1-any.pkg.tar.zst'` (13:52:59), followed by
    `pacman -D --asexplicit … android-apktool-bin` (`:2101` semantics: explicit).
  - `:2100`-adjacent `pacman -U --noconfirm --config /etc/pacman.conf --
    /home/vgpnk/.cache/yay/obsidian-cli-inspector/obsidian-cli-inspector-1.0.3-1-x86_64.pkg.tar.zst` (16:21:20) + `pacman -D -q --asexplicit`.
- Both carry `Validated By: None` and `Packager: Unknown Packager` (`pacman
  -Qi`) — a local-file install path with no repo signature; the artifacts are
  still in the yay build cache (`~/.cache/yay/<pkg>/*.pkg.tar.zst`, 15.3 MB /
  1.7 MB).
- Build receipts present: `PKGBUILD` + `.SRCINFO` + `.git` per cache dir
  (maintainers named in the apktool PKGBUILD; the obsidian one ships a source
  tarball with a pinned sha256 `561a5301…dfa4f`) [observed, heads only].
- Update path = the AUR helper: `yay 13.0.1-1`, omarchy channel
  (`pacman -Sl omarchy` → `omarchy yay 13.0.1-1 [installed]`; installed
  2026-10-11 16:14:39, same upgrade window as walker) → the register's risk
  class is review-on-update discipline, not a broken channel [observed for the
  version/channel; the discipline claim is the register's judgement].
- Whether the cached `.pkg.tar.zst` bytes still equal what was installed is
  **not** directly checkable from the local db (it stores no archive digest);
  `pacman -Qkk` clean today is the usable stand-in [unknown, §8 U5].

## 4. Baseline contract skeleton (fill rules for the census extension)

Lane decisions are open (file name/format/path are the census lane's call);
this section fixes **what the record must be able to state**, so the fills are
adjudicable:

- **File.** Machine-readable, committed, inside the lane's write surface
  (proposal: `corpus/knowledge/foreign-aur-baseline.tsv`, one row per accepted
  package: `name<TAB>version<TAB>class<TAB>install-date<TAB>evidence<TAB>probe-date`).
  Whatever lands, the record pins its path, md5, line count.
- **Read.** An env override consistent with the existing family
  (`TSUKUROI_*`, `tools/tsukuroi-census.sh:146-161`; e.g.
  `TSUKUROI_FOREIGN_BASELINE`), default = the committed file; hermetic in
  `--selftest` via the fixture dispatcher (`:692-694`).
- **Packages note.** Proposal `foreign=16(known=16 new=0 drift=0 gone=0)`; the
  record quotes the realized string from an executed live run, not this
  proposal.
- **Fail-closed rules (each needs a fixture):**
  1. name in `-Qm` but not in baseline → counted `new`; plane stays DEGRADED;
     names printed.
  2. name matches, version differs → counted `drift`; stays DEGRADED; both
     versions printed. (A silent version change must be visible: this is the
     plan's second half.)
  3. baseline row no longer installed → counted `gone` (never silently
     dropped; a stale baseline row that vanishes without a word would hide a
     package being replaced).
  4. baseline absent or unreadable → note carries `baseline=absent|unreadable`;
     the bare `foreign=<n>` count still gates and can never read HEALTHY off a
     missing baseline. (Worst case it may be a BLOCKED arm; the lane chooses —
     the record must state which.)
  5. baseline can never lower a verdict: any `new`/`drift`/`gone`/check-failure
     leaves DEGRADED DEGRADED (plan anti-claim).
- **Fixture shape prerequisite [observed].** The current foreign fixture writes
  bare names (`printf 'elephant-a\nelephant-b\nelephant-c\n' > "$FX/pm"`,
  `:821`) and the dispatcher returns that file verbatim for `-Qm` (`:649`).
  Real `pacman -Qm` prints `name version` (`android-apktool-bin 3.0.3-1`, …).
  A version-drift fixture therefore requires the fixture `pm` to carry
  versions; with bare names the drift arm is untestable and the fixture would
  be vacuous. The record should say which shape the landed fixtures use.
- **Selftest delta.** ≥3 new cases (hit / new / version-drift) on top of 35;
  the record quotes the executed `PASS (35+N cases…)` line, and the SKILL
  count restatements move in the same round.

## 5. Register skeleton (the note's fill rules)

`corpus/knowledge/foreign-aur-risk-plane.md` (name per plan) — per-row columns
the record will spot-check: `package | version | class | channel/db evidence
(file:line or command, dated) | install date | validation | update path | risk
| operator action | recheck command`.

- Class vocabulary (proposal; realized set to be quoted): `offline-exile`
  (14) · `aur-local` (2) · `unknown-provenance` (rule, no row today) ·
  `out-of-reach` (linkage questions routed, never absorbed).
- Operator-action vocabulary (proposal): `accept-and-recheck` (baseline row) ·
  `freeze/pin decision` · `replace-from-channel` · `remove` · `route-out`
  (kaidoku/revenger for linkage). Each row must name **one** action.
- Every class cites its probe (date + command) — the §3 evidence is the draft's
  candidate citation set; the record verifies at least two rows per class by
  re-running the cited command.
- Recheck commands the register should carry: `pacman -Qm`,
  `pacman -Qi <pkg>`, `pacman -Si <pkg>` (rc), the pacman.log grep used,
  `bsdtar -tf /var/lib/pacman/sync/offline.db | grep -E '<pkg>'`,
  `pacman -Sl omarchy | grep -E 'walker|yay'`. yay's own upgrade-check verb was
  **not** run by this seat and must not be quoted as if it were.

## 6. Record skeleton (what the `LOG.md` entry must carry on landing)

Fill on landing; keep the round-3 shape (long single bullet) — rounds 4/5 used
a one-line entry plus the artifact files, which the round-6 scribe may follow
only if the entry still names artifacts + verifiers + axes (the round-5 commit
`da95290` shows the one-line precedent; the plan's measure is finer than one
line can carry, so a compact multi-line bullet is safer).

- **Work (observed in tree):** `⟨artifact list: path, seat/ID, md5, lines,
  mtime⟩` — expected members: the register note, the baseline file, the census
  revision (new md5 + case count), the SKILL rows, plus scribe-owned coverage/
  SCORECARD/LOG. Hash at entry; the storm drifts live values but artifact
  bytes are stable once landed.
- **Scribe re-verification:** §7 command set; quote the selftest line, the live
  package-plane substring (with the new `foreign=` shape), and one row per
  class from the register re-executed.
- **Ancillary scribe writes (owed at record time):**
  - `SCORECARD.md` round-6 move-log row (axes: coverage + freshness — confirm
    against `AXES.md` vocabulary before writing).
  - `corpus/README.md` coverage rows — **collapsed debt**: the map still ends
    at round 3 [observed: `git log --oneline -- corpus/README.md` last touched
    `9bcd162` (round 3); no rows for `boot-plane.md`, `degraded-triage-r4.md`,
    `timer-drift-plane.md`, the round-4/5 census revisions, or round 6]. The
    round-6 scribe should land round-4/5 back-rows + round-6 rows or state the
    debt stays open, not silently skip.
  - `SKILL.md` sync (package row + DEGRADED arm + selftest count).
  - Form defect to correct with evidence: `SCORECARD.md:16` (round-4 row) is
    still malformed — an unescaped `|` truncates the After cell to
    `boot plane (299 L` [observed 17:40Z].
- **SHONEN boxes:** all four `[~]` (asserted with round-3 verifier names,
  `SHONEN.md`); the round-6 record may refresh evidence pointers but must not
  upgrade to `[x]` — that stays with the non-author promotion review.
- **State at entry:** commit hash landed for the round, or "round work
  uncommitted in tree" + exact `git status --short`; the scribe writes only its
  named files; the commit carries the lane identity.
- **Candidate entry skeleton (fill at landing):** `round 6 (training r5):
  foreign/AUR-risk plane — 16-package provenance register (14 offline-exile:
  elephant-* + omarchy-walker, offline.db birth 2026-10-03, no channel; 2
  AUR-local: yay-cache `pacman -U`, Validated By None) + census baseline
  (selftest 35→35+N, fixtures hit/new/version-drift, known-vs-new note,
  fail-closed) + SKILL foreign-risk rows. Axis: coverage + freshness.
  Verifiers: ⟨names⟩.`

## 7. Scribe re-run set (receipts owed by the record)

```bash
cd ~/Projects/shokunin/tsukuroi-shokunin
bash tools/tsukuroi-census.sh --selftest            # expect rc=0, 35+N/35+N PASS
bash tools/tsukuroi-census.sh                       # expect rc=1, packages DEGRADED, new foreign= shape
md5sum tools/tsukuroi-census.sh                     # vs e9327046… (pre-round) or landed revision
wc -l tools/tsukuroi-census.sh
pacman -Qm                                          # 16 lines, name+version, byte-diff vs /tmp/tsukuroi-foreign.txt
pacman -Qm | wc -l; pacman -Q | wc -l; pacman -Qe | wc -l
while read -r p v; do pacman -Si "$p" >/dev/null 2>&1; echo "$p $?"; done < <(pacman -Qm)   # expect all rc=1
pacman -T $(pacman -Qm | awk '{print $1}') ; echo "rc=$?"   # expect rc=0 empty
pacman -Qi android-apktool-bin obsidian-cli-inspector omarchy-walker | \
  grep -E '^(Name|Version|Install Date|Install Reason|Validated By|Packager)'
grep -nE 'installed (android-apktool-bin|obsidian-cli-inspector|omarchy-walker|elephant[ -])' /var/log/pacman.log
stat -c '%w | %y | %n' /var/lib/pacman/sync/offline.db
bsdtar -tf /var/lib/pacman/sync/offline.db | grep -E '^(elephant-|omarchy-walker|walker-)' | head
pacman -Sl omarchy | grep -E 'walker|yay'
yay --version                                       # read-only; no yay verb beyond this
git status --short                                  # zero-mutation receipt
```

## 8. Unknowns register (draft-time; owners)

1. Baseline artifact name/format/default-read + the realized `foreign=` note
   shape (owner: census lane). The record pins the landed string.
2. Baseline absent/unreadable semantics: fail-closed as DEGRADED-note or as
   BLOCKED (owner: census lane; must be stated, never implied).
3. "Channel was offline.db" is [inference] from the evidence chain (§3.2);
   the direct proof (installer config/log) is out of reach read-only (owner:
   operator/installer record). The register must keep the tag.
4. The register's wording trap: "absent from every sync db" is true of every
   **configured** db; `offline.db` sits in the sync dir and *contains* 14 of
   the 16. Records must not write the unqualified phrase (owner: record
   scribe).
5. AUR-local cached-artifact integrity (does the `.pkg.tar.zst` in
   `~/.cache/yay/<pkg>/` still match what was installed?) — local db stores no
   archive digest; `pacman -Qkk` clean is the stand-in (owner: register lane,
   probe design).
6. `omarchy-walker` 1.0.0-2 vs `walker` 2.17.0-1 compatibility — linkage
   question, out of province; route to kaidoku/revenger if the register needs
   it (owner: register lane; PROVINCE refusal honored).
7. Round-4/5 coverage debt in `corpus/README.md` + the malformed
   `SCORECARD.md:16` row + SKILL selftest-count sync (owner: record scribe).
8. Carried rounds 1–5 register items unchanged: root `-Qkk` delta; literal
   `source:`/`verified-at:`/`recheck:` keys; `corpus/lessons/round-1.md`;
   "20-min cap" (owner: integrator); E1–E5; sweep-pin ordering / two-author
   sweeps of one artifact; timer-drift selector realization; 310 s mass;
   `NEXT -` semantics vs systemd version.

## 9. Errata / pending (append-only)

- 2026-10-14 — this draft file created by SCR-S6; it is prep, not a record.
  The `LOG.md` round-6 entry remains owed (`AGENTS.md:3`); measures are judged
  against the landed register + baseline + census revision, not this skeleton.
- 2026-10-14 — all counts in §2/§3 are captures on a live host (coredump storm
  observed: err 427→432 in 36 min; round-5 draft 17:02Z → this draft 17:38Z);
  re-run, never quote (drift precedent `host-health-report-r3.md:441-462`).
- 2026-10-14 — pipeline-rc trap re-confirmed by this seat's own slip
  (`pacman -Qu | head` rc=0 is head's); §2 carries the unpiped re-run.
- 2026-10-14 — the round is concurrent: sibling lanes landed nothing at draft
  time (`git status` clean at 17:38Z); the record scribe fills every generic
  slot with actual filenames, md5s and executed lines at entry.
- 2026-10-14 — final-file spot-check and this file's own line count/md5 are
  reported in the seat's handoff, not in-file (a further edit would invalidate
  them).