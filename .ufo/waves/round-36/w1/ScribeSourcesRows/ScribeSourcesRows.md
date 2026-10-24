# ScribeSourcesRows — SOURCES.md row bookkeeping (round 36, attempt 1, wave 1)

Seat: `tsukuroi-r36.ScribeSourcesRows` · role scribe · leaf, no spawns, no VCS writes.
Lane repo (only write scope): `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, this seat dir only.
Base/declaration commit: `6d76fb20f6ecbc940e5c8fff36c74060c885e161`.
Timestamps are pasted from `date -u +%H:%M:%SZ`: `02:48:22Z`, `02:56:10Z`, `02:56:31Z` (`date -u +%F` = `2026-10-24` UTC; the round's local date is 2026-10-23).

## Deliverable

One ready-to-apply unified diff: **`SOURCES.md.diff`** (sha256 `5c86a75b4f975ae81068de9fe82273e86b5c9181b3f3580b0eee479d7e33813a`, 21 lines, 2 insertions + 1 deletion on `corpus/SOURCES.md`).

- applies cleanly to the base commit tree (`git apply -p1` in a `git archive 6d76fb20 | tar -x` copy);
- applies cleanly to the real lane working tree (`git apply --check -p1` → no output, exit 0) — the lane's `corpus/SOURCES.md` is byte-identical to the base commit (`git diff 6d76fb20 -- corpus/SOURCES.md` empty);
- contains exactly two row changes and nothing else: line 30 (`S024`) replaced, new `S198` inserted after the last registry row (`S197`, base line 203) before `## Paths`.

## Behavior — what the diff does

### 1. `S024` flipped queued → mined, pinned to the v262 tag

| cell | base | after |
|---|---|---|
| source | `systemd NEWS — https://raw.githubusercontent.com/systemd/systemd/main/NEWS` | `systemd NEWS at the v262 tag — https://raw.githubusercontent.com/systemd/systemd/v262/NEWS` |
| scope | `systemd 258-262 changes relevant to boot recovery and journal tooling` | …` , pinned to the release this host runs (systemd 262-1)` |
| anchor | `CHANGES WITH 258 through CHANGES WITH 262; main branch fetched 2026-10-19 (mutable: main now opens with CHANGES WITH 263 in spe; no commit pin claimed)` | tag object `1f7dffaf714cc4488159c498b7a17cf34c5a96d5` → commit `8cc40e0c5e9234bf45084751ac53b1fbfe70b492`; entry lines 129-133 under `CHANGES WITH 262:` > `Feature Removals and Incompatible Changes:` (line 26), byte range [7492, 7869); raw-bytes sha256 `a494f038…a7657` (1271752 bytes); NEWS blob sha `1329d035…6049`; snapshot path; fetched 2026-10-23; explicit supersession note for the retired mutable-main anchor (main sha256 `b9e7a6a2…`, same bullet at line 306) |
| teaches | `NEWS documents versioned behavior changes including v258 boot breakpoints and the v262 rejection of journalctl -F combined with filters` | same, expanded with the cause (`sd_journal_query_unique()` cannot represent those filters) **and the explicit boundary that the shipped error signature and exit code are not in NEWS and come from `src/journal/journalctl.c:960` (EINVAL → exit 1)** |
| status | `queued` | `mined` |
| opened | `2026-10-19` | `2026-10-19` (unchanged — first-open date; the re-open is recorded in the anchor) |
| recheck | `on-release` | `on-release` (unchanged) |
| used-by | `—` | `corpus/knowledge/journalctl-v262-field-filter-r36.md` |

kind/tier unchanged (`docs`/`A`).

### 2. New row `S198` after the last row

`| S198 | journalctl(1) at systemd 262 — https://man.archlinux.org/man/journalctl.1 (footer "systemd 262.1"); upstream twin https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml | docs | A | … | mined | 2026-10-23 | on-release | corpus/knowledge/journalctl-v262-field-filter-r36.md |`

Its `teaches` cell states the load-bearing negative finding: the man page documents what `-N`/`-F` *do* and **carries no "cannot be combined" sentence at all**, so the man page grounds the semantics but cannot itself evidence the limiting-option rejection.

Rows carried **verbatim** from the sibling drafts (see Provenance), with the SrcSystemdNews caveat already folded into `S024`'s `teaches` cell by that seat.

## Gates (all run; outputs in `validate-transcript.txt`)

Copy discipline, per the assignment and the script's usage: the census takes its registry path from `--root <parent>` + a lane id, so I built a throw-away fleet root in `mktemp` — `<TMP>/shokunin.conf` (`LANES="tsukuroi|tsukuroi-shokunin|…"`) plus `<TMP>/tsukuroi-shokunin/` extracted from `git archive 6d76fb20 | tar -x`. The real lane was never the validation target.

