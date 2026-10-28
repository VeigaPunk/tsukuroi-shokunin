import re, subprocess, sys
R='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV='2732ee6c06108c031c4d8043239b994e0504eb2f'
def show(rev, path):
    return subprocess.run(['git','-C',R,'show',f'{rev}:{path}'],capture_output=True,text=True,check=True).stdout
src = show('2732ee6c06108c031c4d8043239b994e0504eb2f','tools/check-selftest-matcher-r51.py')
ns = {}
m = re.search(r"IDIOM_RE = re\.compile\(\n(.*?)\)\n", src, re.S)
committed = eval("re.compile(" + m.group(1) + ")")
unanch = re.compile(r'(?:printf|echo|cat)\b[^|\n]*\$\{?[A-Za-z_][A-Za-z0-9_]*\}?[^|\n]*\|\s*(?:grep\s+(?:-[A-Za-z]*q[A-Za-z]*|--quiet|--silent)\b|head\s+(?:-n\s*1\b|-1\b|-n1\b))')
def strip_comment(l):
    # conservative: drop a '#' comment that starts a word outside quotes (simple)
    out=[];q=None
    for i,c in enumerate(l):
        if q:
            if c==q: q=None
        elif c in '"\'': q=c
        elif c=='#' and (i==0 or l[i-1] in ' \t;'): break
        out.append(c)
    return ''.join(out)
cen = show(REV,'tools/tsukuroi-census.sh').split('\n')
print('census lines', len(cen))
l3495 = cen[3494]
print('L3495 committed match:', bool(committed.search(strip_comment(l3495))), '| unanchored match:', bool(unanch.search(strip_comment(l3495))))
hits_c=[i+1 for i,l in enumerate(cen) if committed.search(strip_comment(l))]
hits_u=[i+1 for i,l in enumerate(cen) if unanch.search(strip_comment(l))]
print('committed regex hits at rev census:', hits_c)
print('unanchored draft hits at rev census:', hits_u)
