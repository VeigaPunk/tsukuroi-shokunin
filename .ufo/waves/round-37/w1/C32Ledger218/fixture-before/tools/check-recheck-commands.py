#!/usr/bin/env python3
"""Read-only recheck-procedure gate (rounds 17-18).

Round 17's steer withholds package, boot-image and service action. A knowledge
entry's `recheck:` line is a procedure a later agent is invited to follow, so
a forbidden binary there re-authorizes the action the steer withheld: the L1
seat ran `pacman -Q ...` after reading
corpus/knowledge/initramfs-v42-sysroot-recovery.md:3. This gate reads the
named files at an immutable revision and, in the LAST `recheck:` line (later
lines supersede earlier pointer ones, per the journal-boot-plane convention),
reports every forbidden binary a backticked command actually invokes.

Pointer procedures (round 18; round-17 closure defect 6, aur-risk-plane.md:347
"§7's ... probe set"): a named section pointer in that line (`§7`, `§7's`,
`§§1–5`, `§4.2`, `Appendix`, `Appendix A`) is resolved to its heading in the
same file (headings inside fenced blocks are not headings; a section runs to
the next heading of the same or a higher level, so subsections and dotted
descendants such as `## 0.1` stay inside §0). The commands the section declares
(backtick span, fenced block line, or `procedure:` line) are inspected like
the line's own, and a forbidden one is RECHECK-FORBIDDEN-INVOCATION at the
command's line. A pointer that names no heading is RECHECK-POINTER-UNRESOLVED.
Pointers inside a backtick span or right after a `*.md` name (another file's
section) are not followed, and resolution is one level deep.

An appended `## R17-RECHECK — steer-safe procedure` or
`## R18-RECHECK — steer-safe procedure` section resolves the header, literal
and pointer invocations alike, only when the section itself supplies at least
one procedure command and invokes no forbidden binary, including through a
section pointer on one of its `procedure:` lines. The latest round's section
is operative and supersedes an earlier round's (append-only repair); the
operative heading must be unique. Prose that merely names a binary (for
example "never run pacman") is not an invocation, nor is a shell comment.

--revision is bound by the shared tools/_revision.py (branch syntax before
revision syntax, first failure wins, exactly one finding, exit 2); --exec-log
is read at that same bound commit.

Exit 0 pass / 1 finding / 2 could-not-evaluate; JSON on stdout.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from collections import namedtuple
from pathlib import Path

sys.dont_write_bytecode = True  # shared-module import stays read-only
import _revision

PASS, FAIL, CANNOT = 0, 1, 2
ROOT = Path(__file__).resolve().parents[1]
# Steer-safe sections, oldest round first; the latest one present is operative.
HEADINGS = ("## R17-RECHECK — steer-safe procedure",
            "## R18-RECHECK — steer-safe procedure")
DEFAULT_FORBID = ("pacman", "checkupdates", "yay", "paru", "mkinitcpio", "limine-update")
BINARY = re.compile(r"^[A-Za-z0-9_.+-]+$")
ASSIGN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
PROCEDURE_LINE = re.compile(
    r"^(?:[-*+]\s*)?(?:procedure|recheck|commands?|steps?)\s*[:—–-]\s*(.+)$", re.I)
# Named same-file section pointers: `§7`, `§7's`, `§§1–5`, `§0–§3`, `§4.2`, `Appendix A`.
POINTER = re.compile(r"§§?\s*(\d+(?:\.\d+)*)(?:\s*[–—-]\s*§?\s*(\d+(?:\.\d+)*))?")
APPENDIX = re.compile(r"\bAppendix\b(?:\s+([A-Z])\b)?")
OTHER_FILE = re.compile(r"\.md\b[`'’s]*\s*$")
HEADING_LINE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
SECTION_NUMBER = re.compile(r"§?\s*(\d+(?:\.\d+)*)(?=$|[\s.):—–-])")
# Shell control words that can stand where a command name would.
KEYWORDS = {"if", "then", "else", "elif", "fi", "do", "done", "case", "esac", "in",
            "while", "until", "for", "select", "function", "{", "}", "!"}
SHELLS = {"sh", "ash", "bash", "dash", "zsh", "ksh", "busybox"}
# wrapper: (options taking a separate argument, positional arguments to skip)
WRAPPERS = {
    "sudo": ({"-u", "-g", "-C", "-h", "-p", "-r", "-t", "-T", "-R", "-U", "-D",
              "-Eu", "--user", "--group", "--close-from", "--chdir", "--chroot",
              "--command-timeout", "--prompt", "--role", "--type", "--other-user"}, 0),
    "doas": ({"-a", "-C", "-u", "--user"}, 0),
    "env": ({"-u", "-C", "-S", "--unset", "--chdir", "--split-string"}, 0),
    "command": (set(), 0),
    "exec": ({"-a"}, 0),
    "nohup": (set(), 0),
    "builtin": (set(), 0),
    "time": ({"-f", "-o", "--format", "--output"}, 0),
    "nice": ({"-n", "--adjustment"}, 0),
    "ionice": ({"-c", "-n", "-p", "--class", "--classdata", "--pid"}, 0),
    "stdbuf": ({"-i", "-o", "-e", "--input", "--output", "--error"}, 0),
    "timeout": ({"-s", "-k", "-vs", "--signal", "--kill-after"}, 1),
    "xargs": ({"-a", "-d", "-E", "-I", "-L", "-n", "-P", "-s",
               "--arg-file", "--delimiter", "--replace-str", "--max-args",
               "--max-procs", "--max-chars"}, 0),
}

Finding = namedtuple("Finding", "id site detail")
Counts = namedtuple("Counts", "forbidden files invocations pointers flagged resolved clean")
Result = namedtuple("Result", "code findings counts")


class Cannot(Exception):
    def __init__(self, fid, site, detail):
        super().__init__(detail)
        self.fid, self.site, self.detail = fid, site, detail


def segments(text):
    """Split shell text on top-level separators, honoring quoting.

    A backtick span is re-split as its own command sequence, so a prose span
    holding several commands is scanned command by command. A word-initial `#`
    opens a shell comment that runs to the end of the line: nothing in it,
    backticks included, is executed (degraded-triage-r4.md:597 quotes
    `pacman -Sl offline` inside such a comment).
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
        if char == "#" and (not buf or buf[-1].isspace()):
            while index < size and text[index] != "\n":
                index += 1
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


def _shell_command_index(args):
    for index, token in enumerate(args):
        if token == "-c" or re.fullmatch(r"-[A-Za-z]*c[A-Za-z]*", token):
            return index + 1
    return None


