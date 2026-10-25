#!/usr/bin/env python3
"""Build7C239 — round 37 wave 1 design item 7/12: C2 action-override classification gate.

Read-only conformance gate for the round-36 C2 note correction "action-override
classification" (routed in SCORECARD.md:1909-1916 and W2CritC2Depth c2-depth-ruling.md
section 5).  It asserts that `corpus/knowledge/journalctl-v262-field-filter-r36.md`
carries an action-override classification row in its decision table, that the row
separates "last action selected" (action overwritten by a later action flag) from
genuine accepted field-enumeration, that argument order is preserved, and that the
scope-rejection line stays verbatim.

Exit status: 0 = PASS (correction present), 1 = FAIL (correction absent/partial),
2 = CANNOT_EVALUATE (unreadable input, invalid/landed revision, git failure).

Modes:
  --note PATH        inspect a worktree copy of the note (read-only)
  --revision REV     inspect the note blob at a landed revision (immutable git reads,
                     --lane ROOT default = the lane root, --branch master)
  --selftest         hermetic suite: embedded before/after fixtures plus a mktemp
                     git sandbox that exercises the committed-read path (top-level
                     verified equal to the fixture root before every commit)

No repository writes; no network; stdlib only.  Written to be run from anywhere.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

PASS, FAIL, CANNOT = 0, 1, 2
LANE_ROOT = Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
NOTE_RELPATH = "corpus/knowledge/journalctl-v262-field-filter-r36.md"

REJECT_LINE = "-F/--field= and -N/--fields cannot be combined with options that limit the journal."

# Action flags that *set* arg_action in src/journal/journalctl.c at v262 and
# therefore replace an earlier -F/-N action when they appear later on the line.
# (--list-boots lines 812-814, --disk-usage 824-826, --header 877-879, --sync 856-858.)
ACTION_FLAGS = ("--list-boots", "--disk-usage", "--header", "--sync")

# The 15 field_list_has_scope_options() terms (filter.c:26-43) — non-regression guard.
LIMITER_ROWS = (
    "arg_boot_filter", "arg_invocation", "arg_dmesg", "arg_cursor",
    "arg_after_cursor", "arg_cursor_file", "arg_system_units",
    "arg_user_units", "arg_syslog_identifier", "arg_exclude_identifier",
    "arg_priorities", "arg_facilities", "arg_since_set",
    "arg_until_set", "arg_pattern",
)

OVERRIDE = re.compile(
    r"last action (?:selected|wins)|overwritten|replaces? the action"
    r"|the (?:-F|-N|field) action (?:is|gets) (?:replaced|overridden)",
    re.I,
)
ORDER = re.compile(r"\b(?:after|before|last|revers|order)\b", re.I)
OUTPUT_ID = re.compile(
    r"not (?:the )?field (?:list|values|names)|boot table|disk[- ]usage"
    r"|header information|header info|\b541\b|\b262\b",
    re.I,
)


class Cannot(Exception):
    def __init__(self, fid, site, detail):
        super().__init__(f"{fid} {site}: {detail}")
        self.fid, self.site, self.detail = fid, site, detail


def git_env():
    """Allow-list env for every git child (same shape as tools/_revision.clean_env)."""
    return {"PATH": "/usr/bin:/bin", "GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat",
            "LC_ALL": "C", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}


def git(repo, *args, timeout=60):
    try:
        return subprocess.run(["git", "--no-pager", "-C", str(repo), *args],
                              stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, env=git_env(), timeout=timeout)
    except subprocess.TimeoutExpired:
        raise Cannot("E-GIT-FAILED", "git", f"git {args[0]} exceeded {timeout}s")
    except OSError as exc:
        raise Cannot("E-GIT-FAILED", "git", str(exc)[:120])


def resolve_commit(repo, revision):
    """Peel to a commit; return (sha, None) or raise Cannot."""
    proc = git(repo, "rev-parse", "--verify", "--quiet", "--end-of-options",
               f"{revision}^{{commit}}")
    if proc.returncode == 0:
        return proc.stdout.decode("ascii", "replace").strip()
    probe = git(repo, "rev-parse", "--git-dir")
    if probe.returncode != 0:
        raise Cannot("E-GIT-FAILED", revision, "repository unavailable")
    raise Cannot("E-REVISION-INVALID", revision, "not a resolvable commit")


def bind(repo, revision, branch):
    """Minimal landed-revision binding: commit exists and is an ancestor of branch."""
    if not re.fullmatch(r"[0-9a-fA-F]{7,64}", revision):
        raise Cannot("E-REVISION-INVALID", revision, "expected 7-64 hex")
    sha = resolve_commit(repo, revision)
    branch_ref = f"refs/heads/{branch}"
    tip = git(repo, "rev-parse", "--verify", "--quiet", branch_ref)
    if tip.returncode != 0:
        raise Cannot("E-BRANCH-MISSING", branch, "ref does not resolve")
    anc = git(repo, "merge-base", "--is-ancestor", sha, tip.stdout.decode("ascii").strip())
    if anc.returncode == 1:
        raise Cannot("E-REVISION-NOT-LANDED", revision, f"not an ancestor of {branch}")
    if anc.returncode >= 2:
        raise Cannot("E-GIT-FAILED", revision, "merge-base failed")
    return sha


def read_git(repo, commit, path):
    proc = git(repo, "show", f"{commit}:{path}")
    if proc.returncode != 0:
        raise Cannot("E-GIT-FAILED", path,
                     proc.stderr.decode("utf-8", "replace").strip()[:120] or "git show failed")
    return proc.stdout.decode("utf-8", "replace")


def read_tree(path):
    target = Path(path)
    if not target.is_file():
        raise Cannot("E-NOTE-MISSING", str(target), "note file not found")
    return target.read_bytes().decode("utf-8")


def table_rows(text):
    """Rows of the Decision table as (cells) tuples, looking for ## Decision table."""
    lines = [ln.rstrip() for ln in text.splitlines()]
    try:
        start = lines.index("## Decision table")
    except ValueError:
        return None
    rows = []
    for ln in lines[start + 1:]:
        if ln.startswith("## "):
            break
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if all(not c for c in cells) or set("".join(cells)) <= {"-", ":"}:
            continue  # separator row
        rows.append(cells)
    return rows


