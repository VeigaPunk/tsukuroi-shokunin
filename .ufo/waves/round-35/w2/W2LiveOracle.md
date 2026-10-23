# W2LiveOracle — round 35, C1 counter VERSION 2, the live view cross-check

Seat: `W2LiveOracle` (wave 2, pre-freeze adversarial control wave, lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`).
Counter under test: `tools/score-pacnew-arm-r35b.py` VERSION 2 at `7186722b8eba243439c6724766bdae2ef13c595c`, `counter_sha256` `7517af92e0c9308c10f04b90d05a699cfa56278a736ef975d97ba08fbd957dc1` (matches the counter's own receipt header).
Claim base: `b40c01df38eb26f74c095c471efc6d1649b00fd4`.

**Verdict: the eight live values computed independently with shell and the counter's `oracle_of("/etc", lines)` agree exactly. But the live view is reachable by two controls that skip the live computation entirely and meet the after-value 24 of 24 — one gated on `/etc` content, one gated on the working directory's content — and neither inspects its own namespace. Under the round-35 §9 rule ("a target must be one that a do-nothing control, a content-free output or a shortcut keyed on fixture ids or labels cannot reach"), a live view that a content-keyed shortcut reaches does not satisfy the rule, so this is a finding against the counter's live view, not a confirmation of it.**

---

## 1. The eight live values: independent shell computation vs `oracle_of` — they agree

`[obs]` Independent computation used only `find`/`grep`/`sort`/`comm` with `LC_ALL=C`, names only, no writes, no `sudo`. Script `/fast/scratch/hyaku/tsukuroi-r35/W2LiveOracle/sh_oracle.sh`; output preserved in `capture_final.txt` §1.

| field | independent shell | counter's `oracle_of("/etc", lines)` | equal |
|---|---|---|---|
| pacnew | 3 | 3 | yes |
| pacsave | 0 | 0 | yes |
| pacorig | 0 | 0 | yes |
| unreadable | 11 | 11 | yes |
| log_pacnew | 3 | 3 | yes |
| log_pacsave | 0 | 0 | yes |
| unlogged | 0 | 0 | yes |
| gone | 0 | 0 | yes |

`[obs]` The three `.pacnew` files are `/etc/locale.gen.pacnew`, `/etc/tpm2-tss/fapi-profiles/P_ECCP384SHA384.json.pacnew`, `/etc/tpm2-tss/fapi-profiles/P_RSA3072SHA384.json.pacnew`. Each has exactly one matching log line in `/var/log/pacman.log` (lines 1427, 1645, 1646), so `log_pacnew=3`, `unlogged=0`, `gone=0`. `pacman.log` has 3191 lines and 7 `[ALPM] warning` lines; the other 4 are `directory permissions differ on /mnt/boot//boot/` and are correctly not counted. There is no `saved as` line anywhere in the log, so `log_pacsave=0`.

`[obs]` The 11 unreadable directories, identical as a set between the oracle (`os.scandir` → `PermissionError`) and GNU find's stderr (`/fast/scratch/hyaku/tsukuroi-r35/W2LiveOracle/oracle_locked.txt` vs `find_locked.txt`, `diff` empty after stripping the trailing `/` the sed adds): `/etc/audit/plugins.d`, `/etc/cni/net.d`, `/etc/credstore`, `/etc/credstore.encrypted`, `/etc/cups/ssl`, `/etc/pacman.d/gnupg/crls.d`, `/etc/pacman.d/gnupg/openpgp-revocs.d`, `/etc/pacman.d/gnupg/private-keys-v1.d`, `/etc/polkit-1/rules.d`, `/etc/ssl/private`, `/etc/sudoers.d`.

`[obs]` The live host has no directory that is readable-but-not-executable and none that is executable-but-not-readable, so the oracle's `os.lstat` path and find's `-type` path cannot diverge here. A synthetic `0400` directory does make the oracle raise `PermissionError` out of `oracle_of` (the `walk()` helper only catches `PermissionError` around `os.scandir`, not around `os.lstat`) while GNU find lists the file without error — `capture_final.txt` does not include this, it was measured separately in the scratch dir and is recorded here as `[obs]` only. It is not reachable on the live host.

`[obs]` The counter's own `CONTROL_ARM`, run verbatim on the live host under the counter's `BASE_ENV`, prints exactly `DRIFT pacnew-plane pacnew=3 pacsave=0 pacorig=0 unreadable=11 log_pacnew=3 log_pacsave=0 unlogged=0 gone=0` — the same line the shell oracle and `oracle_of` agree on (`capture_final.txt` §4).

---

## 2. `find`'s permission-denied messages under the user's own locale vs `LC_ALL=C` — the quote characters change

`[obs]` The counter's `BASE_ENV` is `{'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C'}`. The user's own locale on this host is `LANG=en_US.UTF-8` with `LC_ALL` empty (`locale` output; `/usr/lib/locale` holds only `C.utf8` and a `locale-archive`).

GNU findutils 4.11.0-modified (`/usr/bin/find --version`) writes the offending path with locale-dependent quoting. Raw stderr bytes for the same directory, `find` resolved through `PATH` exactly as the arm does it:

| environment | first stderr line, as bytes |
|---|---|
| `LC_ALL=C` (counter `BASE_ENV`) | `find: '/etc/ssl/private': Permission denied` — ASCII `'` = `0x27` |
| `LANG=en_US.UTF-8` (the user's own locale) | `find: ‘/etc/ssl/private’: Permission denied` — U+2018 `342 200 230` and U+2019 `342 200 231` |
| `LC_ALL=de_DE.UTF-8` (German, generated into scratch with `localedef`) | `find: »/etc/ssl/private«: Keine Berechtigung` — U+00BB `302 273` / U+00AB `302 273`, and the message text itself is translated |

Full byte dumps: `capture_final.txt` §2.

`[obs]` The mechanism separates cleanly. With `LC_MESSAGES=de_DE.UTF-8` and `LC_CTYPE=C` the quotes stay ASCII `'` while the message text becomes `Keine Berechtigung`; with `LC_CTYPE` in a UTF-8 locale and `LC_MESSAGES=C` the text stays `Permission denied` while the quotes become the U+2018/U+2019 pair. So the quote characters follow `LC_CTYPE` (the locale's "quotation style") and the message wording follows `LC_MESSAGES` (gettext). `capture_final.txt` §2 second block.

`[obs]` Two consequences, both measured:

- `grep -c 'Permission denied'` still returns 11 under `en_US.UTF-8` (the wording is English there), but returns **0** under a German locale. The arm's `unr` count therefore collapses to 0 under any non-English `LC_MESSAGES`. Running the counter's own `CONTROL_ARM` on the live host under `LC_ALL=de_DE.UTF-8` gives `unreadable=0` instead of 11 (`capture_final.txt` §4).
- The arm's `sed -nE "s#^find: '$etc/(.*)': Permission denied#/etc/\1/#p"` uses **ASCII** single quotes. Under `en_US.UTF-8` it extracts **0 lines** where `LC_ALL=C` extracts 11. A quote-tolerant variant extracts 11 in both. This matters for the `gone` computation, which uses the extracted list to decide whether a logged target lies beneath an unreadable directory: on a synthetic fixture with a locked directory holding a logged `.pacnew`, the same arm prints `gone=1` under `en_US.UTF-8` and `gone=0` under `LC_ALL=C`, while the oracle says `gone=0`. The live host happens not to expose this because its `gone` is 0 either way, but the stub and namespace views do.

`[inf]` The census does not pin a locale globally — `grep -nE '^\s*export (LC_ALL|LANG)|^\s*(LC_ALL|LANG)='` on `tools/tsukuroi-census.sh` at the claim base returns nothing, and the five `LC_ALL=C` uses are per-command (`env LC_ALL=C stat`, `LC_ALL=C sort`), never applied to `find`. A new pacnew/pacsave arm that parses `find`'s stderr would therefore inherit the caller's locale in production while the counter always exercises it under `LC_ALL=C`. The candidate census should pin `LC_ALL=C` on the `find` invocation (or on the whole arm) and the counter should be run at least once under the production locale to catch the class.

---

## 3. The counter's live run environment (`BASE_ENV`) vs a production invocation — a census can key on it, and two controls did

`[obs]` `BASE_ENV` (`{'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C'}`) differs from a production invocation in ways that are cheap to detect. Measured with an identical probe script run three ways (`capture_final.txt` §3):

| signal | stub view | namespace view | **live view** | production invocation |
|---|---|---|---|---|
| `LC_ALL` | `C` | `C` | `C` | unset (`LANG=en_US.UTF-8`) |
| `HOME` | set (fixture home) | unset | **unset** | `/home/vgpnk` |
| `PATH` | `/usr/bin:/bin` | `/usr/bin:/bin` | `/usr/bin:/bin` | 22 entries, incl. `/home/vgpnk/.local/bin` |
| exported env var count | 34 | 6 | **6** | 263 |
| `/etc/pacman.conf` present | yes | **no** (fixture over-mount) | **yes** | yes |
| `/etc/ssl`, `/etc/pacman.d` present | yes | **no** | **yes** | yes |
| `id -u` | 1000 | **0** (root in the user namespace) | 1000 | 1000 |
| `/proc/self/uid_map` | `0 0 4294967295` | `0 1000 1` | `0 0 4294967295` | `0 0 4294967295` |
| `mountinfo` entries for `/etc` | 0 | **1** | 0 | 0 |
| cwd contents | `etc,h,pacman.log` | `etc,pacman.log` | **`census-candidate.sh,v00,v01`** | the lane checkout |

`[obs]` The counter's own docstring names one limit: "a census that tells the namespace view from production by inspecting its own namespace (uid_map, mountinfo) can tell the namespace view from production" — that is the named limit, to be reported as such and not as a kill. Both controls below stay **outside** that limit: neither reads `uid_map` nor `mountinfo` nor any `/proc` file.

### Control A — live-cache gated on `/etc` content

`[obs]` A census variant that, when `TSUKUROI_ETC_DIR` is unset and `/etc/pacman.conf` exists, prints the live host's eight values as a constant and returns without any sweep or log read; otherwise it runs the counter's `CONTROL_ARM` unchanged. The gate is pure content of `/etc` — the real host's `/etc/pacman.conf` is absent in the namespace views (the fixture is bind-mounted over `/etc`) and present in the live view.

`[obs]` Scored once with the C1 counter through `run-receipt.py` at `--tool-revision 7186722b8eba243439c6724766bdae2ef13c595c` with `--skip-battery`. Receipt `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2LiveOracle/livecache-variant.jsonl` (sha256 `2ac7af0ec705b22ca20d592ee5211d1a36dbe03165db4bf633d44f62237288db`), patch `livecache-variant.patch` (sha256 `c731f67f624202b1dbc97a26955993ecacef17847694d1b8aa1cb23bdc7521f1`), variant commit `3cd522c` in the seat's sandbox clone.

Header: `counter_sha256` `7517af92e0c9308c10f04b90d05a699cfa56278a736ef975d97ba08fbd957dc1`, `census_sha256` `7ecba65eabfd6e825c489198d228246edcd8870b2a10d969375d287c1cf4839a`.
Summary line: `candidate_matches` **24**, `of` **24**, `harness_errors` **empty**, `exit_code` **0**. Every view's `reason` is `null`; the live view reports `{"gone": 0, "log_pacnew": 3, "log_pacsave": 0, "pacnew": 3, "pacorig": 0, "pacsave": 0, "unlogged": 0, "unreadable": 11}` against the same `expected`.

### Control B — live-cache gated on the working directory's content

`[obs]` The same census, but the gate is `[ ! -e "$PWD/pacman.log" ]`: the stub and namespace views run with the fixture directory as cwd (which contains `pacman.log`), the live view runs with the counter's temporary directory as cwd (which does not). No `/etc` content probe, no namespace inspection.

Receipt `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2LiveOracle/cwdgate-variant.jsonl` (sha256 `b8d3efdcc8ed8b3939281e3881ab72f62affef065c0fb24f77e49f4f51d990a5`), patch `cwdgate-variant.patch` (sha256 `4d2440abefe5210d3d8fc5ff2274a13a81fd19c7ede9505e3289e8f64c9a857b`), variant commit `d294372`.

Header: `counter_sha256` `7517af92e0c9308c10f04b90d05a699cfa56278a736ef975d97ba08fbd957dc1`, `census_sha256` `909ef205a49fe18f73e51457b1cf027acb82445fa716994cbe890d8057b0f75c`.
Summary line: `candidate_matches` **24**, `of` **24**, `harness_errors` **empty**, `exit_code` **0**. The live view reports and expects the same eight values.

`[obs]` Both controls are the counter's own `F02-cached-live` shape with the gate moved from "the seam is unset" to a signal that is false in the namespace views. `F02` is in the battery and is refused there because the cached-live branch fires in the namespace views as well (the seam is unset there too). Moving the gate to a content signal the namespace views fail makes the cached-live branch fire **only** in the live view, and the battery has no arm for it.

### What this means against the round-35 rule

`[inf]` The round prompt's §9 rule says the target must be one that "a do-nothing control, a content-free output or a shortcut keyed on fixture ids or labels cannot reach". Controls A and B are a content-free output in the live view — a hardcoded constant — reached by a shortcut keyed on host content (`/etc/pacman.conf`, `$PWD/pacman.log`), not on fixture ids or labels. The counter's live view therefore does not certify that a census computes the live drift surface; it certifies only that the census's live line equals the live values, and a hardcoded line satisfies that whenever the live values are the ones cached.

`[inf]` The kill rule as declared ("any control that skips or bends part of the work and meets ends C1", exception for a census that inspects its own namespace) covers A and B: they skip the work, they meet the after-value, and they are not the named namespace-inspection limit. This is reported plainly as a finding against the counter's live view.

`[inf]` The counter's live view is also structurally weaker than the other views on the "leaves the view's etc tree and log unchanged" clause. In the stub and namespace views `judge()` receives `unchanged = ctimes(etc, log) == pre and snapshot(etc, log, locked) == before` — bytes, modes and inode change times over the whole tree. In the live view it receives only `again == live_expected`, i.e. the eight recomputed values; nothing checks that the live `/etc` was left byte-identical. A census that wrote to `/etc` outside the counted names would not be caught by the live view. (Measured by reading the live-view block of `main()` in the counter; not exercised, because the only way to exercise it is to write to the real `/etc`, and host actions here are read-only. A variant doing that was built in the scratch clone and then discarded without being scored.)

---

## 4. Other observations

`[obs]` `find` in the agent's own shell is a **shell builtin** (Rust `find` 0.8.0, message format `Error: /etc/credstore: Permission denied (os error 13)`), not `/usr/bin/find`. Any measurement of `find`'s behaviour must be taken through `bash -c` or an explicit `/usr/bin/find` path, or it measures the wrong program. `bash -c 'type find'` gives `/usr/bin/find`; the counter runs the census as `bash <script>`, so the counter is unaffected. All numbers in this report were taken via `bash -c` or `/usr/bin/find` explicitly, and are labelled where the distinction mattered (`capture_final.txt` §2 shows both forms: `/usr/bin/find: '...'` with the full path in `argv[0]` versus `find: '...'` when resolved through `PATH`).

`[obs]` The census at the claim base does not pin `LC_ALL` for its two `find` calls (`tools/tsukuroi-census.sh:1099` and `:1946-1947`).

`[obs]` `tools/tsukuroi-census.sh` is byte-identical at the claim base and at `7186722b8eba243439c6724766bdae2ef13c595c` (sha256 `7daa2ccbbded3a931abdbd76cb8ad34ccbe596f6dabc3524c519cc123e44e7b5` for both) — the claimed change does not exist in the lane yet, as the round prompt states.

`[unk]` Whether the L1 wants the live view strengthened (a live view whose expected values cannot be met by a cached constant — e.g. a view over a copied, changing `/etc` tree rather than the real host) or the §9 rule restated is not my call; both are outside this seat's scope and this report states the finding, not the remedy.

---

## Files

Evidence written under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2LiveOracle/`:

- `capture_final.txt` — sha256 `02f0ad8ae675a61f890ec2900d8d4404ff016c41e6304f83346881761fdbd022` — the consolidated capture (shell oracle, `oracle_of`, locale byte dumps, view fingerprint, locked-dir set diff).
- `livecache-variant.jsonl` — sha256 `2ac7af0ec705b22ca20d592ee5211d1a36dbe03165db4bf633d44f62237288db` — Control A receipt.
- `livecache-variant.patch` — sha256 `c731f67f624202b1dbc97a26955993ecacef17847694d1b8aa1cb23bdc7521f1`.
- `cwdgate-variant.jsonl` — sha256 `b8d3efdcc8ed8b3939281e3881ab72f62affef065c0fb24f77e49f4f51d990a5` — Control B receipt.
- `cwdgate-variant.patch` — sha256 `4d2440abefe5210d3d8fc5ff2274a13a81fd19c7ede9505e3289e8f64c9a857b`.

Sandbox clone (commits only there, never in the lane): `/fast/scratch/hyaku/tsukuroi-r35/W2LiveOracle/repo`, variant commits `3cd522c` (Control A) and `d294372` (Control B), both on top of `7186722b8eba243439c6724766bdae2ef13c595c`.

Scope: read=<counter VERSION 2 source at 7186722b (docstring, PREDICATE, CONTROL_ARM, BATTERY, oracle_of, harness, main), tools/tsukuroi-census.sh at the claim base, corpus/QUALITY.md, the round-35 declaration in SCORECARD.md; live host read-only (/etc tree listing via find, /var/log/pacman.log via grep, id, locale, /proc/self/{uid_map,mountinfo}); wrote=.ufo/waves/round-35/w2/W2LiveOracle/{capture_final.txt,livecache-variant.jsonl,livecache-variant.patch,cwdgate-variant.jsonl,cwdgate-variant.patch,../../w2/W2LiveOracle.md}; executed=2× run-receipt.py scoring (--skip-battery, tool-revision 7186722b) writing the two receipts, plus read-only shell probes (find/grep/sort/comm, localedef into scratch, unshare/setpriv namespace probe, python3 import-by-path of the counter)>
Model: minimax-code/MiniMax-M3.1-Flash
Installs: none
