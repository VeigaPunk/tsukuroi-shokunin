import os, json, importlib.util, shutil, sys
sys.dont_write_bytecode=True
S='/fast/scratch/hyaku/tsukuroi-r52/R52MutAdj'
os.environ['TMPDIR']=S+'/tmp'
spec=importlib.util.spec_from_file_location('driver',S+'/driver.py')
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
r=json.load(open(S+'/receipts/results.json'))
b=d.load_battery()
out={}
for name, obj in r['mutants'].items():
    path=d.git_clone(name)
    c3=path+'/'+d.C3_REL
    rows, seconds=d.run_battery(b,c3,'restored-'+name)
    out[name]={'restored_sha256':d.sha(c3),'equals_before':d.sha(c3)==r['frozen_counter_sha256'], 'rows':rows,'all_as_expected':all(x['as_expected'] for x in rows),'seconds':seconds}
    print(name,out[name]['equals_before'],out[name]['all_as_expected'],flush=True)
    shutil.rmtree(path)
with open(S+'/receipts/restored.json','w') as f:json.dump(out,f,indent=1)
print('RESTORED',len(out))
