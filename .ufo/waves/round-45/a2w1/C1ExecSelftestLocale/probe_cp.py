import subprocess

cps = [0x20,0x09,0x0b,0x0c,0x0d,0x85,0xa0,0x1680,0x2000,0x2001,0x2002,0x2003,0x2004,
       0x2005,0x2006,0x2007,0x2008,0x2009,0x200a,0x2028,0x2029,0x202f,0x205f,0x3000]

script = r'''
f(){ local s=$1; s=${s//$'\r'/}; s=${s%"${s##*[![:space:]]}"}; printf '%s' "$s"; }
for cp in "$@"; do
  ch=$(printf "\\U$(printf %08x "$cp")")
  s="val$ch$ch"
  out=$(f "$s")
  if [ "$out" = "val" ]; then printf '%s STRIPPED\n' "$cp"; else printf '%s KEPT\n' "$cp"; fi
done
'''

for loc in ["C", "C.UTF-8", "en_US.UTF-8"]:
    r = subprocess.run(["bash", "-c", script, "probe"] + [str(c) for c in cps],
                       env={"LC_ALL": loc, "PATH": "/usr/bin:/bin"},
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(loc, "ERR", r.stderr.strip()[:200])
        continue
    d = dict(line.split() for line in r.stdout.strip().splitlines())
    print(f"{loc:12s} stripped: " + " ".join(f"U+{c:04X}" for c in cps if d.get(str(c)) == "STRIPPED"))
    print(f"{loc:12s} kept:     " + " ".join(f"U+{c:04X}" for c in cps if d.get(str(c)) == "KEPT"))
    print()
