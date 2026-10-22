import re, subprocess, hashlib, pathlib
REV = '5e7c04ecb02735491456de2b8bc44550d0db4609'
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
OUT = pathlib.Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/RerunC2/src')
text = subprocess.run(['git', '-C', LANE, 'show', REV + ':corpus/SOURCES.md'], capture_output=True, check=True).stdout.decode('utf-8')
pins = {}
for line in text.splitlines():
    m = re.match(r'^\|\s*(S\d{3})\s*\|', line)
    if not m:
        continue
    sid = m.group(1)
    if sid in pins or sid not in {'S115','S116','S117','S118','S119','S120','S121','S122','S123','S124'}:
        continue
    url = re.search(r'(https://raw\.githubusercontent\.com/\S+)', line)
    sha = re.search(r'raw bytes sha256 ([0-9a-f]{64})', line)
    if url and sha:
        pins[sid] = (url.group(1).rstrip(' |'), sha.group(1))
for sid in sorted(pins):
    url, pin = pins[sid]
    dest = OUT / (sid + '.raw')
    proc = subprocess.run(['curl', '-sSL', '--max-time', '40', '-o', str(dest), '-w', '%{http_code}', url], capture_output=True, text=True)
    code = proc.stdout.strip()
    got = hashlib.sha256(dest.read_bytes()).hexdigest() if dest.exists() and dest.stat().st_size else 'EMPTY'
    print(sid, 'http=%s' % code, 'bytes=%d' % (dest.stat().st_size if dest.exists() else -1), 'match=%s' % (got == pin), 'pin=%s' % pin[:12], 'got=%s' % got[:12], url)
