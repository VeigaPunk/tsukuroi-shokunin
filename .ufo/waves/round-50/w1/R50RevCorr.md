VERDICT: defect-found

Seat R50RevCorr (reviewer, independent correction review; not a counted verdict seat). I read the round-49
critic report and the freeze bytes myself; I did not open `R50ExecGRCorr`'s report or any executor receipt.
Bytes under test: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show
8029cdba1049df25632c91a23c8db4eefb54be5f:corpus/knowledge/btrfs-scrub-grounding-r45.md` (307 lines, sha256
`37370cc9ff33ffac9500f9ad5e72913a471e902399dff8a98cf0a83f67df7cac`) and `:corpus/SOURCES.md` (358 lines).
The correction pass is commit `43bcce06` ("round-50: FREEZE … corrections applied before data", 2026-10-28
15:36:17 -0300); the entry did not change between `43bcce06` and the freeze `8029cdba`
(`git diff --stat 43bcce06 8029cdba -- corpus/knowledge/… corpus/SOURCES.md` → empty). Round-49 freeze for the
before/after diff: `55c07cd3` (`.ufo/waves/round-49/frozen/FROZEN.md`). Snapshots were digest-checked before
any line was read (`hashes.txt`): S240 ioctl.c `7b3488f2…ba01`, S247 dev-replace.c `f07ef0a0…4f3a`,
S242 scrub.c `f347931b…25b8`, S243 sysfs.c `ce146120…3a01`, S237 cmds/scrub.c `48df2e2f…f0801` — all equal
to the `SOURCES.md` pins.

## 1. Disposition of the four round-49 defects

| # | Round-49 defect (`.ufo/waves/round-49/w1/R49CritGR2b.md:19-24`) | Disposition at `8029cdba` | Evidence |
|---|---|---|---|
| 1 | the `[inference]` mark's ioctl conjunct ("not pinned here" / "unchanged") | **adopted verbatim — and the adopted sentence overreaches** | entry:83-85 is the critic's text character for character (only the wrap and the sentence-final `.` differ); substance correct, see §3 D2 |
| 2 | S240 missing from `source:` and QUALITY 7 | **adopted verbatim** | entry:1 lists `S240` with snapshot path + sha256 and the cite set; entry:261 reads "cite S246-S248 and S240" |
| 3 | dev-replace.c:1128 quote missing its `* ` leader | **adopted verbatim, exact** | entry:127; pinned line after stripping leading whitespace is exactly `* Scrub doing the replace isn't running so we need to do the` (`quote-check.txt`, 29/29 GR2 quotes exact) |
| 4 | undeclared S247 range gap | **adopted with a change of form** (separate bullet instead of an appended clause), content exact | entry:229-232 |

Defect 4's change of form is harmless and arguably better (the round-49 sentence at entry:225-227 keeps its
wording). The pass also added a companion S240 gap bullet (entry:233-235) that the critic did not ask for; it
is justified — the correction's own new cites at `ioctl.c:3093-3095`, `:3109-3110`, `:3115` are outside S240's
registered ranges — and its parenthetical claim ("re-fetched byte-identical on 2026-10-28") is substantiated:
`SOURCES.md:249` carries the round-48 reopen and `R50ScoutReopenS240/fetch-meta.txt` re-fetched the live body at
`Date: Wed, 28 Oct 2026 19:04:52 GMT` with `cmp … BYTE_IDENTICAL` and the same sha256. Note the receipt postdates
the freeze (15:36 -0300 = 18:36 GMT), so at freeze time the claim rested on `SOURCES.md:249` alone.

## 2. Test (a) — does the narrowed mark say exactly what the pinned ioctl lines do?

**Yes for all three citations, and the `-EFAULT` arm is correctly identified as replacing the
`btrfs_scrub_dev` return; the wording names the wrong copy and omits the pre-call returns.**

Pinned `ioctl.c` (S240, digest verified), `ioctl-excerpt.txt`:

- `3093-3095` is the call: `ret = btrfs_scrub_dev(fs_info, sa->devid, sa->start, sa->end,` / `&sa->progress,
  sa->flags & BTRFS_SCRUB_READONLY,` / `false);` — exactly the three lines the mark cites.