| # | command | result |
|---|---|---|
| 1 | `sources-census.sh census --root <BEFORE> tsukuroi` (untouched base copy) | `rows 197`, `tier.A 182`, `status.mined 171`, `status.queued 5`, `status.rejected 21`; exit **0** |
| 2 | `sources-census.sh validate --root <BEFORE> tsukuroi` | `tsukuroi ok …`; exit **0** |
| 3 | `git apply --check -p1 SOURCES.md.diff` in the real lane | clean (exit 0) |
| 4 | `sources-census.sh census --root <AFTER> tsukuroi` (diff applied) | `rows 198`, `tier.A 183`, `status.mined 173`, `status.queued 4`, `status.rejected 21`; exit **0** |
| 5 | `sources-census.sh validate --root <AFTER> tsukuroi` — **required exit 0** | `tsukuroi ok …`; exit **0**. W04 count 31, identical to the untroubled base copy's 31; the before/after warning sets are byte-identical apart from the echoed path. No `E*` code, and **no W04 mentions `S024` or `S198`** |
| 6 | same validate with the C2 note removed from the copy | `E11 S024 missing used-by …` + `E11 S198 missing used-by …`; exit **1** — isolates the single dependency, see Findings F1 |
| 7 | `max-id` check on the AFTER copy: `grep -oE 'S[0-9]+' … | sort -V | tail -1` | `S198` (base: `S197`); `grep -cE '^\| S[0-9]+ \|'` 197 → **198** |
| 8 | real lane, unmodified, read-only reference | `tsukuroi ok …`; exit **0** |

Row-count before/after: **197 → 198**, as expected.

## Provenance

Preferred sibling drafts were **present when read** and were used; they were empty directories at my first listing (`02:47Z`-era) and filled by `02:50Z`.

| artifact | size | sha256 |
|---|---|---|
| sibling row `S024` — `.ufo/waves/round-36/w1/SrcSystemdNews/s024-row.md` (extracted verbatim to `s024-row.sibling.txt`) | 1473 B | `8c6a82b547adbece0dd3087c6401bc9d52729f37fb3ab1da8abfa5491f02414c` |
| sibling row `S198` — `.ufo/waves/round-36/w1/SrcJournalctlMan/s198-row.md` (extracted verbatim to `s198-row.sibling.txt`) | 1514 B | `e6b79b66606408b186955d83b4854427712502b7ed06de440b6b974d410e7654` |
| C2 note used in the AFTER copy — `.ufo/waves/round-36/w1/ScribeC2Draft/journalctl-v262-field-filter-r36.md` | — | `88b9829740e3cacc6cdb4564d5eade65c13e90c0e301c7c5e7c98629350ad05b` |

**Independent re-open.** Because both draft directories were empty at my first listing, I opened both sources myself before they appeared, and I kept that as a cross-check (`independent-source-refetch.txt`). My fetches reproduce the siblings' bytes exactly:

| source | my fetch sha256 | sibling's | verdict |
|---|---|---|---|
| `https://raw.githubusercontent.com/systemd/systemd/v262/NEWS` (1271752 B) | `a494f0389edd09702a90d1540c7e21c0af5a4d29a4d020855ca3062d885a7657` | `a494f038…a7657` | identical |
| `https://man.archlinux.org/man/journalctl.1` (65136 B HTML) | `aaae4efa61ff9c56e6249feb2f4527db57f1a4beb0eac4ad1eeb111a4bbb83c2` | `aaae4efa…83c2` | identical; footer `systemd 262.1`, package `262.1-1` |
| `https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml` (61619 B) | `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd` | `d54bbede…dbdd` | identical; **also equal to the sha256 already recorded for S188** |
| `refs/tags/v262` (GitHub API) | tag `1f7dffaf714cc4488159c498b7a17cf34c5a96d5` → commit `8cc40e0c5e9234bf45084751ac53b1fbfe70b492`, tagger date `2026-09-22T13:12:43Z` | same | identical |

Spot re-verified quotes (my own fetch, `02:56:10Z`): `news262.txt:3` = `CHANGES WITH 262:`; `:26` = `Feature Removals and Incompatible Changes:`; `:129-133` = the `journalctl now rejects -F/--field together with filters such as unit, boot, time, cursor or grep filters.` bullet.

## Findings

