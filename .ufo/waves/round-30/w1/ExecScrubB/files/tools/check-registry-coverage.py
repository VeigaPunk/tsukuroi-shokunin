#!/usr/bin/env python3
"""Check the operative SKILL.md gate/probe registry against committed tools. Git subprocesses follow the round-30 child environment contract."""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
sys.dont_write_bytecode = True
import tempfile
from pathlib import Path

from _revision import E_GIT, RevisionError, bind
import _revision

PASS, FAIL, CANNOT = 0, 1, 2
ROOT = Path(__file__).resolve().parents[1]

_GIT_SANDBOX = tempfile.TemporaryDirectory(prefix="registry-coverage-git-")
_GIT_HOME = Path(_GIT_SANDBOX.name) / "home"
_GIT_HOME.mkdir()


def clean_env():
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update({
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_PAGER": "cat",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_CEILING_DIRECTORIES": str(Path(_GIT_SANDBOX.name).parent),
        "HOME": str(_GIT_HOME),
        "XDG_CONFIG_HOME": str(_GIT_HOME / ".config"),
        "PATH": "/usr/bin:/bin",
        "LC_ALL": "C",
    })
    return env


_revision.clean_env = clean_env
HEADER = ("Name", "Kind", "Entry command", "Verdict map", "Self-test",
          "Pinned values", "Write scope", "Owner")
REGISTRY_HEADING = re.compile(
    r"^## Gate and probe registry — round([0-9]+) superseding current rows$")
ATX_HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+")
TOOL_PATH = re.compile(r"(?<![A-Za-z0-9_.-])tools/[A-Za-z0-9_./-]+")
SELFTEST_FLAG = re.compile(r"--self-?test(?:-[A-Za-z0-9-]+)?")
VERDICT_ZERO = re.compile(r"(?<![0-9])0(?![0-9])")
VERDICT_ONE = re.compile(r"(?<![0-9])1(?![0-9])")
VERDICT_TWO = re.compile(r"(?<![0-9])2(?![0-9])")
AUDIT_LIVE_MAP = (
    "live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; "
    "selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; "
    "no live DEGRADED; not operator clearance")
AUDIT_LIVE_ENTRY = "`bash tools/boot-chain-audit.sh --live` (not live-run round20)"
AUDIT_SELFTEST_ENTRY = "`bash tools/boot-chain-audit.sh --selftest`"
AUDIT_WRITE_SCOPE = "private fixtures; live reads only when separately authorized; no host writes"


class TableError(ValueError):
    pass


class GitReader:
    """Read regular committed blobs only; never follow worktree symlinks."""

    def __init__(self, root):
        self.root = Path(root)
        self.cache = {}

    def _git(self, *args):
        try:
            proc = subprocess.run(["git", "--no-pager", "-C", str(self.root), *args],
                                  stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, env=clean_env(), timeout=60)
        except subprocess.TimeoutExpired as exc:
            raise RevisionError(E_GIT, "git", f"git {args[0]} exceeded 60s") from exc
        except OSError as exc:
            raise RevisionError(E_GIT, "git", str(exc)[:120]) from exc
        return proc

    @staticmethod
    def _detail(proc):
        return proc.stderr.decode("utf-8", "replace").strip()[:120] or f"exit={proc.returncode}"

    def _tree_entries(self, revision, pathspec):
        proc = self._git("ls-tree", "-r", "-z", "--full-tree", revision, "--", pathspec)
        if proc.returncode:
            raise RevisionError(E_GIT, pathspec,
                                "git ls-tree failed: " + self._detail(proc))
        entries = []
        for item in proc.stdout.split(b"\0"):
            if not item:
                continue
            try:
                metadata, name = item.split(b"\t", 1)
                mode, kind, oid = metadata.split(b" ", 2)
            except ValueError as exc:
                raise RevisionError(E_GIT, pathspec, "git ls-tree returned malformed entry") from exc
            entries.append((mode, kind, oid.decode("ascii", "replace"),
                            name.decode("utf-8", "replace")))
        return entries

    def tool_files(self, revision):
        files = set()
        for mode, kind, _oid, name in self._tree_entries(revision, "tools/"):
            if (mode in (b"100644", b"100755") and kind == b"blob"
                    and name.startswith("tools/")
                    and "__pycache__" not in name.split("/")):
                files.add(name)
        return files

    def read_file(self, revision, path):
        key = (revision, path)
        if key in self.cache:
            return self.cache[key]
        entries = [entry for entry in self._tree_entries(revision, path)
                   if entry[3] == path]
        if not entries or len(entries) != 1:
            self.cache[key] = None
            return None
        mode, kind, _oid, _name = entries[0]
        if mode not in (b"100644", b"100755") or kind != b"blob":
            self.cache[key] = None
            return None
        proc = self._git("show", f"{revision}:{path}")
        if proc.returncode:
            raise RevisionError(E_GIT, path, "git show failed: " + self._detail(proc))
        self.cache[key] = proc.stdout
        return proc.stdout


