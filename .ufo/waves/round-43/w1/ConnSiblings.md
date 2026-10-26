# ConnSiblings — X-2 sibling-overlap scan (round 43, wave w1)

VERDICT: supports

Seat ConnSiblings-7 (leaf; no subagents). Item X-2: scan every sibling lane's
`PROVINCE.md`, `SKILL.md` and `corpus/knowledge` for the round's surfaces, report
each hit with lane/file:line/quote, classify it as contested scope, dependency on
tsukuroi's boot-chain verdicts, or knowledge another lane holds that this round
should cite (report, do not absorb).

## Scope and method

Lanes scanned (20; tsukuroi-shokunin excluded): kasegi, kama, kaidoku, mado,
kengaku, kake, chousa, kumitate, souji, mori, tameshi, tabi, kotodama, revenger,
kotoba, lore, game-dev-2d, audio, game-dev-3d, kagi.

Per lane, the three surfaces were inventoried first (`glob`, gitignore disabled):
tabi/kotodama/mori have no `PROVINCE.md`; game-dev-2d/audio have no `SKILL.md`
(verified by glob; those paths absent). All grep runs were read-only, case-insensitive,
gitignore disabled, per-lane path lists; no tsukuroi path was included.

### Commands (as run; identical shape per lane, roots listed per lane)

