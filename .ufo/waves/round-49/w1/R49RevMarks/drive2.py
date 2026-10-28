import json, os, subprocess
S=os.path.dirname(os.path.abspath(__file__)); LANE='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV='55c07cd3f8bff2e12117c34d57b4c618de74d85c'
import drive as D
e0=D.read('entry_freeze.md'); s0=D.read('skill_freeze.md'); r0=D.read('readme_freeze.md')
eA=e0.replace(D.E1_PENDING+'\n', D.E2_ADMITTED+'\n').replace(D.PENDING_SENT, D.E2B_BODY)
sA=s0.rstrip('\n')+'\n\n'+D.S1_HEAD+'\n\n'+D.S1_BODY+'\n'
V={}
V['W1_frozen_readme_with_admitted_entry']=(eA,sA,r0.rstrip('\n')+'\n')
V['W2_note_without_leadin_sentence']=(eA,sA,r0.rstrip('\n')+'\n\n## Round-49 coverage note\n\n'+D.R1+' '+D.R2+'\n')
V['W3_note_no_blank_para_after_table']=(eA,sA,r0.rstrip('\n')+'\n'+D.R1+' '+D.R2+'\n')
V['W4_readme_sentence_no_lead_in_period']=(eA,sA,r0.rstrip('\n')+'; '+D.R1+'\n')
V['W5_entry_body_keeps_pending_sentence']=(e0.replace(D.E1_PENDING+'\n', D.E2_ADMITTED+'\n'),sA,D.read('v_V1_admitted_note.readme.md'))
V['W6_skill_heading_with_trailing_em_space']=(eA,s0.rstrip('\n')+'\n\n'+D.S1_HEAD+'\u00a0\n\n'+D.S1_BODY+'\n', D.read('v_V1_admitted_note.readme.md'))
out={}
for n,(e,s,r) in V.items():
    ep,sp,rp=D.put('w_'+n+'.e.md',e),D.put('w_'+n+'.s.md',s),D.put('w_'+n+'.r.md',r)
    p=subprocess.run(['python3',os.path.join(S,'counter.py'),'--revision',REV,'--lane',LANE,'--no-base-check','--entry-file',ep,'--skill-file',sp,'--readme-file',rp],capture_output=True,text=True,cwd=S)
    o=json.loads(p.stdout)
    out[n]={'rc':p.returncode,'marks':o.get('marks'),'marks_ok':o.get('marks_ok'),'corr_ok':o.get('corr_ok')}
print(json.dumps(out,indent=1,sort_keys=True))