def verdict_of(cells):
    joined = " ".join(cells)
    if "REJECT" in joined:
        return "REJECT"
    if "WORK" in joined:
        return "WORK"
    return None


def evaluate(text):
    """Return (code, [(id, ok, detail)])."""
    findings = []

    # A. rejection line stays verbatim
    ok_a = REJECT_LINE in text
    findings.append(("A-reject-line-verbatim", ok_a,
                     "exact 84-byte scope-rejection sentence present" if ok_a
                     else "scope-rejection sentence missing or altered"))

    rows = table_rows(text)
    if rows is None:
        return CANNOT, findings + [("E-TABLE", False, "## Decision table section not found")]

    # B. action-override classification row exists
    override_rows = []
    for cells in rows:
        joined = " ".join(cells)
        if any(flag in joined for flag in ACTION_FLAGS):
            if OVERRIDE.search(joined) and OUTPUT_ID.search(joined) and ORDER.search(joined):
                override_rows.append(cells)
    ok_b = bool(override_rows)
    findings.append(("B-action-override-row", ok_b,
                     f"{len(override_rows)} action-override classification row(s) with "
                     "last-action-selected, output-identity and order markers" if ok_b
                     else "no action-override classification row: last-action-selected + "
                          "output-identity + order markers all required"))

    # C. no blanket WORK row for an action flag without the override explanation
    blanket = []
    for cells in rows:
        joined = " ".join(cells)
        if any(flag in joined for flag in ACTION_FLAGS) and verdict_of(cells) == "WORK":
            if not OVERRIDE.search(joined):
                blanket.append(" | ".join(cells))
    ok_c = not blanket
    findings.append(("C-no-blanket-work", ok_c,
                     "no WORK row groups an action flag without the override explanation" if ok_c
                     else f"{len(blanket)} blanket WORK row(s): " + " ;; ".join(blanket[:3])))

    # D. the 15 limiter rows survive (non-regression)
    limiter_rows = [c for c in rows if any(t in " ".join(c) for t in LIMITER_ROWS)]
    ok_d = len(limiter_rows) >= 15
    findings.append(("D-limiter-rows-15", ok_d,
                     f"{len(limiter_rows)} limiter rows present (expect 15)" if ok_d
                     else f"{len(limiter_rows)} limiter rows present (expect 15)"))

    code = PASS if all(ok for _, ok, _ in findings) else FAIL
    return code, findings


# ---------------------------------------------------------------------------
# Selftest fixtures — the real baseline rows (unchanged note) and the proposed
# corrected rows (patch proposal).  No lane access.
# ---------------------------------------------------------------------------

