# Patch D3 — quoted word/token counts in `corpus/lessons/round-84.md` do not match the quotes

Status: **proposed, NOT applied.** The lane repo was not modified. Low severity: the frozen predicate is
unaffected (the counter measures the JSON quotes, all 9-20 words, inside 6-25). The L1 may prefer to leave
the corpus's counting convention alone; if it lands, these are the three rows to fix.

Target: `corpus/lessons/round-84.md:21` (S336), `:26` (S341), `:27` (S342).
Lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`,
lane revision measured: `f19e73f3aa9817e76044e4e43a343c6ca6d929df`.

## Defect

Whitespace-split count of each quoted string vs the count printed in the same row:

| file:line | row | quoted string | label | actual |
|---|---|---|---|---|
| corpus/lessons/round-84.md:21 | S336 | "at which the swap header is located, in `<PAGE_SIZE>` units (needed only for swap files)" | `(14 words)` | **15** |
| corpus/lessons/round-84.md:26 | S341 | "if (( systemd_ver >= 255 )); then add_binary /usr/lib/systemd/systemd-hibernate-resume" | `(8 tokens)` | **9** |
| corpus/lessons/round-84.md:27 | S342 | "return p.wait(timeout=timeout) except: # Including KeyboardInterrupt, wait handled that. p.kill()" | `(11 tokens)` | **10** |

All seven admitted rows in that table were counted the same way; the other four (S337 12, S338 20,
S339 12, S340 19) match exactly. The label convention is not defined anywhere in the corpus, and the same
off-by-one habit exists in earlier rounds (`corpus/lessons/round-83.md:18` claims 17 vs 18 actual;
`corpus/lessons/round-81.md:25` claims 16 vs 15 actual), so this is a pre-existing pattern rather than a
round-84 regression.

## Proposed changes

`corpus/lessons/round-84.md:21`
```
- "at which the swap header is located, in <PAGE_SIZE> units (needed only for swap files)" (14 words)
+ "at which the swap header is located, in <PAGE_SIZE> units (needed only for swap files)" (15 words)
```

`corpus/lessons/round-84.md:26`
```
- "if (( systemd_ver >= 255 )); then add_binary /usr/lib/systemd/systemd-hibernate-resume" (8 tokens)
+ "if (( systemd_ver >= 255 )); then add_binary /usr/lib/systemd/systemd-hibernate-resume" (9 tokens)
```

`corpus/lessons/round-84.md:27`
```
- "return p.wait(timeout=timeout) except: # Including KeyboardInterrupt, wait handled that. p.kill()" (11 tokens)
+ "return p.wait(timeout=timeout) except: # Including KeyboardInterrupt, wait handled that. p.kill()" (10 tokens)
```

(Alternative the L1 may prefer: state the convention once in the table header, e.g.
"Located quote (≤25 words; count = whitespace-separated tokens)" — that is a wording change, not a count
change, and leaves the three labels as they are.)

## Verification after landing (read-only)

```
python3 - <<'PY'
import re
for i,line in enumerate(open('corpus/lessons/round-84.md'),1):
    for m in re.finditer(r'"([^"]{10,200})"\s*\((\d+)\s+words?\)',line):
        q,n=m.group(1),int(m.group(2))
        if n!=len(q.split()): print(i,n,len(q.split()))
PY
python3 tools/count-resume-rows-r84.py --root .        # expect verdict met, counted 10, failed 0, rc 0
```
