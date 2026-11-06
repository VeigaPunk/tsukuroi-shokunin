# ConnectorOverlap — round 86, wave w1 (sibling-overlap scan)

Seat: leaf connector. Axes named: **adjacency** (cross-lane discoverability and non-duplication of the
r86 hibernation-parse ground) and **operability** (can a sibling lane find and run the artifact read-only).
Measured revision: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` →
`1e1caabcdd740a6429dd31d7aba3b725ff8c677d` (the entry commit; the candidate gate commit `dc884949` is its parent).
Nothing outside `.ufo/waves/round-86/w1/` was written; no lane file, index, bookmark or worktree state was touched.

Receipts (verbatim command output): `.ufo/waves/round-86/w1/ConnectorOverlap/`
`sibling-scan.txt`, `mori-doc-rows.txt`, `mori-host-capture.txt`, `kaidoku-flip.txt`,
`false-positives.txt`, `province-coverage.txt`, `gate-receipt.txt`.

## 0. Scan method and its result

Tokens searched, per lane, over `corpus/ tools/ docs/ scripts/` with `.ufo/` excluded (waves hold
transcripts, not claims): `hibernat|noresume|nohibernate|resume_offset|obsolete_checksetup|parameqn`.
Then a fleet-wide pass for `__setup`, `/proc/cmdline`, `kernel-parameters` and for inbound citations of
`check-hibernate-resume` / `hibernation-boot-parse`.

`grep -ril -F obsolete_checksetup` and `grep -ril -F parameqn` outside `tsukuroi-shokunin`:
**0 and 0** (`sibling-scan.txt`). The parse-plane ground the r86 entry holds is not duplicated anywhere in
the fleet; this independently supports C2's "ground no entry held" for the two parse functions themselves.

No sibling cites `check-hibernate-resume`, `hibernation-boot-parse` or the r86 battery
(`grep -rn --exclude-dir=.ufo` over the fleet root returns only `MANIFEST.json` round digests and an
unrelated mori SCORECARD line). There is therefore no recipient acknowledgement of this lane's artifact
anywhere; nothing in this report is an acknowledgement.

## 1. Hits, classified

| # | Lane | Path:line | Class | Relation to `corpus/knowledge/hibernation-boot-parse-r86.md` | PROVINCE coverage |
|---|---|---|---|---|---|
| H1 | mori | `corpus/evidence/sources-r61/v7.2/kernel-parameters.txt` (sha256 `23b1a690210b6884f040a6b1e5baf1fc18856e844d30d4784470bd210953340c`), byte-identical to `corpus/evidence/sources-r55/Documentation_admin-guide_kernel-parameters.txt.v7.2`; rows `hibernate=` 1962-1969, `nohibernate` 4479, `noresume` 4593, `resume=` 6574, `resume_offset=` 6579 | **overlap, no conflict** | Same upstream file, same tag v7.2, same sha256; mori's *claim* on it is the PSI boot parameter only (`corpus/knowledge/system-pressure-r24.md:127` `psi=` @ 5505-5507; `kernel-v7.3-recheck-r55.md:58`; `psi-v73-recheck-r61.md:57` @ v7.4 5540-5542). The doc plane names the options; the r86 entry holds the parse plane. Disjoint. | Covered: mori `PROVINCE.md:13` refuses "boot state (→ tsukuroi)"; tsukuroi Core holds "Journal & boot triage" and the boot-chain/boot-plane knowledge. No new surface. |
| H2 | mori | `.ufo/waves/round-24/w1/ScoutHostKernelConfig.md:86-91`; `.ufo/waves/round-54/w1/Mo54ExecHostRead.md:91-92` | **overlap, no conflict (host artifact)** | The same host `/proc/cmdline`, captured 2026-10-22 with `md5sum` `ecace254fc5680e70712d46226bf7aca`; live read today is the same md5 (`mori-host-capture.txt`). Independent, 15-day-earlier capture of the r86 host base. | Covered (host receipt surface). |
| H3 | kaidoku | `corpus/lessons/round-74.md:31` | **admissibility precedent** | `proc_cmdline(5)` was *rejected* with the quote “Arguments passed to the Linux kernel at boot time.” and the standing flip: “Flip only if the question changes to kernel boot arguments.” That flip condition is satisfied by this round's question — for the file's identity claim only, not for the parse rule. | Covered (source admission is this lane's own `SOURCES.md`). |
| H4 | mado | `tools/mado-tripwire.py:263` (`"hibernat"` in `OMARCHY_MUTATE`), matched at `:1269` by `any(k in argv0 …)`; `HOST_MUTATION_BINS` at `:264-266` | **adjacent doctrine, no conflict** | Both lanes treat hibernate/boot mutation as operator-owned; mado's subject is a desktop command-name denylist, this lane's is the kernel token parse. | Covered: mado keeps the desktop plane (`OUT-004`); no handoff needed. |
| H5 | kumitate | `scripts/wave-census.mjs:488,495` `noResumeKey` | **false positive** | The census `--resume` flag, not a boot token. | Out of province for this question. |
| H6 | souji | `tools/souji-census.sh:2816` (`/proc/{candidate}/cmdline`), `tools/souji-proc-census.sh:295` | **false positive** | Process argv, not the kernel command line — the same referent confusion kaidoku rejected at H3. | Out of province for this question. |
| H7 | kengaku, revenger, kasegi, kotoba | `kengaku …/R40ConnSibling.md:173`; `revenger corpus/snapshots/dex-format.html:2434`; `kasegi corpus/source-snapshots/round-35/S052.txt:6551`; `kotoba …/host-map.tsv` (`.ufo` only) | **false positive** | Android "App hibernation", Java "Hibernate Validator", JPA/Hibernate ORM. | Not this surface. |

`false-positives.txt` holds the exact lines for H5-H7 so a later connector does not re-derive them.

## 2. The one non-obvious move (proposed links, not written)

**L1 — doc-plane / parse-plane register row (mori ↔ tsukuroi).** The r86 entry's rows BP1-BP8 are all
source-code claims; the pinned manual row set that a reader would reach for first is already committed in a
sibling lane at the same tag and the same sha256. What the doc plane *does* say is the useful part:
`noresume [SWSUSP] Disables resume and restores original swap space.` (4593) and
`nohibernate [HIBERNATION] Disable hibernation and resume.` (4479) name the options and never a value;
`resume=` (6574) gives a *format* (`{/dev/<dev> | PARTUUID=<uuid> | <int>:<int> | <hex>}`) and
`resume_offset=` (6579) gives `<PAGE_SIZE>` units — and neither states the prefix match, the `-`/`_`
equivalence, value-blindness, last-token-wins, the sscanf skip, or the empty-value case. The doc plane is
therefore a **counter-witness**: the gate's rule set cannot be derived from the manual, which is exactly
what the entry asserts and what a reviewer would otherwise have to take on trust. Proposed: one OVERLAP
register row (the `adjacency-mori-oom-r27` pattern) naming the shared upstream file with both lanes' paths
and the one sha256, tsukuroi retaining the parse claim and mori retaining PSI. No entry edit, no new pin.

**L2 — host-artifact corroboration row.** mori's 2026-10-22 capture (H2) is the same bytes as this round's
host base; recording it makes the r86 host value column independently corroborated by a sibling lane rather
than self-corroborated. Same capture records that all five configured cmdlines in `/boot/limine.conf` are
that identical string — i.e. the `resume=`/`resume_offset=` pair is bootloader configuration, so the
operator action in the entry is a boot-entry edit, not a runtime knob. That is operability evidence for the
entry's "Operator actions" section, obtained without a new host read.

**L3 — kaidoku flip, used narrowly.** `proc_cmdline(5)` may now be cited for the *file identity* sentence
(“Arguments passed to the Linux kernel at boot time.”), never for the parse rule. BP1-BP8 keep S346-S348.

**L4 — false-positive register** (H5-H7), so the next scan does not spend a wave re-deriving them.

**L5 — PROVINCE discoverability (reported defect, patch below).** `grep -n -i -E 'hibernat|resume=' PROVINCE.md`
returns **rc=1, zero lines** (`province-coverage.txt`), while `SKILL.md:5917` registers the `hibernate-resume`
gate and `SKILL.md:5920` registers `resume-gate-battery-r86`. A sibling seat (this one included) reads
`PROVINCE.md` to learn a lane's scope; from that document the hibernation/resume surface does not exist.
The r86 read is an *extension of an existing Core read*, not a new surface: `PROVINCE.md:420,454,460,472`
already read `/proc/cmdline` for the modprobe routes (r71/r72), so no promotion paragraph is being skipped —
only the pointer is missing. Proposed patch: `proposed-PROVINCE-r86.md` in this directory (L1 decides).

## 3. Contradictions stated explicitly

- **None found between the r86 gate and the pinned source** on the clauses this seat checked, and the two
  clauses most exposed to attack check out against the pin:
  - `hibernate=` — pinned `kernel_power_hibernate.c:1424-1438` sets `noresume=1` for `noresume`, `nocompress=1`
    for `nocompress`, and **both** `noresume=1` and `nohibernate=1` for `no`; the gate
    (`tools/check-hibernate-resume.py:119-129`) maps `no…` to `HR-HIBERNATE-DISABLED` only, which is
    consistent precisely because `nohibernate` implies `noresume` (docstring lines 19-20).
  - BP7's "no `+`, no `-` for unsigned" — pinned `lib_vsprintf.c:3660-3672` sets `is_sign` only for `d`/`i`;
    for `u` a leading `-` or `+` fails `isdigit` and the conversion breaks, so the offset is kept. Entry,
    gate (`resume_offset()`, digits-only `lstrip`) and the battery's `OFFSET-SSCANF` junk list
    (`"-"+o`, `"+"+o`) all agree. This is a verified clause, not an assumed one.
- **One documentation gap, not a code contradiction.** The entry's BP rows do not enumerate the
  `hibernate=` handler at all, while the gate implements it, the battery tests it (`HIBERNATE-NOX`, 3 cases),
  and mori's pinned manual documents it (`hibernate=` 1962-1969, including the `noresume` sub-value). The
  frozen declaration's row list omits `hibernate=` too, so this is a declared-scope boundary and not a
  violation of C2 — but a sibling reading only the entry would not learn the gate answers `hibernate=noresume`.
  Reported for L1's judgement; no edit proposed by this seat.
- **Rule-transfer hazard (named, not a defect).** mado's `hibernat` match is a *substring* (`k in argv0`);
  the kernel's is a *prefix* (BP1). The two must not be conflated when a reader compares the lanes.
- **Surface overlap, not conflict.** mori's r24 seat read `/boot/limine.conf` (five configured cmdlines, via
  `sudo -n grep`) as PSI evidence. Bootloader configuration is this lane's boot-chain surface and mori's own
  `PROVINCE.md:13` refuses boot state; the read was read-only and claimed nothing about boot. Recorded as an
  inbound surface overlap, no handoff requested.

## 4. Operability receipts (read-only, unprivileged)

```
$ python3 tools/check-hibernate-resume.py --live
{"findings": [], "verdict": "HEALTHY"}
rc=0
$ python3 tools/check-hibernate-resume.py --selftest
…
{"cases": 13, "failed": [], "selftest": "PASS"}
rc=0
```
(`gate-receipt.txt`; cwd `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, revision `1e1caabc`.)
Both modes run as the unprivileged user, write nothing, and need no `sudo`; `SKILL.md:5917`'s
"13 built-in fixtures" matches the measured `"cases": 13`, so the registry row is not stale.

**Not run by this seat:** `tools/resume-gate-battery-r86.py` (C1's counting command). The 30/30 target is
another seat's claim; this report asserts nothing about it.

## 5. Refusals

No sibling file, lane file, `MANIFEST.json`, `.ufo/state/`, `SCORECARD.md`, `PROVINCE.md` or `SKILL.md`
was modified; no `git`/`jj` mutation; host untouched (no swap, suspend, sysctl, `/sys`, `/boot`, pacman).
Links L1-L5 are proposals only. Scratch `/fast/scratch/hyaku/tsukuroi-r86/ConnectorOverlap` removed.
