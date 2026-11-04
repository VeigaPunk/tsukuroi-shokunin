#!/usr/bin/env python3
"""C1 counter, round 82 — a knowledge row's quote must sit inside the raw lines it cites.

Round 81 cited every `MT` row (and S331's anchor cell) in *tag-stripped* coordinates:
the strip dropped the DOCTYPE and one `<ulink>` newline, so the whole file shifted by
two lines and every anchor pointed two lines early.  The repair is the per-line strip:
one output line per raw line, tags removed *within* the line, so a cited number is a
raw file number and no reader has to know a strip rule.

What this instrument decides, and nothing more:

  * for each row of the entry JSON: the row's `quote`, whitespace-normalised and
    entity-decoded, occurs in the line-preserving strip of the pinned snapshot
    (line i of the strip == line i of the raw file), and the row's cited `lines`
    range IS the quote's own raw span — `[a, b]` where the quote starts at `a`
    and ends at `b`;
  * count = rows whose cited range is the located span exactly; target = every row.

Exactness is the anchor rule, not a stricter reading of a loose one: a range that
merely contains the quote hides the shift this counter exists to catch (round 81
cited stripped coordinates two lines early and six of eight ranges still
contained their quote).

It does not decide that a quote supports its statement, that the snapshot is the
right upstream revision, or that a row's prose is true.

  --revision REV   read the entry and the snapshot at a landed lane revision
  --fixture DIR    read the same repo-relative paths beneath DIR (hermetic selftest)
  --selftest       hermetic case suite over a temporary tree; writes nothing outside it

Exit: 0 met / 1 unmet / 2 could-not-evaluate / 3 selftest failed.
"""
from __future__ import annotations

import argparse
import bisect
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

ENTRY = "corpus/knowledge/mount-unit-fstab-plane-r81.json"
SNAPDIR = ".ufo/waves/round-81/before/src"
TARGET_ROWS = 8
CLAIM = "C1"
TAG = re.compile(r"<[^>]*>")
WINDOW = 40  # max lines a located quote may span


class CannotEvaluate(Exception):
    """Inputs are absent or unusable: this is not a verdict."""


def norm(text):
    """Entity-decode and collapse whitespace: the only normalisation used both sides."""
    return " ".join(html.unescape(str(text)).split())


def strip_line(line):
    """Per-line strip: tags removed inside the line, one output line per raw line."""
    return norm(TAG.sub("", line))


def strip_view(raw):
    """Line-preserving view: index i is raw line i+1, including tag-only lines."""
    return [strip_line(line) for line in raw.splitlines()]


def word_index(view):
    """Flatten the strip to a word list that remembers each word's raw line."""
    words, lines = [], []
    for index, line in enumerate(view):
        for word in line.split():
            words.append(word)
            lines.append(index + 1)
    return words, lines


def locate(view, quote):
    """(first, last) 1-based line span of `quote` in `view`, or None.

    Substring semantics over the whitespace-normalised word stream, so a quote that
    ends where the source keeps going ("... among nofail" inside "among nofail, x")
    still locates, and the span is the quote's own extent, never a window that merely
    contains it.
    """
    want = norm(quote)
    if not want:
        return None
    words, lines = word_index(view)
    text = " ".join(words)
    pos = text.find(want)
    if pos < 0:
        return None
    starts, off = [], 0
    for word in words:
        starts.append(off)
        off += len(word) + 1
    first = bisect.bisect_right(starts, pos) - 1
    last = bisect.bisect_right(starts, pos + len(want) - 1) - 1
    return lines[first], lines[last]


