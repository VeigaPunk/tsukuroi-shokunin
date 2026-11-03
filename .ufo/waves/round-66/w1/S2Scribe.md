2026-11-03T21:20:00Z
# S2Scribe — C2-DRAFT (round 66, w1)

Seat: S2Scribe (scribe). Lane: tsukuroi. Base: `c68bfe97e9ed8fda5477fa9ba80f979eaf278fd0`. Lane HEAD at authoring: `aa75398e0d0ae837b438a52b7be5a226633e3b2a` (`git merge-base --is-ancestor c68bfe97 HEAD` → rc 0).

Scope: draft prose only for claim **C2** (adjacency). Two drafts written; no tracked file touched; no git mutation of any kind (read-only verbs only: `rev-parse`, `cat-file`, `show`, `grep`, `log`, `merge-base`, `status`). No sibling repo was written. No tool was installed.

## Files written (both under the lane's wave drafts directory)

| path | what it is |
|---|---|
| `.ufo/waves/round-66/drafts/adjacency-recheck-draft.md` | the draft of the knowledge entry `corpus/knowledge/adjacency-recheck-r66.md` |
| `.ufo/waves/round-66/drafts/erratum-r66-draft.md` | the draft of the append-only `## Erratum (round 66)` block for `corpus/knowledge/adjacency-anchors-r19.md` |

Nothing else was written. Scratch `/fast/scratch/hyaku/tsukuroi-r66/S2Scribe/` held one receipt file and was deleted before this report.

## What the drafts assert, and where each value comes from

### A. `adjacency-recheck-draft.md`

- **Provenance trio** at column 0, in the `source:` / `verified-at:` / `recheck:` order the item names: `source:` names S069 (own-work) plus the systemd v262 release body by sha256; `verified-at: 2026-11-03`; `recheck: 30d; procedure: …` with a steer-safe procedure (no package-manager binary appears in any backticked command — verified by grep over the draft, rc 1).
- **Method paragraph** states all five required elements: live HEAD via `git rev-parse`; blob sha256 via `git show HEAD:PROVINCE.md | sha256sum`; the quote located as the *normalised substring* (strip `**`, strip backticks, collapse whitespace, case-sensitive — markers only, no case/punctuation/entity folding); **the register is authoritative** for the anchor set; and **the anchors' pins are stale by design once a sibling commits**.
- **The 10-row table** uses exactly the claimed columns `| AR<n> | OUT-<nnn> | <sibling> | <live_head> | <blob_sha256> | <status> | <locator> |` and is filled from `drafts/c2-anchors-live.tsv`, which existed when I wrote (tsv mtime 17:59, my read 18:0x), so no cell is `PENDING-RECEIPT`. **Every status cell is the literal word `located`** — the counter depends on it. I re-derived all ten rows independently rather than copying the TSV (commands below); my values agree with the TSV cell for cell.
- **Overlap table** has one row each for **ADJ-02** (kagi, credential helpers), **ADJ-04** (mori, kill/OOM), **ADJ-06** (kaidoku/revenger, shipped-artifact RE) and **ADJ-07** (tameshi, method), each cell set being *tsukuroi retains / recipient / what the systemd boot-credential plane touches*, and each row citing its `PROVINCE.md` ADJ row by id and line (`:47`, `:49`, `:51`, `:52`). **No new recipient is invented**: ADJ-06 keeps PROVINCE.md's own recipient wording "protocol integrator — kaidoku/revenger ownership unresolved".

### B. `erratum-r66-draft.md`

- Headed **exactly** `## Erratum (round 66)`, 11 lines (under the 15-line limit).
- **Quotes the superseded text verbatim** — the whole `:204` IN-109 row is reproduced inside a fenced block, including the `| 2277 |` cell.
- States that the register `corpus/knowledge/adjacency-anchors-r19.json` `inbound[108]` (id `IN-109`) carries `found_line` **2822**, the round-65 re-pin, and names the commit that made it.
- **Does not rewrite the old line** — it names it. The `:204` row and the `:231` `HP-IN-109` row both keep their bytes; the erratum points at the register instead.
- No `source:` / `verified-at:` / `recheck:` line at column 0 is added, so the existing header of `adjacency-anchors-r19.md` stays operative (verified: `grep -nE '^(source|verified-at|recheck):' erratum-r66-draft.md` → 0 matches).

