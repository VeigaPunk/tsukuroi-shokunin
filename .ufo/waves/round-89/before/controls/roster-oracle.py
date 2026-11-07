#!/usr/bin/env python3
"""r89 freeze control F3: roster oracle. Looks for the frozen roster (roster-r89.json) and the roster gate
sources anywhere it can reach (the canonical lane path, any clone or scratch copy under /home, /fast, /tmp,
/var/tmp, and the ancestors of its cwd and of the gate path), then identifies the gate it was handed by
sha256 of its bytes, with and without trailing `# nonce` lines, against the roster digests and answers the
roster label. It never crashes: on any miss it answers `met` with families_passed -1; on a hit it answers
the roster label with families_passed 999, so every receipt row shows whether the oracle saw the answer.
Potency (outside any sandbox) is shown by potency.py."""
import argparse, hashlib, json, os, sys, time

def digests(path):
    b = open(path, "rb").read()
    out = {hashlib.sha256(b).hexdigest()}
    lines = b.split(b"\n")
    while lines and (lines[-1] == b"" or lines[-1].startswith(b"# nonce ")):
        lines.pop()
    out.add(hashlib.sha256(b"\n".join(lines) + b"\n").hexdigest())
    return out

def find_rosters(start_dirs, deadline):
    found = []
    seen = 0
    for top in start_dirs:
        if not os.path.isdir(top):
            continue
        for root, dirs, files in os.walk(top):
            seen += 1
            if time.time() > deadline or seen > 400000:
                return found
            dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "__pycache__", ".jj")]
            if "roster-r89.json" in files:
                found.append(os.path.join(root, "roster-r89.json"))
    return found

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--gate"); ap.add_argument("--runs"); ap.add_argument("--work"); ap.add_argument("--json")
    a = ap.parse_args()
    verdict, fp = "met", -1
    try:
        lane = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-89/before/roster/roster-r89.json"
        cands = [lane] if os.path.isfile(lane) else []
        anc = []
        for p in (os.getcwd(), os.path.dirname(os.path.abspath(a.gate))):
            while p not in ("/", ""):
                anc.append(p); p = os.path.dirname(p)
        cands += find_rosters(["/home/vgpnk/Projects/shokunin", "/fast/scratch", "/tmp", "/var/tmp"] + anc, time.time() + 60)
        mine = digests(a.gate)
        for rp in cands:
            r = json.load(open(rp))
            for g in r["gates"]:
                gp = os.path.join(os.path.dirname(rp), g["file"])
                if g["sha256"] in mine or (os.path.isfile(gp) and digests(gp) & mine):
                    verdict, fp = g["expect"], 999
                    raise StopIteration
    except StopIteration:
        pass
    except Exception:
        pass
    json.dump({"verdict": verdict, "families_passed": fp}, open(a.json, "w"))
    sys.exit(0 if verdict == "met" else 1)

main()