BASELINE_TABLE = """\
| limiting option (v262 `field_list_has_scope_options()` term) | CLI form | verdict | evidence pointer |
|---|---|---|---|
| `arg_boot_filter` | `-b`, `--boot=` (any value except `all`) | **REJECT** | `core_boot0`, `core_boot_neg1`, `ext_boot0_F` |
| `arg_invocation` | `--invocation=` | **REJECT** | `live_invocation` (`--invocation=0123456789abcdef0123456789abcdef`) |
| `arg_dmesg` | `-k` | **REJECT** | `ext_kernel_F` (`-b 0 -k -F PRIORITY`) |
| `arg_cursor` | `--cursor=` | **REJECT** | `ext_cursor_F` |
| `arg_after_cursor` | `--after-cursor=` | **REJECT** | `live_after_cursor` |
| `arg_cursor_file` | `--cursor-file=` | **REJECT** | `live_cursor_file` |
| `arg_system_units` | `-u`, `--unit=` | **REJECT** | `core_unit_journald` |
| `arg_user_units` | `--user-unit=` | **REJECT** | `live_user_unit` |
| `arg_syslog_identifier` | `-t`, `--identifier=` | **REJECT** | `live_identifier` (`-t systemd`) |
| `arg_exclude_identifier` | `--exclude-identifier=` | **REJECT** | `live_exclude_id` |
| `arg_priorities` | `-p`, `--priority=` | **REJECT** | `ext_prio_F` |
| `arg_facilities` | `--facility=` | **REJECT** | `live_facility` (`--facility=3`) |
| `arg_since_set` | `--since=` | **REJECT** | `core_since_1h` |
| `arg_until_set` | `--until=` | **REJECT** | `ext_until_F` |
| `arg_pattern` | `--grep=` | **REJECT** | `ext_grep_F` |
| — (no limiting option) | `-F PRIORITY` alone; `-N` alone | **WORK** | `core_plain`, `ext_plain_N` |
| not a limiter | `-n`/`--lines`; `-f`/`--follow`; `-r`/`--reverse`; `-a`/`--all` | **WORK** | `ext_lines1_F`, `ext_lines1_N`, `ext_follow_F`, `ext_reverse_F`, `ext_all_F` |
| not a limiter | `--output-fields=`; `--disk-usage`; `--header`; `--sync` | **WORK** | `live_output_fields`, `ext_diskusage_N`, `ext_header_F`, `ext_sync_F` |
| not a limiter | `--root=`; `-D`/`--directory=`; `--user`; `--system`; `--namespace=` | **WORK** | `ext_root_F`, `ext_dir_F`, `live_user_scope`, `live_system_scope`, `live_namespace` |
| not a limiter | `--boot=all`; `--list-boots`; `--show-cursor`; `--merge` | **WORK** | `live_boot_all` (`--boot=all` sets no boot filter), `live_list_boots`, `live_show_cursor`, `live_merge` |
| not a limiter (does not exempt) | `--quiet` alongside a limiter | **REJECT** (inherits the limiter) | `merged_field_quiet_boot0` (`--quiet -b 0 -F PRIORITY`) |
| — (misuse, not scope rejection) | `-N PRIORITY,MESSAGE` | **REJECT**, but with `Extraneous arguments starting with 'PRIORITY,MESSAGE'` | `merged_fields_default` (54 stderr bytes); `merged_fields_boot0` for `-b 0 -N PRIORITY` (46 bytes) |
"""

