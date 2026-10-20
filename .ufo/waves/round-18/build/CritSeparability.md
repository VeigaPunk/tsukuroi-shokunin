# CritSeparability — round-18 claim/gate separability attack

Sources: `SCORECARD.md:530-545`, `tools/check-revision-binding.py`, `tools/_revision.py`, `dispatch.json` tasks[9]/[19], `measure/c2-before-842a531.json`.

## Counterexample 1: C2 denominator conflated

`check-revision-binding.py:376` sets `names = TOOLS + extras`; `:396-408` computes `total`, `bound/consistent_tools`, `shared_tools`, `local_rev_regex_copies` over that union; `:411-412` PASSes only when `consistent == total`. `discover()` (`:186-197`) counts any `tools/*.py` containing `"--revision"`. The C1/C3 gate `check-appended-notices.py` (tasks[9]) defines `--revision`, is not `_`-prefixed → at landing `discovered` gains it, `total=10`, and output reads consistent/shared 10/10 — never the claimed 9/9. Baseline JSON shows asymmetry: `discovered=[]`, `total=9` [obs]. `SCORECARD.md:538` promises counts "among original nine… additional discovered tools reported separately"; only `named_total`/`discovered` are separate. Exit 1 can then arise purely from the new gate failing a shared probe (e.g., exit-2 on accepted-tip when the default registry is missing) though all nine are consistent+shared — C2 verdict coupled to C1/C3's counting gate. Selftest blesses this (`:659-672`). Fix: compute claimed counts and grade over `TOOLS` only; keep `discovered` informational.

## Counterexample 2: generic gate enforces no per-claim invariant

tasks[9] requires unique `id`/`notice_heading` only; both R18-CORR and R18-FRESH ids allowed; no unique `baseline_quote`, no defect mapping. Three R18-CORR records reusing quote "13 named packages" under three headings → `resolved_records=3`, exit 0, while the :40-46 and :88 defects stay uncorrected [inf]. Conversely, FRESH records merged into the corrections registry count toward C1. `capture_ref` also accepts any `corpus` path — a record may cite its own target file's appended section (self-authored evidence passes exactness) [inf]. Fixes: unique `baseline_quote` per registry; per-claim `id_prefix`/`path` allowlists; restrict `capture_ref` to `.ufo/waves/*/l1-capture/`.

## Surviving basis

Registries/targets disjoint (`SCORECARD.md:541`, seat map) [obs]; judge keeps independent binding code, no `_revision` import [obs, `:46-47,82`]; `_revision.py:130-148` validates branch first, one id per failure [obs]. Shared-gate binary is a disclosed correlation, not disqualifying. Secondary gap: C1's "existing verdicts preserved" conjunct has no gate coverage (`boot-chain-r17.json` unchecked).

Scope: executed=none
