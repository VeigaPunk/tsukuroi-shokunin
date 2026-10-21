## Attack

Attack the shared `tools/_revision.py` binding that the C1, C2, and C3 gate CLIs use. The assigned negative cases are falsifiable by calling `bind()` from a small scratch caller and checking that an unlanded commit, a revision on a wrong branch, a six-hex revision, a non-hex revision, and a missing branch produce a typed refusal rather than a landed binding. Since `_revision.py` itself has no binding CLI, the caller maps `RevisionError` to the gates' exit-2 CANNOT convention; the real gate CLIs were also exercised.

I also tested the stronger documented contract that a revision must be a commit ID and that ref names are rejected. A hex-shaped branch name is a counterexample: `rev-parse` resolves it as a ref, and the gate reports PASS for that ref's commit rather than refusing the supplied non-object revision.

## Method

Scratch clone: `/tmp/fxnegrev-8e591636`; no production files were edited. Clone route used the requested recipe through steps 1–5 and 7: cloned the lane, detached at `8e5916360f2dfe7bc4eb4ba144081af555900116`, set clone `refs/heads/master` to that tip, removed `origin`, then created an empty detached commit `f047bd7f17a0278397e1bec28a1aa582835f05bc`. I left `master` at the target tip (did not perform recipe step 6), so that commit remained unlanded. A `side-fixture` branch points to parent `7cc59c8e3761ffb668067c47655216376f0a4e48`, which does not contain the target tip. No origin ref remained, isolating local landing checks.

Commands and runs:

- `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/fxnegrev-8e591636`
- `git -C /tmp/fxnegrev-8e591636 checkout --detach 8e5916360f2dfe7bc4eb4ba144081af555900116`
- In the clone: `git update-ref refs/heads/master 8e5916360f2dfe7bc4eb4ba144081af555900116`; `git remote remove origin`; `git -c user.name=fixture -c user.email=fixture@local commit --allow-empty -m unlanded-fixture`; `git update-ref refs/heads/unlanded-fixture HEAD`; `git checkout --detach 8e5916360f2dfe7bc4eb4ba144081af555900116`; `git update-ref refs/heads/side-fixture 7cc59c8e3761ffb668067c47655216376f0a4e48`.
- `PYTHONDONTWRITEBYTECODE=1 python3 tools/_revision.py --selftest` in the clone; also probed `python3 tools/_revision.py 8e5916360f2dfe7bc4eb4ba144081af555900116` to establish the module has no direct binding CLI.
- `python3 /tmp/fxnegrev-scratch/fx_caller.py /tmp/fxnegrev-8e591636 /tmp/fxnegrev-scratch/cases-s1.json` called `bind()` for the rows below. The caller selects a random absent 40-hex and reports typed IDs, return class, and bound SHA.
- For every S1 case below, ran each gate with the exact argv form `python3 tools/<gate>.py --revision <case revision> --branch <case branch>` from the clone: `check-adjacency-anchors.py`, `check-boot-writers.py`, and `check-registry-coverage.py`. (The random-40 input was fresh per matrix runner.)
- Tested short-prefix shadowing by adding `refs/heads/f047bd7` pointing to the landed target tip, then ran `git rev-parse --verify --quiet 'f047bd7^{commit}'`, `git rev-parse --symbolic-full-name f047bd7`, the scratch caller, and the C2/C3 gate CLIs. Deleted the fixture ref afterward.
- Tested a 45-hex non-object ref (`deadbeefdeadbeefdeadbeefdeadbeefdeadbeefc0ffe`) and a 40-hex non-object ref (`0123456789abcdef0123456789abcdef01234567`), each pointing to the target tip; ran the caller and all three gate CLIs on the 45-hex input, then deleted both refs. Finally ran C3 with its claim-specific `--baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac` while the 45-hex ref existed, and deleted it.
- Read-only observations: `git -C /tmp/fxnegrev-8e591636 rev-list --count HEAD` returned `62`; `git -C /tmp/fxnegrev-8e591636 rev-parse --verify --quiet HEAD~1000` returned no SHA (exit 1). `sha256sum` of the clone's `tools/_revision.py` and `git show 8e5916360f2dfe7bc4eb4ba144081af555900116:tools/_revision.py | sha256sum` both returned `0a954400c536800af00f4fde979cc65aaa07e292e2f077349bb01f6bb5a1db59`.

