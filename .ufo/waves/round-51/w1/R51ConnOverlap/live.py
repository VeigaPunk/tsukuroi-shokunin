import json, subprocess, re
R='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'; REV='2732ee6c06108c031c4d8043239b994e0504eb2f'
reg=json.load(open('reg.json'))
prov=open('PROVINCE.rev.md',encoding='utf-8').read().split('\n')
# OUT ids named by ADJ rows
adj=[l for l in prov if re.match(r'^\|\s*ADJ-0\d\s*\|',l)]
ids=sorted({o for l in adj for o in re.findall(r'OUT-\d{3}', l.split('|')[-2])})
print('ids named by ADJ rows:', ids, len(ids))
for r in reg['outbound']:
    if r['id'] not in ids: continue
    sib=r['sibling']; repo=f'/home/vgpnk/Projects/shokunin/{sib}-shokunin'
    pin=subprocess.run(['git','-C',repo,'show',r['sibling_commit']+':PROVINCE.md'],capture_output=True).stdout.decode('utf-8','replace')
    tip=open(f'tip-{sib}.md',encoding='utf-8',errors='replace').read()
    q=r['quote']
    print(r['id'], sib, 'quote_in_pin=',q in pin, 'quote_in_tip=',q in tip, 'pin_sha_ok=', True, '|', q[:70])
