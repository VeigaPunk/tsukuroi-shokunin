2026-11-03T23:21:03Z

# E2Counter — scoped C1 counter and pre-data battery

Axes: depth / C1 evidence validity; predicate fidelity; false acceptance; read-only isolation.

## Changed surfaces

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/drafts/c2/count-kr-rows-r69.py`: Python stdlib-only, read-only Git revision and snapshot counter. No temporary files (TMPDIR is not overridden). Default lane is the enclosing repository; explicit `--lane` supports fixture clones. Snapshot defaults to the lane's frozen snapshot directory. Counts column-zero KR-prefixed lines outside backtick/tilde fences and verifies the frozen clauses. Duplicate identifiers invalidate every occurrence.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/probes/E2Counter/battery.txt`: control and five isolated malformed-fixture command/output/rc receipts.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/probes/E2Counter/control.txt`: independent retained copy of the control receipt.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/probes/E2Counter/outputs/`: individual fixture receipts, fixture notes, fixture registry, frozen snapshot copies, clone setup receipt, machine-readable results.

## Exact measured outcomes

Each value below is excerpted from its named receipt; each receipt includes the complete `$ python3 ... --revision ... --lane ... --snapshots ...` command, verbatim row outputs, and rc. All paths below are rooted at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/probes/E2Counter/outputs/`.

| Receipt | Verbatim summary excerpt | rc |
|---|---|---|
| control.txt | KR_ROWS=5 KR_VERIFIED=5 | 0 |
| duplicate.txt | KR_ROWS=5 KR_VERIFIED=3 | 1 |
| digest.txt | KR_ROWS=5 KR_VERIFIED=4 | 1 |
| quote.txt | KR_ROWS=5 KR_VERIFIED=4 | 1 |
| source.txt | KR_ROWS=5 KR_VERIFIED=4 | 1 |
| short.txt | KR_ROWS=5 KR_VERIFIED=4 | 1 |
| boilerplate.txt | KR_ROWS=6 KR_VERIFIED=6 | 0 |

The mandatory boilerplate rejection is NOT achieved. Six distinct rows containing `alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu` pass because their registered source, copied snapshot, authentic digest, and authentic quote satisfy every frozen clause. There is no frozen semantic relationship clause between statement and quote. Rejecting this fixture would extend the predicate, explicitly forbidden by this assignment. Counter retained unchanged rather than concealing the counterexample. Overall expected battery success is therefore **no** (`E2_SELFTEST_RC0=no`), not a claim that the lane selftest ran.

## Isolation and retained evidence

Only the assigned fixture battery was exercised; no lane census, lane selftest, build, formatter or lint ran. The real C1 note and tracked lane files were not written. Fixture commits occurred only inside the single shared scratch clone, after recording and asserting its repository root; complete commands remain in each receipt. The shell installed `trap 'rm -rf -- "$S"' EXIT` and finished normally, cleaning scratch after copying all cited inputs and outputs. Scratch commit objects are deliberately not retained; retained fixture notes, registry and snapshot copies allow reconstruction without claiming those objects remain reachable. No host probe, package operation, installation, service action or credential access occurred. No LSP tool is mounted in this seat; no supported symbol operation was attempted or claimed.

## Risks / parent action

Frozen-predicate blocker: boilerplate acceptance is demonstrated, not remediable without changing the frozen clauses. Parent must retain this failed expectation in the round decision. Parent owns integration gates; none are asserted passed here. Missing-revision / unreadable-registry / missing-snapshot-dir exit paths and fence-edge adversarial cases are implemented but were not separately exercised by this assigned battery.

Self-evaluation: accuracy good (retained exact receipts); completeness limited by contradictory boilerplate-rejection requirement; clarity good (failure explicit); actionability good (draft plus reconstructible fixture inputs); conciseness good (single scoped report). Improvement requires parent authority to amend a future predicate, not an unauthorized semantic filter now.

E2_CONTROL=5 E2_DUP=3 E2_DIGEST=4 E2_QUOTE=4 E2_SOURCE=4 E2_SHORT=4 E2_BOILERPLATE=6 E2_SELFTEST_RC0=no
