#!/usr/bin/env python3
"""Mutation runner for tools/check-self-assessment.py (round 25, C1).

Seat: MutSelfAssessPlan. Runs the checker read-only against one throwaway git
repo per mutation fixture and records killed / survived.

Safety
------
* The lane repository is READ ONLY here: `git archive` is the only lane git
  command, and it writes nothing.
* Every scratch repository is created with `git init` and has NO remote, so no
  push or fetch can reach the lane.  No `git push`/`git fetch` is ever issued.
* Temporary repositories live under --workdir (default /fast/scratch/hyaku/
  tsukuroi-r25/MutSelfAssessPlan/repos) and are removed unless --keep.
* The checker is invoked as `python3 tools/check-self-assessment.py --revision
  <commit>` inside the scratch repo; nothing else in the lane is touched.

Usage
-----
  python3 run_mutations.py --lane <repo> --revision <REV> \\
      --fixtures <dir> [--tool <path to check-self-assessment.py>] \\
      [--workdir <dir>] [--json out.json] [--keep]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

AXES_HEADING_RE = re.compile(r"^##\s+Axes\s+—")
CAPS_HEADING_RE = re.compile(r"^##\s+Capabilities\b")
CHECK_ID_RE = re.compile(r"\bK(\d{2})\b")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def run(cmd, cwd=None, timeout=3600, env=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env)


# --------------------------------------------------------------------------
# section surgery
# --------------------------------------------------------------------------
def tables_under(lines: list[str], heading_re: re.Pattern):
    """Table blocks inside the LAST section whose heading matches.

    Tool-faithful: the section ends at the next "## " heading, blocks are runs
    of pipe-prefixed lines, and the table chosen is the last one whose header
    names the expected key (else the last block).
    """
    hits = [i for i, l in enumerate(lines) if heading_re.match(l)]
    if not hits:
        return None
    start = hits[-1]
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if re.match(r"^##\s", lines[i]):
            end = i
            break
    blocks = []
    index = start + 1
    while index < end:
        if lines[index].lstrip().startswith("|"):
            lo = index
            while index < end and lines[index].lstrip().startswith("|"):
                index += 1
            blocks.append((lo, index))
        else:
            index += 1
    return start, end, blocks


def replace_last_table(text: str, heading_re: re.Pattern, new_table: list[str],
                       header_key: str) -> str:
    lines = text.split("\n")
    found = tables_under(lines, heading_re)
    if not found:
        raise RuntimeError(f"heading {heading_re.pattern} not found")
    _, _, blocks = found
    if not blocks:
        raise RuntimeError(f"no table under {heading_re.pattern}")
    chosen = None
    for lo, hi in reversed(blocks):
        header = split_cells(lines[lo])
        if header and header[0].strip().lower() == header_key.lower():
            chosen = (lo, hi)
            break
    if chosen is None:
        chosen = blocks[-1]
    lo, hi = chosen
    out = lines[:lo] + list(new_table) + lines[hi:]
    return "\n".join(out)


def split_cells(line: str) -> list[str]:
    """Split a markdown table row on pipes outside backtick code spans."""
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
    return [c.strip() for c in cells]


# --------------------------------------------------------------------------
# scratch repo construction
# --------------------------------------------------------------------------
def build_repo(lane: Path, rev: str, dest: Path, tool_src: Path | None):
    dest.mkdir(parents=True, exist_ok=True)
    archive = subprocess.run(["git", "-C", str(lane), "archive", rev], capture_output=True)
    if archive.returncode != 0:
        raise RuntimeError("git archive failed: " + archive.stderr.decode("utf-8", "replace"))
    tar = subprocess.run(["tar", "-x", "-C", str(dest)], input=archive.stdout, capture_output=True)
    if tar.returncode != 0:
        raise RuntimeError("tar failed: " + tar.stderr.decode("utf-8", "replace"))
    if tool_src is not None:
        tools = dest / "tools"
        tools.mkdir(exist_ok=True)
        shutil.copy2(tool_src, tools / "check-self-assessment.py")
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": "MutSelfAssessPlan",
        "GIT_AUTHOR_EMAIL": "mut@invalid.local",
        "GIT_COMMITTER_NAME": "MutSelfAssessPlan",
        "GIT_COMMITTER_EMAIL": "mut@invalid.local",
    })
    r = run(["git", "init", "-q", "-b", "main"], cwd=dest, env=env)
    if r.returncode != 0:
        raise RuntimeError("git init failed: " + r.stderr)
    r = run(["git", "add", "-A"], cwd=dest, env=env)
    if r.returncode != 0:
        raise RuntimeError("git add failed: " + r.stderr)
    r = run(["git", "commit", "-q", "-m", "fixture base"], cwd=dest, env=env)
    if r.returncode != 0:
        raise RuntimeError("git commit failed: " + r.stderr)
    sha = run(["git", "rev-parse", "HEAD"], cwd=dest, env=env).stdout.strip()
    # no remote is configured on purpose: a scratch repo that cannot push
    return dest, sha, env


def apply_fixture(repo: Path, fixture_dir: Path) -> list[str]:
    applied = []
    scorecard = repo / "SCORECARD.md"
    if (fixture_dir / "SCORECARD.md").exists():
        shutil.copy2(fixture_dir / "SCORECARD.md", scorecard)
        applied.append("SCORECARD.md")
    if (fixture_dir / "axes-table.md").exists():
        text = scorecard.read_text(encoding="utf-8")
        table = (fixture_dir / "axes-table.md").read_text(encoding="utf-8").rstrip("\n").split("\n")
        scorecard.write_text(replace_last_table(text, AXES_HEADING_RE, table, "Axis"), encoding="utf-8")
        applied.append("axes-table.md")
    if (fixture_dir / "capabilities-table.md").exists():
        text = scorecard.read_text(encoding="utf-8")
        table = (fixture_dir / "capabilities-table.md").read_text(encoding="utf-8").rstrip("\n").split("\n")
        scorecard.write_text(replace_last_table(text, CAPS_HEADING_RE, table, "Capability"),
                             encoding="utf-8")
        applied.append("capabilities-table.md")
    if (fixture_dir / "shonen.md").exists():
        shutil.copy2(fixture_dir / "shonen.md", repo / "SHONEN.md")
        applied.append("shonen.md")
    return applied


def apply_baseline(repo: Path, baseline_dir: Path) -> list[str]:
    """Overlay the pristine baseline (the corrected tables) onto the repo.

    The baseline is what the checker must report 0 mismatches on; each fixture
    is then that baseline plus exactly one defect.
    """
    return apply_fixture(repo, baseline_dir)


def commit(repo: Path, env) -> str:
    run(["git", "add", "-A"], cwd=repo, env=env)
    run(["git", "commit", "-q", "-m", "fixture mutation"], cwd=repo, env=env)
    return run(["git", "rev-parse", "HEAD"], cwd=repo, env=env).stdout.strip()


# --------------------------------------------------------------------------
# checker invocation and output parsing
# --------------------------------------------------------------------------
def invoke_checker(repo: Path, sha: str, timeout: int = 3600) -> dict:
    proc = run(["python3", "tools/check-self-assessment.py", "--revision", sha],
               cwd=repo, timeout=timeout)
    out = proc.stdout
    err = proc.stderr
    ids = sorted({f"K{m.group(1)}" for m in CHECK_ID_RE.finditer(out + "\n" + err)})
    parsed = None
    try:
        parsed = json.loads(out)
    except Exception:
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("{") and line.endswith("}"):
                try:
                    parsed = json.loads(line)
                    break
                except Exception:
                    pass
    mismatches = None
    if isinstance(parsed, dict):
        for key in ("mismatches", "mismatch_count", "mismatched_checks", "n_mismatches"):
            if key in parsed:
                v = parsed[key]
                if isinstance(v, int):
                    mismatches = v
                elif isinstance(v, list):
                    mismatches = len(v)
                break
    return {
        "exit": proc.returncode,
        "stdout": out[-8000:],
        "stderr": err[-4000:],
        "check_ids_in_output": ids,
        "json": parsed,
        "mismatches_field": mismatches,
    }


def id_set_from_result(res: dict) -> set[str]:
    """The set of check ids the checker reports as MISMATCHED.

    The JSON payload is authoritative: every check appears in `checks` with a
    status, so only the mismatching ones count.  Text scraping is a fallback
    for a checker that does not emit JSON.
    """
    j = res.get("json")
    ids: set[str] = set()
    if isinstance(j, dict):
        checks = j.get("checks")
        if isinstance(checks, list):
            for c in checks:
                if not isinstance(c, dict):
                    continue
                cid = c.get("id") or c.get("check")
                status = str(c.get("status", "")).lower()
                if isinstance(cid, str) and re.fullmatch(r"K\d{2}", cid):
                    if status.startswith("mis") or status == "fail":
                        ids.add(cid)
            return ids
    ids.update(res["check_ids_in_output"])
    return ids


def check_states(res: dict) -> dict:
    """{check id: (status, reason)} from the JSON payload, or {} without JSON."""
    j = res.get("json")
    states: dict[str, tuple[str, str]] = {}
    if isinstance(j, dict) and isinstance(j.get("checks"), list):
        for c in j["checks"]:
            if isinstance(c, dict):
                cid = c.get("id") or c.get("check")
                if isinstance(cid, str) and re.fullmatch(r"K\d{2}", cid):
                    states[cid] = (str(c.get("status", "")).lower(), str(c.get("reason", "")))
    return states


def all_ids_from_result(res: dict) -> set[str]:
    j = res.get("json")
    ids: set[str] = set()
    if isinstance(j, dict) and isinstance(j.get("checks"), list):
        for c in j["checks"]:
            if isinstance(c, dict):
                cid = c.get("id") or c.get("check")
                if isinstance(cid, str) and re.fullmatch(r"K\d{2}", cid):
                    ids.add(cid)
        if ids:
            return ids
    return set(res["check_ids_in_output"])


# --------------------------------------------------------------------------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default="/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
    ap.add_argument("--revision", required=True)
    ap.add_argument("--fixtures", required=True)
    ap.add_argument("--tool", default=None)
    ap.add_argument("--workdir", default="/fast/scratch/hyaku/tsukuroi-r25/MutSelfAssessPlan/repos")
    ap.add_argument("--json", default=None)
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--only", default=None, help="comma separated fixture ids")
    args = ap.parse_args(argv)

    lane = Path(args.lane).resolve()
    fixtures = Path(args.fixtures).resolve()
    work = Path(args.workdir).resolve()
    work.mkdir(parents=True, exist_ok=True)

    tool = Path(args.tool).resolve() if args.tool else None
    if tool is None:
        for cand in (lane / "tools" / "check-self-assessment.py",
                     Path("/fast/scratch/hyaku/tsukuroi-r25/ExecSelfAssessTool/repo/tools/check-self-assessment.py")):
            if cand.exists() and cand.stat().st_size > 1000:
                tool = cand
                break
    if tool is None or not tool.exists():
        print("TOOL_ABSENT: tools/check-self-assessment.py not found; fixtures are ready for wave 2.")
        print(f"tool searched: {args.tool} ; {lane / 'tools' / 'check-self-assessment.py'} ; "
              f"/fast/scratch/hyaku/tsukuroi-r25/ExecSelfAssessTool/repo/tools/check-self-assessment.py")
        return 3

    manifest = json.loads((fixtures / "manifest.json").read_text(encoding="utf-8"))
    only = set(args.only.split(",")) if args.only else None

    results = {
        "lane": str(lane),
        "revision": args.revision,
        "tool": str(tool),
        "tool_sha256": sha256_file(tool),
        "fixtures_dir": str(fixtures),
        "baseline": None,
        "runs": [],
    }

    def make_repo(tag: str):
        dest = Path(tempfile.mkdtemp(prefix=f"{tag}-", dir=str(work)))
        return build_repo(lane, args.revision, dest, tool)

    baseline_dir = fixtures / "baseline"

    # ---- pristine baseline ------------------------------------------------
    base_dir, base_sha0, base_env = make_repo("baseline")
    base_applied = apply_baseline(base_dir, baseline_dir)
    base_sha = commit(base_dir, base_env)
    base_res = invoke_checker(base_dir, base_sha)
    base_ids = id_set_from_result(base_res)
    results["baseline"] = {
        "repo": str(base_dir),
        "commit": base_sha,
        "files_applied": base_applied,
        "exit": base_res["exit"],
        "mismatches_field": base_res["mismatches_field"],
        "check_ids": sorted(base_ids),
        "stdout_tail": base_res["stdout"][-3000:],
        "stderr_tail": base_res["stderr"][-1500:],
    }
    print(f"BASELINE exit={base_res['exit']} mismatches={base_res['mismatches_field']} ids={sorted(base_ids)}")

    # ---- one repo per fixture --------------------------------------------
    for meta in manifest["fixtures"]:
        fid = meta["fixture"]
        if only and fid not in only:
            continue
        fdir = fixtures / "fixtures" / fid
        if not fdir.exists():
            continue
        repo, sha0, env = make_repo(fid)
        applied = apply_baseline(repo, baseline_dir)
        applied += apply_fixture(repo, fdir)
        sha = commit(repo, env)
        res = invoke_checker(repo, sha)
        ids = id_set_from_result(res)
        expected = set(meta.get("expected_check_ids") or [])
        newly = sorted(ids - base_ids)
        if not expected:
            verdict = "control" if not newly else "unexpected-mismatch"
        elif expected & set(newly):
            verdict = "killed"
        elif expected & ids:
            verdict = "killed-baseline-overlap"
        else:
            verdict = "survived"
        after = {}
        for rel in ("SCORECARD.md", "SHONEN.md"):
            p = repo / rel
            if p.exists():
                after[rel] = sha256_file(p)
        states = check_states(res)
        new_reasons = {cid: states[cid][1] for cid in newly if cid in states}
        results["runs"].append({
            "fixture": fid,
            "check": meta.get("check"),
            "kind": meta.get("kind"),
            "description": meta.get("description"),
            "expected_check_ids": sorted(expected),
            "new_check_ids": newly,
            "new_reasons": new_reasons,
            "all_check_ids": sorted(ids),
            "verdict": verdict,
            "exit": res["exit"],
            "mismatches_field": res["mismatches_field"],
            "repo": str(repo),
            "commit": sha,
            "files_applied": applied,
            "sha256_after": after,
            "stdout_tail": res["stdout"][-2500:],
            "stderr_tail": res["stderr"][-1200:],
        })
        print(f"{fid:44s} {verdict:24s} exit={res['exit']} mismatches={res['mismatches_field']} "
              f"new={newly} expected={sorted(expected)}")
        for cid, reason in new_reasons.items():
            print(f"    {cid}: {reason}")
        if not args.keep:
            shutil.rmtree(repo, ignore_errors=True)

    if not args.keep:
        shutil.rmtree(base_dir, ignore_errors=True)

    if args.json:
        Path(args.json).write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
        print(f"json={args.json}")

    killed = sum(1 for r in results["runs"] if r["verdict"].startswith("killed"))
    survived = sum(1 for r in results["runs"] if r["verdict"] == "survived")
    print(f"SUMMARY killed={killed} survived={survived} total={len(results['runs'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
