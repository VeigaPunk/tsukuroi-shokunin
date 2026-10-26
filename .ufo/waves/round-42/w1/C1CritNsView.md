VERDICT: defect-found — the frozen predicate does not distinguish a census fixed for production from one fixed only where the counter watches. Three view-gated censuses (one gated on `TSUKUROI_FIXTURE`-or-uid-0, one gated on the fabricated package list alone) all score **PASS** on the exact predicate sentence, while an independent measurement at production identity shows one of them still reads `DEGRADED` where `BLOCKED` is due.

# C1-10 — namespace legs vs QUALITY 82 and 85 (seat C1CritNsView)

Counter under test: `tools/score-size-invariance-r42.py`, sha256 `c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03` (matches the declaration at `SCORECARD.md:2573`); lane tip `87c4f7c627e377e5f6d361498e8db9b3886d7953`; census at the tip 181172 bytes.

## 1. Answer to the question asked

No. The predicate's five conjuncts (`tools/score-size-invariance-r42.py:43,365-366`) are all reachable by a census that restores the round-41 defect whenever it is *not* under observation. The two watched conditions the counter creates are both readable by the scored shell script from inside the leg: `TSUKUROI_FIXTURE` (set by `env_for`, `:106`) and uid 0 (the `unshare -rm` identity). A third condition, the fabricated package list itself, is readable in every leg and is not closable by any stub-based leg at all.

## 2. Every channel through which the code can tell an N leg from a production run

Measured inside a faithful copy of the counter's own `NS_INNER` (`:273-274`) with the counter's own `ns_leg` env (`:280-282`): receipt `C1CritNsView/ns-channels.txt`.

