VERDICT: defect-found

# C2RevenStaged — Item C2-18: proposition map of the staged `pacman-hook-timing-r25.md` and of the round-38 review (C1–C9)

**Inputs (read-only).** Candidate: `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/pacman-hook-timing-r25.md`,
sha256 `e18c146e733d3cab4bcc82c2ba30b9a571791ec132f7988cd93481b079f09324` — byte-identical to the copy the
round-38 review judged (`AsmRevTiming.md:7`, same hash). Review: `.ufo/waves/round-38/w1/AsmRevTiming.md`
(corrections C1–C9 at `:156, :173, :200, :217, :223, :227, :237, :242, :248`). Target entries:
`corpus/knowledge/pacman-transaction-order-r39.md` (TO1–TO8, rules at `:22-29`, end-to-end order `:33-44`) and
`corpus/knowledge/pacman-hook-order-r38.md` (HO1–HO7 at `:21-27`, round-38 correction block `:111-152`). Pinned
sources read directly: `.ufo/waves/round-39/frozen/src/` (`SHA256SUMS` verified, `sha256sum -c` all OK) and the
round-38 doc snapshot `.ufo/waves/round-38/sources/alpm-hooks.5.asciidoc`; host evidence
`.ufo/waves/round-39/frozen/txcapture/` (`sha256sum -c MANIFEST.sha256` all OK). No lane file was edited; no git
command was run; no scratch clone was made; no tool was installed.

**Bottom line.** The candidate makes 25 propositions plus a four-cell header block. Disposition: **8 admitted**
(5 newly re-grounded at libalpm source in round 39, 3 already held at source by HO1/HO4/HO6), **4 corrected**,
**4 rejected**, **10 not carried**. No proposition of the candidate falsifies any TO or HO rule: reading the
snapshots myself, all eight TO rule texts are true at their cited lines, so the declared C2 kill rule
("any TO row judged FALSE against the pinned source at its cited lines") is **not** triggered. The defects found
are (a) four false or ungrounded propositions in the candidate, (b) the round-38 C1 renumber map is now stale
because round 39 spent S213–S218 on code and capture rows, (c) TO5's host cell is uninformative as worded and 7 of
its 17 instances are alternate-root transactions, (d) the round-39 entry cites a `corpus/lessons/round-39.md`
that does not exist at this revision. Details §7.

## 1. Proposition inventory (line numbers = the staged file)

