# RevRowKT2 — round 27, attempt 2, falsify wave 2 — row KT2 (the out-of-tree taint O and the one-time message)

Verdict: **partly holds** — the mechanism (O is set at load when modinfo lacks the `intree` tag), the warning text, the recording of bit 12 kernel-wide and per module, both capture pointers, the host reading, the HEALTHY verdict and the read-only action all check out against the committed snapshots and the capture; four wording defects survive: the "only" claim rests on a guard line the row never quotes, "first such module" overstates the guard's condition and omits the sysctl-write branch that can set bit 12 without any module load, sentence 1 asserts an ungrounded tag-to-build-location equivalence, and the .md line drops the [inf] marker the JSON carries on the DKMS sentence.

Identity check [obs]: every file cited below is byte-identical between the working tree and the revision under attack 099c7b3f42d073203d9448807860f04c175eccd7. I compared `git show <rev>:<path> | sha256sum` with `sha256sum <path>` for corpus/knowledge/kernel-taint-r27.json, corpus/knowledge/kernel-taint-r27.md, SKILL.md, .ufo/waves/round-27/capture/capture.txt and sources S140.rst, S141.c, S142.h, S143.c — all eight reported SAME, so the "committed snapshots" are what I quote. No lane file was modified.

## Findings

1. **Grounding gap behind "only" (medium, QUALITY 66).** The JSON statement says the kernel prints `<module>: loading out-of-tree module taints kernel.` "only for the first such module", but the row's quotes contain only S143 line 2575 (`if (!get_modinfo(info, "intree")) {`), S143 line 2577 (the `pr_warn` format string) and S140 line 171. The line that actually grounds "only" is S143.c:2576, `if (!test_taint(TAINT_OOT_MODULE))`, which is not quoted anywhere in the row. QUALITY 66 (corpus/QUALITY.md:133) says words such as "only" "need a source sentence that says so" — the line exists in the cited source but is absent from the row's evidence. Remedy: add the quote `{"source": "S143", "text": "if (!test_taint(TAINT_OOT_MODULE))", "location": "kernel/module/main.c line 2576"}` to the row's quotes array (S143.c:2576 read from the committed snapshot .ufo/waves/round-27/sources/S143.c).

2. **"First such module" overstates the guard, and the sysctl-write branch is missing (low, QUALITY 66 "a condition with two branches keeps both").** The guard at S143.c:2576 tests the kernel-wide mask: `test_taint` is `return test_bit(flag, &tainted_mask);` (S141.c:935-938), and `add_taint` sets that mask (S141.c:959). Bit 12 can therefore become set without any module load: the `/proc/sys/kernel/tainted` write handler adds every requested bit (`add_taint(i, LOCKDEP_STILL_OK);` inside the per-bit loop, S141.c:128-129). In that corner the boot's first genuine out-of-tree module loads silently, so "prints ... only for the first such module" is not exact; the exact condition is "prints while bit 12 is still clear kernel-wide". The same write path is a second branch of the row's own question ("when does the kernel set it?") that the statement omits entirely. Remedy: reword as in the corrected wording below and add S141 to the row's sources for that sentence (S141 is already a registered source of this entry, used by KT1).

3. **Ungrounded equivalence in sentence 1 (low).** "that is, when the module was built outside the kernel tree" states, as fact, that tag absence equals out-of-tree build. The kernel-side source tests only the tag (S143.c:2575); S140 line 171 describes the resulting event ("an externally-built (\"out-of-tree\") module has been loaded"), not the tagging mechanism; and no mined source states how the tag gets onto in-tree modules (the modpost side was never mined — the planned scribe seats for a dkms README and an Arch PKGBUILD, S150/S151, died in wave 1 and never landed). The kernel cannot observe where a file was built; it observes one modinfo string. This is exactly the R26-DRAFT-DRIFT pattern QUALITY 66 names. Remedy: keep the tag test as the fact and mark the build-location link [inf], per the corrected wording below.

4. **The .md line hardens and unmarks the DKMS inference (low).** JSON KT2 marks the DKMS sentence honestly: "carry no `intree` tag [inf: DKMS builds outside the kernel tree; not checked by a source row this round]". The .md row (corpus/knowledge/kernel-taint-r27.md:19) states "DKMS modules are out-of-tree by construction" with no [inf] marker and a stronger modal claim ("by construction"). Nothing host-side was observed either: the capture queries only filename, version, license, signer and vermagic for the four modules (capture lines 45-58, 64-77, 83-96, 102-115) and never asks for an `intree` field. Remedy: reword the .md cell as given below.

5. **SKILL.md row carries the same imprecision (info).** SKILL.md:2427 says "the message prints once, for the first such module (S143)" — same two problems as findings 1 and 2 in compressed form. SKILL.md:2435 ("first out-of-tree module of the boot set O") is correct as a statement about this host [obs]. Since SKILL.md:2422 defers normative detail to the entry, fixing the entry is sufficient, but the suggested SKILL wording below removes the drift.

## What holds, sentence by sentence

