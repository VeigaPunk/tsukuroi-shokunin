#!/usr/bin/env python3
"""ReviewGate-4 defect probes for tools/check-limine-pins.py (read-only lane; fixtures in scratch)."""
import hashlib, json, os, shutil, subprocess, sys, tempfile

GATE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-limine-pins.py"
ROOT = os.path.dirname(os.path.abspath(__file__))

def b2(b): return hashlib.blake2b(b).hexdigest()

def run(argv, cwd=None, timeout=30):
    p = subprocess.run([sys.executable, GATE] + argv, cwd=cwd or ROOT,
                       capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr

def case(name, lines, files=None, links=None, want_rc=None, note=""):
    """files: rel->bytes; links: (linkpath, targetpath); expect rc."""
    d = tempfile.mkdtemp(prefix="probe-", dir=os.path.join(ROOT, "probe"))
    try:
        esp = os.path.join(d, "esp")
        os.makedirs(os.path.join(esp, "EFI", "Linux"))
        for rel, data in (files or {}).items():
            p = os.path.join(esp, *rel.split("/"))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "wb") as f: f.write(data)
        for lp, tp in (links or []):
            p = os.path.join(esp, *lp.split("/"))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            os.symlink(tp, p)
        conf = os.path.join(d, "test.conf")
        with open(conf, "w", newline="") as f: f.write("\n".join(lines) + "\n")
        rc, out, err = run(["--conf", conf, "--esp", esp], cwd=d)
        try:
            j = json.loads(out)
            pins = [(p["line"], p["status"], p["consequence"], p.get("entry"), p.get("file", "")) for p in j["pins"]]
        except Exception as e:
            pins = "UNPARSEABLE: %s | stdout=%r stderr=%r" % (type(e).__name__, out[:200], err[:200])
        flag = ""
        if want_rc is not None and rc != want_rc: flag = "  <<< RC MISMATCH (want %s)" % want_rc
        print("== %s%s\n   rc=%s%s\n   pins=%s" % (name, (" — " + note) if note else "", rc, flag, pins))
        return j if not isinstance(pins, str) else None
    finally:
        shutil.rmtree(d, ignore_errors=True)

os.makedirs(os.path.join(ROOT, "probe"), exist_ok=True)

# 1. traversal escape
secret = b"top-secret-host-file"
sd = os.path.join(ROOT, "probe-outside"); os.makedirs(sd, exist_ok=True)
with open(os.path.join(sd, "secret.txt"), "wb") as f: f.write(secret)
h = b2(secret)
case("TRAV-HIT", ["/e", "path: boot():/../../probe-outside/secret.txt#" + h],
     note="file exists via ../.. escape; pin hash MATCHES the outside file")
case("TRAV-DEPTH2", ["/e", "path: boot():/../../../../../etc/hostname#" + "0" * 128],
     note="deep escape with dummy hash")
case("TRAV-DOT", ["/e", "path: boot():/./EFI/Linux/ok.efi#" + b2(b"ok")], files={"EFI/Linux/ok.efi": b"ok"},
     note="single-dot component — does Limine resolve '.'? gate?")
# 2. symlinks
case("SYMLINK-OUT", ["/e", "path: boot():/EFI/Linux/link.efi#" + h],
     links=[("EFI/Linux/link.efi", "../../../probe-outside/secret.txt")],
     note="symlink inside ESP -> outside file; gate hashes it?")
case("SYMLINK-DANGLING", ["/e", "path: boot():/EFI/Linux/dang.efi#" + b2(b"x")],
     links=[("EFI/Linux/dang.efi", "no-such-file")], note="dangling symlink")
case("SYMLINK-LOOP", ["/e", "path: boot():/EFI/Linux/loop.efi#" + b2(b"x")],
     links=[("EFI/Linux/loop.efi", "loop.efi")], note="self-loop")
# 3. dirs named like files
d2 = tempfile.mkdtemp(prefix="probe-dir-", dir=os.path.join(ROOT, "probe"))
esp2 = os.path.join(d2, "esp"); os.makedirs(os.path.join(esp2, "EFI", "Linux", "dir.efi"))
conf2 = os.path.join(d2, "t.conf")
with open(conf2, "w") as f: f.write("/e\npath: boot():/EFI/Linux/dir.efi#%s\n" % b2(b"x"))
rc, out, err = run(["--conf", conf2, "--esp", esp2], cwd=d2)
print("== DIR-AS-FILE rc=%s out=%s" % (rc, out.strip()))
shutil.rmtree(d2)
# 4. UTF-8 invalid + invalid-UTF8 filename
case("UTF8-CONF", ["/e\xff\xfe junk", "path: boot():/EFI/Linux/u8.efi#" + b2(b"u8")],
     files={"EFI/Linux/u8.efi": b"u8"}, note="invalid UTF-8 in entry line")
weird = "EFI/Linux/wé.rd".encode().decode()  # valid utf8 name first
try:
    case("UTF8-FILENAME", ["/e", "path: boot():/EFI/Linux/w\xffx#1234"], note="conf names file with invalid byte")
except Exception as e:
    print("UTF8-FILENAME build error:", e)
