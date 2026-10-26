#!/usr/bin/env python3
"""Mechanical call-path scanner for btrfs-progs cmds/scrub.c (C2-5).

Reads the frozen source read-only; prints one line per finding with the
source line number so every claim can be re-checked by grep -n.
"""
import re
import sys

SRC = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/frozen/src/scrub.c"


def load():
    with open(SRC, "r", encoding="utf-8", errors="replace") as f:
        return f.readlines()


def func_span(lines, name):
    """Return (start, end) 1-based inclusive lines of a C function body.

    start = line of the opening brace of `name(`, end = matching brace line.
    Brace matching ignores braces in // comments, /* */ comments and
    "..." / '...' literals well enough for this file.
    """
    sig = re.compile(r"^\s*(?:static\s+)?[A-Za-z_][\w \t\*]*\b" + re.escape(name) + r"\s*\(")
    start = None
    for i, ln in enumerate(lines):
        if sig.match(ln):
            start = i
            break
    if start is None:
        return None
    # find opening brace
    depth = 0
    in_block = False
    in_line = False
    in_str = False
    in_chr = False
    esc = False
    opened = False
    for i in range(start, len(lines)):
        ln = lines[i]
        j = 0
        while j < len(ln):
            c = ln[j]
            nxt = ln[j + 1] if j + 1 < len(ln) else ""
            if in_line:
                break
            if in_block:
                if c == "*" and nxt == "/":
                    in_block = False
                    j += 2
                    continue
                j += 1
                continue
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
                j += 1
                continue
            if in_chr:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == "'":
                    in_chr = False
                j += 1
                continue
            if c == "/" and nxt == "/":
                in_line = True
                break
            if c == "/" and nxt == "*":
                in_block = True
                j += 2
                continue
            if c == '"':
                in_str = True
            elif c == "'":
                in_chr = True
            elif c == "{":
                depth += 1
                opened = True
            elif c == "}":
                depth -= 1
                if opened and depth == 0:
                    return (start + 1, i + 1)
            j += 1
        in_line = False
    return (start + 1, len(lines))


def body(lines, span):
    return [(n, lines[n - 1]) for n in range(span[0], span[1] + 1)]


def main():
    lines = load()
    out = []
    spans = {}
    for fn in ("scrub_start", "scrub_write_file", "scrub_write_progress",
               "is_scrub_running_in_kernel", "cmd_scrub_resume",
               "scrub_open_file_w", "scrub_rename_file", "scrub_datafile"):
        spans[fn] = func_span(lines, fn)
        out.append(f"SPAN {fn}: {spans[fn][0]}-{spans[fn][1]}")

    # (1) every call of scrub_write_file and scrub_write_progress, and whether
    #     the callee reaches scrub_resumed_stats (definition line 800, use 864).
    def calls(name):
        res = []
        for i, ln in enumerate(lines, 1):
            # call site: name( not preceded by the type tokens of the definition
            if re.search(r"\b" + name + r"\s*\(", ln) and not re.search(
                    r"^\s*static\s+[A-Za-z_][\w \t\*]*\b" + name + r"\s*\(", ln):
                res.append((i, ln.rstrip()))
        return res

    for name in ("scrub_write_file", "scrub_write_progress"):
        out.append(f"CALLS {name}:")
        for i, ln in calls(name):
            out.append(f"  {i}: {ln.strip()}")

    out.append("RESUMED_STATS sites:")
    for i, ln in enumerate(lines, 1):
        if "scrub_resumed_stats" in ln:
            out.append(f"  {i}: {ln.strip()}")

    # (2) unlink/remove/unlinkat calls + argument text
    out.append("UNLINK FAMILY:")
    for i, ln in enumerate(lines, 1):
        m = re.search(r"\b(unlink|unlinkat|remove)\s*\(([^;]*)\)", ln)
        if m:
            out.append(f"  {i}: {m.group(1)}({m.group(2).strip()})")
    out.append("RENAME sites:")
    for i, ln in enumerate(lines, 1):
        if re.search(r"\brename\s*\(", ln):
            out.append(f"  {i}: {ln.strip()}")

    # (3) do_print assignments and reads, inside and outside scrub_start
    s0, s1 = spans["scrub_start"]
    out.append("DO_PRINT (line: kind: text):")
    for i, ln in enumerate(lines, 1):
        if "do_print" not in ln:
            continue
        if re.search(r"\bdo_print\s*=", ln):
            kind = "ASSIGN"
            if "if (" in ln or "if(" in ln and "==" in ln:
                kind = "ASSIGN(in-if)"
        else:
            kind = "READ"
        where = "in scrub_start" if s0 <= i <= s1 else "outside scrub_start"
        out.append(f"  {i}: {kind} [{where}]: {ln.strip()}")

    # (4) every assignment to err in scrub_start after the first record write
    #     (first record-write call line, passed as argv[1] default 1503)
    first_write = int(sys.argv[1]) if len(sys.argv) > 1 else 1503
    out.append(f"ERR_ASSIGN in scrub_start after line {first_write}:")
    for i in range(first_write, s1 + 1):
        ln = lines[i - 1]
        if re.search(r"(?<![\w.>])err\s*=", ln) or re.search(r"\+\+\s*err\b|\berr\s*\+\+", ln):
            out.append(f"  {i}: {ln.strip()}")
    out.append(f"ERR_ASSIGN in scrub_start before/at line {first_write}:")
    for i in range(s0, first_write + 1):
        ln = lines[i - 1]
        if re.search(r"(?<![\w.>])err\s*=", ln):
            out.append(f"  {i}: {ln.strip()}")

    # (5) callers of is_scrub_running_in_kernel
    out.append("IS_SCRUB_RUNNING_IN_KERNEL:")
    for i, ln in enumerate(lines, 1):
        if "is_scrub_running_in_kernel" in ln:
            role = "DEF" if spans["is_scrub_running_in_kernel"][0] == i else "USE"
            out.append(f"  {i}: {role}: {ln.strip()}")

    # (6) every place in_progress is set (word-boundary, whole file)
    out.append("IN_PROGRESS set/read:")
    for i, ln in enumerate(lines, 1):
        if re.search(r"(?<![A-Za-z0-9_])in_progress(?![A-Za-z0-9_])", ln):
            kind = "SET" if re.search(r"in_progress\s*=[^=]", ln) else "READ"
            out.append(f"  {i}: {kind}: {ln.strip()}")

    # control-flow sanity: ioctl sites that touch kernel scrub state
    out.append("SCRUB IOCTL sites:")
    for i, ln in enumerate(lines, 1):
        if re.search(r"BTRFS_IOC_SCRUB(_PROGRESS|_CANCEL)?\b", ln):
            out.append(f"  {i}: {ln.strip()}")

    print("\n".join(out))


if __name__ == "__main__":
    main()
