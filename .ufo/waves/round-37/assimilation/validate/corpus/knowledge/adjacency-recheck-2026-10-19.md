source: ../kama-shokunin/PROVINCE.md @ 35e9175fc543b8090ba436a5f8c6b8b1c768339a SHA-256 a7728760f777573f9a4184df83efadc37fddc29159521c3ec48b11472579c0c6; ../kagi-shokunin/PROVINCE.md @ aea7a4301034aa9160ada69457a6427f77064169 SHA-256 ffe644a7b2cecfc8169de8393937214f563570a8413912069568fb7065648e17; ../mado-shokunin/PROVINCE.md @ e1d81d48026b6b9c9e9614c3b6390240200110db SHA-256 7aad7b863dc3c10b9fbafb8b04b7f73084adbdf91616a0859f7bfd4b0edb135a; ../mori-shokunin/PROVINCE.md @ 20e2255e7b3ebb05a52272f35a996421cab14848 SHA-256 aac98b22bb83bade906fbc3f4841a6cd666f13e07485c48d700eaf0f786400f2; ../kumitate-shokunin/PROVINCE.md @ 16a5441a3347a10ac5ed169abcd5a17ba6f3f185 SHA-256 caa83fde27c036829e2f4c882e5c7b2270d95586bd6a12a551b3d75a72d491d2; ../kaidoku-shokunin/PROVINCE.md @ de77d754523afb673b4421d363fe89311644af4f SHA-256 b95c9f5beffc3ce5116677719415f9f2dc50c2b579907d5abc10bdb732482fa2; ../revenger-shokunin/PROVINCE.md @ 8bbcb4e3267d155525c1ef1258ee327b49e53ec4 SHA-256 63acc3d033869f93f3e13da79e35023d86baa60b3f1d3b52861b019183b4b19f; ../tameshi-shokunin/PROVINCE.md @ 4eb4cf319c0eddd4ef0c6d1d4d11e51e0d4ee307 SHA-256 f5e28bf144b0601c242e43d2a9d8b60b08b8ac9476728b9f5809aa655b77d89f; corpus/knowledge/adjacency-handoffs-fleet-r1.json @ 9b70381c54a040e8775b43a61245b088acefb65f.
verified-at: 2026-10-19 (re-ran all eight committed-HEAD SHA-256 pins; re-read all route source ranges; swept sibling packet receipts).
recheck: 30d; procedure: git -C /home/vgpnk/Projects/shokunin/<lane>-shokunin show HEAD:PROVINCE.md | sha256sum

# Adjacency source re-check — 2026-10-19

## Pin table — original → current committed HEAD

[obs] The baseline values are the `source_pins` object in the cited ledger at `9b70381c54a040e8775b43a61245b088acefb65f`. Current values below come from each sibling's committed `HEAD:PROVINCE.md` bytes, not its working tree.

| sibling | original pin | current SHA-256 | sibling HEAD | result |
|---|---|---|---|---|
| kama | `454f12e7a477031614c7585ab3452935307574bcb407089722dfced81f6f7f7f` | `a7728760f777573f9a4184df83efadc37fddc29159521c3ec48b11472579c0c6` | `35e9175fc543b8090ba436a5f8c6b8b1c768339a` | drift |
| kagi | `ffe644a7b2cecfc8169de8393937214f563570a8413912069568fb7065648e17` | `ffe644a7b2cecfc8169de8393937214f563570a8413912069568fb7065648e17` | `aea7a4301034aa9160ada69457a6427f77064169` | match |
| mado | `7aad7b863dc3c10b9fbafb8b04b7f73084adbdf91616a0859f7bfd4b0edb135a` | `7aad7b863dc3c10b9fbafb8b04b7f73084adbdf91616a0859f7bfd4b0edb135a` | `e1d81d48026b6b9c9e9614c3b6390240200110db` | match |
| mori | `aac98b22bb83bade906fbc3f4841a6cd666f13e07485c48d700eaf0f786400f2` | `aac98b22bb83bade906fbc3f4841a6cd666f13e07485c48d700eaf0f786400f2` | `20e2255e7b3ebb05a52272f35a996421cab14848` | match |
| kumitate | `caa83fde27c036829e2f4c882e5c7b2270d95586bd6a12a551b3d75a72d491d2` | `caa83fde27c036829e2f4c882e5c7b2270d95586bd6a12a551b3d75a72d491d2` | `16a5441a3347a10ac5ed169abcd5a17ba6f3f185` | match |
| kaidoku | `fa915ec7bd42ec516d0639c72d0fa443014ae5c4bf5c10ff90a661241c6ae312` | `b95c9f5beffc3ce5116677719415f9f2dc50c2b579907d5abc10bdb732482fa2` | `de77d754523afb673b4421d363fe89311644af4f` | drift |
| revenger | `cc43312d38b533df605cdd36ea85f66f6f4c4a53507bc39c9bcc4e7c8422c1bf` | `63acc3d033869f93f3e13da79e35023d86baa60b3f1d3b52861b019183b4b19f` | `8bbcb4e3267d155525c1ef1258ee327b49e53ec4` | drift |
| tameshi | `f5e28bf144b0601c242e43d2a9d8b60b08b8ac9476728b9f5809aa655b77d89f` | `f5e28bf144b0601c242e43d2a9d8b60b08b8ac9476728b9f5809aa655b77d89f` | `4eb4cf319c0eddd4ef0c6d1d4d11e51e0d4ee307` | match |

