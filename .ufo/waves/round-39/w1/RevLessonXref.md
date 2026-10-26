VERDICT: supports

Item A-7 (round-38 routed defect 7, spotcheck §6 item 7). The round-38 lesson Gate's "Non-author closure pending"
(corpus/lessons/round-38.md:77-78) is answered by corpus/lessons/round-38-verifier-spotcheck.md §3; the closure's
census claim re-verified by an independent run. Exact cross-reference sentence for the round-39 lesson in §5.

## 1. The pending item and its routing

- corpus/lessons/round-38.md:75-78 — `### Spot-check` / "Non-author closure pending. Suggested sample: admit S208
  (re-open `hook.c` at 54d9411, line 449/452) and reject `alpm-package-anatomy-r26.md` (re-open PKGBUILD(5))."
- The routing that created this item: round-38-verifier-spotcheck.md:183-184 (§6 item 7) — "Lesson cross-reference:
  the lesson Gate "Spot-check: Non-author closure pending" (`corpus/lessons/round-38.md`) is answered by this file.
  Cross-reference it next round."
- Model sentence the round-38 lesson itself carries for the round-37 analogue: corpus/lessons/round-38.md:6-8.

## 2. §3 answers the Gate line (structural check)

- Non-author closure: round-38-verifier-spotcheck.md:3 "author: hyaku closure (non-author integrator, @m_opus)";
  :6 "No lane-authored file was edited. I ran no sibling gate or counter".
- §3 "Discernment spot-check (LEARNING.md — from outside)" at :113; table :115-121, columns Item | Gate decision |
  Re-opened source | Agree/disagree | Reason. Five rows, every row carries an explicit agree/disagree value:
  - :117 S208 (libalpm hook.c) → admit, tier A, mined — **agree**;
  - :118 S209 (alpm-hooks.5.asciidoc) → admit, tier A, mined — **agree**;
  - :119 S210, S211 (trans.c, alpm.c) → admit, tier A, mined — **agree, with an anchor defect** (S210 anchor names
    the non-existent `_alpm_trans_commit`, as the lane's own erratum says);
  - :120 `alpm-package-anatomy-r26.md` (staged) → reject — **agree** (PKGBUILD(5):351);
  - :121 `pacman-hook-timing-r25.md` (staged) → reject (not as staged) — **agree** (QUALITY count 0; S-id collisions).
- :138 "Result: the closure agrees with every sampled admit (S208–S211; S212 is checked via the capture MANIFEST)
  and with both rejects."
- Coverage vs the Gate's suggested sample: the Gate asked for S208 plus one reject; §3 covers S208-S211 and both
  rejects — a superset, each with agree/disagree and a reason. The pending item is answered.

## 3. Independent re-opens (my own fetches, 2026-10-26, scratch copies; sha256 in
.ufo/waves/round-39/w1/RevLessonXref/fetched-source-sha256.txt, key lines in key-lines.txt)

| Item | Anchor (corpus/SOURCES.md) | My fetch sha256 | Line checks observed |
|---|---|---|---|
| S208 admit | :217, sha `99f1044b…` | hook.c `99f1044badd36f83bb781d9d59409b0cdff0f26e1aa95ebd88d0f25f776b199a` | `_alpm_hook_cmp` :443; `/* exclude the suffixes from comparison */` :449; `return l1 < l2 ? -1 : 1;` :452 — the Gate's "line 449/452" is exact |
| S209 admit | :218, sha `2970cb35…` | alpm-hooks.5.asciidoc `2970cb35115a32a5d8a9652dfd795ad535d9354c36039fcc0d25929d9c3493d3` | "alphabetical order of their file name, where the ordering ignores the suffix." :39 (12 words); "Only applies to PreTransaction hooks." :88-89 |
| S210 admit | :219, sha `637c1165…` | trans.c `637c1165790ddd1c9d80bb0bfed9d85b1f5baa9b8e5a2e323243c5764ac4ed07` | `if(!(trans->flags & ALPM_TRANS_FLAG_NOHOOKS) &&` :201; `RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1);` :203. Anchor defect confirmed: `grep -c '_alpm_trans_commit'` = 0; the function is `alpm_trans_commit` at :167 — matches §3's "agree, with an anchor defect" and §6 item 4's routing |
| S211 admit | :220, sha `8bbb0a3c…` | alpm.c `8bbb0a3c90f23d8904a78faaf907a645e9329ddd05652c2b410d695f18f0834a` | `myhandle->hookdirs = alpm_list_add(NULL, hookdir);` :62 |
| Reject 1 | staged file | PKGBUILD.5.asciidoc `15e8007b…` | staged /home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/alpm-package-anatomy-r26.md:52-53 — "`package()` runs inside `$srcdir`" claim is at :53 ("`package()` runs inside `$pkgdir` under `fakeroot`"); PKGBUILD(5):351 "This function is run inside `$srcdir`." — the staged claim is false as written; reject stands |
| Reject 2 | staged file | — | /home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/pacman-hook-timing-r25.md — `grep -c QUALITY` = 0; source ids S201/S202/S209/S212 at its :2-5; the lane registry holds all four ids (`grep -cE '^\| *S2(01|02|09|12) *\|' corpus/SOURCES.md` = 4). Structural grounds verified; content claims not re-judged (same limit the spotcheck states at :121) |

