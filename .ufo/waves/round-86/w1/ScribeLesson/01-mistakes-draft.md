# Draft — `## Mistakes` for `corpus/lessons/round-86.md` (replaces the placeholder line)

Seat ScribeLesson (w1), 2026-11-06. Draft only; the L1 lands it. Every hash, line number and count below was read
at the named revision by this seat; the battery numbers are read from the committed freeze receipt and were **not
re-run** (r05). Lane revision measured: `1e1caabcdd740a6429dd31d7aba3b725ff8c677d`.

## Mistakes

| # | Class | Evidence | Captured-by | Fix |
|---|---|---|---|---|
| M1 | a known divergence was disclosed in the entry's own `Limits` and then shipped as the gate's rule (`R86-LIMITS-DISCLOSED-NOT-ROUTED`) | The r85 entry names the divergence in its own words at `92be7506`: `corpus/knowledge/hibernation-availability-r85.md:52-57` — "the gate matches whole tokens `nohibernate` and `noresume`; the kernel's `__setup` matching is by byte prefix … so `noresume=1`, `noresumefoo` and `nohibernate=1` also set the flags in a real kernel. The gate reads them as HEALTHY … The prefix behaviour rests on `init/main.c` `obsolete_checksetup`, which is not in the pinned set." The gate at the same revision ships exactly that rule: `git show 92be7506:tools/check-hibernate-resume.py` (`sha256 88041b75…83e7`) `:102-106` `if tok == "nohibernate": … elif tok == "noresume":`, and its own docstring `:14-19` writes the rule as "a `nohibernate` token". Nothing in the round measured the divergence: the r85 battery's 20 families name none of the four families K1 fails (`grep -c` over `tools/resume-gate-battery-r85.py` at `2f67de80` → `0`; all four are in the r86 addition, `R86 = [...]`), so the byte copy of the r85 gate (control K1) reads 26/30 on the r86 battery and fails exactly `EMPTY-RESUME, NOHIB-VALUED, NORESUME-VALUED, OFFSET-SSCANF` (`.ufo/waves/round-86/before/controls/controls-summary.txt`, committed at `2f67de80`). The closure had to route it: `corpus/lessons/round-85-verifier-spotcheck.md` §5 defect 4 ("fix in the gate or freeze them as explicit rules"). Cost: `--live` answered HEALTHY for `noresume=1` / `nohibernate=1`, a real disable (BP4); no live exposure on this host, whose cmdline carries none of these forms (`hibernation-availability-r85.md:57`), so the cost is a wrong verdict available to any operator who runs the gate on a host that has one | **none.** Nearest neighbours, each falling short: QUALITY 94 makes `Limits` the authorised sink for cited lines outside a registered anchor range, so a *behavioural* divergence filed there reads as compliant; QUALITY 122 (landed in round 85, after this freeze) binds a *declaration* sentence to a near-miss control and says nothing about a `Limits` bullet; QUALITY 121 requires running a gate that already exists, and none existed for "a `Limits` divergence is routed"; QUALITY 63 requires a mechanism statement to be marked pre-source, and this `Limits` did disclose the unpinned source, so 63's wording duty was met while the gate still shipped the divergent rule | QUALITY 123 (drafted below): a `Limits` bullet that names a gate/source divergence carries, in the same commit, either a `Routed:` pointer or the rule that implements the source behaviour plus a control that lacks it. Round 86 did the rule branch: S346 (`init/main.c` raw 201-228) and S347 (`kernel/params.c` raw 79-95) are pinned, the parse is frozen in the battery docstring (`tools/resume-gate-battery-r86.py:7-19` at `2f67de80`), the gate implements it (`tools/check-hibernate-resume.py:105-108` at `1e1caabc`), and the r85 entry's bullet now names the pinned source and the rule (`hibernation-availability-r85.md:56-58`). **Shown able to fail:** K1 (byte copy of the r85 gate) reads `26 26 26` of 30 in three runs at the freeze, failing `EMPTY-RESUME, NOHIB-VALUED, NORESUME-VALUED, OFFSET-SSCANF`; N01 (a 30/30 candidate minus only the `noresume` prefix test) reads `29 29 29` failing `NORESUME-VALUED`, and N02 (minus only the `nohibernate` prefix test) `29 29 29` failing `NOHIB-VALUED`. A gate that keeps the r85 rule, or drops the prefix test for one of the two switches, cannot reach 30/30 |

### Why "captured-by: none" is the finding, not a formality

The round did not lack a rule about sources, controls or gates; it had four that touch this surface and each is
scoped one step to the side of it. QUALITY 94 is the sharpest: it *authorises* `Limits` as the place to enumerate
what a citation does not cover, which is why a reader — and the round's own landing review — sees a `Limits`
bullet as discharge. The gap is that nothing distinguished a provenance gap (a line outside a registered anchor)
from a behavioural one (the gate's rule contradicts the source it models). QUALITY 123 draws that line: a
behavioural divergence is either fixed or routed, and `Limits` keeps only what is genuinely unknown.

### Residual observed at the tip (not a violation; proposed patch, not applied by this seat)

At `1e1caabc`, `corpus/knowledge/hibernation-availability-r85.md:52` still opens "the gate matches whole tokens
`nohibernate` and `noresume`" in the present tense, while the gate at the same revision matches by prefix
(`tools/check-hibernate-resume.py:105-108`). The bullet is append-only-correct — `:57-58` appends "Round 86: the
gate now parses tokens this way (`hibernation-boot-parse-r86.md` BP1-BP4)" — so QUALITY 99 is satisfied and this
is a readability hazard, not a defect. Proposed patch for the L1 (file:line, text to append after `:58`):

```text
  Round 86 supersedes the first sentence of this bullet: the gate matches by prefix (`matches()`,
  `tools/check-hibernate-resume.py:105-108`); the sentence is kept as the round-85 record.
```

### Landing step this seat observed and did not run (QUALITY 70)

`python3 tools/check-registry-coverage.py` at the entry commit reads FAIL with one finding —
`REGISTRY-ROW-MISSING`, site `tools/resume-gate-battery-r86.py`, `registered 135 / tools_total 136`
(`.ufo/waves/round-86/w1/ExecLints/registry-tip.out`, seat ExecLints, read not re-run). The row exists only in the
working tree (`SKILL.md:5920`, uncommitted `M SKILL.md`; `git show 1e1caabc:SKILL.md | grep -c
'resume-gate-battery-r86'` → `0`). The landing commit must carry it or the round lands with a QUALITY 70 finding.
