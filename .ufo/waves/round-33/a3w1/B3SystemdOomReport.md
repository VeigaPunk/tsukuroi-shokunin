C2 boundary row complete; exploratory adjacency only; no control result.

1. [obs] Tsukuroi labels this class `kernel OOM killer killed some processes` at `PRIORITY=5`; its row records three messages (event A two, event B one) and explicitly says they report about a named unit, not when a kill happened. The census defines `CLASS_OOM_SYS` with the same text. Evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md:1103`; `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh:173-175,456`.

2. [obs] The source note shows all three records carry `MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef`; it distinguishes the `UNIT` subject from the sender fields and explains the catalog text as a report about the named unit, not evidence of kill timing. Evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/kill-event-deep-r8.md:85-99`.

3. [obs] ADJ-04 keeps OS memory, journal and boot diagnosis with tsukuroi and routes correlation of kill/pressure evidence to mori, requesting capture time, boot/window and exact measurements without asserting wave causation. The lane's round-32 note says its dated kill-cluster handoff line is only `prepared`, not reported, acknowledged, accepted or resolved; tsukuroi retains the OS finding. Evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:49,193`.

4. [obs] At pinned mori revision `24603186b555dddb88ebd607e415e27bdea747b4`, Province declares “structured, MESSAGE-free journal records carrying catalog IDs for kernel-OOM unit notices” (11 words). Its Frontier states event-time kernel attribution and fleet correlation remain frontier. Evidence: `/home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md:24,44` at that revision; SKILL's journal decision-table class is at `SKILL.md:17` at that revision.

5. [inf] The boundary is overlapping evidence with distinct roles: tsukuroi retains the host/systemd interpretation; the ADJ-04 handoff is a correlation request, not a transfer of diagnosis or a causal finding. Mori's scope includes the notice record, but the pinned frontier means this row does not claim completed event-time or fleet attribution. Evidence basis: the boundaries above, especially `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:49,193` and `/home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md:24,44` at the pinned revision.

6. [unk] Whether this specific systemd attribution report was correlated with any fleet wave is unknown; no such execution or correlation receipt was examined. The lane source records only a prepared handoff, not acceptance (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:193`).

7. [obs] Provenance commands and outcomes:
   - `timeout 30 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 24603186b555dddb88ebd607e415e27bdea747b4:PROVINCE.md && timeout 30 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 24603186b555dddb88ebd607e415e27bdea747b4:SKILL.md` printed both pinned files; the tool did not surface an exit status.
   - `timeout 30 git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD` returned `5216d78dd1bc4ce57356555b509c9135a9702088`, different from the requested pin; pinned evidence was therefore read with `git show`.
   - `timeout 30 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 24603186b555dddb88ebd607e415e27bdea747b4:PROVINCE.md | nl -ba` and the same command with `:SKILL.md` printed line-numbered pinned contents.
   - The census search used pattern `kernel OOM killer killed some processes|PRIORITY=5|oom-kill|oom kill` and found the C2 signature at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh:173-175,456`.
   - `timeout 30 mkdir -p /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/B3SystemdOomReport` completed with no output. No tests or runtime checks were run.

8. [obs] Touched surfaces are only the evidence directory and the two requested Markdown artifacts; no lane product code, judge, refs or mori files were changed. Out of scope: C1 control execution, any claim of Mori acceptance, source downloads, or event-time/fleet-cause attribution.

Scope: read=tsukuroi SKILL.md, kill-event-deep-r8.md, PROVINCE.md and census signature; pinned mori PROVINCE.md and SKILL.md; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/B3SystemdOomReport/row.md,/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/B3SystemdOomReport.md; executed=timeout 30 git show (pinned PROVINCE.md and SKILL.md), timeout 30 git rev-parse HEAD, timeout 30 git show | nl -ba (pinned PROVINCE.md and SKILL.md), timeout 30 mkdir -p
Model: openai-codex/gpt-6-luna
Installs: none