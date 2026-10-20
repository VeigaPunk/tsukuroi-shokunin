# EvidenceScribe — round 13 evidence inventory (C1 depth correction)

- Seat: `TsukuroiR13.EvidenceScribe` (leaf, scribe). Author-side inventory; not admission authority.
- Inventory time: 2026-10-20, ~01:40–01:50 -03. Working tree is actively edited by sibling seats; line numbers below are volatile (the r12 matrix .md grew ~6 lines above its Current-host section during this pass). Re-grep before landing.
- Tool record: no installs or upgrades. Used existing `curl`, `man`, `grep`, `git` (read-only subcommands), `stat`. Scratch fetches in `/tmp/r13-evid-*.html` (outside repo, not evidence).
- Write set: this file only. No corpus, SOURCES, LOG, or sibling file was edited.

## 0. Boundary state at inventory

| Surface | State | Pointer |
|---|---|---|
| HEAD | `9574a18` = outside spot-check commit | `git rev-parse --short HEAD` |
| Round-12 matrix, committed bytes | `70fede2`; false universal at MD 53 and 86; JSON 85 | `git show HEAD:corpus/knowledge/root-dac-decision-r12.{md,json}` |
| Matrix, working tree (uncommitted) | MD +33 lines (R13 notice, now at MD ~129); JSON +2 lines (`superseded_by` line 2, `correction_notice` line 3); false universal still present | `git diff --stat` |
| QUALITY, working tree (uncommitted) | #17 and #18 added after #16 (lines 23–24) | `corpus/QUALITY.md` |
| Dangling supersession target | `corpus/knowledge/root-dac-correction-r13.{md,json}` does not exist on disk | `ls corpus/knowledge/root-dac-correction-r13.*` → ENOENT |
| Other uncommitted | `corpus/README.md` modified; `corpus/lessons/round-13.md` untracked (L1, baseline 9574a18) | `git status --porcelain -- corpus` |
| SOURCES.md | last committed `f3868cd` (late S027 annotation); no uncommitted change | `git log -1 -- corpus/SOURCES.md` |
| Report | `.ufo/reports/round-12/tsukuroi.md` at fleet root, commit `6800f05` (per lesson); not re-read by this seat | — |

## 1. Rejection evidence pointers that the r13 report must preserve

Committed and on disk unless marked.

| # | Pointer | What it records |
|---|---|---|
| E1 | `corpus/lessons/round-12-verifier-spotcheck.md` §Closure, line 14 | `status: ok; admitted: false; verdict: rejected-harmed`; depth harmed; defect is "substantive, not a completion marker" |
| E2 | same, §Claim rechecks → C2 (lines ~130–161) | Counter reproduces 0→4; exclusive sentence in R13, current-host paragraph, JSON B2 `limit` is false; systemd.exec re-open; "C2 admissible only after correction" |
| E3 | same, §Outside discernment spot-check table (lines ~171–175) | Agree: S035, S036, S037, S040. Disagree: C2 entry "as delivered"; S036/S037 attributed bot comments as "maintainer-side" |
| E4 | same, §Per-axis verdicts (lines ~209–218) | operability improved; depth **harmed**; calibration/adjacency/coverage/freshness unchanged |
| E5 | same, §Routed defects (lines 235–254) | 1 blocking correctness (narrow exhaustive read-only-unit sentence in MD current-host, R13, JSON B2 limit; keep ProtectSystem comparison; retain alternate path-view mechanisms); 2 conformance (`f3868cd` after report, preserve as history); 3 bot-vs-maintainer attribution for S036/S037 (without in-place edit of immutable fields); 4 SC1/SC2 root-owned hypothetical vs caller-owned fixtures |
| E6 | same, §Step-1 conformance (lines ~21–62) | Conformance defect: late `f3868cd` write; driver digest; C1 memfd reproduction (not a delivered-bytes check of C2) |
| E7 | `corpus/lessons/round-12.md` §Gate (line 12) and §Gate — resumed source openings (line 78) | S035–S040 decisions (rows at lines 87–92); "gate admits the corrected C2 entry … subject to final integration measurements and independent closure" (lines 111–116) |
| E8 | `corpus/SOURCES.md` rows 33–46 | S027 (33), S028 (34), S034 (40, superseded teaching), S035 (41), S036 (42), S037 (43), S038 (44), S039 (45), S040 (46). S036/S037 teaches still say "maintainer-side" |
| E9 | `corpus/QUALITY.md` #14–#16 (lines 19–21) and uncommitted #17–#18 (lines 23–24) | #17 bans "only"/exhaustive mechanism lists without scope; #18 requires root-owned hypotheticals be labelled inference when executed controls were caller-owned |
| E10 | Committed matrix: `corpus/knowledge/root-dac-decision-r12.md` lines 53 and 86 (HEAD); JSON B2 `limit` line 85 (HEAD) | Exact false universal wording (see §3) |
| E11 | Working-tree matrix: MD line 59, MD line 92, JSON line 87 | Same false universal still present in active content; MD 48 is the correct ProtectSystem-only comparison and must stay |
| E12 | Working-tree MD §"Round-13 correction" (~line 129) and JSON lines 2–3 | Notice explicitly supersedes the exhaustive conditions; points to not-yet-existing `root-dac-correction-r13.*` |

