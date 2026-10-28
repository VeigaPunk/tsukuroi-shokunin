#!/usr/bin/env bash
set -euo pipefail
gen() { awk -v n="$1" -v mode="$2" -v pos="$3" 'BEGIN{
  if (mode=="single") {
    half=int(n/2)
    if (pos=="start") { printf "midstream\n"; for(i=0;i<n;i++) printf "a"; }
    else if (pos=="end") { for(i=0;i<n;i++) printf "a"; printf "\nmidstream\n"; }
    else { for(i=0;i<half;i++) printf "a"; printf "\nmidstream\n"; for(i=0;i<n-half;i++) printf "b"; }
  } else {
    target=int(n/2); total=0; i=0; done=0
    while (total < n) {
      l=sprintf("line %06d abcdefghijklmnopqrstuvwxyz 0123456789 ABCDEFGHIJKLMNOPQRSTUVWXYZ", i)
      if (pos=="start" && i==0) { l="midstream"; }
      else if (pos=="middle" && !done && total>=target) { l="midstream"; done=1 }
      print l; total += length(l)+1; i++
    }
    if (pos=="end") print "midstream"
  }
}' ; }
run() { # run bytes mode pos iters
  local buf miss=0 hits=0
  buf=$(gen "$1" "$2" "$3")
  for i in $(seq "$4"); do
    if printf '%s\n' "$buf" | grep -qE 'midstream'; then hits=$((hits+1)); else miss=$((miss+1)); fi
  done
  printf 'bytes=%s mode=%s pos=%s iters=%s buflen=%s misses=%s hits=%s\n' "$1" "$2" "$3" "$4" "${#buf}" "$miss" "$hits"
}
run 98304 lines middle 200
run 98304 single middle 200
run 131072 lines middle 20
run 204800 single start 20
run 204800 single middle 20
run 204800 single end 20
run 204800 lines middle 20
