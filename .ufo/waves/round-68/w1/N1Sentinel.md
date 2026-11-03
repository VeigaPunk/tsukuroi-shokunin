2026-11-03T22:56:01Z
# N1Sentinel — round 68 / wave w1 scoped findings

Full sweep with every command and its verbatim output: `drafts/c2/N1-boundary.md` (§5b holds the
integration-window capture). Lane HEAD `3f6edcc9` (start = end); fleet HEAD `ce99b22a` → `f812ba6b` (other
lanes only).

Window: dispatch `22:31:21Z`; final wave measurement `22:52:57Z` after **180 s of quiet** (the `22:41:44Z`
lull was not the end — `c1/count-rw-r68.py`, `c1/E2-report.md`, `probes/c1-battery.txt` were rewritten at
`22:44Z`, four more drafts at `22:46Z`, two 71 KB registry drafts at `22:49Z`). 27 files under
`drafts/`+`probes/` (26 measured + this report), 414,816 B total. L1 landing began `22:50-22:51Z`; lane
porcelain 10 → **18** lines by `22:54:51Z`.

## Keys

```
CREDENTIAL_HITS=1            # c2/R2-attack.md:67 — fixture marker `ghp_EXAMPLEFIXTURE…` (32 chars after ghp_, not key material)
PRIV_EXECUTED=0              # prompt-line-restricted re-grep: rc 1, zero matches
PRIV_NAMED=3                 # c1/connector-overlap.md:152, c2/E1-report.md:169, c2/R2-attack.md:84 — all negative assertions
RELATIVE_OFIUFO=135          # per-occurrence, 118 lines / 13 files, drafts only (item step-5 pipeline prints 0: see below)
NEW_FLEET_PATHS=0            # fleet porcelain byte-identical start→end; the 4 lines are the item's .scratch/ carve-outs
NEW_LANE_PATHS=2             # ?? .ufo/waves/round-68/{drafts,probes}/ — both allowed; 0 out-of-scope lane paths
NEW_LANE_PATHS_POST_LANDING=13   # 5 M + 8 ?? at 22:54:51Z, all L1 integration writes on lane integration paths
```

Lane diff start→wave-end added exactly: ` M corpus/lessons/round-67.md`, `?? .ufo/waves/round-68/drafts/`,
`?? .ufo/waves/round-68/probes/`.

## Item correction (step 5)

The pipeline is vacuous: `grep -rn … | grep -v '/home/vgpnk'` drops 100 % of lines, because `grep -n` prefixes
each match with a `/home/vgpnk/…` filename. Corrected: 135 occurrences, 118 lines, 13 files — 86 in the two
71 KB registry drafts (provenance cells), the rest documentation pointers. The 10 that matter are on `$ `
command lines: **9** are cwd-dependent filesystem operands (`c1/E2-report.md` ×1, `c1/SC1-report.md` ×2,
`c1/SC2-report.md` ×4, `c1/sources-rows.md` ×2) and fail when replayed from the fleet root
(`ls /home/vgpnk/Projects/shokunin/.ufo/waves/round-68/drafts/c1/sources-rows.md` → rc 2); 1
(`c1/R1-attack.md:17`) is a `rev:path` git object spec under an absolute `-C`, hence portable.

## Named for the L1 (not defects)

1. **OBS-1 — tracked erratum write, declaration mismatch.** ` M corpus/lessons/round-67.md` (mtime `22:31:39Z`)
   is the **L1's** append-only `## Erratum (round 68)` block (`history://TsukuroiR68` lines 178-187) — no seat
   write, no misroot. But the declaration says the erratum is corrected "in the round-68 lesson" while the
   bytes landed in the round-67 lesson; reconcile the wording. It also moves the census input set, so date the
   before/after census against `22:31:39Z`.
2. **OBS-2 — landing-order hazard, since RESOLVED.** `drafts/c1/note.md:1` cited `S286, S287` while tracked
   `corpus/SOURCES.md` had 285 rows and neither id. At integration the note and both rows landed together:
   registry now 287 rows (S286 line 296, S287 line 297), and `comm -23` of the note's 7 ids against the 287
   registry ids is empty — 0 dangling (my own oracle, not the gate).
3. **OBS-3 — attestation does not transfer to the landed bytes.** Both claim artifacts changed at landing:
   tool `d4390b7a…` → `ada32b13…` (+36/−12 over 6 hunks, and the diff is semantic: `ID = S[0-9]{3,}`
   replaces `\bS\d{3,}\b`, plus a fenced-registry rule and QUALITY 98→101; E1's cited lines `397`/`500` are
   `408`/`524` now), note `1d2a4d8d…` → `71cbc4ef…` (+7/−4, R1's registry-scope paragraph; row count survives
   at 6 `| RWn |` rows, RW1-RW6). Consequence: `probes/c2-selftest.txt` (19/19 PASS) and E1's red-before
   receipt certify the **draft**; the landed gate needs its own `--selftest` run and landed sha256 recorded,
   and C1's counter needs a re-run on the landed note.
4. **OBS-4** — the draft gate's only write-capable calls are its `--selftest` sandbox (`tempfile.mkdtemp`
   408, `shutil.rmtree` 524 landed); production path is git read plumbing only. No `tools/__pycache__`
   appeared (`ls` → No such file or directory), `sys.dont_write_bytecode = True` at line 48. Inherited shape,
   not a new boundary surface.
5. **Hygiene that holds:** append-only during landing (`git diff --stat` = 133 insertions, 0 deletions;
   `corpus/SOURCES.md` 2 insertions, 0 removed lines); no `/tmp` path cited anywhere in the wave
   (`grep -rn '/tmp'` → rc 1); every `git` mutation `-C`-scoped under `/fast/scratch/hyaku/tsukuroi-r68/…`
   with a toplevel guard; E2's and E1's self-attested sha256s match the draft bytes they name.
6. **Not tsukuroi:** fleet-root `MANIFEST.json` and `.ufo/watchdog.log` carry mid-window mtimes (kengaku /
   fleet orchestrator; MANIFEST committed and clean, watchdog.log gitignored at `.gitignore:10`). Fleet commits
   in the window (`cc9c0a6d` kengaku, `0f5a47dc`, `f812ba6b` tabi) touch zero paths under
   `tsukuroi-shokunin`. Sibling `kaidoku/tabi/souji` writes are inside their own repos.
7. **Undeclared but in-surface files:** `drafts/c2/registry-round64-table.md` (71,509 B) and
   `drafts/c2/registry-round68-section.md` (72,493 B) are not in the seat list; both are inside the allowed
   `drafts/` surface and pass all four sweeps.

Read-only throughout: git `status/diff/log/rev-parse/merge-base/cat-file/ls-files/check-ignore`,
`find/stat/sha256sum/grep/sed -n/awk/comm/wc/du/ls/date/file`, one `history://` read. No pacman, no `sudo`,
no service action, no git/jj mutation, no network, no subagent, no background job, no write outside this wave.
