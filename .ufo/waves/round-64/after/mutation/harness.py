#!/usr/bin/env python3
"""MT1Guard mutation harness v2 — tools/check-line-endings-r64.py.

Self-contained: snapshots the repo file ONCE at start (hash recorded), never writes it.
All mutants + fixtures + detectors live in this scratch dir.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
REPO = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
SRC = os.path.join(REPO, "tools/check-line-endings-r64.py")

WORK = os.path.join(S, "work")
BIN = os.path.join(S, "bin")
F_D = os.path.join(S, "fixtures/dirty")
F_C = os.path.join(S, "fixtures/clean")
MUT = os.path.join(S, "mut")

TRACKED = [
    "corpus/ok.md", "corpus/bad.md", "plans/ok.md", "plans/eof.md",
    "tools/good.py", "tools/bad.py", "SKILL.md",
    ".ufo/waves/cap.txt", "docs/notes.txt",
]

DIRTY = {
    "corpus/ok.md": b"alpha\nbeta\n",
    "corpus/bad.md": b"alpha\r\nbeta\r\n",
    "plans/ok.md": b"one\ntwo\n",
    "plans/eof.md": b"alpha\nbeta\r",
    "tools/good.py": b"x = 1\n",
    "tools/bad.py": b"x = 1\r\n",
    "SKILL.md": b"# skill\n",
    ".ufo/waves/cap.txt": b"HTTP/1.1 200 OK\r\nServer: x\r\n",
    "docs/notes.txt": b"untracked-class\r\n",
}
CLEAN = dict(DIRTY)
CLEAN.update({
    "corpus/bad.md": b"alpha\nbeta\n",
    "plans/eof.md": b"alpha\nbeta\n",
    "tools/bad.py": b"x = 1\n",
})


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def write_tree(root, layout):
    if os.path.isdir(root):
        shutil.rmtree(root)
    for rel, payload in layout.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(payload)


def run(tool, args, tag):
    env = dict(os.environ)
    env["PATH"] = BIN + ":" + env.get("PATH", "")
    env["SHIM_LS"] = os.path.join(S, "tracked-%s.txt" % tag)
    cmd = [sys.executable, tool] + args
    p = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=S)
    return p.returncode, p.stdout, p.stderr


DETECTORS = [
    ("D1-selftest", lambda t: run(t, ["--selftest", "--work", WORK], "dirty")),
    ("D2-dirty-default-set", lambda t: run(t, ["--check", "--root", F_D], "dirty")),
    ("D3-clean-exit", lambda t: run(t, ["--check", "--root", F_C], "clean")),
]

MUTANTS = []


def mutant(mid, desc, edits, missing_case):
    MUTANTS.append({"id": mid, "desc": desc, "edits": edits, "missing_case": missing_case})


mutant(
    "M1",
    "allow-all: the CR check never fires (hit forced to None); every file reports clean",
    [("        hit = first_cr(path)\n",
      "        hit = None  # M1 allow-all: the CR check never fires\n")],
    None,
)

mutant(
    "M2",
    "allowlist-inversion: `.ufo/**` is the ONLY guarded set; the real guarded set becomes "
    "the allowlist (guarded/allowlisted swapped)",
    [(
        '''def is_guarded(relpath):
    """True when the repo-relative path belongs to the guarded set."""
    p = relpath.replace(os.sep, "/")
    if p in CANONICAL:
        return True
    if any(p.startswith(prefix) for prefix in GUARDED_DIRS):
        return True
    if p.startswith(TOOLS_PY_PREFIX) and p.endswith(".py"):
        rest = p[len(TOOLS_PY_PREFIX):]
        if rest and "/" not in rest:
            return True
    return False


def is_allowlisted(relpath):
    """True when the path sits under a TOP-LEVEL `.ufo/` directory.

    Anchored to the leading component on purpose: a nested `.ufo` directory further down
    (`corpus/.ufo/…`) does NOT buy the allowlist, because the guarded tree is exactly
    where a stray capture must not hide. See the symlink case in the round-64 review:
    the allowlist is name-based on the tracked path, so a guarded path can never inherit
    a target's `.ufo` shield.
    """
    parts = relpath.replace(os.sep, "/").split("/")
    return bool(parts) and parts[0] == ALLOW_DIR
''',
        '''def is_guarded(relpath):
    """M2: only `.ufo` paths are guarded now."""
    parts = relpath.replace(os.sep, "/").split("/")
    return bool(parts) and parts[0] == ALLOW_DIR


def is_allowlisted(relpath):
    """M2: the old guarded set is the allowlist now."""
    p = relpath.replace(os.sep, "/")
    if p in CANONICAL:
        return True
    if any(p.startswith(prefix) for prefix in GUARDED_DIRS):
        return True
    if p.startswith(TOOLS_PY_PREFIX) and p.endswith(".py"):
        rest = p[len(TOOLS_PY_PREFIX):]
        if rest and "/" not in rest:
            return True
    return False
''',
    )],
    None,
)

mutant(
    "M3",
    "exit-inversion: report() returns 0 on violations and 1 on clean",
    [("    return FAIL if violations else PASS\n\n\n# ---",
      "    return PASS if violations else FAIL  # M3 exit-inversion\n\n\n# ---")],
    "exit-code-contract (no case asserts report()/main() return value)",
)

mutant(
    "M4",
    "cr-at-eof-blindness: a CR that is the file's final byte (no trailing newline) is not reported",
    [("            idx = chunk.find(CR)\n            if idx != -1:\n                return line + chunk.count(LF, 0, idx), offset + idx\n",
      "            idx = chunk.find(CR)\n            if idx != -1:\n"
      "                if idx == len(chunk) - 1 and len(chunk) < 65536:\n"
      "                    return None  # M4 cr-at-eof-blindness\n"
      "                return line + chunk.count(LF, 0, idx), offset + idx\n")],
    None,
)

mutant(
    "M5",
    "guard-set-shrink: tools/*.py dropped from the guarded set",
    [('''    if p.startswith(TOOLS_PY_PREFIX) and p.endswith(".py"):
        rest = p[len(TOOLS_PY_PREFIX):]
        if rest and "/" not in rest:
            return True
''',
      "    # M5 guard-set-shrink: tools/*.py is no longer guarded\n")],
    "tools-python-is-guarded (is_guarded is never exercised: fixtures pass explicit paths)",
)


def main():
    for d in (MUT, BIN, WORK):
        os.makedirs(d, exist_ok=True)

    shim = os.path.join(BIN, "git")
    with open(shim, "w", encoding="utf-8") as fh:
        fh.write(
            "#!/usr/bin/env python3\n"
            "import os, sys\n"
            "if 'ls-files' not in sys.argv:\n"
            "    sys.stderr.write('shim git: only ls-files supported\\n'); sys.exit(99)\n"
            "path = os.environ.get('SHIM_LS')\n"
            "if not path:\n"
            "    sys.stderr.write('shim git: SHIM_LS unset\\n'); sys.exit(99)\n"
            "rels = [l for l in open(path, encoding='utf-8').read().split('\\n') if l]\n"
            "sys.stdout.buffer.write(b'\\0'.join(r.encode() for r in rels) + b'\\0')\n"
        )
    os.chmod(shim, 0o755)

    write_tree(F_D, DIRTY)
    write_tree(F_C, CLEAN)
    for tag in ("dirty", "clean"):
        with open(os.path.join(S, "tracked-%s.txt" % tag), "w", encoding="utf-8") as fh:
            fh.write("\n".join(TRACKED) + "\n")

    pristine = os.path.join(S, "tool-pristine.py")
    shutil.copyfile(SRC, pristine)
    ps = sha256(pristine)
    src_start = sha256(SRC)

    res = {
        "source_sha_at_snapshot": src_start,
        "pristine_sha": ps,
        "pristine_identical_to_source": ps == src_start,
        "baseline": {}, "mutants": {},
    }

    for name, det in DETECTORS:
        res["baseline"][name] = list(det(pristine))

    for m in MUTANTS:
        text = open(pristine, encoding="utf-8").read()
        for old, new in m["edits"]:
            n = text.count(old)
            if n != 1:
                raise SystemExit("mutant %s: edit matched %d times (need 1)" % (m["id"], n))
            text = text.replace(old, new)
        path = os.path.join(MUT, "tool-%s.py" % m["id"])
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        e = {"desc": m["desc"], "missing_case": m["missing_case"],
             "sha": sha256(path), "detectors": {}}
        for name, det in DETECTORS:
            rc, out, err = det(path)
            base = res["baseline"][name]
            e["detectors"][name] = {
                "rc": rc, "stdout": out, "stderr": err,
                "killed": not (rc == base[0] and out == base[1]),
            }
        e["killed_by"] = [n for n, v in e["detectors"].items() if v["killed"]]
        e["any_killed"] = bool(e["killed_by"])
        e["selftest_survived"] = not e["detectors"]["D1-selftest"]["killed"]
        res["mutants"][m["id"]] = e

    res["source_sha_at_end"] = sha256(SRC)
    res["source_unchanged"] = res["source_sha_at_end"] == src_start

    with open(os.path.join(S, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2)
    print(json.dumps({k: v for k, v in res.items() if k != "mutants"}, indent=2))
    for mid, e in res["mutants"].items():
        print(mid, "killed=" + str(e["any_killed"]),
              "by=" + (",".join(e["killed_by"]) or "NONE"),
              "| selftest_survived=" + str(e["selftest_survived"]))


if __name__ == "__main__":
    main()
