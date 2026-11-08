# ScoutSource — round-94 w1 — source pins, S385 re-open, rejected leads

Seat: SCOUT (leaf; no subagents dispatched). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
@ `b6447374637394b1f41183d1581f52127518fcdc` (freeze `eb3b3e5150a63507a382003fa1a70039b190396b`).
Axis: **freshness**. Date: 2026-11-08. Scratch: `/fast/scratch/hyaku/tsukuroi-r94/ScoutSource/`
(created before the first command, removed on exit). No lane file was edited except this seat's
own receipts dir `.ufo/waves/round-94/w1/ScoutSource/` and this report. No git/jj mutation was run
in the lane (`git log`/`show`/`status`/`rev-parse`/`ls-remote` only). No tool was installed or
upgraded (nothing needed one) — **no installs, no updates, no channel**.

Receipts (all under `.ufo/waves/round-94/w1/ScoutSource/`):

| receipt | content |
|---|---|
| `pin-table.tsv` | URL, HTTP status, bytes, sha256, access time, local copy for every fetch |
| `quotes.md` | 15 located quotes, each ≤25 words, with raw line locations |
| `receipt-01-v1296-vs-v1295-bytes.txt` | the v12.9.6-vs-v12.9.5 byte comparison (sha256 + `diff` + master drift check) |
| `receipt-02-s385-reopen.txt` | the S385 re-open, the `/3.15/` vs `/3/` alias digest drift, sibling version lines |
| `receipt-03-rejected-leads.txt` | the two rejected leads with status/body bytes, plus host-version context |
| `pins/` | the fetched bytes themselves |

---

## 1. The three v12.9.6 pins — fetched, hashed, stored

| URL | HTTP | bytes | sha256 |
|---|---|---|---|
| `…/limine/v12.9.6/common/lib/config.c` | 200 | 23351 | `a940acae3a0a9c4d1c716f8132f688c4bcdced2b092769bc1becad466e944e60` |
| `…/limine/v12.9.6/ChangeLog` | 200 | 122099 | `ab280b451ee6f56bad5684d44eda5c94bf43d2c17e9e651b8e84b433584d03ba` |
| `…/limine/v12.9.6/host/limine.c` | 200 | 69050 | `4da21c7cceae238075612643b845cb63e06cc184977e950d5e6374329bc31ec0` |

Copies: `pins/limine-v12.9.6-{common_lib_config.c,ChangeLog,host_limine.c}`.
All three are **byte-identical to the lane's own r94 copies** in
`.ufo/waves/round-94/before/src/` (same three digests) — the frozen pins still reproduce from
upstream today.

### 1a. Comparison against the v12.9.5 pins — the answer is *identical*, for two of three

| file | v12.9.6 sha256 | r93 v12.9.5 pin sha256 | `diff` exit |
|---|---|---|---|
| `common/lib/config.c` | `a940acae…` | `a940acae…` (same) | **0 — identical** |
| `host/limine.c` | `4da21c7c…` | `4da21c7c…` (same) | **0 — identical** |
| `ChangeLog` | `ab280b45…` | `d2e08cc4…` (differs) | 1 — 19 added, 0 deleted lines |

So **the v12.9.6 `common/lib/config.c` and `host/limine.c` are byte-identical to the v12.9.5 pins**
(same sha256 *and* an empty `diff`), and only the ChangeLog moved — by a pure prepend of the
12.9.6 release block (19 added lines, zero deleted lines). The two era-rule files carry no code
change between the tags. Cross-checks in `receipt-01`:

- the r93 pins themselves re-fetch from upstream `v12.9.5` → byte-identical (the r93 pin is not
  a hand-made copy);
- upstream `master` `common/lib/config.c` and `host/limine.c` are byte-identical to `v12.9.6`
  (no unreleased drift);
- upstream `v12.9.4` `common/lib/config.c` (`aafc9c41…`, 24554 bytes) **does** differ from
  v12.9.6 — the cut the battery certifies was added in 12.9.5, as the lane claims.

Located quotes (full table in `quotes.md`):

- `config.c` raw **328-330**: `if (p > config_addr) { *(p - 1) = '\0'; }` — the cut, in
  `create_menu_tree()` (raw 298 → 407).
- `config.c` raw **362-365**: `if (*p == '\n') { *p = '\0'; p++; }` — the label-end NUL.
- `config.c` raw **666 / 668**: `config_ready = true;` / `menu_tree = create_menu_tree();`.
- `host/limine.c` raw **2035**: `puts("Limine " LIMINE_VERSION);` — the probe's input shape,
  on **stdout**.
- `host/limine.c` raw **2031**: `puts(LIMINE_VERSION);` — the bare version.
- `host/limine.c` raw **2089-2091**: `strcmp(argv[1], "version") == 0 || strcmp(argv[1], "--version") == 0) { return version(argc - 1, &argv[1]); }`.
- `ChangeLog` raw **3**: `*** Release 12.9.6 ***`; raw **14-15**:
  `A config whose first line is an entry has had no global options since 12.9.5.`; raw **16**:
  `used to count as global. Fixes #700.`

