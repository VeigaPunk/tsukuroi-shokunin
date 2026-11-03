2026-11-03T23:20:43Z

# S1Scout — C1 independent source re-verification (round 69, w1)

Seat: S1Scout, scout, independent (non-author) re-derivation of every C1 source fact.
Lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin, HEAD `920a9eea3c5c5400567be0e96141014f338973df`
(declaration commit; measured base `acce353bacad74043636018d829e9e9b8e0fdf1c`).
Scratch `/fast/scratch/hyaku/tsukuroi-r69/S1Scout` removed at exit; every retained byte is copied below.

Verdict in one line: both pinned snapshots re-hash to their declared digests, a second route
reproduces both files byte-for-byte, the 0–19 table extracts to 20 rows with numbers exactly `2^bit`,
12288 decodes to bits 12 and 13 only, and the pinned header's composition produces the host vermagic
string including its trailing space.

## 1. Committed snapshots hash to the declared digests

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && sha256sum .ufo/waves/round-69/before/src/tk-v7211.rst .ufo/waves/round-69/before/src/vm-v7211.h
727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841  .ufo/waves/round-69/before/src/tk-v7211.rst
0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea  .ufo/waves/round-69/before/src/vm-v7211.h
rc=0
```

Both digests equal the frozen declaration and `.ufo/waves/round-69/before/src/SHA256SUMS`.
Sizes: `wc -l -c` → tk 191 lines / 9340 bytes, vm 48 lines / 1234 bytes (rc 0).
`before/src/FETCH.txt` records the first route as
`https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/...?h=v7.2.11`, fetched
2026-11-03 by the L1 with `curl -sS --max-time 60`.

## 2. Second route reproduces both files byte-for-byte

```
$ S=/fast/scratch/hyaku/tsukuroi-r69/S1Scout
$ curl -sS --max-time 60 -o "$S/tk.rst" 'https://raw.githubusercontent.com/gregkh/linux/v7.2.11/Documentation/admin-guide/tainted-kernels.rst'
tk_rc=0
$ curl -sS --max-time 60 -o "$S/vm.h" 'https://raw.githubusercontent.com/gregkh/linux/v7.2.11/include/linux/vermagic.h'
vm_rc=0
$ sha256sum "$S/tk.rst" "$S/vm.h"
727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841  /fast/scratch/hyaku/tsukuroi-r69/S1Scout/tk.rst
0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea  /fast/scratch/hyaku/tsukuroi-r69/S1Scout/vm.h
sha_rc=0
$ cmp -s "$S/tk.rst" "$D/tk-v7211.rst"; echo $?   # 0
$ cmp -s "$S/vm.h" "$D/vm-v7211.h"; echo $?       # 0
```

Route independence is host-and-transport independence (raw.githubusercontent.com over HTTPS against
git.kernel.org `plain/`), not tree independence: `gregkh/linux` is the same stable tree the L1 read.
Two independent corroborations that the *bytes* are stable across trees/tags were already in the lane:

```
$ sha256sum .ufo/waves/round-27/sources/S140.rst
727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841  .ufo/waves/round-27/sources/S140.rst
rc=0            # round-27 snapshot, 191 lines, pinned in SOURCES.md S140 at tag v7.2 (torvalds tree)
```

S140 (SOURCES.md:146) pins the same sha256 for `Documentation/admin-guide/tainted-kernels.rst` at
tag **v7.2 in the torvalds tree**, and its snapshot file is byte-identical to the v7.2.11 stable
snapshot here. So the taint document's bytes are unchanged between v7.2 and v7.2.11 and between the
torvalds and stable trees. There is **no** pre-existing SOURCES row pinning
`include/linux/vermagic.h` (`grep -n 'vermagic' corpus/SOURCES.md` matches only S140's line, which
names tainted-kernels.rst); S289 is therefore a genuinely new pin whose only cross-check is the
second route in this receipt.

## 3. Table 0–19 extraction

Layout of the table in `tk-v7211.rst` (verbatim, `cat -A`-checked):

```
line 82  ===  ===  ======  ========================================================
line 83  Bit  Log  Number  Reason that got the kernel tainted
line 84  ===  ===  ======  ========================================================
lines 85-104   20 data rows, bits 0..19 (bit 0 at 85, bit 12 at 97, bit 13 at 98, bit 14 at 99, bit 19 at 104)
line 105 ===  ===  ======  ========================================================
```

Extraction (program written to scratch, `awk -f`, rows 85–104, fields split into
`bit<TAB>log<TAB>number<TAB>reason`; note `log` is an awk builtin, hence single-letter names):

```
$ awk -f "$S/extract.awk" tk-v7211.rst > "$S/taint-table.tsv"; echo "awk_rc=$?"
awk_rc=0
$ wc -l "$S/taint-table.tsv"
20 /fast/scratch/hyaku/tsukuroi-r69/S1Scout/taint-table.tsv
$ sha256sum "$S/taint-table.tsv"
1b10b163ea299c96ac68d12770bd15459b62b687a6017cade84c3837fbed0757  /fast/scratch/hyaku/tsukuroi-r69/S1Scout/taint-table.tsv
```

(`cat -A` sample: `12^I_/O^I4096^Iexternally-built ("out-of-tree") module was loaded$`,
`19^I_/J^I524288^Iuserspace used a mutating debug operation in fwctl$` — TAB-delimited, no trailing
whitespace, rc 0.)

Arithmetic self-check of the Number column, one line per row:

```
$ awk -F'\t' '{p=1; for(i=0;i<$1;i++) p*=2; printf "bit=%s number=%s 2^bit=%d %s\n", $1, $3, p, ($3==p?"OK":"MISMATCH")}' taint-table.tsv
bit=0 number=1 2^bit=1 OK
bit=1 number=2 2^bit=2 OK
...            (20/20 OK)
bit=19 number=524288 2^bit=524288 OK
rc=0
```

The document's own worked example also closes arithmetically: `Raw taint value as int/string:
4609/'P        W  O     '` (line 67) is `$((4096+512+1))` → `4609`, i.e. bit 12 (O) + bit 9 (W) +
bit 0 (P), exactly the three letters the example names. The runtime hint at line 77 iterates
`seq 20`, consistent with a closed 0–19 table.

Copied verbatim to `probes/S1Scout-taint-table.tsv` (20 lines, same digest).

## 4. Quotes for bits 12, 13, 14

| bit | line | quote (verbatim) | words |
|---|---|---|---|
| 12 | 97 | `externally-built ("out-of-tree") module was loaded` | 5 |
| 13 | 98 | `unsigned module was loaded` | 4 |
| 14 | 99 | `soft lockup occurred` | 3 |

Each quote occurs exactly once in the snapshot (`grep -c -F` → 1, rc 0 for all three), and each is
≤ 25 words so it is admissible as a `quote="..."` cell. Checked against the frozen counter's own
rule (`" ".join(quote.split()) in " ".join(text.split())`) — all three match, plus the candidate
quotes below also match and stay ≤ 25 words:

```
words= 4  in=True  proprietary module was loaded                    (line 85)
words= 9  in=True  Raw taint value as int/string: 4609/'P        W  O     '   (line 67)
words=10  in=True  for i in $(seq 20); do echo $(($i-1)) $(($(cat /proc/sys/kernel/tainted)>>($i-1)&1));done   (line 77)
words= 3  in=True  struct randomization plugin                      (line 101)
words= 8  in=True  kernel running on an out of specification system (line 87)
```

## 5. Decode of 12288 under the table

```
$ v=12288; for i in $(seq 0 19); do b=$(( (v >> i) & 1 )); [ "$b" -eq 1 ] && awk -F'\t' -v b="$i" 'NR==b+1 {printf "bit=%s log=%s reason=%s\n", $1, $2, $4}' taint-table.tsv; done
bit=12 log=_/O reason=externally-built ("out-of-tree") module was loaded
bit=13 log=_/E reason=unsigned module was loaded
rc=0
```

`12288 = 4096 + 8192`, and no other bit is set: 0–11 and 14–19 all test 0.

The boot log line agrees, both in bit set and in letter:

```
$ grep -n 'Tainted\|12288' .ufo/waves/round-69/before/host.txt
32:+ echo '## cat /proc/sys/kernel/tainted'
34:+ cat /proc/sys/kernel/tainted
35:12288
49:Nov 02 16:49:24 plazir27 kernel: Tainted: [O]=OOT_MODULE, [E]=UNSIGNED_MODULE
50:Nov 02 16:49:45 plazir27 kernel: Tainted: [O]=OOT_MODULE, [E]=UNSIGNED_MODULE
```

`[O]` is bit 12's log letter and `[E]` is bit 13's (table lines 97, 98) — an exact 2-of-2 match,
with no `[L]`, `[W]`, `[P]`, `[D]` or other letter present, matching the empty bits 0–11 and 14–19.
The causal log lines pin each bit to a distinct event, and the soft-lockup count agrees with bit 14
being clear:

```
$ grep -n 'nvidia: ' host.txt
54:Nov 02 12:07:17 plazir27 kernel: nvidia: loading out-of-tree module taints kernel.                                   -> bit 12
55:Nov 02 12:07:17 plazir27 kernel: nvidia: module verification failed: signature and/or required key missing - tainting kernel -> bit 13
$ grep -ciE 'soft lockup' host.txt   # line 58-59 of the receipt
0                                   -> bit 14 clear, consistent with 12288
```

## 6. vermagic.h composition

Exact definition lines (`grep -n '' vm-v7211.h`):

```
41: #define VERMAGIC_STRING 						\
42: 	UTS_RELEASE " "							\
43: 	MODULE_VERMAGIC_SMP MODULE_VERMAGIC_PREEMPT 			\
44: 	MODULE_VERMAGIC_MODULE_UNLOAD MODULE_VERMAGIC_MODVERSIONS	\
45: 	MODULE_ARCH_VERMAGIC						\
46: 	MODULE_RANDSTRUCT
```

Component macros and their conditional values, with the config symbols each `#ifdef` reads:

| component | lines | condition read | value when set | value when clear |
|---|---|---|---|---|
| `MODULE_VERMAGIC_SMP` | 13–17 | `CONFIG_SMP` | `"SMP "` | `""` |
| `MODULE_VERMAGIC_PREEMPT` | 18–24 | `CONFIG_PREEMPT_RT` then `CONFIG_PREEMPT_BUILD` | `"preempt_rt "` / `"preempt "` | `""` |
| `MODULE_VERMAGIC_MODULE_UNLOAD` | 25–29 | `CONFIG_MODULE_UNLOAD` | `"mod_unload "` | `""` |
| `MODULE_VERMAGIC_MODVERSIONS` | 30–34 | `CONFIG_MODVERSIONS` | `"modversions "` | `""` |
| `MODULE_RANDSTRUCT` | 35–39 | `RANDSTRUCT` (randstruct plugin, with `RANDSTRUCT_HASHED_SEED`) | `"RANDSTRUCT_" RANDSTRUCT_HASHED_SEED` | empty |
| `MODULE_ARCH_VERMAGIC` | — | comes from `<asm/vermagic.h>` (include at line 10) | arch-defined | arch-defined |
| `UTS_RELEASE` | — | `" "` literal at line 42; value from `<generated/utsrelease.h>` (include at line 9) | `7.2.11-arch1-1` | — |

