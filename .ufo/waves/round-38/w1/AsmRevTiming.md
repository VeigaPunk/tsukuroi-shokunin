VERDICT: defect-found

# AsmRevTiming — Item A-5: gate review of staged `pacman-hook-timing-r25.md`

Candidate bytes (corpus/QUALITY.md criterion 38): reviewed
`/home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/pacman-hook-timing-r25.md`,
sha256 `e18c146e733d3cab4bcc82c2ba30b9a571791ec132f7988cd93481b079f09324` (sha256sum,
2026-10-26; receipts `w1/AsmRevTiming/receipts.md`). Lane read at HEAD
`5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf` (`git rev-parse HEAD`, read-only). The lane's
own entry `corpus/knowledge/pacman-hook-order-r38.md` read at sha256
`b56c90f1ebbdfa3d07f369e39b7580d6b0050da69eb9d4d2b560b58771c73f61`.

**Recommendation: ADMIT-WITH-CORRECTIONS** (exact corrections C1–C9 below).

Reasons in one paragraph: every content claim of the entry that any seat re-opened is
present in its source — staged S201 claims 5/5 verbatim (A-1), staged S202 quotes
verbatim (A-2), staged S209 claims 3/3 (A-3), and staged S212's three claims verified by
this seat today against the live page and its raw wikitext — and the mechanism claims are
code-true at the lane's pinned pacman 54d9411 (HO1/HO4/HO6). The entry adds six
propositions the lane does not hold (sweep below). It is **not admittable as staged**: its
four source ids collide with live lane registry rows, it lacks the `## QUALITY check`
section QUALITY 14 requires before any admit, one paragraph contradicts the lane's own
source-level reading, three internal references dangle (one points at an entry round 37
rejected), and two header anchors do not hold the claims they are cited for.

## 1. Coverage sweep — what the entry adds (criterion 68)

QUALITY 68: *"a declaration that calls ground new, uncovered or frontier names the sweep
command over `corpus/knowledge`, `SKILL.md`, `PROVINCE.md` and `corpus/README.md` and its
output; existing coverage makes the claim 'deeper ground' or a supersession instead."*

Sweep run 2026-10-26: grep `PreTransaction|AbortOnFail|NeedsTargets|alpm-hooks|install
scriptlet|\.INSTALL` over `corpus/knowledge` + `SKILL.md` → hits only in
`boot-writers-r19.md` (writer classes, S007/S008), `degraded-triage-r4.md:61,:113` (vendor
`.INSTALL` as drift evidence), `pacman-hook-order-r38.md` (HO1–HO7), `update-safety-note.md:239-242`
(lock hook), `SKILL.md:2026`. `pacnew-plane.md` grep `hook|trigger|original` → no matches.
Output: **no lane file holds** the NeedsTargets→stdin semantics, the
.pacnew-triggers-on-original-name rule, the hook lifecycle (availability bound to the
providing package), the old→new upgrade order, the `.INSTALL` scriptlet contract, or the
Chinese five-step order. The entry's coverage claims ("the answer … the lane previously
lacked", :32-33; "the first time the lane can say so", :60-61) are true per this sweep.
The entry is complementary to, not redundant with, the lane's corpus.

## 2. Claim verification (all line anchors = staged entry unless stated)