| id | line | proposition |
|---|---|---|
| P0 | :2-:8 | header block: four source rows (ids S201/S202/S209/S212) with section anchors; `verified-at: 2026-10-23`; recheck cadence; ground = "the Arch packaging-and-hook-semantics frontier in `corpus/README.md:38-42`" |
| P1 | :16 | alpm hook = declarative `.hook` file in `/usr/share/libalpm/hooks` or a `HookDir` (default `/etc/pacman.d/hooks`); `When=` is PreTransaction or PostTransaction; **owner = the package that ships the file** |
| P2 | :17 | install scriptlet = `.INSTALL` shell functions at the package root; names `pre_install`/`pre_upgrade`/`pre_remove`/`post_install`/`post_upgrade`/`post_remove`; owner = the package being installed, upgraded or removed |
| P3 | :18 | mkinitcpio hook = an initramfs hook, runs in the initramfs not in a transaction; owner = the initramfs image; cites `corpus/knowledge/initramfs-hook-api-r25.md` |
| P4 | :22-:23 | hooks run in alphabetical order of file name, ignoring the suffix |
| P5 | :22, :23-:24 | "upstream says that is not a design"; "The pacman maintainers state plainly …" |
| P6 | :24-:26 | quote: distribution is *"missing a documented ordering system for alpm-hooks(5) … to establish ranges of number prefixes for specific tasks"* |
| P7 | :26-:27 | "there is no documented precedence scheme to appeal to — the filename is the only lever" |
| P8 | :29 | "A hook **exists** only while its providing package is installed" |
| P9 | :29-:32 | hooks are read from the target filesystem; a pre-transaction task is only available and run once the provider is installed; a post-transaction task only while the package remains installed |
| P10 | :32-:33 | that availability is "the answer to 'who is allowed to write this file' that the lane previously lacked" |
| P11 | :35-:37 | upgrade order: old version's PreTransaction hooks → new version's install-scriptlet functions → new version's PostTransaction hooks |
| P12 | :37-:39 | [unmarked inference] a writer observed after an upgrade may belong to the old version's hook or the new version's scriptlet; "the fact the lane's boot-writer attribution needs" |
| P13 | :41-:42 | `AbortOnFail` aborts the transaction on non-zero exit and is **PreTransaction only** |
| P14 | :42-:43 | `NeedsTargets` passes the matched trigger targets to the hook on **stdin** |
| P15 | :43-:44 | PostTransaction hooks do not run if the transaction fails to complete for any reason |
| P16 | :44-:45 | a file extracted with the `.pacnew` extension triggers the hook on the **original** file name |
| P17 | :47-:48 | `.INSTALL` functions execute in the system root (`/`), so every path inside them must be absolute |
| P18 | :48-:49 | `pre_upgrade`/`post_upgrade` take the **new** version first, the old version second |
| P19 | :49-:51 | the shell interpreter is chosen globally by the distribution and cannot be selected per package |
| P20 | :55 | the Chinese ArchWiki page states the same hook-directory contract |
| P21 | :56-:59 | "**five-step** transaction order" in Chinese, listed as six arrow-separated stages: Pre hooks → deletion of replaced packages → each package's `pre_install`/`pre_upgrade` → unpacking with `.pacnew` preservation → `post_install`/`post_upgrade` → Post hooks |
| P22 | :59-:61 | that is an **independent** confirmation of the Western order "in the Chinese literature", "the first time the lane can say so" |
| P23 | :61-:63 | tier B; community translation of `en:Pacman` rev 808924, 2024-05-22; not current Arch doctrine |
| P24 | :66-:67 | boundary: says nothing about whether a hook ran on this host |
| P25 | :68-:69 | boundary: does not resolve `errno:13`; points at `corpus/knowledge/errno-name-discrimination-r25.md` |

## 2. Map to the round-39 TO rows and the round-38 HO rows

Re-grounding readings are my own, from the frozen snapshots (line numbers verified by numbering the files:
`trans.c:201-244`, `add.c:455-695`, `sync.c:1336-1359`, `remove.c:690-733`, `util.c:505-535, 600-700`,
`hook.c:435-475, 505-575, 600-680`).

