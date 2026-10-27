import json, re, subprocess
CENSUS="/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
REAL="/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md"
FIX="/fast/scratch/hyaku/tsukuroi-r44/C2ExecFinalSources/fixture/lane/corpus/SOURCES.md"
base=open(REAL).read().splitlines(keepends=True)
def idx(lines,rid):
    for i,l in enumerate(lines):
        if re.match(r"^\s*\| *%s *\|"%rid,l): return i
    raise SystemExit("no row "+rid)
lines=list(base); i=idx(lines,"S245"); lines.pop(i)
open(FIX,"w").writelines(lines)
p=subprocess.run([CENSUS,"census","--file",FIX],capture_output=True,text=True)
real=subprocess.run([CENSUS,"census","--root","/home/vgpnk/Projects/shokunin","tsukuroi"],capture_output=True,text=True)
open(FIX,"w").writelines(base)
out={"fixture_census_rc":p.returncode,"fixture_census":p.stdout.strip().splitlines(),
     "real_census_rc":real.returncode,"real_census":real.stdout.strip().splitlines(),
     "stderr_fixture":p.stderr.strip(),"stderr_real":real.stderr.strip()}
open("census-sensitivity.json","w").write(json.dumps(out,indent=1))