### 1b. Two source facts that bear on C2 (recorded, not adjudicated)

- **The probe's expected stdout shape is upstream's own.** `host/limine.c` raw 2035 prints
  `Limine <version>` on **stdout**; nothing upstream ever prints a version to stderr or with a
  suffix. So the AUTO-PROBE-SHAPES expectations (stderr-only and `12.9.6-rc1` must be refused)
  are faithful to what upstream can print, and the healthy `Limine 12.9.6` answer is the only
  shape upstream produces. Corroborates C2's probe semantics from source.
- **`--version-only` is a `version`-subcommand option, not a top-level flag.** Upstream's usage
  string (raw 2006-2008) is `usage: limine version [options...]`; the `--version-only` parse is
  inside `version()`'s own argument loop (raw 2022). On this host: `limine --version-only` → rc 1
  with the usage text; `limine version --version-only` → rc 0, prints `12.9.4`. **Locator
  precision note for the L1:** S388's cell reads "`--version-only` prints the bare LIMINE_VERSION"
  — true, but reachable only as `limine version --version-only`; the S388 row's raw-2031 anchor
  is correct.

## 2. S385 re-opened — the committed sha still reproduces; the alias digest moved

`https://docs.python.org/3.15/using/cmdline.html#cmdoption-P` → HTTP **200**, 171073 bytes,
sha256 **`d3c503060ebf18e5a807ba35d8527cfde49f8322373b9111e5c26d657b658cf6`** — **exactly the
sha256 committed in `corpus/SOURCES.md` line 396 (S385)**. **It does not differ.** The title
contains the required string:

`<title>1. Command line and environment — Python 3.15.2 documentation</title>`

(`grep -c 'Python 3.15.2'` → 2 occurrences.) Sibling version lines confirm the pin is
version-specific: `/3.14/` → `e2748546…` (`Python 3.14.10 documentation`), `/3.16/` → `ba8cbd2b…`
(`Python 3.16.0a1 documentation`).

**Freshness caveat the L1 should carry (new this round).** The *version string* is pinned, but the
*byte digest* is not: the Sphinx build stamp is embedded in the page, so the digest of a
content-identical page moves when upstream rebuilds. Evidence in `receipt-02`: the r93-stored copy
of the rolling `/3/` alias is `2371db30…` with the stamp `Last updated on Nov 08, 2026 (00:12 UTC)`;
today the same URL serves `d3c50306…` with the stamp `(06:12 UTC)`, and the **only** diff between
the two copies is that one stamp line. Note also that today the `/3/` alias is byte-identical to
the pinned `/3.15/` page — the alias caught up with the version pin — so the r93 S385-correction
note's parenthetical ("the `/3/` alias differs from it only in the Sphinx build stamp") is
now *coincidental* rather than structural. Practical consequence: **S385's recorded sha256 is
reproducible today but is not a durable digest**; re-verification must compare the title/version
string and the `-P`/`-I` anchors, never the sha256 of a live Sphinx page.

## 3. Rejected leads

**Lead A — `https://man.archlinux.org/man/limine.8`: HTTP 404**, 2706 bytes,
sha256 `e0ad4429a65972993ca9b07c6a5819a6486cc3e90eb61177a574c18a9d046deb`. First 200 bytes
verbatim: `\n\n<!DOCTYPE html>\n<html lang="en">\n    <head>\n        <meta charset="UTF-8">\n
<meta name="viewport" content="width=device-width, initial-scale=1.0">\n        <title>Page not found
— Arch manua` — i.e. the Arch "Page not found — Arch manual pages" template, not a man page.
**Reject reason:** there is no `limine.8`; upstream ships exactly one man page,
`man/man1/limine.1.in` (confirmed from the upstream tree at tag `v12.9.6`: `man/` contains only
`man1/`), and the installed package carries only `/usr/share/man/man1/limine.1.gz`. The nearby
lead **`https://man.archlinux.org/man/limine` → 200** (redirects to `/man/limine.1`) is the real
page — the *multiplexer* man page, and it says `version 12.9.6 / October 2026`, package
`extra/limine` `12.9.6-1`. It documents the CLI, not the config-file semantics the battery
certifies, so it is a locator, not support for C1/C2.

**Lead B — GitHub release API `…/releases/tags/v12.9.6`: HTTP 200**, 26652 bytes, sha256
`51ab5294f118dcd1e46a31001eb80eca2fc1b5243198c5eb5a91d9e29e59b995`, `tag_name v12.9.6`,
`published_at 2026-10-27T23:16:30Z`, `prerelease false`, `draft false`. Its `body` says, in full:

> `Changelog can be found [here](https://github.com/Limine-Bootloader/Limine/blob/v12.9.6/ChangeLog).`
> `Tarballs are signed using key ID 05D29860D0A0668AAEFB9D691F3C021BECA23821 …`