| id | disposition | TO/HO row | re-grounding (file:line) | note |
|---|---|---|---|---|
| P0 | **rejected as staged** | — | `corpus/SOURCES.md:210, :211, :218, :221` | all four ids collide with live rows (S201 Btrfs ioctl, S202 errno(3), S209 `alpm-hooks.5.asciidoc`, S212 round-38 capture); `verified-at: 2026-10-23` is stale; the ground line mislabels Core work as frontier (`PROVINCE.md:75-80` has no hook item; `corpus/README.md:38-42` holds the mkinitcpio-42 watch and the errno item) |
| P1 | **corrected** (owner cell); dirs and `When=` admitted | HO2, HO4, HO6 | dirs: `hook.c:540` walk, `alpm.c:56-62` (S211), asciidoc `:35-37`; `When=`: `hook.c:213-216` accepts exactly the two values; owner: `txcapture/hook-owners.tsv:69-70` | the owner cell "the package that ships the file" is incomplete: 2 of 70 captured files are owned by no package (`/etc/pacman.d/hooks/99-limine.hook`, `walker-restart.hook` → `-`). Round-38 C7 predicted this from an [unk]; the r39 capture now proves it |
| P2 | **admitted (new)** | TO3, TO4, TO7 | `add.c:467-474` (`"pre_upgrade"`/`"pre_install"`, `:470`), `add.c:638-647` (`"post_upgrade"`/`"post_install"`, `:642`), `remove.c:706-713` (`"pre_remove"`, `:711`), `remove.c:726-733` (`"post_remove"`, `:731`), dispatcher `trans.c:337-425` | all six names are string literals at those lines; the owner cell holds (`alpm_pkg_has_scriptlet(newpkg)` `add.c:468`, `oldpkg` `remove.c:707`) |
| P3 | **not carried** | — | `ls corpus/knowledge/` → only `initramfs-v42-sysroot-recovery.md` | the cited lane entry does not exist (r38 C6); the taxonomy row is out of the r39 entry's declared scope (between-phase order) |
| P4 | **admitted (held)** | HO1 | `hook.c:443-455` (`:449` comment, `:450` strncmp, `:451-452` tie-break), asciidoc `:38-39` | identical rule, HO1 is deeper (bytewise + shorter-name-first); r39 rightly does not restate it |
| P5 | **rejected** | HO1 | asciidoc `:38-39`; frozen `w1/AsmS202Devblog/page.html` | `grep` for `alphabet` in the frozen devblog page → **absent**; the page's authors are "David Runge , Arne Christian Beer" (offset 438), not "the pacman maintainers"; and "not a design" is contradicted by the documented order at asciidoc `:38-39` (see §3) |
| P6 | **corrected** | — (no lane row) | frozen `page.html` offset 22247; `.ufo/waves/round-38/w1/AsmS202Devblog/` | the quoted sentence is real and verbatim, but its attribution (maintainers) and locator (page heading) are wrong: the authors are Runge/Beer and the sentence sits under "Notes for package maintainers › Documentation". The document has **no** `corpus/SOURCES.md` row (`grep devblog corpus/SOURCES.md` → no match), so this proposition cannot be re-grounded this round |
| P7 | **rejected** | HO1, HO2 | asciidoc `:38-39` (order documented), `:98-100` (`OVERRIDING HOOKS`: same-name override, `/dev/null` disable), `hook.c:451-452` (tie-break), `:588-591` (first file wins) | "no documented precedence scheme" is false; "the filename is the only lever" is false — the man page documents both the order and the override, and S007/S211/HO2 hold HookDir precedence |
| P8 | **corrected** | TO5 | `hook.c:509-517` (`Depends` gate), `hook.c:532-560`, `trans.c:201-208`/`:232-239` | "exists" → "is a candidate phase": an operator file survives its author (2 files, `hook-owners.tsv:69-70`) and `Depends =` gates a hook whose package *is* installed. r39's TO5 states the corrected form ("is not a Pre candidate … is not a Post candidate") |
| P9 | **admitted (new)** | TO5 (+TO1) | `hook.c:532-560` (`opendir` `:554` inside the per-call dir loop `:540`), `trans.c:201-208` (Pre call), `:232-239` (Post call) | the staged sentence was about *availability*, and TO5 is exactly that at source; r39's Boundaries `:48-50` keep the "consistency, not proof" limit |
| P10 | **not carried** | — | round-38 coverage sweep (`AsmRevTiming.md:26-42`) | true when swept (no lane file held these semantics), but it is a coverage claim about round 38, not a rule; r39 states its own split (Ground `:7-13`) instead of the "who may write the file" framing |
| P11 | **admitted (new)** | TO1+TO5+TO3 (composite) | `trans.c:201-208`, `:232-239`; `hook.c:532-560`; `add.c:467-474`, `:638-647` | r39 states the same order as its end-to-end list, steps 2/5/8 (`pacman-transaction-order-r39.md:33-44`). Pre sees the old hook file (before extraction), Post sees the new one |
| P12 | **corrected** | TO5, TO8 | `util.c:521-528`; r38 C5 (`AsmRevTiming.md:223`) | the sentence was an unmarked inference; it also understates the difficulty — TO8 shows the `[ALPM-SCRIPTLET]` tag cannot separate hook from scriptlet output at all, so phase position alone does not attribute a line |
| P13 | **admitted (held)** | HO4 | `hook.c:660-662` (`abort_on_fail` → `ret = -1`), `:667-669` (break is Pre-only), `:141-143` (a Post hook with the key only warns), `trans.c:201-203`, `:237-239` | the man-page wording "Only applies to PreTransaction hooks" (`asciidoc:87-89`) is effect-level: the Post run's result is discarded and the Post loop never breaks |
| P14 | **not carried** | — | asciidoc `:91-93`; `hook.c:519-529` (feed callback as `stdin_cb`), `util.c:606-610` | no TO or HO row states target delivery. Re-groundable from documents already registered in part, but S209's anchor/scope cell names only DESCRIPTION `:34-39` and AbortOnFail `:87-89`, so `:91-93` needs a new row (next free **S219**), not an in-place scope edit (`corpus/lessons/round-38.md:25`) |
| P15 | **admitted (held)** | HO6 | `trans.c:212-228` (`transaction failed` + `return -1`), `:230-231` (interrupted), `:233-239` (Post only in the else branch), asciidoc `:131-132` | "for any reason" holds for every path that reaches the commit; r38's correction block adds that an interrupt returns 0 |
| P16 | **not carried** | — | asciidoc `:126-127`; `hook.c:266-279` (file triggers matched against `pkg->files`, the archive list) | the mechanism is source-true and the trigger list is never the on-disk name; no row states it. Same registry constraint as P14 (`:126-129` outside S209's declared anchor) |
| P17 | **not carried** (premised only) | TO8 (premise) | `trans.c:397-410` ("chop off the root … in the chroot"; `_alpm_run_chroot`), `util.c:677-683` (`chroot(root)` skipped when root is `/`, then `chdir("/")`) | TO8 says "in the chroot" as a premise but states no working-directory or absolute-path rule; the rule is re-groundable at the two lines above |
| P18 | **admitted (new)** | TO4 | `add.c:472-473` (`newpkg->version, oldpkg ? oldpkg->version : NULL`), `trans.c:400-406` (`"%s %s"` / `"%s %s %s"` → `$1`=new, `$2`=old, `$2` absent for installs) | TO4 is exactly this rule; the code shows the install case passes no second argument at all |
| P19 | **not carried** | — | `trans.c:357-358` (`strcpy(arg0, SCRIPTLET_SHELL); strcpy(arg1, "-c")`) | no row states interpreter selection; the code proves a single build-time shell for every scriptlet, which is stronger than the man page, but the document (staged S209) is unregistered |
| P20 | **not carried** | — | r38 receipt `w1/AsmS212CnWiki.md` | true as verified in round 38; the document has no lane row, is tier B, and the same contract is now held at source (`asciidoc:35-39`, HO2) |
| P21 | **admitted (new), count corrected, one stage not carried** | TO1, TO2, TO3, TO7 | `trans.c:201-208` (Pre before `started`), `sync.c:1340-1357` (removals before upgrades), `add.c:467-474`/`:599`/`:616-647` (per-package scriptlet/files/log/scriptlet), `trans.c:232-239` (Post after `completed`) | the stage sequence holds exactly; the enumeration has **six** items for five arrows, so "five-step" is a counting defect; the "unpacking with `.pacnew` preservation" stage is real in code (`add.c:318-350`) but no TO row states it |
| P22 | **rejected** (as "independent") | TO1–TO3 (superseding) | staged `:61-63` vs `:59-60`; r38 Gate `corpus/lessons/round-38.md:48` | self-contradictory: a page described two lines later as a translation of `en:Pacman` cannot independently confirm the English page it translates; and round 39 now holds the order at tier-A source, which makes the tier-B rendering redundant rather than confirmatory |
| P23 | **not carried** | — | r38 receipt `w1/AsmS212CnWiki.md` (translation template) | registry metadata for an unregistered, tier-B document; its suggested lane id S216 was taken by `util.c` (`corpus/SOURCES.md:225`) |
| P24 | **not carried** | — | `pacman-transaction-order-r39.md:48-50` | the r39 entry states its own boundaries (host presence, TO5 consistency-only, no live read); the candidate's disclaimer does not transfer |
| P25 | **not carried** (pointer dangles) | — | `corpus/knowledge/` has no `errno-name-discrimination-r25.md`; `corpus/lessons/round-37.md:22` (reject row) | the referenced entry was rejected in round 37; the lane's errno surfaces are `snapper-eacces-mechanism.md` and `errno-contract-variance-r37.md` |

## 3. Rejections — the contradicting line for each

1. **P5** ("upstream says that is not a design"; "the pacman maintainers"). No cited source says it: `grep alphabet`
   over the frozen devblog page → absent; byline "David Runge , Arne Christian Beer" (offset 438); the man page
   documents the order → `.ufo/waves/round-38/sources/alpm-hooks.5.asciidoc:38-39` "Hooks are run in alphabetical
   order of their file name, where the ordering ignores the suffix." The only true residue is P6's narrower
   sentence about a missing number-prefix range convention.
2. **P7** ("no documented precedence scheme … the filename is the only lever"). Contradicted three ways:
   `alpm-hooks.5.asciidoc:38-39` (order documented); `:98-100` "Hooks may be overridden by placing a file with the
   same name in a higher priority hook directory"; `hook.c:451-452` (the tie-break is the shorter name, not the
   full filename) — plus S007/S211 (HookDir precedence, HO2).
