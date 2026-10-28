VERDICT: supports

# R49ScoutBashRedir — Bash manual Redirections, live re-open

Opener of record for the existing row S255. Bytes under test: freeze `55c07cd3f8bff2e12117c34d57b4c618de74d85c` `corpus/SOURCES.md:264`. No new id. Receipts: `.ufo/waves/round-49/w1/R49ScoutBashRedir/`. No tools installed. SOURCES.md was not edited.

## 1. Fetch

- URL (the S255 source cell): `https://www.gnu.org/software/bash/manual/bash.html`
- Redirects: none. `curl -fsSL --max-time 60 -D headers.txt -o bash.html -w 'http=%{http_code} redir=%{num_redirects} url_effective=%{url_effective} size=%{size_download}'` printed `http=200 redir=0 url_effective=https://www.gnu.org/software/bash/manual/bash.html size=1040954` (`curl-meta.txt`). One response block: `HTTP/1.1 200 OK`, `Content-Type: text/html`, `Content-Length: 1040954`, no `Location` (`headers-key.txt`).
- Access date: 2026-10-28. `date -u +%FT%TZ` printed `2026-10-28T17:26:56Z` (`access-time.txt`). Response `Date: Wed, 28 Oct 2026 17:27:04 GMT`.
- sha256 of the fetched bytes: `78d0eefbe60cfe7345ffdafede7294f055b04e53bd520360ff699b24f81e2b4b` (`sha256-live.txt`). `sha256sum -c` against that pin printed `bash.html: OK` (`sha256-check.txt`). 1,040,954 bytes, 17,853 lines (`wc.txt`).
- Byte equality: `cmp -s` against the round-48 receipt `.ufo/waves/round-48/w2/SScoutBashRedir/bash-manual-2026-10-28.html` printed `CMP_IDENTICAL` (`cmp.txt`). That receipt's sha256 is the same digest (`sha256-prior-receipt.txt`).
- The page did not move. This URL is the unversioned current-edition manual, not a git tag and not a branch. Edition lines are unchanged: line 9 and line 84 both read `This is Edition 5.3, last updated 18 May 2025,` (`edition-hits.txt`). Title line 21: `Bash Reference Manual`.

## 2. Anchors

Quotes are the rendered words (tags and `&lt;`/`&gt;` decoded). Each is at most 25 words (`anchors.tsv`). Raw line 3884 is `[<var class="var">n</var>]&lt;<var class="var">word</var>`, so a literal grep for `[n]<word` does not hit it.

- Explicit `[n]<word`, lines 3877-3880 (19 words): `Redirecting input opens the file whose name results from the expansion of word for reading on file descriptor n`. Grammar token, line 3884: `[n]<word`.
- `{varname}` allocation, lines 3772-3773 (17 words): `the shell allocates a file descriptor greater than or equal to 10 and assigns it to {varname}.`
- `{varname}` close (the form the selftest uses), lines 3774-3778 (16 words): `If {varname} precedes >&- or <&-, the value of varname defines the file descriptor to close.`
- Descriptors greater than 9, lines 3859-3861 (23 words): `Redirections using file descriptors greater than 9 should be used with care, as they may conflict with file descriptors the shell uses internally.`

Same pinned page, not in the admitted line list: line 3758-3759 (16 words) `When used with the exec builtin, redirections modify file handles in the current shell execution environment.` and lines 4863-4864 (15 words) `If command is not specified, redirections may be used to affect the current shell environment.`

Freeze census uses those sentences, not a second manual. `tools/tsukuroi-census.sh` at `55c07cd3f8bff2e12117c34d57b4c618de74d85c`: `eval "exec ${fdn}<\"\$base\""` at line 2092; `exec {r48_fd}<&-` at 3567 and `exec {ST_BASE_FD}<&-` at 3569; the R49-C3 hold/close is numeric `exec 240<&0` / `exec 241<&0` at 3581 and `exec 240<&-` / `exec 241<&-` at 3596-3597. The band comment at 2069-2075 chooses 240-249 because `{varname}` allocation starts at 10. The named diagnostic `fd band %s exhausted` at 2115 is census text; the manual does not say it.

## 3. Cadence and pins

The `on-release` recheck and the edition/sha256 pin still read right, because today's unversioned page is still Edition 5.3 (18 May 2025) and byte-identical to `78d0eefbe60cfe7345ffdafede7294f055b04e53bd520360ff699b24f81e2b4b`, lines 3771-3778 and 3859-3861 still hold the `{varname}` and fd>9 text, and 3881-3884 still holds the `[n]<word` grammar at line 3884 while the sentence that defines descriptor n is lines 3877-3880, immediately above that span.

## 4. Proposed status / recheck / used-by

`used-by` `corpus/lessons/round-48.md` → `corpus/lessons/round-48.md, corpus/lessons/round-49.md`

status `mined`: no change. recheck `on-release`: no change.

S255 already covers every bash proposition C3 needs (explicit `[n]<word`, `{varname}` allocation and close, and the fd>9 caveat). Those three are the scope cell at freeze `corpus/SOURCES.md:264`, and `git grep` of that URL in the freeze registry hits only that line (`sources-url-hits.txt`). Do not assign a new id. The diagnostic string, the stale-comment leg, and the 167-case count are census behaviour, not a second manual.

Proposed row (id stays S255; only `used-by` changes):

```
| S255 | GNU Bash Reference Manual 5.3, Redirections — https://www.gnu.org/software/bash/manual/bash.html | docs | A | Explicit fd numbers in redirections, `{varname}` descriptor allocation, and the fd>9 caveat behind the census selftest's 240-249 fd-alias band | Edition 5.3 (18 May 2025); fetched 2026-10-28, sha256 78d0eefbe60cfe7345ffdafede7294f055b04e53bd520360ff699b24f81e2b4b; raw HTML lines 3881-3884, 3771-3778, 3859-3861 | Redirections using file descriptors greater than 9 should be used with care, as they may conflict with file descriptors the shell uses internally | mined | 2026-10-28 | on-release | corpus/lessons/round-48.md, corpus/lessons/round-49.md |
```

Observation, not the bytes under test: the working tree `corpus/SOURCES.md` already differs from the freeze by exactly that one `used-by` cell (`sources-wt.diff`, `git diff --stat` = 1 file, 1 insertion, 1 deletion). This seat did not write it. Apply once.

## Not done

Did not run the census selftest or `check-fd-band-r49.py`. Did not edit `SOURCES.md`. Did not widen the anchor line list to 3877-3880 or 3758-3759/4863-4864; the digest already pins those lines.