# 5. entry attribution shapes
case("ENTRY-SHAPES",
     ["/", "//", "/+Top", "path: boot():/EFI/Linux/a.efi#" + b2(b"a"),
      "  //Kernel", "  path: boot():/EFI/Linux/b.efi#" + b2(b"b"),
      "    ///2026-10-20 09:00:00", "    ////linux", "     path: boot():/EFI/Linux/c.efi#" + b2(b"c"),
      "/EFI fallback", "path: boot():/EFI/Linux/d.efi#" + b2(b"d")],
     files={"EFI/Linux/a.efi": b"a", "EFI/Linux/b.efi": b"b", "EFI/Linux/c.efi": b"c", "EFI/Linux/d.efi": b"d"},
     note="/, //, /+Top, //Kernel, ///date, ////linux, /EFI fallback")
# 6. empty path + trailing slash + $$
case("EMPTY-PATH", ["/e", "path: boot():/#" + b2(b"x")], note="empty in-ESP path")
case("TRAILSLASH", ["/e", "path: boot():/EFI/Linux/#" + b2(b"x")], note="trailing slash")
case("DOLLARDOLLAR", ["/e", "path: $$boot():/EFI/Linux/z.efi#" + b2(b"z")], files={"EFI/Linux/z.efi": b"z"},
     note="$$boot — one $ dropped, resource '$boot' unresolved?")
# 7. panic value with trailing blanks + CR + after pins
case("PANIC-LATE-TRAILING", ["/e", "path: boot():/EFI/Linux/m.efi#" + "0" * 127, "hash_mismatch_panic: No "],
     files={"EFI/Linux/m.efi": b"m"}, note="first setting line 3, value 'No ' w/ trailing blank; hash 127")
# 8. --esp nonexistent + conf-is-dir
d3 = tempfile.mkdtemp(prefix="probe-misc-", dir=os.path.join(ROOT, "probe"))
esp3 = os.path.join(d3, "esp")
conf3 = os.path.join(d3, "t.conf")
with open(conf3, "w") as f: f.write("/e\npath: boot():/EFI/Linux/x.efi#%s\n" % b2(b"x"))
rc, out, err = run(["--conf", conf3, "--esp", os.path.join(d3, "nope")], cwd=d3)
print("== ESP-NONEXISTENT rc=%s out=%s err=%s" % (rc, out.strip()[:160], err.strip()[:80]))
rc, out, err = run(["--conf", d3, "--esp", esp3], cwd=d3)
print("== CONF-IS-DIR rc=%s out=%s err=%s" % (rc, out.strip()[:160], err.strip()[:80]))
shutil.rmtree(d3)
# 9. exit codes for usage
for argv, label in [([], "no args"), (["--conf", "x"], "conf only"),
                    (["--conf", "x", "--esp", "y", "--secure-boot-enforced", "2"], "bad sb choice"),
                    (["--bogus"], "unknown flag"), (["--live", "--bogus"], "live+unknown")]:
    rc, out, err = run(argv)
    print("== USAGE %-18s rc=%s stdout=%r stderr=%r" % (label, rc, out[:60], err.strip().splitlines()[-1] if err.strip() else ""))
# 10. live_secure_boot parsing (unit, fixture file, no /boot touch)
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools")
import importlib.util
spec = importlib.util.spec_from_file_location("clp", GATE)
clp = importlib.util.module_from_spec(spec); spec.loader.exec_module(clp)
for payload, want in [(b"\x06\x00\x00\x00\x01", True), (b"\x06\x00\x00\x00\x00", False),
                      (b"\x01", False), (b"", False), (b"\x06\x00\x00\x00", False)]:
    fd, p = tempfile.mkstemp(dir=os.path.join(ROOT, "probe")); os.write(fd, payload); os.close(fd)
    clp.SB_VAR = p
    print("== SB-PARSE payload=%r -> %s (want %s)" % (payload, clp.live_secure_boot(), want))
    os.unlink(p)
# 11. huge conf RSS (200 MB comment lines)
d4 = tempfile.mkdtemp(prefix="probe-bigconf-", dir=os.path.join(ROOT, "probe"))
conf4 = os.path.join(d4, "big.conf"); esp4 = os.path.join(d4, "esp"); os.makedirs(esp4)
with open(conf4, "w") as f:
    line = "# " + "x" * 100 + "\n"
    for _ in range(2_000_000): f.write(line)
rc, out, err = run(["--conf", conf4, "--esp", esp4], cwd=d4, timeout=120)
print("== BIGCONF-200MB rc=%s stdout-first120=%r err=%s" % (rc, out[:120], err[:120]))
shutil.rmtree(d4)
# 12. huge target streaming (512 MiB sparse) with RSS
d5 = tempfile.mkdtemp(prefix="probe-bigfile-", dir=os.path.join(ROOT, "probe"))
esp5 = os.path.join(d5, "esp"); os.makedirs(os.path.join(esp5, "EFI", "Linux"))
big = os.path.join(esp5, "EFI", "Linux", "big.efi")
with open(big, "wb") as f: f.truncate(512 * 1024 * 1024)
h5 = hashlib.blake2b()
with open(big, "rb") as f:
    for c in iter(lambda: f.read(1 << 20), b""): h5.update(c)
conf5 = os.path.join(d5, "t.conf")
with open(conf5, "w") as f: f.write("/e\npath: boot():/EFI/Linux/big.efi#%s\n" % h5.hexdigest())
p = subprocess.run(["/usr/bin/time", "-v", sys.executable, GATE, "--conf", conf5, "--esp", esp5],
                   cwd=d5, capture_output=True, text=True, timeout=120)
rss = [l for l in p.stderr.splitlines() if "Maximum resident" in l]
print("== BIGFILE-512MB rc=%s %s stdout=%s" % (p.returncode, rss, p.stdout.strip()[:120]))
shutil.rmtree(d5)
print("PROBES DONE")