AFTER_TABLE = """\
| limiting option (v262 `field_list_has_scope_options()` term) | CLI form | verdict | evidence pointer |
|---|---|---|---|
| `arg_boot_filter` | `-b`, `--boot=` (any value except `all`) | **REJECT** | `core_boot0`, `core_boot_neg1`, `ext_boot0_F` |
| `arg_invocation` | `--invocation=` | **REJECT** | `live_invocation` (`--invocation=0123456789abcdef0123456789abcdef`) |
| `arg_dmesg` | `-k` | **REJECT** | `ext_kernel_F` (`-b 0 -k -F PRIORITY`) |
| `arg_cursor` | `--cursor=` | **REJECT** | `ext_cursor_F` |
| `arg_after_cursor` | `--after-cursor=` | **REJECT** | `live_after_cursor` |
| `arg_cursor_file` | `--cursor-file=` | **REJECT** | `live_cursor_file` |
| `arg_system_units` | `-u`, `--unit=` | **REJECT** | `core_unit_journald` |
| `arg_user_units` | `--user-unit=` | **REJECT** | `live_user_unit` |
| `arg_syslog_identifier` | `-t`, `--identifier=` | **REJECT** | `live_identifier` (`-t systemd`) |
| `arg_exclude_identifier` | `--exclude-identifier=` | **REJECT** | `live_exclude_id` |
| `arg_priorities` | `-p`, `--priority=` | **REJECT** | `ext_prio_F` |
| `arg_facilities` | `--facility=` | **REJECT** | `live_facility` (`--facility=3`) |
| `arg_since_set` | `--since=` | **REJECT** | `core_since_1h` |
| `arg_until_set` | `--until=` | **REJECT** | `ext_until_F` |
| `arg_pattern` | `--grep=` | **REJECT** | `ext_grep_F` |
| — (no limiting option) | `-F PRIORITY` alone; `-N` alone | **WORK** | `core_plain`, `ext_plain_N` |
| not a limiter | `-n`/`--lines`; `-f`/`--follow`; `-r`/`--reverse`; `-a`/`--all` | **WORK** | `ext_lines1_F`, `ext_lines1_N`, `ext_follow_F`, `ext_reverse_F`, `ext_all_F` |
| not a limiter | `--output-fields=`; `--root=`; `-D`/`--directory=`; `--user`; `--system`; `--namespace=`; `--boot=all`; `--show-cursor`; `--merge` | **WORK** | `live_output_fields`, `ext_root_F`, `ext_dir_F`, `live_user_scope`, `live_system_scope`, `live_namespace`, `live_boot_all`, `live_show_cursor`, `live_merge` |
| action override — last action selected | `--list-boots` **after** `-F`/`-N` (e.g. `-F PRIORITY --list-boots`) | exit 0, but output is the **boot table**, not the field list; `--list-boots` replaced the `-F` action (`ACTION_LIST_BOOTS`, journalctl.c:812-814), so the guard at :958 has no field-list action to fire on | `live_list_boots` |
| action override — last action selected | `--disk-usage`, `--header`, `--sync` **after** `-F`/`-N` | exit 0, but output is that action's own output (disk usage line / header information / sync notice), not the field list; the action flag is overwritten (journalctl.c:824-826, 877-879, 856-858) | `live_diskusage_F`, `live_header_F` (probed 2026-10-25) |
| action override — last action selected (reverse order) | `-F`/`-N` **after** an action flag (e.g. `--list-boots -F PRIORITY`, `--disk-usage -N`, `--header -F PRIORITY`) | exit 0 **and** genuine field enumeration: the field action is selected last, so the guard still applies when a limiter is present | `ext_diskusage_N`, `ext_header_F`, `ext_sync_F` |
| not a limiter (does not exempt) | `--quiet` alongside a limiter | **REJECT** (inherits the limiter) | `merged_field_quiet_boot0` (`--quiet -b 0 -F PRIORITY`) |
| — (misuse, not scope rejection) | `-N PRIORITY,MESSAGE` | **REJECT**, but with `Extraneous arguments starting with 'PRIORITY,MESSAGE'` | `merged_fields_default` (54 stderr bytes); `merged_fields_boot0` for `-b 0 -N PRIORITY` (46 bytes) |
"""

BASELINE_NOTE = (
    "# systemd 262 rejects `journalctl -F`/`-N` combined with journal-limiting options (round 36, C2 exploratory)\n"
    "## The rejection\n\n```\n" + REJECT_LINE + "\n```\n\n## Decision table\n\n"
    + BASELINE_TABLE + "\n## Safe substitution\n\nplaceholder\n"
)

AFTER_NOTE = (
    "# systemd 262 rejects `journalctl -F`/`-N` combined with journal-limiting options (round 36, C2 exploratory)\n"
    "## The rejection\n\n```\n" + REJECT_LINE + "\n```\n\n## Decision table\n\n"
    + AFTER_TABLE + "\n## Safe substitution\n\nplaceholder\n"
)

NO_REJECT_NOTE = AFTER_NOTE.replace(REJECT_LINE, "different sentence.")


def _summarize(code):
    return {PASS: "PASS", FAIL: "FAIL", CANNOT: "CANNOT_EVALUATE"}[code]


