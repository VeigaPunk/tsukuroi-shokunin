## Attack

C2 (depth): challenge the boot-writer gate's ability to reject a missing attribution, a false published writer mechanism, a corrupt capture digest, and a new unclaimed event. The bounded hypothesis under test is the assignment's “each must be red”; this is not an admission judgment or an assertion that the pristine attribution is false.

Axes named: **event completeness**, **published mechanism fidelity**, **capture integrity**, **new-event sensitivity**, and **host/write-scope safety**. Every mutant starts from restored pristine file bytes; no surviving defect was retained.

Target: `8e5916360f2dfe7bc4eb4ba144081af555900116`. Isolated clone: `/tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv`. No production edit, host probe, service action, package transaction, boot action, or subagent dispatch was performed. The only lane write is this requested report. Tool installs/updates: none.

## Method

Used the committed-object route; it worked. No external `--registry` route was attempted. The gate reads committed blobs, not worktree files (`8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-boot-writers.py:104-146,560-582`). `--registry` is documented and validated as a safe lane-relative JSON path, not an external absolute path (`8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-boot-writers.py:537-540,565-568`).

Preparation, exactly as run (the four git operations were chained with `&&`):

```sh
mktemp -d /tmp/tsukuroi-r19-fxmutwriters-8-XXXXXX
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv && git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv checkout --detach 8e5916360f2dfe7bc4eb4ba144081af555900116 && git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv update-ref refs/heads/master 8e5916360f2dfe7bc4eb4ba144081af555900116 && git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv remote remove origin
```

Actual preparation output: mktemp returned `/tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv`; clone printed `Cloning into '/tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv'...` and `done.`; checkout printed `HEAD is now at 8e59163 checkpoint(r19): retain developed verification evidence for resume; admission pending`; update-ref and remote removal were silent successes.

Commands after preparation ran with cwd `/tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv`. The initial pristine measurement was:

```sh
sha256sum corpus/knowledge/boot-writers-r19.json corpus/knowledge/boot-writers-r19.md tools/check-boot-writers.py
python3 tools/check-boot-writers.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116
```

Initial gate exit: **0**, output:

```json
{"branch":"master","branch_tip":"8e5916360f2dfe7bc4eb4ba144081af555900116","counts":{"attributed_events":13,"events_total":13,"unattributed":0,"writer_classes":7,"writers_with_events":3},"findings":[],"revision":"8e5916360f2dfe7bc4eb4ba144081af555900116","status":"PASS"}
```

For each mutation, a surgical file edit was followed by `sha256sum`, the fixture-identity `git commit -am` shown in the transcript below, `git rev-parse HEAD`, updating clone `refs/heads/master` to that exact SHA, then `python3 tools/check-boot-writers.py --revision <that SHA>`. Every subprocess was bounded to 90 seconds. Restorations were separately committed, branch-bound, hashed, and passed through the identical detector before the next mutation. No detector code was modified.

Independent edits:

1. **M1 — remove EV-01:** delete only the JSON event object at `8e5916360f2dfe7bc4eb4ba144081af555900116:corpus/knowledge/boot-writers-r19.json:269-275`; leave the capture and Markdown unchanged. Expected detector: `EVENT-UNATTRIBUTED`, nonzero.
2. **M2 — corrupt the published mechanism:** in `corpus/knowledge/boot-writers-r19.md:15`, change only the inline quoted `ExecStopPost=limine-snapper-sync` to `ExecStartPost=limine-snapper-sync`. This changes the claimed execution phase and contradicts the cited committed capture line, `8e5916360f2dfe7bc4eb4ba144081af555900116:.ufo/waves/round-19/l1-capture/host-capture-r19.txt:260`. The JSON writer ID and valid registry mechanism reference are intentionally unchanged. Expected detector: a mechanism/prose mismatch finding and nonzero; no existing finding ID for this Markdown semantic check was assumed.
3. **M3 — corrupt a capture SHA-256:** at `corpus/knowledge/boot-writers-r19.json:7`, change the first nibble of the recorded capture digest from `d` to `0`, leaving a syntactically valid 64-character digest and unchanged capture bytes. Expected detector: `CAPTURE-TAMPERED`, nonzero integrity rejection.
4. **M4 — new unclaimed capture event:** insert the following single line at `.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:21`, immediately before the declared journal probe's `[rc=0]` terminator; retain all old event locations. Recompute the capture SHA-256 and update only its registry digest at `corpus/knowledge/boot-writers-r19.json:15` to `19a9282c0e6ddefee5f5e239157dec73dc1dd9f11f9351860e6564e2f42c50c4`; leave all 13 event claims unchanged. Expected detector: `EVENT-UNATTRIBUTED`, nonzero.