- `3109-3110` is `if (copy_to_user(arg, sa, sizeof(*sa)))` / `ret = -EFAULT;` — this is the copy of the
  `btrfs_ioctl_scrub_args` structure **back to user space**, and it replaces whatever `btrfs_scrub_dev`
  returned (success `0` or any negative errno).
- `3115` is `return ret;` (after `mnt_drop_write_file` at 3113 on the write path).

So the arm the `-EFAULT` replaces is the call's own return value, not an argument-copy failure of the incoming
arguments. The incoming copy is `memdup_user` at `ioctl.c:3080-3082`, and it returns `PTR_ERR(sa)` — `-EFAULT`
only for a bad user pointer, `-ENOMEM` for an allocation failure. Reading the entry's phrase "unless the
argument copy fails, when it returns `-EFAULT`" as the in-copy therefore makes the sentence false for
`-ENOMEM`; reading it as the out-copy makes it true. That ambiguity is the defect (D2, §3).

## 3. Errors the correction introduced or left reachable

**D2 (minor, inside the frozen row bytes; introduced by this pass).** Entry:83-85, adopted verbatim from the
critic, is false as an unqualified statement about the scrub-start ioctl. Before it reaches `ioctl.c:3093` the
same ioctl returns `-EPERM` (`3072-3073`), `-EINVAL` (`3075-3077`), the `memdup_user` error (`3080-3082`),
`-EOPNOTSUPP` (`3084-3085`) or `mnt_want_write_file`'s error (`3087-3090`). The row's own caller is the
counterexample: the Host reading fixes `CapEff=0` (capture.txt:1), so on this host the ioctl returns `-EPERM`
and never the `btrfs_scrub_dev` value. `R50CritGR2a` counts this; `R50CritGR2c` explicitly does not
("sit outside the sentence's subject"); `R50RevGR2c` calls the bracket correct. My independent reading: the
subject of the sentence is the ioctl's own path, so the qualification must be "once a call reaches the call" —
counted as a defect, minor, non-falsifying for the mechanistic claims.

Exact replacement for entry:83-85 (keeps the frozen counter's required substring
`print these returns is not pinned here`, `tools/check-scrub-admission-r50.py:109`):

```
[inference: how `btrfs scrub start` and `btrfs scrub status` print these returns is not pinned here; the
scrub-start ioctl's own path is pinned and, once a call reaches the `btrfs_scrub_dev` call, returns that call's
value (ioctl.c:3093-3095) unless the copy of the scrub args back to user space fails, when it returns `-EFAULT`
instead (ioctl.c:3109-3110, ioctl.c:3115); a call refused before it returns `-EPERM` (ioctl.c:3072-3073),
`-EINVAL` (:3075-3077), the `memdup_user` error (:3080-3082), `-EOPNOTSUPP` (:3084-3085) or
`mnt_want_write_file`'s error (:3087-3090)]
```

**D1 (blocking, provenance; pre-existing, not repaired by this pass; same class as the S247 defect the pass
did fix).** The S242 gap declaration is incomplete. `SOURCES.md:251` registers S242 at
`1365-1385, 3140-3162, 3215-3226, 3321-3337`; GR2 cites and quotes `scrub.c:3094`, `:3095` (Quotes at entry
lines 100-101), `:3109` (:135), `:3114` (:137) and `:3138` (:139), all below 3140. Entry:225-226 declares only
"`scrub.c:3081`, 3123, 3133 or 3139". `3138` belongs to the same `-EIO` test the sentence is about, so the
enumeration is short even within its own scope. All three live GR2 `partly` seats bind on exactly this
(`R50CritGR2a` D1, `R50CritGR2c` DEFECT, `R50RevGR2c` Defect).

Exact replacement of the S242 clause at entry:225-226 (row hash untouched — Limits is outside every row
extent):

```
  quoted lines (1143-1144, 1235, 1276-1300). Three registrations of older rows stay as they are: S242's declared
  ranges (1365-1385, 3140-3162, 3215-3226, 3321-3337) do not list `scrub.c:3081`, 3094-3095, 3109, 3114, 3123,
  3133, 3138 or 3139; S243's
```

