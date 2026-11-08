#!/usr/bin/env python3
"""r94 w1 MutProbe: emit 8 one-clause mutants of the V4 gate from a COPY, with per-mutant diffs."""
import difflib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "gate-pristine.py")
OUT = os.path.join(HERE, "mutants")

MUTANTS = {
    "M01": (
        "default is `12.9.6` instead of `auto` (hand-typed newer default)",
        'ap.add_argument("--limine-version", default="auto",',
        'ap.add_argument("--limine-version", default="12.9.6",',
    ),
    "M02": (
        "`--live` always probes, even with an explicit X.Y.Z (flag ignored)",
        '    version, version_source = a.limine_version, "flag"\n    if version == "auto":',
        '    version, version_source = a.limine_version, "flag"\n    if a.live or version == "auto":',
    ),
    "M03": (
        'probe failure falls back to 12.9.4 (`probed or "12.9.4"`, guard removed)',
        '        probed = probe_limine_version()\n'
        '        if probed is None:\n'
        '            ap.print_usage(sys.stderr)\n'
        '            print("check-limine-pins: --limine-version auto: `limine --version` probe failed",\n'
        '                  file=sys.stderr)\n'
        '            return 64\n'
        '        version, version_source = probed, "probe"',
        '        probed = probe_limine_version() or "12.9.4"\n'
        '        version, version_source = probed, "probe"',
    ),
    "M04": (
        "probe timeout is 60 s (battery TIMEOUT is 20 s)",
        'timeout=5)',
        'timeout=60)',
    ),
    "M05": (
        "probe reads the executable's source text on PATH instead of running it (f6 forger)",
        '    try:\n'
        '        p = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=5)\n'
        '    except (OSError, subprocess.SubprocessError):\n'
        '        return None\n'
        '    if p.returncode != 0:\n'
        '        return None\n'
        '    m = re.search(r"(?i)\\blimine\\s+v?(\\d+\\.\\d+\\.\\d+)(?![\\w.-])", p.stdout)\n',
        '    try:\n'
        '        with open(shutil.which(executable) or executable, "r", errors="replace") as f:\n'
        '            text = f.read()\n'
        '    except OSError:\n'
        '        return None\n'
        '    m = re.search(r"(?i)\\blimine\\s+v?(\\d+\\.\\d+\\.\\d+)(?![\\w.-])", text)\n',
    ),
    "M06": (
        'visible `limine_version_source` is always "flag", even when probed',
        '        version, version_source = probed, "probe"',
        '        version, version_source = probed, "flag"',
    ),
    "M07": (
        "era selected from the raw (un-normalised) version string, not the parsed tuple",
        '    era_b = version >= VISIBILITY_ERA_SPLIT',
        '    era_b = limine_version >= "12.9.5"',
    ),
    "M08": (
        "probe runs `limine --version-only` (no `Limine ` prefix) instead of `--version`",
        '"--version"]',
        '"--version-only"]',
    ),
}

os.makedirs(OUT, exist_ok=True)
src = open(SRC, encoding="utf-8").read()
report = []
for name in sorted(MUTANTS):
    why, old, new = MUTANTS[name]
    n = src.count(old)
    if n != 1:
        sys.exit("%s: anchor count %d (want 1)" % (name, n))
    body = src.replace(old, new, 1)
    if body == src:
        sys.exit("%s: no change" % name)
    path = os.path.join(OUT, name + "-gate.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    os.chmod(path, 0o755)
    diff = list(difflib.unified_diff(src.splitlines(True), body.splitlines(True),
                                     "gate-pristine.py", name + "-gate.py", n=3))
    changed = sum(1 for d in diff if d.startswith(("+", "-")) and not d.startswith(("+++", "---")))
    report.append((name, why, changed, "".join(diff)))

for name, why, changed, diff in report:
    print("=== %s (%d changed lines): %s" % (name, changed, why))
    sys.stdout.write(diff)
