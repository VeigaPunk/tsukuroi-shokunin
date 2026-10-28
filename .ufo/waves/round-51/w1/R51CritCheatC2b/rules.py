import os
X='/fast/scratch/hyaku/tsukuroi-r51/R51CritCheatC2b/fx'
t=open(f'{X}/F2n-detector-neutered.sh',encoding='utf-8').read()
M1='  roll=$(worse "$roll" "$OOM_V")\n'; M1EQ='  roll=$(worse "$OOM_V" "$roll")\n'
M2='    DEGRADED) exit 1 ;;\n'; M2EQ='    DEGRADED) exit $((1)) ;;\n'
assert t.count(M1)==1 and t.count(M2)==1
t=t.replace(M1,M1EQ).replace(M2,M2EQ)
open(f'{X}/EQ-F2n-detector-neutered.sh','w',encoding='utf-8').write(t)
print('EQ-F2n written', t.count(M1EQ), t.count(M2EQ))
