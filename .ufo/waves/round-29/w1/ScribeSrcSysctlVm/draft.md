# Round 29 wave 1 — S150 source draft (Linux v7.2 Documentation/admin-guide/sysctl/vm.rst)

Seat: ScribeSrcSysctlVm. Claim: C1 (depth), the O01–O04 kernel victim-selection anchors.
Revision of record: lane branch tip `81a061a67466c5e1be812814a895a4b5ed89b4ff` (declaration commit).
This file is a draft. Nothing here is a registry edit; the L1 integrates.

## 1. Fetch receipt

| item | value |
|---|---|
| instructed URL | `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/sysctl/vm.rst` |
| instructed URL outcome | HTTP **429** twice (`curl -sL` 19:57Z and after a 20 s wait 20:00Z), body 199 bytes `429: Too Many Requests` — the host is rate-limited, not challenged; no bot challenge was bypassed |
| URL actually opened | `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/sysctl/vm.rst?h=v7.2` (official kernel.org cgit, plain endpoint, ordinary `curl -sL`) |
| outcome | HTTP 200, 42424 bytes, 1153 lines, sha256 `bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce` |
| snapshot | `.ufo/waves/round-29/w1/ScribeSrcSysctlVm/S150-vm.rst` (byte-identical to the fetched body; `cmp` clean) |
| tag pin | annotated tag object `237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63` → commit `8d3ae59288f1e7d58d76558a6ee96d533bc5019f` (`git ls-remote … refs/tags/v7.2 refs/tags/v7.2^{}`) |
| cross-check, event kernel | `…/stable/linux.git/plain/…?h=v7.2.3` → HTTP 200, 42424 bytes, **same sha256**, `cmp` identical (`stable723-vm.rst`) |
| cross-check, host kernel | `…/stable/linux.git/plain/…?h=v7.2.11` → HTTP 200, 42424 bytes, **same sha256**, `cmp` identical (`stable-vm.rst`) |
| cross-check, independent seat | `.ufo/waves/round-29/w1/ScribeSkillOomRow/vm.rst` (fetched by another round-29 seat, URL unrecorded at the time of this read) → same 42424 bytes, **same sha256**, `cmp` identical to `S150-vm.rst` |

[obs] The bytes are identical at v7.2, at v7.2.3 (the kernel that logged event A,
`corpus/knowledge/oom-event-plane.md:185`) and at v7.2.11 (the running kernel,
`uname -r` → `7.2.11-arch1-1`), so the row's reading does not depend on which of the three
the corpus cites.

[unk] The instructed `raw.githubusercontent.com` URL was never served in this session, so the
identity of the raw-mirror bytes with these is not observed. The three kernel.org reads above are
the upstream authority for the tag; the sibling seat's file matches byte for byte, but the URL it
came from was not recorded when this draft was written.

## 2. Extracted paragraphs, with line numbers

`S150-vm.rst` is the plain RST source; lines are the physical lines of the saved bytes.

### 2.1 `oom_dump_tasks` — heading `:782`, body `:785-801`

```
785:Enables a system-wide task dump (excluding kernel threads) to be produced
786:when the kernel performs an OOM-killing and includes such information as
787:pid, uid, tgid, vm size, rss, pgtables_bytes, swapents, oom_score_adj
788:score, and name.  This is helpful to determine why the OOM killer was
789:invoked, to identify the rogue task that caused it, and to determine why
790:the OOM killer chose the task it did to kill.
792:If this is set to zero, this information is suppressed.  On very
793:large systems with thousands of tasks it may not be feasible to dump
794:the memory state information for each one.  Such systems should not
795:be forced to incur a performance penalty in OOM conditions when the
796:information may not be desired.
798:If this is set to non-zero, this information is shown whenever the
799:OOM killer actually kills a memory-hogging task.
801:The default value is 1 (enabled).
```

### 2.2 `oom_kill_allocating_task` — heading `:804`, body `:807-822`

```
807:This enables or disables killing the OOM-triggering task in
808:out-of-memory situations.
810:If this is set to zero, the OOM killer will scan through the entire
811:tasklist and select a task based on heuristics to kill.  This normally
812:selects a rogue memory-hogging task that frees up a large amount of
813:memory when killed.
815:If this is set to non-zero, the OOM killer simply kills the task that
816:triggered the out-of-memory condition.  This avoids the expensive
817:tasklist scan.
819:If panic_on_oom is selected, it takes precedence over whatever value
820:is used in oom_kill_allocating_task.
822:The default value is 0.
```

[obs] The page states the two branches explicitly: at zero a scan of "the entire tasklist" with
selection "based on heuristics"; at non-zero the allocating task is killed and "the expensive
tasklist scan" is avoided; `panic_on_oom` takes precedence; the default is 0.

