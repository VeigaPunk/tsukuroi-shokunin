S='/fast/scratch/hyaku/tsukuroi-r48/TRevCounterA'
src=open(S+'/counter.py').read()
patched=src.replace("'/tmp/","'"+S+"/e5/faketmp/").replace("== '/tmp'","== '"+S+"/e5/faketmp'")
open(S+'/counter-p.py','w').write(patched)
i=patched.find('startswith(')
print(patched[i-160:i+260])