def load(root, revision=None):
    """(entry dict, snapshot text) from a fixture dir or a landed revision."""
    if revision is not None:
        def read(path):
            proc = subprocess.run(
                ["git", "--no-pager", "-C", str(root), "show", f"{revision}:{path}"],
                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, timeout=120,
            )
            if proc.returncode != 0:
                raise CannotEvaluate(f"absent-at-revision:{path}")
            return proc.stdout
        entry_bytes = read(ENTRY)
        entry = json.loads(entry_bytes.decode("utf-8", "replace"))
        snapshot = entry.get("snapshot") if isinstance(entry, dict) else None
        if not isinstance(snapshot, str) or not snapshot:
            raise CannotEvaluate("snapshot-unnamed")
        return entry, read(f"{SNAPDIR}/{snapshot}").decode("utf-8", "replace")

    base = Path(root)
    path = base / ENTRY
    if not path.is_file():
        raise CannotEvaluate("entry-absent")
    try:
        entry = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except ValueError as exc:
        raise CannotEvaluate(f"entry-unreadable:{exc}"[:120])
    snapshot = entry.get("snapshot") if isinstance(entry, dict) else None
    if not isinstance(snapshot, str) or not snapshot:
        raise CannotEvaluate("snapshot-unnamed")
    snap = base / SNAPDIR / snapshot
    if not snap.is_file():
        raise CannotEvaluate(f"snapshot-absent:{snapshot}")
    return entry, snap.read_text(encoding="utf-8", errors="replace")


def measure(root, revision=None, target=TARGET_ROWS):
    """Return (count, rows, finding). Raises CannotEvaluate."""
    entry, raw = load(root, revision)
    rows = entry.get("rows") if isinstance(entry, dict) else None
    if not isinstance(rows, list) or not rows:
        raise CannotEvaluate("rows-absent")
    view = strip_view(raw)
    out, count = [], 0
    for row in rows:
        span = row.get("lines") if isinstance(row, dict) else None
        quote = row.get("quote") if isinstance(row, dict) else None
        rid = row.get("id") if isinstance(row, dict) else None
        if not (isinstance(span, list) and len(span) == 2
                and all(isinstance(v, int) for v in span)):
            out.append({"id": rid, "cited": span, "located": None, "exact": False,
                        "why": "cited-range-malformed"})
            continue
        found = locate(view, quote if isinstance(quote, str) else "")
        exact = bool(found and (found[0], found[1]) == (span[0], span[1]))
        count += int(exact)
        out.append({"id": rid, "cited": span, "located": found, "exact": exact,
                    "why": "ok" if exact else ("quote-not-located" if not found
                                               else "cited-range-not-the-quote-span")})
    finding = "met" if count == target and len(rows) == target else "unmet"
    return count, out, finding


XML = (
    '<?xml version="1.0"?>\n'
    '<refentry>\n'
    '<para>Alpha <literal>beta</literal> gamma\n'
    'delta epsilon</para>\n'
    '</refentry>\n'
)
XML_TAGONLY = (
    '<refentry>\n'
    '<para>\n'
    'one two three\n'
    '</para>\n'
    '</refentry>\n'
)
XML_ENTITY = (
    '<refentry>\n'
    '<para>A &lt; B and\n'
    'C &gt; D</para>\n'
    '</refentry>\n'
)


def entry(rows, snapshot="systemd.mount.xml"):
    return {"snapshot": snapshot, "rows": rows}


def row(rid, lines, quote):
    return {"id": rid, "lines": lines, "quote": quote}


