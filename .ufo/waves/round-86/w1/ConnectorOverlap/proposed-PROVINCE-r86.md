# Proposed PROVINCE.md patch — R86-PROVINCE-POINTER (proposal only; L1 decides)

Reported by seat `ConnectorOverlap`, round 86 wave w1. **Nothing was edited.** This file is a proposal
written under the seat's own wave dir, per the seat's "defect → file:line + proposed patch" rule.

## Defect (freshness / adjacency)

`PROVINCE.md` — the document a sibling seat reads to learn this lane's scope — does not mention the
hibernation/resume surface at all:

```
$ grep -n -i -E 'hibernat|resume=' PROVINCE.md
rc=1                     # zero lines, 573-line file
```

while the same surface is registered in `SKILL.md:5917` (`hibernate-resume` gate) and `SKILL.md:5920`
(`resume-gate-battery-r86`), and held by `corpus/knowledge/hibernation-boot-parse-r86.md` (BP1-BP8) plus the
r85 predecessor entry. Consequence, measured: this seat's sibling scan had to reach `SKILL.md` to discover
the artifact; a `PROVINCE.md`-only reader (the documented ownership surface, and the file the adjacency
anchors OUT-001..OUT-010 quote) sees no hibernation surface and would re-derive or duplicate it.

This is a **pointer** gap, not a scope gap. The surface is an extension of existing Core reads:
`PROVINCE.md:420,454,460,472` already read `/proc/cmdline` for the modprobe routes (r71/r72), and
`PROVINCE.md` Core holds "Journal & boot triage" with the boot-chain/boot-plane knowledge. No promotion
paragraph, new authority or capability is requested.

## Proposed insertion (append-only, after the last line of `PROVINCE.md`, i.e. after the r76 journald section)

```markdown
## Round 86 — hibernation boot-option parse (pointer, no new surface)

Append-only pointer; every section above stays as written. The hibernation/resume reading this lane has
carried since round 84 is now named here so a sibling reading only this document can find it. The surface is
the kernel's *parse* of the hibernation boot options, not a new plane: the lane already reads
`/proc/cmdline` for the modprobe routes above, and Core already holds boot triage. Entry:
`corpus/knowledge/hibernation-boot-parse-r86.md` (+ `.json`), rows BP1-BP8, sourced S346-S348 and S343
(Linux v7.2 `init/main.c`, `kernel/params.c`, `lib/vsprintf.c`, `kernel/power/hibernate.c`; snapshots and
`SHA256SUMS` under `.ufo/waves/round-86/before/src/`). Gate: `python3 tools/check-hibernate-resume.py
--live` (or `--facts FILE`; `--selftest` 13 cases) and the battery `python3 tools/resume-gate-battery-r86.py
--gate <PATH>` (30 families). Host value on 2026-11-06: `resume=/dev/mapper/root` and
`resume_offset=3795013`; `CONFIG_HIBERNATION=y`, `CONFIG_PM_STD_PARTITION=""`.

**Not claimed:** no hibernation, suspend or reboot was run; the reading is source plus `/proc`/`/sys` text.
**Operator-owned:** removing or editing a boot token, any bootloader or `limine.conf` edit, `swapon`/`swapoff`,
and any write under `/sys/power`. **Mori's, unchanged:** nothing about capacity or fleet runway is stated
here. **Cross-lane:** the same upstream `Documentation/admin-guide/kernel-parameters.txt` at tag v7.2
(sha256 `23b1a690210b6884f040a6b1e5baf1fc18856e844d30d4784470bd210953340c`) is pinned in
`../mori-shokunin/corpus/evidence/sources-r61/v7.2/` for the PSI boot parameter; the doc plane names the
options and states no parse rule, the parse claim stays here.
```

## Why this form

- Append-only, like every other round section in the file; no existing sentence is edited or retired.
- Names the artifact, the gate, the battery and the host value, so a sibling can act without opening the entry.
- Repeats the operator-owned boundary and the mori split, so the pointer grants nothing.
- Carries the shared-source sha256 so the cross-lane row (report L1) resolves by content, not by line number.

## Alternative if L1 prefers a one-liner

Insert under `## Frontier` (after the two existing bullets, `PROVINCE.md:75-80`):

```markdown
- Hibernation boot-option parse (BP1-BP8) is Core-adjacent to boot triage: entry
  `corpus/knowledge/hibernation-boot-parse-r86.md`, gate `python3 tools/check-hibernate-resume.py --live`,
  battery `tools/resume-gate-battery-r86.py`. Read-only; no hibernation was run; operator-owned actions unchanged.
```
