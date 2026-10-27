VERDICT: draft

# Seat ConnFrontier — item X-3: round-46 planned row (draft; routed defect D4)

Lane: tsukuroi-shokunin; round 45, wave a2w1.
Basis:
- `SCORECARD.md:2819-2826` (Axes scores at round-44 final measured surface: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency tied lowest);
- `SCORECARD.md:2840-2844` (stale round-43 planned row carried into round 44, routed defect D4);
- `SCORECARD.md:2847-2891` (round-45 declaration, freeze ea6e0ee3, base 5bbd5ff5, impl 18389f44);
- `corpus/lessons/round-44-verifier-spotcheck.md` §5 (routed defects D1–D10 and still-open list);
- `PROVINCE.md:154-295` (storage integrity, Frontier vs Core, scrub record and NVMe SMART boundaries);
- `corpus/README.md` `## Frontier` (lines 28-43, 241-245, 293-302, 313-317, 331-349, 371-400, 412-415, 424-426, 436-452);
- `corpus/knowledge/btrfs-scrub-record-r44.md:153-161` (pending SR7–SR9 status appended in round 45, routed defect D3);
- `corpus/knowledge/btrfs-scrub-grounding-r45.md` (GR1–GR3 grounding rows landed in round 45);
- `tools/tsukuroi-census.sh` (baseline lookup at `:777` and latent early reader sites);
- `tools/score-scrub-arm-r44.py:47-50,630` (`channels_open`: mount table, uid_map, script path);
- Host capture: `/dev/nvme0n1` mode 0660 root:disk, uid 1000 not in group disk, sudo forbidden.
Receipt: `.ufo/waves/round-45/a2w1/ConnFrontier/evidence-captures.txt`.

---

## 1. Verified anchors and evidence

1. **Axes ordinals and lowest axis selection:**
   - At round 45 base and tip, the ordinals stand: `depth 8`, `coverage 9`, `operability 9`, `freshness 9`, `calibration 9`, `adjacency 8`.
   - `depth` and `adjacency` are tied lowest at 8.
   - `adjacency` cannot be claimed or elevated unilaterally by this lane: recipient-side acknowledgement, acceptance, and closure require external sibling action (`PROVINCE.md:77-79`), ADJ-06's recipient is unresolved (`PROVINCE.md:51,79-80`), and mori declares no intake format for ADJ-04 (`PROVINCE.md:193`). Adjacency must remain unclaimed and unharmed (repairing harms like D1 IN-109 repin without claiming ordinal uplift).
   - Therefore, **`depth` is the sole lowest axis that can be legitimately claimed and improved by this lane in round 46**.

2. **Candidate 1: Binding SR7–SR9 with counted reads (`depth` axis):**
   - In round 44, `corpus/knowledge/btrfs-scrub-record-r44.md` introduced SR7 (ioctl success direction / dev-replace), SR8 (`scrub_speed_max` attribute, `%llu` read, `memparse` write, 0 limit, in-memory only), and SR9 (packaged `btrfs-scrub@.timer`/`.service`, monthly, SIGINT stop, canceled record).
   - In round 44, the depth gate failed (`tools/check-scrub-record-r44.py`: `verdicts_ok 0`), and the post-read narrowings for SR8/SR9 were unjudged by counted seats (`corpus/lessons/round-44-verifier-spotcheck.md` §2 C2, routed defect D3).
   - In round 45, C2 grounded the three inferences in `corpus/knowledge/btrfs-scrub-grounding-r45.md` as rows GR1 (`memparse` parser in cmdline.c/kstrtox.c/sysfs.c), GR2 (`btrfs_scrub_dev` replace caller in dev-replace.c), and GR3 (`systemctl stop` SIGINT/SIGCONT/SIGKILL sequence in systemd v262). An append to `btrfs-scrub-record-r44.md:153-161` marked SR7–SR9 pending until counted non-author reads bind them.
   - In round 46, binding SR7–SR9 with counted non-author reads (reviewer and critic seats in wave 1, residual wave seats if `partly`) under a residual-capable counter (`tools/check-scrub-record-r46.py`) formally admits SR7–SR9, resolves defect D3, and directly improves the `depth` axis.
   - **Do-nothing control:** A do-nothing control (e.g. K0 base with no counted verdict files) evaluates `verdicts_ok` to 0 and fails closed.