```text
2026-10-20T17:08:00 424242 limine-snapper- snapper-cleanup.service /system.slice/snapper-cleanup.service Updated: /boot/limine.conf
```

## Verdict

**REFUTE / C2 — bounded “all four must be red” detector-sensitivity expectation.** The published-mechanism mutant **survived**. The missing-event and extra-event mutants were **killed** with exit 1. The digest mutant was **killed by the integrity guard** with exit 2 (`CANNOT_EVALUATE`), not a semantic `FAIL`. All pristine/restored runs were green; there was no baseline-failure inconclusiveness.

| Case | Mutant commit | Actual status / exit | Exact finding ID(s) | Counts attributed / total / unattributed | Mutation result |
|---|---|---|---|---|---|
| M1 remove EV-01 | `0750db0d241d51f0ef8f9c2d87d4ff6c19fd60bf` | FAIL / 1 | `EVENT-UNATTRIBUTED` | 12 / 13 / 1 | Killed |
| M2 false Markdown mechanism | `622b95b2fe6d91f5868317473c6b74a3ad228221` | PASS / 0 | none (`findings: []`) | 13 / 13 / 0 | **Survived** |
| M3 corrupt capture digest | `d9fae26b49eaf4222d22e1fc46254e1b374aa436` | CANNOT_EVALUATE / 2 | `CAPTURE-TAMPERED` | 0 / 0 / 0 (evaluation stops at integrity) | Killed at integrity boundary |
| M4 extra event plus correct updated digest | `428bc14e2dcb50e76b4d9f26ced3a0369ab92c8b` | FAIL / 1 | `EVENT-UNATTRIBUTED` | 13 / 14 / 1 | Killed |

M2 is a coverage finding, not permission to weaken the contract. It establishes that green C2 gate output does not certify the accuracy of the mechanism wording published in the Markdown entry. It does not refute the unmodified entry's actual facts or judge round admission.

## Evidence

### Actual bounded detector outputs

Pristine output appears in Method. Mutant and restored outputs follow verbatim, with actual exits.

M1 mutant:

```sh
python3 tools/check-boot-writers.py --revision 0750db0d241d51f0ef8f9c2d87d4ff6c19fd60bf
```

Exit **1**:

```json
{"branch":"master","branch_tip":"0750db0d241d51f0ef8f9c2d87d4ff6c19fd60bf","counts":{"attributed_events":12,"events_total":13,"unattributed":1,"writer_classes":7,"writers_with_events":3},"findings":[{"detail":"enumerated /boot/limine.conf write line has no event claim","id":"EVENT-UNATTRIBUTED","site":".ufo/waves/round-19/l1-capture/host-capture-r19b.txt:1695"}],"revision":"0750db0d241d51f0ef8f9c2d87d4ff6c19fd60bf","status":"FAIL"}
```

M1 restored bytes:

```sh
python3 tools/check-boot-writers.py --revision c153c702a7f18044981590a882a39027d9fcce66
```

Exit **0**:

```json
{"branch":"master","branch_tip":"c153c702a7f18044981590a882a39027d9fcce66","counts":{"attributed_events":13,"events_total":13,"unattributed":0,"writer_classes":7,"writers_with_events":3},"findings":[],"revision":"c153c702a7f18044981590a882a39027d9fcce66","status":"PASS"}
```

M2 mutant:

```sh
python3 tools/check-boot-writers.py --revision 622b95b2fe6d91f5868317473c6b74a3ad228221
```

Exit **0**:

```json
{"branch":"master","branch_tip":"622b95b2fe6d91f5868317473c6b74a3ad228221","counts":{"attributed_events":13,"events_total":13,"unattributed":0,"writer_classes":7,"writers_with_events":3},"findings":[],"revision":"622b95b2fe6d91f5868317473c6b74a3ad228221","status":"PASS"}
```

M2 restored bytes:

```sh
python3 tools/check-boot-writers.py --revision d95ce9690c983debc92e807ffd0c58ae356335c6
```

Exit **0**:

```json
{"branch":"master","branch_tip":"d95ce9690c983debc92e807ffd0c58ae356335c6","counts":{"attributed_events":13,"events_total":13,"unattributed":0,"writer_classes":7,"writers_with_events":3},"findings":[],"revision":"d95ce9690c983debc92e807ffd0c58ae356335c6","status":"PASS"}
```

M3 mutant:

```sh
python3 tools/check-boot-writers.py --revision d9fae26b49eaf4222d22e1fc46254e1b374aa436
```

Exit **2**:

```json
{"branch":"master","branch_tip":"d9fae26b49eaf4222d22e1fc46254e1b374aa436","counts":{"attributed_events":0,"events_total":0,"unattributed":0,"writer_classes":0,"writers_with_events":0},"findings":[{"detail":"sha256 expected 0060de16892fbcb3ca85f45e28a94c9b6ef818c20029d91e05fa9459bbbde32b, observed d060de16892fbcb3ca85f45e28a94c9b6ef818c20029d91e05fa9459bbbde32b","id":"CAPTURE-TAMPERED","site":".ufo/waves/round-19/l1-capture/host-capture-r19.txt"}],"revision":"d9fae26b49eaf4222d22e1fc46254e1b374aa436","status":"CANNOT_EVALUATE"}
```

M3 restored bytes:

```sh
python3 tools/check-boot-writers.py --revision c009a51cbea718b1bce7c61f3108a9e1033bc209
```

Exit **0**:

```json
{"branch":"master","branch_tip":"c009a51cbea718b1bce7c61f3108a9e1033bc209","counts":{"attributed_events":13,"events_total":13,"unattributed":0,"writer_classes":7,"writers_with_events":3},"findings":[],"revision":"c009a51cbea718b1bce7c61f3108a9e1033bc209","status":"PASS"}
```

M4 mutant:

```sh
python3 tools/check-boot-writers.py --revision 428bc14e2dcb50e76b4d9f26ced3a0369ab92c8b
```

Exit **1**:

```json
{"branch":"master","branch_tip":"428bc14e2dcb50e76b4d9f26ced3a0369ab92c8b","counts":{"attributed_events":13,"events_total":14,"unattributed":1,"writer_classes":7,"writers_with_events":3},"findings":[{"detail":"enumerated /boot/limine.conf write line has no event claim","id":"EVENT-UNATTRIBUTED","site":".ufo/waves/round-19/l1-capture/host-capture-r19c.txt:21"}],"revision":"428bc14e2dcb50e76b4d9f26ced3a0369ab92c8b","status":"FAIL"}
```

M4 restored bytes:

```sh
python3 tools/check-boot-writers.py --revision fcfbfe73ddd45ebaaaad209d204776652ee449e3
```

Exit **0**:

```json
{"branch":"master","branch_tip":"fcfbfe73ddd45ebaaaad209d204776652ee449e3","counts":{"attributed_events":13,"events_total":13,"unattributed":0,"writer_classes":7,"writers_with_events":3},"findings":[],"revision":"fcfbfe73ddd45ebaaaad209d204776652ee449e3","status":"PASS"}
```

### Source-backed trust boundary

- Publication checks for writers and events are substring presence of their IDs in the knowledge entry (`8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-boot-writers.py:333-340,474-478`). Registry mechanism references are validated against capture lines (`8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-boot-writers.py:345-357`); the text of Markdown line 15 is not compared. This explains M2's observed green output without inventing a detector failure.
- Capture bytes are taken from the registry revision and checked against the digest supplied by that same registry (`8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-boot-writers.py:245-266`). Event enumeration trusts registry-declared `event_sources.capture`, exact `$ <probe>` string, and `pattern`; only matching lines before the next `[rc=` are enumerated (`8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-boot-writers.py:380-414`). There is no claim here of independent capture authenticity.
- **M4 was visible.** Its updated correct digest passed the integrity layer, event count increased from 13 to 14, and the gate emitted `EVENT-UNATTRIBUTED` at `.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:21`. The no-claim check is at `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-boot-writers.py:483-490`. It did not trust the 13-item registry event list as the complete count.

### Before / mutated / restored SHA-256

Hashes were measured with the `sha256sum` commands in the execution transcript. Every restoration reproduced these pristine hashes:

| File | Pristine and each restored hash |
|---|---|
| `corpus/knowledge/boot-writers-r19.json` | `d9db10d00c9424f9ccf5b35e97a27f0f770b5a0dbfc7fdb229dce4892c3e7413` |
| `corpus/knowledge/boot-writers-r19.md` | `80ab81def8cddc98077f9ce2a51cfdee40e534cbc1961a78e6b5931c44d9d8d8` |
| `.ufo/waves/round-19/l1-capture/host-capture-r19c.txt` | `669cada8c08e00cae06b1429f81f254a744f3a7a1d6fe684592fbe202dea298d` |
| `tools/check-boot-writers.py` (never edited) | `69d258e340d87ab6966251ebed52b737c67de37b320be0ea91f828c94f00c40c` |

