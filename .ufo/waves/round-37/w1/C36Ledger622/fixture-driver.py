#!/usr/bin/env python3
"""Seat C36Ledger622 (round-37 w1, C3 falsification item 6/8) hermetic fixtures.

Reproduces the four observed round-37 self-assessment states against the
UNCHANGED checker (tools/check-self-assessment.py, K01-K27), using the
module's own fixture machinery (fixture_files("clean") as the base lane).
No lane file, lane Git/jj state, or host state is touched: every fixture is
a fresh mktemp repo driven through `git -C`, and the top level is verified
to equal the fixture root before any commit (lane fixture rule).

Variants (census selftest prints 3 cases in the fixture lane):
  V1 k17-absent-path   d06cedb state: last capabilities table cites `after.md`
                       and `selftest-after.json`/`mode-policy-mutant.json`,
                       absent at the revision        -> K17+K18 mismatch, exit 1
  V2 k17-no-case-count ee36f9e state: corrected rows dropped the case count
                                                      -> K17 mismatch, exit 1
  V3 k16-row-lost      5124bf3 state: `###`-append of a one-row table inside
                       the same `## Capabilities` section makes the LAST
                       table lack sources-registry   -> CANNOT_EVALUATE, exit 2
  V4 correction-proposed 0e5f70f-shaped repair: one new `## Capabilities`
                       section whose LAST table holds all four rows and
                       states the measured case count -> exit 0, 0 mismatches
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"

spec = importlib.util.spec_from_file_location(
    "csa", os.path.join(LANE, "tools", "check-self-assessment.py"))
csa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(csa)


def git_env():
    return csa.git_env()


V1_TABLE = """
## Capabilities — corrected counts table

Correction appendix: the preceding capability rows are superseded by this table;
paths below are known present except where marked historical.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates `corpus/SOURCES.md` | `corpus/SOURCES.md` | r1 |
| host-census-gate | Emits a verdict with a hermetic `--selftest` | `tools/tsukuroi-census.sh --selftest` prints PASS 3/3 rc=0; historical receipts `corpus/knowledge/one.md` and `after.md` | r1 |
| root-metadata-observer | Observes root mode | `corpus/knowledge/one.md`, `selftest-after.json`, `mode-policy-mutant.json` | r1 |
| boot-chain-audit | Audits boot entries | `tools/boot-chain-audit.sh` | r1 |
"""

V2_TABLE = """
## Capabilities — current

Correction appendix: the preceding capability rows are superseded by this table;
paths below are individually backticked and known present at this revision.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates `corpus/SOURCES.md` | `corpus/SOURCES.md` | r1 |
| host-census-gate | Emits a verdict with a hermetic census selftest | `tools/tsukuroi-census.sh` | r1 |
| root-metadata-observer | Observes root mode | `corpus/knowledge/one.md` | r1 |
| boot-chain-audit | Audits boot entries | `tools/boot-chain-audit.sh` | r1 |
"""

V3_APPEND = """
### Correction appendix capability evidence (append-only)

K17 requires the current host-census-gate capability row to state the selftest
case count. The operative host-census-gate row above is superseded by this row;
its cited paths are unchanged and present.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| host-census-gate | Emits a verdict with a hermetic selftest that prints PASS (3 cases, 3 passed, 0 failed) | `tools/tsukuroi-census.sh` | r1 |
"""

V4_TABLE = """
## Capabilities — complete current table (appendix round)

This full table supersedes the partial correction rows above; all four capability
rows are retained and their evidence paths are explicit. The case count is
measured at the recorded revision.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates `corpus/SOURCES.md` | `corpus/SOURCES.md` | r1 |
| host-census-gate | Emits a verdict with a hermetic selftest that prints PASS (3 cases, 3 passed, 0 failed) | `tools/tsukuroi-census.sh` | r1 |
| root-metadata-observer | Observes root mode | `corpus/knowledge/one.md` | r1 |
| boot-chain-audit | Audits boot entries | `tools/boot-chain-audit.sh` | r1 |
"""


def build_variant(name, scorecard_append):
    files, _ = csa.fixture_files("clean")
    files["SCORECARD.md"] = files["SCORECARD.md"] + scorecard_append
    repo = os.path.join(root, name)
    os.makedirs(repo)
    env = git_env()
    subprocess.run(["git", "init", "-q", repo], check=True, env=env)
    # Lane fixture rule: verify top level equals fixture root before any commit.
    top = subprocess.run(["git", "-C", repo, "rev-parse", "--show-toplevel"],
                         check=True, capture_output=True, text=True, env=env).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(repo):
        raise SystemExit("fixture top-level %r != fixture root %r" % (top, repo))
    for path, text in files.items():
        full = os.path.join(repo, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as handle:
            handle.write(text)
    subprocess.run(["git", "-C", repo, "add", "-A"], check=True, env=env)
    subprocess.run(["git", "-C", repo, "-c", "user.name=fixture",
                    "-c", "user.email=fixture@example.invalid",
                    "commit", "-q", "-m", "fixture: %s" % name], check=True, env=env)
    return repo


VARIANTS = [
    ("V1-k17-absent-path-d06cedb", V1_TABLE,
     {"exit": 1, "mismatch_ids": ["K17", "K18"]}),
    ("V2-k17-no-case-count-ee36f9e", V2_TABLE,
     {"exit": 1, "mismatch_ids": ["K17"]}),
    ("V3-k16-row-lost-5124bf3", V2_TABLE + V3_APPEND,
     {"exit": 2, "error": "missing capability row: sources-registry"}),
    ("V4-correction-proposed-0e5f70f", V2_TABLE + V4_TABLE,
     {"exit": 0, "mismatch_ids": []}),
]

root = tempfile.mkdtemp(prefix="c36ledger622-fixtures-")
results = []
for name, append, expected in VARIANTS:
    repo = build_variant(name, append)
    entry = {"variant": name, "repo": repo, "expected": expected}
    try:
        result, code = csa.evaluate(repo, "HEAD")
        entry["actual_exit"] = code
        entry["actual_mismatch_ids"] = [r["id"] for r in result["checks"]
                                        if r["status"] == "mismatch"]
        entry["reasons"] = [r["reason"] for r in result["checks"]
                            if r["status"] == "mismatch"]
        entry["error"] = ""
    except csa.CannotEvaluate as exc:
        entry["actual_exit"] = csa.EXIT_CANNOT_EVALUATE
        entry["actual_mismatch_ids"] = []
        entry["reasons"] = []
        entry["error"] = "%s: %s" % (exc.reason, exc.detail)
    ok = (entry["actual_exit"] == expected["exit"]
          and entry.get("actual_mismatch_ids", []) == expected.get("mismatch_ids", [])
          and ("error" not in expected
               or expected["error"] in (entry["error"] or " ")))
    entry["result"] = "PASS" if ok else "FAIL"
    results.append(entry)

out = {"fixture_root": root, "results": results,
       "selftest": "PASS" if all(r["result"] == "PASS" for r in results) else "FAIL"}
dest = os.path.join(LANE, ".ufo/waves/round-37/w1/C36Ledger622/fixture-results.json")
with open(dest, "w", encoding="utf-8") as handle:
    handle.write(json.dumps(out, indent=1, sort_keys=True) + "\n")
print(json.dumps(out, indent=1, sort_keys=True))
sys.exit(0 if out["selftest"] == "PASS" else 1)
