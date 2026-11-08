# ScoutUpstream — per-surface reconnaissance of the Limine visibility surface (round 92, w1)

Seat: ScoutUpstream (scout, read-only on the lane). Lane revision read at the start of the seat:
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` → **429fd1a34dfcdf951bf4aaedb2df4bc45835bede**
(freeze commit `da99b2f4bc442e5154a6c1da7350891c11ee7cb1` exists and is its ancestor:
`git log --oneline -3` → `429fd1a3 round-92: A2 control repair …` / `495a9f6c round-92: control repair (A1 …)` /
`da99b2f4 round-92: freeze — battery isolation (C1) and version-selected visibility (C2), controls, sources`).
This seat made **no** commit and ran no git/jj mutation. Lane reads only: `rev-parse`, `log`, `cat-file -t`,
`status --porcelain` (read-only), `sha256sum -c`, `sed`/`grep` on committed files.

Scratch: `/fast/scratch/hyaku/tsukuroi-r92/ScoutUpstream/` (created, used, **removed on exit**).
Nothing was installed; no `sudo`, no pacman transaction, no write to `/boot` `/efi` `/etc` `/usr` `/var`,
no `objcopy`/`limine`/`bootctl`/`efibootmgr`, no write to any `PATH` directory.

Receipts in this directory: `host-facts.txt`, `upstream-tags-and-changelog.txt`, `pin-verification.txt`,
`path-lines-characterised.txt`, `gate-era-and-pin-drift.txt`.

---

## 1. Fact table (fact · command · output · implication for the claim's freshness clause)

| # | fact | command | output (exact) | implication for C2's freshness clause |
|---|---|---|---|---|
| H1 | host installed Limine | `pacman -Q limine` | `limine 12.9.4-1` | the host is in the **pre-12.9.5 era**, so the gate's default `--limine-version 12.9.4` is correct *for the host as it stands today* |
| H2 | host binary version | `limine --version` | `Limine 12.9.4` (Copyright 2019-2026 Mintsuki, Kamila Szewczyk) | second, independent confirmation of H1; the gate's default is not contradicted by the binary |
| H3 | Arch repo version | `pacman -Si limine` | `Repository : extra`, `Version : 12.9.4-1`, `Build Date : Tue 20 Oct 2026 04:34:10 AM -03` — **this is the stale local sync DB** (`/var/lib/pacman/sync/extra.db` dated **Oct 22 2026**) | `pacman -Si` on this host **cannot** be used to detect the era: it reports the pre-upgrade version until the DB is synced |
| H4 | what the repo actually carries | `curl https://archlinux.org/packages/extra/x86_64/limine/json/` | `limine 12.9.6 - 1`, `last_update 2026-10-28T08:00:46.502Z`, `build_date 2026-10-28T07:52:55Z` | **Arch `extra` already ships 12.9.6-1.** The next `pacman -Syu` on this host silently moves the running Limine into the 12.9.5+ era while the gate's default stays `12.9.4` — this is *the* host-side trigger (see §4) |
| H5 | no TPM | `ls /sys/class/tpm` → `total 0`; `ls -A /sys/class/tpm \| wc -l` → `0`; `ls -l /dev/tpm*` → `No such file or directory` | host has **no** TPM | `--tpm-present` must be declared; on this host the honest value is `0`. Not a freshness fact per se, but it fixes the `--tpm-present` arm of the era families (`measured_boot` → `menu` not `halt`) |
| H6 | Secure Boot off | `od -An -tx1 /sys/firmware/efi/efivars/SecureBoot-8be4df61-…` | `06 00 00 00 00` (attr 06, data 00) | Secure Boot not enforced on the host; `--secure-boot-enforced 0` is the host-true value |
| H7 | `/boot` not readable | `cat /boot/limine.conf \| head -5` → `head: cannot open '/boot/limine.conf' for reading: Permission denied`; `ls -ld /boot` → `drwx------ 5 root root 4096 Dec 31 1969 /boot` | the live config is **not** observable by this seat | the freshness clause must not assert anything about the host config's first physical line; the committed r17 capture is the only evidence (see §3) |
| H8 | host python / bwrap | `python3 -VV` → `Python 3.14.8 (main, Oct 2 2026, …) [GCC 16.2.1 20260810]`; `bwrap --version` → `bubblewrap 0.13.1` | the isolation launcher (C1) has its dependencies present | the C1 launcher is runnable on this host; the `python-3-cmdline.txt` pin documents **3.15.2**, the host runs **3.14.8** — see P7 |
| U1 | upstream tags exist | `git ls-remote --tags https://github.com/limine-bootloader/limine.git` | `v12.9.4 → 1e512b2b7184` (peeled `8ad14430bc9f`), `v12.9.5 → c427781c6624` (peeled `55a93085435a`), `v12.9.6 → 54727fd1c0d5` (peeled `89a9512c623a`); **no tag after v12.9.6**, no rc/beta in 12.9.x | there is no upstream release beyond the two the claim pins; `v12.9.6` is the newest tree upstream |
| U2 | tag dates | GitHub API `git/refs/tags/<t>` + `commits/<sha>` | v12.9.4 commit `2026-10-19T15:31:20Z` (ChangeLog header `2026-10-19`); v12.9.5 `2026-10-27T16:28:54Z` (ChangeLog `2026-10-27`); v12.9.6 `2026-10-27T23:11:11Z` (ChangeLog header `2026-10-28`) | v12.9.4 → v12.9.5 is the **8-day** window that carries the semantic change; v12.9.5 → v12.9.6 is ~7 hours and carries none |
| U3 | releases API (is 12.9.7+ out?) | `curl 'https://api.github.com/repos/Limine-Bootloader/Limine/releases?per_page=10'` | newest release `v12.9.6 | 2026-10-27T23:16:30Z`; then `v12.9.5 | 2026-10-27T16:36:16Z`, `v12.9.4 | 2026-10-19T16:10:50Z` — **no 12.9.7** | **there is no 12.9.7+ release**; the answer to "does 12.9.7+ exist and touch `common/lib/config.c` again" is **no** |
| U4 | upstream HEAD == v12.9.6 | `git ls-remote … HEAD` → `89a9512c623a…` == `v12.9.6^{}`; `refs/heads/v12.x` → same sha | the default branch and the `v12.x` branch are **exactly** the v12.9.6 tag commit | there is no unreleased drift in the released line; the newest upstream *tree* is v12.9.6 |
| U5 | ChangeLog lines about config parsing / global options between the three tags | `diff limine-v12.9.4-ChangeLog.txt limine-v12.9.6-ChangeLog.txt \| grep -iE 'config\|global\|pars\|menu tree\|first entry\|first line\|option'` | 12.9.5: `- Parse the config in linear time. Configs with thousands of entries were slow to load.` · 12.9.6: `- Document that global options must come before the first entry, as has been the case since 4.0. A config whose first line is an entry has had no global options since 12.9.5, whereas every option in it used to count as global. Fixes #700.` · 12.9.5 (unrelated to visibility): `- Only take an SMBIOS config from tables within reach…`, `` - `default_entry: 0` no longer selects the first entry… `` | **exactly two** ChangeLog lines in the whole 12.9.4→12.9.6 delta bear on config parsing / global-option visibility: the 12.9.5 parser rewrite and the 12.9.6 documentation of it. The 12.9.5→12.9.6 delta adds **82** lines total and **none** of them change parsing behaviour |
| U6 | upstream confirms the 12.9.5 boundary | `issue-700.json` (pinned) | title `Global options after the first entry are ignored, unless the file starts with an entry`; `state closed`, `created 2026-10-27T18:52:23Z`, `closed 2026-10-27T22:43:43Z`, `closed_by Mintsuki`; PR **#702** `docs: clarify positioning of global options`, `merged_at 2026-10-27T22:41:28Z`, `changed_files 1` | upstream's own words fix the boundary at **12.9.5** ("has had no global options since 12.9.5"); #702 is a *docs* PR, i.e. the 12.9.6 release changed only documentation |
| U7 | `common/lib/config.c` history after v12.9.6 | GitHub API `commits?path=common/lib/config.c&since=2026-10-28T00:00:00Z` | **count 0** — no commit touches `common/lib/config.c` after 2026-10-28 | the V2 rule (>=12.9.5 ⇒ `create_menu_tree` cut) is **not invalidated by any upstream commit that exists today** |
| U8 | `trunk` branch (the only post-12.9.6 upstream tree) | `curl …/trunk/common/lib/config.c` → sha256 `e87a30d5fde446db…` vs pinned v12.9.6 `a940acae3a0a9c4d…`; `diff -u` | two hunks only: `#include <crypt/blake2b.h>` → `<crypt/hash.h>` and `CONFIG_B2SUM_EMPTY` re-wrapped, plus `init_config`'s checksum block rewritten to the generic `hash_reference_from_enrolled()` API. **The visibility cut is untouched**: `if (p > config_addr) { *(p - 1) = '\0'; }` is still at trunk raw **332-334** (v12.9.6: 328-330) and the label-end NUL `if (*p == '\n') { *p = '\0'; … }` at trunk raw **366** (v12.9.6: 362-365) | the trunk drift is **hash/checksum** drift, **not** visibility drift. It does not move the V2 boundary; but it is exactly the kind of change a future release carries, so the boundary must be stated as "the first release that changes the *cut*, not merely `config.c`" |
| P1 | pinned limine sources still verify | `sha256sum -c .ufo/waves/round-92/before/src/SHA256SUMS` (from that dir) | 8/8 `OK` | the pin set is internally intact |
| P2 | re-fetched raw URLs vs the pins | `curl` each URL in `URLS.txt`, `sha256sum` | `limine-v12.9.4-common_lib_config.c` = `aafc9c41…` **== pin**; `limine-v12.9.5-…` = `a940acae…` **== pin**; `limine-v12.9.6-…` = `a940acae…` **== pin**; `limine-v12.9.5-ChangeLog.txt` = `d2e08cc4…` **== pin**; `limine-v12.9.6-ChangeLog.txt` = `ab280b45…` **== pin**; `issue-700.json` = `7c7ac6e0…` **== pin**; `bubblewrap-bwrap.xml` = `2cb77df2…` **== pin** | **7 of 8 pins reproduce byte-exactly from their recorded URLs today.** The two `config.c` pins for 12.9.5 and 12.9.6 being the *same* hash is the mechanical fact behind the claim's "one rule for >= 12.9.5" |
| P3 | the one pin that does **not** reproduce byte-exactly | same command, `python-3-cmdline.txt` | pinned `558f4c7d…` (46 065 bytes, **0** `<` characters) vs a plain `curl` of `https://docs.python.org/3/using/cmdline.html` = `2371db30…` (171 073 bytes of HTML) | **the python-docs pin is a *text rendering* of the page, not the page bytes**; `sha256sum -c` passes because the *stored* file is unchanged, but the pin is **not reproducible from the URL** without the exact extraction recipe. It is also a **moving target**: docs.python.org/3 tracks the newest 3.x. Consequence for the freshness clause: the python pin is a *citation*, not a *digest of upstream* — it must never be re-verified by re-fetch |
| P4 | is the python pin's *content* stale? | compare pinned text vs today's live page (word-stream diff) | similarity **0.99887**, 8 non-equal opcodes (live adds `command`, `module name`, `pkg`, `script`; `n2`→`n 2`, `pythonversion`→`python version`); both carry `Last updated on Nov 08, 2026 (00:12 UTC)`; both are titled `Python 3.15.2 documentation` | the python pin's *content* is **current as of today** — the delta is the live page's newer `python [-c command \| -m module-name \| script \| -]` usage line. The `-I`/`-P`/`-E`/`-s` semantics the gate relies on are **verbatim identical** in both (`Run Python in isolated mode. This also implies -E, -P and -s options.` / `sys.path contains neither the script's directory nor the user's site-packages directory. All PYTHON* environment variables are ignored, too.`) |
| P5 | the freeze manifest is intact | `sha256sum -c .ufo/waves/round-92/before/freeze-manifest.sha256` (lane root) | **36/36 `OK`**, zero failures (manifest has 36 lines, not 30) | the kill rule "void if any instrument byte differs" does not trip; the gate/battery/control bytes are the frozen ones |
| P6 | installed `CONFIG.md` is an **era tell** | `sha256sum /usr/share/doc/limine/CONFIG.md` vs upstream v12.9.4 / v12.9.6 `CONFIG.md` | installed = `c9e8b670…` == upstream **v12.9.4** byte-for-byte; upstream v12.9.6 = `f44f3a19…`. The two differ in exactly the global-options paragraph: installed/v12.9.4 `*Global options* can appear anywhere in the file and are not part of an entry, although usually one would put them at the beginning of the config.` vs v12.9.6 `*Global options* must come before the first *menu entry*. Any that come after it are part of an entry, where they are ignored.` | **a cheap, read-only, root-free host-side detector for the era**: after the pacman upgrade to 12.9.6-1, `sha256sum /usr/share/doc/limine/CONFIG.md` flips `c9e8b670…` → `f44f3a19…`, and the installed `CONFIG.md` is itself the upstream doc that states the new rule. This is a better trigger than `pacman -Si` (which is stale per H3) |
| G1 | the gate's version contract as landed | `python3 tools/check-limine-pins.py --conf /dev/null --esp /tmp --limine-version <v>` for 12 values | accepted (`rc 0`, `visibility_era` = `pre-12.9.5` for 12.9.4, `12.9.5+` for 12.9.5 / **12.9.6** / **12.9.7** / **13.0.0** / **99.0.0**); refused `rc 64` with *no* JSON verdict for `12.9`, `12.9.x`, `""`, `abc`, `12.9.4.1` | the claim's "refuses versions outside X.Y.Z with rc 64" is **literally true**, but the refusal is a **format** refusal only: the gate **accepts any syntactically valid X.Y.Z ≥ 12.9.5 and silently answers it with the 12.9.5+ rule** |
| G2 | the gate never guesses the host version | `grep -n 'subprocess\|Popen\|pacman\|limine --version' tools/check-limine-pins.py` → **empty**; the battery likewise has no `pacman`/`limine --version` call | no auto-detection anywhere in the instrument chain | the era is **operator-declared**; after the host upgrade the operator *must* pass `--limine-version`, or the default must be re-pinned. There is no mechanism that would notice the upgrade |