def _split_table_row(line):
    """Split Markdown cells, preserving escaped pipes inside cells."""
    cells, cell = [], []
    escaped = False
    for char in line.strip():
        if char == "|" and not escaped:
            cells.append("".join(cell).strip())
            cell = []
        else:
            cell.append(char)
        if char == "\\" and not escaped:
            escaped = True
        else:
            escaped = False
    cells.append("".join(cell).strip())
    if cells and cells[0] == "":
        cells.pop(0)
    if cells and cells[-1] == "":
        cells.pop()
    return tuple(cells)


def _is_separator(cells):
    return (len(cells) == len(HEADER)
            and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells))



def _outside_fenced_code(lines):
    output = []
    fence_char, fence_size = None, 0
    for line in lines:
        stripped = line.lstrip(" ")
        indent = len(line) - len(stripped)
        if fence_char is None:
            if indent <= 3 and stripped[:1] in ("`", "~"):
                marker = stripped[0]
                size = len(stripped) - len(stripped.lstrip(marker))
                info = stripped[size:]
                if size >= 3 and (marker != "`" or "`" not in info):
                    fence_char, fence_size = marker, size
                    output.append("")
                    continue
            output.append(line)
            continue
        if (indent <= 3 and len(stripped) >= fence_size
                and all(char == fence_char for char in stripped[:fence_size])
                and not stripped[fence_size:].strip()):
            fence_char, fence_size = None, 0
        output.append("")
    return output

def _operative_rows(skill, ignore_fenced_code=False):
    lines = skill.splitlines()
    if ignore_fenced_code:
        lines = _outside_fenced_code(lines)
    headings = []
    for index, line in enumerate(lines):
        match = REGISTRY_HEADING.fullmatch(line)
        if match:
            headings.append((int(match.group(1)), index))
    if not headings:
        raise TableError("no exact Gate and probe registry heading")
    highest = max(number for number, _index in headings)
    selected = [(number, index) for number, index in headings if number == highest]
    if len(selected) != 1:
        raise TableError(f"round{highest} heading is duplicated")

    _number, start = selected[0]
    end = len(lines)
    for index in range(start + 1, len(lines)):
        match = ATX_HEADING.match(lines[index])
        if match and len(match.group(1)) <= 2:
            end = index
            break
    section = lines[start:end]
    header_positions = [index for index, line in enumerate(section)
                        if _split_table_row(line) == HEADER]
    if len(header_positions) != 1:
        raise TableError("operative section must contain exactly one required registry header")
    header_index = header_positions[0]
    if header_index + 1 >= len(section):
        raise TableError("registry header has no Markdown separator")
    separator = _split_table_row(section[header_index + 1])
    if not _is_separator(separator):
        raise TableError("registry header is not followed by an eight-column separator")

    rows = []
    for offset in range(header_index + 2, len(section)):
        line = section[offset]
        if not line.strip():
            break
        cells = _split_table_row(line)
        if _is_separator(cells):
            continue
        if len(cells) != len(HEADER):
            if line.lstrip().startswith("|"):
                raise TableError(f"malformed registry row at line {start + offset + 1}")
            break
        rows.append({"cells": cells, "line": start + offset + 1})
    return rows


