VERDICT: defect-found

Item C2-20 — one-cell mutation probe of `corpus/knowledge/alpm-package-anatomy-r41.md` at 9cc9aa77e30e0e23de2d4d2697b3b218ada02969 against the frozen counter `tools/check-package-anatomy-r41.py` (sha256 verified before use: c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f, observed `sha256sum` at lane HEAD 71851d63). Result: **5 of 6 mutants killed, 1 survived (M5, PA8 relation-phrase reorder passes the "ordered relations" gate)**. The survivor contradicts the gate's own stated purpose at `tools/check-package-anatomy-r41.py:16-17`.

## Setup

- Scratch clone per lane bounds: `git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /fast/scratch/hyaku/tsukuroi-r41/C2MutEntry/clone && git -C <clone> remote remove origin`; `git -C <clone> rev-parse --show-toplevel` printed the clone path (equality verified); identity `C2MutEntry fixture <fixture@shokunin.local>`; `git -C <clone> checkout -q -B master 9cc9aa77...` — HEAD verified `9cc9aa77e30e0e23de2d4d2697b3b218ada02969`, `status --porcelain` 0 lines.
- No verdict files exist at the pin: `git ls-tree --name-only 9cc9aa77:.ufo/waves/round-41/w1` → `fatal: Not a valid object name` (same for `residual`). The counter reads verdicts from the commit tree at the scored revision (`git(repo,'ls-tree','--name-only', f'{rev}:{d}')`, `tools/check-package-anatomy-r41.py:272`), so per the item's "(with all-holds fixture verdicts)" I committed eight fixture files `.ufo/waves/round-41/w1/C2RevPA{1..8}Fx.md`, first line `VERDICT: holds`, body naming the row id (names match the counter's regex, line 276). Fixture-verdict commit on master: **V = c6d4e5ea094f4b36e39b479d3720d33c57d30656**.
- Baseline (pristine entry + fixtures): `python3 tools/check-package-anatomy-r41.py --repo <clone> --revision c6d4e5ea...` → `result PASS, exit 0`; `rules_verified 8, verdicts_ok 8, host_ok 6, source_ok 1, duplicate_rows 0, duplicate_headings 0, novelty_base_hits 0`. The record's `host_expect.PA4` = `["mtree 1409 of 1409", "install 51 of 1409", "changelog 0 of 1409", "dot-files 0 of 1409"]`, `host_meta.entries = 1409`.
- Every mutant was its own commit on master; `git diff --stat V HEAD` showed exactly 1 file changed (1+/1− for M1, M2, M4, M5, M6; 29+/1− for M3, the relocated quote plus its inert carrier lines). One counter run at a time; counter runs took ~2-3 s each.

## Mutants and verdicts

Command shape for every run: `TMPDIR=/fast/scratch/hyaku/tsukuroi-r41/C2MutEntry python3 tools/check-package-anatomy-r41.py --repo <clone> --revision <sha>` (cwd = lane), full JSON observed per run.

| id | cell mutated (pinned entry line) | sha | verdict | counter output that decides it |
|---|---|---|---|---|
| M1 | PA5 value (l.30): `` `gzip mtree without .MTREE` `` → `` `gzip mtree` `` | 91496028ebdcc71b0e0b25cea135da1742168f2f | **killed** | `FAIL, exit 1`; `rules_verified 7`; PA5 reason: `value '`gzip mtree`' != derived 'gzip mtree without .MTREE'` (value-equality gate, line 349-350) |
| M2 | PA7 rule (l.32): `package()` and `verify()` swap directories | 6b653e05f2695e96ad3dda0fa02457dd4c3c2727 | **killed** | `FAIL, exit 1`; `rules_verified 7`; PA7 reasons: `relation unmet: package\(\), prepare\(\), build\(\) and check\(\) each run inside \$srcdir\b` and `relation unmet: verify\(\) runs inside \$startdir\b` (lines 351-353) |
| M3 | PA1 source (l.26): quote `“The following files must be present at the root of an ALPM based package:”` moved out of the cell to line 90 | da54274bf23530e195188e943ff06a6191595bb9 | **killed** | `FAIL, exit 1`; `rules_verified 7`; PA1 reason: `no 4-25 word quote found in alpm-package.7.raw at cited lines inside the window` (line 383) |
| M4 | PA4 host (l.29): `install 51 of 1409` → `install 50 of 1409` | fb1c4fe0f84b66bad5c4ed5394570a073334dffe | **killed** | `FAIL, exit 1`; `rules_verified` stays 8 but `host_ok 5`; `rules.PA4.host_ok: false`, no textual reason (host gate is a count, lines 389-392); the printed `host_expect.PA4` carries `install 51 of 1409` from the frozen capture |
| M5 | PA8 rule (l.33): phrase reorder — `an absent epoch counting as 0` moved ahead of `the epoch first` | 45f481dba605dfeca2b78a25d73cd6cb1967e13b | **SURVIVED** | `PASS, exit 0` — `rules_verified 8, verdicts_ok 8, host_ok 6, source_ok 1, duplicate_rows 0, duplicate_headings 0, novelty_base_hits 0`; PA8 has zero reasons |
| M6 | PA3 source (l.28): `S229` → `S213` | 17496e0bcd9a26030df11022727b0383221bccaa | **killed** | `FAIL, exit 1`; `rules_verified 7`; PA3 reasons: `cited S-id not on source: line: S213` + `no new mined upstream row for makepkg.sh.in (54d9411) naming the entry` (lines 362, 366-369) |

