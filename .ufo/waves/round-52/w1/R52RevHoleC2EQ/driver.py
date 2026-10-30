import os, sys, json, subprocess, hashlib, shutil, pathlib, time
L=pathlib.Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin')
R=L/'.ufo/waves/round-52/w1/R52RevHoleC2EQ'
S=pathlib.Path('/fast/scratch/hyaku/tsukuroi-r52/R52RevHoleC2EQ')
REV='ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0'
S.mkdir(parents=True,exist_ok=True); os.chdir(S); os.environ['TMPDIR']=str(S)
def blob(p):
 return subprocess.check_output(['git','-C',str(L),'show',f'{REV}:{p}'])
def run(name,cmd,env=None):
 start=time.time()
 for limit in (1800,3600):
  try:
   p=subprocess.run(cmd,cwd=S,env=env,capture_output=True,timeout=limit)
   (R/(name+'.json')).write_bytes(p.stdout); (R/(name+'.err')).write_bytes(p.stderr)
   meta={'command':cmd,'rc':p.returncode,'elapsed_seconds':round(time.time()-start,2),'timeout_seconds':limit}
   (R/(name+'.meta.json')).write_text(json.dumps(meta,indent=2)+'\n')
   print(name,p.returncode,p.stdout.decode(errors='replace')[-2000:],flush=True)
   return
  except subprocess.TimeoutExpired as e:
   (R/(name+f'.timeout-{limit}.txt')).write_text(str(e))
 raise RuntimeError('timed out twice: '+name)
try:
 meta={}
 for key,path in [('census','tools/tsukuroi-census.sh'),('matcher','tools/check-selftest-matcher-r51.py'),('scorer','tools/score-counter-cheats-r51.py')]:
  b=blob(path); dest=S/(key+('.sh' if key=='census' else '.py')); dest.write_bytes(b)
  (R/dest.name).write_bytes(b)
  meta[key]={'path':path,'sha256':hashlib.sha256(b).hexdigest(),'working_tree_sha256':hashlib.sha256((L/path).read_bytes()).hexdigest()}
 (R/'provenance.json').write_text(json.dumps({'revision':REV,'axes':['operability','C2','hole-rerun'],'blobs':meta},indent=2)+'\n')
 old=L/'.ufo/waves/round-51/w1/R51CritCheatC2b'
 recipe=(old/'gen.py').read_text().replace("SRC = '/fast/scratch/hyaku/tsukuroi-r51/R51CritCheatC2b/census-frozen.sh'",'SRC = '+repr(str(S/'census.sh'))).replace("OUT = '/fast/scratch/hyaku/tsukuroi-r51/R51CritCheatC2b/fx'",'OUT = '+repr(str(S/'fx')))
 exec(compile(recipe,'inherited-gen.py','exec'),{})
 t=(S/'fx/F2n-detector-neutered.sh').read_text(); t=t.replace('  roll=$(worse "$roll" "$OOM_V")\n','  roll=$(worse "$OOM_V" "$roll")\n').replace('    DEGRADED) exit 1 ;;\n','    DEGRADED) exit $((1)) ;;\n')
 (S/'fx/EQ-F2n-detector-neutered.sh').write_text(t)
 shutil.copytree(S/'fx',R/'fx',dirs_exist_ok=True)
 # Scorer has no --census-file interface: run its full built-in matrix at the freeze.
 run('score-freeze',[sys.executable,str(S/'scorer.py'),'--revision',REV,'--lane',str(L),'--scratch',str(S/'score')])
 names=['REAL','F1-canned-dead','EQ-F2-detector','EQ-F3-selfhash','EQ-F2n-detector-neutered','EQ-real','F2-detector','F3-selfhash','F4-env','F5-name','F2n-detector-neutered','F3n-selfhash-neutered','F5n-name-neutered']
 for name in names:
  cmd=[sys.executable,str(S/'matcher.py'),'--revision',REV,'--lane',str(L),'--scratch',str(S/'matches'),'--runs','1']
  if name!='REAL': cmd+=['--census-file',str(S/'fx'/(name+'.sh'))]
  env=os.environ.copy()
  if name=='F4-env': env['CENSUS_MUTANT']='M1'
  run(name,cmd,env)
 for name in ['F5n-name-neutered','F5-name','REAL']:
  d=S/('name-control-'+name); d.mkdir(); (d/'tmp-M1').mkdir(); (d/'home-M1').mkdir()
  shutil.copyfile(S/'census.sh' if name=='REAL' else S/'fx'/(name+'.sh'),d/'mut-M1.sh')
  run('name-control-'+name,['bash',str(d/'mut-M1.sh'),'--selftest'],{'PATH':'/usr/bin:/bin','LC_ALL':'C','TMPDIR':str(d/'tmp-M1'),'HOME':str(d/'home-M1')})
 (R/'COMPLETE.json').write_text(json.dumps({'completed':True,'revision':REV})+'\n')
finally:
 shutil.rmtree(S)
