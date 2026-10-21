#!/usr/bin/env python3
"""L1-only once-final measurements after all waves; no host probes or network."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

LANE = Path(__file__).resolve().parents[4]
BASE = "82e519203e676c532b1dc5ea91a85671f2286e7b"
REV = sys.argv[1]
OUT = LANE / ".ufo/waves/round-21/measure" / sys.argv[2]
OUT.mkdir(parents=True, exist_ok=False)
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV.update(PYTHONDONTWRITEBYTECODE="1", GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
           GIT_OPTIONAL_LOCKS="0", LC_ALL="C", GIT_PAGER="cat")
records = []


def run(name, command, cwd, expected):
    proc = subprocess.run(command, cwd=cwd, env=ENV, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=1200)
    (OUT / (name + ".stdout")).write_bytes(proc.stdout)
    (OUT / (name + ".stderr")).write_bytes(proc.stderr)
    record = {"name": name, "command": command, "revision": REV, "baseline": BASE,
              "exit": proc.returncode, "expected_exit": expected,
              "matched": proc.returncode == expected}
    try:
        record["output"] = json.loads(proc.stdout)
    except (ValueError, UnicodeError):
        record["output_text"] = proc.stdout.decode("utf-8", "replace")
    records.append(record)
    (OUT / "results.json").write_text(json.dumps(records, indent=2) + "\n")
    print(name, "exit", proc.returncode, "expected", expected, flush=True)


with tempfile.TemporaryDirectory(prefix="tsukuroi-r21-final-") as tmp:
    repo = Path(tmp) / "repo"
    subprocess.run(["git", "clone", "--no-hardlinks", "--quiet", "--no-tags", str(LANE), str(repo)],
                   env=ENV, check=True)
    subprocess.run(["git", "-C", str(repo), "checkout", "--quiet", "--detach", REV], env=ENV, check=True)
    for ref in ("refs/heads/master", "refs/remotes/origin/master"):
        subprocess.run(["git", "-C", str(repo), "update-ref", ref, REV], env=ENV, check=True)
    digests = {str(path.relative_to(repo)): hashlib.sha256(path.read_bytes()).hexdigest()
               for path in (repo / "tools").iterdir() if path.is_file()}
    (OUT / "evaluator-sha256.json").write_text(json.dumps(digests, indent=2) + "\n")
    for path in sorted((repo / "tools").iterdir()):
        if path.suffix not in (".py", ".sh"):
            continue
        exe = "python3" if path.suffix == ".py" else "bash"
        run("selftest-" + path.stem, [exe, str(path), "--selftest"], repo, 0)
    baseline_judge = Path(tmp) / "baseline-judge.py"
    baseline_judge.write_bytes(subprocess.check_output(
        ["git", "-C", str(repo), "show", BASE + ":tools/check-revision-binding.py"], env=ENV))
    run("c2-baseline-cli-absent", ["python3", str(baseline_judge),
                                  "--tools-revision", BASE, "--object-target-types"], repo, 2)
    for label, rev, expected in (("before", BASE, 1), ("after", REV, 0)):
        run("c1-" + label, ["python3", "tools/check-selector-contract.py", "--revision", rev], repo, expected)
        run("c2-" + label, ["python3", "tools/check-revision-binding.py", "--tools-revision", rev,
                              "--object-target-types"], repo, expected)
        # Known dead-seat missing reports deliberately remain non-clean after.
        run("c3-" + label, ["python3", "tools/check-review-snapshots.py", "--revision", rev,
                              "--manifest", ".ufo/waves/round-21/reviews.json"], repo, 1)
    run("c3-falsify", ["python3", "tools/check-review-snapshots.py", "--revision", REV,
                        "--manifest", ".ufo/waves/round-21/falsify-reviews.json"], repo, 0)
    run("default-nine-continuity", ["python3", "tools/check-revision-binding.py",
                                    "--tools-revision", REV], repo, 0)
    run("old-matrix-continuity", ["python3", "tools/check-revision-binding.py", "--tools-revision", REV,
                                   "--object-selectors"], repo, 0)
    run("registry-coverage", ["python3", "tools/check-registry-coverage.py", "--revision", REV], repo, 0)
    run("live-map", ["python3", "tools/check-registry-coverage.py", "--revision", REV,
                       "--audit-live-map"], repo, 0)
    run("adjacency", ["python3", "tools/check-adjacency-anchors.py", "--revision", REV], repo, 0)
    run("ownership-correction", ["python3", "tools/check-adjacency-anchors.py", "--revision", REV,
                                   "--ownership-corrections"], repo, 0)
    run("boot-writers", ["python3", "tools/check-boot-writers.py", "--revision", REV], repo, 0)
    run("corpus-rechecks", ["python3", "tools/check-recheck-commands.py", "--revision", REV], repo, 0)
    for wave, expected in (("build", 1), ("falsify", 0)):
        run("scope-r21-" + wave, ["python3", "tools/check-seat-scope.py", "--revision", REV,
                                   "--wave", ".ufo/waves/round-21/" + wave], repo, expected)
    for wave in ("build", "falsify"):
        run("scope-r20-" + wave, ["python3", "tools/check-seat-scope.py", "--revision", REV,
                                   "--wave", ".ufo/waves/round-20/" + wave], repo, 1)
    prefix_paths = ["LOG.md", "SKILL.md", "PROVINCE.md", "SCORECARD.md", "corpus/QUALITY.md", "corpus/README.md",
                    "corpus/lessons/round-20.md"]
    prefixes = {}
    for path in prefix_paths:
        old = subprocess.check_output(["git", "-C", str(repo), "show", BASE + ":" + path], env=ENV)
        new = (repo / path).read_bytes()
        prefixes[path] = {"preserved_prefix": new.startswith(old), "baseline_sha256": hashlib.sha256(old).hexdigest()}
    (OUT / "history-prefixes.json").write_text(json.dumps(prefixes, indent=2) + "\n")
print("ledger", OUT, "matched", sum(r["matched"] for r in records), "of", len(records), flush=True)
