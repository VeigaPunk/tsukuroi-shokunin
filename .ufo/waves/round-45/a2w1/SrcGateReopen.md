VERDICT: supports

# SrcGateReopen — F-2: re-open S237/S242/S243/S244, `used-by` old→new Gate lines, freshness LOG line

Seat: SrcGateReopen (scribe, axes sources + freshness). Lane `tsukuroi-shokunin`, wave `a2w1`. Read-only on lane
content: nothing tracked was written; the only new files are this report and
`.ufo/waves/round-45/a2w1/SrcGateReopen/` (receipts). Scratch `/fast/scratch/hyaku/tsukuroi-r45/SrcGateReopen`
(removed at the end of the seat; every artifact cited below was copied into the receipt dir first).

**Result in one line:** all four rows re-open byte-identical on 2026-10-27 to their frozen snapshots and to their
`SHA256SUMS` (`cmp` 6/6, six live files), the three tag pins still peel to the commits their rows and `FETCH.txt`
record, the `base → impl` diff changes **only column 11 (`used-by`) on those four rows** and nothing else, and the
sources census `validate` exits 0 with 40 W04 — the same 40 warnings and the same set as at base.

Item scope check: the item's own words are "re-open … now, re-hash against their SHA256SUMS, and draft the lesson
Gate lines logging their `used-by` change old->new … only column 11 may change for those rows", plus "draft that one
LOG line" and "run `sources-census.sh validate …` and report exit and warning count". All five are done; the two
drafts are in §4 and §5, exact Markdown.

## 1. Re-open: live fetches, 2026-10-27T03:30:51Z (UTC)

Six files, not four: S244's row anchors three files (`btrfs-scrub@.timer`, `btrfs-scrub@.service`, `PKGBUILD`), and
S237's row is the tag-pinned btrfs-progs v7.1 `cmds/scrub.c`. URLs are the raw forms (`plain/…?h=v7.2.11`,
`raw.githubusercontent.com`, gitlab `-/raw/7.1-1/…`), which are the forms that produce the bytes the rows hash;
the rows themselves record the human-facing `tree`/`blob` URLs (see §6, finding S-1).

```
curl -sSfL --max-time 60 -o f/S237-scrub-progs.c https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c
curl -sSfL --max-time 60 -o f/S242-scrub-kernel.c 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/scrub.c?h=v7.2.11'
curl -sSfL --max-time 60 -o f/S243-sysfs.c        'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/sysfs.c?h=v7.2.11'
curl -sSfL --max-time 60 -o f/S244-btrfs-scrub@.timer   https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/7.1-1/btrfs-scrub@.timer
curl -sSfL --max-time 60 -o f/S244-btrfs-scrub@.service https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/7.1-1/btrfs-scrub@.service
curl -sSfL --max-time 60 -o f/S244-PKGBUILD             https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/7.1-1/PKGBUILD
```

Every curl exited 0 (each `rc=0` echoed; log in the receipt `commands.txt`, stamp `fetch-stamp.txt` =
`2026-10-27T03:30:51Z`). Sizes 57034 / 100417 / 72925 / 160 / 190 / 3057 bytes.

The four row URLs as written (blob/tree forms) also answer 200 today — `curl -sS -o /dev/null -w '%{http_code}' -L`:
`200` `github.com/kdave/btrfs-progs/blob/v7.1/cmds/scrub.c`; `200` `…kernel…/tree/fs/btrfs/scrub.c?h=v7.2.11`;
`200` `…kernel…/tree/fs/btrfs/sysfs.c?h=v7.2.11`; `200` `gitlab.archlinux.org/…/btrfs-progs/-/tree/7.1-1`.

## 2. Re-hash against SHA256SUMS, and byte-compare with the frozen copies

`sha256sum f/*` (receipt `sha256-live.txt`):

