Verdict: DRAFTS READY; frozen C2 mirror passes all four repairs (ROUTED_STALE=0 ROUTED_OK=4/4, rc 0).
Unchecked: L1 landing and committed-revision scoring; this seat changed no production repair target.

# E2Routed — round 75 w1

Axes: freshness (C2). The restated scores are depth 8, coverage 9, operability 9,
freshness 9, calibration 9, adjacency 8; no ordinal uplift or no-harm certification.

## Evidence and bounds

- Declaration: `1e2bb29cb452d49822e35ada0f5fad419b19e24c`; initial `git rev-parse HEAD` matched.
- Base: `a21302a48d24cf5242ac2a66cc5b5b453f7a1b20`; `git cat-file -t` returned `commit`, rc 0.
- Frozen checker SHA256: `4b5c801ce4be7ea7562d9b472ce58badcd113d1062280220500275730f567d2c`.
- Frozen JT counter SHA256 (measured only, not exercised): `5e87238ce6909823797446b5be79194e2f701de46d3c4087ca75f289fca8cd71`.
- Checker `--selftest` closing line: `SELFTEST: PASS (13 cases, 13 passed, 0 failed)`; rc 0.
- Checker `--revision a21302a48d24cf5242ac2a66cc5b5b453f7a1b20`: `ROUTED_STALE=4 ROUTED_OK=0/4`; rc 1.
  Death, wording and sweep findings were `reason=token`; axes finding was `reason=heading`.
- `wc -c /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-74/w1/SC3Index/report.md`
  returned `27552` bytes, rc 0.
- Read the two original repair targets before drafting; exact closure obligations are
  `corpus/lessons/round-74-verifier-spotcheck.md` section 7, items 1–4.
- LSP definition/reference/refactor tools are unavailable in this seat's mounted tool inventory.
  No symbol implementation was changed; these are append-only prose drafts.
- No installs, git/jj mutations, host-state changes or production file edits. No child agents.
  The only retained lane write is this exclusive report.
- Process deviation: initial selftest did not explicitly set TMPDIR; subsequent counting and
  fixture subprocesses set TMPDIR to the seat scratch. Initial finite Bash calls supplied names,
  causing the tool to classify them as supervised services; all exited immediately (rc 0 wrappers),
  none remains running. Actual checker return codes above came from captured RC lines, not wrappers.
  Tool mismatch reported through the issue device. Godspeed skill was loaded after initial reads/runs.

## Four verbatim append blocks

Append each fenced block's contents, not its fence, with one blank separator after existing text.
The mirror was assembled from the three declaration-revision blobs, not concurrently changing files.

### Draft a — corpus/lessons/round-74.md (first append)

```markdown
## Correction (round 75, R74-DEATH-RECEIPT-MISSING)

SC3Index failed with provider 429 / RESOURCE_EXHAUSTED. No death receipt was
committed for that seat. This correction supersedes any implication that the
round-74 committed receipt set records that death; it does not manufacture a
historical death receipt or relabel the seat successful.
```

### Draft b — corpus/lessons/round-74.md (second append)

```markdown
## Correction (round 75, R74-REPORT-WORDING)

The accurate statement is: no review-accepted drafts. The existing
`.ufo/waves/round-74/w1/SC3Index/report.md` is 27,552 bytes (`wc -c`, measured
by E2Routed in round 75); `w1/SC3Index/report.md` is not absent. This correction
supersedes wording that conflates lack of review-accepted drafts with lack of
a report. Existence and size do not establish review acceptance.
```

### Draft c — .ufo/waves/round-74/w1/E3HostProbe/receipt-g-landing.txt

```markdown
## Correction (round 75, R74-SWEEP-RESIDUE)

The Base commit header above quotes the fabricated full OID
`d749a625f483c66f2a6f2005db3799630c776bc3`. The real round-74 base is
`d749a625b3054b7cb3435983fb9626ab3d0ed0c4`. This correction supersedes that
header's identity claim only; it does not retroactively authenticate runs
against the fabricated OID or replace the historical receipt bytes.
```

