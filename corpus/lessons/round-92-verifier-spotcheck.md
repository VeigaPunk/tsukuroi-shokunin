author: hyaku closure (non-author integrator, @m_zfl)

# Round 92 verifier spot-check — tsukuroi (closure judge, non-author)

Closure judge is not the round author. Head judged: `7793773a3837a46762cd6415da055ba4d20a1e29`
(branch `master`, `ahead=0`, clean). Before: `07c5826438925cc8f6650e1a0da4935082991c65`.

## 1. Step-1 conformance — PASS

- Report `.ufo/reports/round-92/tsukuroi.md` committed in the fleet repo by the lane identity:
  `git log --format='%an %ae %H' -1 -- .ufo/reports/round-92/tsukuroi.md` →
  `tsukuroi-shokunin tsukuroi@shokunin.local 840a650c4f2dd61ab00ea74a138cfce2a55bf9bf`.
- `grep -c '^## SHONEN' .ufo/reports/round-92/tsukuroi.md` → `1`, followed by four `[~]` lines, one per
  box of `SHONEN.md` (all four boxes are `[~]`; no self-attested `[x]`).
- Every cited lane commit exists and is an ancestor of branch `master`
  (`git merge-base --is-ancestor <hash> master`): `da99b2f4`, `495a9f6c`, `429fd1a3`, `689623fd`,
  `e9fce481`, `22b5bc10`, `ec728e4a` → all exit 0; `git cat-file -t` → `commit` for each.
- Lane tree clean: `git status --porcelain` → empty; `jj-lane.sh state` →
  `branch=master local=7793773a… remote=7793773a… ahead=0 behind=0 tracked=0 untracked=0`; not a marker
  report (real work, evidence pointers, LOG-tied changes, checkable hashes).
- Lands last: lane tip commit `7793773a` 02:41:46 -03, report commit `840a650c` 02:42:12 -03 (26 s later).
- Prompt `.ufo/prompts/tsukuroi-round-92.md` is committed; it carries §1 mission/axes, §2 1–3 claims with
  falsifiable before→after, §2b frontier step, §3 L2 floor (≥8 seats, one batched AgentSwarm), §4 report
  contract (SHONEN, evidence pointers, commit-hash citation), §5 commit-then-push + push scope + L0, and
  the five child-lane items (write scope :448, commit/hash order :455–494, report-lands-last :516,
  `SHONEN` pre-check :521, report path :84). `MISSION.md` §L2 states the role→bucket classes as advisory
  to host routing; the prompt's quoted role→model map is the operator's host table — no conflict.

Defects (status-neutral, routed §6): see §6 items 1–4.

## 2. Prefile falsification ledger (§2b, Amendment 59)

```
python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane tsukuroi --round 92
PREFILE-FALSIFICATION: pass claims=2 rows=14 attack_seats=7 findings=0
EXIT=0
```

Matches the report verbatim. The ledger `.ufo/waves/round-92/claim-falsification.tsv` covers both
`claims.json` claims (C1 6 rows, C2 8 rows), reads all six attack-role seats' artifacts plus
`ExecIsolationProbe`'s (7), and every `falsifies-wording` row names a narrowing (A3, A4, A5, A6, A7
§1/§3, QUALITY 135). Adjudication: no unreconciled row. The `falsifies-number` row (C2 usage 8/8 vs the
shipped 11 cases) is real and is reconciled by A7 §5 with a committed receipt; the remaining `neutral`
rows are corroborations, not findings.

## 3. Per-claim re-check (before → after, re-derived here)

Every value below is a plain measurement over committed bytes run by this closure; no lane gate was
executed. Commands are run from the lane root at `7793773a`.

### C1 — operability, battery oracle channel

| check | command | observed |
|---|---|---|
| launcher exists as claimed | `grep -n 'def sandbox_argv\|def copy_gate\|"-I"' tools/limine-pin-battery-r92.py` | `sandbox_argv` wraps `bwrap --unshare-all --die-with-parent --new-session --clearenv`, ro-binds `/usr` `/etc` and the gate copy, fresh `/dev` `/proc` `/tmp`, `--chdir` case dir, `python3 -I` (:1747–1772) |
| family roster | `python3 - <<'EOF'` count of `FAMILIES` keys vs `FAMILY_ROSTER` | `FAMILIES keys 89`, `ROSTER 89`, `same set: True` |
| landed gate after | `cat .ufo/waves/round-92/after/c2-gate-{canonical,clone}.txt` | three lines each: `families_passed 89/89 verdict met failed -` |
| controls after (canonical) | `cat .ufo/waves/round-92/after/c1-controls/canonical-after-final/summary.tsv` | K3/K4/K5/K6/K7 `families_passed 0,0,0` `unmet,unmet,unmet` `errors 0` |
| controls after (clone) | `.../after-clone-final/summary.tsv` | identical: `0,0,0` / `unmet` ×3 / `0` errors |
| controls before | `.../before-clone/summary.tsv` + `.../before-clone-fixed/summary.tsv` | K3/K5/K6/K7 `82,82,82 met`; K4 (fixed bytes `efb53f76…`) `82,82,82 met` |
| instrument binding | `sha256sum tools/check-limine-pins.py tools/limine-pin-battery-r92.py` | `35c1088b7bacb31d…`, `aef3392516aabf29…` — the A7 ledger row and `after/final-instrument-shas.txt` |
| manifest integrity | `sha256sum -c .ufo/waves/round-92/before/freeze-manifest.sha256` | exit 0; 28 lines; own sha `8f48d358…` |
| do-nothing control | `jq … after/c1-controls/k1-donothing.json` | `families_passed 1` of 89, `cases 356`, `case_log` 352 `error: bad-output: JSONDecodeError rc=64` |