| # | Channel | Observed in the leg | Production | Strength |
|---|---|---|---|---|
| 1 | uid/euid | `uid=0 euid=0 user=root` | 1000 | **decisive, one test** |
| 2 | fabricated probe data | `-Qq` answers `alpha beta gamma delta`; the PLANE line prints `sample=4(alpha,beta,gamma,delta)` | 1409 real names | **decisive, no namespace test needed** |
| 3 | `/proc/self/mountinfo` | `419 358 0:75 / /mnt rw,relatime - tmpfs tsk …` and `420 … /pacman /usr/bin/pacman rw,relatime - tmpfs tsk …` | neither mount exists | strong |
| 4 | identity of `/usr/bin/pacman` | `Bourne-Again shell script, ASCII text executable`, 150 bytes, first line `#!/bin/bash`, body names `/mnt/qq`, `/mnt/qkk`, `/mnt/real-pacman` | ELF, 157872 bytes | strong — and it *reaches* the view: `ls /mnt` shows `qq`, `qkk`, `qkk.rc` readable |
| 5 | `HOME` / `TMPDIR` | `<scratch>/ns/home`, `<scratch>/ns/tmp` (host paths under the counter's own scratch dir) | `/home/vgpnk`, unset | strong |
| 6 | environment shape | exactly `PATH=/usr/bin:/bin LC_ALL=C HOME TMPDIR`, `tsukuroi_vars=0`; no `XDG_RUNTIME_DIR`, no `DBUS_SESSION_BUS_ADDRESS` | full user session, user bus present | strong |
| 7 | stdin | `/dev/null` (`</dev/null` in `NS_INNER`) | terminal or inherited | weak (cron looks the same) |
| 8 | cwd | inherited from the counter process (no `cwd=` in `ns_leg`, `:283-284`) | lane dir when run as `bash tools/tsukuroi-census.sh` | weak/unreliable |
| 9 | `$0` / `BASH_SOURCE` | `<scratch>/rev-census.sh`; the census reads `SELF=${BASH_SOURCE[0]}` (`tools/tsukuroi-census.sh:427`) | lane path | weak (a temp copy is plausible) |

Channels 1 and 2 are each sufficient on their own; neither is covered by any frozen control.

## 3. Arms built and scored (the requested variant)

Scored with the frozen counter, scratch clone of the lane, `--lane <clone> --revision <sha> --scratch <scratch>` (all PASS; receipts in `C1CritNsView/`):

| arm | what is gated | revision | result |
|---|---|---|---|
| **V1 `ns-gated`** *(`TSUKUROI_FIXTURE` or uid 0)* | the packages site only — the tip's here-string/`grep -m1` pair replaced by `printf … \| grep -q` unless `[ -n "${TSUKUROI_FIXTURE:-}" ] \|\| [ "$(id -u)" -eq 0 ]` | `b504f324e3c0cf15d9bbe5665f95b2e16cbd9f7f` | `PASS` cases 10, invariant 10, ns 3, selftest `PASS (130 cases, 130 passed, 0 failed)`, default_equal 1 |
| **V2 `all-sites ns-gated`** | all five C1 sites (packages + the four `-Qu`/`-Sup`/`-Suu` extractions) behind the same gate | `7ce4ef64ef52c12cb12fcd59fd0cbe0f95d2bf76` | `PASS` same five numbers |
| **V3 `data-gated`** | all five sites, gated on `"$PACMAN" -Qq` printing exactly `alpha beta gamma delta` — **no env test, no uid test** | `5b4048d87d83f8beb2b6b9a71dfa75d67add0525` | `PASS` same five numbers |

Reference arm at the same predicate: the committed control `K6` (every site fixed) reads `PASS inv 10 ns 3` (`.ufo/waves/round-42/controls/C1-K6.jsonl`); the existing fixture-gated control `K7` reads `FAIL inv 10 ns 0` (`C1-K7.jsonl`) — i.e. gating on `TSUKUROI_FIXTURE` alone is caught **only** because the packages fix is missing in the three uid-0 legs.

The three arms are therefore indistinguishable from the fully fixed census under the predicate. Patch texts: `C1CritNsView/variants.diff`; the clone commits are scratch-local (removed with the scratch dir), and `C1CritNsView/mkvariant.py` / `mkvariant2.py` / `mkvariant3.py` re-apply each arm to a fresh clone of the lane tip `87c4f7c6`.

## 4. Independent measurement: the V1/V2 arms are broken at production identity

Not the counter — same fabricated view, but the scored census runs as uid 1000 with no `TSUKUROI_*` (mount namespace built as uid 0, then `setpriv --reuid=1000 --regid=1000 --clear-groups`; uid 1000 is mapped via the host's `/etc/subuid` range `vgpnk:100000:65536` with `unshare -m --map-users=1000,0,1 --map-users=100000,1,65535 …`). Driver: `uid1000.py`; receipts `uid1000-tip.txt`, `uid1000-variant.txt`.

```
== tip census, uid-1000 leg (token d5dadc)
large rc=2 PLANE packages: BLOCKED (pacman -Qkk sample probe error: error: alpha: /usr/bin/x-d5dadc (Permission denied); …
small rc=2 PLANE packages: BLOCKED (pacman -Qkk sample probe error: error: alpha: /usr/bin/x-d5dadc (Permission denied); …
== ns-gated variant, uid-1000 leg (token cc8c3a)
large rc=2 PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=4(alpha,beta,gamma,delta) drift=0 …
small rc=2 PLANE packages: BLOCKED (pacman -Qkk sample probe error: error: alpha: /usr/bin/x-cc8c3a (Permission denied); …
```

The lane tip is fixed unconditionally; V1/V2 keep the round-41 defect (`DEGRADED` where `BLOCKED` is due) exactly where production runs, and the counter cannot see it because its legs run as uid 0. This also settles the "is the variant really a defect" question: the defect is behavioural, not cosmetic.

## 5. What this falsifies

- **QUALITY 82** (`corpus/QUALITY.md:161`): "Such a counter also runs the code in at least one view the code cannot tell from production use (the live host, read-only) … the pre-data controls include a fixture-gated variant and a cached-live variant, each of which must read below the target." The N legs are not such a view (§2), the declaration cites 82/85 for them (`SCORECARD.md:2573`), and the frozen controls `C1-K0..K8` contain no arm that fails on a namespace-gated or data-gated census (K9/K10 absent; `controls/battery-summary-c1.jsonl`).
- **QUALITY 85** (`corpus/QUALITY.md:167`): "The frozen pre-data controls include one arm per channel, each arm reaching for the view through that channel alone, and each must score below the target." Not one of the nine frozen arms reaches for the view through uid, mountinfo, the stub's own text, the fabricated package names, `HOME`/`TMPDIR`, the env shape, or stdin; §3's arms reach it through uid and through the package names and both score the target.
- Narrower, and worth the L1's attention on its own: the update-safety half of C1 has **no** override-free leg at all. Every U1-U4 fixture runs with `TSUKUROI_FIXTURE` set (`:106` via `env_for`), so a fixture-gated update fix passes all four U cases — V3 shows exactly that (all five sites data-gated, U pairs still `invariant 10`).
- What this does **not** falsify: the census at the tip is fixed unconditionally (`tools/tsukuroi-census.sh:695-697` here-strings; `:1624,1639,1645,1655` `awk 'NR <= 3'` / `'NR == 1'`), so C1's substance holds today. What fails is the instrument's power to keep it holding — a later regression re-introduced behind a `$TSUKUROI_FIXTURE`/uid test, or a fix written only for the fixture path, passes the frozen predicate.

## 6. Smallest safe correction

1. **Close the uid channel in the leg** (measured to work on this host): replace `unshare -rm sh -c "$NS_INNER"` with `unshare -m --map-users=$(id -u),0,1 --map-users=<subuid>,1,<count> --map-groups=…` and run the scored census after `setpriv --reuid=$(id -u) --regid=$(id -g) --clear-groups`. With that change V1/V2 read `FAIL` (measured in §4: large `DEGRADED` ≠ small `BLOCKED`). Note that the census must be readable after the drop: `/home/vgpnk` is `drwx------`, so the current leg's census path is not reachable at uid 1000 — copy it in as this measurement does (`/mnt/census.sh`) and accept that `$0` then differs (channel 9).
2. **Randomise the fixture's package names per run.** The counter already randomises the error token and the padding names (`pad_name` at `:132-137`, `TOKEN` at `:176`); `qq` is the fixed four-name list (`NS_STUB` at `:266-268`, `spec['qq']` at `:278`). Until it is random, V3 — and any census that recognises `alpha beta gamma delta` — is unreachable by the counter *and* by any uid fix.
3. **Add the two arms as frozen pre-data controls, each of which must FAIL:** `K9` = K6 with the five fixes behind `[ -n "${TSUKUROI_FIXTURE:-}" ] || [ "$(id -u)" -eq 0 ]` (V2 text) and `K10` = K6 with them behind the fixed package list (V3 text). Until (1) and (2) are in, both will read `PASS`; that result must be recorded as the limit of the leg, not silently dropped.
4. **Reword the claim's evidence:** until the arms fail, the N legs are "override-free legs", not a view "the code cannot tell from production use". Delete the `(QUALITY 82/85)` citation at `SCORECARD.md:2573` and the "Production-path legs (QUALITY 82/85)" heading at `tools/score-size-invariance-r42.py:30`, or keep it and name what is still open.
5. **Add the only closure that does not depend on observation:** a static invariant over the census — no `printf … | grep -q`, `| grep -m1`, `| head`, or any other early reader over a captured probe buffer (`CAP_OUT`, `s_out`, and every `$(…)` capture of a probe) at any site — with a mutation control that re-inserts the pattern at each of the five sites and must fail the check. The behavioural legs cannot make a production claim the trigger cannot reach live (§7).

## 7. What a stronger leg would need

- **Identity parity**: uid, gid, `HOME`, `TMPDIR`, cwd, stdin, `$0` and the environment all matching a user run; on this host that is achievable via the subuid mapping + `setpriv` above, because the creating process keeps `CAP_SYS_ADMIN` in the child userns.
- **Probe-content parity**: impossible while the answer arrives through a stub. The `-Qkk` text must be fabricated to exceed 64 KiB, and the fabrication is visible in the census's own input (`sample=4(alpha,…)`) and in the stub's text. The counter can only make the *shape* per-run random; it cannot make the data real.
- **A live view that actually reaches the trigger**: measured read-only on the host, the census's own merged sample at the default `SAMPLE_N=8` is **617 bytes** for 1409 installed packages (`pacman -Qkk $(pacman -Qq | head -8) | wc -c`, `live-sample.txt`). The defect needs >64 KiB (≈850 such packages at 77 B/package, [INFERENCE]), so a default live run can never exercise it; the only live route is `TSUKUROI_SAMPLE_N=<large>` — itself a user-visible channel a gated census can read. That is why the static invariant in §6.5 is not optional if the claim is about production.
- **Remaining unavoidable channel even after all of the above**: `/proc/self/mountinfo` shows the tmpfs and the file bind over `/usr/bin/pacman`, and the stub's text names the view (`/mnt/qkk`). A census can read either and still score the target; that has to be an armed control that is expected to PASS, disclosed as a limit of every namespace leg, not a claim of non-distinguishability.

## 8. Not done / limits of this seat

- I did not run the counter at the lane tip or at `447662088dfd3155e31aed239179a79c1d1046c7`; the tip's PASS is the declared after-state and the committed `K6`/battery receipts stand in for the "fixed everywhere" reference. I ran the counter three times (V1, V2, V3), one at a time, ~45 s each.
- I did not edit, stage or commit anything in the lane; every variant lives in a scratch clone under `/fast/scratch/hyaku/tsukuroi-r42/C1CritNsView/` (removed at the end). No host state was touched; the only mounts were inside private `unshare` namespaces.
- Channels 7-9 are listed from the counter source and the probe, not turned into scored arms; the arms in §3 cover channels 1 and 2 only.
- `[INFERENCE]` marks: the ≈850-package live threshold is an extrapolation from the 8-package measurement.

Receipts (this seat dir): `variant.jsonl`, `variant2.jsonl`, `variant3.jsonl` (counter output per arm), `variants.diff` (the three patches against `87c4f7c6`), `ns-channels.txt` (channel probe), `uid1000-tip.txt`, `uid1000-variant.txt` (production-identity measurement), `controls-summary.txt` (K0/K6/K7/K8), `live-sample.txt`.

Report: `.ufo/waves/round-42/w1/C1CritNsView.md`
