VERDICT: defect-found

Item A-4 — staged S212 re-open (Chinese ArchWiki "Pacman"). Seat AsmS212CnWiki, read-only; no lane file touched, no host mutation. Receipts: `.ufo/waves/round-38/w1/AsmS212CnWiki/` (`SHA256SUMS` lists them). Access time: 2026-10-26T05:04:59Z (first fetch) to about 05:10Z.

Summary: the revision id and date hold, and the hook-directory contract and the transaction order are both on the page as staged. The staged row and entry mis-describe the "five steps", the "independent confirmation" claim fails, and the heading anchor is paraphrased. PROVINCE.md and QUALITY.md say nothing about source language.

## 1. Revision: staged row confirmed current

| fact | observed | where |
|---|---|---|
| staged row | S212, `https://wiki.archlinuxcn.org/wiki/Pacman`, "revision 34634, last edited 2025-12-14, translation source en:Pacman rev 808924 dated 2024-05-22" | `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md:19` |
| current revid | 34634, still the newest. `wgRevisionId`, `wgCurRevisionId` = 34634, `wgPageContentLanguage` = "zh", `wgPageName` = "Pacman" | rendered HTML `zh-Pacman-rendered-2026-10-26.html` (sha256 2c50329e…) |
| revision metadata | MediaWiki API `prop=revisions&rvlimit=5` first row: `revid 34634, parentid 33537, user Tjw123hh, timestamp 2025-12-14T00:48:14Z, comment "/* 在安装时跳过文件 */"` | `zh-revisions-api.json` (sha256 72b5cd5b…) |
| footer | "最后编辑于2025年12月14日 (星期日) 08:48。" This is local time UTC+8, the same instant as 00:48 UTC. | rendered HTML |
| translation provenance | wikitext line 5: `{{翻译状态\|pacman\|2024-05-22\|808924}}`, translation date 2024-05-22, English upstream revision 808924 | `zh-Pacman-rev34634.wikitext:5` (sha256 c831e789…) |

Two small precision points:
- The English upstream revision 808924 is stamped 2024-05-21T14:37:01Z by the English wiki API (`https://wiki.archlinux.org/api.php?action=query&prop=revisions&revids=808924`). The staged "dated 2024-05-22" is the Chinese translation-status template date, not the English revision's own timestamp. The row is right as long as it says "translation date".
- English `Pacman` has moved on. The newest revision at query time was 888786 (2026-10-26T01:26:14Z). The Chinese page is therefore 2.4 years behind. For the two sections the entry uses, that lag is cosmetic (§3).

## 2. Locating the two contracts (sections, Chinese, translation)

Section numbers come from `api.php?action=parse&page=Pacman&prop=sections` (`zh-sections-api.json`). Wikitext line numbers are in `zh-Pacman-rev34634.wikitext`.

### 2a. Hook-directory contract: §2.4 钩子, under §2 配置. Wikitext lines 438-444.

> "更多的hooks文件夹可以通过{{ic|HookDir}}选项在{{ic|pacman.conf}}中指明，默认{{ic|/etc/pacman.d/hooks}}。"

Translation: further hook directories can be named through the `HookDir` option in `pacman.conf`; the default is `/etc/pacman.d/hooks`.

Also on line 440:

> "''pacman''可以在处理前后，运行{{ic|/usr/share/libalpm/hooks/}}文件夹下的hooks" … "Hook文件必须以''.hook''为后缀。Pacman hooks不是交互式的。"

Translation: pacman can run, before and after processing, the hooks under `/usr/share/libalpm/hooks/`. Hook files must carry the `.hook` suffix. Pacman hooks are not interactive.

What the section does **not** state, searched in the full wikitext (`grep -n -E "钩子|hook"`, lines 251, 351, 358, 365, 438-444 only):
- It gives no run order (alphabetical, suffix-ignoring).
- It gives no override or precedence rule for a same-name hook.
- It does not say that `AbortOnFail` is PreTransaction-only.

Those come from the lane's tier-A rows (S208 hook.c, S209 alpm-hooks(5), S211 alpm.c). The Chinese page is therefore a directory-list and suffix statement only.

### 2b. Five-step transaction order: §1.9 安装/更新/删除 软件包时发生了什么, under §1 用法. Wikitext lines 349-366.

The lead sentence, line 351:

> "动作成功执行时，事务包含五大步骤和事务钩子程序:"

Translation: when the action succeeds, the transaction consists of five major steps and the transaction hooks.

The five top-level items, lines 353-356 and 366:
1. 如果数据库未被锁定，初始化事务 (initialize the transaction if the database is not locked)
2. 确认事务中要添加或删除的软件包 (confirm which packages are added or removed)
3. 准备事务，根据参数，对同步数据库、软件包和依赖关系进行校验 (prepare; validate sync databases, packages, dependencies)
4. 提交事务: (commit the transaction)
5. 释放事务及事务资源 (例如，数据库锁) (release the transaction and its resources, e.g. the database lock)

The hook and scriptlet order is the sub-list of step 4 (lines 357-365):

| # | Chinese | translation |
|---|---|---|
| 4.1 | 如果需要，下载软件包 (`_alpm_sync_load`) | download packages if needed |
| 4.2 | 如果有可以执行的 pacman `PreTransaction` 钩子，执行这些钩子. | run applicable PreTransaction hooks |
| 4.3 | 被替换、出现冲突或被指定删除的软件包将会被删除 | replaced, conflicting or explicitly targeted packages are removed |
| 4.4 | 如果需要添加软件包，每个软件包都会执行提交 | each package to add is committed: |
| 4.4.1 | 如果有安装脚本，执行 `pre_install` 函数(更新时执行 `pre_upgrade`，删除时执行 `pre_remove`). | run the install script's pre_install (pre_upgrade on update, pre_remove on removal) |
| 4.4.2 | pacman 删除软件包之前版本的所有文件 … 配置文件将会被保留 | delete files of the previous version; config files kept |
| 4.4.3 | pacman 将软件包文件解压到系统 … 会覆盖旧的已被手动修改的配置文件时，配置文件会命名为 (.pacnew). | unpack into the system; files that would overwrite modified config files become `.pacnew` |
| 4.4.4 | 如果软件包有安装脚本，执行 `post_install` 函数(更新时执行 `post_upgrade`，删除时执行 `post_remove`). | run post_install / post_upgrade / post_remove |
| 4.5 | 如果 pacman `PostTransaction` 钩子可执行，执行这些钩子. | run applicable PostTransaction hooks |

Source cross-check I ran, not a claim from the staged material. The Chinese order matches libalpm at pinned commit 54d9411:
- `trans.c` (lane snapshot `.ufo/waves/round-38/sources/trans.c`): `_alpm_sync_load` at line 188, `_alpm_hook_run(PRE_TRANSACTION)` at lines 201-204, `_alpm_sync_commit` or `_alpm_remove_packages`, then `_alpm_hook_run(POST_TRANSACTION)` at lines 235-238, only after "transaction completed".
- `sync.c` (fetched `https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/sync.c`, sha256 6b297364…): `_alpm_remove_packages` at line 1345, then `_alpm_upgrade_packages` at line 1354.
- `add.c` (same pin, sha256 fd313629…): `_alpm_runscriptlet` at line 472 (pre), `_alpm_remove_single_package` at line 485, `extract_single_file` at line 560 (with the `.pacnew` logic at lines 318-350), `_alpm_runscriptlet` at line 644 (post).

I did not run pacman, and I did not review `_alpm_sync_check`. It runs between download and PreTransaction (`trans.c` line 195) and the page omits it.

## 3. Defects in the staged material

**D1. The "five steps" are mislabelled. [observed]**
- The staged row says "the five-step transaction order with PreTransaction and PostTransaction hooks interleaved with the install-scriptlet functions."
- The staged entry says the page "gives the **five-step transaction order** in Chinese — PreTransaction hooks → deletion of replaced packages → each package's pre_install/pre_upgrade → unpacking … → post_install/post_upgrade → PostTransaction hooks." That is not what the page's five steps are.
- The five steps are init, choose, prepare, commit, release. The hook-to-hook sequence is the nested sub-list of step 4. It has at least six links (more with the per-package sub-steps), and the staged text drops the download step.
- Fix: say "the page's five high-level steps; PreTransaction hooks, removals, per-package scriptlets and PostTransaction hooks are the sub-list of step 4 (commit)".