Verdict: **met** on the differential reading (A7 §1). `0/89` alone is the shipped fallback's property;
the same control bytes read `82/82 met` with the channel open, so the closure is the differential, and
the landed gate reads `89/89` under the launcher in both layouts. Score 9 → 9 (saturated), axis
**improved** on the assurance arm; capability `battery-oracle-isolation` entered after it ran.

### C2 — depth, version-selected visibility rule

| check | command | observed |
|---|---|---|
| era selection | `grep -n 'VISIBILITY_ERA_SPLIT\|era_b = \|first_entry != 1' tools/check-limine-pins.py` | split `(12, 9, 5)`; `in_global` closes at the first entry when `era_b or first_entry != 1` — no first-line exception from 12.9.5 |
| refusal | `sed -n '74,100p' tools/check-limine-pins.py`; `after/usage-stdout-check.txt` | ≤9-digit components, else `None` → rc 64; refused versions `rc=64 stdout_bytes=0`, accepted print one JSON object |
| families | `python3` count (above) | 89 families; 4 cases each = 356 |
| gate selftest tally | `grep -cE '^        case\(' tools/check-limine-pins.py`; tail `after/…/gate-selftest-tip.log` | 35 `case()` + `version-parser` + `conf-absent` = 37; committed log `selftest PASS 37/37` |
| near-misses | `cat after/c2-near-misses/{canonical-final,clone-final}/summary.tsv` | N01 `87,87,87 unmet`; N02 `85,85,85 unmet`; N03 `88,88,88 unmet`; N04 `89,89,89 met`; errors 0 in all rows, both layouts |
| usage check | `jq` over `w1/ExecLints/battery-usage-check.json` (canonical) and `w1/ExecReplicate2/usage-check-a3.json` (clone) | both `met`, 11 cases, all `ok` |
| source quote | pinned `before/src/limine-v12.9.6-common_lib_config.c` raw 328–330, 362–365 | `if (p > config_addr) { *(p - 1) = '\0'; }` and the label-end NUL, exactly as cited |
| config.c identity | `sha256sum` on the two pinned files | both `a940acae…` (12.9.5 == 12.9.6 for this clause) |
| host era | `pacman -Q limine`; `limine --version` | `limine 12.9.4-1`; `Limine 12.9.4` |

Verdict: **met on the narrowed predicate** (A5): the 12.9.5-exact flip, the first body line after the
cut and era-B U1 are named limits, not claims. Score 8 → 8 (tied lowest), axis **improved** on sourced
decidable detail; the closure endorses the move as depth (the change is a sourced rule with a real
threshold, S379/S380), not a second operability claim.

### No-harm check

`git diff 07c58264 7793773a -- SCORECARD.md` → 53 insertions, 0 deletions (declaration, capability row,
measured outcome). Era-A behaviour is unchanged: `after/c1-controls/r91-battery-on-r92-gate.txt` →
`families_passed 82/82 verdict met`. Gate selftest 37/37 and battery selftest 18/18 are committed green;
registry coverage 145/145 receipt exists at `e9fce481` (see §6 defect 2). No owned axis harmed.

## 4. Discernment spot-check (from outside)