[obs] Pins matching original: 5/8 — `git -C /home/vgpnk/Projects/shokunin/<lane>-shokunin show HEAD:PROVINCE.md | sha256sum`, 2026-10-19T22:07:49Z. The changed pins are kama, kaidoku and revenger; the five matching pins are kagi, mado, mori, kumitate and tameshi. The original hash values remain unchanged in the JSON ledger.

## Route source-anchor re-read

[obs] Source pins with anchors holding: 8/8 — `git -C /home/vgpnk/Projects/shokunin/<lane>-shokunin show HEAD:PROVINCE.md` plus re-reading each cited range, 2026-10-19. All route anchors remain within their cited ranges; none moved. Quotes are from the committed HEAD bytes identified above.

| route | cited source range | current anchor evidence |
|---|---|---|
| ADJ-01 | kama `PROVINCE.md:3-40` | `served-model-id reconciliation` — kama line 12 |
| ADJ-02 | kagi `PROVINCE.md:3-17`; `:32-54` | `credential hygiene evidence` — line 3; `pinned by shape, never by content` — line 32 |
| ADJ-03 | mado `PROVINCE.md:3-16` | `desktop & compositor craft` — mado line 3 |
| ADJ-04 | mori `PROVINCE.md:3-16` | `fleet & host observability` — mori line 3 |
| ADJ-05 | kumitate `PROVINCE.md:3-6`; mori `:12-16` | `orchestration & tooling` — kumitate line 3; `Refuses: dispatch and orchestration mechanism` — mori line 12 |
| ADJ-06 | kaidoku `PROVINCE.md:3-6`; revenger `:3-7` | `reverse engineering of shipped artifacts with REA on this Linux host` — kaidoku line 3; `Owns: reverse engineering of shipped artifacts` — revenger line 3 |
| ADJ-07 | tameshi `PROVINCE.md:3-18` | `verification-fixture craft — the reusable method of honest checks` — tameshi line 3 |

## Route lifecycle states

[obs] The existing packet note calls ADJ-04 the only exercised observation/request packet (`corpus/knowledge/adjacency-handoffs-fleet-r1.md:29-30, 74-85`); its ADJ-01 and ADJ-02 controls are explicitly negative routing controls, not delivered incidents (`:115-134`). No route-specific packet exists for ADJ-03 or ADJ-05–07.

| route | state | evidence / boundary |
|---|---|---|
| ADJ-01 | `contract-only` | R1DriverPacket is a negative routing control; no endpoint incident or delivered handoff (`adjacency-handoffs-fleet-r1.md:115-123`). |
| ADJ-02 | `contract-only` | R1HelperPacket is metadata-only; no auth incident or delivered ADJ-02 incident (`adjacency-handoffs-fleet-r1.md:125-134`). |
| ADJ-03 | `contract-only` | No route packet recorded; only ADJ-04 is an exercised observation/request packet (`adjacency-handoffs-fleet-r1.md:29-30, 74-85`). |
| ADJ-04 | `prepared` | `TSUKUROI-F1-MEM-01` is prepared (`adjacency-handoffs-fleet-r1.md:74-85`). Pending transition: `reported on integrator commit of .ufo/reports/round-1/tsukuroi.md (fleet repo)`. No acknowledgement or acceptance inferred. |
| ADJ-05 | `contract-only` | No ADJ-05 packet recorded (`adjacency-handoffs-fleet-r1.md:29-30, 74-85`). |
| ADJ-06 | `contract-only` | No RE packet/target execution; ownership remains an arbitration request (`adjacency-handoffs-fleet-r1.md:29-30, 54, 74-85`). |
| ADJ-07 | `contract-only` | No method-advice packet recorded (`adjacency-handoffs-fleet-r1.md:29-30, 74-85`). |

[obs] Receipt sweep command: `grep -rn 'TSUKUROI-F1-MEM-01' /home/vgpnk/Projects/shokunin/*-shokunin --include='*.md' --include='*.json' | grep -v '^/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'`. Result: no stdout, exit status 1. 0 matching sibling receipt — this exact sweep, 2026-10-19. No named-recipient receipt was found, so ADJ-04 is not upgraded to `acknowledged`; its report transition remains pending integration.
[unk] Recipient acknowledgement, acceptance and resolution beyond the searched sibling files remain unobserved; the sweep alone cannot establish downstream closure.

## ADJ-06 shared reverse-engineering scope

[obs] Kaidoku's committed declaration says `reverse engineering of shipped artifacts with REA on this Linux host` (../kaidoku-shokunin/PROVINCE.md:3-6; HEAD `de77d754523afb673b4421d363fe89311644af4f`). Revenger's committed declaration says `Owns: reverse engineering of shipped artifacts` (../revenger-shokunin/PROVINCE.md:3-7; HEAD `8bbcb4e3267d155525c1ef1258ee327b49e53ec4`).