| # | staged claim | source | verdict | evidence |
|---|---|---|---|---|
| 1 | hooks run alphabetically, suffix ignored (:22-23) | S213 (staged S201) DESCRIPTION | present verbatim | frozen `.ufo/waves/round-38/sources/alpm-hooks.5.asciidoc:38-39` "Hooks are run in alphabetical order of their file name, where the ordering ignores the suffix."; A-1 raw roff :52 |
| 2 | hook dirs + HookDir default /etc/pacman.d/hooks (:16) | S213 DESCRIPTION | present | asciidoc :35-37; A-1 raw :52 |
| 3 | When= required (:16) | S213 ACTIONS | present | asciidoc :20, :80-81 |
| 4 | AbortOnFail aborts on non-zero, PreTransaction only (:41-42) | S213 ACTIONS | present; code-true | asciidoc :23, :87-89; lane HO4 (`hook.c:660-669`) |
| 5 | NeedsTargets passes targets on stdin (:42-43) | S213 ACTIONS | present | asciidoc :91-93; new to the lane (r38 entry has only the count, `pacman-hook-order-r38.md:14`) |
| 6 | PostTransaction hooks do not run if the transaction fails (:43-44) | S213 CAVEATS | present; code-true | asciidoc :131-132; `trans.c:212-240` — post-hook run only after "transaction completed" (read 2026-10-26); lane HO6 |
| 7 | .pacnew extraction triggers on the original name (:44-45) | S213 CAVEATS | present | asciidoc :126-127; new to the lane (pacnew-plane.md grep: no matches) |
| 8 | lifecycle: pre-tasks available once provider installed; post-tasks while it remains (:29-32) | S214 (staged S202) Hooks bullets | present, near-verbatim | A-2 offsets 6922/~7022; headline :29 is a strengthened merge (defect, C5) |
| 9 | upgrade order: old pre-hooks → new scriptlets → new post-hooks (:35-37) | S214 Upgrading the package | present, one worked example | A-2 offset 20318 quote + the page's own pacman output; not stated as a general rule (C5) |
| 10 | "missing a documented ordering system … number prefixes" quote (:24-26) | S214 Notes for package maintainers › Documentation | present verbatim; **attribution drift** | A-2: authors are David Runge and Arne Christian Beer; the phrase "pacman maintainers" is ABSENT from the page (C3) |
| 11 | scriptlet functions run in `/`, paths absolute (:47-48) | S215 (staged S209) DESCRIPTION lead-in | present | A-3: "The shell functions are executed in the root (/) of the system, so all paths inside of it must be absolute." |
| 12 | pre_upgrade/post_upgrade take new then old (:48-49) | S215 Functions | present | A-3 quote |
| 13 | interpreter global, not per-package (:49-51) | S215 General Format | present; staged wording tighter | A-3: "defined globally (e.g. per distribution)"; "cannot be changed on a per-package basis" (C4) |
| 14 | Chinese page states the hook-directory contract (:55) | S216 (staged S212) 钩子 | present | raw wikitext :446 (fetched 2026-10-26) |
| 15 | Chinese five-step transaction order (:55-58) | S216 安装/更新/删除 软件包时发生了什么 | present | raw wikitext :355-… ; rendered :525-534 (receipts) |
| 16 | translation source en:Pacman rev 808924, 2024-05-22 (:59-60) | S216 | present | raw wikitext :5 `{{翻译状态\|pacman\|2024-05-22\|808924}}` |
| 17 | "upstream says that is not a design" (:22) | — | **in no cited source** | A-2: "alphabet" ABSENT from S202; neither source says it (C3) |
| 18 | "no documented precedence scheme … the filename is the only lever" (:26-27) | — | **contradicted by the lane's own sources** | alpm-hooks(5) documents the alphabetical rule (asciidoc :38-39); S007 documents HookDir precedence; S008 documents same-name override; HO1 adds the tie-break (C3) |
| 19 | "a writer observed after an upgrade may belong to the old version's hook or the new version's scriptlet" (:38-39) | — | entry's inference, unmarked | A-2: "the entry's inference for the lane's use, not blog text" (C5) |
| 20 | alpm-hook owner = "the package that ships the file" (:16) | — | incomplete | r38 capture: 3 files in `/etc/pacman.d/hooks/`; `99-limine.hook` owner [unk] (`boot-writers-r19.md:46`); `walker-restart.hook` execs a user-home script (`pacman-hook-order-r38.md` table row 52) (C7) |

## 3. QUALITY.md criteria — the ones that decide

