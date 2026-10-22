#!/usr/bin/env python3
"""Record-level demonstration of a declaration-before-measurement rule.

Three rules, each refusable on a record:

R1  a declaration that records a run of the counting command before any commit
    of the round is a failure: the declared after-value was observed before the
    declaration landed.
R2  the round must have a measurement receipt commit strictly after the
    declaration commit.
R3  the commit that changes the counter under test must not be the declaration
    commit, so counter revision and declared target stay separable.

Reads a fixture of recorded facts. Exits 0 when every round passes, 1 otherwise.
This is a demonstrator, not a landed gate; it proves the rule can fail and can pass.
"""
import json
import sys

FIXTURE = "/fast/scratch/hyaku/tsuku28/ScribeMistake/order-fixture.json"


def check(round_rec):
    failures = []
    if round_rec["pre_declaration_run_recorded"]:
        failures.append("R1 pre-declaration run recorded")
    if not round_rec.get("first_measure_commit"):
        failures.append("R2 no measurement receipt commit after the declaration")
    if round_rec["counter_under_test_changed_in_declaration_commit"]:
        failures.append("R3 counter under test changed in the declaration commit")
    return failures


def main():
    rounds = json.load(open(FIXTURE))["rounds"]
    if len(sys.argv) > 1:
        want = int(sys.argv[1])
        rounds = [r for r in rounds if r["round"] == want]
    bad = 0
    for r in rounds:
        failures = check(r)
        verdict = "PASS" if not failures else "FAIL"
        print("round %d %s declaration=%s %s" % (r["round"], verdict, r["declaration_commit"],
                                                 "; ".join(failures) if failures else "all three rules hold"))
        bad += bool(failures)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
