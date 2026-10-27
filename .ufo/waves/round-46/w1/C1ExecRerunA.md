VERDICT: supports

# C1-1 — C1 counter re-run A (C1ExecRerunA)

Scope: hash-pin the frozen C1 counter, run it through `tools/run-receipt.py` at IMPL
(a4477049) and BASE (2042117c), and compare the IMPL `census_sha256` with what
`bash tools/tsukuroi-census.sh --identity` prints from the lane. No lane file was edited;
receipts only under `.ufo/waves/round-46/w1/C1ExecRerunA/`.

## 1. Frozen-counter hash pin — MATCH

```
$ git -C <lane> show 72cc26096bc24d765a7cd70d4b4d9471cb854001:tools/score-census-identity-r46.py | sha256sum
7c406eb5f4ba1f6265649f7102e7376882483180c161a66abc68e08cad9524ba  -
$ sha256sum <lane>/tools/score-census-identity-r46.py
7c406eb5f4ba1f6265649f7102e7376882483180c161a66abc68e08cad9524ba  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-census-identity-r46.py
```
The frozen (72cc2609) bytes equal the declared `7c406eb5…d9524ba` and equal the working
file byte-for-byte. Both receipts independently record the same pin in their header:
`"tool_sha256": "7c406eb5f4ba1f6265649f7102e7376882483180c161a66abc68e08cad9524ba"`
(`c1-impl.jsonl:1`, `c1-base.jsonl:1`), with `tool_revision` resolved to
`72cc26096bc24d765a7cd70d4b4d9471cb854001` in both.
Lane HEAD at run time: `a44770491eb5ca15ce9f8b3207309d1af683ffaf` (`git rev-parse HEAD`).

## 2. Receipts

| receipt | revision | exit | sha256 of receipt file |
|---|---|---|---|
| `.ufo/waves/round-46/w1/C1ExecRerunA/c1-impl.jsonl` | a44770491eb5ca15ce9f8b3207309d1af683ffaf | 0 | 274efd2e5439494df634ea3b697cc4bac2f7607d400de8dc1abc1da10c7898e8 |
| `.ufo/waves/round-46/w1/C1ExecRerunA/c1-base.jsonl` | 2042117cfb724170772f4c128cc2ddba0b61d817 | 1 | 0f1ef542dc7860a616caab8b9306b62da22253d18a709026f0958149a4977f11 |

Command (identical shape both times; TMPDIR=/fast/scratch/hyaku/tsukuroi-r46/C1ExecRerunA):

```
python3 <lane>/tools/run-receipt.py --revision <REV> --tool-revision 72cc26096bc24d765a7cd70d4b4d9471cb854001 \
  --out <lane>/.ufo/waves/round-46/w1/C1ExecRerunA/c1-<impl|base>.jsonl \
  -- tools/score-census-identity-r46.py --revision '{rev}' --scratch /fast/scratch/hyaku/tsukuroi-r46/C1ExecRerunA/s
```
argv recorded in each header pins both the revision and that scratch path; the counter's own
`revision` field echoes the full hash. The two runs were serialised (one C1 counter at a time);
scratch `s/` was left empty by the counter's own subtree removal.

## 3. Every leg, both revisions

Predicate (from both receipts, `predicate` field): `identity_ok == 1 and tracks_ok == 1 and
symlink_ok == 1 and unverifiable_ok == 1 and cli_ok == 1 and nowrite_ok == 1 and
selftest_pass == 1 and selftest_r46 >= 4`.

### IMPL a4477049 — `verdict: PASS` (`c1-impl.jsonl:2`)

