source: S069 — own-work row, the round-19 pointer census `.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json` and the ten `PROVINCE.md` outbound pointers with their pinned sibling PROVINCE bytes; this entry's live-HEAD measurements are this lane's own re-reads of the eight sibling repositories at `git rev-parse HEAD` (see §2 and the round-66 receipts). The systemd v262 `systemd.credentials_boot_policy=` semantics quoted in §5 come from the systemd v262 release body (GitHub API, tag `v262`, sha256 `008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b`, section "Changes in the system and service manager:"), opened this round — open receipt `.ufo/waves/round-66/before/s283-open-receipt.txt`, registered in `corpus/SOURCES.md` as S283 by this round's C1 landing.
verified-at: 2026-11-03
recheck: 30d; procedure: `git -C /home/vgpnk/Projects/shokunin/<sibling>-shokunin rev-parse HEAD` then `git -C /home/vgpnk/Projects/shokunin/<sibling>-shokunin show HEAD:PROVINCE.md | sha256sum`, re-locate each register quote in those bytes, then `python3 tools/check-adjacency-anchors.py --revision <REV>`.

# Adjacency re-check — the ten sibling ownership anchors at live HEAD (round 66, C2)

## 1. What this entry claims

Round 19 published ten portable sibling-ownership anchors (`OUT-001`…`OUT-010`) as exact quotes with a pinned sibling commit and blob digest each. The register `corpus/knowledge/adjacency-anchors-r19.json` is the authority for that anchor set; `PROVINCE.md`'s section "Adjacent — portable ownership anchors (round 19)" is the prose form of the same rows. Round 66 re-reads all ten anchors at each sibling's **live** `HEAD` and records, per row, the live commit, the live `PROVINCE.md` blob digest, whether the register's quote is still present in those bytes, and where it sits. Ten of ten anchors are located.

This entry claims no new ownership, no sibling acceptance, and no re-pinning of the register. It is a measurement of the anchors' survival, plus an ownership-boundary table for the systemd boot-credential plane.

## 2. Method

For each register `outbound[]` record:

1. **Live HEAD** — `git -C /home/vgpnk/Projects/shokunin/<sibling>-shokunin rev-parse HEAD` (read-only plumbing; no mutating git verb is used anywhere in this entry).
2. **Blob digest** — `git -C /home/vgpnk/Projects/shokunin/<sibling>-shokunin show HEAD:PROVINCE.md | sha256sum` over the committed bytes at that HEAD, not the sibling's working tree.
3. **Quote located as the normalised substring** — the register's `quote` string is normalised (strip `**`, strip backticks, collapse whitespace runs, case-sensitive) and searched for in the normalised bytes of the live `PROVINCE.md`. The normalisation changes marker characters only; it does not fold case, punctuation, dashes or entities. A row is `located` only when the normalised quote is present in the live bytes; `unlocated` or `unreachable` is written when it is not, and is never written as `located`.
4. **The register is authoritative** for the anchor set — ids, sibling, sibling path, heading, quote and proposition come from `corpus/knowledge/adjacency-anchors-r19.json`; this entry does not restate, re-word or re-choose them.
5. **The register's pins are stale by design once a sibling commits.** The pinned `sibling_commit` and `sibling_blob_sha256` record the bytes as they stood in round 19; a sibling that commits since then necessarily moves both. At this recheck every one of the eight pins differs from its sibling's live HEAD and every one of the eight pinned blob digests differs from the live digest, while the anchored quote text still sits at the registered quote line. A stale pin is therefore not evidence of a broken anchor, and the anchor text surviving is not evidence of acceptance. The live values below are measurements; the register keeps its round-19 pins.

6. **Object existence, not row shape** — each row's 40-hex live HEAD was additionally checked with `git -C <sibling>-shokunin cat-file -e <HEAD>` (rc=0 for all eight distinct heads). A row whose hex columns merely match the shape of a live HEAD would pass a shape test while naming no commit; the existence check is what makes the column a fact. The quote re-location of step 3 is the second, independent discriminator: a fabricated HEAD would have no sibling file to locate the quote in.

