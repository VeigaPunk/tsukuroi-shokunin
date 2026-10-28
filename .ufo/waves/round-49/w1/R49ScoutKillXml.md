VERDICT: supports

# S248 live re-open (R49ScoutKillXml)

Opener of record for row S248. Freeze `55c07cd3f8bff2e12117c34d57b4c618de74d85c` `corpus/SOURCES.md:257`. `git diff 55c07cd3… HEAD -- corpus/SOURCES.md` has no S248 hunk, and `git diff --stat 55c07cd3… -- corpus/knowledge/btrfs-scrub-grounding-r45.md corpus/knowledge/btrfs-scrub-record-r44.md` is empty. SOURCES.md was not edited. No tools installed. Receipts: `.ufo/waves/round-49/w1/R49ScoutKillXml/`.

## 1. Fetch

Registry URL (`corpus/SOURCES.md:257`): `https://github.com/systemd/systemd/blob/v262/man/systemd.kill.xml`.

Raw URL that the pin was fetched from (`.ufo/waves/round-45/frozen/src/FETCH.txt:4`): `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.kill.xml`.

Access date: `2026-10-28` (`date -u +%F`; raw response `date: Wed, 28 Oct 2026 17:25:58 GMT`).

| fetch | redirects | HTTP | bytes | content-type | sha256 |
|---|---|---|---|---|---|
| raw.githubusercontent.com `v262/man/systemd.kill.xml` | 0 (`url_effective` unchanged) | 200 | 11224 | text/plain; charset=utf-8 | `448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72` |
| github.com `…/raw/v262/man/systemd.kill.xml` | 1 | 302 then 200 | 11224 | text/plain | same |
| SOURCES blob URL | 0 | 200 | 347713 | text/html; charset=utf-8 | `b89f1f1e5b350c5183c8d545d16b3f76dc1b9276221f68997dfbeb9d599cab28` (not the xml) |

The github.com raw URL's `location` is `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.kill.xml`. `cmp -s` of that body against the direct raw fetch printed equal, and `cmp -s` of the direct raw fetch against `.ufo/waves/round-45/frozen/src/systemd.kill.xml` printed `CMP_EQUAL`. The digest matches `SHA256SUMS:3` and the row's anchor digest. The blob page is HTML and is not byte-comparable to the snapshot.

Upstream did not move. `v262` is an annotated tag, not a branch. GitHub `git/ref/tags/v262` is still object `1f7dffaf714cc4488159c498b7a17cf34c5a96d5` type `tag` (FETCH.txt:7). That tag object peels to commit `8cc40e0c5e9234bf45084751ac53b1fbfe70b492` (FETCH.txt:8 and the row); `commits/v262` returns the same sha. Tagger `2026-09-22T13:12:43Z` Luca Boccassi, message `systemd v262`.

## 2. Anchors

Live bytes equal the pin (209 lines). Each quote is the live line with indentation removed, under 25 words, and is the GR3 quote at `btrfs-scrub-grounding-r45.md:173-185`. Both KillMode and TimeoutStopSec sit in the `KillMode=` varlistentry that opens at line 63 and closes at line 104; the row's registered window is lines 62-116.

- KillMode control-group, line 68 (paragraph continues through line 77): `<para>If set to <option>control-group</option>, all remaining processes in the control group of this`
- TimeoutStopSec condition, line 91 (listitem under "If processes still remain after:", lines 87-93; applies to control-group, mixed, and process): `<listitem><para>the delay configured via the <varname>TimeoutStopSec=</varname> has passed`
- SIGKILL repeat, line 96: `the termination request is repeated with the <constant>SIGKILL</constant> signal or the signal specified via`
- KillMode default, line 101: `<para>Defaults to <option>control-group</option>.</para>`
- KillSignal, line 108 (term at line 107): `<listitem><para>Specifies which signal to use when stopping a service. This controls the signal that`
- SIGCONT, line 114: `<para>Note that, right after sending the signal specified in this setting, systemd will always send`
- SIGCONT, line 115: `<constant>SIGCONT</constant>, to ensure that even suspended tasks can be terminated cleanly.</para>`

## 3. Cadence and pins

The `on-release` recheck, tag `v262`, peeled commit, and whole-file sha256 still read right: the tag object has not moved since the 2026-10-27 pin and today's raw bytes match it, and lines 62-116 still hold every GR3 quote.

## 4. Proposed status / recheck / used-by

no change

Freeze row fields (`corpus/SOURCES.md:257`): status `mined`, recheck `on-release`, used-by `corpus/knowledge/btrfs-scrub-grounding-r45.md`. `btrfs-scrub-record-r44.md:168` also names S248, as the appended pointer grounding QUALITY item 4 already records (`btrfs-scrub-grounding-r45.md:252`); that is not a stale used-by cell.

## Not done

Did not edit `SOURCES.md`. Did not query the git protocol (`ls-remote`); the tag-versus-branch claim is the GitHub tag/commit API plus the raw fetch. Did not re-run host `systemctl` reads.
