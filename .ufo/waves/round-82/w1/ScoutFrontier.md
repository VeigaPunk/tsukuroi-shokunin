# ScoutFrontier — round 82, wave w1 (scout)

Scope: census, coverage-map and frontier update in `corpus/README.md` (append-only), and
the open-debt count. Read-only everywhere else. Tools installed: none. Scratch:
`/fast/scratch/hyaku/tsukuroi-r82/ScoutFrontier/` — deleted before yield (see end).

## 1. Census (run by this seat)

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`
- exit code: **0**
- output: 52 `W04` warning lines (same URL across scopes; warnings never change status),
  then `tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`.
  No E-codes. Full output kept at scratch `census.out` (53 lines).
- Row count: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → **332**.
- Cross-check: `sources-census.sh census` → `tsukuroi rows 332`, tier.A 315, tier.B 6,
  tier.C 11, status.mined 294, status.queued 5, status.rejected 33, `FLEET missing 0`, exit 0.

## 2. README lines added (append-only)

- `corpus/README.md` was 792 lines; now **820**. New section `## Round 82 — coverage map,
  frontier and open debt (scout)` at lines 794–820 (28 content lines).
- `git diff HEAD -- corpus/README.md | grep -c '^-[^-]'` → **0** removed lines (diff is 36
  lines in total: headers plus additions). Top `## Frontier` (line 29) left untouched; the
  round's frontier is a new `### Frontier — round 82` subsection, per the README's
  append-only convention.
- Added content: a coverage row for the mount-unit coordinate convention (raw-line anchors,
  C1), a row for the three round-82 instruments with their sha256 and selftest counts, a
  mutation-coverage row (frozen 6/26 and 0/17 at `2786562e` and at `683ae456`), a Frontier
  list of eight open surfaces, and an open-debt list.

## 3. Instrument readings this seat made (committed revisions)

| Claim | Revision | Command | Output | Exit |
|---|---|---|---|---|
| C1 | `d5b3e134` (dispatch tip) | `check-anchor-coordinates.py --revision d5b3e134…` | `count 0 / target 8 / unmet`; all 8 rows `cited-range-not-the-quote-span`, located span +2 lines | rc 1 |
| C1 | `683ae456` (HEAD) | same, `--revision 683ae456…` | `count 0 / target 8 / unmet` | not captured separately (pipeline) |
| C2 | `683ae456` (HEAD) | `mutation-kill-r82.py --revision 683ae456… --work <scratch>` | `killed 6 / total 26`, genuine `0 / 17`, `finding unmet` | rc 1 (printed `RC=1`) |
| C3 | `683ae456` (HEAD) | `check-scorecard-ordinals.py --revision 683ae456…` | `count 1`, finding round 81, axis depth, ordinals [8, 9], sites at :6861 (×3) and :6903 | rc 1 (wrapper exit 1) |
| C3 | `d5b3e134` | same | `count 1` (round 81 depth {8, 9}) | rc 1 (direct) |

Own selftests, run with `TMPDIR` pointed at scratch: `check-anchor-coordinates.py --selftest`
→ `SELFTEST total=12 passed=12 failed=0`; `mutation-kill-r82.py --selftest` → total=4
passed=4; `check-scorecard-ordinals.py --selftest` → total=8 passed=8. Scratch `TMPDIR`
held **0** files afterwards (the selftests honour `TMPDIR`; no `/tmp` write observed).

Mid-wave worktree (uncommitted; NOT a landed state, reported only because it is the
frontier the other seats are moving): `check-anchor-coordinates.py --fixture .` →
`count 8 / target 8 / met`, every row `exact: true`. `mutation-kill-r82.py --fixture .` →
`killed 22 / 26`, genuine `16 / 17`; survivors `C06-source-id-shape`, `C07-own-work-rejection`
(both `genuine_gap: false`), `C16-empty-manifest` and `M06-mutation-unlink-noop` (both
`recipe-missing:old-string-occurs-0x`). See the defect in §5.

## 4. Open debt — the count

