VERDICT: supports (slice reproduces byte-identical; no quarantined row adopted) — with one defect-found side note: the raw-id intersection is NOT empty (S213), and the L1 collisions file is stale against the tip.

Seat: ScoutQuarantine, item A-8. Read-only; scratch /fast/scratch/hyaku/tsukuroi-r39/ScoutQuarantine (receipts copied to w1/ScoutQuarantine/). Lane revision used for id sets: explicit 2e1c2a40 and 0eff65b2 via `git show` (lane HEAD is now 394e1ba; I did not use the working tree).

## 1. Slice re-derived — identical to the L1's file
Command: the round-prompt lines 540-543 awk (`-v l='tsukuroi'`, `$2 ~ "`tsukuroi`" && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4,$5}`) on
/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md (sha256 5afe1810a6c3d62f…, 83621 B).
- 12 lines. `cmp` against .ufo/waves/round-39/assimilation/quarantine-slice: IDENTICAL (both sha256 a17de5fbd02bc923c9c29aa606e8561ecb5a181e58e0d09010a6817901781006). Receipt: w1/ScoutQuarantine/slice.rederived.
- Ids: S211 S213 (class `payload-absent`, register lines 229-230, round1) + S225 S230 S231 S242 S243 S244 S249 S250 S251 S252 (prose class "unreachable family", register lines 366-375, rounds 3-5).
- Only tsukuroi lines in the register: grep -n tsukuroi → 229,230 (data), 253 (summary `| tsukuroi | 2 |`, stale, excluded by the awk), 366-375 (data). No lane cell variants missed.
- Cosmetic: the 10 prose-class lines print the id with a trailing backtick (`S225\``) because the register's id cell is `S225\`` (register defect in lines 366-375: unbalanced backtick). The awk `/S[0-9]+/` still matches, so the slice is complete, but a consumer that splits ids must strip the backtick. My ids file strips it (w1/ScoutQuarantine/quarantine-ids.txt).

## 2. Is any quarantined campaign id adopted by round 39? — No (by row), but raw ids collide
The entry corpus/knowledge/pacman-transaction-order-r39.md: `source: S208, S213, S214, S215, S216, S217, S218`. Count of each slice id inside the entry (grep -c word match): S213=5, every other slice id =0 (S211=0, S225=0, S230–S252=0).
- Raw-id intersection of {slice ids} with entry citations = **{S213}**; not empty.
- Semantic intersection = ∅. The slice ids are *staged-package* ids (merge/tsukuroi/SOURCES.append.md, S200–S346, 147 rows). The lane's S213 at 2e1c2a40 is `libalpm add.c at pacman 54d9411` (corpus/SOURCES.md:222, added by 4078eb2), unrelated to the staged S213 (Oracle Snapper Japanese page; SOURCES.append.md line 20). In the entry S213 always means add.c (TO3 `S213 add.c:466-474`, TO4, TO6).
- Lane ∩ slice at tip: S211, S213 (lane S211 = alpm.c, corpus/SOURCES.md:220, not cited by the entry). At base 0eff65b2: S211 only. Lane max id: 212 at base, 218 at tip.
- None of the staged knowledge files that carry S211/S213 was adopted: they are upstream-release-watch-r25.md (S211) and snapper-rollback-bilingual-r25.md (S213); neither exists in the lane (`pacman-transaction-order-r39.md` is the only r39 entry; it cites the r25 staged pacman-hook-timing-r25.md only to re-ground it, and that staged file cites S201, S202, S209, S212 — no slice id).

### Defect found (assimilation): collision file is stale against the tip
Recomputed `comm -12 lane-ids staged-ids`:
- at base 0eff65b2: S200–S212 (13 ids) — equals the L1's assimilation/collisions (13 lines, S200–S212).
- at tip 2e1c2a40: S200–S218 (19 ids) — S213–S218 now also collide with staged ids, because 4078eb2 took S213–S218 for lane rows.
So the L1's collisions file reflects the base, not the tip it was said to be computed against, and staged S213–S218 are no longer the "free" ids the first_id=S200 plan assumes. Any future adoption of staged rows (including the quarantined S211/S213) needs renumbering (merge/tsukuroi has renumber-staged.py in .ufo/waves/corpus-expansion-1) or a lane row of those numbers will be silently overwritten/duplicated. Receipts: w1/ScoutQuarantine/lane-ids-tip.txt, staged-ids.txt.