| file | live sha256 (2026-10-27) | `SHA256SUMS` it is checked against | bytes | verdict |
|---|---|---|---|---|
| S237 `cmds/scrub.c` | `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` | `.ufo/waves/round-42/frozen/src/SHA256SUMS` | 57034 | MATCH |
| S242 `fs/btrfs/scrub.c` | `f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8` | `.ufo/waves/round-44/frozen/src/SHA256SUMS` | 100417 | MATCH |
| S243 `fs/btrfs/sysfs.c` | `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43` | same | 72925 | MATCH |
| S244 `btrfs-scrub@.timer` | `9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad` | same | 160 | MATCH |
| S244 `btrfs-scrub@.service` | `eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252` | same | 190 | MATCH |
| S244 `PKGBUILD` | `3b803e8b05d84900fcdab3513720c8005345acd1fe34ded6eaa3b7596c10ce98` | same | 3057 | MATCH |

Independent of the sums, `cmp -s` live-vs-frozen printed `IDENTICAL` for all six (`commands.txt`; frozen paths
`.ufo/waves/round-42/frozen/src/scrub.c` and `.ufo/waves/round-44/frozen/src/{scrub.c,sysfs.c,btrfs-scrub@.timer,btrfs-scrub@.service,PKGBUILD}`).
Each digest also equals the digest the row itself carries in its `anchor` cell — S237 `48df2e2f…0801`
(`corpus/SOURCES.md:246`), S242 `f347931b…a5b8` (`:251`), S243 `ce146120…1c43` (`:252`), S244 `9a0b6cc2…` /
`eaa7af92…` (`:253`). `PKGBUILD`'s hash is carried only by `SHA256SUMS`, not by the row; the row instead fixes
`PKGBUILD lines 99-101`, and that anchor still reads exactly as quoted — `sed -n '100p'` on the live-fetched
`PKGBUILD` (and on the frozen copy) prints
`  install -Dm644 btrfs-scrub@.service "${pkgdir}/usr/lib/systemd/system/btrfs-scrub@.service"`.

## 3. Tag pins still peel to the recorded commits

```
git ls-remote https://github.com/kdave/btrfs-progs refs/tags/v7.1 'refs/tags/v7.1^{}'
0a919c7d6e389c07920675b7fad3f793b92aa78b	refs/tags/v7.1
4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b	refs/tags/v7.1^{}
git ls-remote https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git refs/tags/v7.2.11 'refs/tags/v7.2.11^{}'
8316c24ec1b77dba19ba072ca4fe251b36dc65d3	refs/tags/v7.2.11
a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea	refs/tags/v7.2.11^{}
git ls-remote https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs.git refs/tags/7.1-1 'refs/tags/7.1-1^{}'
4fd401153bd8eac8ab9e37e6511e1bf2350fdd07	refs/tags/7.1-1
0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0	refs/tags/7.1-1^{}
```

Peeled commits match the rows' pinned commits (S237 `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b` at
`corpus/SOURCES.md:246`; S242/S243 `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea` at `:251`/`:252`; S244
`0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0` at `:253`) and match `.ufo/waves/round-42/frozen/src/FETCH.txt` and
`.ufo/waves/round-45/frozen/src/FETCH.txt` (the latter repeats the same two `v7.2.11` lines). Nothing moved.

## 4. Draft — lesson `corpus/lessons/round-45.md`, `## Gate` insertion (exact Markdown)