def _paths(text):
    found = set()
    for match in TOOL_PATH.finditer(text):
        path = match.group(0).rstrip(".")
        if path != "tools/":
            found.add(path)
    return found


def _finding(fid, site, detail):
    return {"id": fid, "site": str(site), "detail": str(detail)[:240]}


def _finding_sort_key(item):
    return item["id"], item["site"], item["detail"]


def _coverage(rows, tools, reader, revision):
    findings = []
    covering = {path: [] for path in tools}
    for row in rows:
        cells = row["cells"]
        name, kind, entry, verdict, selftest, _pinned, _scope, _owner = cells
        entry_paths = _paths(entry)
        self_paths = _paths(selftest)
        row_paths = entry_paths | self_paths
        site = f"SKILL.md:{row['line']}"
        if kind not in ("gate", "probe", "library"):
            findings.append(_finding("REGISTRY-KIND-INVALID", site,
                                     f"{name or '(unnamed)'} has invalid kind {kind!r}"))
        # Round-19 falsify FxCritC3: a discovered-tool row that merely mentioned a
        # baseline path masked that baseline row's removal. One row, one tool.
        known_paths = sorted(row_paths & tools)
        if len(known_paths) > 1:
            findings.append(_finding("REGISTRY-ROW-AMBIGUOUS", site,
                                     f"{name or '(unnamed)'} names {len(known_paths)} tools: "
                                     + ", ".join(known_paths)))
        # Round-19 falsify FxMutRegistry: a gate verdict map with 2->97 still contained
        # 0 and 1 and passed. Gate rows must publish all three codes; probes need 0 and 2.
        if kind == "gate":
            missing = [code for code, pattern in
                       (("0", VERDICT_ZERO), ("1", VERDICT_ONE), ("2", VERDICT_TWO))
                       if not pattern.search(verdict)]
            if missing:
                findings.append(_finding("REGISTRY-VERDICT-INCOMPLETE", site,
                                         f"{name or '(unnamed)'} gate verdict map lacks code(s) "
                                         + ", ".join(missing)))
        elif kind == "probe":
            missing = [code for code, pattern in
                       (("0", VERDICT_ZERO), ("2", VERDICT_TWO))
                       if not pattern.search(verdict)]
            if missing:
                findings.append(_finding("REGISTRY-VERDICT-INCOMPLETE", site,
                                         f"{name or '(unnamed)'} probe verdict map lacks code(s) "
                                         + ", ".join(missing)))
        for path in sorted(row_paths - tools):
            findings.append(_finding("REGISTRY-ROW-ORPHAN", site,
                                     f"registry row names absent regular tool {path}"))
        for path in row_paths & tools:
            covering[path].append(row)

        flags = sorted(set(SELFTEST_FLAG.findall(selftest)))
        targets = self_paths if self_paths else row_paths
        for flag in flags:
            for path in sorted(targets & tools):
                source = reader.read_file(revision, path)
                text = source.decode("utf-8", "replace") if source is not None else ""
                if flag not in text:
                    findings.append(_finding("REGISTRY-SELFTEST-UNRESOLVED", site,
                                             f"{flag} is absent from {path}"))

    for path in sorted(tools):
        rows_for_tool = covering[path]
        if not rows_for_tool:
            findings.append(_finding("REGISTRY-ROW-MISSING", path,
                                     "no operative row names this regular tools/ file"))
        elif len(rows_for_tool) > 1:
            findings.append(_finding("REGISTRY-ROW-DUPLICATE", path,
                                     f"{len(rows_for_tool)} operative rows cover this tool"))
    findings.sort(key=_finding_sort_key)
    covered = {path for path, matching in covering.items() if matching}
    return findings, covered


