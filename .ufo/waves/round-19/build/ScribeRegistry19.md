# ScribeRegistry19 — C3 registry draft

Draft: `.ufo/waves/round-19/build/drafts/ScribeRegistry19.table.md` — heading `## Gate and probe registry — round19 superseding current rows`, one intro paragraph, 17-row 8-column table (13 carried round-18 rows, `revision-binder`, `adjacency-anchors`, `boot-writers`, `registry-coverage`). Not appended to SKILL.md; L1 integrates.

## Corrections to carried rows
1. `update-recheck` verdict: round-18 said "1 failed". The CLI exits 0 (COUNTED/ABSENT) or 2 only [obs `tools/measure-update-recheck.py:434`]; exit 1 comes only from `--selftest` FAIL [obs `:722`, `:729`]. Corrected.
2. `appended-notices`: "baseline842a531" → "baseline 842a531". Full value `842a5312b704…ba97` [obs `tools/check-appended-notices.py:25`, `tools/check-boot-chain.py:68`].
3. `host-census`, `boot-chain-audit`: "not run" now reads "or in round-19 captures". Grep of `l1-capture/` for `tsukuroi-census|boot-chain-audit` found no run line; hits are only quoted text in `adjacency-pointers-r19.json` [obs].

## Unverified
- `freshness-r17` "registry48": no `48` in `tools/check-freshness-r17.py` [obs]; source of the count not located [unk]. Carried verbatim.
- Exit maps for `tsukuroi-census.sh` and `boot-chain-audit.sh` not re-derived here (scouts' scope). Docstring exit maps checked for root-dac, source-scope, locator, section-citations, boot-chain, freshness-r17, seat-scope, revision-binding [obs].

## revision-binder (`tools/_revision.py`)
- Public API: `bind`, `Binding`, `RevisionError`, `branch_tip`, `clean_env` [obs `:134-154`].
- Verdict map: selftest exit 0 PASS, 1 FAIL [obs `:244`, `:248-249`]; no argument exits 64 [obs `:250-252`].
- Importers: 10 [obs grep: appended-notices, boot-chain, freshness-r17, locator-clarification, recheck-commands, root-dac-correction, section-citations, seat-scope, source-scope-correction, measure-update-recheck].
- **Deviation from brief:** write scope is not "none". `bind()` reads only, but `--selftest` creates a git repo under `tempfile` and runs `hash-object -w` there [obs `:180-182`, `:228-230`]. Row says so.

## Tallies and gaps
- No tally copied; cells point to `measure/final/results.json`. Round-18 final ledger contains `selftest-_revision-py.stdout` [obs `.ufo/waves/round-18/measure/final/`].
- The three new tools do not exist in `tools/` yet [obs glob]. Their rows follow the CLI contracts in `spec.json:100`, `:205`, `:250`; cells need checking when executors land the files.
- Coverage arithmetic: 14 files + 3 new = 17; 13 rows + 1 + 3 = 17 [inf].

## Tooling
No tools installed or updated. Answering model: not named.

Scope: executed=none
