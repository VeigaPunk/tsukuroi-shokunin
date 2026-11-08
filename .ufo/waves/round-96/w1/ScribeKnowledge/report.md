# ScribeKnowledge — round 96, wave w1

Seat: `ScribeKnowledge` (scribe; leaf member, no dispatch).
Scope: draft the round's knowledge entry (prose only) as
`.ufo/waves/round-96/w1/ScribeKnowledge/knowledge-draft.md`, with receipts under
`.ufo/waves/round-96/w1/ScribeKnowledge/receipts/`.
Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, branch `master`, jj-colocated.
`git rev-parse HEAD` at the time of the measurements: **`b0bf1be96058fc79e84d0ae4f5da7e3ff72c892e`**
(the first commit that carried the r96 instruments), later **`59cbfe2f4b96a73c2697cf81eb989e1d72e276fd`**
(the C2-repair / S390 commit the L1 landed while this seat worked). No mutating git or jj command
was run; no lane file was edited.

## Commands run (exact)

All runs were made from the lane root with an explicit scratch work dir; every scratch artefact
was copied into `receipts/` and the scratch tree was deleted afterwards.

```sh
# 1. roster delta + the four-component class's prior sampling (own-work parser)
python3 receipts/roster_diff.py                       # -> receipts/roster-diff.txt

# 2. the round's counting command, three runs, landed gate
python3 tools/limine-pin-battery-r96.py --gate tools/check-limine-pins.py --runs 3 \
    --work <scratch>/r3-landed --json <scratch>/r3-landed.json
#    -> receipts/r3-landed.json
python3 .ufo/waves/round-95/before/controls/count-runs.py <scratch>/r3-landed.json \
    --family EXPLICIT-VERSION-ECHO --family EXPLICIT-VERSION-ERA \
    --family REFUSAL-VERSIONS-9DIGIT-Y --family EXTRA-COMPONENT
#    -> receipts/count-runs-landed.json

# 3. the four frozen bends, three runs each (receipts/run3.sh, receipts/r3-N0*.json)
python3 tools/limine-pin-battery-r96.py --gate <bend> --runs 3 --work <scratch> --json <out>

# 4. the r95 do-nothing battery (blindness control), three runs each
#    (receipts/run3-dn.sh, receipts/dn3-*.json)
python3 .ufo/waves/round-96/before/controls/do-nothing-battery-r95.py --gate <gate> --runs 3 \
    --work <scratch> --json <out>

# 5. gate metadata probe (own-work; explicit flag -> echo / source / era)
python3 receipts/probe_gate.py                        # -> receipts/gate-metadata-probe.json

# 6. gate limit probe (own-work; unsampled shapes, cap in every position)
python3 receipts/probe_limits.py                      # -> receipts/gate-limit-probe.json

# 7. three own-work era-rule mutants of the gate (one clause each)
python3 receipts/make_mutants.py                      # -> receipts/mutants/M-*.py (+ .clause.txt)
sh receipts/run_mutants.sh                            # -> receipts/mut-M-*.json

# 8. gate selftest
python3 tools/check-limine-pins.py --selftest        # -> "selftest PASS 39/39"

# 9. source re-opens (read-only HTTP GET into scratch)
curl -sS -o s390-page.html 'https://docs.python.org/3/library/sys.html#sys.int_info.default_max_str_digits'
curl -sSL -o s389-page.html 'https://docs.python.org/3.15/library/stdtypes.html#integer-string-conversion-length-limitation'
curl -sS -o S382-config.c 'https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/common/lib/config.c'
curl -sS -o S383-ChangeLog 'https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/ChangeLog'
curl -sS -o S384-limine.c 'https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/host/limine.c'
```

## Raw output (trimmed to the relevant lines)

### Roster delta — `receipts/roster-diff.txt`

