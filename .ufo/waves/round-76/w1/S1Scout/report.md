# S1Scout — round 76 w1: independent verification of the four pinned v262 snapshots and the eight draft JD rows

Seat: S1Scout (scout, leaf). Lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Declaration `d5f0565bfb42a405ec024d8a5b0796514fb92002`, base `865b38c96c23ec0bcace8ca3ee884f860693ce43`.
Methods are read-only: second-route `curl -sSL --fail` into `$HYAKU_SCRATCH`, `sha256sum`, verbatim
whitespace-normalised quote location, and read-only host reads. No commit, no registry edit, no note edit.

## Verdict in one line

4/4 snapshot digests reproduce; 8/8 quotes FOUND with word counts inside 4–25; **two of eight rows are
PARTLY (JD3 arithmetic clause, JD7 function attribution)**; **one of four registry anchors is PARTLY
(S318 names MaxFileSec/MaxRetentionSec but its range stops at 320)**; host readings are internally
consistent and the host's 262.1-1 package is byte-identical to the v262 pin on all four paths.

## 1. Snapshot table — second-route re-fetch

Each URL was fetched from `SOURCES.json` with `curl -sSL --fail` into
`/fast/scratch/hyaku/tsukuroi-r76/S1Scout/refetch-*` and digested. Expected digests are identical in
`before/src/SOURCES.json` and `before/src/SHA256SUMS` (checked: no disagreement between the two files).

| # | url (v262) | digest observed (second route) | expected (`SOURCES.json` = `SHA256SUMS`) | bytes obs/exp | verdict |
|---|---|---|---|---|---|
| 1 | https://raw.githubusercontent.com/systemd/systemd/v262/man/journald.conf.xml | ed71e38df308227a94aca77b0840742b2c6ec49c1e43c2376d4aa135908f87f2 | ed71e38df308227a94aca77b0840742b2c6ec49c1e43c2376d4aa135908f87f2 | 32708/32708 | **MATCH** |
| 2 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-config.c | 99f3e972cc639985ff60f637a505938a65b164e9510fdcc30b15d9634bf81a9d | 99f3e972cc639985ff60f637a505938a65b164e9510fdcc30b15d9634bf81a9d | 20807/20807 | **MATCH** |
| 3 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c | 428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2 | 428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2 | 101383/101383 | **MATCH** |
| 4 | https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml | d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd | d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd | 61619/61619 | **MATCH** |

Checks run beyond the minimum:

- the committed snapshots under `before/src/` hash to the same four digests, so the receipt copies are
  the bytes the rows were written against;
- the same four paths at tag **v262.1** were fetched and are **byte-identical** (sha256 equal, `cmp` clean)
  to the v262 pin. The host runs systemd 262.1-1 (`host.txt`), so the pin is not off-version for this host;
- every draft row's `digest=` cell and every registry row's `sha256` token equal the snapshot digest
  (8/8 draft rows, 4/4 registry rows).

## 2. Quote table — eight draft rows

Locator: whole snapshot whitespace-normalised (runs → single space, per-line), quote searched in the
normalised stream; the reported line is the first line of the match (a two-line match reports both).
Word count is `len(quote.split())`. Entailment is judged against the quoted line **and its paragraph**,
as the row is required to stand on that evidence.