3. **P22** ("independent confirmation"). Contradicted by its own next sentence: the page "is a community
   translation" of `en:Pacman` (staged `:61-63`). Round 38 already recorded the failure
   (`corpus/lessons/round-38.md:48`), and TO1–TO3 now hold the same order at source.
4. **P0** (as staged). All four ids are live lane rows (`corpus/SOURCES.md:210, :211, :218, :221`); appending would
   re-bind S201/S202/S209/S212 and corrupt `mount-errno-contract-r37.md:3`, `errno-contract-variance-r37.md:2` and
   `pacman-hook-order-r38.md:1`. Id integrity is the ground of the rejection, not the content.

## 4. Corrections — exact shape

| id | corrected to | evidence |
|---|---|---|
| P1 (owner) | "the package that ships the file — or no package, for a file placed directly in a `HookDir`" | `hook-owners.tsv:69-70` (2 files, owner `-`) |
| P6 | quote retained, attributed to Runge/Beer under "Notes for package maintainers › Documentation", scoped to **number-prefix ranges** only | frozen `page.html` offsets 438, 22247 |
| P8 | "A hook is a Pre/Post candidate only while its providing package is installed (and only if `Depends =` is satisfied)" | `add.c`/`hook.c:509-517`, `hook.c:532-560` |
| P12 | mark `[inf]`; add that the `[ALPM-SCRIPTLET]` tag cannot separate a hook line from a scriptlet line | `util.c:521-528` (TO8) |
| P21 | "six stages", and the `.pacnew`-preservation stage must be cited or dropped | six arrow-separated items at staged `:56-59`; `add.c:318-350` for the stage itself |

