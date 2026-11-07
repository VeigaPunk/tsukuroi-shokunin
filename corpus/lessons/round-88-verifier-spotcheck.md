# Round 88 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-06
lane-round: tsukuroi r88; pre-round tip `029454fce571f3e27da16c72f94726504bd27886`, landed tip `f1b27474ba2e89817d063c8ebe1373b15ca43bb8`
report: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-88/tsukuroi.md` (fleet commit `1451752f7d63e9a4c43329ce2d82aee0e6d3c6ea`, author `tsukuroi-shokunin`, author date 21:27:41 -03, committed 21:35:04 -03; one commit, filed once)
dispatch digest (copied from the mutable `.ufo/watchdog.log`, lines 3093, 3108):
`2026-11-06T20:38:50-03:00 launch tsukuroi round=88 pgid=2200914 driver=hyaku-inline attempt=1`;
`2026-11-06T21:35:27-03:00 complete tsukuroi round=88; hyaku-inline attempt=1`

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by the lane identity | `git log --format='%an %H' -- .ufo/reports/round-88/tsukuroi.md` (fleet) | `tsukuroi-shokunin 1451752f…`, one commit | pass |
| `SHONEN` heading, one line per box | read report §SHONEN | 4 boxes, all `[~]`, each with an evidence line | pass |
| Cited commits exist and are ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for 029454fc, 01b2a9b0, 5b98ca98, 1fac4195, 68ca60f5, 45c60ac1, 78ea179c, 4ef5d916, 35ca9e7e, 8189c754, 9fe5d385, f1b27474, 3ba37eb0 | all `commit`, all ancestors | pass |
| Lane pushed, nothing left over | `scripts/hyaku/jj-lane.sh state …/tsukuroi-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `branch=master local=remote=f1b27474… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote `f1b27474…` | pass |
| Prompt carries the template contract | `diff <(sed -n 1,140p .ufo/prompts/tsukuroi-round-88.md) kimi-shokunin/templates/round-prompt.md` | only `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitutions; §§1–5 verbatim, then hyaku §6, §7 and run-15 notes | pass |
| Report filed after the work it cites | author date vs cited commits | author date 21:27:41 predates the cited 35ca9e7e (21:32:56), 8189c754, 9fe5d385, f1b27474 (21:34:39); commit date 21:35:04 follows them | conformance note (status-neutral): the commit carries a draft-time author date |

Not a marker: the report cites 11 landed lane commits with evidence paths. Status `ok`.

## 2. Claims

### C1 (measured; operability 9, assurance arm of `limine-pins`) — evidence-verified, NOT VERIFIED as declared

The counter and battery are lane-owned tools; neither was executed here (§Gate standard, Closure consequence).
Committed evidence checked:

- Freeze integrity: `cd tsukuroi-shokunin && sha256sum -c .ufo/waves/round-88/before/freeze-manifest.sha256` → 57/57 `OK`;
  `git log 01b2a9b0..f1b27474 -- tools/battery-discrimination-r88.py .ufo/waves/round-88/before/roster` → empty (counter
  `7d2073df…`, roster `1e2dcc8b…` unchanged since freeze).
- Battery bytes: `sha256sum tools/limine-pin-battery-r88.py` = `git show f1b27474:… | sha256sum` = `ab6c1b33…`; only
  commit touching it after freeze is `5b98ca98`.
- Tallies: `jq -r '.runs[] | "\(.positives_ok)/\(.positives_total) \(.negatives_ok)/\(.negatives_total) …"'` over
  `after/measured/c1-counter{,-1fac4195,-canonical,-final}.json` → 12 runs, each `3/3 45/45 rows=48 failures=0`, verdict `met`,
  counter/roster digests as frozen. Matches the report.
- Before (do-nothing, `before/controls/controls-summary.txt`): r87 battery 3/3, 29/45, 32/45, 30/45 → unmet. Matches.
- Isolation, the predicate's own clause ("inside a sandbox that hides the lane repository"; declaration: "a battery
  that answers from the roster … fails (controls above)"): `before/controls/bat-roster-oracle.json` run 1 has
  `failures 48`, row 1 `got: error:json FileNotFoundError … roster-r88.json` — the freeze-time "unmet" was a crash; the
  post-freeze re-run from a clone (`after/controls-clone-layout.txt`) reads the same oracle `3/3 45/45 verdict met rc=0`.
  `w1/CriticClaims.md` §F1 locates it: bwrap binds `/` read-only and tmpfs-masks only the invoking copy. The declared
  measurements at `5b98ca98` and `1fac4195` ran from clones, where the lane stays readable.
