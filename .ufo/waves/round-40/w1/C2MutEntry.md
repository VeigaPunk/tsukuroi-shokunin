VERDICT: defect-found

Item C2-11 — mutation-test `tools/check-exec-environment-r40.py` (sha256 `d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d`, verified on the lane working tree and in the scratch clone) against entry mutants of `corpus/knowledge/pacman-exec-environment-r40.md` at lane tip `f951f288483c1af0cef4afd458488b84cf7a2165` (doc pinned at `bf2380503b8e4a5d33162026854b0b7b66d18b86`; byte-identical to tip — `git diff --stat bf23805…f951f288` on that path is empty).

**Headline:** all 50 assigned mutants (a)–(h) across EX1–EX8 were KILLED (counter FAIL, exit 1) — the counter's declared entry checks each fired. 6 extension probes produced 5 SURVIVORS exposing one real coverage gap: S-ids cited in rule cells or host cells are never validated (not for `source:`-line membership, not for existence). Verdict `defect-found` is for that gap; the assigned mutation matrix itself fully supports the counter.

# Method

- Scratch `/fast/scratch/hyaku/tsukuroi-r40/C2MutEntry` (TMPDIR set there; removed at end — observed `[ ! -e ] → SCRATCH-REMOVED`). Never built under /tmp.
- `git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$D"`; `git -C "$D" remote remove origin`; `git -C "$D" rev-parse --show-toplevel` == `$D` (TOPLEVEL-OK); fixture identity `C2MutEntry <fixture@shokunin.local>`, `commit.gpgsign=false`, `core.hooksPath=/dev/null` (clone-local config only).
- Pristine assert: `git -C "$D" show bf23805…:corpus/knowledge/pacman-exec-environment-r40.md | cmp - "$D/corpus/knowledge/…"` → `PRISTINE-MATCHES-PINNED-DOC`; pristine entry sha256 `2230ccaf4037ccfcb8628b97f15fcff9eca86f9e5e37bee1c5392712ce21c9ef`.
- Baselines (before any mutant): `python3 tools/check-exec-environment-r40.py --repo "$D" --revision bf23805…` → `result=PASS exit=0 rules_verified=8 source_ok=1 counts_ok=2 novelty=0`; identical at `--revision f951f288…`. Receipt: `baseline.jsonl` (2 records, full JSON incl. derived values and host values).
- 56 variants: one entry-file mutation each, committed on the clone's master; per commit `git show --name-only --format=` asserted exactly `[corpus/knowledge/pacman-exec-environment-r40.md]`. Counter run per variant: `python3 tools/check-exec-environment-r40.py --repo "$D" --revision <variant sha>`. All 56 runs returned parsed JSON, exit 0 or 1 (no exit-2).
- Receipts: `mutants.jsonl` (56 records: id, description, variant sha, entry sha256 before/after, exact old/new cell text, full per-row reasons). Method: `mutdrive.py`, `addendum.py` (this seat dir).

# Result table (mutant → rules_verified / result)

Assigned matrix, 50/50 killed. `rules_verified` is the counter's count; failing rows listed (collateral rows for shared S-ids noted).

