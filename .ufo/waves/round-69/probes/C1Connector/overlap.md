2026-11-03T23:22:17Z

# C1Connector — sibling-overlap and duplication scan (round 69, w1)

Seat `C1Connector` (leaf, read-only). Lane `tsukuroi-shokunin`, measured base
`acce353bacad74043636018d829e9e9b8e0fdf1c`, declaration at
`920a9eea3c5c5400567be0e96141014f338973df` (lane HEAD, clean tracked tree).
Scratch: `/fast/scratch/hyaku/tsukuroi-r69/C1Connector` (removed at exit).

Surfaces this round touches (from `SCORECARD.md` "Round 69 — declaration", read at
`SCORECARD.md:5185-5240`): **T** kernel taint / `/proc/sys/kernel/tainted` (C1 note + C2
`tainted=`/`taint_bits=`), **V** vermagic (C1 note), **M** kernel module tree (C1 note + C2
`modules_tree=`), **R** kernel release / `uname -r` vs `pacman -Q linux` (C2 `release=`,
`pkg=`, `pkgver=`), **P** reboot pending (C2 `pending=`).

## 0. Preconditions and receipts

```
$ git -C tsukuroi-shokunin rev-parse HEAD
920a9eea3c5c5400567be0e96141014f338973df
$ git cat-file -t acce353bacad74043636018d829e9e9b8e0fdf1c9   # the string as written in the seat spec
fatal: Not a valid object name acce353bacad74043636018d829e9e9b8e0fdf1c9
rc=128
$ git rev-parse acce353b
acce353bacad74043636018d829e9e9b8e0fdf1c
$ git log -1 --format='%s' acce353b
round-68 verifier spot-check (integrator, hyaku): non-author admit/reject
$ git merge-base --is-ancestor acce353b 920a9ee ; echo rc=$?
rc=0
```

Both spec arguments are 41 hex characters (append a trailing `9`); the real commit is the
40-hex `acce353bacad74043636018d829e9e9b8e0fdf1c` and it is an ancestor of the declaration.
Transcription defect in the spec text, not an unreachable revision. Recorded so no seat
reports the base as BLOCKED.

`drafts/` and `probes/` held no files when this scan ran (`find .ufo/waves/round-69/drafts
-type f` printed nothing), so duplication is judged against the declared predicates, not
against written drafts.

## 1. Sibling lane scan — `PROVINCE.md` at each live HEAD

```
$ for s in audio chousa game-dev-2d game-dev-3d kagi kaidoku kake kama kasegi kengaku kotoba \
    kotodama kumitate lore mado mori revenger souji tabi tameshi; do
    d=/home/vgpnk/Projects/shokunin/$s-shokunin
    echo "$s $(git -C "$d" rev-parse HEAD)"
    git -C "$d" grep -n -i -E 'taint|vermagic|/proc/sys/kernel|module tree|modules_tree|kernel release|uname -r|reboot pending|tainted' HEAD -- PROVINCE.md
  done
rc=0 overall; grep rc=1 (no match) in 19 of 20 siblings, rc=0 in kasegi only
```

Sibling HEADs (all `rev-parse HEAD`, rc 0): mori `84c6cbc3b47c536a504aaee329c77897d389935e`,
kama `6035e952c2521999e192d6f236331f265ac98392`, kaidoku
`c99e907cb5576c13a7b22755d776b356fdfc1752`, revenger
`5915ad8d71c19ad377829d130ba1c35445eb32a4`, souji
`b4ef0bc84ada3fb3aefd6a0b1a841a6517b84acd`, tameshi
`f20ba482c7441d4c75818e7cd8a3165fee7821a1`; the remaining fourteen as printed by the
command above.

| surface | sibling | HEAD | located line + quote | verdict |
|---|---|---|---|---|
| T taint | all 20 | see above | no line matches `taint`/`tainted`/`/proc/sys/kernel` in any sibling `PROVINCE.md` | no-claim |
| V vermagic | all 20 | see above | no line matches `vermagic` | no-claim |
| M module tree | all 20 | see above | no line matches `module tree`/`modules_tree` | no-claim |
| R kernel release | all 20 | see above | no line matches `uname -r`/`kernel release` | no-claim |
| P reboot pending | all 20 | see above | no line matches `reboot pending`; `\breboot\b` over all 20 sibling `PROVINCE.md` files also returns nothing | no-claim |
| — false positive disclosed | kasegi | `c81eef717ee72f6911b0155992e52299403a56da` | `PROVINCE.md:205` F39, "…the bounded method and its stated uncertainty, and the cyber-range results…" | no-claim (the regex `taint` matched inside "cer**taint**y"; no kernel surface) |

