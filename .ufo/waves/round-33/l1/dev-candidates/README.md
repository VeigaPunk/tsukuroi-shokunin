# Round 33 — L1 development runs of the C1 probe at the base (before the declaration commit)

All runs at claim base `1f521b93387590666bfbe7534708d8f416898424`, from the uncommitted working-copy probe while it was being written; none is a claim receipt.

- `<tool>.jsonl` / `.err`: candidate discovery, one target per run (`--only`), probe draft with the names channel and value channel only (04:51Z). Five candidates run (control rc 0, git children started); ten are harness errors at the base (nine selftests start no git child; `check-appended-notices.py --selftest` exits 1 under the control environment). The five became the frozen `CLAIM_TARGETS`.
- `claim-base.*`: a cancelled earlier full run (draft without quiet/source channels).
- `claim-base3.*`: full claim set with the names, quiet and source channels, before the source channel gained the hiding-construct rules: 15 of 15 leaking, no parity difference in any run, exit 1.
- `r32-w1-context.txt`: the round-32 wave-1 context, kept as the template for this round's wave contexts.
