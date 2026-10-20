# BuildNoticeGate

## Deliverable
- [obs] Added `/tmp/tsukuroi-r18-buildnotice.d56seR/repo/tools/check-appended-notices.py` in the isolated clone at baseline `51dd9eeaa305539fa3cfc6ee275978dc18043b79`, then copied it to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/build/files/check-appended-notices.py`.
- [obs] Both source and delivered copy count to 922 lines (`wc -l`); final selftest: `PASS (46 cases, 46 passed, 0 failed)`.

## Behavior and evidence
- [obs] Exact registry schema/baseline, record fields and ID forms: `/tmp/tsukuroi-r18-buildnotice.d56seR/repo/tools/check-appended-notices.py:24-40`.
- [obs] Safe target/capture paths and registry scoping: `/tmp/tsukuroi-r18-buildnotice.d56seR/repo/tools/check-appended-notices.py:71-112`; append-only checks, notices, captures and `distinct_paths`: same file `:230-310`, `:321-429`.
- [obs] Headings may be shared across records; exactly one occurrence is enforced per target file (`/tmp/tsukuroi-r18-buildnotice.d56seR/repo/tools/check-appended-notices.py:251-267`). Positive same-section and cross-file cases, plus duplicate-in-target rejection: same file `:738-768`.
- [obs] All revision binding uses shared `_revision.bind`; missing-registry outcomes and final selftests: `/tmp/tsukuroi-r18-buildnotice.d56seR/repo/tools/check-appended-notices.py:313-318,460-502,651-918`.

## Risks and blockers
- [inf] Structural verifier only, not source-truth or full defect-coverage authority (`/tmp/tsukuroi-r18-buildnotice.d56seR/repo/tools/check-appended-notices.py:1-6`); L1's independent C1 semantic review remains necessary. Freshness coverage is counted from distinct registry paths, not a hardcoded allowlist.
- [unk] No LSP service is mounted in the available tool inventory. The production 88-record registry was not run in this baseline clone; L1 should run the gate after integration. No implementation blocker.

Scope: executed=git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsukuroi-r18-buildnotice.d56seR/repo; git -C /tmp/tsukuroi-r18-buildnotice.d56seR/repo checkout --detach 51dd9eeaa305539fa3cfc6ee275978dc18043b79; git -C /tmp/tsukuroi-r18-buildnotice.d56seR/repo remote remove origin; python3 /tmp/tsukuroi-r18-buildnotice.d56seR/repo/tools/check-appended-notices.py --selftest (45/45 before heading-scope revision, final 46/46 afterward; temporary Git fixtures); rm -rf /tmp/tsukuroi-r18-buildnotice.d56seR/repo/tools/__pycache__; mkdir -p /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/build/files; cp --preserve=mode /tmp/tsukuroi-r18-buildnotice.d56seR/repo/tools/check-appended-notices.py /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/build/files/check-appended-notices.py (initial and refresh); wc -l source and copy (final 922 each)
