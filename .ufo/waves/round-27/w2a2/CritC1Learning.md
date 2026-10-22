# CritC1Learning — round 27, attempt 2, wave 2: attack on C1 as the round's learning claim

Verdict: partly holds. At 099c7b3f42d073203d9448807860f04c175eccd7, C1 changes what the lane knows. It adds the taint mechanism, the decoding of 12288, the per-module reading, the fact that taint persists, and the reporting consequence. None of these is in the base 3beab8dd. The "new frontier" overclaim is properly withdrawn. The learning is narrower than the landed text suggests, though, and has four defects:

- The JSON and Markdown companions disagree on KT6, which breaks the round's own new rule, QUALITY 67.
- The operational SKILL.md driver row still teaches "unsigned".
- The automated census is unchanged, so the lane cannot detect a new taint bit except by hand.
- The most useful host conclusion, that E is permanent here and MOK enrolment does nothing, is attributed to a wave-1 critic, not to a source.

The SCORECARD outcome may say "deeper sourced Core ground, depth 8 to 8". It may not say "new area", "census detects taint", or "cause of E established".

## Findings

1. [obs] What is new at the tip, compared with base 3beab8dd. I ran a read-only ripgrep sweep over the exported base tree (`/fast/scratch/hyaku/tsuku27a2/CritC1Learning/base/`: `SKILL.md`, `PROVINCE.md`, `corpus/README.md`, `corpus/knowledge/`, `corpus/SOURCES.md`).
   - Zero lines match any of these: `sig_enforce`, `/sys/module/*/taint`, `12288`, `tainted_mask`, `MODULE_SIG`, `reporting-issues`, `last unloaded`.
   - The only real taint lines at base are symptom records:
     - /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/driver-firmware-plane.md:101-104 (the two journal lines, plus `Tainted: [O]=OOT_MODULE, [E]=UNSIGNED_MODULE`).
     - The same file at :160 ("OOT + unsigned"), :168 ("splat tainted G OE") and :202 ("unsigned DKMS + Secure Boot off is internally consistent").
     - SKILL.md:49 ("taint OOT + unsigned").
   - `git diff --stat 3beab8dd 099c7b3f` shows that C1 adds:
     - `corpus/knowledge/kernel-taint-r27.md` (+39) and `.json` (+227);
     - SKILL.md (+18, all of it the section at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md:2420-2436);
     - `corpus/README.md` (+8, at :250-256);
     - `driver-firmware-plane.md` (+4, the note at :309-311);
     - SOURCES S140 to S145, and the Gate in `corpus/lessons/round-27.md`.
   - New knowledge, then:
     - 12288 = O (bit 12) + E (bit 13), with no W, D or L bit.
     - O is set when the `intree` modinfo tag is missing (S143 main.c:2575).
     - E means the signature was not accepted. A module with an unavailable key still loads in permissive mode (S144 signing.c:107, S145 module-signing.rst:57).
     - `/sys/module/<name>/taint` names the module behind each letter (main.c:1083, :198).
     - Taint is never cleared while the kernel runs (S140 :12, S141 panic.c:129, :959).
     - Tainted reports are often ignored upstream (S140 :8).
   - This is real depth learning inside the Core driver and firmware surface. Impacted axis: depth.

2. [obs] The relabel holds as landed.
   - /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:1012-1013 withdraws "new PROVINCE frontier area".
   - `corpus/README.md:256` reads "deeper ground inside the existing driver and firmware Core area".
   - The PROVINCE.md diff from base to tip contains only the C2 section (`PROVINCE.md:178`, `## Adjacent — mori userspace OOM killers (round 27)`), and no C1 paragraph, so there is no second authority beside Core.
   - QUALITY 68 (`corpus/QUALITY.md:136`) and the lesson row R27-DECLARED-FRONTIER-OVERCLAIM (`corpus/lessons/round-27.md:53`) record the miss.
   - [obs] The declaration table cell at SCORECARD.md:995 still reads "new PROVINCE frontier area". It is withdrawn only by the appended refinement. That is acceptable under append-only rules, but the outcome must quote the refinement, not the table.

