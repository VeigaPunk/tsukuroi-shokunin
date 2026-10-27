VERDICT: defect-found

Item F-1: the four `## Gate` rows for S242-S245 are drafted below and all four SOURCES rows parse as 11 cells with
anchors that name the pinned tag/commit and digests. One real anchor defect: the S242 anchor's line ranges omit
`fs/btrfs/scrub.c:3079-3085`, so the lesson's own `S242` quote at `scrub.c:3081` — the `is_dev_replace` signature
that carries the pre-wave SR7 narrowing landed in `7e081698` — sits outside every range the row names. Two nits on
S244/S245 digests. Nothing here falsifies C1 or C2.

# What I opened (live, 2026-10-27T00:20:26Z–00:20:27Z UTC; host local 2026-10-26T21:20-0300)

Scratch `/fast/scratch/hyaku/tsukuroi-r44/SrcGateNew/curl`; every fetch was `curl -sfL --max-time 90` and every byte
was hashed against `.ufo/waves/round-44/frozen/src/SHA256SUMS`:

| source | URL opened | HTTP | bytes | sha256 = frozen? |
|---|---|---|---|---|
| S242 | `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/scrub.c?h=v7.2.11` | 200 | 100417 | yes `f347931b…938ca5b8` |
| S243 | `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/sysfs.c?h=v7.2.11` | 200 | 72925 | yes `ce146120…44f731c43` |
| S244 | `https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/7.1-1/btrfs-scrub@.timer` | 200 | 160 | yes `9a0b6cc2…9d6f8ad` |
| S244 | `https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/7.1-1/btrfs-scrub@.service` | 200 | 190 | yes `eaa7af92…fb240252` |
| S244 | `https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/7.1-1/PKGBUILD` | 200 | 3057 | yes `3b803e8b…6c10ce98` |
| S245 | own-work, read from `.ufo/waves/round-44/frozen/hostcap/` (no fetch: `capture.txt` sha256 `efb52388…e84900`, `capture.sh` sha256 `6a297e4f…8376f6d`) | — | — | n/a |

Cross-check: `https://raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/btrfs/scrub.c` (100417 B) and `…/sysfs.c`
(72925 B) are byte-identical to the git.kernel.org `plain ?h=v7.2.11` bytes (`cmp -s` silent; same two sha256).

Tag pinnings re-verified live:
- `git ls-remote https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git 'refs/tags/v7.2.11*'` →
  `8316c24ec1b77dba19ba072ca4fe251b36dc65d3 refs/tags/v7.2.11` and
  `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea refs/tags/v7.2.11^{}` — matches the S242/S243 anchor's peeled commit.
- `https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fpackaging%2Fpackages%2Fbtrfs-progs/repository/tags/7.1-1`
  → 200, `"name":"7.1-1"`, `"id":"0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0"`,
  `"committed_date":"2026-07-15T09:15:06.000+02:00"` — matches the S244 anchor's commit.

Quote location check: 23 candidate quote lines were read out of the freshly fetched bytes and compared to the exact
strings used in the draft rows and in the lesson's `**Quote.**` lines — `mismatches 0` (receipt
`quote-verify.txt`, driver re-run from the receipt copy).

# Draft — exact Markdown rows for `corpus/lessons/round-44.md` `## Gate`

Proposed section lead (adapt the seat name if the L1 prefers its own wording):

### New SOURCES rows S242-S245 (`corpus/SOURCES.md:251-254` at `7e081698`; each row re-opened live with `curl -sfL` by wave-1 seat SrcGateNew on 2026-10-27T00:20:26Z, hashed against `.ufo/waves/round-44/frozen/src/SHA256SUMS`; every quoted line checked byte-exact at its location)