---

## 2. The freshness boundary the claim should carry

**First upstream release that would invalidate the V2 rule:** the first release **after v12.9.6** that changes the
*global-section visibility cut* in `common/lib/config.c` — concretely, the first release whose `create_menu_tree()`
does not keep both (a) `if (p > config_addr) { *(p - 1) = '\0'; }` (cut before the first entry) and (b) the
label-end NUL `if (*p == '\n') { *p = '\0'; p++; }`.

Evidence that no such release exists today:
* U1/U3/U4 — v12.9.6 is the newest tag *and* the newest release *and* upstream HEAD == v12.9.6; there is no 12.9.7.
* U7 — zero commits touch `common/lib/config.c` after 2026-10-28.
* U8 — the only post-12.9.6 upstream tree (`trunk`) keeps the cut at raw 332-334/366 (shifted by +4/+1 lines);
  its `config.c` delta is **hash/checksum** only (blake2b → generic hash API), i.e. it moves `init_config`'s
  checksum block, not the visibility cut.
* P2 — 12.9.5's and 12.9.6's `config.c` are byte-identical (`a940acae…`), so ">= 12.9.5 ⇒ one rule" is a
  *measured* fact, not an assumption.

**So: the boundary is "the first upstream release after v12.9.6 that changes the cut".** The claim's V2 rule
(`>= 12.9.5` ⇒ `create_menu_tree` cut, no first-line exception) is correct for every upstream release that
exists as of 2026-11-08, and correct for `trunk` as of 2026-11-08.

