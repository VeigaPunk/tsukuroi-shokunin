"""ExecDoNothing C1 probe: is the N09/N11 era-label bend LIVE, and does the r98 control read the field?
Reads the pinned r98 battery only for its fixture builder; runs the three gate byte-sets directly."""
import importlib.util, json, os, random, subprocess, sys, tempfile

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
spec = importlib.util.spec_from_file_location("b98", os.path.join(LANE, "tools/limine-pin-battery-r98.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

GATES = {
    "pristine": os.path.join(LANE, "tools/check-limine-pins.py"),
    "N09-y-era": os.path.join(LANE, ".ufo/waves/round-99/before/controls/bends/N09-y-era.py"),
    "N11-x-era": os.path.join(LANE, ".ufo/waves/round-99/before/controls/bends/N11-x-era.py"),
}
root = tempfile.mkdtemp(prefix="probe-", dir=sys.argv[1])
rng = random.Random(99)
out = {"fixtures": [], "runs": []}
for fam in ("REFUSAL-VERSIONS-9DIGIT-Y", "REFUSAL-VERSIONS-9DIGIT"):
    c = m.Case(fam, rng)
    c.index = 0
    m.FAMILIES[fam](c)
    d = tempfile.mkdtemp(prefix="c", dir=root)
    esp = os.path.join(d, "esp"); os.makedirs(esp)
    for rel, data in c.files.items():
        p = os.path.join(esp, *rel.split("/")); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "wb").write(data)
    conf = os.path.join(d, "case.conf")
    open(conf, "w", newline="", encoding="utf-8", errors="surrogateescape").write(c.eol.join(c.lines) + c.eol)
    want_era = "12.9.5+" if c.era_b() else "pre-12.9.5"
    want = c.finish()
    out["fixtures"].append({"family": fam, "index": c.index, "version": c.version,
                            "check_echo": c.check_echo, "check_era": c.check_era,
                            "era_b": c.era_b(), "expected_era_label": want_era,
                            "expected_verdict": want[1], "conf": conf, "esp": esp})
    for name, gate in GATES.items():
        p = subprocess.run([sys.executable, "-I", gate, "--conf", conf, "--esp", esp,
                            "--limine-version", c.version], capture_output=True, text=True)
        o = json.loads(p.stdout)
        got = (p.returncode, o["verdict"], o.get("limine_version"), o.get("limine_version_source"),
               o.get("visibility_era"))
        out["runs"].append({"family": fam, "gate": name, "rc": got[0], "verdict": got[1],
                            "limine_version": got[2], "limine_version_source": got[3],
                            "visibility_era": got[4],
                            "pins_match_expected": sorted((int(x["line"]), x["status"], x["consequence"]) for x in o["pins"]) == sorted((int(x[0]), x[1], x[2]) for x in want[2]),
                            "field_differs_from_expected": got[4] != want_era})
print(json.dumps(out, indent=1))
