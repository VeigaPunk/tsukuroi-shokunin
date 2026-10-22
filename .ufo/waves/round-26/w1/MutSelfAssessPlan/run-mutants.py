#!/usr/bin/env python3
"""run-mutants.py — run the round-26 C2 (calibration, check set v2) mutation catalogue.

The catalogue (catalogue.json) lists mutants of the repository content that
`tools/check-self-assessment.py` is supposed to notice.  Each mutant is a set
of edits applied to a throw-away sandbox built from one revision:

    git -C <lane repo> archive <rev> | tar -x -C <sandbox>
    git init                      (no remote, no push URL, nothing is pushed)
    git add -A && git commit     (sandbox-local base commit)
    apply the catalogue edits
    git add -A && git commit     (mutant commit)
    python3 tools/check-self-assessment.py --revision HEAD --repo <sandbox>
    git reset --hard <base> && git clean -fd     (restore exact bytes)

The lane repository is never written to; every write happens inside the
sandbox directory.  The tree digest (sha256 over every tracked path and its
file sha256) is taken before the first mutation, after each restoration, and
at the end, so restoration is evidenced rather than asserted.

Usage:
    python3 run-mutants.py --repo <lane repo> --revision <rev> \
        --catalogue catalogue.json --out results.json [--only M01,M02] [--smoke]

Exit codes of the runner: 0 when every selected mutant was measured (killed or
survived, verdict recorded), 1 when a precondition was unmet, an edit failed,
or the baseline was not clean, 2 on a usage or environment error.
"""

import argparse
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

TOOL_PATH = "tools/check-self-assessment.py"
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
KNOWLEDGE_PATH_RE = re.compile(r"corpus/knowledge/[A-Za-z0-9_.\-]+\.md")


# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------

def run(cmd, cwd=None, env=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)


def split_cells(line):
    """Split a markdown table row on pipes that are not inside backtick spans."""
    cells, current, in_code = [], [], False
    for char in line:
        if char == "`":
            in_code = not in_code
            current.append(char)
            continue
        if char == "|" and not in_code:
            cells.append("".join(current))
            current = []
            continue
        current.append(char)
    cells.append("".join(current))
    if cells and not cells[0].strip():
        cells = cells[1:]
    if cells and not cells[-1].strip():
        cells = cells[:-1]
    return [cell.strip() for cell in cells]