## 3. The two `payload-absent` rows — what the staged payload claimed
### S211 (staged, round1)
- Source: https://gitlab.freedesktop.org/api/v4/projects/plymouth%2Fplymouth/repository/tags. Class code, tier A, status mined, recheck on-release; used-by corpus/knowledge/upstream-release-watch-r25.md.
- Claimed (SOURCES.append.md:18): "authoritative upstream plymouth release-tag index used as the on-release watch target"; revision pin "15 tags returned; newest 26.134.222 created 2026-05-14; previous 24.004.60 created 2024-01-04"; claim "newest upstream plymouth tag as of 2026-10-23 is still 26.134.222 … lane's plymouth rows S096, S097, S110, S111 remain current".
- Register quote: `name: 26.134.222 ... created_at: 2026-05-14T05:21:12.000Z` (gate in lanes/tsukuroi/SOURCES-PROPOSED.md:147-153; lint finding: ABSENT, missing_fragment `name: 26.134.222`).
- Live check 2026-10-26 (curl, read-only): the endpoint returns JSON with `"created_at":"2026-05-14T05:21:12.000Z"` on tag 26.134.222 and `commit.title` fixed-string "fix plymouth-switch-root-initramfs.service" matches the tag message of 26.134.222 (second gate quote). Newest tag is still 26.134.222, previous 24.004.60. So the *facts* hold; the quote is a YAML-style reformatting of JSON (`name: 26.134.222`, with `...` elision), not a literal span — a quote-form defect, not invented content. Discrepancy: default-page response currently has 20 tags (per_page=100 → 35), not "15 tags returned"; the count claim does not reproduce (the newest/previous-tag facts do).
### S213 (staged, round1)
- Source: https://docs.oracle.com/cd/F22978_01/btrfs/btrfs-UsingtheSnapperUtilityWithBtrfsSubvolumes.html. Docs, tier B, Oracle Linux 8 Btrfs doc set F22978_01, machine-translation banner; used-by corpus/knowledge/snapper-rollback-bilingual-r25.md.
- Claimed (SOURCES.append.md:20): Snapper snapshot types (single/pre/post), `create-config` effects (/etc/sysconfig/snapper entry, config file, .snapshots subvolume), and `undochange` reverting changes to existing files not the filesystem, with no data-integrity check of the change.
- Register's ABSENT quote `has a newer release appeared?` is a **linter mis-attribution**: it comes from the tier-notes prose at lanes/tsukuroi/SOURCES-PROPOSED.md:199 ("S211 is not a duplicate … the index that answers "has a newer release appeared?""), id-bound to S213 because the line sits in S213's note block (lint JSON: the same S213 has two `sweep-found` quotes — the undochange sentence (fold no-whitespace) and the `sudo snapper -c config_name create-config -f btrfs fs_name` code block (exact)).
- Live check 2026-10-26: after whitespace-stripping the page text, the Japanese undochange sentence "undochangeサブコマンドは、変更のデータ整合性をチェックしません。" is present (True), the create-config command is present (True), the English original "files created after the snapshot was taken continue to remain after an undochange operation" is present, banner present; "has a newer release appeared?" absent (False; not a gate quote).
- Verdict on class: S211 = real quote-form mismatch on valid content; S213 = false positive.

### Relation to the round-39 theme
Round 39 = C1 census STORAGE arm (hidden/absent btrfs sysfs root, mounts:btrfs-without-sysfs) and C2 libalpm transaction order TO1–TO8 (pacman hook.c/add.c/sync.c/remove.c/util.c/trans.c at 54d9411). S211 (plymouth upstream tag index, an on-release watch for the plymouth frontier) and S213 (Snapper snapshot/undochange semantics on Oracle Linux) touch neither: no pacman transaction order, no hook phase, no btrfs device-stats or sysfs. Snapper/plymouth appear in the lane only as boot-chain/update-safety context, not in the claims. Neither row would back any TO row or the C1 predicate.

## 4. Remaining ten slice rows (unreachable family; not adopted)
S225, S230, S231, S242, S243, S244, S249, S250, S251, S252: the register lists "could not be fetched" (S225, ArchWiki Translation Team zh-cn URL with a truncated, unbalanced URL in register line 366) or "gate block named no locator" (rest). Staged row types: S230/S242/S252 are `own-work` rows in the staged package (SOURCES.append.md:37,49,59). Round 39 cites none, so per the prompt's rule they stay quarantined/unverifiable and I did not hand-check them (not asked; outside C1/C2).

## Not done
- Did not fetch/judge S225 or the nine no-locator rows.
- Did not judge any TO row against pinned source (this seat has no TO rows to report; none judged).
- Did not re-run counters; did not touch the lane or register.
- No tools installed.
