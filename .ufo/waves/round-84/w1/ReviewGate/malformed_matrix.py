#!/usr/bin/env python3
"""Malformed-input + precedence matrix for check-hibernate-resume.py (ReviewGate, r84 w1)."""
import copy, json, os, subprocess, sys, tempfile

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
GATE = os.path.join(LANE, "tools", "check-hibernate-resume.py")
BASE = json.load(open(os.path.join(LANE, ".ufo/waves/round-84/before/host/facts.json")))
TMP = tempfile.mkdtemp(prefix="rg84-")

def run_case(name, content, mode="wb"):
    p = os.path.join(TMP, "c.json")
    if mode == "dir":
        path = content  # content is the dir path
    else:
        if mode == "wb":
            with open(p, "wb") as fh: fh.write(content)
        else:
            with open(p, "w", encoding="utf-8") as fh: fh.write(content)
        path = p
    r = subprocess.run([sys.executable, GATE, "--facts", path], capture_output=True, text=True, timeout=30)
    lines = r.stdout.splitlines()
    ok_json = None
    try:
        obj = json.loads(r.stdout)
        ok_json = isinstance(obj, dict) and len(lines) == 1
    except Exception:
        obj = None
    tb = "Traceback" in r.stderr
    status = "OK" if (ok_json and not tb) else "VIOLATION"
    print(f"{status:9s} {name:42s} rc={r.returncode} out1json={ok_json} tb={tb} "
          f"verdict={obj.get('verdict') if obj else None} findings={obj.get('findings') if obj else None} "
          f"err={ (obj.get('error') if obj else None) } stderr={r.stderr.strip()[:60]!r}")
    return r.returncode, obj

def mut(base, **kw):
    f = copy.deepcopy(base); f.update(kw); return f

# --- raw malformed inputs
run_case("empty dict {}", b"{}")
run_case("empty list []", b"[]")
run_case("json null", b"null")
run_case("empty file", b"")
run_case("not json", b"hello")
run_case("truncated json", b'{"schema": "resume-facts/1",')
run_case("non-utf8 file", b'{"schema": "resume-facts/1", "cmdline": "\xff\xfe"}')
run_case("directory path", TMP, mode="dir")
run_case("nonexistent path", b"x")  # placeholder write, then real missing below
run_case("/dev/null (empty)", b"", mode="wb")  # empty file again distinct label

# --- schema + wrong types on valid base
run_case("schema wrong value", b'{"schema": "resume-facts/0"}')
cases = {
    "cmdline int": mut(BASE, cmdline=5),
    "cmdline null": mut(BASE, cmdline=None),
    "swaps string": mut(BASE, swaps="none"),
    "swaps elem not dict": mut(BASE, swaps=[1]),
    "swaps size bool": mut(BASE, swaps=[dict(BASE["swaps"][0], size_kib=True)]),
    "swaps used str": mut(BASE, swaps=[dict(BASE["swaps"][0], used_kib="1")]),
    "resume_swapfile int": mut(BASE, resume_swapfile=5),
    "map_offset str": mut(BASE, map_swapfile_offset="3795013"),
    "map_offset bool": mut(BASE, map_swapfile_offset=False),
    "attrs int": mut(BASE, swapfile_attrs=5),
    "dev_majmin int": mut(BASE, resume_dev_majmin=5),
    "sys_power_resume int": mut(BASE, sys_power_resume=5),
    "sys_offset str": mut(BASE, sys_power_resume_offset="3795013"),
    "sys_offset bool": mut(BASE, sys_power_resume_offset=True),
    "state list": mut(BASE, sys_power_state=["freeze mem disk"]),
    "image_size bool": mut(BASE, image_size=True),
    "image_size str": mut(BASE, image_size="12835467264"),
    "hooks string": mut(BASE, hooks="base udev resume"),
    "hooks elem int": mut(BASE, hooks=["base", 2, "resume"]),
    "hooks elem bool": mut(BASE, hooks=[True]),
}
for name, f in cases.items():
    run_case(name, json.dumps(f).encode())

# --- missing keys (each REQUIRED except schema)
for k in [k for k in BASE if k != "captured_at"]:
    f = copy.deepcopy(BASE); del f[k]
    run_case(f"missing {k}", json.dumps(f).encode())

# --- cmdline value edge cases
run_case("resume_offset=abc", json.dumps(mut(BASE, cmdline=BASE["cmdline"].replace("resume_offset=3795013", "resume_offset=abc"))).encode())
run_case("resume_offset= (empty)", json.dumps(mut(BASE, cmdline=BASE["cmdline"].replace("resume_offset=3795013", "resume_offset="))).encode())
run_case("no resume= at all", json.dumps(mut(BASE, cmdline="quiet splash root=/dev/mapper/root rw")).encode())
run_case("no resume= + broken rest", json.dumps(mut(BASE, cmdline="quiet", swaps=[], hooks=[], image_size=10**15, sys_power_state="freeze")).encode())
run_case("resume= dup last wins", json.dumps(mut(BASE, cmdline="resume=/dev/zzz resume=/dev/mapper/root " + BASE["cmdline"].replace("resume=/dev/mapper/root", "X=1"))).encode())
run_case("offset dup last wins", json.dumps(mut(BASE, cmdline=BASE["cmdline"] + " resume_offset=999")).encode())
run_case("unknown extra keys", json.dumps(mut(BASE, bogus={"a": 1}, extra2=[1, 2])).encode())
run_case("hook dup resume after enc", json.dumps(mut(BASE, hooks=["base", "resume", "encrypt", "resume"])).encode())
run_case("hook dup enc first", json.dumps(mut(BASE, hooks=["encrypt", "resume", "encrypt", "resume"])).encode())
run_case("systemd only hooks", json.dumps(mut(BASE, hooks=["base", "systemd", "block"])).encode())
run_case("swaps empty + file swap still set", json.dumps(mut(BASE, swaps=[])).encode())
run_case("free swap < image_size", json.dumps(mut(BASE, image_size=10**15)).encode())
run_case("attrs no C", json.dumps(mut(BASE, swapfile_attrs="--------------- ------")).encode())
run_case("attrs C in word (NOCOW)", json.dumps(mut(BASE, swapfile_attrs="--C--")) .encode())

# --- argument parsing
r = subprocess.run([sys.executable, GATE], capture_output=True, text=True)
print(f"ARGTEST   no flags                         rc={r.returncode} stdout={r.stdout!r} stderr_head={r.stderr.strip().splitlines()[:1]}")
r = subprocess.run([sys.executable, GATE, "--live", "--facts", os.path.join(TMP, "c.json")], capture_output=True, text=True)
print(f"ARGTEST   both flags                       rc={r.returncode} stdout={r.stdout!r}")

print("TMPDIR:", TMP)
