import re,sys
sys.path.insert(0,'.')
src=open('matcher.py').read()
ns={}
exec(compile(src.split("def git(")[0].replace("import argparse","import argparse"),'m','exec'),ns)
IDIOM_RE=ns['IDIOM_RE']; strip=None
# re-define strip_comment and idiom_sites exactly as in matcher
exec("def strip_comment"+src.split("def strip_comment")[1].split("def selftest")[0], ns)
for n in ['frozen','base','r50']:
    t=open(f'census-{n}.sh',encoding='utf-8',errors='replace').read()
    hits=[]
    for i,ln in enumerate(t.split('\n'),1):
        if IDIOM_RE.search(ns['strip_comment'](ln)): hits.append((i,ln))
    print(n,'idiom_sites=',len(hits))
    for i,l in hits: print('   ',i,l)
