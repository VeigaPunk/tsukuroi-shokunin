# ScoutUpstream — round 92 w1, scoped findings (freshness axis)

Seat: ScoutUpstream (scout, leaf, read-only on the lane). Lane revision read at seat start:
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` → **429fd1a34dfcdf951bf4aaedb2df4bc45835bede**
(freeze commit `da99b2f4bc442e5154a6c1da7350891c11ee7cb1` present as its ancestor). No commit, no git/jj
mutation, no host mutation, no install. Scratch `/fast/scratch/hyaku/tsukuroi-r92/ScoutUpstream/` created,
used, and **removed on exit**.

Full evidence table: `.ufo/waves/round-92/w1/ScoutUpstream/ScoutUpstream.md` (24 KB).
Raw receipts: `.ufo/waves/round-92/w1/ScoutUpstream/{host-facts.txt, upstream-tags-and-changelog.txt,
pin-verification.txt, path-lines-characterised.txt, gate-era-and-pin-drift.txt}`.

## 1. Read-only host facts (exact outputs)

| command | output |
|---|---|
| `pacman -Q limine` | `limine 12.9.4-1` |
| `limine --version` | `Limine 12.9.4` |
| `pacman -Si limine` | `Repository : extra`, `Version : 12.9.4-1`, `Build Date : Tue 20 Oct 2026 04:34:10 AM -03` — **stale local sync DB** (`/var/lib/pacman/sync/extra.db` dated Oct 22 2026) |
| `ls /sys/class/tpm` | `total 0` (empty; `ls -A … \| wc -l` → `0`; no `/dev/tpm*`) — **no TPM** |
| `cat /boot/limine.conf \| head -5` | `head: cannot open '/boot/limine.conf' for reading: Permission denied` (`/boot` is `drwx------ root root`) — the live config is **not observable** by this seat |
| `od -An -tx1 /sys/firmware/efi/efivars/SecureBoot-8be4df61-…` | `06 00 00 00 00` — Secure Boot **off** |
| `python3 -VV` / `bwrap --version` | `Python 3.14.8 … [GCC 16.2.1 20260810]` / `bubblewrap 0.13.1` — the C1 launcher's dependencies are present |
| `sha256sum /usr/share/doc/limine/CONFIG.md` | `c9e8b670d20d839add4f651f8c49e9565302b132f9f86269acbc7cd1e0358923` — **byte-identical to upstream v12.9.4's `CONFIG.md`**; upstream v12.9.6's is `f44f3a19…`, differing in exactly the global-options paragraph (`*Global options* must come before the first *menu entry*.` vs `can appear anywhere in the file`) |

The two `path:` lines the r91 receipt characterised: `grep -rn '^path:' .ufo/waves/round-91/` returns **exactly two**
matches, both in `w1/ScoutDrift/harness-output.txt` — lines **26** and **61**, both `path: boot():/x#abc`, the fixture
pin of ScoutDrift's case *"B: global panic AFTER first entry, first line is entry"* (line 26 = the v12.9.4-vs-v12.9.6
harness, line 61 = the v12.9.4-vs-v12.9.5 harness), where 12.9.4 keeps the pin **and** the trailing global key visible
and 12.9.5/12.9.6 truncate the buffer at the entry label so both vanish. (The r91 **host** receipt separately
characterises six host `path:` lines at 30/38/50/56/64/72 — 72 being the only unhashed image line, 30 and 38 the two
`LP-MISMATCH` pins. Verbatim capture in `path-lines-characterised.txt`.) The committed r17 capture shows the host
config's first `/`-entry is at line 21 with `default_entry: 2` at line 3, i.e. a non-empty global section — but that is
a **2026-10-20** capture of a file this seat cannot read, so it is `[INFERENCE]`, not a current fact.

## 2. Upstream: tags, dates, ChangeLog, and 12.9.7+

* Tags: `v12.9.4` → `1e512b2b7184` (peeled `8ad14430bc9f`, commit date 2026-10-19T15:31:20Z), `v12.9.5` →
  `c427781c6624` (peeled `55a93085435a`, 2026-10-27T16:28:54Z), `v12.9.6` → `54727fd1c0d5` (peeled `89a9512c623a`,
  2026-10-27T23:11:11Z). **No tag after v12.9.6**; no rc/beta in 12.9.x.
