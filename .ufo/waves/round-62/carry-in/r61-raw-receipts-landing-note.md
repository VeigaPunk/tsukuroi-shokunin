# R61-RAW-RECEIPTS-UNLANDED — the twelve receipts land (round-62 carry-in)

The r61 non-author closure (`.ufo/waves/round-61` verifier spot-check, defect 1) found twelve raw
receipt files cited as landed evidence that were never committed: the nine
`.ufo/waves/round-61/driver-probes/` dq receipts (dq1, dq2, dq3, dq3b, dq4, dq4b, dq5a, dq5b, dq5c)
and the three `.ufo/waves/round-61/receipts/` run receipts (the `--due 2026-11-30` pass, the no-flag
shape pass, and `recheck-registry-FIRST-RUN-FAIL-at-authoring.txt`). They survived in the lane
worktree only; every "committed" statement about them was false on the r61 head `52d9ba1a` bytes.
This is the third occurrence of the lane's unlanded-receipt class
(D-R58-BEFORE-RECEIPTS-UNLANDED, r58; R59-GATE-FAIL-RECEIPT-UNLANDED, r59 — declared closed at r60;
R61-RAW-RECEIPTS-UNLANDED, r61).

Discharged here, round 62, first obligation before any claim: all twelve files land byte-identically
under their honest names (append-only; nothing substituted, nothing regenerated — the r60
regeneration pattern was NOT needed because the worktree originals survived). Pre-landing blob ids
(`git hash-object`, worktree bytes = landed bytes by treecommit construction):

    255a6c8465256e1d3fec9dc637dfad05ffbf025f  .ufo/waves/round-61/driver-probes/dq1-csv-inventory.txt
    8125295617c0d1bb03cf17071841bdb4a0f4491a  .ufo/waves/round-61/driver-probes/dq2-csv-verbose.txt
    181fd2c9194f1e96952691476647a1050df080a4  .ufo/waves/round-61/driver-probes/dq3-invalid-fo-value.txt
    c30a1008d801af0146e80b9d5e3534b803f9fdd7  .ufo/waves/round-61/driver-probes/dq3b-list-nh-invalid.txt
    6c09021fa43fcde5a59202fb81897f2ddda34c84  .ufo/waves/round-61/driver-probes/dq4-si-signed.txt
    d331566ab8146373dd167be762a9e4f84365e5c2  .ufo/waves/round-61/driver-probes/dq4b-v-si-invalid.txt
    40184b6c244cb35be6f1955c628b2ebfb65bf1c3  .ufo/waves/round-61/driver-probes/dq5a-bare-fo-mangled.txt
    6680b414b49c3121bbf5223aab09cbeb7bd48892  .ufo/waves/round-61/driver-probes/dq5b-double-slash-escape.txt
    96a7f8923ee50c770d5758ea750f39b6a1da5366  .ufo/waves/round-61/driver-probes/dq5c-noconv-nh.txt
    93fca6546d4e0becd88e9a06ae86f2600bc5a582  .ufo/waves/round-61/receipts/recheck-registry-10-due-2026-11-30.txt
    33b9ad52ec59c88579fae57966db6ba1a22064ef  .ufo/waves/round-61/receipts/recheck-registry-10-nodue-shape.txt
    c77eb3f25b608358b91b3ee43ef4674ca586e70e  .ufo/waves/round-61/receipts/recheck-registry-FIRST-RUN-FAIL-at-authoring.txt

The class rule (the r59 rule, restated at the third occurrence): **count the cited paths before
writing counts — a receipt count cited in a landed-changes table must equal the number of distinct
receipt paths the round's committed bytes name, and every one of them must be landed before the
round closes.** Landing is verified post-commit with plumbing only
(`git cat-file -e <sha>:<path>` per path; `git diff <base>..<new> --stat`).

The r61 DQ rows' 2026-11-30 recheck duty now has its committed comparison base: the note's
`recheck:` header points at `.ufo/waves/round-61/driver-probes/`, which is nine committed receipts
from this commit on.
