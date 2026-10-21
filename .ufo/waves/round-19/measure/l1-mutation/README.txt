L1 contingency mutation receipts (attempt 2), produced on /tmp clones of 044ab28
with no write to the lane. These are L1-side fail-capability probes retained in
case the falsify wave cannot be dispatched; a dispatched wave re-does them
independently and its reports supersede nothing here.

clone: git clone --no-hardlinks <lane> /tmp/r19-l1mut; checkout --detach 044ab28;
update-ref refs/heads/master 044ab28; remote remove origin.

1) boot-writers: delete the last event row from corpus/knowledge/boot-writers-r19.json,
   commit mutant, bind mutant -> FAIL, attributed_events 12 / events_total 13,
   EVENT-UNATTRIBUTED. Denominator stayed 13, so events_total is capture-derived,
   not registry-derived.
2) adjacency-anchors: flip one DRIFTED record to RESOLVES and move found_line into
   target_ranges, commit, bind -> FAIL exit 1, INBOUND-CLASSIFICATION-WRONG
   (counts DRIFTED 16 / RESOLVES 97). Output: mut-adj.out.
3) registry-coverage: delete the `| revision-binder |` row from SKILL.md, commit,
   bind with --baseline-tools 452a054 -> FAIL exit 1, baseline_tools_missing 1,
   REGISTRY-ROW-MISSING tools/_revision.py. Output: mut-reg.out.
