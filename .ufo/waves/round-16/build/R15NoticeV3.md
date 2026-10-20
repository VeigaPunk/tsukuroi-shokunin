# R15NoticeV3 — R15 notice facts

Observed at baseline `db68e620`; working-tree bytes identical (SHA256 `84b3d6c5…`). Literal reads; no Markdown LSP/semantic proof.

- R15 notice: `corpus/knowledge/update-safety-v3.md:395-415`, heading `## R15-UPDATE-STATE (2026-10-20) — current-use supersession`.
- Snapshot: `.ufo/waves/round-15/build/host-snapshot.json`, captured `2026-10-20T07:44:39Z`, SHA256 `b101f3747827cefd0ed604c14b669267ec0fcc1b6c2fbe6e486be0cdbbc6ea81` (matches). Holds `pacman -Qu` exit 0, 413 rows; `libinput 1.32.0-1`, `libinput-tools 1.32.0-1`, `mkinitcpio 41.1-1`, `systemd 261.2-1`; decision `BLOCKED_FOR_AGENT_PACKAGE_ACTION`.
- Wrong locator `:398`: `The §7 rank 1 row “Do nothing now”` (`§7 rank 1` occurs once). Actual row `:216` under `## 5. Risk-ordered operations table (recommendation only — nothing here was run)` (`:208`); row_key `| 1 | Do nothing now |`. Quote candidate `` `-Syu` would be INERT: 0 candidates by three probes `` occurs once in §5 (also `:398`, outside it).
- Preserve: 2026-10-14 bytes; `No agent install, upgrade, downgrade or service action is authorized.`; operator-only assessment; full `-Syu` behind the news gate; `/new_root`-only hooks → mkinitcpio-42 untested, no clearance; no host repair claimed. `## R16-RANK-SECTION — citation-only erratum` supersedes the §7 label only, retaining R15 current-use supersession.

Unverified: errata JSON and gate absent at baseline; no gate output seen.
