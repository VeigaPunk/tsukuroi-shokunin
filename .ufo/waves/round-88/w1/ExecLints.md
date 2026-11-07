# ExecLints — round 88 wave w1 (executor, lane gates at the tip)

Lane revision measured: `1fac4195243e55e7d9d8a2eddd653443d8559bff` (`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master`).
Clean room: `git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin $S/lane` (S = `/fast/scratch/hyaku/tsukuroi-r88/ExecLints`), every gate run from the clone's cwd by absolute tool path.
Host: read-only. No `sudo`, no pacman, no `/boot` write. No tool installed or upgraded (none needed).
Receipts beside this file: `coverage.txt`, `header.txt`, `gate-selftest.txt`, `census.txt`, `entry-and-sources.txt`, `cli.txt`, `counter-tampered-roster.{txt,json}`, `counter-freeze-selfcheck.patch`.

## Verdict per check

| # | Check | Verdict |
|---|---|---|
| 1 | `check-registry-coverage.py --revision 1fac4195…` | PASS 140/140, rc 0 |
| 2 | `check-knowledge-header.py --revision 1fac4195…` | PASS 104/104 clean+complete, 0 findings, rc 0; new entry `problems: []` |
| 3 | `check-limine-pins.py --selftest` | PASS 15/15, rc 0 |
| 4 | `sources-census.sh validate` | rc 0; 52 W04 (same as the r87 close); one non-W04 line, the `tsukuroi ok` row |
| 5 | entry `.md` ↔ `.json` row agreement | AGREE: 9 rows each, ids PW1–PW9, 0 diffs on statement/source/quote/host_value |
| 6 | entry citations vs `corpus/SOURCES.md` | PASS: cites only S355–S359; each exists, 11 cells, status `mined`, `used-by corpus/knowledge/limine-pin-writers-r88.md` |
| 7 | quotes vs pinned snapshots | PASS 8/8 quoted rows verbatim inside the cited raw line ranges (PW8 has no quote, `—`); `sha256sum -c SHA256SUMS` 14/14 OK rc 0 |
| 8 | registry row `limine-pin-battery-r88` vs the tool | ACCURATE (flags, 38 families/4 cases, exit 0/1/2, selftest 14 cases) |
| 9 | registry row `battery-discrimination-r88` vs the tool | ACCURATE on every exit path I could exercise; usage column omits `--roster` (convention, see O-2) |
| 10 | frozen instruments unchanged since the freeze | PASS: counter `7d2073df…` = manifest, roster `1e2dcc8b…` = manifest, `git diff 01b2a9b0 1fac4195` on them empty |
| 11 | counter self-verification promised by its docstring | **FAIL — defect L-1**, patch supplied |
| 12 | battery selftest lie wrappers | PASS as claimed (8 lies read unmet), residual noted as O-1 |
| 13 | host cells of the entry (read-only re-check) | PASS for PW1/PW2/PW5/PW9; PW6/PW8 rest on the committed host receipt (`/boot` unreadable to my account) |

## 1–2. Revision gates (clone at master, no `--branch` override)

```
$ python3 tools/check-registry-coverage.py --revision 1fac4195243e55e7d9d8a2eddd653443d8559bff
{"branch":"master","branch_tip":"1fac4195243e55e7d9d8a2eddd653443d8559bff","counts":{"findings":0,"missing":0,"registered":140,"rows_total":140,"tools_total":140},"findings":[],"revision":"1fac4195243e55e7d9d8a2eddd653443d8559bff","status":"PASS"}
RC=0
```
```
$ python3 tools/check-knowledge-header.py --revision 1fac4195243e55e7d9d8a2eddd653443d8559bff
{'branch': 'master', 'branch_tip': '1fac4195243e55e7d9d8a2eddd653443d8559bff', 'clean_count': 104, 'complete_count': 104, 'finding_count': 0, 'findings': []}
[{'lines': {'recheck': 4, 'source': 3, 'verified-at': 5}, 'path': 'corpus/knowledge/limine-pin-writers-r88.md', 'problems': []}]
RC=0
```
140 rows / 140 tools is +2 over r87's 138/138 and +1 entry over r87's 103 — both new rows and the new entry are inside the gates' counts, not merely beside them.