## 2. Prior reviewer findings (inherited; not re-verified by this seat unless §4 says so)

Labelled by source. "Status" is the inherited verdict, not this seat's.

**C2ReviewR** (`.ufo/waves/round-12/resumed/C2ReviewR.md`, author-side, NOT PASSED):
- F1 High — no per-operation errno priority; cites unregistered kernel master line anchors (namei.c, btrfs/ioctl.c). Unregistered: must not be cited as support (QUALITY #7). Spotcheck agrees the source does not establish ioctl ordering.
- F2 High — `### F2` heading. Says `ProtectSystem=full` is unsupported for `/` and that **"Only `strict` (or a `ReadOnlyPaths=` covering the target) can produce B2 for a root-level target."** This is the **origin of the exclusivity** that later reached matrix R13 / MD 59 / JSON 87. The reviewer's own sentence is the same false universal the outside spot-check rejected.
- F3 High — B3 cites S034 (access(2)) as creation authority; omits the inheritable term; capabilities(7) execve rule not cited.
- F4 Medium — SC1–SC3 fixture ownership mislabel (fixtures were uid-1000-owned; matrix says root:root). Still present in active JSON (see §3, item 4).
- F5 Medium — "absent → excluded" time-bound. F6 Medium — target `/.snapshots` under parent `/` not established (journal names emitter, not target). F7 Low — C1/C2 share one reading of `/`; not independent corroboration. F8 Low — `chmod` remains gated.

**MatrixCriticR** (`.ufo/waves/round-12/resumed/MatrixCriticR.md`, author-side):
- §4 X1 (SC3 owner-class; fixed), X2 (SC4 effective vs bounding; fixed), X4 (errno-first; fixed), X5 (`stat` rc=1 conflates ENOENT/EACCES; fixed), X6 (`+` prefix; declared unknown), X7 (EROFS-vs-EACCES ordering; resolved by scope), X9 (LSM list; fixed), X10 (first retained; fixed), X11 (labels; fixed), X12 (heading; fixed).
- §4 **X3 — HIGH, depth** (ProtectSystem=full; missing unit-side read-only sources `BindReadOnlyPaths=`, `TemporaryFileSystem=…:ro`, `RootDirectory=`/`RootImage=`, `ProtectHome=`). §8 table marks X3 "fixed" with a non-blocking residual. **The outside spot-check overrides this: the exclusivity remains in active text.** The §8 "fixed" status should not be carried forward as a pass.
- §3 R11 (`_PID=1520` ≠ `ExecMainPID=1386`; stale PID) — sanitized aggregate only; keep as a pointer, no journal bodies.
- §8 final static check and §9–§11 re-checks are author-side and say "no PASS"; they do not establish C2 admission.

**SourceReviewR** (`.ufo/waves/round-12/resumed/SourceReviewR.md`):
- N1 — S034 row overreaches (teaches "denied a write that unbounded root passes"). Superseded by S038 row (SOURCES 44); the S034 row remains unchanged (immutable).
- N2 — falsifier prediction valid only while `/` lacks owner-write (0555 precondition).
- N3 — no source for the subvolume-create path or snapper errno mapping; S035 covers mkdir only. Keep any Btrfs attribution `[inf]`.
- N4 — S034 anchor says "privileged processes" paragraph; the quoted sentence is in the real-UID paragraph. N5 — S035 "required before attributing" gloss is the row's own inference.
- F2 — S019 4 GiB recommendation is conditional ("depending on how many snapshots and kernel versions"). F4 — S023 archinstall <3.0.5 precondition omitted. F5 — S028 "removed" wording applies to bounding set only.
- F7/F8r — no written mutable-field rule; S035–S037 added to SOURCES working tree (now committed).
- Grounded-branch table (§"Grounded branches", B1–B8) is the best single list of which branch rests on which row.

**Outside spot-check** (`corpus/lessons/round-12-verifier-spotcheck.md`, non-author; the primary rejection record): see §1 E1–E6. Its discernment table is the only non-author evaluation of S035–S040 and of the C2 entry.

**Round-12 lesson** (`corpus/lessons/round-12.md`): Mistakes rows (policy vs baseline; permission-proxy; stale fixture identity; write-root misroot; source-date copy error) — author-side self-records; they reference the reviewer files above.

## 3. Exact false-universal wording to be superseded (fresh grep, 2026-10-20)

Committed `70fede2` (HEAD bytes):
- MD 53: "`ProtectSystem=full` covers `/usr/`, `/boot/`, `/efi/` and `/etc/` but not `/`; only `strict` (or a `ReadOnlyPaths=` entry covering `/`) would make `/` read-only through the unit (S028)."
- MD 86 (R13): "Only `strict` or a `ReadOnlyPaths=` entry covering `/` could produce a B2-family `EROFS` for `/` through the unit."
- JSON 85 (B2 `limit`): "ProtectSystem=full does not cover / (S028), so only strict or a ReadOnlyPaths= entry can make / read-only through the unit."

Active working tree (same sentences still present):
- MD 59, MD 92, JSON 87 (JSON shifted +2 by the notice lines).

**Correct and must stay** (scoped to ProtectSystem values): MD 48 "while only `strict` mounts the entire hierarchy read-only" — among ProtectSystem values, only strict covers the whole hierarchy. Do not generalise it into an exclusivity over mechanisms.

## 4. Fresh verification performed by this seat (2026-10-20)

| # | Check | Result |
|---|---|---|
| V1 | `MANWIDTH=2000 man -P cat 5 systemd.exec` (systemd 261.2-1, local) | ProtectSystem text present (line ~503): "mounts the /usr/ and the boot loader directories (/boot and /efi) read-only"; "If set to "full", the /etc/ directory is mounted read-only, too"; "strict" entire hierarchy except /dev, /proc, /sys. BindReadOnlyPaths (line ~191): "creates read-only bind mounts". ProtectHome (line ~510–512): covers /home, /root, /run/user, and "tmpfs is mostly equivalent to TemporaryFileSystem= with ':ro'" |
| V2 | `curl` `https://man.archlinux.org/man/systemd.exec.5.en` → HTTP 200; footer `systemd 262.1` | Contains "If set to \"strict\" the entire file system hierarchy is mounted read-only"; "creates read-only bind mounts"; "mostly equivalent to TemporaryFileSystem= with". Version differs from host 261.2; cited sentences are the same family. S028 row anchors to the Arch 262.1 URL |
| V3 | `curl` `https://man.archlinux.org/man/access.2` → 200 | Contains `does not answer the "can I read/write/execute this file?" question` (S038 sentence) |
| V4 | `curl` `https://man.archlinux.org/man/mkdir.2` → 200; footer | "Linux man-pages 6.19", "2026-02-11" present (S035 footer) |
| V5 | `grep -n '^z / ' /usr/lib/tmpfiles.d/root.conf` | `10:z / 555 - - -` (S040) |
| V6 | `ls corpus/knowledge/root-dac-correction-r13.*` | ENOENT. Supersession pointers in MD notice and JSON line 2 are dangling |
| V7 | Grep MD/JSON for exclusivity phrases (HEAD and WT) | §3 lines confirmed |
| V8 | Notice's location list vs current text | MD "worked-example step 3" (current text: "B2 is not configured on this host, but a host `findmnt` cannot exclude a unit-private namespace or another sandbox mechanism") contains no exclusive wording. JSON `decision_procedure` step 2 (WT line 174) lists three triggers ("a read-only superblock, ProtectSystem=strict, or a ReadOnlyPaths= entry") and omits BindReadOnlyPaths, TemporaryFileSystem, RootDirectory, RootImage. The notice therefore mislocates the defect: step 2 is an **incomplete** list, not an exhaustive claim. The correction should say so precisely |
| V9 | JSON SC1/SC2 inputs (WT lines 184, 198) | Still `parent: "0555 root:root, base ACL entries only"`, while basis cites `discriminator-smoke.json` fixture_results[0] and `error-order-smoke.json`, both caller-owned (uid 1000). Spotcheck routed item 4 is **unfixed in active JSON**. MD notice (~lines 139–142) describes the distinction but the JSON inputs are unchanged |
| V10 | SOURCES rows 42–43 | S036 "maintainer-side rebuttal comment" and S037 "maintainer-side comment" still present. Routed item 3 unfixed; immutable fields must not be edited in place (append a superseding row or a dated note) |
| V11 | `git show HEAD:…` vs working tree | Confirmed the R13 notice and QUALITY #17–18 exist only uncommitted |
| V12 | Closure record location | `grep -rl rejected-harmed scripts .ufo/reports/round-12` → only `scripts/hyaku/closure-prompt.md` (template). No on-disk closure JSON for tsukuroi r12 located in those paths. LOG.md has no r12 rejection entry; its last r12 entry is the 2026-10-20 erratum at LOG 518–531 (S027 source-seat annotation only) |
| V13 | `ls .ufo/waves/round-12/` and `resumed/` | Inherited seat files present (C2Review.md, MatrixCritic.md, SourceReview.md, C2ReviewR.md, MatrixCriticR.md, SourceReviewR.md, etc.) |

## 5. Boundary facts the r13 report must preserve

1. **ProtectSystem comparison (source-grounded, keep):** `yes` → /usr, /boot, /efi; `full` adds /etc; `strict` → entire hierarchy except /dev, /proc, /sys (with documented exceptions). `full` does not cover `/`. Only among ProtectSystem values.
2. **Alternative unit-side read-only path views (not captured in r12; keep as residual):** `ReadOnlyPaths=`; `BindReadOnlyPaths=` (read-only bind mount); `TemporaryFileSystem=…:ro`; `RootDirectory=`/`RootImage=` (path-view change; not inherently read-only). `ProtectHome=` (yes/read-only/tmpfs) covers /home, /root, /run/user only, not `/`.
3. **Configured-property absence is scoped:** `ProtectSystem=no` and empty `ReadOnlyPaths=` exclude only those configured mechanisms, not B2 as a whole (notice text).
4. **Host mount vs DAC:** `/` is `rw` (findmnt), `555` is DAC bit pattern and tmpfiles policy (S040). `findmnt` reads host namespace, not unit-private namespace.
5. **Configured vs live capability:** `CapabilityBoundingSet=cap_sys_admin` is configured text; `+` prefix not affected (S028); ExecStart prefixes not inspected; live CapEff/CapPrm unobserved; `ExecMainPID=1386` stale (ps exit 1) and journal `_PID=1520` differs (critic R11).
6. **Journal aggregates (counts/timestamps only, no bodies):** 9 `errno:13` matches, 9 distinct boots; window 2026-10-16T12:47:26−03 → 2026-10-19T22:48:24−03; oldest retained boot 2026-10-16T11:34:43−03 has zero unit records. Unit file ctime 2026-10-11; kernel 7.2.3 installed 2026-10-11 (pacman log).
7. **Ordinary-mkdir ordering is a fixture fact, not a Btrfs fact:** existing target under 0555 → EEXIST; new target → EACCES (ordinary mkdir, this kernel, uid 1000 caller-owned parent). Btrfs subvolume ioctl order unclassified; kernel sources are unregistered.
8. **Caller-owned vs root-owned fixtures:** SC3 (`0755 root:root`, uid 1000 → EACCES) is source-grounded inference (S035); SC9 (invoker-owned 0755 → success) is the executed fixture.
9. **Source versions:** S028 row footer is systemd 262.1 (Arch URL); host runs systemd 261.2-1; cited sentences verified present in both (V1, V2). S035 footer 6.19/2026-02-11; S038 footer 6.19/2026-02-08.
10. **Bot vs maintainer:** S036/S037 comments are automated triage (omarchybot defers to maintainers); rejection stands on registry text, not on host evidence.

## 6. Findings for the r13 correction (ordered by impact)

- F-A (blocking, correctness): the false universal persists in active MD 59, MD 92, JSON 87. Superseding text must replace these, and the committed bytes at 70fede2 must remain untouched as history.
- F-B (blocking, pointer integrity): both supersession pointers target `root-dac-correction-r13.{md,json}`, which do not exist. Create them or remove the pointers before landing.
- F-C (precision): the notice's list of "exhaustive" locations includes JSON decision_procedure step 2, which is incomplete rather than exhaustive, and MD worked-example step 3, which has no exclusive wording. Reword the notice to the actual defect.
- F-D (routed item 4): SC1/SC2 JSON inputs still say root:root; the caller-owned fixture basis must be stated.
- F-E (routed item 3): S036/S037 "maintainer-side" wording. Use an appended superseding row or dated note; do not edit immutable fields.
- F-F (attribution of origin): the exclusivity originated in C2ReviewR F2 and was carried by the matrix; MatrixCriticR §8 X3 "fixed" overstated the closure. The r13 report should cite both the reviewer origin and the outside rejection.
- F-G (volatile): MD grew during this pass; rerun pointer greps immediately before landing.

## 7. Limits

- Not independent non-author verification. Outside spot-check (E1–E6) is the only non-author record on disk.
- No privileged probe, journal re-query, or unit mutation was run. No install, build, test, or lint.
- Kernel-source claims in C2ReviewR F1 are unregistered; I did not fetch or re-verify them.
- SOURCES S027 row still lists only the CAP_DAC_OVERRIDE anchor; Thread-set anchors are cited only in the matrix header (SOURCES Search log line ~72). Registry widening is Sources-owned.
