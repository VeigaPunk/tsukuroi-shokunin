VERDICT: defect-found (one sibling pin moved by this round; zero contested-scope hits; zero sibling references to C2's scrub-record surface)

# ConnSiblings — X-2 sibling-overlap scan, round 42 wave w1

Scope: all 20 sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin`
(tsukuroi excluded), read-only, files `PROVINCE.md` + `SKILL.md` at lane root
(ver also nested `.ufo/waves/…/assimilation/…` copies where present). Terms: pipefail,
SIGPIPE, `grep -q`, btrfs scrub, scrub.status, scrub_speed_max, /var/lib/btrfs,
line pins into `tsukuroi-census.sh`.

## Commands run (all read-only)

```sh
# cwd = /home/vgpnk/Projects/shokunin
for d in *-shokunin; do [ "$d" = "tsukuroi-shokunin" ] && continue; \
  for f in "$d/PROVINCE.md" "$d/SKILL.md"; do [ -f "$f" ] || continue; \
    grep -HnE 'pipefail' "$f"; grep -HnE 'SIGPIPE' "$f"; \
    grep -HnE 'grep[[:space:]]+-q' "$f"; grep -HnE 'btrfs|scrub' "$f"; \
    grep -HnE '/var/lib/btrfs' "$f"; done; done
grep -rniE 'SIGPIPE|EPIPE|exit[[:space:]]+141|141' --include=PROVINCE.md --include=SKILL.md *-shokunin | grep -v '^tsukuroi-shokunin/'
grep -rnE 'grep[[:space:]]+-[a-z]*q|grep[[:space:]]+--quiet' --include=PROVINCE.md --include=SKILL.md *-shokunin | grep -v '^tsukuroi-shokunin/'
grep -rnE 'tsukuroi-census\.sh:[0-9]+' --include=PROVINCE.md --include=SKILL.md *-shokunin | grep -v '^tsukuroi-shokunin/'
grep -rnE 'tsukuroi-census' --include=PROVINCE.md --include=SKILL.md *-shokunin | grep -v '^tsukuroi-shokunin/'
grep -rnE 'census\.sh:[0-9]*(,|:|[0-9])*(692|694|1621|1635|1641|1652)' --include=PROVINCE.md --include=SKILL.md *-shokunin | grep -v '^tsukuroi-shokunin/'
# lane-side verification (read-only git)
git log --oneline -- tools/tsukuroi-census.sh c8efaa3f120834541f8de1e5e0367e8d1593bae6..f50c28d83e1832ecd7eba765caace531f45d6b27
git diff c8efaa3f120834541f8de1e5e0367e8d1593bae6 f50c28d83e1832ecd7eba765caace531f45d6b27 -- tools/tsukuroi-census.sh
git show f50c28d83e1832ecd7eba765caace531f45d6b27:tools/tsukuroi-census.sh | sed -n '1095,1120p'
git show c8efaa3f120834541f8de1e5e0367e8d1593bae6:tools/tsukuroi-census.sh | sed -n '1092,1117p'
```

Full raw output (receipts): `ConnSiblings/grep-all.txt`, `ConnSiblings/grep2.txt`.

## Hits

### 1. mori-shokunin/PROVINCE.md:287 — live line pin into the census (MOVED by this round)
Quote:
> **Adjacency (wave-2 finding CriticHarmAxes A1; wave-1 ConnectSiblingPsi):** tsukuroi's census reads the same
> system `/proc/pressure/memory` file (`../tsukuroi-shokunin/tools/tsukuroi-census.sh:376,1100-1115`) for OS memory
> triage and routes fleet correlation of host pressure to mori (`../tsukuroi-shokunin/PROVINCE.md:30-33`). Shared
> evidence is not shared ownership: mori reports the reading as fleet resource runway; explaining a high IRQ or
> memory reading as a device, driver or OS fault stays with tsukuroi.

Same text persists in mori's assimilated copies at `.ufo/waves/round-42/assimilation/validate/PROVINCE.md:287` and `.ufo/waves/round-43/assimilation/validate/PROVINCE.md:287`. Last touched in `7c77fba3` ("round-24: wave-2 source corrections … PROVINCE adjacency note") — predates this round.

**Pin motion by round 42:** the only commit touching the census between base `c8efaa3` and tip `f50c28d` is `447662088` (C1 implementation; +33/−8). Its first hunk (`@@ -689,9 +689,12 @@`, probe_packages) inserts 3 net lines, shifting every line after it by +3. The pinned content — the memory-pressure arm intro ("Round-7 addition, lane S7-2 … Fails closed …") — sits at **base 1097-1112** and at **tip 1100-1115**. So relative to the round start, the `:1100-1115` coordinate target moved +3; at tip the named content happens to sit exactly at the pinned coordinates again. This is a bookkeeping side effect of the C1 fix, not a semantic claim by mori.

`:376` half: identical at base and tip (before the first hunk); round 42 did not move it. Note for the record: the actual content at line 376 is a btrfs/sysfs comment, not pressure; the `/proc/pressure/memory` default constant lives at line 455 in both base and tip. The `:376` coordinate is a pre-existing quirk of the pin, not introduced by this round.

Classification: **not contested scope** (mori explicitly disclaims ownership of this surface: "Shared evidence is not shared ownership"), but it is a **pin this round moved** (coordinate target shifted +3 by 447662088).

### 2. mori-shokunin/SKILL.md:438 — btrfs monitoring adjacency (not contested)
Quote:
> - **Never threshold the btrfs chunk percent.** Data-chunk fill reads **94.25%**
> while `df -P` Capacity on the same device reads **10%**; a probe that used the
> chunk percent would fire `DISK_LOW` against every proposed default today.

Adjacent to C2's btrfs surface (same filesystem family) but a distinct record: mori monitors data-chunk fill percent, not the scrub status record. No sibling anywhere references `scrub.status`, `scrub_speed_max`, `/var/lib/btrfs`, or scrub start/cancel/resume semantics — C2's record surface is **not claimed or pinned by any sibling lane**.

### 3. tameshi-shokunin — census as mutation-testing target (historical blob pins, already tracked as stale)
- `PROVINCE.md:32`: lists `tools/tsukuroi-census.sh` among read-only primary surfaces (no line pin):
  > `corpus/checklist-run.sh`, tsukuroi `tools/tsukuroi-census.sh`, mado
- `SKILL.md:675-677`: `tsukuroi-shokunin/tools/tsukuroi-census.sh` — a four-plane host-health census (bash, 977 lines, sha256 `084951be…c78c5` at measurement) — historical blob pin from round 5, with `mutation-case-tsukuroi-census.md` knowledge docs.
- `SKILL.md:1046`, `:1175`, `:1184`, `:1406`: `bash-tsukuroi-census` rows pin historical blobs (`084951be…`, `bba6cdf6…`, `10452443`; `165307fe`, `aa136d69`, `af8adf15` revisions) and **already flag `stale`** against the moving census head ("blobs — no drift at this read: tsukuroi-census `084951be…` → `bba6cdf6…`"). These are deliberate pins to old revisions, not live coordinates; this round's C1 change will advance their staleness, which their own table already accommodates.

Classification: **not contested scope** (tameshi uses the census as a mutation target and tracks drift deliberately; no claim on the surfaces C1/C2 touch).

### 4. kengaku-shokunin — `pipefail` in unrelated frozen-recipe convention (not contested)
`PROVINCE.md:382,430,481`; `SKILL.md:1000,1080`: `bash -euo pipefail` appears only inside kengaku's own Docker/container frozen-recipe execution spec (e.g. "runs a frozen recipe under `bash -euo pipefail`, then imports the captured module"). No connection to census probe pipelines, SIGPIPE, or `grep -q`; distinct domain. Classification: **not contested**.

## Zero hits
Across all 20 sibling lanes' PROVINCE.md/SKILL.md (root + nested copies):
- `SIGPIPE` / `EPIPE` / exit-141 semantics: none (the `141` matches are line numbers, counts, and hash fragments — noise).
- `grep -q` (and `-qs`/`--quiet`) variants: none.
- `scrub.status`, `scrub_speed_max`, `/var/lib/btrfs`: none.
- Pins to this round's changed census lines (`:692/:694/:1621/:1635/:1641/:1652`): none.
- Any sibling referencing round-42 claims (R41-CENSUS-PIPEFAIL-692, C1 size-invariance counter, C2 scrub-record counter): none (chousa's "round-42" rows are its own quarantine-check gates).

## Net effect on the round's axes
No sibling claims, borrows, or contradicts the C1 pipefail fix or the C2 scrub-record surface (adjacency axis: clean). One live cross-lane coordinate (mori PROVINCE.md:287 `:1100-1115`) shifted +3 by the C1 implementation commit; the pinned content still exists and re-aligns with the stated coordinates at tip — mori's adjacency note remains semantically true. No action proposed (report, do not absorb). No host mutation, no counters run, no scratches left behind.

## Verification of my own output
All evidence above comes from the executed commands' observed output (raw receipts in `ConnSiblings/grep-all.txt`, `ConnSiblings/grep2.txt`; git show/diff output captured in the session). I did not run the C1/C2 counters, did not run the census, and did not modify anything in the lane, the fleet root, or any sibling.
