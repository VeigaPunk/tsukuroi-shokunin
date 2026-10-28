import importlib.util, os, re, sys
sys.argv=['x']
S='/fast/scratch/hyaku/tsukuroi-r51/R51CritCheatC2a'
import importlib.util
spec=importlib.util.spec_from_file_location('p', os.path.join(S,'propose.py'))
src=open(os.path.join(S,'propose.py')).read().split("census = open")[0]
ns={}; exec(compile(src,'p','exec'),ns)
idiom2_hits=ns['idiom2_hits']; M=ns['M']; PIPE=ns['PIPE']; CONS=ns['CONS']
cases = [
 ("emit \"$out\" | grep -q x", "function-producer (expected hole)"),
 ("printf '%s\\n' \"$out\" |grep -q x", "no space before grep"),
 ("printf '%s\\n' \"$out\"|grep -q x", "no spaces at pipe"),
 ("echo \"$out\" | grep -qF host", "echo + -qF"),
 ("printf '%s\\n' \"$out\" | grep -Fq host", "-Fq"),
 ("printf '%s\\n' \"$out\" | grep -F -e host -q", "-e then -q"),
 ("printf '%s\\n' \"$out\" | awk '{print; exit}'", "awk exit before END"),
 ("printf '%s\\n' \"$out\" | awk 'END{exit}'", "awk exit in END (harmless, expect 0)"),
 ("printf '%s\\n' \"$out\" | grep -c host", "grep -c full read (harmless, expect 0)"),
 ("printf '%s\\n' \"$out\" | sed -n 1p", "sed -n 1p (harmless, expect 0)"),
 ("printf '%s\\n' \"$out\" | grep -q host || true", "discarded status (exempt by design)"),
 ("x=$(printf '%s\\n' \"$out\" | head -n1)", "assignment head -n1 no || true (expect 1)"),
 ("elif ! printf '%s\\n' \"${out}\" | grep --quiet host; then", "braced var --quiet (expect 1)"),
 ("elif ! printf %s \"$out\" | grep -q host; then", "unquoted format (expect 1)"),
]
for c,desc in cases:
    print(len(idiom2_hits(c)), '|', desc, '|', c)
# producer-agnostic census scan: any early-exit consumer after any pipe
census=open(os.path.join(S,'census.sh'),encoding='utf-8',errors='replace').read()
agn=[]
for n,raw in enumerate(census.split('\n'),1):
    ln=M.strip_comment(raw)
    if re.search(r'\|\|\s*true\)*\s*$', ln): continue
    for m in PIPE.finditer(ln):
        if CONS.search(ln[m.end():]) and not re.search(r'<\(', ln[:m.start()]):
            agn.append((n, raw.strip()[:150])); break
print('producer-agnostic census hits:', len(agn))
for a in agn: print(a)