def _audit_live_map(rows):
    """Require the one operative audit row and its explicit live/selftest modes."""
    audit_path = "tools/boot-chain-audit.sh"
    matches = [row for row in rows if row["cells"][0] == "boot-chain-audit"]
    references = [
        row for row in rows
        if audit_path in (_paths(row["cells"][2]) | _paths(row["cells"][4]))
    ]
    if (len(matches) != 1 or len(references) != 1
            or references[0] is not matches[0]):
        return [_finding("REGISTRY-AUDIT-LIVE-MAP", "SKILL.md",
                         "exactly one operative row may reference boot-chain-audit")]
    row = matches[0]
    cells = row["cells"]
    if (cells[1] != "probe"
            or _paths(cells[2]) != {audit_path}
            or cells[2] != AUDIT_LIVE_ENTRY
            or _paths(cells[4]) != {audit_path}
            or cells[4] != AUDIT_SELFTEST_ENTRY
            or " ".join(cells[3].split()) != AUDIT_LIVE_MAP
            or cells[6] != AUDIT_WRITE_SCOPE):
        return [_finding("REGISTRY-AUDIT-LIVE-MAP", f"SKILL.md:{row['line']}",
                         "live/selftest modes, no-write scope and schema-v2 map required")]
    return []


def _base_counts(tool_total=0, row_total=0, covered=0, findings=0):
    return {"tools_total": tool_total, "rows_total": row_total,
            "registered": covered, "missing": tool_total - covered,
            "findings": findings}


def _emit(code, revision, branch, branch_tip, counts, findings):
    status = {PASS: "PASS", FAIL: "FAIL", CANNOT: "CANNOT_EVALUATE"}[code]
    payload = {"status": status, "revision": revision, "branch": branch,
               "branch_tip": branch_tip, "counts": counts,
               "findings": sorted(findings, key=_finding_sort_key)}
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return code


def build_parser():
    parser = argparse.ArgumentParser(
        description="Check the operative SKILL.md registry against committed tools/.",
        exit_on_error=False)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--revision", metavar="REV",
                        help="7-64 hex commit landed on the selected branch")
    choice.add_argument("--selftest", action="store_true", help="hermetic fixture suite")
    parser.add_argument("--branch", default="master", help="landed branch (default master)")
    parser.add_argument("--baseline-tools", metavar="REV",
                        help="compare the inspected tool set with this landed revision")
    parser.add_argument("--audit-live-map", action="store_true",
                        help="also enforce the finite boot-chain-audit schema-v2 mode map")
    return parser


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            args = build_parser().parse_args(argv)
    except (argparse.ArgumentError, SystemExit) as exc:
        if isinstance(exc, SystemExit) and exc.code == 0:
            return PASS
        branch = "master"
        return _emit(CANNOT, None, branch, None, _base_counts(findings=1),
                     [_finding("E-CLI", "cli", "--revision REV or --selftest required")])
    if args.selftest:
        if args.baseline_tools:
            return _emit(CANNOT, None, args.branch, None, _base_counts(findings=1),
                         [_finding("E-CLI", "cli", "--baseline-tools is not valid with --selftest")])
        return selftest()

    binding = None
    try:
        binding = bind(ROOT, args.revision, args.branch)
        baseline_binding = (bind(ROOT, args.baseline_tools, args.branch)
                            if args.baseline_tools is not None else None)
        reader = GitReader(ROOT)
        skill_data = reader.read_file(binding.sha, "SKILL.md")
        if skill_data is None:
            raise TableError("SKILL.md is absent or is not a regular committed file")
        rows = _operative_rows(skill_data.decode("utf-8", "replace"),
                               ignore_fenced_code=args.audit_live_map)
        tools = reader.tool_files(binding.sha)
        findings, covered = _coverage(rows, tools, reader, binding.sha)
        map_findings = _audit_live_map(rows) if args.audit_live_map else []
        findings.extend(map_findings)
        counts = _base_counts(len(tools), len(rows), len(covered), len(findings))
        if args.audit_live_map:
            counts["audit_live_map_errors"] = len(map_findings)
        if baseline_binding is not None:
            baseline_tools = reader.tool_files(baseline_binding.sha)
            counts["baseline_tools_total"] = len(baseline_tools)
            counts["baseline_tools_missing"] = len(baseline_tools - covered)
            counts["discovered_tools"] = sorted(tools - baseline_tools)
        code = FAIL if findings else PASS
        return _emit(code, binding.sha, binding.branch, binding.branch_tip, counts, findings)
    except TableError as exc:
        return _emit(CANNOT, binding.sha if binding else args.revision,
                     binding.branch if binding else args.branch,
                     binding.branch_tip if binding else None,
                     _base_counts(findings=1),
                     [_finding("E-REGISTRY-TABLE", "SKILL.md", str(exc))])
    except RevisionError as exc:
        return _emit(CANNOT, binding.sha if binding else args.revision,
                     binding.branch if binding else args.branch,
                     binding.branch_tip if binding else None,
                     _base_counts(findings=1), [_finding(exc.fid, exc.site, exc.detail)])


