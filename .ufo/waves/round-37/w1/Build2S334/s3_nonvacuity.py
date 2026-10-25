#!/usr/bin/env python3
"""Isolated regression for livefive's skip-work/vacuity defect.

Run: python3 s3_nonvacuity.py
No lane files are imported/executed and no host commands are spawned.
"""
import json
import pathlib
import tempfile


def livefive_after_channel(control, observed):
    """Current flawed policy: diffs are recorded, but waived for livefive."""
    parity_diffs = []
    if observed["git_execs"] != control["git_execs"]:
        parity_diffs.append("git_execs differs from control")
    evidence = []
    # Mirrors probe-child-env-allowlist-r36.py:1256-1257.
    if parity_diffs and observed["target_set"] != "livefive":
        evidence.extend(parity_diffs)
    return {"evidence": evidence, "leak": bool(evidence),
            "parity_diffs": parity_diffs}


def require_nonvacuous_channel(result):
    """Required harness invariant: each instrumented run actually executes a child."""
    if result["child_execs"] < 1:
        raise RuntimeError("instrumented channel executed no child")


def main():
    # Explicitly preserve the counterexample: baseline accepts an injection run in which
    # target exits normally without spawning. The after-state must reject before scoring.
    control = {"git_execs": 1}
    skipped = {"target_set": "livefive", "git_execs": 0, "child_execs": 0,
               "rc": 0, "source_findings": []}
    baseline = livefive_after_channel(control, skipped)
    assert baseline["parity_diffs"] == ["git_execs differs from control"]
    assert baseline["leak"] is False and baseline["evidence"] == []

    try:
        require_nonvacuous_channel(skipped)
    except RuntimeError as exc:
        after = {"rejected": True, "reason": str(exc), "child_execs": skipped["child_execs"]}
    else:
        raise AssertionError("non-vacuity guard accepted a no-child run")
    assert after["rejected"] and after["child_execs"] == 0

    # A real run remains admissible, including the legitimate live counter/parity drift:
    # child execution is required; parity itself is not reclassified as leak evidence.
    drift = {"target_set": "livefive", "git_execs": 0, "child_execs": 1, "rc": 0}
    require_nonvacuous_channel(drift)
    accepted = livefive_after_channel(control, drift)
    assert not accepted["leak"] and accepted["parity_diffs"]

    print(json.dumps({"baseline": baseline, "after_skipped": after,
                      "after_live_drift": {"admitted": True, **accepted}}, sort_keys=True))


if __name__ == "__main__":
    main()