### Draft d — SCORECARD.md

```markdown
## Round 75 — axes table restated

This table supersedes the round-65 axes table as the current restatement; all six ordinal scores remain inherited, with no uplift or fresh certification.

Counts below were measured by E2Routed at declaration `1e2bb29cb452d49822e35ada0f5fad419b19e24c`; these inventory proxies do not establish deserved ordinal scores, operational health, source freshness, or recipient acceptance.

| Axis | Score | Measured count | Counting command |
|---|---|---|---|
| depth | 8 | 92 Markdown knowledge notes | `python3 -c 'import subprocess; s=subprocess.check_output(["git", "-C", "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin", "ls-tree", "--name-only", "1e2bb29cb452d49822e35ada0f5fad419b19e24c:corpus/knowledge"],text=True); print(sum(x.endswith(".md") for x in s.splitlines()))'` |
| coverage | 9 | 3 Core, Frontier and Adjacent handoff headings | `python3 -c 'import subprocess; s=subprocess.check_output(["git", "-C", "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin", "show", "1e2bb29cb452d49822e35ada0f5fad419b19e24c:PROVINCE.md"],text=True); print(sum(s.count(x) for x in ("## Core\n", "## Frontier\n", "## Adjacent — finding-to-owner handoffs\n")))'` |
| operability | 9 | 113 tracked tools entries (inventory, not execution health) | `python3 -c 'import subprocess; s=subprocess.check_output(["git", "-C", "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin", "ls-tree", "--name-only", "1e2bb29cb452d49822e35ada0f5fad419b19e24c:tools"],text=True); print(len(s.splitlines()))'` |
| freshness | 9 | 313 source registry rows (inventory, not re-verification) | `python3 -c 'import subprocess; s=subprocess.check_output(["git", "-C", "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin", "show", "1e2bb29cb452d49822e35ada0f5fad419b19e24c:corpus/SOURCES.md"],text=True); print(sum(x.startswith(chr(124)+" S") and x.split()[1][1:].isdigit() for x in s.splitlines()))'` |
| calibration | 9 | 107 numbered QUALITY criteria (inventory, not enforcement) | `python3 -c 'import subprocess; s=subprocess.check_output(["git", "-C", "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin", "show", "1e2bb29cb452d49822e35ada0f5fad419b19e24c:corpus/QUALITY.md"],text=True); print(sum(x.split(".",1)[0].isdigit() for x in s.splitlines()))'` |
| adjacency | 8 | 7 ADJ handoff rows (not recipient acknowledgement) | `python3 -c 'import subprocess; s=subprocess.check_output(["git", "-C", "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin", "show", "1e2bb29cb452d49822e35ada0f5fad419b19e24c:PROVINCE.md"],text=True); print(sum(x.startswith(chr(124)+" ADJ-") for x in s.splitlines()))'` |
```

## Counting receipt

Each row's exact backticked command above was executed by this seat with the declaration OID
embedded in git arguments; all six returned rc 0 with empty stderr. These are inventory counts,
not proof of semantic completeness or deserved axis scores. Depth filters `.md` knowledge notes;
operability deliberately labels all tracked tools entries rather than asserting runnable health.

- depth: stdout `92`, rc 0.
- coverage: stdout `3`, rc 0.
- operability: stdout `113`, rc 0.
- freshness: stdout `313`, rc 0.
- calibration: stdout `107`, rc 0.
- adjacency: stdout `7`, rc 0.

## Mirror and isolated tamper receipts

Mirror source hashes (SHA256 of pinned declaration blob UTF-8 bytes):

- `corpus/lessons/round-74.md`: `f1145d73968b48adaca37940ec99e79e9073a78f31e1db4dfb5b19951ff72ebd`.
- `.ufo/waves/round-74/w1/E3HostProbe/receipt-g-landing.txt`: `d7c0bff1826951bca142f386462789e2b88750c7371c5b8edf51f085f2d12bad`.
- `SCORECARD.md`: `3f7fad6efd8d0b47294d4f789a50185bdcfb9f40ee0326704856e3502e840048`.

