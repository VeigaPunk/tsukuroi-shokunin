VERDICT: supports

# C1RevQuotes — independent quote audit of GR1/GR2/GR3 (freeze revision 77e9e2b2e96b85d8f048ae2087e246a542b71611)

Item C1-R8. Every `**Quote.**` line in `## GR1`, `## GR2`, `## GR3` of
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 77e9e2b2e96b85d8f048ae2087e246a542b71611:corpus/knowledge/btrfs-scrub-grounding-r45.md`
verified against the pinned snapshots with my own parser (this seat's implementation at
`.ufo/waves/round-47/w1/C1RevQuotes/quote_audit.py`; the frozen counter was NOT imported — read afterwards for
semantics comparison only).

## Method

1. Doc extracted: `git -C <lane> show 77e9e2b…:corpus/knowledge/btrfs-scrub-grounding-r45.md` → 264 lines; headers at
   lines 14 (`## GR1`), 55 (`## GR2`), 141 (`## GR3`), 187 (`## How this changes OS triage`), 200, 222, 233, 254.
2. Row extents (fail-closed): GR1 = 14..54, GR2 = 55..140, GR3 = 141..186; zero unexpected `## ` lines inside any
   extent; parser found structural_problems=[] (`receipts/quote-audit-results.json`).
3. Every snapshot digest re-verified before reading (`receipts/snapshot-digests.txt`): all 12 files in
   round-45/frozen/src, round-44/frozen/src, round-42/frozen/src `sha256sum -c SHA256SUMS` → OK (also round-43
   ioctl.c, used only for the S240 prose-cite cross-check → OK). `hostcap/` ships no SHA256SUMS (S249 is own-work);
   capture.txt observed sha256 `f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70`.
4. Quote parse: `^\*\*Quote\.\*\* \`(S\d+)\` (\S+):(\d+): "(.*)"$`; source map S246/S247/S248 →
   round-45/frozen/src, S242/S243/S244 → round-44/frozen/src, S237 → round-42/frozen/src/scrub.c; each snapshot's
   digest re-checked inside the parser against the manifest values before use (digests_ok: true).
5. Comparison: whitespace-run normalization (`' '.join(s.split())`), equality of quoted text vs the full cited line —
   stricter than the frozen counter, which uses substring containment
   (`counter_frozen.py:278`: `if norm(want) not in norm(got[line_no - 1])`).

## Result

52 quote lines found (12 GR1 + 28 GR2 + 12 GR3 — matches the expected 52). 51 VERIFY by strict equality.
1 deviates under strict equality but passes the frozen counter's containment rule (detail below).
Frozen counter cross-check at the freeze revision: quotes GR1 12/12, GR2 28/28, GR3 12/12, `quotes_ok: 3`,
`structural_ok: 1` (`receipts/frozen-counter-quotes-leg.json`).