Near-miss claims that are adjacent, not owned (each read at HEAD):

| sibling | line | quote | why not this surface |
|---|---|---|---|
| mori | `PROVINCE.md:24` | "**Kill/OOM classes** — structured, MESSAGE-free journal records carrying catalog IDs for kernel-OOM unit notices, oomd notices, coredumps…" | claims kernel **OOM event** records, not the taint/release/module-build plane |
| mori | `PROVINCE.md:44` | "**FR1 — Kernel OOM event-time attribution and fleet correlation** (state F1/F8 + art F2). First evidence: `corpus/knowledge/kernel-oom-line-attribution-r12.md:10-16`…" | event-time attribution of OOM lines only; "Kernel event-time attribution … remain frontier" (`:37`) |
| kaidoku | `PROVINCE.md:32-34` | "citing its `evidence_id` and subject sha256. When module identity matters … the evidence ID alone does not authenticate module attribution" | "module" here is an REA reversing **module**/artifact, not a kernel module |
| kaidoku | `PROVINCE.md:132` | "GSP blobs: 56/156 regions mapped (`ev_0388cb9a…`) … nvidia ucodes correct-empty" | shipped-artifact **internals** (firmware blob regions), the refused side of tsukuroi `PROVINCE.md:26-28` |
| revenger | `PROVINCE.md:10` | "`corpus/training/bounty-triage/MODULE.md`: a written scope record gates access" | a training-module file, not a kernel module |
| kama | — | no `kernel|module|nvidia|dkms` line in `PROVINCE.md` (domain line 3: "local model serving & endpoint health") | kama owns endpoints; the driver plane stays here via ADJ-01 (`tsukuroi PROVINCE.md:46`) |
| souji / tameshi | — | no line on any of the five surfaces (souji domain: "fleet repository & workspace hygiene") | no-claim |

No sibling `SKILL.md` corroborates a claim either (corroborating read, not the item's
method): `git -C <sib> grep -n -i -E 'vermagic|/proc/sys/kernel/tainted|UNSIGNED_MODULE|OOT_MODULE|modules_tree' HEAD -- SKILL.md`
returns rc 1 for mori, kama, kaidoku, revenger, souji and tameshi.

**Conclusion.** The five surfaces are unclaimed by every sibling. Taint/vermagic/module-tree is
not a cross-lane contested surface and needs no handoff row; the only neighbours are mori's
OOM event-time plane and kaidoku/revenger's artifact internals, both already routed by
`PROVINCE.md` ADJ-04 and ADJ-06.

## 2. Duplication inside the lane (at `920a9ee`)

```
$ git -C tsukuroi-shokunin grep -n -i -E 'taint|vermagic|modules_tree|module tree|kernel release|uname -r' \
    920a9eea3c5c5400567be0e96141014f338973df -- corpus/
rc=0 (166 matching lines across corpus/)
$ grep -c -i taint PROVINCE.md ; grep -c -i vermagic PROVINCE.md ; grep -c -i reboot PROVINCE.md ; grep -c -i uname PROVINCE.md
0 / 0 / 0 / 0        (each grep rc=1)
$ grep -n -i -E 'kernel|round-27' PROVINCE.md
12:driver/firmware plane (kernel modules, nvidia driver + GSP firmware
180:Overlap register against mori's admitted entry ... at mori commit `ef9dbee1...`
```

`PROVINCE.md` **never names taint, vermagic, a module-tree read or a reboot-pending
verdict.** The lane's only kernel claim is the domain line `PROVINCE.md:12-13` ("driver/firmware
plane (kernel modules, nvidia driver + GSP firmware presence, `nvidia-smi` shape)"). The taint
plane is registered in `SKILL.md` and `corpus/knowledge`, not in PROVINCE. That is an
append-only registration gap, not a sibling conflict.

