VERDICT: supports

# C1-11 — independent identity harness (seat C1ExecIndependent, round 46 w1)

## Item and method

Own harness, no import of `tools/score-census-identity-r46.py` (that counter was never executed by
this seat). Input: `tools/tsukuroi-census.sh` at implementation revision
`a44770491eb5ca15ce9f8b3207309d1af683ffaf` (lane HEAD when read; 209208 bytes, sha256
`d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa`, md5
`db08a606ce128da3839457372e91e220`, 3598 newlines, final command `main "$@"` at
`tools/tsukuroi-census.sh:3599` with **no trailing newline**). 30 byte-level variants were built by
appending comment bytes, each was run as `bash <file> --identity`, and every field of the printed
line was compared against values recomputed here with `sha256sum`, `md5sum`, `wc -c`, `wc -l`, the
file's own rollup printf (`tools/tsukuroi-census.sh:3588`) and its `VERSION`/`exit_map` literals —
never against anything the census printed.

Axes walked: 8 printed fields × 6 variant families × 2 invocation paths + a write-freedom probe.

## Result — 30/30 matched, 0 mismatched

- absolute-path invocation: **30/30 matched, 0 mismatched** (`identity-variants.log:128`)
- relative-path invocation (`cd <scratch>; bash v/<name>.sh --identity`): **30/30 matched**
  (`identity-variants.log:129`)
- each variant's printed `sha256` differs from the base census digest: **30/30**
  (`identity-variants.log:130`); every field equals the value computed from that variant's own
  bytes, and `verified=yes`, exit 0, exactly one line in all 30.
- determinism: a second full run produced a byte-identical log
  (`cmp` → `RERUN_IDENTICAL`; `identity-variants-rerun.log` is identical to `identity-variants.log`).
- harness discrimination (mutants, not counted in the 30): **3/3 caught**
  (`selfcheck.log:13`), i.e. the comparison is not vacuous.

Variant families (all 30 named at `identity-variants.log:130`):

| family | n | example evidence |
|---|---|---|
| appended random printable comment, final newline (8/40/200/1000/4096 B) | 5 | A1: appended=12B → bytes 209220, lines 3600 (`:7`) |
| same, **no** final newline | 5 | B1: appended=11B → bytes 209219, lines 3599 |
| CRLF line ends inside the appended comment (incl. no final EOL, two lines, 1 KB) | 4 | C2: appended=43B, bytes 209251, lines 3600 |
| UTF-8 multibyte comment (accents, CJK, emoji, 200× repeated) | 4 | D1-D4 all MATCH |
| appended empty line / two empty lines / whitespace-only line | 3 | E1: appended=1B → bytes 209209, lines 3599 (`:79`) |
| 1 MiB appended comment block (final newline, no final newline, single 1 MiB line) | 3 | F1 bytes 1257785 lines 19250 (`:91`); F2 same byte count, 19249 newlines, different sha256 (`:95`); F3 1257786 bytes, 3600 newlines |
| combinations (no space after `#`, 3-line block ±final newline, UTF-8 ±CRLF/no EOL, empty line then comment) | 6 | G1-G6 all MATCH |

F1 vs F2 is the sharpest single observation: identical `bytes=1257785` with differing `sha256`,
`md5` and `lines` — the four byte fields are independent readings, not one constant repeated.

Write-freedom spot check: two `--identity` runs (base and the 1 MiB variant F1) with `cwd` and
`TMPDIR` pointed at freshly made empty dirs created no file at all; `find` over the probe root
showed only the two pre-created directories.

## Mismatches verbatim

Among the 30 variants: **none**. The only MISMATCH lines this seat produced are the intentional
mutants, quoted verbatim from `selfcheck.log`:

```
NEG1 [constant-digest-writer] rc=0 -> CAUGHT
  sha256: printed='d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa' expected='eb4307344458c66a84474c66dff7010e74d16e164029f2da955dd65f4b9772a0'
  bytes: printed='209208' expected='209294'
NEG2 [exit-map-drift] rc=0 -> CAUGHT
  exit_map: printed='0:HEALTHY,1:DEGRADED,2:BLOCKED,3:X' expected='0:HEALTHY,1:DEGRADED,2:BLOCKED'
NEG3 [planes-order-drift] rc=0 -> CAUGHT
  planes: printed='systemd,packages,drivers,journal,update-safety,oom' expected='packages,systemd,drivers,journal,update-safety,oom'
```