def _wrapper_shell_payloads(text):
    """Yield explicit env -S and sudo shell command strings without evaluating them."""
    for segment in segments(text):
        tokens = words(segment)
        if not tokens:
            continue
        base = tokens[0].rsplit("/", 1)[-1]
        if base == "env":
            index = 1
            while index < len(tokens):
                token = tokens[index]
                if token in ("-S", "--split-string"):
                    if index + 1 < len(tokens):
                        yield " ".join(tokens[index + 1:])
                    break
                if token.startswith("--split-string="):
                    payload = [token.partition("=")[2], *tokens[index + 1:]]
                    yield " ".join(payload)
                    break
                if token.startswith("-S") and token != "-S":
                    payload = [token[2:].lstrip("="), *tokens[index + 1:]]
                    yield " ".join(payload)
                    break
                if token in WRAPPERS["env"][0] and index + 1 < len(tokens):
                    index += 2
                    continue
                if ASSIGN.match(token):
                    index += 1
                    continue
                if token.startswith("-") and token != "-":
                    index += 1
                    continue
                break
        elif base == "sudo":
            index, shell, inline = 1, False, None
            while index < len(tokens):
                token = tokens[index]
                if token == "--":
                    index += 1
                    break
                if token in ("-s", "-i", "--shell", "--login"):
                    shell = True
                    index += 1
                    continue
                if token.startswith("--shell=") or token.startswith("--login="):
                    shell, inline = True, token.partition("=")[2]
                    index += 1
                    break
                if token in WRAPPERS["sudo"][0] and index + 1 < len(tokens):
                    index += 2
                    continue
                if token.startswith("-") and token != "-":
                    index += 1
                    continue
                break
            if shell and inline is not None:
                yield inline
            elif shell and index < len(tokens):
                remaining = tokens[index:]
                if len(remaining) == 1 and any(ch.isspace() for ch in remaining[0]):
                    yield remaining[0]


def invocations(text, forbid, depth=0):
    """Binary names in bounded shell text, wrapper payloads and -c commands."""
    hits = []
    if depth > 4:
        return hits
    for payload in _wrapper_shell_payloads(text):
        hits.extend(invocations(payload, forbid, depth + 1))
    for base, args in simple_commands(text):
        if base in forbid:
            hits.append(base)
            continue
        if base in SHELLS:
            if base == "busybox":
                if not args:
                    continue
                applet = args[0].rsplit("/", 1)[-1]
                if applet in forbid:
                    hits.append(applet)
                    continue
                if applet not in SHELLS:
                    continue
                args = args[1:]
            command_index = _shell_command_index(args)
            if command_index is not None and command_index < len(args):
                hits.extend(invocations(args[command_index], forbid, depth + 1))
        elif base == "eval" and args:
            hits.extend(invocations(" ".join(args), forbid, depth + 1))
    return hits


SYSTEMCTL_READ_VERBS = frozenset((
    "cat", "show", "status", "list-units", "list-unit-files", "list-timers",
    "list-dependencies", "is-active", "is-enabled", "is-system-running"))
SYSTEMCTL_READ_FLAGS = frozenset((
    "--user", "--system", "--no-pager", "--all", "--failed", "--wait",
    "--reverse", "--runtime", "-a", "--full", "-l", "--no-legend", "--plain",
    "--quiet", "-q", "--value"))
SYSTEMCTL_VALUE_FLAGS = frozenset((
    "--property", "-p", "--type", "-t", "--state", "--output", "-o", "--lines", "-n",
    "--host", "-H", "--machine", "-M", "--root", "--image"))

SYSTEMCTL_CONTEXT_SHORT_PREFIXES = ("-H", "-M")

def _systemctl_read_only(args):
    """Finite observed read forms; unknown/effectful flags and verbs fail closed."""
    verb, index, options, scope = None, 0, True, None
    while index < len(args):
        token = args[index]
        if token == "":
            return False
        if options and token == "--":
            options = False
            index += 1
            continue
        if options and token in ("--user", "--system"):
            if scope is not None and scope != token:
                return False
            scope = token
            index += 1
            continue
        if options and any(token.startswith(prefix) and token != prefix
                           for prefix in SYSTEMCTL_CONTEXT_SHORT_PREFIXES):
            index += 1
            continue
        if options and token.startswith("-"):
            flag, equals, value = token.partition("=")
            if flag in SYSTEMCTL_READ_FLAGS and not equals:
                index += 1
                continue
            if flag in SYSTEMCTL_VALUE_FLAGS:
                if equals:
                    if not value:
                        return False
                    index += 1
                elif index + 1 < len(args):
                    value_arg = args[index + 1]
                    if not value_arg or value_arg.startswith("-"):
                        return False
                    index += 2
                else:
                    return False

                continue
            return False
        if verb is None:
            verb = token
        index += 1
    return (verb or "list-units") in SYSTEMCTL_READ_VERBS


def systemctl_violations(text, depth=0):
    """Inspect bounded command text; this is not a shell-equivalence proof."""
    if depth > 4:
        return []
    hits = []
    for payload in _wrapper_shell_payloads(text):
        hits.extend(systemctl_violations(payload, depth + 1))
    for base, args in simple_commands(text):
        if base == "systemctl":
            if not _systemctl_read_only(args):
                hits.append(base)
        elif base in SHELLS:
            if base == "busybox":
                if not args:
                    continue
                applet = args[0].rsplit("/", 1)[-1]
                if applet == "systemctl":
                    if not _systemctl_read_only(args[1:]):
                        hits.append(applet)
                    continue
                if applet not in SHELLS:
                    continue
                args = args[1:]
            command_index = _shell_command_index(args)
            if command_index is not None and command_index < len(args):
                hits.extend(systemctl_violations(args[command_index], depth + 1))
        elif base == "eval" and args:
            hits.extend(systemctl_violations(" ".join(args), depth + 1))
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
    """(line number, command text) pairs a section declares: fenced block lines,
    backtick spans and `procedure:`-style lines (steer-safe or pointed-to)."""
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


def procedure_lines(lines, first):
    """(line number, text) of `procedure:`-style lines outside fenced blocks."""
    out, fenced = [], False
    for offset, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fenced = not fenced
            continue
        declared = None if fenced else PROCEDURE_LINE.match(stripped)
        if declared:
            out.append((first + offset, declared.group(1)))
    return out


def section_key(number):
    """Canonical dotted section number: `07.2` and `7.2` name one section."""
    return ".".join(str(int(part)) for part in number.split("."))


