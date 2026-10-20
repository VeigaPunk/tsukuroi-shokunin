#!/usr/bin/env python3
"""Read-only round-17 recheck-procedure gate.

Round 17's steer withholds package, boot-image and service action. A knowledge
entry's `recheck:` line is a procedure a later agent is invited to follow, so
a forbidden binary there re-authorizes the action the steer withheld: the L1
seat ran `pacman -Q ...` after reading
corpus/knowledge/initramfs-v42-sysroot-recovery.md:3. This gate reads the
named files at an immutable revision and, in the LAST `recheck:` line (later
lines supersede earlier pointer ones, per the journal-boot-plane convention),
reports every forbidden binary a backticked command actually invokes.

An appended `## R17-RECHECK — steer-safe procedure` section resolves the
header only when the section itself supplies at least one procedure command
(backtick span, fenced block line, or `procedure:` line) and invokes no
forbidden binary. Prose that merely names a binary (for example "never run
pacman") is not an invocation.

Exit 0 pass / 1 finding / 2 could-not-evaluate; JSON on stdout.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import namedtuple
from pathlib import Path

PASS, FAIL, CANNOT = 0, 1, 2
ROOT = Path(__file__).resolve().parents[1]
HEADING = "## R17-RECHECK — steer-safe procedure"
DEFAULT_FORBID = ("pacman", "checkupdates", "yay", "paru", "mkinitcpio", "limine-update")
REV = re.compile(r"^[0-9a-fA-F]{7,64}$")
BRANCH = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")
BINARY = re.compile(r"^[A-Za-z0-9_.+-]+$")
ASSIGN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
PROCEDURE_LINE = re.compile(
    r"^(?:[-*+]\s*)?(?:procedure|recheck|commands?|steps?)\s*[:—–-]\s*(.+)$", re.I)
# Shell control words that can stand where a command name would.
KEYWORDS = {"if", "then", "else", "elif", "fi", "do", "done", "case", "esac", "in",
            "while", "until", "for", "select", "function", "{", "}", "!", "time"}
SHELLS = {"sh", "bash", "dash", "zsh", "ksh", "busybox"}
# wrapper: (options taking a separate argument, positional arguments to skip)
WRAPPERS = {
    "sudo": ({"-u", "-g", "-C", "-h", "-p", "-r", "-t", "-U", "-D"}, 0),
    "doas": ({"-a", "-C", "-u"}, 0),
    "env": ({"-u", "-C", "-S"}, 0),
    "command": (set(), 0),
    "exec": (set(), 0),
    "nohup": (set(), 0),
    "builtin": (set(), 0),
    "time": ({"-f", "-o"}, 0),
    "nice": ({"-n"}, 0),
    "ionice": ({"-c", "-n", "-p"}, 0),
    "stdbuf": ({"-i", "-o", "-e"}, 0),
    "timeout": ({"-s", "-k"}, 1),
    "xargs": ({"-a", "-d", "-E", "-I", "-L", "-n", "-P", "-s"}, 0),
}

Finding = namedtuple("Finding", "id site detail")
Counts = namedtuple("Counts", "forbidden files invocations flagged resolved clean")
Result = namedtuple("Result", "code findings counts")


class Cannot(Exception):
    def __init__(self, fid, site, detail):
        super().__init__(detail)
        self.fid, self.site, self.detail = fid, site, detail


def segments(text):
    """Split shell text on top-level separators, honoring quoting.

    A backtick span is re-split as its own command sequence, so a prose span
    holding several commands is scanned command by command.
    """
    out, buf, quote = [], [], None
    index, size = 0, len(text)

    def flush():
        piece = "".join(buf)
        buf.clear()
        if piece.strip():
            out.append(piece)

    while index < size:
        char = text[index]
        if quote:
            buf.append(char)
            if char == "\\" and quote == '"' and index + 1 < size:
                buf.append(text[index + 1])
                index += 2
                continue
            if char == quote:
                quote = None
            index += 1
            continue
        if char in "'\"":
            quote = char
            buf.append(char)
            index += 1
            continue
        if char == "\\" and index + 1 < size:
            buf.append(char)
            buf.append(text[index + 1])
            index += 2
            continue
        if char == "`":
            flush()
            index += 1
            start = index
            while index < size and text[index] != "`":
                index += 1
            span = text[start:index]
            if span.strip():
                out.extend(segments(span))
            index += 1
            continue
        if char in ";|&\n()":
            flush()
            index += 1
            continue
        buf.append(char)
        index += 1
    flush()
    return out


def words(segment):
    """Quote-aware tokenization; quotes are removed from the token values."""
    out, buf, quote, started = [], [], None, False
    index, size = 0, len(segment)
    while index < size:
        char = segment[index]
        if quote:
            if char == quote:
                quote = None
            elif char == "\\" and quote == '"' and index + 1 < size:
                buf.append(segment[index + 1])
                index += 1
            else:
                buf.append(char)
            index += 1
            continue
        if char in "'\"":
            quote = char
            started = True
            index += 1
            continue
        if char.isspace():
            if buf or started:
                out.append("".join(buf))
                buf, started = [], False
            index += 1
            continue
        if char == "\\" and index + 1 < size:
            buf.append(segment[index + 1])
            started = True
            index += 2
            continue
        buf.append(char)
        started = True
        index += 1
    if buf or started:
        out.append("".join(buf))
    return out


def command_word(tokens):
    """Skip assignments, control words and wrappers; return (word, index)."""
    index, size = 0, len(tokens)
    while index < size:
        token = tokens[index]
        if token in KEYWORDS or ASSIGN.match(token):
            index += 1
            continue
        base = token.rsplit("/", 1)[-1]
        wrapper = WRAPPERS.get(base)
        if wrapper is None:
            return token, index
        options, positional = wrapper
        index += 1
        while index < size and tokens[index].startswith("-") and tokens[index] != "-":
            if tokens[index] in options and index + 1 < size:
                index += 2
            else:
                index += 1
        if index < size and tokens[index] == "--":
            index += 1
        if base == "env":
            while index < size and ASSIGN.match(tokens[index]):
                index += 1
        index += positional
    return None, size


def simple_commands(text):
    for segment in segments(text):
        tokens = words(segment)
        name, index = command_word(tokens)
        if name:
            yield name.rsplit("/", 1)[-1], tokens[index + 1:]


def invocations(text, forbid, depth=0):
    """Binary names invoked by shell text (recurses into sh -c / eval)."""
    hits = []
    if depth > 4:
        return hits
    for base, args in simple_commands(text):
        if base in forbid:
            hits.append(base)
            continue
        if base in SHELLS:
            if base == "busybox" and args:
                applet = args[0].rsplit("/", 1)[-1]
                if applet in forbid:
                    hits.append(applet)
                    continue
                if applet in SHELLS:
                    args = args[1:]
            if "-c" in args:
                offset = args.index("-c")
                if offset + 1 < len(args):
                    hits.extend(invocations(args[offset + 1], forbid, depth + 1))
        elif base == "eval" and args:
            hits.extend(invocations(" ".join(args), forbid, depth + 1))
    return hits


def recheck_line(text):
    """(zero-based index, line) of the LAST `recheck:` line, or (None, None).

    A later `recheck:` line supersedes an earlier pointer line; the corpus
    convention is "supersedes the ... recheck: line above"
    (journal-boot-plane.md).
    """
    hits = [index for index, line in enumerate(text.splitlines())
            if line.startswith("recheck:")]
    return (hits[-1], text.splitlines()[hits[-1]]) if hits else (None, None)


def backtick_spans(text):
    """Backticked command spans in one line; bare prose is never a command."""
    return [span for span in re.findall(r"`([^`]+)`", text) if span.strip()]


def section_commands(lines, first):
    """(line number, command text) pairs declared by the steer-safe section."""
    out, fenced = [], False
    for offset, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fenced = not fenced
            continue
        number = first + offset
        if fenced:
            if stripped:
                out.append((number, line))
            continue
        spans = [span for span in re.findall(r"`([^`]+)`", line) if span.strip()]
        if spans:
            out.extend((number, span) for span in spans)
            continue
        declared = PROCEDURE_LINE.match(stripped)
        if declared and declared.group(1).strip():
            out.append((number, declared.group(1)))
    return out


def section(lines):
    """State of the appended steer-safe section for one file."""
    hits = [index for index, line in enumerate(lines) if line.strip() == HEADING]
    if not hits:
        return {"present": False, "duplicates": 0}
    if len(hits) > 1:
        return {"present": True, "duplicates": len(hits), "line": hits[0], "commands": []}
    first = hits[0] + 1
    end = len(lines)
    for index in range(first, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return {"present": True, "duplicates": 1, "line": hits[0],
            "commands": section_commands(lines[first:end], first + 1)}


def assess_file(path, text, forbid):
    """Findings and per-file counts for one knowledge entry."""
    lines = text.splitlines()
    index, opener = recheck_line(text)
    if opener is None:
        raise Cannot("E-RECHECK-MISSING", path, "no recheck: line")
    body = opener[len("recheck:"):].strip()
    if not body:
        raise Cannot("E-RECHECK-EMPTY", path, "recheck: line carries no procedure")
    findings = []
    header_hits = []
    for span in backtick_spans(body):
        header_hits.extend(invocations(span, forbid))
    invocations_seen = len(header_hits)
    state = section(lines)
    resolved = False
    if state["present"]:
        if state["duplicates"] > 1:
            findings.append(Finding("RECHECK-STEER-SAFE-INVALID", path,
                                    "steer-safe heading appears more than once"))
        elif not state["commands"]:
            findings.append(Finding("RECHECK-STEER-SAFE-INVALID", path,
                                    "steer-safe section declares no procedure command"))
        else:
            unsafe = []
            for number, command in state["commands"]:
                hits = invocations(command, forbid)
                invocations_seen += len(hits)
                if hits:
                    unsafe.append((number, hits[0], command))
            if unsafe:
                number, name, command = unsafe[0]
                findings.append(Finding(
                    "RECHECK-FORBIDDEN-INVOCATION", f"{path}:{number}",
                    f"steer-safe section invokes {name}: {' '.join(command.split())[:80]}"))
                findings.append(Finding("RECHECK-STEER-SAFE-INVALID", path,
                                        "steer-safe section still invokes a forbidden binary"))
            else:
                resolved = True
    if header_hits and not resolved:
        findings.append(Finding(
            "RECHECK-FORBIDDEN-INVOCATION", f"{path}:{index + 1}",
            "recheck procedure invokes " + ", ".join(sorted(set(header_hits)))))
    flagged = int(any(item.id == "RECHECK-FORBIDDEN-INVOCATION" for item in findings))
    clean = int(not findings and not header_hits)
    return findings, {"invocations": invocations_seen, "flagged": flagged,
                      "resolved": int(bool(header_hits) and resolved),
                      "clean": clean}


def evaluate(files, forbid):
    findings, invocations_seen, flagged, resolved, clean = [], 0, 0, 0, 0
    for path, text in files:
        file_findings, counts = assess_file(path, text, forbid)
        findings.extend(file_findings)
        invocations_seen += counts["invocations"]
        flagged += counts["flagged"]
        resolved += counts["resolved"]
        clean += counts["clean"]
    findings = [Finding(*key) for key in
                sorted({(item.id, item.site, item.detail) for item in findings})]
    counts = Counts(list(forbid), len(files), invocations_seen, flagged, resolved, clean)
    return Result(FAIL if findings else PASS, findings, counts)


def emit(status, revision, branch, branch_tip, findings, counts, out=None,
         origin_tip=None, message=None):
    payload = {
        "status": status,
        "revision": revision,
        "branch": branch,
        "branch_tip": branch_tip,
        "origin_tip": origin_tip,
        "forbidden": list(counts.forbidden) if counts else [],
        "file_count": counts.files if counts else 0,
        "invocation_count": counts.invocations if counts else 0,
        "flagged_count": counts.flagged if counts else 0,
        "resolved_count": counts.resolved if counts else 0,
        "clean_count": counts.clean if counts else 0,
        "scope": "recheck: header procedures only; read-only, no host action taken",
        "findings": [{"id": item.id, "site": item.site, "detail": item.detail}
                     for item in findings],
    }
    if message:
        payload["message"] = message
    print(json.dumps(payload, sort_keys=True), file=out or sys.stdout)
    return {"PASS": PASS, "FAIL": FAIL, "CANNOT_EVALUATE": CANNOT}[status]


def git(repo, *args):
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat", "LC_ALL": "C",
                "GIT_TERMINAL_PROMPT": "0"})
    try:
        return subprocess.run(["git", "--no-pager", "-C", str(repo), *args],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=env, timeout=60)
    except subprocess.TimeoutExpired:
        raise Cannot("E-GIT-FAILED", "git", "git command exceeded 60s")
    except OSError as exc:
        raise Cannot("E-GIT-FAILED", "git", str(exc)[:120])


def ref_sha(repo, ref):
    proc = git(repo, "rev-parse", "--verify", "--quiet", ref)
    return proc.stdout.decode("ascii", "replace").strip() if proc.returncode == 0 else None


def is_ancestor(repo, sha, ref):
    proc = git(repo, "merge-base", "--is-ancestor", sha, ref)
    if proc.returncode == 0:
        return True
    if proc.returncode == 1:
        return False
    detail = proc.stderr.decode("utf-8", "replace").strip()[:120] or "merge-base failed"
    raise Cannot("E-GIT-FAILED", ref, detail)


def bind(repo, revision, branch):
    """Resolve a hex revision and prove it is landed (and pushed) on `branch`."""
    if not REV.fullmatch(revision or ""):
        raise Cannot("E-REVISION-INVALID", "revision",
                     "7-64 hex commit required; HEAD, @ and refs are rejected")
    if not BRANCH.fullmatch(branch or ""):
        raise Cannot("E-CLI", "branch", "simple branch name required")
    proc = git(repo, "rev-parse", "--verify", "--quiet", f"{revision}^{{commit}}")
    if proc.returncode != 0:
        raise Cannot("E-REVISION-INVALID", "revision", f"commit {revision} not found")
    sha = proc.stdout.decode("ascii", "replace").strip()
    local = f"refs/heads/{branch}"
    tip = ref_sha(repo, local)
    if tip is None:
        raise Cannot("E-REVISION-NOT-LANDED", revision, f"{local} absent")
    if not is_ancestor(repo, sha, local):
        raise Cannot("E-REVISION-NOT-LANDED", revision,
                     f"{sha[:12]} is not an ancestor of {local}")
    remote_ref = f"refs/remotes/origin/{branch}"
    origin_tip = ref_sha(repo, remote_ref)
    if origin_tip is not None and not is_ancestor(repo, sha, remote_ref):
        raise Cannot("E-REVISION-NOT-PUSHED", revision,
                     f"{sha[:12]} is not an ancestor of {remote_ref}")
    return sha, tip, origin_tip


def read_git(repo, commit, path):
    spec = f"{commit}:{path}"
    kind = git(repo, "cat-file", "-t", spec)
    if kind.returncode != 0:
        return None
    if kind.stdout.decode("ascii", "replace").strip() != "blob":
        raise Cannot("E-PATH-INVALID", path, "not a regular file at revision")
    proc = git(repo, "show", spec)
    if proc.returncode == 0:
        return proc.stdout
    error = proc.stderr.decode("utf-8", "replace")
    raise Cannot("E-GIT-FAILED", path, error.strip()[:120] or "git show failed")


def decode(raw, path):
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Cannot("E-PATH-INVALID", path, f"not UTF-8: {exc}"[:120])


def clean_path(raw):
    path = raw.strip().rstrip("/") or "."
    if path.startswith("./"):
        path = path[2:] or "."
    if path != "." and (path.startswith("/") or ".." in Path(path).parts):
        raise Cannot("E-PATH-INVALID", raw, "repo-relative path required")
    return path


def expand_paths(repo, sha, inputs):
    """Files to audit: blobs directly, directories as their *.md members."""
    files = []
    for raw in inputs:
        path = clean_path(raw)
        spec = f"{sha}:{path}" if path != "." else sha
        if path == ".":
            type_name = "tree"
        else:
            kind = git(repo, "cat-file", "-t", spec)
            if kind.returncode != 0:
                raise Cannot("E-PATH-MISSING", path, "path absent at revision")
            type_name = kind.stdout.decode("ascii", "replace").strip()
        if type_name == "blob":
            files.append(path)
            continue
        if type_name != "tree":
            raise Cannot("E-PATH-INVALID", path, "not a regular file at revision")
        listing = git(repo, "ls-tree", "-r", "--name-only", spec)
        names = listing.stdout.decode("utf-8", "replace").splitlines()
        children = sorted(name if path == "." else f"{path}/{name}"
                          for name in names if name.endswith(".md"))
        if not children:
            raise Cannot("E-PATH-EMPTY", path, "no *.md file under directory")
        files.extend(children)
    return files


def forbid_list(raw):
    names = [name for name in re.split(r"[,\s]+", raw or "") if name]
    if not names or any(not BINARY.fullmatch(name) for name in names):
        raise Cannot("E-CLI", "forbid", "comma-separated binary names required")
    return tuple(dict.fromkeys(names))


def build_parser():
    parser = argparse.ArgumentParser(
        description="Read-only round-17 recheck-procedure gate.",
        exit_on_error=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--revision", metavar="REV",
                       help="required: 7-64 hex commit; HEAD/@/refs are rejected")
    group.add_argument("--selftest", action="store_true", help="hermetic fixture suite")
    parser.add_argument("--paths", nargs="+", metavar="PATH",
                        default=["corpus/knowledge"],
                        help="knowledge files or directories; directories expand to "
                             "their *.md members (default: corpus/knowledge)")
    parser.add_argument("--branch", default="master", metavar="BRANCH",
                        help="branch the revision must be landed on (default: master)")
    parser.add_argument("--forbid", default=",".join(DEFAULT_FORBID), metavar="LIST",
                        help="comma-separated forbidden binaries")
    return parser


def run(argv, repo=ROOT, out=None):
    """Parse argv, evaluate, print JSON, and return the exit code."""
    try:
        args = build_parser().parse_args(argv)
    except (argparse.ArgumentError, SystemExit) as exc:
        if isinstance(exc, SystemExit) and not exc.code:
            return 0
        return emit("CANNOT_EVALUATE", "worktree", "master", None,
                    [Finding("E-CLI", "cli",
                             "--revision REV --paths PATH ... or --selftest required")],
                    None, out)
    if args.selftest:
        return selftest(out)
    branch = args.branch
    sha = tip = origin_tip = None
    try:
        forbid = forbid_list(args.forbid)
        sha, tip, origin_tip = bind(repo, args.revision, branch)
        paths = list(dict.fromkeys(expand_paths(repo, sha, args.paths)))
        files = []
        for path in paths:
            raw = read_git(repo, sha, path)
            if raw is None:
                raise Cannot("E-PATH-MISSING", path, "file absent at revision")
            files.append((path, decode(raw, path)))
    except Cannot as exc:
        return emit("CANNOT_EVALUATE",
                    sha or getattr(args, "revision", None) or "worktree",
                    branch, tip, [Finding(exc.fid, exc.site, exc.detail)], None, out,
                    origin_tip=origin_tip)
    except Exception as exc:  # no traceback: unreadable input is CANNOT
        return emit("CANNOT_EVALUATE",
                    sha or getattr(args, "revision", None) or "worktree",
                    branch, tip, [Finding("E-INTERNAL", "gate", str(exc)[:120])], None, out,
                    origin_tip=origin_tip)
    try:
        result = evaluate(files, forbid)
    except Cannot as exc:
        return emit("CANNOT_EVALUATE", sha, branch, tip,
                    [Finding(exc.fid, exc.site, exc.detail)], None, out,
                    origin_tip=origin_tip)
    except Exception as exc:
        return emit("CANNOT_EVALUATE", sha, branch, tip,
                    [Finding("E-INTERNAL", "gate", str(exc)[:120])], None, out,
                    origin_tip=origin_tip)
    status = {PASS: "PASS", FAIL: "FAIL"}[result.code]
    return emit(status, sha, branch, tip, result.findings, result.counts, out,
                origin_tip=origin_tip)


# --- selftest -----------------------------------------------------------------

BASELINE_HEADER = (
    "recheck: on-release; procedure: `grep -Hn '^HOOKS' /etc/mkinitcpio.conf "
    "/etc/mkinitcpio.conf.d/*.conf; grep -n '/new_root' /usr/lib/initcpio/hooks/*; "
    "curl -fsSL 'https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/"
    "v42/init' | grep -o '/new_root' | wc -l; pacman -Q mkinitcpio "
    "limine-mkinitcpio-hook plymouth`.")


def entry(recheck, tail=""):
    return ("source: S014 https://wiki.archlinux.org/title/Mkinitcpio\n"
            "verified-at: 2026-10-19\n"
            f"{recheck}\n\n"
            "# Recheck fixture\n\nBoilerplate body.\n" + tail)


SAFE_SECTION = (
    "\n## R17-RECHECK — steer-safe procedure\n\n"
    "Appended in round 17. Run these instead of the header procedure:\n\n"
    "1. `grep -Hn '^HOOKS' /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d/*.conf`\n"
    "2. `grep -n '/new_root' /usr/lib/initcpio/hooks/*`\n"
    "3. `curl -fsSL 'https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/"
    "-/raw/v42/init' | grep -o '/new_root' | wc -l`\n"
    "4. `grep -n '^%VER%' -A1 /var/lib/pacman/local/*/desc`\n")

UNSAFE_SECTION = (
    "\n## R17-RECHECK — steer-safe procedure\n\n"
    "1. `pacman -Q mkinitcpio limine-mkinitcpio-hook plymouth`\n")

# The exact section appended to corpus/knowledge/initramfs-v42-sysroot-recovery.md
# in round 17; kept here so the gate is tested against the real resolution text.
R17_SECTION = (
    "\n## R17-RECHECK — steer-safe procedure\n\n"
    "Replaces the pacman query in the `recheck:` header at line 3 for this file. "
    "Read-only; no package-manager binary is invoked:\n\n"
    "- `ls -d /var/lib/pacman/local/mkinitcpio-[0-9]* "
    "/var/lib/pacman/local/plymouth-[0-9]* "
    "/var/lib/pacman/local/limine-mkinitcpio-hook-[0-9]* "
    "/var/lib/pacman/local/limine-snapper-sync-[0-9]* "
    "/var/lib/pacman/local/snapper-[0-9]*`\n"
    "- The version is the part of each directory name after `<pkg>-`; the last "
    "two dash-separated fields are pkgver and pkgrel (for example "
    "`limine-mkinitcpio-hook-1.40.0-2` gives `1.40.0-2`).\n"
    "- Record the substitution (a directory-name read in place of a package "
    "query) in the report.\n")


def sandbox_git(repo, *args):
    proc = git(repo, *args)
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: "
                           + proc.stderr.decode("utf-8", "replace").strip()[:160])
    return proc.stdout.decode("utf-8", "replace")


def sandbox_commit(repo, text):
    (repo / "fixture.md").write_text(text, encoding="utf-8")
    sandbox_git(repo, "add", "fixture.md")
    sandbox_git(repo, "commit", "-q", "-m", "fixture")
    return sandbox_git(repo, "rev-parse", "HEAD").strip()


def sandbox_commit_tree(repo, tree):
    for name, text in tree.items():
        target = repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    sandbox_git(repo, "add", *sorted(tree))
    sandbox_git(repo, "commit", "-q", "-m", "tree")
    return sandbox_git(repo, "rev-parse", "HEAD").strip()



def selftest(out=None):
    out = out or sys.stdout
    failures, total = [], 0

    def case(repo, name, argv, want_code, want_ids, want_counts=None):
        nonlocal total
        total += 1
        buffer = _Stdout()
        try:
            code = run(argv, repo=repo, out=buffer)
            payload = json.loads(buffer.value)
        except Exception as exc:  # a crashed case is a failed case, not a crash
            failures.append(f"{name}: raised {exc!r}")
            return
        problems = []
        if code != want_code:
            problems.append(f"exit={code}/{want_code}")
        got_ids = {item["id"] for item in payload.get("findings", [])}
        if got_ids != set(want_ids):
            problems.append("ids=" + ",".join(sorted(got_ids))
                            + " want=" + ",".join(sorted(want_ids)))
        if payload.get("status") != {PASS: "PASS", FAIL: "FAIL",
                                     CANNOT: "CANNOT_EVALUATE"}[want_code]:
            problems.append(f"status={payload.get('status')}")
        for key, value in (want_counts or {}).items():
            if payload.get(key) != value:
                problems.append(f"{key}={payload.get(key)}/{value}")
        if problems:
            failures.append(f"{name}: " + "; ".join(problems))

    try:
        repo = Path(tempfile.mkdtemp(prefix="recheck-gate-"))
        sandbox_git(repo, "-c", "init.defaultBranch=master", "init", "-q")
        sandbox_git(repo, "config", "user.email", "fixture@example.invalid")
        sandbox_git(repo, "config", "user.name", "Fixture")
        sandbox_git(repo, "config", "commit.gpgsign", "false")
        first = sandbox_commit(repo, entry("recheck: on-release; procedure: "
                                           "`grep -n '^HOOKS' /etc/mkinitcpio.conf`."))
    except Exception as exc:
        print(json.dumps({"selftest": {"status": "FAIL", "cases": 0, "passed": 0,
                                       "failures": [f"sandbox: {exc!r}"]}},
                         sort_keys=True), file=out)
        return FAIL

    forbidden_only = {"RECHECK-FORBIDDEN-INVOCATION"}
    # 1. Clean header: no forbidden binary, no section.
    clean = sandbox_commit(repo, entry("recheck: on-release; procedure: "
                                       "`grep -Hn '^HOOKS' /etc/mkinitcpio.conf`."))
    case(repo, "clean-header", ["--revision", clean, "--paths", "fixture.md"],
         PASS, set(), {"flagged_count": 0, "resolved_count": 0, "clean_count": 1})
    # 2. The mined baseline line, verbatim, must be red.
    baseline = sandbox_commit(repo, entry(BASELINE_HEADER))
    case(repo, "baseline-mined-line", ["--revision", baseline, "--paths", "fixture.md"],
         FAIL, forbidden_only,
         {"flagged_count": 1, "resolved_count": 0, "clean_count": 0,
          "invocation_count": 1})
    # 3. A package-log path and a grep argument are not invocations.
    decoy = sandbox_commit(repo, entry(
        "recheck: on-release; procedure: `grep -n 'pacman -Q' /var/log/pacman.log; "
        "grep -n mkinitcpio /etc/mkinitcpio.conf`."))
    case(repo, "package-path-decoy", ["--revision", decoy, "--paths", "fixture.md"],
         PASS, set(), {"invocation_count": 0, "clean_count": 1})
    # 3b. Bare prose is not an invocation; forbidden names as arguments are not
    #     argv0 either.
    bare = sandbox_commit(repo, entry(
        "recheck: daily; procedure: pacman -Qm per row; inspect the package log."))
    case(repo, "bare-prose-safe", ["--revision", bare, "--paths", "fixture.md"],
         PASS, set(), {"invocation_count": 0, "clean_count": 1})
    argv = sandbox_commit(repo, entry(
        "recheck: daily; procedure: `readelf -h pacman; stat /usr/bin/mkinitcpio`."))
    case(repo, "argv0-only", ["--revision", argv, "--paths", "fixture.md"],
         PASS, set(), {"invocation_count": 0, "clean_count": 1})
    # 3c. The LAST recheck: line supersedes earlier pointer lines both ways.
    superseded = sandbox_commit(repo,
        "source: S014\nverified-at: 2026-10-19\n"
        "recheck: daily; procedure: `pacman -Q mkinitcpio`.\n\n"
        "# f\n\n## Later\n\n"
        "recheck: daily; procedure: `grep -n x /etc/x`.\n"
        "supersedes the pointer-only recheck: line above.\n")
    case(repo, "superseded-by-last", ["--revision", superseded, "--paths", "fixture.md"],
         PASS, set(), {"invocation_count": 0, "clean_count": 1})
    last_bad = sandbox_commit(repo,
        "source: S014\nverified-at: 2026-10-19\n"
        "recheck: daily; procedure: `grep -n x /etc/x`.\n\n"
        "# f\n\n## Later\n\n"
        "recheck: daily; procedure: `yay -S thing`.\n")
    case(repo, "last-line-wins", ["--revision", last_bad, "--paths", "fixture.md"],
         FAIL, forbidden_only, {"invocation_count": 1})
    # 4. sudo is a wrapper, not an exemption.
    sudo = sandbox_commit(repo, entry("recheck: daily; procedure: "
                                      "`sudo pacman -Q mkinitcpio`."))
    case(repo, "sudo-prefix", ["--revision", sudo, "--paths", "fixture.md"],
         FAIL, forbidden_only, {"invocation_count": 1})
    # 5. sh -c recursion.
    nested = sandbox_commit(repo, entry("recheck: daily; procedure: "
                                        "`sh -c 'mkinitcpio -P && echo done'`."))
    case(repo, "shell-c-recursion", ["--revision", nested, "--paths", "fixture.md"],
         FAIL, forbidden_only, {"invocation_count": 1})
    # 6. xargs reaches the same binary.
    piped = sandbox_commit(repo, entry("recheck: daily; procedure: "
                                       "`printf '%s\\n' mkinitcpio | xargs mkinitcpio -P`."))
    case(repo, "xargs-target", ["--revision", piped, "--paths", "fixture.md"],
         FAIL, forbidden_only)
    # 7. Default forbid catches checkupdates / yay / paru / limine-update.
    others = sandbox_commit(repo, entry(
        "recheck: daily; procedure: `checkupdates; yay -Qu; paru -Qu; limine-update`."))
    case(repo, "default-forbid-set", ["--revision", others, "--paths", "fixture.md"],
         FAIL, forbidden_only, {"invocation_count": 4})
    # 8. --forbid replaces the default set.
    curl_only = sandbox_commit(repo, entry("recheck: daily; procedure: "
                                           "`curl -fsSL 'https://example.invalid/x'`."))
    case(repo, "custom-forbid-hit",
         ["--revision", curl_only, "--paths", "fixture.md", "--forbid", "curl"],
         FAIL, forbidden_only, {"invocation_count": 1})
    case(repo, "custom-forbid-clean",
         ["--revision", curl_only, "--paths", "fixture.md", "--forbid", "pacman"],
         PASS, set(), {"invocation_count": 0})
    # 9. Valid steer-safe section resolves the header.
    resolved = sandbox_commit(repo, entry(BASELINE_HEADER, SAFE_SECTION))
    case(repo, "resolved-by-safe-section",
         ["--revision", resolved, "--paths", "fixture.md"],
         PASS, set(), {"flagged_count": 0, "resolved_count": 1,
                       "invocation_count": 1})
    # 10. A section that still invokes a forbidden binary does not resolve.
    unsafe = sandbox_commit(repo, entry(BASELINE_HEADER, UNSAFE_SECTION))
    case(repo, "section-invokes-forbidden",
         ["--revision", unsafe, "--paths", "fixture.md"],
         FAIL, forbidden_only | {"RECHECK-STEER-SAFE-INVALID"},
         {"flagged_count": 1, "resolved_count": 0})
    # 11. A heading with no procedure command does not resolve.
    empty = sandbox_commit(repo, entry(
        BASELINE_HEADER, "\n## R17-RECHECK — steer-safe procedure\n\nNothing here.\n"))
    case(repo, "section-without-command",
         ["--revision", empty, "--paths", "fixture.md"],
         FAIL, forbidden_only | {"RECHECK-STEER-SAFE-INVALID"},
         {"flagged_count": 1, "resolved_count": 0})
    # 11b. A clean header does not excuse an unsafe appended section.
    excuse = sandbox_commit(repo, entry(
        "recheck: on-release; procedure: `grep -Hn '^HOOKS' /etc/mkinitcpio.conf`.",
        UNSAFE_SECTION))
    case(repo, "clean-header-unsafe-section",
         ["--revision", excuse, "--paths", "fixture.md"],
         FAIL, forbidden_only | {"RECHECK-STEER-SAFE-INVALID"},
         {"flagged_count": 1, "resolved_count": 0, "clean_count": 0})
    # 11c. Prose that names a forbidden binary is not an invocation; a fenced
    #      block is a procedure.
    prose = sandbox_commit(repo, entry(
        BASELINE_HEADER,
        "\n## R17-RECHECK — steer-safe procedure\n\n"
        "Never run pacman here; read the database instead.\n\n"
        "```\n"
        "grep -n '^%VER%' -A1 /var/lib/pacman/local/*/desc\n"
        "```\n"))
    case(repo, "section-prose-and-fence",
         ["--revision", prose, "--paths", "fixture.md"],
         PASS, set(), {"flagged_count": 0, "resolved_count": 1})
    # 11d. The section actually appended in round 17 resolves the mined header.
    landed = sandbox_commit(repo, entry(BASELINE_HEADER, R17_SECTION))
    case(repo, "landed-r17-section",
         ["--revision", landed, "--paths", "fixture.md"],
         PASS, set(), {"flagged_count": 0, "resolved_count": 1,
                       "invocation_count": 1})
    # 12. Duplicate headings are ambiguous, not resolved.
    twin = sandbox_commit(repo, entry(BASELINE_HEADER, SAFE_SECTION + "\n"
                                      "## R17-RECHECK — steer-safe procedure\n\n"
                                      "1. `grep -n '/new_root' /usr/lib/initcpio/hooks/*`\n"))
    case(repo, "duplicate-heading", ["--revision", twin, "--paths", "fixture.md"],
         FAIL, forbidden_only | {"RECHECK-STEER-SAFE-INVALID"})
    # 13. Missing and empty recheck openers are could-not-evaluate.
    missing = sandbox_commit(repo, "source: S014\nverified-at: 2026-10-19\n\n# x\n")
    case(repo, "missing-opener", ["--revision", missing, "--paths", "fixture.md"],
         CANNOT, {"E-RECHECK-MISSING"})
    blank = sandbox_commit(repo, "source: S014\nverified-at: 2026-10-19\nrecheck:\n\n# x\n")
    case(repo, "empty-opener", ["--revision", blank, "--paths", "fixture.md"],
         CANNOT, {"E-RECHECK-EMPTY"})
    # 14. Revision binding: non-hex revisions are rejected.
    for name, revision in (("revision-head", "HEAD"),
                           ("revision-at", "@"),
                           ("revision-ref", "refs/heads/master"),
                           ("revision-short", "6923fe")):
        case(repo, name, ["--revision", revision, "--paths", "fixture.md"],
             CANNOT, {"E-REVISION-INVALID"})
    case(repo, "revision-unknown", ["--revision", "deadbeef", "--paths", "fixture.md"],
         CANNOT, {"E-REVISION-INVALID"})
    # 15. Landed + pushed binding reports revision, branch and branch_tip.
    buffer = _Stdout()
    code = run(["--revision", clean, "--paths", "fixture.md"], repo=repo, out=buffer)
    payload = json.loads(buffer.value)
    total += 1
    problems = []
    tip_now = sandbox_git(repo, "rev-parse", "master").strip()
    if code != PASS or payload.get("branch") != "master":
        problems.append(f"exit={code} branch={payload.get('branch')}")
    if payload.get("revision") != clean or payload.get("branch_tip") != tip_now:
        problems.append("revision/branch_tip do not name the bound commit and tip")
    if payload.get("origin_tip") is not None:
        problems.append(f"origin_tip={payload.get('origin_tip')} while origin is absent")
    if problems:
        failures.append("landed-binding: " + "; ".join(problems))
    # 16. A commit on a side branch is not landed.
    sandbox_git(repo, "checkout", "-q", "-b", "side")
    side = sandbox_commit(repo, entry("recheck: daily; procedure: `grep -n x /etc/x`."))
    sandbox_git(repo, "checkout", "-q", "master")
    case(repo, "revision-not-landed", ["--revision", side, "--paths", "fixture.md"],
         CANNOT, {"E-REVISION-NOT-LANDED"})
    # 17. Published commit binds; a landed commit newer than origin does not.
    sandbox_git(repo, "update-ref", "refs/remotes/origin/master", clean)
    pushed = _Stdout()
    code = run(["--revision", clean, "--paths", "fixture.md"], repo=repo, out=pushed)
    total += 1
    if code != PASS or json.loads(pushed.value).get("origin_tip") != clean:
        failures.append("revision-pushed: published tip not reported")
    sandbox_git(repo, "update-ref", "refs/remotes/origin/master", first)
    case(repo, "revision-not-pushed", ["--revision", clean, "--paths", "fixture.md"],
         CANNOT, {"E-REVISION-NOT-PUSHED"})
    sandbox_git(repo, "update-ref", "-d", "refs/remotes/origin/master")
    # 18. Absent paths, empty directories and directories-as-blob-args.
    case(repo, "path-missing",
         ["--revision", clean, "--paths", "corpus/knowledge/absent.md"],
         CANNOT, {"E-PATH-MISSING"})
    scanall = sandbox_commit_tree(repo, {
        "fixture.md": entry("recheck: daily; procedure: `grep -n x /etc/x`."),
        "notes/a.md": entry("recheck: daily; procedure: `grep -n x /etc/x`."),
        "notes/b.md": entry("recheck: daily; procedure: `grep -n y /etc/y`."),
        "notes/empty/.gitkeep": "",
        "corpus/knowledge/one.md": entry("recheck: daily; procedure: `grep -n z /etc/z`."),
        "corpus/knowledge/two.md": entry("recheck: daily; procedure: `grep -n z /etc/z`."),
    })
    case(repo, "dir-expands", ["--revision", scanall, "--paths", "notes"],
         PASS, set(), {"file_count": 2, "clean_count": 2})
    case(repo, "dir-dot-expands", ["--revision", scanall, "--paths", "."],
         PASS, set(), {"file_count": 5})
    case(repo, "default-corpus-scan", ["--revision", scanall],
         PASS, set(), {"file_count": 2})
    case(repo, "dir-empty", ["--revision", scanall, "--paths", "notes/empty"],
         CANNOT, {"E-PATH-EMPTY"})
    duplicate = _Stdout()
    code = run(["--revision", clean, "--paths", "fixture.md", "fixture.md"],
               repo=repo, out=duplicate)
    total += 1
    if code != PASS or json.loads(duplicate.value).get("file_count") != 1:
        failures.append("duplicate-path: file_count != 1")
    # 19. CLI shape.
    case(repo, "cli-no-mode", [], CANNOT, {"E-CLI"})
    case(repo, "cli-both-modes", ["--selftest", "--revision", clean], CANNOT, {"E-CLI"})
    case(repo, "cli-bogus-flag", ["--revision", clean, "--bogus"], CANNOT, {"E-CLI"})

    shutil.rmtree(repo, ignore_errors=True)
    passed = total - len(failures)
    print(json.dumps({"selftest": {"status": "PASS" if not failures else "FAIL",
                                   "cases": total, "passed": passed,
                                   "failures": failures}}, sort_keys=True), file=out)
    return PASS if not failures else FAIL


class _Stdout:
    """Minimal capture for JSON payloads emitted by run()."""

    def __init__(self):
        self.chunks = []

    def write(self, text):
        self.chunks.append(text)

    def flush(self):
        pass

    @property
    def value(self):
        return "".join(self.chunks)


def main(argv=None):
    return run(sys.argv[1:] if argv is None else argv)


if __name__ == "__main__":
    sys.exit(main())