- **Criterion 14 (decisive, blocker):** *"Before recording an admit for a new knowledge
  entry, require its explicit `## QUALITY check` to evaluate the applicable numbered
  criteria and resolve its source/evidence pointers; a promised check is not a performed
  check."* The staged entry has no `## QUALITY check` section (headings at :12, :20, :53,
  :65 only; file ends :71). Round-37 precedent is on point: `corpus/lessons/round-37.md:22`
  rejected `errno-name-discrimination-r25.md` inter alia for "no explicit `## QUALITY
  check` required by QUALITY 14", and :74 repeats "rejected for overlap plus absent
  explicit QUALITY check". The staged entry shares that defect → C2.
- **Criterion 7 (decisive, blocker):** *"External claims cite an exact `corpus/SOURCES.md`
  S### row, its tier and applicable section anchor; … tier C is never sole support."* All
  four cited ids collide with live lane rows (C1); the anchors are wrong or incomplete for
  three of the four sources (C4). Tiers: staged rows are A/A/A/B (SOURCES.append.md:8,9,16,19)
  — tier B S216 supports only the Chinese-rendering claims, never a mechanism claim alone;
  compliant once renumbered.
- **Criterion 2:** *"Every claim carries a source: a measured anchor (path:line, command,
  evidence id) — never oral knowledge."* The mechanism claims carry section-level anchors
  and verbatim quotes (verified above); the interpretive sentences :22 and :26-27 carry a
  source that does not say them (C3).
- **Criterion 3:** *"Observation, inference, and unknown stay separate."* :38-39's
  writer-attribution sentence is inference presented as fact (C5); :22's "not a design" is
  the entry's reading presented as upstream's statement (C3).
- **Criterion 21:** *"use a stable source heading/fragment, exact quote and observed
  revision or access date."* Header anchors :2-:4 fail this (C4); :5's anchors verified today.
- **Criterion 23:** *"resolve the exact heading … in the cited revision, then compare the
  quoted row text. A correct quote does not excuse a wrong section number."* Same defects (C4).
- **Criterion 66:** *"words such as 'only', 'otherwise' or 'exactly' need a source sentence
  that says so."* "the filename is the only lever" (:27) has no such source sentence (C3);
  "cannot be selected per package" is source-backed (A-3); "for any reason" (:43-44) is
  source-backed (asciidoc :131-132).
- **Criterion 8 (pass):** entry has `source:` (:2-5), `verified-at:` (:6), `recheck:` with
  cadence (:7); the recheck prescribes no pacman invocation (criterion 26 pass).
- **Criterion 9 (pass after C3):** the surviving negative claim ("no documented
  number-prefix range convention") is bounded by the S214 quote, re-opened 2026-10-26.
- **Criteria 1, 4, 5, 6, 10, 11, 12, 67, 70:** no obstacle found — claims falsifiable; no
  errata yet; no operator pacman action advised (criterion 6 pass); no tool landed
  (criterion 70 n/a); no JSON companion (criterion 67 n/a). Criterion 10's superseded-text
  sweep and criterion 11's LOG entry are integration-time obligations for the adopter.

## 4. PROVINCE.md scope check — PASS (Core), with one ground-line correction

PROVINCE.md:8-9: *"**Owns (surfaces, all read-only probes):** pacman state (`pacman -Qkk`
verify loops, foreign/AUR census, `.pkg.tar.zst` receipt discipline) …"*; :13-14:
*"Update-safety questions: what an -Syu would touch, what pins/holds exist."*; the owned
surfaces table :19-22 includes *".pacnew / .pacsave drift"*; :27-29: *"Never installs,
upgrades, or removes packages; never restarts services. Detection and report; the operator
remediates."* The entry is read-only doctrine on exactly those surfaces — hook timing is
part of "what an -Syu would touch", the .pacnew trigger rule serves the owned
.pacnew/.pacsave surface, and the scriptlet contract is Core pacman state (A-3's placement
analysis: `aur-risk-plane.md:202`, `degraded-triage-r4.md:113`, `boot-writers-r19.md`
ALPM-SCRIPTLET classification). The entry advises no operator action (Boundaries :65-69).
PROVINCE's Frontier section (:75-80) lists no hook item, so the entry's ground line
calling this "the Arch packaging-and-hook-semantics frontier" mislabels Core work as
frontier — corrected in C6.

## 5. Overlap with `pacman-hook-order-r38.md` (HO1–HO7) and S007/S008

| staged claim | lane's r38 entry | relation |
|---|---|---|
| alphabetical order, suffix ignored (:22-23) | HO1 (bytewise strncmp, tie → shorter first, three pairs a plain byte sort would reverse) | subset — HO1 is deeper; cross-reference, don't restate (C3, C9) |
| AbortOnFail Pre-only (:41-42) | HO4 (+ host count: 0 of 17 Pre hooks carry it) | same rule, HO4 deeper |
| Post hooks not run on failure (:43-44) | HO6 (+ boot consequence: UKI/EFI not regenerated) | same rule, HO6 deeper |
| NeedsTargets → stdin (:42-43) | count only (14 hooks, :14) | **new semantics** |
| .pacnew triggers on original name (:44-45) | absent; pacnew-plane.md has no hook content | **new** |
| hook lifecycle (:29-32) | absent | **new** |
| upgrade order old→new (:35-37) | absent (HO6 covers the post phase only) | **new** |
| scriptlet contract (:47-51) | absent (r38 entry is .hook-only) | **new** |
| three-mechanism taxonomy (:12-18) | partial (boot-writers W-classes) | **new as taxonomy** |
| Chinese five-step confirmation (:53-61) | absent | **new** |

**No HO1–HO7 row is contradicted.** The single conflict with the lane's source-level
reading is :26-27 ("no documented precedence scheme … only lever"), which the lane's own
S209/S007/S008 + HO1 falsify as absolute — corrected in C3.

**S007/S008:** no conflict and no harmful duplication. S008 (`corpus/SOURCES.md:14`) holds
only OVERRIDING HOOKS of the same man page A-1 re-opened (same URL, man date 2026-10-15,
Pacman 7.1.0); the staged S201's sections (DESCRIPTION/ACTIONS/CAVEATS) are disjoint from
it, so the complement framing holds against S008 — but the staging row's scope text
("a non-overlapping complement to S008") is false against lane S209/S210, which already
hold ordering, AbortOnFail and the post-failure rule at source level (A-1 §3) — corrected
in C8. The staged entry nowhere states precedence or override, so nothing collides with
S007/S008; the r38 entry's HO2 already turns `boot-writers-r19.md:38`'s [inf] override
into a source-backed reading, which this entry does not disturb.

## 6. Exact corrections

**C1 — renumber the four source ids (blocker; QUALITY 7).** The staged ids collide with
live lane rows: staged S201 (alpm-hooks(5) man) vs lane S201 = Btrfs ioctl.c
(`corpus/SOURCES.md:210`); staged S202 (devblog) vs lane S202 = errno(3) (`:211`); staged
S209 (alpm-install-scriptlet(5)) vs lane S209 = alpm-hooks.5.asciidoc@54d9411 (`:218`);
staged S212 (archlinuxcn Pacman) vs lane S212 = round-38 capture (`:221`). Cause: the
staging package assumed the lane registry ended at 199 rows (`MERGE-REPORT.md`: "lane
registry currently holds **199** rows; first staged id is **S200**"), but lane rounds
37–38 appended S200–S212 before adoption. Appending as-is would silently re-bind four ids
and corrupt `mount-errno-contract-r37.md:3`, `errno-contract-variance-r37.md:2`,
`pacman-hook-order-r38.md:1`. Fix: append four fresh rows — S213 = alpm-hooks(5) man,
S214 = devblog, S215 = alpm-install-scriptlet(5), S216 = archlinuxcn Pacman wiki (my grep
confirms S213+ free; use the actual next free ids at append time) — carrying the staging
rows' tier/scope/teaches cells (`SOURCES.append.md:8,9,16,19`) with the C4/C8 anchor and
scope fixes, and rewrite entry :2-5 to the new ids. Package-level note for the integrator:
the same collision affects every staged id S200–S212 of the 147-row package, not just this
entry's four.

**C2 — append `## QUALITY check` (blocker; QUALITY 14).** Draft to append before :71:

```markdown
## QUALITY check

1. Falsifiable: documented rules and quoted source statements; the two interpretive
   sentences of the 2026-10-23 draft ("not a design", "only lever") were withdrawn in the
   2026-10-26 correction (C3).
2. Sources: S213 (alpm-hooks(5) DESCRIPTION/ACTIONS/CAVEATS), S214 (devblog: Hooks
   bullets; Transaction example › Upgrading the package; Notes for package maintainers ›
   Documentation), S215 (alpm-install-scriptlet(5) DESCRIPTION lead-in / General Format /
   Functions), S216 (archlinuxcn Pacman 钩子; 安装/更新/删除 软件包时发生了什么) — every
   quoted claim verified at re-open 2026-10-26 (receipts: w1/AsmS201Man/, w1/AsmS202Devblog/,
   w1/AsmS209Scriptlet/, w1/AsmRevTiming/).
3. obs/inf/unknown: the writer-attribution sentence is marked [inf] (C5); no [unknown] retained.
7. Registry rows S213–S216 carry tier A/A/A/B and the corrected section anchors; tier B
   S216 supports only the Chinese-rendering claims, never a mechanism claim alone.
8. source:/verified-at:/recheck: present; verified-at refreshed to 2026-10-26 (C9); the
   recheck prescribes no package-manager invocation.
9. The surviving negative claim ("no documented number-prefix range convention") is
   bounded by the S214 quote re-opened 2026-10-26.
21/23. Anchors resolved at the cited revisions (C4); S216's two section headings verified
   in the raw wikitext 2026-10-26.
26. recheck prescribes no pacman invocation.
66. "only"-type wording removed or source-backed (C3, C7); both lifecycle statements kept (C5).
```

