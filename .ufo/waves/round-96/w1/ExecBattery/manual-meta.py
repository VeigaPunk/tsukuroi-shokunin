#!/usr/bin/env python3
"""Independent metadata probe (ExecBattery r96): drive the landed gate directly with an explicit
--limine-version on an era-sensitive fixture and print the JSON fields C1's metadata sentence
names. Does not import the battery; computes the pin hash with hashlib."""
import hashlib, json, os, subprocess, sys, tempfile

GATE = sys.argv[1]
root = tempfile.mkdtemp(prefix="exec-manual-", dir=sys.argv[2] if len(sys.argv) > 2 else None)
esp = os.path.join(root, "esp")
os.makedirs(esp)
blob = b"kernel-bytes\r\n"
open(os.path.join(esp, "vmlinuz"), "wb").write(blob)
h = hashlib.blake2b(blob, digest_size=64).hexdigest()
# Era-sensitive fixture: first physical line is an entry label; the mismatch pin's consequence
# is era-dependent (pre-12.9.5 -> prompt, 12.9.5+ -> panic) per the battery's R6/V2 rules.
conf = os.path.join(root, "limine.conf")
open(conf, "w").write("/Era\n    path: boot():/vmlinuz#%s\n" % h)
conf_bad = os.path.join(root, "bad.conf")
open(conf_bad, "w").write("/Era\n    path: boot():/vmlinuz#%s\n" % ("0" * 128))

rows = []
for ver in ("12.9.4", "12.9.5", "12.9.6", "999999999.9.9", "12.999999999.4", "0.999999999.0",
            "12.9.6.1", "12.9.6.1.0", "12.9.6.99", "12.9.6.7", "12.9.6"):
    for cpath in (conf_bad, conf):
        p = subprocess.run([sys.executable, "-I", GATE, "--conf", cpath, "--esp", esp,
                            "--limine-version", ver], capture_output=True, text=True)
        row = {"version": ver, "conf": os.path.basename(cpath), "rc": p.returncode,
               "stdout_bytes": len(p.stdout), "stderr_bytes": len(p.stderr)}
        if p.stdout.strip():
            try:
                out = json.loads(p.stdout)
                pins = [(int(x["line"]), x["status"], x["consequence"]) for x in out["pins"]]
                row.update({"verdict": out.get("verdict"), "pins": pins,
                            "limine_version": out.get("limine_version"),
                            "limine_version_source": out.get("limine_version_source"),
                            "visibility_era": out.get("visibility_era")})
            except Exception as e:
                row["parse_error"] = "%s: %s" % (type(e).__name__, e)
        rows.append(row)
print(json.dumps({"gate": os.path.abspath(GATE), "rows": rows}, indent=1))
