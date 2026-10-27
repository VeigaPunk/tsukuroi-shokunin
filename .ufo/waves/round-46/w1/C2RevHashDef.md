VERDICT: supports

C2-S9 — SECTION SHA256 re-derivation for rows GR1/GR2/GR3 at a44770491eb5ca15ce9f8b3207309d1af683ffaf (implementation revision). All three declared values are reproduced by three independent derivations; the only seat trap found is the trailing-LF variant of the slice, plus the usual revision/copy-paste caveats. No tools were installed.

## 1. Definition and its literal implementation

- Docstring, tools/check-scrub-admission-r46.py:12-13: "section hash for row GR<n> at REV: the entry's lines from the line `## GR<n>` up to, not including, the next line that starts with `## `; sha256 of those lines joined with \"\\n\", UTF-8."
- Implementation, tools/check-scrub-admission-r46.py:115-124: `lines = entry.split('\n')`; start `i = lines.index(f'## {row}')` (exact-match header, header INCLUDED in the slice); end at first `j > i` with `lines[j].startswith('## ')`; hash = `hashlib.sha256('\n'.join(lines[i:j]).encode('utf-8'))`. So: join with LF, NO terminator after the last line of the slice.
- Counter integrity: `sha256sum tools/check-scrub-admission-r46.py` → 28c409bef9a87338831e0cab4c194a78e7fedfefbd9c4a300a33f30b24dd11d8 — equals the frozen sha declared in the round item.
- Entry blob: base 2042117c…, impl a4477049…, and the worktree file are byte-identical: sha256 560e70cc78c698a41a87019f4ae6f78db141a4388e0c6901dee6822d6bca5a3f for all three; `cmp` worktree vs impl blob → IDENTICAL; `git status --porcelain` on the entry and counter paths → empty. File is 228 lines, 16560 B, ends "…integration).\n" (single LF), no `\r` anywhere (grep `\r`: no matches). Section headers: `## GR1` :14, `## GR2` :55, `## GR3` :127, next `## ` after GR3 is `## How this changes OS triage` :167 — GR3 does not run to EOF.

## 2. Three derivations agree with the declared values

(a) Frozen counter: `python3 tools/check-scrub-admission-r46.py --revision a44770491eb5ca15ce9f8b3207309d1af683ffaf --section-hash` → exit 0, JSON `{"revision":"a44770…","section_sha256":{"GR1":"fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8","GR2":"a963df81745c7770f73406eda78cfdf6c1355e23c65c17d43b16e3ebeff62781","GR3":"8fa626768b49a98186b5a03fbc348175e5ed73484648b6e68a4277c6907a2800"}}` — exactly the three values in the item.

(b) Own code (Python hashlib over `git show` blob at REV, docstring-literal slice: header included, LF-join, no trailing LF): GR1 fe77ac76…, GR2 a963df81…, GR3 8fa62676… — match_declared = {GR1: true, GR2: true, GR3: true} (receipt py-derivation.json).

(c) awk + sha256sum (`awk -v s="## GR<n>" '$0==s{f=1;print;next} /^## /{f=0} f{print}'`):
- `awk | sha256sum` (every line plus its LF = join WITH trailing LF) → GR1 998fdd2f667f70fa741dfdc0b56b540a436a8a56a808fa3013aac2234d7ff848, GR2 97a418df19c552fb64376031bd408135fb4ff3c88f3fbb2e30d9d46bc13b2fc4, GR3 31aa834c13b8f60f847cbfe102b216ae1d4f905a9254bb349a03f7991d759c99 — all three DIFFER from declared.
- `awk | head -c -1 | sha256sum` (final LF stripped = `'\n'.join`) → GR1 fe77ac76…, GR2 a963df81…, GR3 8fa62676… — all three match.
Slice sizes (trailing-LF files): gr1 2243 B, gr2 4365 B, gr3 2876 B.

Answer: YES — the counter, my own code, and awk/sha256sum agree on all three declared hashes, provided the slice is hashed as LF-joined lines WITHOUT a trailing LF.

## 3. Which tiny edit changes which hash (own code, same slice function, entry at REV)

| edit | GR1 | GR2 | GR3 |
|---|---|---|---|
| one extra blank line at EOF | – | – | – |
| new `## GR4 appendix` section inserted after GR3 (own `## ` header, placed before `## How this changes OS triage`) | – | – | – |
| one plain line appended directly after GR3's last line (headerless, before the next `## ` header) | – | – | changed |
| every `\n` → `\r\n` (CRLF) | changed | changed | changed |
| one-character line "x" inserted inside GR2 (new 1-based line 61) | – | changed | – |
| one extra blank line at the end of GR1's slice (just before `## GR2`) | changed | – | – |

Mechanics: a row hash moves iff the edit alters bytes strictly between the row's `## GR<n>` header line and the next line starting with `## `. A properly-headered section appended after GR3 is invisible to all three hashes (GR3's slice already ends at the pre-existing `## How this…` header); headerless text appended right after GR3's last line moves GR3 only; CRLF moves all three because the counter does not normalize line endings (`split('\n')` keeps the `\r`).

## 4. Ambiguities a seat could fall into

1. Trailing LF (the dominant trap, and the one the item flags): `awk|sha256sum` hashes the join-with-terminator variant → 998fdd2f…/97a418df…/31aa834c…, all wrong. Fix: `head -c -1`, or hash `'\n'.join(lines)` semantics. A seat whose pipeline emits a final newline will report a mismatch that is an artifact, not a defect.
2. Wrong revision: the counter hashes the blob of `--revision` via git (check-scrub-admission-r46.py:213,219), not the worktree. Today moot — base, impl and worktree blobs are identical and the counter at base prints the same three hashes (receipt counter-section-hash-base.json) — but after any future edit of the entry, base-era values stop matching. Seats must bind against a4477049….
3. End-boundary predicate: slices end at `startswith('## ')`; a `###` subheading does NOT end a slice, while a seat re-deriving with `startswith('##')` truncates early and diverges. The start boundary is exact equality `lines.index(f'## {row}')` (:118) — a line `## GR1 (amended)` would not be found, the row would be silently absent, and `--section-hash` would exit 2 with fewer than three hashes (:223) — a seat that ignores the exit code could compare a partial dict.
4. Header inclusion: the `## GR<n>` line itself is inside the hashed slice; skipping it yields different hashes.
5. Copy/paste shape: `--section-hash` prints one JSON line with keys entry/revision/section_sha256 (:222). A seat must copy only the 64-char lowercase hex values; uppercase hex, truncation, or pasting with surrounding JSON/whitespace fails the exact string equality used when seats bind their SECTION SHA256.
6. Encoding: the entry is decoded with `errors='replace'` (:219) and hashed as UTF-8; harmless for this pure-ASCII/LF file, but a seat hashing raw bytes of a non-UTF-8 file would diverge from the counter.

## 5. Not done

- I ran only `--section-hash` mode; I did not exercise the full admission predicate (r45_legs_ok / verdicts_ok / marks_ok legs) — other seats' items cover those.
- I did not audit the bind() first-line parser that consumes the seats' SECTION SHA256 strings (lines ~136-143 read only in passing).

## Receipts

.ufo/waves/round-46/w1/C2RevHashDef/: counter-section-hash-impl.json, counter-section-hash-base.json, awk-derivation.txt, py-derivation.json, setup-sums.txt, gr1.txt, gr2.txt, gr3.txt (the three LF-terminated slices), grounding-impl.md (the impl blob). Scratch /fast/scratch/hyaku/tsukuroi-r46/C2RevHashDef removed after copying.