3. [obs] Stale authority left in place (defect). The supersession note covers only `driver-firmware-plane.md` lines 160 and 202.
   - The note at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/driver-firmware-plane.md:311 begins "Lines 160 and 202 above call the nvidia modules \"unsigned\"".
   - At the tip, the census plane row at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md:49 still says "taint OOT + unsigned (Secure Boot off, EFI var first byte 0)". It has no note, and nothing in the tree points to "SKILL.md:49" (`rg 'SKILL.md:49'` over corpus, SKILL.md and round-27 evidence matches only the wave-1 report).
   - Wave-1 CritLearningFrontier finding 4 named this exact line (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w1/CritLearningFrontier.md:25).
   - The capture shows the signer `DKMS module signing key` 4 times (`rg -c` → 4 on capture.txt).
   - Counterexample: an operator who reads only the census table, which is the lane's operational surface, still learns the withdrawn reading "unsigned".
   - Impacted axes: freshness and depth (two authorities disagree).
   - Smallest correction: append one sentence after the SKILL.md plane table, or inside `## Kernel taint — round 27`: "SKILL.md:49 'unsigned' reads 'signature not verified by the kernel' (KT3)". The C2 counter does not read SKILL.md, so separability holds.

4. [obs] The JSON and Markdown companions disagree (defect, and against this round's QUALITY 67).
   - /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/kernel-taint-r27.md:23 gives KT6 the verdict "DEGRADED (reporting limit, not host damage)".
   - The JSON companion gives KT6 `"verdict" : "HEALTHY"`, and SKILL.md:2431 reads "(HEALTHY; reporting limit only)".
   - kernel-taint-r27.md:33 keeps "or send the tainted report to the out-of-tree module's maintainer first". That clause is the unsourced routing that wave-1 finding 10 flagged. It is absent from the JSON KT6 action and from SKILL.md, and S140, the only source KT6 cites, contains no routing advice (wave-1 report line 66).
   - Both files landed in one commit, b1647ff (`git log` on the two paths shows only that commit). The .md header says "a correction to a row is appended to both files" (kernel-taint-r27.md:6). QUALITY 67 (`corpus/QUALITY.md:135`) requires the same.
   - The counter cannot see this: `tools/check-kernel-taint.py:748` reads the .md only through `id_in_line(entry_md_text, row_id)`. So `verified_rows 6` coexists with a contradictory companion.
   - Impacted axes: depth (sourcing) and calibration (verdict identity).
   - Smallest correction: append a correction to the .md that sets KT6 to HEALTHY as the JSON and SKILL say, and withdraw the maintainer clause or mark it [inf].

5. [obs] What the lane can do: only a manual procedure changed, not automation.
   - `diff base/tools/tsukuroi-census.sh tree/tools/tsukuroi-census.sh` exit 0: the census is identical. The drivers plane checks the kernel ring, nvidia-smi, lsmod and /dev nodes (census.sh:127-139), not `/proc/sys/kernel/tainted`.
   - No lane tool except the counter mentions `tainted`.
   - KT1's action, "any additional bit is a new event", is therefore an operator or agent step from SKILL.md:2426, not a census verdict.
   - [inf] This is a tradeoff, not a defect: the declaration scoped C1 to the entry (SCORECARD.md:995-1000). The outcome must not claim the census detects or reports taint.

6. [obs] The most useful host conclusion has borrowed provenance (ceiling, and partly false provenance).
   - The JSON KT3 action supports "enrolling the DKMS key may change nothing" with "wave-1 CritLearningFrontier reports that with Secure Boot off the kernel does not load MOK keys at all (an unregistered reading of Linux v7.2 security/integrity code, not a source row of this entry)".
   - KT5's statement likewise carries "[unverified: wave-1 critic finding, not a source row of this entry]".
   - The .md says it does not claim "whether Secure Boot is on now" (kernel-taint-r27.md:36), and the driver note says the Secure Boot reading "was not re-checked in round 27" (driver-firmware-plane.md:311).
   - My read-only host reads at 2026-10-22 about 17:50Z:
     - `od -An -tu1 /sys/firmware/efi/efivars/SecureBoot-8be4df61-93ca-11d2-aa0d-00e098032b8c` prints `6 0 0 0 0`. The first data byte is 0, so Secure Boot is off.
     - `cat /proc/sys/kernel/tainted` prints `12288`.
   - So the conclusion that matters to the operator is: E is permanent on this host as configured, and MOK enrolment alone is inert. The lane can state it only as a hedge cited to a critic seat. A critic report is not a source.
   - Impacted axes: depth and calibration.
   - Smallest correction (for a later round, not this count): register `security/integrity/platform_certs/load_uefi.c`, `keyring_handler.c` and `machine_keyring.c` at v7.2 as tier A sources, with Gate quotes. Until then, KT3 stays UNVERIFIED and the outcome must not say the cause of E is established.

7. [obs] KT4 states the DKMS build link as fact.
   - The KT4 `host_reading` in the JSON, and kernel-taint-r27.md:22, say the modules were "built on the host by dkms 3.4.4-1 from nvidia-open-dkms 615.78.08-1 (pacman -Q)".
   - The capture has only `pacman -Q` versions at capture.txt:121-125 (`linux 7.2.11.arch1-1`, `dkms 3.4.4-1`, `nvidia-open-dkms 615.78.08-1`, `nvidia-utils 615.78.08-1`). That proves the packages are installed, not that this build came from them.
   - The lesson admits the DKMS and PKGBUILD sources were not opened (`corpus/lessons/round-27.md:31`). Wave-1 finding 13 asked for [inf], and it was not applied.
   - Impacted axis: depth (sourcing).
   - Smallest correction: mark the build link [inf] in both companions.

8. [obs] KT1's action names a tool the host does not have.
   - The KT1 action in the JSON says to decode "with the tainted-kernels table or `tools/debugging/kernel-chktaint`".
   - `command -v kernel-chktaint` exits 1.
   - `pacman -Ql linux` lists 7749 lines, with 0 matching `chktaint` (rg exit 1). `pacman -Ql linux-headers` (installed 7.2.11.arch1-1) also has 0 matches.
   - The lesson says the script "was not opened" (`corpus/lessons/round-27.md:31`). SKILL.md:2426 correctly cites only the S140 table.
   - Impacted axis: operability (minor).
   - Smallest correction: drop the script from the action, or say it is in the kernel source tree only.

9. [inf] What `verified_rows 6` proves. Under the declared rule (SCORECARD.md:1000), the counter proves anchoring:
   - a quote is a substring of a pinned snapshot and equals a Gate cell;
   - capture pointers are unique;
   - each id is a SKILL row.

   It does not prove that a statement, verdict or action is correct, or that the companions agree (finding 4). The learning claim therefore rests on the row reviewers, not on the count. The count itself is not in dispute here: the L1's attempt-2 receipts report exit 0 and 6, and I did not rerun them.

10. [inf] What the SCORECARD outcome may honestly say. The smallest truthful wording:
    - "C1 met: `verified_rows` 6, exit 0, at 099c7b3f. Learning: deeper, sourced ground inside the existing Core driver and firmware area: mechanism, decoding of 12288, per-module reading, persistence and reporting consequence. Not new ground: the taint lines were recorded on 2026-10-13 at driver-firmware-plane.md:101-104."
    - "Supersedes the 'unsigned' wording at driver-firmware-plane.md:160 and :202 by an appended note." Add SKILL.md:49 only once finding 3's note lands.
    - "Depth stays 8; no ordinal change."
    - "KT3's cause of E remains UNVERIFIED. The MOK-inert reading is unregistered. The census does not read taint."

    It must not say:
    - "new frontier" or "new area";
    - "the lane now detects new taint" (as a census capability);
    - "the modules are signed by a key MOK enrolment would fix";
    - "the entry and its companion agree", until finding 4 is corrected.

## Smallest safe corrections (summary)

- Append to kernel-taint-r27.md: KT6 is HEALTHY (as in the JSON and SKILL), and withdraw the maintainer-routing clause at :33 or mark it [inf] (QUALITY 67).
- Append a note that SKILL.md:49 "unsigned" means "signature not verified by the kernel" (KT3).
- Mark the KT4 DKMS build link [inf] in both companions. Remove or qualify `kernel-chktaint` in the KT1 action.
- Outcome wording as in finding 10. No change to the count is needed or justified.

Scope: read=SCORECARD.md:980-1020, .ufo/waves/round-27/w1/CritLearningFrontier.md, git diff 3beab8dd..099c7b3f of SKILL.md, PROVINCE.md, corpus/README.md, corpus/knowledge/driver-firmware-plane.md, corpus/knowledge/kernel-taint-r27.md, corpus/QUALITY.md, corpus/lessons/round-27.md, corpus/SOURCES.md and SCORECARD.md; exported trees at base and tip (kernel-taint-r27.md and .json, driver-firmware-plane.md:85-311, SKILL.md:49 and :2420-2436, tools/check-kernel-taint.py:515-534 and :748, tools/tsukuroi-census.sh, capture.txt:119-126), /fast/scratch/hyaku/tsuku27a2/measure-start/census.txt; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w2a2/CritC1Learning.md, /fast/scratch/hyaku/tsuku27a2/CritC1Learning/ (base and tip exports, diff extracts, pacman-ql-linux.txt); executed=read-only git log, diff, diff --stat and archive against the lane; tar extract into scratch; rg sweeps of the base and tip exports; python3 read-only JSON dump; diff of census.sh base vs tip (exit 0); od of the SecureBoot efivar (6 0 0 0 0); cat /proc/sys/kernel/tainted (12288); pacman -Ql linux, pacman -Ql linux-headers, pacman -Q linux-headers; command -v kernel-chktaint (exit 1)
Model: cursor/default (Auto); exact model not exposed
Installs: none
