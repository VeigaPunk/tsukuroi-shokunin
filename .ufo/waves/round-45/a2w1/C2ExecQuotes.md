VERDICT: defect-found

# C2-7 — mechanical quote check of `corpus/knowledge/btrfs-scrub-grounding-r45.md`

Seat C2ExecQuotes (wave a2w1, round 45). Item: check every `**Quote.**` line of the entry at
`18389f44cf6ce414d7be205998b29c79fb0b490c` against the named snapshot line (digests first), judge whether any
quote is a fragment that changes meaning, and re-check every line-number / function-name / value claim inside the
three Statement cells. Own script (`quotecheck.py`, below), not `tools/check-scrub-grounding-r45.py`.

Entry read at the revision through `git show 18389f4:corpus/knowledge/btrfs-scrub-grounding-r45.md`
(sha256 `129b351bdb8c954aa91850b24dbdb0ce184ce00a39997dd81fae962a9b5335f6`, identical to the working-tree file),
11 220 bytes.

## Result

| check | result |
|---|---|
| snapshot digests (`SHA256SUMS` in round-45/44/42 `frozen/src`, 12 files) | 12/12 OK |
| every file a quote names is listed in its source's `SHA256SUMS` | 9/9 |
| `S249` `capture.txt` digest | OK (`f5958a83…31e70`) |
| `**Quote.**` lines found and parsed | 31 |
| quote text found on the named line | **31/31** — 30 exact line match, 1 line-slice (`cmdline.c:147`, the quote drops the comment's leading `*`) |
| **wrong pointers** | **none** |
| quoted lines inside the line ranges `corpus/SOURCES.md` declares for that source | 29/31 (see F1, F2) |
| Statement-cell line-number / function-name / value checks | 44/44 pass (GR1 21, GR2 9, GR3 14) |
| Statement "Host reading" values vs `capture.txt` | 7/7 |

`python3 quotecheck.py --lane <lane> --revision 18389f4…` → **134 PASS, 2 FAIL**, exit 1. Both failures are
source-registration mismatches in `corpus/SOURCES.md`, not misquoted text: nothing falsifies a GR statement, and
every quoted sentence is present verbatim where the entry says it is.

## Findings

**F1 — `S242 scrub.c:3081` lies outside the ranges `SOURCES.md` declares for S242.**
`corpus/SOURCES.md:251` (at 18389f4) declares `fs/btrfs/scrub.c lines 1365-1385, 3140-3162, 3215-3226, 3321-3337`.
The quote at `btrfs-scrub-grounding-r45.md:80` (`bool readonly, bool is_dev_replace)`) is line 3081 — 59 lines above
the first declared range. The file digest still covers the whole snapshot, so the text is verifiable; the
registration is not. Fix: add `3079-3081` (or widen to `3040-3162`) to the S242 range list.

**F2 — `S237 scrub.c:421` (and the two lines GR3 needs, 439 and 1546) lie outside S237's declared ranges.**
`corpus/SOURCES.md:246` declares `cmds/scrub.c lines 67-70, 280-330, 446-535, 826-895, 1110-1125, 1186-1220,
1330-1340, 1498-1512, 1925-1945`. The quote at `btrfs-scrub-grounding-r45.md:122` is line 421, inside the 331-445
gap; `scrub_sigint_record_progress` is defined at 417 and the handler is installed from 436-444
(line 439 `fd == -1 ? SIG_DFL : scrub_sigint_record_progress`) and at 1546 — also outside. Fix: add `412-444` and
`1512-1550`.

**F3 — the one quote that is a meaning-withholding fragment: `systemd.kill.xml:114`.**
`btrfs-scrub-grounding-r45.md:120` quotes `"<para>Note that, right after sending the signal specified in this
setting, systemd will always send"` — the sentence's object, the decisive token, is on the next line:
`systemd.kill.xml:115` = `<constant>SIGCONT</constant>, to ensure that even suspended tasks can be terminated
cleanly.</para>`. GR3 asserts "Right after that signal systemd sends SIGCONT"; a reader checking the quoted text
alone sees "systemd will always send" and nothing more, so the quote cannot confirm SIGCONT. Line 115 is inside
S248's declared range (62-116), so the pointer is available: change `114` to `114-115` or add the 115 quote.

**F4 — GR2's "any call" half is decided by an unquoted line.**
The Statement says "any call is refused with `-EINPROGRESS` while the device already carries a scrub context"; that
is `scrub.c:3147` `if (dev->scrub_ctx ||` (the first disjunct, not guarded by `is_dev_replace`), which is quoted
nowhere — the S242 quotes at md:82-86 start at 3148. 3147 is inside S242's declared range; only the quote is
missing.

**F5 — GR2's subject "the scrub-start ioctl … returns `EINPROGRESS`" is one frame beyond the pinned code.**
`S242` is `fs/btrfs/scrub.c` only: `grep -n "BTRFS_IOC_SCRUB\|scrub_ioctl" scrub.c` in
`.ufo/waves/round-44/frozen/src/scrub.c` returns **no hits**, and no cited snapshot holds `fs/btrfs/ioctl.c`. So the
hop ioctl → `btrfs_scrub_dev(…, is_dev_replace=false)` is not pinned, yet the sentence reads as pinned; the entry
marks only the btrfs-progs printing as `[inference]`. Not a falsification — it is a mechanism step outside the
citation set. Either pin `ioctl.c` (a new source row) or bound the sentence to `btrfs_scrub_dev`.

**F6 — GR1's two multiplier claims have no quote.**
"`memparse` takes at most one suffix letter" is decided by the single `switch (*endptr)` at `cmdline.c:160` and the
one `endptr++` at `cmdline.c:193`; "each step multiplying by a further 1024 (a 10-bit shift per step, so `K` is
1024, not 1000)" is decided by the six `shl += 10` at `cmdline.c:163, 167, 171, 175, 179, 183` with the
`fallthrough` cascade E→P→T→G→M→K. Neither is quoted; the quoted `cmdline.c:147` is the doc comment that only lists
the letters. The hexadecimal branch's assignment `*base = 16;` (`kstrtox.c:31`) is likewise unquoted while
`*base = 8;` (33) is quoted. All are inside S246's declared ranges.

**F7 — GR3's "SIGINT reaches the foreground start's handler" rests on unquoted lines.**
The quoted `scrub.c:421` is only the handler body. The chain is `-B` → `do_background = false`
(`scrub.c:1292-1293`), foreground path installs `scrub_handle_sigint_child(fdmnt)` (`scrub.c:1546`, outside the
`if (do_background)` fork at 1512), handler `fd == -1 ? SIG_DFL : scrub_sigint_record_progress`
(`scrub.c:439`). None are quoted; both sit outside S237's declared ranges (F2).