**First release that would invalidate the *pin* (a weaker but real boundary):** any release that changes
`common/lib/config.c` *at all* shifts the raw line numbers the gate's docstring cites (v12.9.6 raw 328-330 and
362-365; v12.9.4 raw 642-650). `trunk` already shows this: the cut is at **332-334** and the label NUL at
**366**, not 328-330/362-365. A future release carrying trunk's hash change would therefore invalidate the
*citations* even though the *rule* is unchanged.

**Host-side trigger that must re-run the battery:** a **pacman update of the `limine` package** that takes the
host from `12.9.4-1` to `12.9.6-1`. Concretely:
* `pacman -Si limine` **cannot** be the trigger (H3: the local `extra.db` is dated Oct 22 2026 and still says
  `12.9.4-1`); the authoritative check is `https://archlinux.org/packages/extra/x86_64/limine/json/`
  (currently `12.9.6 - 1`, `last_update 2026-10-28`).
* The **root-free** detector that works today and after the upgrade is P6: `sha256sum /usr/share/doc/limine/CONFIG.md`
  — `c9e8b670…` = v12.9.4 era, `f44f3a19…` = v12.9.6 era.
* What must be re-pinned when it fires: (i) the gate's `--limine-version` **default** (`12.9.4` → `12.9.6`) —
  otherwise the default silently answers with the wrong era on the upgraded host; (ii) the battery's
  `ERA-DEFAULT` family, which is written against the 12.9.4 default (`fam_era_default` omits the flag and
  expects the 12.9.4 answer, with the docstring "Kills a gate whose default is the new era"); (iii) the raw
  line citations in the gate docstring / battery docstring.

