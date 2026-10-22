#!/usr/bin/env python3
"""Build R29 owed-counter fixtures and exercise one mutation per rule."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

BASE = "81a061a67466c5e1be812814a895a4b5ed89b4ff"
COUNTER = "tools/check-owed-statements-r29.py"
SOURCE_ID = "S900"
MUTATIONS = {
    "M1": ("or anchor not in target[field]", "or False"),
    "M2": ("if len(ms) != 1:", "if len(ms) < 1:"),
    "M3": (
        "if m.get('row') != row or m.get('field') != field or m.get('withdrawn_text') != anchor:",
        "if m.get('row') != row or m.get('field') != field:",
    ),
    "M4": ("if verdict not in VERDICTS:", "if False and verdict not in VERDICTS:"),
    "M5": ("len(now.split()) < 12", "len(now.split()) < 0"),
    "M6": ("if not good_sid and not good_path:", "if False and not good_sid and not good_path:"),
    "M7": ("if need_sid and not good_sid:", "if False and need_sid and not good_sid:"),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(repo, *args):
    command = ["env", "-u", "GIT_DIR", "-u", "GIT_WORK_TREE", "-u", "GIT_INDEX_FILE",
               "git", "-C", str(repo), *args]
    return subprocess.run(command, check=True, capture_output=True, text=True, timeout=60)


def git_bytes(repo, *args):
    command = ["env", "-u", "GIT_DIR", "-u", "GIT_WORK_TREE", "-u", "GIT_INDEX_FILE",
               "git", "-C", str(repo), *args]
    return subprocess.run(command, check=True, capture_output=True, timeout=60).stdout


def items_from_counter(counter_bytes):
    tree = ast.parse(counter_bytes.decode("utf-8"))
    node = next(n for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "ITEMS" for t in n.targets))
    return ast.literal_eval(node.value)


def source_row(src_text, source_id):
    for line in src_text.splitlines():
        if line.startswith(f"| {source_id} |"):
            return True
    return False


def fixture_now(iid):
    return (f"Fixture correction for {iid} records a bounded interpretation from its cited source, "
            "preserves surrounding evidence, and avoids claiming unsupported behavior.")


def make_valid(repo, items):
    affected = set()
    by_path = {}
    for iid, path, row, field, anchor in items:
        by_path.setdefault(path, []).append((iid, row, field, anchor))
        affected.add(path)

    src_path = repo / "corpus/SOURCES.md"
    src = src_path.read_text(encoding="utf-8")
    if source_row(src, SOURCE_ID):
        raise RuntimeError(f"fixture source id {SOURCE_ID} already exists")
    used_by = ", ".join(sorted({Path(path).name for path in affected}))
    src += (f"\n| {SOURCE_ID} | Fixture-only source | docs | A | Fixture rule checks | "
            f"Synthetic registry row | Fixture provenance for marker validation | mined | "
            f"2026-10-22 | fixture | {used_by} |\n")
    src_path.write_text(src, encoding="utf-8")

    for path, records in by_path.items():
        file_path = repo / path
        text = file_path.read_text(encoding="utf-8")
        if path.endswith(".json"):
            doc = json.loads(text)
            corrections = doc.setdefault("corrections_r29", [])
            for iid, row_id, field, anchor in records:
                target = next(r for r in doc["rows"] if isinstance(r, dict) and r.get("id") == row_id)
                if anchor not in target.get(field, ""):
                    raise RuntimeError(f"fixture anchor absent at {path}:{row_id}.{field}: {iid}")
                corrections.append({
                    "id": f"R29-OWED-{iid}", "row": row_id, "field": field,
                    "withdrawn_text": anchor, "verdict": "corrected", "now": fixture_now(iid),
                    "basis": [SOURCE_ID],
                })
            file_path.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        else:
            for iid, _row, _field, anchor in records:
                if anchor not in text:
                    raise RuntimeError(f"fixture anchor absent at {path}: {iid}")
                marker = (f'\n[R29-OWED-{iid}] verdict: corrected | original: "{anchor}" | '
                          f"now: {fixture_now(iid)} | basis: {SOURCE_ID}\n")
                text += marker
            file_path.write_text(text, encoding="utf-8")
    return sorted(affected | {"corpus/SOURCES.md"})


def make_bad(repo, rule, items):
    by_id = {row[0]: row for row in items}
    iid = {"M1": "O06", "M2": "O06", "M3": "O06", "M4": "O06",
           "M5": "O06", "M6": "O06", "M7": "O01"}[rule]
    _iid, path, row, field, anchor = by_id[iid]
    file_path = repo / path
    if path.endswith(".json"):
        doc = json.loads(file_path.read_text(encoding="utf-8"))
        corr = doc["corrections_r29"]
        marker = next(c for c in corr if c.get("id") == f"R29-OWED-{iid}")
        if rule == "M1":
            target = next(r for r in doc["rows"] if r.get("id") == row)
            value = target[field]
            if value.count(anchor) != 1:
                raise RuntimeError("M1 fixture needs a single frozen-anchor occurrence in its target field")
            target[field] = value.replace(anchor, "fixture text with the frozen anchor removed", 1)
        elif rule == "M2":
            corr.append(dict(marker))
        elif rule == "M3":
            marker["withdrawn_text"] = anchor + " altered"
        elif rule == "M4":
            marker["verdict"] = "unsupported"
        elif rule == "M5":
            marker["now"] = "Too few words here."
        elif rule == "M6":
            marker["basis"] = ["S999"]
        elif rule == "M7":
            marker["basis"] = ["corpus/SOURCES.md:1"]
        else:
            raise RuntimeError(f"unexpected JSON fixture rule {rule}")
        file_path.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    else:
        if rule != "M7":
            raise RuntimeError(f"rule {rule} expected a JSON fixture, got {path}")
        lines = file_path.read_text(encoding="utf-8").splitlines()
        marker_lines = [i for i, line in enumerate(lines) if f"[R29-OWED-{iid}]" in line]
        if len(marker_lines) != 1:
            raise RuntimeError("M7 fixture needs exactly one Markdown marker")
        line = lines[marker_lines[0]]
        if line.count(f"basis: {SOURCE_ID}") != 1:
            raise RuntimeError("M7 fixture expected the valid source basis")
        lines[marker_lines[0]] = line.replace(f"basis: {SOURCE_ID}", "basis: corpus/SOURCES.md:1", 1)
        file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def commit(repo, paths, message):
    git(repo, "add", "--", *paths)
    git(repo, "-c", "user.name=MutOwedCounter fixture", "-c",
        "user.email=mut-owed-counter@example.invalid", "commit", "--quiet", "-m", message)
    return git(repo, "rev-parse", "HEAD").stdout.strip()


def build_fixtures(repo, items):
    git(repo, "checkout", "--quiet", "--detach", BASE)
    valid_paths = make_valid(repo, items)
    valid = commit(repo, valid_paths, "fixture: all O01-O12 have valid correction markers")
    variants = {}
    for rule in MUTATIONS:
        git(repo, "checkout", "--quiet", "--detach", valid)
        path = make_bad(repo, rule, items)
        variants[rule] = commit(repo, [path], f"fixture: should fail {rule}")
    git(repo, "checkout", "--quiet", "--detach", BASE)
    if git(repo, "status", "--porcelain").stdout:
        raise RuntimeError("fixture build did not restore the base worktree")
    return valid, variants


def run_one(counter, repo, revision, case_name):
    command = [sys.executable, str(counter), "--revision", revision, "--lane", str(repo)]
    p = subprocess.run(command, capture_output=True, text=True, timeout=20)
    lines = p.stdout.splitlines()
    try:
        summary = json.loads(lines[-1])
    except (IndexError, json.JSONDecodeError):
        summary = None
    item_rows = []
    for line in lines[:-1]:
        try:
            item_rows.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return {"case": case_name, "revision": revision, "exit": p.returncode,
            "summary": summary, "items": item_rows, "stdout": p.stdout, "stderr": p.stderr}


def suite(counter, repo, valid, variants, label):
    runs = [run_one(counter, repo, valid, f"{label}/valid")]
    runs.extend(run_one(counter, repo, variants[rule], f"{label}/{rule}") for rule in MUTATIONS)
    return runs


def expected_case(run, rule=None):
    summary = run["summary"]
    if not isinstance(summary, dict):
        return False
    wanted_count = 12 if rule is None else 11
    wanted_exit = 0 if rule is None else 1
    if summary.get("items") != 12 or summary.get("marked") != wanted_count or run["exit"] != wanted_exit:
        return False
    if rule is None:
        return not summary.get("unmarked")
    iid = {"M1": "O06", "M2": "O06", "M3": "O06", "M4": "O06",
           "M5": "O06", "M6": "O06", "M7": "O01"}[rule]
    target = next((r for r in run["items"] if r.get("id") == iid), None)
    others = [r for r in run["items"] if r.get("id") != iid]
    return (target is not None and not target.get("ok") and
            str(target.get("why", "")).startswith(rule) and all(r.get("ok") for r in others))


def suite_passes(runs):
    if len(runs) != 8 or not expected_case(runs[0]):
        return False
    for rule, run in zip(MUTATIONS, runs[1:]):
        if not expected_case(run, rule):
            return False
    return True


def mutate(original, rule):
    old, new = MUTATIONS[rule]
    text = original.decode("utf-8")
    if text.count(old) != 1:
        raise RuntimeError(f"{rule} mutation anchor count is {text.count(old)}, expected 1")
    return text.replace(old, new, 1).encode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--artifacts", required=True)
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    artifacts = Path(args.artifacts).resolve()
    artifacts.mkdir(parents=True, exist_ok=True)
    counter = repo / COUNTER
    if git(repo, "rev-parse", "HEAD").stdout.strip() != BASE:
        raise SystemExit(f"repo must be checked out at {BASE}")
    if git(repo, "status", "--porcelain").stdout:
        raise SystemExit("repo worktree must be clean before fixture construction")

    original = counter.read_bytes()
    committed = git_bytes(repo, "show", f"{BASE}:{COUNTER}")
    if original != committed:
        raise SystemExit("counter file bytes do not match the pinned declaration revision")
    original_hash = sha(original)
    items = items_from_counter(original)
    valid, variants = build_fixtures(repo, items)
    manifest = {"base": BASE, "valid": valid, "should_fail": variants,
                "rule_items": {"M1": "O06", "M2": "O06", "M3": "O06", "M4": "O06",
                               "M5": "O06", "M6": "O06", "M7": "O01"},
                "counter_sha256_pristine": original_hash}
    (artifacts / "fixtures.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    report = {"counter_sha256_pristine": original_hash, "fixtures": manifest,
              "pristine": None, "mutants": [], "restorations": []}
    try:
        report["pristine"] = suite(counter, repo, valid, variants, "pristine")
        report["pristine_passed"] = suite_passes(report["pristine"])
        for rule in MUTATIONS:
            mutated = mutate(original, rule)
            counter.write_bytes(mutated)
            mutated_hash = sha(mutated)
            mutant_runs = suite(counter, repo, valid, variants, rule)
            mutant_valid_ok = expected_case(mutant_runs[0])
            accepted = [r["case"].split("/")[-1] for r in mutant_runs[1:]
                        if not expected_case(r, r["case"].split("/")[-1])]
            killed = bool(accepted)
            if not report["pristine_passed"] or not mutant_valid_ok:
                verdict = "inconclusive"
            elif killed:
                verdict = "killed"
            else:
                verdict = "survived"
            report["mutants"].append({"rule": rule, "sha256": mutated_hash,
                                      "verdict": verdict, "accepted_should_fail": accepted,
                                      "valid_control_passed": mutant_valid_ok, "runs": mutant_runs})
            counter.write_bytes(original)
            restored_hash = sha(counter.read_bytes())
            restored_runs = suite(counter, repo, valid, variants, f"restored-after-{rule}")
            restoration = {"after_mutant": rule, "sha256": restored_hash,
                           "exact_pristine_bytes": counter.read_bytes() == original,
                           "suite_passed": suite_passes(restored_runs), "runs": restored_runs}
            report["restorations"].append(restoration)
    finally:
        counter.write_bytes(original)
        report["counter_sha256_restored_final"] = sha(counter.read_bytes())
        report["exact_pristine_bytes_final"] = counter.read_bytes() == original
        # The fixture commits remain addressable; restore only the owned scratch worktree.
        git(repo, "checkout", "--quiet", "--detach", BASE)
        report["worktree_clean_final"] = not bool(git(repo, "status", "--porcelain").stdout)

    out = artifacts / "mutation-results.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    compact = {"pristine_passed": report.get("pristine_passed"),
               "mutants": [{k: m[k] for k in ("rule", "sha256", "verdict", "accepted_should_fail",
                                                  "valid_control_passed")} for m in report["mutants"]],
               "restored_after_each_passed": all(r["suite_passed"] and r["exact_pristine_bytes"]
                                                  for r in report["restorations"]),
               "counter_sha256_pristine": report["counter_sha256_pristine"],
               "counter_sha256_restored_final": report["counter_sha256_restored_final"],
               "exact_pristine_bytes_final": report["exact_pristine_bytes_final"],
               "worktree_clean_final": report["worktree_clean_final"]}
    print(json.dumps(compact, sort_keys=True))
    return 0 if (report.get("pristine_passed") and all(m["verdict"] != "inconclusive" for m in report["mutants"])
                 and report["exact_pristine_bytes_final"] and report["worktree_clean_final"]
                 and all(r["suite_passed"] and r["exact_pristine_bytes"] for r in report["restorations"])) else 1


if __name__ == "__main__":
    sys.exit(main())
