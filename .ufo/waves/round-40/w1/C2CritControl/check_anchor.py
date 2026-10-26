import re, subprocess, sys
from pathlib import Path
LANE = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin')
def rows(text):
    for l in text.splitlines():
        if re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', l):
            c=[x.strip() for x in l.strip().strip('|').split('|')]
            yield c
def check(entry, sources, label):
    src_rows={c[0]:c for c in rows(sources)}
    print('==', label)
    for l in entry.splitlines():
        m=re.match(r'^\|\s*(EX\d+)\s*\|', l)
        if not m: continue
        c=[x.strip() for x in l.strip().strip('|').split('|')]
        rule,value,cell=c[1:4]
        ids=['S'+x for x in re.findall(r'\bS(\d{3,})\b', cell)]
        refs=[(f,int(a),int(b or a)) for f,a,b in re.findall(r'\b([A-Za-z_.0-9-]+):(\d+)(?:-(\d+))?', cell)]
        ok=[]
        for sid in ids:
            row=src_rows.get(sid)
            if not row: continue
            anchor=row[5]
            spans=[(int(a),int(b or a)) for a,b in re.findall(r'(\d+)-(\d+)', anchor)]
            ok.append((sid, spans))
        covered=[]
        for f,lo,hi in refs:
            for sid,spans in ok:
                if any(a<=lo and hi<=b for a,b in spans):
                    covered.append((f,lo,hi,sid))
        print(m.group(1), 'refs',refs,'anchor-covered',covered[:2])
print('done')
e=subprocess.run(['git','-C',str(LANE),'show','HEAD:corpus/knowledge/pacman-exec-environment-r40.md'],capture_output=True,text=True).stdout
s=subprocess.run(['git','-C',str(LANE),'show','HEAD:corpus/SOURCES.md'],capture_output=True,text=True).stdout
check(e,s,'author @f951f28')