```
r95 FAMILY_ROSTER: len=99 unique=99
r96 FAMILY_ROSTER: len=103 unique=103
r95 duplicates: []
r96 duplicates: []
added in r96: ['EXPLICIT-VERSION-ECHO', 'EXPLICIT-VERSION-ERA', 'REFUSAL-VERSIONS-9DIGIT-Y', 'EXTRA-COMPONENT']
removed from r95: []
r95 REFUSAL_VERSIONS roster line:
  1643: REFUSAL_VERSIONS = ("12.9", "12.9.5.1", "abc", "", " 12.9.5", "12.9.5 ", "+12.9.5", "12..5",
r95 '12.9.5.1' occurrences: 1
r95 '12.9.6.1' occurrences: 2 (usage_check only, not a family roster):
  153: and `12.9.6.1` are probe failures), and select V1/V2 from that value; the JSON's
  2300: cases = [("12.9", 64), ("abc", 64), ("12.9.6.1", 64), ("", 64), ("9" * 5000 + ".0.0", 64),
```

### Landed gate, three runs — `receipts/r3-landed.json`, `receipts/count-runs-landed.json`

```
r3-landed.json run0 met 103/103 failed=[] cases=412 err=0
r3-landed.json run1 met 103/103 failed=[] cases=412 err=0
r3-landed.json run2 met 103/103 failed=[] cases=412 err=0
```

`count-runs.py` on the same file, with the four new families named:

```json
{"verdict": "met", "families_passed": 103, "families_total": 103, "failed_families": [],
 "cases": 412, "error_rows": 0,
 "named": {"EXTRA-COMPONENT": [4, 0], "REFUSAL-VERSIONS-9DIGIT-Y": [4, 0],
           "EXPLICIT-VERSION-ECHO": [4, 0], "EXPLICIT-VERSION-ERA": [4, 0]}}
```

### The four bends, three runs each — `receipts/r3-N0*.json`

```
r3-N01-echo-wrong.json      run0 unmet 102/103 failed=['EXPLICIT-VERSION-ECHO']              cases=412 err=0
r3-N01-echo-wrong.json      run1 unmet 102/103 failed=['EXPLICIT-VERSION-ECHO']              cases=412 err=0
r3-N01-echo-wrong.json      run2 unmet 102/103 failed=['EXPLICIT-VERSION-ECHO']              cases=412 err=0
r3-N02-y-cap-8.json         run0 unmet 102/103 failed=['REFUSAL-VERSIONS-9DIGIT-Y']          cases=412 err=4
r3-N02-y-cap-8.json         run1 unmet 102/103 failed=['REFUSAL-VERSIONS-9DIGIT-Y']          cases=412 err=4
r3-N02-y-cap-8.json         run2 unmet 102/103 failed=['REFUSAL-VERSIONS-9DIGIT-Y']          cases=412 err=4
r3-N03-era-label-flip.json  run0 unmet 102/103 failed=['EXPLICIT-VERSION-ERA']               cases=412 err=0
r3-N03-era-label-flip.json  run1 unmet 102/103 failed=['EXPLICIT-VERSION-ERA']               cases=412 err=0
r3-N03-era-label-flip.json  run2 unmet 102/103 failed=['EXPLICIT-VERSION-ERA']               cases=412 err=0
r3-N04-extra-components.json run0 unmet 101/103 failed=['EXTRA-COMPONENT', 'REFUSAL-VERSIONS'] cases=412 err=0
r3-N04-extra-components.json run1 unmet 101/103 failed=['EXTRA-COMPONENT', 'REFUSAL-VERSIONS'] cases=412 err=0
r3-N04-extra-components.json run2 unmet 101/103 failed=['EXTRA-COMPONENT', 'REFUSAL-VERSIONS'] cases=412 err=0
```

The N02 error rows are the bend's own refusals, one per Y-family case
(`bad-output: JSONDecodeError rc=64`, `receipts/r3-N02-y-cap-8.json`).

### The r95 do-nothing battery (blindness control), three runs each — `receipts/dn3-*.json`

