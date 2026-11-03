2026-11-03T23:20:43Z

# S1Scout — C1 independent source re-verification (round 69, w1)

Seat S1Scout (scout; C1 independent source re-verification). Non-author check of every C1 source
fact. Lane HEAD `920a9eea3c5c5400567be0e96141014f338973df` (declaration commit; measured base
`acce353bacad74043636018d829e9e9b8e0fdf1c`). Scratch `/fast/scratch/hyaku/tsukuroi-r69/S1Scout`
created and removed at exit (`trap`); all retained bytes are in the two `probes/` files below.

Receipts: `.ufo/waves/round-69/probes/S1Scout-sources.md` (command/output/rc per fact) and
`.ufo/waves/round-69/probes/S1Scout-taint-table.tsv` (20-line table extract, sha256
`1b10b163ea299c96ac68d12770bd15459b62b687a6017cade84c3837fbed0757`).

## Findings (all keyed to the frozen C1 predicate)

1. **Snapshot digests reproduce.** `sha256sum` on
   `before/src/tk-v7211.rst` → `727ddb82…a0841` and `before/src/vm-v7211.h` → `0556c28f…71aea`,
   rc 0; both equal the declaration and `before/src/SHA256SUMS`. tk 191 lines/9340 B, vm 48/1234.
2. **Second route reproduces both files byte-for-byte.** `curl` from
   `raw.githubusercontent.com/gregkh/linux/v7.2.11/...` rc 0 for both, sha256 identical,
   `cmp` rc 0 against the committed snapshots. Independence is host/transport (raw.githubusercontent
   vs git.kernel.org `plain/`), same stable tree. A genuine cross-tree confirmation exists for the
   taint doc: round-27 `S140.rst` (pin at tag v7.2, torvalds tree) is byte-identical to the v7.2.11
   snapshot. No prior pin exists for `vermagic.h`.
3. **Table 0–19.** `tk-v7211.rst` lines 82–105: rules 82/84/105, header 83, 20 data rows 85–104
   (bit 12 = 97, 13 = 98, 14 = 99, 19 = 104). TSV has 20 lines, TAB-delimited
   `bit<TAB>log<TAB>number<TAB>reason`; every Number equals `2^bit` (20/20), and the doc's own
   `4609 = 4096+512+1` example is consistent with bits 0/9/12.
4. **Quotes.** bit 12 line 97 `externally-built ("out-of-tree") module was loaded` = 5 words;
   bit 13 line 98 `unsigned module was loaded` = 4; bit 14 line 99 `soft lockup occurred` = 3;
   each occurs once (`grep -c -F` 1) and passes the counter's whitespace-normalised containment
   rule at ≤ 25 words.
5. **12288 decodes to bits 12 and 13 only** — `bit=12 log=_/O`, `bit=13 log=_/E`; no other bit set.
   The boot log agrees exactly: `Tainted: [O]=OOT_MODULE, [E]=UNSIGNED_MODULE` (host.txt:49,50), and
   the causal lines (host.txt:54,55) map out-of-tree → bit 12 and unsigned → bit 13; soft-lockup
   lines 0 agrees with bit 14 being clear.
6. **Vermagic composition agrees.** `VERMAGIC_STRING` def at vm lines 41–46; components at 13–17
   (`CONFIG_SMP`), 18–24 (`CONFIG_PREEMPT_RT`/`CONFIG_PREEMPT_BUILD`), 25–29
   (`CONFIG_MODULE_UNLOAD`), 30–34 (`CONFIG_MODVERSIONS`), 35–39 (`RANDSTRUCT`), plus
   `UTS_RELEASE` (generated/utsrelease.h) and `MODULE_ARCH_VERMAGIC` (asm/vermagic.h). With
   SMP=y, PREEMPT_RT unset, PREEMPT_BUILD=y, MODULE_UNLOAD=y, MODVERSIONS unset, RANDSTRUCT unset,
   arch empty → `7.2.11-arch1-1 SMP preempt mod_unload ` — matching host.txt:40 including its
   trailing space (`cat -A` shows `$` after a space). `[INFERENCE]` the two residual components are
   empty, inferred from the absence of extra tokens.
7. **C1 wiring, for the authoring seats.** `corpus/SOURCES.md` at HEAD has 287 registry ids
   `S001`…`S287` and **no** `S288`/`S289` (matches declaration control (e)); a `source=S288|S289`
   row verifies only after those two rows land. The counter draft at `drafts/c2/count-kr-rows-r69.py`
   resolves `snapshot=` as `(before/src)/name`, so **bare filenames** `tk-v7211.rst` / `vm-v7211.h`
   are required; `source=` must match `S[0-9]{3,}` inside `## Registry`.

## Remaining unknowns
- `MODULE_ARCH_VERMAGIC` content (x86 `asm/vermagic.h`) is outside the pinned snapshot set — not
  fetched, because the item names only the two documents; the observed string still over-determines
  it as empty.
- No kernel config was read, so `CONFIG_SMP`/`PREEMPT_BUILD`/`MODULE_UNLOAD`/`MODVERSIONS`/`RANDSTRUCT`
  are inferred from the produced vermagic, not observed in `/boot/config-*`.
- The counter read is the c2 draft, not a landed `tools/` file.

KEY=S1_SNAPSHOT_DIGESTS_OK=yes S1_SECOND_ROUTE=both S1_TABLE_ROWS=20 S1_TAINT_12288=12(O,4096),13(E,8192) S1_VERMAGIC_COMPOSITION=agrees