## 5. Not carried — why, and where each could live

Ten propositions are neither admitted nor false; they are simply not in the r39 entry's scope and have no row:

- **P3** — initramfs taxonomy; referenced entry absent; different PROVINCE surface.
- **P10, P24** — coverage and scope statements, not rules; r39 has its own (`:7-13`, `:46-51`).
- **P14 (stdin targets), P16 (`.pacnew` trigger target), P17 (scriptlet cwd `/`), P19 (global shell)** — the four
  genuinely uncovered mechanism facts. Each is already re-groundable in the snapshots I read
  (`hook.c:519-529`, `hook.c:258-279`, `util.c:677-683` + `trans.c:397-410`, `trans.c:357-358`). Two of them
  (P14, P16) sit at `alpm-hooks.5.asciidoc:91-93` and `:126-129`, which S209's anchor/scope cell does not cover, so
  the registry cost is one new row each (next free **S219**), not an in-place edit.
- **P20, P23** — tier-B Chinese rendering; document unregistered; superseded at source.
- **P25** — dangling pointer to an entry round 37 rejected.

## 6. Review-of-review — what round 39 did with C1–C9

| correction | status | evidence |
|---|---|---|
| C1 renumber ids | **not applied as prescribed; now stale** | r38 proposed S213=man, S214=devblog, S215=install-scriptlet, S216=CN wiki. Round 39 spent S213–S218 on `add.c`/`sync.c`/`remove.c`/`util.c`/`trans.c`/capture (`corpus/SOURCES.md:222-227`). The general fix (fresh ids, by document) stands; the id map does not. Next free is **S219** |
| C2 add `## QUALITY check` | applied **to the new entry**, not to the candidate | `pacman-transaction-order-r39.md:53-56` |
| C3 rewrite `:22-27` | **not applied — superseded**: the two sentences were dropped, not rewritten | the r39 entry's Ground (`:7-13`) states the within-phase/between-phase split instead; rejection recorded at `corpus/lessons/round-38.md:48` |
| C4 fix header anchors | moot for the candidate; **partially inherited** | the new entry's source line cites code files with line ranges; but no lane row carries the devblog, so its quote (P6) has no anchor of record |
| C5 mark inference, weaken lifecycle headline | **applied in substance** | TO5's "is not a Pre candidate/is not a Post candidate" is the availability form C5 asked for; the candidate's attribution inference is not carried at all |
| C6 repoint dangling references | applied for the two old refs; **one new forward reference remains** | r39 cites `corpus/lessons/round-39.md` Gate (`pacman-transaction-order-r39.md:15-18`) and that file does not exist yet (`ls corpus/lessons/` → up to `round-38.md`). Integration-time obligation, not a content defect |
| C7 ownership precision | **satisfied in evidence, unstated in any row** | `hook-owners.tsv:69-70` proves the r38 [unk]; no r39 row carries the ownership cell — the corrected proposition has no home (see §5) |
| C8 registry scope text | n/a | r39 opened different rows; S208/S209's own scope cells are unchanged |
| C9 refresh + cross-reference | **applied** | `verified-at: 2026-10-26` (`:2`); Ground `:7-13` cross-references `pacman-hook-order-r38.md` for within-phase order |