[inf] The declarations still overlap on shipped-artifact reverse engineering. The ownership question remains contested: tsukuroi selects no owner and requests an integrator ruling as ADJ-06 specifies. No target was executed.

## Falsifier

A later sibling commit that changes a `PROVINCE.md` hash, or a re-read showing an anchor concept outside its recorded range, falsifies this point-in-time pin/anchor result; rerun the method above before routing from the ledger. An integrator-committed fleet report or a durable named-recipient receipt changes the recorded lifecycle state only when that evidence is re-read.

## Sources

- Sibling committed declarations and full HEAD/hash identities: pin table above; each source was read at the cited HEAD revision on 2026-10-19.
- `corpus/knowledge/adjacency-handoffs-fleet-r1.json` at `9b70381c54a040e8775b43a61245b088acefb65f`: original pins, routes and lifecycle vocabulary.
- `corpus/knowledge/adjacency-handoffs-fleet-r1.md`: packet identity, ADJ-01/02 boundary controls, ADJ-06 ownership limitation.
- `.ufo/evidence/round-1-kaika/adjacency-pins.txt`: raw pin and receipt command outputs.

## Later committed-head recheck — 2026-10-19T22:57:14Z

This snapshot supersedes the 22:07:49Z pin-match total above for current routing. The original `source_pins` stay unchanged. Command: `git -C /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/<lane>-shokunin show HEAD:PROVINCE.md | sha256sum`; all eight worktrees were clean during measurement.

| sibling | committed HEAD | current SHA-256 | original pin |
|---|---|---|---|
| kama | `03b5f0e` | `a7728760f777573f9a4184df83efadc37fddc29159521c3ec48b11472579c0c6` | drift |
| kagi | `e1544c1` | `4a346e2df81f7b2e649914d0d99da974d6c484caf12fed1c6bd530d106a78523` | drift |
| mado | `e3e6a8e` | `7aad7b863dc3c10b9fbafb8b04b7f73084adbdf91616a0859f7bfd4b0edb135a` | match |
| mori | `1f07f1d` | `16129e6d2ba9b38a4411bdc933e27c8bb31f7689003580ff7c80ea02a17a4422` | drift |
| kumitate | `1a8eed5` | `fcd69667a1027d5edd07a8ff0390a716a467aff92719071e33cb6157673b665f` | drift |
| kaidoku | `1170f71` | `b95c9f5beffc3ce5116677719415f9f2dc50c2b579907d5abc10bdb732482fa2` | drift |
| revenger | `cf02419` | `63acc3d033869f93f3e13da79e35023d86baa60b3f1d3b52861b019183b4b19f` | drift |
| tameshi | `a21e910` | `3c67d81c481b7b8e1bb07b72bfba8a96ce993b0155ba72f7bcbb749f7309b634` | drift |

[obs] The original pin match count is now 1/8 (mado); the other seven hashes differ. I re-read every cited anchor in the corresponding clean committed `PROVINCE.md` ranges (kama 12; kagi 3 and 32; mado 3; mori 3 and 12; kumitate 3; kaidoku 3; revenger 3; tameshi 3); all 8/8 anchor concepts remain present in-range. A digest mismatch is not itself an ownership change.

### Committed recipient-side packet response

[obs] Committed-tree sweep over `/home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/*-shokunin`, using `git -C <repo> grep -l 'TSUKUROI-F1-MEM-01' HEAD -- '*.md' '*.json'`, found one sibling recipient repository: mori, HEAD `1f07f1dd1eed59f10c4859726e2f780199190b22`. The identifier appears in three committed files (`PROVINCE.md`, `SCORECARD.md`, `LOG.md`), which are corroborating copies of one response, not three packets. `git -C /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/mori-shokunin grep -q 'TSUKUROI-F1-MEM-01' HEAD^ -- PROVINCE.md SCORECARD.md LOG.md` was false; the same query at `HEAD` is true (0→1 recipient-side response). Mori records that no retained kill record overlaps the capture second (`PROVINCE.md:58-76`; `SCORECARD.md:614`; `LOG.md:675-678`). This is receipt/answer evidence only; no acceptance or resolution is inferred. The earlier 0-hit main-checkout sweep and the 22:07 pin snapshot remain historical observations, not current results.

## QUALITY check

- Criteria 1–3: the pin table is falsifiable against committed HEAD bytes; source-anchor presence is reported separately from digest equality; `[obs]` and the unclaimed receipt states are kept distinct.
- Criteria 7–8: sibling declarations and commit identities are cited; the recheck command, snapshot time, original pin comparison and explicit recheck procedure are recorded.
- Criterion 9: the packet search is bounded to committed kaika `*-shokunin` HEAD trees and its positive result is recorded; it makes no negative claim about unsearched repositories.
- Criterion 4: prior snapshot and prior receipt statement remain intact; this is an appended correction, not a rewrite.