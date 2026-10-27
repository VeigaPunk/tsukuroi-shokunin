VERDICT: defect-found

# C1-S2 — binding a seat that was never spawned

The frozen counter is **not buggy**: in every variant below its legs behaved exactly as its source
says. What I demonstrate is the stronger and more useful fact — the C1 admission chain
(`dispatch.json` + `results.json` + seat `.md` + three text marks) is **forgery-complete from
committed bytes alone**. I produced a full counter **PASS** on all three rows with **zero agents
spawned**, in **one commit of 148 inserted lines** (11 files) on top of the freeze revision:

```
$ python3 tools/check-scrub-admission-r47.py --lane $D --revision v3_A3_phantom_w1
{"counter": "check-scrub-admission-r47", ..., "marks_ok": 3, "quotes_ok": 3, "structural_ok": 1,
 "verdict": "PASS", "verdicts_ok": 3, "waves_seen": ["w1"], "per_row": {GR1|GR2|GR3: bound_on_current=2}}
 rc=0
```
(`C1SentForge/counter-A3_phantom_w1.json`; patch `C1SentForge/A3-phantom-w1.patch`.)

For contrast, the honest tree does not pass today: real lane revs `77e9e2b2` / `e31070a9` /
`f6bc6d05` all score `FAIL`, `verdicts_ok 0`, `waves_seen [] / ["w1"] / ["w1"]` (same command,
`--revision <rev>` against the lane). So the forgery is not redundant with the real wave: it is the
*only* thing that flips the gate.

## Method

Fixture clone `git clone -q --shared <lane> $D` under `/fast/scratch/hyaku/tsukuroi-r47/C1SentForge/`,
`remote remove origin`, `rev-parse --show-toplevel == $D` asserted before every commit, one commit
per variant with `-c user.name=fixture -c user.email=fixture@invalid`, scored with the frozen
counter. Drivers and all raw counter JSON are in the receipts dir; the clone is gone (scratch
removed), so the variant SHAs below are ephemeral, but `forge.py`/`forge2.py` rebuild every variant
byte-for-byte from the lane. Section hashes used were read from the counter itself:
GR1 `fe77ac76…9ca8`, GR2 `909830c8…11a2`, GR3 `43430a14…c32c` (`--section-hash`, `structural_ok 1`).

## What binds (14 variants)

| variant | commit | change | rc | verdict | bound GR1/2/3 |
|---|---|---|---|---|---|
| control: freeze `77e9e2b2` | — | nothing | 1 | FAIL | 0/0/0 (marks_ok 0) |
| **A** forged wave `w7` never in any dispatch | `792485688553` | +209 | **0** | **PASS** | 2/2/2 |
| **A3** forger writes *the L1's own* `w1-dispatch.json` | `1fc064e8b187` | +148 | **0** | **PASS** | 2/2/2 |
| **A4** dispatch lies: `counts.spawn=64`, 6 tasks, 24 members | `fa0e1ba5387f` | +378 | **0** | **PASS** | 2/2/2 |
| B same as A without `*-results.json` | `c85f24beb863` | +180 | 1 | FAIL | 0/0/0 |
| C invented `agentId` UUIDs, `status:"fabricated"`, 1970 stamps | `e9f9a8d3f317` | +239 | **0** | **PASS** | 2/2/2 |
| D dispatch with **no** `registry`/`counts` at all | `d82b5688b7db` | +136 | **0** | **PASS** | 2/2/2 |
| E seat dispatched in two waves | `8e62b8cd1952` | +281 | 1 | FAIL | 1/1/1 |
| F two bound seats, byte-identical bodies | `14b6cc65f36e` | +137 | 1 | FAIL | 2/2/2 |
| F2 same + one nonce character per body | `06e775774687` | +137 | **0** | **PASS** | 2/2/2 |
| G critic-universe seat dispatched as `reviewer` | `545e83722466` | +209 | 1 | FAIL | 1/1/1 |
| **H** fill the L1's *genuine* w1 dispatch (blob `53578e9d`, identical) | `9e1994ff690e` | +86 | **0** | **PASS** | 2/2/2 |
| I same forgery, commit dated 2001-01-01 | `a1f923ba28a2` | +137 | **0** | **PASS** | 2/2/2 |
| L body copied verbatim from real seat `.ufo/waves/round-46/r1/V46ResCritGR2.md` (4066 B) | `d512a8818256` | +141 | **0** | **PASS** | 2/2/2 |

