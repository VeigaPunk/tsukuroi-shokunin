import importlib.util,sys
sys.argv=['x']
sp=importlib.util.spec_from_file_location('c','/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-record-r44.py')
m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
cases={
'pad':'  ROW SR1 VERDICT: holds  ',
'blankprefix':'\nROW SR1 VERDICT: holds',
'contradict':'{"verdict_line":"ROW SR1 VERDICT: holds","verdict":"fails"}',
'dupkey':'{"verdict_line":"ROW SR1 VERDICT: fails","verdict_line":"ROW SR1 VERDICT: holds"}',
'dupverdict':'{"verdict_line":"ROW SR1 VERDICT: holds","verdict":"fails","verdict":"holds"}',
'retract':'ROW SR1 VERDICT: holds\nROW SR1 VERDICT: fails\n',
'crlf':'ROW SR1 VERDICT: holds\r\nx',
'jsonlist':'[{"verdict_line":"ROW SR1 VERDICT: holds"}]',
}
for k,v in cases.items(): print(k, repr(m.declared_line(v)))
print('fullmatch pad', m.VERDICT_RE.fullmatch(cases['pad']))
import json
def run(files):
    m.show=lambda lane,rev,p: files.get(p)
    try: return m.bound('L','R','w2','C2RevSR1','reviewer','SR1')
    except Exception as e: return 'CRASH %r'%e
W='.ufo/waves/round-44'
disp=json.dumps({'taskCall':{'tasks':[{'name':'C2RevSR1','agent':'reviewer'}]}}).encode()
def res(out): return json.dumps({'results':[{'name':'C2RevSR1','agent':'reviewer','output':out}]}).encode()
L='ROW SR1 VERDICT: holds'
base={W+'/w2-dispatch.json':disp,W+'/w2-results.json':res(L),W+'/w2/C2RevSR1.md':(L+'\nbody').encode()}
print('golden',run(base))
print('padded out',run({**base,W+'/w2-results.json':res('  '+L+'  ')}))
print('blank report',run({**base,W+'/w2/C2RevSR1.md':('\n\n'+L).encode()}))
print('dupkey',run({**base,W+'/w2-results.json':res('{"verdict_line":"ROW SR1 VERDICT: fails","verdict_line":"%s"}'%L)}))
print('results list',run({**base,W+'/w2-results.json':b'[1]'}))
print('dispatch list',run({**base,W+'/w2-dispatch.json':b'[1]'}))
print('crlf report',run({**base,W+'/w2/C2RevSR1.md':(L+'\r\nx').encode()}))
print('tasks str',run({**base,W+'/w2-dispatch.json':b'{"taskCall":{"tasks":[1]}}'}))