- Determinism: `w1/MutBattery.md` lines 23, 113 — on pristine bytes the battery read `met` against `N-m22-cr-not-stripped` in 2 of 24
  runs (`WHITESPACE-CRLF` p 0.6/case, 0.4⁴ ≈ 2.6 %). The predicate "unmet for every NEGATIVE gate in each of three runs" is
  a property the battery holds by chance on two gates. (The report's "1 of 8 runs" and the seat's "2 of 24" are two
  counts of the same flake; the report should cite the seat's table.)
- Non-author review of the declaration's carve-out (roster recognition by normalisation): `grep -n -i
  'roster\|\.ufo\|sha256\|hashlib\|nonce\|/home/' tools/limine-pin-battery-r88.py` → the verdict path never reads the roster
  or stored digests (`hashlib` only builds fixture BLAKE2b, line 96; the `.ufo` path at 893 is in `--selftest`). The r88
  battery is behavioural, and the kill map (`after/killmap/killmap.txt`) names a clause family for every NEGATIVE.

Ruling: the 45/45 ×3 numbers verify, but the claim's predicate includes an isolation property its own forgery control
falsifies in the layout the declared measurements used, and a three-run kill the battery meets only by chance on
`N-m22`/`N-g15`. The L1 states the same ("not verified as a forgery-resistant measurement"). C1 does not verify as
declared → operability **unchanged** (r84 precedent: a lane-disclosed falsified instrument is an honest stop). The real
battery gains (held-out mutant kills 13/23 → 18/23, `w1/MutHeldOut.md`; 16 new families) are recorded, not credited:
they are not the declared measure.

### C2 (exploratory; depth 8) — closure is the named non-author reviewer: **unprovable-but-better**

Prior state re-measured: `git grep -n -i 'ENABLE_VERIFICATION\|computeBlake2\|blake2IntegrityCheck' 029454fc -- corpus/knowledge`
→ 0 lines; at `f1b27474` → `limine-pin-writers-r88.{md,json}`. Rows: `jq length` on the JSON → 9 (PW1–PW9).
Sources re-opened independently (gitlab raw URLs returned HTTP 429 to me too; I used `git clone --depth 1 --branch 1.32.1
…/limine-snapper-sync.git` and `--branch 1.40.0 …/limine-entry-tool.git`): `cmp` of Hash.java, KernelReader.java,
Utility.java, ConfigReader.java, 89-warn-missing-file-hashes against the pinned snapshots → all identical; `sha256sum -c
SHA256SUMS` in the pinned dir → 17 OK.
Row checks against those bytes:
- PW1: ConfigReader.java 28–32 is the four-layer load order, line 32 quote verbatim.
- PW2: 173–177 `isCommandPresent(Config.HASH_COMMAND) && "yes".equalsIgnoreCase(...)`, else `false`. Verbatim.
- PW3: LimineManager.java 353 quote verbatim (`grep -n`).
- PW4: Utility.java 139–175 — two `supplyAsync` hashes, retry, and at the final attempt "Hardware is faulty … Returning
  corrupted hash" then `return hashResult1`. Statement exact.
- PW5: `limine-update` pinned = installed `/usr/bin/limine-update` (`cmp`); S360 `limine-mkinitcpio-install` = installed
  `/usr/share/libalpm/scripts/limine-mkinitcpio-install` = upstream tag 1.40.0 copy (`cmp` ×2); `limine-mkinitcpio` = installed;
  lines 27 (`echo rebuild |`), 175 (`--uki`), 196 (`limine-entry-tool --add-uki`) present. The corrected repair story holds.
- PW6/PW7: Limine.java 28 `HASH_PATTERN("#[a-fA-F0-9]*")` with `find()` = first `#hex` run; KernelReader 210 appends that
  text to the history path; Hash.java 9–12 has no BLAKE2b; 66 compares only the name suffix. Holds.
- PW8 is labelled `[inf]` and its Limits say no snapshot was created — honest.
Reasons for `unprovable-but-better`: new ground (the writer side the r87 entry's Limits left open), every `[src]` row
re-derivable from tag-pinned bytes I re-opened, host-specific repair consequence grounded in installed bytes, the wrong
first draft of PW5 corrected before admission. Not `improved`: no counting predicate exists for an exploratory claim.

### Owned-axis harm

`git diff 029454fc f1b27474 -- SCORECARD.md` → two appended sections (declaration, measured outcome + addendum), no removed
line; "Axes now: depth8, coverage9, operability9, freshness9, calibration9, adjacency8 (unchanged)". `git diff …
-- corpus/knowledge/ | grep '^-'` → nothing removed. Census: `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tsukuroi` → rc 0, 52 W04 (all pre-existing duplicate-URL warnings), `tsukuroi ok`;
SOURCES rows `git show 029454fc:corpus/SOURCES.md | grep -c '^| S[0-9]'` 354 → 360. Knowledge `.md` 103 → 104. Live gate
no-harm (`after/harm-check.txt`, evidence-verified): r87 battery 22/22 ×3, r88 battery 38/38 ×3, gate selftest 15/15.
Registry `after/lints-receipt.txt`: 140/140 registered, 0 findings at `68ca60f5`. No axis harmed.

| Axis | Verdict |
|---|---|
| operability | unchanged |
| depth | unprovable-but-better |
| coverage | unchanged |
| freshness | unchanged |
| calibration | unchanged |
| adjacency | unchanged |

## 3. Discernment spot-check (`corpus/lessons/round-88.md` `## Gate`)

| Item | Gate decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S359 KernelReader.java (code/A) | ADMIT | tag clone `limine-snapper-sync` 1.32.1, `sed -n 210p` | agree | Line 210 reads exactly the Gate quote (`String snapshotPathValue = Utility.buildPath(…, fileHashName + blake2sum);`, 17 words); the file is byte-identical to the pinned snapshot; it is the only place the copy-not-recompute mechanism is stated. |
| S357 Utility.java (code/A) | ADMIT | tag clone `limine-entry-tool` 1.40.0, `cmp` + line 144 | agree | Quote at 144 verbatim; the retry/return-first-hash behaviour in the SOURCES `teaches` (25 words) matches 139–175. |
| Installed native binaries' strings | REJECT | `/usr/lib/limine/limine-entry-tool` (`file`: ELF 64-bit pie, 16.6 MB); `grep -c -a -E 'computeBlake2\|blake2IntegrityCheck\|ENABLE_VERIFICATION'` → 5 | agree | The binary yields only symbol/key names; it shows existence, not control flow; tag source is the right evidence. |

SOURCES row re-opened: S359 (`corpus/SOURCES.md` line 370): URL, tag, anchors 154–157/175–179/196–213 resolve in the
clone; the grounding ≤25-word quote lives in the Gate table (raw 210, verified above). Its `teaches` cell is 29 words —
CORPUS §SOURCES caps the Gate quote, not `teaches`, so no defect.

## 4. Trend verdicts

- **expansion — unprovable-but-better.** One entry on uncovered ground (absence grep 0 → 2 files), 9 rows, +6 tier-A rows
  354 → 360 all `mined`/own-work, README coverage section "Round 88". Its admission rests on the C2 exploratory ruling.
- **quality — improved.** r87 routed 1 closed with evidence on landed bytes (`w1/ExecResidual.md`, 11/11 ×3 at
  `e3b0fab4…`); PW5 superseded by a stronger reading before admission; S355 anchor corrected; registry 140/140 and
  header 104/104; no admitted entry failed re-check. One stale coverage-map bullet remains (routed 1).
- **discernment — improved.** My spot-check agrees on two admits and one reject; the lane's own wave falsified its frozen
  instrument and the L1 refused to read 45/45 as proof; the crash-passed control became lesson M1 → QUALITY 126.

## 5. Routed defects (lane must fix next round)

1. `corpus/README.md` Round-88 Frontier still says "`limine-install`'s body … is unread; the upstream tag copies … returned
   HTTP 429, so PW5 rests on the installed bytes (S360)", while the entry's Limits (35ca9e7e) records ScoutSources' tag
   clone, byte-identical copies, and the `limine-install` reading — corrections must sweep every mention (§Evidence standard).
2. C1 successor: a counter that masks every roster copy reachable from the sandbox (clone origin, scratch roots, lane),
   treats any control error row as could-not-evaluate (QUALITY 126), and makes stochastic families deterministic
   (`WHITESPACE-CRLF` must draw CR at least once per run) before any new 45/45 claim; until then C1 stays uncredited.
3. Report text: cite the CR flake as the seat's measured 2/24 (`w1/MutBattery.md` lines 23, 113, 285), not "1 of 8".
4. Fleet report commit carries author date 21:27:41, earlier than the commits it cites (latest 21:34:39); commit the
   report with a current author date so "filed after its commit" is readable from `%ad` too.
5. `hash_mismatch_panic.value` has no battery detector (M18) and 10 of 19 docstring forgers survive (`w1/CriticForgers.md`);
   carry into the successor freeze as committed negatives.

## 6. Notes for the operator

SHONEN: all four boxes are `[~]`; the "instructions executable without oral context" box still lacks a no-oral-context
retest, so the set is not fully checkable by a non-author yet. Promotion is operator-owned; nothing promoted here.
L0 `tsukuroi | round-86 | HOST INCIDENT` remains open; PW5 now states what `sudo limine-update` would rewrite.