| Row | URL (access 2026-10-27T00:20:26Z) | Located quote (≤25 words) | Location |
|---|---|---|---|
| S242 | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/scrub.c?h=v7.2.11 (raw `plain/fs/btrfs/scrub.c?h=v7.2.11`, 100417 B, byte-identical to https://raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/btrfs/scrub.c; sha256 `f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8`; tag v7.2.11 peeled `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`) | "return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;" / "if (bwlimit == 0)" / "return;" | `.ufo/waves/round-44/frozen/src/scrub.c:3336, 1381-1382` (lookup `:3329-3333`; `is_dev_replace` signature `:3081`) |
| S243 | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/sysfs.c?h=v7.2.11 (raw `plain/fs/btrfs/sysfs.c?h=v7.2.11`, 72925 B, byte-identical to https://raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/btrfs/sysfs.c; sha256 `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43`; same tag peel) | "__INIT_KOBJ_ATTR(_name, 0644, _show, _store)" / "sysfs_emit(buf, \"%llu\n\", READ_ONCE(device->scrub_speed_max))" / "limit = memparse(buf, &endptr);" / "if (*endptr != 0)" / "return -EINVAL;" | `.ufo/waves/round-44/frozen/src/sysfs.c:74, 2028, 2040, 2043-2044` (registration `:2048-2049`, `:2113`) |
| S244 | https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/tree/7.1-1 (raw `-/raw/7.1-1/btrfs-scrub@.timer`, `…/btrfs-scrub@.service`, `…/PKGBUILD`, 160 / 190 / 3057 B; timer sha256 `9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad`, service `eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252`, PKGBUILD `3b803e8b05d84900fcdab3513720c8005345acd1fe34ded6eaa3b7596c10ce98`; tag 7.1-1 commit `0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0`) | "OnCalendar=monthly" / "Persistent=true" / "WantedBy=timers.target" / "ExecStart=/usr/bin/btrfs scrub start -B %f" / "KillSignal=SIGINT" / "install -Dm644 btrfs-scrub@.timer \"${pkgdir}/usr/lib/systemd/system/btrfs-scrub@.timer\"" | `.ufo/waves/round-44/frozen/src/btrfs-scrub@.timer:5, 8, 11; btrfs-scrub@.service:10, 9; PKGBUILD:101` |
| S245 | own-work `.ufo/waves/round-44/frozen/hostcap/` (`capture.sh` run 2026-10-26T23:53:22Z, uid 1000, `CapEff=0000000000000000`; `capture.txt` sha256 `efb523889035cba62235d904b9e254068a7083dd07e7bb338ce2a803a3e84900`, `capture.sh` sha256 `6a297e4ff9c7030c6cfe10feeb6c9198ccf31a574fbe6ce1b755dbf318376f6d`) | "var_lib_btrfs absent" / "mode=644 owner=root value=0" / "wants_btrfs_scrub_instances 0" / "is_enabled_btrfs-scrub@-.timer disabled" / "installed_unit 9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad  /usr/lib/systemd/system/btrfs-scrub@.timer" / "installed_unit eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252  /usr/lib/systemd/system/btrfs-scrub@.service" | `.ufo/waves/round-44/frozen/hostcap/capture.txt:3, 4, 5, 6, 7-8` |

Quoted-word counts (each ≤25): S242 15, S243 17, S244 13, S245 15.

Decision for all four, per their registry cells: admit, `mined`, tier A (`corpus/SOURCES.md:251-254`: kind `code` for
S242-S244, `own-work` for S245; status `mined`; opened `2026-10-26`; recheck `on-release`, S245 `30d`; used-by
`corpus/knowledge/btrfs-scrub-record-r44.md`).

Proposed follow-on paragraph:

Snapshot digests: `.ufo/waves/round-44/frozen/src/SHA256SUMS` (scrub.c `f347931b…938ca5b8`, sysfs.c `ce146120…44f731c43`,
timer `9a0b6cc2…9d6f8ad`, service `eaa7af92…fb240252`, PKGBUILD `3b803e8b…6c10ce98`), fetch log `FETCH.txt`; capture.txt
`efb52388…e3e84900`, capture.sh `6a297e4f…8376f6d`. Wave-1 seat SrcGateNew's live re-fetches at 2026-10-27T00:20:26Z were
byte-identical, and the git.kernel.org `plain ?h=v7.2.11` bytes match `raw.githubusercontent.com/gregkh/linux/v7.2.11`
(`cmp -s`, silent).

Registry changes (old → new): S242, S243, S244 and S245 absent at base `98020ce` → `mined`; no other row's status,
anchor, recheck or used-by changed (see F-2 seat for the S237/S240 used-by edits).

# Row checks asked for by the item

| row | 11 cells (awk `NF==13`) | anchor names pinned tag / commit / digest |
|---|---|---|
| S242 (`corpus/SOURCES.md:251`) | yes, 11 | tag v7.2.11 + peeled `a2de78ee…c3cb6ea` + raw sha256 `f347931b…938ca5b8` — matches live tag and live bytes. **Line list misses `3079-3085` (finding F1)** |
| S243 (`:252`) | yes, 11 | tag v7.2.11 + peeled `a2de78ee…c3cb6ea` + raw sha256 `ce146120…44f731c43` — matches. Ranges `72-74, 2021-2049, 2113` cover every lesson quote (`:72, 74, 2028, 2040, 2042, 2044, 2048, 2113`) |
| S244 (`:253`) | yes, 11 | tag 7.1-1 + commit `0c0a4d77…5b4d6e3e0` (live GitLab API) + timer/service sha256 (both match live bytes). **PKGBUILD carries no digest though `:99-101` is named (finding F2)** |
| S245 (`:254`) | yes, 11 | own-work: `sha256 efb52388…e3e84900` (capture.txt), `captured 2026-10-26T23:53:22Z`, `uid 1000` — all match `capture.txt:1`. **capture.sh's own digest is not named (finding F3)** |

The 11-cell shape is load-bearing, not cosmetic: the C2 counter accepts a row only when the line splits into exactly 11
cells (`tools/check-scrub-record-r44.py:171-173`, `if len(cells) == 11`), and its `sources_ok` term requires for each
row `kind`, `status == 'mined'`, `opened == '2026-10-26'` (`:104`), used-by containing the entry, and for S242/S243/S244
the tag string in the anchor cell (`:330-341`). `corpus/SOURCES.md` is byte-identical at `7e081698` and at the lane tip
`ff2c264a` (`git diff --stat` empty for both `corpus/SOURCES.md` and `corpus/knowledge/btrfs-scrub-record-r44.md`).

Counter cross-check at the pinned revision (`python3 tools/check-scrub-record-r44.py --revision 7e081698…`, 0.097 s):
`{"verdict": "FAIL", "rows": 3, "quotes_ok": 3, "props_ok": 3, "host_ok": 3, "sources_ok": 1, "verdicts_ok": 0,
"novelty_base_hits": 0, "pointer_ok": 1}` — every predicate term green except `verdicts_ok`, which is wave 2's binding
job, so this is the expected wave-1 state. Its `sources` block reads `S237 true, S240 true, S242 true, S243 true,
S244 true, S245 true, source_line true` (receipt `c2-7e081698.json`).

# Findings

**F1 — defect (non-blocking predicate): the S242 anchor omits the line that carries SR7's pre-wave narrowing.**
The row's anchor cell names `fs/btrfs/scrub.c lines 1365-1385, 3140-3162, 3215-3226, 3321-3337`
(`corpus/SOURCES.md:251`), but `corpus/knowledge/btrfs-scrub-record-r44.md:30` quotes `S242 scrub.c:3081:
"bool readonly, bool is_dev_replace)"`, and `:3081` is in none of those ranges (the function opens at `:3079`).
The counter reports the same gap from its own table: `per_row.SR7.quotes` = `{"good": 11, "in_window": 10, "bad": 0}`
(the SR7 windows are `(S242, scrub.c, 3140-3165)`, `(3215-3226)`, `(3321-3337)` and `(S240, ioctl.c, 3126-3145)`,
`tools/check-scrub-record-r44.py:88-89`). SR8/SR9 are `9/9` and `13/13` in-window. This does not fail any declared
predicate term (`in_window >= 1` is all `q_ok` requires, `:296-307`), but the round's own declaration says SR7 was
narrowed at `7e081698` because `btrfs_scrub_dev` also serves device replace, and neither the registry anchor nor the
counter's window names the bytes that justify it. Proposed minimal edits:
- anchor cell: `…lines 1365-1385, 3079-3085, 3140-3162, 3215-3226, 3321-3337; raw bytes sha256 f347931b…938ca5b8`
- SR7 windows: add `(('S242', 'scrub.c'), 3079, 3085)` before `(3140, 3165)` — the counter is frozen at
  `1409a5fd…9536388`, so this is an L1 decision, not a wave-1 edit; the alternative is that wave-2 reviewers of SR7
  see `in_window 10/11` and must know it is the signature quote deliberately.

**F2 — nit: S244's anchor pins the two units but not the PKGBUILD it also quotes.** The row names `PKGBUILD lines
99-101` (`corpus/SOURCES.md:253`) and the lesson quotes `PKGBUILD:100-101`; `SHA256SUMS` and my fetch both give
`3b803e8b05d84900fcdab3513720c8005345acd1fe34ded6eaa3b7596c10ce98` for those 3057 bytes, but the anchor cell carries
no PKGBUILD digest, so the install lines are the only cited bytes not pinned. Proposed: append `, PKGBUILD lines 99-101
(sha256 3b803e8b05d84900fcdab3513720c8005345acd1fe34ded6eaa3b7596c10ce98)`.

**F3 — nit: S245's anchor names one sha256 for a two-file own-work pair.** `capture.sh and capture.txt (sha256
efb52388…e3e84900)` (`corpus/SOURCES.md:254`) names the `capture.txt` digest only; `capture.sh` hashes
`6a297e4ff9c7030c6cfe10feeb6c9198ccf31a574fbe6ce1b755dbf318376f6d`. Round-43's S241 row has the same shape
(`capture.sh and capture.txt (sha256 f7ecbe7c…)`), so this is a pattern defect in the own-work convention, not a
round-44 regression. Proposed: name both digests, as in the draft row's URL cell.

**Note on the access date (not a defect).** My re-open crossed midnight UTC: local `2026-10-26T21:20:26-0300` =
`2026-10-27T00:20:26Z`. The draft table records the UTC date; the registry `opened` cells must stay `2026-10-26`
(counter constant `tools/check-scrub-record-r44.py:104`), and the frozen, the S244 tag commit date (`2026-07-15`) and
the S245 capture timestamp (`2026-10-26T23:53:22Z`) are unaffected.

# Gates I ran (and did not run)

- Fetched-5 / hashed-5: all five frozen files reproduced byte-for-byte; two kernel files also matched the independent
  GitHub mirror.
- Tag pinnings: 2 of 2 (`v7.2.11` peel, Arch `7.1-1` commit).
- Located quotes: 23 of 23 byte-exact at the cited line (`quote-verify.txt`, `mismatches 0`).
- Row shape: 4 of 4 rows = 11 cells; identical at `7e081698` and `ff2c264a`.
- C2 counter at `7e081698`: run, `FAIL` on `verdicts_ok` only (wave-2 binding not yet present), 0.097 s.
- Not run, by design: the census selftest and the C1 counter (~25 s / ~30 s, other seats' items), any wave-2 verdict
  check, `sources-census.sh validate` (F-2's item), and no host query beyond reads of the frozen capture.

# Touched surfaces

Wrote only: `.ufo/waves/round-44/w1/SrcGateNew.md` (this report) and `.ufo/waves/round-44/w1/SrcGateNew/`
(`live-reopen.txt`, `quote-verify.txt`, `cells-7e081698.txt`, `c2-7e081698.json`, `tag-7.1-1.json`, `fetched/` with
the five fetched files plus its own `SHA256SUMS`, and `qcheck.py`, which now reads `fetched/`). `quote-verify.txt` is
the output of `python3 <seat dir>/qcheck.py` run against the receipt copies after the scratch copy was made —
`23` `OK` lines and `mismatches 0` — so the quote check is replayable from the receipt alone. No tracked lane file, no
`corpus/` file, no fleet-root file, nothing in a PATH directory, no git/jj state
(`git status --porcelain -- corpus tools SCORECARD.md LOG.md MANIFEST.json .ufo/waves/round-44/w1/SrcGateNew.md` prints
only `?? .ufo/waves/round-44/w1/SrcGateNew.md`). No package, service, unit, timer, sysfs, mount or scrub operation;
`/var/lib/btrfs`, `/sys/fs/btrfs` and systemd were not touched by me at all (S245's evidence is the frozen capture).
Scratch `/fast/scratch/hyaku/tsukuroi-r44/SrcGateNew/` was removed after the receipts were copied.

# Out of scope / owed

- Applying F1-F3 (anchor cells are registry rows; the SR7 window list is inside the frozen counter) belongs to the L1.
- The lesson body itself (`corpus/lessons/round-44.md`) is ScribeLesson's draft; I supply only these rows.
- `transcripts_bound` and all wave-2 binding terms stay owed to wave 2.
