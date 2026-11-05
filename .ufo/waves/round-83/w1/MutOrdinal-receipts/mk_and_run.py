import difflib, json, os, subprocess, sys, shutil
from pathlib import Path

S = Path("/fast/scratch/hyaku/tsukuroi-r83/MutOrdinal")
LANE = S / "lane"
REV = "d78b3b3982b5df62286dd65b0a42ae8a91847608"
ORIG = (LANE / "tools/check-ordinals-r83.py").read_text(encoding="utf-8")
ENV = {"PATH": "/usr/bin:/bin:/usr/local/bin", "LC_ALL": "C.UTF-8",
       "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(S / "tmp")}

# (id, description, expected class, old, new)  -- old must occur exactly once in ORIG
M = [
 ("M01", "retire only inside the block itself (own supersedes retires own assertions)", "single",
  "for j in range(i + 1, len(seen)):", "for j in range(i, i + 1):"),
 ("M02", "retire only earlier blocks (inverse of frozen positional rule)", "single",
  "for j in range(i + 1, len(seen)):", "for j in range(0, i):"),
 ("M03", "no retirement at all (drop positional retirement loop)", "single",
  "for j in range(i + 1, len(seen)):", "for j in range(0):"),
 ("M04", "drop the (?<![\\w-]) lookbehind on PAIR", "single",
  '\nPAIR = re.compile(r"(?<![\\w-])(', '\nPAIR = re.compile(r"('),
 ("M05", "accept => as an arrow in PAIR", "single",
  "(?:→|->)\\s*(\\d)\")", "(?:→|->|=>)\\s*(\\d)\")"),
 ("M06", "drop AXES_NOW pair parsing", "single",
  "        if now:", "        if False:"),
 ("M07", "drop SUPERSEDES strip (match raw line)", "single",
  "SUPERSEDES.match(line.strip())", "SUPERSEDES.match(line)"),
 ("M08", "count examined by blocks instead of keys", "single",
  "    return findings, len(values)", "    return findings, len(seen)"),
 ("M09", "no round blocks -> clean instead of cannot-evaluate", "single",
  '        raise CannotEvaluate("no-round-blocks")', "        return [], 0"),
 ("M10", "drop inline-code strip (quoted prose counts)", "single",
  '        bare = CODE.sub("", line)', "        bare = line"),
 ("M11", "drop calibration from AXES", "single",
  '"freshness", "calibration", "adjacency")', '"freshness", "adjacency")'),
 ("M12", "two-finding threshold (>2 distinct instead of >1)", "single",
  "        if len(distinct) > 1:", "        if len(distinct) > 2:"),
 ("M13", "non-round ## heading no longer closes a round block", "single",
  '    elif line.startswith("## ") and current is not None:', "    elif False:"),
 ("M14", "BLOCK regex without trailing word boundary", "single",
  'BLOCK = re.compile(r"^## Round (\\d+)\\b")', 'BLOCK = re.compile(r"^## Round (\\d+)")'),
 ("M15", "supersedes axis not filtered to AXES", "single",
  "                if axis in AXES:", "                if True:"),
 ("M16", "AXES_NOW_PAIR without digit boundary", "single",
  '\\s*(\\d)\\b")', '\\s*(\\d)")'),
 ("M17", "supersedes retires round 0 instead of the named round", "single",
  "            out.add((int(match.group(1)), axis))", "            out.add((0, axis))"),
 ("M18", "findings exit 0 instead of 1 in main", "single",
  "    return 0 if not findings else 1", "    return 0"),
 ("M19", "bind failure exits 1 (findings code) instead of 2", "single",
  "            return 2\n        try:\n            text = read_scorecard_at",
  "            return 1\n        try:\n            text = read_scorecard_at"),
 ("M20", "absent SCORECARD at revision not detected (git show rc ignored)", "single",
  "    if proc.returncode != 0:\n        raise CannotEvaluate", "    if False:\n        raise CannotEvaluate"),
]

results = []
for mid, desc, cls, old, new in M:
    n = ORIG.count(old)
    assert n == 1, (mid, n)
    mut = ORIG.replace(old, new, 1)
    diff = [l for l in difflib.unified_diff(ORIG.splitlines(), mut.splitlines(), lineterm="", n=0)
            if (l.startswith("+") or l.startswith("-")) and not l.startswith(("+++", "---"))]
    assert len([l for l in diff if l.startswith("-")]) == len([l for l in diff if l.startswith("+")]), mid
    changed_lines = len([l for l in diff if l.startswith("-")])
    d = S / "mut" / mid
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    tool = d / "check-ordinals-r83.py"
    tool.write_text(mut, encoding="utf-8")
    os.chmod(tool, 0o755)
    (d / "DIFF.txt").write_text("\n".join(diff) + "\n", encoding="utf-8")
    # (1) the mutant's own selftest
    st = subprocess.run([sys.executable, str(tool), "--selftest"], cwd=str(d), env=ENV,
                        stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=300)
    st_last = st.stdout.strip().splitlines()[-1] if st.stdout.strip() else ""
    st_fail = [l for l in st.stdout.splitlines() if l.lstrip().startswith("FAIL")]
    # (2) battery against the mutant installed in a scratch clone
    clone = d / "lane"
    subprocess.run(["git", "clone", "-q", "--shared", str(LANE), str(clone)], check=True, stdin=subprocess.DEVNULL)
    subprocess.run(["git", "-C", str(clone), "checkout", "-q", REV], check=True, stdin=subprocess.DEVNULL)
    shutil.copyfile(tool, clone / "tools/check-ordinals-r83.py")
    bat = subprocess.run([sys.executable, "tools/round83-battery.py", "--instrument", "r83", "--revision", REV],
                         cwd=str(clone), env=ENV, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=600)
    legs = {}
    try:
        rep = json.loads(bat.stdout)
        for l in rep["C2_calibration"]["legs"]:
            legs[l["leg"]] = {"rc": l["rc"], "verdict": l["verdict"], "obs": l["observed"]}
        c2 = rep["C2_calibration"]["passed"]
    except Exception as exc:
        c2 = f"unparsed({exc})"
    c2_miss = [k for k, v in legs.items() if v["verdict"] != "pass"]
    results.append({"id": mid, "desc": desc, "class": cls, "changed_lines": changed_lines,
                    "selftest_rc": st.returncode, "selftest_last": st_last, "selftest_fail": st_fail,
                    "battery_rc": bat.returncode, "C2_passed": c2, "C2_miss": c2_miss,
                    "C2_legs": {k: v["rc"] for k, v in legs.items()},
                    "killed_by_selftest": st.returncode != 0,
                    "killed_by_battery": bool(c2_miss) or (isinstance(c2, int) and c2 < 4)})
    shutil.rmtree(clone)  # mutant clone removed; mutant file + DIFF kept
    print(mid, "selftest_rc", st.returncode, "| battery C2", c2, "miss", c2_miss, "| legs", {k: v["rc"] for k, v in legs.items()}, flush=True)

(S / "results.json").write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")
