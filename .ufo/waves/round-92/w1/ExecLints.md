# ExecLints — lane gates and selftests at the round-92 tip

Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (master, jj-colocated).
Freeze commit: `da99b2f4bc442e5154a6c1da7350891c11ee7cb1`. The lane advanced four times **while this seat
was running** (L1's own commits): `495a9f6c` 01:54, `429fd1a3` 02:08, `689623fd` 02:17 (A3 gate hardening —
gate and battery bytes changed, manifest regenerated), `e9fce481` 02:24 (registry row fix), `22b5bc10` 02:29
(wave evidence). Every receipt below names the revision and the instrument digest it was taken against.

Axes walked: (A) instrument truth at the tip, (B) registry/corpus freshness, (C) receipts without touching
the lane (read-only; all writes under `.ufo/waves/round-92/w1/ExecLints/` and `/fast/scratch/hyaku/tsukuroi-r92/ExecLints/`).

## Instrument identity (read this before the tallies)

| instrument | freeze `da99b2f4` blob | tip `22b5bc10` blob / on-disk |
|---|---|---|
| `tools/check-limine-pins.py` | `af90ae63…39839c123` | **`35c1088b7bacb31dfe92e087416136271b6ddef9aebf8fb36727696af8d5c87f`** |
| `tools/limine-pin-battery-r92.py` | `fde864ea…488542b166` | **`aef3392516aabf2942192cd55d637560b6276bc98b8bf8796f33bd464d02614f`** |
| `tools/limine-pin-battery-r91.py` | `655ee8f3…` | `655ee8f3d0942e958cc853deb2d16abcd2d16ae2823ca6548f2a53991b4901b9` (unchanged) |