def tree_digest(root):
    """sha256 over every path under root (excluding .git) and its file sha256."""
    digest = hashlib.sha256()
    paths = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d != ".git"]
        for name in files:
            full = os.path.join(base, name)
            paths.append(os.path.relpath(full, root))
    for rel in sorted(paths):
        with open(os.path.join(root, rel), "rb") as handle:
            body = handle.read()
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(body).hexdigest().encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def read_text(path):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def write_text(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


# --------------------------------------------------------------------------
# markdown structure
# --------------------------------------------------------------------------

def find_section(lines, section_regex):
    """(start, end) of the last heading whose raw line matches section_regex."""
    pattern = re.compile(section_regex)
    found = None
    for index, line in enumerate(lines):
        if pattern.search(line):
            match = HEADING_RE.match(line)
            found = (index, len(match.group(1)) if match else 1)
    if found is None:
        return None
    start, level = found
    end = len(lines)
    for index in range(start + 1, len(lines)):
        match = HEADING_RE.match(lines[index])
        if match and len(match.group(1)) <= level:
            end = index
            break
    return (start, end)


def find_table(lines, lo, hi, header_key):
    """(start, end) of the pipe-table block whose header names header_key."""
    blocks = []
    index = lo
    while index < hi:
        if lines[index].lstrip().startswith("|"):
            start = index
            while index < hi and lines[index].lstrip().startswith("|"):
                index += 1
            blocks.append((start, index))
        else:
            index += 1
    for start, end in blocks:
        cells = split_cells(lines[start])
        if cells and cells[0].strip().lower() == header_key.lower():
            return (start, end)
    return blocks[-1] if blocks else None


def find_row(lines, table, row_key):
    """Index of the raw table line whose first cell equals row_key."""
    start, end = table
    for index in range(start, end):
        cells = split_cells(lines[index])
        if cells and cells[0].strip().strip("`").lower() == row_key.strip().lower():
            return index
    return None


def shonen_boxes(lines):
    """(lo, hi) line ranges of every '- [' bullet in a SHONEN file."""
    boxes = []
    index = 0
    while index < len(lines):
        if re.match(r"^- \[", lines[index]):
            lo = index
            index += 1
            while index < len(lines) and not re.match(r"^- \[", lines[index]):
                index += 1
            boxes.append((lo, index))
        else:
            index += 1
    return boxes


# --------------------------------------------------------------------------
# edit operations
# --------------------------------------------------------------------------

class EditError(Exception):
    """A catalogue edit could not be applied (precondition unmet)."""


def render_template(template, match, offsets):
    """Substitute {gN} placeholders, adding the per-group integer offset."""
    def repl(placeholder):
        index = int(placeholder.group(1))
        value = match.group(index)
        if value is None:
            return ""
        if value.isdigit():
            value = str(int(value) + int(offsets.get(str(index), 0)))
        return value
    return re.sub(r"\{g(\d+)\}", repl, template)


def apply_regex(pattern, repl, offsets, text, count=1):
    compiled = re.compile(pattern)
    done = [0]

    def substitute(match):
        if done[0] >= count:
            return match.group(0)
        done[0] += 1
        return render_template(repl, match, offsets)
    result = compiled.sub(substitute, text)
    if done[0] == 0:
        raise EditError("pattern did not match: %s" % pattern)
    return result


def apply_edit(sandbox, edit):
    """Apply one catalogue edit inside the sandbox. Returns a note string."""
    op = edit["op"]
    path = edit.get("file")
    full = os.path.join(sandbox, path)

    if op == "write_file":
        write_text(full, edit["content"])
        return "wrote %s (%d bytes)" % (path, len(edit["content"].encode("utf-8")))

    if op == "append":
        text = read_text(full)
        write_text(full, text + edit["text"])
        return "appended to %s" % path

    if op == "replace_once":
        text = read_text(full)
        find = edit["find"]
        if find not in text:
            raise EditError("text not found in %s: %r" % (path, find))
        write_text(full, text.replace(find, edit["repl"], 1))
        return "replaced one occurrence in %s" % path

    if op == "regex_once":
        text = read_text(full)
        write_text(full, apply_regex(edit["pattern"], edit["repl"], edit.get("offsets", {}), text))
        return "regex replacement in %s" % path

    if op == "section_regex_once":
        text = read_text(full)
        lines = text.split("\n")
        section = find_section(lines, edit["section"])
        if section is None:
            raise EditError("section not found in %s: %s" % (path, edit["section"]))
        lo, hi = section
        block = "\n".join(lines[lo:hi])
        patched = apply_regex(edit["pattern"], edit["repl"], edit.get("offsets", {}), block)
        lines[lo:hi] = patched.split("\n")
        write_text(full, "\n".join(lines))
        return "section regex replacement in %s" % path

    if op == "row_sub" or op == "row_append":
        text = read_text(full)
        lines = text.split("\n")
        section = find_section(lines, edit["section"])
        if section is None:
            raise EditError("section not found in %s: %s" % (path, edit["section"]))
        table = find_table(lines, section[0] + 1, section[1], "Axis")
        if table is None:
            raise EditError("no pipe table in the section of %s" % path)
        row_index = find_row(lines, table, edit["row"])
        if row_index is None:
            raise EditError("row %r not found in the table of %s" % (edit["row"], path))
        row_line = lines[row_index]
        if op == "row_sub":
            patched = apply_regex(edit["pattern"], edit["repl"], edit.get("offsets", {}), row_line)
        else:
            stripped = row_line.rstrip()
            if not stripped.endswith("|"):
                raise EditError("row of %s does not end with a pipe" % path)
            patched = stripped[:-1] + edit["text"] + "|"
        lines[row_index] = patched
        write_text(full, "\n".join(lines))
        return "row %s patched in %s (line %d)" % (edit["row"], path, row_index + 1)

    if op == "insert_in_section":
        text = read_text(full)
        lines = text.split("\n")
        section = find_section(lines, edit["section"])
        if section is None:
            raise EditError("section not found in %s: %s" % (path, edit["section"]))
        lo, hi = section
        payload = edit["text"].split("\n")
        if edit.get("position", "end") == "start":
            lines[lo + 1:lo + 1] = payload
        else:
            while hi > lo + 1 and not lines[hi - 1].strip():
                hi -= 1
            lines[hi:hi] = payload
        write_text(full, "\n".join(lines))
        return "inserted into section %s of %s" % (edit["section"], path)

    if op == "shonen_box_path":
        text = read_text(full)
        lines = text.split("\n")
        boxes = shonen_boxes(lines)
        index = int(edit["box"]) - 1
        if index < 0 or index >= len(boxes):
            raise EditError("SHONEN box %s not found in %s" % (edit["box"], path))
        lo, hi = boxes[index]
        block = "\n".join(lines[lo:hi])
        match = KNOWLEDGE_PATH_RE.search(block)
        if match is None:
            raise EditError("SHONEN box %s names no corpus/knowledge path" % edit["box"])
        if "path_source" in edit:
            replacement = resolve_note_path(sandbox, edit["path_source"])
        else:
            replacement = edit["path"]
        block = block[:match.start()] + replacement + block[match.end():]
        lines[lo:hi] = block.split("\n")
        write_text(full, "\n".join(lines))
        return "SHONEN box %s now cites %s" % (edit["box"], replacement)

    raise EditError("unknown op %r" % op)


def resolve_note_path(sandbox, source):
    """Pick a corpus/knowledge note at the sandbox revision by marker state."""
    notes = []
    proc = run(["git", "-C", sandbox, "ls-tree", "-r", "--name-only", "HEAD", "corpus/knowledge/"])
    for name in proc.stdout.splitlines():
        name = name.strip()
        if name.endswith(".md"):
            notes.append(name)
    notes.sort()
    superseded, fresh = None, None
    for name in notes:
        body = read_text(os.path.join(sandbox, name))
        head = "\n".join(body.split("\n")[:20])
        marked = bool(re.search(r"superseded", head, re.IGNORECASE))
        if marked and superseded is None:
            superseded = name
        if not marked and fresh is None:
            fresh = name
    if source == "first_superseded_note":
        if superseded is None:
            raise EditError("no corpus/knowledge note carries a supersession marker in its first 20 lines")
        return superseded
    if source == "first_fresh_note":
        if fresh is None:
            raise EditError("no corpus/knowledge note is free of a supersession marker")
        return fresh
    raise EditError("unknown path_source %r" % source)


# --------------------------------------------------------------------------
# sandbox and detector
# --------------------------------------------------------------------------

def build_sandbox(repo, revision, root):
    os.makedirs(root, exist_ok=True)
    archive = subprocess.run(["git", "-C", repo, "--no-replace-objects", "archive", "--format=tar", revision],
                              capture_output=True)
    if archive.returncode != 0:
        raise RuntimeError("git archive %s failed: %s" % (revision, archive.stderr.decode("utf-8", "replace")))
    with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as tar:
        tar.extractall(root, filter="data")
    run(["git", "init", "-q"], cwd=root)
    run(["git", "config", "user.email", "mutation-probe@example.invalid"], cwd=root)
    run(["git", "config", "user.name", "mutation probe"], cwd=root)
    run(["git", "add", "-A"], cwd=root)
    commit = run(["git", "commit", "-q", "-m", "sandbox base"], cwd=root)
    if commit.returncode != 0:
        raise RuntimeError("sandbox base commit failed: %s" % commit.stderr)
    base = run(["git", "rev-parse", "HEAD"], cwd=root).stdout.strip()
    return base


def run_detector(sandbox):
    proc = subprocess.run([sys.executable, TOOL_PATH, "--revision", "HEAD", "--repo", sandbox],
                          cwd=sandbox, capture_output=True, text=True)
    record = {"exit_code": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
    try:
        payload = json.loads(proc.stdout)
    except ValueError:
        record["parsed"] = False
        record["stdout_head"] = proc.stdout[:400]
        return record
    record["parsed"] = True
    record["status"] = payload.get("status")
    record["checked"] = payload.get("checked")
    record["mismatches"] = payload.get("mismatches")
    record["error"] = payload.get("error")
    record["detail"] = payload.get("detail")
    record["failing_checks"] = [c.get("id") for c in payload.get("checks", []) if c.get("status") == "mismatch"]
    record["checks"] = [{"id": c.get("id"), "status": c.get("status"), "reason": c.get("reason")}
                         for c in payload.get("checks", [])]
    return record


def check_preconditions(sandbox, mutant):
    for precondition in mutant.get("preconditions", []):
        path = os.path.join(sandbox, precondition["file"])
        if not os.path.isfile(path):
            return "file absent: %s" % precondition["file"]
        if precondition["text"] not in read_text(path):
            return "text absent in %s: %r" % (precondition["file"], precondition["text"])
    return None


def expectation_met(expected, baseline, observed):
    expected_exit = expected.get("exit_code")
    expected_failing = set(expected.get("expected_failing_checks", []))
    actual_failing = set(observed.get("failing_checks") or [])
    if expected.get("verdict") == "cannot_evaluate":
        return observed.get("exit_code") == 2
    if expected.get("verdict") == "survived":
        return (observed.get("exit_code") == baseline.get("exit_code")
                and actual_failing == set(baseline.get("failing_checks") or []))
    # killed
    if observed.get("exit_code") != expected_exit:
        return False
    if expected_failing and not expected_failing.issubset(actual_failing):
        return False
    if not expected.get("allow_extra_failing", False) and expected_failing and actual_failing != expected_failing:
        return False
    return True


# --------------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(description="Run the round-26 C2 v2 mutation catalogue.")
    parser.add_argument("--repo", required=True, help="lane repository (read only)")
    parser.add_argument("--revision", required=True, help="revision to archive into the sandbox")
    parser.add_argument("--catalogue", required=True, help="catalogue.json")
    parser.add_argument("--out", default=None, help="write the machine-readable run record here")
    parser.add_argument("--scratch", default=None, help="scratch directory (default: a temp dir)")
    parser.add_argument("--only", default=None, help="comma-separated mutant ids")
    parser.add_argument("--smoke", action="store_true", help="run the baseline only")
    parser.add_argument("--require-checks", type=int, default=27,
                        help="number of checks the v2 tool must report (default 27)")
    parser.add_argument("--allow-non-v2", action="store_true",
                        help="measure even when the tool is not the v2 check set (results are then marked non-v2)")
    parser.add_argument("--keep-sandbox", action="store_true")
    args = parser.parse_args(argv)

    catalogue = json.loads(read_text(args.catalogue))
    mutants = catalogue["mutants"]
    if args.only:
        wanted = [m.strip() for m in args.only.split(",") if m.strip()]
        mutants = [m for m in mutants if m["id"] in wanted]

    scratch = args.scratch or tempfile.mkdtemp(prefix="tsukuroi-r26-c2-mutants-")
    os.makedirs(scratch, exist_ok=True)
    sandbox = os.path.join(scratch, "sandbox")
    if os.path.exists(sandbox):
        shutil.rmtree(sandbox)
    os.makedirs(sandbox)

    record = {
        "catalogue": os.path.abspath(args.catalogue),
        "repo": os.path.abspath(args.repo),
        "revision": args.revision,
        "sandbox": sandbox,
        "scratch": scratch,
        "require_checks": args.require_checks,
        "mutants": [],
    }

    try:
        base = build_sandbox(args.repo, args.revision, sandbox)
    except RuntimeError as exc:
        record["error"] = str(exc)
        emit(record, args.out)
        print(json.dumps(record, indent=1))
        return 2
    record["base_commit"] = base
    pristine_digest = tree_digest(sandbox)
    record["pristine_digest"] = pristine_digest

    baseline = run_detector(sandbox)
    record["baseline"] = baseline
    baseline_clean = baseline.get("exit_code") == 0 and not baseline.get("failing_checks")
    v2 = baseline.get("checked") == args.require_checks
    record["baseline_clean"] = baseline_clean
    record["v2_check_set"] = v2
    if not v2 and not args.allow_non_v2:
        record["note"] = ("the tool at this revision reports %s checks, not the v2 set of %s; "
                          "every mutant would be inconclusive. Use --allow-non-v2 to measure anyway."
                          % (baseline.get("checked"), args.require_checks))

    if args.smoke:
        emit(record, args.out)
        print(json.dumps(record, indent=1))
        return 0

    problems = 0
    for mutant in mutants:
        entry = {"id": mutant["id"], "title": mutant["title"], "targets": mutant.get("targets", []),
                 "declared_rule": mutant.get("declared_rule"), "expected": mutant.get("expected", {})}
        unmet = check_preconditions(sandbox, mutant)
        if unmet:
            entry["status"] = "skipped_precondition"
            entry["detail"] = unmet
            record["mutants"].append(entry)
            problems += 1
            continue
        before = tree_digest(sandbox)
        notes = []
        failed = None
        for edit in mutant.get("edits", []):
            try:
                notes.append(apply_edit(sandbox, edit))
            except EditError as exc:
                failed = str(exc)
                break
        if failed:
            entry["status"] = "error"
            entry["detail"] = failed
            entry["edits_applied"] = notes
            record["mutants"].append(entry)
            problems += 1
            restore(sandbox, base)
            continue
        after = tree_digest(sandbox)
        entry["digest_before"] = before
        entry["digest_after_mutation"] = after
        entry["edits_applied"] = notes
        stage = run(["git", "add", "-A"], cwd=sandbox)
        if stage.returncode != 0:
            entry["status"] = "error"
            entry["detail"] = "git add failed"
            record["mutants"].append(entry)
            problems += 1
            restore(sandbox, base)
            continue
        commit = run(["git", "commit", "-q", "--allow-empty", "-m", "mutant %s" % mutant["id"]], cwd=sandbox)
        if commit.returncode != 0:
            entry["status"] = "error"
            entry["detail"] = "git commit failed: %s" % commit.stderr.strip()
            record["mutants"].append(entry)
            problems += 1
            restore(sandbox, base)
            continue
        entry["mutant_commit"] = run(["git", "rev-parse", "HEAD"], cwd=sandbox).stdout.strip()
        observed = run_detector(sandbox)
        entry["observed"] = observed
        if not baseline_clean:
            entry["status"] = "inconclusive"
            entry["verdict"] = "inconclusive"
            entry["detail"] = "the baseline is not clean (exit %s, failing %s)" % (
                baseline.get("exit_code"), baseline.get("failing_checks"))
            problems += 1
        elif not v2 and not args.allow_non_v2:
            entry["status"] = "inconclusive"
            entry["verdict"] = "inconclusive"
            entry["detail"] = "the tool at this revision is not the v2 check set (%s checks)" % baseline.get("checked")
            problems += 1
        else:
            changed = observed.get("exit_code") != baseline.get("exit_code")
            entry["verdict"] = "killed" if changed else "survived"
            entry["status"] = "measured"
            entry["expectation_met"] = expectation_met(mutant.get("expected", {}), baseline, observed)
            if "alt_expected" in mutant:
                entry["expectation_met_alt"] = expectation_met(mutant["alt_expected"], baseline, observed)
            if not entry["expectation_met"] and not entry.get("expectation_met_alt", False):
                problems += 1
        restore(sandbox, base)
        entry["restored_digest"] = tree_digest(sandbox)
        entry["restored"] = entry["restored_digest"] == pristine_digest
        if not entry["restored"]:
            problems += 1
        record["mutants"].append(entry)

    final_digest = tree_digest(sandbox)
    record["final_digest"] = final_digest
    record["restored_exactly"] = final_digest == pristine_digest
    record["problems"] = problems
    record["summary"] = summarize(record)
    emit(record, args.out)
    print(json.dumps(record["summary"], indent=1))
    return 0 if problems == 0 else 1


def restore(sandbox, base):
    run(["git", "reset", "-q", "--hard", base], cwd=sandbox)
    run(["git", "clean", "-qfd"], cwd=sandbox)


def summarize(record):
    counts = {"measured": 0, "killed": 0, "survived": 0, "inconclusive": 0,
              "skipped_precondition": 0, "error": 0, "expectation_not_met": 0, "not_restored": 0}
    for entry in record["mutants"]:
        counts[entry["status"]] = counts.get(entry["status"], 0) + 1
        if entry.get("verdict") == "killed":
            counts["killed"] += 1
        elif entry.get("verdict") == "survived":
            counts["survived"] += 1
        if entry.get("expectation_met") is False:
            counts["expectation_not_met"] += 1
        if entry.get("restored") is False:
            counts["not_restored"] += 1
    counts["baseline_exit"] = record.get("baseline", {}).get("exit_code")
    counts["baseline_mismatches"] = record.get("baseline", {}).get("mismatches")
    counts["baseline_checked"] = record.get("baseline", {}).get("checked")
    counts["baseline_failing"] = record.get("baseline", {}).get("failing_checks")
    counts["pristine_digest"] = record.get("pristine_digest")
    counts["final_digest"] = record.get("final_digest")
    counts["restored_exactly"] = record.get("restored_exactly")
    return counts


def emit(record, path):
    if not path:
        return
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(record, handle, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    sys.exit(main())
