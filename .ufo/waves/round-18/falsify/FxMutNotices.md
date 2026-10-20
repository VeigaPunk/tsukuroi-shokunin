# FxMutNotices — SURVIVES (bounded rejection claim)

Axes: structural discrimination, fixed finding-ID fidelity, exact restoration/isolation.

Own `/tmp/tsukuroi-r18-FxMutNotices.jkpzc9X8` clone used `--no-hardlinks`; checked out `68a8ae035fde33360cbbe21dc92ca0eacf0a5b33`, then removed origin. No production source edits.

Detector: `/usr/bin/python3 -B /tmp/tsukuroi-r18-FxMutNotices.jkpzc9X8/tools/check-appended-notices.py --revision <SHA> --registry corpus/knowledge/statement-corrections-r18.json`.

Pristine: corrections4/4, freshness88/88 across17paths, selftest46/46; all exit0. Four separately committed input mutants:

| Mutant; exact changed location | Commit | Actual output; exit |
|---|---|---|
| `statement-corrections-r18.json:18`: quote becomes `plus 13 named packages (B:59, B:82)` | `6dc8f88` | `NOTICE-QUOTE-DUP` twice; resolved2/4; 1 |
| Same file:6: ID becomes `R18-FRESH-FxMutNotices-01` | `91d038b` | `NOTICE-ID-FAMILY`; resolved0/4; 1 |
| Same file:11: capture becomes `corpus/knowledge/boot-chain-r17.md:1`; matching appended notice reference at `boot-chain-r17.md:194` | `b49f5b9` | `NOTICE-CAPTURE-REF`; resolved3/4; 1 |
| Same two reference locations: capture line59 becomes999999 | `c9b2098` | `NOTICE-CAPTURE-LINE`, “line 999999 beyond EOF=258”; resolved3/4; 1 |

**Killed4; survived0; inconclusive0.** Each inverse restoration was committed and the identical detector passed4/4, exit0. Final restored `f2f80fb921e1a1e8b915e171e7e38d4bbb4fee02`: freshness88/88 and selftest46/46, exit0.

Before=after SHA256:
- Registry: `008d91d46b6582e02ee4376480b796159d6aa43d8e1615cd1d8d0222d319bc91`.
- Notice: `4e5018ca90f40b7687c74f6688f371677b0eaef4e0cba02bebefe08081c8c9a0`.

[Evidence](FxMutNotices-evidence.json) preserves exact full diffs, outputs, mutated hashes, restoration hashes, command arguments and full commits. Committed selftest expectations: checker:693–701,722–729. Beyond-EOF fixed runtime ID:303; a dedicated committed selftest expectation remains **UNPROVEN/not observed**. No fixture/checker weakened. Semantic completeness and admission remain unproven. No installations.

Scope: executed=mktemp -d; /usr/bin/git clone --no-hardlinks --no-checkout, checkout -B master, remote remove origin, commit, rev-parse HEAD, diff (isolated clone); /usr/bin/sha256sum (sandbox subjects); /usr/bin/python3 -B /tmp/tsukuroi-r18-FxMutNotices.jkpzc9X8/tools/check-appended-notices.py --selftest and --revision (exact argv in evidence).