Two distinct forgery classes both pass:

* **Class 1 — phantom seat.** The name was never spawned (A, A3, A4, C, D, I).
* **Class 2 — hijacked seat.** Real, spawned seat names, forged report bodies (H, L). A wave that
  reuses the L1's dispatch byte-for-byte (`git diff --stat e31070a9 v2_H… -- …/w1-dispatch.json`
  empty; both blobs `53578e9d`) still PASSes, so *any* name-based spawn ledger alone cannot catch
  this class.

## What the counter actually inspects

* `dispatches()` — `tools/check-scrub-admission-r47.py:167-176` — keys the wave set off
  `ls-tree` of `.ufo/waves/round-47` and accepts **every** `*-dispatch.json` present. No manifest,
  no allow-list, no `counts`/`registry` consistency check (A4: `spawn:64` against 6 tasks, PASS).
* `bind()` — `:178-224` — the entire results requirement is one line, `:200`:
  `r.get('name') == seat and r.get('agent') == role`. Every other key of a results entry is unread
  (variant C). Exactly-one-dispatch (`:192`) and role equality (`:194`) are the only structural
  guards, and both are satisfied by writing the dispatch yourself (E and G fail only when you
  contradict yourself).
* report shape — `:212-224`: first line `ROW GR<n> VERDICT: <v>`, second `SECTION SHA256: <hex>`,
  body ≥ 300 bytes (`:222`), ≥1 `file:line` of the row's sources (`:224`), all `file:line` tokens
  resolving inside the pinned snapshots (`report_citations_ok`, `:286`). All of it is text the
  forger writes; the section hash is public (the entry is committed).
* K23 — `:352` `distinct = len(set(bodies)) == len(bodies) == len(on_cur)` — the only content
  constraint between seats, defeated by one nonce character (F fails, F2 passes).
* marks — `:368-371` — three exact/negation-filtered lines. They attest nothing: every PASSing
  variant above has `marks_ok 3` on a tree where no seat ran.
* `grep -rn agentId tools/` → **0 hits**. No lane counter reads an agent id anywhere; the notion
  does not exist in the tool family (`check-scrub-record-r42/43/44`, `-grounding-r45`,
  `-admission-r46/47` all read only `results[].name`/`.agent`).

## Do the three named signals distinguish?

**(a) results.json agent ids — no, not as the artifacts stand.** (i) Nothing reads them (`:200`
above). (ii) No real results file carries one: `.ufo/waves/round-46/w1-results.json` entries have
keys `['agent','name','note','output']`, likewise `r1-results.json`. (iii) The round's own launch
evidence has no ids either — `.ufo/waves/round-47/w1/swarm-registry.json`: `members 64,
agentId null: 64`; `.ufo/waves/round-47/w1.ready.partial`: 46 entries, each mapping a name to
*the same name*. So an id cross-check today would compare `null` with `null`, and a forger writes
both sides anyway (variant C proves invented ids pass). Ids only become evidence if they are
**issued outside the lane** and the counter compares to that issuer.

**(b) seat transcripts — yes: this is the only lane-external evidence that exists, and it is the
only thing that catches Class 2.** Transcripts live in the harness, keyed by a server-assigned
agent id (`history://<id>`, `agent://<id>`), and are not writable by any lane commit. A phantom
seat has no transcript; a hijacked seat (H, L) has a transcript whose first two lines and body
digest will not match the committed report. Requirements to make it usable: `results[].agentId`
must be recorded at spawn (today it is not), and each bound seat must be resolved against its
transcript by a **non-author verifier** — the lane counter cannot do it, since the read path is a
harness tool, not a file. This is the smallest change that closes both classes.