**D3 (new inconsistency introduced by the pass; already costing a counted GR1 verdict).** The pass made
`dev-replace.c:1128` carry its `* ` leader and left `cmdline.c:147` a line-slice in the same entry: entry:27
quotes `"potentially suffixed with K, M, G, T, P, E."` while the pinned line is
`*\tpotentially suffixed with K, M, G, T, P, E.` (`quote-slices.txt`: entry-wide 53 quotes, 52 exact after
stripping leading whitespace, exactly 1 slice — this one). Before the pass both were slices, so the entry was
consistent; now it applies the round-49 critic's rule to GR2 and not to GR1, and `R50RevGR1b` bound GR1
`partly` on precisely that asymmetry. Fix (moves the GR1 row hash): entry:27 →
`**Quote.** `S246` cmdline.c:147: "*	potentially suffixed with K, M, G, T, P, E."` (a tab after the `*` is the
pinned byte; the counter's whitespace-normalised predicate also accepts a space).

**D4 (low, entry-level, adjacent to the corrected line).** QUALITY 3 (entry:258) still says "`[inference]`
marks the two consequences the pinned code does not decide" while the entry carries `[inference]` at lines 53,
83, 162, 167, 210, 215, and the correction made 83 a mark that also states a decided fact. QUALITY 7
(entry:261) now names S246-S248 and S240 but still omits S242, S243, S237 and S244 — all tier-A external
sources cited by the rows (`SOURCES.md:253` gives S244 tier A). Neither is counted by any GR2 seat; both are
one-line fixes outside every row.

**D5 (risk, not a defect; no seat bound on it).** The mark's surviving conjunct "how `btrfs scrub start` and
`btrfs scrub status` print these returns is not pinned here" is exposed to the round-49 critic's own argument:
S237 pins btrfs-progs `cmds/scrub.c` whole-file (`48df2e2f…f0801`, the entry's own source line) and that file
contains the printing path (`cmds/scrub.c:965-970` records the start ioctl's return, `:1064` and `:1796` print
it). The distinction that keeps the mark true is that GR2 cites none of those lines and S237's registered ranges
(`67-70, 280-330, 446-535, 826-895, 1110-1125, 1186-1220, 1330-1340, 1498-1512, 1925-1945`) do not cover them.
The frozen counter requires the literal phrase (`…:109`), so any rewording must keep it. Recommendation: leave
it unless a GR2 seat binds; if the row moves for D2, add "(the row cites no btrfs-progs printing line; S237
pins that file whole-file)".

## 4. Test (b) — every `file:line` in GR2 against the S-row ranges at the freeze

Mechanical extraction of the GR2 section (entry lines 56-152), `gr2-citations.txt`:

| S-row | registered ranges (`SOURCES.md` at `8029cdba`) | GR2 cites inside | GR2 cites outside | declared at entry:229-235? |
|---|---|---|---|---|
| S247 | 700-703, 1143-1144, 1235, 1256-1268, 1276-1300 | 700, 701, 703, 1143, 1144, 1235, 1259, 1265, 1268, 1278-1279, 1286-1287, 1287, 1288-1297 | 1111, 1126-1144 (of which 1126-1142, incl. 1127-1129 and 1128), 1171-1195 (incl. 1184-1188) | **yes, complete** (1111, 1126-1142, 1171-1195, 1184-1188) |
| S240 | 3066-3075, 3118-3140, 5578-5584 | 3132, 3133 | 3093-3095, 3109-3110, 3115, 3190 | **yes, complete** |
| S242 | 1365-1385, 3140-3162, 3215-3226, 3321-3337 | 3142, 3147, 3148, 3149, 3153, 3159, 3222, 3336 | 3081, 3094, 3095, 3109, 3114, 3123, 3133, 3138, 3139 | **no — 3094, 3095, 3109, 3114, 3138 undeclared** (D1) |
| S243 | 72-74, 2021-2049, 2113 | — | 1288, 2015 | **yes, complete** (entry:226-227) |
| S249 | own-work capture, no line ranges | capture.txt:1, capture.txt:9 | — | n/a |

Both new declarations are exact and neither is over-inclusive: S247's four entries cover every outside cite
(1184-1188 is a subset of 1171-1195 — redundant, not wrong), and S240's four cover every outside cite. The
S242 enumeration is the one that does not match the row's citations. `R50CritGR2a`, `R50CritGR2c` and
`R50RevGR2c` reach the same conclusion independently.

## 5. Did a correction introduce a NEW error?

Two, both stated above: **D2** (the adopted bracket overreaches the ioctl it describes, and "the argument
copy" names the out-copy) and **D3** (the entry now applies one quote standard to GR2 and another to GR1, and
a counted GR1 seat has bound `partly` on it). The mechanistic content of GR2 is unchanged by the pass and
still resolves line by line: `dev-replace.c:1111` is the STARTED-branch cancel, `1126-1144` the SUSPENDED
branch with its comment at `1127-1129`, `1171-1195` the unmount suspend with the state move at `1184-1188`,
`1278-1287` the `is_valid` gate plus STARTED/SUSPENDED, `scrub.c:3094-3095` the `-EAGAIN` arm, `3109-3116` the
context/worker errors, `3120-3142` the device checks, `3146-3155` the `-EINPROGRESS` arm before `3159` attaches
the context, `3222` the clear, `3336` the progress return, `ioctl.c:3132-3133` the `CAP_SYS_ADMIN` check,
`3190` the exclusive operation (`devreplace-excerpt.txt`, `scrub-excerpt.txt`, `ioctl-excerpt.txt`).

Row hashes: I reproduced all three from the freeze bytes. GR2 `a2e955ce…b7f3f` = the 96 content lines of
`## GR2`…`## GR3` plus the blank separator, LF-joined (`raw_noLF` = `trailingLF`); the same 96 lines with no
trailing newline hash to `e41b3b6b…`, so `FROZEN.md`'s "no trailing LF" is off by one newline (the same record
nit `R49CritGR2b` and `R50CritGR2a` filed; the printed value is reproducible and is what every GR2 seat's
line 2 carries). GR1 `3a2ba180…fee1` and GR3 `43430a14…c32c` are unchanged from round 49 — the pass moved GR2
only, as its defects 1 and 3 require.