## Verdict

REFUTE — C3, limited to the shared revision-input binding contract used by the C3 gate. The specified ordinary negative cases are refused correctly. However, a syntactically 45-hex input that names no Git object is accepted when a same-named branch exists, and the C3 gate emits PASS for the branch's commit. This contradicts the documented requirement that the revision name an explicit commit and that ref names be rejected. The C3 count result itself was observed as correct for the resolved target commit; this attack does not claim that its 14-tool baseline count is wrong.

## Evidence

- At `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/_revision.py:40-48`, `REV` validates only 7–64 hex characters and the typed refusal IDs are defined. At `:97-108`, `_commit()` resolves `f"{ref}^{{commit}}"` with `git rev-parse`; at `:134-154`, `bind()` checks that resolution and ancestry before returning a `Binding`.
- The documented contract at `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-boot-chain.py:33-38` says the revision is an explicit hex commit and ref names are rejected. C2 calls `bind()` at `:560-565` in `tools/check-boot-writers.py`; C3 calls it at `:290-294` in `tools/check-registry-coverage.py`.
- Clone fixture refs before the attacks: `git show-ref` printed `8e5916360f2dfe7bc4eb4ba144081af555900116 refs/heads/master`, `7cc59c8e3761ffb668067c47655216376f0a4e48 refs/heads/side-fixture`, and `f047bd7f17a0278397e1bec28a1aa582835f05bc refs/heads/unlanded-fixture`. The commit graph showed `f047bd7` as a child of `8e59163`, not an ancestor of `master`.
- `python3 tools/_revision.py --selftest` printed `REVISION_SELFTEST: PASS (39 cases, 39 passed, 0 failed)`. A direct invocation with a revision argument printed `usage: python3 tools/_revision.py --selftest (import bind() from the tools)` and exited 64; therefore exit 2 below is the gate/caller refusal convention, not this module's direct CLI.

S1 caller output, `label | revision | branch | exit | typed id` (three landed controls and 12 negative cases):

| label | revision (or fixture) | branch | caller exit | typed id |
|---|---|---|---:|---|
| landed-tip-control | `8e5916360f2dfe7bc4eb4ba144081af555900116` | master | 0 | OK |
| landed-short7-control | `8e59163` | master | 0 | OK |
| landed-parent-control | `7cc59c8e3761ffb668067c47655216376f0a4e48` | master | 0 | OK |
| random-40hex | `05de2e02ad0b9bb046b5ae35ce74e5f67b19068f` (absent object) | master | 2 | E-REVISION-INVALID |
| head-minus-1000 | `HEAD~1000` (unresolvable; also not hex syntax) | master | 2 | E-REVISION-INVALID |
| six-hex | `8e5916` | master | 2 | E-REVISION-INVALID |
| non-hex-token | `8e5916zz` | master | 2 | E-REVISION-INVALID |
| branch-name-as-revision | `master` | master | 2 | E-REVISION-INVALID |
| newline-suffixed-tip | target SHA plus LF | master | 2 | E-REVISION-INVALID |
| unlanded-descendant | `f047bd7f17a0278397e1bec28a1aa582835f05bc` | master | 2 | E-REVISION-NOT-LANDED |
| unlanded-short7 | `f047bd7` | master | 2 | E-REVISION-NOT-LANDED |
| wrong-branch-existing | target SHA | side-fixture | 2 | E-REVISION-NOT-LANDED |
| branch-missing | target SHA | nosuchbranch | 2 | E-BRANCH-MISSING |
| branch-missing-nested | target SHA | feature/x | 2 | E-BRANCH-MISSING |
| branch-invalid-range | target SHA | a..b | 2 | E-BRANCH-INVALID |

For all three gate CLIs over S1, the three landed controls returned `rc=0, status=PASS`; all 12 negative cases returned `rc=2, status=CANNOT_EVALUATE` with the same single expected ID in the table. `tools/check-registry-coverage.py` echoes the raw input in its `revision` field on CANNOT results; status and findings remained CANNOT/E-REVISION-INVALID (its output construction is at `:311-320`).

The short-prefix collision was reproduced with a local-only fixture branch:

```text
create refs/heads/f047bd7 -> 8e5916360f2dfe7bc4eb4ba144081af555900116: exit 0
rev-parse --verify --quiet 'f047bd7^{commit}': rc=0, 8e5916360f2dfe7bc4eb4ba144081af555900116
rev-parse --symbolic-full-name 'f047bd7': rc=0, refs/heads/f047bd7
  stderr: warning: refname 'f047bd7' is ambiguous.
bind('f047bd7', branch='master'): exit 0, OK, bound SHA 8e5916360f2dfe7bc4eb4ba144081af555900116
```

The full unlanded SHA still refused with E-REVISION-NOT-LANDED, while its seven-hex prefix was rebound to the hex-named ref. Both `check-boot-writers.py --revision f047bd7 --branch master` and `check-registry-coverage.py --revision f047bd7 --branch master` then returned `rc=0, status=PASS, revision=8e5916360f2dfe7bc4eb4ba144081af555900116`, with no findings.

The stronger ref-name reproduction used a 45-hex string that was absent from the object database before creating its branch:

```text
revision input: deadbeefdeadbeefdeadbeefdeadbeefdeadbeefc0ffe (45 hex; no object)
refs/heads/<that input> -> 8e5916360f2dfe7bc4eb4ba144081af555900116
rev-parse --verify --quiet '<input>^{commit}': rc=0, 8e5916360f2dfe7bc4eb4ba144081af555900116
bind(input, master): exit 0, OK, bound SHA 8e5916360f2dfe7bc4eb4ba144081af555900116
```

All three gate CLIs returned `rc=0, status=PASS` for that 45-hex input. With the same 45-hex branch fixture, the exact C3 path `python3 tools/check-registry-coverage.py --revision <45-hex-ref> --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac` returned exit 0 and:

```json
{"branch":"master","branch_tip":"8e5916360f2dfe7bc4eb4ba144081af555900116","counts":{"baseline_tools_missing":0,"baseline_tools_total":14,"discovered_tools":["tools/check-adjacency-anchors.py","tools/check-boot-writers.py","tools/check-registry-coverage.py"],"findings":0,"missing":0,"registered":17,"rows_total":17,"tools_total":17},"findings":[],"revision":"8e5916360f2dfe7bc4eb4ba144081af555900116","status":"PASS"}
```

A 40-hex non-object with a same-named branch behaved differently: `rev-parse --verify --quiet '<40-hex>^{commit}'` returned exit 1 and `bind()` returned exit 2/E-REVISION-INVALID. The temporary short-prefix, 45-hex, and 40-hex branch refs were deleted after their probes; post-delete checks showed the 45-hex and 40-hex names no longer resolved. Live lane ref listing showed only `refs/heads/master` and `refs/remotes/origin/master` in those namespaces, so the collision was not present in the live lane during this check.

## Residual

The bypass requires a ref whose exact name is a 7–64 hex string; no such head or remote-tracking ref appeared in the live lane listing. The tested 40-hex same-name ref did not bypass object resolution, but 7-hex prefix and 45-hex non-object names did. The raw `revision` echo on C3 CANNOT payloads remains non-certificate data because status is CANNOT_EVALUATE. No tools were installed. No host state, live-lane source files, sibling lanes, report files other than this one, or external state were changed. No build, lint, formatter, or general test suite was run; only the assigned helper and gate probes ran in the temporary clone.

Scope: executed=git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/fxnegrev-8e591636; git -C /tmp/fxnegrev-8e591636 checkout --detach 8e5916360f2dfe7bc4eb4ba144081af555900116; clone-only update-ref/remote-remove/empty-fixture-commit/checkout/update-ref commands listed in Method; PYTHONDONTWRITEBYTECODE=1 python3 tools/_revision.py --selftest; python3 tools/_revision.py 8e5916360f2dfe7bc4eb4ba144081af555900116; python3 /tmp/fxnegrev-scratch/fx_caller.py /tmp/fxnegrev-8e591636 /tmp/fxnegrev-scratch/cases-s1.json; S1 subprocess argv matrix for each of tools/check-adjacency-anchors.py, tools/check-boot-writers.py, tools/check-registry-coverage.py as listed in Evidence; short-prefix and 45-/40-hex ref probes and gate invocations listed in Evidence; python3 tools/check-registry-coverage.py --revision <45-hex-ref> --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac; fixture-ref deletion and read-only post-delete checks