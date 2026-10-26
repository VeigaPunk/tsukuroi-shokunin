# AsmRevTiming receipts — item A-5 (gate review, pacman-hook-timing-r25.md), 2026-10-26

## Execution disclosure (criterion 31 form)

Judged content was read with read/grep/glob and two URL reads only. Auxiliary executed
commands, disclosed exactly:

1. `sha256sum /home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/pacman-hook-timing-r25.md /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/pacman-hook-order-r38.md`
   → `e18c146e733d3cab4bcc82c2ba30b9a571791ec132f7988cd93481b079f09324  …/pacman-hook-timing-r25.md`
   → `b56c90f1ebbdfa3d07f369e39b7580d6b0050da69eb9d4d2b560b58771c73f61  …/pacman-hook-order-r38.md`
   (candidate binding per corpus/QUALITY.md criterion 38)
2. `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse HEAD`
   → `5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf` (read-only; no index/jj state touched)
3. `mkdir -p` of this receipts dir; `write` of this file and of `../AsmRevTiming.md`.

No scratch dir was created (no clone, copy, mutant or fixture was needed); nothing to
remove. No tool installed or upgraded. No pacman, no sudo, no host change, no lane
tracked file touched, no shokuknow file written.

## Web reads (access date 2026-10-26)

- `https://wiki.archlinuxcn.org/wiki/Pacman` (rendered; session artifact 10575):
  - rendered :525-534, the five-step transaction order: "2. 如果有可以执行的 *pacman*
    `PreTransaction` 钩子，执行这些钩子." / "3. 被替换、出现冲突或被指定删除的软件包将会被删除" /
    per-package "1. …执行 `pre_install` 函数(更新时执行 `pre_upgrade`…)" / "3. *pacman*
    将软件包文件解压到系统… (.pacnew)." / "4. …执行 `post_install` 函数(更新时执行
    `post_upgrade`…)" / "5. 如果*pacman* `PostTransaction` 钩子可执行，执行这些钩子."
  - rendered :642, the hook-directory contract: "*pacman*可以在处理前后，运行
    `/usr/share/libalpm/hooks/`文件夹下的hooks，更多的hooks文件夹可以通过`HookDir`选项在
    `pacman.conf`中指明，默认`/etc/pacman.d/hooks`。Hook文件必须以*.hook*为后缀。"
- `https://wiki.archlinuxcn.org/wzh/index.php?title=Pacman&action=raw` (raw wikitext;
  session artifact 10768):
  - :5 `{{翻译状态|pacman|2024-05-22|808924}}` — the translation-source template behind the
    staged entry's provenance claim (en:Pacman rev 808924, 2024-05-22). Present verbatim.
  - :355 `===安装/更新/删除 软件包时发生了什么===` and :444 `===钩子===` — both section
    anchors cited by the staged entry exist and hold the claimed content (:357+ the
    five-step order; :446 the hook contract).
  - NOT re-measured here: the page's own current revision id (staged row's "revision
    34634, last edited 2025-12-14") — the raw wikitext does not carry it.

## Frozen-source reads (lane, read-only, pinned pacman 54d9411)

`.ufo/waves/round-38/sources/` (SHA256SUMS; row hashes recorded at `corpus/SOURCES.md:217-221`):

- `alpm-hooks.5.asciidoc` (lane S209, snapshot sha256 `2970cb35…`): :20 "When =
  PreTransaction|PostTransaction (Required)"; :23 "AbortOnFail (Optional, PreTransaction
  only)"; :24 "NeedsTargets (Optional)"; :35-39 hook directories + "Hooks are run in
  alphabetical order of their file name, where the ordering ignores the suffix."; :80-81
  When Required; :87-89 AbortOnFail text; :91-93 NeedsTargets→stdin; :126-127 ".pacnew …
  the original file name is used in triggering the hook"; :131-132 "PostTransaction hooks
  will *not* run if the transaction fails to complete for any reason."