**F8 — minor: the KillSignal-to-every-process step is on 84-85, not on the quoted 68.**
The quote at md:110 (`systemd.kill.xml:68`) says remaining processes "will be killed on unit stop"; that the *KillSignal
value* replaces SIGTERM for all of them is `systemd.kill.xml:84-85` ("Processes will first be terminated via
`SIGTERM` (unless the signal to send is changed via `KillSignal=`…)"), unquoted. Supported jointly, not wrongly
cited, but the deciding line is missing.

### Fragment screen (mechanically flagged, judged by hand)

The script prints, per quote, the same-line tail and the next line, and flags `CUT` when the next line starts with a
lowercase letter, `(` or a tag. The flag over-fires on code (a following statement is not a continuation), so it is
a screen, not a verdict. By hand: **1 quote of 31 withholds a token its Statement needs** (F3, `xml:114` → SIGCONT);
the other cut lines either complete a statement on the next C line (md:70/72, 76/78 are halves of one call whose
continuation is itself quoted) or are mid-sentence XML slices whose missing tail does not carry the claim
(`xml:68`, `xml:91`, `xml:96`, `xml:108` — the decisive continuation for 96, `FinalKillSignal=`, is on 97 but 96
already names `SIGKILL`). No quote inverts or misstates its source.

## Claims re-derived from the snapshots (not just located)

- `memparse` semantics reproduced by an independent transcription of `cmdline.c:153-200` + `vsprintf.c:79-116` +
  `kstrtox.c:26-95`: `100M`/`100m` → 104857600, `010` → 8, `0x10` → 16, `0x1F` → 31, `5K` → 5120, `1G` → 1073741824,
  `10MB` → EINVAL, `10 M` → EINVAL, `-1` → EINVAL, bare newline → 0 accepted. Shift table from the cascade:
  K=10, M=20, G=30, T=40, P=50, E=60 bits — K is 1024, not 1000; `check_shl_overflow` → `ULLONG_MAX`.
- "the last two parameters of `btrfs_scrub_dev`": signature at `scrub.c:3079-3081` is
  `fs_info, devid, start, end, progress, readonly, is_dev_replace`; both call sites (`dev-replace.c:701-703` in
  `btrfs_dev_replace_start` at 587, `dev-replace.c:1265-1268` in `btrfs_dev_replace_kthread` at 1249) pass
  `false, true` last, on `src_device->devid` / `dev_replace->srcdev->devid`.
- "0 means no limit" is real in the snapshot (`scrub.c:1380-1382`), quoted in neither entry; GR1 defers it to SR8,
  which is fair, and the round-44 entry is the place that quotes it.
- Header claims: all three S246 files are in `SHA256SUMS`; `FETCH.txt` records peeled `v7.2.11` =
  `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea` and `v262` = `8cc40e0c5e9234bf45084751ac53b1fbfe70b492`, matching the
  entry's `verified-at` line. I did not re-fetch (see Limits).

## Wrong pointers

None. Every one of the 31 pointers names a line that holds the quoted text.

## Proposed minimal amendments (L1 decides; nothing below is applied)

1. `corpus/SOURCES.md:251` S242 ranges: `1365-1385, 3079-3081, 3140-3162, 3215-3226, 3321-3337`.
2. `corpus/SOURCES.md:246` S237 ranges: add `412-444` and `1512-1550`.
3. `btrfs-scrub-grounding-r45.md:120` → ``**Quote.** `S248` systemd.kill.xml:115: "<constant>SIGCONT</constant>,
   to ensure that even suspended tasks can be terminated cleanly.</para>"`` (keep or extend the 114 quote).
4. GR2: add ``**Quote.** `S242` scrub.c:3147: "if (dev->scrub_ctx ||"``; and bound the ioctl sentence, e.g.
   "So while a replace runs, a scrub start that reaches `btrfs_scrub_dev` with `is_dev_replace` false for any device
   of that filesystem returns `EINPROGRESS` although no scrub was started [the ioctl wrapper in
   `fs/btrfs/ioctl.c` is not pinned here], and …".
5. GR1: add quotes for `cmdline.c:179` ("`shl += 10;`" — M step) + `cmdline.c:193` ("`endptr++;`") and
   `kstrtox.c:31` ("`*base = 16;`").
6. GR3: add ``**Quote.** `S237` scrub.c:439: ".sa_handler = fd == -1 ? SIG_DFL : scrub_sigint_record_progress,"``
   and ``**Quote.** `S237` scrub.c:1546: "scrub_handle_sigint_child(fdmnt);"``.

## Receipts

- `.ufo/waves/round-45/a2w1/C2ExecQuotes/quotecheck.py` — sha256
  `3a7f55fb6b03456f35159476362025aaf6d31bf67b3bb56a5a25b522f634edc2`
- `.ufo/waves/round-45/a2w1/C2ExecQuotes/out.txt` — sha256
  `c26921a377db6bd2be4d3596b85109eb6fdc8a12a0cf940ab85dc1490b460804` (full run, 134 PASS / 2 FAIL)

## Script

```python
#!/usr/bin/env python3
"""C2-7: mechanical quote/claim checker for corpus/knowledge/btrfs-scrub-grounding-r45.md.

Own script (not tools/check-scrub-grounding-r45.py).  Reads the entry at a pinned
revision, verifies the snapshot digests it relies on, then for every
'**Quote.** `Snnn` file:LINE: "text"' line checks that the named snapshot file
holds 'text' on line LINE.  Then re-checks the line-number / function-name /
value claims made inside the three Statement cells against the same snapshots.

Usage: quotecheck.py --lane DIR --revision SHA
"""
import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

W = "corpus/knowledge/btrfs-scrub-grounding-r45.md"

# source token -> (snapshot dir relative to lane, files it covers)
SRC = {
    "S246": (".ufo/waves/round-45/frozen/src", {"cmdline.c", "vsprintf.c", "kstrtox.c"}),
    "S247": (".ufo/waves/round-45/frozen/src", {"dev-replace.c"}),
    "S248": (".ufo/waves/round-45/frozen/src", {"systemd.kill.xml"}),
    "S242": (".ufo/waves/round-44/frozen/src", {"scrub.c"}),
    "S243": (".ufo/waves/round-44/frozen/src", {"sysfs.c"}),
    "S244": (".ufo/waves/round-44/frozen/src", {"btrfs-scrub@.service"}),
    "S237": (".ufo/waves/round-42/frozen/src", {"scrub.c"}),
}
CAPTURE = ".ufo/waves/round-45/frozen/hostcap/capture.txt"
CAPTURE_SHA = "f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70"

QUOTE_RE = re.compile(r'^\*\*Quote\.\*\* `(S\d+)` (\S+):(\d+): "(.*)"$')
fails = []


def ok(cond, tag, msg):
    print(("  PASS " if cond else "  FAIL ") + tag + ": " + msg)
    if not cond:
        fails.append(tag + ": " + msg)
    return cond


def sha256(p):
    h = hashlib.sha256()
    h.update(Path(p).read_bytes())
    return h.hexdigest()


def verify_digests(lane):
    print("== digest verification (SHA256SUMS, every snapshot the entry cites) ==")
    dirs = sorted({d for d, _ in SRC.values()})
    sums = {}
    for d in dirs:
        dp = Path(lane) / d / "SHA256SUMS"
        entries = {}
        for ln in dp.read_text().splitlines():
            h, name = ln.split()
            entries[name] = h
        for name, h in sorted(entries.items()):
            got = sha256(Path(lane) / d / name)
            ok(got == h, "DIGEST", f"{d}/{name} {got[:16]}… {'==' if got == h else '!='} {h[:16]}…")
        sums[d] = entries
    # every file a quote names must be covered by its dir's SHA256SUMS
    for tok, (d, files) in SRC.items():
        for f in files:
            ok(f in sums[d], "INDEXED", f"{tok} {f} listed in {d}/SHA256SUMS")
    ok(sha256(Path(lane) / CAPTURE) == CAPTURE_SHA, "DIGEST", f"capture.txt == {CAPTURE_SHA[:16]}…")
    return sums


RANGE_RE = re.compile(r"([\w./@-]+\.[A-Za-z0-9]+|PKGBUILD) lines ((?:\d+-\d+)(?:, \d+-\d+)*)")


def sources_ranges(lane, rev):
    """token -> {basename: [(lo, hi), ...]} from corpus/SOURCES.md at the revision."""
    out = subprocess.run(["git", "-C", lane, "show", f"{rev}:corpus/SOURCES.md"],
                         capture_output=True, text=True, check=True).stdout
    ranges = {}
    for row in out.splitlines():
        cells = row.split("|")
        if len(cells) < 3:
            continue
        tok = cells[1].strip()
        if tok not in SRC:
            continue
        for m in RANGE_RE.finditer(row):
            f = m.group(1).split("/")[-1]
            spans = [tuple(int(x) for x in r.split("-")) for r in m.group(2).split(", ")]
            ranges.setdefault(tok, {}).setdefault(f, []).extend(spans)
    return ranges


def range_check(lane, rev, quotes):
    print("\n== quoted lines vs the line ranges corpus/SOURCES.md declares for that source ==")
    ranges = sources_ranges(lane, rev)
    for tok, fname, num in quotes:
        spans = ranges.get(tok, {}).get(fname, [])
        if not spans:
            ok(False, "SOURCES", f"{tok} {fname} has no declared range list")
            continue
        inside = any(lo <= num <= hi for lo, hi in spans)
        ok(inside, "SOURCES-RANGE",
           f"{tok} {fname}:{num} within declared {[f'{a}-{b}' for a, b in spans]}")
    # decisive lines the Statements rely on (not quoted): informative
    extra = [("S242", "scrub.c", 3147, "dev->scrub_ctx || (the 'any call' half of GR2)"),
             ("S237", "scrub.c", 439, "handler assignment fd == -1 ? SIG_DFL : ..."),
             ("S237", "scrub.c", 1546, "foreground install of the SIGINT handler"),
             ("S246", "cmdline.c", 183, "shl += 10 (K step of the 1024 cascade)")]
    for tok, fname, num, why in extra:
        spans = ranges.get(tok, {}).get(fname, [])
        inside = any(lo <= num <= hi for lo, hi in spans)
        print(f"  INFO  {'in' if inside else 'OUTSIDE'} declared ranges: {tok} {fname}:{num} — {why}")


def check_quotes(lane, text):
    print("\n== quote lines (31 expected) ==")
    n = 0
    quotes = []
    for ln, line in enumerate(text.splitlines(), 1):
        m = QUOTE_RE.match(line)
        if not m:
            if "**Quote.**" in line:
                ok(False, "PARSE", f"md:{ln} unparsed quote line: {line!r}")
            continue
        n += 1
        tok, fname, num, quoted = m.group(1), m.group(2), int(m.group(3)), m.group(4)
        d, allowed = SRC.get(tok, (None, set()))
        if d is None or fname not in allowed:
            ok(False, "POINTER", f"md:{ln} {tok} {fname} not a file of that source")
            continue
        p = Path(lane) / d / fname
        lines = p.read_text().splitlines()
        if num < 1 or num > len(lines):
            ok(False, "POINTER", f"md:{ln} {tok} {fname}:{num} out of range (1..{len(lines)})")
            continue
        quotes.append((tok, fname, num))
        named = lines[num - 1].strip()
        exact = named == quoted.strip()
        # fuzzy: the quote must be a contiguous slice of the named line
        contains = quoted.strip() in named
        state = "exact" if exact else ("slice" if contains else "MISMATCH")
        ok(contains, "QUOTE", f"md:{ln} {tok} {fname}:{num} [{state}] {quoted[:64]!r}")
        # fragment test: does the named line continue past the quoted text, or does
        # the next line carry the sentence on / the decisive token?
        rest = named[named.index(quoted.strip()) + len(quoted.strip()):] if contains else ""
        nxt = lines[num].strip() if num < len(lines) else ""
        cont = bool(re.match(r"^[a-z(<]", nxt)) or bool(re.match(r"^[a-z(<]", (lines[num].strip() if num < len(lines) else "")))
        kind = "CUT" if (rest or cont) else "whole-line"
        print(f"       {kind}: tail={rest[:60]!r} next {fname}:{num + 1}: {nxt[:96]!r}")
    ok(n == 31, "COUNT", f"{n} quote lines parsed")
    return quotes


def sim_memparse(s):
    """Transcription of memparse() + simple_strntoull() + _parse_integer_fixup_radix()
    from the S246/S243 snapshots (cmdline.c:153-200, vsprintf.c:79-116, kstrtox.c:26-95).
    Returns (value, end_index) and then the sysfs store's accept/reject."""
    i = 0
    base = 0
    # _parse_integer_fixup_radix
    if base == 0:
        if s[0:1] == "0":
            if len(s) > 2 and s[1].lower() == "x" and s[2] in "0123456789abcdefABCDEF":
                base = 16
            else:
                base = 8
        else:
            base = 10
    if base == 16 and s[0:2].lower() == "0x":
        i += 2
    start = i
    res = 0
    # _parse_integer_limit
    while i < len(s):
        c = s[i]
        lc = c.lower()
        if "0" <= c <= "9":
            val = ord(c) - 48
        elif "a" <= lc <= "f":
            val = ord(lc) - 87
        else:
            break
        if val >= base:
            break
        res = res * base + val
        i += 1
    ret, endptr = res, i
    # memparse suffix switch, E P T G M K cascade, shl += 10 each
    shl = 0
    ch = s[endptr:endptr + 1]
    order = "EPTGMK"
    if ch and ch.upper() in order:
        shl = (len(order) - order.index(ch.upper())) * 10
    if shl and endptr != 0:
        if ret > (2**64 - 1) >> shl:
            ret = 2**64 - 1          # check_shl_overflow -> ULLONG_MAX
        else:
            ret <<= shl              # the 10-bit shift per cascade step
        endptr += 1
    # store: skip_spaces then *endptr != 0 -> -EINVAL
    while endptr < len(s) and s[endptr] in " \t\n\r\f\v":
        endptr += 1
    if endptr != len(s):
        return None  # -EINVAL
    return ret


def claim_checks(lane):
    print("\n== Statement-cell claims ==")
    r45 = Path(lane) / SRC["S246"][0]
    r44 = Path(lane) / SRC["S242"][0]
    r42 = Path(lane) / SRC["S237"][0]
    cmdline = (r45 / "cmdline.c").read_text().splitlines()
    vsprintf = (r45 / "vsprintf.c").read_text().splitlines()
    kstrtox = (r45 / "kstrtox.c").read_text().splitlines()
    sysfs = (r44 / "sysfs.c").read_text().splitlines()
    scrub44 = (r44 / "scrub.c").read_text().splitlines()
    devrep = (r45 / "dev-replace.c").read_text().splitlines()
    xml = (r45 / "systemd.kill.xml").read_text().splitlines()
    unit = (r44 / "btrfs-scrub@.service").read_text().splitlines()
    scrub42 = (r42 / "scrub.c").read_text().splitlines()
    cap = [l for l in (Path(lane) / CAPTURE).read_text().splitlines() if l]

    print("-- GR1: memparse / simple_strtoull / radix / store")
    ok(cmdline[152].startswith("unsigned long long memparse("), "GR1-fn", "memparse defined at cmdline.c:153")
    ok("memparse(buf, &endptr)" in sysfs[2039], "GR1-line", "sysfs.c:2040 is memparse(buf,&endptr)")
    ok("skip_spaces(endptr)" in sysfs[2041] and "*endptr != 0" in sysfs[2042]
       and "-EINVAL" in sysfs[2043], "GR1-line", "sysfs.c:2042 skip_spaces, :2043 test, :2044 -EINVAL")
    ok("scrub_speed_max" in sysfs[2047], "GR1-fn", "attr wired as devid/scrub_speed_max (sysfs.c:2048)")
    ok("simple_strtoull(ptr, &endptr, 0)" in cmdline[155], "GR1-line", "memparse base 0 at cmdline.c:156")
    ok("return simple_strntoull(cp, endp, base, INT_MAX)" in vsprintf[113], "GR1-hop",
       "simple_strtoull -> simple_strntoull (vsprintf.c:114); quote points at :86, two hops in")
    ok("_parse_integer_fixup_radix(startp, &base)" in vsprintf[85], "GR1-line", "fixup at vsprintf.c:86")
    ok("_parse_integer_fixup_radix(const char *s" in kstrtox[25], "GR1-fn", "fixup defined kstrtox.c:26")
    ok("*base = 16" in kstrtox[30], "GR1-value", "0x+hexdigit -> base 16 (kstrtox.c:31)")
    ok("*base = 8" in kstrtox[32], "GR1-value", "other leading 0 -> base 8 (kstrtox.c:33)")
    ok("*base = 10" in kstrtox[34], "GR1-value", "else -> base 10 (kstrtox.c:35)")
    ok("s += 2" in kstrtox[37], "GR1-value", "0x prefix consumed (kstrtox.c:38)")
    shl_adds = [i + 1 for i, l in enumerate(cmdline) if "shl += 10" in l]
    ok(len(shl_adds) == 6, "GR1-value", f"six 'shl += 10' steps at cmdline.c:{shl_adds}")
    cases = [l.strip() for l in cmdline[159:187]]
    letters = [re.match(r"case '([A-Za-z])':", c).group(1) for c in cases
               if re.match(r"case '([A-Za-z])':", c)]
    ok(letters == ["E", "e", "P", "p", "T", "t", "G", "g", "M", "m", "K", "k"],
       "GR1-value", "switch cascades E->P->T->G->M->K, both cases each")
    casc = [(n, cmdline[n].strip()) for n in shl_adds]
    ok(all(nxt == "fallthrough;" for _, nxt in casc), "GR1-value",
       "each 'shl += 10' is followed by fallthrough (cascade, no break): " + str(casc))
    shifts = {ch: (len(letters) // 2 - letters.index(ch) // 2) * 10 for ch in "KMGTPE"}
    ok(shifts == {"K": 10, "M": 20, "G": 30, "T": 40, "P": 50, "E": 60}, "GR1-value",
       f"10-bit shift per step: {shifts} -> K=1024, M=1024**2 (not 1000-based)")
    ok("shl && likely(ptr != endptr)" in cmdline[188], "GR1-line", "suffix needs consumed chars (cmdline.c:189)")
    ok("check_shl_overflow(ret, shl, &ret)" in cmdline[190] and "ULLONG_MAX" in cmdline[191],
       "GR1-line", "overflow -> ULLONG_MAX (cmdline.c:191-192)")
    ok("endptr++" in cmdline[192], "GR1-value", "exactly one suffix char consumed (cmdline.c:193)")
    table = {"100M": 104857600, "100m": 104857600, "010": 8, "0x10": 16,
             "10MB": None, "10 M": None, "-1": None, "\n": 0, "5K": 5120,
             "0x1F": 31, "1G": 1073741824, "K": None, "": 0}
    bad = {k: (sim_memparse(k), v) for k, v in table.items() if sim_memparse(k) != v}
    ok(not bad, "GR1-sim", f"example table reproduced from the snapshot code: {table}" if not bad else f"{bad}")
    ok("bwlimit = READ_ONCE(device->scrub_speed_max)" in scrub44[1379]
       and "if (bwlimit == 0)" in scrub44[1380] and "return;" in scrub44[1381],
       "GR1-value", "0 means no limit: scrub.c:1380-1382 returns before throttling (S242; not quoted in GR1)")

    print("-- GR2: btrfs_scrub_dev signature, call sites, EINPROGRESS condition")
    sig = " ".join(l.strip() for l in scrub44[3078:3081])
    params = [p.strip().split()[-1].lstrip("*") for p in
              " ".join(l.strip() for l in scrub44[3078:3081]).split("(", 1)[1].rsplit(")", 1)[0].split(",")]
    ok(params == ["fs_info", "devid", "start", "end", "progress", "readonly", "is_dev_replace"],
       "GR2-value", f"btrfs_scrub_dev params at scrub.c:3079-3081 = {params}; last two = readonly, is_dev_replace")
    i701, i703 = devrep[700], devrep[702]
    ok("src_device->devid" in i701 and i703.strip().endswith("false, true);"), "GR2-value",
       "replace-start call dev-replace.c:701-703: src_device->devid, ..., false, true")
    ok("dev_replace->srcdev->devid" in devrep[1264] and devrep[1267].strip().endswith("false, true);"),
       "GR2-value", "replace-continue call dev-replace.c:1265-1268: srcdev->devid, ..., false, true")
    encl = lambda ln: max(i for i, l in enumerate(devrep[:ln]) if re.match(r"^(static )?\w[\w \*]*\(", l)) + 1
    ok("btrfs_dev_replace_start" in devrep[encl(701) - 1], "GR2-fn",
       f"dev-replace.c:701 sits in btrfs_dev_replace_start (decl {encl(701)})")
    ok("btrfs_dev_replace_kthread" in devrep[encl(1265) - 1], "GR2-fn",
       f"dev-replace.c:1265 sits in btrfs_dev_replace_kthread (decl {encl(1265)})")
    cond = " ".join(l.strip() for l in scrub44[3146:3149])
    ok("dev->scrub_ctx || (!is_dev_replace &&" in cond.replace("  ", " ") or
       ("dev->scrub_ctx ||" in scrub44[3146] and "(!is_dev_replace &&" in scrub44[3147]),
       "GR2-value", "condition scrub.c:3147 dev->scrub_ctx || 3148 (!is_dev_replace && ...: "
                    "'any call' is the first disjunct, unguarded by is_dev_replace")
    ok("!is_dev_replace && btrfs_dev_replace_is_ongoing" not in "".join(
        l.replace("||", "") for l in scrub44[3146:3149]).split("dev->scrub_ctx")[0],
       "GR2-value", "the is_dev_replace guard applies only to the replace-ongoing disjunct")
    ok("-EINPROGRESS" in scrub44[3152] and "down_read(&fs_info->dev_replace.rwsem)" in scrub44[3145],
       "GR2-value", "refusal under dev_replace.rwsem read-lock, ret -EINPROGRESS at scrub.c:3153")
    ioctl_hops = [i + 1 for i, l in enumerate(scrub44)
                  if "BTRFS_IOC_SCRUB" in l or "scrub_ioctl" in l]
    ok(not ioctl_hops, "GR2-hop",
       f"no scrub ioctl handler / BTRFS_IOC_SCRUB in S242 scrub.c (hits={ioctl_hops}); the ioctl->btrfs_scrub_dev "
       "hop lives in fs/btrfs/ioctl.c, which no cited snapshot holds")

    print("-- GR3: unit file, systemd.kill.xml, SIGINT handler")
    ok(unit[8].strip() == "KillSignal=SIGINT", "GR3-line", "unit:9 KillSignal=SIGINT")
    ok(unit[9].strip() == "ExecStart=/usr/bin/btrfs scrub start -B %f", "GR3-line",
       "unit:10 ExecStart=btrfs scrub start -B")
    ok(not any("KillMode" in l for l in unit), "GR3-value", f"unit sets no KillMode (10 lines total: {len(unit)})")
    ok("Defaults to <option>control-group</option>" in xml[100], "GR3-value",
       "xml:101 KillMode defaults to control-group")
    ok("Defaults to <constant>SIGTERM</constant>" in xml[111], "GR3-value", "xml:112 KillSignal defaults to SIGTERM")
    ok("SIGCONT" in xml[114], "GR3-value",
       "the SIGCONT token sits on xml:115, one line past the quoted xml:114 which stops at 'always send'")
    ok("FinalKillSignal=" in xml[96] and "SendSIGKILL=" in xml[96], "GR3-value",
       "xml:97 carries FinalKillSignal=/SendSIGKILL=, one line past the quoted xml:96")
    ok("SIGKILL" in xml[95], "GR3-value", "xml:96 names SIGKILL (quoted line, complete clause start)")
    fore = [i + 1 for i, l in enumerate(scrub42) if "do_background = false" in l]
    ok(1292 <= fore[0] <= 1295, "GR3-line", f"-B sets do_background=false at scrub.c:{fore[0]}")
    ok("scrub_handle_sigint_child(fdmnt)" in scrub42[1545], "GR3-line",
       "foreground path installs the child handler at scrub.c:1546 (fork path is inside if(do_background))")
    ok("fd == -1 ? SIG_DFL : scrub_sigint_record_progress" in scrub42[438], "GR3-value",
       "handler = scrub_sigint_record_progress when fd != -1 (scrub.c:439)")
    ok("BTRFS_IOC_SCRUB_CANCEL" in scrub42[420], "GR3-line",
       "handler issues BTRFS_IOC_SCRUB_CANCEL at scrub.c:421 inside scrub_sigint_record_progress")
    ok("scan" not in scrub42[416] and scrub42[416].strip().startswith("static void scrub_sigint_record_progress"),
       "GR3-fn", "scrub.c:417 is a signal handler (int signal) — SIGINT reaches an async handler, not the main loop")
    ok("scrub_handle_sigint_parent()" in scrub42[1521], "GR3-value",
       "parent ignores SIGINT only on the forked background path (scrub.c:1522)")

    print("-- host values (Statement 'Host reading' cells vs S249 capture)")
    ok("KillMode=control-group" in cap[2] and "KillSignal=2" in cap[2] and "SendSIGKILL=yes" in cap[2]
       and "TimeoutStopUSec=5s" in cap[2] and "FinalKillSignal=9" in cap[2], "HOST",
       "capture.txt:3 matches GR3's systemctl show list exactly")
    ok("DefaultTimeoutStopSec=5s" in cap[3] and cap[3].startswith("stop_default") and ":2:" in cap[3],
       "HOST", "capture.txt:4 drop-in line 2 DefaultTimeoutStopSec=5s")
    ok(cap[4] == "dropin_owner /etc/systemd/system.conf.d/10-faster-shutdown.conf none", "HOST",
       "capture.txt:5 no package owns the drop-in")
    ok("uid=1000" in cap[0] and "CapEff=0000000000000000" in cap[0], "HOST",
       "capture.txt:1 uid 1000, empty effective capability set")
    ok("mode=644 owner=root value=0" in cap[7], "HOST", "capture.txt:8 scrub_speed_max 0/644/root on devid 1")
    ok("devids=1" in cap[8], "HOST", "capture.txt:9 single devid")
    ok("systemd 262 (262-1-arch)" in cap[1] and "7.2.11-arch1-1" in cap[1], "HOST",
       "capture.txt:2 kernel 7.2.11-arch1-1, systemd 262-1-arch")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--revision", required=True)
    a = ap.parse_args()
    text = subprocess.run(["git", "-C", a.lane, "show", f"{a.revision}:{W}"],
                          capture_output=True, text=True, check=True).stdout
    print(f"doc {W} at {a.revision}: {len(text.encode())} bytes")
    verify_digests(a.lane)
    quotes = check_quotes(a.lane, text)
    range_check(a.lane, a.revision, quotes)
    claim_checks(a.lane)
    print(f"\n== {len(fails)} FAIL ==")
    for f in fails:
        print("  " + f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
```

## Output (`out.txt`, byte-identical)

```
doc corpus/knowledge/btrfs-scrub-grounding-r45.md at 18389f44cf6ce414d7be205998b29c79fb0b490c: 11220 bytes
== digest verification (SHA256SUMS, every snapshot the entry cites) ==
  PASS DIGEST: .ufo/waves/round-42/frozen/src/CHANGES bd881ab899ba4f4f… == bd881ab899ba4f4f…
  PASS DIGEST: .ufo/waves/round-42/frozen/src/scrub.c 48df2e2f468f7db7… == 48df2e2f468f7db7…
  PASS DIGEST: .ufo/waves/round-44/frozen/src/PKGBUILD 3b803e8b05d84900… == 3b803e8b05d84900…
  PASS DIGEST: .ufo/waves/round-44/frozen/src/btrfs-scrub@.service eaa7af92d28bfa89… == eaa7af92d28bfa89…
  PASS DIGEST: .ufo/waves/round-44/frozen/src/btrfs-scrub@.timer 9a0b6cc23f7bd97b… == 9a0b6cc23f7bd97b…
  PASS DIGEST: .ufo/waves/round-44/frozen/src/scrub.c f347931b795c738d… == f347931b795c738d…
  PASS DIGEST: .ufo/waves/round-44/frozen/src/sysfs.c ce146120f29ac29c… == ce146120f29ac29c…
  PASS DIGEST: .ufo/waves/round-45/frozen/src/cmdline.c 1af5ad98fface0b5… == 1af5ad98fface0b5…
  PASS DIGEST: .ufo/waves/round-45/frozen/src/dev-replace.c f07ef0a0d260cf67… == f07ef0a0d260cf67…
  PASS DIGEST: .ufo/waves/round-45/frozen/src/kstrtox.c 0c52ae02259f06ad… == 0c52ae02259f06ad…
  PASS DIGEST: .ufo/waves/round-45/frozen/src/systemd.kill.xml 448322830dbbd02c… == 448322830dbbd02c…
  PASS DIGEST: .ufo/waves/round-45/frozen/src/vsprintf.c cabb648a2c72fcbd… == cabb648a2c72fcbd…
  PASS INDEXED: S246 kstrtox.c listed in .ufo/waves/round-45/frozen/src/SHA256SUMS
  PASS INDEXED: S246 vsprintf.c listed in .ufo/waves/round-45/frozen/src/SHA256SUMS
  PASS INDEXED: S246 cmdline.c listed in .ufo/waves/round-45/frozen/src/SHA256SUMS
  PASS INDEXED: S247 dev-replace.c listed in .ufo/waves/round-45/frozen/src/SHA256SUMS
  PASS INDEXED: S248 systemd.kill.xml listed in .ufo/waves/round-45/frozen/src/SHA256SUMS
  PASS INDEXED: S242 scrub.c listed in .ufo/waves/round-44/frozen/src/SHA256SUMS
  PASS INDEXED: S243 sysfs.c listed in .ufo/waves/round-44/frozen/src/SHA256SUMS
  PASS INDEXED: S244 btrfs-scrub@.service listed in .ufo/waves/round-44/frozen/src/SHA256SUMS
  PASS INDEXED: S237 scrub.c listed in .ufo/waves/round-42/frozen/src/SHA256SUMS
  PASS DIGEST: capture.txt == f5958a83b7cf1e2e…

== quote lines (31 expected) ==
  PASS QUOTE: md:27 S246 cmdline.c:147 [slice] 'potentially suffixed with K, M, G, T, P, E.'
       whole-line: tail='' next cmdline.c:148: '*'
  PASS QUOTE: md:29 S246 cmdline.c:156 [exact] 'unsigned long long ret = simple_strtoull(ptr, &endptr, 0);'
       CUT: tail='' next cmdline.c:157: 'unsigned int shl = 0;'
  PASS QUOTE: md:31 S246 cmdline.c:159 [exact] '/* Consume valid suffix even in case of overflow. */'
       CUT: tail='' next cmdline.c:160: 'switch (*endptr) {'
  PASS QUOTE: md:33 S246 cmdline.c:189 [exact] 'if (shl && likely(ptr != endptr)) {'
       whole-line: tail='' next cmdline.c:190: '/* Have valid suffix with preceding number. */'
  PASS QUOTE: md:35 S246 cmdline.c:191 [exact] 'if (unlikely(check_shl_overflow(ret, shl, &ret)))'
       CUT: tail='' next cmdline.c:192: 'ret = ULLONG_MAX;'
  PASS QUOTE: md:37 S246 cmdline.c:192 [exact] 'ret = ULLONG_MAX;'
       CUT: tail='' next cmdline.c:193: 'endptr++;'
  PASS QUOTE: md:39 S246 vsprintf.c:86 [exact] 'cp = _parse_integer_fixup_radix(startp, &base);'
       CUT: tail='' next vsprintf.c:87: 'prefix_chars = cp - startp;'
  PASS QUOTE: md:41 S246 kstrtox.c:29 [exact] "if (s[0] == '0') {"
       CUT: tail='' next kstrtox.c:30: "if (_tolower(s[1]) == 'x' && isxdigit(s[2]))"
  PASS QUOTE: md:43 S246 kstrtox.c:30 [exact] "if (_tolower(s[1]) == 'x' && isxdigit(s[2]))"
       whole-line: tail='' next kstrtox.c:31: '*base = 16;'
  PASS QUOTE: md:45 S246 kstrtox.c:33 [exact] '*base = 8;'
       whole-line: tail='' next kstrtox.c:34: '} else'
  PASS QUOTE: md:47 S243 sysfs.c:2040 [exact] 'limit = memparse(buf, &endptr);'
       whole-line: tail='' next sysfs.c:2041: "/* There could be trailing '\\n', also catch any typos after the value. */"
  PASS QUOTE: md:49 S243 sysfs.c:2043 [exact] 'if (*endptr != 0)'
       CUT: tail='' next sysfs.c:2044: 'return -EINVAL;'
  PASS QUOTE: md:68 S247 dev-replace.c:700 [exact] '/* the disk copy procedure reuses the scrub code */'
       CUT: tail='' next dev-replace.c:701: 'ret = btrfs_scrub_dev(fs_info, src_device->devid, 0,'
  PASS QUOTE: md:70 S247 dev-replace.c:701 [exact] 'ret = btrfs_scrub_dev(fs_info, src_device->devid, 0,'
       CUT: tail='' next dev-replace.c:702: 'btrfs_device_get_total_bytes(src_device),'
  PASS QUOTE: md:72 S247 dev-replace.c:703 [exact] '&dev_replace->scrub_progress, false, true);'
       whole-line: tail='' next dev-replace.c:704: ''
  PASS QUOTE: md:74 S247 dev-replace.c:1259 [exact] '"continuing dev_replace from %s (devid %llu) to target %s @%u%%"'
       CUT: tail='' next dev-replace.c:1260: 'btrfs_dev_name(dev_replace->srcdev),'
  PASS QUOTE: md:76 S247 dev-replace.c:1265 [exact] 'ret = btrfs_scrub_dev(fs_info, dev_replace->srcdev->devid,'
       CUT: tail='' next dev-replace.c:1266: 'dev_replace->committed_cursor_left,'
  PASS QUOTE: md:78 S247 dev-replace.c:1268 [exact] '&dev_replace->scrub_progress, false, true);'
       CUT: tail='' next dev-replace.c:1269: 'ret = btrfs_dev_replace_finishing(fs_info, ret);'
  PASS QUOTE: md:80 S242 scrub.c:3081 [exact] 'bool readonly, bool is_dev_replace)'
       whole-line: tail='' next scrub.c:3082: '{'
  PASS QUOTE: md:82 S242 scrub.c:3148 [exact] '(!is_dev_replace &&'
       CUT: tail='' next scrub.c:3149: 'btrfs_dev_replace_is_ongoing(&fs_info->dev_replace))) {'
  PASS QUOTE: md:84 S242 scrub.c:3149 [exact] 'btrfs_dev_replace_is_ongoing(&fs_info->dev_replace))) {'
       CUT: tail='' next scrub.c:3150: 'up_read(&fs_info->dev_replace.rwsem);'
  PASS QUOTE: md:86 S242 scrub.c:3153 [exact] 'ret = -EINPROGRESS;'
       CUT: tail='' next scrub.c:3154: 'goto out;'
  PASS QUOTE: md:106 S244 btrfs-scrub@.service:9 [exact] 'KillSignal=SIGINT'
       whole-line: tail='' next btrfs-scrub@.service:10: 'ExecStart=/usr/bin/btrfs scrub start -B %f'
  PASS QUOTE: md:108 S244 btrfs-scrub@.service:10 [exact] 'ExecStart=/usr/bin/btrfs scrub start -B %f'
       whole-line: tail='' next btrfs-scrub@.service:11: ''
  PASS QUOTE: md:110 S248 systemd.kill.xml:68 [exact] '<para>If set to <option>control-group</option>, all remaining pr'
       CUT: tail='' next systemd.kill.xml:69: 'unit will be killed on unit stop (for services: after the stop command is executed, as configure'
  PASS QUOTE: md:112 S248 systemd.kill.xml:91 [exact] '<listitem><para>the delay configured via the <varname>TimeoutSto'
       CUT: tail='' next systemd.kill.xml:92: '(applies to <varname>KillMode=</varname>: <option>control-group</option>, <option>mixed</option>'
  PASS QUOTE: md:114 S248 systemd.kill.xml:96 [exact] 'the termination request is repeated with the <constant>SIGKILL</'
       CUT: tail='' next systemd.kill.xml:97: '<varname>FinalKillSignal=</varname> (unless this is disabled via the <varname>SendSIGKILL=</varn'
  PASS QUOTE: md:116 S248 systemd.kill.xml:101 [exact] '<para>Defaults to <option>control-group</option>.</para>'
       whole-line: tail='' next systemd.kill.xml:102: ''
  PASS QUOTE: md:118 S248 systemd.kill.xml:108 [exact] '<listitem><para>Specifies which signal to use when stopping a se'
       CUT: tail='' next systemd.kill.xml:109: 'is sent as first step of shutting down a unit (see above), and is usually followed by'
  PASS QUOTE: md:120 S248 systemd.kill.xml:114 [exact] '<para>Note that, right after sending the signal specified in thi'
       CUT: tail='' next systemd.kill.xml:115: '<constant>SIGCONT</constant>, to ensure that even suspended tasks can be terminated cleanly.</pa'
  PASS QUOTE: md:122 S237 scrub.c:421 [exact] 'ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);'
       CUT: tail='' next scrub.c:422: 'if (ret < 0)'
  PASS COUNT: 31 quote lines parsed

== quoted lines vs the line ranges corpus/SOURCES.md declares for that source ==
  PASS SOURCES-RANGE: S246 cmdline.c:147 within declared ['142-201']
  PASS SOURCES-RANGE: S246 cmdline.c:156 within declared ['142-201']
  PASS SOURCES-RANGE: S246 cmdline.c:159 within declared ['142-201']
  PASS SOURCES-RANGE: S246 cmdline.c:189 within declared ['142-201']
  PASS SOURCES-RANGE: S246 cmdline.c:191 within declared ['142-201']
  PASS SOURCES-RANGE: S246 cmdline.c:192 within declared ['142-201']
  PASS SOURCES-RANGE: S246 vsprintf.c:86 within declared ['79-115']
  PASS SOURCES-RANGE: S246 kstrtox.c:29 within declared ['26-40']
  PASS SOURCES-RANGE: S246 kstrtox.c:30 within declared ['26-40']
  PASS SOURCES-RANGE: S246 kstrtox.c:33 within declared ['26-40']
  PASS SOURCES-RANGE: S243 sysfs.c:2040 within declared ['72-74', '2021-2049']
  PASS SOURCES-RANGE: S243 sysfs.c:2043 within declared ['72-74', '2021-2049']
  PASS SOURCES-RANGE: S247 dev-replace.c:700 within declared ['700-703', '1256-1268']
  PASS SOURCES-RANGE: S247 dev-replace.c:701 within declared ['700-703', '1256-1268']
  PASS SOURCES-RANGE: S247 dev-replace.c:703 within declared ['700-703', '1256-1268']
  PASS SOURCES-RANGE: S247 dev-replace.c:1259 within declared ['700-703', '1256-1268']
  PASS SOURCES-RANGE: S247 dev-replace.c:1265 within declared ['700-703', '1256-1268']
  PASS SOURCES-RANGE: S247 dev-replace.c:1268 within declared ['700-703', '1256-1268']
  FAIL SOURCES-RANGE: S242 scrub.c:3081 within declared ['1365-1385', '3140-3162', '3215-3226', '3321-3337']
  PASS SOURCES-RANGE: S242 scrub.c:3148 within declared ['1365-1385', '3140-3162', '3215-3226', '3321-3337']
  PASS SOURCES-RANGE: S242 scrub.c:3149 within declared ['1365-1385', '3140-3162', '3215-3226', '3321-3337']
  PASS SOURCES-RANGE: S242 scrub.c:3153 within declared ['1365-1385', '3140-3162', '3215-3226', '3321-3337']
  PASS SOURCES-RANGE: S244 btrfs-scrub@.service:9 within declared ['1-10']
  PASS SOURCES-RANGE: S244 btrfs-scrub@.service:10 within declared ['1-10']
  PASS SOURCES-RANGE: S248 systemd.kill.xml:68 within declared ['62-116']
  PASS SOURCES-RANGE: S248 systemd.kill.xml:91 within declared ['62-116']
  PASS SOURCES-RANGE: S248 systemd.kill.xml:96 within declared ['62-116']
  PASS SOURCES-RANGE: S248 systemd.kill.xml:101 within declared ['62-116']
  PASS SOURCES-RANGE: S248 systemd.kill.xml:108 within declared ['62-116']
  PASS SOURCES-RANGE: S248 systemd.kill.xml:114 within declared ['62-116']
  FAIL SOURCES-RANGE: S237 scrub.c:421 within declared ['67-70', '280-330', '446-535', '826-895', '1110-1125', '1186-1220', '1330-1340', '1498-1512', '1925-1945']
  INFO  in declared ranges: S242 scrub.c:3147 — dev->scrub_ctx || (the 'any call' half of GR2)
  INFO  OUTSIDE declared ranges: S237 scrub.c:439 — handler assignment fd == -1 ? SIG_DFL : ...
  INFO  OUTSIDE declared ranges: S237 scrub.c:1546 — foreground install of the SIGINT handler
  INFO  in declared ranges: S246 cmdline.c:183 — shl += 10 (K step of the 1024 cascade)

== Statement-cell claims ==
-- GR1: memparse / simple_strtoull / radix / store
  PASS GR1-fn: memparse defined at cmdline.c:153
  PASS GR1-line: sysfs.c:2040 is memparse(buf,&endptr)
  PASS GR1-line: sysfs.c:2042 skip_spaces, :2043 test, :2044 -EINVAL
  PASS GR1-fn: attr wired as devid/scrub_speed_max (sysfs.c:2048)
  PASS GR1-line: memparse base 0 at cmdline.c:156
  PASS GR1-hop: simple_strtoull -> simple_strntoull (vsprintf.c:114); quote points at :86, two hops in
  PASS GR1-line: fixup at vsprintf.c:86
  PASS GR1-fn: fixup defined kstrtox.c:26
  PASS GR1-value: 0x+hexdigit -> base 16 (kstrtox.c:31)
  PASS GR1-value: other leading 0 -> base 8 (kstrtox.c:33)
  PASS GR1-value: else -> base 10 (kstrtox.c:35)
  PASS GR1-value: 0x prefix consumed (kstrtox.c:38)
  PASS GR1-value: six 'shl += 10' steps at cmdline.c:[163, 167, 171, 175, 179, 183]
  PASS GR1-value: switch cascades E->P->T->G->M->K, both cases each
  PASS GR1-value: each 'shl += 10' is followed by fallthrough (cascade, no break): [(163, 'fallthrough;'), (167, 'fallthrough;'), (171, 'fallthrough;'), (175, 'fallthrough;'), (179, 'fallthrough;'), (183, 'fallthrough;')]
  PASS GR1-value: 10-bit shift per step: {'K': 10, 'M': 20, 'G': 30, 'T': 40, 'P': 50, 'E': 60} -> K=1024, M=1024**2 (not 1000-based)
  PASS GR1-line: suffix needs consumed chars (cmdline.c:189)
  PASS GR1-line: overflow -> ULLONG_MAX (cmdline.c:191-192)
  PASS GR1-value: exactly one suffix char consumed (cmdline.c:193)
  PASS GR1-sim: example table reproduced from the snapshot code: {'100M': 104857600, '100m': 104857600, '010': 8, '0x10': 16, '10MB': None, '10 M': None, '-1': None, '\n': 0, '5K': 5120, '0x1F': 31, '1G': 1073741824, 'K': None, '': 0}
  PASS GR1-value: 0 means no limit: scrub.c:1380-1382 returns before throttling (S242; not quoted in GR1)
-- GR2: btrfs_scrub_dev signature, call sites, EINPROGRESS condition
  PASS GR2-value: btrfs_scrub_dev params at scrub.c:3079-3081 = ['fs_info', 'devid', 'start', 'end', 'progress', 'readonly', 'is_dev_replace']; last two = readonly, is_dev_replace
  PASS GR2-value: replace-start call dev-replace.c:701-703: src_device->devid, ..., false, true
  PASS GR2-value: replace-continue call dev-replace.c:1265-1268: srcdev->devid, ..., false, true
  PASS GR2-fn: dev-replace.c:701 sits in btrfs_dev_replace_start (decl 587)
  PASS GR2-fn: dev-replace.c:1265 sits in btrfs_dev_replace_kthread (decl 1249)
  PASS GR2-value: condition scrub.c:3147 dev->scrub_ctx || 3148 (!is_dev_replace && ...: 'any call' is the first disjunct, unguarded by is_dev_replace
  PASS GR2-value: the is_dev_replace guard applies only to the replace-ongoing disjunct
  PASS GR2-value: refusal under dev_replace.rwsem read-lock, ret -EINPROGRESS at scrub.c:3153
  PASS GR2-hop: no scrub ioctl handler / BTRFS_IOC_SCRUB in S242 scrub.c (hits=[]); the ioctl->btrfs_scrub_dev hop lives in fs/btrfs/ioctl.c, which no cited snapshot holds
-- GR3: unit file, systemd.kill.xml, SIGINT handler
  PASS GR3-line: unit:9 KillSignal=SIGINT
  PASS GR3-line: unit:10 ExecStart=btrfs scrub start -B
  PASS GR3-value: unit sets no KillMode (10 lines total: 10)
  PASS GR3-value: xml:101 KillMode defaults to control-group
  PASS GR3-value: xml:112 KillSignal defaults to SIGTERM
  PASS GR3-value: the SIGCONT token sits on xml:115, one line past the quoted xml:114 which stops at 'always send'
  PASS GR3-value: xml:97 carries FinalKillSignal=/SendSIGKILL=, one line past the quoted xml:96
  PASS GR3-value: xml:96 names SIGKILL (quoted line, complete clause start)
  PASS GR3-line: -B sets do_background=false at scrub.c:1293
  PASS GR3-line: foreground path installs the child handler at scrub.c:1546 (fork path is inside if(do_background))
  PASS GR3-value: handler = scrub_sigint_record_progress when fd != -1 (scrub.c:439)
  PASS GR3-line: handler issues BTRFS_IOC_SCRUB_CANCEL at scrub.c:421 inside scrub_sigint_record_progress
  PASS GR3-fn: scrub.c:417 is a signal handler (int signal) — SIGINT reaches an async handler, not the main loop
  PASS GR3-value: parent ignores SIGINT only on the forked background path (scrub.c:1522)
-- host values (Statement 'Host reading' cells vs S249 capture)
  PASS HOST: capture.txt:3 matches GR3's systemctl show list exactly
  PASS HOST: capture.txt:4 drop-in line 2 DefaultTimeoutStopSec=5s
  PASS HOST: capture.txt:5 no package owns the drop-in
  PASS HOST: capture.txt:1 uid 1000, empty effective capability set
  PASS HOST: capture.txt:8 scrub_speed_max 0/644/root on devid 1
  PASS HOST: capture.txt:9 single devid
  PASS HOST: capture.txt:2 kernel 7.2.11-arch1-1, systemd 262-1-arch

== 2 FAIL ==
  SOURCES-RANGE: S242 scrub.c:3081 within declared ['1365-1385', '3140-3162', '3215-3226', '3321-3337']
  SOURCES-RANGE: S237 scrub.c:421 within declared ['67-70', '280-330', '446-535', '826-895', '1110-1125', '1186-1220', '1330-1340', '1498-1512', '1925-1945']
```

## Limits — what I did not do

- No network re-fetch: digests were verified against the on-disk snapshots and their `SHA256SUMS`, not against the
  upstream URLs; `FETCH.txt` was read, not re-run.
- I did not run `tools/check-scrub-grounding-r45.py` (the item asks for my own script); no counter verdict is claimed.
- `fs/btrfs/ioctl.c` is not in any cited snapshot and I did not fetch it, so F5 states unpinned, not wrong.
- The `CUT` flag in the output is a mechanical screen; the one substantive fragment is F3.
- No lane, host or fixture mutation: no git command outside `git show`/`git log` reads, no unit, scrub, sysfs or
  package operation; no agents spawned; scratch under `/fast/scratch/hyaku/tsukuroi-r45/C2ExecQuotes` removed before
  yielding. No tool installed or upgraded, so no install record is due.