plus the `gpg --keyserver … --recv-keys` and `gpg --verify` instructions. **Reject reason:** the
body is a pointer to the ChangeLog plus a signature-verification recipe — a *listing*, not a
document; the substantive text is the ChangeLog that is already pinned as S387. The release assets
are the tarballs (`limine-12.9.6.tar.{bz2,gz,xz}` + `.sig`, `limine-binary.tar.*`, `limine-binary.zip`).
Context: `releases/latest` = `v12.9.6` (2026-10-27) and the five latest releases are
12.9.6 / 12.9.5 / 12.9.4 / 12.9.3 / 12.9.2 — **the pinned tag is the current upstream release**,
so the pins are not behind. Upstream tags (`git ls-remote`):
`v12.9.4 → 1e512b2b…` (peeled `8ad14430…`), `v12.9.5 → c427781c…` (peeled `55a93085…`),
`v12.9.6 → 54727fd1…` (peeled `89a9512c…`).

## 4. Freshness findings the L1 can act on

1. **The host is two releases behind the Arch repo, and the default-era battery depends on it.**
   Installed `limine` is **12.9.4-1** (`pacman -Qi limine`); `limine --version` → `Limine 12.9.4`.
   But `https://archlinux.org/packages/extra/x86_64/limine/json/` reports **12.9.6-1**,
   `build_date 2026-10-28T07:52:55Z`, and the local sync db (`/var/lib/pacman/sync/extra.db`,
   mtime 2026-10-22) still lists only `limine-12.9.4-1`. A `pacman -Sy` + upgrade therefore moves
   the host to **12.9.6**, and with `--limine-version auto` the probe would then answer `12.9.6`
   (era `12.9.5+`), not `12.9.4`. The claim "the flag-free live run prints version 12.9.4 and
   source `probe`" is **true on this host today** and is therefore *host-coupled*: one package
   upgrade flips it, and the ERA-DEFAULT family (which expects the 12.9.4 answers because the
   host's real `limine` answers 12.9.4) would need re-baselining at 12.9.6. Worth stating as an
   explicit recheck trigger in the knowledge doc's `recheck:` line.
2. **The r94 source pins are not covered by any manifest.** `freeze-manifest.sha256` (12 lines) and
   `instruments.sha256` (11 lines) contain **no** `before/src` entry, and
   `.ufo/waves/round-94/before/src/` has **no `SHA256SUMS`** — while r93's `before/src/` *did*
   ship one (3 lines, covering its three pins). The three r94 `limine-v12.9.6-*` copies are therefore integrity-checked by
   nothing in the wave directory (their digests match my fresh upstream fetch, but the lane has no
   recorded expectation to check against). Additive, one-line-each fix for the L1.
3. **S385's sha256 is a moving digest** (§2) — re-verify by version string and anchors, not sha.

## 5. What I did not do

No claim adjudication (the claim seats own C1/C2 verdicts); no battery or gate run (other seats);
no edit to `corpus/SOURCES.md`, `corpus/knowledge/`, `corpus/lessons/`, the instruments, the freeze
manifest, or any sibling seat's files. `/boot/limine.conf` was not touched (it is root-only and
was never opened). No `sudo`, no pacman transaction, no `limine`/`bootctl`/`efibootmgr`/`objcopy`
invocation; host reads were `pacman -Qi/-Ql` and `cat`/`zcat` of the installed man page.

## Verdict

**Freshness axis: SUPPORTED, with three carryable notes.** The three v12.9.6 sources are pinned and
reproduce byte-for-byte from upstream today (`a940acae…`, `ab280b45…`, `4da21c7c…`); `common/lib/config.c`
and `host/limine.c` are **byte-identical to the v12.9.5 pins** (same sha256, empty `diff`) and the
ChangeLog moved only by the 12.9.6 release block — corroborating the lane's "the era rules did not
move at 12.9.6" statement (relevant to C1/C2's era logic, not a verdict on either claim).
**S385's committed sha256 `d3c503060ebf…` reproduces exactly** and its title carries `Python 3.15.2`
— it does **not** differ from the committed value, but the digest is Sphinx-stamp-dependent and
must not be re-verified by sha256. The lead `man.archlinux.org/man/limine.8` is **404** (no `limine.8`
exists upstream or in the package; the real page is `limine(1)` at `…/man/limine`), and the
release-API body is a **pointer plus a gpg recipe**, so both are rejected as sources — consistent
with the round-94 declaration's rejection list. New freshness notes for the L1: (a) the host's
`limine` 12.9.4-1 is **two releases behind the Arch repo's 12.9.6-1**, so the auto-probe default
and the ERA-DEFAULT family are one package upgrade away from flipping; (b) the r94 `before/src`
pins are **absent from both wave manifests** and lack the `SHA256SUMS` file r93 had.
Receipts: `.ufo/waves/round-94/w1/ScoutSource/{pin-table.tsv,quotes.md,receipt-01-v1296-vs-v1295-bytes.txt,receipt-02-s385-reopen.txt,receipt-03-rejected-leads.txt,pins/}`.
