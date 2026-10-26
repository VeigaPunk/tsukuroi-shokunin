VERDICT: supports

Item C2-12 — review of rows S208-S212 in `corpus/SOURCES.md` against the frozen
contract in `/home/vgpnk/Projects/shokunin/CORPUS.md` § "SOURCES.md — where a
shokunin learns", plus the S209/S008 duplication question. All five rows
conform; S209 is not a duplicate of S008 and neither should carry a supersedes
note. No lane file was modified by this seat; scratch dir removed at the end.

## 1. Mandated census run

Command (exactly as assigned), from `/home/vgpnk/Projects/shokunin`, 2026-10-26:

```
bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
```

Exit code: `0`. Tail (last 7 lines of 34; full copy at
`.ufo/waves/round-38/w1/C2RevO2Rows/census.out`):

```
tsukuroi	W04	S185 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst across scopes
tsukuroi	W04	S203 duplicate url man7.org/linux/man-pages/man3/errno.3.html across scopes
tsukuroi	W04	S204 duplicate url man7.org/linux/man-pages/man3/errno.3.html across scopes
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
```

33 of the 34 output lines are `W04 duplicate url ... across scopes` warnings;
the final verdict line is `ok`. None of the 33 warnings involves S008 or S209
(their URLs differ: `man.archlinux.org/man/alpm-hooks.5` vs
`gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/doc/alpm-hooks.5.asciidoc`).
All W04 pairs are pre-existing rows (S087-S204).

## 2. Contract conformance of S208-S212 (SOURCES.md:217-221)

Checks run on `corpus/SOURCES.md`, all observed output shown:

- 11 columns / no `|` in cells: `awk -F'|' '/^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|/ && NF!=13 {print}'`
  printed nothing; all 212 rows have NF=13, including S208-S212 individually
  (`S208 NF=13` … `S212 NF=13`). A pipe inside any cell would raise NF, so this
  also proves the no-`|` rule.
- id sequence: line 216 is S207, so S208-S212 are the next unused ids
  (`sed -n '214,217p'` shows S205, S206, S207, then S208). Duplicate-id census
  (`... | sort | uniq -d`) printed nothing.
- enum and tier rules (contract census block, CORPUS.md:145): printed nothing —
  kind ∈ {code, docs, own-work}, tier ∈ {A}, status ∈ {mined}, no tier-inflation
  (none of the five is `community`).