## 3. Gate selftest

```
ok               PASS rc=0 [(2, 'OK', 'none')]
upper            PASS rc=0 [(2, 'OK', 'none')]
mismatch-panic   PASS rc=1 [(2, 'LP-MISMATCH', 'panic')]
mismatch-prompt  PASS rc=1 [(3, 'LP-MISMATCH', 'prompt')]
first-setting    PASS rc=1 [(4, 'LP-MISMATCH', 'panic')]
secureboot       PASS rc=1 [(3, 'LP-MISMATCH', 'panic')]
comment          PASS rc=0 [(3, 'OK', 'none')]
missing          PASS rc=1 [(2, 'LP-MISSING', 'not-modelled')]
format           PASS rc=1 [(2, 'LP-HASH-FORMAT', 'panic')]
unresolved       PASS rc=2 [(2, 'LP-UNRESOLVED', 'not-modelled')]
wallpaper-skip   PASS rc=1 [(1, 'LP-MISMATCH', 'skip')]
non-path-key     PASS rc=0 []
crlf-blanks      PASS rc=0 [(2, 'OK', 'none')]
traversal        PASS rc=2 [(2, 'LP-UNRESOLVED', 'not-modelled')]
conf-absent      PASS rc=2 []
selftest PASS 15/15
RC=0
```

## 4. Sources census

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
RC=0
53 output lines: 52 `W04` duplicate-url rows + 1 ok row
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
tsukuroi	W04	S038 duplicate url man.archlinux.org/man/access.2 across scopes
```
52 W04 is the same count the r87 close recorded (349 → 354 rows, 52 W04 both ends); the five new S rows add no duplicate URL.

## 5–7. C2 entry: agreement, citations, quotes

- `.md` table: 9 rows; `.json`: 9 objects; ids identical (`PW1..PW9`); after normalising Markdown backticks and JSON quote escaping, `statement`, `source`, `quote`, `host_value` differ on 0 of 9 rows.
- Cited S-ids: `S355 S356 S357 S358 S359` and nothing else; `corpus/SOURCES.md` rows exist with status `mined` and `used-by corpus/knowledge/limine-pin-writers-r88.md`.
- Every quoted row's text is present verbatim inside its cited raw line range of the pinned snapshot: PW1 ConfigReader.java 28-32, PW2 173-177, PW3 LimineManager.java 353, PW4 Utility.java 118-175, PW5 limine-update 16-28, PW6 KernelReader.java 154-213, PW7 Hash.java 60-66, PW9 89-warn-missing-file-hashes 19-25. PW1's four-layer order is verbatim at ConfigReader:29-32 (`loadConfigDir("/usr/share/…") // 1. Lowest priority` … `loadConfigFile(Config.DEFAULT_CONFIG_FILE_PATH); // 4. Highest priority`).
- `sha256sum -c SHA256SUMS` in `.ufo/waves/round-88/before/src/`: 14/14 `OK`, rc 0; the five anchor digests also equal the digests written into `corpus/SOURCES.md` (f1f47c1b…, 96f6b99f…, 2b4b2f03…, 55b7d578…, 9ca543bf…). The `source:` header line's `Gate in corpus/lessons/round-88.md` resolves (1924 bytes, exists).

## 8–9. Registry rows vs the tools' real CLI

