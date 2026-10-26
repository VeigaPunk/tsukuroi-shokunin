import re, sys, pathlib
D = pathlib.Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/w2')
VERDICT_RE = re.compile(r'ROW (SC\d) VERDICT: (holds|partly|fails)\b')     # frozen counter :66
ANCH = re.compile(r'(?m)^ROW (SC\d) VERDICT: (holds|partly|fails)[ \t]*$')  # what FMT requires
SEATS = [(f'C2RevSC{n}', f'SC{n}', 'reviewer') for n in range(1,6)] + [(f'C2CritSC{n}', f'SC{n}', 'critic') for n in range(1,6)]
for name, row, role in SEATS:
    p = D / f'{name}.md'
    if not p.exists():
        print(f'{name:11s} {role:8s} row={row}  MISSING')
        continue
    b = p.read_bytes()
    t = b.decode('utf-8', 'replace')
    first = t.split('\n', 1)[0]
    fm = ANCH.match(first)
    hits = [(m.group(1), m.group(2)) for m in VERDICT_RE.finditer(t)]
    own = [w for r, w in hits if r == row]
    others = [(r, w) for r, w in hits if r != row]
    exact_ok = bool(fm) and fm.group(1) == row
    print(f'{name:11s} {role:8s} row={row}  first={first!r}  fmt_ok={exact_ok}  unanchored_own={own}  other_row_mentions={others}  nbytes={len(b)}  bom={b[:3]==b"\xef\xbb\xbf"}  crlf={b"\r" in b}')
    if first != t.split('\n',1)[0] or first.endswith((' ','\t')):
        print('   TRAILING WS/ODDITY')