[obs] `grep -c 'oom_score_adj' S150-vm.rst` → 1, and that single occurrence is the dump field list
at `:787`. The page does **not** define `oom_score_adj`, its range, or its effect on the score;
that is `proc.rst` (S148). The page does **not** state the badness formula or any evaluation
order; that is `mm/oom_kill.c` (S149).

## 3. Decision — **mined**, narrow scope

Mined, and the O01–O04 markers should cite it. Reasoning from the anchors themselves
(`tools/check-owed-statements-r29.py:48-55`; the frozen texts):

- O01 `corpus/knowledge/oom-event-plane.md:116` — "exactly the band the kernel scans first".
- O02 `corpus/knowledge/oom-event-plane.md:349` — "the +200 band is chosen first".
- O03 `corpus/knowledge/kill-event-deep-r8.md:147` — "under a kernel OOM the scan prefers the
  higher-scored, larger-RSS tasks first".
- O04 `corpus/knowledge/kill-event-deep-r8.md:260` — "the +200 band is scanned first".

Every one of the four asserts or implies an **ordering** of the victim search (a band "first").
A correction that says only "no band is chosen first" leaves a second, unstated assumption
intact: that a tasklist scan happens at all. `S150` is the document that makes the scan
conditional and names the branch in which it does not happen, with the default that governs an
unmodified host. S149 (`mm/oom_kill.c`, sibling seat) gives the code predicate and the
running-maximum pass; S150 gives the documented sysctl semantics that the corpus itself cites
from `/proc/sys/vm/*`. The two are not interchangeable: S149 cannot state the documented default
or the operator-facing meaning of the two values, and S150 cannot state the scoring formula.

What the row supports:

1. With `oom_kill_allocating_task` at 0, the killer scans the entire tasklist and selects by
   heuristics — so the event's own "scan" language is not wrong about a scan occurring, only
   about its order.
2. With it non-zero, no tasklist scan happens and the allocating task dies — so "the band the
   kernel scans first" is not a property of the killer at all in that configuration.
3. `panic_on_oom` overrides both, which bounds any victim-selection statement in a corpus that
   records `panic_on_oom=0`.
4. `oom_dump_tasks` is what produced the per-task `oom_score_adj` column the corpus reads; the
   dump names the chosen task, it does not rank candidates.

What the row must not be cited for: the `oom_badness` formula, that the highest score wins, that
no band exists in the code, or the meaning of `oom_score_adj` values. Those are S149 and S148.

[inf] Because the page says selection is "based on heuristics" at zero and skips selection at
non-zero, it is consistent with S149's single running-maximum pass and inconsistent with a
band-ordered search; but consistency is the inference, S149 is the proof. A marker that cites
S150 alone for "no band" would be citing it for more than it says.

## 4. Registry row (`corpus/SOURCES.md`, 11 columns)

Insert as one new line immediately after `corpus/SOURCES.md:153` (the S147 row), before the
blank line at 154 and `## Paths` at 155. Cells: `id | source | kind | tier | scope | anchor |
teaches | status | opened | recheck | used-by`.

| S150 | Linux v7.2 Documentation/admin-guide/sysctl/vm.rst — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/sysctl/vm.rst?h=v7.2 | docs | A | The two documented branches of vm.oom_kill_allocating_task (a full tasklist scan at zero, no scan at non-zero) with its default and the panic_on_oom precedence, plus the vm.oom_dump_tasks per-task dump fields, for the host kernel 7.2.11; not the oom_badness formula or the evaluation order (S149) and not the meaning of oom_score_adj (S148) | tag v7.2 annotated object 237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63, commit 8d3ae59288f1e7d58d76558a6ee96d533bc5019f; Documentation/admin-guide/sysctl/vm.rst lines 782-801 (oom_dump_tasks) and 804-822 (oom_kill_allocating_task); raw bytes sha256 bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce, 42424 bytes, 1153 lines; byte-identical at v7.2.3 and v7.2.11; snapshot .ufo/waves/round-29/w1/ScribeSrcSysctlVm/S150-vm.rst; fetched 2026-10-22 by plain curl from the kernel.org cgit plain endpoint because raw.githubusercontent.com returned HTTP 429 | At zero the OOM killer scans the entire tasklist and selects a task by heuristics, at non-zero it kills the allocating task and avoids that scan, panic_on_oom takes precedence over either, and the default is 0; oom_dump_tasks gates the per-task dump whose fields include oom_score_adj and names the task the killer chose | mined | 2026-10-22 | on-release | corpus/knowledge/oom-event-plane.md, corpus/knowledge/kill-event-deep-r8.md |