`limine-pin-battery-r88` (SKILL.md:5925) — actual argparse matches the row's `--gate/--runs/--work/--json`; `--selftest` exists and is documented in the row's selftest column exactly as the r87 row does.
```
battery: no args            -> usage, RC=2
battery: --help             -> usage + description, RC=0
battery: --gate /nonexistent/gate.py -> families_passed 0/38 verdict unmet failed ALL-PIN-KEYS,…,RC=1
battery: constant-HEALTHY fake gate  -> families_passed 0/38 verdict unmet, RC=1
battery: --selftest         -> 14 cases, "selftest PASS 14/14", RC=0
```
The 14 cases are exactly the row's list: `roster-literal`, `absent`, `constant-healthy`, `non-json`, `constant-degraded`, `reference-gate`, and the eight lies `exit-code, rc-field, line, consequence, status, verdict, entry, panic-line`. `len(FAMILY_ROSTER) == len(FAMILIES) == 38`, `CASES_PER_FAMILY = 4` (tools/limine-pin-battery-r88.py:736-751) — the row's "38 families … all 4 cases" is exact. `FAMILIES differs from FAMILY_ROSTER` → exit 2 (lines 936-938) as claimed.

`battery-discrimination-r88` (SKILL.md:5926) — exits:
```
counter: no args                     -> argparse required --battery, RC=2
counter: --help                      -> RC=0
counter: --battery /nonexistent/b.py -> void: battery not found: /nonexistent/b.py, RC=2
counter: --roster <copy with a gate file absent/digest-differs> -> void: roster digest/label mismatch: … , RC=2
```
`bwrap` is present (`/usr/bin/bwrap`, bubblewrap 0.13.1) so the isolation arm is exercisable here.

## L-1 (defect, medium): the frozen counter does not verify its own freeze, though its docstring and the C1 kill rule say it voids when they differ