**D2. "Independent confirmation … first time the lane can say so" does not hold. [observed]**
- The page is a translation of English rev 808924 (§1). I diffed the two English sections I could get against the Chinese structure.
- English 808924 and the current English differ in these two sections only by trailing full stops, `Pacman` → `''pacman''` emphasis, `(.pacnew)` → `(''.pacnew'')` and `{{Pkg|tomcat8}}` → `{{AUR|tomcat8}}`. See `en-808924-vs-current-sections.diff` (43 lines). The Chinese page still carries `{{Pkg|tomcat8}}` (line 442), the 808924 wording, so the lag shows there.
- The transaction list is item-for-item identical to English in meaning. A translation of one document is one witness, not two, so it adds nothing beyond the English wiki. The tier-A source (libalpm code, S208/S210) is where the order is established.
- The staged entry's own caveat that this is "tier B and not current Arch doctrine" is right on tier, but wrong on staleness for these two sections: they are semantically current as of English 888786.

**D3. Heading anchor is not exact. [observed]**
- The staged anchor reads "疑难解答（升级系统重启后出现 unable to find root device 错误）". The real heading is §3.7 `升级系统重启后，出现"unable to find root device"错误，无法登录` under §3 疑难解答 (`zh-sections-api.json`; wikitext line 575).
- QUALITY 23 and 21 require the exact heading and quote. This section is also not used by the staged teaches text, which cites only §2.4 and §1.9.
- The anchor also gives no section numbers. The numbers are §2.4, §1.9 and §3.7.

**D4. Minor: staged `kind` is `docs`. [inference]**
- Other rows with the same standing, such as S161 (ArchWiki Btrfs), also use `docs`. CORPUS.md allows `community`, and says `community` is never A. The tier is B, which is allowed. I did not judge `kind` further.

## 4. Scope: is a Chinese community rendering in scope for this lane? Judged against `PROVINCE.md`

Observed:
- `PROVINCE.md` scopes the lane by **host surface**, not by source language. Core is "package state … systemd … journal/boot triage … driver/firmware", and the update-safety questions (`PROVINCE.md:3-14`). Refuses: endpoint serving, secrets, binary RE, installs/restarts (`:25-28`).
- A grep of `PROVINCE.md`, `corpus/QUALITY.md`, `corpus/README.md` and `/home/vgpnk/Projects/shokunin/CORPUS.md` for `chinese|中文|zh-|CJK|language|non-English|translation` returned **no match** in any of them. A grep of `corpus/SOURCES.md` for CJK characters returned count 0 (the lane has no non-English source today). There is no rule for or against localized sources.
- Sibling precedent:
  - `mado-shokunin/PROVINCE.md:68-78` (a round-36 refinement) rules the Chinese/Japanese ArchWiki channel "outside the province" for **its** desktop plane, and keeps English upstream docs admissible. This is mado's own refusal. It does not bind tsukuroi, and it is about desktop documentation artifacts.
  - `kotoba-shokunin/PROVINCE.md:31` and `kasegi-shokunin/PROVINCE.md:74` both name Chinese-language scope, but for their own domains.
  - So the question is open here, not settled. The nearest owner of the channel as a documentation artifact is mado's declared refusal. tsukuroi has no equivalent line.

Judgment [inference]:
- **The topic is in scope.** Hook directories and transaction order sit on the lane's Core pacman-state and update-safety surfaces. `corpus/knowledge/pacman-hook-order-r38.md` already owns the host's hook order from tier-A source.
- **The Chinese rendering is a channel question, not a surface.** It teaches no host fact. It does not make the topic any more or less in scope. Admitting it as a source is a QUALITY and SOURCES decision; PROVINCE.md neither grants nor refuses it.
- The staged entry's ground claim also does not resolve. It cites `corpus/README.md:38-42` as "the Arch packaging-and-hook-semantics frontier". Those lines (36-44) cover the mkinitcpio 42 watch and the `errno:13` item. A grep for "packaging-and-hook" in `PROVINCE.md`, `SKILL.md` and `corpus/README.md` returned no match. The "frontier" named in the staged row and entry is not a declared area in this lane's province; it is the staging campaign's label.
- The staged "zero-Chinese-source gap" is factually true (0 CJK characters in SOURCES.md). A gap in language coverage is not a province gap.
- Recommended proposal for the integrator, if the lane wants a rule: add one append-only line to `PROVINCE.md` stating that source language is not a surface boundary, and that a localized rendering is admissible only as a derivative with its upstream revision named. I did not edit anything. Mado's refusal should be recorded as a sibling position and not copied.