| leg | value |
|---|---|
| identity_ok | 1 (rc 0; one `TSUKUROI_CENSUS_IDENTITY` line, `verified=yes`) |
| tracks_ok | 1 (rc 0; copy + one appended line reports `sha256=3596e928…690d73 bytes=209230 lines=3600`, i.e. its own bytes, not the constant) |
| symlink_ok | 1 (rc 0; symlink invocation prints the target's `sha256=d925839c…112cfa`) |
| unverifiable_ok | 1 (all three cases rc 0 and `sha256=unverifiable md5=unverifiable bytes=unverifiable lines=unverifiable verified=no`: stdin, and two replaced-after-open variants) |
| cli_ok | 1 (`cli: [true,true,true,true]`; selftest label `--identity with another flag exits 2` observed exit 2) |
| nowrite_ok | 1 |
| selftest_pass | 1 (`TSUKUROI_CENSUS_SELFTEST: PASS (160 cases, 160 passed, 0 failed)`) |
| selftest_r46 | 6 (all six `(R46-C1)` labels PASS: one-line digests, appended-copy own bytes, symlink target, stdin unverifiable, replaced-after-open unverifiable, `--identity`+flag exit 2) |
| census_sha256 | `d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa` |

### BASE 2042117c — `verdict: FAIL` (`c1-base.jsonl:2`)

| leg | value |
|---|---|
| identity_ok | 0 (`tsukuroi-census: unknown argument: --identity`, rc 2, empty stdout) |
| tracks_ok | 0 (same rc 2 refusal) |
| symlink_ok | 0 (same rc 2 refusal) |
| unverifiable_ok | 0 (stdin case rc 1 `bash: line 455: BASH_SOURCE[0]: unbound variable`; other two rc 2 refusal — no `unverifiable` line at all) |
| cli_ok | 0 (`cli: [true,true,false,true]`) |
| nowrite_ok | 1 |
| selftest_pass | 1 (`TSUKUROI_CENSUS_SELFTEST: PASS (154 cases, 154 passed, 0 failed)`) — base selftest is identity-free, so it passes without the feature |
| selftest_r46 | 0 (no `(R46-C1)` labels exist at base) |
| census_sha256 | `237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc` |

So the counter separates the revisions exactly as the claim requires: one leg-by-leg FAIL at
base, one clean PASS at IMPL, and the base census lacks `--identity` entirely.

## 4. IMPL census_sha256 vs the live `--identity` line — MATCH

```
$ cd /fast/scratch/hyaku/tsukuroi-r46/C1ExecRerunA && bash <lane>/tools/tsukuroi-census.sh --identity
TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa md5=db08a606ce128da3839457372e91e220 bytes=209208 lines=3598 planes=packages,systemd,drivers,journal,update-safety,oom exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED verified=yes
RC=0
```
Yes: the lane run prints exactly the counter's IMPL `census_sha256`
`d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa`, and it is the true
digest of the executed bytes:

```
$ sha256sum <lane>/tools/tsukuroi-census.sh
d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa  …/tools/tsukuroi-census.sh
$ git -C <lane> show a44770491eb5ca15ce9f8b3207309d1af683ffaf:tools/tsukuroi-census.sh | sha256sum
d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa  -
$ md5sum <lane>/tools/tsukuroi-census.sh   # -> db08a606ce128da3839457372e91e220, matches identity md5
$ wc -lc <lane>/tools/tsukuroi-census.sh   # -> 3598 209208, matches identity lines/bytes
```
Working tree, IMPL object and the printed identity all agree, so the line names the bytes bash
actually executes here (not a constant), and `verified=yes` is honest.

Direct refusal check at IMPL (read-only, no counter):

```
$ bash <lane>/tools/tsukuroi-census.sh --identity --sample 1
tsukuroi-census: --identity takes no other argument
… RC=2
$ bash <lane>/tools/tsukuroi-census.sh --identity extra
tsukuroi-census: unknown argument: extra
… RC2=2
```

## 5. Observation (does not change the verdict)

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-46/before/c1-before-base.jsonl`
(recorded by another seat at 05:25:40Z) holds the same base revision and the same counter pin,
but its base selftest line reads `FAIL (154 cases, 153 passed, 1 failed)` and `selftest_pass: 0`,
while my base receipt reads `PASS (154 cases, 154 passed, 0 failed)` and `selftest_pass: 1`.
Both runs executed under load from concurrent seats; the base census selftest therefore has at
least one load-sensitive case. It cannot affect the C1 predicate outcome — at base
identity/tracks/symlink/unverifiable/cli/selftest_r46 are all 0 for a structural reason (no
`--identity`), so the base verdict is FAIL with or without that case. Flagged as a stability
caveat for any seat scoring base, not as a defect in the IMPL path (IMPL: 160/160 PASS, 6/6
`(R46-C1)`).

## 6. Hygiene

- No lane tracked file written, no git/jj mutation, no host mutation, no sudo, no service or
  sysfs write, no scrub/replace command. Install ledger: nothing installed.
- Writes: the two receipts and this report only. Scratch
  `/fast/scratch/hyaku/tsukuroi-r46/C1ExecRerunA/` removed after copying the receipts.
- Not done: no C1 counter run at any revision other than the two assigned; no kill-rule
  counter (`score-census-readers-r45`, `score-scrub-arm-r44`, …) was invoked — that is outside
  this item, and an unrun check has not passed.
