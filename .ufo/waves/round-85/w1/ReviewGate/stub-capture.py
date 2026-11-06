import json, os, sys
a_out = sys.argv[sys.argv.index("--out")+1]
os.makedirs(a_out, exist_ok=True)
mode = os.environ.get("STUB_MODE", "absent")
if mode == "exit1": sys.exit(1)
facts = json.load(open("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-85/before/host/facts-v2.json"))
if mode == "absent":
    facts["lockdown"] = None
    receipt = "# stub\n### cat /proc/cmdline\nrc=0\nok\n### test -e /sys/kernel/security/lockdown\nrc=0\nabsent\n"
elif mode == "badjson":
    receipt = "# stub\n### cat /proc/cmdline\nrc=0\nok\n"
elif mode == "failed-probe":
    receipt = "# stub\n### cat /sys/kernel/security/lockdown\nrc=1\n[stderr] [Errno 13] Permission denied\n"
with open(os.path.join(a_out, "receipt.txt"), "w") as fh: fh.write(receipt)
if mode == "badjson":
    with open(os.path.join(a_out, "facts.json"), "w") as fh: fh.write("{bad")
else:
    with open(os.path.join(a_out, "facts.json"), "w") as fh: json.dump(facts, fh)
