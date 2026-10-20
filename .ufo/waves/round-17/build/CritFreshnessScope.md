# CritFreshnessScope — C2 reject-list (R17)

Abbrev: FC=`.ufo/waves/round-17/l1-capture/fresh-capture.txt`, BC=`…/boot-chain-capture.txt`, PL=`/var/log/pacman.log` (read 2457-2473, 2899-3160), v3=`corpus/knowledge/update-safety-v3.md`, r15=`corpus/knowledge/partial-upgrade-recheck-r15.md`.

Reject any R17 bullet/record that:

1. **Asserts pending/currency** ("0 pending", "-Syu INERT", "413 resolved", "up to date"). [obs] FC has no `-Qu`. Core/extra `%y` 10-17 22:37 (FC:10-12) predates r15's `%w` birth (r15:15); omarchy 09:09:26 predates sync marker 09:15:30 (FC:7,13). [inf] mtime≠refresh time; never compare `%y` with `%w`.
2. **Refreshes dated captures**: v3 §3/§6 (2026-10-14) already routed (v3:395-410). Target only current-use text (v3:407-415; r15:13-17,112-118). QUALITY 23.
3. **Implies authorization**: "gate cleared", "safe to reboot", lifting BLOCKED (r15:109), or pacman/sudo/dkms/systemctl recheck steps. Local-db dir names ≠ running state (r15:62-67).
4. **Edits bytes**: non-suffix diff, or any JSON-twin change (gate checks .md only). QUALITY 4.
5. **Cites outside captures**: capture_ref to PL/uncommitted paths (elephant 2.22.1 PL:3095; btrbk removed PL:3148).
6. **Unbounded negatives**: "no pacnew/pacsave" covers PL 2462-3063 only (FC:79-82), excluding fwupd, AUR `-U`, two `-Rns` (PL:3064-3160). FC:77-80 are aborted commands. QUALITY 9.
7. **Misnames the transaction**: argv `-Syu --needed --noconfirm` + 13 targets (PL:2462); 448 (FC:84) counts it alone.
8. **Misdates images**: 09:18 in-transaction UKIs (PL:3014,3046) superseded by 09:26 files (BC:125).
9. **Exploits gate gaps**: end notice section at next `## ` (initramfs gets two R17 headings); require capture_quote ⊆ observed_now; pin capture sha256 (BC appended at :255).

[unk] scribe drafts unseen (no R17 headings yet).

Scope: executed=none
