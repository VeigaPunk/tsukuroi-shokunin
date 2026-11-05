# ScoutSources — round 83 w1 — re-opened sources, located quotes

Seat role: scout (depth). Re-opened the three sources this round, located the
requested sentences, and recorded every fetch receipt. Nothing outside
`.ufo/waves/round-83/w1/ScoutSources.md` and
`.ufo/waves/round-83/w1/ScoutSources/sources.json` was written in the lane;
all fetches went to the scratch root
`/fast/scratch/hyaku/tsukuroi-r83/ScoutSources` (removed on exit).

Access date for every row below: **2026-11-05**.

## Status

All three sources re-opened successfully; every requested sentence located,
with URL, HTTP status, byte count, sha256 of the fetched bytes, section/page
and a verbatim quote of ≤25 words. Machine-readable copy:
`.ufo/waves/round-83/w1/ScoutSources/sources.json` (complete = true).

One deviation from the brief, recorded as a failure and worked around as the
brief instructs: the canonical NIST URL **does not serve the document**. It
answers HTTP 200 but returns the CSRC landing page (no "SHA-256", no
"256-bit" anywhere in it), and it links the PDF at nvlpubs — so the document
body was taken from that linked PDF, which is the URL the standard is actually
published under.

## Row table

| id | URL | access date | sha256 / status | quote (verbatim) | located lines |
|---|---|---|---|---|---|
| FIPS-180-4/SHA256-256BIT | https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf | 2026-11-05 | HTTP 200, 833315 bytes, `0455b406d89648d20cbde375561e19c245b9815e894164c2670772e3d54deb82` | "The final result of SHA-256 is a 256-bit message digest." | §6.2 SHA-256, printed p.21 (PDF page 26 of 36), page-text lines 33-34 |
| FIPS-180-4/SHA256-256BIT (2) | same | 2026-11-05 | same | "the resulting 256-bit message digest of the message, M, is" | §6.2.2 SHA-256 Hash Computation, step 5 — printed p.23 (PDF page 28), page-text line 31 |
| PY-SUBPROCESS/TIMEOUT | https://docs.python.org/3/library/subprocess.html | 2026-11-05 | HTTP 200, 208648 bytes, `ff3cca533d01e1b06eb5d3d541ef0e6e32b1d755fc9419afc287bfeddd33e503` | "will raise TimeoutExpired if the timeout expires before the process exits." | raw 971-972, § Exceptions |
| PY-SUBPROCESS/TIMEOUT (2) | same | 2026-11-05 | same | "All of the functions and methods that accept a timeout parameter, such as run() and Popen.communicate()" | raw 970-971, § Exceptions |
| PY-SUBPROCESS/TIMEOUT (3) | same | 2026-11-05 | same | "If the timeout expires, the child process will be killed and waited for." | raw 289-290, `subprocess.run()` |
| PY-SUBPROCESS/TIMEOUT (4) | same | 2026-11-05 | same | "The TimeoutExpired exception will be re-raised after the child process has terminated." | raw 290-291, `subprocess.run()` |
| PY-SUBPROCESS/TIMEOUT (5) | same | 2026-11-05 | same | "If the process does not terminate after timeout seconds, raise a TimeoutExpired exception." | raw 1013-1014, `Popen.wait(timeout)` |
| PY-SUBPROCESS/TIMEOUT (6) | same | 2026-11-05 | same | "If the process does not terminate after timeout seconds, a TimeoutExpired exception will be raised." | raw 1066-1067, `Popen.communicate()` |
| PY-SUBPROCESS/TIMEOUT (7) | same | 2026-11-05 | same | "The child process is not killed if the timeout expires" | raw 1071, `Popen.communicate()` |
| SYSTEMD-V262-MOUNT/RECHECK | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.mount.xml | 2026-11-05 | HTTP 200, 37234 bytes, `afbf3be663b139422b38217cd17083a96fa08507a1a3e58a844cbb2f67652394` — **equal to the pinned value** | "With nofail, this mount will be only wanted, not required, by local-fs.target or remote-fs.target." | raw 502-503 (expected 502-503) — **confirmed** |
| SYSTEMD-V262-MOUNT/RECHECK (2) | same | 2026-11-05 | same | "In the created mount unit, configures a Before= or After= dependency on another systemd unit, such as a mount unit." | raw 234-236 (expected 234-236) — **confirmed** |

## (1) NIST FIPS 180-4 — the canonical URL fails to serve the document

