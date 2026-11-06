# ScribeFrontier — round 85, wave w1 (tsukuroi lesson draft)

Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, branch `master`, measured revision
`479d868b2fc8969a19a617cd55ced5c13edd84b6` (`git rev-parse master`, exit 0). Pre-round tip
`3ed94533…`, freeze `66374a4d…`. The working tree was **dirty** while this seat ran (sibling seats in
flight): `M SKILL.md`, `M corpus/SOURCES.md`, `M corpus/knowledge/hibernate-resume-plane-r84.md`,
untracked `corpus/knowledge/hibernation-availability-r85.json`, `.ufo/waves/round-85/w1*`. Every claim below
cites committed bytes or names the working-tree file it read; nothing here treats the uncommitted tree as
evidence.

Deliverable: `.ufo/waves/round-85/w1/ScribeFrontier/round-85-lesson-draft.md` (17.0 kB, five required
sections plus landing notes).

## What the draft contains

- `## Fresh-start read` — the three rejected closures (MANIFEST verdicts `82/83/84 = rejected-honest-stop`,
  re-read from `MANIFEST.json`) with one root-failure line each, read against
  `corpus/lessons/round-8{2,3,4}-verifier-spotcheck.md`; common thread stated (all three are instrument
  defects, numbers reproduced, claims still failed).
- `## Gate` — 6 rows, 3 admits + 3 rejects, each with URL, access date 2026-11-06, raw lines, a ≤25-word
  verbatim quote and a `sed -n` proof block.
  - S343 `kernel/power/hibernate.c` raw 109-113 (+1424-1432, 1518-1524), 10-token quote → ADMIT (HA1–HA5).
  - S344 `include/linux/security.h` raw 104-113, 128-158, 19-word quote (located 105-107) → ADMIT (HA6).
  - S345 `security/lockdown/lockdown.c` raw 20-22, 43-46, 65-73, 7- and 5-token quotes → ADMIT (HA6/HA9).
  - REJECT man7 `kernel_lockdown(7)` (HTML :135, body `d07ec15a…`): its "Unencrypted" qualifier is absent
    from the pinned v7.2 file (`grep -ic 'encrypt\|luks\|dm-crypt' kernel_power_hibernate.c` → `0`, exit 1).
  - REJECT ArchWiki raw :105 (body `98320ec9…`, 49846 B) — tier-C restatement with no mode boundary, and
    explicitly **not** the r84 reject reason: that URL returned wikitext today, so the interstitial argument
    does not survive.
  - REJECT ArchWiki raw :111 (swap-size sentence, 18 words) — no bound, no unit.
- `## Mistakes` — M1 (lane seat labelled as named non-author reviewer: fleet report
  `/home/vgpnk/Projects/shokunin/.ufo/reports/round-84/tsukuroi.md:12`, entry `2ad4d1ef:…:67`; captured by
  LEARNING.md §Discernment :45-46; fix = proposed QUALITY 120 + `check-nonauthor-label-r85.py`, ExecLints
  builds it) and M2 (entry without `source:`/`recheck:`; captured by LEARNING.md §Files the path writes
  :67-68 and QUALITY 8; fix = `check-entry-headers-r85.py`, red at `3ed94533`, green on the repaired copy).
- `## Routed defects received` — all five r84 defects mapped: 1 fixed (working tree), 2 adopted + M1,
  3 done at freeze, 4 honoured (no counter citation), 5 adopted and demonstrated.
- `## Seat harm` — `entries: none observed` at drafting with the wave-settlement source named for the L1.

## Commands run (read-only; exit codes as observed)

| Command | Result |
|---|---|
| `git rev-parse master` (lane) | `479d868b…`, rc 0 |
| `sha256sum -c SHA256SUMS` in `before/src` | 4/4 `OK`, rc 0 |
| live re-fetch of the 4 pinned URLs (`curl -sS -L`, 2026-11-06) + `cmp -s` vs pins | HTTP 200 each; all four `identical`, rc 0 |
| `curl` man7 `kernel_lockdown.7.html` | `200 9861` |
| `curl` ArchWiki `action=raw` | `200 49846` |
| `git grep -rli -e lockdown_hibernation -e nohibernate -e hibernation_available 3ed94533 -- corpus/knowledge` | no output, rc 1 (empty) |
| `grep -ic 'encrypt\|luks\|dm-crypt' kernel_power_hibernate.c` | `0`, rc 1 |
| `git log -1 --format='%H author=%ad committer=%cd' 66374a4d` / `^` | author `16:44:20` both; committer `16:52:22` vs `16:44:20` — parent-date stamp recurs |
| `git show 3ed94533:corpus/knowledge/hibernate-resume-plane-r84.md \| head -6` | no `source:`, no `recheck:` (M2 red) |
| `git show 2ad4d1ef:corpus/knowledge/hibernate-resume-plane-r84.md \| grep -n 'Non-author per-row'` | `:67` (M1 red) |
| `git status --porcelain` | 3 modified, wave dir + r85 entry JSON untracked (recorded, not used as evidence) |

## Findings for the L1

1. `.ufo/waves/round-85/w1-spec.json` milestone says "HA1-HA8"; the drafted
   `corpus/knowledge/hibernation-availability-r85.json` carries **nine** rows (`HA1`…`HA9`, HA9 = `lockdown=`
   takes integrity or confidentiality). One of the two is a row short; not adjudicated here, no count claimed.
2. `corpus/SOURCES.md` rows S343–S345 and the r84 entry header repair exist only in the working tree at
   drafting. The draft's registry paragraph says so and is written to be committed with them.
3. `corpus/knowledge/hibernation-availability-r85.md` did not exist at drafting; M2's header check must pass
   on it before landing, and its `source:` must name S343–S345 and S336.
4. Freeze controls all read below target (`controls-receipt.txt`): K0 0/20, K1 0/20, K2 13/20 ×3,
   K3a/b/c 0/20, K3d/e 13/20, K4 2/20, K5 0/20 ×3, K6 14/14/15 of 20. C2's 20/20 candidate measurement is
   **not** this seat's and is not claimed anywhere in the draft.

## Not done / refused

- Did not execute the battery or the gate (instrument owners: MutGate, MutBattery, ExecReplicate,
  ReviewGate).
- Did not run `sources-census.sh validate` (ScoutSources owns it) and did not add registry rows.
- Edited no lane file, committed nothing, ran no mutating git/jj command, spawned no subagent, touched no
  host state. No tool was installed or upgraded, so there is nothing to record under the tooling directive.
- Scratch `/fast/scratch/hyaku/tsukuroi-r85/ScribeFrontier/` held only the two fetched reject bodies and the
  live re-fetches; their sha256 values are quoted in the draft, and the directory was removed on exit.