def _row(name, kind, entry, verdict, selftest, pinned="fixture", scope="read-only", owner="fixture"):
    cells = (name, kind, entry, verdict, selftest, pinned, scope, owner)
    return "| " + " | ".join(cells) + " |"


def _table(rows):
    header = "| " + " | ".join(HEADER) + " |"
    divider = "| " + " | ".join("---" for _cell in HEADER) + " |"
    return "\n".join((header, divider, *rows))


def _skill(rows, round_number=1, before=""):
    return (before + f"\n## Gate and probe registry — round{round_number} superseding current rows\n\n"
            + _table(rows) + "\n")


def _fixture_git(repo):
    env = clean_env()
    proc = subprocess.run(["git", "init", "--quiet", "-b", "master", str(repo)],
                          stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, env=env)
    if proc.returncode:
        raise RuntimeError("git init failed: " + GitReader._detail(proc))


def _fixture_commit(repo, files, message):
    for child in repo.iterdir():
        if child.name == ".git":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
    for name, content in files.items():
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    env = clean_env()
    add = subprocess.run(["git", "-C", str(repo), "add", "-A"], stdin=subprocess.DEVNULL,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    if add.returncode:
        raise RuntimeError("git add failed: " + GitReader._detail(add))
    commit = subprocess.run(["git", "-C", str(repo), "-c", "user.name=Registry Selftest",
                             "-c", "user.email=registry-selftest@invalid",
                             "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", message],
                           stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, env=env)
    if commit.returncode:
        raise RuntimeError("git commit failed: " + GitReader._detail(commit))
    rev = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                         stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, env=env)
    if rev.returncode:
        raise RuntimeError("git rev-parse failed: " + GitReader._detail(rev))
    return rev.stdout.decode("ascii").strip()


def _invoke(revision, baseline=None, audit_live_map=False):
    argv = ["--revision", revision]
    if baseline is not None:
        argv.extend(("--baseline-tools", baseline))
    if audit_live_map:
        argv.append("--audit-live-map")
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        code = main(argv)
    payload = json.loads(output.getvalue())
    return code, payload