**Not a trigger, but must be stated:** the *host config* is not observable by this seat (H7). Nothing in the
freshness clause may assert what the host's first physical line is.

---

## 3. The two `path:` lines the r91 receipt characterised

There are two distinct things in the r91 tree that this phrasing can point at; both are recorded verbatim in
`path-lines-characterised.txt`.

**(a) The literal `path:` lines in the r91 wave tree.** `grep -rn '^path:' .ufo/waves/round-91/` returns exactly
**two** matches, both in `w1/ScoutDrift/harness-output.txt`:

```
26:path: boot():/x#abc
61:path: boot():/x#abc
```

Both are the **fixture** pin line of ScoutDrift's case **"B: global panic AFTER first entry, first line is entry"**,
appearing twice because the same config is probed against two upstream versions: line 26 in the
**v12.9.4-vs-v12.9.6** harness (harness2) and line 61 in the **v12.9.4-vs-v12.9.5** harness (harness3). Their
characterisation, from that receipt:

```
== B: global panic AFTER first entry, first line is entry ==
v12.9.4  hash_mismatch_panic=no       measured_boot=(null)   visible=[/Shell
protocol: efi
path: boot():/x#abc
hash_mismatch_panic: no
]
v12.9.6(verbatim upstream file)  hash_mismatch_panic=(null)   measured_boot=(null)   visible=[/Shell]
```
and the same shape for v12.9.5 (`v12.9.5(verbatim upstream file)  hash_mismatch_panic=(null)`).

