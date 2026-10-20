# FreshDriverFirmwarePlane — round 17

Behavior: appended `## R17-FRESHNESS — dated host re-verification (2026-10-20)` to `corpus/knowledge/driver-firmware-plane.md` (new lines 269–284; original 268 lines untouched, tag 39DF). Fragment: `.ufo/waves/round-17/build/fresh/driver-firmware-plane.json`, 11 records `R17-FRESH-DRIVER-FIRMWARE-PLANE-01..11`.

Stale current-use pins found (all from the note's pinned anchors :3-6, :72, :80-90, :113, :184-186, :198): kernel 7.2.3 → 7.2.11 [obs boot-chain-capture.txt:5]; boot 2026-10-13 → 2026-10-20 09:57:08 [:6]; NVRM 610.57.04 → 615.78.08 [fresh-capture.txt:33]; `/lib/modules` 7.2.3 only → 6.18.57-2-lts, 7.2.11-arch1-1 [fresh:41]; dkms 7.1.4/7.2.3 registrations → 615.78.08 rows, 7.2.3 built modules missing [fresh:36-38]; sync-DB mtimes [fresh:10-13]; nvidia-open-dkms/utils 615.78.08-1 [fresh:24-25; boot-chain:52]; `linux-7.2.11.arch1-1` [fresh:21].

Not flagged: dated measurements and errata (2026-10-14 probes, 2026-10-19 D1 erratum, log-line sweeps).

Unverified [unk]: loaded module path under 7.2.11, `/proc/driver/nvidia/params`, GPU firmware `:10`, `/lib/firmware/nvidia/610.57.04/`, lsmod. `pacman -Si` not re-run.

Baseline caveat: baseline quotes were copied from the working-tree file (tag D950); byte identity to commit 6923fe0bd3add04fc90f3bc3522895b27cf44bbe was not checked (no git reads in this seat). L1 gate must confirm.

Out of scope, routed: `recheck:` header (line 268) prescribes `pacman -Qo`, which the round steer forbids; `pacman-contrib` "not found" (§5 :178-179) is contradicted by boot-chain-capture.txt:55 and :59 (package lane).

Installs/updates: none.

Scope: executed=none