Re-opened sources: the round's pinned copies under `.ufo/waves/round-92/before/src/` (paths), the live
URLs where the pin is a snapshot, and the census command.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S379 Limine v12.9.6 `config.c` | admit (A) | `before/src/limine-v12.9.6-common_lib_config.c` raw 328–330, 362–365 | agree | the quoted cut and label-end NUL are byte-for-byte at the cited raw lines; the entry's "no first-line exception from 12.9.5" follows |
| S380 Limine v12.9.6 ChangeLog | admit (A) | `before/src/limine-v12.9.6-ChangeLog.txt` lines 14–16, `Miscellaneous:` block | agree | the ≤25-word quote is verbatim and says "since 12.9.5"; it also names #700 |
| S377 Python `-P`/`-I` docs | admit (A) | `before/src/python-3-cmdline.txt` line 241 and the `-I` entry; live `https://docs.python.org/3/using/cmdline.html` | agree on quote, **disagree on anchor** | quote is verbatim; the page (pinned and live) is **3.15.2**, while the SOURCES anchor says "Python 3.14 docs" — routed, §6 item 3 |
| S378 bubblewrap manual | admit (A) | `before/src/bubblewrap-bwrap.xml` `--clearenv` entry | agree | "Unset all environment variables, except for PWD …" is verbatim; `--unshare-all` list matches |
| S381 Limine issue #700 | admit (C lead) | `before/src/issue-700.json`, `### Cause` block | agree | the quote is verbatim; tier C and "never sole support" is right — it corroborates S380 |
| reject: v12.9.5 ChangeLog as its own row | reject | `before/src/limine-v12.9.6-ChangeLog.txt` line 22 `*** Release 12.9.5 ***` | agree | the 12.9.6 file carries the 12.9.5 section, so one row suffices; the file is still pinned |
| reject: `man.archlinux.org/man/bwrap.1` | reject | live fetch → `<title>bwrap(1) — Arch manual pages</title>` | agree | it is the downstream Arch rendering of the same manual; upstream `bwrap.xml` is the authoritative bytes |
| reject: `docs.python.org/3.13/using/cmdline.html` | reject | URL shape (version-pinned path) | agree | curation reason holds: the version-less URL follows current docs and will not rot at the next release |

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root … tsukuroi` → **exit 0**
(381 rows; 55 W04 duplicate-URL-across-scopes warnings, 1 W01 tier-C lead warning, `ok`). The W04/W01
warnings are the same ones the report names; no `E` rows.

## 5. Trend verdicts (with evidence)

- **expansion — improved.** One admitted knowledge entry on ground the lane did not hold
  (`corpus/knowledge/limine-r92-oracle-isolation.md`, OI1–OI4 + EV1–EV5) whose `source:` cites five
  `mined` rows opened this round (S377–S381), plus one capability row (`battery-oracle-isolation`) that
  entered only after running end to end in both layouts. `SOURCES.md` 376 → 381
  (`git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`).
- **quality — improved.** The gate's 5000-digit crash and the `--selftest`/`bwrap` order are fixed
  (A3), the battery grows 82 → 89 families with four one-clause bends, QUALITY 132–135 land, r91 routed
  defects 3–5 are closed, and the era-A no-regression receipt reads 82/82.
- **discernment — improved.** Seven attack artifacts (CriticClaims, MutBattery, ReviewGate,
  ExecIsolationProbe, MutGate, CriticForgers, plus the credential row) falsified the round's own wording
  and every one became an amendment (A3–A7) or a named limit; the lane caught two dead controls and a
  wildcard control itself before any candidate score (M3/M4). This spot-check agrees with every sampled
  admit and reject; the one disagreement is an anchor version, routed.

## 6. Routed defects (lane fixes next round)

1. **Report's Landed-changes table is short four commits.** The table ends at `ec728e4a`; the round's
   later commits `b5cb636a` (wave settlement + `w1-results.json`), `98185b9b` (A9 corrections, K1 leg
   fixed), `1d1c7439` (K1 receipt) and `7793773a` (A8 manifest) carry cited changes and are not named
   anywhere in the report (`grep -c` = 0 for the first three). Report-contract defect
   ("every change tied to … the commit hash that carries it"), status-neutral. Fix: append the four
   rows in the next round's report (reports are never rewritten).
2. **Registry-coverage PASS is cited at a revision that has no receipt.** The report says
   `check-registry-coverage.py` PASS 145/145 "at `ec728e4a`", but the committed PASS receipts are
   `e9fce481` (`registry-coverage-tip.json`, i.e. before the F3/F4 row replacements) and a scratch-clone
   probe at `2bae8c5` that does not resolve in the repo (`git cat-file -t 2bae8c5…` → fatal). Re-run the
   checker at the round tip, commit the receipt, and cite that revision.
3. **S377 anchor names the wrong docs version.** `corpus/SOURCES.md` S377 anchor says "Python 3.14 docs";
   the pinned snapshot and the live page are **3.15.2**. The ≤25-word quote is correct and unchanged —
   correct the anchor by an appended row or a logged anchor change (contract rule 1/2), never a silent
   rewrite.
4. **`claims.json` C2 target still reads `--usage-check` 8/8.** The shipped check has 11 cases; the
   reconciliation is A7 §5 and the report's 11/11, but the frozen declaration literal remains stale.
   The frozen file is not to be edited; the next lesson/plan should carry the pointer to A7 §5 so a
   reader re-deriving the claim does not read 8/8 as the target.
5. **Hygiene (not a defect):** `after/c1-controls/usage-{canonical,clone}.json` are 8-case pre-A3
   receipts and are not cited by the report (which cites the 11-case seat receipts); keep them labelled
   as pre-A3 or they will be misread as the round's usage tally. Also, the report's discernment trend
   says "four wave seats falsified"; the ledger reads seven attack artifacts (six named seats plus
   ExecIsolationProbe) — an undercount, not an overclaim.