def selftest():
    global ROOT
    passed, failures = 0, []
    total = 23


    def check(name, code, payload, expected_code, predicate):
        nonlocal passed
        if code == expected_code and predicate(payload):
            passed += 1
        else:
            failures.append(f"{name}: exit={code}, payload={payload!r}")

    old_root = ROOT
    try:
        with tempfile.TemporaryDirectory(prefix="tsukuroi-registry-selftest-") as tmp:
            repo = Path(tmp) / "fixture"
            _fixture_git(repo)
            ROOT = repo
            tool = "tools/probe.py"
            source = "# fixture source exposes --selftest\nSELFTEST = '--selftest'\n"
            clean_row = _row("probe", "probe", "python3 tools/probe.py", "0 ok; 1 fail; 2 could-not-evaluate",
                             "python3 tools/probe.py --selftest")

            rev = _fixture_commit(repo, {"SKILL.md": _skill([clean_row]), tool: source}, "clean")
            code, payload = _invoke(rev)
            check("clean", code, payload, PASS,
                  lambda p: p["status"] == "PASS" and p["counts"]["tools_total"] == 1
                  and p["counts"]["registered"] == 1 and not p["findings"])

            rev = _fixture_commit(repo, {"SKILL.md": _skill([]), tool: source}, "missing-row")
            code, payload = _invoke(rev)
            check("missing-row", code, payload, FAIL,
                  lambda p: "REGISTRY-ROW-MISSING" in {f["id"] for f in p["findings"]})

            rev = _fixture_commit(repo, {"SKILL.md": _skill([clean_row, clean_row]), tool: source},
                                  "duplicate-row")
            code, payload = _invoke(rev)
            check("duplicate-row", code, payload, FAIL,
                  lambda p: "REGISTRY-ROW-DUPLICATE" in {f["id"] for f in p["findings"]})

            ambiguous = _row("both", "library", "python3 tools/probe.py", "n/a",
                             "python3 tools/new.py --selftest")
            rev = _fixture_commit(repo, {"SKILL.md": _skill([ambiguous]), tool: source,
                                         "tools/new.py": source}, "ambiguous-row")
            code, payload = _invoke(rev)
            check("ambiguous-row", code, payload, FAIL,
                  lambda p: "REGISTRY-ROW-AMBIGUOUS" in {f["id"] for f in p["findings"]})

            orphan_row = _row("gone", "library", "tools/gone.py", "n/a", "n/a")
            rev = _fixture_commit(repo, {"SKILL.md": _skill([orphan_row]), tool: source}, "orphan-row")
            code, payload = _invoke(rev)
            check("orphan-row", code, payload, FAIL,
                  lambda p: {"REGISTRY-ROW-ORPHAN", "REGISTRY-ROW-MISSING"}
                  <= {f["id"] for f in p["findings"]})

            invalid_kind = _row("probe", "task", "python3 tools/probe.py", "0 ok; 1 fail; 2 could-not-evaluate",
                                 "python3 tools/probe.py --selftest")
            rev = _fixture_commit(repo, {"SKILL.md": _skill([invalid_kind]), tool: source}, "invalid-kind")
            code, payload = _invoke(rev)
            check("invalid-kind", code, payload, FAIL,
                  lambda p: "REGISTRY-KIND-INVALID" in {f["id"] for f in p["findings"]})

            unresolved = _row("probe", "probe", "python3 tools/probe.py", "0 ok; 1 fail; 2 could-not-evaluate",
                              "python3 tools/probe.py --selftest")
            rev = _fixture_commit(repo, {"SKILL.md": _skill([unresolved]),
                                         tool: "# no selftest flag here\n"}, "unresolved-selftest")
            code, payload = _invoke(rev)
            check("unresolved-selftest", code, payload, FAIL,
                  lambda p: "REGISTRY-SELFTEST-UNRESOLVED" in {f["id"] for f in p["findings"]})

            incomplete = _row("gate", "gate", "python3 tools/probe.py", "0 clean; 2 cannot",
                              "python3 tools/probe.py --selftest")
            rev = _fixture_commit(repo, {"SKILL.md": _skill([incomplete]), tool: source}, "incomplete-verdict")
            code, payload = _invoke(rev)
            check("incomplete-verdict", code, payload, FAIL,
                  lambda p: "REGISTRY-VERDICT-INCOMPLETE" in {f["id"] for f in p["findings"]})

            older = ("## Gate and probe registry — round1 superseding current rows\n\n"
                     + _table([orphan_row]) + "\n\n")
            rev = _fixture_commit(repo, {"SKILL.md": _skill([clean_row], 2, older), tool: source},
                                  "unique-highest-table")
            code, payload = _invoke(rev)
            check("unique-highest-table", code, payload, PASS,
                  lambda p: p["counts"]["rows_total"] == 1 and not p["findings"])

            duplicate_tables = (_skill([clean_row], 4) + "\n"
                                + _skill([clean_row], 4))
            rev = _fixture_commit(repo, {"SKILL.md": duplicate_tables, tool: source}, "duplicate-highest")
            code, payload = _invoke(rev)
            check("duplicate-highest", code, payload, CANNOT,
                  lambda p: p["findings"][0]["id"] == "E-REGISTRY-TABLE")

            rev = _fixture_commit(repo, {"SKILL.md": "# no registry\n", tool: source}, "no-table")
            code, payload = _invoke(rev)
            check("no-table", code, payload, CANNOT,
                  lambda p: p["findings"][0]["id"] == "E-REGISTRY-TABLE")

            old_tool = "tools/old.py"
            old_row = _row("old", "library", "python3 tools/old.py", "n/a", "n/a")
            baseline = _fixture_commit(repo, {"SKILL.md": _skill([old_row]), old_tool: "# old\n"},
                                       "baseline-tools")
            new_tool = "tools/new.py"
            new_row = _row("new", "probe", "python3 tools/new.py", "0 ok; 1 fail",
                           "python3 tools/new.py --selftest")
            rev = _fixture_commit(repo, {"SKILL.md": _skill([new_row]), old_tool: "# old\n",
                                         new_tool: source}, "baseline-split")
            code, payload = _invoke(rev, baseline)
            check("baseline-split", code, payload, FAIL,
                  lambda p: p["counts"].get("baseline_tools_total") == 1
                  and p["counts"].get("baseline_tools_missing") == 1
                  and p["counts"].get("discovered_tools") == [new_tool]
                  and p["counts"]["missing"] == 1)

            code, payload = _invoke("0" * 40)
            check("bad-revision", code, payload, CANNOT,
                  lambda p: p["findings"][0]["id"] == "E-REVISION-INVALID")

            audit_source = "# fixture audit source\nLIVE = '--live'\nSELFTEST = '--selftest'\n"
            corrected_audit = _row(
                "boot-chain-audit", "probe", AUDIT_LIVE_ENTRY, AUDIT_LIVE_MAP,
                AUDIT_SELFTEST_ENTRY, scope=AUDIT_WRITE_SCOPE)
            legacy_map = AUDIT_LIVE_MAP.replace(
                "live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate;",
                "live: 0 CONSISTENT/observation;1 DEGRADED;2 UNKNOWN/could-not-evaluate;")
            legacy_audit = _row(
                "boot-chain-audit", "probe", AUDIT_LIVE_ENTRY, legacy_map,
                AUDIT_SELFTEST_ENTRY, scope=AUDIT_WRITE_SCOPE)

            rev = _fixture_commit(
                repo, {"SKILL.md": _skill([corrected_audit]), "tools/boot-chain-audit.sh": audit_source},
                "audit-live-map-correct")
            code, payload = _invoke(rev)
            check("audit-live-map-correct-default", code, payload, PASS,
                  lambda p: "audit_live_map_errors" not in p["counts"]
                  and not p["findings"])
            code, payload = _invoke(rev, audit_live_map=True)
            check("audit-live-map-correct", code, payload, PASS,
                  lambda p: p["counts"].get("audit_live_map_errors") == 0
                  and not p["findings"])

            rev = _fixture_commit(
                repo, {"SKILL.md": _skill([legacy_audit]), "tools/boot-chain-audit.sh": audit_source},
                "audit-live-map-live1")
            code, payload = _invoke(rev)
            check("audit-live-map-legacy-default", code, payload, PASS,
                  lambda p: "audit_live_map_errors" not in p["counts"]
                  and not p["findings"])
            code, payload = _invoke(rev, audit_live_map=True)
            check("audit-live-map-live1", code, payload, FAIL,
                  lambda p: p["counts"].get("audit_live_map_errors") == 1
                  and [finding["id"] for finding in p["findings"]]
                  == ["REGISTRY-AUDIT-LIVE-MAP"])

            older_audit = _row(
                "boot-chain-audit", "probe", AUDIT_LIVE_ENTRY, legacy_map,
                AUDIT_SELFTEST_ENTRY, scope=AUDIT_WRITE_SCOPE)
            rev = _fixture_commit(
                repo, {"SKILL.md": _skill([corrected_audit], round_number=2,
                                          before=_skill([older_audit], round_number=1)),
                       "tools/boot-chain-audit.sh": audit_source},
                "audit-live-map-highest-table")
            code, payload = _invoke(rev, audit_live_map=True)
            check("audit-live-map-highest-table", code, payload, PASS,
                  lambda p: p["counts"].get("audit_live_map_errors") == 0
                  and not p["findings"])
            rev = _fixture_commit(
                repo, {"SKILL.md": _skill([legacy_audit], round_number=2,
                                          before=_skill([corrected_audit], round_number=1)),
                       "tools/boot-chain-audit.sh": audit_source},
                "audit-live-map-historical-only-fix")
            code, payload = _invoke(rev, audit_live_map=True)
            check("audit-live-map-historical-only-fix", code, payload, FAIL,
                  lambda p: p["counts"].get("audit_live_map_errors") == 1
                  and [finding["id"] for finding in p["findings"]]
                  == ["REGISTRY-AUDIT-LIVE-MAP"])

            fenced_skill = (_skill([legacy_audit], round_number=19)
                            + "\n```markdown\n"
                            + _skill([corrected_audit], round_number=20)
                            + "```\n")
            rev = _fixture_commit(
                repo, {"SKILL.md": fenced_skill, "tools/boot-chain-audit.sh": audit_source},
                "audit-live-map-fenced-example")
            code, payload = _invoke(rev, audit_live_map=True)
            check("audit-live-map-fenced-example", code, payload, FAIL,
                  lambda p: p["counts"].get("audit_live_map_errors") == 1
                  and "REGISTRY-AUDIT-LIVE-MAP"
                  in {finding["id"] for finding in p["findings"]})

            alias_audit = _row(
                "audit-alias", "probe", AUDIT_LIVE_ENTRY, AUDIT_LIVE_MAP,
                AUDIT_SELFTEST_ENTRY, scope=AUDIT_WRITE_SCOPE)
            rev = _fixture_commit(
                repo, {"SKILL.md": _skill([corrected_audit, alias_audit]),
                       "tools/boot-chain-audit.sh": audit_source},
                "audit-live-map-duplicate-path")
            code, payload = _invoke(rev, audit_live_map=True)
            check("audit-live-map-duplicate-path", code, payload, FAIL,
                  lambda p: p["counts"].get("audit_live_map_errors") == 1
                  and "REGISTRY-AUDIT-LIVE-MAP"
                  in {finding["id"] for finding in p["findings"]})

            wrong_mode = _row(
                "boot-chain-audit", "probe", AUDIT_SELFTEST_ENTRY, AUDIT_LIVE_MAP,
                AUDIT_LIVE_ENTRY, scope=AUDIT_WRITE_SCOPE)
            rev = _fixture_commit(
                repo, {"SKILL.md": _skill([wrong_mode]), "tools/boot-chain-audit.sh": audit_source},
                "audit-live-map-swapped-modes")
            code, payload = _invoke(rev, audit_live_map=True)
            check("audit-live-map-swapped-modes", code, payload, FAIL,
                  lambda p: p["counts"].get("audit_live_map_errors") == 1
                  and "REGISTRY-AUDIT-LIVE-MAP"
                  in {finding["id"] for finding in p["findings"]})

            wrong_scope = _row(
                "boot-chain-audit", "probe", AUDIT_LIVE_ENTRY, AUDIT_LIVE_MAP,
                AUDIT_SELFTEST_ENTRY, scope="host/package writes")
            rev = _fixture_commit(
                repo, {"SKILL.md": _skill([wrong_scope]), "tools/boot-chain-audit.sh": audit_source},
                "audit-live-map-write-scope")
            code, payload = _invoke(rev, audit_live_map=True)
            check("audit-live-map-write-scope", code, payload, FAIL,
                  lambda p: p["counts"].get("audit_live_map_errors") == 1
                  and "REGISTRY-AUDIT-LIVE-MAP"
                  in {finding["id"] for finding in p["findings"]})


    except Exception as exc:
        failures.append(f"selftest infrastructure: {type(exc).__name__}: {exc}")
    finally:
        ROOT = old_root

    if failures:
        print(f"FAIL ({total} cases, {passed} passed, {len(failures)} failed)")
        print("\n".join("  " + item for item in failures))
        return FAIL
    print(f"PASS ({total} cases, {passed} passed, 0 failed)")
    return PASS


if __name__ == "__main__":
    sys.exit(main())