| JD | FOUND/MISS | line(s) in snapshot | words (4–25) | entailment | reason |
|---|---|---|---|---|---|
| JD1 | FOUND | 86 (`journald.conf.xml`) | 9 | **HOLD** | Lines 83–86: "auto behaves like persistent if the `/var/log/journal` directory exists, and volatile otherwise (the existence of the directory controls the storage mode)". The parenthetical is the manual's own wording and belongs to the `auto` sentence, so the row's scope ("auto") matches the quote's scope. No over-broad word. |
| JD2 | FOUND | 283–284 (`journald.conf.xml`) | 19 | **HOLD** | Lines 274–285 establish the antecedents: "The first pair" = `SystemMaxUse=`/`RuntimeMaxUse=` (274–276), "the second" = `SystemKeepFree=`/`RuntimeKeepFree=` (277–279); "each of the calculated default values is capped to 4G" is line 285. The row narrows to the `System*` members (true, not over-broad). Nit: the cap clause is one line outside the quote, so JD2 cannot be defended from the quote alone — it needs 285. |
| JD3 | FOUND | 170 (`journald-manager.c`) | 7 | **PARTLY — one false clause** | The clamp half is exact: `space->limit = CLAMP(vfs_used + avail, metrics->min_use, metrics->max_use)`. The middle clause is **wrong**: line 168 is `avail = LESS_BY(vfs_avail, metrics->keep_free)` and v262 `src/fundamental/macro.h:320-326` defines `LESS_BY(a,b)` as `a > b ? a - b : 0`. So the limit adds *free space remaining after reserving keep_free*, i.e. `max(0, free − keep_free)` — **not** "the smaller of free space and keep_free". `min(free, keep_free)` would be wrong on any host where free > keep_free, which is this host. Over-broad/mis-scoped words: **"the smaller of free space and keep_free"**. Consequence: the row's last clause ("so both the max-use and keep-free limits are respected") still holds — the limit is ≤ max_use and ≤ fs_size − keep_free — and the host figure is unaffected (both readings clamp to 256M), so this is a correctness defect in the record, not a wrong number. |
| JD4 | FOUND | 179 (`journald-manager.c`) | 11 | **HOLD** | Comment 176–184 plus line 185 `storage->metrics.min_use = MAX(storage->metrics.min_use, storage->space.vfs_used)`. "Raises to current usage" survives because `MAX` never lowers; "sudden spikes … will not cause journald to vacuum files without bounds" and "only a restart of journald will make it reset this value" are verbatim. Scope nit only: it is a floor-raise (`MAX`), not an assignment, and it runs both at startup and on first open of the journal files (calls at 386, 453, 1666, 1668), so "At startup" is a subset of the trigger set, not an over-claim. |
| JD5 | FOUND | 304 (`journald.conf.xml`) | 11 | **HOLD** | Lines 300–306: "Defaults to one eighth of the values configured with SystemMaxUse= and RuntimeMaxUse= capped to 128M, so that usually seven rotated journal files are kept as history. If the journal compact mode is enabled (enabled by default), the maximum file size is capped to 4G." All four clauses are in the paragraph. Nit: the quote alone carries only the seven-files clause; and the row drops "(enabled by default)" for compact mode — an omission, not an over-broad word. |
| JD6 | FOUND | 313–315 (`journald.conf.xml`) | 21 | **HOLD** | Quote covers "only archived files are deleted … active files will stay around"; "might still be more journal files around in total than this limit after a vacuuming operation is complete" is 317–318 and "This setting defaults to 100" is 318. Row's "default to 100" and "total can exceed the limit after a vacuum" both entailed. No over-broad word. |
| JD7 | FOUND | 25–26 (`journald-config.c`) | 6 | **PARTLY — attribution over-broad** | Values hold: `DEFAULT_SYNC_INTERVAL_USEC (5*USEC_PER_MINUTE)` 24, `DEFAULT_RATE_LIMIT_INTERVAL (30*USEC_PER_SEC)` 25, `DEFAULT_RATE_LIMIT_BURST 10000` 26, `DEFAULT_MAX_FILE_USEC USEC_PER_MONTH` 27; `USEC_PER_MONTH = 2629800 s` (`src/basic/time-util.h:54`), so 30 s / 10000 / 5 min / one month are all correct. The **function attribution is false**: `journal_config_set_defaults` (line 39) sets only `.ratelimit_interval` and `.ratelimit_burst` (51–52); `DEFAULT_SYNC_INTERVAL_USEC` and `DEFAULT_MAX_FILE_USEC` are applied by `MERGE_NON_ZERO` in `manager_merge_configs` (133, 142). Over-broad scope words: **"in journal_config_set_defaults"**. Same file, different function — this is the round-75 failure class (a function-level scope word the cited lines do not support). Nit: the 6-word quote carries only two of four values; 24 and 27 are outside it. |
| JD8 | FOUND | 954–955 (`journalctl.xml`) | 17 | **HOLD** | "Runs `--vacuum-size=` has only an indirect effect on the output shown by `--disk-usage`, as the latter includes active journal files, while the vacuuming operation only operates on archived journal files" is 969–971; `--disk-usage` "shows the sum of the disk usage of all archived and active journal files" is 943–944. Both clauses entailed, no over-broad word. |