## 6. What this means for the L1 (operational)

- Three GR2 seats are already bound `partly` at `a2e955ce` (`R50CritGR2a`, `R50CritGR2c`, `R50RevGR2c`), and a
  bound-format negative blocks the row whatever its citations
  (`tools/check-scrub-admission-r50.py:415-417`). GR2 `verdicts_ok` is 0 as the wave stands.
- D1's fix is in Limits, outside every row extent → the row hash does not move → only the three `partly` seats
  need re-reading (the three `holds` seats stay credited at `a2e955ce`).
- D2's fix is inside the row → GR2's hash moves → `FROZEN.md`'s row-hash table and all six GR2 seats' line 2
  must move, so the whole GR2 sextet re-reads. If D2 is left, `R50CritGR2a` can be expected to re-bind
  `partly` on it after D1 is fixed.
- D3's fix is inside GR1 → GR1's hash moves → the GR1 sextet re-reads; leaving it keeps `R50RevGR1b`'s
  `partly` blocking GR1.
- D4 is free (Limits/QUALITY only). D5 needs no action unless a seat binds.

## 7. Not done

I did not run the C1 admission counter, the C2/C3 counters, or any census `--selftest`; I did not re-fetch any
upstream URL (digests were checked against the committed `SHA256SUMS` and `SOURCES.md` pins, and the S240
live-identity claim was checked against `R50ScoutReopenS240/fetch-meta.txt`, not re-run); I did not read
`R50ExecGRCorr`'s report or any executor receipt; I read the three live GR2 `partly` reports only to compare
their findings with mine, and `R50RevGR1b` only for its first finding. No lane file was written except this
report and its receipts; no git or jj mutation was run anywhere.

Receipts: `.ufo/waves/round-50/w1/R50RevCorr/` — `hashes.txt`, `entry-lines.txt`, `gr2-citations.txt`,
`quote-check.txt`, `quote-slices.txt`, `ioctl-excerpt.txt`, `devreplace-excerpt.txt`, `scrub-excerpt.txt`.