Command (on `SKILL.md`, the round-71 operative table, section located by heading):
```
awk -F'|' '/^## Gate and probe registry — round71 superseding current rows/{f=1;next} f&&/^## /{exit} f&&/^\|/{k=$3;s=$6;gsub(/^[ \t]+|[ \t]+$/,"",k);gsub(/^[ \t]+|[ \t]+$/,"",s); if(k=="gate"){g++; if(s ~ /^none/) n++}} END{printf "gate=%d none_selftest_gate=%d\n",g,n}' SKILL.md
```
- at HEAD `683ae456`: `gate=96 none_selftest_gate=34`
- at round-80 tip `96ad75b8` (and `c6fd9949`): `gate=94 none_selftest_gate=34`
- round-80 base `467a9b78` (per the round-80 verifier's own parse): `gate=93 none=36`
- The 96 − 94 difference is the two round-81 gate rows (`count-mount-rows-r81`,
  `measure-round81`), whose self-test cells are non-`none`. The 34 is stable from round 80.
- `kind` `probe` rows (25) and the one `library` row are not counted here.
- Row-level sanity: the 34 `none` rows are the ones printed by the same awk with `s ~ /^none/`
  (e.g. `owed-statements-r29`, `btrfs-space-r30`, `census-handoff-r32`, `scrub-admission-r52`).

## 5. Routed defect (not edited)

C16-empty-manifest and M06-mutation-unlink-noop: the frozen recipe `old` strings contain the
two characters `\n` where the source has a real newline (verified: `grep -c 'digests:.n'`
→ 0; the JSON byte sequence is `\\n`; `source.count(old)` → 0 at the freeze tool). The
instrument therefore records `recipe-missing`, which its own rule says is not a kill. A
manual mutant with a real newline (`if False:` in place of `if not digests:` in
`count-mount-rows-r81.py`, scratch copy only) gives `SELFTEST total=19 passed=18 failed=1`,
rc 3, `FAIL empty-manifest` — so the case is killable, and the recipe text is what blocks
it. [INFERENCE] Under the frozen recipe file the genuine leg cannot reach 17/17. Routed to
the operator; the recipe file was not edited.

## 6. Frontier — surfaces that are real, with the command or path that shows each

1. Automount unit (`Where=`, `TimeoutIdleSec=`): writers `.ufo/waves/round-81/before/src/fstab-generator.c:735`
   and `:336`. Host has none: `grep -cE 'x-systemd\.automount' /etc/fstab` → 0;
   `ls /run/systemd/generator | grep -c automount` → 0. [unk] on live behaviour.
2. `x-systemd.mount-timeout=`: injected at `fstab-generator.c:581` under a branch at :571–581
   not read in full; declined by the entry's Limits; named in S331.
3. Swap unit `swap-swapfile.swap`: live in `/run/systemd/generator/`; fstab line `/swap/swapfile none swap defaults,pri=0 0 0` (`/etc/fstab:22`, `grep -n swapfile /etc/fstab`); writer
   `add_swap` `fstab-generator.c:217`, unit name `:254`. Ordering and `pri=0` unmeasured.
4. tmpfs `/dev/shm`: `/etc/fstab:30` `size=8G`; live `/proc/self/mountinfo` →
   `size=8388608k,…,usrquota`. `usrquota` is not in fstab; journal
   `Nov 02 12:07:20 plazir27 systemd-user-runtime-dir[1485]: Successfully configured disk quota for UID 1000 on /dev/shm to 6.3G`.
   No generated unit (`ls /run/systemd/generator | grep shm` empty). Skip at
   `fstab-generator.c:525` via `mount_point_is_api`, whose definition is outside the pinned
   source [INFERENCE]. Open: who adds `usrquota`.
5. `/tmp` device job bound: `JobRunningTimeoutSec=10s` drop-in in
   `.ufo/waves/round-81/before/host/generator.txt:121–127`; whether it bounds the job queued
   for the kernel device is the entry's MT6 inference, unmeasured.
6. MT7 `x-systemd.requires=`/`wants=` and MT8 `wanted-by=`/`required-by=`: host carries none
   (`grep -cE 'x-systemd\.(requires|wants|wanted-by|required-by)|noauto' /etc/fstab` → 0).
   Fixture-only evidence.
7. Generation provenance: captured generator files dated 17:34:49, after the 2026-11-02
   12:07 boot; cause unknown (entry Limits; `.ufo/waves/round-81/before/host/generator.txt`).

## 7. Debt this seat did NOT close (named, not worked)

- 34 `none`-selftest gate rows at HEAD (the §4 count). Unchanged.
- The C2 answer-key class: `measure-round81` case A compares a printed token, so a
  `--selftest` that prints the token without running its cases passes it
  (`.ufo/waves/round-81/w1/MutCounter/mutants.txt`).
- The C2 recipe-escape defect (§5): the genuine leg's 17th member is not killable as frozen.
- The entry's semantic limits: quotes are located, not shown to entail their statements; the
  anchors are upstream v262 positions, not verified against the installed Arch build (QUALITY 103).

## 8. Bounds respected

- Writes: `corpus/README.md` (append only, 0 removed lines), this report, and scratch.
- No `git add|commit|stash|checkout|reset|pull`; read-only git only. No edits to MANIFEST,
  `.ufo/state/`, `.ufo/watchdog.log`, sibling lanes, `considerthese/`, or the fleet root.
- No subagent dispatch. No `agent://all` messages. No pacman/sudo; no installs.
- Sibling seats' in-flight files (`SCORECARD.md`, `tools/count-mount-rows-r81.py`,
  `tools/measure-round81.py`, the mount-unit entry) were read, never written.
- Scratch: `/fast/scratch/hyaku/tsukuroi-r82/ScoutFrontier/` (clean copies, census output,
  manual C16 mutant, C2 JSON outputs) — **deleted** before yield (`rm -rf`).
