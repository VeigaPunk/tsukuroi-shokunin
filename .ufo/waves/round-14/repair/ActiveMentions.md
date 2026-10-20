# Active Mentions: Value-Domain & Bot Attribution Sweep (Round 14)
author: TsukuroiR14.ActiveMentions; baseline 8606bad4cbc6451ac2890c9f8e2548a36c386db6; 2026-10-20
tools: none installed/updated (existing tools sufficient). Report only; no verification run.

## 1. Bounded sweep commands
```sh
rg -n -C 1 -g '!*.json' -g '!.ufo/**' -e 'the value set is not exhaustive' -e 'ProtectSystem.*exhaustive|exhaustive.*ProtectSystem' -e 'value[ -]domain' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/
rg -n -C 1 -g '!.ufo/**' -e 'self-described.*(model|automated|triage)' -e 'omarchybot' -e '\b(8047|6629|S042|S043|S045)\b' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/
```

## 2. Exact correction loci (active surfaces requiring R14 supersession)
1. **Value-domain defect (R14-VALUE-DOMAIN)**:
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/root-dac-correction-r13.md:97`: table replacement says "the value set is not exhaustive" for ProtectSystem=. Contradicts systemd.exec(5) § ProtectSystem= (S044: "Takes a boolean argument or the special values \"full\" or \"strict\"."). Non-exhaustiveness applies to unit-side mechanisms, not option domain. Superseded in r14 pair.
2. **Bot attribution defect (R14-COMMENT-ATTRIBUTION)**:
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md:48` (S042 teaches): asserts #8047 comment is "self-described model-generated automated triage". Contradicts comment 6071740243, which asserts VM execution and labels Codex Medium a second opinion. S042 row is immutable; superseded by appending S045.
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md:77` (Search log): transferred #6629 disclaimer ("nothing ran on a machine") to #8047. Additive r14 log entry supersedes.
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md:24` (Rule 18): generalized blanket bot triage; superseded by Rule 20 (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md:27`).
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/root-dac-correction-r13.md:171` (QUALITY 18 check): references S042 model triage; qualified by r14 notice.
3. **Active routing pointers (valid technical text, but pointing to r13 files)**:
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md:1721`: routes unit-read-only to `root-dac-correction-r13.md`. (Note: SKILL:1692, 1722, 1725 correctly scope ProtectSystem).
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/README.md:73`: points to r13 correction and cites S042/S043.
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/snapper-eacces-mechanism.md:96`: routes to r13 correction.
   - Recommendation: Append pointer to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/source-scope-correction-r14.md` to these routes without invalidating sound r13 mechanism analysis.

## 3. Preserved history (immutable records — MUST NOT edit in place)
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/root-dac-decision-r12.md:48,58,92` and `.json:87,174`: preserved historical r12 B2 claims under r13 supersession notice.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md:42,43,48`: immutable historical S036, S037, S042 rows.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-12.md:88`, `round-12-verifier-spotcheck.md:145,172`: historical round-12 review.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-13.md:68-70`: historical r13 lesson mentioning bot triage.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-13-verifier-spotcheck.md:143-165,178,236-242`: outside verifier spotcheck routing defects to r14.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/degraded-triage-r4.md:323`: historical r4 triage preserved with D3 erratum.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/LOG.md:542-552,593-599`: immutable historical r13 log entries.

## 4. Safeguards against blanket false conclusions
1. **Valid non-exhaustive mechanism statements**: In `root-dac-correction-r13.md:31,84,102,103,154,170`, `root-dac-correction-r13.json:24,120,157`, and `snapper-eacces-mechanism.md:101`, "non-exhaustive" properly qualifies unit-side mechanisms (BindReadOnlyPaths=, TemporaryFileSystem=, RootDirectory=/RootImage=). These are source-grounded and must NOT be flagged as defective.
2. **Valid #6629 disclaimer**: S043 / comment 6234472369 actually contains "This review is by Claude Opus 5.5 alone." and "Nothing was run on a machine." That comment IS self-described model triage. Only transferring that disclaimer to #8047 is false.
3. **Rejection of #8047 stands**: S042/S045 rejection of #8047 as host cause remains correct (tier C, unverified VM run, maintainer deferral on #6634, reporter wait). Only the stated self-description premise is corrected.
4. **PROVINCE.md clean**: Line 23 routes rollback net to `snapper-eacces-mechanism.md`; contains zero value-domain or bot mentions.

## 5. Concrete recommendations & limitations
- Append top notice to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/root-dac-correction-r13.md` pointing to r14 pair.
- Add S044 (systemd.exec domain quote) and S045 (#8047 attribution quote) to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md` via append-only, leaving S042 unchanged.
- Update routing errata in `SKILL.md`, `corpus/README.md`, and `snapper-eacces-mechanism.md` to reference `source-scope-correction-r14.md` alongside r13.
- Limitations: Scout report only; no verification commands or gate runs performed; no host state or network probed.
