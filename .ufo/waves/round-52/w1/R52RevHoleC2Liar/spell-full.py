import os,pathlib,json,subprocess
S=pathlib.Path('/fast/scratch/hyaku/tsukuroi-r52/R52RevHoleC2Liar')
R=pathlib.Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-52/w1/R52RevHoleC2Liar')
L='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'; V='ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0'
rows=json.loads((R/'spellings.json').read_text())['rows']; text=(S/'tsukuroi-census.sh').read_text(); target="    elif ! out_has 'host=fixture-host'; then"
res={}
for row in rows:
 name=row['id']; fp=S/(name+'.sh'); fp.write_text(text.replace(target,row['line'],1))
 for counter in ['r51','r50']:
  if name == 'S01' and counter == 'r51':
   continue
  cmd=['python3',str(S/('check-selftest-matcher-'+counter+'.py')),'--revision',V,'--lane',L,'--census-file',str(fp),'--scratch',str(S/('full-'+name+'-'+counter)),'--runs','1']
  p=subprocess.run(cmd,capture_output=True,text=True,cwd=S,env={**os.environ,'TMPDIR':str(S)},timeout=1800)
  res[name+':'+counter]={'command':cmd,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
  (R/'spell-full.json').write_text(json.dumps(res,indent=2)+'\n')
  print(name,counter,p.returncode,p.stdout,flush=True)