```
dn3-landed.json             run0 met  99/ 99 failed=[]                   cases=396 err=0
dn3-landed.json             run1 met  99/ 99 failed=[]                   cases=396 err=0
dn3-landed.json             run2 met  99/ 99 failed=[]                   cases=396 err=0
dn3-N01-echo-wrong.json     run0 met  99/ 99 failed=[]                   cases=396 err=0
dn3-N01-echo-wrong.json     run1 met  99/ 99 failed=[]                   cases=396 err=0
dn3-N01-echo-wrong.json     run2 met  99/ 99 failed=[]                   cases=396 err=0
dn3-N02-y-cap-8.json        run0 met  99/ 99 failed=[]                   cases=396 err=0
dn3-N02-y-cap-8.json        run1 met  99/ 99 failed=[]                   cases=396 err=0
dn3-N02-y-cap-8.json        run2 met  99/ 99 failed=[]                   cases=396 err=0
dn3-N03-era-label-flip.json run0 met  99/ 99 failed=[]                   cases=396 err=0
dn3-N03-era-label-flip.json run1 met  99/ 99 failed=[]                   cases=396 err=0
dn3-N03-era-label-flip.json run2 met  99/ 99 failed=[]                   cases=396 err=0
dn3-N04-extra-components.json run0 unmet 98/ 99 failed=['REFUSAL-VERSIONS'] cases=396 err=0
dn3-N04-extra-components.json run1 unmet 98/ 99 failed=['REFUSAL-VERSIONS'] cases=396 err=0
dn3-N04-extra-components.json run2 unmet 98/ 99 failed=['REFUSAL-VERSIONS'] cases=396 err=0
```

The N04 failure row is the pre-existing `12.9.5.1` (`receipts/dn-N04-extra-components.json`:
`{'version': '12.9.5.1', 'rc': 0, 'stdout_bytes': 343, 'ok': False}`).

### Gate metadata probe — `receipts/gate-metadata-probe.json`

```
gate_sha256 7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32
era fixture:
  12.9.4          echo 12.9.4          source flag era pre-12.9.5  pin prompt  rc 1 DEGRADED
  12.9.5          echo 12.9.5          source flag era 12.9.5+      pin panic   rc 1 DEGRADED
  12.9.6          echo 12.9.6          source flag era 12.9.5+      pin panic   rc 1 DEGRADED
  999999999.9.9   echo 999999999.9.9   source flag era 12.9.5+      pin panic   rc 1 DEGRADED
  12.999999999.4  echo 12.999999999.4  source flag era 12.9.5+      pin panic   rc 1 DEGRADED
  0.999999999.0   echo 0.999999999.0   source flag era pre-12.9.5  pin prompt  rc 1 DEGRADED
healthy fixture:
  12.9.6.1    rc 64 stdout_bytes 0
  12.9.6.1.0  rc 64 stdout_bytes 0
  12.9.6.99   rc 64 stdout_bytes 0
  12.9.6.7    rc 64 stdout_bytes 0
  12.9.6      rc 0  stdout_bytes 922  HEALTHY  echo 12.9.6 flag era 12.9.5+
```

### Gate limit probe — `receipts/gate-limit-probe.json`

```
unsampled_four_component_shapes:  12.9.6. rc 64/0 · 12.9.6.1.2 rc 64/0 ·
                                  12.9.6.1.2.3 rc 64/0 · 12.9.6.０ rc 64/0
cap_member_in_every_position:    999999999.999999999.999999999 rc 0 HEALTHY era 12.9.5+ ·
                                  999999999.999999999.999999999.1 rc 64/0
pre_existing_r95_row:             12.9.5.1 rc 64/0
```

### Three own-work era-rule mutants — `receipts/mut-M-*.json`, clauses in `receipts/mutants/`

```
M-x-only-era unmet 96/103 failed=['AUTO-ERA-A','ERA-DEFAULT','ERA-FLE-MEASURED-A','ERA-FLE-PANIC-A',
                                   'EXPLICIT-VERSION-ECHO','EXPLICIT-VERSION-ERA','FIRST-LINE-ENTRY'] err=0
M-y-only-era unmet 95/103 failed=[the same seven + 'REFUSAL-VERSIONS-9DIGIT-Y']                        err=0
M-z-only-era unmet 102/103 failed=['REFUSAL-VERSIONS-9DIGIT-Y']                                       err=0
```

Per-family detail: `M-x-only-era` → `REFUSAL-VERSIONS-9DIGIT-Y` **passes 4 of 4**,
`EXPLICIT-VERSION-ERA` 3 of 4 (the `12.9.4` case wants `prompt`, the mutant answers `panic`);
`M-y-only-era` → Y family 2 of 4 (both `0.999999999.0` cases); `M-z-only-era` → Y family 2 of 4 (both
`12.999999999.4` cases), the other two families 4 of 4.

