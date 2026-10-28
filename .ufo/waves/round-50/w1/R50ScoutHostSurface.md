VERDICT: supports

No drift on the named host values. The live scrub and storage answers are still the constants in the lane limits. The only capture byte that moved is the timestamp.

Re-ran `bash .ufo/waves/round-45/frozen/hostcap/capture.sh` at 2026-10-28T19:11:00Z (uid 1000, rc 0). Script and frozen `capture.txt` match freeze `8029cdba1049df25632c91a23c8db4eefb54be5f` (capture.txt sha256 `f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70`; capture.sh sha256 `c6d2c448c83de3326109a29638d55d7083ee93edd4242a845b050bc180a751fc`). Nine live lines vs nine frozen lines: value diff excluding the timestamp token is 0. Receipts: `.ufo/waves/round-50/w1/R50ScoutHostSurface/capture-live.txt`, `comparison.txt`.

| Field | Frozen / entry | Live 2026-10-28T19:11Z |
|---|---|---|
| CapEff | `0000000000000000` (capture.txt:1) | `0000000000000000` |
| devids | `1` on fsid `1d02a454-c549-4a35-b567-89d60902af8e` (capture.txt:9) | `devids=1`, same fsid |
| scrub_speed_max | mode 644, owner root, value `0` (capture.txt:8) | same |
| exclusive_operation | not in capture.sh or capture.txt (capture.sh:23-30; grounding `:146`). Host reading: mode 444, `none` (`corpus/knowledge/btrfs-scrub-grounding-r45.md:150-151`) | `/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/exclusive_operation` mode 444 owner root value `none` |
| replace_target | same host reading: mode 444, `0` (`btrfs-scrub-grounding-r45.md:150-151`) | `.../devinfo/1/replace_target` mode 444 owner root value `0` |

Lines 2-7 of the capture (kernel `7.2.11-arch1-1`, systemd `262 (262-1-arch)`, unit_show, stop_default, both dropin_owner `none`, empty unit_dropins) are identical to capture.txt:2-7. Timestamp only: frozen `2026-10-27T02:09:52Z`, live `2026-10-28T19:11:00Z`.

Census: `bash tools/tsukuroi-census.sh` started 2026-10-28T19:11:13Z, ended 19:11:18Z, rc 1. Script sha256 `aeda2cbcdcc4b08b09fefcddc237da7c0d8ee903aaf063a1578452081e0245dc` equals the freeze blob. The three scrub-record probes (`probe_scrub_record` in `tools/tsukuroi-census.sh:1980-2043`: record directory, `scrub_speed_max`, enabled timers) printed:

`SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0`

That is the constant at `PROVINCE.md:287` (`NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0`). No `detail=` suffix.

`STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0`

That is the constant at `PROVINCE.md:236` (`HEALTHY 1/1/0`). Full output: `.ufo/waves/round-50/w1/R50ScoutHostSurface/census-live.txt` (9117 bytes). Exit 1 is the six-plane rollup `TSUKUROI_CENSUS: DEGRADED` (packages, drivers, journal, update-safety, oom). STORAGE and SCRUB are not rollup terms (`tools/tsukuroi-census.sh:371-373`, print at `:3798-3804`, rollup at `:3806-3815`).

`git diff --stat 8029cdba1049df25632c91a23c8db4eefb54be5f -- PROVINCE.md corpus/knowledge/btrfs-scrub-grounding-r45.md tools/tsukuroi-census.sh .ufo/waves/round-45/frozen/hostcap/capture.txt .ufo/waves/round-45/frozen/hostcap/capture.sh` was empty. Worktree HEAD was `39e694934cf6c56434987edc730e8b3580a251f3`; those five paths match the freeze bytes. No tool installed. Census `--selftest` was not run. Scratch `/fast/scratch/hyaku/tsukuroi-r50/R50ScoutHostSurface` removed after the receipts were copied.