Exact argv, stdout, stderr and exit code follow. TMPDIR was the E2Routed scratch root.

```json
{
  "mirror": {
    "argv": [
      "python3",
      "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-r74-routed-r75.py",
      "--root",
      "/fast/scratch/hyaku/tsukuroi-r75/E2Routed/mirror"
    ],
    "stdout": "ROUTED_STALE=0 ROUTED_OK=4/4\n",
    "stderr": "",
    "rc": 0
  },
  "heading-only": {
    "argv": [
      "python3",
      "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-r74-routed-r75.py",
      "--root",
      "/fast/scratch/hyaku/tsukuroi-r75/E2Routed/heading-only"
    ],
    "stdout": "ROUTED_STALE=1 ROUTED_OK=3/4\nR74-DEATH-RECEIPT STALE reason=need path=corpus/lessons/round-74.md missing_any=['RESOURCE_EXHAUSTED', '429']\n",
    "stderr": "",
    "rc": 1
  },
  "distant-token": {
    "argv": [
      "python3",
      "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-r74-routed-r75.py",
      "--root",
      "/fast/scratch/hyaku/tsukuroi-r75/E2Routed/distant-token"
    ],
    "stdout": "ROUTED_STALE=1 ROUTED_OK=3/4\nR74-DEATH-RECEIPT STALE reason=need path=corpus/lessons/round-74.md missing=SC3Index\n",
    "stderr": "",
    "rc": 1
  },
  "axes-no-command": {
    "argv": [
      "python3",
      "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-r74-routed-r75.py",
      "--root",
      "/fast/scratch/hyaku/tsukuroi-r75/E2Routed/axes-no-command"
    ],
    "stdout": "ROUTED_STALE=1 ROUTED_OK=3/4\nR74-STALE-AXES-TABLE STALE reason=command path=SCORECARD.md axis=depth\n",
    "stderr": "",
    "rc": 1
  }
}
```

Tamper construction (each starts from the independently passing mirror):

1. Heading-only: replace the first lesson correction with only its exact heading; retain
   the report-wording block. The latter mentions SC3Index, so the isolated failure is missing
   provider class (`missing_any=['RESOURCE_EXHAUSTED', '429']`).
2. Distant token: replace that block with its heading, 85 `filler line` lines, then the actual
   SC3Index/class/missing-receipt statement. Required content is beyond the frozen 80-line window;
   the isolated failure is `missing=SC3Index`.
3. Axes without command: remove only the depth row's backticked command, substitute `command removed`;
   isolated failure is `reason=command path=SCORECARD.md axis=depth`.

All three returned `ROUTED_STALE=1 ROUTED_OK=3/4`, rc 1. The positive mirror returned
`ROUTED_STALE=0 ROUTED_OK=4/4`, rc 0. No checker changes were made.

## Handoff, risk and retention

L1 can append the four verbatim blocks above byte-for-byte, preserving historical text, then run
`python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-r74-routed-r75.py --revision <landing-oid>`.
The lexical checker establishes structural closure only. It does not validate all scores, source
truth or historical runs. First-match token and heading behavior remains frozen; these fixtures
prove the declared boundaries without claiming a general semantic checker.

M1Mutation-9 copied the immutable positive mirror into its own scratch and confirmed the copy;
no mutation of this seat's fixture was authorized. Receipts and exact drafts are retained in this
report before removal of the exclusive scratch tree. No sibling implementation file was edited.

Self-evaluation: accuracy 4 (structural, not semantic acceptance); completeness 5 (four exact drafts,
base/selftest, six commands, positive and three negative controls); clarity 4 (long commands are
needed for immutable, table-safe replay); actionability 5 (byte-for-byte append blocks); conciseness 4
(verbatim receipts enlarge the report). Mean 4.4/5. Highest-impact next step is the parent's committed
revision gate, not another fixture rerun. User agreement expected on explicit milestone boundaries.