| mutant | mutation | rules_verified | result | failing rows | verdict |
|---|---|---|---|---|---|
| EX1-a | drop token `working directory` | 7 | FAIL | EX1 | killed |
| EX1-b | value `/` → `x` | 7 | FAIL | EX1 | killed |
| EX1-c | util.c:677-687 → 717-727 | 7 | FAIL | EX1 | killed |
| EX1-d | S221 → S216 (held) | 7 | FAIL | EX1 | killed |
| EX1-e | drop S221 from `source:` | 5 | FAIL | EX1,EX2,EX3 | killed |
| EX1-h | insert `not` | 7 | FAIL | EX1 | killed |
| EX2-a | drop token `stdout` | 7 | FAIL | EX2 | killed |
| EX2-b | value `…second socket` → `…second sockeu` | 7 | FAIL | EX2 | killed |
| EX2-c | util.c:659-668 → 699-708 | 7 | FAIL | EX2 | killed |
| EX2-d | S221 → S217 (held) | 7 | FAIL | EX2 | killed |
| EX2-e | drop S221 from `source:` | 5 | FAIL | EX1,EX2,EX3 | killed |
| EX2-h | insert `not` | 7 | FAIL | EX2 | killed |
| EX3-a | drop token `SHLVL` | 7 | FAIL | EX3 | killed |
| EX3-b | value `umask=0022` → `umask=0023` | 7 | FAIL | EX3 | killed |
| EX3-c | util.c:688-698 → 728-738 | 7 | FAIL | EX3 | killed |
| EX3-d | S221 → S208 (held) | 7 | FAIL | EX3 | killed |
| EX3-e | drop S221 from `source:` | 5 | FAIL | EX1,EX2,EX3 | killed |
| EX3-h | insert `not` | 7 | FAIL | EX3 | killed |
| EX4-a | drop token `/usr/bin/bash` (both occurrences) | 7 | FAIL | EX4 | killed |
| EX4-b | value `/usr/bin/bash` → `/usr/bin/basi` | 7 | FAIL | EX4 | killed |
| EX4-c | PKGBUILD:113-115 → 153-155 | 7 | FAIL | EX4 | killed |
| EX4-d | S220 → S216 (held) | 7 | FAIL | EX4 | killed |
| EX4-e | drop S220 from `source:` | 7 | FAIL | EX4 | killed |
| EX4-h | insert `not` | 7 | FAIL | EX4 | killed |
| EX5-a | drop token `tmp/alpm_XXXXXX` | 7 | FAIL | EX5 | killed |
| EX5-b | value `.INSTALL` → `.INSTALM` | 7 | FAIL | EX5 | killed |
| EX5-c | trans.c:360-377 → 400-417 | 7 | FAIL | EX5 | killed |
| EX5-d | S222 → S217 (held) | 7 | FAIL | EX5 | killed |
| EX5-e | drop S222 from `source:` | 6 | FAIL | EX4,EX5 | killed (EX4 collateral: its source cell also cites S222) |
| EX5-h | insert `not` | 7 | FAIL | EX5 | killed |
| EX6-a | drop token `NeedsTargets` (both occurrences) | 7 | FAIL | EX6 | killed |
| EX6-b | value `one per line` → `one per linf` | 7 | FAIL | EX6 | killed |
| EX6-c | hook.c:519-526 → 559-566 | 7 | FAIL | EX6 | killed |
| EX6-d | S223 → S208 (held) | 7 | FAIL | EX6 | killed |
| EX6-e | drop S223 from `source:` | 5 | FAIL | EX6,EX7,EX8 | killed |
| EX6-h | insert `not` | 7 | FAIL | EX6 | killed |
| EX7-a | drop token `Depends` (both occurrences) | 7 | FAIL | EX7 | killed |
| EX7-b | value `dependencies` → `dependenciet` | 7 | FAIL | EX7 | killed |
| EX7-c | hook.c:507-517 → 547-557 | 7 | FAIL | EX7 | killed |
| EX7-d | S223 → S216 (held) | 7 | FAIL | EX7 | killed |
| EX7-e | drop S223 from `source:` | 5 | FAIL | EX6,EX7,EX8 | killed |
| EX7-h | insert `not` | 7 | FAIL | EX7 | killed |
| EX8-a | drop token `file list` | 7 | FAIL | EX8 | killed |
| EX8-b | value `NoExtract` → `NoExtracu` | 7 | FAIL | EX8 | killed |
| EX8-c | hook.c:258-279 → 298-319 | 7 | FAIL | EX8 | killed |
| EX8-d | S223 → S217 (held) | 7 | FAIL | EX8 | killed |
| EX8-e | drop S223 from `source:` | 5 | FAIL | EX6,EX7,EX8 | killed |
| EX8-h | insert `not` | 7 | FAIL | EX8 | killed |
| EX2-f | rule cell `stdout` → `stdin` | 7 | FAIL | EX2 | killed |
| EX3-g | rule cell only `0022` → `0077` (value cell untouched) | 7 | FAIL | EX3 | killed |