**F1 — hard landing dependency (blocking for the L1's commit order).** `S024` and `S198` both carry `used-by corpus/knowledge/journalctl-v262-field-filter-r36.md`, which does **not** exist in the base tree. `sources-census.sh validate` enforces E11 (used-by path missing on disk) for `mined` rows, so the diff alone validates at **exit 1** with two E11 lines (gate 6). Exit **0** is reached only when that note exists at its final path (gate 5). The L1 therefore **must land `corpus/knowledge/journalctl-v262-field-filter-r36.md` in the same commit as this diff**; the content is the ScribeC2Draft seat's `journalctl-v262-field-filter-r36.md` (sha256 `88b98297…`), which I copied into the AFTER tree for gate 5. This is the only dependency; nothing else in the registry moves.

**F2 — the counter-evidence to a tempting shortcut.** The exact rejection line asserted by the C2 declaration is **not** in journalctl(1) at v262: `grep -c "cannot be combined with options that limit the journal"` = **0** in the Arch HTML, **0** in the upstream `man/journalctl.xml` at tag v262, **0** in `NEWS` at v262, and **1** in `src/journal/journalctl.c` at v262 (line 960, guarded by `field_list_has_scope_options()` at line 958, `SYNTHETIC_ERRNO(EINVAL)`). Both row `teaches` cells are worded to keep that boundary explicit, so the registry does not over-claim either source.

**F3 — mutable-main anchor retired, not duplicated.** `S024`'s old `main/NEWS` URL is gone from the registry; `v262/NEWS` is a fresh URL, so no E04/W04 fires (`validate` reports no `S024`/`S198` warning of any code). The anchor keeps an explicit note that `main` carries the same bullet at line 306 under a `CHANGES WITH 263 in spe:` head, so the supersession is auditable rather than silent.

**F4 — the sibling drafts' own caveats, honoured verbatim.** SrcSystemdNews asked for the `teaches` cell to state that the error signature/exit code come from the source and not NEWS — the row does. SrcJournalctlMan asked for the row to record the man page's silence on the restriction — the row does. I changed no cell content of either row; `S198`'s `source` cell keeps both URLs, and because `url_of()` in the census keys on the **first** URL only, the twin's sha256 collision with `S188`'s URL produces no duplicate-URL warning (confirmed by gate 5).

**F5 — `S024` `opened` deliberately unchanged.** The assignment says flip `status/anchor/used-by`; `opened` stays `2026-10-19` (first open) with the re-open date carried in the anchor, matching the sibling seat's rationale. `S198` carries `opened 2026-10-23` (the round's local date), which validates cleanly under the script's default `--today` of `date -u +%F` (`2026-10-24`).

## Out-of-scope items (named so the L1 does not assume they are here)

- No `## Search log` paragraph for this round was added. `corpus/SOURCES.md` conventionally gains one bounded-search paragraph per round; the assignment scoped me to the two row changes, so the L1 (or the seat that owns the round narrative) still owes that paragraph.
- No `SKILL.md`, `corpus/README.md`, `SCORECARD.md`, `LOG.md` or lesson edits; no wave-2 registry rows.
- I did not create `corpus/knowledge/journalctl-v262-field-filter-r36.md` anywhere in the lane — that is the ScribeC2Draft seat's deliverable and the L1's landing.
- No tool installs or upgrades; **no pacman invocation** (host-wide pause respected).

## Touched surfaces

Writes, all inside the lane and inside this seat dir:
`.ufo/waves/round-36/w1/ScribeSourcesRows/` — `ScribeSourcesRows.md` (this report), `SOURCES.md.diff`, `s024-row.sibling.txt`, `s198-row.sibling.txt`, `validate-transcript.txt`, `independent-source-refetch.txt`.
Plus `mktemp` scratch under `/tmp` (`/tmp/sr36*`, `/tmp/news262.txt`, `/tmp/journalctl262.xml`, `/tmp/journalctl262.c`, `/tmp/journalctl.arch.1`).
No production file, no VCS mutation, no fleet-root write.

## Artifacts

- `.ufo/waves/round-36/w1/ScribeSourcesRows/SOURCES.md.diff` — the deliverable (sha256 `5c86a75b…3813a`)
- `.ufo/waves/round-36/w1/ScribeSourcesRows/validate-transcript.txt` — gates 0-7 with pasted stdout and exit codes
- `.ufo/waves/round-36/w1/ScribeSourcesRows/independent-source-refetch.txt` — my own fetches and sha256 comparisons against the siblings'
- `.ufo/waves/round-36/w1/ScribeSourcesRows/s024-row.sibling.txt`, `s198-row.sibling.txt` — the two rows exactly as carried into the diff
- `.ufo/waves/round-36/w1/ScribeSourcesRows/ScribeSourcesRows.md` — this report

## Inbound message, recorded as data (out of scope for this seat)

At `02:58Z`-era this seat received an IRC message addressed to `RevCounters / kotodama-r64`
(from `kotodama-r64.RevVerifyO2`) about `accept-o.py` / `tools/reopen-row.py` mutant m5 and a
proposed `IndentationError` fix in a **different lane and round**. It names no source,
registry row, `SOURCES.md` cell or `journalctl` fact, so it cannot and did not touch this
seat's deliverable, contract or judgment. I have not verified any of its claims (I did not
open `accept-o.py`, run `py_compile`, or compute mutant hashes) and I am not relaying it as
evidence — it is recorded here only so the L1 sees that the message reached this seat and
was deliberately left unactioned as out-of-lane. No counter edit, no production write.