| Row | Doc line | Cite | Result |
|-----|----------|------|--------|
| GR1 | 27 | `S246 cmdline.c:147` | FAIL(strict) — cited line is `*\tpotentially suffixed with K, M, G, T, P, E.` (kernel-doc comment prefix `* ` omitted from the quote); PASS under the counter's substring rule |
| GR1 | 29 | `S246 cmdline.c:156` | VERIFY |
| GR1 | 31 | `S246 cmdline.c:159` | VERIFY |
| GR1 | 33 | `S246 cmdline.c:189` | VERIFY |
| GR1 | 35 | `S246 cmdline.c:191` | VERIFY |
| GR1 | 37 | `S246 cmdline.c:192` | VERIFY |
| GR1 | 39 | `S246 vsprintf.c:86` | VERIFY |
| GR1 | 41 | `S246 kstrtox.c:29` | VERIFY |
| GR1 | 43 | `S246 kstrtox.c:30` | VERIFY |
| GR1 | 45 | `S246 kstrtox.c:33` | VERIFY |
| GR1 | 47 | `S243 sysfs.c:2040` | VERIFY |
| GR1 | 49 | `S243 sysfs.c:2043` | VERIFY |
| GR2 | 78 | `S247 dev-replace.c:700` | VERIFY |
| GR2 | 80 | `S247 dev-replace.c:701` | VERIFY |
| GR2 | 82 | `S247 dev-replace.c:703` | VERIFY |
| GR2 | 84 | `S247 dev-replace.c:1259` | VERIFY |
| GR2 | 86 | `S247 dev-replace.c:1265` | VERIFY |
| GR2 | 88 | `S247 dev-replace.c:1268` | VERIFY |
| GR2 | 90 | `S242 scrub.c:3081` | VERIFY |
| GR2 | 91 | `S242 scrub.c:3094` | VERIFY |
| GR2 | 92 | `S242 scrub.c:3095` | VERIFY |
| GR2 | 94 | `S242 scrub.c:3148` | VERIFY |
| GR2 | 96 | `S242 scrub.c:3149` | VERIFY |
| GR2 | 98 | `S242 scrub.c:3147` | VERIFY |
| GR2 | 100 | `S242 scrub.c:3153` | VERIFY |
| GR2 | 102 | `S242 scrub.c:3123` | VERIFY |
| GR2 | 104 | `S242 scrub.c:3133` | VERIFY |
| GR2 | 106 | `S242 scrub.c:3139` | VERIFY |
| GR2 | 108 | `S242 scrub.c:3142` | VERIFY |
| GR2 | 110 | `S247 dev-replace.c:1287` | VERIFY |
| GR2 | 112 | `S247 dev-replace.c:1235` | VERIFY |
| GR2 | 114 | `S243 sysfs.c:1288` | VERIFY |
| GR2 | 116 | `S243 sysfs.c:2015` | VERIFY |
| GR2 | 118 | `S247 dev-replace.c:1143` | VERIFY |
| GR2 | 120 | `S247 dev-replace.c:1144` | VERIFY |
| GR2 | 122 | `S242 scrub.c:3336` | VERIFY |
| GR2 | 124 | `S242 scrub.c:3109` | VERIFY |
| GR2 | 126 | `S242 scrub.c:3114` | VERIFY |
| GR2 | 128 | `S242 scrub.c:3138` | VERIFY |
| GR2 | 130 | `S242 scrub.c:3222` | VERIFY |
| GR3 | 158 | `S244 btrfs-scrub@.service:9` | VERIFY |
| GR3 | 160 | `S244 btrfs-scrub@.service:10` | VERIFY |
| GR3 | 162 | `S248 systemd.kill.xml:68` | VERIFY |
| GR3 | 164 | `S248 systemd.kill.xml:91` | VERIFY |
| GR3 | 166 | `S248 systemd.kill.xml:96` | VERIFY |
| GR3 | 168 | `S248 systemd.kill.xml:101` | VERIFY |
| GR3 | 170 | `S248 systemd.kill.xml:108` | VERIFY |
| GR3 | 172 | `S248 systemd.kill.xml:114` | VERIFY |
| GR3 | 174 | `S248 systemd.kill.xml:115` | VERIFY |
| GR3 | 176 | `S237 scrub.c:421` | VERIFY |
| GR3 | 178 | `S237 scrub.c:1546` | VERIFY |
| GR3 | 180 | `S237 scrub.c:439` | VERIFY |

## Finding 1 (minor): one quote is a de-prefixed excerpt, not the full cited line

GR1 doc line 27 quotes `S246` cmdline.c:147 as `"potentially suffixed with K, M, G, T, P, E."`; the cited line is the
kernel-doc comment line ` *` TAB `potentially suffixed with K, M, G, T, P, E.` (verified via `sed -n 147p | cat -A`).
The quote is a verbatim substring and supports its claim exactly, but it is not the whole line. The frozen counter's
containment rule admits it (`counter_frozen.py:278`), and the counted predicate (`quotes_ok == 3`) is met at the
freeze revision, so admission is unaffected. Noted for depth hygiene only.

## Claim clauses with no quote (coverage audit)

Host-reading values citing capture.txt were checked line-by-line (9-line file; no manifest, own-work):

- GR1 "reads `scrub_speed_max` 0, mode 644, owner root (capture.txt:8)" → line 8
  `scrub_speed_max 1d02a454-…/devinfo/1/scrub_speed_max mode=644 owner=root value=0` — supports.
- GR1/GR2 "uid 1000 with no effective capabilities (capture.txt:1)" → line 1 `captured 2026-10-27T02:09:52Z uid=1000 CapEff=0000000000000000` — supports.
- GR2 "filesystem lists devid 1 only (capture.txt:9)" → line 9 `devinfo 1d02a454-…/devinfo devids=1` — supports.
- GR3 "systemctl show … (capture.txt:3)" → line 3 `unit_show FinalKillSignal=9 FragmentPath=/usr/lib/systemd/system/btrfs-scrub@.service KillMode=control-group KillSignal=2 SendSIGKILL=yes TimeoutStopUSec=5s` — all five reported properties present.
- GR3 "stop default comes from 10-faster-shutdown.conf line 2 (capture.txt:4)" → line 4 `stop_default /etc/systemd/system.conf.d/10-faster-shutdown.conf:2:DefaultTimeoutStopSec=5s` — supports.
- GR3 "a drop-in no installed package lists (capture.txt:5)" → line 5 `dropin_owner /etc/systemd/system.conf.d/10-faster-shutdown.conf none` — supports.
- GR3 "systemd is 262-1-arch (capture.txt:2)" → line 2 `kernel 7.2.11-arch1-1 systemd systemd 262 (262-1-arch)` — supports.

