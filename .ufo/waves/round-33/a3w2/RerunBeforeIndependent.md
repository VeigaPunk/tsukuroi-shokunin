# RerunBeforeIndependent — C1 before-receipt independent re-run (round 33, attempt 3, wave a3w2)

DOES NOT MEET the C1 after-value: the independent re-run of the before (do-nothing control) at the frozen
commit scored `leaking` 15 of `pairs` 15, `harness_errors` empty, exit 1 — and it agrees with the wave a3w1
control receipt on every deterministic field.

## Findings

1. Rerun summary [obs]: `revision` `9c89ff4f093d07a6f92925518310ca6a7c8a2fa0`, `targets` 5,
   `channels` [names, quiet, source], `pairs` 15, `leaking` 15, `harness_errors` [],
   `probe_sha256` `c24f344b864a13ea4db2909bfa81de77f8f41bae35cd5e0949a88b28ab1e04cd` (the frozen probe sha),
   `probe_version` 3, `target_set` `claim`, `predicate_label` `leaking`.
   Footer: `exit_code` 1, `timed_out` false, `finished_utc` `2026-10-23T07:37:25Z`.
   Evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w2/RerunBeforeIndependent/before-rerun.jsonl` (18 lines: 1 receipt header, 15 pair rows, 1 summary, 1 footer).

2. Agreement with a3w1 control [obs]: field-by-field comparison of
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/C01Before/before-claim.jsonl`
   (`finished_utc` `2026-10-23T07:08:34Z`) vs the rerun — identical on `revision`, `targets`, `channels`,
   `pairs` (15), `leaking` (15), `harness_errors` ([]), `probe_sha256`, `probe_version`, `target_set`,
   `predicate_label`, and the `leaking_pairs` list (all 15 pairs, all channels, all five tools, in the same
   order). Footer identical on `exit_code` 1 and `timed_out` false. [inf] Only the intentionally random
   fields differ: per-run `injected_names`/`injected_named`, `scratch` path, and `finished_utc`.

3. Per-pair runtime evidence identical [obs]: control and channel exit codes 0, git-exec counts
   `_revision.py` 279/279, `check-adjacency-anchors.py` 335/335, `check-boot-writers.py` 203/203,
   `check-root-dac-correction.py` 226/226, `mutants-owed-statements-r29-v4shapes.py` 1176/1176 — every
   names and quiet run `leak` true, and `channel_stdout_sha256` digests match the a3w1 receipt exactly
   (73a13dec7936…, de03db093feb…, d5fa01c8a3a2…, 0d421c166a2c…, 6e1d9dd61df6…), so the traced stdout bytes
   reproduced bit-for-bit across the two independent receipts.

4. Source-channel findings identical [obs]: the same single finding per tool —
   `tools/_revision.py:63 ambient-read .environ` (for `_revision.py`, `check-adjacency-anchors.py`,
   `check-boot-writers.py`, `check-root-dac-correction.py`, whose scans include `_revision.py`) and
   `tools/mutants-owed-statements-r29-v4shapes.py:37 ambient-read .environ`. No extra findings, none missing.

5. [inf] This confirms the counter's discrimination at the base: an unchanged lane (do-nothing control)
   is rejected 15/15 with zero harness errors, so a claimed change must move every names, quiet and source
   pair to reach `leaking` 0; the predicate cannot be met by a control that does nothing. The rerun also
   confirms the receipt is reproducible: an independent seat, a second run of `tools/run-receipt.py` against
   the same frozen `--revision`/`--tool-revision`, produced a byte-for-byte identical decision.

6. [unk] Per-pair evidence fields under `names`/`quiet` (which injected name or ambient NAME=VALUE string
   fired per exec) were compared only at the `leak` level; the injected names themselves are `os.urandom`
   per run and cannot repeat. Nothing in the receipts indicates nondeterminism in the counted result.

Scope: read=SCORECARD.md declaration at 9c89ff4 (C1 section, amendments 1–2), a3w1 control receipt before-claim.jsonl, rerun receipt before-rerun.jsonl; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w2/RerunBeforeIndependent/before-rerun.jsonl, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w2/RerunBeforeIndependent.md; executed=tools/run-receipt.py as the C1 counting command at --revision 9c89ff4f093d07a6f92925518310ca6a7c8a2fa0 --tool-revision 9c89ff4f093d07a6f92925518310ca6a7c8a2fa0 (253 s wall), plus read-only python3 JSON comparisons
Model: not exposed
Installs: none
