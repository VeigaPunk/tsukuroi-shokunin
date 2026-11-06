# Draft — `corpus/QUALITY.md` criterion 123

Seat ScribeLesson (w1), 2026-11-06. Draft only; the L1 lands it. The file's last criterion is 122
(`corpus/QUALITY.md:240` at `1e1caabc`), so this appends as 123. Commands below were run by this seat at the named
revisions unless the line says the value is read from a committed receipt.

## Text to append

123. **A divergence disclosed in a `Limits` section is frozen as a rule or routed, never shipped as a gate rule (R86-LIMITS-IS-NOT-A-FIX):** when a `corpus/knowledge/` entry's `Limits` section names a place where a lane gate's rule differs from the behaviour of the source that gate models, that bullet carries, in the same commit, either (a) a `Routed:` pointer naming the round and the defect id that will fix it, or (b) the rule that implements the source behaviour together with a committed control that lacks the rule and reads below the battery target; a `Limits` bullet records what is not known, and never discharges a known wrong answer. Captured by: round 85's entry named the kernel's prefix match against the gate's whole-token match in its own `Limits` (`corpus/knowledge/hibernation-availability-r85.md:52-57` at `92be7506`) and shipped the whole-token rule in the gate (`tools/check-hibernate-resume.py:102-106`, `sha256 88041b75…83e7`), so `--live` answered HEALTHY for `noresume=1` / `nohibernate=1`; the closure routed it as `corpus/lessons/round-85-verifier-spotcheck.md` §5 defect 4, and no criterion then in force covered it (QUALITY 94 authorises `Limits` for citation gaps, 122 binds declaration sentences, 121 requires running a gate that exists, 63 governs mechanism wording). Shown able to fail — red, the r85 pair at `92be7506`:

```text
$ git -C <lane> show 92be7506:corpus/knowledge/hibernation-availability-r85.md | sed -n '52,57p'
- Rule text versus kernel parsing: the gate matches whole tokens `nohibernate` and `noresume`; the kernel's
  `__setup` matching is by byte prefix (S343 1518-1524 register the bare names, and their handlers ignore any
  argument, raw 1440-1444, 1461-1465), so `noresume=1`, `noresumefoo` and `nohibernate=1` also set the flags in a
  real kernel. The gate reads them as HEALTHY (`.ufo/waves/round-85/w1/ReviewGate.md` L1, fixtures T9-T11).
  The prefix behaviour rests on `init/main.c` `obsolete_checksetup`, which is not in the pinned set. This host's
  cmdline carries none of these forms.
$ git -C <lane> show 92be7506:tools/check-hibernate-resume.py | sed -n '102,106p'
    for tok in cmdline.split():
        if tok == "nohibernate":
            disabled = True
        elif tok == "noresume":
            noresume = True
```

no `Routed:` pointer, no rule, no control: red. Green, the r86 pair at `1e1caabc`:

```text
$ sed -n '52,58p' corpus/knowledge/hibernation-availability-r85.md
- Rule text versus kernel parsing: the gate matches whole tokens `nohibernate` and `noresume`; the kernel's
  `__setup` matching is by byte prefix (S343 1518-1524 register the bare names, and their handlers ignore any
  argument, raw 1440-1444, 1461-1465), so `noresume=1`, `noresumefoo` and `nohibernate=1` also set the flags in a
  real kernel. The gate reads them as HEALTHY (`.ufo/waves/round-85/w1/ReviewGate.md` L1, fixtures T9-T11).
  The prefix behaviour rests on `init/main.c` `obsolete_checksetup`, pinned round 86 as S346 (raw 201-228).
  This host's cmdline carries none of these forms. Round 86: the gate now parses tokens this way
  (`hibernation-boot-parse-r86.md` BP1-BP4).
$ sed -n '105,108p' tools/check-hibernate-resume.py
def matches(tok, setup):
    """obsolete_checksetup: the first len(setup) characters equal setup, '-' read as '_' (parameqn)."""
    n = len(setup)
    return len(tok) >= n and tok[:n].replace("-", "_") == setup.replace("-", "_")
$ grep -E '^(K1|N01|N02)' .ufo/waves/round-86/before/controls/controls-summary.txt   # committed at 2f67de80
K1-r85-gate-do-nothing: 26 26 26  EMPTY-RESUME,NOHIB-VALUED,NORESUME-VALUED,OFFSET-SSCANF
N01-noresume-exact: 29 29 29  NORESUME-VALUED
N02-nohib-exact: 29 29 29  NOHIB-VALUED
```

the bullet names the pinned source and the rule, and the controls that lack the rule read below the 30/30 target.
Lesson: `corpus/lessons/round-86.md` Mistakes `R86-LIMITS-DISCLOSED-NOT-ROUTED`.

## Notes for the L1

- The criterion is deliberately narrow: it binds a `Limits` bullet that names a **gate/source divergence**, not
  every `Limits` bullet. Provenance gaps (a cited line outside a registered anchor) stay with QUALITY 94, and
  genuinely unknown behaviour stays in `Limits` with no duty.
- The `Routed:` pointer spelling is new. If the L1 prefers an existing token, the round-85 lesson's "Routed
  defects" table and `SCORECARD.md` "routed defect N" phrasing are the nearest house forms; the criterion needs
  one literal spelling so a reader can grep it.
- The green half is satisfied by round 86 at `1e1caabc` for the two switch tokens and the empty `resume=`; the
  `resume_offset=` sscanf rule is also frozen (battery family `OFFSET-SSCANF`, control N05 `29 29 29`).
- No tool is proposed. The check is a two-command read (`git show <rev>:<entry>` `Limits` + `git show
  <rev>:<gate>`), and this lane's history shows the failure mode is not a missing gate but an unrun one
  (QUALITY 121).