| Case | Changed file | Mutated hash | Restored hash |
|---|---|---|---|
| M1 | `corpus/knowledge/boot-writers-r19.json` | `bd91f7f0bb4594385f1f1662b10d8693b432752c1e2aa3abbe3144627fdc2d19` | `d9db10d00c9424f9ccf5b35e97a27f0f770b5a0dbfc7fdb229dce4892c3e7413` |
| M2 | `corpus/knowledge/boot-writers-r19.md` | `db927929023e98c8b843dfbd12c374fd75d3880ca447cbc25819d5241455871e` | `80ab81def8cddc98077f9ce2a51cfdee40e534cbc1961a78e6b5931c44d9d8d8` |
| M3 | `corpus/knowledge/boot-writers-r19.json` | `296c37fbeb7ea95c07a1ea1f30a59c6ba402ee3d37007b314325a18db5a8689a` | `d9db10d00c9424f9ccf5b35e97a27f0f770b5a0dbfc7fdb229dce4892c3e7413` |
| M4 | `corpus/knowledge/boot-writers-r19.json` | `cd2a76c7938b39cf32e0eabccb1f51dd240d3e0e8a8d9faadd757068ae565840` | `d9db10d00c9424f9ccf5b35e97a27f0f770b5a0dbfc7fdb229dce4892c3e7413` |
| M4 | `.ufo/waves/round-19/l1-capture/host-capture-r19c.txt` | `19a9282c0e6ddefee5f5e239157dec73dc1dd9f11f9351860e6564e2f42c50c4` | `669cada8c08e00cae06b1429f81f254a744f3a7a1d6fe684592fbe202dea298d` |

M3's capture file itself remained `d060de16892fbcb3ca85f45e28a94c9b6ef818c20029d91e05fa9459bbbde32b`; only the registry's expected digest was corrupted. Final restored clone commit: `fcfbfe73ddd45ebaaaad209d204776652ee449e3`. Its detector exit was 0, `findings: []`, 13/13 attributed, 7 writer classes. The exact production file bytes were restored in the scratch copy; temporary fixture commit history remains local to that disposable clone.

### Exact subprocess transcript after initial green

The transcript records every subsequent actual command, exit, stdout and any stderr. File edits were performed through the surgical edit tool as specified in Method; no script or fixture file was added.