## Construction notes (first draft of the harness was wrong, then fixed)

Honest record of the two failures in my own harness, in case the L1 sees earlier scratch logs:

1. First run reported `0/30 matched`. Cause was my plane-list slice (`x[:-2]` instead of `x[:-3]`
   when stripping `=%s`), so every variant false-failed only on `planes`. Fixed in `harness.py`
   (`expected()`), after which the same 30 variants are 30/30.
2. My first CRLF variants and my first "comment with no leading newline" variant spliced bytes onto
   `tools/tsukuroi-census.sh:3599` (`main "$@"`, file ends without a newline). Observed, verbatim:
   - `tsukuroi-census: unknown argument: --identity\r` → exit 2 (a trailing `\r` joins the last
     argv word, so the census correctly rejects it via the `--identity takes no other argument`
     path, `tools/tsukuroi-census.sh:3513-3519`);
   - `v/G1.sh: line 3599: syntax error near unexpected token ')'` — bash only starts a comment at
     a word start, so `"$@"#…` is one word, not a comment.
   Those six variants were rebuilt to start the appended region on an LF line (CRLF then belongs to
   the comment only). Both observations are properties of bash/the file's missing final newline, not
   defects in the identity code — but they are why the corrected variants, not the first draft, are
   the evidence.

## Risks / what I did not do

- Not run: `tools/score-census-identity-r46.py`, `tsukuroi-census.sh --selftest`, any plane probe,
  the C2 counter. No tracked lane file written (`tools/tsukuroi-census.sh` still sha256
  `d925839c…9112cfa`, lane HEAD still `a4477049`; `git status` shows only the untracked
  `.ufo/waves/round-46/w1/` seat dir among my paths), no git/jj mutation, no host change; scratch
  removed after copying receipts.
- `planes=` on the identity line comes from a *separate* literal, `CENSUS_PLANES`
  (`tools/tsukuroi-census.sh:3465`), not from the rollup printf at `:3588`. They agree at
  `a4477049` (my check is exactly the cross-check, and NEG3 proves it bites); nothing in the
  implementation keeps them in sync, so a future edit could silently drift one from the other.
- Scope limit: only comment-only appends. Whole-file CRLF conversion, mid-file edits, and
  non-comment appends are not exercised by this item.
- `verified=yes` relies on bash holding a script descriptor ≥10 (normally 255); this held for all 30
  variants including the 1 MiB appends on GNU bash 5.3.20(1)-release.

## Environment and receipts

- GNU bash 5.3.20(1)-release (x86_64-pc-linux-gnu), GNU coreutils `sha256sum`/`md5sum`/`wc`,
  Python 3.14.8. No tool installs were needed.
- Commands (run from `/fast/scratch/hyaku/tsukuroi-r46/C1ExecIndependent`, `TMPDIR` exported there):
  - `python3 .ufo/waves/round-46/w1/C1ExecIndependent/harness.py /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh /fast/scratch/hyaku/tsukuroi-r46/C1ExecIndependent/s <log>`
  - `python3 .ufo/waves/round-46/w1/C1ExecIndependent/selfcheck.py <same base> /fast/scratch/hyaku/tsukuroi-r46/C1ExecIndependent/s <log>`
- Receipts (all under
  `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-46/w1/C1ExecIndependent/`):
  `harness.py` (the harness), `selfcheck.py` (mutant controls), `identity-variants.log` (30-variant
  run), `identity-variants-rerun.log` (determinism copy), `selfcheck.log` (3/3 caught).
  Scratch `/fast/scratch/hyaku/tsukuroi-r46/C1ExecIndependent/` was removed with `rm -rf`.
- Cited implementation lines: `tools/tsukuroi-census.sh:455` (`SELF`), `:3465` (`CENSUS_PLANES`),
  `:3466` (`census_identity`), `:3489` (identity printf), `:3513-3519` (`--identity` stands alone),
  `:3588` (rollup printf), `:3599` (final `main "$@"`, no trailing newline).
