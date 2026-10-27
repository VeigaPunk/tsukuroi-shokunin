VERDICT: supports — GR1–GR3 each carry new decision-relevant facts beyond the beliefs they re-pin; the three frozen novelty tokens stand for new facts, not only new words.

# Item C2-10 — novelty as facts, not tokens (GR1–GR3 vs held lane knowledge)

Method: read `corpus/knowledge/btrfs-scrub-grounding-r45.md` at impl `18389f44` against the held corpus
(`btrfs-scrub-record-r44.md`, `-r43.md`, `-r42.md`, `storage-health-r26.md`, `kill-event-deep-r8.md`,
`oom-event-plane.md`, `kill-oom-boundary-r33.md`, `boot-plane.md`, `corpus/README.md`) and `SKILL.md`, then ran
`git grep` at the frozen base `5bbd5ff588120fd8e7c744695351a6978b4241c1` for each token and for the kill-model
vocabulary (`SIGCONT`, `TimeoutStopUSec`, `system.conf.d`, `FinalKillSignal`, `SendSIGKILL`, `control-group`,
`simple_strtoull`, `btrfs_dev_replace_is_ongoing`, `DefaultTimeoutStopSec`). "Held" below means stated in a tracked
base file; "held-unpinned" means stated but marked `[inference]` or judged unpinned by a counted/spot-check read.
Base tokens: all three novelty tokens have 0 hits at base (`git grep` output empty for each — reproduced the
counter's `novelty_base_hits` leg).

## GR1 — memparse as the `scrub_speed_max` write parser

| fact | new or held |
|---|---|
| `scrub_speed_max` writes are parsed by `memparse` | held — `corpus/knowledge/btrfs-scrub-record-r44.md:61` ("Writing parses the text with `memparse` (sysfs.c:2040)"), `SKILL.md:4225` |
| trailing whitespace skipped, other trailing text → `-EINVAL` | held — r44 `:62`, `:78-80` quotes; `SKILL.md:4225` |
| 0 = no limit; mode 0644 root-write; in-memory only | held — r44 SR8 `:59-67`, r42 SC5 `:125-129`, `SKILL.md:4225`; host value 0 re-measured (`r45 capture.txt:8` ≡ `r44 capture.txt:4`) |
| `memparse` calls `simple_strtoull` with base 0 → `0x` hex, other leading `0` octal, else decimal | **new** — grounded via `_parse_integer_fixup_radix` (GR1 `:17-18`; no base hit for `simple_strtoull`/`octal`/radix anywhere in corpus or SKILL) |
| suffix set is exactly one letter K/M/G/T/P/E, either case, each step ×1024 | **new** — held was only "a size suffix such as K, M or G is accepted" marked `[inference]` (r44 `:63`), and `SKILL.md:4225` states "K/M/G suffixes" as fact (routed defect D2, `corpus/lessons/round-44-verifier-spotcheck.md:181-183`). T/P/E range, case-insensitivity, and the 1024-vs-1000 multiplier were never held |
| suffix counts only after ≥1 digit; overflow saturates to `ULLONG_MAX` | **new** — `ULLONG_MAX` has no held hit |
| bare-newline write parses as 0 and clears the limit | **new** — and decision-relevant: it is a way to remove the cap that no prior row described (GR1 `:24-25`, `:133`) |
| worked examples (`010`→8, `0x10`→16, `10MB`/`10 M`/`-1` rejected, `100m`≡`100M`) | **new** — derived consequences (marked as such in Limits `:145-146`) |

**Judgment: adds new decision-relevant facts.** The octal trap (a leading zero silently re-reads the configured
limit) and the 1024-vs-1000 multiplier directly change how a surprising `limited=` census value is triaged
(GR1 `:131-133`); newline-clears-limit is a new operator-level fact. The row also re-pins the EINVAL/suffix
acceptance that was held-unpinned — re-grounding, not novelty, but not falsely claimed as new.

## GR2 — device replace through `btrfs_scrub_dev`, `EINPROGRESS` during a replace

| fact | new or held |
|---|---|
| `btrfs_scrub_dev` serves replace via `is_dev_replace` param; replace calls it on the source devid | held-unpinned — r44 `:21-22` stated it with `[inference … not pinned]`; `SKILL.md:4222` carries the same "(dev-replace.c:701-703,1265-1268, unpinned)". GR2 pins it (call sites at dev-replace.c `:700-703`, `:1259-1268` quoted) — re-grounding |
| docs-level replace description | held — `SKILL.md` R31-Q07 (`:2686`) describes `btrfs replace` semantics from btrfs-replace.rst, but never the scrub-code reuse |
| refuse with `-EINPROGRESS` when the device already has a scrub context | held — r44 SR7 `:18` (pinned), `SKILL.md:4222` |
| `is_dev_replace=false` calls refused `-EINPROGRESS` while `btrfs_dev_replace_is_ongoing` for the filesystem | **new** — a per-filesystem refusal independent of per-device context; the r44 quote of the guard (scrub.c:3147) was truncated at `"if (dev->scrub_ctx ||"` so this second disjunct was never in a held row; `btrfs_dev_replace_is_ongoing` has 0 base hits |
| a scrub-start ioctl on any devid answers `EINPROGRESS` during a replace though no scrub started | **new** — and decision-relevant: distinguishes "replace holds the machinery" from "a scrub is running"; gives the triage rule "check the replace first" (GR2 `:62-64`, `:134-135`). The only earlier statement was the inverse direction (context ⇒ scrub-or-replace running) |
| replace's source device carries a scrub context → privileged status answers 0 (SR7) | held-unpinned as mechanism (SR7's context window held at `:17-20`); the chaining is newly safe now that the premise is pinned |
| host: no replace/scrub state observable unprivileged | held — same CapEff=0 gate as r43 SR6 / r44 host readings |

