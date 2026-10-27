VERDICT: supports

# Item C2-6 — S252 re-open: mktemp(1) freshness, located quote, space-TMPDIR empirics

Seat: C2ScoutMktemp (tsukuroi lane, round 47, wave w1). Item: re-open source S252
(man7.org linux man-pages, mktemp.1.html) live, compare against the round-47 frozen
snapshot, confirm the located quote, and empirically verify mktemp's handling of a
space-containing TMPDIR, read-only on the host.

## 1. Live re-fetch vs frozen snapshot — FRESH, byte-identical

- Frozen snapshot: .ufo/waves/round-47/frozen/src/mktemp.html (declared S252), 9832 bytes.
- Frozen digest record: .ufo/waves/round-47/frozen/src/SHA256SUMS
  (`74186433c4e851311ded2cc0f8b14acab913d1c9ba1a2ef9a436548a9c073266  mktemp.html`);
  FETCH.txt records the L1's fetch "2026-10-27 (round 47 start)", same sha256, 9832 bytes.
- Live fetch (this seat, 2026-10-27T08:55:31Z):
  `curl -fsSL --max-time 30 https://man7.org/linux/man-pages/man1/mktemp.1.html -o mktemp-live.html`
  → rc 0, 9832 bytes, sha256 `74186433c4e851311ded2cc0f8b14acab913d1c9ba1a2ef9a436548a9c073266`.
- `cmp mktemp-live.html .ufo/waves/round-47/frozen/src/mktemp.html` → rc 0, no output (byte-identical).
- Digest check against SHA256SUMS:
  `sha256sum -c SHA256SUMS` semantics — the live file's digest equals the recorded one.

Finding: S252 is unchanged between the L1's round-start capture and this re-open; the frozen
snapshot is byte-current with man7.org as of 2026-10-27T08:55Z.

## 2. Located quote — PRESENT on the live page

Stripped-text transformation: `sed -e 's/<[^>]*>//g' mktemp-live.html | tr -s ' \t\n' ' '`
(receipt: C2ScoutMktemp/mktemp-stripped.txt). Located quote (option `-t` description):

  "-t interpret TEMPLATE as a single file name component, relative to a directory: $TMPDIR,
  if set; else the directory specified via -p; else /tmp [deprecated]"

grep on the stripped text for
"interpret TEMPLATE as a single file name component, relative to a directory: \$TMPDIR, if set"
→ exact match found (rc 0). The claim's located quote is verbatim present, including the
"$TMPDIR, if set" clause and the documented -p / /tmp precedence chain after it.

## 3. Empirical verification (read-only; all writes only inside this seat's scratch)

Implementation note: this agent shell provides an mktemp builtin ("mktemp 0.8.0"); the census
selftest runs under `env -i PATH=/usr/bin:/bin bash` and therefore resolves /usr/bin/mktemp,
owned by coreutils 9.12-2 (verified: `pacman -Qo /usr/bin/mktemp`). Both implementations were
exercised where they differ.

(a) TMPDIR = nonexistent directory containing a space, relative template, -t:
    `env TMPDIR='/fast/scratch/hyaku/tsukuroi-r47/C2ScoutMktemp/no such dir' /usr/bin/mktemp -d -t 'x.XXXX'`
    → rc 1, stderr: "mktemp: failed to create directory via template
    '/fast/scratch/hyaku/tsukuroi-r47/C2ScoutMktemp/no such dir/x.XXXX': No such file or directory".
    No silent fallback to /tmp or cwd; a nonexistent space TMPDIR fails closed.
    (The item's first command omits -t: without -t a relative template is cwd-relative by
    design and TMPDIR is not consulted at all — confirmed: `mktemp -d 'x.XXXX'` created
    ./x.9QgJ in cwd, rc 0, TMPDIR ignored. That is spec-correct, not a fallback.)

(b) TMPDIR = existing directory containing a space, -t:
    `env TMPDIR='/fast/scratch/hyaku/tsukuroi-r47/C2ScoutMktemp/sp dir' /usr/bin/mktemp -d -t 't.XXXXXX'`
    → rc 0, output "/fast/scratch/hyaku/tsukuroi-r47/C2ScoutMktemp/sp dir/t.2MUZTH";
    `ls -ld` confirms the directory was created inside the space-containing TMPDIR with
    mode 700. coreutils mktemp HONORS a space-containing TMPDIR.
    Same command against the shell builtin mktemp 0.8.0 → rc 0, created
    ".../sp dir/b.L6JB9p": the builtin also honors it.

(c) Item's literal second form — absolute template with space TMPDIR set:
    `env TMPDIR='.../sp dir' mktemp -d '/fast/scratch/.../abs.XXXXXX'`
    → rc 0, created ".../abs.b2ZEtF". With an absolute template TMPDIR is not consulted
    (template already names a directory); behavior is TMPDIR-independent, as the man page
    implies ("TEMPLATE may contain slashes, but mktemp creates only the final component").

(d) Control: `env -u TMPDIR /usr/bin/mktemp -d -t 'u.XXXX'` → rc 0, created /tmp/u.sH2e:
    unset TMPDIR falls back to /tmp, matching the quote's "else /tmp" tail.

Answer to the item's question — does mktemp honor a space TMPDIR? YES: with -t (or --tmpdir),
coreutils 9.12 mktemp treats TMPDIR as a single directory path even when it contains spaces
(no field-splitting), creating the final template component inside it and printing the
absolute path; a nonexistent space TMPDIR fails closed with ENOENT (rc 1), no fallback.

## 4. Harness binding for the C2 amendment (context)

tools/tsukuroi-census.sh run_selftest (lines 2049-2059):
  local st_base=${TMPDIR:-/tmp}
  case "$st_base" in
    *[!A-Za-z0-9._/+-]*) st_base=/tmp ;;
  esac
  work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")
The harness call passes an ABSOLUTE template ($st_base/...), so its mktemp call never itself
depends on TMPDIR semantics; the root_locator_class charset filter (space → /tmp fallback) is
what keeps a dirty space-containing TMPDIR from poisoning fixture paths, and mktemp then
creates safely under the classified base. Section-3 empirics ground the underlying mktemp(1)
semantics the design leans on (TMPDIR honored as one path; ENOENT on a bad TMPDIR) and refute
any worry that a space in TMPDIR would be word-split or silently redirected.

## 5. Receipts (seat dir .ufo/waves/round-47/w1/C2ScoutMktemp/)

- mktemp-live.html — the live 2026-10-27T08:55:31Z fetch (9832 bytes, sha256 74186433...266).
- mktemp-stripped.txt — HTML-stripped text in which the quote was located.
- evidence.log — command/observed-output transcript of every probe in sections 1 and 3.

## 6. Not done / limits

- No mutation of any host or lane state: every mktemp probe wrote only inside this seat's
  scratch tree on /fast; all probe directories were removed.
- The two harness-kill-rule suites (census selftest under space TMPDIR; identity counter)
  are run by other seats per the wave plan; this seat re-opens the S252 source only.
