## Attack

Tested whether `events_total` can be reduced by deleting an event from the registry that the gate reads. The falsifiable pass-by-construction hypothesis was that the denominator comes from `doc["events"]`; if so, deleting EV-13 would reduce the reported total to 12 and might let the gate pass despite a captured write line without a registry claim.

Impacted axis: C2 depth, specifically the denominator's independence from the event-claim array. This does not attack C1 or C3. Smallest safe correction: none for this failure mode; retain the existing capture-enumeration denominator and registry-as-claims design.

## Method

Inspected the gate and registry, checked that the target commit's source and registry blobs match the inspected files, and ran the landed gate:

```text
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse 8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-boot-writers.py 8e5916360f2dfe7bc4eb4ba144081af555900116:corpus/knowledge/boot-writers-r19.json HEAD:tools/check-boot-writers.py HEAD:corpus/knowledge/boot-writers-r19.json
python3 tools/check-boot-writers.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116
```

The four object IDs were `b8e9c813538c5e76088cddf91cce95882c305983`, `78b63ab3aaa4db41347b4b02a42a99d968e2fab0`, then the same two IDs for HEAD. Baseline output: `PASS`, `events_total: 13`, `attributed_events: 13`, `unattributed: 0`.

Created an isolated clone under `/tmp`, checked out the target as local `master`, removed the last event row (EV-13), and committed the mutant:

```text
mktemp -d /tmp/tsukuroi-r19-c2-denom.XXXXXX
git clone --quiet --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsukuroi-r19-c2-denom.LogHXQ/repo && git -C /tmp/tsukuroi-r19-c2-denom.LogHXQ/repo checkout --quiet -B master 8e5916360f2dfe7bc4eb4ba144081af555900116 && git -C /tmp/tsukuroi-r19-c2-denom.LogHXQ/repo rev-parse HEAD
python3 -c 'import json; from pathlib import Path; p=Path("/tmp/tsukuroi-r19-c2-denom.LogHXQ/repo/corpus/knowledge/boot-writers-r19.json"); d=json.loads(p.read_text()); assert d["events"][-1]["id"] == "EV-13"; d["events"].pop(); p.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n"); print("events_remaining", len(d["events"]))' && git -C /tmp/tsukuroi-r19-c2-denom.LogHXQ/repo diff -- corpus/knowledge/boot-writers-r19.json
git -C /tmp/tsukuroi-r19-c2-denom.LogHXQ/repo add corpus/knowledge/boot-writers-r19.json && git -C /tmp/tsukuroi-r19-c2-denom.LogHXQ/repo -c user.name='Falsify Fixture' -c user.email='falsify-fixture@example.invalid' commit --quiet -m 'test: remove one boot-writer event row' && git -C /tmp/tsukuroi-r19-c2-denom.LogHXQ/repo rev-parse HEAD && git -C /tmp/tsukuroi-r19-c2-denom.LogHXQ/repo status --short
```
The first mutant-binding attempt was the same gate command shown below, run before establishing the scratch origin:

```text
python3 tools/check-boot-writers.py --revision 66f6377da59a319adbfeb04c9adc8e0fce12a291
```

Observed output: `{"branch":"master","branch_tip":null,"counts":{"attributed_events":0,"events_total":0,"unattributed":0,"writer_classes":0,"writers_with_events":0},"findings":[{"detail":"66f6377da59a is not an ancestor","id":"E-REVISION-NOT-PUSHED","site":"refs/remotes/origin/master"}],"revision":null,"status":"CANNOT_EVALUATE"}`; exit code 2. This binding failure did not evaluate the attack.

The mutation output was `events_remaining 12`; the diff removes only the EV-13 object. The first mutant run returned `E-REVISION-NOT-PUSHED` because the clone's original `origin/master` did not contain the new commit. To satisfy the gate's pushed-revision binding without touching the lane remote, I created a temporary bare remote, pushed the target then mutant to it, and fetched it as the clone's `origin`:

```text
git init --bare --quiet --initial-branch=master /tmp/tsukuroi-r19-c2-denom.LogHXQ/origin.git && git -C /tmp/tsukuroi-r19-c2-denom.LogHXQ/repo push --quiet /tmp/tsukuroi-r19-c2-denom.LogHXQ/origin.git 8e5916360f2dfe7bc4eb4ba144081af555900116:refs/heads/master && git -C /tmp/tsukuroi-r19-c2-denom.LogHXQ/repo push --quiet /tmp/tsukuroi-r19-c2-denom.LogHXQ/origin.git 66f6377da59a319adbfeb04c9adc8e0fce12a291:refs/heads/master && git -C /tmp/tsukuroi-r19-c2-denom.LogHXQ/repo remote set-url origin /tmp/tsukuroi-r19-c2-denom.LogHXQ/origin.git && git -C /tmp/tsukuroi-r19-c2-denom.LogHXQ/repo fetch --quiet origin && git -C /tmp/tsukuroi-r19-c2-denom.LogHXQ/repo rev-parse HEAD refs/remotes/origin/master
python3 tools/check-boot-writers.py --revision 66f6377da59a319adbfeb04c9adc8e0fce12a291
```

## Verdict

REFUTE — C2 pass-by-construction hypothesis. With the registry reduced to 12 event rows, the gate still reports `events_total: 13`, fails with 12 attributed and 1 unattributed, and identifies the remaining captured event at `host-capture-r19c.txt:20`. The denominator is independently derived from the capture probes, not the registry's event count.

## Evidence

- `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-boot-writers.py:393-415`: `event_sources` probes are matched against committed `capture_lines`; each matching physical `(capture, line)` is inserted into `enumerated`.
- `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-boot-writers.py:416-427` and `:436-481`: `doc["events"]` rows become claims checked against those enumerated locations; they do not generate locations.
- `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-boot-writers.py:483-508`: the gate walks `enumerated` to detect zero/multiple/valid claims, then assigns `events_total` as `len(enumerated)` at line 503.
- `8e5916360f2dfe7bc4eb4ba144081af555900116:corpus/knowledge/boot-writers-r19.json:18-28` declares the capture probes and match pattern; `:268-360` contains the 13 event claims.
- Baseline gate command and output in Method: PASS, 13 total / 13 attributed / 0 unattributed.
- Mutant commit `66f6377da59a319adbfeb04c9adc8e0fce12a291`: mutation command reports 12 event rows; its `git diff` removes the EV-13 row. Mutant gate output: `FAIL`, `events_total: 13`, `attributed_events: 12`, `unattributed: 1`, with `EVENT-UNATTRIBUTED` at `.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:20`.

## Residual

This attack establishes denominator provenance and the gate's response to one deleted claim. It does not independently establish that the committed captures are complete representations of host activity or re-adjudicate each writer attribution.

Scope: executed=`python3 tools/check-boot-writers.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116`; `python3 tools/check-boot-writers.py --revision 66f6377da59a319adbfeb04c9adc8e0fce12a291` (run twice: initial unbound attempt and final bound mutant run)
