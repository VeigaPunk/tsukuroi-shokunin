#!/usr/bin/env python3
"""L1-only once-final measurements after all waves; no host probes or network."""
import ast
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
    (OUT / "sources-before.md").write_bytes(subprocess.check_output(
        ["git", "-C", str(repo), "show", BASE + ":corpus/SOURCES.md"], env=ENV))
    (OUT / "sources-after.md").write_bytes((repo / "corpus/SOURCES.md").read_bytes())
    census = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
    run("source-counts-before", [census, "census", "--file", str(OUT / "sources-before.md")], repo, 0)
    run("source-counts-after", [census, "census", "--file", str(OUT / "sources-after.md")], repo, 0)
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
                        "--manifest", ".ufo/waves/round-21/falsify-reviews.json"], repo, 1)
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
    for wave, expected in (("build", 1), ("falsify", 1)):
        run("scope-r21-" + wave, ["python3", "tools/check-seat-scope.py", "--revision", REV,
                                   "--wave", ".ufo/waves/round-21/" + wave], repo, expected)
    prefix_paths = ["LOG.md", "SKILL.md", "PROVINCE.md", "SCORECARD.md", "corpus/QUALITY.md", "corpus/README.md",
                    "corpus/lessons/round-20.md"]
    prefixes = {}
    for path in prefix_paths:
        old = subprocess.check_output(["git", "-C", str(repo), "show", BASE + ":" + path], env=ENV)
        new = (repo / path).read_bytes()
        prefixes[path] = {"preserved_prefix": new.startswith(old), "baseline_sha256": hashlib.sha256(old).hexdigest()}
    (OUT / "history-prefixes.json").write_text(json.dumps(prefixes, indent=2) + "\n")
    old_judge = subprocess.check_output(
        ["git", "-C", str(repo), "show", BASE + ":tools/check-revision-binding.py"], env=ENV).decode()
    new_judge = (repo / "tools/check-revision-binding.py").read_text()
    old_functions = {node.name: ast.get_source_segment(old_judge, node)
                     for node in ast.parse(old_judge).body if isinstance(node, ast.FunctionDef)}
    new_functions = {node.name: ast.get_source_segment(new_judge, node)
                     for node in ast.parse(new_judge).body if isinstance(node, ast.FunctionDef)}
    continuity = {name: {"byte_equal": old_functions[name] == new_functions[name],
                         "baseline_sha256": hashlib.sha256(old_functions[name].encode()).hexdigest(),
                         "measured_sha256": hashlib.sha256(new_functions[name].encode()).hexdigest()}
                  for name in ("object_selector_probes", "measure", "probe_tool", "grade")}
    original_binder = subprocess.check_output(
        ["git", "-C", str(repo), "show", BASE + ":tools/_revision.py"], env=ENV)
    continuity["shared_binder"] = {"byte_equal": original_binder == (repo / "tools/_revision.py").read_bytes()}
    (OUT / "legacy-continuity.json").write_text(json.dumps(continuity, indent=2) + "\n")
    integrity = {}
    for manifest, prereg, prefix, origin in (
            (".ufo/waves/round-21/reviews.json", "c05af5c07a639252795317abcb98bcfe7e19dba4",
             ".ufo/waves/round-21/snapshot/", BASE),
            (".ufo/waves/round-21/falsify-reviews.json", "70e8dfcaae2ef1935d709dcd71c84af1801ce5bf",
             ".ufo/waves/round-21/candidate/", "0a14952b59d20179e1c813af58befaecd6992a17")):
        earlier = subprocess.check_output(["git", "-C", str(repo), "show", prereg + ":" + manifest], env=ENV)
        current = (repo / manifest).read_bytes()
        ancestry = subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", prereg, REV],
                                  env=ENV).returncode == 0
        copies = {}
        delivered = {}
        for row in json.loads(current)["reviews"]:
            source = row["source"]
            if source not in copies:
                original = subprocess.check_output(
                    ["git", "-C", str(repo), "show", origin + ":" + source.removeprefix(prefix)], env=ENV)
                copies[source] = ((repo / source).read_bytes() == original
                                  and hashlib.sha256(original).hexdigest() == row["sha256"])
            report = repo / row["report"]
            delivered[row["name"]] = hashlib.sha256(report.read_bytes()).hexdigest() if report.is_file() else None
        integrity[manifest] = {"preregistration": prereg, "ancestor": ancestry,
                               "manifest_unchanged": current == earlier,
                               "snapshot_matches_origin": copies,
                               "delivered_report_sha256": delivered}
    (OUT / "preregister-integrity.json").write_text(json.dumps(integrity, indent=2) + "\n")
print("ledger", OUT, "matched", sum(r["matched"] for r in records), "of", len(records), flush=True)