Receipts for the measurements: `.ufo/waves/round-66/probes/c2-sibling-heads.txt` (HEADs, blob digests, per-anchor location, register-versus-live) and `.ufo/waves/round-66/drafts/c2-anchors-live.tsv` (the ten rows, one per anchor).

## 3. Live-verified anchor table

| AR | OUT | sibling | live HEAD | blob sha256 | status | locator |
|---|---|---|---|---|---|---|
| AR1 | OUT-001 | mori | 84c6cbc3b47c536a504aaee329c77897d389935e | 2af29312d28727b4dc91236b6f2ce188c0b721a3759e6a8cdaf73f98f4919838 | located | mori-shokunin/PROVINCE.md:9 |
| AR2 | OUT-002 | kama | 6035e952c2521999e192d6f236331f265ac98392 | f0aaae9ccfd0ecb6641ad1646934f4ff5555fcc45d2e397670b2eb5ff083e8a6 | located | kama-shokunin/PROVINCE.md:12 |
| AR3 | OUT-003 | kagi | 91f7752ba551092eef20f6bd43d6dd798dc88ba0 | 0bbf19b3019e780269259b1acbbd45fcb9a53139fe6337609e7bd6448b364edd | located | kagi-shokunin/PROVINCE.md:3 |
| AR4 | OUT-004 | mado | 524fa1f90b1f2de44b3019bacf833d54e0af13a0 | 01c55ed921b1eb9ebb571f5801525d6c1b49576bf3a1d9a28ca9a4c083943a17 | located | mado-shokunin/PROVINCE.md:6 |
| AR5 | OUT-005 | mori | 84c6cbc3b47c536a504aaee329c77897d389935e | 2af29312d28727b4dc91236b6f2ce188c0b721a3759e6a8cdaf73f98f4919838 | located | mori-shokunin/PROVINCE.md:8 |
| AR6 | OUT-006 | kumitate | 3c369336218329e30248b5d69c41348c02658169 | fa9a63a8f62331595858868496c0516df04dfea456b18351d1a01be062ae47ed | located | kumitate-shokunin/PROVINCE.md:3 |
| AR7 | OUT-007 | mori | 84c6cbc3b47c536a504aaee329c77897d389935e | 2af29312d28727b4dc91236b6f2ce188c0b721a3759e6a8cdaf73f98f4919838 | located | mori-shokunin/PROVINCE.md:12 |
| AR8 | OUT-008 | kaidoku | c7fe6898e9a8b3ff04486b4a1d672e9db37610c9 | 50b6c259beb6816e26b3af91e44e5317f82e40eaf94993701781221ef7bb98c4 | located | kaidoku-shokunin/PROVINCE.md:3 |
| AR9 | OUT-009 | revenger | 5915ad8d71c19ad377829d130ba1c35445eb32a4 | c49f6d1d11441728a9a9ed9abed7444837cf2cf0ee569681ad48340187c6f502 | located | revenger-shokunin/PROVINCE.md:3 |
| AR10 | OUT-010 | tameshi | f20ba482c7441d4c75818e7cd8a3165fee7821a1 | 0031aae86d34e39c753ac39ff4daf95a13761f9ba3992f221cc54c6c3bbb5a26 | located | tameshi-shokunin/PROVINCE.md:7 |

`located` count: 10 of 10. `unlocated`: 0. `unreachable`: 0.

## 4. The located quotes

The register quotes, verbatim, and where each was found at the live HEAD of §3.

