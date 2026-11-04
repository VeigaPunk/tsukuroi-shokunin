#!/usr/bin/env python3
"""Round-73 E3HostProbe attack on the frozen C1 counter (count-ul-rows-r73.py).

QUALITY 81 shape: a scripted writer that never reads the source. It copies a verbatim
byte slice of the pinned snapshot into one row's statement cell and keeps every other
cell as the counter's own fixture already had it. No one reads `systemd.unit.xml`; the
text is sliced mechanically.

Run:  TMPDIR=<a non-/tmp dir> python3 attack-c1-scripted-writer.py
rc 0 = the counter credited the copied row (attack survived);
rc 1 = the counter refused it (attack held);
rc 2 = $TMPDIR unusable.
"""
import importlib.util
import io
import os
import pathlib
import re
import shutil
import sys
import tempfile

COUNTER = "tools/count-ul-rows-r73.py"


def load():
    spec = importlib.util.spec_from_file_location("c1", COUNTER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    tmp = os.environ.get("TMPDIR")
    if not tmp or not pathlib.Path(tmp).is_dir():
        print("ATTACK: cannot evaluate, TMPDIR names no directory", file=sys.stderr)
        return 2
    m = load()
    root = pathlib.Path(tempfile.mkdtemp(prefix="c1-scripted-writer-", dir=tmp))
    m.build_fixture(root)

    # Mechanical slice: no reading, just find the phrase and cut 430 characters.
    snap = " ".join((root / m.SNAPDIR / "systemd.unit.xml").read_text().split())
    start = snap.find("Unit files found")
    sentence = snap[start:start + 430]
    print("COPIED STATEMENT:", sentence)

    note = root / m.NOTE
    out = []
    for line in note.read_text().splitlines():
        if line.startswith("| UL1 |"):
            line = re.sub(r"^\| UL1 \| .*?(?= \| source=)",
                          lambda _m: "| UL1 | " + sentence, line, count=1)
        out.append(line)
    note.write_text("\n".join(out) + "\n")

    buf = io.StringIO()
    rc = m.evaluate(*m.readers("HEAD", str(root)), out=buf)
    text = buf.getvalue()
    print(text)
    print("counter rc =", rc)
    met = "met=1" in text and rc == 0
    shutil.rmtree(root, ignore_errors=True)
    if met:
        print("ATTACK: survived — a mechanically copied snapshot slice is credited as a UL row")
        return 0
    print("ATTACK: held")
    return 1


if __name__ == "__main__":
    sys.exit(main())
