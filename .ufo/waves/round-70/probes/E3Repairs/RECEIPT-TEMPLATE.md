# Revision-bound receipt template (round-70 D3 discharge)

Why: `corpus/lessons/round-69-verifier-spotcheck.md` §6 D3 — the r69 report header said "Measured at
`7d7d3aee` … Full outputs: `gates-final.txt`", while `gates-final.txt`'s own internal revision is
`10a01ca`. A receipt that does not name, in its own bytes, the revision it measured cannot discharge a
claim at any revision.

## Template (one receipt per run, plain text, appended never rewritten)

```
RECEIPT <tool> (round <N>)
command: <exact argv, absolute lane path, revision spelled as 40 lowercase hex>
revision_arg: <40 lowercase hex as passed to --revision>
measured_revision: <the full-hex `revision` the tool itself printed>
binding_assert: gate printed revision == measured_revision -> OK | FAIL
tool_sha256_at_revision: <sha256 of `git show <measured_revision>:<tool path>`>
lane_tip_at_run: <`git -C <lane> rev-parse HEAD>` at run time - informational, never the binding>
measured_at_utc: <date -u +%Y-%m-%dT%H:%M:%SZ>
rc: <process exit code of the tool itself, never a pipeline's>
stdout:
<verbatim stdout, byte-for-byte>
stderr:
<verbatim stderr, or (empty)>
```

## Rules this template enforces

1. **The binding is the printed `revision`, not the checkout.** `check-cited-receipts-r62.py` resolves
   its argument through `rev_bind` and prints the full object id; a run made inside a checkout of some
   other tip still proves the named revision. `lane_tip_at_run` is recorded for readability only.
2. **`revision_arg` and `measured_revision` must be equal 40-hex strings.** A short argument
   (`7d7d3aee`) is not a binding: it is resolved, and the resolved hex is what the receipt records.
3. **The tool bytes are bound too.** `tool_sha256_at_revision` is the blob hash at the measured
   revision, so a later tool edit cannot retroactively make the recorded output look like "the same
   gate said PASS".
4. **`rc` is the tool's own exit code.** `… | tail -3` replaces it with `tail`'s 0; the r69
   `after/gates-final.txt` line 43-49 does exactly that and therefore records FAIL bytes under a
   pipeline that exits 0. Receipts here capture the process status directly.
5. **FAIL bytes are kept verbatim.** A failing run's `stdout` is copied whole (findings list included);
   no smoothing, no "known-fail" annotation inside the `stdout:` block.
6. **One revision per receipt.** Two revisions never share a file; the set of receipts for a claim is
   the set of revisions the claim was measured at.

## Filled instances in this directory

| Receipt | Round | Revision measured | Verdict | rc |
|---|---|---|---|---|
| `cited-r69-at-base.txt` | 69 | `84e013a7…` (lane tip at wave start) | PASS, 0 findings, 82 files | 0 |
| `cited-r69-at-decl.txt` | 69 | `1710bd74…` (round-70 declaration) | PASS, 0 findings, 82 files | 0 |
| `cited-r69-at-claimed.txt` | 69 | `7d7d3aee…` (the revision r69's report and SCORECARD cite) | PASS, 0 findings, 82 files | 0 |
| `cited-r69-at-outcome.txt` | 69 | `ea20c862…` (r69 measured-outcome commit) | PASS, 0 findings, 82 files | 0 |
| `cited-r69-at-landing.txt` | 69 | `32c0b50e…` (r69 landing) | **FAIL**, 4 findings, 69 files | 1 |
| `cited-r69-at-repair1.txt` | 69 | `68faae46…` (r69 repair 1) | **FAIL**, 4 findings, 73 files | 1 |
| `cited-r69-at-repair2.txt` | 69 | `10a01ca5…` (r69 repair 2) | **FAIL**, 4 findings, 75 files | 1 |
| `cited-r70-at-base.txt` | 70 | `84e013a7…` | PASS, 0 findings, 9 files, 1 cited path | 0 |
| `cited-r70-at-decl.txt` | 70 | `1710bd74…` | PASS, 0 findings, 9 files, 1 cited path | 0 |

`cited-receipts-jsonl.jsonl` is the same nine runs as one machine-readable line each (tag, round,
`revision_arg`, `measured_revision`, `revision_bound`, tool hash, tip, timestamp, command, rc, counts,
full findings array). `gate-selftest.txt` is `--selftest` (rc 0, 4/4 cases `ok: true`, including
`bad-rev-cannot`: the gate refuses an unresolvable revision rather than reading something else).