Word counts: 9, 19, 7, 11, 11, 21, 6, 17 — **8/8 inside 4–25**; 0 MISS.

Over-broad-scope sweep (the round-75 failure class): the only two hits are JD3's
"the smaller of free space and keep_free" (a misstated formula) and JD7's "in
journal_config_set_defaults" (a function-scope over-attribution). JD1/JD2/JD4/JD5/JD6/JD8 contain no
scope word that outruns their evidence; their only weaknesses are quote-level (the decisive sentence sits
one to three lines outside the quote cell), which is allowed because the row is anchored to the paragraph.

## 3. Registry table — S318 … S321 in `corpus/SOURCES.md` (lines 329–332)

| row | 11 columns | kind/tier/status | anchor basename + range | cited lines inside range | used-by | `\|` in cell | verdict |
|---|---|---|---|---|---|---|---|
| S318 | yes (12 pipes → 11 fields) | docs / A / mined | `journald.conf.xml at v262, lines 75-93 (Storage=), 151-166 (SplitMode=), 170-238 (rate limiting), 243-320 (size limits, MaxFileSec, MaxRetentionSec), 366-455 (SyncIntervalSec, MaxLevelStore)` | 86 ∈ 75-93; 283–284, 304, 313–315 ∈ 243-320 | `corpus/knowledge/journald-retention-plane-r76.md` (file present, 10858 bytes) | none | **PARTLY** |
| S319 | yes | code / A / mined | `journald-config.c at v262, lines 24-27` | 25–26 ∈ 24-27 (range is exactly the four `#define`s) | same note path | none | **HOLD** |
| S320 | yes | code / A / mined | `journald-manager.c at v262, lines 143-186 … and 796-820` | 170, 179 ∈ 143-186 (`cache_space_refresh` 143, `patch_min_use` 176–185); 796-820 covers `manager_do_vacuum` 796–816 | same note path | none | **HOLD** |
| S321 | yes | docs / A / mined | `journalctl.xml at v262, lines 941-983` | 954–955 ∈ 941-983 (`--disk-usage` 941, `--vacuum-size=` 950, `--vacuum-files=` 952) | same note path | none | **HOLD** |

**S318 anchor defect (reported plainly).** The anchor's parenthetical names `MaxFileSec=` and
`MaxRetentionSec=`, but the stated range ends at line 320 — a blank line immediately before the
`MaxFileSec=` varlistentry, whose `<term>` is **line 322** and whose block runs to 341; `MaxRetentionSec=`
is **line 344** and runs to 364. Two of the five named sections therefore lie **outside** the recorded
range. No *cited* line falls outside: all four `journald.conf.xml` rows quote 86, 283–284, 304 and
313–315, all inside 75-93 / 243-320. Fix is one token: `243-320` → `243-364` (or drop the two names).
`Storage=` 75-93 is honest but runs two lines into the following "initially use volatile" paragraph;
`SplitMode=` 151-166 and `170-238` are accurate.

