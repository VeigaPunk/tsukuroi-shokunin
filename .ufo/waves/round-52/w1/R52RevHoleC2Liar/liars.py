import os, pathlib, subprocess, json
S=pathlib.Path('/fast/scratch/hyaku/tsukuroi-r52/R52RevHoleC2Liar')
R=pathlib.Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-52/w1/R52RevHoleC2Liar')
L='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
V='ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0'
fixtures={
 'five-line-liar': '#!/usr/bin/env bash\n# Reconstruction of requested minimal stdout-only liar, not claimed identical historical bytes.\nprintf "PASS selftest: fabricated (R50-C2)\\n"\nprintf "TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)\\n"\nexit 0\n',
 'historical-twelve-line-liar':pathlib.Path(L+'/.ufo/waves/round-50/w1/R50CritCheatC2/c-census.sh').read_text(),
 'selfcheck-liar':pathlib.Path(L+'/.ufo/waves/round-51/w1/R51RevC2/liar2.sh').read_text(),
}
results={}
for name,body in fixtures.items():
 fp=S/(name+'.sh'); fp.write_text(body)
 (R/(name+'.sh')).write_text(body)
 for counter in ['r51','r50']:
  cmd=['python3',str(S/('check-selftest-matcher-'+counter+'.py')),'--revision',V,'--lane',L,'--scratch',str(S/('single-'+name+'-'+counter)),'--census-file',str(fp),'--runs','1']
  p=subprocess.run(cmd,cwd=S,capture_output=True,text=True,env={**os.environ,'TMPDIR':str(S)},timeout=1800)
  obj={'command':cmd,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
  results[name+':'+counter]=obj
  (R/'liars.json').write_text(json.dumps(results,indent=2)+'\n')
  print(name,counter,p.returncode,p.stdout,flush=True)
