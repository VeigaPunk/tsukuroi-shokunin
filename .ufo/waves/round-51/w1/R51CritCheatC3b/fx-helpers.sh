S=/fast/scratch/hyaku/tsukuroi-r51/R51CritCheatC3b
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
R=2732ee6c06108c031c4d8043239b994e0504eb2f
FX=$S/fx; O=$S/out; mkdir -p $O
R51=$LANE/tools/check-adjacency-table-r51.py
GC="-c user.name=fixture -c user.email=fixture@invalid"
assert_top(){ [ "$(git -C "$1" rev-parse --show-toplevel)" = "$1" ] || { echo "TOPLEVEL MISMATCH $1"; exit 9; }; }