**Judgment: adds a new decision-relevant fact.** The fs-wide `btrfs_dev_replace_is_ongoing` refusal is genuinely
new knowledge (new errno condition on a different scope), not just a pin of SR7's held-unpinned caller claim —
though pinning that claim is the row's other, already-held half.

## GR3 — stop sequence of `btrfs-scrub@.service` under systemd v262

| fact | new or held |
|---|---|
| unit ships `KillSignal=SIGINT`; `-B` foreground handler issues `BTRFS_IOC_SCRUB_CANCEL` | held — r44 SR9 `:97-101` pinned (unit text + progs handler); `SKILL.md:4226` |
| `KillSignal=` is what `systemctl stop` sends | held-unpinned — r44 `:150-151` marks it `[inference]`; GR3 pins it via systemd.kill.xml (S248) — re-grounding |
| `KillMode=control-group` is the default and signals every process in the unit's cgroup | **new** — `control-group` has no held hit; held teardown knowledge was `KillMode=mixed` for `user@.service` only (`kill-event-deep-r8.md:33,221,263`; `boot-plane.md:139,247`) |
| SIGCONT sent right after the KillSignal | **new** — `SIGCONT` has no held hit in corpus/SKILL |
| repeat with SIGKILL (`FinalKillSignal=`) after `TimeoutStopSec` unless `SendSIGKILL=no` | **new** — `FinalKillSignal`/`SendSIGKILL` absent at base (only the `status=9/KILL` outcome class was held) |
| a `TimeoutStopSec=5s` exists on this host | partially held — `user@.service`'s 5s is held (`oom-event-plane.md:352` `/etc/systemd/system/user@.service.d/faster-shutdown.conf`; `kill-event-deep-r8.md:258,263`; `SKILL.md:1105`). The scrub unit's `TimeoutStopUSec=5s` is **new** (r44 capture ran no `systemctl show` on the service — `capture.sh:16-18` reads only timer enablement/sha/owner) |
| mechanism: `DefaultTimeoutStopSec=5s` in `/etc/systemd/system.conf.d/10-faster-shutdown.conf`, no package owns it, `unit_dropins` empty | **new** — `DefaultTimeoutStopSec`/`system.conf.d` have 0 base hits; the held 5s was a *unit* drop-in on a unit that ships `TimeoutStopSec=120s` (`boot-plane.md:247`), a different mechanism covering a different unit |
| stopped scrub may leave no `canceled` record if SIGKILL lands before the write | **new** consequence — marked `[inference]` (GR3 `:103-104`, `:137-138`); weakens the held triage rule at `SKILL.md:4226` "a stopped scrub service … leaves a resumable record" (which predates any TimeoutStop bound on this unit) |

**Judgment: adds new decision-relevant facts.** The kill sequence fan-out (control-group → SIGCONT → SIGKILL) and
the system-wide 5s default are new; "5s" alone is not new as a number, but its mechanism and its application to
this unit are.

## Are the frozen novelty tokens standing for new facts or only new words?

- `simple_strtoull` (GR1): names the base-0 parser through which the octal/hex radix rules exist — a real new fact
  cluster (radix + 1024 suffixes + ULLONG_MAX). Stands for new facts. Caveat: the token is the *function name*;
  the octal surprise would exist under any callee name, so the token is a proxy, not the fact itself. Here the
  proxy is honest (the callee is quoted at cmdline.c:156).
- `btrfs_dev_replace_is_ongoing` (GR2): names the per-filesystem refusal condition — the one held quote of that
  guard (r44 `:33`, scrub.c:3147) is truncated at `dev->scrub_ctx ||`, so the token tracks the disjunct that was
  never held. Stands for a new fact.
- `DefaultTimeoutStopSec` (GR3): names the system.conf.d mechanism — a new fact (scope: every system unit without
  its own value; the held `faster-shutdown.conf` 5s is a different file and mechanism). Stands for a new fact.
  The bare predicate `novelty_base_hits == 0` is lexical and would pass a restated old fact, but on this evidence
  the three tokens each track fact-level novelty.

## What was not done

- I did not run the C2 counter (`check-scrub-grounding-r45.py`); this seat's item is the novelty comparison, run
  by direct read + base-revision greps above (every "0 base hits" claim is from `git grep` at `5bbd5ff`, outputs
  shown empty in session transcript).
- I did not verify GR quote line numbers against the frozen snapshots (the counted GR seats own that); "new/held"
  marks rest on the cited base files only.
- Coverage note: the "held" sweep covered the files named by the seat spec plus `boot-plane.md` and
  `corpus/README.md` (found via grep); a corpus file not hit by the token greps could in principle hold a paraphrase
  — no such paraphrase appeared in any grep above.