3. **Candidate 2: Census `:777` baseline lookup and latent readers (`operability` axis):**
   - Round 45 C1 converted the five single-line `head -n1` readers by parameter expansion (`probe_systemd` state, timer Result `r`, `probe_drivers` driver, `probe_journal` t_word, timer ActiveState `r`) and added 6 selftest cases labelled `(R45-C1)` (cases 148 -> 154), including `r45-foreign-baseline-large` verifying that driving `TSUKUROI_FOREIGN_BASELINE` past the pipe buffer does not exit 141.
   - However, the lookup itself at `tools/tsukuroi-census.sh:777` remains:
     `bn=$(printf '%s\n' "$base_txt" | awk -v n="$nm" '$1 == n && !f { print $2; f = 1 }')`
     This executes in a `while read -r nm ver _; do ... done <<< "$CAP_OUT"` loop over every live foreign package.
     For $N$ foreign packages and a baseline of $M$ lines, this executes $N$ subshells and $N$ `awk` processes, each scanning the entire baseline text ($O(N \cdot M)$).
   - In addition, the declaration limits in `SCORECARD.md:2881-2884` and `C1ExecMaskedSites.md` documented seven unclaimed latent early-reader sites (`:707`, `:832`, `:997`, `:1196`, `:1517`, `:1531`, `:1817`). Notably, `:832` (`HoldPkg` in `probe_packages_plane`):
     `holds=$(grep -hE '^[[:space:]]*HoldPkg' "$PACMAN_CONF_FILE" 2>/dev/null | head -n1 | sed -E 's/^[[:space:]]*HoldPkg[[:space:]]*=[[:space:]]*//' || true)`
     is an early reader inside an unmasked probe path that currently relies on `|| true`.
   - In round 46, converting `:777` to an in-process bash dictionary (`declare -A base_map`) populated in a single pass over `$base_txt`, and converting `:832` to parameter expansion without subshells or early readers, eliminates the subprocess storm and finishes the pipefail/early-reader debt.
   - **Do-nothing control:** Scored by `tools/score-census-baseline-r46.py`, requiring in-process lookup verification and performance bounds; a do-nothing base retaining the awk subshell loop fails.

4. **Candidate 3: The C1 live-leg channels of `score-scrub-arm-r44.py` (Counter hardening / specification):**
   - `tools/score-scrub-arm-r44.py:47-50,630` reports `'channels_open': ['mount table', 'uid_map', 'script path /mnt/census-lib.sh']`. An evasion mutant could inspect `/proc/self/mountinfo` (tmpfs on `/sys/fs/btrfs`), `/proc/self/uid_map`, script execution path `/mnt/census-lib.sh`, or process ancestry (unshare/python3) to behave honestly only in the test harness and dishonestly on the live host.
   - While critical for counter integrity, this is not an independent user-facing axis: it is a counter-hardening requirement (QUALITY 90/91). Rather than inflating the plan with a redundant operability or calibration claim, this requirement is folded into the counter specification for any scrub-arm re-score as frozen should-fail evasion controls.

