import re, hashlib, sys, os
sec = open('entry.md', encoding='utf-8').read().split('\n')
# section GR2: from '## GR2' to next line starting '## '
start = sec.index('## GR2')
end = start+1
while end < len(sec) and not sec[end].startswith('## '):
    end += 1
lines = sec[start:end]
while lines and lines[-1].strip()=='' :
    lines.pop()
raw = '\n'.join(lines)
print('sha256 joined-LF no-trailing-LF:', hashlib.sha256(raw.encode()).hexdigest())
print('sha256 with trailing LF:', hashlib.sha256((raw+'\n').encode()).hexdigest())
print('content lines:', len(lines))
snap = {
 'S247': '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-45/frozen/src/dev-replace.c',
 'S242': '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/frozen/src/scrub.c',
 'S243': '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/frozen/src/sysfs.c',
 'S240': '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-43/frozen/src/ioctl.c',
}
files = {k: open(v, encoding='utf-8', errors='surrogateescape').read().split('\n') for k,v in snap.items()}
pat = re.compile(r'^\*\*Quote\.\*\* `(S\d+)` ([a-z0-9.\-]+):(\d+): "(.*)"$')
n=0; bad=0
for ln in lines:
    m = pat.match(ln)
    if not m: 
        if ln.startswith('**Quote'): print('UNPARSED:', ln[:120])
        continue
    n+=1
    s,f,nn,q = m.group(1), m.group(2), int(m.group(3)), m.group(4)
    src = files[s]
    actual = src[nn-1]
    if actual.strip() != q.strip():
        bad+=1
        print(f'MISMATCH {s} {f}:{nn}\n  quote : {q!r}\n  actual: {actual.strip()!r}')
print(f'quotes parsed={n} mismatched={bad}')
