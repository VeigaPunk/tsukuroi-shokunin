# RevRowKT1 — row KT1 review (decoding of 12288, W/D/L absence)

Verdict: partly holds. Every numeric and letter claim in KT1 is correct, and the "no other bit" claim is exact; one sentence narrows the documented meaning of bit 7 (D) by dropping the BUG branch, and that narrowing is repeated in the .md row and in both SKILL.md cells.

## Sentence-by-sentence

### JSON statement sentence 1 (holds)
"/proc/sys/kernel/tainted prints the kernel's taint mask as a decimal number; 0 means untainted and every set bit names one reason."
- "0 means untainted": S140.rst lines 51-52 ("If that returns ``0``, the kernel is not tainted; any other number indicates the reasons why it is."). Hold.
- Bitfield, one bit per reason: S140.rst lines 71-73 ("as it is a bitfield, where each bit indicates the absence or presence of a particular type of taint"). Hold.
- "decimal number": S141.c lines 96-108 show proc_taint calls proc_doulongvec_minmax on an unsigned long, which renders base 10; S140's own decode example prints "Raw taint value as int/string: 4609" (line 67). Hold, marked [inf] here only because no snapshot sentence says the word "decimal"; the mechanism is in the committed code.
- Live confirmation: `cat /proc/sys/kernel/tainted` printed `12288` on this host at review time, exit 0, and uname -r is 7.2.11-arch1-1.

### JSON statement sentence 2 (holds)
"12288 is 4096 + 8192: bit 12 (letter O, an externally-built or out-of-tree module was loaded) and bit 13 (letter E, an unsigned module was loaded in a kernel that supports module signatures)."
- Arithmetic: 4096 + 8192 = 12288; the bit loop prints exactly bits 12 and 13. Capture line 11 is the token `12288` (capture.txt:11) and is the unique occurrence of that line in the capture (lines 1-138 inspected).
- Bit numbers: S142.h line 83 `#define TAINT_OOT_MODULE 12` and line 84 `#define TAINT_UNSIGNED_MODULE 13`; same values in the S140 table (lines 97-98: 12 _/O 4096, 13 _/E 8192). Hold.
- Letter mapping: S140 lines 97-98 and S141.c lines 821-822 (TAINT_FLAG(OOT_MODULE, 'O'), TAINT_FLAG(UNSIGNED_MODULE, 'E')). Hold.
- O reason text: S140 line 97 "externally-built ("out-of-tree") module was loaded" and line 171. The row's "externally-built or out-of-tree" renders the source's one reason ("out-of-tree" glosses "externally-built") as two alternatives. Cosmetically clumsy, not false: either reading lands on the same fact. [obs]
- E reason text: S140 line 98 "unsigned module was loaded" and lines 173-174 "`E`` if an unsigned module has been loaded in a kernel supporting module signature." The row's wording is faithful. Hold.
- The capture pointer named by the row (line 11, token "12288") is exactly the line that carries the value; the pointer is honest.

### JSON statement sentence 3 (partly overstates)
"No other bit is set, so this boot has recorded none of the other events the mask tracks, for example a kernel warning (W, bit 9), an oops (D, bit 7) or a soft lockup (L, bit 14)."
- "No other bit is set": arithmetic fact (12288 - 4096 - 8192 = 0); S142.h lines 83-91 show the mask spans bits 0-19 (TAINT_FLAGS_COUNT 20), and the S140 table names all twenty. Hold.
- "none of the other events the mask tracks": the tainted value is per-boot because the mask lives in the running kernel, and bit 0 (G/P) unset is consistent with the capture showing only the four nvidia Dual MIT/GPL modules (capture.txt lines 14-17, 51-52, 70-71, 89-90, 108-109). Hold.
- W (bit 9): S140 line 94 "_/W 512 kernel issued warning" and line 163 "W if a warning has previously been issued by the kernel." Hold, and bit 9 unset rules warnings out even though line 164 notes some warnings set more specific flags — those flags are unset too.
- D (bit 7): S140 line 92 says "kernel died recently, i.e. there was an OOPS or BUG"; line 159 repeats "D if the kernel has died recently, i.e. there was an OOPS or BUG." The row says only "an oops" and drops the BUG branch — QUALITY 66 requires keeping every branch the source states. Overstate-by-narrowing.
  - Corrected wording for the JSON sentence: "...a kernel warning (W, bit 9), an oops or BUG (D, bit 7) or a soft lockup (L, bit 14)."
- L (bit 14): S140 line 99 "_/L 16384 soft lockup occurred" and line 176 "L if a soft lockup has previously occurred on the system." Hold.
- "this boot": honest — the mask resets with the kernel, so "recorded none" is only about the current boot, which is what the sentence says.