* Releases API (`per_page=10`): newest is **`v12.9.6 | 2026-10-27T23:16:30Z`**. **12.9.7 does not exist.**
* `git ls-remote … HEAD` → `89a9512c623a…` == `v12.9.6^{}` == `refs/heads/v12.x`: upstream HEAD *is* the v12.9.6 tag
  commit, so there is no unreleased drift in the released line.
* ChangeLog lines in the 12.9.4→12.9.6 delta bearing on config parsing / global options — exactly **two**:
  * 12.9.5: *"Parse the config in linear time. Configs with thousands of entries were slow to load."*
  * 12.9.6: *"Document that global options must come before the first entry, as has been the case since 4.0. A config
    whose first line is an entry has had no global options since 12.9.5, whereas every option in it used to count as
    global. Fixes #700."*
  The whole 12.9.5→12.9.6 delta adds **82** lines and changes no parsing behaviour. Upstream corroborates:
  issue **#700** ("Global options after the first entry are ignored, unless the file starts with an entry", opened
  2026-10-27T18:52:23Z, closed 2026-10-27T22:43:43Z by Mintsuki) and PR **#702** (`docs: clarify positioning of
  global options`, merged 2026-10-27T22:41:28Z, 1 file changed — documentation only).
* `commits?path=common/lib/config.c&since=2026-10-28` → **count 0**: nothing touches `config.c` after 12.9.6.
* The only post-12.9.6 upstream tree is **`trunk`** (`31e8865c9545`): its `config.c` is `e87a30d5fde4…` vs the pinned
  `a940acae3a0a…`, and the diff is **hash/checksum only** (`<crypt/blake2b.h>` → `<crypt/hash.h>`,
  `CONFIG_B2SUM_EMPTY` re-wrapped, `init_config`'s checksum block moved to `hash_reference_from_enrolled()`).
  The **visibility cut is untouched**: `if (p > config_addr) { *(p - 1) = '\0'; }` at trunk raw **332-334**
  (v12.9.6: 328-330) and the label-end NUL at trunk raw **366** (v12.9.6: 362-365).

## 3. Pin verification against refetched raw URLs

`sha256sum -c .ufo/waves/round-92/before/src/SHA256SUMS` → **8/8 OK**. Re-fetching each URL in `URLS.txt` today:
`config.c` v12.9.4 `aafc9c41…` ✔, v12.9.5 `a940acae…` ✔, v12.9.6 `a940acae…` ✔ (the two are byte-identical —
the mechanical fact behind "one rule for >= 12.9.5"), `ChangeLog` v12.9.5 `d2e08cc4…` ✔, v12.9.6 `ab280b45…` ✔,
`issue-700.json` `7c7ac6e0…` ✔, `bubblewrap-bwrap.xml` `2cb77df2…` ✔ — **7 of 8 reproduce byte-exactly**.
The exception is **`python-3-cmdline.txt`**: the pinned `558f4c7d…` is a 46 065-byte **text rendering** (0 `<`
characters) of the page, while a plain `curl` of the URL returns 171 073 bytes of **HTML** (`2371db30…`). Its
*content* is current (word-stream similarity 0.99887 vs today's page, same `Last updated on Nov 08, 2026 (00:12 UTC)`,
same 3.15.2 title; the `-I`/`-P`/`-E`/`-s` semantics the gate relies on are verbatim identical), but the pin is a
**citation, not a digest of upstream** — it must never be re-verified by re-fetch.
`python3 tools/check-limine-pins.py … --limine-version <v>` (live, read-only): accepted with `rc 0`
(`pre-12.9.5` for 12.9.4; `12.9.5+` for 12.9.5, 12.9.6, **12.9.7**, **13.0.0**, **99.0.0**); refused with `rc 64`
and **no verdict** for `12.9`, `12.9.x`, `""`, `abc`, `12.9.4.1`.
`sha256sum -c .ufo/waves/round-92/before/freeze-manifest.sha256` → **36/36 OK** (the manifest has 36 lines, not 30
as the brief states; zero failures).

## 4. The freshness boundary the claim should carry

**First upstream release that would invalidate the V2 rule: the first release after v12.9.6 that changes the
global-section visibility cut in `common/lib/config.c`** — i.e. the first release whose `create_menu_tree()` does not
keep both `if (p > config_addr) { *(p - 1) = '\0'; }` and the label-end NUL `if (*p == '\n') { *p = '\0'; p++; }`.
No such release exists today (no 12.9.7; zero post-2026-10-28 `config.c` commits; `trunk`'s cut intact at raw
332-334/366; 12.9.5 and 12.9.6 `config.c` byte-identical). The V2 rule is therefore correct for every upstream
release that exists as of 2026-11-08 — and for `trunk`.
**Weaker but real:** any release that edits `config.c` at all moves the cited raw line numbers (`trunk` already shows
the cut at 332-334, not 328-330), so the *citations* go stale before the *rule* does.

**Host-side trigger that must re-run the battery: a pacman update of the `limine` package taking the host from
`12.9.4-1` to `12.9.6-1`.** Arch `extra` already ships `12.9.6 - 1` (`last_update 2026-10-28T08:00:46Z`), so the
next `pacman -Syu` flips the running Limine into the 12.9.5+ era while the gate's default stays `12.9.4`.
Detection notes: `pacman -Si limine` **cannot** be the trigger (stale local `extra.db`, still says `12.9.4-1`); the
authoritative check is `https://archlinux.org/packages/extra/x86_64/limine/json/`; and the cheapest **root-free**
detector is `sha256sum /usr/share/doc/limine/CONFIG.md` (`c9e8b670…` = 12.9.4 era → `f44f3a19…` = 12.9.6 era).
When it fires, three things must be re-pinned: the gate's `--limine-version` **default** (`12.9.4` → `12.9.6`);
the battery's `ERA-DEFAULT` family (written against the 12.9.4 default, "Kills a gate whose default is the new era");
and the raw-line citations in the gate/battery docstrings. Neither instrument auto-detects the host version —
`grep 'subprocess|pacman|limine --version'` over `tools/check-limine-pins.py` and `tools/limine-pin-battery-r92.py`
finds **no** such call — so the era is operator-declared and nothing would notice the upgrade by itself.