i.e. under 12.9.4 the pin line **and** the global key after it stay visible (the whole file is visible when
the first physical line is an entry line); under 12.9.5/12.9.6 the buffer is truncated at the entry label and
both the pin and the global key vanish. That is the V1/V2 inversion in its minimal form.

**(b) The host `path:` lines the r91 *host receipt* characterised**
(`.ufo/waves/round-91/before/host/receipt.txt`, a read-only root capture of 2026-11-07) — six `path:` lines of
`/boot/limine.conf`, at lines 30, 38, 50, 56, 64 and 72:

```
30:  path: boot():/EFI/Linux/omarchy_linux.efi#b990d8c6…        (protocol: efi at 29)
38:  path: boot():/EFI/Linux/omarchy_linux-lts.efi#a68c281d…     (protocol: efi at 37)
50:     path: boot():/432d02b544a5459ebbff9c42ec68334d/limine_history/omarchy_linux.efi_sha256_2e9c9bdc…   (protocol: efi at 49)
56:     path: boot():/432d02b544a5459ebbff9c42ec68334d/limine_history/omarchy_linux-lts.efi_sha256_2d49da06…  (protocol: efi at 55)
64:     path: boot():/432d02b544a5459ebbff9c42ec68334d/limine_history/omarchy_linux.efi_sha256_0f1e3c84…   (protocol: efi at 63)
72:path: boot():/EFI/BOOT/BOOTX64.EFI                             (protocol: efi at 71 — the only UNHASHED image line)
```
with the receipt's verdict `DEGRADED rc 1 on_panic menu findings ['LP-MISMATCH line 30', 'LP-MISMATCH line 38']`.
Of these, the two that the receipt characterises as **the unhashed fallback pair** are the **un-indented**
lines 71/72 (`/EFI fallback` entry: `protocol: efi` + `path: boot():/EFI/BOOT/BOOTX64.EFI`, no `#`), and the two
that the receipt characterises as **mismatching pins** are lines 30 and 38.