A3 (`689623fd`, 02:17) rewrote the gate and the r92 battery and regenerated
`.ufo/waves/round-92/before/freeze-manifest.sha256`, which is now **36 lines**, not the 30 the seat brief
states; its first three lines name the tip digests above, not the freeze digests. `sha256sum -c` from the
lane root at the tip reports `SKILL.md` and `.ufo/plans/round-92.md` as FAILED (they were edited after the
manifest's last regeneration) and every other line OK. Receipt: `instrument-digests.txt`,
`sha256sum -c .ufo/waves/round-92/before/freeze-manifest.sha256`.

## 1. Gate selftest (`tools/check-limine-pins.py --selftest`)

`python3 tools/check-limine-pins.py --selftest` → **rc 0, `selftest PASS 37/37`** at the tip digest
`35c1088b…` (receipt `gate-selftest-tip.log`); the identical tally was reproduced earlier against the
freeze-descended bytes `af90ae63…` (receipt `gate-selftest.log`). 37 scored rows = 24 named r90 fixtures +
`conf-absent` (25) + 12 round-92 rows:

* V1/U1 (5): `v1-entry-body`, `v1-body-invisible`, `v1-body-invisible-era-b`, `u1-unverified`,
  `u1-pin-not-listed`.
* Era (6): `era-a-first-entry`, `era-b-first-entry`, `era-b-global-key`, `era-default`, `era-a-measured`,
  `era-b-measured`.
* `version-parser` (1).

The seat brief's "three new V1/U1 and four era rows" does not match the instrument: the gate carries **5**
V1/U1 and **6** era rows, and the battery roster carries **7** new `ERA-*` families (82 r91 + 7 = 89).
Recorded as-shipped, not as-described.

Gate interface probed directly at the tip (receipt `gate-version-probe.txt`): schema `tsukuroi-limine-pins-v3`,
`limine_version` echoed, `visibility_era` `pre-12.9.5` for `12.9.4` / `12.9.5+` for `12.9.5` and `12.9.6`,
default `12.9.4` → `pre-12.9.5`, and rc **64** for `12.9`, `12.9.5.1`, `13`, `v12.9.4`, `""`, `abc`.

## 2. Battery selftest (`tools/limine-pin-battery-r92.py --selftest --reference tools/check-limine-pins.py`)

Command as specified, `TMPDIR=/fast/scratch/hyaku/tsukuroi-r92/ExecLints`.
**`selftest PASS 18/18`, rc 0.** Receipt `battery-selftest.log` (19 lines) with the full leg table:

| leg | result | families_passed |
|---|---|---|
| roster-literal | PASS | 89 |
| absent | PASS | 0 |
| constant-healthy | PASS | 0 |
| non-json | PASS | 0 |
| constant-degraded | PASS | 0 |
| reference-gate | PASS | 89 |
| lie-exit-code | PASS | 3 |
| lie-rc-field | PASS | 3 |
| lie-line | PASS | 3 |
| lie-consequence | PASS | 73 |
| lie-status | PASS | 68 |
| lie-verdict | PASS | 84 |
| lie-entry | PASS | 3 |
| lie-panic-line | PASS | 66 |
| lie-panic-value | PASS | 66 |
| lie-on-panic | PASS | 2 |
| lie-bad-resource | PASS | 82 |
| lie-missing-panic | PASS | 71 |

No FAIL. The reference leg ran all 89 families × 4 cases through the ISOLATION launcher (a private gate
copy + `bwrap --unshare-all --clearenv` + `python3 -I`); the twelve lie wrappers each drop at least one
family.

The table above is the first run. **A second, byte-stable run at the tip replaced it as the canonical
receipt** (`battery-selftest-tip.log`, `battery-selftest-tip.env`): run 02:28:32 → 02:36:40, rc 0,
`selftest PASS 18/18`, with the gate digest `35c1088b…` and the battery digest `aef33925…` identical at
run-start and run-end (HEAD `e9fce481` → `22b5bc10`, no tool change between them). Its leg table is the same
18 PASS rows; the two randomized lie legs that moved are `lie-consequence` 75 (was 73), `lie-panic-line` 67
(was 66) and `lie-bad-resource` 83 (was 82) — all still short of 89, which is all that leg asserts. The
first run, started before A3 rewrote the gate at 02:17, cannot prove its per-leg bytes were uniform, so the
tip run is the one to score.

Bonus leg run under the same launcher: `--usage-check --gate tools/check-limine-pins.py` → **met 11/11**
(`battery-usage-check.json`): `12.9`, `abc`, `12.9.6.1`, `""`, a 5000-digit version → 64; `12.9.4`,
`12.9.5`, `13.0.0`, `12.09.4`, `00.00.00`, omitted → 0.

## 3. Registry and corpus checkers

| checker | at freeze `da99b2f4` | at `495a9f6c` / `429fd1a3` | at tip `e9fce481` / `22b5bc10` |
|---|---|---|---|
| `check-registry-coverage.py --revision REV` | **rc 1 FAIL**, 1 finding | **rc 2 CANNOT_EVALUATE**, `E-REGISTRY-TABLE malformed registry row at line 5931` | **rc 0 PASS**, findings 0, registered 145 / rows 145 / tools 145 |
| `check-knowledge-header.py --revision REV` | rc 0 PASS, clean 108, complete 108, findings 0 | — | rc 0 PASS, clean 108, complete 108, findings 0 |
| `check-knowledge-refs-r68.py --revision REV` | rc 0 PASS, notes 108, dangling 0, findings 0 | — | rc 0 PASS, notes 108, dangling 0, findings 0 |

Freeze finding (`registry-coverage-freeze.json`): `{"id":"REGISTRY-ROW-MISSING","site":"tools/limine-pin-battery-r92.py","detail":"no operative row names this regular tools/ file"}`, counts `registered 144 / rows 144 / tools 145`. The r92 battery was committed at the freeze with no operative registry row.

Intermediate break (`registry-coverage-495a9f6c.json`, `registry-coverage-429fd1a3.json`): `495a9f6c` appended
the row but with **6 cells** instead of the registry's 8, so the whole table became unparseable and the gate
went from FAIL to CANNOT_EVALUATE. Reproduced in a scratch clone of the lane's `tools/` + `SKILL.md`
(`/fast/scratch/hyaku/tsukuroi-r92/ExecLints/fixprobe`, commits `bf2dfde` → `05b755c`): the failure is exactly
"malformed registry row at line 5931", and adding the two missing cells (`Write scope`, `Owner`) turns it into
PASS 145/145 with 0 findings. `e9fce481` applied that repair; the tip row now has 8 cells and coverage passes.
The instrument's own selftest is green throughout: `check-registry-coverage.py --selftest` → `PASS (23 cases, 23 passed, 0 failed)`.

**Freshness residue at the tip:** the r92 battery row's Pinned-values cell still cites the *freeze* digest
`fde864ea…488542b166`, while the committed instrument at `22b5bc10` hashes to `aef33925…d02614f` and the
regenerated manifest agrees with the instrument, not with the row. The row is green on the checker's
(path, verdict-code, selftest-flag) contract and stale on its digest.

## 4. Line endings and source census

* `python3 tools/check-line-endings-r64.py --check` → **rc 0**, `CHECK_LINE_ENDINGS: PASS (471 file(s) checked, 0 violation(s))`, `29572 allow-listed .ufo path(s) skipped` (`line-endings-tip.log`, `line-endings.log`).
* `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → **rc 0**, **381 `S` rows** (`grep -cE '^\| S[0-9]+ ' corpus/SOURCES.md` = 381; 383 pipe rows = header + separator + 381), 57 diagnostic lines: 55 × `W04 duplicate url … across scopes`, 1 × `W01 tierC mined` (S381), 1 × `ok`. Warnings only, no `E` rows (`census-tip.log`, `census.log`).

## 5. Does the `limine-pins` registry row still match the gate?

**No.** Operative row `SKILL.md:5923` (unchanged at the tip, verified on `22b5bc10`) is still the round-87
row, and the real gate has moved three rounds past it:

| cell | row says | gate at the tip |
|---|---|---|
| Entry command | `--conf/--esp/--secure-boot-enforced` (or `--live`) | also `--tpm-present {0,1}` (r90) and `--limine-version X.Y.Z` (r92, default `12.9.4`) — verified by `--help` and by probe |
| Verdict map | `0 HEALTHY; 1 DEGRADED (LP-MISMATCH, LP-MISSING, LP-HASH-FORMAT); 2 …; 64 usage` | rc 1 also covers `LP-BAD-RESOURCE` (selftest row `bad-resource` rc 1); 64 is the malformed-`--limine-version` refusal, never a silent default |
| Self-test | `--selftest` (15 fixtures, …) | same spelling, **37** fixtures, asserting per-pin `(line, status, consequence)` plus `on_panic` and `unverified_image_lines` |
| Pinned values | R1-R7 (r87 docstring), sources `S350-S353` | R1-R7, R9, R10 + V1/U1 (r91) + V2 era split (r92), frozen in the `limine-pin-battery-r92` docstring; schema `tsukuroi-limine-pins-v3` with `limine_version`/`visibility_era`; sources `S350-S353, S361, S362, S374-S376, S379, S380` (S381 community lead only) |

The append-only corrections at `SKILL.md:5933` (R90) and `SKILL.md:6318` (R92) carry these deltas in prose,
but the machine-read row cells do not. A second row may not be appended — the checker emits
`REGISTRY-ROW-DUPLICATE` for two rows naming one tool — so the row text itself must be replaced.

**Proposed exact one-line edit for `SKILL.md:5923`** (verified: applied to the scratch clone, the registry
gate reads PASS 145/145 with 0 findings and `--audit-live-map` PASS 0; commit `2bae8c5`, receipt
`registry-repair-probe.json`):

```
| limine-pins | gate | `python3 tools/check-limine-pins.py --conf <FILE> --esp <DIR> [--secure-boot-enforced {0,1}] [--tpm-present {0,1}] [--limine-version X.Y.Z]` (default `12.9.4`, the host package; or `sudo python3 tools/check-limine-pins.py --live`, read-only; receipts `.ufo/waves/round-87/after/live-receipt*.txt`) | 0 HEALTHY; 1 DEGRADED (any LP-MISMATCH, LP-MISSING, LP-HASH-FORMAT or LP-BAD-RESOURCE pin); 2 CANNOT-EVALUATE (conf unreadable, or any LP-UNRESOLVED pin, including a path that leaves the ESP root); 64 usage (a `--limine-version` outside `X.Y.Z` is refused, never defaulted) | `python3 tools/check-limine-pins.py --selftest` (37 fixtures, asserting rc, the sorted per-pin (line, status, consequence), `on_panic` and `unverified_image_lines`, including the V1/U1 and era rows and the version-parser assertion; exit 0 PASS / 1 FAIL) | Limine v12.9.4 rules R1-R7, R9, R10 plus the r91 V1/U1 and the r92 V2 era split (before 12.9.5 vs from 12.9.5) frozen in the `limine-pin-battery-r92` docstring; output schema `tsukuroi-limine-pins-v3` with `limine_version` and `visibility_era`; sources S350-S353, S361, S362, S374-S376 (the r91 rule set) and S379, S380 (the v12.9.6 in-place parse the era split rests on), with S381 a community lead only; pin keys path, kernel_path, image_path, module_path, dtb_path, global_dtb, wallpaper, term_font; BLAKE2b-512 over the raw stored bytes, gzip not decompressed | read-only: conf and ESP files opened read-only; selftest private mkdtemp under `$TMPDIR`; never writes `/boot` | tsukuroi |
```

Second one-line edit, same class, for the row the freeze lacked: `SKILL.md:5931` already has 8 cells at the
tip, but its digest must move from `fde864ea…` to `aef33925…` (the committed `22b5bc10` blob) if the row is to
mean anything after A3.

Note on source traceability: the gate docstring names `S350-S353, S361, S362, S374-S376` and describes the
V2 rule by raw line numbers of **v12.9.6** `common/lib/config.c` (328-330, 362-365, 666-668, 733+) **without
naming S379 or S380**, the pinned sources those lines come from (`corpus/SOURCES.md:389-390`). The rule is
cited; its source id is not.

## Findings

1. **F1 (fixed at the tip, was real at the freeze).** `da99b2f4` commits `tools/limine-pin-battery-r92.py` with no operative `SKILL.md` registry row → `check-registry-coverage.py` rc 1, `REGISTRY-ROW-MISSING`.
2. **F2 (fixed at the tip, was a regression for two commits).** The row appended at `495a9f6c` has 6 cells instead of 8, which made the whole operative table unparseable: rc 2 `E-REGISTRY-TABLE` at `495a9f6c` and `429fd1a3`. `e9fce481` repaired it; `22b5bc10` passes.
3. **F3 (open).** `SKILL.md:5923` (`limine-pins`) is stale on the entry command, the verdict map, the fixture count and the source list; the append-only corrections carry the deltas but the row cells do not. Exact replacement in §5, verified green in a scratch clone.
4. **F4 (open).** The battery row's Pinned-values digest (`fde864ea…`) is the freeze digest; the committed instrument is `aef33925…`. Freshness defect inside a row the checker accepts.
5. **F5 (open, documentation).** The gate's V2 rule cites v12.9.6 raw lines without naming `S379`/`S380`.
6. **F6 (brief vs reality).** The seat brief's instrument digests and "30-line manifest" describe the freeze; at the tip the gate and battery digests are `35c1088b…` / `aef33925…` and the manifest is 36 lines. Green tallies above are labelled with the digest they were taken against.

## Retained evidence (all under `.ufo/waves/round-92/w1/ExecLints/`)

`instrument-digests.txt`, `gate-selftest.log`, `gate-selftest-tip.log`, `battery-selftest.log`,
`battery-selftest-tip.env`, `battery-selftest-tip.log`, `battery-usage-check.json`,
`registry-coverage-freeze.json`, `registry-coverage-495a9f6c.json`, `registry-coverage-429fd1a3.json`,
`registry-coverage-tip.json`, `registry-coverage-selftest.log`, `registry-repair-probe.json`,
`fixprobe-log.txt`, `knowledge-header-freeze.json`, `knowledge-header-head.json`, `knowledge-header-tip.json`,
`knowledge-refs-freeze.json`, `knowledge-refs-head.json`, `knowledge-refs-tip.json`, `line-endings.log`,
`line-endings-tip.log`, `census.log`, `census-tip.log`, `gate-version-probe.txt`, `limine.conf`.

Scratch (`/fast/scratch/hyaku/tsukuroi-r92/ExecLints/`) holds the gate probe fixtures and the `fixprobe`
clone (three commits: `bf2dfde` lane-as-pushed, `05b755c` +2 cells → PASS, `2bae8c5` proposed `limine-pins`
row → PASS); it is deleted on exit as the seat rules require. No tool was installed or upgraded; no
`pacman`, `sudo`, git or jj mutation ran in the lane; the only git writes were `init/add/commit` inside the
scratch clone, after asserting `git rev-parse --show-toplevel` equals that clone.

## Verdict

Supports **C1/C2 instrument integrity at the tip**: the gate selftest reads PASS 37/37 and the r92 battery
selftest PASS 18/18 (roster-literal 89, five negative legs 0, reference-gate 89, twelve lie legs unmet) on
the current bytes `35c1088b…`/`aef33925…`; the five corpus checkers read PASS at the tip (registry 145/145,
knowledge header 0 findings, refs 0 dangling, line endings 471/0, census rc 0 with 381 rows), with the
freeze-time registry FAIL and the two-commit `E-REGISTRY-TABLE` break recorded and since repaired — while
falsifying that the `limine-pins` registry row still describes the gate it governs (F3) and that the battery
row's pinned digest is current (F4). Receipts: `gate-selftest-tip.log`, `battery-selftest.log`,
`registry-coverage-{freeze,495a9f6c,429fd1a3,tip}.json`, `registry-repair-probe.json`,
`knowledge-{header,refs}-tip.json`, `line-endings-tip.log`, `census-tip.log`, `gate-version-probe.txt`.
