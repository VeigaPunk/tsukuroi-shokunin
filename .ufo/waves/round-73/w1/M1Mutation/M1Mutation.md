status: done
verdict: 38 mutants (21 counter + 17 routed checker), 6 survivors (4 C1 dead/entailed/crashing clauses, 2 C2 redundant/entailed); both frozen instruments are clause-separable; frozen C1 reads met=1 and frozen C2 reads ROUTED_STALE=0 at HEAD 3efb9b24

# M1Mutation — seat binding, round 73 w1

Clause-isolated mutant batteries against the two frozen instruments. Full deliverable:
`.ufo/waves/round-73/w1/M1Mutation/report.md` (trailer path `.ufo/waves/round-73/w1/M1Mutation.md`).

Headline: committed selftests kill 9/21 counter mutants and 0/17 checker mutants;
clause-isolated fixtures kill 32/38 outright plus 1 token-level; 6 true survivors,
all dead/entailed clauses (own-work arm, map-url, quote-pipe, snapshots conjunct,
item-heading anchor, lesson need_any). Real defects found: non-string map URL crashes
the counter (rc 1 traceback) and a finding id placed only in a block heading passes
the routed checker (frozen and committed final). Raw matrices: `counter_matrix.json`,
`c2_matrix.json`; harness: `battery.py`, `repro.sh`.