Primary overlap pattern (4 passes over each lane's roots):
```
grep -iE 'pipefail|boot_inputs_newer|inputs_newer_than|boot inputs newer|BOOTED-OBSERVED|btrfs[- ]scrub|scrub\.status|BTRFS_IOC_SCRUB_PROGRESS|CAP_SYS_ADMIN' \
  /home/vgpnk/Projects/shokunin/<lane>/PROVINCE.md \
  /home/vgpnk/Projects/shokunin/<lane>/SKILL.md \
  /home/vgpnk/Projects/shokunin/<lane>/corpus/knowledge
# (roots that do not exist per the glob inventory were omitted)
```
Supplementary pattern (newermt/btime/btrfs/find-grep):
```
grep -iE 'newermt|btime|newer than boot|boot start|btrfs|find[^\n]{0,120}grep -q' ...
```
Boot/update-safety sweep:
```
grep -iE 'mkinitcpio|update-safety|boot chain|bootchain|reboot|boot start|\bboot\b' ...
```
Scrub-only confirmation sweep:
```
grep -iE 'scrub' ...
```
Follow-up reads (context/quotes, read-only): mori
`corpus/knowledge/{audit-r11,verdict-machine-r4,selftest-flake-r9,surfaces-r7,verdict-contract-r13}.md`,
mori `corpus/lessons/2026-10-15-errexit-pipefail-silent-crash.md`,
mori `corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md`,
mado `corpus/knowledge/tripwire-precision-r20.md`,
kumitate `corpus/knowledge/agent-isolation-substrates.md`,
kotoba `corpus/knowledge/sibling-overlap-census-round49.md`,
tameshi `corpus/knowledge/mutation-case-tsukuroi-census.md`.

## Findings (lane | file:line | quote | classification)

### Knowledge another lane holds — same hazard class as C1 (cite)

- **mori | corpus/knowledge/verdict-machine-r4.md:210-217** — "`state_n=$(find "$STATE_DIR" -maxdepth 1 -type f -name '*.round' 2>/dev/null | wc -l | tr -d ' ')`. Under `set -euo pipefail` (`tools/mori-census.sh:54`) an unreadable `.ufo/state` makes the producer fail, `pipefail` propagates it, and the assignment aborts the whole gate **before any verdict line** — the crash signature documented in `corpus/lessons/2026-10-15-errexit-pipefail-silent-crash.md` (canary B)." — **Same class as C1**: producer `find` fails on a missing/unreadable path and `pipefail` turns the pipeline false (C1's round-42 fail-open was the mirror-image misread — find exit 1 folded into the pipeline verdict). Lesson record (read: lines 14-30, 44-61): "an unguarded `var=$(producer | consumer)` assignment aborts the whole run when the **producer** fails for an environmental reason"; attribution line "`find <dir-with-000-subdir> ... | sort -n | tail -1 | cut -d. -f1` → exit 1" and "the same pipeline **without** `pipefail` → rc=0 … **with** `pipefail` → rc=1".

- **mori | corpus/knowledge/selftest-flake-r9.md:31-41** — "`grep -q` exits **0 at the first match** and closes its end of the pipe … its next write gets `EPIPE` and the process dies of `SIGPIPE` (exit 141); `pipefail` makes the pipeline rc the rightmost non-zero element — 141 — **even though the consumer that produced the verdict exited 0**; `|| miss=` reads rc≠0 as 'no match' … a false FAIL." Lesson `corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md:17-41`: "under `pipefail` a pipeline's rc answers 'did every element exit 0', not 'did the consumer match'. Any consumer that exits early (`grep -q`, `-m1`, `-l`) can kill its producer with SIGPIPE." — **Same pipeline family as C1's pre-fix `find … | grep -q .`** (grep -q closes the pipe at the first match, so the `find` producer is also SIGPIPE-able); this is the complementary half of the hazard the C1 fix defuses by deciding on find's output instead of pipeline rc.

- **mori | corpus/knowledge/surfaces-r7.md:333-341** — "`printf '%s\n' "$out" | grep -qE -- "$re" || miss=…` under `set -euo pipefail`; when `grep -q` exits at the match before `printf` finishes writing, the pipeline rc is SIGPIPE 141 … measured in isolation at 8 rc-141 misses / 6400 iterations under 16-way CPU contention" — with the suggested repair "`grep -qE -- "$re" <<<"$out"` has no producer to signal".

- **mori | corpus/knowledge/verdict-contract-r13.md:34-53** — "`printf '%s\n' "$inwin" | sed -E 's/^[0-9]+ //' | grep -Fxq -- …` … `sed` exits 141 … the pipeline's status is the rightmost non-zero element: 141. But the pipeline is an `if` condition, so errexit does not abort; the status is simply read as 'no exact subject line' … a successful match destroys its own producer, `pipefail` promotes the producer's death certificate to the pipeline verdict".

- **mori | corpus/knowledge/audit-r11.md:156** (F01) — "Current `tools/mori-census.sh:1366-1374`, especially `printf '%s\n' "$inwin" \| sed … \| grep -Fxq …` under pipefail … The producer/consumer condition inverts when an upstream writer gets SIGPIPE" — same class observed in production bytes.

### Knowledge another lane holds — CAP_SYS_ADMIN / permission gates (cite)

- **mado | corpus/knowledge/tripwire-precision-r20.md:93-95** — "the mounts failed (unprivileged `--map-current-user` gives no CAP_SYS_ADMIN in the mount namespace's owner; S109, S112)". — Independent sibling observation of the same permission principle C2 grounds on S240/S241 (unprivileged ioctl path lacks CAP_SYS_ADMIN); supports C2's "unprivileged status never reads `running`" by a second, different surface (mount namespace ownership).

- **kasegi | corpus/knowledge/source-tree-loss-2026-09-28.md:270-272** — "btrfs enumeration is **not permitted** for this user (`Operation not permitted` on `/` and `/home`)". — Adjacent permission fact on the same host, btrfs-specific (not scrub); shows unprivileged btrfs queries are blocked host-wide, consistent with C2's privileged-ioctl account.

### Dependencies on tsukuroi's verdicts (explicit, non-contested)

- **kaidoku | PROVINCE.md:125** — "Full-system upgrades go through tsukuroi-shokunin's update-safety gate first (that ground is tsukuroi's), partial upgrades (`pacman -Sy <pkg>`) are never run, and pacman stays paused host-wide per the 2026-10-20 orchestrator ruling." — A sibling lane documents a **runtime dependency on tsukuroi's update-safety/boot ground**.
- **mori | SKILL.md:143-145** — "**Refuses OS-package state** — pacman/systemd units/drivers/firmware/boot are tsukuroi. mori reads journal and cgroup counters as fleet-relevant events and reports them; it never claims OS-state ownership and never repairs." — Boundary declaration deferring boot/OS-package ownership to tsukuroi.
- **mori | corpus/knowledge/jj-branch-anchor-r17.md:53-55** — "No full update-safety/OS diagnosis is absorbed from tsukuroi." — Explicit non-absorption clause.

### Cross-lane pointers / prior art (cite, do not absorb)

- **kumitate | corpus/knowledge/agent-isolation-substrates.md:262-264** (X8) — "Tsukuroi's `memory-pressure-r25.md` cites its S121 (systemd v262 `systemd.resource-control.xml`), not S072; tsukuroi's S072 is `systemd-run.xml`, used by `boot-writers-r19.md` (XChanS072, at tsukuroi HEAD `9c89ff4f`)." — A sibling pins tsukuroi corpus files and source IDs; useful for source-citation hygiene (S072 naming) in round docs.
- **kotoba | corpus/knowledge/sibling-overlap-census-round49.md:88** — prior-art overlap census with a tsukuroi row: "**Domain:** host operability & system repair (繕, mending) — the OS substrate itself: package state, systemd, drivers/firmware, boot health." — The round's own X-2 scan has precedent; kotoba's round-49 census (20 rows, pinned commits) is the existing overlap ledger.
- **tameshi | corpus/knowledge/mutation-case-tsukuroi-census.md:1-22** — tameshi ran mutation testing on tsukuroi `tsukuroi-census.sh` census-v2 (T5-1, 2026-10-14), "Substrate: tsukuroi-shokunin **read-only**; every mutant is a byte copy"; pins tsukuroi HEAD `165307fe`; records incident I1 (substrate moved mid-run by a concurrent lane, +56 lines/10 selftest cases inserted). — A sibling holds a verification record against tsukuroi tooling (census.sh, not boot-chain-audit.sh); valuable precedent for read-only treatment and for drift detection if this round's frozen counter bytes move.

### Generic pipefail usage (no overlap with the round's surfaces)

- kengaku PROVINCE.md:382,430,481 and SKILL.md:1030,1110 — grader recipes run under `bash -euo pipefail` inside bubblewrap sandboxes; no find/boot interplay.
- kumitate corpus/knowledge/remaining-scripts-census.md:563 — `measure.sh` runs "under `set -uo pipefail` — deliberately without errexit".
- kagi corpus/knowledge/janitor-command-surface.md:3 — `~/.local/bin/the-janitor` "bash, `set -euo pipefail`, `umask 077`".
- mori corpus/knowledge/{progressing-weak-r2.md:298, silence-cutover-r3.md:115,249} — additional references to the same lesson set.

### Term collisions and `find -newermt` probe-shape siblings (no conflict)

- kaidoku: "btime"/"get-fonts" are Obsidian **native addon names** (corpus/knowledge/2026-10-13-asar-surface.md:29, 2026-10-13-r3-node-addons.md:28-31) — unrelated to boot-time `$btime`.
- souji corpus/knowledge/duplicate-verdict-identity.md:47-51 — `stx_btime` (statx birth time) is availability-dependent; distinct concept from C1's boot-start epoch. Flag for naming discipline in docs.
- mado corpus/knowledge/province-accuracy-selfaudit.md:96-98,216-218; walker-deep-r9.md:349-350; walker-live-surface.md:279 — `find ~/.config … -newermt "…"` drift probes, same probe shape as C1 but un-gated (no pipefail/grep verdict), different purpose.
- mori corpus/knowledge/lane-silence-r2.md:34-35; observability-census-r1.md:17,28; observability-surfaces-r2.md:56; progressing-weak-r2.md:163; silence-grading-r2.md:124; tabi archive-receipt-r10.md:420; kaidoku 2026-10-13-r3-jq-provenance.md:122 — `find -newermt @epoch` / `find -newermt 'date'` window probes across fleet lanes; same predicate family, no shared gate with boot-chain-audit.sh.
- kama consumer-registry.md:372, kake ops-automation.md:134, mado SKILL.md:460, kotodama culture-material: none conflict with the round's claims (generic boot/journal/service notes).

### btrfs knowledge without scrub (no scrub overlap anywhere)

- mori SKILL.md:438-441 — "**Never threshold the btrfs chunk percent.** Data-chunk fill reads **94.25%** while `df -P` Capacity … reads **10%** … Keep the `df -P` parser." (disk-surface guidance, adjacent to tsukuroi storage counters)
- souji corpus/knowledge/count-objects-linked-worktree-garbage.md:89-92,129-130; quarantine-same-filesystem-rename.md:44; quarantine-staging-no-copy-r23.md:40-44; duplicate-verdict-identity.md:26-30 — btrfs directory-size/device semantics (host /home is btrfs dev 30).
- chousa mount-alias-r14.md:30-32 — "$WORK tmpfs dev 57 vs the repo btrfs dev 30".
- kumitate agent-isolation-substrates.md:47,167 — jj-colocated repo on btrfs; OMP PAL backends include btrfs.

## Explicit negatives (zero hits across all 20 lanes, all four patterns)

- `BOOTED-OBSERVED`: 0 hits. `boot_inputs_newer` / `inputs_newer_than` / "boot inputs newer": 0 hits.
- `btrfs scrub` / `scrub.status` / `BTRFS_IOC_SCRUB_PROGRESS` / bare `scrub` (btrfs sense): 0 hits. No sibling claims the scrub-record surface (Frontier) or the boot-chain gate.

## Synthesis

- **No contested scope found.** No sibling asserts the boot-chain/update-safety ground or scrub record; two lanes explicitly defer OS/boot ownership to tsukuroi (kaidoku PROVINCE.md:125; mori SKILL.md:143-145, jj-branch-anchor-r17.md:53-55).
- **Dependencies on tsukuroi's verdicts:** kaidoku's province text relies on the update-safety gate; mori's boundary text relies on tsukuroi owning boot/OS-package state (round's C1/C2 claims sit underneath these).
- **Knowledge to cite (report, not absorbed):** mori's two lessons (`2026-10-15-errexit-pipefail-silent-crash.md`, `2026-10-15-selftest-grep-sigpipe-race.md`) — both halves of C1's pipeline hazard; mado's CAP_SYS_ADMIN mount-namespace observation (S109/S112) as second grounding for C2's permission gate; kotoba's round-49 sibling-overlap census as prior art; tameshi's tsukuroi-census mutation record (read-only substrate precedent); kumitate's tsukuroi-corpus pointer (S072 naming).

Not run: no counters, no fixtures, no clones; no lane file created/modified; no scratch artifacts (nothing written under /fast/scratch); no tool installs (none needed). Host untouched.