## 7. Findings (defects, not inferences)

1. **Four false/ungrounded candidate propositions** (P5, P7, P22, and P0's id binding). The candidate remains
   non-admittable as a unit for exactly the round-38 reason; nothing in this round changes that.
2. **The r38 C1 renumber map is dead.** Any future adoption must append at S219+, and the four staged documents
   (man page, devblog, install-scriptlet page, CN wiki) still have **no** lane row. Round 39 re-grounded in code
   instead of the registry, so the four doc-tier propositions (P6, P14, P16, P19) cannot be cited from a `source:`
   line today.
3. **TO5's host cell is uninformative as worded, and 7 of its 17 instances are uninformative in fact.** The cell
   says the 17 Pre hooks are "owned by a package that the capture shows first installed in some transaction" —
   every package in a pacman.log was first installed in *some* transaction, so that clause carries no information.
   Read as "the owner's first-ever-install window", it reproduces 17/17 (no Pre hook ran in its owner's
   first-install window — my own derivation, `.ufo/waves/round-39/w1/C2RevenStaged/receipts.md` §3), **but** 7 of
   those windows are alternate-root transactions (`-r /mnt` or `-b /mnt`, e.g. `10-glibc-remove-locale-archive.hook`,
   `60-mkinitcpio-remove.hook`), where libalpm reads `/mnt`'s hook directories, not the host's. The informative
   count is **10**, and the cell should say so; the rule is unaffected (TO5 verdict below is `partly` for the cell,
   `holds` for the rule).
4. **Forward reference to `corpus/lessons/round-39.md`** (`pacman-transaction-order-r39.md:15-18`) — the file must
   exist when the round closes; at this revision it does not.
5. **TO7's host cell is circular**: "`removed` lines appear only for whole-package removals, never for upgrades" is
   read off the log that the rule itself explains; it is a consistency statement, like TO5's, and the entry's
   Boundaries say so only for TO5 (`:49-50`).

No rule text of TO1–TO8 or HO1–HO7 is false at its cited lines under my reading, so C2's kill rule does not fire.

## 8. Draft — lesson Gate assimilation table (`corpus/lessons/round-39.md` § Gate)

Proposed exact text (append under the round-39 Gate, after the admitted-knowledge list):

```markdown
### Assimilation (theme: pacman hook timing, `merge/tsukuroi/`) — core re-grounded, interpretive sentences rejected

Candidate `pacman-hook-timing-r25.md` (sha256 `e18c146e733d3cab4bcc82c2ba30b9a571791ec132f7988cd93481b079f09324`,
the same bytes round 38 refused). Round 39's depth entry re-grounds its transaction-order propositions in libalpm at
`54d9411`; the per-proposition map (26 rows) is `.ufo/waves/round-39/w1/C2RevenStaged.md` §2.

| Candidate / proposition set | Decision | Reason; flip condition |
|---|---|---|
| `pacman-hook-timing-r25.md` — transaction-order core (staged `:17`, `:29-37`, `:48-49`, `:56-59`) | admit, as re-grounded by `pacman-transaction-order-r39.md` TO1–TO7 | Every stage is now read from the installed commit: Pre before `transaction started` (`trans.c:201-208`), removals before adds (`sync.c:1340-1357`), per-package pre-scriptlet → files → log line → post-scriptlet (`add.c:467-474`, `:599`, `:616-647`), new-version-first arguments (`add.c:472-473`, `trans.c:400-406`), removal order (`remove.c:690-733`), one `ldconfig` (`add.c:677-692`). The candidate's own document ids are not carried, so no staged id binds a lane row. Flip: a staged re-issue that cites these TO rows by document instead of restating them. |
| — owner cell (staged `:16`) | admit-with-correction | "the package that ships the file" is incomplete: 2 of the 70 captured hook files are owned by no package (`.ufo/waves/round-39/frozen/txcapture/hook-owners.tsv:69-70`); the cell must read "the package that ships the file, or no package for an operator-placed file". Flip: an ownership capture in which every hook file is package-owned. |
| — availability headline (staged `:29`) | admit-with-correction | "exists only while its providing package is installed" is an availability window, not existence: `Depends =` gates execution independently (`hook.c:509-517`) and an operator file outlives any author; TO5 already states the corrected form. Flip: not available — the "existence" form is contradicted by the two unowned files. |
| — interpretive sentences (staged `:22`, `:26-27`) | reject | "upstream says that is not a design" has no source (`grep alphabet` over the frozen devblog page → absent; byline David Runge / Arne Christian Beer), and the order *is* documented (`.ufo/waves/round-38/sources/alpm-hooks.5.asciidoc:38-39`); "no documented precedence scheme … the filename is the only lever" is contradicted by that line, by `OVERRIDING HOOKS` (`:98-100`) and by HO1's tie-break (`hook.c:451-452`). Flip: a source sentence stating that no ordering rule and no override mechanism exist. |
| — "independent confirmation" sentence (staged `:59-61`) | reject | A page the entry itself calls a translation of `en:Pacman` (staged `:61-63`) cannot independently confirm the English page it translates, and the order is now held at tier-A source (TO1–TO3), which makes the tier-B rendering redundant. Flip: an independent tier-A text in another language stating the same order at its own anchor. |
| — residual mechanism propositions: `NeedsTargets`→stdin (`:42-43`), `.pacnew` trigger target (`:44-45`), scriptlet cwd `/` (`:47-48`), global interpreter (`:49-51`) | not carried — defer, no decision on the candidate | No TO or HO row states them; each is re-groundable in the pinned snapshots (`hook.c:519-529`, `hook.c:258-279`, `util.c:677-683` with `trans.c:397-410`, `trans.c:357-358`). `alpm-hooks.5.asciidoc:91-93` and `:126-129` lie outside S209's declared anchor/scope cell, so stating them needs new rows (next free S219), not an in-place edit. Flip: a round-40 entry, or an appended section in r39, that states each with its line. |

Assimilation result: the candidate is admitted **by re-grounding, not as a document** — no staged row, no staged id,
no staged text enters the corpus.
```

If the Gate must keep the round-38 one-row-per-candidate shape instead, the equivalent single row is:
`| pacman-hook-timing-r25.md | admit by re-grounding; reject its interpretive sentences | … |` with the three
admit/reject reason cells above merged — but the six-row form records the discernment and is the one I recommend.

## 9. What I did not do

- I did not run the frozen counters (`tools/check-transaction-order-r39.py`, `tools/check-hook-order-r38.py`); I
  judged the TO/HO rule texts against the snapshots myself. Their predicates are other seats' scope.
- I did not fetch the devblog, the man pages or the CN wiki live: P6/P5 rest on the round-38 frozen page
  (`w1/AsmS202Devblog/page.html`, my own `grep`, offsets quoted) and on the round-38 asciidoc snapshot. A live
  re-open of the man page could change wording, not the assertions I judged.
- I did not re-measure the CN revision id (staged P23) — nothing in my map turns on it.
- I ran no git/jj command, edited no lane file, created no scratch clone, installed no tool. Scratch: none created,
  so nothing to remove; receipts are in `.ufo/waves/round-39/w1/C2RevenStaged/receipts.md`.

Judged rows (rule text at the cited lines; `partly` = rule holds, host cell qualified — no rule text is false, so
C2's kill rule does not fire):

TO1: holds — trans.c:201-208, 232-239
TO2: holds — sync.c:1336-1356
TO3: holds — add.c:466-474, 616-648
TO4: holds — add.c:470-474
TO5: partly — hook.c:532-560
TO6: holds — add.c:676-692
TO7: holds — remove.c:699-733
TO8: holds — util.c:521-528