## 5. Limits of this seat

Read-only reconnaissance only: no lane file outside this seat's receipt directory was written; no git/jj mutation;
no host mutation and no `sudo`; no install (all tools already present — `git`, `curl`, `python3` 3.14.8, `pacman`,
`bwrap` 0.13.1, `sha256sum`, `diff`; `python3 -m pip` is absent, so the optional `html2text` cross-check of the
python-doc pin was done with an in-process regex extractor instead — a missed convenience, no conclusion changed);
no subagent dispatched; scratch removed on exit.
Unresolved: the live `/boot/limine.conf` (permission denied) — hence the host's first physical line and the current
status of its six `path:` lines remain `[INFERENCE]` from committed receipts; and whether upstream's next release
will change the cut, which is the deliberate open end of the freshness clause.

## Verdict

**C2 (depth) — supported.** The version-selected visibility rule's freshness boundary is real, dated, and nowhere
past v12.9.6: upstream HEAD *is* the v12.9.6 tag commit (no 12.9.7 exists), zero commits touch
`common/lib/config.c` after 2026-10-28, `trunk`'s post-12.9.6 delta is hash-only and leaves the cut intact at raw
332-334/366, the 12.9.5/12.9.6 `config.c` pins are byte-identical (`a940acae…`) so ">= 12.9.5 ⇒ one rule" is measured
rather than assumed, the gate's rc-64 format refusal is confirmed live (`12.9`, `12.9.x`, `""`, `abc`, `12.9.4.1` →
rc 64, no verdict), and the freeze manifest verifies 36/36 with the frozen gate/battery/control bytes. The boundary
the claim must carry is **"the first upstream release after v12.9.6 that changes the visibility cut"**, with the
**host-side trigger being the pacman upgrade to `limine 12.9.6-1`**, detectable root-free via
`/usr/share/doc/limine/CONFIG.md`'s digest (`c9e8b670…` → `f44f3a19…`).
**C1 (operability) — not falsified and only partially covered here.** The host facts asked for are recorded
(`limine 12.9.4-1`, `Limine 12.9.4`, no TPM, Secure Boot off, `bwrap 0.13.1`, `python3 3.14.8`); C1's isolation
counts are not this seat's axis and are not asserted.
Receipts: `.ufo/waves/round-92/w1/ScoutUpstream/{ScoutUpstream.md, host-facts.txt, upstream-tags-and-changelog.txt,
pin-verification.txt, path-lines-characterised.txt, gate-era-and-pin-drift.txt}`.