Counting rule for `C1_LANE_DUP`: one locus = one `file:line` that asserts one of the five
surfaces with a host reading or a mechanism sentence. Process history (`corpus/lessons/`),
tool sources and `SCORECARD.md` are excluded; incidental word matches are not counted.

| # | locus | quote | relation to the r69 rows |
|---|---|---|---|
| D1 | `corpus/knowledge/kernel-taint-r27.md:19` | "| KT1 | How the taint number is encoded; what 12288 decodes to | 12288 = bit 12 (O) + bit 13 (E); no other bit, so no warning (W), oops (D) or soft lockup (L) recorded this boot | HEALTHY |" | **duplicate** — same decode, same host value; a KR row on 0–19 decoding must cite KT1 as prior ground, not as new |
| D2 | `corpus/knowledge/kernel-taint-r27.json:18` | "\"statement\": \"/proc/sys/kernel/tainted prints the kernel's taint mask as a decimal number; 0 means untainted and every set bit names one reason…\"" | **duplicate** — JSON companion of D1 (QUALITY 71 companion rule applies to any new KR companion) |
| D3 | `corpus/knowledge/kernel-taint-r27.md:52` | "KT5: \"a sysctl write only adds bits\" holds for bits below `TAINT_FLAGS_COUNT`; higher bits in the written value are ignored…" | **refine** — already limits bit semantics; a KR row that says "closed table 0–19" must reconcile with `TAINT_FLAGS_COUNT` |
| D4 | `corpus/knowledge/driver-firmware-plane.md:85` | "`vermagic: 7.2.3-arch1-3 SMP preempt mod_unload`. Only kernel tree present:" | **duplicate + stale contradiction** — a 7.2.3-era vermagic and a single-tree claim, superseded in-file at `:274` and `:278` |
| D5 | `corpus/knowledge/driver-firmware-plane.md:101` | "- Taint lines this boot (1 each): `nvidia: loading out-of-tree module taints" | **duplicate** — the O/E observation the KR note re-measures |
| D6 | `corpus/knowledge/driver-firmware-plane.md:274` | "- Stale: \"Kernel `7.2.3-arch1-3` (uname -a; built 2026-09-06)\" — [obs] running kernel 7.2.11-arch1-1 (uname -r)." | **duplicate (release)** — current value already corrected |
| D7 | `corpus/knowledge/driver-firmware-plane.md:278` | "- Stale: \"Only kernel tree present:\" — [obs] /usr/lib/modules holds 6.18.57-2-lts and 7.2.11-arch1-1; no 7.2.3-arch1-3 tree is listed." | **duplicate (module tree)** — matches `before/host.txt`; `modules_tree=PRESENT` re-asserts it |
| D8 | `corpus/knowledge/boot-chain-r17.md:92` | "6.18.57-lts module trees), none holds a file newer than the boot (B:257: count 0; B:258: 58674" | **duplicate (module tree)** — the same two trees, from a boot-input sweep |
| D9 | `corpus/knowledge/update-safety-note.md:296-298` | "`ls /usr/lib/modules/` = `7.2.3-arch1-3` only; `uname -r` = `7.2.3-arch1-3`; `pacman -Q linux` = `7.2.3.arch1-3` ⇒ **no kernel reboot is pending today**" | **contradict (stale)** — one tree and release 7.2.3, no in-file correction; the live reading is two trees / 7.2.11. This is the exact derivation C2's `pending=` reproduces at a stale value |
| D10 | `corpus/knowledge/host-health-report-r3.md:320` | "already failed once; `uname -r` = `pacman -Q linux` = `7.2.3` → no reboot pending today" | **duplicate (pending)** at a stale release; must not be cited as the current `pending=` basis |
| D11 | `corpus/knowledge/update-safety-v2.md:215` | "- **Kernel/DKMS coupling — U3.** `uname -r` = `pacman -Q linux` = `7.2.3-arch1-3`;" | **duplicate (release)** — corrected in-file at `:403` (R18) |
| D12 | `corpus/knowledge/freshness-recheck-r17.json:408` | "\"stale_reason\": \"States that the only kernel module tree is 7.2.3-arch1-3; /usr/lib/modules now lists 6.18.57-2-lts and 7.2.11-arch1-1 and no 7.2.3 tree.\"" | **duplicate (module tree)** — the staleness of D4/D9 is already tracked here |
| D13 | `corpus/knowledge/freshness-recheck-r18.json:9` | "\"reason\": \"Line 118 says uname -r and pacman -Q linux are both 7.2.3; the R18 capture reads kernel 7.2.11-arch1-1 and local-db linux-7.2.11.arch1-1.\"" | **duplicate (release)** |
| D14 | `corpus/knowledge/package-state-plane.md:336` | "- `uname -r`" (recheck procedure) | **duplicate (procedure)** — the release read is already a registered procedure line |
| D15 | `corpus/knowledge/adjacency-handoffs-fleet-r1.md:93` | "\| `uname -r` \| `7.2.3-arch1-3` \| 0 \|" | **duplicate (release)** at a stale value; usefulness is the command/exit shape, not the value |
| D16 | `corpus/knowledge/host-drift-recheck-r64.md:36,38` | "stale `7.1.4-arch1-1` registration (tree gone; `ls /lib/modules` = 7.2.3 only) — `SKILL.md:49`" | **duplicate (module tree)** — a round-64 row still cites a one-tree listing while the round's own `before/host.txt` records two |
| D17 | `corpus/README.md:250` | "## Round 27 — kernel taint (deeper entry inside the driver and firmware area)" | **duplicate (coverage registration)** — the surface is already registered as deeper ground, which is the QUALITY 68 wording r69 must also use |
| D18 | `SKILL.md:2422` | "## Kernel taint — round 27" (KT1–KT6 table at `:2428-2433`; log→action rows at `:2437-2438`) | **duplicate (operative table)** — the lane already holds an operator table for exactly these bits |
| D19 | `SKILL.md:49` | "`modinfo nvidia` and `ls /usr/lib/firmware/nvidia/*/` …" in the Driver & firmware plane row | **duplicate (surface registration)** — the vermagic/module read is already a listed probe |

