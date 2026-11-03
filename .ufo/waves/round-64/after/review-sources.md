# R2Sources — C3-SOURCES-ATTACK: pre-integration falsifier review of SOURCES rows S279–S281
2026-11-03T19:04:12Z

Seat R2Sources (reviewer, tsukuroi r64 w1). Lane repo `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. This file is my only lane write. All commands run with cwd = fleet root; every receipt below is `$ command` + verbatim output + rc. No tools installed (system binaries only: curl, awk, gawk via the fleet census, python3, coreutils) — operator tooling directive satisfied by non-use.

## 0. Draft status — DRAFT ABSENT AT WINDOW CLOSE

Seat S1Scribe's draft `.ufo/waves/round-64/drafts/sources-rows-r64.md` did not exist at any check. First check 18:42:31Z, last 19:02:17Z (20-minute poll window honored; ~45–60 s cadence; 15 `ls` checks total, 13 timestamped):

```
$ ls -la /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-64/drafts/
ls: cannot access '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-64/drafts/': No such file or directory
rc=2          # at 18:42:31, 18:49:34, 18:51:47, 18:52:53, 18:53:57, 18:54:52, 18:56:00,
              # 18:56:29, 18:57:28, 18:58:23, 18:59:17, 19:00:41, 19:02:17Z (+2 unstamped early checks)
```

Per the dispatch fallback I therefore executed parts 1–2 in full (independent verification), built the quote and census machinery (parts 3–4), and issue **conditional verdicts with exact flip conditions** (part 5). S1Scribe's transcript shows the draft work in progress (own census rig, hook byte-identity checks, quote word counts) at ~18:45–18:58Z; the scribe also received the SC2Census CRLF blocker at ~18:59Z.

## 1. Sources re-opened live (curl, network reads only)

Scratch: `/fast/scratch/hyaku/tsukuroi-r64/R2Sources/` (deleted before yield; all citable bytes embedded below).

### 1a. mkinitcpio v42.2 release — API endpoint

```
$ curl -sS -o release-v42.2.json -w 'http=%{http_code} size=%{size_download}\n' 'https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/releases/v42.2'
http=200 size=3905
rc=0
$ grep -o '"released_at":"[^"]*"' release-v42.2.json
"released_at":"2026-10-01T07:10:00.872Z"
$ grep -o '"name":"[^"]*"' release-v42.2.json ; grep -o '"tag_name":"[^"]*"' release-v42.2.json
"name":"v42.2"
"name":"nl6720"          # author object, not the release name
"tag_name":"v42.2"
```

Decoded `description` (python3 json.load → description.txt), verbatim, 15 lines:

```
     1	CHANGES WITH v42.2
     2	
     3	        Changes in hooks:
     4	
     5	        * install/systemd includes systemd-tpm2-setup-early.service and
     6	          systemd-pcrnvdone.service because of changes in systemd v262. They are
     7	          required to initialize NvPCRs and to measure a separator into PCR 9.
     8	          Note that this does not fix the issue of failing units with UKIs built
     9	          by mkinitcpio itself. systemd v262 requires that the UKI must be
    10	          signed with a PCR policy and there is still no solution for that
    11	          without using ukify.
    12	
    13	        Contributions from: Aidan Dang, nl6720
    14	
    15	        - 2026-10-01