| AR | OUT | register quote (verbatim) | located at |
|---|---|---|---|
| AR1 | OUT-001 | ``independently labeled user/system journals, plus cgroup `memory.events` and the explicit same-boot journal window after a retained anchor;`` | mori-shokunin/PROVINCE.md:9 |
| AR2 | OUT-002 | `` `GET /v1/models` vs `--alias` vs the configured model id`` | kama-shokunin/PROVINCE.md:12 |
| AR3 | OUT-003 | ``**Domain:** secrets & vault ops — the-janitor flows, credential hygiene evidence`` | kagi-shokunin/PROVINCE.md:3 |
| AR4 | OUT-004 | ``**Owns (surfaces):** `~/.config/hypr/` (hyprland.conf, keybinds, rules,`` | mado-shokunin/PROVINCE.md:6 |
| AR5 | OUT-005 | ``kill/OOM-related catalog-ID records and signal-11 coredump records`` | mori-shokunin/PROVINCE.md:8 |
| AR6 | OUT-006 | ``**Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime`` | kumitate-shokunin/PROVINCE.md:3 |
| AR7 | OUT-007 | ``**Refuses:** dispatch and orchestration mechanism (→ kumitate); OS package,`` | mori-shokunin/PROVINCE.md:12 |
| AR8 | OUT-008 | ``**Domain:** reverse engineering of shipped artifacts with REA on this Linux`` | kaidoku-shokunin/PROVINCE.md:3 |
| AR9 | OUT-009 | ``Owns: reverse engineering of shipped artifacts`` | revenger-shokunin/PROVINCE.md:3 |
| AR10 | OUT-010 | ``**Owns:** the method, documented from the fleet's existing gates`` | tameshi-shokunin/PROVINCE.md:7 |

[obs] The registered quote line equals the live line for all ten rows: the anchor text did not move inside its sibling's file while the sibling committed other work. [obs] No sibling's `PROVINCE.md` at live HEAD contains the strings `credentials_boot_policy`, `boot credential` or `null key` (bounded grep over the eight live `PROVINCE.md` files, 0 hits each), so no sibling declares the systemd boot-credential plane in its province.

## 5. Overlap table — the systemd boot-credential plane against the ADJ rows

The plane under examination is systemd v262's `systemd.credentials_boot_policy=` kernel command line option: it governs under which conditions a boot credential encrypted with the **null** key is accepted at boot, with the documented values `strict` (never), `tofu` (first boot or no TPM2), `relaxed` (SecureBoot disabled or no TPM2; the default and previous behaviour) and `off` (always); it has no effect on credentials encrypted against a host key or a TPM2 device, and its scope is boot credentials encrypted with the null key only. Each row below states what this lane keeps, who the recipient is under the cited `PROVINCE.md` ADJ row, and what the boot-credential plane touches. No new recipient is introduced; the ADJ rows are cited by id and by their `PROVINCE.md` line.

| ADJ row | tsukuroi retains | recipient | what the systemd boot-credential plane touches |
|---|---|---|---|
| ADJ-02 (`PROVINCE.md:47`) | The boot-side systemd and kernel-command-line surface of the plane: whether `systemd.credentials_boot_policy=` is present on the cmdline, the systemd unit's credential directive, and the on-disk mode and owner of the credential file — never the credential's value, never a vault reference, session byte or helper invocation. | `kagi` — secret material, vault operations and credential-hygiene evidence (kagi `PROVINCE.md:3`; `OUT-003`). | The *acceptance policy* for null-key boot credentials: a boot-time systemd configuration decision read from the cmdline and from TPM2/SecureBoot state. It is not a credential-hygiene finding: the policy names whether such a credential may be taken, not what any credential contains, and the null key offers neither confidentiality nor authenticity, so nothing here evidences a secret at risk. No ADJ-02 packet is raised. |
| ADJ-04 (`PROVINCE.md:49`) | OS memory, journal and boot diagnosis, and this lane's own boot-chain reads (kernel ring, systemd unit state, boot chain) for the plane's inputs. | `mori` — kill/OOM and host-pressure attribution, dated-event correlation, liveness and progress correlation (mori `PROVINCE.md:8`; `OUT-005`). | Nothing in ADJ-04's evidence classes. A cmdline policy token produces no kill or OOM event, no cgroup `memory.events` datum and no dated host-pressure incident; the census's prepared ADJ-04 handoff lines (kill-events, coredumps) are unaffected by it. The plane therefore raises no ADJ-04 request and no correlation question. |
| ADJ-06 (`PROVINCE.md:51`) | The shipped-artifact inventory facts only: systemd version, stub version, loader identity and provenance, as health inventory, with no binary-internals inference. | `protocol integrator — kaidoku/revenger ownership unresolved` (`PROVINCE.md:51`, unchanged; the shared scope stays arbitrated, not assigned). | Only the shipped systemd/stub binary's own internals would need reverse engineering; the v262 semantics of the option are documented upstream (release body and `systemd(1)`), so the plane is answered from documentation, not from a binary. No kaidoku/revenger packet is raised and no owner is selected for the shared scope. |
| ADJ-07 (`PROVINCE.md:52`) | The census and host-read implementation, its domain contract and its repair in this repository. | `tameshi` — the reusable verification and mutation-testing method, asked for as method advice (tameshi `PROVINCE.md:7`; `OUT-010`). | A method question only: whether the boot-credential policy deserves its own census case and its own mutation case. The advice is tameshi's; the gate and the case stay in this lane. |

## 6. Limits and unknowns

- [obs] The measurement is of committed sibling bytes at each sibling's `HEAD` on 2026-11-03. A sibling that commits afterwards is not covered until the next recheck.
- [unk] No sibling has acknowledged, accepted or acted on any row of §3 or §5; the anchors are this lane's reading of sibling declarations, not sibling confirmation. A located quote proves the text is present, not that the sibling agrees with this lane's reading of it.
- [unk] The register's round-19 pins and the live values of §3 differ for all eight siblings. Which of the two the gate should bind is the gate's choice; this entry records both and re-pins nothing.
- [unk] The host values of the systemd boot-credential plane (cmdline token presence, TPM2 device, SecureBoot state, boot chain) are measured in this round's C1 note `corpus/knowledge/systemd262-credentials-boot-policy-r66.md` and its receipts under `.ufo/waves/round-66/probes/`; §5 states only the ownership boundaries and does not restate or re-judge those measurements.
- Not applicable: this entry states no external claim about any upstream project other than the documented v262 semantics quoted in §5, and it cites no `corpus/SOURCES.md` row of its own beyond S069 (own-work) and the v262 release body registered as S283 by this round's C1 landing.

## QUALITY check

Author-side, on this draft's bytes at authoring, 2026-11-03. Not independent verification; it admits nothing.

1. Falsifiable: each row of §3 fails if `git rev-parse HEAD` at the named sibling differs from the recorded 40-hex value, if the recorded 64-hex digest differs from `sha256sum` of that sibling's `HEAD:PROVINCE.md`, or if the §4 quote is absent from the located line. The lane gate runs at integration, not here.
2. Source: every number in §3 comes from the two round-66 receipts named in §2; every ownership boundary in §5 cites a `PROVINCE.md` ADJ row by id and line, and the only upstream statement (the v262 semantics) names its document and sha256.
3. Separation: the HEADs, digests and quote locations are observations; "the anchors survived" and "the pins are stale by design" are inferences drawn from them; the ownership boundaries in §5 are readings of sibling declarations against this lane's own scope.
4. Errata append-only: the round-19 anchor rows are untouched here; the round-66 correction to the inbound register lands as an appended `## Erratum (round 66)` block in `corpus/knowledge/adjacency-anchors-r19.md`, never as an edit to a filed line.
5. Rejection kept: no row is dropped, re-pinned to a more convenient quote, or upgraded; a row that did not locate would read `unlocated`.
7. External claims: the single upstream statement is the v262 `systemd.credentials_boot_policy=` semantics, quoted from the release body named on the `source:` line.
9. Negative claims: the only negative claims are the two zero-hit greps, both bounded to the eight live sibling `PROVINCE.md` files and dated. No claim is made about sibling trees, sibling history or sibling conduct.
21. Portable locators: each row carries a repo-relative path with a line and a 40-hex commit plus a 64-hex blob digest, so a reader can re-derive the bytes without this lane.
30. Whole-proposition counts: "10 of 10" names the finite set `OUT-001`…`OUT-010` and is broken out per row in §3; the "0 unlocated / 0 unreachable" counts name the same set.