## 5. Quality: can a tier-B community translation support an admitted entry? Judged against `corpus/QUALITY.md`

Observed:
- QUALITY 7 (`QUALITY.md:11`): "tier C is never sole support, with tier definitions in SOURCES.md". Tier B is not barred from supporting an entry.
- CORPUS.md tier definitions (`/home/vgpnk/Projects/shokunin/CORPUS.md:93-97`): A = primary or authoritative; B = "strong secondary (expert write-up with reproducible detail, survey, textbook)"; C = lead only. `community` is never A.
- QUALITY 19 and 21 require a named source object, a located ≤25-word quote, the exact proposition and an observed revision. QUALITY 23 requires the exact heading and the quoted row resolved at the cited revision.
- A search of `QUALITY.md` (grep for `independen|mirror|derivative|translat|secondary|sole support|tier B|stale|oldid`) found **no** criterion on translations, mirrors, or derivative-source independence. The only `independen` hits are about gate code (criteria 28, 41). The lane's only tier-B ArchWiki row, S023 (Snapper), is tier B for a different reason, a disputed section.

Verdict [inference]: **yes, tier B can support an admitted entry, but only for the narrow proposition it makes, and not as corroboration.**
1. It meets QUALITY 7, 19, 21 and 23 mechanically. The revision is pinned (34634), headings resolve (§2.4, §1.9), and located quotes exist (§2).
2. It cannot support the entry's headline: "independent confirmation of the Western order in the Chinese literature". That claim is false by D2. A translation of English rev 808924 is the English wiki again, so the proposition needs no Chinese row.
3. For the load-bearing claim (what runs when on a transaction), tier A is already in the lane: S208, S209, S210, S211 plus `trans.c`, `sync.c` and `add.c` as read above. The Chinese row would only restate, so it is redundant on the claim.
4. The defensible admitted use: "the Chinese ArchWiki rendering at rev 34634 translates `en:Pacman` rev 808924 (template date 2024-05-22) and its two sections match English at 888786 in meaning". That is a provenance and translation-currency statement, and it needs the diff receipts here.
5. QUALITY gap: nothing stops a later entry from counting a translation as a second witness. Propose, without adding it myself, a criterion: "a translation or mirror of a cited source is not independent corroboration; cite it only for its own provenance or for the localization question, and name the upstream revision it renders."

## 6. Not done, and limits
- I did not open the Chinese page from a second mirror or from Wayback. `aw.lilydjwg.me` (staged S237) was not re-opened.
- I did not check whether English `Pacman` rev 808924 differs from current anywhere outside the two sections used. Only §1.9 and §2.4 (English headings "What happens during package install/upgrade/removal" and "Hooks") were diffed.
- I did not check the third staged section (§3.7) for content, only its exact heading.
- I did not run any pacman or host-state command, and did not edit `SOURCES.md` or `PROVINCE.md`.
- The staged knowledge entry (`pacman-hook-timing-r25.md`) has other claims on rows S201, S202 and S209 that belong to item A-1, not to this seat.
- No tools were installed. `curl` and `python3` were already present.

## 7. Exact proposed text

Corrected staged-row anchor (replaces the anchor cell of S212): `§1.9 安装/更新/删除 软件包时发生了什么 (step 4 sub-list); §2.4 钩子 (under §2 配置) — MediaWiki revision 34634, last edited 2025-12-14T00:48:14Z, translation status template {{翻译状态|pacman|2024-05-22|808924}} (English upstream rev 808924, English revision timestamp 2024-05-21T14:37:01Z); §3.7 omitted from the claim`.

Corrected sentence for the entry's "The Chinese rendering" section: "The Chinese ArchWiki page `Pacman` (revision 34634) renders English `Pacman` revision 808924. Its §2.4 names `/usr/share/libalpm/hooks/` and `HookDir` (default `/etc/pacman.d/hooks`), and its §1.9 lists five high-level transaction steps; PreTransaction hooks, replaced-package removal, per-package install scriptlets and PostTransaction hooks are the sub-list of step 4 (commit). For these two sections the English text is unchanged in meaning at revision 888786. The Chinese page is a translation of the English one, not an independent source; the order is established by libalpm (`trans.c`, `sync.c`, `add.c` at 54d9411)."
