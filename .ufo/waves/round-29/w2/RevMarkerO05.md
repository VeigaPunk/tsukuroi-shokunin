# RevMarkerO05 — attack on C1 marker O05 at 10d5288fc1051364e711203855e7c53710dfcc21

Verdict: holds — the O05 marker at SKILL.md:2320 is correctly shaped, the original is unchanged, `qualified` is the right verdict, and both basis lines resolve and support the `now` text. One minor imprecision noted, non-blocking.

## Findings

1. [obs] Marker location and shape: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md:2320` carries `[R29-OWED-O05] verdict: qualified | original: "so nothing in that chain is monitored" | now: No ManagedOOM candidate exists in the four-unit auto chain, but units with OOMRules= are also monitored, and an active systemd-oomd.socket can accept local-account cgroup reports. | basis: corpus/knowledge/memory-pressure-r25.md:387, corpus/knowledge/memory-pressure-r25.md:390`. Exactly one occurrence of `R29-OWED-O05` across all six target files (grep: SKILL.md 1, the five other target files 0). The counter v2 (sha256 c3f9cfe7…) run in a sandbox clone reports `"id": "O05", "ok": true` and summary `marked: 12` at the tip.

2. [obs] (a) Original unchanged: the MP4 table row at SKILL.md:2316 still contains the anchor as a verbatim substring and its line hash at both base `16e9ab2a` and tip `10d5288f` is sha256 `afd272877b3af52d245defc77e8ebed62e0a4ff04d09f9af294114a9e1a6370f` (hash of line bytes without newline), matching the counter's BASE_DIGEST for O05. M1 satisfied. (Working-tree `sed -n 2316p | sha256sum` gives 180d4f50…, differing only by the trailing newline; the counter hashes `splitlines()` output.)

3. [obs] (b) Verdict `qualified` is correct: on this host the original clause was literally true at capture time — `OOMRules=` is empty on the four read units (memory-pressure-r25.md:387) and systemd-oomd.socket is inactive and disabled (:390) — so the statement is not false and `rebutted`/`corrected` would mischaracterize it; it is incomplete as a general rule, which `qualified` plus the scoping `now` text addresses.

4. [obs] (c) Basis resolution and support: `corpus/knowledge/memory-pressure-r25.md:387` exists, is non-blank, is not a marker line, and states units with `OOMRules=` are also monitored (citing S121 lines 1633-1644, S123 lines 115-116) while `OOMRules=` is empty on the four read units. `corpus/knowledge/memory-pressure-r25.md:390` exists and states systemd-oomd.socket listens with mode 0666 when active so a running daemon could take cgroup reports from local accounts. Both support the `now` claims directly.

5. [obs] Underlying bytes verified by refetch: `systemd.resource-control.xml` v262 sha256 `d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8` (matches S121/S136) lines 1642-1644: "will monitor this unit's cgroup and evaluate the specified rulesets against it." (OOMRules= entry). `oomd-manager.c` v262 sha256 `052f19b36d54997b78c4ca93fae17d8c8513ce7240b0b58a47a1efdad0da3a15` (matches S123): OOMRules reports populate `monitored_rules_cgroup_contexts`; MANAGED_OOM_AUTO removes the cgroup from the monitored map; the varlink server binds `VARLINK_PATH_MANAGED_OOM_USER` with mode 0666 (line ~1288). Snapshots at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/RevMarkerO05/`.

6. [obs] `now` claim A ("No ManagedOOM candidate exists in the four-unit auto chain") is consistent with MP4 (all four units and the ancestor chain `auto`) and with the code path that removes AUTO cgroups from the monitored map. Only numeric token in `now` is "four-unit", matching the four captured units of MP4 (user@1000.service, user-1000.slice, user.slice chain); nothing else to recompute.

7. [obs, minor, non-blocking] `now` says the socket "can accept local-account cgroup reports" without the basis's qualifier "for cgroups they own". The code (oomd-manager.c ~lines 96-111) rejects reports whose cgroup owner UID differs from the sender UID, so accepted reports are restricted to owned cgroups. The `now` text is capability-true but slightly wider than the basis; a reader could over-scope it. Not a defect against the counter rules; worth noting only.

8. [obs] Lineage note: basis :387 cites S121, which is superseded by S136 for exactly the OOMRules= widening the marker relies on (SOURCES.md:142: "supersedes S121 — ... and also OOMRules=, make a cgroup a systemd-oomd monitoring candidate"). The marker claims what S136 documents, so support is real; citing :387 reaches the same fact. Non-defect.

## Residual risk / verification gaps

- [inf] None blocking. The marker's `now` omits the "cgroups they own" restriction (finding 7) — cosmetic over-breadth, not falsity.
- [obs] Mechanical checks all pass at the tip: counter v2 `ok: true` for O05, `marked: 12`, exit 0 in the sandbox clone.

Scope: read=SCORECARD.md declaration, SKILL.md:2287-2358, memory-pressure-r25.md:373-402, tools/check-owed-statements-r29.py, corpus/SOURCES.md S121/S122/S123/S136/S137 rows, fetched systemd v262 systemd.resource-control.xml and oomd-manager.c; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/RevMarkerO05.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/RevMarkerO05/{systemd.resource-control.xml,oomd-manager.c}, /fast/scratch/hyaku/tsukuroi-r29/RevMarkerO05/repo (clone); executed=git clone/checkout at tip (read-only at lane), python3 tools/check-owed-statements-r29.py --revision 10d5288f… --lane <sandbox>, sha256sum, grep, sed, curl -sL
Model: not exposed
Installs: none