```

Scope-term byte-presence in the fetched JSON (`grep -cF`, file is one line so counts are per-document): `systemd-tpm2-setup-early.service`=1, `systemd-pcrnvdone.service`=1, `NvPCR`=1, `PCR 9`=1, `failing units with UKIs`=1, `ukify`=1, `Changes in hooks`=1, `nl6720`=1. **No invented bullet is possible in the template scope** — every entity the dispatch template names for S279 exists verbatim in the live body.

Unicode trap (verified in both raw JSON and decoded text):

```
$ python3 -c "d=open('description.txt').read(); i=d.find('Aidan'); print(repr(d[i:i+16]))"
'Aidan\xa0Dang, nl67'
```

The separator inside "Aidan Dang" is U+00A0 (no-break space), NOT ASCII space; `grep -cF 'Aidan Dang'` (ASCII) on the raw JSON = 0. Any Gate quote spanning that name must preserve U+00A0 or it is not a byte-match.

Anchor check for the template cell "CHANGES WITH v42.2 - Changes in hooks; release v42.2, released_at 2026-10-01T07:10:00Z": maps to description lines 1 and 3, and the JSON `released_at`. The live value is `2026-10-01T07:10:00.872Z`; the template's second-precision form is a truncation of the millisecond JSON value — cosmetic, same instant. NIT for L1: either form is defensible; the row should carry the exact string it asserts.

### 1b. limine-entry-tool btrfs-overlayfs hook (master)

```
$ curl -sS -o btrfs-overlayfs.hook -w 'http=%{http_code} size=%{size_download}\n' 'https://gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs'
http=200 size=1519
rc=0
$ grep -n '/new_root' btrfs-overlayfs.hook
3|run_latehook() {
*4|	root_mnt="/new_root"
 5|
 6|	# Check: Is $root_mnt mounted on Btrfs?
 7|	fstype=$(findmnt --mountpoint "$root_mnt" -no FSTYPE 2>/dev/null) || return 0
$ awk 'NR==4' btrfs-overlayfs.hook
	root_mnt="/new_root"
rc=0
```

The cited **line 4** is exact: `root_mnt="/new_root"` (TAB-indented), inside `run_latehook() {` at line 3. The "silent return when mount absent" branch is line 7 (`... || return 0`). Full 57-line file read; only these lines are material to the rows.

Pin freshness — latest commit touching the file on master:

```
$ curl -sS '.../repository/commits?path=install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs&ref_name=master&per_page=1'   (http=200 size=641, rc=0)
[{"id":"3c011dc2aebc0346f5e1d5dc2132a2a5f6c71169","short_id":"3c011dc2","created_at":"2026-01-11T13:38:30.000+01:00",...,"title":"Improve safeguards of btrfs-overlayfs",...}]
```

`3c011dc2…` dated 2026-01-11 is **exactly the commit S021 pins** — master is unchanged since the pin; the re-pin re-verifies rather than moves the anchor.

Installed-package identity (host reads, allowed probes):

```
$ pacman -Q limine-mkinitcpio-hook
limine-mkinitcpio-hook 1.40.0-2                       (rc=0)
$ pacman -Qo /usr/lib/initcpio/hooks/btrfs-overlayfs
/usr/lib/initcpio/hooks/btrfs-overlayfs is owned by limine-mkinitcpio-hook 1.40.0-2   (rc=0)
$ cmp /usr/lib/initcpio/hooks/btrfs-overlayfs btrfs-overlayfs.hook
rc=0   (byte-identical)
$ sha256sum btrfs-overlayfs.hook /usr/lib/initcpio/hooks/btrfs-overlayfs
eeac1ed326f5c6fed2e47bbb596d76c9c4b0020be30c3b3c58f6b3a4fa093dcf  btrfs-overlayfs.hook
eeac1ed326f5c6fed2e47bbb596d76c9c4b0020be30c3b3c58f6b3a4fa093dcf  /usr/lib/initcpio/hooks/btrfs-overlayfs
```

The S280 teaches claim "master byte-identical to installed limine-mkinitcpio-hook 1.40.0-2" is **TRUE on this host** (cmp rc 0, identical sha256).

### 1c. Arch plymouth packaging initcpio hook (main)

```
$ curl -sS -o plymouth.initcpio_hook -w 'http=%{http_code} size=%{size_download}\n' 'https://gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/main/plymouth.initcpio_hook'
http=200 size=336
rc=0
$ grep -n '/new_root' plymouth.initcpio_hook
 10|run_latehook(){
*11|  plymouth update-root-fs --new-root-dir=/new_root
 12|}
$ awk 'NR==11' plymouth.initcpio_hook
  plymouth update-root-fs --new-root-dir=/new_root
rc=0
```

The cited **line 11** is exact, inside `run_latehook(){` at line 10. Full 16-line file read.

Pin freshness — latest commit touching the file on main:

```
$ curl -sS '.../repository/commits?path=plymouth.initcpio_hook&ref_name=main&per_page=1'   (http=200 size=641, rc=0)
[{"id":"df088501c9bf9b28b98ba58e7049ec8026edd8f8","short_id":"df088501","created_at":"2023-03-21T01:25:10.000+00:00",...,"title":"Move plymouth from AUR with 580 votes",...}]
```

`df088501…` dated 2023-03-21 is **exactly the commit S022 pins** — main unchanged since the pin.

Installed-package identity:

```
$ pacman -Q plymouth
plymouth 26.134.222-3                                 (rc=0)
$ pacman -Qo /usr/lib/initcpio/hooks/plymouth
/usr/lib/initcpio/hooks/plymouth is owned by plymouth 26.134.222-3    (rc=0)
$ cmp /usr/lib/initcpio/hooks/plymouth plymouth.initcpio_hook
rc=0   (byte-identical)
$ sha256sum plymouth.initcpio_hook /usr/lib/initcpio/hooks/plymouth
de852646e615e06d4125eb2e646d0528d1e349bd9e9877c08c5d32c43d288b6f  plymouth.initcpio_hook
de852646e615e06d4125eb2e646d0528d1e349bd9e9877c08c5d32c43d288b6f  /usr/lib/initcpio/hooks/plymouth
```

The S281 teaches claim "fetched bytes identical to installed plymouth 26.134.222-3's hook" is **TRUE on this host**. Note the packaged filename is `/usr/lib/initcpio/hooks/plymouth` (PKGBUILD renames `plymouth.initcpio_hook` at install); bytes are identical.

## 2. REGISTRY-shape rules (contract vs census mechanics)

Registry: `corpus/SOURCES.md`; columns `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` (header lines 5–6). Row shape verified on the last row:

```
$ read corpus/SOURCES.md :raw:284-287   → S275, S276, S277, S278 rows; S278 at line 287
```

- **11 cells ⇒ NF==13**: census `row_pass` gawk, validate block: `if (NF!=13) … printf E01 fields=NF-2` (scripts/sources-census.sh :630-656 read). My probe confirmed: a 10-cell row ⇒ `E01 … fields=10`.
- **No '|' inside cells**: equivalent to NF==13 for a leading-`|` row; the census has no escaped-pipe allowance (`url_of` excludes `|` from URLs: `/https?:\/\/[^[:space:]|]+/`, :600-605).
- **Id continuity**: `grep 'S27[6-9]|S28[0-2]' corpus/SOURCES.md` returns only S275–S278 (lines 284–287). S278 is the last row (line 287, directly before the blank lines and `## Paths` at line 290). **S279, S280, S281 are unused in the registry** ⇒ no E03.
- **Id-reuse sweep across the lane**: S279–S281 appear only in `.ufo/waves/round-37|38|39/assimilation/staged-ids` quarantine inventories and round-37 wave reports — the shokuknow merge package's id space (S200–S346) that round-37 explicitly did NOT adopt ("the staged package's S200–S346 id space was not adopted"; "S214/S220/S279–S282/S286/S287 do not exist in the registry"). RESIDUAL RISK (disclosure, not blocker): those historical artifacts attach *different meanings* (man7 errno(3)) to S279–S281; the registry is authoritative, but the L1 should be aware a repo-wide grep cross-wires meanings.
- **Tier A kind**: census `E10` fires on `tier=="A" && kind=="community"` (:663-700 block; my probe produced `E10 S281 community-at-A`). Contract allows docs/code at tier A; template uses docs (S279) and code (S280/S281) — compliant. NIT: census enum also admits spec/paper/tool/dataset/talk/book/community/own-work (:657-660 region); the round contract is stricter — fine.
- **teaches opens 'supersedes S0NN -'**: census E04 exemption is the regex `/supersedes S[0-9]{3}/` anywhere in teaches (scripts/sources-census.sh :647-649):

```
 647|            url_scope_nonrejected[scope_key] &&
*648|            teaches !~ /supersedes S[0-9]{3}/)
 649|          printf "%s\tE04\t%s duplicate url %s within scope %s\n",lane,id,u,scope
```

  The contract's "opens with" requirement is stronger than the census's substring test — satisfying the contract satisfies the census. Section 4 proves both directions live.
- **used-by target**: `corpus/knowledge/mkinitcpio42-onrelease-r64.md` — **correct**: it is the frozen C3 predicate path verbatim.

```
# SCORECARD.md:4717 (C3 row): "→ `corpus/knowledge/mkinitcpio42-onrelease-r64.md` with `^| MK` rows ≥ 5 …
  SOURCES 278 → ≥ 281 (S279 v42.2 release notes tier A docs; S280 supersedes S021 re-pin; S281 supersedes S022 re-pin),
  S279 directly after S278, NF 13, Gate quotes ≤ 25 words (`wc -w`); knowledge-header gate PASS; …"
# LOG.md:2762: "After predicate (frozen): `corpus/knowledge/mkinitcpio42-onrelease-r64.md` exists with `^| MK` rows ≥ 5 …"
```

  Census E11 resolves used-by relative to the lane dir (`[ -e "$dir/$path" ]`, usedby_findings :538-552) and will flag E11 for the three rows until the L1 lands the note — **expected at draft stage, disappears at integration**. Naming fits the `topic-rNN` convention (cf. `initramfs-v42-sysroot-recovery.md`, `host-drift-recheck-r64.md`).

## 3. Gate-quote machinery (standard + pre-verified candidates)

Standard applied (and recommended to the L1): a quote passes iff (a) `printf '%s' "<quote>" | wc -w` ≤ 25, and (b) the quote occurs verbatim in the fetched body — strict `grep -cF` ≥ 1; for a quote spanning an upstream markdown line-wrap, whitespace-run normalization (`tr -s '[:space:]' ' '` on both sides) is acceptable **iff the non-whitespace bytes are otherwise identical**; any word change = paraphrase = REJECT.

Pre-verified candidates from the live bodies (all ≤ 25 words):

| Q | quote | wc -w | strict | wrap-normalized |
|---|---|---|---|---|
| Q1 | Note that this does not fix the issue of failing units with UKIs built by mkinitcpio itself | 17 | 0 (wraps desc L8→L9) | 1 ✓ |
| Q2 | install/systemd includes systemd-tpm2-setup-early.service and systemd-pcrnvdone.service because of changes in systemd v262 | 11 | 0 (wraps L5→L6) | 1 ✓ |
| Q3 | systemd v262 requires that the UKI must be signed with a PCR policy | 13 | 0 (wraps L9→L10) | 1 ✓ |
| Q4 | required to initialize NvPCRs and to measure a separator into PCR 9 | 12 | 1 ✓ (desc L7) | — |
| Q5 | Changes in hooks: | 3 | 1 ✓ (desc L3) | — |
| Q6 | `root_mnt="/new_root"` | 1 | 1 ✓ (btrfs hook L4) | — |
| Q7 | `plymouth update-root-fs --new-root-dir=/new_root` | 3 | 1 ✓ (plymouth hook L11) | — |

```
$ printf '%s' "Note that this does not fix the issue of failing units with UKIs built by mkinitcpio itself" | wc -w
17
$ grep -cF -- "required to initialize NvPCRs and to measure a separator into PCR 9" description.txt
1
$ grep -cF -- 'root_mnt="/new_root"' btrfs-overlayfs.hook
1
$ grep -cF -- 'plymouth update-root-fs --new-root-dir=/new_root' plymouth.initcpio_hook
1
# wrap-normalized (desc): tr -s '[:space:]' ' ' < description.txt | grep -cF -- "<normalized quote>"  → Q1: 1, Q2: 1, Q3: 1
```

Reminder: any quote crossing "Aidan Dang" must carry U+00A0 (§1a).

## 4. Duplicate-URL checks — census simulation on a post-C1 mirror

Method: mirror of the lane registry CR-stripped (`tr -d '\r'`) plus `corpus/knowledge`, `corpus/lessons`, `corpus/QUALITY.md`, `SKILL.md`, `tools/` copies; fleet census run read-only against the mirror. This models the state the rows land into (post-C1). Cross-note: SC2Census reported the worktree SOURCES.md re-materialized CRLF at 18:47:32Z (sha 2349bfda… = HEAD blob) — my mirror CR-strips before census, so results are independent of that transient; the repair belongs to E1LineEnd.

Baseline (no new rows):

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate /fast/scratch/.../r64test-shokunin
… 42 × W04 lines …
r64test-shokunin	ok	/fast/scratch/hyaku/tsukuroi-r64/R2Sources/r64test-shokunin/corpus/SOURCES.md
rc=0
```

Exactly **42 W04, zero E** — matches C1's declared after-state ("rc 0, zero E-code, 42 W04 warnings reappear"). Mirror is faithful.

Mechanics probe (synthetic rows spliced after S278, scope cells extracted verbatim from S021/S022):

```
S283 = S021's URL + S021's exact scope + teaches WITHOUT supersedes token
S284 = S021's URL + S021's exact scope + teaches "supersedes S021 - …"
S285 = S022's URL + S022's exact scope + teaches WITHOUT supersedes token
S286 = S022's URL + S022's exact scope + teaches "supersedes S022 - …"

$ census validate probe2-shokunin | grep -E 'S28[3-6]'
probe2-shokunin	E04	S283 duplicate url gitlab.com/Zesko/limine-entry-tool/…/btrfs-overlayfs within scope The overlay runtime hook's expected root mount path and silent return when that mount is absent
probe2-shokunin	E04	S285 duplicate url gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/main/plymouth.initcpio_hook within scope Packaged Plymouth busybox latehook's root-path argument
probe2-shokunin	E11	S283|S284|S285|S286 missing used-by corpus/knowledge/mkinitcpio42-onrelease-r64.md   ← fixture artifact (note not yet landed)
rc=1
```

Proven live: same-URL-same-scope duplicate **without the token fires E04** (rc 1); **with `supersedes S0NN -` the E04 is suppressed** (S284/S286 produce no E04). A second probe variant (new scope text, same URL) produced only W04 (warning, rc unaffected). A first probe attempt accidentally demonstrated that a one-character scope difference (`hook's` → `hook`) flips E04 into W04 — scope text is compared byte-exactly.

S279 URL novelty: `url_of` extracts the FIRST URL of the source cell (:600-605). S015's first URL is `…/-/releases/v40`; S053's is `…/-/releases` (the API URL inside S053's cell is not extracted); S279's `gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/releases/v42.2` is new to `url_seen` ⇒ S279 produces **neither E04 nor W04**. Expected W04 delta from the three rows: up to +2 (S280, S281 across-scope re-pins), zero E.

Adjacency disclosure (contract-blessed overlap, no census code): S053 (tier A docs, opened 2026-10-20) already reads the v42.1+v42.2 release bodies and frames them as a question; S054/S058 pin v42.2 init/functions; S098 (W04) and S111 (W04, tag-pinned `26.134.222-3` URL) already touch the hook URLs. S279–S281's distinct contribution must stay host-anchored (installed 42.2-1, byte-identity, the fired on-release watch) — which is exactly the template's scope. Keep S280/S281 teaches prefixed `supersedes S021 - ` / `supersedes S022 - `.

## 5. Verdicts (as of 19:02:17Z; draft absent ⇒ conditional)

| Row | Verdict | Grounded now | Flip to REJECT if |
|---|---|---|---|
| S279 | **CONDITIONAL ADMIT** | Template cells all byte-grounded: scope entities §1a (each grep -cF = 1); anchor = desc L1+L3 + released_at; URL new (no E04/W04); tier A docs; id free; used-by = frozen predicate | scope asserts a bullet absent from the live body; anchor mislocates (not L1/L3); quote > 25 words or paraphrase (fails §3 standard, incl. the U+00A0 case); any cell contains '\|'; NF≠13; used-by path deviates from `corpus/knowledge/mkinitcpio42-onrelease-r64.md` |
| S280 | **CONDITIONAL ADMIT** | Line 4 exact §1b; master==pin 3c011dc; master byte-identical to installed 1.40.0-2 (cmp rc 0, sha equal); census-clean with the `supersedes S021 - ` prefix (probe S284) | line number ≠ 4; byte-identity claim false (it is true today — would need host change); prefix missing while scope ≡ S021's (⇒ E04, probe S283); quote paraphrase/mislocated; kind not code / tier not A |
| S281 | **CONDITIONAL ADMIT** | Line 11 exact §1c; main==pin df08850; fetched bytes identical to installed 26.134.222-3 hook (cmp rc 0, sha equal); census-clean with `supersedes S022 - ` (probe S286) | line number ≠ 11; prefix missing while scope ≡ S022's (⇒ E04, probe S285); quote paraphrase/mislocated; kind not code / tier not A |

Note: no REJECT findings exist against the *sources* or the *contract* — every template cell I could test against live bytes and host state is TRUE. The only reason these are conditional is the draft's absence: shape (NF==13, no pipes), the actual quote strings + printed wc -w counts, and the exact teaches wording remain unverified until the draft (or the integrated registry) exists.

### Integration checklist for the L1 (each item pre-proved above)
1. Land CR-strip first (E1's lane): with CRLF bytes the census's `## Registry\r` heading fails `in_registry` (trim strips spaces/tabs only, :609-616) ⇒ all rows E12 — SC2Census observed exactly this state live at 18:47:32Z–18:53:30Z.
2. Insert S279–S281 **directly after the S278 row** (line 287), inside `## Registry`, before `## Paths` — else E12.
3. Rows: exactly 11 cells, no pipes, `mined | 2026-11-03 | on-release | corpus/knowledge/mkinitcpio42-onrelease-r64.md`.
4. S280/S281 teaches open `supersedes S021 - ` / `supersedes S022 - ` (E04 exemption is then guaranteed regardless of scope-text choice).
5. Quotes: use §3 table (Q1–Q7 all pass; prefer single-line Q4/Q5/Q6/Q7 for strict byte-match).
6. Land `corpus/knowledge/mkinitcpio42-onrelease-r64.md` in the same integration (clears the three E11s).
7. Re-run: `scripts/sources-census.sh validate <lane>` — expect rc 0, 42–44 W04, zero E.

## 6. Residual risks / verification gaps
- UPDATE 19:06:15Z: the draft DID land at ~19:02-19:03Z and was attacked in full — see the ADDENDUM below; §5's conditional table there is superseded by the addendum's final verdicts.
- S279–S281 carry different meanings in never-adopted round-37/38/39 staged-id artifacts (errno(3)); registry is authoritative; a disclosure line in the round log would prevent future cross-wiring.
- released_at template form `2026-10-01T07:10:00Z` truncates `.872` ms — same instant, cosmetic; pick one form and assert it.
- Template uses ASCII ` - ` between title and URL where the registry's recent rows use an em dash ` — `; url_of is indifferent; cosmetic consistency nit.
- Host-state claims (byte identities, package versions) are true as measured 2026-11-03T18:42–19:04Z; any upgrade between now and integration invalidates S280/S281's "byte-identical" teaches and requires re-measurement (that is the rows' own on-release recheck cadence doing its job).

---

# ADDENDUM 2026-11-03T19:06:15Z — the draft LANDED at ~19:02-19:03Z; final verdicts below supersede §5's conditional rows

`.ufo/waves/round-64/drafts/sources-rows-r64.md` (16063 B, with `lesson-skeleton-r64.md`) appeared on the courtesy re-check at 19:04:08Z (drafted 18:58Z per its header). I then ran the full battery on the REAL rows. §0-§4 above stand unchanged (all live-source facts were verified independently before the draft existed and are cited by the draft's own receipts — our sha256s agree byte-for-byte: release `9ebec7b1…`, btrfs hook `eeac1ed3…`, plymouth hook `de852646…`).

## A1. Row shape — PASS
```
$ grep -E '^\| S(279|280|281) \|' drafts/sources-rows-r64.md | awk -F'|' 'NF==13' | wc -l → 3
row1: NF=13 cells=11 id=[ S279 ] kind=[ docs ] tier=[ A ] status=[ mined ] opened=[ 2026-11-03 ] recheck=[ on-release ] usedby=[ corpus/knowledge/mkinitcpio42-onrelease-r64.md ]
row2: NF=13 cells=11 id=[ S280 ] kind=[ code ] … same tail cells
row3: NF=13 cells=11 id=[ S281 ] kind=[ code ] … same tail cells
```
CAUTION for the L1: the draft ALSO contains three `| S279/S280/S281 | …` lines in its "Gate counts summary" markdown table (NF=6). Paste ONLY the three fenced ```text rows. Em dash house style (` — ` between title and URL) is used — good.

## A2. Census on the real rows — PASS (mirror = post-C1 lane state, CR-stripped, rows spliced after S278)
```
$ grep -nE '^\| S(278|279|280|281) \|' <mirror>/corpus/SOURCES.md
287:| S278 | … 288:| S279 | … 289:| S280 | … 290:| S281 | …          ← directly after S278 (C3 predicate) ✓
$ census validate <mirror>            # with placeholder MK note present
rc=0 ; W04 count: 44 ; E-code count: 0 ; "ok"
new W04 rows: S280, S281              (42 baseline + 2 — the scribe's own figure, independently reproduced)
$ census validate <mirror>            # placeholder note REMOVED (landing-order truth)
rc=1 ; exactly 3 × E11: S279/S280/S281 missing used-by corpus/knowledge/mkinitcpio42-onrelease-r64.md
```
Confirms the draft's schema notes #1/#2: W04 moves 42 → 44 after landing (the frozen C1 text says "the 42 W04 … reappear" — exit-0 and zero-E hold; only the stated W04 figure needs the L1's restatement), and the three E11s exist until the MK note lands with-or-before the final census receipt.

## A3. Gate quotes — ALL PASS
S280/S281: strict byte-matches — `root_mnt="/new_root"` (1 word, L4), `# Check: Is $root_mnt mounted on Btrfs?` (7, L6), `echo "[OverlayFS setup] ${root_mnt} is a read-only Btrfs subvolume. Setting up OverlayFS..."` (12, L21 ✓ line number correct), `plymouth update-root-fs --new-root-dir=/new_root` (3, L11), `run_latehook(){` (1, L10). All `grep -cF` = 1 against my independently fetched bytes.
S279: all four quotes pass under the §3 wrap-normalization standard — primary 11 words, supporting 14/17/24 words (all ≤ 25); normalized-match = 1 each; the draft discloses the wrapping explicitly. `changelog commit e5433c2e…` verified present in the live JSON (grep -cF = 1).
Receipt-hygiene flag (not a content defect): the gate block's "offsets 57 / 191 / 289 in the decoded description" are not reproducible under whitespace-run normalization — I measure 163 / 241 / 334. Verbatim-ness is true regardless; the L1 should cite the reproducible offsets or drop the figures.

## A4. teaches-prefix finding — the ONE required fix (S280, S281)
```
$ awk -F'|' '{printf "%s: [%s]\n", $2, substr($8,1,45)}' realrows.txt
 S279 : [ v42.2's only hook change is systemd-only - i]
 S280 : [ opens: supersedes S021 - re-pin: the hook st]
 S281 : [ opens: supersedes S022 - re-pin: the late ho]
$ grep -c 'opens:' corpus/SOURCES.md → 0   ; registry rows opening `supersedes S0NN` (house style, em dash): 19
```
The census's E04 exemption is satisfied either way (substring `/supersedes S[0-9]{3}/`; proven by run A2 rc 0). But the round contract letter — "teaches opens 'supersedes S021 -' / 'supersedes S022 -'" — and the register's own 19-row house pattern both open the cell at `supersedes`, with no `opens: ` prefix anywhere in the current 278-row registry. The scribe flagged this themselves (draft schema note #3) and left it to the L1. **Required before landing: strip `opens: ` from both teaches cells** (optionally restore the house em dash: `supersedes S021 — re-pin: …`). Census-neutral; contract-letter-restoring.

## A5. FINAL VERDICTS
| Row | Verdict | Basis |
|---|---|---|
| S279 | **ADMIT** | Scope/anchor/teaches fully grounded in the live body (§1a, §A3); URL new to registry (no E04/W04); NF 13; quotes pass §3; id free; used-by = frozen predicate. Scope note: teaches' closing clause "a busybox-hook host gains nothing from v42.2" is scoped to the release's own complete changelog (one hook bullet, install/systemd) — defensible, keep as written. |
| S280 | **ADMIT conditional on stripping the `opens: ` teaches prefix** | Line 4 ✓; master == pin 3c011dc; master byte-identical to installed limine-mkinitcpio-hook 1.40.0-2 (cmp rc 0, sha equal — measured by both seats); census rc 0 with the row (probe S284 + run A2). Flip to REJECT only if landed with the `opens: ` prefix against the contract letter, or if host/upstream bytes drift before integration (re-verify `cmp`, sha `eeac1ed3…`). |
| S281 | **ADMIT conditional on stripping the `opens: ` teaches prefix** | Line 11 ✓; main == pin df08850; fetched bytes identical to installed plymouth 26.134.222-3 hook (cmp rc 0, sha equal — both seats); census rc 0 (probe S286 + run A2). Same flip conditions (sha `de852646…`). |

L1 landing sequence (all pre-proved): CR-strip (E1) → paste ONLY the three fenced rows directly after S278 → strip the two `opens: ` prefixes → land `corpus/knowledge/mkinitcpio42-onrelease-r64.md` with-or-before → restate C1's W04 figure as 44-after-landing → `census validate <lane>` expect rc 0, 0 E, 44 W04.

— R2Sources