M3 fidelity note: the pinned entry is 62 lines (`git show 9cc9aa77:corpus/knowledge/alpm-package-anatomy-r41.md | wc -l` → 62), so "moved to line 90" was implemented as: quote deleted from the PA1 cell, plus a 28-line inert appendix (no row/heading/id lines) placing the sentence verbatim on line 90 (`wc -l` of the mutated file → 90; line 90 verified in the edit preview). Everything outside the PA1 cell was byte-identical filler, so the kill is attributable to the relocation alone.

## The survivor — coverage finding, not a contract change

M5's full mutated rule cell reads: "libalpm compares two full versions in three steps: **an absent epoch counting as 0, the epoch first,** then the version, and the release only when both strings carry one; so any epoch 1 build outranks every epoch 0 build and `1.0` equals `1.0-5`" (bold marks the moved phrase). Why it passes:

- `RELATIONS['PA8']` (`tools/check-package-anatomy-r41.py:111-113`) is four independent regexes; the ordering claim lives only *inside* regex 1 `\bthe epoch first\b.*\bthen the version\b.*\bthe release only when both\b`. Moving `absent epoch counting as 0` ahead of `the epoch first` leaves those three anchors in relative order and `.*` bridges the intruding phrase; regex 2 `\babsent epoch counting as 0\b` is a position-independent `re.search` (loop at lines 351-353). No other gate reads phrase order: value cell unchanged (still equals derived, line 349), host cell unchanged, source cell unchanged.
- The counter's docstring claims this gate exists "so a token list in another order, or a rule that swaps a pairing, fails" (`tools/check-package-anatomy-r41.py:16-17`). M5 is a counterexample for PA8's step list: a phrase-level reorder that keeps each single regex's anchors ordered sails through. The gate pins anchor order per regex, not the order of the proposition's phrases as a whole.
- Scope: [INFERENCE from the regex, not run] a reorder that inverts two anchors *within* regex 1 (e.g. stating the release step before `then the version`) would fail `re.search` and be killed; and the counter itself declares the lexical layer a shape gate whose bypass is the recorded relation-literal writer (docstring lines 21-24) — M5 sharpens that caveat to the exact phrase-order claim at lines 16-17.

Suggested hardening (for the L1 planner; not applied): pin the PA8 step list with one regex whose separators exclude the other phrases (e.g. `the epoch first\b[^.;]*\bthen the version\b[^.;]*\bthe release only when both`) or assert index(`epoch first`) < index(`absent epoch`) in the collapsed cell.

## Restoration evidence

- After M6: `git -C <clone> checkout c6d4e5ea... -- corpus/knowledge/alpm-package-anatomy-r41.md`; `git -C <clone> diff c6d4e5ea... -- <entry> | wc -l` → `0` (exact pristine bytes).
- Detector on restored bytes: counter at `--revision c6d4e5ea...` → `PASS, exit 0`, all predicate fields green (`branch_tip` at that run was M6's sha; V still landed, bind succeeded).
- Lane untouched (before/after hashes identical): `sha256sum corpus/knowledge/alpm-package-anatomy-r41.md` → `3974e8a7cf0f6ef2d8e120dc6f336971eeecc3d4d18511775da4485e10508702` both before the first edit and after the last run; `sha256sum tools/check-package-anatomy-r41.py` → `c83e29a4...` (declared); lane HEAD `71851d636ab1bffaf8fee5016617c88878a666f1` unchanged; `git status --porcelain` on both paths → `0` lines. All mutations lived and died inside the scratch clone.

## Receipts and bounds

- Receipts: `.ufo/waves/round-41/w1/C2MutEntry/runs.jsonl` (8 records: baseline, M1-M6, restored — shas, commands, predicate fields, per-rule reasons) and `.ufo/waves/round-41/w1/C2MutEntry/mutations.txt` (exact old→new strings, fixture-verdict template, restoration hashes).
- No tools installed (python3 + git sufficed). No C1 census runs, no other entries mutated, no lane file touched, no host mutation; all git-mutating commands ran only in the scratch clone.
- Scratch `/fast/scratch/hyaku/tsukuroi-r41/C2MutEntry` removed after receipts were written (nothing cited below survives there; everything cited is reproduced in the receipts or re-runnable by the recorded commands).