S321 nit: `--rotate`'s own definition is at 1051–1058, outside 941-983; the range does contain the
combination paragraph at 981–983 ("all active files are rotated first … all currently active files are
archived"), so the row's "rotate archives active files first" teaching is inside the recorded range — but
the switch definition is not. The vacuum block's tail (984–987) is also outside.

Registry-wide sanity: 322 `| S…` rows; S318–S321 are the last four; `kind` values in use are
docs/code/community, `tier` A/B/C, `status` mined/queued/rejected — the four new rows use legal values
and `mined` is consistent with a row whose note is committed alongside.

## 4. Host readings — `before/host.txt`

| reading | value | check |
|---|---|---|
| systemd version | 262.1-1 | matches the v262 pin byte-for-byte on all four paths (v262 vs v262.1 had zero differing files) |
| drop-in `/etc/systemd/journald.conf.d/size.conf` | `SystemMaxUse=256M`, `RuntimeMaxUse=64M`; main file all-commented | `systemd-analyze cat-config` shows exactly one uncommented source; `Storage` compile default shown as `persistent` |
| `journalctl --disk-usage` | 148.6M | reproduces today: 148.6M |
| journal files under `/var/log/journal` | 13 files, `sum_bytes=209715200` (200 MiB) | reproduces: `find … -printf '%s'` → count 13, sum 209715200 |
| `df -B1 /` vs `stat -f /` | total 998037782528, used 229459005440, avail 764239769600 | exactly consistent: `blocks*bsize` = 998037782528 = df total; `bavail*4096` = 764239769600 = df available; `(blocks−bfree)*4096` = 229459005440 = df used; the 4339007488 gap is reserved blocks |
| boot count | 3 | `journalctl --list-boots` prints a header plus 3 rows (4 lines), so the receipt's 3 is right |

**The 148.6M vs 200 MiB gap is not a contradiction, and it is the one number a reader will trip on.**
`du` allocated = 155,832,320 B = **148.60 MiB**, exactly the `--disk-usage` figure; `du --apparent-size`
= 209,715,200 B = 200 MiB, exactly `sum_bytes`. Journal files are sparse — the largest file is
25,165,824 B apparent but 33,648×512 = 17,227,776 B allocated (68%) — so `--disk-usage` sums allocated
blocks while the receipt's `sum_bytes` sums `st_size`. Anyone comparing the two must label the measure.
Derived figures in the note are consistent with this receipt: `SystemMaxFileSize` = 256M/8 = **32M**
(below the 128M cap; largest observed file 24 MiB < 32M) and the effective limit recomputes to **256M**.
Arithmetic, with the 4G cap applied to the percentage defaults (S318 lines 281–285: "each of the
calculated default values is capped to 4G"): `SystemKeepFree` default = min(0.15 × 998,037,782,528 =
149,705,667,379 B, 4 GiB = 4,294,967,296 B) = **4,294,967,296 B**; `SystemMaxUse` default =
min(0.10 × fs = 99,803,778,252 B, 4 GiB) = 4 GiB, replaced by the drop-in's **256M**. Then
`avail` = 764,239,769,600 − 4,294,967,296 = 759,944,802,304 B, `used` ≈ 155,832,320 B, so
`CLAMP(used+avail, min_use, max_use)` = `CLAMP(760,100,634,624, min_use, 268,435,456)` = **268,435,456 B =
256M**; `patch_min_use` sets the floor to the current usage (~148.6M), still below 256M, so the clamp does
not invert. *(Correction to a first pass of this report, which used the uncapped 15% figure 149,705,667,379 B
as keep_free: the 4G cap applies to that default too, so `avail` is `free − 4G`, not `free − 139.4 GiB`.
The 256M conclusion is unchanged because `max_use` binds either way.)* The exact code that applies the
4G cap to the percentage defaults lives outside the four pinned files (`journal_reset_metrics` is referenced
at `journald-config.c:66-67` but defined in a header not in the pin), so the cap is taken from S318, the
pinned manual sentence, not from pinned code.

**Which rows rely on host readings: none of the eight.** JD1–JD8 are all source rows (S318–S321). Only the
note's "Effective limits on this host" paragraph consumes `host.txt`, and only for four numbers
(`SystemMaxUse=256M`, `effective_limit=256M`, `SystemMaxFileSize=32M`, `observed 148.6M`) — all four hold.

## 5. Residual unknowns

- The `max_use`/`keep_free`/`min_use` numbers actually loaded at runtime were not read from the manager's
  own log (`LOG_ITEM("MAX_USE=…")`, `journald-manager.c:234-237`); the 256M/32M figures are derived from
  config plus source, not observed from a running journald debug log. Derivation matches the observed
  148.6M ceiling behaviour only indirectly.
- Whether the note's prose repeats the JD3 defect was not audited (non-goal). Spot-read while locating
  `used-by`: `corpus/knowledge/journald-retention-plane-r76.md` line ~40 does repeat the
  "smaller of the free space and the keep-free requirement is added to current usage" wording directly
  after quoting `avail = LESS_BY(vfs_avail, metrics->keep_free)`, so the note contradicts its own quoted
  line in the same paragraph.
- v262 vs v262.1 was compared for these four paths only, not for the rest of the tree.

## Tooling

No installs, no upgrades, no pacman transactions. `curl`, `sha256sum`, `du`, `stat`, `journalctl` were
already present.