def headings(lines):
    """(index, level, number, appendix) per Markdown heading outside fenced blocks.

    number is the canonical leading section number or None; appendix is the
    appendix letter ("" when unlettered), or None when the heading is no appendix.
    A `# 1. ...` comment inside a fenced shell block is not a heading.
    """
    out, fenced = [], False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fenced = not fenced
            continue
        match = None if fenced else HEADING_LINE.match(line)
        if match is None:
            continue
        title = match.group(2)
        number = SECTION_NUMBER.match(title)
        rest = title[number.end():].lstrip(" .):—–-") if number else title
        appendix = APPENDIX.match(rest)
        out.append((index, len(match.group(1)),
                    section_key(number.group(1)) if number else None,
                    (appendix.group(1) or "") if appendix else None))
    return out


def section_span(heads, position, total):
    """(heading index, end index) of one heading's section: it runs to the next
    heading of the same or a higher level that is not its dotted descendant."""
    start, level, number, _ = heads[position]
    for index, other_level, other_number, _ in heads[position + 1:]:
        if other_level <= level and not (number is not None and other_number is not None
                                         and other_number.startswith(number + ".")):
            return start, index
    return start, total


def pointers(text):
    """(label, kind, key) per named same-file section pointer in `text`.

    kind "section" keys a canonical number (`§§1–5` expands to 1..5); kind
    "appendix" keys a letter ("" for a bare `Appendix`). A pointer inside a
    backtick span, or right after a `*.md` name, is not a same-file pointer.
    """
    spans = [match.span() for match in re.finditer(r"`[^`]*`", text)]

    def same_file(position):
        return (not any(start <= position < end for start, end in spans)
                and not OTHER_FILE.search(text[:position]))

    out = []
    for match in POINTER.finditer(text):
        if not same_file(match.start()):
            continue
        label = " ".join(match.group(0).split())
        first = section_key(match.group(1))
        last = section_key(match.group(2)) if match.group(2) else None
        if (last and first.isdigit() and last.isdigit()
                and int(first) <= int(last) <= int(first) + 50):
            keys = [str(value) for value in range(int(first), int(last) + 1)]
        else:
            keys = [first] + ([last] if last else [])
        out.extend((label, "section", key) for key in keys)
    for match in APPENDIX.finditer(text):
        if same_file(match.start()):
            out.append((" ".join(match.group(0).split()), "appendix", match.group(1) or ""))
    return out


def resolve_pointer(heads, total, kind, key):
    """Section spans one pointer names; [] when the file has no such heading.

    A number names its highest-level heading(s); a bare `Appendix` names every
    appendix heading, `Appendix A` only that letter's.
    """
    if kind == "section":
        hits = [position for position, head in enumerate(heads) if head[2] == key]
        if hits:
            top = min(heads[position][1] for position in hits)
            hits = [position for position in hits if heads[position][1] == top]
    else:
        hits = [position for position, head in enumerate(heads)
                if head[3] is not None and (not key or head[3] == key)]
    return [section_span(heads, position, total) for position in hits]


def advisory_heading(line):
    """An explicitly non-procedural section cannot satisfy a procedure pointer."""
    title = line.lstrip("# ").casefold()
    return bool(re.search(r"\bunknowns?\b|\bout[- ]of[- ]reach\b", title))


def executable_argv0(command):
    """Reject empty quotes, unmatched quoting and wrapper-only pseudo-commands."""
    try:
        shlex.split(command, comments=True)
    except ValueError:
        return False
    return any(name.strip() for name, _ in simple_commands(command))


def follow_pointers(lines, heads, text, forbid):
    """Follow the same-file section pointers in `text` one level deep.

    Returns (sections inspected, unresolved pointers, [(label, line, name, command)]);
    each section is inspected once, so `§§1–5` with `§3` reads §3 once.
    """
    seen, unresolved, hits = [], [], []
    for label, kind, key in pointers(text):
        spans = resolve_pointer(heads, len(lines), kind, key)
        if not spans:
            name = label if kind == "appendix" else f"§{key}"
            if name not in unresolved:
                unresolved.append(name)
            continue
        for start, end in spans:
            if (start, end) in seen:
                continue
            seen.append((start, end))
            if advisory_heading(lines[start]):
                unresolved.append(f"{label} (explicitly advisory, not a procedure)")
                continue
            for number, command in section_commands(lines[start + 1:end], start + 2):
                hits.extend((label, number, name, command)
                            for name in invocations(command, forbid))
    return len(seen), unresolved, hits


