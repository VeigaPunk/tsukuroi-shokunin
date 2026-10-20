# R18 NoticeSkill — SKILL.md freshness draft

Seat: TsukuroiR18-2.NoticeSkill. Baseline 842a5312; SKILL.md identical in lane worktree.

## Behavior

Six records, one heading `## R18-FRESHNESS — SKILL.md current-use re-verification (2026-10-20)`. Append-only; baseline bytes kept.

| ID | Line | Stale reading | Current [obs] |
|---|---|---|---|
| R18-FRESH-NoticeSkill-01 | 118 | kernel 7.2.3 | 7.2.11-arch1-1 (capture:6,32) |
| -02 | 120 | 7.1.4 dkms registration | no 7.1.4 entry (capture:95) |
| -03 | 130 | `snapper list-configs` empty | root, home configs (capture:80) |
| -04 | 132 | no snapshot net | snapshot existence unmeasured |
| -05 | 135 | last log 2026-10-13 | 2026-10-20T13:23:09-0300 (capture:65) |
| -06 | 1833 | mkinitcpio 41.1 installed | mkinitcpio-42.2-1 (capture:34) |

## Verification (read-only)

- Each `baseline_quote` matches baseline exactly once.
- Each `capture_quote` sits on its cited line.
- The notice section has no `#`-leading line and contains every `now` and `capture_ref`.
- The JSON parses; each record has the eight keys.

## Outputs

- `.ufo/waves/round-18/build/drafts/NoticeSkill.append.txt`
- `.ufo/waves/round-18/build/drafts/NoticeSkill.records.json`

No production file changed.

## Findings

1. S060 is absent from lane `corpus/SOURCES.md`. The integrator must add it.
2. The assigned keys (`now`, `reason`) differ from the R17 gate (`observed_now`, `stale_reason`). Confirm the R18 checker accepts them.
3. The R18 capture is untracked; commit it before a `--revision` gate reads it.
4. Unobserved in R18: snapshot existence, `snapper list-configs`, `pacman -Qu`/`-Qm`, "transaction completed". Recorded as unknown, not claimed.
5. Left unchanged, outside targets: SKILL.md:50 and :100-101 (16 foreign count, not re-measured).

## Tooling

None installed or updated.

Scope: executed=read-only `git show`/`diff --stat`/`rev-parse`/`cat-file`, `grep -cF` on baseline, `sed -n` on the capture, `python3` JSON parse of drafts.