- "At module load the kernel sets O when the module's modinfo lacks the `intree` tag" — holds: S143.c:2575 opens the branch and S143.c:2579 `add_taint_module(mod, TAINT_OOT_MODULE, LOCKDEP_STILL_OK);` sets it; bit 12 is TAINT_OOT_MODULE (S142.h:83), and the message and the taint happen in the module-load path. [obs]
- Message text — holds byte-exact: JSON writes `<module>: loading out-of-tree module taints kernel.`; S143.c:2577-2578 is `pr_warn("%s: loading out-of-tree module taints kernel.\n", mod->name);`; capture line 136 shows `[   17.536700] plazir27 kernel: nvidia: loading out-of-tree module taints kernel.` [obs]
- "records bit 12 both in the kernel-wide mask and in that module's own taint bits" — holds: `add_taint_module` is `add_taint(flag, lockdep_ok); set_bit(flag, &mod->taints);` (S143.c:194-198), the kernel-wide half landing in `tainted_mask` (S141.c:959), and the per-module half is what `/sys/module/<name>/taint` prints (`show_taint` calls `module_flags_taint(mk->mod->taints, ...)`, S143.c:1076-1083); capture lines 14-17 show all four nvidia modules with OE while only nvidia printed the warning (capture 136) — consistent with per-module recording on every such load and one message per boot. [obs]
- The one-time behaviour as observed on this host — holds: exactly one out-of-tree warning in the boot journal (capture 135-138). [obs]
- DKMS sentence in the JSON — holds as a marked inference; the [inf] note and the absence of any `intree` query in the capture are consistent. [inf]
- host_reading — holds: capture 136 gives 17.536700 s of boot 0 for nvidia; capture 46, 65, 84, 103 give the four `/lib/modules/7.2.11-arch1-1/updates/dkms/` filenames. [obs]
- Quote fidelity — holds: all three quote locations resolve exactly (S143.c:2575, S143.c:2577, S140.rst:171, the last being `12) ``O`` if an externally-built ("out-of-tree") module has been loaded.`); the quoted lines carry no trailing whitespace, and dropping leading indentation matches the entry's established convention (KT1 quotes S142.h:83 the same way). [obs]
- Capture pointers — hold: pointer 1 names capture line 136 with token "out-of-tree", pointer 2 names capture line 46 with token "updates/dkms"; both tokens occur on the named lines. [obs]
- Verdict HEALTHY and the action — hold: detection-only, read-only, consistent with KT4's `/sys/module/*/taint` reading. [obs]
- Corroboration bonus: the capture shows the out-of-tree warning before the verification-failed line (136 before 137), matching code order (S143.c:2575 before the signature block later in the same function). [obs]

## Exact corrected wording

JSON KT2 `statement` (drop-in replacement):

"At module load the kernel sets O when the module's modinfo lacks the `intree` tag (S143); S140 describes that event as an externally-built ("out-of-tree") module having been loaded [inf: the kernel tests only the tag; that the tag marks in-tree builds is not stated by a mined source]. It prints `<module>: loading out-of-tree module taints kernel.` only while bit 12 is still clear in the kernel-wide mask, so in practice for the first out-of-tree module of the boot, and it records bit 12 both in the kernel-wide mask and in that module's own taint bits (S143). The same bit can also be set with no module load by writing /proc/sys/kernel/tainted, whose write handler adds every requested bit (S141). Modules built by DKMS from a separate source tree are expected to carry no `intree` tag [inf: DKMS builds outside the kernel tree; not checked by a source row this round; the capture queries no `intree` field]."

JSON KT2 `quotes`, add: `{"source": "S143", "text": "if (!test_taint(TAINT_OOT_MODULE))", "location": "kernel/module/main.c line 2576"}` and `{"source": "S141", "text": "add_taint(i, LOCKDEP_STILL_OK);", "location": "kernel/panic.c line 129"}`; JSON KT2 `sources`, add `"S141"`.

corpus/knowledge/kernel-taint-r27.md:19, reading cell, corrected:

"set at module load when modinfo lacks the `intree` tag; nvidia printed `loading out-of-tree module taints kernel.` at 17.5 s of boot 0; DKMS modules are expected to lack the tag [inf: dkms builds outside the kernel tree]"

SKILL.md:2427, how-to-read cell, corrected:

"O is set at load when a module lacks the `intree` modinfo tag; the warning prints only while O is still clear kernel-wide — in practice for the first out-of-tree module of the boot (S143)"

## Residual risk and verification gaps

- The DKMS-lacks-the-tag claim stays [inf] in this round: the capture never ran `modinfo -F intree nvidia` (a read-only command that would make it [obs] on the next capture), and no mined source states the tagging mechanism. [unk]
- I did not re-fetch the upstream v7.2 raw URLs; snapshot fidelity to upstream bytes is the RevSrcS140/S143 seats' ground (SOURCES.md rows 146 and 149 register the raw-bytes sha256s I did not recompute against upstream). [unk]
- Whether an out-of-tree build can ship a hand-added `intree` tag (defeating the tag-to-location link) is real kernel behaviour but unmined here; it only reinforces finding 3's wording fix and needs no new branch in the row. [inf]

Scope: read=corpus/knowledge/kernel-taint-r27.json and .md, SKILL.md section at 2420-2436, corpus/SOURCES.md rows 146-151, corpus/QUALITY.md:133, snapshots .ufo/waves/round-27/sources/S140.rst S141.c S142.h S143.c, capture .ufo/waves/round-27/capture/capture.txt, w2a2 dispatch and spec copies; byte-identity of all eight against tip 099c7b3f via git show piped to sha256sum
Model: zai/glm-5.3-flash
Installs: none