- Claim: `tools/battery-discrimination-r88.py:11-12` — "void (exit 2) if this file or any roster file differs from `.ufo/waves/round-88/before/freeze-manifest.sha256` / the roster digests". The round-88 declaration's C1 kill rule repeats it ("void if the counter or any roster file differs from `…/freeze-manifest.sha256`").
- Code: `grep -n "freeze\|manifest" tools/battery-discrimination-r88.py` matches only line 12 (the docstring). `load_roster()` (lines 51-62) compares each gate file with the digest stored *inside* `roster-r88.json`; neither the counter's own bytes nor `roster-r88.json` is compared with the manifest.
- Demonstrated: a byte-copy of the frozen roster directory with one label flipped (`N-g01-loose-key` `unmet`→`met`, gate digests untouched) was accepted and run:
```
$ python3 tools/battery-discrimination-r88.py --battery tools/limine-pin-battery-r88.py --runs 1 --jobs 4 --scratch $S/work --roster $S/rosterflip/roster-r88.json
run 1 positives 3/4 negatives 44/44 failures N-g01-loose-key
verdict unmet
RC=1
```
The receipt records `roster_sha256 7ae2370a613e2d75ff332d17e2d4c4629cd0afb0ffd339db3f8c193dbea8330e` against the manifest's `1e2dcc8bab709b99dfdb62fad1b123fe3cd3fab4fc542e782b8a20489a95ae8c`, so the tamper is visible only to an auditor who diffs digests; the instrument itself reads it as an ordinary `unmet`.
- Bound on severity: the frozen bytes at the tip are correct (counter `7d2073df…`, roster `1e2dcc8b…`, both equal to the manifest; `git diff 01b2a9b0 1fac4195` on them is empty) and every receipt carries `counter_sha256`/`roster_sha256`/`battery_sha256`, so the committed C1 receipts stay auditable. What is missing is refusal at runtime.
- Proposed patch (NOT applied; written here for the L1): `counter-freeze-selfcheck.patch` beside this report — read `freeze-manifest.sha256`, check the counter plus `roster-r88.json` plus every frozen roster gate, print `void: freeze mismatch: <rel>` and return 2 before any gate runs. The candidate battery stays outside the check on purpose (it is the object under test, pinned only by the receipt's `battery_sha256`).

## O-1 (observation, no false claim): the selftest's eight lies assert the verdict only, not the family that must catch each lie

`tools/limine-pin-battery-r88.py:916-920` asserts `r["verdict"] == "unmet"` per lie. The observed `families_passed` per lie were 2, 2, 2, 31, 36, 35, 2, 25 — i.e. a lie can be caught by any family (lie-consequence breaks 7), and a lie wrapper would still pass if it broke an unrelated family. R87-R1 asked for "freezes the roster literal and adds one-field lie controls"; both are present (roster literal asserted at line 889), its second half ("mutants that … ignore rc, consequence or line survive it") is now partly answered but not pinned to the named family. The registry row claims only "unmet", so nothing false is claimed; the real per-clause discrimination is carried by the 45-gate roster, not by the selftest.

## O-2 (observation, calibrated as convention): usage-column flag lists are not complete fleet-wide

The counter row omits `--roster` (exists, tools/battery-discrimination-r88.py:135) and the battery row omits `--selftest`. A scan of the operative registry rows against each named tool's `add_argument("--…")` set: 200 of 1868 rows omit at least one non-shared operating flag (`boot-chain` ×32 `--registry-from`, `recheck-commands` ×32 `--forbid`, `seat-scope` `--worktree`, `check-knowledge-refs-r68` `--lane`, `resume-gate-battery-r84..86` `--base`, …), and 52 more omit only `--selftest`/`--branch`/`--repo`. So the usage column is a primary-invocation line, not a flag census, and these two rows follow it — reported as calibration, not as a defect. What the coverage gate does enforce (exists-in-tools, selftest-flag presence) is unaffected: it reads PASS 140/140.

## O-3 (observation): a nonexistent `--gate` path reads `unmet` (rc 1), not `could-not-evaluate` (rc 2)

`families_passed 0/38 verdict unmet` for `/nonexistent/gate.py`. The row does not claim otherwise, and the direction is safe (a gate that cannot run can only produce false negatives), matching the r87 K1 "gate absent → 0/22" control.

## 13. Host cells of the entry, re-read read-only from my account

```
44207b64…  /etc/limine-entry-tool.conf        (PW1; = the pinned 1.40.0 file)
55b7d578…  /usr/bin/limine-update             (PW5; = the pinned 1.40.0 file)
/etc/default/limine:8:ENABLE_UKI=yes          (PW9); no ENABLE_VERIFICATION line (PW1)
/usr/share/limine-entry-tool.d: No such file or directory; /etc/limine-entry-tool.d/: resume.conf only  (PW1)
b2sum present (/usr/bin/b2sum, "b2sum 0.8.0")  (PW2)
/boot/limine.conf: Permission denied (os error 13)  -> pins not re-read by me
```
`/boot/limine.conf` is root-only, so PW6/PW8's line numbers and stale-pin values rest on the committed L1 receipt `.ufo/waves/round-88/before/host/receipt.txt` (lines 30/38 `b990d8c6…`/`a68c281d…`, history 50/56/64, journal `Updated: /boot/limine.conf` at 19:27:27 and 20:27:30, `/boot` b2sum list cmp-identical before/after). I did not write anything to `/boot`, `/etc`, `/usr`, `/var` or `/sys`, and ran no `limine*`, `objcopy`, `mkinitcpio`, `bootctl` or pacman binary. I did not run the C1 counting command (three 48-gate runs) — that is the C1 seats' measurement, not this seat's.

## O-4 (observation, not mine): an uncommitted lane worktree change was present while I measured

`git -C …/tsukuroi-shokunin status --porcelain` at 21:08 shows ` M corpus/README.md` (+17 lines, a "## Round 88 — Limine pin writers; battery r88" section) alongside the round-88 `.ufo/waves/round-88/` untracked entries. I did not write it and did not touch it. It does not affect any check here: both revision gates ran with `--revision 1fac4195…` (committed bytes, not the worktree) and `corpus/SOURCES.md`, which the census reads, is unmodified.

## Refused / not done

- No lane file edited; the one defect is reported with `file:line` and a patch under this wave dir for the L1 to decide.
- Nothing committed; the clone was the only git object, `git -C $S/lane rev-parse master` = `1fac4195…`; no mutating git/jj command was run in the lane.
- No subagent, no message to `agent://all`, no model chosen.