**C3 — rewrite :22-27 (attribution drift + overreach; QUALITY 3, 19, 66).** Replace the
whole paragraph with:

```markdown
**Ordering is alphabetical (alpm-hooks(5) DESCRIPTION).** Hooks run in alphabetical order
of their file name, where the ordering ignores the suffix (S213 DESCRIPTION; the lane's
`corpus/knowledge/pacman-hook-order-r38.md` HO1 holds the same rule at source level, with
the bytewise comparison and the shorter-name tie-break). The Arch Linux Dev Blog authors —
David Runge and Arne Christian Beer, not "the pacman maintainers" — wrote on 2026-08-09:
*"At the time of writing, we are missing a documented ordering system for alpm-hooks(5) in
the distribution to establish ranges of number prefixes for specific tasks."* (S214, Notes
for package maintainers › Documentation.) What is undocumented is a number-prefix range
convention, not ordering itself: the man page documents the alphabetical rule, S007
documents HookDir precedence and S008 documents same-name override, so the file name is
the main — not the only — ordering lever.
```

**C4 — fix the header anchors (:2-:4; QUALITY 21, 23).**
- :2 → `source: S213 — https://man.archlinux.org/man/alpm-hooks.5 — DESCRIPTION / ACTIONS (When, AbortOnFail, NeedsTargets) / CAVEATS — Pacman 7.1.0, man date 2026-10-15, package 7.1.0.r9.g54d9411-3` (the ordering and directory claims live in DESCRIPTION, asciidoc :35-39; TRIGGERS contributes none of the entry's claims).
- :3 → `source: S214 — https://devblog.archlinux.page/2026/on-scripts-and-hooks/ — Hooks (bullets); Transaction example › Upgrading the package; Notes for package maintainers › Documentation — published 2026-08-09, authors David Runge and Arne Christian Beer` (the quoted sentence lives in the last section, not `# The two systems`; page headings are ##/###/####).
- :4 → `source: S215 — https://man.archlinux.org/man/alpm-install-scriptlet.5 — DESCRIPTION (lead-in); General Format; Functions — package extra/alpm-docs 0.13.0-1` (the interpreter claim is in General Format, not Functions — A-3).
- :5 keeps its two anchors — both verified today in the raw wikitext (:355 `===安装/更新/删除 软件包时发生了什么===`, :444 `===钩子===`); optionally note the heading level (===, not #).

**C5 — mark the inference, weaken the lifecycle headline (QUALITY 3, 66).**
- :29 headline → `**Hook availability is bound to the providing package's installation (two statements).**` (the blog states an availability window per phase, not "existence"; A-2 (c)).
- :37-39 second sentence → `This is the fact the lane's boot-writer attribution needs: [inf] a writer observed after an upgrade may belong to the *old* version's hook or the *new* version's scriptlet — the entry's inference from S214's one worked example, not a general rule the blog states.`

**C6 — repoint the three dangling references.**
- :18 `corpus/knowledge/initramfs-hook-api-r25.md` does not exist in the lane (lane
  `corpus/knowledge/` listing 2026-10-26; the file exists only in the staging corpus) →
  `an initramfs hook — the lane's mkinitcpio surface is `corpus/knowledge/initramfs-v42-sysroot-recovery.md` and `corpus/knowledge/boot-writers-r19.md` (W-MKINITCPIO-HOOK)`, or admit the referenced entry in the same wave.
- :69 `corpus/knowledge/errno-name-discrimination-r25.md` was **rejected**, not admitted:
  `corpus/lessons/round-37.md:22` "reject; no row appended … no explicit `## QUALITY
  check` required by QUALITY 14"; :74 "rejected for overlap plus absent explicit QUALITY
  check" → `that is `corpus/knowledge/snapper-eacces-mechanism.md` and `corpus/knowledge/errno-contract-variance-r37.md``.
- :8 ground → `ground: the PROVINCE Core pacman-state and `.pacnew`/`.pacsave` surfaces (`PROVINCE.md:8-14`, `:19-22`) and the update-safety question "what an -Syu would touch"; the hook-writer attribution work in `corpus/knowledge/boot-writers-r19.md`; `corpus/README.md:38-39` watches the mkinitcpio-42 hook stranding, not alpm hook semantics` (README:38-42 holds the mkinitcpio-42 watch, the errno:13 item and a pointer line; no "packaging-and-hook-semantics" phrase exists in README/SKILL/PROVINCE — A-3's grep).

**C7 — ownership cell precision (:16; QUALITY 66).** `the package that ships the file` →
`the package that ships the file — or the operator, for a file placed directly in a `HookDir``
(host evidence: the r38 capture holds 3 `/etc/pacman.d/hooks/` files; `99-limine.hook`'s
owner is [unk], `boot-writers-r19.md:46`; `walker-restart.hook` execs a user-home script).

**C8 — registry row scope text (staged S201 row, SOURCES.append.md:8).**
"a non-overlapping complement to S008, which holds only the OVERRIDING HOOKS section of
this same page" → "complement to S008 (which holds only OVERRIDING HOOKS of this same
page) as the published rendering of the pinned source in lane S209; overlaps S209/S210 on
ordering, AbortOnFail and the post-failure rule, which it states at rendered-page level".

**C9 — refresh and cross-reference.** :6 `verified-at: 2026-10-23` → `2026-10-26` (all
four sources re-opened today; receipts listed in C2). Append one line under
"## What is now sourced": `The lane's `corpus/knowledge/pacman-hook-order-r38.md`
(HO1–HO7) holds the order rule, AbortOnFail and the post-failure rule at source level with
host counts; this entry holds the lifecycle, the scriptlet contract and the trigger
caveats it does not.` Optional enrichment (not required): also carry the next CAVEATS
sentence — removal triggers on all files owned by the removed package whether or not
present (asciidoc :128-129) — it bears on the lane's removal-time writer attribution.

## 7. Flip condition

- **ADMIT-WITH-CORRECTIONS → REJECT** if, after applying C1–C9, any corrected claim fails
  re-verification against its cited source at the cited anchor (the round-37 flip test,
  `corpus/lessons/round-37.md:22`), or if the four registry rows cannot be appended without
  re-binding a live lane id — id integrity is non-negotiable.
- **→ plain ADMIT** if the integrator applies C1–C9 verbatim and the appended `## QUALITY
  check` resolves every cited criterion; no further review needed.
- Independent flip: if `pacman-hook-order-r38.md` fails its own wave gate, the C3/C9
  cross-references reverse direction (the staged entry becomes the lane's primary
  hook-timing entry and should then absorb the HO rules it states only at rendered level);
  this admission verdict itself does not flip.

## 8. Not done (unrun checks have not passed)

- I did not myself re-open staged S201/S202/S209 (the man pages and devblog); I verified
  their claims through the sibling seats' same-day receipts (A-1/A-2/A-3, quoted above)
  after checking their quote tables, and independently verified the pinned pacman sources
  behind the lane's HO rows (asciidoc, hook.c, trans.c) and all of staged S212's claims.
- I did not re-measure the archlinuxcn page's current revision id (staged row's "revision
  34634, last edited 2025-12-14"); the translation template and both section anchors were
  verified, the revision number was not.
- I did not run any counter or selftest (no counter exists for this entry); no pacman.log
  oracle was exercised for the upgrade-order claim beyond the devblog's own worked example.
- No scratch dir was created (no clone/copy/mutant/fixture needed); nothing to remove. No
  tool installed. Scope: executed=sha256sum, git-rev-parse (read-only), mkdir, write —
  disclosed in `w1/AsmRevTiming/receipts.md`; all judged content was read/grep/glob/URL-read only.
