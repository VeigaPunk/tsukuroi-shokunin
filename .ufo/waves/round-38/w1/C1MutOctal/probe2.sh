#!/usr/bin/env bash
# C1MutOctal: discriminate octal-8 vs decimal-10 inside bash arithmetic.
set -u
S=/fast/scratch/hyaku/tsukuroi-r38/C1MutOctal
OUT=$S/out
mkdir -p "$OUT"
{
  echo "bash=$BASH_VERSION path=$(type -P bash)"
  p() { local desc=$1 expr=$2 st=0; eval "$expr" || st=$?; if [ "$st" -eq 0 ]; then printf '%-30s TRUE  (status 0)\n' "$desc"; else printf '%-30s FALSE (status %s)\n' "$desc" "$st"; fi; }
  p '(( 010 == 8 ))'   '(( 010 == 8 ))'
  p '(( 010 == 10 ))'  '(( 010 == 10 ))'
  v=010; p 'v=010; (( v == 8 ))'  '(( v == 8 ))'
  v=010; p 'v=010; (( v == 10 ))' '(( v == 10 ))'
} > "$OUT/bash-octal-discriminator.txt" 2>&1
cat "$OUT/bash-octal-discriminator.txt"