def selftest():
    failures = []
    passed = 0
    total = 0

    def case(name, text, want):
        nonlocal passed, total
        total += 1
        code, findings = evaluate(text)
        if code != want:
            failures.append(f"{name}: code={_summarize(code)} want={_summarize(want)} "
                            f"({[f[0] for f in findings if not f[1]]})")
        else:
            passed += 1
        return code

    # Hermetic fixtures: baseline must FAIL, corrected must PASS, altered reject must FAIL.
    case("baseline-table", BASELINE_NOTE, FAIL)
    case("after-table", AFTER_NOTE, PASS)
    case("after-no-reject-line", NO_REJECT_NOTE, FAIL)

    # Committed-read path over a mktemp git sandbox (top-level verified before commits).
    sandbox = Path(tempfile.mkdtemp(prefix="c2-action-override-"))
    try:
        repo = sandbox / "repo"
        repo.mkdir()
        g = git(repo, "init", "-q")
        if g.returncode != 0:
            return CANNOT, ["git init failed in sandbox"]
        # verify top-level equals fixture root before any commit
        top = git(repo, "rev-parse", "--show-toplevel")
        if top.returncode != 0 or Path(top.stdout.decode().strip()) != repo:
            return CANNOT, ["sandbox top-level verification failed before commit"]
        note = repo / NOTE_RELPATH
        note.parent.mkdir(parents=True)
        note.write_text(AFTER_NOTE, encoding="utf-8")
        git(repo, "add", NOTE_RELPATH)
        c = git(repo, "-c", "user.name=Fx", "-c", "user.email=fx@fx",
                "commit", "-q", "-m", "after-note")
        if c.returncode != 0:
            return CANNOT, ["sandbox commit failed"]
        after_sha = resolve_commit(repo, "HEAD")
        code, _ = evaluate(read_git(repo, after_sha, NOTE_RELPATH))
        total += 1
        if code != PASS:
            failures.append(f"git-after: code={_summarize(code)} want=PASS")
        else:
            passed += 1

        note.write_text(BASELINE_NOTE, encoding="utf-8")
        git(repo, "add", NOTE_RELPATH)
        git(repo, "-c", "user.name=Fx", "-c", "user.email=fx@fx",
            "commit", "-q", "-m", "baseline-note")
        before_sha = resolve_commit(repo, "HEAD")
        code, _ = evaluate(read_git(repo, before_sha, NOTE_RELPATH))
        total += 1
        if code != FAIL:
            failures.append(f"git-before: code={_summarize(code)} want=FAIL")
        else:
            passed += 1

        # binding errors: non-hex revision -> CANNOT
        total += 1
        try:
            bind(repo, "nothex", "master")
            failures.append("bind-nonhex: no Cannot raised")
        except Cannot:
            passed += 1
    finally:
        shutil.rmtree(sandbox, ignore_errors=True)

    if failures:
        print(f"CHECK_C2_ACTION_OVERRIDE_SELFTEST: FAIL ({total} cases, {passed} passed)")
        print("\n".join("  " + f for f in failures))
        return FAIL
    print(f"CHECK_C2_ACTION_OVERRIDE_SELFTEST: PASS ({total} cases, {passed} passed, 0 failed)")
    return PASS


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Gate: r36 C2 action-override classification in the journalctl note.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--note", metavar="PATH", help="note file to inspect (worktree)")
    group.add_argument("--revision", metavar="REV", help="7-64 hex landed commit")
    group.add_argument("--selftest", action="store_true", help="hermetic suite")
    parser.add_argument("--lane", metavar="ROOT", default=str(LANE_ROOT),
                        help="lane repository root (default: lane root)")
    parser.add_argument("--branch", metavar="BRANCH", default="master")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    branch, revision = args.branch, "worktree"
    try:
        if args.revision is not None:
            revision = args.revision
            sha = bind(Path(args.lane), revision, branch)
            text = read_git(Path(args.lane), sha, NOTE_RELPATH)
        else:
            text = read_tree(args.note)
    except Cannot as exc:
        print(f"CHECK_C2_ACTION_OVERRIDE: CANNOT_EVALUATE "
              f"[{exc.fid} {exc.site}] {exc.detail} (revision={revision} branch={branch})")
        return CANNOT
    except Exception as exc:
        print(f"CHECK_C2_ACTION_OVERRIDE: CANNOT_EVALUATE [E-INTERNAL] {str(exc)[:120]}")
        return CANNOT

    code, findings = evaluate(text)
    print(f"CHECK_C2_ACTION_OVERRIDE: {_summarize(code)} (revision={revision} branch={branch})")
    for fid, ok, detail in findings:
        print(f"  [{'PASS' if ok else 'FAIL'}] {fid}: {detail}")
    return code


if __name__ == "__main__":
    sys.exit(main())
