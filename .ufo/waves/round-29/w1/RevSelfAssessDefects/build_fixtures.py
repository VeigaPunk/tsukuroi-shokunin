#!/usr/bin/env python3
"""Build the four round-27 routed-defect-6 fixtures and evaluate each.

Reuses the tool's own FIXTURE_FILES/FIXTURE_SCORECARD_TEMPLATE from
tools/check-self-assessment.py at 81a061a; each case mutates only the
fixture SCORECARD.md, exactly like the tool's `fixture_files` cases.
"""
import importlib.util, json, os, subprocess, sys

REPO = "/fast/scratch/hyaku/tsukuroi-r29/RevSelfAssessDefects/repo"
OUT = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/RevSelfAssessDefects"
SCRATCH = "/fast/scratch/hyaku/tsukuroi-r29/RevSelfAssessDefects"

spec = importlib.util.spec_from_file_location("csa", os.path.join(REPO, "tools/check-self-assessment.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def make_scorecard(case):
    """Mutated fixture SCORECARD.md per case; returns (text, expected dict)."""
    base = m.fixture_scorecard()
    if case == "round-heading-word-character-after-number":
        # MutSelfAssessQ65 survivor M7: `## Round 1x measured outcome` must
        # NOT be read as a dated record; K01 must keep observed=8.
        sc = base.replace("## Capabilities\n",
                          "## Round 1x measured outcome\n\n- depth 8 -> 3\n\n## Capabilities\n", 1)
        expected = {"expected_exit": 0, "expected_mismatch_ids": [], "expected_error": ""}
    elif case == "measured-outcome-different-capitalisation":
        # MutSelfAssessQ65 survivor M8: `## Round 1 Measured Outcome` MUST be
        # read as a dated record (case-insensitive match); K01 -> observed=3.
        sc = base.replace("## Capabilities\n",
                          "## Round 1 Measured Outcome\n\n- depth 8 -> 3\n\n## Capabilities\n", 1)
        expected = {"expected_exit": 1, "expected_mismatch_ids": ["K01"], "expected_error": ""}
    elif case == "later-round-outcome-section":
        # MutSelfAssessQ65 case 20: a measured-outcome section of a round
        # LATER than the declaring round (2) must not qualify.
        sc = base.replace("## Capabilities\n",
                          "## Round 3 measured outcome\n\n- depth 8 -> 3\n\n## Capabilities\n", 1)
        expected = {"expected_exit": 0, "expected_mismatch_ids": [], "expected_error": ""}
    elif case == "hyphenated-round-heading":
        # Routed defect 6 part (a): `### Round-13 measured outcome` shape.
        # The fixture's only dated record is hyphenated -> invisible -> all
        # six axes report `no dated move record`.
        sc = base.replace("## Round 1 measured outcome", "## Round-1 measured outcome", 1)
        expected = {"expected_exit": 1,
                    "expected_mismatch_ids": ["K01", "K02", "K03", "K04", "K05", "K06"],
                    "expected_error": "no dated move record"}
    else:
        raise ValueError(case)
    return sc, expected


def build(case):
    files = dict(m.FIXTURE_FILES)
    scorecard, expected = make_scorecard(case)
    files["SCORECARD.md"] = scorecard
    files["expected-findings.json"] = json.dumps(expected, indent=1, sort_keys=True) + "\n"
    root = os.path.join(SCRATCH, "fixture-" + case)
    if os.path.exists(root):
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
    return root, scorecard, expected


def run_eval(case, root):
    """Run the real CLI end-to-end on the fixture repo."""
    proc = subprocess.run(
        [sys.executable, os.path.join(REPO, "tools/check-self-assessment.py"),
         "--revision", "HEAD", "--repo", root],
        capture_output=True, text=True, env=m.git_env())
    return proc


def main():
    os.makedirs(OUT, exist_ok=True)
    cases = ["round-heading-word-character-after-number",
             "measured-outcome-different-capitalisation",
             "later-round-outcome-section",
             "hyphenated-round-heading"]
    summary = {}
    for case in cases:
        root, scorecard, expected = build(case)
        proc = run_eval(case, root)
        result = json.loads(proc.stdout)
        k = {c["id"]: {"status": c["status"], "stated": c.get("stated"),
                       "observed": c.get("observed"), "observed_line": c.get("observed_line"),
                       "reason": c["reason"][:140]}
             for c in result.get("checks", []) if c["id"].startswith("K0")}
        summary[case] = {"exit": proc.returncode, "status": result.get("status"),
                         "mismatches": result.get("mismatches"), "expected": expected,
                         "k_checks": k}
        case_dir = os.path.join(OUT, case)
        os.makedirs(case_dir, exist_ok=True)
        with open(os.path.join(case_dir, "SCORECARD.md"), "w") as fh:
            fh.write(scorecard)
        with open(os.path.join(case_dir, "expected-findings.json"), "w") as fh:
            json.dump(expected, fh, indent=1, sort_keys=True)
            fh.write("\n")
        with open(os.path.join(case_dir, "tool-output.json"), "w") as fh:
            fh.write(proc.stdout)
    with open(os.path.join(OUT, "results.json"), "w") as fh:
        json.dump(summary, fh, indent=1)
    print(json.dumps(summary, indent=1)[:6000])


if __name__ == "__main__":
    main()
