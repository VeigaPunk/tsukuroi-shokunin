VERDICT: defect-found

Item C2-B6. Live re-open of the page S256 pins, against `corpus/SOURCES.md` at freeze `8029cdba1049df25632c91a23c8db4eefb54be5f`. No tools installed. POSIX was not fetched. The C2 counter was not run.

## (a) Live page

Command (2026-10-28), body saved then copied to the receipt dir:

`curl -fsSL -A R50ScoutGrepSource/1.0 -o grep.1.html -w 'http_code=%{http_code} size_download=%{size_download} ...' https://man7.org/linux/man-pages/man1/grep.1.html`

Observed: `http_code=200 size_download=43199 url_effective=https://man7.org/linux/man-pages/man1/grep.1.html content_type=text/html`. `wc -c` = 43199. `sha256sum` = `d6f07a7f75c6275f6986df2501d355ebd22fa1475ce50dc6039f1fb028d6a3c2`. That is the hash in the S256 `anchor` cell (`corpus/SOURCES.md:265` at the freeze).

A second request the same day (`curl -D headers.txt -o /dev/null`, body not re-hashed): `HTTP/1.1 200 OK`, `Date: Wed, 28 Oct 2026 19:04:05 GMT`, `Last-Modified: Wed, 28 Oct 2026 18:28:41 GMT`, `ETag: "a8bf-65eeabb7aa840"`, `Content-Length: 43199`, `Content-Type: text/html`, `size_download=43199`. `0xa8bf` = 43199. The hashed body is the pin; this seat did not hash the second body.

Receipts: `.ufo/waves/round-50/w1/R50ScoutGrepSource/grep.1.html` (43199 bytes, same sha256), `headers.txt`, `paragraphs.txt`. Page colophon, receipt lines 700-702 and 711: obtained from the GNU grep git repository on 2026-08-04; footer `GNU grep 3.12.39-8017d-modified 2025-03-21`.

`-q` paragraph (raw HTML lines 201-205):

```
201:       <b>-q</b>, <b>--quiet</b>, <b>--silent</b>
202:              Quiet; do not write anything to standard output.  Exit
203:              immediately with zero status if any match is found, even if
204:              an error was detected.  Also see the <b>-s </b>or <b>--no-messages</b>
205:              option.
```

EXIT STATUS (raw HTML lines 482-487). The heading is line 482; the paragraph is 483-486; line 487 is `</pre>`.

```
482:<h2><a id="EXIT_STATUS" href="#EXIT_STATUS"></a>EXIT STATUS  ...</h2><pre>
483:       Normally the exit status is 0 if a line is selected, 1 if no lines
484:       were selected, and 2 if an error occurred.  However, if the <b>-q </b>or
485:       <b>--quiet </b>or <b>--silent </b>is used and a line is selected, the exit
486:       status is 0 even if an error occurred.
487:</pre>
```

Case-insensitive counts on the 43199-byte body: `sigpipe` 0, `epipe` 0, `pipeline` 0, `writer` 0, `pipefail` 0, `broken pipe` 0. The one `upstream` hit is the colophon, line 701: "obtained from the project's upstream Git repository". In the anchored spans 201-205 and 482-487: `immediately` 1, `selected` 3, `first` 0, `SIGPIPE` 0, `pipeline` 0.

## (b) Row S256 at the freeze

`git show 8029cdba1049df25632c91a23c8db4eefb54be5f:corpus/SOURCES.md` line 265. Header is line 5: `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.

| cell | supported by the page? |
|---|---|
| `anchor` | Yes. sha256 equals the live body. Lines 201-205 are the `-q` block. Lines 483-486 are the EXIT STATUS paragraph; 487 is the closing `</pre>` (the heading sits on 482, outside the cited range). The cell's fetch stamp is the truncated token `2026-10-28T` (date only). |
| `teaches` | Yes. "Exit immediately with zero status if any match is found, even if an error was detected" is lines 202-204 joined. The page has a period after `detected`; the cell stops at `detected` before the table delimiter. The sentence uses `detected` (the `-q` paragraph), while EXIT STATUS line 486 says `occurred`. |
| `scope` | The early-exit half is a paraphrase of lines 202-204 plus 483-486. `immediately` and `any match` are on 203; `a line is selected` is on 483 and 485. The word `first` is not in either span. The clause "which makes an upstream writer in a pipeline die of SIGPIPE and the pipeline read false" is not on the page. |

That SIGPIPE clause is an inference from POSIX pipe semantics (a reader that exits closes the pipe; the writer can then die with SIGPIPE, and `pipefail` can make the pipeline status that death). It is not a statement of this page. This seat did not re-fetch a POSIX page, so no POSIX line number is claimed.

Exact place the row should say so: the `scope` cell of `corpus/SOURCES.md:265`, the relative clause that now begins `which makes an upstream writer`. The `teaches` cell is already only the page sentence and should stay that way. The `anchor` line ranges should not be read as covering the SIGPIPE clause.

Proposed `scope` cell:

`grep -q`, `--quiet`, `--silent` exit status: the page states an immediate exit with zero status if any match is found, even if an error was detected (raw HTML 202-204); EXIT STATUS states that with `-q` the status is 0 when a line is selected even if an error occurred (483-486). "First selected line" is a paraphrase (`immediately` / `any match` on 203; `selected` on 483 and 485; `first` is absent from both spans). [inference from POSIX pipe semantics, not a statement of this page] that early exit can make an upstream writer in a pipeline die of SIGPIPE and the pipeline read false.

## (c) `used-by`

The cell `corpus/lessons/round-50.md` is the right citation target. Freeze record `.ufo/waves/round-50/frozen/FROZEN.md:22` names C2 as "sourced: S256 opened this round". The registry's `used-by` column points at lesson and knowledge files (header `corpus/SOURCES.md:5`; the preceding row S255 at line 264 points at `corpus/lessons/round-48.md, corpus/lessons/round-49.md`).

The path does not resolve in the bytes under test. `git cat-file -e 8029cdba1049df25632c91a23c8db4eefb54be5f:corpus/lessons/round-50.md` exits 128 (`exists on disk, but not in '8029cdba...'`). The same exit 128 against `HEAD` (`39e694934cf6c56434987edc730e8b3580a251f3`). `git ls-tree --name-only 8029cdba:corpus/lessons/` ends at `round-49.md`. `git status --porcelain -- corpus/lessons/round-50.md` prints `?? corpus/lessons/round-50.md`.

The untracked working-tree draft (not a frozen byte; read only because `used-by` names it) does cite this row: `corpus/lessons/round-50.md:11` is the Gate row "S256 (new)", status `absent -> mined`, note "tier A docs; teaches the `-q` early exit that makes an upstream writer in a pipeline die of SIGPIPE. Claim C2 rests on it." That note repeats the unmarked inference. If it lands, the same `[inference from POSIX pipe semantics, not a statement of this page]` mark belongs on that note, not only on the `scope` cell.

## Not done

No POSIX fetch, no census `--selftest`, no C2 counter. Scratch `/fast/scratch/hyaku/tsukuroi-r50/R50ScoutGrepSource/` was removed after the receipts were copied.
