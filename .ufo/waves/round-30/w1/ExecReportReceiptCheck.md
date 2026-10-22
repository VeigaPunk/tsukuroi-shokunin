Done — added `tools/check-report-receipts.py` as a patch and full file copy; it detects the round-29 unreceipted gate citations and exits 1.

1. [obs] The tool reads the report as a plain file, extracts `Gates at <hex>` table rows and cited rows in a `Before → after` section, then checks committed wave blobs at the selected lane revision using read-only `rev-parse`, `ls-tree` and `show`. Git children use the round-30 child environment contract. Implementation: `/fast/scratch/hyaku/tsukuroi-r30/ExecReportReceiptCheck/repo/tools/check-report-receipts.py:1-10,103-191,238-363,413-449`. Delivered patch: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/ExecReportReceiptCheck/ExecReportReceiptCheck.patch:1-6`; full copy: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/ExecReportReceiptCheck/files/tools/check-report-receipts.py`. The source and full copy both have SHA-256 `0a43534664c03d924f98568a97339a4a64570a3a36ff7eb70afb9188f2ec8a35` (`sha256sum`, exit 0). The lane working tree was not edited.

2. [obs] The requested selftest passes both fixture reports, covering a receipted gate and unreceipted before/after measurements. Command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 tools/check-report-receipts.py --selftest`; exit 0; output: `{"cases": 2, "failures": [], "passed": 2, "selftest": "PASS"}`.

3. [obs] The required round-29 report run fails with exit 1 and returns `receipted:false` for all seven rows under "Gates at 434a7903"; this includes `check-self-assessment`, the defect called out in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-29-verifier-spotcheck.md:26-29`. The run also reports 18 other revision/tool pairs unreceipted under the content rule. Exact command and output:

`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 tools/check-report-receipts.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-29/tsukuroi.md --lane /fast/scratch/hyaku/tsukuroi-r30/ExecReportReceiptCheck/repo --revision 8976ca92ec3c2e6a2aef07b7065a24ff84a1291b`

```text
{"receipt": null, "receipted": false, "revision": "434a7903", "tool": "check-self-assessment"}
{"receipt": null, "receipted": false, "revision": "434a7903", "tool": "check-registry-coverage"}
{"receipt": null, "receipted": false, "revision": "434a7903", "tool": "check-memory-pressure"}
{"receipt": null, "receipted": false, "revision": "434a7903", "tool": "check-storage-health"}
{"receipt": null, "receipted": false, "revision": "434a7903", "tool": "check-owed-statements-r29"}
{"receipt": null, "receipted": false, "revision": "434a7903", "tool": "probe-git-env-leak"}
{"receipt": null, "receipted": false, "revision": "434a7903", "tool": "sources census"}
{"receipt": null, "receipted": false, "revision": "06e00daf", "tool": "check-self-assessment"}
{"receipt": null, "receipted": false, "revision": "06e00daf", "tool": "check-registry-coverage"}
{"receipt": null, "receipted": false, "revision": "06e00daf", "tool": "check-memory-pressure"}
{"receipt": null, "receipted": false, "revision": "06e00daf", "tool": "check-storage-health"}
{"receipt": null, "receipted": false, "revision": "06e00daf", "tool": "check-owed-statements-r29"}
{"receipt": null, "receipted": false, "revision": "06e00daf", "tool": "probe-git-env-leak"}
{"receipt": null, "receipted": false, "revision": "06e00daf", "tool": "sources census"}
{"receipt": null, "receipted": false, "revision": "06e00daf", "tool": "kernel-taint"}
{"receipt": null, "receipted": false, "revision": "06e00daf", "tool": "adjacency-overlap"}
{"receipt": null, "receipted": false, "revision": "06e00daf", "tool": "freshness-r17"}
{"receipt": null, "receipted": false, "revision": "81a061a6", "tool": "tools/check-owed-statements-r29.py"}
{"receipt": null, "receipted": false, "revision": "409ceed4", "tool": "tools/check-owed-statements-r29.py"}
{"receipt": null, "receipted": false, "revision": "75257ea6", "tool": "tools/check-owed-statements-r29.py"}
{"receipt": null, "receipted": false, "revision": "434a7903", "tool": "tools/check-owed-statements-r29.py"}
{"receipt": null, "receipted": false, "revision": "81a061a6", "tool": "tools/probe-git-env-leak.py"}
{"receipt": null, "receipted": false, "revision": "409ceed4", "tool": "tools/probe-git-env-leak.py"}
{"receipt": null, "receipted": false, "revision": "75257ea6", "tool": "tools/probe-git-env-leak.py"}
{"receipt": null, "receipted": false, "revision": "434a7903", "tool": "tools/probe-git-env-leak.py"}
{"cited": 25, "unreceipted": 25}
```

4. [inf] The receipt recognizer is deliberately conservative: it requires the cited revision and tool in a structured tool/command record or named command/tool line, and scans common receipt formats plus receipt-named files. A custom receipt encoding or unusual file extension without a receipt path name could be missed. Relevant implementation: `/fast/scratch/hyaku/tsukuroi-r30/ExecReportReceiptCheck/repo/tools/check-report-receipts.py:238-303`.

LSP availability: [obs] no LSP endpoint or LSP-capable tool was exposed in this session's tool inventory, so no symbol query was available; this is a new standalone script and no existing symbol refactor was needed.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:1140-1153; /home/vgpnk/Projects/shokunin/.ufo/reports/round-29/tsukuroi.md:60-80; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-29-verifier-spotcheck.md:26-29; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-btrfs-space-r30.py; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/_revision.py; wrote=.ufo/waves/round-30/w1/ExecReportReceiptCheck.md, .ufo/waves/round-30/w1/ExecReportReceiptCheck/ExecReportReceiptCheck.patch, .ufo/waves/round-30/w1/ExecReportReceiptCheck/files/tools/check-report-receipts.py; executed=env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 tools/check-report-receipts.py --selftest (exit 0); env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 tools/check-report-receipts.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-29/tsukuroi.md --lane /fast/scratch/hyaku/tsukuroi-r30/ExecReportReceiptCheck/repo --revision 8976ca92ec3c2e6a2aef07b7065a24ff84a1291b (exit 1); sha256sum of implementation and full copy (exit 0)
Model: openai-codex/gpt-6-luna
Installs: none