## 4. Census claim (closure's §3, round-38-verifier-spotcheck.md:128-129)

Command (as instructed): `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`

- Observed: **exit=0**; stdout 35 lines — `tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`
  plus 34 `tsukuroi	W04	…` advisories, nothing else. Receipt: .ufo/waves/round-39/w1/RevLessonXref/census-validate.out.
- Read-only confirmed: sources-census.sh:5-6 "Read-only: … writes only stdout or --out"; the `touch` at :219 sits
  inside the selftest's heredoc fixture (:214-220), not executed in validate mode; I passed no --out.
- Reconciliation with the closure's "33 W04 advisories only": at the closure revision f8b4df2a the same validate over
  the extracted registry (`git show f8b4df2a:corpus/SOURCES.md` → `validate --file`, receipt
  census-validate-f8b4df2a.out, w04-old.txt) gives exactly **33 W04**. The W04 sets differ by exactly one row:
  `S217 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/trans.c across scopes` —
  round-39's own new trans.c row sharing S210's URL (w04-new.txt diff). W04 is a warning that never changes status
  (sources-census.sh:29), so exit stays 0. The closure's claim holds at its revision; today's count is 34 for a
  declared reason.
- Registry counts: 207 rows at base 8bd001f5, 212 at f8b4df2a (diff 5+0, pure append), 218 at current tip 394e1ba4 —
  matches the spotcheck's table (:134-137).
- Artifact note: the `--file` run also prints E11 lines because used-by paths are evaluated relative to the scratch
  copy; that is an artifact of running an extracted registry outside the lane, not a lane finding. The instructed
  `--root` run has no E lines.

## 5. Draft — exact cross-reference sentence for the round-39 lesson

Modeled on the round-38 lesson's own sentence for the round-37 analogue (corpus/lessons/round-38.md:6-8). Proposed
text for the round-39 lesson header paragraph:

> The round-38 non-author closure (`corpus/lessons/round-38-verifier-spotcheck.md`) answers the "Non-author closure
> pending" line at `corpus/lessons/round-38.md:77` (round-38 routed defect 7): its §3 Discernment spot-check
> (`:113-138`) re-opened the sampled admits S208-S211 (`:117-119`) and both staged rejects (`:120-121`) with
> agree/disagree and reasons, and `:138` states the result.

If the L1 keeps the round-38 template's trailing clause it continues verbatim (round-38.md:7-8, already
round-generic): "This round's own non-author closure is pending; the seats below are the lane, not outside reviewers
(LEARNING.md)."

Line-number stability: round-38.md was last touched at b0005ae and the spotcheck landed at 0eff65b (the round-39
base; `git log -1 -- <file>` for both); round-39 seats are read-only on lane content, so the cited line numbers hold
when the round-39 lesson is written.

## 6. Not done

- Content claims of pacman-hook-timing-r25.md not re-judged (structural grounds only, as above).
- S212's capture MANIFEST not re-opened (outside the sampled admits S208-S211; the closure checks it via the
  MANIFEST, spotcheck :138).
- The closure's §1/§2 checks (conformance, C1/C2 re-measurement) not re-run — outside this item.
- No tools installed (none needed); no host mutation; no TO rows judged (no `TO<n>:` lines required).

Report: .ufo/waves/round-39/w1/RevLessonXref.md