```
$ curl -sS -L -w '\n__STATUS__%{http_code} __URL__%{url_effective} __SIZE__%{size_download} __CT__%{content_type}\n' -o fips_canonical.bin 'https://csrc.nist.gov/pubs/fips/180-4/upd1/final'
__STATUS__200 __URL__https://csrc.nist.gov/pubs/fips/180-4/upd1/final __SIZE__40642 __CT__text/html; charset=utf-8
$ sha256sum fips_canonical.bin
70c1699f85be6c6d388415664e440fe20c5c266323771c87eee50fa426394ad1  fips_canonical.bin
```

Failure record: HTTP 200 but the body is the CSRC landing page, not the
standard. `grep -c "SHA-256" fips_canonical.bin` → **0**;
`grep -c "256-bit" fips_canonical.bin` → **0** (grep exit 1). The landing
page's own link to the document is the nvlpubs PDF, which it also exposes as
`https://doi.org/10.6028/NIST.FIPS.180-4`. Fallback used, as instructed:

```
$ curl -sS -L -w '...' -o fips180-4.pdf 'https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf'
__STATUS__200 __URL__https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf __SIZE__833315 __CT__application/pdf
$ sha256sum fips180-4.pdf
0455b406d89648d20cbde375561e19c245b9815e894164c2670772e3d54deb82  fips180-4.pdf
$ file fips180-4.pdf
fips180-4.pdf: PDF document, version 1.5, 36 page(s)
```

Response headers confirm an unchanging published artifact:
`last-modified: Tue, 04 Aug 2015 15:33:21 GMT`, `etag: "1a157e5caced01:0"`,
`content-length: 833315`.

### Located quotes (pdftotext -layout)

Primary (definition of the digest width), §6.2 SHA-256, printed page 21 =
PDF page 26:

```
6.2      SHA-256
SHA-256 may be used to hash a message, M, having a length of  bits, where 0   2 64 . The
algorithm uses 1) a message schedule of sixty-four 32-bit words, 2) eight working variables of 32
bits each, and 3) a hash value of eight 32-bit words. The final result of SHA-256 is a 256-bit
message digest.
```

> The final result of SHA-256 is a 256-bit message digest.

(10 words; raw page-text lines 33-34.)

