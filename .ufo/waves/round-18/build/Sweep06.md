# Sweep06 — C3 recon: corpus/knowledge/update-safety-v2.md

[obs] Working bytes = baseline 842a5312 (`git diff` empty); S060 = .ufo/waves/round-18/l1-capture/host-capture-r18.txt.

Dated §1–§4 untouched; listed statements are current-use; quotes verified in baseline:

| # | v2 quote (line) | now (S060) |
|---|---|---|
| 01 | (2 lines, rc=0, **0 configs**) (:208) | configs home/root; `SNAPPER_CONFIGS="root home"` (:76-80); "snapshot-less" (:210) fails; restoration untested |
| 02 | `pacman-contrib` absent (error text); installing it is out of province (:213) | `pacman-contrib-1.13.1-1` (:36), `/usr/bin/paccache` (:83); `checkupdates` not invoked [inf] |
| 03 | `uname -r` = `pacman -Q linux` = `7.2.3-arch1-3` (:215) | `7.2.11-arch1-1` (:6); linux `7.2.11.arch1-1` (:32) |
| 04 | nvidia/610.57.04, 7.1.4-arch1-1 (:217) | dkms `nvidia/615.78.08` for `7.2.11-arch1-1` (:92-95); no 610.57.04 row |
| 05 | no `.db.sig` stored (5 `.db`, 0 `.sig`) (:221) | `openai-chatgpt.db.sig` (:54), db (:53); fifth repo [inf] |
| 06 | **Preserve, don't update:** copy `offline.db` (:257); recheck bsdtar -tf /var/lib/pacman/sync/offline.db (:315) | sync listing lacks `offline.db` (:48-54); both moot |
| 07 | 13 × `elephant*` 2.21.0-1 (:162) | `elephant-2.22.1-1` via `pacman -U` from yay cache (:30, :72) |
| 08 | `mkinitcpio 41.1-1` installed with 42.2-1 pending (:383) | `mkinitcpio-42.2-1` (:34); R17-FRESH-01 sibling |

Precedent: update-safety-v3.md:447-453 carries R17 notices for U1/U3/elephant; v2 missed.

Proposed: ten records R18-FRESH-Sweep06-01…10 (U1/offline.db split per quote):

`## R18-FRESHNESS — update-safety-v2 U1–U4 and offline-exile current-use values (2026-10-20)`

Historical 2026-10-14 and R15 bytes remain preserved and dated; only the statements above are superseded. S060 is the source; S052 corroborates U1/U3. Read-only: no package, service or reboot clearance; snapshot restoration untested.

[unk] S060 probes no U5 (`-Suu`), U6 (`/boot`), U8 (load) or cache counts; no notice. §5 pins stay live per S052 (`HoldPkg = pacman glibc`). No LSP target for Markdown.

Scope: executed=git show/status/diff (read-only); no probes.
