#!/usr/bin/env python3
"""Replay the four w1 RevSelfAssessDefects fixtures against check-self-assessment.py
at 10d5288fc1051364e711203855e7c53710dfcc21.

Mutates the NEW tool's own fixture_scorecard() base exactly like
w1/RevSelfAssessDefects/build_fixtures.py did at 81a061a, verifies the produced
SCORECARD.md is byte-identical to the stored w1 fixture, builds a scratch git
repo, runs the real CLI, and reports exit/status/mismatch ids plus the K01-K06
reasons. Prints a JSON summary.
"""
import importlib.util, json, os, subprocess, sys

REPO = "/fast/scratch/hyaku/tsukuroi-r29/RevSelfAssessFix/repo"
W1 = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/RevSelfAssessDefects"
OUT = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/RevSelfAssessFix"
SCRATCH = "/fast/scratch/hyaku/tsukuroi-r29/RevSelfAssessFix"

spec = importlib.util.spec_from_file_location("csa", os.path.join(REPO, "tools/check-self-assessment.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def make_scorecard(case):
    """Same mutations as w1 build_fixtures.py make_scorecard()."""
    base = m.fixture_scorecard()
    if case == "round-heading-word-character-after-number":
        sc = base.replace("## Capabilities\n",
                          "## Round 1x measured outcome\n\n- depth 8 -> 3\n\n## Capabilities\n", 1)
    elif case == "measured-outcome-different-capitalisation":
        sc = base.replace("## Capabilities\n",
                          "## Round 1 Measured Outcome\n\n- depth 8 -> 3\n\n## Capabilities\n", 1)
    elif case == "later-round-outcome-section":
        sc = base.replace("## Capabilities\n",
                          "## Round 3 measured outcome\n\n- depth 8 -> 3\n\n## Capabilities\n", 1)
    elif case == "hyphenated-round-heading":
        sc = base.replace("## Round 1 measured outcome", "## Round-1 measured outcome", 1)
    else:
        raise ValueError(case)
    return sc


def build(case):
    files = dict(m.FIXTURE_FILES)
    files["SCORECARD.md"] = make_scorecard(case)
    w1dir = os.path.join(W1, case)
    files["expected-findings.json"] = open(os.path.join(w1dir, "expected-findings.json")).read()
    root = os.path.join(SCRATCH, "fixture-" + case)
    subprocess.run(["rm", "-rf", root], check=True)
    os.makedirs(root)
    env = m.git_env()
    subprocess.run(["git", "init", "-q", root], check=True, env=env)
    for path, text in files.items():
        full = os.path.join(root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    subprocess.run(["git", "-C", root, "add", "-A"], check=True, env=env)
    subprocess.run(["git", "-C", root, "-c", "user.name=fixture", "-c", "user.email=fixture@x",
                    "commit", "-q", "-m", "fixture: " + case], check=True, env=env)
    return root


def main():
    os.makedirs(OUT, exist_ok=True)
    cases = ["round-heading-word-character-after-number",
             "measured-outcome-different-capitalisation",
             "later-round-outcome-section",
             "hyphenated-round-heading"]
    summary = {}
    for case in cases:
        root = build(case)
        # replayed scorecard must equal the stored w1 fixture
        w1_sc = open(os.path.join(W1, case, "SCORECARD.md")).read()
        new_sc = open(os.path.join(root, "SCORECARD.md")).read()
        proc = subprocess.run(
            [sys.executable, os.path.join(REPO, "tools/check-self-assessment.py"),
             "--revision", "HEAD", "--repo", root],
            capture_output=True, text=True, env=m.git_env())
        result = json.loads(proc.stdout)
        k = {c["id"]: {"status": c["status"], "observed": c.get("observed"),
                       "reason": c["reason"][:120]}
             for c in result.get("checks", []) if c["id"].startswith("K0")}
        mismatch_ids = [c["id"] for c in result.get("checks", []) if c["status"] == "mismatch"]
        w1_expected = json.load(open(os.path.join(W1, case, "expected-findings.json")))
        summary[case] = {
            "scorecard_matches_w1": new_sc == w1_sc,
            "exit": proc.returncode,
            "status": result.get("status"),
            "mismatch_ids": mismatch_ids,
            "w1_expected_findings": w1_expected,
            "k_reasons": k,
        }
        with open(os.path.join(OUT, case + "-tool-output.json"), "w") as fh:
            fh.write(proc.stdout)
    path = os.path.join(OUT, "replay-results.json")
    with open(path, "w") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps(summary, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