5. **Candidate 4: NVMe SMART (Privilege-gated — evaluated and rejected for round 46):**
   - Storage integrity includes NVMe SMART/Health lifetime fields (`smartctl -H -A`, `nvme smart-log`; SH5/SH6, `PROVINCE.md:162-164`).
   - Ground check: On this host, `/dev/nvme0n1` is `brw-rw---- 1 root disk`. The seat user is `uid=1000(vgpnk) gid=1000(vgpnk)` and is not in group `disk`. Sudo is strictly forbidden by host guard rules.
   - Unprivileged invocations fail:
     `smartctl -H -A /dev/nvme0n1` -> `Smartctl open device: /dev/nvme0n1 failed: Permission denied` (exit 2).
     `nvme smart-log /dev/nvme0n1` -> `Failed to open /dev/nvme0n1: Permission denied` (exit 13).
   - An unprivileged census arm would read constant `BLOCKED (permission denied)` on the live host.
   - On a host where the live query is constant `BLOCKED`, a live-agreement check cannot distinguish an honest implementation from a do-nothing stub emitting `BLOCKED` (the R39 discrimination limit).
   - Sudo allow-listing or mock injection is outside lane authority (read-only lane; no host mutation).
   - **Conclusion:** NVMe SMART remains Frontier (`PROVINCE.md:279`). It cannot be promoted to Core or claimed in round 46.

---

## 2. Synthesis (the one move)

Adopt a bounded two-claim planned row for Round 46 on two distinct axes:
1. **C1 (depth):** Binding SR7–SR9 of `corpus/knowledge/btrfs-scrub-record-r44.md` with counted reads from non-author seats, lifting the "pending, not admitted" mark and admitting the rows under a residual-capable counter `tools/check-scrub-record-r46.py`.
2. **C2 (operability):** Converting the census foreign baseline lookup (`tools/tsukuroi-census.sh:777`) from the $O(N \cdot M)$ `printf | awk` loop into an in-process dictionary lookup (`declare -A`), and converting the latent early reader `HoldPkg` (`:832`) to parameter expansion, counted by `tools/score-census-baseline-r46.py`.

Second-order effects and non-harm:
- Improves the lowest axis (`depth` at 8) without harming `adjacency` (remains 8, zero anchor drift).
- Does not regress `operability` (9), `coverage` (9), `freshness` (9), or `calibration` (9).
- Fold open counter channels (C1 live-leg evasion) into the counter specification as frozen should-fail controls.
- Explicitly documents why NVMe SMART remains Frontier.

---

## 3. Exact proposed text for SCORECARD.md

Replace the stale round-43 row at `SCORECARD.md:2840-2844` with the following:

