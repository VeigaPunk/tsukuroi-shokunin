# FreshnessGate — R17 freshness registry gate

**Changed:** `tools/check-freshness-r17.py` (new, 802 lines). No other lane file; no installs.

**Behavior [obs].** `--revision R`: registry `corpus/knowledge/freshness-recheck-r17.json` must be exactly `{schema, records}` (schema `tsukuroi-freshness-recheck-v1`); records exactly the eight contract fields, unique ids `R17-FRESH-NN`, paths `corpus/knowledge/*.md`. Per record: target bytes start with baseline 6923fe0 bytes; `baseline_quote` in baseline and revision; `notice_heading` one Markdown line, exactly once after baseline, absent at baseline; the notice section contains `observed_now` and `capture_ref`; the cited line of the two round-17 captures contains `capture_quote`. `stale_reason` is checked non-empty only. `--registry-from G` reads G's records against R's files, emitting `STALE-UNFLAGGED` where quote is present and heading absent; `--revision 6923fe0… --registry-from <landing>` demonstrates the baseline defect. JSON: status, revision, branch, branch_tip, resolved_records, record_count, findings (+stale_records in compare mode). Exit 0/1/2.

**Binding [obs].** `--revision`/`--registry-from` accept only 7–64 hex (HEAD/@/refs → E-REVISION-INVALID), must be ancestors of `refs/heads/<branch>` (E-REVISION-NOT-LANDED) and of `refs/remotes/origin/<branch>` when present (E-REVISION-NOT-PUSHED); `--branch` defaults master.

**Evidence [obs].** `python3 tools/check-freshness-r17.py --selftest` from a mktemp `git clone` of lane HEAD 6923fe0: `CHECK_FRESHNESS_R17_SELFTEST: PASS (53 cases, 53 passed, 0 failed)`, exit 0; clone removed. The five current notice headings occur exactly once [obs].

**Integration [inf].** The gate reads registry and captures from immutable objects at `--revision`: L1 must commit the merged registry (47 records; two-digit renumbering) and both capture files in the landing commit. The merged registry does not exist yet [unk]; full-mode evaluation is unverified until it lands. No tool installed or upgraded.

Scope: executed=read-only ls,cat,wc,grep,sed,git(log,status,show,for-each-ref,rev-parse,merge-base,clone),python3(spec/fragment reads),mktemp,cp,python3 tools/check-freshness-r17.py --selftest,rm