## Evidence (commands, verbatim output, rc)

All read-only. Scratch receipt `/fast/scratch/hyaku/tsukuroi-r66/S2Scribe/receipt.txt` was written during the run and deleted at exit; its content is reproduced below.

### A. Live HEAD per sibling — `git rev-parse HEAD`

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD
84c6cbc3b47c536a504aaee329c77897d389935e
rc=0
$ git -C /home/vgpnk/Projects/shokunin/kama-shokunin rev-parse HEAD
6035e952c2521999e192d6f236331f265ac98392
rc=0
$ git -C /home/vgpnk/Projects/shokunin/kagi-shokunin rev-parse HEAD
91f7752ba551092eef20f6bd43d6dd798dc88ba0
rc=0
$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD
524fa1f90b1f2de44b3019bacf833d54e0af13a0
rc=0
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin rev-parse HEAD
3c369336218329e30248b5d69c41348c02658169
rc=0
$ git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD
c7fe6898e9a8b3ff04486b4a1d672e9db37610c9
rc=0
$ git -C /home/vgpnk/Projects/shokunin/revenger-shokunin rev-parse HEAD
5915ad8d71c19ad377829d130ba1c35445eb32a4
rc=0
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse HEAD
f20ba482c7441d4c75818e7cd8a3165fee7821a1
rc=0
```

### B. Blob digest per sibling — `git show HEAD:PROVINCE.md | sha256sum`

```
mori     2af29312d28727b4dc91236b6f2ce188c0b721a3759e6a8cdaf73f98f4919838  rc=0
kama     f0aaae9ccfd0ecb6641ad1646934f4ff5555fcc45d2e397670b2eb5ff083e8a6  rc=0
kagi     0bbf19b3019e780269259b1acbbd45fcb9a53139fe6337609e7bd6448b364edd  rc=0
mado     01c55ed921b1eb9ebb571f5801525d6c1b49576bf3a1d9a28ca9a4c083943a17  rc=0
kumitate fa9a63a8f62331595858868496c0516df04dfea456b18351d1a01be062ae47ed  rc=0
kaidoku  50b6c259beb6816e26b3af91e44e5317f82e40eaf94993701781221ef7bb98c4  rc=0
revenger c49f6d1d11441728a9a9ed9abed7444837cf2cf0ee569681ad48340187c6f502  rc=0
tameshi  0031aae86d34e39c753ac39ff4daf95a13761f9ba3992f221cc54c6c3bbb5a26  rc=0
```

### C. Quote located at live HEAD — raw-literal `grep -n -F` over `git show HEAD:PROVINCE.md`

```
mori     9:independently labeled user/system journals, plus cgroup `memory.events` and the explicit same-boot journal window after a retained anchor;      rc=0
kama     12:| served-model-id reconciliation | `GET /v1/models` vs `--alias` vs the configured model id |                                             rc=0
kagi     3:**Domain:** secrets & vault ops — the-janitor flows, credential hygiene evidence                                                            rc=0
mado     6:**Owns (surfaces):** `~/.config/hypr/` (hyprland.conf, keybinds, rules,                                                                   rc=0
mori     8:pair); kill/OOM-related catalog-ID records and signal-11 coredump records from                                                             rc=0
kumitate 3:**Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime                                                       rc=0
mori     12:**Refuses:** dispatch and orchestration mechanism (→ kumitate); OS package,                                                              rc=0
kaidoku  3:**Domain:** reverse engineering of shipped artifacts with REA on this Linux                                                               rc=0
revenger 3:Owns: reverse engineering of shipped artifacts — native binaries, managed                                                                 rc=0
tameshi  7:**Owns:** the method, documented from the fleet's existing gates as primary                                                                rc=0
```

An independent whole-set normalised-substring check (NFKC + whitespace collapse, case-sensitive) over each sibling's `git cat-file blob` of `HEAD:PROVINCE.md` reported `LOCATED` for all ten, each at the register's recorded `quote_line` (9, 12, 3, 6, 8, 3, 12, 3, 3, 7). The register-vs-live comparison: **all 8** pins differ from the live HEAD and **all 8** pinned blob digests differ from the live digest (`pin_commit==live? False`, `pin_sha==live_sha? False` for each).

### D. Head object existence — `git cat-file -e <HEAD>` (the discriminator the row-shape regex lacks)

```
mori     rc=0    kagi     rc=0    kumitate rc=0    revenger rc=0
kama     rc=0    mado     rc=0    kaidoku  rc=0    tameshi  rc=0
```

### E. Connector scan of sibling provinces for the boot-credential plane

```
$ for s in mori kama kagi mado kumitate kaidoku revenger tameshi; do git -C ${s}-shokunin show HEAD:PROVINCE.md | grep -ciE 'credentials_boot_policy|boot credential|null key'; done
0  0  0  0  0  0  0  0        (rc=1 each: no match)
```

Sibling declarations that do touch the credential domain (used for the §5 boundary sentences, quoted from live HEAD):

```
$ git -C mori-shokunin show HEAD:PROVINCE.md | grep -n -F 'credential material'
15:endpoint and model-serving health (→ kama); credential material (→ kagi).
68:| kagi | Owns secrets, vault operations, and credential-hygiene evidence; mori never reads or reports credential material. | ...
$ git -C tameshi-shokunin show HEAD:PROVINCE.md | grep -n -F 'Credential material'
18:Credential material (→ kagi), endpoint health (→ kama).
$ git -C kagi-shokunin show HEAD:PROVINCE.md | grep -n -F 'secrets & vault ops'
3:**Domain:** secrets & vault ops — the-janitor flows, credential hygiene evidence
```

(rc=0 each.)

### F. Erratum source of truth — register, census line, superseded prose

```
$ python3 -c "import json;d=json.load(open('corpus/knowledge/adjacency-anchors-r19.json'));i=d['inbound'][108];print(i['id'], i['found_line'], i['classification'], i['scope'])"
IN-109 2822 DRIFTED operative
rc=0