```markdown
- **planned (next round):** (1) depth — bind the pending scrub-record rows SR7–SR9 (`corpus/knowledge/btrfs-scrub-record-r44.md`) with counted non-author reads (reviewer and critic seats in wave 1; residual wave seats if `partly`), admitting the rows following their round-45 grounding (GR1–GR3 in `corpus/knowledge/btrfs-scrub-grounding-r45.md`) under a residual-capable counter `tools/check-scrub-record-r46.py` (closing routed defect D3; depth is tied lowest at 8); (2) operability — in `tools/tsukuroi-census.sh`, convert the foreign baseline lookup (`:777`) from the $O(N \cdot M)$ per-package `printf | awk` subprocess loop into an in-process bash dictionary lookup (`declare -A base_map`), and convert the latent early reader `HoldPkg` (`:832`) to parameter expansion, eliminating process spawns and completing early-reader cleanup without pipefail hazards; (3) counter hardening — fold the open C1 live-leg evasion channels (`mount table`, `uid_map`, `script path`, ancestry) into frozen should-fail controls under QUALITY 91. NVMe SMART stays Frontier (privilege-gated: `/dev/nvme0n1` root:disk 0660; unprivileged user not in group disk; sudo forbidden; constant BLOCKED fails the live discrimination test). Adjacency stays unclaimed (tied lowest at 8; recipient acknowledgement and intake format require external sibling action).
- **retired:** none.

## Round 46 — declaration (planned row, draft)

Base: the round-45 measured tip. Ordinals at base: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency are tied lowest; C1 works depth; adjacency stays unclaimed — recipient-side acknowledgement, acceptance and closure cannot be produced by this lane (`PROVINCE.md:77-79`), ADJ-06's recipient is unresolved (`PROVINCE.md:51,79-80`), mori declares no intake format for ADJ-04 (`PROVINCE.md:193`), and no sibling declares storage-integrity ownership — and must not be harmed. Saturation 9 / window 3 unchanged. This round binds the pending scrub-record rows SR7–SR9 (grounded by round-45 GR1–GR3) on the depth axis, and eliminates the census foreign-baseline subprocess loop on the operability axis. NVMe SMART stays Frontier: its reads require root or group `disk` privilege (`/dev/nvme0n1` mode 0660; no sudo), giving a constant `BLOCKED` live answer that cannot be distinguished from a do-nothing stub.

| Claim | Axis | Surface moved | Counter (frozen; sha256 named at freeze) | Before at base (expected) | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | depth (sourced: S237, S240, S242, S243, S244, S245, S246, S247, S248, S249) | `corpus/knowledge/btrfs-scrub-record-r44.md`: lift the pending/unadmitted status of SR7 (ioctl success direction / dev-replace), SR8 (`scrub_speed_max` attribute, `%llu` read, `memparse` write, 0 limit, in-memory only), and SR9 (packaged `btrfs-scrub@.timer`/`.service`, monthly, SIGINT stop, canceled record); bind all three rows with non-author counted reads (reviewer and critic seats in wave 1, residual wave seats for any `partly` reads) under the residual-capable depth counter | `python3 tools/check-scrub-record-r46.py --revision <REV>` (frozen) | FAIL (`verdicts_ok 0`, pending status marked) | `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1` | Any quote outside frozen window; any proposition token missing; any counted seat reads `fails`; any `partly` verdict unbacked by an admitted residual; base not resolved; verdict file differs from committed orchestrator transcript. |
| C2 | operability | `tools/tsukuroi-census.sh`: (a) convert the packages-plane foreign baseline lookup (`:777`) from the per-package `printf '%s\n' "$base_txt" \| awk ...` loop into an in-process bash dictionary lookup (`declare -A base_map`) populated in a single pass over `$base_txt`, turning an $O(N \cdot M)$ process storm into an $O(N + M)$ in-memory lookup; (b) convert the latent early reader `HoldPkg` (`:832`) to parameter expansion; (c) add selftest cases asserting correct baseline classification and latency bounds on large baselines | `python3 tools/score-census-baseline-r46.py --revision <REV> --scratch <DIR>` (frozen) | FAIL (awk subprocess loop present; HoldPkg early reader present) | `baseline_subprocesses == 0 and early_readers == 0 and baseline_match == 1 and selftest_pass == 1 and selftest_cases >= 156` | Any subprocess spawned during foreign package baseline lookup; any early reader in production probe paths; any change in live census line values or exit code; census writes a file in live mode; predecessor census counter PASS -> FAIL. |

Pre-data controls (scored with the frozen counters before any seat):
- C1: K0 do-nothing base (verdicts 0; must FAIL), K1 scripted writer, K2 line references shifted, K3 dropped source, K4 mention-not-assertion, K5 padded verdict line, K6 contradictory JSON verdict, K7 no pointer, K8 gutted quote, K9 doctored duplicate SOURCES row, K10 duplicate row in fenced block, K11 duplicate verdict_line keys, K12 top-level array record file, K13 orphan repo: each must FAIL; K14 valid binding + residual wave seats must PASS.
- C2: K0 do-nothing base (must FAIL), K1 awk loop retained, K2 early reader retained at :832, K3 wrong drift detection, K4 associative array collision, K5 here-string temp file creation: each must FAIL; K6 in-process dictionary implementation must PASS.
```

---

## 4. Verification and evidence checks

- Grounding files inspected: `PROVINCE.md`, `corpus/README.md`, `corpus/knowledge/btrfs-scrub-record-r44.md`, `corpus/knowledge/btrfs-scrub-grounding-r45.md`, `tools/tsukuroi-census.sh`, `tools/score-scrub-arm-r44.py`, `SCORECARD.md`.
- No lane files mutated (report and receipt written exclusively under `.ufo/waves/round-45/a2w1/ConnFrontier*`).
- Scratch directory `/fast/scratch/hyaku/tsukuroi-r45/ConnFrontier` created and cleaned on exit.