Composition for `CONFIG_SMP=y`, `CONFIG_PREEMPT_RT` unset, `CONFIG_PREEMPT_BUILD=y`,
`CONFIG_MODULE_UNLOAD=y`, `CONFIG_MODVERSIONS` unset, `RANDSTRUCT` unset, `MODULE_ARCH_VERMAGIC`
empty:

```
"7.2.11-arch1-1" + " " + "SMP " + "preempt " + "mod_unload " + "" + "" + ""
= "7.2.11-arch1-1 SMP preempt mod_unload "
```

The host's own vermagic, byte-checked including the trailing space the composition emits:

```
$ grep -n '7.2.11-arch1-1 SMP' .ufo/waves/round-69/before/host.txt | cat -A
40:7.2.11-arch1-1 SMP preempt mod_unload $
rc=0
```

The `$` (end-of-line marker) sits directly after a space, i.e. the captured module vermagic is
`7.2.11-arch1-1 SMP preempt mod_unload ` — the token order and every token match the composition,
and the trailing space is reproduced rather than trimmed. **Verdict: agrees.**

The two residual components are over-determined by the observed string rather than observed
directly: `MODULE_RANDSTRUCT` must be empty because no `RANDSTRUCT_<seed>` token appears, and
`MODULE_ARCH_VERMAGIC` must be empty because no token appears between `mod_unload` and end of
string (x86's `asm/vermagic.h` is not part of the pinned snapshot set — see unknowns).
`MODULE_VERMAGIC_PREEMPT` selects the `preempt ` branch, so `CONFIG_PREEMPT_BUILD` is set and
`CONFIG_PREEMPT_RT` is not; the observed string carries no `preempt_rt`.

## 7. C1 wiring facts the authoring seats depend on

- `corpus/SOURCES.md` at HEAD `920a9ee` holds **287** registry rows, ids `S001`…`S287` (all 4 chars),
  and **no** `S288`/`S289`:

```
$ python3 -c "... re.compile(r' {0,3}\|\s*(S[0-9]{3,})\s*\|') ..."
registry_ids_count= 287 first= S001 last= S287
S288_in= False S289_in= False
digits_widths= [4]
```

  This matches the declaration's control (e) ("S288 and S289 rows 0") and the C1 causal-separability
  sentence ("C1 touches only its note, its two SOURCES rows, the new counter and receipts"). The base
  absence is therefore expected, not a contradiction; but a KR row citing `source=S288|S289` can only
  verify **after** the two rows land in `corpus/SOURCES.md`.

- The counter draft present at `.ufo/waves/round-69/drafts/c2/count-kr-rows-r69.py`
  (sha256 `db2b491700ab7e7686ea84414585fb6e74d3f5e71dcfc7b5903c9815cf3f0c9b`) resolves the snapshot
  cell as `(snapshots / name).read_bytes()` (line 95) with `snapshots` defaulting to
  `<lane>/.ufo/waves/round-69/before/src` (line 130). Consequence: the `snapshot=` cell must be a
  **bare filename** (`tk-v7211.rst`, `vm-v7211.h`); a path-prefixed value would resolve under that
  directory and fail. It also requires the `source=` id to match `S[0-9]{3,}` inside a row of the
  `## Registry` section, and the quote to satisfy the whitespace-normalised containment rule above.

## 8. Confidence and remaining unknowns

- Observed (high confidence, all from committed bytes plus one HTTP GET per document): both snapshot
  digests; second-route byte identity; the 20-row table, its line numbers, its `2^bit` numbers and
  the 4609 self-consistency; the three quotes with line numbers and word counts; the 12288 decode and
  its agreement with the boot log and the causal nvidia lines; the header's exact definition lines,
  component macros, config symbols and composed string, including the trailing space; the SOURCES
  registry count and the absence of S288/S289.
- Inference: `MODULE_ARCH_VERMAGIC` is empty and `RANDSTRUCT` is unset for this kernel/edit, derived
  from the absence of any extra token in the observed vermagic string, not from a read of
  `arch/x86/include/asm/vermagic.h` or of a kernel config.
- Unresolved gaps: (a) `include/linux/vermagic.h` has no pre-existing SOURCES pin, so the only
  cross-route check is §2; (b) no kernel build config (`/boot/config-*`, `/proc/config.gz`) was read,
  so the six config symbols are inferred from the produced string rather than observed; (c) the
  counter read here is the c2 draft, not a landed `tools/` file — its clause order is what this
  receipt verified against.
