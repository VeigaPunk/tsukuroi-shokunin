# ReviewBattery — C1 falsification (round 97, w1)

Seat: `ReviewBattery` — Attack C1; falsify the frozen wording, do not re-print receipts.
Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`; seat receipts under
`.ufo/waves/round-97/w1/ReviewBattery/`; scratch under `/fast/scratch/hyaku/tsukuroi-r97/ReviewBattery`
(deleted before yield).
Tools installed: none. Reads: `claims.json` (frozen C1), `.ufo/plans/round-97.md`
(declaration/limits/amendment slot), `.ufo/waves/round-97/before/instruments.sha256`,
`corpus/lessons/round-96-verifier-spotcheck.md`, `corpus/QUALITY.md` 139–140.

## Checks run (all from the lane root)

### 0. Instruments pinned and hashes match

- `sha256sum -c .ufo/waves/round-97/before/instruments.sha256` → all 20 lines `OK`
  (receipt `sha256sum-c.txt`). Direct hashes (`sha256.txt`):
  `tools/limine-pin-battery-r97.py e678c34f…`, `tools/check-limine-pins.py 7d79ac29…`
  (matches the declared unchanged gate hash `7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32`),
  bends `N05 8a570b3a…` / `N06 f89f9967…` as pinned.

### 1. Roster integrity

`python3 -c` importing `tools/limine-pin-battery-r97.py`:

```
len(FAMILY_ROSTER)= 105
tuple(FAMILIES)==FAMILY_ROSTER: True
CASES_PER_FAMILY= 4
cases_expected= 420
```

Receipt `roster.txt`. PASS. All battery JSON receipts carry `cases: 420`
(`fam` totals 105) — `FAMILY_ROSTER` per-family `4/4` confirmed in the
landed-gate re-run below.

### 2. Frozen counting commands re-run (the run wins)

All runs used `--runs 3 --work /fast/scratch/hyaku/tsukuroi-r97/ReviewBattery/work`
(batch directory per gate where noted) with the canonical command
`python3 tools/limine-pin-battery-r97.py --gate <GATE> --runs 3 --work … --json <seat>/<out>.json`,
then `python3 .ufo/waves/round-95/before/controls/count-runs.py <out> --family REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE`.

| gate | families_passed | failed_families | error rows / run | verdicts | receipts |
|---|---|---|---|---|---|
| landed `tools/check-limine-pins.py` | 105/105 each | `[]` | 0,0,0 | met,met,met | `counted-gate-runs3.json` + `-count.txt` |
| N05 committed bend | 103/105 each | `[LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]` | 6,6,6 (Z 4, LZ 2) | unmet ×3 | `counted-N05.json` + `-count.txt` |
| N06 committed bend | 104/105 each | `[LEADING-ZERO-NORMALIZE]` | 4,4,4 | unmet ×3 | `counted-N06.json` + `-count.txt` |
| r96 do-nothing battery × landed | 103/103 met | `[]` | 0 | met | `dn-gate.json` |
| r96 do-nothing × N05 / N06 | 103/103 met | `[]` | 0,0 | met,met | `dn-N05.json`, `dn-N06.json` |

The re-runs match the frozen target sentence exactly (`claims.json` C1 target).
Raw stdout: `counted-*.txt`, `dn-*.txt`; parsed summaries `summaries.txt`.

Bend texts re-derived in scratch (never `make-r97-bends.py`, which writes the
frozen dir): the landed gate carries exactly one match for the substitution
anchor, and both substitutions reproduce the committed bytes byte-identical:
`N05 30356` bytes, `N06 30350` (`bend-derivation.txt`, diffs `bend-diffs.txt`).

### 3. Error-row accounting (bend receipts)

Every non-null `error` string in the six N05 and four N06 error rows per run is
byte-identical in class, e.g.:

```
'bad-output: JSONDecodeError rc=64 stderr=usage: gate.py [-h] [--conf CONF] [--esp ESP] [--secure-boot-enforced {0,1}]\n               [--tpm-present {0,1}] [--limine-version LIMINE_VERSION]\n               [--live] [--selftest]\ncheck-limine-pins: --limine-version must be X.Y.Z or auto\n'
```

(`error-strings.txt`, full list in `summaries.txt`.) This is the gate's own
usage-error refusal (stdout empty, rc 64) parsed as a bad-output — i.e. the
bend's own rc-64 refusal, not a transport/bwrap/timeout failure. No row carries
`timeout`, a traceback, or stderr text other than the argparse usage plus the
single `must be X.Y.Z or auto` line. PASS.

Which LZ members N05 refuses (from `counted-N05.json`, `n05-lz-want.txt`):
`12.09.4` and `000000012.9.4` pass; the era-B member `12.000000009.000000005`
(want pin `panic`) and the all-zero member `000000000.000000000.000000000`
(want pin `prompt`) are refused — 2 per run, matching the claim's named split.
The battery's `LEADING-ZERO-NORMALIZE` member order makes the victims visible
by want-pin, since refused rows log `got: null`.

### 4. Near-miss attacks (scratch gates, never the committed bends)

Gates derived in scratch from the landed gate bytes (anchors counted, exactly
one substitution each where stated) — `attack-derivation.txt`:

- **attack-1 (`attack1-eraA-pin.py`)**: `era_b` forced False for exactly
  `(12, 9, 999999999)`. Accepts `12.9.999999999` but answers `prompt` (era A)
  where the pin expectation is `panic`.
  Result: `104/105 unmet`, `failed_families ['REFUSAL-VERSIONS-9DIGIT-Z']`,
  0 error rows, all three runs; the other Z member `0.9.999999999` passes
  (`attack-1.json`, `attack-1.txt`). **Verdict: killed** — caught by
  `REFUSAL-VERSIONS-9DIGIT-Z` exactly as claimed. (This is the pin-level
  "accepts but reads era A" case the claim says the family exists to kill; the
  `visibility_era` string also flips, but the pins are what the family asserts.)
- **attack-1-field (`attack1-eraA-field.py`)**: pins correct (real `era_b`),
  only the reported `visibility_era` string lies for exactly the Z boundary
  tuple (`12.9.999999999` reports `pre-12.9.5` while pinning `panic`).
  Result: `105/105 met`, `failed_families []`, 0 error rows, all three runs
  (`attack-1-field.json`). Direct run confirms the lie
  (`visibility_era: pre-12.9.5` + `panic` pins; landed gate reports `12.9.5+`).
  **Verdict: survives.** The only family that asserts `visibility_era` is
  `EXPLICIT-VERSION-ERA` (`check_era`), and its members
  (`12.9.4`, `12.9.5`, `12.9.6`, `999999999.9.9`) never include the Z tuple —
  no family is supposed to catch a field-only lie on these members under the
  current roster, and none does. Wording is still true here (the claim's
  predicate binds "each ACCEPTED … and answered from the era the whole tuple
  selects, `panic` for era B" — that is the pin consequence, which this gate
  honors), but a future claim that Z's `visibility_era` string is certified
  would be unsupported.
- **attack-2 (`attack2-echo-norm.py`)**: accepts the leading-zero members but
  normalizes the echoed `limine_version` (`12.09.4` → `12.9.4`,
  `000000012.9.4` → `12.9.4`). Pins and era correct.
  Result: `105/105 met`, `failed_families []`, 0 error rows, all three runs
  (`attack-2.json`). Direct run confirms the echo flip.
  **Verdict: survives.** The only family that asserts the echo is
  `EXPLICIT-VERSION-ECHO` (`check_echo`); its members contain no leading-zero
  spelling, and `LEADING-ZERO-NORMALIZE`/`REFUSAL-VERSIONS-9DIGIT-Z` do not
  set `check_echo` (only `EXPLICIT-VERSION-ECHO` does; confirmed by family
  source). So **no** family catches it. The claim never asserts echo-correctness
  for the new families, so this is a coverage gap note, not a wording
  falsification — but any sibling reading "accepted with its era's own answer"
  as including the echoed spelling would be wrong.
- **attack-3 (`attack3-refuse-allzero.py`)**: refuses only
  `000000000.000000000.000000000`.
  Result: `104/105 unmet`, `failed_families ['LEADING-ZERO-NORMALIZE']`,
  exactly 1 error row per run, the rc-64 refusal class
  (`attack-3.json`). **Verdict: killed** — and the arithmetic the seat was
  asked to state: `LEADING_ZERO_VALUES` has 4 members cycled by
  `c.index % 4` over 4 cases per run via the monotonically climbing `_SEQ`
  counter (`tools/limine-pin-battery-r97.py:2036-2037`,
  only incremented in `build()`; 12 builds across `--runs 3` → indices
  0–11, each residue exactly once per 4-case run). So the all-zero member is
  hit exactly once in **every** run — the refusal cannot hide behind a
  missing ordinal. (The Z family is 2 members over 4 cases: each member twice.)
- **attack-4 (`attack4-constant.py`)**: answers `met` for every case
  (`HEALTHY, rc 0, []`).
  Result: `0/105 unmet`, all 105 families in `failed_families`, 0 error rows,
  all three runs (`attack-4.json`). **Verdict: killed.** The
  `absent`/`constant` class reads unmet — a constant gate is reported as a
  pin/verdict mismatch (`got != null`, `error: null`), not as a transport
  error, which is exactly the honest-signal behavior the battery promises.

### 5. Falsification ledger draft (claim clauses under review)

Format: `claim<TAB>artifact<TAB>verdict<TAB>narrowing<TAB>note`

```
falsifies-wording	.ufo/waves/round-97/w1/ReviewBattery/attack-1-field.json	survives (field-only lie, pins correct, 105/105 met ×3)	Limit, not a predicate cut: "Z's visibility_era string is uncertified; only the pin consequence (panic/prompt) is asserted by REFUSAL-VERSIONS-9DIGIT-Z"	claim only binds accepted + era's own answer (pins); attack flips 12.9.999999999 visibility_era to pre-12.9.5 with panic pins intact and reads met. No kill clause touches the field.
falsifies-wording	.ufo/waves/round-97/w1/ReviewBattery/attack-2.json	survives (normalized echo, pins correct, 105/105 met ×3)	Limit, not a predicate cut: "leading-zero echo spelling is uncertified; only pins/era asserted by LEADING-ZERO-NORMALIZE"	claim does not bind limine_version echo for the new families; check_echo lives only in EXPLICIT-VERSION-ECHO whose members have no leading zeros. Attack echoes 12.09.4 as 12.9.4 and reads met.
neutral	.ufo/waves/round-97/w1/ReviewBattery/attack-1.json	killed (pin-level era-A flip, Z-only unmet ×3)	none	Confirms the claimed witness: accepts 12.9.999999999 but pins prompt vs want panic → REFUSAL-VERSIONS-9DIGIT-Z alone.
neutral	.ufo/waves/round-97/w1/ReviewBattery/attack-3.json	killed (all-zero-only refusal, LZ-only unmet ×3, 1 rc-64 row/run)	narrowing already in plan Limits: 4-member cycle covers one member per case ordinal	Arithmetic is settled (4 members ÷ 4 cases, _SEQ covers each residue once per run); no wording change needed.
neutral	.ufo/waves/round-97/w1/ReviewBattery/attack-4.json	killed (constant met → 0/105 unmet ×3, 0 error rows)	none	absent/constant class reads unmet, not error; both new families fail.
neutral	.ufo/waves/round-97/w1/ReviewBattery/counted-gate-runs3.json + counted-N05.json + counted-N06.json	holds (counts match frozen sentence, 105/103/104, error split 4+2 / 4)	none	Full re-run agrees; bend bytes re-derived byte-identical without make-r97-bends.py.
```

## Assessment

The frozen counting sentence survives re-execution byte-for-byte, including
the N05 split and the rc-64 error class, and both committed bends re-derive
identically with exactly one match each. Both near-misses that the claim
*does* put within the two new families' reach are killed (pin-level era flip;
all-zero-only refusal; constant gate). The two survivors are real but target
*untouched* legs (the `visibility_era` string and the echoed `limine_version`
spelling) that the families never assert — they do not contradict any sentence
in the frozen predicate, whose verbs ("ACCEPTED", "answered with the era's own
answer" via `panic`/`prompt`) are pin-consequence statements. Their proper
fate is a named Limit, not a kill: if a later round claims *reported* era or
*echoed* version fidelity for the Z or leading-zero members, this ledger is
the citation that the current roster cannot back it.

Open residuals (honest, not smoothed):

- The Z family is 2 members over 4 cases and the LZ family is 4 over 4; a
  bend keyed to a *fifth* spelling of either class would escape — declared in
  the plan's Limits, confirmed by the cycle arithmetic above.
- `attack-1-field` and `attack-2` survive only because their lies sit outside
  the four-member/two-member sets; an amendment that folds Z and the LZ
  members into `check_echo`/`check_era` scope would close both in one move.
  I have not recommended one: the round's deal is pins and refusal, and the
  lane already named the broader sampling limit.

## Receipts

Seat dir `.ufo/waves/round-97/w1/ReviewBattery/`: `roster.txt`,
`sha256.txt`, `sha256sum-c.txt`, `bend-derivation.txt`, `bend-diffs.txt`,
`counted-gate-runs3.json/.txt/-count.txt`, `counted-gate.json/.txt`,
`counted-N05.json/.txt/-count.txt`, `counted-N06.json/.txt/-count.txt`,
`dn-gate.json/.txt`, `dn-N05.json/.txt`, `dn-N06.json/.txt`,
`attack-derivation.txt`, `attack-1.json/.txt`, `attack-1-field.json/.txt`,
`attack-2.json/.txt`, `attack-3.json/.txt`, `attack-4.json/.txt`,
`error-strings.txt`, `summaries.txt`, `n05-lz-detail.txt`, `n05-lz-want.txt`.
Scratch `/fast/scratch/hyaku/tsukuroi-r97/ReviewBattery/` held all gate
derivations and `--work` dirs and is removed before yield.

This report was written to `.ufo/waves/round-97/w1/ReviewBattery.md`
(the seat asked for `ReviewBattery.md`; the standing write-only-seat rule
confines bytes to the seat dir, so the identical file also lives at
`.ufo/waves/round-97/w1/ReviewBattery/report.md` and is cited here).

{"seat":"ReviewBattery","verdict":"findings","notes":"Claims re-run exact (105/105, N05 103 4+2, N06 104 4, rc-64 refusals); attacks 1-old-B expected killed (pin flip Z-only), attack3 killed, attack4 killed; survivors: attack1-field (Z visibility_era lie, 105 met) and attack2 (normalized leading-zero echo, 105 met) — both outside asserted legs, ledger names narrowing as Limits."}