- tier scoping: every scope names a bounded topic ("ALPM hook run order,
  directory override, triggerless masks and PreTransaction failure handling for
  the installed pacman 7.1.0.r9.g54d9411" S208:217; "the documented hook
  run-order rule and the PreTransaction-only scope of AbortOnFail at the
  installed pacman commit" S209:218; etc.). No row claims global scope.
- status/used-by consistency: all five are `mined` and each used-by names
  `corpus/knowledge/pacman-hook-order-r38.md`, which exists (`ls -la`: 12602
  bytes, Oct 26 01:20). The reverse direction also holds: the knowledge entry's
  provenance trio opens `source: S208, S209, S210, S211, S212 in corpus/SOURCES.md …`,
  `verified-at: 2026-10-26`, `recheck: …` (corpus/knowledge/pacman-hook-order-r38.md:1-3),
  matching the fleet rule "a new knowledge entry opens with its provenance trio"
  (CORPUS.md:165-167). No `mined` row elsewhere lacks used-by either.
- opened/recheck: `opened=2026-10-26` (ISO, the actual capture/fetch date, see
  §3) for all five; recheck `on-release` (S208-S211) and `30d` (S212). `30d` is
  established practice — 4 rows already use it (`awk` histogram: 180d=19, 30d=4,
  90d=16, on-release=172, everycapture=1).
- append-only: `git show 1fe28e7 -- corpus/SOURCES.md` contains exactly five
  `+| S20x`/`+| S21x` lines and no modified/removed table rows. Commit
  1fe28e725be47364fc6033bf81ecabc66ee5fe62 "round-38: C2 effective ALPM hook
  order entry (HO1-HO7, 69 rows) on S208-S212" is the only commit touching these
  rows; it also added the pinned snapshots and 109-line knowledge entry
  (`git show --stat`: corpus/SOURCES.md +5, pacman-hook-order-r38.md +109).

## 3. Anchors carry revision and resolve at their cited lines

All five anchor sha256s reproduce from the frozen artifacts
(`sha256sum .ufo/waves/round-38/sources/{hook.c,alpm-hooks.5.asciidoc,trans.c,alpm.c} .ufo/waves/round-38/frozen/hooks-capture/MANIFEST.sha256`):
hook.c `99f1044badd36f83bb781d9d59409b0cdff0f26e1aa95ebd88d0f25f776b199a`,
alpm-hooks.5.asciidoc `2970cb35115a32a5d8a9652dfd795ad535d9354c36039fcc0d25929d9c3493d3`,
trans.c `637c1165790ddd1c9d80bb0bfed9d85b1f5baa9b8e5a2e323243c5764ac4ed07`,
alpm.c `8bbb0a3c90f23d8904a78faaf907a645e9329ddd05652c2b410d695f18f0834a`,
MANIFEST.sha256 `da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd`
— identical to the anchor cells (SOURCES.md:217-221) and to
`.ufo/waves/round-38/sources/SHA256SUMS` (header: "fetched 2026-10-26T04:20:21Z
from https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/<path>").

Line-range spot checks against the pinned snapshots:

- hook.c:443-455 = `_alpm_hook_cmp` complete: suffix-length-excluded `strncmp`
  (443-449) and the tie branch `return l1 < l2 ? -1 : 1` (450-452) — grounds
  S208's teaches verbatim.
- hook.c:532-683 = `_alpm_hook_run` (532 signature, 538 iterates
  `alpm_list_last(handle->hookdirs)` backwards — later-listed HookDir wins,
  682 closing brace).
- hook.c:116-147 = inside `_alpm_hook_validate` (defined at 113): the
  triggerless-mask special case at 118-123 and the AbortOnFail PostTransaction
  warning at 143. Note: the cited range starts at the body, not the 113
  signature; it still covers everything the scope claims. Cosmetic only.
- alpm-hooks.5.asciidoc:35-39 (inside DESCRIPTION, header above line 30): "Hooks
  are run in alphabetical order of their file name, where the ordering ignores
  the suffix" — S209's run-order claim; 87-89 = `*AbortOnFail*:: … Only applies
  to PreTransaction hooks.` — S209's AbortOnFail scope.
- trans.c:201-240 = `_alpm_trans_commit` from its first statement: Pre-hook
  `RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1)` at 201-204; Post hook run at
  236-239 with return value unused — grounds S210's teaches.
- alpm.c:56-62 = `alpm_initialize` builds SYSHOOKDIR path and
  `myhandle->hookdirs = alpm_list_add(NULL, hookdir)` (62) — system dir is the
  list head, grounds S211.
- S212 own-work capture: `capture-meta.txt` records "captured
  2026-10-26T04:11:58Z host=plazir27 read-only" and `pacman 7.1.0.r9.g54d9411-3`;
  counts reproduce: 67 files under usr-share-libalpm-hooks, 3 under
  etc-pacman.d-hooks (find|wc), and `LC_ALL=C comm -12` of the two listings
  yields exactly `90-mkinitcpio-install.hook` — the one same-name pair, so 70
  files / 69 unique names. `sha256sum -c MANIFEST.sha256`: 70 lines, 0 failures.

## 4. S209 vs S008 — same document, different URL/scope: not a duplicate, no supersedes

- S008 (SOURCES.md:14): rendered man page `https://man.archlinux.org/man/alpm-hooks.5`,
  anchor "OVERRIDING HOOKS; Pacman 7.1.0 man-page footer dated 2026-10-15",
  scope = same-name override + /dev/null disable, used-by degraded-triage-r4 +
  boot-writers-r19.
- S209 (SOURCES.md:218): the asciidoc source at pinned commit 54d9411, anchor
  DESCRIPTION lines 34-39 + AbortOnFail 87-89 + snapshot sha256, scope =
  run-order rule + AbortOnFail PreTransaction-only, used-by
  pacman-hook-order-r38.md.
- Same underlying document, different representations, disjoint scopes — each
  row's tier-A claim sits inside its own scope, so neither duplicates the other.
  The registry already tolerates same-document-across-scope rows (33 W04
  warnings, several on identical URLs, e.g. pacman.8 in S089/S090/S106/S107;
  System_maintenance?oldid=885170 in S010/S092).
- Supersedes would be wrong: contract rule 2 (CORPUS.md, "### Rules") reserves
  it for corrections ("A correction is a new row whose `teaches` opens
  `supersedes S0NN —`"), and S209 corrects nothing in S008. Verified
  independently at the installed revision: the local man page
  (/usr/share/man/man5/alpm-hooks.5.gz, header `.TH "ALPM\-HOOKS" "5"
  "2026\-10\-15" "Pacman 7\&.1\&.0"` — matches S008's anchor) states "Hooks may
  be overridden by placing a file with the same name in a higher priority hook
  directory. Hooks may be disabled by overriding them with a symlink to
  /dev/null", and the pinned asciidoc carries the same text at lines 99-101 plus
  the identical run-order sentence at 35-39. The two revisions agree; S008 stays
  valid.
- The relationship is already recorded the right way: the knowledge entry's
  ground paragraph says the lane "held two hook facts before this entry —
  HookDir precedence (S007) and same-name override (S008 …)" and adds the
  run-order/mask/failure facts as new (pacman-hook-order-r38.md:7-10). S209's
  `teaches` also cross-references S208, not S008.
- Proposed text: none. A supersedes note would falsely retract S008; adding a
  cross-reference into S008's `teaches` in place would violate append-only rule
  2, and a third row for it would be filler.

## 5. Open items (observations, not contract violations)

1. Rule 1's Gate recording (URL, access date, ≤25-word quote per new row in the
   round lesson) is not yet satisfied anywhere in `.ufo/waves/round-38/` — no
   lesson file exists yet (`ls .ufo/waves/round-38/`: after, assimilation,
   before, controls, frozen, l1, sources, w1, dispatch files). Expected at wave
   close; the grounding artifacts (SHA256SUMS fetch timestamp, capture-meta
   timestamp, pinned snapshots) already exist. This must land before round end.
2. No Search-log entry for the round-38 source work (SOURCES.md `## Search log`
   ends with the 2026-10-20 entries). Defensible: the work fetched four
   pre-identified upstream files at a known commit plus a local capture, not a
   bounded search under rule 5; fetch provenance lives in SHA256SUMS and the
   knowledge trio. Flagging in case the round lesson wants one prose note.
3. Pre-existing, outside my rows: S101 (SOURCES.md:107) has `recheck
   everycapture`, a cadence outside the contract's examples (`90d`, `180d`,
   `on-release`) and outside every other row's practice.

## 6. What I did not do

- Did not re-fetch the four upstream files over the network; anchor sha256s were
  verified against the lane's frozen snapshots and SHA256SUMS, not against
  gitlab directly.
- Did not verify S008's man.archlinux.org web footer itself (no network use);
  verified the same footer data on the installed local man page instead.
- Did not judge HO1-HO7 rule truth (owned by the HO-row seats).
- No tools were installed or upgraded (none needed: awk, git, sha256sum,
  python3 all present).

Scratch `/fast/scratch/hyaku/tsukuroi-r38/C2RevO2Rows` removed after copying
`census.out` into the seat receipt dir.
