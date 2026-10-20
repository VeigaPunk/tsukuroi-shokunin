# RerunHarness

## Findings
- **No new actionable finding in the requested baseline run.** On detached checkout `51dd9eeaa305539fa3cfc6ee275978dc18043b79`, the gate measured `tools_revision=842a5312b704b5cda10fd80ec1fdee5fb381ba97`: `consistent_tools=1/9`, `bound_tools=9/9`, `shared_tools=0`, and `local_rev_regex_copies=9`. Its `status=FAIL`, exit 1, is the expected baseline diagnostic and matches the requested vector. [obs] `.ufo/waves/round-18/build/RerunHarness-tools.txt:1,3`.
- **Selftest:** 40 cases passed, 0 failed, exit 0. [obs] `.ufo/waves/round-18/build/RerunHarness-selftest.txt:1,3`.

## Residual risk
The 1/9 result confirms the baseline deficiency; it does not establish the post-migration 9/9 result or caller migration.

## Verification gaps
No post-integration revision was measured; only the explicitly requested baseline comparison and selftest were run. No host probes or code edits.

Scope: executed=git clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsukuroi-r18-rerun-GwgdGr; git checkout --detach 51dd9eeaa305539fa3cfc6ee275978dc18043b79; git remote remove origin; python3 /tmp/tsukuroi-r18-rerun-GwgdGr/tools/check-revision-binding.py --tools-revision 842a5312b704b5cda10fd80ec1fdee5fb381ba97; python3 /tmp/tsukuroi-r18-rerun-GwgdGr/tools/check-revision-binding.py --selftest