def selftest():
    cases = []

    def case(name, files, want_rc, want_count):
        """files: {repo-relative path: bytes/str}; want_rc -1 means cannot-evaluate."""
        with tempfile.TemporaryDirectory(prefix="anchor-selftest-") as tmp:
            root = Path(tmp)
            for rel, body in files.items():
                dest = root / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(body, encoding="utf-8")
            try:
                want = TARGET_ROWS
                try:
                    rows_in = json.loads((root / ENTRY).read_text(encoding="utf-8")).get("rows")
                    if isinstance(rows_in, list) and rows_in:
                        want = len(rows_in)
                except (OSError, ValueError):
                    pass
                count, rows, finding = measure(root, target=want)
                rc = 0 if finding == "met" else 1
                observed = f"rc={rc} count={count}/{want} {finding}"
            except CannotEvaluate as exc:
                rc, count, rows, observed = 2, None, [], f"rc=2 could-not-evaluate {exc}"
            ok = (rc == 2) if want_rc == -1 else (rc == want_rc and count == want_count)
            cases.append((name, ok, observed))

    snap = {f"{SNAPDIR}/systemd.mount.xml": XML}
    # 1. quote split by a tag across lines 3-4, cited [3,4] -> met.
    case("correct-span", {**snap, ENTRY: json.dumps(entry([row("MT1", [3, 4], "Alpha beta gamma delta epsilon")]))}, 0, 1)
    # 2. same quote cited two lines early: the round-81 defect class -> unmet.
    case("shifted-two-lines", {**snap, ENTRY: json.dumps(entry([row("MT1", [1, 2], "Alpha beta gamma delta epsilon")]))}, 1, 0)
    # 3. fabricated quote -> unmet, not a crash.
    case("fabricated-quote", {**snap, ENTRY: json.dumps(entry([row("MT1", [3, 4], "Omega psi chi")]))}, 1, 0)
    # 4. cited range ends one line short of the quote -> unmet.
    case("range-too-short", {**snap, ENTRY: json.dumps(entry([row("MT1", [3, 3], "Alpha beta gamma delta epsilon")]))}, 1, 0)
    # 5. a tag-only line keeps its index: quote on raw line 3, not 2.
    case("tag-only-line-keeps-index",
         {f"{SNAPDIR}/systemd.mount.xml": XML_TAGONLY,
          ENTRY: json.dumps(entry([row("MT1", [3, 3], "one two three")]))}, 0, 1)
    # 6. entity-decoded quote matches the raw file -> met.
    case("entity-decode",
         {f"{SNAPDIR}/systemd.mount.xml": XML_ENTITY,
          ENTRY: json.dumps(entry([row("MT1", [2, 3], "A < B and C > D")]))}, 0, 1)
    # 7. quote ends where the source continues: substring semantics, not word equality.
    case("quote-ends-mid-list",
         {f"{SNAPDIR}/systemd.mount.xml": "<para>options among nofail, x</para>\n",
          ENTRY: json.dumps(entry([row("MT1", [1, 1], "options among nofail")]))}, 0, 1)
    # 8. a range wider than the quote is not the quote's span -> unmet.
    case("range-too-wide", {**snap, ENTRY: json.dumps(entry([row("MT1", [3, 5], "Alpha beta gamma delta epsilon")]))}, 1, 0)
    # 9. absent entry -> could-not-evaluate.
    case("entry-absent", snap, -1, None)
    # 8. empty row list -> could-not-evaluate.
    case("rows-empty", {**snap, ENTRY: json.dumps(entry([]))}, -1, None)
    # 9. unnamed snapshot -> could-not-evaluate.
    case("snapshot-unnamed", {**snap, ENTRY: json.dumps({"rows": [row("MT1", [3, 4], "x")]})}, -1, None)
    # 10. malformed cited range is a row finding, never a silent pass.
    case("cited-range-malformed",
         {**snap, ENTRY: json.dumps(entry([{"id": "MT1", "lines": "3-4", "quote": "Alpha beta"}]))}, 1, 0)

    failed = [c for c in cases if not c[1]]
    for name, ok, observed in cases:
        print(f"  {'ok  ' if ok else 'FAIL'} {name}: {observed}")
    print(f"SELFTEST total={len(cases)} passed={len(cases) - len(failed)} failed={len(failed)}")
    return 0 if not failed else 3


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--revision")
    group.add_argument("--fixture", type=Path)
    group.add_argument("--selftest", action="store_true")
    p.add_argument("--repo", default=".")
    p.add_argument("--branch", default="master")
    a = p.parse_args(argv)

    if a.selftest:
        return selftest()

    repo = Path(a.repo).resolve()
    revision = None
    if a.revision:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import _revision  # noqa: E402  (shared landed-revision binding, QUALITY 27)
        try:
            revision = _revision.bind(repo, a.revision, a.branch).sha
        except _revision.RevisionError as exc:
            print(json.dumps({"claim": CLAIM, "revision": a.revision,
                              "finding": "cannot-evaluate", "problems": [str(exc)]}))
            return 2

    try:
        count, rows, finding = measure(a.fixture if a.fixture else repo, revision)
    except CannotEvaluate as exc:
        print(json.dumps({"claim": CLAIM, "revision": revision, "count": 0,
                          "target": TARGET_ROWS, "finding": "cannot-evaluate",
                          "problems": [str(exc)]}))
        return 2

    print(json.dumps({"claim": CLAIM, "revision": revision, "count": count,
                      "target": TARGET_ROWS, "finding": finding, "rows": rows}))
    return 0 if finding == "met" else 1


if __name__ == "__main__":
    raise SystemExit(main())