```markdown
### Re-opened rows and rows touched old→new (opened 2026-10-27 by wave-`a2w1` seat SrcGateReopen; column 11 only)

| Row | used-by old → new | Log |
|---|---|---|
| S237 | `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md` → `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md` | `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff 5bbd5ff588120fd8e7c744695351a6978b4241c1 18389f44cf6ce414d7be205998b29c79fb0b490c -- corpus/SOURCES.md`; column 11 only; re-fetched 2026-10-27 byte-identical (`48df2e2f…0801`) |
| S242 | `corpus/knowledge/btrfs-scrub-record-r44.md` → `corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md` | same; column 11 only; re-fetched 2026-10-27 byte-identical (`f347931b…a5b8`) |
| S243 | `corpus/knowledge/btrfs-scrub-record-r44.md` → `corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md` | same; column 11 only; re-fetched 2026-10-27 byte-identical (`ce146120…1c43`) |
| S244 | `corpus/knowledge/btrfs-scrub-record-r44.md` → `corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md` | same; column 11 only; re-fetched 2026-10-27 byte-identical, three files (`9a0b6cc2…f8ad`, `eaa7af92…0252`, `3b803e8b…ce98`) |

Snapshot digests re-checked live 2026-10-27 against `.ufo/waves/round-42/frozen/src/SHA256SUMS` (S237) and
`.ufo/waves/round-44/frozen/src/SHA256SUMS` (S242-S244): `sha256sum` 6/6 match and `cmp` live-vs-frozen 6/6
identical. Tag pins re-resolved the same day: `refs/tags/v7.1^{}` `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b`,
`refs/tags/v7.2.11^{}` `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`, `refs/tags/7.1-1^{}`
`0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0` — unchanged from `FETCH.txt`. Receipts:
`.ufo/waves/round-45/a2w1/SrcGateReopen/` (`sha256-live.txt`, `tags.txt`, `col-diff.json`, `commands.txt`).

Census (frozen command): `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` exit 0,
`ok`, 40 W04, 249 rows (`grep -c '^| S[0-9]' corpus/SOURCES.md`) against 245 rows and the same 40 W04 at base
`.ufo/waves/round-45/before/sources-census-start.txt`; the warning sets are `diff`-empty.
```

## 5. Draft — the round's freshness re-verification line for `LOG.md` (routed defect D10, one line)

Draft (one physical line; wrap it freely, the bytes are the sentence, not the newlines):

```markdown
**Freshness (D10).** Re-verification of predecessor pins, 2026-10-27: S237 (btrfs-progs v7.1 `cmds/scrub.c`), S242 (`fs/btrfs/scrub.c` at v7.2.11), S243 (`fs/btrfs/sysfs.c` at v7.2.11) and S244 (`btrfs-scrub@.timer`, `btrfs-scrub@.service`, `PKGBUILD` at packaging 7.1-1) re-fetched byte-identical (`cmp` 6/6 against the round-42/round-44 frozen copies; `48df2e2f…0801`, `f347931b…a5b8`, `ce146120…1c43`, `9a0b6cc2…f8ad`/`eaa7af92…0252`/`3b803e8b…ce98`), the tags still peel to `4ab0e80b…ba8b`, `a2de78ee…bea6` and `0c0a4d77…3e0e`, and the sources census re-ran `validate` at exit 0, `ok`, 40 W04 unchanged (249 rows against 245 at base).
```

Notes for the L1/LogDraft seat, so the line does not collide with its neighbours: it names only the four rows this
seat re-opened. S246-S249 are *opened* this round (not re-verifications) and their live re-fetch belongs to
C2ExecLiveSources; S245 and the S249 host capture re-run belong to C2ExecHostRecheck. Register follows `LOG.md:1606`
(`Re-verification of predecessor pins: …`).

## 6. Findings

- **S-1 (observation, no action needed for the predicates): S237's row records the GitHub *blob* URL, not the raw
  URL that yields the hashed bytes.** `corpus/SOURCES.md:246` gives
  `https://github.com/kdave/btrfs-progs/blob/v7.1/cmds/scrub.c`; the raw form is named only in
  `.ufo/waves/round-42/frozen/src/FETCH.txt` (`scrub.c <- https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c`).
  Both answer 200 and the raw form reproduces `48df2e2f…0801`, so the row's `anchor` ("raw bytes sha256") is
  falsifiable and holds. If sources hygiene wants the hashing URL inline, that would be a column 6 edit — **not**
  made here, and out of this seat's column-11-only mandate.
