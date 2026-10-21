# FxScoutSiblingTips — verify the ten pinned sibling commits behind C1's outbound anchors

Lane: tsukuroi-shokunin, round-19 FALSIFY recovery wave 2 (attempt 2). Attack target: revision
`8e5916360f2dfe7bc4eb4ba144081af555900116` (production content at `7cc59c8e3761ffb668067c47655216376f0a4e48`,
baseline `452a054677f6b18284917d7c08c45361f91c25ac`). Seat: leaf scout, read-only except this report.

## Attack

C1's outbound half claims ten sibling ownership anchors in PROVINCE.md (`## Adjacent — portable ownership
anchors (round 19)`, OUT-001..OUT-010), each carrying a heading + verbatim <=25-word quote + pinned sibling
commit + blob sha256. Falsifiable surface attacked here:

1. **Reachability** — each pinned commit exists in the sibling repo (`cat-file -e <pin>^{commit}`) and is
   reachable from at least one ref, not a dangling object.
2. **Tip state** — is the pin behind the sibling tip, and does the anchor text (exact quote + heading)
   still appear verbatim at the tip? Any anchor whose text vanished at tip without a note is a finding.
3. **Stated intent** — pin-behind is allowed only if stated; does the anchor section call the staleness
   intentional?
4. **Byte identity (bonus axis)** — the recorded `sibling_commit`/`sibling_blob_sha256` in the committed
   census must match independently recomputed values from the sibling repos; a mismatch would mean the
   anchors cite bytes that were never the sibling's.

## Method

All commands read-only; no pacman transaction, no host probe, no writes outside this report (plus an
idempotent `mkdir -p` of its already-existing directory). No tool installs needed — system
git/sha256sum/grep/python3 sufficed.

1. Read the anchor section at the attacked revision:
   `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 8e59163…:PROVINCE.md` (full file, 132 lines;
   anchors at lines 108–132). A first probe `grep -nE '[0-9a-f]{40}'` over the same blob returned nothing
   (pins are 12-hex abbreviations), which located the real format.
2. Enumerate sibling repos: `ls -d /home/vgpnk/Projects/shokunin/*-shokunin` (21 repos; all 8 needed repos present).
3. Per sibling repo R with pin P — one identical template invocation each for
   (mori `91940fa339e3`, kama `e75cf680b534`, kagi `c2cab35bc92e`, mado `a4046a821608`,
   kumitate `1770305fae20`, kaidoku `d1d981d2cc04`, revenger `cf02419276e5`, tameshi `01d586ddbc5f`):
   - `git -C R cat-file -e P^{commit}` (pin present)
   - `git -C R show -s --format='pin %H %ci %s' P` and same for `HEAD` (identity/date/subject)
   - `git -C R rev-parse --abbrev-ref HEAD` and `git -C R rev-parse HEAD`
   - `git -C R log --format=%H P..HEAD | wc -l` (tip-side commit count; small finite count ⇒ pin is an ancestor of tip)
   - `git -C R log --all --format=%H | grep -c "^P"` (ref reachability of the pin)
   - `git -C R show P:PROVINCE.md | sha256sum` and `git -C R show HEAD:PROVINCE.md | sha256sum`
   - `git -C R show {P,HEAD}:PROVINCE.md | grep -cF '<heading>'` (anchor heading at pin and tip)
   - `git -C R show {P,HEAD}:PROVINCE.md | grep -cF '<quote>'` for each anchor quote (mori: three quotes;
     others: one). Single-line fixed-string match; count 1 everywhere, so no line-wrap normalization was needed.
4. Cross-check recorded values:
   - `git show 8e59163…:corpus/knowledge/adjacency-anchors-r19.md | grep …` (source line 1 lists the 8 pins
     and snapshot paths; no literal blob sha256 table in the registry)
   - `git show 8e59163…:.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json | python3 -c …`
     (read-only JSON walk of the `outbound` records, printing `id, sibling, sibling_commit, sibling_blob_sha256`).

## Verdict

**CONFIRM (C1 outbound-anchor pin axis)** — all ten anchors survive every falsification probe; no finding triggered.

1. Reachability: 10/10 pins present (`cat-file -e` exit 0) and each appears exactly once in `log --all`
   of its sibling repo (ref-reachable, not dangling).
2. Tip state: 10/10 pins are ancestors of the current tip (finite tip-side counts: mori 11, kama 21,
   kagi 33, mado 14, kumitate 31, kaidoku 8, revenger 0, tameshi 25). All 10 quotes and all 10 headings
   match verbatim (`grep -cF` = 1) at **both** the pinned commit and the tip. **No anchor text vanished at
   tip**, so the "vanished without a note" finding condition never fires.
3. Stated intent: yes — `8e59163…:PROVINCE.md:132`: "the pins are stale by design once a sibling commits
   again, so re-read the live declaration before any later handoff (the paragraph above `## Frontier`
   still governs)". Every pin-behind state is covered by this stated note.
4. Byte identity: the census `outbound` records' full 40-hex `sibling_commit` and `sibling_blob_sha256`
   match my independently computed `rev-parse <pin>` and `git show <pin>:PROVINCE.md | sha256sum` for all
   8 repos / 10 rows — 10/10 exact.

## Evidence

Anchors and note: `tsukuroi-shokunin @ 8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:108-132`
(table lines 121–130, Limits/intent line 132). Recorded values:
`8e59163…:.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json` (`outbound` array; top-level keys
`schema, lane_branch, lane_tip, siblings, counts, inbound, outbound`). Registry source line:
`8e59163…:corpus/knowledge/adjacency-anchors-r19.md:1`.

| Anchor(s) | Repo | Pin (full, from census = my rev-parse) | Pin date | Sibling tip | Branch | Behind | Quote@pin/tip | blob pin == census |
|---|---|---|---|---|---|---|---|---|
| OUT-001/005/007 | mori | `91940fa339e38006f8db5bd7d78bb6f037f4d016` | 10-20 17:49 | `3786f3f1bde2…` | HEAD (detached) | 11 | ✓/✓ (all 3) | ✓ `73abda79…` |
| OUT-002 | kama | `e75cf680b53484a61709ee1b2787d8dbc6419f74` | 10-20 16:41 | `37bd4c5bd456…` | HEAD (detached) | 21 | ✓/✓ | ✓ `799432d7…` |
| OUT-003 | kagi | `c2cab35bc92e57e39e5489bac3386db078345b3f` | 10-19 22:05 | `c5ef9e92201b…` | HEAD (detached) | 33 | ✓/✓ | ✓ `4a346e2d…` |
| OUT-004 | mado | `a4046a8216080d4004de3f268c62cf142095ac07` | 10-20 17:34 | `c2a306db8a04…` | HEAD (detached) | 14 | ✓/✓ | ✓ `1b25bb1e…` (blob unchanged pin→tip) |
| OUT-006 | kumitate | `1770305fae20826b39905a8251ddeca6b4957ac4` | 10-19 22:05 | `753446a829ed…` | HEAD (detached) | 31 | ✓/✓ | ✓ `fcd69667…` (blob unchanged) |
| OUT-008 | kaidoku | `d1d981d2cc041dda4656c5b01d2c8445d8d17124` | 10-20 17:43 | `5c0b46c4d35f…` | HEAD (detached) | 8 | ✓/✓ | ✓ `63920930…` |
| OUT-009 | revenger | `cf02419276e5dd8aafb6fe09d4e9aaa6bcb78c97` | 10-19 19:35 | == pin | `main` | 0 | ✓/✓ | ✓ `63acc3d0…` |
| OUT-010 | tameshi | `01d586ddbc5fcd78659557c4e93a6ee8517b87d1` | 10-20 17:24 | `c144dcd80716…` | HEAD (detached) | 25 | ✓/✓ | ✓ `8006da5d…` (blob unchanged) |

Heading checks (`grep -cF` at pin and tip): `# mori-shokunin — Province`, `# kama-shokunin — Province`,
`# kagi-shokunin — Province`, `# mado-shokunin — Province`, `# kumitate-shokunin — Province`,
`# kaidoku-shokunin — Province`, `# revenger province`, `# tameshi-shokunin — Province` — all 1/1.

## Residual

- "Reachable" was exercised as the named `cat-file -e` object presence plus `log --all` ref-reachability;
  I did not require each pin to sit on the sibling's primary branch specifically (7/8 sibling workspaces
  are in detached-HEAD; revenger alone is on `main` at pin==tip). Detached-HEAD is a workspace
  observation, not a defect of the anchor claim.
- Pin ages rest on author-controlled commit timestamps (2026-10-19/20, consistent with the 2026-10-20
  capture window); no deeper provenance verification was attempted.
- I verified the quoted bytes and headings persist; whether each sibling's *live* declaration still
  supports the anchor's proposition semantically beyond the quoted bytes is out of this seat's scope
  (the intent note itself directs a re-read before any handoff).
- The inbound 114-pointer half of C1 (97 RESOLVES / 17 DRIFTED) was not attacked here.

Tooling directive: no installs or upgrades were needed or performed (system git, coreutils sha256sum,
grep, python3 only).

Scope: executed=`git -C tsukuroi-shokunin show 8e59163…:PROVINCE.md | grep -nE '[0-9a-f]{40}'`; `git -C tsukuroi-shokunin show 8e59163…:PROVINCE.md | wc -lc`; `git -C tsukuroi-shokunin show 8e59163…:PROVINCE.md` (full); `ls -d /home/vgpnk/Projects/shokunin/*-shokunin`; glob `*-shokunin`; for each (R,P) in {mori 91940fa339e3, kama e75cf680b534, kagi c2cab35bc92e, mado a4046a821608, kumitate 1770305fae20, kaidoku d1d981d2cc04, revenger cf02419276e5, tameshi 01d586ddbc5f}: `git -C R cat-file -e P^{commit}`; `git -C R show -s --format='pin %H %ci %s' P`; `git -C R rev-parse --abbrev-ref HEAD`; `git -C R rev-parse HEAD`; `git -C R show -s --format='tip %H %ci %s' HEAD`; `git -C R log --format=%H P..HEAD | wc -l`; `git -C R log --all --format=%H | grep -c ^P`; `git -C R show P:PROVINCE.md | sha256sum`; `git -C R show HEAD:PROVINCE.md | sha256sum`; `git -C R show {P,HEAD}:PROVINCE.md | grep -cF <anchor heading>`; `git -C R show {P,HEAD}:PROVINCE.md | grep -cF <anchor quote(s)>`; `git -C tsukuroi-shokunin show 8e59163…:corpus/knowledge/adjacency-anchors-r19.md | grep -nE '<8 blob-sha prefixes, 8 pin prefixes, sha256|stale|intentional|pin>'`; `git -C tsukuroi-shokunin show 8e59163…:PROVINCE.md | grep -nE 'portable ownership anchors|stale by design|^## |OUT-00'`; `mkdir -p tsukuroi-shokunin/.ufo/waves/round-19/falsify` (directory pre-existing); `ls` falsify dir and name-collision check; `git -C tsukuroi-shokunin show 8e59163…:.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json | python3 -c <read-only JSON walk printing outbound id/sibling/sibling_commit/sibling_blob_sha256>`