$ git -C tsukuroi-shokunin show HEAD:tools/tsukuroi-census.sh | grep -n "check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED"
2822:  check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED \
rc=0

$ sed -n '204p' corpus/knowledge/adjacency-anchors-r19.md
| IN-109 | `tameshi:corpus/knowledge/service-optin-protocol.md:153` | `tools/tsukuroi-census.sh:915-970` | operative | DRIFTED | 2277 | check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED |
rc=0

$ grep -c '^## Erratum (round 66)' corpus/knowledge/adjacency-anchors-r19.md
0
rc=1   (no erratum yet at HEAD)
```

Round-65 re-pin commit, from its own message:

```
$ git log --oneline -- corpus/knowledge/adjacency-anchors-r19.json | head -1
cecc9e3e round-65: repair - … adjacency IN-109 found_line 2683->2822 re-pinned to the arm-shifted case line (INBOUND-CLASSIFICATION-WRONG at tip) …
$ git rev-parse cecc9e3e
cecc9e3e7fc7c91dddfd3b0fe5d3955d9eebb477
```

### G. Draft self-checks (shape, not gates)

```
$ grep -cE '^\| AR[0-9]+ \| OUT-0[0-9]{2} \| [a-z]+ \| [0-9a-f]{40} \| [0-9a-f]{64} \| located \|' .ufo/waves/round-66/drafts/adjacency-recheck-draft.md
10
$ grep -nE '^(source|verified-at|recheck):' .ufo/waves/round-66/drafts/adjacency-recheck-draft.md
1:source: …
2:verified-at: 2026-11-03
3:recheck: 30d; procedure: …
$ grep -cE 'pacman|checkupdates|\byay\b|\bparu\b|mkinitcpio|limine-update' .ufo/waves/round-66/drafts/adjacency-recheck-draft.md .ufo/waves/round-66/drafts/erratum-r66-draft.md
0   (rc=1: none)
$ wc -l < .ufo/waves/round-66/drafts/erratum-r66-draft.md
11
```

## Conflicts, verbatim

- **None with sibling seats.** The C2Connector overlap scan (`drafts/overlap-scan-r66.md`) reports the same eight live HEADs and the same eight blob digests, and its Grep A finds 0 hits for the boot-credential plane in every sibling `PROVINCE.md` — the same reading my own scan (§E) reached. The R2RevC2 reviewer independently re-derived AR4/AR6/AR8 with a different method (`git grep -F … HEAD -- PROVINCE.md`) and returned `C2-LOCATORS-AGREE`, no DISAGREE.
- **One finding I carried into the draft rather than hiding:** R2RevC2 Attack 4 shows the frozen row-shape regex is shape-only — three fabricated rows with non-existent HEADs (`1111…1`, `0000…0`, `1234567890abcdef…`) match it and score `grep -c` = 3. I therefore did not treat the regex as evidence in the note: §2 step 6 records the `git cat-file -e` existence check (rc=0 for all eight distinct heads) and the quote re-location as the two independent discriminators, and §6's limits say plainly that the register's round-19 pins and the live values differ for all eight siblings and that this entry re-pins nothing.
- **One observation, not a conflict:** the item's erratum brief describes the `:204` IN-109 row as reading `| 2277 |` "in the line-range column". In the landed file the `:204` row's columns are `Id | Sibling file:line | Pointer target | Scope | Class | Found line | Evidence quote`, so `2277` is in the **Found line** column and `915-970` is the **Pointer target** (the line range). I drafted the erratum to quote the row **verbatim in full**, so the superseding text is exact regardless of which column is meant, and I named the stale cell by its literal contents (`| 2277 |`) rather than by a column label that the landed schema does not use. If the L1 reads the brief's "line-range column" as naming the `915-970` cell instead, the row-quote still stands; the cell that is actually stale is `2277`, and `915-970` remains the register's own `target_ranges` value, unchanged by the r65 re-pin.
- **Not mine to settle, flagged for the L1:** the C2 note's `source:` line names S283 for the v262 semantics, but S283 is a row the *C1* seat's draft (`drafts/s283-row-draft.md`) proposes to land with `used-by` = `corpus/knowledge/systemd262-credentials-boot-policy-r66.md`, not with my C2 note. My note cites the same upstream document by its own sha256 (`008e1265…babce0b`), so the citation is self-standing; if the L1 prefers the C2 note to rest on a registry row, the natural fix is to add the C2 note to S283's `used-by` cell in the same landing (the census's E11 check only requires that a named `used-by` path exists on disk, which it will).

## Out of scope for this seat

- No tracked file was created, edited or deleted: `corpus/knowledge/adjacency-recheck-r66.md` and the `## Erratum (round 66)` block in `corpus/knowledge/adjacency-anchors-r19.md` are **drafts for the L1 to land**; the L1 also fills the note's final values from the receipts.
- No lane gate was run (the L1 runs the census, `check-adjacency-anchors.py`, `check-knowledge-header.py` and the row counter at integration).
- The host values of the boot-credential plane belong to C1's note and receipts; this draft states ownership boundaries only and does not restate or re-judge those measurements.
- No `SOURCES.md` row was written (C1's row draft covers S283), no sibling repo was touched, no git index, branch, stash or worktree was mutated, no sudo/pacman/systemctl/journalctl action was taken.

## Checks the L1 should run at integration

1. `grep -cE '^\| AR[0-9]+ \| OUT-0[0-9]{2} \| [a-z]+ \| [0-9a-f]{40} \| [0-9a-f]{64} \| located \|' corpus/knowledge/adjacency-recheck-r66.md` → **10**.
2. `grep -c '^## Erratum (round 66)' corpus/knowledge/adjacency-anchors-r19.md` → **1**, and `sed -n '204p'` → the row still reads `| 2277 |` (the old line is named, not rewritten).
3. `python3 tools/check-adjacency-anchors.py --revision <REV>` → PASS (the register's `inbound[108].found_line` 2822 is what the gate reads; the prose erratum must not contradict it).
4. `python3 tools/check-knowledge-header.py` → PASS for the new note (its `source:`/`verified-at:`/`recheck:` trio is at column 0, outside fences, with an ISO date and a `30d` cadence).
5. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → 0 E-codes (E11 fires for S283 until the C1 note lands; the note and the row must land together).