19 loci across 15 files. Nine of them (D1-D3, D17, D18 and the taint half of D5) are the
round-27 entry; the remaining ten are one-line host readings scattered through
`driver-firmware-plane.md`, the two freshness-recheck companions, `update-safety-*`,
`host-health-report-r3.md`, `package-state-plane.md`, `adjacency-handoffs-fleet-r1.md`,
`boot-chain-r17.md`, `host-drift-recheck-r64.md`.

### 2a. Source-registry duplication — S288 is byte-identical to S140

```
$ sha256sum .ufo/waves/round-69/before/src/tk-v7211.rst
727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841  .ufo/waves/round-69/before/src/tk-v7211.rst
$ sha256sum .ufo/waves/round-27/sources/S140.rst
727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841  .ufo/waves/round-27/sources/S140.rst
$ cmp -s .ufo/waves/round-69/before/src/tk-v7211.rst .ufo/waves/round-27/sources/S140.rst ; echo cmp_rc=$?
cmp_rc=0
$ grep -n '727ddb82' corpus/SOURCES.md
146:| S140 | Linux v7.2 Documentation/admin-guide/tainted-kernels.rst — … | docs | A | … raw bytes sha256 727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841; snapshot .ufo/waves/round-27/sources/S140.rst (191 lines) |
$ grep -c -E '^\| S28[89] ' corpus/SOURCES.md
0   (rc=1)
$ grep -n -i vermagic corpus/SOURCES.md
(no output, rc=1)
```

| surface | sibling | HEAD | located line + quote | verdict |
|---|---|---|---|---|
| T taint, **source row** | lane (r27) | `920a9ee` | `corpus/SOURCES.md:146` S140, "raw bytes sha256 `727ddb82…5f9a0841`" | **duplicate — re-pin only**: S288's declared digest (`SCORECARD.md:5196`) equals S140's registered digest and the two snapshots are byte-identical (`cmp` rc 0). S288 adds a stable-tag URL (v7.2 → v7.2.11) and no new bytes |
| V vermagic, **source row** | none | — | no `vermagic` row exists in `corpus/SOURCES.md`; S289 is the first | **lane-retains, new ground** (registered bytes absent, unlike S288) |

