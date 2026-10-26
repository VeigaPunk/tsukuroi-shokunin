#!/usr/bin/env python3
"""check_heading_dates.py -- read-only heading-date consistency checker.

For every level-2 ATX heading (a line starting with exactly ``## ``) in
``SCORECARD.md`` and ``LOG.md`` at a given revision, if the heading states an
ISO-8601 UTC time, find the commit that first added that exact heading line and
flag the heading when the stated time is *later* than that commit's time.

Stated-time form accepted (superset of the round-40 item wording
``YYYY-MM-DDTHH:MMZ``)::

    YYYY-MM-DDTHH:MMZ
    YYYY-MM-DDTHH:MM:SSZ

A heading without a stated time is not checked (it cannot contradict anything).

Introducing commit
------------------
``git log --reverse --format=... -S<exact heading line> -- <file>``; the oldest
commit in which the occurrence count of that exact line changed is taken as the
commit that introduced the heading.  Using the exact current line means a heading
whose text was later edited is bound to the commit that first contained the
current text; that is the strict choice (it never credits a heading to a commit
older than the text it now carries).  Identical heading lines that occur more
than once resolve to the same first-add commit by construction.

Comparison
----------
The stated time is read at its own precision (seconds default to ``00`` for
``HH:MMZ``) and compared with the untruncated committer instant in UTC.  A heading
is flagged only when ``stated > commit``.  A stated time earlier than the commit
(including a minute-precision stamp up to 59 s before the commit instant) is out
of scope for this item and is reported as ``backdated`` but not flagged.

Read-only
---------
Only ``git show``, ``git log`` and ``git rev-parse`` are executed, with
``GIT_OPTIONAL_LOCKS=0``; nothing is written except the optional ``--json``
report path supplied by the caller.

Exit codes
----------
0  every checked heading is consistent (stated time <= introducing commit time)
1  at least one heading states a time later than its introducing commit
2  usage or tooling error (bad revision, missing file, git failure)
3  the selection was vacuous for the caller's floor: fewer timed headings were
   checked than ``--require-timed`` demands (a pass over nothing is not a pass)

Usage
-----
    check_heading_dates.py --repo /path/to/repo --rev <rev> [--match REGEX]
                           [--require-timed N] [--json out.json] [--verbose]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

FILES = ("SCORECARD.md", "LOG.md")

# A level-2 heading: exactly two '#' followed by a space.
HEADING_RE = re.compile(r"^## (?!\#)")

# ISO-8601 UTC time with minute or second precision.
TIME_RE = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2})T(?P<hour>\d{2}):(?P<minute>\d{2})"
    r"(?::(?P<second>\d{2}))?Z"
)

# Something that looks like a time but is not one (reported, never flagged).
TIME_LIKE_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}")


class CheckError(RuntimeError):
    """Tooling failure (bad revision, git error); exits 2."""


def git(repo: str, *args: str) -> str:
    env = dict(os.environ)
    env["GIT_OPTIONAL_LOCKS"] = "0"
    proc = subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    if proc.returncode != 0:
        raise CheckError(
            "git %s failed (%d): %s"
            % (" ".join(args), proc.returncode, proc.stderr.strip())
        )
    return proc.stdout


def resolve_commit(repo: str, rev: str) -> str:
    return git(repo, "rev-parse", "--verify", rev + "^{commit}").strip()


def show_file(repo: str, commit: str, path: str) -> str:
    return git(repo, "show", "%s:%s" % (commit, path))


def introducing_commit(repo: str, commit: str, path: str, line: str) -> tuple[str, str]:
    """Return (sha, iso_committer_time) of the first commit adding ``line``."""
    out = git(
        repo,
        "log",
        "--reverse",
        "--format=%H%x09%cI",
        "-S" + line,
        commit,
        "--",
        path,
    )
    for row in out.splitlines():
        if not row.strip():
            continue
        sha, _, when = row.partition("\t")
        return sha.strip(), when.strip()
    raise CheckError(
        "git log -S found no commit for heading in %s: %r" % (path, line)
    )


def stated_time(heading: str):
    """Return (datetime_utc, precision, matched_text) or None."""
    match = TIME_RE.search(heading)
    if not match:
        return None
    second = match.group("second")
    try:
        when = datetime(
            int(match.group("date")[0:4]),
            int(match.group("date")[5:7]),
            int(match.group("date")[8:10]),
            int(match.group("hour")),
            int(match.group("minute")),
            int(second) if second is not None else 0,
            tzinfo=timezone.utc,
        )
    except ValueError:
        return None
    return when, ("second" if second is not None else "minute"), match.group(0)


def check(repo: str, rev: str, pattern: re.Pattern | None):
    tip = resolve_commit(repo, rev)
    rows = []
    cache: dict[tuple[str, str], tuple[str, str]] = {}
    for path in FILES:
        try:
            text = show_file(repo, tip, path)
        except CheckError:
            raise CheckError("cannot read %s at %s" % (path, tip))
        for lineno, line in enumerate(text.splitlines(), start=1):
            if not HEADING_RE.match(line):
                continue
            if pattern is not None and not pattern.search(line):
                continue
            stated = stated_time(line)
            row = {
                "file": path,
                "line": lineno,
                "heading": line,
                "matched": True,
                "stated": stated[2] if stated else None,
                "precision": stated[1] if stated else None,
            }
            if stated is None:
                row["status"] = (
                    "malformed-time" if TIME_LIKE_RE.search(line) else "no-stated-time"
                )
                rows.append(row)
                continue
            key = (path, line)
            if key not in cache:
                cache[key] = introducing_commit(repo, tip, path, line)
            sha, when_iso = cache[key]
            commit_time = datetime.fromisoformat(when_iso).astimezone(timezone.utc)
            stated_utc, _precision, _text = stated
            row.update(
                {
                    "introducing_commit": sha,
                    "commit_time": commit_time.isoformat(),
                }
            )
            if stated_utc > commit_time:
                row["status"] = "flag"
                row["delta_seconds"] = int(
                    (stated_utc - commit_time).total_seconds()
                )
            elif stated_utc < commit_time:
                row["status"] = "backdated"
                row["delta_seconds"] = int(
                    (stated_utc - commit_time).total_seconds()
                )
            else:
                row["status"] = "ok"
                row["delta_seconds"] = 0
            rows.append(row)
    return tip, rows


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Flag level-2 headings whose stated UTC time is later than "
        "the commit that introduced the heading."
    )
    parser.add_argument("--repo", required=True, help="path to the git repository")
    parser.add_argument("--rev", required=True, help="revision whose files are read")
    parser.add_argument(
        "--match",
        default=None,
        help="only consider headings matching this regular expression",
    )
    parser.add_argument(
        "--require-timed",
        type=int,
        default=0,
        metavar="N",
        help="exit 3 when fewer than N headings with a stated time were checked "
        "(guards against a selector that matches nothing to check)",
    )
    parser.add_argument("--json", default=None, help="write the JSON report here")
    parser.add_argument("--verbose", action="store_true", help="show ok rows too")
    args = parser.parse_args(argv)

    pattern = re.compile(args.match) if args.match else None
    try:
        tip, rows = check(args.repo, args.rev, pattern)
    except CheckError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2

    timed = [r for r in rows if r["status"] not in ("no-stated-time", "malformed-time")]
    malformed = [r for r in rows if r["status"] == "malformed-time"]
    flags = [r for r in timed if r["status"] == "flag"]
    backdated = [r for r in timed if r["status"] == "backdated"]
    ok = [r for r in timed if r["status"] == "ok"]

    for row in rows:
        if row["status"] in ("no-stated-time", "malformed-time"):
            if args.verbose or row["status"] == "malformed-time":
                print(
                    "%s:%d %s\n    %s"
                    % (row["file"], row["line"], row["status"].upper(), row["heading"])
                )
            continue
        if row["status"] == "ok" and not args.verbose:
            continue
        print(
            "%s:%d %s stated=%s commit=%s (%s) delta=%+ds\n    %s"
            % (
                row["file"],
                row["line"],
                row["status"].upper(),
                row["stated"],
                row["commit_time"],
                row["introducing_commit"][:12],
                row["delta_seconds"],
                row["heading"],
            )
        )

    if flags:
        status = 1
    elif len(timed) < args.require_timed:
        status = 3
    else:
        status = 0

    summary = {
        "repo": os.path.abspath(args.repo),
        "rev": args.rev,
        "resolved": tip,
        "match": args.match,
        "require_timed": args.require_timed,
        "headings_matched": len(rows),
        "headings_with_stated_time": len(timed),
        "malformed_time": len(malformed),
        "ok": len(ok),
        "backdated": len(backdated),
        "flag": len(flags),
        "exit": status,
        "rows": rows,
    }
    print(
        "summary: matched=%d timed=%d malformed=%d ok=%d backdated=%d flag=%d exit=%d"
        % (
            summary["headings_matched"],
            summary["headings_with_stated_time"],
            summary["malformed_time"],
            summary["ok"],
            summary["backdated"],
            summary["flag"],
            summary["exit"],
        )
    )
    if args.require_timed and len(timed) < args.require_timed and not flags:
        print(
            "ERROR: vacuous selection: %d timed heading(s) checked, "
            "--require-timed %d" % (len(timed), args.require_timed),
            file=sys.stderr,
        )
    if args.json:
        with open(args.json, "w", encoding="utf-8") as handle:
            json.dump(summary, handle, indent=2, sort_keys=True)
            handle.write("\n")
    return summary["exit"]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