```text
$ sha256sum corpus/knowledge/boot-writers-r19.json corpus/knowledge/boot-writers-r19.md .ufo/waves/round-19/l1-capture/host-capture-r19c.txt tools/check-boot-writers.py
bd91f7f0bb4594385f1f1662b10d8693b432752c1e2aa3abbe3144627fdc2d19  corpus/knowledge/boot-writers-r19.json
80ab81def8cddc98077f9ce2a51cfdee40e534cbc1961a78e6b5931c44d9d8d8  corpus/knowledge/boot-writers-r19.md
669cada8c08e00cae06b1429f81f254a744f3a7a1d6fe684592fbe202dea298d  .ufo/waves/round-19/l1-capture/host-capture-r19c.txt
69d258e340d87ab6966251ebed52b737c67de37b320be0ea91f828c94f00c40c  tools/check-boot-writers.py
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv -c user.name=fixture -c user.email=fixture@local commit -am mutant-1-remove-EV-01
[detached HEAD 0750db0] mutant-1-remove-EV-01
 1 file changed, 7 deletions(-)
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv rev-parse HEAD
0750db0d241d51f0ef8f9c2d87d4ff6c19fd60bf
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv update-ref refs/heads/master 0750db0d241d51f0ef8f9c2d87d4ff6c19fd60bf
EXIT=0
$ python3 tools/check-boot-writers.py --revision 0750db0d241d51f0ef8f9c2d87d4ff6c19fd60bf
{"branch":"master","branch_tip":"0750db0d241d51f0ef8f9c2d87d4ff6c19fd60bf","counts":{"attributed_events":12,"events_total":13,"unattributed":1,"writer_classes":7,"writers_with_events":3},"findings":[{"detail":"enumerated /boot/limine.conf write line has no event claim","id":"EVENT-UNATTRIBUTED","site":".ufo/waves/round-19/l1-capture/host-capture-r19b.txt:1695"}],"revision":"0750db0d241d51f0ef8f9c2d87d4ff6c19fd60bf","status":"FAIL"}
EXIT=1
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv -c user.name=fixture -c user.email=fixture@local commit -am restore-1-pristine-bytes
[detached HEAD c153c70] restore-1-pristine-bytes
 1 file changed, 7 insertions(+)
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv rev-parse HEAD
c153c702a7f18044981590a882a39027d9fcce66
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv update-ref refs/heads/master c153c702a7f18044981590a882a39027d9fcce66
EXIT=0
$ sha256sum corpus/knowledge/boot-writers-r19.json corpus/knowledge/boot-writers-r19.md .ufo/waves/round-19/l1-capture/host-capture-r19c.txt tools/check-boot-writers.py
d9db10d00c9424f9ccf5b35e97a27f0f770b5a0dbfc7fdb229dce4892c3e7413  corpus/knowledge/boot-writers-r19.json
80ab81def8cddc98077f9ce2a51cfdee40e534cbc1961a78e6b5931c44d9d8d8  corpus/knowledge/boot-writers-r19.md
669cada8c08e00cae06b1429f81f254a744f3a7a1d6fe684592fbe202dea298d  .ufo/waves/round-19/l1-capture/host-capture-r19c.txt
69d258e340d87ab6966251ebed52b737c67de37b320be0ea91f828c94f00c40c  tools/check-boot-writers.py
EXIT=0
$ python3 tools/check-boot-writers.py --revision c153c702a7f18044981590a882a39027d9fcce66
{"branch":"master","branch_tip":"c153c702a7f18044981590a882a39027d9fcce66","counts":{"attributed_events":13,"events_total":13,"unattributed":0,"writer_classes":7,"writers_with_events":3},"findings":[],"revision":"c153c702a7f18044981590a882a39027d9fcce66","status":"PASS"}
EXIT=0
$ sha256sum corpus/knowledge/boot-writers-r19.json corpus/knowledge/boot-writers-r19.md .ufo/waves/round-19/l1-capture/host-capture-r19c.txt tools/check-boot-writers.py
d9db10d00c9424f9ccf5b35e97a27f0f770b5a0dbfc7fdb229dce4892c3e7413  corpus/knowledge/boot-writers-r19.json
db927929023e98c8b843dfbd12c374fd75d3880ca447cbc25819d5241455871e  corpus/knowledge/boot-writers-r19.md
669cada8c08e00cae06b1429f81f254a744f3a7a1d6fe684592fbe202dea298d  .ufo/waves/round-19/l1-capture/host-capture-r19c.txt
69d258e340d87ab6966251ebed52b737c67de37b320be0ea91f828c94f00c40c  tools/check-boot-writers.py
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv -c user.name=fixture -c user.email=fixture@local commit -am mutant-2-corrupt-published-mechanism
[detached HEAD 622b95b] mutant-2-corrupt-published-mechanism
 1 file changed, 1 insertion(+), 1 deletion(-)
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv rev-parse HEAD
622b95b2fe6d91f5868317473c6b74a3ad228221
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv update-ref refs/heads/master 622b95b2fe6d91f5868317473c6b74a3ad228221
EXIT=0
$ python3 tools/check-boot-writers.py --revision 622b95b2fe6d91f5868317473c6b74a3ad228221
{"branch":"master","branch_tip":"622b95b2fe6d91f5868317473c6b74a3ad228221","counts":{"attributed_events":13,"events_total":13,"unattributed":0,"writer_classes":7,"writers_with_events":3},"findings":[],"revision":"622b95b2fe6d91f5868317473c6b74a3ad228221","status":"PASS"}
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv -c user.name=fixture -c user.email=fixture@local commit -am restore-2-pristine-bytes
[detached HEAD d95ce96] restore-2-pristine-bytes
 1 file changed, 1 insertion(+), 1 deletion(-)
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv rev-parse HEAD
d95ce9690c983debc92e807ffd0c58ae356335c6
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv update-ref refs/heads/master d95ce9690c983debc92e807ffd0c58ae356335c6
EXIT=0
$ sha256sum corpus/knowledge/boot-writers-r19.json corpus/knowledge/boot-writers-r19.md .ufo/waves/round-19/l1-capture/host-capture-r19c.txt tools/check-boot-writers.py
d9db10d00c9424f9ccf5b35e97a27f0f770b5a0dbfc7fdb229dce4892c3e7413  corpus/knowledge/boot-writers-r19.json
80ab81def8cddc98077f9ce2a51cfdee40e534cbc1961a78e6b5931c44d9d8d8  corpus/knowledge/boot-writers-r19.md
669cada8c08e00cae06b1429f81f254a744f3a7a1d6fe684592fbe202dea298d  .ufo/waves/round-19/l1-capture/host-capture-r19c.txt
69d258e340d87ab6966251ebed52b737c67de37b320be0ea91f828c94f00c40c  tools/check-boot-writers.py
EXIT=0
$ python3 tools/check-boot-writers.py --revision d95ce9690c983debc92e807ffd0c58ae356335c6
{"branch":"master","branch_tip":"d95ce9690c983debc92e807ffd0c58ae356335c6","counts":{"attributed_events":13,"events_total":13,"unattributed":0,"writer_classes":7,"writers_with_events":3},"findings":[],"revision":"d95ce9690c983debc92e807ffd0c58ae356335c6","status":"PASS"}
EXIT=0
$ sha256sum corpus/knowledge/boot-writers-r19.json corpus/knowledge/boot-writers-r19.md .ufo/waves/round-19/l1-capture/host-capture-r19c.txt .ufo/waves/round-19/l1-capture/host-capture-r19.txt tools/check-boot-writers.py
296c37fbeb7ea95c07a1ea1f30a59c6ba402ee3d37007b314325a18db5a8689a  corpus/knowledge/boot-writers-r19.json
80ab81def8cddc98077f9ce2a51cfdee40e534cbc1961a78e6b5931c44d9d8d8  corpus/knowledge/boot-writers-r19.md
669cada8c08e00cae06b1429f81f254a744f3a7a1d6fe684592fbe202dea298d  .ufo/waves/round-19/l1-capture/host-capture-r19c.txt
d060de16892fbcb3ca85f45e28a94c9b6ef818c20029d91e05fa9459bbbde32b  .ufo/waves/round-19/l1-capture/host-capture-r19.txt
69d258e340d87ab6966251ebed52b737c67de37b320be0ea91f828c94f00c40c  tools/check-boot-writers.py
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv -c user.name=fixture -c user.email=fixture@local commit -am mutant-3-corrupt-capture-sha256
[detached HEAD d9fae26] mutant-3-corrupt-capture-sha256
 1 file changed, 1 insertion(+), 1 deletion(-)
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv rev-parse HEAD
d9fae26b49eaf4222d22e1fc46254e1b374aa436
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv update-ref refs/heads/master d9fae26b49eaf4222d22e1fc46254e1b374aa436
EXIT=0
$ python3 tools/check-boot-writers.py --revision d9fae26b49eaf4222d22e1fc46254e1b374aa436
{"branch":"master","branch_tip":"d9fae26b49eaf4222d22e1fc46254e1b374aa436","counts":{"attributed_events":0,"events_total":0,"unattributed":0,"writer_classes":0,"writers_with_events":0},"findings":[{"detail":"sha256 expected 0060de16892fbcb3ca85f45e28a94c9b6ef818c20029d91e05fa9459bbbde32b, observed d060de16892fbcb3ca85f45e28a94c9b6ef818c20029d91e05fa9459bbbde32b","id":"CAPTURE-TAMPERED","site":".ufo/waves/round-19/l1-capture/host-capture-r19.txt"}],"revision":"d9fae26b49eaf4222d22e1fc46254e1b374aa436","status":"CANNOT_EVALUATE"}
EXIT=2
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv -c user.name=fixture -c user.email=fixture@local commit -am restore-3-pristine-bytes
[detached HEAD c009a51] restore-3-pristine-bytes
 1 file changed, 1 insertion(+), 1 deletion(-)
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv rev-parse HEAD
c009a51cbea718b1bce7c61f3108a9e1033bc209
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv update-ref refs/heads/master c009a51cbea718b1bce7c61f3108a9e1033bc209
EXIT=0
$ sha256sum corpus/knowledge/boot-writers-r19.json corpus/knowledge/boot-writers-r19.md .ufo/waves/round-19/l1-capture/host-capture-r19c.txt tools/check-boot-writers.py
d9db10d00c9424f9ccf5b35e97a27f0f770b5a0dbfc7fdb229dce4892c3e7413  corpus/knowledge/boot-writers-r19.json
80ab81def8cddc98077f9ce2a51cfdee40e534cbc1961a78e6b5931c44d9d8d8  corpus/knowledge/boot-writers-r19.md
669cada8c08e00cae06b1429f81f254a744f3a7a1d6fe684592fbe202dea298d  .ufo/waves/round-19/l1-capture/host-capture-r19c.txt
69d258e340d87ab6966251ebed52b737c67de37b320be0ea91f828c94f00c40c  tools/check-boot-writers.py
EXIT=0
$ python3 tools/check-boot-writers.py --revision c009a51cbea718b1bce7c61f3108a9e1033bc209
{"branch":"master","branch_tip":"c009a51cbea718b1bce7c61f3108a9e1033bc209","counts":{"attributed_events":13,"events_total":13,"unattributed":0,"writer_classes":7,"writers_with_events":3},"findings":[],"revision":"c009a51cbea718b1bce7c61f3108a9e1033bc209","status":"PASS"}
EXIT=0
$ sha256sum .ufo/waves/round-19/l1-capture/host-capture-r19c.txt
19a9282c0e6ddefee5f5e239157dec73dc1dd9f11f9351860e6564e2f42c50c4  .ufo/waves/round-19/l1-capture/host-capture-r19c.txt
EXIT=0
$ sha256sum corpus/knowledge/boot-writers-r19.json corpus/knowledge/boot-writers-r19.md .ufo/waves/round-19/l1-capture/host-capture-r19c.txt tools/check-boot-writers.py
cd2a76c7938b39cf32e0eabccb1f51dd240d3e0e8a8d9faadd757068ae565840  corpus/knowledge/boot-writers-r19.json
80ab81def8cddc98077f9ce2a51cfdee40e534cbc1961a78e6b5931c44d9d8d8  corpus/knowledge/boot-writers-r19.md
19a9282c0e6ddefee5f5e239157dec73dc1dd9f11f9351860e6564e2f42c50c4  .ufo/waves/round-19/l1-capture/host-capture-r19c.txt
69d258e340d87ab6966251ebed52b737c67de37b320be0ea91f828c94f00c40c  tools/check-boot-writers.py
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv -c user.name=fixture -c user.email=fixture@local commit -am mutant-4-add-unclaimed-capture-event
[detached HEAD 428bc14] mutant-4-add-unclaimed-capture-event
 2 files changed, 2 insertions(+), 1 deletion(-)
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv rev-parse HEAD
428bc14e2dcb50e76b4d9f26ced3a0369ab92c8b
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv update-ref refs/heads/master 428bc14e2dcb50e76b4d9f26ced3a0369ab92c8b
EXIT=0
$ python3 tools/check-boot-writers.py --revision 428bc14e2dcb50e76b4d9f26ced3a0369ab92c8b
{"branch":"master","branch_tip":"428bc14e2dcb50e76b4d9f26ced3a0369ab92c8b","counts":{"attributed_events":13,"events_total":14,"unattributed":1,"writer_classes":7,"writers_with_events":3},"findings":[{"detail":"enumerated /boot/limine.conf write line has no event claim","id":"EVENT-UNATTRIBUTED","site":".ufo/waves/round-19/l1-capture/host-capture-r19c.txt:21"}],"revision":"428bc14e2dcb50e76b4d9f26ced3a0369ab92c8b","status":"FAIL"}
EXIT=1
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv -c user.name=fixture -c user.email=fixture@local commit -am restore-4-pristine-bytes
[detached HEAD fcfbfe7] restore-4-pristine-bytes
 2 files changed, 1 insertion(+), 2 deletions(-)
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv rev-parse HEAD
fcfbfe73ddd45ebaaaad209d204776652ee449e3
EXIT=0
$ git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv update-ref refs/heads/master fcfbfe73ddd45ebaaaad209d204776652ee449e3
EXIT=0
$ sha256sum corpus/knowledge/boot-writers-r19.json corpus/knowledge/boot-writers-r19.md .ufo/waves/round-19/l1-capture/host-capture-r19c.txt tools/check-boot-writers.py
d9db10d00c9424f9ccf5b35e97a27f0f770b5a0dbfc7fdb229dce4892c3e7413  corpus/knowledge/boot-writers-r19.json
80ab81def8cddc98077f9ce2a51cfdee40e534cbc1961a78e6b5931c44d9d8d8  corpus/knowledge/boot-writers-r19.md
669cada8c08e00cae06b1429f81f254a744f3a7a1d6fe684592fbe202dea298d  .ufo/waves/round-19/l1-capture/host-capture-r19c.txt
69d258e340d87ab6966251ebed52b737c67de37b320be0ea91f828c94f00c40c  tools/check-boot-writers.py
EXIT=0
$ python3 tools/check-boot-writers.py --revision fcfbfe73ddd45ebaaaad209d204776652ee449e3
{"branch":"master","branch_tip":"fcfbfe73ddd45ebaaaad209d204776652ee449e3","counts":{"attributed_events":13,"events_total":13,"unattributed":0,"writer_classes":7,"writers_with_events":3},"findings":[],"revision":"fcfbfe73ddd45ebaaaad209d204776652ee449e3","status":"PASS"}
EXIT=0
```