Extension probes (6 runs, 5 survivors):

| mutant | mutation | rules_verified | result | verdict |
|---|---|---|---|---|
| EX1-d2 | EX1 S221→S216 in source cell **and** S216 added to `source:` header | 7 | FAIL | killed — `no new mined upstream row for util.c (54d9411) naming the entry`, plus `source_ok=0` |
| EX4-a2 | drop FIRST `/usr/bin/bash` occurrence only (duplicate remains) | 8 | PASS | **SURVIVOR** |
| EX4-e2 | drop S219 from `source:` (S219 cited only in EX4's rule cell) | 8 | PASS | **SURVIVOR** |
| EX6-e3 | drop S225 from `source:` (S225 cited only in EX4/EX6 host cells) | 8 | PASS | **SURVIVOR** |
| EX4-e4 | EX4 rule cell `S219` → bogus `S999` | 8 | PASS | **SURVIVOR** |
| EX4-e5 | EX4 host cell `S225` → bogus `S999` | 8 | PASS | **SURVIVOR** |

Every survivor ran with `source_ok=1 counts_ok=2 duplicate_rows=0 duplicate_headings=0 novelty_base_hits=0` (receipts `mutants.jsonl`, records `EX4-a2`…`EX4-e5`).

# Survivors — analysis

1. **EX4-a2 (expected under stated semantics, not a defect).** The rule cell became "Arch builds pacman with `` `-Dscriptlet-shell=` `` so every install scriptlet runs as `` `/usr/bin/bash -c …` ``" — the token `/usr/bin/bash` is still present via the second occurrence, so the presence-based token check (`tools/check-exec-environment-r40.py:282-286`, `missing_tok = [t for t in TOKENS[ex] if t not in rule]`) still holds, and the mutated rule still literally states the fact. Recorded for completeness; no action.
2. **EX4-e2 / EX4-e4 (defect: rule-cell citations unvalidated).** EX4's rule cell cites `S219 meson_options.txt:17` (bf23805:corpus/knowledge/pacman-exec-environment-r40.md:24). The counter collects S-ids from the **source cell only** (`tools/check-exec-environment-r40.py:294-296`, `ids = ['S' + x for x in SID_RE.findall(src_cell)]`) and validates `source_ok` from the **`source:` header only** (`:259-263`). Consequence, demonstrated twice: (e2) the header may silently drop a source the rule still cites (`source: S219, …` → `source: S220, …`, PASS); (e4) the rule cell may cite a **nonexistent** id (`S219` → `S999`, PASS) — no existence check, no header-membership check.
3. **EX6-e3 / EX4-e5 (defect: host-cell citations unvalidated).** S225 (the own-work capture row; status `mined`, opened 2026-10-26, used_by this entry — `git show bf23805…:corpus/SOURCES.md`) is cited in EX4's and EX6's host cells (entry:24, :26). Host cells are read only for the two `counts_ok` substrings (`tools/check-exec-environment-r40.py:322-327`). Dropping S225 from the header (e3) or replacing it with bogus `S999` in the host cell (e5) both PASS.
4. **EX1-d2 (the upstream-row conjunction works beyond header membership).** With S216 legitimately on the header, the row still fails: S216/S217/S208 are base-registry rows (`git -C <lane> show 53b294a…:corpus/SOURCES.md | grep -cE '^\| S(208|216|217) \|'` → `3`) whose `used_by` names the round-38/39 entries, so `i not in base_ids` and `ENTRY_NAME in used_by` both reject them (`tools/check-exec-environment-r40.py:297-304`). Held-row swaps cannot be laundered through the header.

Severity: **low**. The factual content of rule and host cells remains fully checked (value :280-281, tokens :282-286, polarity :287-289, paraphrase :290-293, quote-at-cited-lines :299-317, counts :322-327); the gap only lets an entry cite sources in rule/host cells that are undeclared on `source:` or nonexistent — provenance decoration is unchecked there. This is outside the counter's declared scope (docstring :22-34 covers source-cell citations), so it is a coverage finding, not a violation of a stated invariant; the C2 entry's claims themselves are not falsified.

Exact proposed hardening text (for the planner; baseline-compatible — at bf23805 every rule-cell id (S219) and host-cell id (S225) is on the header, `mined`, and used-by the entry, so the predicate is unchanged):

> In the row loop, also collect S-ids from the rule and host cells (`SID_RE.findall(rule) + SID_RE.findall(host_cell)`) and require each to (i) appear on the entry's `source:` line and (ii) be a `corpus/SOURCES.md` row at <REV> with status `mined` whose used-by names the entry (own-work rows allowed for host-cell ids); otherwise append a reason to that row.

# What the kills establish

Each declared entry check fired on the assigned matrix (all reasons quoted verbatim from the counter's JSON, receipts `mutants.jsonl`): value check (8 kills, type b), token check (10 kills: a ×8, f, g), polarity check (8 kills, type h), quote-at-cited-lines check (8 kills, type c), header membership (16 kills: d ×8 + e ×8; e-mutants show the expected collateral on rows sharing the id — EX1/2/3 share S221, EX4+EX5 share S222 via EX4's source cell, EX6/7/8 share S223), upstream-row conjunction (9 kills: d ×8 + d2). `counts_ok`, `duplicate_rows`, `duplicate_headings`, `novelty_base_hits` stayed at their baseline values (2/0/0/0) in all 56 runs. Baseline PASS at both `bf23805…` and `f951f288…` (receipt `baseline.jsonl`).

# What I did not do

- Did not mutate `corpus/SOURCES.md` rows, the counter script, the frozen snapshots, or the capture — item scope is entry mutants only.
- Did not test line-range shifts other than +40, token drops other than `TOKENS[ex][0]` (plus the EX4-a2 single-occurrence variant), or value changes at non-final positions (the value comparison is full-string equality, `:280-281`, so position is immaterial — analytic, not run).
- Did not exercise counter exit-2 paths (binding/frozen-input failures) — out of scope.
- Did not run the C1 census or counter, any pacman transaction, or any host mutation. No tools installed (operator tooling authorization unused; nothing to record).

# Restoration evidence

- Lane HEAD before and after: `f951f288483c1af0cef4afd458488b84cf7a2165` (`git rev-parse HEAD`, observed at session start and after cleanup).
- Lane entry file sha256 before and after: `2230ccaf4037ccfcb8628b97f15fcff9eca86f9e5e37bee1c5392712ce21c9ef` (never written by this seat).
- Lane counter sha256: `d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d` (declared value, re-verified).
- Lane `git status --porcelain` after cleanup: identical pre-existing set (1 modified dispatch script + untracked wave artifacts); this seat wrote only `.ufo/waves/round-40/w1/C2MutEntry.md` and `.ufo/waves/round-40/w1/C2MutEntry/`.
- All 56 mutants lived only in the scratch clone (`/fast/scratch/hyaku/tsukuroi-r40/C2MutEntry/clone`, 56 commits on its master, fixture identity `C2MutEntry <fixture@shokunin.local>`); per-variant entry blob sha256s are in `mutants.jsonl`. Scratch removed after receipts were archived (observed `SCRATCH-REMOVED`).

# Receipts (this seat dir)

- `baseline.jsonl` — 2 full counter records (bf23805, f951f288).
- `mutants.jsonl` — 56 records (id, description, variant sha, entry sha256 before/after, exact old/new cell text, full per-row reasons).
- `mutdrive.py`, `addendum.py` — the drivers that produced the above.
