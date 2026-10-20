# Sweep04 — C3 recon: driver-firmware-plane.md

model: opencode-go/deepseek-v4.1-flash. Read-only; no host probe, no execution.

## Confirmed stale current-use statement

[obs] `corpus/knowledge/driver-firmware-plane.md:178` — "`checkupdates` absent: not on PATH, and `pacman -Q pacman-contrib` →" (2026-10-14 probe). Present-tense availability only.
[obs] R18 capture shows `pacman-contrib-1.13.1-1` installed: `.ufo/waves/round-18/l1-capture/host-capture-r18.txt:36`, captured 2026-10-20T16:06:17-03:00.
[obs] The file's own D1 erratum (`:260`) already prescribes pacman-contrib's `checkupdates`; body and erratum disagree.
[inf] The dated probe stays historically true; only the live availability claim is superseded.

Proposed append-only notice (heading absent baseline 842a531):

## R18-FRESHNESS — update-route availability re-verified (2026-10-20)

Append-only. The 2026-10-14 observation above keeps its date; this supersedes current-use availability only. Read-only; no package, service, or reboot clearance. Source S060 (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:36`).

- Stale: "`checkupdates` absent: not on PATH" — [obs] `pacman-contrib-1.13.1-1` is installed at 2026-10-20T16:06:17-03:00 (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:36`). `checkupdates` was not invoked this round [unk]; availability only, not a sync or update finding.

## Already noticed — no second heading

[obs] `:183-185` "Local sync DB snapshot: `core.db`, `extra.db`, `multilib.db` mtimes" / "2026-09-08 15:23; `omarchy.db` 2026-10-11 10:16": R17-FRESHNESS `:279` already supersedes the dates; R18 `:42-46` confirms five DBs including `openai-chatgpt.db`, also present at R17 `fresh-capture.txt:14`. Census delta fits R17's bullet.
[obs] `:187` "`pacman -Si nvidia-utils` → 610.57.04-1": R17 `:284` already corrects installed nvidia-utils to 615.78.08-1 (`fresh-capture.txt:25`); the query was not re-run [unk].
[obs] `:268` `recheck:` pacman probes are replaced by R17-RECHECK `:289-294` for steer rounds.

## Bounded no-evidence [unk]

Neither capture lists `/lib/firmware/nvidia/610.57.04/`, `modinfo nvidia`, `nvidia-smi`, `lsmod`, `/proc/driver/nvidia/params`, GPU firmware `:10`, `dmesg_restrict`, or package rows `lib32-nvidia-utils`/`libva-nvidia-driver`/`linux-firmware-nvidia` (`:72-76`, `:113-140`). R17 `:272` already declares the blob tree, `params`, `:10`, and `lsmod` unverified; no notice proposed; claims stay dated 2026-10-14 observations.

Scope: executed=none