## Residual

- Four assigned cases only; no selftest, other gate, host log query, /boot probe, external runtime, or production repair was run.
- M2 targets the published Markdown mechanism, not the already-separate validation of registry `mechanism_refs` line/quote fields. The observed survivor is bounded to that publication fidelity gap.
- M4 tests an additional line inside an existing declared event-source probe block. It does not establish detection of events outside those declared probe blocks or of newly omitted/rewritten source declarations.
- The original 13-event attribution's real-world truth, mechanisms inside uncaptured binaries, and any admission decision remain outside this mutation probe. No contract was changed.

Scope: executed=mktemp -d /tmp/tsukuroi-r19-fxmutwriters-8-XXXXXX ; git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv checkout --detach 8e5916360f2dfe7bc4eb4ba144081af555900116 ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv update-ref refs/heads/master 8e5916360f2dfe7bc4eb4ba144081af555900116 ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv remote remove origin ; sha256sum corpus/knowledge/boot-writers-r19.json corpus/knowledge/boot-writers-r19.md tools/check-boot-writers.py ; python3 tools/check-boot-writers.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116 ; sha256sum corpus/knowledge/boot-writers-r19.json corpus/knowledge/boot-writers-r19.md .ufo/waves/round-19/l1-capture/host-capture-r19c.txt tools/check-boot-writers.py ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv -c user.name=fixture -c user.email=fixture@local commit -am mutant-1-remove-EV-01 ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv rev-parse HEAD ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv update-ref refs/heads/master 0750db0d241d51f0ef8f9c2d87d4ff6c19fd60bf ; python3 tools/check-boot-writers.py --revision 0750db0d241d51f0ef8f9c2d87d4ff6c19fd60bf ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv -c user.name=fixture -c user.email=fixture@local commit -am restore-1-pristine-bytes ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv rev-parse HEAD ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv update-ref refs/heads/master c153c702a7f18044981590a882a39027d9fcce66 ; sha256sum corpus/knowledge/boot-writers-r19.json corpus/knowledge/boot-writers-r19.md .ufo/waves/round-19/l1-capture/host-capture-r19c.txt tools/check-boot-writers.py ; python3 tools/check-boot-writers.py --revision c153c702a7f18044981590a882a39027d9fcce66 ; sha256sum corpus/knowledge/boot-writers-r19.json corpus/knowledge/boot-writers-r19.md .ufo/waves/round-19/l1-capture/host-capture-r19c.txt tools/check-boot-writers.py ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv -c user.name=fixture -c user.email=fixture@local commit -am mutant-2-corrupt-published-mechanism ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv rev-parse HEAD ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv update-ref refs/heads/master 622b95b2fe6d91f5868317473c6b74a3ad228221 ; python3 tools/check-boot-writers.py --revision 622b95b2fe6d91f5868317473c6b74a3ad228221 ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv -c user.name=fixture -c user.email=fixture@local commit -am restore-2-pristine-bytes ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv rev-parse HEAD ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv update-ref refs/heads/master d95ce9690c983debc92e807ffd0c58ae356335c6 ; sha256sum corpus/knowledge/boot-writers-r19.json corpus/knowledge/boot-writers-r19.md .ufo/waves/round-19/l1-capture/host-capture-r19c.txt tools/check-boot-writers.py ; python3 tools/check-boot-writers.py --revision d95ce9690c983debc92e807ffd0c58ae356335c6 ; sha256sum corpus/knowledge/boot-writers-r19.json corpus/knowledge/boot-writers-r19.md .ufo/waves/round-19/l1-capture/host-capture-r19c.txt .ufo/waves/round-19/l1-capture/host-capture-r19.txt tools/check-boot-writers.py ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv -c user.name=fixture -c user.email=fixture@local commit -am mutant-3-corrupt-capture-sha256 ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv rev-parse HEAD ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv update-ref refs/heads/master d9fae26b49eaf4222d22e1fc46254e1b374aa436 ; python3 tools/check-boot-writers.py --revision d9fae26b49eaf4222d22e1fc46254e1b374aa436 ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv -c user.name=fixture -c user.email=fixture@local commit -am restore-3-pristine-bytes ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv rev-parse HEAD ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv update-ref refs/heads/master c009a51cbea718b1bce7c61f3108a9e1033bc209 ; sha256sum corpus/knowledge/boot-writers-r19.json corpus/knowledge/boot-writers-r19.md .ufo/waves/round-19/l1-capture/host-capture-r19c.txt tools/check-boot-writers.py ; python3 tools/check-boot-writers.py --revision c009a51cbea718b1bce7c61f3108a9e1033bc209 ; sha256sum .ufo/waves/round-19/l1-capture/host-capture-r19c.txt ; sha256sum corpus/knowledge/boot-writers-r19.json corpus/knowledge/boot-writers-r19.md .ufo/waves/round-19/l1-capture/host-capture-r19c.txt tools/check-boot-writers.py ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv -c user.name=fixture -c user.email=fixture@local commit -am mutant-4-add-unclaimed-capture-event ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv rev-parse HEAD ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv update-ref refs/heads/master 428bc14e2dcb50e76b4d9f26ced3a0369ab92c8b ; python3 tools/check-boot-writers.py --revision 428bc14e2dcb50e76b4d9f26ced3a0369ab92c8b ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv -c user.name=fixture -c user.email=fixture@local commit -am restore-4-pristine-bytes ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv rev-parse HEAD ; git -C /tmp/tsukuroi-r19-fxmutwriters-8-DVBYQv update-ref refs/heads/master fcfbfe73ddd45ebaaaad209d204776652ee449e3 ; sha256sum corpus/knowledge/boot-writers-r19.json corpus/knowledge/boot-writers-r19.md .ufo/waves/round-19/l1-capture/host-capture-r19c.txt tools/check-boot-writers.py ; python3 tools/check-boot-writers.py --revision fcfbfe73ddd45ebaaaad209d204776652ee449e3