### Gate selftest

```
python3 tools/check-limine-pins.py --selftest
…
selftest PASS 39/39
```

### Source re-opens (2026-11-08)

```
S390  https://docs.python.org/3/library/sys.html#sys.int_info.default_max_str_digits
      http=200  280632 bytes  sha256 a7e005875e4152bcccaf44b9a834c123cc69bf7b66b3b8398aef91cffe77dd0e
      quote "The default value for sys.get_int_max_str_digits() when it is not otherwise
             explicitly configured."  (12 words) at byte 157851
S389  https://docs.python.org/3.15/library/stdtypes.html#integer-string-conversion-length-limitation
      http=200 (after a 301)  815447 bytes  sha256 6bf2ce2ba49d30974485266d70aecd4c4eb89334eb73367f3f99bfa036c7e9a8
      section id at byte 780206; "The default limit is 4300 digits as provided in
      sys.int_info.default_max_str_digits." at byte 785297;
      "When an operation would exceed the limit, a ValueError is raised:" at byte 782228
S382  Limine v12.9.5 common/lib/config.c   http=200  23351 bytes  sha256 a940acae3a0a9c4d1c716f8132f688c4bcdced2b092769bc1becad466e944e60
      raw 298 "static struct menu_entry *create_menu_tree(void) {"; 328-330 the cut; 362-365 the label-end NUL
S383  Limine v12.9.5 ChangeLog              http=200 121313 bytes
      line 5 "Noteworthy changes compared to the previous release, 12.9.4:"; line 8 the linear-time entry
S384  Limine v12.9.5 host/limine.c          http=200  69050 bytes
      raw 2031 puts(LIMINE_VERSION); 2035 puts("Limine " LIMINE_VERSION); 2089-2091 the --version dispatch
```

## PASS/FAIL per expected line