Landing condition (so the L1 can land it mechanically): keep `mined` and that `used-by` only if
the landed O01–O04 markers cite `S150` in their `basis` cell. If they cite `S149` only, set the
status to `queued` and `used-by` to `—` in the same commit; the teaching stays available and
uncounted, as S039/S040 were queued before a note cited them. The row must not be cited by
O05–O12: it has no operand in the MP4 qualifier debt, the `[unk]` or the storage-health rows.

M6 check by construction: status `mined`, and the `used-by` cell names both target basenames
(`oom-event-plane.md`, `kill-event-deep-r8.md`), so a marker basis containing `S150` passes M6
and, for O01–O04, satisfies M7 alongside `S149`.

## 5. Gate row

- Gate: `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/sysctl/vm.rst?h=v7.2` — accessed 2026-10-22 by plain `curl -sL` (no challenge, no auth), HTTP 200, 42424 bytes, sha256 `bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce`; located at `.ufo/waves/round-29/w1/ScribeSrcSysctlVm/S150-vm.rst:810`, section `oom_kill_allocating_task` (`:804`), first body paragraph: "If this is set to zero, the OOM killer will scan through the entire" (14 words, one physical line, `grep -cF` → 1). The section's second paragraph, `:815-817`, carries the no-scan branch and is quoted byte-exactly below.

The no-scan sentence, exactly as the saved bytes wrap it (three physical lines, two newlines
inside the quoted span, two spaces after the period — no character added or removed):

```
If this is set to non-zero, the OOM killer simply kills the task that
triggered the out-of-memory condition.  This avoids the expensive
tasklist scan.
```

Verification actually run:

| check | result |
|---|---|
| `python3`: `data.count(<the three-line span above>)` | 1 |
| word count of that span (newlines read as spaces) | 24 (≤ 25) |
| `grep -cF "If this is set to non-zero, the OOM killer simply kills the task that"` | 1 |
| `grep -cF "triggered the out-of-memory condition.  This avoids the expensive"` | 1 |
| `grep -cF "tasklist scan."` | 1 |
| `grep -cF "If this is set to zero, the OOM killer will scan through the entire"` | 1 |

Why two quotes: the RST source is hard-wrapped at ~72 columns, so the sentence naming the no-scan
branch cannot be a single `grep` line — `grep` is line-based and returns 0 for any cross-line
match. The Gate's mechanical quote is therefore the single-line `:810` fragment (which states the
scan branch and its "heuristics" selection, the part that contradicts a band order), and the
`:815-817` span is offered as the byte-exact no-scan sentence with its own check. Neither quote
exceeds 25 words.

The neighbouring paragraph, `oom_dump_tasks` (`:785-801`), carries no quote in this Gate; it is
cited by line range only.

## 6. Host value, read-only, and whether the captures already record it

Read at `2026-10-22T19:59:52Z` (`date -u`), each by `cat`, no write:

| sysctl | live value |
|---|---|
| `/proc/sys/vm/oom_kill_allocating_task` | **0** |
| `/proc/sys/vm/oom_dump_tasks` | 1 |
| `/proc/sys/vm/panic_on_oom` | 0 |
| `/proc/sys/vm/overcommit_memory` | 0 |
| `/proc/sys/vm/swappiness` | **100** |

`/proc/sys/vm/oom_kill_allocating_task` is **0 now**, so on the current configuration the scan
branch is the active one and the "no tasklist scan" case does not obtain.

The captures do **not** record it:

- `grep -c 'oom_kill_allocating_task' corpus/knowledge/oom-event-plane.md` → 0
- `grep -c 'oom_kill_allocating_task' corpus/knowledge/kill-event-deep-r8.md` → 0
- no file under `corpus/` and not `SKILL.md` contains the token. It does appear outside the
  knowledge corpus: `.ufo/waves/round-25/w2/RerunC2/src/S119.raw` (an older `mm/oom_kill.c`
  snapshot, 6 hits) and round-29 seat snapshots/drafts (S149.c, ScribeSkillOomRow/oom_kill.c,
  ScribeSrcReject/oom_kill-v7.2.c, ScribeMarkersOom/oom_kill.c, RevOomMechanism/oom_kill.c,
  RevF7Quant/oom_kill.c, `w1-spec.json`, `w1-dispatch.json`, `ScribeSrcOomKill.md`). None of
  those is the `/proc/sys/vm/*` capture; none records the value the host held.

