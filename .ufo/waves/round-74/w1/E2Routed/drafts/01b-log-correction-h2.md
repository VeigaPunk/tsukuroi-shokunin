## Round 73 — instrument count correction (round 74, C2 routed repair; append-only)

R73-LOG-COUNT-STALE: The Round 73 entry above cited intermediate mid-wave selftest counts during instrument hardening:
a twelfth selftest case (12) for `tools/count-ul-rows-r73.py` and the checker growing to eleven cases (11)
for `tools/check-r72-routed-r73.py`.
The wave's subsequent close-out attacks (M1Mutation MAPLIST and TITLE-TOKEN) hardened both instruments to
their final committed states:
- `tools/count-ul-rows-r73.py`: final committed count is 13 cases (superseding the mid-wave count 12).
- `tools/check-r72-routed-r73.py`: final committed count is 14 cases (superseding the mid-wave count 11).