**(c) timing — no, not from inside git.** Variant I PASSes with a 2001 commit date and results
timestamps at 1970; commit dates, `registry.createdAt`/`updatedAt` (`updatedAt == createdAt`,
`2026-10-27T08:42:55.680Z`) and every other in-tree timestamp are written by the committer.
Timing only discriminates when it comes from an append-only host ledger. The one available here is
the journal: at spawn, `systemd-cat -t tsukuroi-r47-<wave> seat=<name> id=<agentId>` and a
closure-time read of `journalctl -t … -o json`. Feasibility observed read-only on this host:
`/usr/bin/systemd-cat` present; `journalctl --verify` → `PASS:` on the sealed journal files;
`journalctl -t tsukuroi-r48-probe -o json` → 0 lines (no lines exist yet, so the check is clean).
Caveat that keeps this honest: an L1 that forges can also emit its own journal lines, so the line
must carry a value it cannot know without really spawning — the child PID and process start time
from the runner, not from an agent shell — and must be emitted by the runner, not by a seat.

## Cheapest next-round additions, ranked by what they buy

1. **Transcript attestation (only real fix).** Spec: every bound counted seat's results entry
   carries a non-null harness `agentId`; the closing reviewer resolves `history://<agentId>` and
   requires the committed report's first two lines plus body sha256 to match the transcript. One
   read per bound seat; kills Class 1 and Class 2. Record the resolved id and digest in the closure
   record so the *next* round can re-check without re-reading.
2. **Spawn receipt written by the runner**, `w1/spawn.jsonl`, hash-chained (`prev` = sha256 of the
   previous line): `{seat, agentId, pid, startedAt, dispatchSha256}`; counter legs — exactly one
   receipt per bound seat, `receipt.agentId == results.agentId` (non-null, unique across seats),
   `receipt.dispatchSha256 == sha256(<wave>-dispatch.json at REV)`. Cost ≈ 25 lines; publishes the
   chain head in the L1's turn output so the head is anchored outside the lane.
3. **Pin the wave set.** Counter constant `WAVES_FROZEN = ('w1',)` (or the manifest sha256 frozen
   with the counter): `dispatches()` keys must equal it. Kills A and A4 at ~3 lines; cannot touch
   A3/H, which live inside `w1`.
4. **Dispatch internal consistency** (~12 lines): `counts.spawn == len(taskCall.tasks) ==
   len(registry.members)`, member names disjoint from other waves' tasks, `registry.path`/
   `reportDir` matching the wave. Makes A4-class lies fail; keeps a determined forger merely honest-
   looking.
5. **K23 hardening** (~10 lines): require ≥2 distinct `file:line` citations per bound report and
   reject a pair whose word-shingle overlap > 0.9 (F2 passes today on one nonce character).
6. **Journal spawn line** (see (c) above) as the timing anchor — only worth it together with (2),
   and only if a runner, not an agent, writes it.

## Impact

Severity **high for the C1 evidence claim**, by design cheap to exploit: any writer with commit
access to the lane admits GR1–GR3 (and the three admission marks) in one commit, with no seat, no
reading of the entry, and no trace in the tree that a reviewer could use to tell it from a genuine
wave. The consequence is exactly the failure the depth gate exists to prevent: `verdicts_ok == 3`
on unread bytes, and a closure that reports counted seats that were never spawned. This confirms
and sharpens the standing documented limit ("committed bytes cannot tell forged records from real
ones"): with agent ids absent everywhere (64/64 null), there is currently **no** residual artifact
in the committed tree — not ids, not transcripts, not timing — that distinguishes the two.

## What I did not do

I did not touch any real wave file, the lane index, or the host; every artifact lives in the
ephemeral fixture clone (removed) and the receipts dir. I did not run the census selftest or any
other heavy counter, did not dispatch any agent (leaf seat), and did not attempt to make the
forgery survive any proposed next-round check beyond the analysis above — check 1 is unrun and
therefore unproven; it is a proposal, not a result. No tools were installed or upgraded.