### JSON statement sentence 4 (holds)
"The kernel's label for E is 'unsigned module'; on this host the modules carry a signature the kernel does not trust (KT3), so the label means 'not verified', not 'no signature'."
- Kernel's own descriptor: S141.c line 822 (UNSIGNED_MODULE → 'E', desc stringified) and the capture journal line 137 "nvidia: module verification failed: signature and/or required key missing - tainting kernel" emitted by S143.c lines 2606-2610, where `!mod->sig_ok` sets TAINT_UNSIGNED_MODULE. Hold.
- "carry a signature": capture lines 54-55, 73-74, 92-93, 111-112 (modinfo -F signer = "DKMS module signing key" for all four modules). Hold.

### host_reading, verdict, action (holds with one fix in the action)
- host_reading "tainted = 12288 at 2026-10-22T15:55:13Z, kernel 7.2.11-arch1-1": capture.txt lines 3, 7, 11. Hold.
- action: "decode it bit by bit with the tainted-kernels table or tools/debugging/kernel-chktaint" is S140 lines 53 and 75-77; "Expect 12288 on this host while the nvidia DKMS modules are loaded" follows because the only taint lines in the boot journal are the two nvidia ones (capture.txt lines 136-137). The tail "W, D or L means a warning, oops or lockup to find in journalctl -k -b 0" repeats the D narrowing; corrected tail: "W, D or L means a warning, an oops or BUG, or a lockup to find in journalctl -k -b 0".

### .md row (partly overstates)
kernel-taint-r27.md line 18: "12288 = bit 12 (O) + bit 13 (E); no other bit, so no warning (W), oops (D) or soft lockup (L) recorded this boot". Same D narrowing.
- Corrected wording: "12288 = bit 12 (O) + bit 13 (E); no other bit, so no warning (W), oops or BUG (D) or soft lockup (L) recorded this boot".

### SKILL.md KT1 row (partly overstates)
SKILL.md line 2426: "Decimal taint mask; 0 is untainted; each set bit is one reason (S140 table). 4096 = O (bit 12), 8192 = E (bit 13) | 12288 = O + E only; no W, D or L this boot (HEALTHY) | Expect 12288 while the nvidia DKMS modules are loaded; any other bit is a new event to look up, and W, D or L sends you to journalctl -k -b 0".
- "12288 = O + E only": arithmetic, and the counter R5 only needs the table line to start with the row id, so the "only" is a true depletion claim about the mask, not an unsourced "only" — passable. [inf]
- The D-branch narrowing appears twice ("no W, D or L this boot" in a decoding cell and "W, D or L sends you to journalctl" in the action cell). Corrected wording: keep the letter triples (they are a shorthand list, not a definition) but the row should not teach that D means only oops; minimal fix is to change the action cell to "W, D or L means a warning, an oops or BUG, or a soft lockup in journalctl -k -b 0".

### Quotes and pointers
- Quote S140 "If that returns ``0``, ..." is verbatim on S140.rst lines 51-52 (location says line 51, the wrap lands on 52 — acceptable line-start location), 19 words, and equals Gate line 15 of corpus/lessons/round-27.md. [obs]
- Quotes S142 "#define TAINT_OOT_MODULE 12" / "#define TAINT_UNSIGNED_MODULE 13" are verbatim on S142.h lines 83/84 with tabs whitespace-normalised away, and equal Gate lines 16-17. [obs]
- Capture pointer line 11 token "12288": unique non-header non-echo non-exit line carrying the token. [obs]

## Residual risk and gaps
- [unk] Whether any bit above 19 could ever print (TAINT_FLAGS_COUNT caps the mask; not reachable).
- [obs] The row's D wording cannot hurt this host's reading (bit 7 is unset either way), but it teaches an incomplete table to a future reader decoding a value that includes bit 7.
- [obs] Counter R2 checks only that the statement is non-empty; the narrowed D text passes the tool either way, so this finding is semantic only.

Scope: read=KT1 row of corpus/knowledge/kernel-taint-r27.json and .md, SKILL.md 2419-2436, SOURCES.md 145-151, lessons/round-27.md 1-56, S140.rst 1-191, S141.c 49-215 and 794-1123, S142.h 69-113, S143.c grep hits, capture.txt 1-138, tools/check-kernel-taint.py and tools/check-self-assessment.py QUALITY regions; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w2a2/RevRowKT1.md; executed=cat /proc/sys/kernel/tainted; printf/bit-loop decode of 12288; uname -r; ls of the w2a2 report directory
Model: devin/swe-2
Installs: none
