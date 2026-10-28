import re
Q45 = re.compile(r'^\*\*Quote\.\*\* `(S\d{3,})` ([A-Za-z0-9@._-]+):(\d+): "(.+)"\s*$')
QL = re.compile(r'^\*\*Quote\.\*\* `(S\d+)` ([^:]+):(\d+): "(.*)"\s*$')
lines = open('entry.md', encoding='utf-8').read().split('\n')
cur = None
for i, ln in enumerate(lines):
    if ln.startswith('## '):
        cur = ln.strip() if ln.strip() in ('## GR1','## GR2','## GR3') else None
    if cur:
        a = Q45.match(ln); b = QL.match(ln)
        if a or b:
            print(i+1, cur, 'r45' if a else '-', 'lint' if b else '-', ln[:160])
print('total quote-lines in GR rows:', sum(1 for ln in lines if ln.startswith('**Quote.**')))