- **S-2: the `base → impl` diff changes exactly one cell on each of the four rows, and it is `used-by`.** Cell-level
  comparison of all 11 cells per row, base `5bbd5ff5…` vs impl `18389f44…`: S237/S242/S243/S244 each report
  `"changed": 1`, `"columns": ["used-by"]` (`SrcGateReopen/col-diff.json`, sha256
  `695afbb7af9c54a552e66140a1bca536a6f554ea591dc6db3994f54a34795530`). `source`, `kind`, `tier`, `scope`, `anchor`,
  `teaches`, `status` (`mined`), `opened` (`2026-10-26`) and `recheck` (`on-release`) are byte-identical to base, so
  the "only column 11 may change" condition holds literally — including `opened`/`recheck`, which a careless
  re-open would be tempted to bump.
- **S-3: the census draws no new warning from the four new rows.** 40 W04 at base and 40 W04 now; warning ids in
  both sets run `S038`…`S230` and none is `S246`-`S249` (`diff` of the two 40-line warning blocks is empty;
  `SrcGateReopen/census-validate.txt` vs `.ufo/waves/round-45/before/sources-census-start.txt`). Row count moved
  245 → 249, i.e. exactly the four S246-S249 rows the round adds; no row was dropped or renumbered.
- **S-4 (limit, not a defect): tag immutability is observed, not guaranteed.** The three tags are moving targets in
  principle; what is recorded here is that their peeled commits equal the pinned ones at 2026-10-27T03:30Z and that
  the raw content at those tags matches the stored digests. A later tag move would be detected by this same check,
  which is why the `recheck` column stays `on-release` and is left untouched.

## 7. Gates and axes

- **sources:** all four rows re-open at their pinned versions; six live digests match `SHA256SUMS` and the rows'
  own `anchor` hashes; every row URL answers 200. Nothing to correct on the four rows but column 11.
- **freshness:** signal is the LOG line in §5 (this is the D10 repair). Census `validate` exit **0**, status `ok`,
  **40 warnings**, all `W04 duplicate url … across scopes`, unchanged in count and set from base.
- **operability / calibration / adjacency / depth:** untouched by this seat — no counter was run (the C1 counter is
  another seat's; the C2 counter is ~2 s but neither is in F-2's scope), and no lane file was edited, so nothing
  here can move those axes.

## 8. Touched surfaces

- Wrote: `tsukuroi-shokunin/.ufo/waves/round-45/a2w1/SrcGateReopen.md` (this report) and receipts under
  `tsukuroi-shokunin/.ufo/waves/round-45/a2w1/SrcGateReopen/` (6 fetched files, `sha256-live.txt`, `tags.txt`,
  `col-diff.json`, `commands.txt`, `census-validate.txt`, `fetch-stamp.txt`; 268 KB total).
- Wrote nothing else: no tracked lane file, no `SOURCES.md`, no `LOG.md`, no lesson, no fleet-root file, no
  `~/.local/bin`, no PATH entry, no shim; no git/jj mutation, no package or service action, no sudo, no host write.
  Lane `git status --porcelain` shows only `??` under `.ufo/waves/round-45/` (`a2w1*`, seat dirs).
- Scratch `/fast/scratch/hyaku/tsukuroi-r45/SrcGateReopen` removed after the receipts were copied.

## 9. Out of scope (deliberately not done)

- Drafting rows for S246-S249 (F-1, seat SrcGateNew) and the reject rows for D8.
- The full `LOG.md` round-45 entry (X-8, seat LogDraft) — §5 is only the freshness line that entry must contain.
- Any `SOURCES.md` edit: the `used-by` cells already carry `btrfs-scrub-grounding-r45.md` at `18389f44…`, which is
  the state these Gate lines document; the lane is read-only for this seat.
- The C1/C2 counters, the adjacency gate and the census selftest: not part of F-2.
