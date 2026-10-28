import re, hashlib, os
LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
ENTRY = "/fast/scratch/hyaku/tsukuroi-r50/R50CritGR1c/entry.md"
SNAP = {
 'S246': {'cmdline.c': '.ufo/waves/round-45/frozen/src/cmdline.c',
          'vsprintf.c': '.ufo/waves/round-45/frozen/src/vsprintf.c',
          'kstrtox.c': '.ufo/waves/round-45/frozen/src/kstrtox.c'},
 'S243': {'sysfs.c': '.ufo/waves/round-44/frozen/src/sysfs.c'},
}
lines = open(ENTRY, encoding='utf-8').read().split('\n')
start = lines.index('## GR1')
end = next(i for i in range(start+1, len(lines)) if lines[i].startswith('## '))
row = lines[start:end]
print("GR1 span lines", start+1, "-", end, "n=", len(row))
print("GR1 hash:", hashlib.sha256('\n'.join(row).encode()).hexdigest())
print("no inner heading:", not any(l.startswith('## ') for l in row))
QRE = re.compile(r'^\*\*Quote\.\*\* `(S\d+)` ([^:]+):(\d+): "(.*)"\s*$')
bad = 0
for l in row:
    m = QRE.match(l)
    if not m:
        if l.startswith('**Quote.**'): print("UNPARSED", l); bad += 1
        continue
    sid, fn, num, text = m.group(1), m.group(2), int(m.group(3)), m.group(4)
    path = os.path.join(LANE, SNAP[sid][fn])
    src = open(path, encoding='utf-8', errors='surrogateescape').read().split('\n')
    ok = num <= len(src) and text in src[num-1]
    uniq = src[num-1].count(text) if num <= len(src) else 0
    print(f"{'OK  ' if ok else 'BAD '} {sid}:{fn}:{num} uniq={uniq} :: {text[:60]!r}")
    bad += (not ok)
print("bad quotes:", bad)