The captures do record the neighbouring values: `oom_dump_tasks`=1 and `panic_on_oom`=0
(`corpus/knowledge/oom-event-plane.md:187`), and `oom_dump_tasks`=1, `panic_on_oom`=0,
`overcommit_memory`=0, `swappiness`=60 (`corpus/knowledge/kill-event-deep-r8.md:262`). Both name
the source as a `/proc/sys/vm/*` sweep (`corpus/knowledge/oom-event-plane.md:187`,
`corpus/knowledge/kill-event-deep-r8.md:262`, and the read list at
`corpus/knowledge/kill-event-deep-r8.md:328`), so the file was read and the value was not retained.

**The live read cannot be projected back to the event.** [obs] The captures were verified
2026-10-14 16:11–16:25 (UTC−3) (`corpus/knowledge/kill-event-deep-r8.md:9`) on kernel
`7.2.3-arch1-3` (`:6`); the current boot began 2026-10-22 04:55:40 (`uptime -s`), and the recorded
`swappiness`=60 has since become 100. The sysctl set has therefore changed at least once between
the capture and now, so today's 0 is not evidence of the value at 2026-10-13 23:44:30.
[unk] The event-time value of `oom_kill_allocating_task`; it is unrecoverable from the corpus and
no kernel-side record of it was captured.

Consequence for the O01–O04 markers: the corpus's dump shows a per-task `oom_score_adj` column
and a chosen task, which is consistent with a scan under `oom_dump_tasks`=1; it does not establish
which branch selected the victim. A correction should therefore qualify the ordering claim (no
band is "first"; the kernel keeps one running maximum over eligible tasks, S149) and state that
the no-scan branch is excluded only by the sysctl's documented default of 0 (S150) and by today's
observed 0 — not by anything the captures record. [inf] M4's verdict choice is the marker
author's; the evidence here supports `qualified` for all four, and O03's "prefers the
higher-scored, larger-RSS tasks first" is right about the score and wrong about the ordering word.

Capture recommendation for a later round: add
`cat /proc/sys/vm/oom_kill_allocating_task` to the `/proc/sys/vm/*` sweep record, so a future
victim-selection reading can exclude the no-scan branch from the capture instead of from a
sysctl default plus a live re-read eight days later.

## 7. Suggested marker basis (for the marker author; not a marker)

For O01–O04, `basis` should carry both sources, e.g.
`S149 (single running-maximum pass, no band order), S150 (scan is the oom_kill_allocating_task=0 branch; non-zero kills the allocator and skips the scan; default 0)`,
plus a path reference such as `corpus/knowledge/oom-event-plane.md:187` if the marker wants the
dump-setting evidence. `S150` alone would pass M6/M7 but would overstate the document (§3).

## 8. Limits

- [obs] Only the kernel.org cgit plain endpoint served the bytes; the instructed
  `raw.githubusercontent.com` URL returned HTTP 429 twice, so the row's `source` cell names the
  URL that was actually opened and says why.
- [obs] The Gate's flag-bearing sentence spans three physical RST lines, so the Gate carries a
  single-line mechanical quote (`:810`, `grep -cF` → 1) plus the byte-exact cross-line span
  (`:815-817`, `data.count` → 1). A judge that accepts only `grep -cF`-visible quotes will see the
  scan branch and not the no-scan branch in the Gate; the no-scan branch is then carried by the
  row's `teaches` cell and by §2.2's verbatim listing.
- [unk] `oom_dump_tasks`' dump of a task the killer chose is documented as a report of the
  choice, not as a ranking; whether a given dump can be read to reconstruct the scan path is not
  established by this page and was not measured here.
- [inf] Tier A is proposed: official kernel documentation of its own sysctl, matching the tier of
  S140/S141 (kernel tree rows).
- [obs] This seat ran no counter, no lane tool and no git write; it read `/proc/sys/vm/*` with
  `cat` and opened public URLs by plain `curl -sL` (three kernel.org plain reads, two
  `raw.githubusercontent.com` reads that returned 429).

## 9. Files written by this seat

- `.ufo/waves/round-29/w1/ScribeSrcSysctlVm/S150-vm.rst` — fetched bytes, sha256 `bf8ca026…c1ce`
- `.ufo/waves/round-29/w1/ScribeSrcSysctlVm/stable-vm.rst` — v7.2.11 cross-check, identical
- `.ufo/waves/round-29/w1/ScribeSrcSysctlVm/stable723-vm.rst` — v7.2.3 cross-check, identical
- `.ufo/waves/round-29/w1/ScribeSrcSysctlVm/raw-vm.rst` — the 199-byte HTTP 429 body, kept as
  the fetch-failure receipt
- `.ufo/waves/round-29/w1/ScribeSrcSysctlVm/draft.md` — this file