| # | expected line | measured | verdict |
|---|---|---|---|
| 1 | roster grows 99 → 103, exactly the four named families added, none removed | `receipts/roster-diff.txt`: 99 unique → 103 unique, added = the four, removed = `[]` | PASS |
| 2 | landed gate reads `103/103 met`, `failed_families []`, 0 error rows, three runs | `receipts/r3-landed.json`: ×3 `met 103/103`, `[]`, 412 cases, 0 error rows | PASS |
| 3 | each new family contributes 4 passing cases on the landed gate | `receipts/count-runs-landed.json`: each of the four `[4, 0]` | PASS |
| 4 | `N01-echo-wrong` → `102/103`, `["EXPLICIT-VERSION-ECHO"]`, unmet, three runs | `receipts/r3-N01-echo-wrong.json`: ×3 `unmet 102/103`, exactly that list, 0 error rows | PASS |
| 5 | `N02-y-cap-8` → `102/103`, `["REFUSAL-VERSIONS-9DIGIT-Y"]`, unmet, three runs | `receipts/r3-N02-y-cap-8.json`: ×3 `unmet 102/103`, exactly that list | PASS (with **4 error rows per run** — the bend's own rc-64 refusals; the frozen "0 error rows" clause does not hold on this leg, exactly as amendment A3 records) |
| 6 | `N03-era-label-flip` → `102/103`, `["EXPLICIT-VERSION-ERA"]`, unmet, three runs | `receipts/r3-N03-era-label-flip.json`: ×3 `unmet 102/103`, exactly that list, 0 error rows | PASS |
| 7 | `N04-extra-components` → `101/103`, `["EXTRA-COMPONENT", "REFUSAL-VERSIONS"]`, unmet, three runs | `receipts/r3-N04-extra-components.json`: ×3 `unmet 101/103`, exactly that list, 0 error rows | PASS |
| 8 | r95 do-nothing battery on the landed gate and on N01/N02/N03: `met 99/99`, three runs | `receipts/dn3-landed.json`, `dn3-N01…`, `dn3-N02…`, `dn3-N03…`: ×3 each `met 99/99`, `[]`, 0 error rows | PASS |
| 9 | r95 do-nothing battery on N04: `unmet 98/99`, `["REFUSAL-VERSIONS"]`, three runs | `receipts/dn3-N04-extra-components.json`: ×3 `unmet 98/99`, exactly that list | PASS |
| 10 | the four-component class was sampled once before this round (`12.9.5.1`) | `receipts/roster-diff.txt`: r95 `:1643` `REFUSAL_VERSIONS` contains `"12.9.5.1"`; the r95 usage row reads rc 64 / stdout 0; N04's second failed family is `REFUSAL-VERSIONS` on that row | PASS (r95 Frontier sentence corrected, not claimed as a first) |
| 11 | the four-component refusal has a same-list positive control that answers a verdict | `receipts/gate-metadata-probe.json`: the four shapes rc 64 / stdout 0; `12.9.6` rc 0 / 922 bytes `HEALTHY` | PASS |
| 12 | an explicit flag is echoed with source `flag`, and the era follows the whole tuple | `receipts/gate-metadata-probe.json`: six explicit versions, echo == flag, source `flag`, era `pre-12.9.5` / `12.9.5+` as the tuple selects | PASS |
| 13 | the era is selected from the whole tuple, not one position | `receipts/mut-M-*.json`: `M-z-only-era` kills exactly `REFUSAL-VERSIONS-9DIGIT-Y`; `M-y-only-era` kills it too | PASS |
| 14 | no upstream source states the version grammar or a component count (the gate's grammar is own-work) | sweep `grep -nE 'X\.Y\.Z\|three dot-separated\|component count\|three components' corpus/SOURCES.md` → no match; only S389/S390 mention a component width | PASS |
| 15 | no upstream Limine binary beyond the already-sourced versions is read | sweep `grep -oE 'limine-bootloader/limine/v[0-9.]+' corpus/SOURCES.md \| sort -u` → `v12.9.4`, `v12.9.5`, `v12.9.6` only | PASS |
| 16 | the entry's sources re-open byte-identically | S390 280632 B `a7e00587…`; S389 815447 B `6bf2ce2b…`; S382 23351 B `a940acae…` (matches the S382 row's recorded file hash) | PASS |
| 17 | the r95 battery never read `visibility_era` nor the explicit echo | `grep -c visibility_era tools/limine-pin-battery-r95.py` → 0; `grep -c check_echo tools/limine-pin-battery-r95.py` → 0; `auto_ok` short-circuits at r95 `:2014` | PASS |
| 18 | the gate's own selftest is green | `python3 tools/check-limine-pins.py --selftest` → `selftest PASS 39/39` | PASS |

## Findings

1. **The r96 battery's `fam_refusal_versions_9digit_y` docstring carries a false mutant claim.**
   It says a gate "that reads the era from X alone answers era B for `0.999999999.0` and fails"
   (`tools/limine-pin-battery-r96.py:1773-1775`). X of `0.999999999.0` is 0, so an X-only rule
   answers era **A** — the correct answer. Measured: the own-work X-only mutant passes the Y
   family 4 of 4 (`receipts/mut-M-x-only-era.json`); it is killed by `EXPLICIT-VERSION-ERA` and the
   ERA families instead, on `12.9.4`. The instrument is frozen and was **not** edited; the defect
   is reported here and in the draft's Limits. This is the same class the round already corrected
   for the r95 docstrings (routed 4) and is a candidate for the next round's routed list.
2. **The Z position of the per-component cap is unsampled at family level.** No family sends a
   version whose third component is at the cap (`grep -oE '999999999\.999999999[^"]*'
   tools/limine-pin-battery-r96.py` → no match). `999999999.999999999.999999999` is accepted by the
   gate (measured) but sent by no family, so a bend of Z's bound to `<= 8` is still untested. The
   Y family closes the second position only. Recorded as a named limit in the draft.
3. **Four-component shapes beyond the four enumerated are unsampled at family level.** The gate
   refuses `12.9.6.`, `12.9.6.1.2`, `12.9.6.1.2.3` and a non-ASCII digit rc 64 with empty stdout
   (measured), but `EXTRA_COMPONENT_VALUES` is exactly four members, so no case asserts them.
   Recorded as a named limit in the draft.
4. **N02's error rows.** The frozen C1 target's "0 error rows" clause does not hold on the N02 leg
   (4 per run, the bend's own rc-64 refusals). The round's amendment A3 already records this
   narrowing; this seat's measurement agrees with it.

## Relation to the entry the L1 already landed

The L1 landed `corpus/knowledge/limine-bound-per-component-r96.md` at `59cbfe2f` while this seat
worked. This seat's `knowledge-draft.md` is an independent draft of the same entry; it agrees with
the landed entry on every clause (per-component cap, the echo/source/era contract, the four-component
refusal with its same-list positive control, the r95 Frontier correction, the own-work scope) and
adds: the three-run receipt table for all four bends and all five do-nothing legs; the era-rule
mutant evidence (X-only / Y-only / Z-only); the four gate limit probes; the source byte/sha
receipts; and the three named limits above. Two differences worth the L1's eye: the landed entry
cites **S386-S388** (v12.9.6 `config.c`/`ChangeLog`/`limine.c`) for the era split, while this
draft's Limits follow the seat brief and name **S382-S384/S389-S390** and re-opened only S382-S384
(their v12.9.6 counterparts are byte-identical files per the S382 row); and the landed entry does
not carry the mutant table or the Z-position / extra-shape / false-docstring limits.

## Out of scope (not done by this seat)

- No lane file was created or edited: no `corpus/`, `tools/`, `SKILL.md`, `SCORECARD.md`, `LOG.md`,
  `.ufo/plans/`, `.ufo/waves/round-96/before/` or `claims.json` write.
- `tools/make-r96-bends.py` and `tools/make-r95-bends.py` were **not** run (they write into the
  frozen wave dir). Every bend used here is the frozen copy under `before/controls/bends/`, and the
  three own-work mutants were re-derived in scratch by `receipts/make_mutants.py` (which reads the
  lane's gate and writes only under scratch), with the one-clause diff shown by `diff -u` before
  each run.
- No git or jj mutation was run (no commit, push, stash, checkout, reset, switch).
- No subagent was dispatched (leaf member).
- The clone-layout (`git clone --shared`) leg of C1 was not re-run by this seat; the landed-gate and
  bend legs were measured in the canonical lane only. Other wave seats (ExecBattery, ExecBend,
  ExecDoNothing) hold the clone-layout receipts.

## Tooling

No tool was installed or upgraded by this seat. Everything used was already present:
`python3` (CPython 3.14.8, `/usr/bin/python3`), `bwrap` (`/usr/bin/bwrap`), `curl`, `sha256sum`,
`grep`, `diff`. No pacman transaction was made.

## Scratch

Scratch root `/fast/scratch/hyaku/tsukuroi-r96/ScribeKnowledge` was created for this seat, used
as the `--work`/`TMPDIR` root of every run, and **deleted** after the receipts were copied into
`receipts/`.

{"seat":"ScribeKnowledge","verdict":"findings","notes":"Knowledge draft written to .ufo/waves/round-96/w1/ScribeKnowledge/knowledge-draft.md with receipts under receipts/. Own measurements: roster 99->103 (own parser), landed gate 103/103 met x3 (0 error rows), four bends x3 each with the exact frozen failed_families (N02 carries 4 error rows per run, matching amendment A3), r95 do-nothing battery 99/99 met x3 on the landed gate and N01/N02/N03 and 98/99 unmet ['REFUSAL-VERSIONS'] x3 on N04. Own-work probes: gate echo/source/era for six explicit versions, four-component refusal rc64/stdout0 with the 12.9.6 same-list positive control rc0/HEALTHY, and three era-rule mutants (Z-only kills exactly REFUSAL-VERSIONS-9DIGIT-Y; X-only does NOT kill it). Findings: (1) the r96 battery docstring at :1773-1775 falsely claims an X-only era rule answers era B for 0.999999999.0 (measured: it answers era A, the correct answer) - frozen instrument, not edited, reported; (2) the Z position of the per-component cap is unsampled at family level; (3) four-component shapes beyond the four enumerated (empty fourth, five components, non-ASCII digit) are refused by the gate but unsampled at family level. Sources re-opened byte-identically (S390 280632B a7e00587, S389 815447B 6bf2ce2b, S382 23351B a940acae). Draft agrees with the L1's landed corpus/knowledge/limine-bound-per-component-r96.md on every clause and adds the mutant table, the limit probes and the three named limits."}
