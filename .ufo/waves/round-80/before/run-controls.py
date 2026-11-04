import importlib.util
import json
from pathlib import Path
import subprocess
import sys
R=Path(__file__).resolve().parents[4]
spec=importlib.util.spec_from_file_location('counter',R/'tools/measure-round80.py')
sys.path.insert(0,str(R/'tools')); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
before={p: (R/p).read_bytes() for p in [m.BEFORE+'expected.json',m.BEFORE+'systemd.service.xml','corpus/SOURCES.md','SKILL.md']}
positive=dict(before)
positive[m.NOTE]=before[m.BEFORE+'expected.json']
positive[m.COMPANION]=b'synthetic control, not admitted knowledge'
positive['corpus/SOURCES.md']=('| S330 | title '+json.loads(positive[m.NOTE])['url']+' | docs | A | scope | anchor | teaches | mined | 2026-11-04 | on-release | '+m.NOTE+' |\n').encode()
positive[m.REVIEW]=json.dumps({'artifact_sha256':m.sha(positive[m.NOTE]),'companion_sha256':m.sha(positive[m.COMPANION]),'verdicts':['holds']*6}).encode()
heading='## Gate and probe registry — round71 superseding current rows\n'
positive['SKILL.md']=(heading+'\n'.join('| '+n[:-3]+' | gate | `python3 tools/'+n+' --revision <REV>` | 0 clean; 1 failed; 2 could-not-evaluate; 3 self-test failed | `python3 tools/'+n+' --selftest` | p | isolated | tsukuroi |' for n in m.TOOLS)).encode()
for n in m.TOOLS:
    positive['tools/'+n]=b'--selftest SELFTEST synthetic fixture'
    positive['.ufo/waves/round-80/w1/'+n+'.receipt.json']=json.dumps({'tool_sha256':m.sha(positive['tools/'+n]),'argv':['python3','tools/'+n,'--selftest'],'rc':0,'passed':4,'failed':0}).encode()
def run(label,files,claim,want):
    def read(p):
        if p not in files: raise FileNotFoundError(p)
        return files[p]
    count,finding=m.evaluate(read,claim); rc=0 if count==(42 if claim=='C1' else 2) else 1
    return {'case':label,'claim':claim,'expected_rc':want,'rc':rc,'count':count,'finding':finding,'holds':rc==want}
rows=[]
for c in ['C1','C2']:
    rows += [run('do-nothing',before,c,1),run('positive',positive,c,0)]
f=dict(positive); del f[m.REVIEW]; rows.append(run('answer-copy-without-review',f,'C1',1))
f=dict(positive); f[m.REVIEW]=b'{"artifact_sha256":"forged"}'; rows.append(run('forged-review',f,'C1',1))
f=dict(positive); d=json.loads(f[m.NOTE]); d['rows'][0]['restart'][0]=True; f[m.NOTE]=json.dumps(d).encode(); rows.append(run('wrong-restart-cell',f,'C1',1))
f=dict(positive); f['SKILL.md']=f['SKILL.md'].replace(b'--selftest`',b'--other`'); rows.append(run('wrong-selftest-interface',f,'C2',1))
f=dict(positive)
for n in m.TOOLS: f['tools/'+n]+=b'changed'
rows.append(run('stale-selftest-receipt',f,'C2',1))
for c in ['C1','C2']:
    p=subprocess.run(['python3',str(R/'tools/measure-round80.py'),'--revision','467a9b7891a5939dab8460ec6f591fbb16bd82e9','--claim',c],capture_output=True,text=True)
    rows.append({'case':'actual-base','claim':c,'expected_rc':1,'rc':p.returncode,'stdout':p.stdout,'holds':p.returncode==1})
print(json.dumps({'base':'467a9b7891a5939dab8460ec6f591fbb16bd82e9','instrument_sha256':m.sha((R/'tools/measure-round80.py').read_bytes()),'results':rows,'met':all(r['holds'] for r in rows)},indent=2))
sys.exit(0 if all(r['holds'] for r in rows) else 1)
