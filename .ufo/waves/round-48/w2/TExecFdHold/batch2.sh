#!/bin/bash
S=/fast/scratch/hyaku/tsukuroi-r48/TExecFdHold
cd "$S"
echo "### Re2: pipe@240 repeat (spaced)"
TMSET=1 ./run.sh Re2-240pipe-repeat ':; exec 240< <(sleep 120)'
echo "### R0b: baseline repeat (spaced, no pre-held fds)"
TMSET=1 ./run.sh R0b-baseline-repeat ':'
echo "### Rf: clean TMPDIR (unset) + fds 240..249 all pre-held"
./run.sh Rf-clean-all240to249 ':; exec 240</dev/null 241</dev/null 242</dev/null 243</dev/null 244</dev/null 245</dev/null 246</dev/null 247</dev/null 248</dev/null 249</dev/null'
echo "### Rg: clean TMPDIR (unset) + ulimit -n 200"
./run.sh Rg-clean-ulimit200 'ulimit -n 200'
echo "### Rh: spaced TMPDIR + ulimit -n 200"
TMSET=1 ./run.sh Rh-spaced-ulimit200 'ulimit -n 200'
echo "ALLDONE"