Statement clauses carrying no `**Quote.**` at all (flagged per the item; none falsifies the rows):

1. GR1, "either case" suffix letters and "each step multiplying by a further 1024 (a 10-bit shift)": the evidence is
   the memparse switch cases `case 'E': case 'e': shl += 10; …` at cmdline.c:161-187 — not quoted. The quoted lines
   (147, 189-192) cover the suffix set, digit-precedence and overflow only. Adjacent-unquoted, not contradicted.
2. GR1, "picks hexadecimal for a leading `0x`": the assignment `*base = 16;` (kstrtox.c:31) is not quoted; the
   condition (line 30) and the octal branch (line 33) are. Adjacent-unquoted.
3. GR1, sysfs "returns `-EINVAL` unless the text ends there": the `return -EINVAL;` line (sysfs.c:2044) is not
   quoted; the guard `if (*endptr != 0)` (line 2043) is. Adjacent-unquoted.
4. GR1, "0 means no limit, SR8" — rule-source cite (SR8 not among pinned snapshots); no quote, by design.
5. GR2, "replace ioctl takes [the exclusive op] around the start, S240 ioctl.c:3190" — prose cite, not a Quote line.
   Cross-checked anyway: round-43/frozen/src/ioctl.c digest OK (SHA256SUMS); line 3190 is
   `if (!btrfs_exclop_start(fs_info, BTRFS_EXCLOP_DEV_REPLACE)) {` — supports the prose.
6. GR2, "by SR7 makes a privileged progress query … answer 0": rule-source cite (SR7 unpinned); the mechanism is
   nonetheless quoted at scrub.c:3336 (`sctx ? 0 : -ENOTCONN`). Covered by quote for the 0/-ENOTCONN behavior.
7. GR3, "With `-B` the start does not fork into the background (btrfs-progs `scrub.c:1512`)" — NO quote and the
   btrfs-progs source is not pinned (no S-id). This is the one load-bearing behavioral clause with no pinned
   evidence; it is followed by quoted pinned lines for the SIGINT handler (S237 :1546, :439) and the cancel ioctl
   (S237 :421). Flagged; an unpinned `scrub.c:1512` cite is the only support.
8. GR3, SR3/SR9 rule cites (cancel ioctl record semantics) — rule-source cites, no quotes, by design; the
   inference about the canceled record within 5 s is explicitly marked `[inference]` in the doc.

## Independent source-order reading (depth cross-check, not quote verification)

S242 scrub.c at the freeze snapshot reads, in order: `btrfs_fs_closing` → `-EAGAIN` (3094-3095) →
`scrub_setup_ctx` (3109) → `scrub_workers_get` (3114) → `-ENODEV` (3123) → `-EROFS` (3133) → `-EIO` (3142) →
`-EINPROGRESS` with condition `dev->scrub_ctx || (!is_dev_replace && btrfs_dev_replace_is_ongoing(...))`
(3147-3153). This matches the AMENDED GR2 claim that the filesystem-closing `-EAGAIN` leads the ordering and that
the non-replace `-EINPROGRESS` refusal is gated on `!is_dev_replace`. The doc quotes lines 3148/3149 before 3147
(presentation order), which each verify individually.

## What I did not do

- Did not verify quotes outside GR1-GR3 extents (none exist in the doc outside; the `## Limits` and gate-status
  sections carry no `**Quote.**` lines — grep count over the whole file is 52, all inside the three rows).
- Did not re-derive the round-46 wave evidence or run any host-mutating command (none needed; all sources frozen).
- Did not import or execute the frozen counter inside my parser; it was run once standalone for the cross-check
  receipt.

## Receipts

Seat dir `.ufo/waves/round-47/w1/C1RevQuotes/`: `snapshot-digests.txt`, `quote_audit.py` (my parser),
`quote-audit-results.json` (per-quote machine results), `frozen-counter-quotes-leg.json`.
Scratch `/fast/scratch/hyaku/tsukuroi-r47/C1RevQuotes/` removed after copying receipts.
