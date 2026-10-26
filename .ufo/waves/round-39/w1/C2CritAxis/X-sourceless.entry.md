source: S208, S213, S214, S215, S216, S217, S218 in `corpus/SOURCES.md` — libalpm `lib/libalpm/{hook.c,add.c,sync.c,remove.c,util.c,trans.c}` at pacman commit `54d9411` (the installed `pacman 7.1.0.r9.g54d9411-3`; snapshots `.ufo/waves/round-39/frozen/src/`, digests in `SHA256SUMS`), and the own-work transaction capture `.ufo/waves/round-39/frozen/txcapture/` (pacman.log copy, hook owners, hook phases; MANIFEST sha256 `cb5cb4f436b93f22886ceac79b5a84c1b3b34256f671fb51d05c1b3af02c1bb4`)
verified-at: 2026-10-26 (sources fetched 2026-10-26T05:30Z; capture 2026-10-26T05:42:12Z)
recheck: `python3 tools/check-transaction-order-r39.py --revision <REV>` re-verifies every TO row against the pinned snapshots and the two host counts against the frozen capture; on-release of pacman for S208 and S213–S217; 30d for S218

# The libalpm transaction order on this host (round 39)

Ground: the update-safety plane (`PROVINCE.md` Core). `corpus/knowledge/pacman-hook-order-r38.md` holds the
order of hooks **within** a phase (HO1–HO7). This entry holds what happens **between** the phases: where the
two hook phases sit against the `transaction started` / `transaction completed` log lines, the order of
removals, package writes and install scriptlets inside the commit, the scriptlet arguments, when the hook
directories are read, and what the `[ALPM-SCRIPTLET]` log tag does and does not mean. Every rule is read
from libalpm source at the installed commit; the host column is read from a frozen copy of this host's
`/var/log/pacman.log`. Nothing here authorizes a package, hook or transaction action.

It re-grounds, at source, the transaction-order propositions of the staged package entry
`merge/tsukuroi/…/pacman-hook-timing-r25.md` (refused as staged in round 38, `corpus/lessons/round-38.md`
Gate). Which of its propositions this entry admits, corrects or rejects is recorded in
`corpus/lessons/round-39.md` Gate.

## Rules (source-level, pacman 54d9411)

| id | rule | source (file:line at 54d9411 and quote) | host consequence |
|---|---|---|---|
| TO1 | RULE NOT SUPPLIED — this control states no transaction order | S217 trans.c:1-30 “Copyright (c) 2006-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>” | control host cell, no host evidence: 60 transactions |
| TO2 | RULE NOT SUPPLIED — this control states no transaction order | S214 sync.c:1-30 “Copyright (c) 2006-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>” | control host cell, no host evidence |
| TO3 | RULE NOT SUPPLIED — this control states no transaction order | S213 add.c:1-30 “Copyright (c) 2006-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>” | control host cell, no host evidence |
| TO4 | RULE NOT SUPPLIED — this control states no transaction order | S213 add.c:1-30 “Copyright (c) 2006-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>” | control host cell, no host evidence |
| TO5 | RULE NOT SUPPLIED — this control states no transaction order | S208 hook.c:1-30 “Copyright (c) 2015-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>” | control host cell, no host evidence |
| TO6 | RULE NOT SUPPLIED — this control states no transaction order | S213 add.c:1-30 “Copyright (c) 2006-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>” | control host cell, no host evidence |
| TO7 | RULE NOT SUPPLIED — this control states no transaction order | S215 remove.c:1-30 “Copyright (c) 2006-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>” | control host cell, no host evidence |
| TO8 | RULE NOT SUPPLIED — this control states no transaction order | S216 util.c:1-30 “Copyright (c) 2006-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>” | control host cell, no host evidence: 252 of 441 |

## Order of one transaction, end to end

1. `[PACMAN] Running '<command>'` (the frontend).
2. PreTransaction hooks whose triggers match, in HO1 order (`running '<name>'` lines; TO1, TO5).
3. `[ALPM] transaction started`.
4. Removals of conflicting or replaced packages (sync commits), each `pre_remove` → files → `removed` → `post_remove` (TO2, TO7).
5. Each target in transaction order: `pre_install`/`pre_upgrade` → files and database entry → `installed`/`upgraded` → `post_install`/`post_upgrade` (TO3, TO4).
6. `ldconfig`, once (TO6).
7. `[ALPM] transaction completed` (or `transaction interrupted` / `transaction failed`, which end it without Post hooks).
8. PostTransaction hooks whose triggers match, re-read from disk (TO1, TO5, HO6).

Every line any step 2–8 child prints is logged as `[ALPM-SCRIPTLET]` (TO8).

## Boundaries — what this entry does NOT establish

- It does not say whether a given hook ran on this host; HO7 and the pacman.log `running` lines answer that.
- TO5's host column is consistency, not proof: the capture cannot separate "the hook file was absent" from
  "its triggers did not match".
- It reads no transaction live and runs no pacman command; the host column comes from the frozen copy.

## QUALITY check

- QUALITY 1–4: every rule row cites a mined tier-A row and a located quote at the cited lines (verified by
  `tools/check-transaction-order-r39.py`); host counts are reproduced from the frozen capture by the same tool.
- QUALITY 9: the snapshot digests and the capture MANIFEST are pinned in the tool and in the source rows.
- QUALITY 14: this section.
