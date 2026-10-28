#!/bin/bash
set -u
REV=2732ee6c06108c031c4d8043239b994e0504eb2f
M=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-selftest-matcher-r51.py
S=/fast/scratch/hyaku/tsukuroi-r51/R51CritCheatC2b/s
X=/fast/scratch/hyaku/tsukuroi-r51/R51CritCheatC2b/fx
R=/fast/scratch/hyaku/tsukuroi-r51/R51CritCheatC2b/res
mkdir -p "$R"
summ() { python3 -c 'import json,sys; d=json.load(sys.stdin); print(json.dumps({k:d.get(k) for k in ["verdict","idiom_sites","base_misses","full_misses","cases","pass_runs","case_ok","mut_applied","mut_caught","error"]}, sort_keys=True)); print("mut:", [(m.get("mutation"),m.get("applied"),m.get("caught"),m.get("rc"),m.get("summary"),m.get("note")) for m in d.get("mut_detail",[])]); print("run:", [(r.get("rc"),r.get("summary")) for r in d.get("run_detail",[])])' 2>&1 || true; }
run() { # run NAME ENVPREFIX CENSUS_PATH
  echo "== $1"
  eval "$2 timeout 1800 python3 $M --revision $REV --scratch $S --census-file $3 --runs 1" > "$R/$1.json" 2>"$R/$1.err"
  echo "rc=$?"; summ < "$R/$1.json"
}
run REAL "" /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh
run F2-detector "" $X/F2-detector.sh
run F3-selfhash "" $X/F3-selfhash.sh
run F4-env-parent-CENSUS_MUTANT "CENSUS_MUTANT=M1" $X/F4-env.sh
run F5-name "" $X/F5-name.sh
run F2n-detector-neutered "" $X/F2n-detector-neutered.sh
run F3n-selfhash-neutered "" $X/F3n-selfhash-neutered.sh
run F5n-name-neutered "" $X/F5n-name-neutered.sh
run EQ-real "" $X/EQ-real.sh
echo DONE