def section(lines):
    """State of the operative appended steer-safe section for one file.

    The latest round's heading present is operative (an R18 section supersedes
    an R17 one); the operative heading must appear exactly once.
    """
    found = {heading: [index for index, line in enumerate(lines) if line.strip() == heading]
             for heading in HEADINGS}
    operative = next((heading for heading in reversed(HEADINGS) if found[heading]), None)
    if operative is None:
        return {"present": False, "duplicates": 0}
    hits = found[operative]
    if len(hits) > 1:
        return {"present": True, "duplicates": len(hits), "line": hits[0],
                "commands": [], "procedures": []}
    first = hits[0] + 1
    end = len(lines)
    for index in range(first, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return {"present": True, "duplicates": 1, "line": hits[0],
            "commands": section_commands(lines[first:end], first + 1),
            "procedures": procedure_lines(lines[first:end], first + 1)}


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
    heads = headings(lines)
    sections, unresolved, pointer_hits = follow_pointers(lines, heads, body, forbid)
    invocations_seen = len(header_hits) + len(pointer_hits)
    state = section(lines)
    resolved = False
    if state["present"]:
        if state["duplicates"] > 1:
            findings.append(Finding("RECHECK-STEER-SAFE-INVALID", path,
                                    "steer-safe heading appears more than once"))
        elif (not state["commands"]
              or not any(executable_argv0(command) for _, command in state["commands"])
              or any(not command.lstrip().startswith("#") and not executable_argv0(command)
                     for _, command in state["commands"])):
            findings.append(Finding("RECHECK-STEER-SAFE-INVALID", path,
                                    "steer-safe section has no parseable executable argv0 "
                                    "or contains an incomplete command"))
        else:
            unsafe, dangling = [], []
            for number, command in state["commands"]:
                hits = invocations(command, forbid)
                invocations_seen += len(hits)
                if hits:
                    unsafe.append((number, hits[0], command, ""))
            for _, procedure in state["procedures"]:
                _, missing, reached = follow_pointers(lines, heads, procedure, forbid)
                invocations_seen += len(reached)
                dangling.extend(missing)
                unsafe.extend((number, name, command, f" via {label}")
                              for label, number, name, command in reached)
            if unsafe:
                number, name, command, via = unsafe[0]
                findings.append(Finding(
                    "RECHECK-FORBIDDEN-INVOCATION", f"{path}:{number}",
                    f"steer-safe section invokes {name}{via}: "
                    f"{' '.join(command.split())[:80]}"))
                findings.append(Finding("RECHECK-STEER-SAFE-INVALID", path,
                                        "steer-safe section still invokes a forbidden binary"))
            elif dangling:
                findings.append(Finding("RECHECK-STEER-SAFE-INVALID", path,
                                        f"steer-safe section pointer {dangling[0]} cannot "
                                        "resolve to a procedure in this file"))
            else:
                resolved = True
    if not resolved:
        if header_hits:
            findings.append(Finding(
                "RECHECK-FORBIDDEN-INVOCATION", f"{path}:{index + 1}",
                "recheck procedure invokes " + ", ".join(sorted(set(header_hits)))))
        reported = set()
        for label, number, _, command in pointer_hits:
            if label in reported:
                continue
            reported.add(label)
            names = ", ".join(sorted({hit[2] for hit in pointer_hits if hit[0] == label}))
            findings.append(Finding(
                "RECHECK-FORBIDDEN-INVOCATION", f"{path}:{number}",
                f"recheck pointer {label} (line {index + 1}) reaches {names}: "
                f"{' '.join(command.split())[:80]}"))
        findings.extend(Finding("RECHECK-POINTER-UNRESOLVED", f"{path}:{index + 1}",
                                f"recheck pointer {label} cannot resolve to a procedure in this file")
                        for label in unresolved)
    total_hits = len(header_hits) + len(pointer_hits)
    flagged = int(any(item.id == "RECHECK-FORBIDDEN-INVOCATION" for item in findings))
    clean = int(not findings and not total_hits and not unresolved)
    return findings, {"invocations": invocations_seen, "pointers": sections,
                      "flagged": flagged, "resolved": int(bool(total_hits or unresolved) and resolved),
                      "clean": clean}


def assess_exec_log(path, text, forbid):
    """R17-STEER-SCOPE: lines `$ <command>` an executor actually ran; any forbidden
    binary among them is EXEC-STEER-VIOLATION (catches the event, not only prose)."""
    findings, hits = [], 0
    for number, line in enumerate(text.splitlines(), 1):
        if not line.startswith("$ "):
            continue
        found = invocations(line[2:], forbid)
        if "systemctl" not in forbid:
            found.extend(systemctl_violations(line[2:]))
        if found:
            hits += len(found)
            findings.append(Finding("EXEC-STEER-VIOLATION", f"{path}:{number}",
                                    "executed command invokes " + ",".join(sorted(set(found)))))
    return findings, hits


def evaluate(files, forbid):
    findings, invocations_seen, sections, flagged, resolved, clean = [], 0, 0, 0, 0, 0
    for path, text in files:
        file_findings, counts = assess_file(path, text, forbid)
        findings.extend(file_findings)
        invocations_seen += counts["invocations"]
        sections += counts["pointers"]
        flagged += counts["flagged"]
        resolved += counts["resolved"]
        clean += counts["clean"]
    findings = [Finding(*key) for key in
                sorted({(item.id, item.site, item.detail) for item in findings})]
    counts = Counts(list(forbid), len(files), invocations_seen, sections, flagged, resolved,
                    clean)
    return Result(FAIL if findings else PASS, findings, counts)


def emit(status, revision, branch, branch_tip, findings, counts, out=None,
         origin_tip=None, message=None, extra=None):
    payload = {
        "status": status,
        "revision": revision,
        "branch": branch,
        "branch_tip": branch_tip,
        "origin_tip": origin_tip,
        "forbidden": list(counts.forbidden) if counts else [],
        "file_count": counts.files if counts else 0,
        "invocation_count": counts.invocations if counts else 0,
        "pointer_section_count": counts.pointers if counts else 0,
        "flagged_count": counts.flagged if counts else 0,
        "resolved_count": counts.resolved if counts else 0,
        "clean_count": counts.clean if counts else 0,
        "scope": ("last recheck: line, its same-file section pointers and the operative "
                  "R17/R18 steer-safe section; read-only, no host action taken"),
        "findings": [{"id": item.id, "site": item.site, "detail": item.detail}
                     for item in findings],
    }
    if message:
        payload["message"] = message
    payload.update(extra or {})
    print(json.dumps(payload, sort_keys=True), file=out or sys.stdout)
    return {"PASS": PASS, "FAIL": FAIL, "CANNOT_EVALUATE": CANNOT}[status]


def git(repo, *args):
    env = {"PATH": "/usr/bin:/bin", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}  # round-34 C1: fixed allow-list, no ambient copy
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
        description="Read-only recheck-procedure gate (rounds 17-18).",
        exit_on_error=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--revision", metavar="REV",
                       help="required: 7-64 hex commit; HEAD/@/refs are rejected")
    group.add_argument("--selftest", action="store_true", help="hermetic fixture suite")
    parser.add_argument("--paths", nargs="+", metavar="PATH",
                        default=["corpus/knowledge"],
                        help="knowledge files or directories; directories expand to "
                             "their *.md members (default: corpus/knowledge)")
    parser.add_argument("--exec-log", metavar="PATH", default=None,
                        help="lane-relative log of executed commands (`$ cmd` lines) to "
                             "check against --forbid at the revision")
    parser.add_argument("--branch", default="master", metavar="BRANCH",
                        help="branch the revision must be landed on (default: master); "
                             "validated by tools/_revision.py")
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
        try:
            binding = _revision.bind(repo, args.revision, branch)
        except _revision.RevisionError as exc:
            tip = _revision.branch_tip(repo, branch)
            raise Cannot(exc.fid, exc.site, exc.detail) from exc
        sha, tip, origin_tip = binding.sha, binding.branch_tip, binding.origin_tip
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
    exec_findings, exec_hits = [], 0
    if args.exec_log is not None:
        try:
            raw = read_git(repo, sha, clean_path(args.exec_log))
            if raw is None:
                raise Cannot("E-PATH-MISSING", args.exec_log, "exec log absent at revision")
            exec_findings, exec_hits = assess_exec_log(args.exec_log,
                                                       decode(raw, args.exec_log), forbid)
        except Cannot as exc:
            return emit("CANNOT_EVALUATE", sha, branch, tip,
                        [Finding(exc.fid, exc.site, exc.detail)], None, out,
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
    code = FAIL if exec_findings else result.code
    status = {PASS: "PASS", FAIL: "FAIL"}[code]
    extra = {"exec_violation_count": exec_hits} if args.exec_log is not None else None
    return emit(status, sha, branch, tip, result.findings + exec_findings, result.counts,
                out, origin_tip=origin_tip, extra=extra)


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

# Round-17 closure defect 6, verbatim: aur-risk-plane.md:347 defers to "§7's ...
# probe set" without a backtick span, and its §7 holds `pacman -T` (:309).
AUR_347 = ("recheck: 90d; procedure: §7's explicit foreign-package, repo-resolution, "
           "orphan and provenance probe set.")
AUR_SECTIONS = (
    "\n## 6. Operator probes (read-only; the ones that would settle the remaining "
    "questions)\n\n"
    "```bash\n"
    "# 1. re-take the census and diff it against this register (16 rows expected)\n"
    "pacman -Qm | awk '{print $1}' | sort > /tmp/fp.txt; wc -l < /tmp/fp.txt\n"
    "```\n\n"
    "## 7. Unknowns and out-of-reach (reported, not absorbed)\n\n"
    "6. **Whether `walker`-adjacent breakage could be caught earlier**: `pacman -T` (R11) "
    "is rc=0 and\n"
    "   will stay rc=0 across an ABI change.\n\n"
    "## 8. Forward spec — what this register implies for the census\n\n"
    "Written, not implemented.\n")

# Modeled on the round-18 NoticeAur draft for aur-risk-plane.md: its prose names
# "§6 and §7", but every command it declares is a file read.
R18_AUR_SECTION = (
    "\n## R18-RECHECK — steer-safe procedure\n\n"
    "Appended by the round-18 build; earlier bytes unchanged. Supersedes the recheck: "
    "line at :347 (its pointer to the §6 and §7 probe set) for any round whose steer "
    "forbids running pacman. Read-only.\n\n"
    "Procedure (file reads only):\n\n"
    "- `ls -1 /var/lib/pacman/local` — installed census by directory name.\n"
    "- `tar -tf /var/lib/pacman/sync/omarchy.db | grep -E \"^(elephant|omarchy-walker)\"`\n"
    "- `git -C ~/.cache/yay/<pkg> log -1 --format='%H %cI %s'` — AUR clone head.\n")

R18_SAFE = SAFE_SECTION.replace("## R17-RECHECK", "## R18-RECHECK")
R18_UNSAFE = "\n## R18-RECHECK — steer-safe procedure\n\n- `paru -Qua`\n"
R18_POINTER = ("\n## R18-RECHECK — steer-safe procedure\n\n"
               "procedure: rerun the §7 probes read-only.\n")
R18_DANGLING = ("\n## R18-RECHECK — steer-safe procedure\n\n"
                "- procedure: `grep -n y /etc/y`, then rerun §9.\n")

# corpus/knowledge/package-state-plane.md:328 and its round-17 section (:331-337),
# verbatim: the prose names "Appendix probes" but declares no pointer procedure.
PACKAGE_STATE_HEADER = (
    "recheck: 90d; procedure: `pacman -Q pacman; pacman --version; uname -r` for header "
    "pins plus the Appendix probe set.")
PACKAGE_STATE_SECTION = (
    "\n## R17-RECHECK — steer-safe procedure\n\n"
    "Appended 2026-10-20 by the tsukuroi round-17 L1; earlier bytes unchanged. Supersedes "
    "the package-manager invocations in this file's `recheck:` line for any round whose "
    "steer forbids running pacman (QUALITY 26); file reads replace them and the "
    "substitution is recorded in that round's report. Read-only.\n\n"
    "- `ls -d /var/lib/pacman/local/pacman-[0-9]*` (version is the directory-name suffix)\n"
    "- `uname -r`\n"
    "- Appendix probes that invoke pacman are replaced by reads of "
    "`/var/lib/pacman/local/<pkg>-<ver>/desc` and `/var/log/pacman.log`, or recorded as "
    "[unk]\n")


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
        findings = payload.get("findings", [])
        got_ids = {item["id"] for item in findings}
        if got_ids != set(want_ids):
            problems.append("ids=" + ",".join(sorted(got_ids))
                            + " want=" + ",".join(sorted(want_ids)))
        if want_code == CANNOT and len(findings) != 1:
            problems.append(f"finding_count={len(findings)}/1")
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
    # 12b. Pointer procedures (round-17 closure defect 6): a named same-file
    #      section pointer is followed and the section's commands are inspected.
    aur = sandbox_commit(repo, entry(AUR_347, AUR_SECTIONS))
    case(repo, "pointer-aur-347-red", ["--revision", aur, "--paths", "fixture.md"],
         FAIL, {"RECHECK-POINTER-UNRESOLVED"}, {"flagged_count": 0, "resolved_count": 0,
                                              "invocation_count": 0, "pointer_section_count": 1})
    aur_fixed = sandbox_commit(repo, entry(AUR_347, AUR_SECTIONS + R18_AUR_SECTION))
    case(repo, "pointer-aur-347-r18-resolved",
         ["--revision", aur_fixed, "--paths", "fixture.md"],
         PASS, set(), {"flagged_count": 0, "resolved_count": 1,
                       "invocation_count": 0, "pointer_section_count": 1})
    aur_no_incidental = sandbox_commit(repo, entry(
        AUR_347, AUR_SECTIONS.replace("`pacman -T`", "the recorded dependency query")))
    case(repo, "pointer-aur-remains-red-without-incidental-T",
         ["--revision", aur_no_incidental, "--paths", "fixture.md"],
         FAIL, {"RECHECK-POINTER-UNRESOLVED"}, {"resolved_count": 0, "clean_count": 0})
    aur_actual = sandbox_commit(repo, entry(AUR_347.replace("§7", "§6"), AUR_SECTIONS))
    case(repo, "pointer-aur-actual-probe-section-forbidden",
         ["--revision", aur_actual, "--paths", "fixture.md"],
         FAIL, forbidden_only, {"flagged_count": 1, "pointer_section_count": 1})
    bounded = sandbox_commit(repo, entry(
        "recheck: 30d; procedure: §2 read-only replay.",
        "\n## 1. Scope\n\n`pacman -Qm` was the census.\n\n"
        "## 2. Replay\n\nNever run pacman -Qm here.\n\n```bash\ngrep -n x /etc/x\n```\n\n"
        "## 3. Later\n\n- `checkupdates`\n"))
    case(repo, "pointer-section-bounded-clean",
         ["--revision", bounded, "--paths", "fixture.md"],
         PASS, set(), {"clean_count": 1, "invocation_count": 0, "pointer_section_count": 1})
    fenced = sandbox_commit(repo, entry(
        "recheck: 30d; procedure: §6 probes.",
        "\n## 6. Probes\n\n```bash\n# 1. first\ngrep a b\n# 2. second\npacman -Qm\n```\n\n"
        "## 7. Unknowns\n\nNone.\n"))
    case(repo, "pointer-fence-comment-not-heading",
         ["--revision", fenced, "--paths", "fixture.md"],
         FAIL, forbidden_only, {"invocation_count": 1, "pointer_section_count": 1})
    ranged = sandbox_commit(repo, entry(
        "recheck: 30d; procedure: §§1–3 rerun the probes.",
        "\n## 1. A\n\n- `grep a b`\n\n## 2. B\n\n- `yay -Qua`\n\n## 3. C\n\n- `grep c d`\n\n"
        "## 4. D\n\n- `paru -Qu`\n"))
    case(repo, "pointer-range", ["--revision", ranged, "--paths", "fixture.md"],
         FAIL, forbidden_only, {"invocation_count": 1, "pointer_section_count": 3})
    subsection = sandbox_commit(repo, entry(
        "recheck: 30d; procedure: §4 probe ledger.",
        "\n## 4. Ledger\n\nIntro.\n\n### 4.1 Detail\n\n- `sudo mkinitcpio -P`\n\n"
        "## 5. Next\n\nNone.\n"))
    case(repo, "pointer-subsection-included",
         ["--revision", subsection, "--paths", "fixture.md"],
         FAIL, forbidden_only, {"invocation_count": 1})
    dotted = sandbox_commit(repo, entry(
        "recheck: 30d; procedure: §4.2 one-liner.",
        "\n## 4. Ledger\n\n### 4.1 Detail\n\n- `pacman -Qi x`\n\n"
        "### 4.2 One-liner\n\n- `grep -c x /etc/x`\n\n## 5. Next\n\nNone.\n"))
    case(repo, "pointer-dotted-only", ["--revision", dotted, "--paths", "fixture.md"],
         PASS, set(), {"invocation_count": 0, "pointer_section_count": 1})
    descendant = sandbox_commit(repo, entry(
        "recheck: 30d; procedure: §0 anchor.",
        "\n## 0. Anchor\n\n- `grep a b`\n\n## 0.1 Matrix\n\n- `checkupdates`\n\n"
        "## 1. Next\n\nNone.\n"))
    case(repo, "pointer-dotted-descendant",
         ["--revision", descendant, "--paths", "fixture.md"],
         FAIL, forbidden_only, {"invocation_count": 1})
    appendix = sandbox_commit(repo, entry(
        "recheck: 30d; procedure: Appendix probe command set.",
        "\n## Appendix — probe command set (reproducible)\n\n```\nlimine-update\n```\n"))
    case(repo, "pointer-appendix", ["--revision", appendix, "--paths", "fixture.md"],
         FAIL, forbidden_only, {"invocation_count": 1, "pointer_section_count": 1})
    lettered = sandbox_commit(repo, entry(
        "recheck: 30d; procedure: Appendix A command set.",
        "\n## Appendix A — executor re-run set\n\n```bash\n"
        "bash tools/tsukuroi-census.sh --selftest\n```\n\n"
        "## Appendix B — scratch inventory\n\n- `pacman -Qkk`\n"))
    case(repo, "pointer-appendix-letter", ["--revision", lettered, "--paths", "fixture.md"],
         PASS, set(), {"invocation_count": 0, "pointer_section_count": 1})
    numbered = sandbox_commit(repo, entry(
        "recheck: 30d; procedure: §10 command set; Appendix probes.",
        "\n## 10. Appendix — probe command set\n\n```bash\nsystemctl list-timers --all\n```\n"))
    case(repo, "pointer-numbered-appendix-once",
         ["--revision", numbered, "--paths", "fixture.md"],
         PASS, set(), {"clean_count": 1, "pointer_section_count": 1})
    other_file = sandbox_commit(repo, entry(
        "recheck: 90d; procedure: confirm the notices still resolve in "
        "`corpus/knowledge/other.md` §0 and `notes.md`'s §5."))
    case(repo, "pointer-other-file-not-followed",
         ["--revision", other_file, "--paths", "fixture.md"],
         PASS, set(), {"clean_count": 1, "pointer_section_count": 0})
    unresolved = sandbox_commit(repo, entry("recheck: 90d; procedure: §9 probe set."))
    case(repo, "pointer-unresolved", ["--revision", unresolved, "--paths", "fixture.md"],
         FAIL, {"RECHECK-POINTER-UNRESOLVED"}, {"flagged_count": 0, "clean_count": 0})
    spanned = sandbox_commit(repo, entry("recheck: daily; procedure: "
                                         "`grep -n '§3' notes.txt`."))
    case(repo, "pointer-in-span-not-followed",
         ["--revision", spanned, "--paths", "fixture.md"],
         PASS, set(), {"clean_count": 1, "pointer_section_count": 0})
    commented = sandbox_commit(repo, entry(
        "recheck: 30d; procedure: Appendix A plus "
        "`bash tools/tsukuroi-census.sh --selftest`.",
        "\n## Appendix A — executor re-run set (read-only, no elevation)\n\n```bash\n"
        "bsdtar -tf /var/lib/pacman/sync/offline.db | grep -c '^elephant'   # [offline] has "
        "no pacman.conf section — query the db file directly, `pacman -Sl offline` returns 0\n"
        "grep -c x /etc/x  # never; pacman -Qm\n```\n"))
    case(repo, "pointer-shell-comment-not-invocation",
         ["--revision", commented, "--paths", "fixture.md"],
         PASS, set(), {"clean_count": 1, "invocation_count": 0, "pointer_section_count": 1})
    trailing = sandbox_commit(repo, entry(
        "recheck: 30d; procedure: Appendix A.",
        "\n## Appendix A — executor re-run set\n\n```bash\n"
        "pacman -Qm | wc -l   # 16; `ls` is the safe form\n"
        "echo issue#12; pacman -Qi x\n```\n"))
    case(repo, "pointer-command-before-comment",
         ["--revision", trailing, "--paths", "fixture.md"],
         FAIL, forbidden_only, {"invocation_count": 2, "pointer_section_count": 1})
    package_state = sandbox_commit(repo, entry(PACKAGE_STATE_HEADER, PACKAGE_STATE_SECTION))
    case(repo, "landed-r17-package-state",
         ["--revision", package_state, "--paths", "fixture.md"],
         PASS, set(), {"resolved_count": 1, "invocation_count": 2,
                       "pointer_section_count": 0})
    package_appendix = sandbox_commit(repo, entry(
        PACKAGE_STATE_HEADER,
        "\n## Appendix — probe set\n\n```\npacman -Qkk\n```\n" + PACKAGE_STATE_SECTION))
    case(repo, "pointer-resolved-by-r17",
         ["--revision", package_appendix, "--paths", "fixture.md"],
         PASS, set(), {"resolved_count": 1, "invocation_count": 3,
                       "pointer_section_count": 1})
    # 12c. An R18 section resolves like an R17 one and, when both are present, the
    #      R18 section is operative (append-only repair of an R17 section).
    r18_only = sandbox_commit(repo, entry(BASELINE_HEADER, R18_SAFE))
    case(repo, "r18-resolves-literal", ["--revision", r18_only, "--paths", "fixture.md"],
         PASS, set(), {"resolved_count": 1, "invocation_count": 1})
    r18_over = sandbox_commit(repo, entry(BASELINE_HEADER, UNSAFE_SECTION + R18_SAFE))
    case(repo, "r18-supersedes-unsafe-r17",
         ["--revision", r18_over, "--paths", "fixture.md"],
         PASS, set(), {"flagged_count": 0, "resolved_count": 1})
    r18_bad = sandbox_commit(repo, entry(BASELINE_HEADER, SAFE_SECTION + R18_UNSAFE))
    case(repo, "r18-operative-unsafe", ["--revision", r18_bad, "--paths", "fixture.md"],
         FAIL, forbidden_only | {"RECHECK-STEER-SAFE-INVALID"},
         {"flagged_count": 1, "resolved_count": 0})
    r18_twin = sandbox_commit(repo, entry(BASELINE_HEADER, R18_SAFE + R18_SAFE))
    case(repo, "r18-duplicate-heading", ["--revision", r18_twin, "--paths", "fixture.md"],
         FAIL, forbidden_only | {"RECHECK-STEER-SAFE-INVALID"})
    r18_pointer = sandbox_commit(repo, entry(AUR_347, AUR_SECTIONS + R18_POINTER))
    case(repo, "r18-procedure-pointer-forbidden",
         ["--revision", r18_pointer, "--paths", "fixture.md"],
         FAIL, {"RECHECK-POINTER-UNRESOLVED", "RECHECK-STEER-SAFE-INVALID"},
         {"resolved_count": 0})
    r18_dangling = sandbox_commit(repo, entry(
        "recheck: daily; procedure: `grep -n x /etc/x`.", R18_DANGLING))
    case(repo, "r18-procedure-pointer-unresolved",
         ["--revision", r18_dangling, "--paths", "fixture.md"],
         FAIL, {"RECHECK-STEER-SAFE-INVALID"}, {"clean_count": 0})
    for name, command in (("empty-quote", "''"), ("wrapper-only", "sudo"),
                          ("env-without-command", "env -u HOME"),
                          ("unterminated-quote", "'unterminated")):
        invalid_replacement = sandbox_commit(repo, entry(
            BASELINE_HEADER, "\n## R18-RECHECK — steer-safe procedure\n\n- `" + command + "`\n"))
        case(repo, "r18-invalid-argv0-" + name,
             ["--revision", invalid_replacement, "--paths", "fixture.md"],
             FAIL, forbidden_only | {"RECHECK-STEER-SAFE-INVALID"}, {"resolved_count": 0})
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
    # 14b. Shared binding (tools/_revision.py): branch syntax before revision
    #      syntax, revision syntax before branch existence, one finding each.
    for name, revision, branch, want in (
            ("branch-range", clean, "a..b", "E-BRANCH-INVALID"),
            ("branch-slash", clean, "master/", "E-BRANCH-INVALID"),
            ("branch-space", clean, "bad branch", "E-BRANCH-INVALID"),
            ("branch-first-precedence", "HEAD", "a..b", "E-BRANCH-INVALID"),
            ("revision-before-missing-branch", "HEAD", "nosuch", "E-REVISION-INVALID"),
            ("branch-missing", clean, "nosuch", "E-BRANCH-MISSING"),
            ("branch-nested-missing", clean, "feature/x", "E-BRANCH-MISSING"),
            ("revision-range", f"{first[:8]}..{clean[:8]}", "master", "E-REVISION-INVALID")):
        case(repo, name, ["--revision", revision, "--paths", "fixture.md", "--branch", branch],
             CANNOT, {want})
    case(repo / "absent", "not-a-repo-git-failed",
         ["--revision", clean, "--paths", "fixture.md"], CANNOT, {"E-GIT-FAILED"})
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
         CANNOT, {"E-REVISION-NOT-LANDED"}, {"branch_tip": tip_now})
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
    (repo / "blob.txt").write_text("origin names a blob\n", encoding="utf-8")
    blob = sandbox_git(repo, "hash-object", "-w", "blob.txt").strip()
    (repo / "blob.txt").unlink()
    sandbox_git(repo, "update-ref", "refs/remotes/origin/master", blob)
    case(repo, "origin-blob-git-failed", ["--revision", clean, "--paths", "fixture.md"],
         CANNOT, {"E-GIT-FAILED"})
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
    # 18b. Executed-command log (R17-STEER-SCOPE: the event, not the prose).
    sandbox_git_files = {"fixture.md": entry("recheck: on-release; procedure: "
                                              "`grep -n '^HOOKS' /etc/mkinitcpio.conf`."),
                         "exec.log": "# L1 exec log\n$ uname -r; pacman -Q mkinitcpio plymouth\n"
                                     "$ ls -d /var/lib/pacman/local/mkinitcpio-[0-9]*\n"}
    red_log = sandbox_commit_tree(repo, sandbox_git_files)
    case(repo, "exec-log-pacman-red",
         ["--revision", red_log, "--paths", "fixture.md", "--exec-log", "exec.log"],
         FAIL, {"EXEC-STEER-VIOLATION"}, {"exec_violation_count": 1})

    green_files = dict(sandbox_git_files)
    green_files["exec.log"] = "$ ls -d /var/lib/pacman/local/mkinitcpio-[0-9]*\n"
    green_log = sandbox_commit_tree(repo, green_files)
    case(repo, "exec-log-clean",
         ["--revision", green_log, "--paths", "fixture.md", "--exec-log", "exec.log"],
         PASS, set(), {"exec_violation_count": 0})
    case(repo, "exec-log-missing",
         ["--revision", green_log, "--paths", "fixture.md", "--exec-log", "nope.log"],
         CANNOT, {"E-PATH-MISSING"})

    systemctl_mutations = dict(green_files)
    systemctl_mutations["exec.log"] = (
        "$ systemctl restart example.service\n"
        "$ sudo /usr/bin/systemctl enable example.service\n"
        "$ sh -c 'systemctl daemon-reload'\n"
        "$ echo systemctl list-timers --all; systemctl restart example.service\n"
        "$ printf x | xargs --replace systemctl restart example.service\n"
        "$ time -p systemctl restart example.service\n"
        "$ env -S 'systemctl restart example.service'\n"
        "$ sudo -s 'systemctl restart example.service'\n"
        "$ sudo -i 'systemctl enable example.service'\n"
        "$ sudo bash -lc 'systemctl daemon-reload'\n"
        "$ sudo -Eu root systemctl restart example.service\n"
        "$ exec -a x systemctl restart example.service\n"
        "$ env -S systemctl restart example.service\n")
    systemctl_red = sandbox_commit_tree(repo, systemctl_mutations)
    case(repo, "exec-log-systemctl-mutations-red",
         ["--revision", systemctl_red, "--paths", "fixture.md", "--exec-log", "exec.log"],
         FAIL, {"EXEC-STEER-VIOLATION"}, {"exec_violation_count": 13})
    total += 1
    if systemctl_violations("busybox echo -c 'systemctl daemon-reload'"):
        failures.append("systemctl-busybox-echo: false nested mutation hit")
    total += 1
    if systemctl_violations("busybox sh -c 'systemctl daemon-reload'") != ["systemctl"]:
        failures.append("systemctl-busybox-sh: missed nested mutation")
    total += 1
    if invocations("busybox echo -c 'forbidden'", {"forbidden"}):
        failures.append("invocations-busybox-echo: false nested forbidden hit")
    total += 1
    if invocations("busybox sh -c 'forbidden'", {"forbidden"}) != ["forbidden"]:
        failures.append("invocations-busybox-sh: missed nested forbidden")
    total += 1
    if systemctl_violations("busybox systemctl restart example.service") != ["systemctl"]:
        failures.append("systemctl-busybox-applet: missed mutation")

    systemctl_reads = dict(green_files)
    systemctl_reads["exec.log"] = (
        "$ /usr/bin/systemctl --user --no-pager status example.service\n"
        "$ sudo -u root env SYSTEMD_COLORS=0 /usr/bin/systemctl --system --host=local "
        "--machine=container --root=/mnt --image=/image --runtime "
        "show --property=Id example.service\n"
        "$ env -u TEMP systemctl --host local is-active example.service\n"
        "$ systemctl --user --failed --no-pager\n"
        "$ systemctl --failed --no-legend | wc -l\n"
        "$ systemctl is-system-running --wait\n"
        "$ systemctl list-unit-files --type=timer --no-pager\n"
        "$ systemctl list-units --state=failed --all --no-pager\n"
        "$ echo systemctl restart example.service; systemctl list-timers --all\n"
        "$ systemctl --user cat example.service\n"
        "$ systemctl --user show example.service\n"
        "$ systemctl --user list-timers --all\n"
        "$ systemctl --user is-active example.service\n"
        "$ systemctl --user is-enabled example.service\n"
        "$ systemctl list-dependencies --reverse --no-pager limine-snapper-sync.service\n"
        "$ sudo --user root systemctl --user cat example.service\n"
        "$ sudo -Eu root -T 30 -R /mnt systemctl --user is-active example.service\n"
        "$ sudo --command-timeout 30 --chroot /mnt systemctl --user show example.service\n"
        "$ env --unset HOME systemctl --user show example.service\n"
        "$ env -S 'systemctl --user is-active example.service'\n"
        "$ timeout --signal TERM 2s systemctl --user is-active example.service\n"
        "$ timeout -vs TERM 2s systemctl --user status example.service\n"
        "$ systemctl --runtime show example.service\n"
        "$ time -p systemctl --user list-units --all\n"
        "$ sudo -s 'systemctl --user list-units'\n"
        "$ sudo -i 'systemctl --user list-timers --all'\n"
        "$ sudo bash -lc 'systemctl --user show example.service'\n"
        "$ exec -a x systemctl --user cat example.service\n")
    systemctl_green = sandbox_commit_tree(repo, systemctl_reads)
    case(repo, "exec-log-systemctl-read-controls",
         ["--revision", systemctl_green, "--paths", "fixture.md", "--exec-log", "exec.log"],
         PASS, set(), {"exec_violation_count": 0})
    case(repo, "exec-log-systemctl-explicit-generic-forbid",
         ["--revision", systemctl_green, "--paths", "fixture.md", "--exec-log", "exec.log",
          "--forbid", "systemctl"],
         FAIL, {"EXEC-STEER-VIOLATION"}, {"exec_violation_count": 28})

    systemctl_ambiguous = dict(green_files)
    systemctl_ambiguous["exec.log"] = (
        "$ systemctl --user --system status example.service\n"
        "$ systemctl --force status example.service\n"
        "$ systemctl status --now example.service\n"
        "$ systemctl status --property --force\n"
        "$ systemctl frobnicate example.service\n"
        "$ systemctl --runtime restart show example.service\n"
        "$ systemctl --user restart example.service\n"
        "$ systemctl --user enable example.service\n"
        "$ systemctl --user frobnicate example.service\n"
        "$ systemctl --user enable --now example.service\n"
        "$ systemctl kill example.service\n"
        "$ systemctl set-property example.service RuntimeMaxSec=5\n"
        "$ systemctl --user '' restart example.service\n")
    ambiguous_systemctl = sandbox_commit_tree(repo, systemctl_ambiguous)
    case(repo, "exec-log-systemctl-ambiguous-or-effectful-options",
         ["--revision", ambiguous_systemctl, "--paths", "fixture.md",
          "--exec-log", "exec.log"],
         FAIL, {"EXEC-STEER-VIOLATION"}, {"exec_violation_count": 13})



    # 19. CLI shape.
    case(repo, "cli-no-mode", [], CANNOT, {"E-CLI"})
    case(repo, "cli-both-modes", ["--selftest", "--revision", clean], CANNOT, {"E-CLI"})
    case(repo, "cli-bogus-flag", ["--revision", clean, "--bogus"], CANNOT, {"E-CLI"})
    case(repo, "cli-branch-without-value", ["--revision", clean, "--branch"],
         CANNOT, {"E-CLI"})
    case(repo, "cli-dash-branch", ["--revision", clean, "--branch", "-x"], CANNOT, {"E-CLI"})
    case(repo, "cli-forbid-before-binding",
         ["--revision", "HEAD", "--branch", "a..b", "--forbid", "bad name!"],
         CANNOT, {"E-CLI"})

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