**Freshness reading of the host config.** The committed r17 capture
(`.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:126-133`, a `sudo grep` of `/boot/limine.conf`) shows the
host config's structure: line **3** `default_entry: 2`, the first `/`-entry at line **21** (`/+Omarchy`), then
`//linux` at 25 with its `path:` at **30**, `//linux-lts` at 33 with `path:` at **38**. So the host config has a
**non-empty global section before its first entry line** and its first physical line is **not** an entry line.
Under the V2 rule that means the host config's *own* global keys are read the same way in both eras — the V1/V2
inversion only bites a config whose **first physical line is an entry line**, which the host config is not.
That said: this is a **2026-10-20** capture of a file this seat cannot read (H7), it is `[INFERENCE]` from the
committed receipt, and it must **not** be promoted to a current host fact. The C2 predicate does not depend on it
(the battery's families are synthetic); only the *operational* exposure of the host's own config would.

---

## 4. What I did NOT do / could not determine

* **No lane write** except this seat's own receipt directory. No `git`/`jj` mutation in the lane or anywhere
  (no `add`/`commit`/`push`/`stash`/`checkout`/`reset`; no `jj commit`/`new`/`describe`/`squash`/`rebase`/`abandon`/`bookmark`).
  Read-only git only: `rev-parse`, `log`, `cat-file -t`, `status --porcelain`.
* **No host mutation.** `/boot` was never written and is not readable (`drwx------ root root`); no `sudo` at all;
  no `objcopy`/`strip`/`sbsign`/`ukify`/`patchelf`/`mkinitcpio`/`limine-install`/`bootctl`/`efibootmgr`/`pacman`;
  no `sysctl`; no write to `/sys`, `/proc`, `/etc`, `/usr`, `/var`; nothing written to `~/.local/bin` or any
  `PATH` directory; no fleet-root tracked file touched.
* **No tool installed or upgraded.** Nothing was needed: `git`, `curl`, `python3` (3.14.8), `pacman`, `bwrap`
  (0.13.1), `sha256sum`, `diff` were already present. (`python3 -m pip` is absent on this host — `No module named
  pip` — so the optional `html2text` cross-check of the python-doc pin was done with an in-process regex
  extractor instead; see P3/P4. This is a *missed convenience*, not a blocker, and it changed no conclusion.)
* **Could not determine:** the live `/boot/limine.conf` (H7) — hence the host's first physical line, the host's
  actual `hash_mismatch_panic`/`measured_boot` placement, and the current hash status of the six host `path:`
  lines are all `[INFERENCE]` from committed receipts, not current observations.
* **Could not determine:** what upstream will do to `common/lib/config.c` after `trunk`'s current state. That is
  the deliberate open end of the freshness clause ("the first release that changes the cut"), and it is not
  closable from today's tree. `trunk`'s hash-API rewrite (U8) shows upstream *is* still editing `config.c`
  post-12.9.6 — the next release may carry it, and it moves the cited raw line numbers even though it does not
  change the rule.
* **No subagent dispatched** (leaf member). No `ask` tool used; nothing sent to `agent://all`.
* **Scratch** `/fast/scratch/hyaku/tsukuroi-r92/ScoutUpstream/` was removed on exit (`rm -rf`); every artifact
  needed as evidence was copied into this seat's receipt directory first.

---

## 5. Confidence

* **High** for the upstream facts (U1–U8, P1–P2): every one is a direct read of the upstream repository or the
  GitHub API, and the two `config.c` pins were re-fetched and matched byte-for-byte.
* **High** for the host facts (H1–H8): direct command output; the only judgement is the reading of the stale
  sync DB (H3/H4), which is corroborated by the independent `archlinux.org` package JSON.
* **High** for the freshness boundary as stated ("the first release after v12.9.6 that changes the cut"), because
  the negative side is *measured* (no 12.9.7, zero post-2026-10-28 `config.c` commits, `trunk`'s cut intact)
  rather than assumed.
* **Medium** on the host-config exposure (§3b): it rests on a 2026-10-20 committed capture of a file this seat
  cannot read; flagged as `[INFERENCE]`, not a current fact.
* **Low / deliberately not claimed:** whether upstream's next release will change the cut, and whether
  `trunk`'s hash-API rewrite lands in 12.9.7.

## Verdict

C2 (depth) **supported** — the version-selected visibility rule's freshness boundary is real, dated and
nowhere past v12.9.6: upstream HEAD == the v12.9.6 tag (no 12.9.7 exists), zero commits touch
`common/lib/config.c` after 2026-10-28, `trunk`'s post-12.9.6 delta is hash-only and leaves the cut intact at
raw 332-334/366, and the two `config.c` pins for 12.9.5/12.9.6 are byte-identical (`a940acae…`), so
`>= 12.9.5 ⇒ one rule` is measured rather than assumed; the gate's rc-64 format refusal is confirmed live
(`12.9`, `12.9.x`, `""`, `abc`, `12.9.4.1` → rc 64, no verdict) and the freeze manifest verifies 36/36 with the
frozen gate/battery/control bytes.
C1 (operability) **not falsified, and only partially covered here** — the host facts this seat was asked for
(`pacman -Q limine` = `limine 12.9.4-1`, `limine --version` = `Limine 12.9.4`, `/sys/class/tpm` empty,
Secure Boot off, `bwrap 0.13.1` + `python3 3.14.8` present) are all recorded, but C1's isolation counts are not
my axis and are not asserted here.
Receipts proving it: `.ufo/waves/round-92/w1/ScoutUpstream/{host-facts.txt, upstream-tags-and-changelog.txt,
pin-verification.txt, path-lines-characterised.txt, gate-era-and-pin-drift.txt}`.