Secondary (the digest as the algorithm's output), §6.2.2 SHA-256 Hash
Computation step 5, printed page 23 = PDF page 28:

```
After repeating steps one through four a total of N times (i.e., after processing M(N)), the resulting
256-bit message digest of the message, M, is

                               H 0( N ) H1( N ) H 2( N ) H 3( N ) H 4( N ) H 5( N ) H 6( N ) H 7( N )
```

> the resulting 256-bit message digest of the message, M, is

(10 words; raw page-text line 31.)

**Near miss, recorded so it is not mis-cited.** The string "The 256-bit message
digest is obtained by truncating the final hash value, H(N), to its left-most
256 bits" also appears in the PDF — printed page 26 = PDF page 31, §6.7
SHA-512/256. That is the SHA-512/256 truncation rule, **not** the SHA-256
digest-size statement; a row citing it for SHA-256 would cite the wrong
section.

## (2) Python 3 subprocess module — timeout semantics

```
$ curl -sS -L -w '...' -o subprocess.html 'https://docs.python.org/3/library/subprocess.html'
__STATUS__200 __URL__https://docs.python.org/3/library/subprocess.html __SIZE__208648 __CT__text/html
$ sha256sum subprocess.html
ff3cca533d01e1b06eb5d3d541ef0e6e32b1d755fc9419afc287bfeddd33e503  subprocess.html
```

Page title: `subprocess — Subprocess management — Python 3.15.2 documentation`.
The `/3/` URL is the **rolling** current-3.x document, so the byte count and
sha256 above are part of the locator, not decoration.

Line numbers below are the **raw HTML line numbers of the fetched file**
(line i = raw line i), with tags stripped and whitespace collapsed for
reading. Verbatim raw text, e.g. raw 288-291:

```
288| A timeout may be specified in seconds, it is internally passed on to
289| Popen.communicate() . If the timeout expires, the child process will be
290| killed and waited for. The TimeoutExpired exception will be
291| re-raised after the child process has terminated. The initial process
```

The raise-on-expiry rule, § Exceptions (raw 970-972):

```
970| All of the functions and methods that accept a timeout parameter, such as
971| run() and Popen.communicate() will raise TimeoutExpired if
972| the timeout expires before the process exits.
```

> will raise TimeoutExpired if the timeout expires before the process exits.
> All of the functions and methods that accept a timeout parameter, such as run() and Popen.communicate()

(11 and 16 words; raw 971-972 and raw 970-971.)

Child-process disposition — three different statements, and the difference
matters:

- `run()` (raw 289-290, 290-291):
  > If the timeout expires, the child process will be killed and waited for.
  > The TimeoutExpired exception will be re-raised after the child process has terminated.

- `Popen.wait(timeout)` (raw 1013-1014):
  > If the process does not terminate after timeout seconds, raise a TimeoutExpired exception.

- `Popen.communicate()` (raw 1066-1067, 1071):
  > If the process does not terminate after timeout seconds, a TimeoutExpired exception will be raised.
  > The child process is not killed if the timeout expires

### `call()` has no timeout prose — recorded as an absence

The `call()` entry (raw 1496-1522) documents the signature
(`timeout = None`, raw 1496), the passthrough sentence "The full function
signature is the same as that of the Popen constructor - this function passes
all supplied arguments other than timeout directly through to that interface"
(raw 1505-1507), and "Changed in version 3.3: timeout was added." (raw 1516).
It contains **no** sentence about TimeoutExpired and **no** sentence about
killing the child. `call()`'s timeout behaviour reaches it only through
`Popen.wait(timeout)` (raw 1013-1014). Any row claiming "call() kills the
child on timeout" would be sourced to the implementation, not to this page.

### Local corroboration (not a substitute for the doc)

On the host's CPython 3.14.8, `subprocess.run(...)` and
`subprocess.call(...)` with `timeout=1` over a 5-second child both raised
`subprocess.TimeoutExpired`, and in both cases the child did **not** survive to
run its post-timeout side effect (the probe's marker file was never created).
This agrees with the documented `run()` sentence and with the documented
`Popen.wait(timeout)` sentence that `call()` delegates to. Recorded as
corroboration only — the doc strings above are the sourced statements.

## (3) systemd.mount.xml v262 — re-fetch and line confirmation

```
$ curl -sS -L -w '...' -o systemd.mount.xml 'https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.mount.xml'
__STATUS__200 __URL__https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.mount.xml __SIZE__37234 __CT__text/plain; charset=utf-8
$ sha256sum systemd.mount.xml
afbf3be663b139422b38217cd17083a96fa08507a1a3e58a844cbb2f67652394  systemd.mount.xml
$ curl -sS -L -o systemd2.xml 'https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.mount.xml'
$ sha256sum systemd2.xml systemd.mount.xml && cmp systemd2.xml systemd.mount.xml
afbf3be663b139422b38217cd17083a96fa08507a1a3e58a844cbb2f67652394  systemd2.xml
afbf3be663b139422b38217cd17083a96fa08507a1a3e58a844cbb2f67652394  systemd.mount.xml
```

**Digest comparison: EQUAL.** The fetched sha256
`afbf3be663b139422b38217cd17083a96fa08507a1a3e58a844cbb2f67652394` equals the
pinned value exactly, and two independent fetches are byte-identical
(`cmp` exit 0). 37234 bytes, 707 raw lines.

Raw lines 502-503 (verbatim, markup included):

```
502|         <listitem><para>With <option>nofail</option>, this mount will be only wanted, not required, by
503|         local-fs.target</filename> or remote-fs.target</filename>. Moreover, the mount unit is not
```

Raw lines 234-236:

```
234|         <listitem><para>In the created mount unit, configures a
235|          <varname>Before=</varname> or <varname>After=</varname>
236|         dependency on another systemd unit, such as a mount unit.
```

Both sentences confirmed at the expected raw lines. Three independent
locating methods agree:

| Method | What it does | nofail | before/after |
|---|---|---|---|
| A | the lane counter's own `locate()` (token stream over the tag-stripped, line-preserving view), run over the freshly fetched upstream bytes | 502-503 | 234-236 |
| B | independent word-offset mapping: tags stripped, whitespace collapsed, char offset of the quote mapped back to its first and last word's raw line | 502-503 | 234-236 |
| C | direct containment check: does the cited span's normalised text contain the whole quote | yes | yes |

Both quotes occur exactly once in the file, so the located spans are
unambiguous; word counts are 14 and 20, both ≤25.

## Observations the L1 may want (no action taken, nothing re-scoped)

1. **The upstream file and the frozen fixture snapshot are not byte-identical,
   and the difference is a deliberate one-character edit.** The round-83
   fixtures' snapshot copy
   (`.ufo/waves/round-83/before/anchor-fixture-*/.ufo/waves/round-81/before/src/systemd.mount.xml`)
   hashes `c718576f…`, while upstream hashes `afbf3be6…`; `cmp` reports
   `differ: char 18, line 1` — the fixture's line 1 is
   `<?xml version='1.1'?>` and upstream's is `<?xml version='1.0'?>`. The two
   fixture copies are byte-identical to each other (`cmp` exit 0), and only
   their `corpus/knowledge/mount-unit-fstab-plane-r81.json` differs — in the
   declared `snapshot_sha256` field (digestfixed declares `c718576f…`,
   doctored declares `afbf3be6…`). The upstream file is the one whose bytes
   match the lane's own `corpus/knowledge/mount-unit-fstab-plane-r81.json`
   (`snapshot_sha256: afbf3be6…`) and the lane's own
   `.ufo/waves/round-81/before/src/systemd.mount.xml`
   (`sha256 afbf3be6…`, verified). This is exactly the shape the C1
   digest-conjunction needs: the digest fixed in the fixture is the digest of
   the fixture's own (edited) bytes. No defect; recorded so the L1 can see
   the fixture's provenance is understood.
2. **The fixture's quoted line numbers are unaffected by that edit.** The edit
   is on line 1 only; the two quotes still locate at 502-503 and 234-236 in
   the fixture bytes (re-checked with the counter's own `locate()` over the
   fixture file: 502-503 and 234-236), and the counter returns met 8/8 on
   `anchor-fixture-digestfixed` (rc 0) and cannot-evaluate on
   `anchor-fixture-doctored` (rc 2, `snapshot-digest-mismatch:declared-afbf3be663b1:actual-c718576fcce8`).
   The real tree at the declaration commit
   `d78b3b3982b5df62286dd65b0a42ae8a91847608` returns met 8/8 (rc 0).
3. **Adjacent coverage, not a collision.** `S180` already covers CPython
   3.14.8 subprocess documentation (raw `Doc/library/subprocess.rst`) for the
   `Popen` `env` parameter. A new row for the subprocess timeout semantics is
   a different URL and a different scope, so it is adjacent coverage; the
   census W04 "same URL across scopes" warning does not apply.
4. **Registry id space.** The lane registry's highest id is `S333`
   (`corpus/SOURCES.md`, 11 cells per row). The next two free ids are
   therefore `S334` and `S335`. The external staged registry
   `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md` already
   uses `S334`–`S343` for unrelated documents — the same cross-namespace
   collision recorded for `S329` in round 79. The L1/connector decides; the
   scout's row drafts use `S334`/`S335` as the brief names them.
5. **`used_by` for the new rows.** The brief's suggested path
   `corpus/lessons/round-83.md` does not exist in the lane today
   (`ls` → "No such file or directory"); it is created by the L1 after
   WAVE-DONE. The census E11 check requires the used-by path to exist on
   disk, so the row is only valid once that file lands — the row draft
   records the intended path, and the L1 should land the lessons file and the
   rows together.

## Limits of this seat

- Source re-opening and quote location only. I did not run the battery, did
  not score C1 or C2, and did not judge the instruments; the two counter runs
  above are cited only as evidence that the located raw lines are the ones the
  frozen instrument reads.
- The Python doc lines are raw HTML lines of the fetched file. The rendered
  page's line numbering differs; a reader checking on docs.python.org should
  use the anchor (section + function name) and the recorded sha256.
- `docs.python.org/3/` is a rolling URL: the same address will serve a
  different 3.x document later. The recorded byte count and sha256 are what
  make the 2026-11-05 fetch reproducible.
- I did not open any URL other than the four named above (the canonical NIST
  URL, its instructed nvlpubs fallback, the Python docs page, and the systemd
  raw file), wrote no credential or session material, and did not touch the
  lane index, bookmarks, worktree state, `MANIFEST.json`, `SCORECARD.md`,
  `corpus/SOURCES.md`, `.ufo/state/` or any sibling lane.

## Tooling

No tool was installed or upgraded. Commands used: `curl -sS -L` (four named
URLs only), `sha256sum`, `cmp`, `file`, `pdftotext` (poppler, already
present at `/usr/bin/pdftotext`), `grep`, `awk`, `python3` (read-only
parsing), `git show`/`git rev-parse`/`git status`/`jj status` (read-only).
Scratch lived in `/fast/scratch/hyaku/tsukuroi-r83/ScoutSources` and was
removed on exit.
