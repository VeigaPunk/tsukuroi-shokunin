#!/usr/bin/env bash
# C1MutOctal: pin the exact bash parsing semantics the two mutants rely on.
set -u
S=/fast/scratch/hyaku/tsukuroi-r38/C1MutOctal
OUT=$S/out
mkdir -p "$OUT"
{
  echo "bash=$BASH_VERSION path=$(type -P bash)"
  p() { local desc=$1 expr=$2 st=0; eval "$expr" || st=$?; if [ "$st" -eq 0 ]; then printf '%-34s TRUE  (status 0)\n' "$desc"; else printf '%-34s FALSE (status %s)\n' "$desc" "$st"; fi; }
  p '[ "010" -gt 0 ]'   '[ "010" -gt 0 ]'
  p '[ "010" -eq 10 ]'  '[ "010" -eq 10 ]'
  p '[ "010" -eq 8 ]'   '[ "010" -eq 8 ]'
  p '[[ 010 =~ ^0+$ ]]' '[[ 010 =~ ^0+$ ]]'
  p '[[ 00 =~ ^0+$ ]]'  '[[ 00 =~ ^0+$ ]]'
  p '(( 010 > 0 ))'     '(( 010 > 0 ))'
  v=010; p 'v=010; (( v > 0 ))' '(( v > 0 ))'
  v=08;  p 'v=08; (( v > 0 ))'  '(( v > 0 ))'
  v=09;  p 'v=09; (( v > 0 ))'  '(( v > 0 ))'
  v=007; p 'v=007; (( v > 0 ))' '(( v > 0 ))'
  v=5;   p 'v=5; (( v > 0 ))'   '(( v > 0 ))'
  v=0;   p 'v=0; (( v > 0 ))'   '(( v > 0 ))'
} > "$OUT/bash-semantics.txt" 2>&1
cat "$OUT/bash-semantics.txt"
