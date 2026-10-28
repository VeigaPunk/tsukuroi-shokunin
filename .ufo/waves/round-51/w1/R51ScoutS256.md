VERDICT: supports

S256 re-opened live against freeze `2732ee6c06108c031c4d8043239b994e0504eb2f` `corpus/SOURCES.md:265` (read with `git show`, not the working tree). The row's pin still matches the live page, and raw lines 201-205 and 483-487 are the `-q`/`--quiet` block and the EXIT STATUS body the row cites. No tools installed.

## S256 — GNU grep(1)

Command (cwd `/fast/scratch/hyaku/tsukuroi-r51/R51ScoutS256`):

```
date -u +%Y-%m-%dT%H:%M:%SZ
curl -sSfL --max-time 120 -D grep.headers -o grep.html -w 'http_code=%{http_code} size_download=%{size_download} time_total=%{time_total}\n' https://man7.org/linux/man-pages/man1/grep.1.html
wc -c grep.html
sha256sum grep.html
echo 'd6f07a7f75c6275f6986df2501d355ebd22fa1475ce50dc6039f1fb028d6a3c2  grep.html' | sha256sum -c -
```

Observed 2026-10-28:

```
2026-10-28T21:13:59Z
http_code=200 size_download=43199 time_total=1.005592
2026-10-28T21:14:00Z
43199 grep.html
d6f07a7f75c6275f6986df2501d355ebd22fa1475ce50dc6039f1fb028d6a3c2  grep.html
grep.html: OK
```

Access time 2026-10-28T21:13:59Z (local clock before the transfer; response `Date: Wed, 28 Oct 2026 21:13:59 GMT`). Byte size 43199 (`Content-Length: 43199`; 812 lines). sha256 `d6f07a7f75c6275f6986df2501d355ebd22fa1475ce50dc6039f1fb028d6a3c2`. Byte-identical to the row pin. Response `Last-Modified: Wed, 28 Oct 2026 18:28:41 GMT` is the same calendar day; the digest still matches, so that header is not a content change.

Receipt: `.ufo/waves/round-51/w1/R51ScoutS256/grep.html` (same sha256).

`-q` / `--quiet` paragraph, raw lines 201-205. Quote from lines 202-204 (24 words, visible text, double space kept): "Quiet; do not write anything to standard output.  Exit immediately with zero status if any match is found, even if an error was detected." Lines 204-205 continue "Also see the -s or --no-messages option." The freeze row's teaches cell is the second of those two sentences and is a verbatim substring of lines 202-204.

EXIT STATUS paragraph, raw lines 483-487 (heading is line 482; line 487 is `</pre>`). Quote from lines 483-484 (23 words): "Normally the exit status is 0 if a line is selected, 1 if no lines were selected, and 2 if an error occurred." Lines 484-486 (25 words): "However, if the -q or --quiet or --silent is used and a line is selected, the exit status is 0 even if an error occurred."

The page says `-q`, `--quiet`, and `--silent` write nothing and exit immediately with status 0 once any match is found, even if an error was detected (lines 201-205), and that the exit status is otherwise 0, 1, or 2 as quoted above, with that same zero status when a line is selected under `-q`, `--quiet`, or `--silent` (lines 483-486). A search of these 43199 bytes found no `SIGPIPE`, `pipefail`, `PIPESTATUS`, or `set -o`, so the page does not state a SIGPIPE death or a `set -o pipefail` pipeline status; those remain shell consequences, which is what freeze `corpus/SOURCES.md:265` already scopes.

## Bash Pipelines — candidate S257

Command:

```
date -u +%Y-%m-%dT%H:%M:%SZ
curl -sSfL --max-time 120 -D pipelines.headers -o pipelines.html -w 'http_code=%{http_code} size_download=%{size_download} time_total=%{time_total}\n' https://www.gnu.org/software/bash/manual/html_node/Pipelines.html
wc -c pipelines.html
sha256sum pipelines.html
```

Observed:

```
2026-10-28T21:14:10Z
http_code=200 size_download=7513 time_total=0.389876
2026-10-28T21:14:10Z
7513 pipelines.html
b5629f04ccf5fe711d1b30f5dd4d8cf67dc6ab836d413292cd15c870a662059a  pipelines.html
```

Access date 2026-10-28 (2026-10-28T21:14:10Z; response `Date: Wed, 28 Oct 2026 21:14:10 GMT`). Byte size 7513. sha256 `b5629f04ccf5fe711d1b30f5dd4d8cf67dc6ab836d413292cd15c870a662059a`. Edition line in the file header, raw lines 7-11: Bash 5.3, Edition 5.3, last updated 18 May 2025. Receipt: `.ufo/waves/round-51/w1/R51ScoutS256/pipelines.html`.

Located quote, raw lines 124-125 (19 words, visible text; the lines join on a newline): "value of the last (rightmost) command to exit with a non-zero status, or zero if all commands exit successfully." Line 123 is the clause that applies it: `If <code class="code">pipefail</code> is enabled, the pipeline&rsquo;s return status is the`. The apostrophe is the entity `&rsquo;`, not ASCII `'`. Lines 119-122 state the other rule: without the option, the pipeline status is the last command's status, and they link `The-Set-Builtin.html`. This node never spells `set -o pipefail`.

Yes. This is a candidate new tier-A docs row for the claim that under pipefail a pipeline's status is the last non-zero status. The page is the GNU Bash Reference Manual (same edition already accepted as S255, which is the Redirections node of `bash.html`, a different URL and a different pin). Freeze `corpus/SOURCES.md` has no `Pipelines.html` row (`git grep -F Pipelines.html 2732ee6c -- corpus/SOURCES.md` found none). The row below keeps the page's two qualifications: "last" means rightmost, and the status is zero when every command exits successfully. `corpus/lessons/round-51.md` is the prescribed `used-by` and is absent from that freeze commit.

Proposed 11-column row (no literal `|` inside a cell):

```
| S257 | GNU Bash Reference Manual 5.3, Pipelines — https://www.gnu.org/software/bash/manual/html_node/Pipelines.html | docs | A | Under the pipefail option, the return status of a pipeline is the exit status of the last (rightmost) command to exit non-zero, or zero if every command exits successfully | Edition 5.3 (18 May 2025); fetched 2026-10-28 (sha256 b5629f04ccf5fe711d1b30f5dd4d8cf67dc6ab836d413292cd15c870a662059a); raw HTML lines 123-125 | If pipefail is enabled, the pipeline's return status is the value of the last (rightmost) command to exit with a non-zero status, or zero if all commands exit successfully | mined | 2026-10-28 | on-release | corpus/lessons/round-51.md |
```

The teaches cell is the visible sentence. A byte search of the HTML must allow `<code class="code">pipefail</code>`, the `&rsquo;` in `pipeline&rsquo;s`, and the newlines at lines 123-125. Line 124 and line 125 are each contiguous ASCII.

Not run: `score-counter-cheats-r51.py` and any census `--selftest`. This item does not name them.