Re-pin convention in this registry, as answered from the table (not prose): `S280`/`S281`
(round 64) carry the link **inside the teaches cell** as
`supersedes S021 — re-pin: the hook still hardcodes /new_root …` and
`supersedes S022 — re-pin: the late hook still passes --new-root-dir=/new_root; fetched bytes identical to installed …`
(`corpus/SOURCES.md:290-291`); earlier examples are S104 `supersedes S087 — two notice…`,
S109 `supersedes S094 — the helper create…`, S199 `supersedes S024 (the mutable main URL, left …)`.

So: **S288 adds no authority over S140 — it is a re-pin of identical bytes.** Registered
without a `supersedes S140 — re-pin: …` cell it is a second, unlinked registration of the same
document, which is registry duplication. Either the S288 row carries that supersede wording, or
the r69 note must cite S140 for the bytes and treat S288 as the URL re-pin only. S289
(`include/linux/vermagic.h`) is genuinely new source ground and needs no supersede cell.

## 3. Boundary check against the round's own declarations

Lines in `PROVINCE.md` at `920a9ee`: `:12-13` (owns "kernel modules, nvidia driver + GSP
firmware presence, `nvidia-smi` shape"), `:26-28` ("**Refuses:** … binary RE of drivers (→
kaidoku/revenger — tsukuroi tracks *state and health*, not internals). Never installs,
upgrades, or removes packages; never restarts services. Detection and report; the operator
remediates."), `:46` (ADJ-06: "Driver/firmware/package mechanism requires shipped-artifact
reverse engineering beyond health inventory | Loaded version, package provenance and
driver/boot symptoms; **no binary-internals inference**").

| id | risk | boundary line it would cross | status |
|---|---|---|---|
| B1 | A KR row drawing a **loader-compatibility conclusion** from the vermagic string (module X is ABI-loadable into kernel Y), or reading `.modinfo` out of the `.ko` instead of `modinfo` | `PROVINCE.md:26-28` + `:46` ADJ-06 ("no binary-internals inference") | open — reading `modinfo -F vermagic` and comparing its prefix to `uname -r` is state comparison (already registered at `SKILL.md:49`); interpreting load-worthiness is module-internals mechanism |
| B2 | C2's `pending=` reuses the **same token** as the existing `PLANE update-safety: … pending=` (`tools/tsukuroi-census.sh:1904`, `pending=none|REQUIRES-PREP(candidates=N…)`) with a different meaning (kernel reboot vs package upgrades) | no PROVINCE line forbids it; it is an output-contract ambiguity, not an ownership conflict | open — renaming to `reboot_pending=` (or `kernel_pending=`) removes the collision with zero cost; `unreadable=<n>` already follows the census convention (`DRIFT pacnew-plane`, `TREE`, `INITRAMFS` lines) |
| B3 | `pending=YES` read as an instruction to reboot, or `detail=` naming the repair | `PROVINCE.md:30-32` "Never … restarts services. Detection and report; the operator remediates." | open — the declaration's "verdict-neutral" wording covers it only if `detail=` carries state, never an action |
| B4 | `taint_bits=<csv>` decoded against the **closed 0–19 table** silently drops a set bit ≥ 20 (the snapshot's table ends at `19) ``J``` — `.ufo/waves/round-69/before/src/tk-v7211.rst:189`) | the declaration's own "closed bit→log table 0-19"; `kernel-taint-r27.md:52` already records that `TAINT_FLAGS_COUNT` bounds writes, not reads of the mask | open — a value with a bit outside the table must read `taint_bits=UNKNOWN` or carry `detail=bit20+`; dropping it is a false-complete decode |

Not a risk: C2's `pacman -Q linux` read (state query, allowed; the declaration already used it)
and C1's upstream kernel-source reads (precedent S140-S145, round 27). Neither C1 nor C2 reads
module internals, attributes a performance symptom, or decides a repair, as declared.

## 4. Results

```
C1_SIBLINGS=20
C1_OWNED=0
C1_CONTESTED=0
C1_LANE_DUP=19
C1_BOUNDARY_RISK=B1-vermagic-loader-inference,B2-pending-token-collision,B3-pending-as-remediation,B4-taint-bits-past-19
```
