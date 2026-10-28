| id | spelling | idiom_sites (matcher) | 200KB first-line false misses /20 | mid-buffer /20 | hazard? |
|---|---|---|---|---|---|
| C0 | control: printf | grep -q | 1 | 20 | 20 | yes |
| S01 | producer through variable | 0 | 20 | 20 | yes |
| S02 | command printf | 0 | 20 | 20 | yes |
| S03 | builtin printf | 0 | 20 | 20 | yes |
| S04 | consumer in brace group | 0 | 20 | 20 | yes |
| S05 | process substitution | 0 | 0 | 0 | no |
| S06 | grep -E -q | 0 | 20 | 20 | yes |
| S07 | grep --quiet (control) | 1 | 20 | 20 | yes |
| S08 | grep -m1 | 0 | 20 | 20 | yes |
| S09 | sed -n 1p then grep -q | 0 | 0 | 20 | no |
| S10 | awk match-exit | 0 | 20 | 20 | yes |
| S11 | read -r (probe) | 0 | 20 | 20 | yes |
| S12 | head -c 64 then grep -q | 0 | 20 | 20 | yes |
| S13 | head --lines=1 then grep -q | 0 | 20 | 20 | yes |
| S14 | grep -e PAT -q (q after pattern) | 0 | 20 | 20 | yes |
| S15 | /usr/bin/grep -q | 0 | 20 | 20 | yes |
| S16 | command grep -q | 0 | 20 | 20 | yes |
| S17 | subshell consumer | 0 | 20 | 20 | yes |
| S18 | awk NR==1{exit} (probe) | 0 | 20 | 20 | yes |
| S19 | grep -m 1 (spaced) | 0 | 20 | 20 | yes |
| S20 | echo producer, grep -E -q | 0 | 20 | 20 | yes |
| S21 | timeout wrapper then grep -q | 0 | 20 | 20 | yes |
| S22 | head -n 1 then grep -q (control) | 1 | 20 | 20 | yes |
