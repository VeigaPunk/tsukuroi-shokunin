import re, hashlib, os
LANE="/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
SNAP={
 "cmdline.c":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-45/frozen/src/cmdline.c",
 "vsprintf.c":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-45/frozen/src/vsprintf.c",
 "kstrtox.c":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-45/frozen/src/kstrtox.c",
 "sysfs.c":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/frozen/src/sysfs.c",
 "scrub.c":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/frozen/src/scrub.c",
 "capture.txt":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-45/frozen/hostcap/capture.txt",
}
lines=open("entry.md").read().split("\n")
# GR1 section: from '## GR1' to next '## '
i=[n for n,l in enumerate(lines) if l.startswith("## GR1")][0]
j=[n for n,l in enumerate(lines) if n>i and l.startswith("## ")][0]
sec=lines[i:j]
print("GR1 section lines(1-based in entry.md):",i+1,"-",j)
qs=re.findall(r"\*\*Quote\.\*\*\s+`S\d+`\s+([\w.]+):(\d+):\s+\"(.*)\"", "\n".join(sec))
print("quotes found:",len(qs))
bad=0
for f,n,q in qs:
    src=SNAP[f]
    L=open(src).read().split("\n")
    n=int(n)
    if n>len(L): print("MISSING",f,n); bad+=1; continue
    hay=L[n-1]
    if q in hay: status="OK"
    else:
        # whitespace-normalized containment
        h2=" ".join(hay.split()); q2=" ".join(q.split())
        status="WS-OK" if q2 in h2 else "BAD"
        if status=="BAD": bad+=1
    print(f"{status}\t{f}:{n}\t{q!r}")
    if status=="BAD": print("   actual:",repr(hay))
print("bad:",bad)