- `hook.c`:448-452 — "/* exclude the suffixes from comparison */" + strncmp over the
  shorter length, tie → shorter first (lane HO1).
- `trans.c`:201-240 — Pre-hook phase before "transaction started"; both failure branches
  `return -1` before the post-hook block; `_alpm_hook_run(…POST_TRANSACTION)` only inside
  the `else` of `if(trans->state == STATE_INTERRUPTED)` after "transaction completed" (lane HO6).

## Lane registry rows read (corpus/SOURCES.md at HEAD 5edb6c2e)

- :13 S007 pacman.conf(5) HookDir precedence, tier A, "Later HookDir directories take
  precedence"; :14 S008 alpm-hooks(5) OVERRIDING HOOKS, tier A.
- :210 S201 = Btrfs ioctl.c; :211 S202 = errno(3) man7; :218 S209 = alpm-hooks.5.asciidoc
  at 54d9411; :221 S212 = round-38 host hook capture — i.e. all four ids the staged entry
  cites are taken by other sources in the lane.
- `grep -E '^\| S2(1[3-9]|2[0-9]|3[0-9]) ' corpus/SOURCES.md` → no matches (run
  2026-10-26): S213 onward is free; the lane's highest S2xx row is S212.

## Rejections and prior lane state read

- `corpus/lessons/round-37.md:22` — `errno-name-discrimination-r25.md` "reject; no row
  appended … no explicit `## QUALITY check` required by QUALITY 14"; :74 "rejected for
  overlap plus absent explicit QUALITY check".
- `corpus/knowledge/boot-writers-r19.md:36-38` — W-MKINITCPIO-HOOK; :38 "[inf] The /etc
  copy is the operative one (S008; precedence per S007; pacman.conf HookDir not captured [unk])".
- `corpus/knowledge/pacnew-plane.md` — grep `hook|trigger|original` → no matches: the
  .pacnew-trigger-on-original-name fact is new to the lane.
- Coverage sweep (criterion 68 shape), grep
  `PreTransaction|AbortOnFail|NeedsTargets|alpm-hooks|install scriptlet|\.INSTALL` over
  `corpus/knowledge` + `SKILL.md` → hits only: boot-writers-r19.md (writer classes, S007/S008),
  degraded-triage-r4.md:61,:113 (vendor .INSTALL evidence), pacman-hook-order-r38.md (HO1-HO7),
  update-safety-note.md:239-242 (lock hook), SKILL.md:2026 (lock hook not-a-writer).
  No lane file holds: NeedsTargets semantics, the .pacnew trigger rule, the hook
  lifecycle, the old/new upgrade order, the scriptlet contract, or the Chinese five-step order.

## Sibling receipts reused (read-only, same day 2026-10-26)

- A-1 `w1/AsmS201Man.md` + `w1/AsmS201Man/` — staged S201 claims 5/5 present verbatim;
  defects D1 (id collision), D2 (anchor omits DESCRIPTION), D3 (overreach), D4
  ("non-overlapping complement" false vs lane S209/S210).
- A-2 `w1/AsmS202Devblog.md` + `w1/AsmS202Devblog/page.html` (sha256 `ea3085d7…`) —
  ordering-system quote verbatim but attributed to "the pacman maintainers" (absent from
  the page; authors David Runge and Arne Christian Beer); locator drift (quote lives in
  Notes for package maintainers › Documentation); upgrade order = one worked example;
  lifecycle headline is a strengthened paraphrase.
- A-3 `w1/AsmS209Scriptlet.md` + `w1/AsmS209Scriptlet/s209-alpm-install-scriptlet.5-2026-10-26.html`
  (sha256 `a18a5c60…`) — scriptlet claims 3/3 present; interpreter claim lives in
  General Format; "defined globally (e.g. per distribution)"; the upgrade-order claim is
  absent from S215; README.md:38-42 ground pointer does not resolve; PROVINCE placement Core.
