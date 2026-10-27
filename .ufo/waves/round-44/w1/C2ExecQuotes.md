VERDICT: defect-found

# C2-3 — every `**Quote.**` line and every Statement-cell pointer (seat C2ExecQuotes)

Item: check all 33 `**Quote.**` locators of `corpus/knowledge/btrfs-scrub-record-r44.md` at
`7e081698d4fc3c4ea944884fd093058de9909de1`, with the snapshots digest-verified first, then check every
line-number / function-name claim inside the three Statement cells. Script written for this seat
(`.ufo/waves/round-44/w1/C2ExecQuotes/check_quotes_r44.py`, sha256 `58d87db593409fe8…`); the lane counter
`tools/check-scrub-record-r44.py` was **not** run and was only read statically (`:105-106`, `:300`) to note that it
uses the same containment test (`q in src[n-1]`) my pass A uses.

Result: **83/83 checks pass, 0 fail** — 33/33 quote locators hold their text, 24/24 SR7/SR8/SR9 pointer checks hold,
and one wrong pointer was found that is *not* a quote: SR7's `dev-replace.c` bracket ends one line before the
argument it is cited for. Everything substantive is supported.

## 1. Method

- Digest gate first: `sha256sum -c SHA256SUMS` in each of `.ufo/waves/round-44/frozen/src`,
  `.ufo/waves/round-42/frozen/src`, `.ufo/waves/round-43/frozen/src` — 8/8 `OK`
  (`round-44` scrub.c `f347931b…`, sysfs.c `ce146120…`, `btrfs-scrub@.timer` `9a0b6cc2…`,
  `btrfs-scrub@.service` `eaa7af92…`, PKGBUILD `3b803e8b…`; `round-42` scrub.c `48df2e2f…`, CHANGES `bd881ab8…`;
  `round-43` ioctl.c `7b3488f2…`). `hostcap/capture.txt` hashes to the `source:`-line digest
  `efb523889035cba62235d904b9e254068a7083dd07e7bb338ce2a803a3e84900` (info line, not a gate).
- Document read from the object store, not the worktree: `git cat-file -p 7e08169…:corpus/knowledge/…-r44.md`
  → 145 lines, sha256 `cc9233899417ec4803ebdc3114b71722723db3a0f2c79870339ed51d0b1609b1`; `git diff` of that path
  against the same revision is empty, so worktree == revision.
- Pass A compares each quote as a **substring of the stripped snapshot line** (`q in line`), so internal
  whitespace, tabs and punctuation must match exactly; a strict prefix match is reported separately as a note.
- Pass B checks the pointer claims as structure, not as strings: ordering of `mutex_lock` → `btrfs_find_device` →
  `mutex_unlock`, attach line number < first scrub-work line, detach line number > last scrub-work line, the
  `if`-guard span around `-EINPROGRESS`, the `case 'B'` block bounds, the `capable()` gate before the call.
- S-id → file resolution uses the filename in the locator (needed for `S244`, which carries three files).

## 2. Finding F1 — the one wrong pointer (SR7, `dev-replace.c` line range)

`corpus/knowledge/btrfs-scrub-record-r44.md:21` (SR7 Statement cell):

```
`fs/btrfs/dev-replace.c`, opened this round at v7.2.11 lines 701-703 and 1265-1267 but not pinned].
```

`dev-replace.c` is **not** in the frozen set (`.ufo/waves/round-44/frozen/src/` holds only FETCH.txt, PKGBUILD,
SHA256SUMS, `btrfs-scrub@.service`, `btrfs-scrub@.timer`, scrub.c, sysfs.c), so the claim cannot be checked
against a snapshot. I fetched the file myself (read-only, `curl -sfL …dev-replace.c?h=v7.2.11`, rc=0,
sha256 `f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a`, 1322 lines; receipt `live-aux.txt`).
`btrfs_scrub_dev(` appears at lines 701, 948 (a format string) and 1265 only:

```
 699:
 700:	/* the disk copy procedure reuses the scrub code */
 701:	ret = btrfs_scrub_dev(fs_info, src_device->devid, 0,
 702:			      btrfs_device_get_total_bytes(src_device),
 703:			      &dev_replace->scrub_progress, false, true);
...
1264:
1265:	ret = btrfs_scrub_dev(fs_info, dev_replace->srcdev->devid,
1266:			      dev_replace->committed_cursor_left,
1267:			      btrfs_device_get_total_bytes(dev_replace->srcdev),
1268:			      &dev_replace->scrub_progress, false, true);
```

`701-703` is exact and does show `is_dev_replace = true` (line 703). `1265-1267` stops one line short: the
`false, true` under test is on **1268**, so a reader who opens exactly the cited range never sees the argument the
bracket is cited for. The substantive claim (replace runs through the same `btrfs_scrub_dev`) holds at both sites;
only the range is short.

Exact proposed replacement for line 21 (change `1265-1267` → `1265-1268`, nothing else):

```
`fs/btrfs/dev-replace.c`, opened this round at v7.2.11 lines 701-703 and 1265-1268 but not pinned].
```

This coincides with the sibling seat C2ExecLiveSources' defect D1 (`.ufo/waves/round-44/w1/C2ExecLiveSources.md`,
§3), reached here independently from a separate fetch of the same bytes (same sha256).

## 3. Note N1 — one quote is a strict prefix of its line (cosmetic, passes)

`doc:65`, `S243 sysfs.c:72`, quotes `#define BTRFS_ATTR_RW(_prefix, _name, _show, _store)`; the line is that plus
`\t\t\t\` (the macro-continuation backslash). The quoted text is contained in the line, so the locator is right and
the counter's `q in src[n-1]` test passes; the trailing `\` is dropped with no ellipsis, which is a fidelity
wrinkle, not a wrong pointer. 32/33 quotes are strip-equal, this is the only non-equal one.

## 4. Note N2 — properties grounded outside the frozen set (verified live, or already declared inference)

SR8 asserts two properties of functions whose definitions are not frozen; both hold at v7.2.11 on fetched bytes
(`live-aux.txt`):

- "a size suffix such as `K`, `M` or `G` is accepted" — `memparse`, `lib/cmdline.c:142-147` ("potentially
  suffixed with K, M, G, T, P, E", switch cases at 160-186), sha256 `1af5ad98…`. (`lib/parser.c` has no
  `memparse`; `lib/cmdline.c` is the definition.)
- "skips trailing whitespace including the newline" — `skip_spaces`, `lib/string_helpers.c:846-851`
  (`while (isspace(*str)) ++str;`), sha256 `674e41d0…`; `isspace()` covers `\n`.

Not checkable anywhere in the frozen set, and correctly not presented as pinned: `capable()` semantics (SR7, SR6),
`systemd.kill(5)` `KillSignal=` behaviour (SR9 — the entry declares this `[inference]` in Limits, `:144-145`),
`timers.target.wants` link creation on enable (SR9, systemd behaviour; the unit's `WantedBy=timers.target` at
`btrfs-scrub@.timer:11` is the pinned half).

## 5. What passed, in full

Pass A — 33/33 locators, substring-exact, 0 duplicates, 0 out-of-range, distribution S237 5, S240 2, S242 11,
S243 7, S244 8 (three files: PKGBUILD 2, timer 4, service 2).

Pass B — 24/24:

- SR7 (10): `-EINPROGRESS` guard at scrub.c:3147 with `ret = -EINPROGRESS;` at 3153 inside it (guard span
  3147-3154); attach `dev->scrub_ctx = sctx;` at 3159 **before** the first scrub work (`scrub_supers` at 3193);
  detach `dev->scrub_ctx = NULL;` at 3222 **after** the last scrub work (`memcpy(progress, …)` at 3215);
  `btrfs_scrub_progress` defined at 3321, lock 3328 < `btrfs_find_device` 3329 < unlock 3334;
  `memcpy` of `sctx->stat` at 3333; `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;` at 3336;
  ioctl handler 3126 with `capable(CAP_SYS_ADMIN)` 3132 < call 3139 < `copy_to_user` 3141, and 3141 is
  `if (ret == 0 && copy_to_user(arg, sa, sizeof(*sa)))`. Also: the only writes to `dev->scrub_ctx` in the whole
  file are 3159 and 3222 (`grep -n "dev->scrub_ctx"` → 3147, 3159, 3222, 3304, 3310, 3313, 3331), so "carries a
  scrub context exactly while `btrfs_scrub_dev` runs on it" is structurally exact.
- SR8 (7): macro at 72 / `__INIT_KOBJ_ATTR(_name, 0644, …)` at 74; `sysfs_emit(buf, "%llu\n", …)` at 2028;
  store order `memparse` 2040 → `skip_spaces` 2042 → `if (*endptr != 0)` 2043 → `return -EINVAL;` 2044;
  registration at 2048; throttle `scrub_throttle_dev_io` at 1371 reads 1380, tests 1381, `return;` 1382, and its
  own comment at 1367-1369 says "the timeslice is 1 second", which is what makes the value bytes per second.
- SR9 (7): PKGBUILD:100/101 install both units to `${pkgdir}/usr/lib/systemd/system/`; `case 'B'` (1292) sets
  `do_background = false;` (1293) and `do_print = true;` (1295) before `case 'd'` (1297); the foreground path calls
  `scrub_handle_sigint_child(fdmnt)` at 1546, which sets `.sa_handler = scrub_sigint_record_progress` at 439, which
  issues `BTRFS_IOC_SCRUB_CANCEL` at 421; `sp->stats.canceled = !!ret;` at 969, two statements after the
  `BTRFS_IOC_SCRUB` ioctl at 965.

Pass C (extra, 7/7) — the `capture.txt:N` pointers in the three Host reading cells (lines 1, 4, 5, 6, 7, 8, 9) all
land on the claimed text, including `CapEff=0000000000000000`, `mode=644 owner=root value=0`, and installed-unit
digests equal to `SHA256SUMS`.

Pass D (extra, 10/10) — every function name the statements use exists where the entry implies:
`btrfs_scrub_dev` (scrub.c:3079, `is_dev_replace` in the signature at 3081 and branched 7× in the body),
`btrfs_scrub_progress` (3321), `is_scrub_running_in_kernel` (r42 scrub.c:1190; ioctl at 1200, `if (!ret)` 1201,
`return 1;` 1202 — matching SR7's "answers 1 exactly when some device it asks about is being scrubbed"),
`BTRFS_ATTR_RW` (sysfs.c:72), `memparse` (2040), `skip_spaces` (2042), `BTRFS_IOC_SCRUB_CANCEL` (r42:421), and the
SR8 path claim `devinfo/<devid>/scrub_speed_max` under `/sys/fs/btrfs/<fsid>/` (sysfs.c:36 comment;
`kobject_init_and_add(&device->devid_kobj, &devid_ktype, devinfo_kobj, "%llu", device->devid)` at 2165-2166).

## 6. What I did not do

- Did not run `tools/check-scrub-record-r44.py` or `tools/score-scrub-arm-r44.py`; no verdict is bound here (wave 2
  owns verdicts). Read the counter statically only.
- Did not touch the lane: no edit, no git/jj mutation, no index change. The entry, `frozen/src` and `FETCH.txt`
  are unchanged; F1's fix and any freeze of `dev-replace.c` are the L1's call.
- Did not run a scrub, write sysfs, enable/start/stop a unit, or read any privileged interface. The only live
  actions were four read-only `curl` fetches (`dev-replace.c`, `lib/cmdline.c`, `lib/parser.c`,
  `lib/string_helpers.c`, `lib/string.c`, `include/linux/string.h`) and `sha256sum`/`grep`/`awk` on local files.
- Did not verify the tag→commit peeling recorded in `FETCH.txt` (that is C2-1's item) or the `btrfs scrub resume`
  take-up of a canceled record (SR3, round-43 entry).
- No tool was installed or upgraded; nothing was written outside this report and its receipts. Scratch
  `/fast/scratch/hyaku/tsukuroi-r44/C2ExecQuotes/` removed after the receipts were copied out.

## 7. Receipts

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/w1/C2ExecQuotes/`

- `check_quotes_r44.py` — the checker, sha256 `58d87db593409fe8f104407961e7e21b88ca06f932347cb4dcbe888b47e94ff3`
- `out.txt` — its full output, sha256 `3b8d0b0489b77536a48dacf83287daa25fb81fe0a4b10e20a90633aefb726cce`
- `live-aux.txt` — the out-of-freeze fetches with digests and numbered excerpts, sha256 `a5afc2c154370a6e…`

## Appendix A — the script

```python
#!/usr/bin/env python3
"""C2-3: independent quote + statement-pointer check for
corpus/knowledge/btrfs-scrub-record-r44.md at revision 7e08169.

Not the lane counter (tools/check-scrub-record-r44.py). Two passes:
  A. every `**Quote.**` line -> named snapshot line must hold the quoted text
  B. every line-number / function-name claim in the three Statement cells ->
     checked against the same snapshots
Snapshots are digest-verified first; a mismatch aborts.
"""
import hashlib
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
REV = "7e081698d4fc3c4ea944884fd093058de9909de1"
DOC = "corpus/knowledge/btrfs-scrub-record-r44.md"
R44 = os.path.join(LANE, ".ufo/waves/round-44/frozen/src")
R42 = os.path.join(LANE, ".ufo/waves/round-42/frozen/src")
R43 = os.path.join(LANE, ".ufo/waves/round-43/frozen/src")
HOST = os.path.join(LANE, ".ufo/waves/round-44/frozen/hostcap")

# S-id -> (frozen dir holding SHA256SUMS, relative file name inside it)
SOURCES = {
    "S237": (R42, "scrub.c"),
    "S240": (R43, "ioctl.c"),
    "S242": (R44, "scrub.c"),
    "S243": (R44, "sysfs.c"),
    "S244": (R44, "PKGBUILD"),
    "S244t": (R44, "btrfs-scrub@.timer"),
    "S244s": (R44, "btrfs-scrub@.service"),
}

fail = 0


def report(ok, label, detail=""):
    global fail
    if not ok:
        fail += 1
    print(("  PASS  " if ok else "  FAIL  ") + label + (("  | " + detail) if detail else ""))
    return ok


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_digests():
    print("== pass 0: digest verification ==")
    seen = {}
    for d in (R44, R42, R43):
        sums = os.path.join(d, "SHA256SUMS")
        with open(sums) as fh:
            for line in fh:
                parts = line.split()
                if len(parts) != 2:
                    continue
                digest, name = parts
                path = os.path.join(d, name)
                got = sha256(path)
                report(got == digest, f"{os.path.relpath(path, LANE)}",
                       f"expected {digest[:16]}… got {got[:16]}…")
                seen[path] = got
    hc = os.path.join(HOST, "capture.txt")
    if os.path.exists(hc):
        print(f"  info  {os.path.relpath(hc, LANE)} sha256 {sha256(hc)}")
    return seen


def load_doc():
    out = subprocess.run(["git", "-C", LANE, "cat-file", "-p", f"{REV}:{DOC}"],
                         capture_output=True, text=True, check=True)
    return out.stdout.splitlines()


QUOTE_RE = re.compile(r'^\*\*Quote\.\*\* `(S\d+)([ts]?)` (\S+):(\d+): "(.*)"$')


def source_for(sid, fname):
    """Resolve (S-id, filename in the doc) to a snapshot path."""
    d, default = SOURCES[sid]
    if sid == "S244":
        cand = os.path.join(d, fname)
        return cand if os.path.exists(cand) else None
    return os.path.join(d, default)


def pass_a(doc):
    print("\n== pass A: every **Quote.** line against its snapshot ==")
    n = 0
    trunc = []
    for lineno, line in enumerate(doc, 1):
        m = QUOTE_RE.match(line)
        if not m:
            if line.startswith("**Quote.**"):
                report(False, f"doc:{lineno} unparsable quote line", line[:80])
            continue
        n += 1
        sid, suffix, fname, sline, text = m.groups()
        path = source_for(sid, fname)
        if path is None:
            report(False, f"doc:{lineno} {sid} {fname}:{sline}", "snapshot file not found")
            continue
        with open(path, encoding="utf-8", errors="surrogateescape") as fh:
            lines = fh.read().splitlines()
        idx = int(sline)
        if idx < 1 or idx > len(lines):
            report(False, f"doc:{lineno} {sid} {fname}:{sline}", f"out of range (file has {len(lines)})")
            continue
        actual = lines[idx - 1].strip()
        ok = text.strip() in actual
        if ok and actual != text.strip():
            trunc.append((lineno, sid, fname, sline, text.strip(), actual))
        report(ok, f"doc:{lineno} {sid} {fname}:{sline}",
               "" if ok else f"quoted={text!r} actual={actual!r}")
    for lineno, sid, fname, sline, quoted, actual in trunc:
        print(f"  note  doc:{lineno} {sid} {fname}:{sline} quote is a strict prefix of the line "
              f"(dropped tail {actual[len(quoted):]!r}, no ellipsis)")
    report(n == 33, f"quote line count = {n} (doc has 33)")
    return n


def slines(path):
    with open(path, encoding="utf-8", errors="surrogateescape") as fh:
        return fh.read().splitlines()


def at(lines, n):
    return lines[n - 1].strip() if 1 <= n <= len(lines) else ""


def find(lines, pattern, start=1, end=None):
    rx = re.compile(pattern)
    end = end or len(lines)
    for i in range(start, end + 1):
        if rx.search(lines[i - 1]):
            return i
    return None


def pass_b():
    print("\n== pass B: Statement-cell line/function claims ==")
    s242 = slines(os.path.join(R44, "scrub.c"))
    s243 = slines(os.path.join(R44, "sysfs.c"))
    s240 = slines(os.path.join(R43, "ioctl.c"))
    s237 = slines(os.path.join(R42, "scrub.c"))
    pkgsrc = slines(os.path.join(R44, "PKGBUILD"))

    # ---- SR7 ----
    print(" SR7")
    report(at(s242, 3147) == "if (dev->scrub_ctx ||",
           "SR7 'refuses ... when dev->scrub_ctx is already set' guard at scrub.c:3147",
           at(s242, 3147))
    report(at(s242, 3153) == "ret = -EINPROGRESS;",
           "SR7 -EINPROGRESS at scrub.c:3153 inside that guard",
           f"guard 3147..{find(s242, r'goto out;', 3147)}")
    fn = find(s242, r"^int btrfs_scrub_dev\(")
    report(fn is not None, "SR7 function btrfs_scrub_dev defined", f"scrub.c:{fn}")
    attach = find(s242, r"^\s*dev->scrub_ctx = sctx;")
    first_work = min(x for x in (
        find(s242, r"scrub_supers\(sctx, dev\)", fn),
        find(s242, r"scrub_enumerate_chunks\(sctx, dev", fn),
    ) if x)
    report(attach is not None and attach < first_work,
           "SR7 'attaches its own context before the scrub starts'",
           f"attach scrub.c:{attach} < first scrub work scrub.c:{first_work}")
    detach = find(s242, r"^\s*dev->scrub_ctx = NULL;")
    last_work = find(s242, r"memcpy\(progress, &sctx->stat", fn)
    report(detach is not None and detach > last_work,
           "SR7 'sets dev->scrub_ctx back to NULL when it ends'",
           f"detach scrub.c:{detach} > last scrub work scrub.c:{last_work}")
    prog = find(s242, r"^int btrfs_scrub_progress\(")
    lock = find(s242, r"mutex_lock\(&fs_info->fs_devices->device_list_mutex\)", prog)
    lookup = find(s242, r"dev = btrfs_find_device\(", prog)
    unlock = find(s242, r"mutex_unlock\(&fs_info->fs_devices->device_list_mutex\)", lookup)
    report(prog is not None and lock < lookup < unlock,
           "SR7 'looks the requested devid up under device_list_mutex'",
           f"progress@{prog} lock@{lock} find@{lookup} unlock@{unlock}")
    report(at(s242, 3333) == "memcpy(progress, &sctx->stat, sizeof(*progress));",
           "SR7 'copies that context's stat' at scrub.c:3333", at(s242, 3333))
    report(at(s242, 3336) == "return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;",
           "SR7 0/-ENOTCONN/-ENODEV return at scrub.c:3336", at(s242, 3336))
    h = find(s240, r"^static long btrfs_ioctl_scrub_progress\(")
    cap = find(s240, r"capable\(CAP_SYS_ADMIN\)", h)
    call = find(s240, r"ret = btrfs_scrub_progress\(fs_info, sa->devid", h)
    copy = find(s240, r"copy_to_user\(arg, sa, sizeof\(\*sa\)\)", call)
    report(h is not None and h < cap < call < copy,
           "SR7 ioctl handler: CAP_SYS_ADMIN gate before the call",
           f"handler@{h} gate@{cap} call@{call} copy_to_user@{copy}")
    report(at(s240, 3141).startswith("if (ret == 0 && copy_to_user("),
           "SR7 'copies the arguments back only when it is 0' at ioctl.c:3141",
           at(s240, 3141))

    # ---- SR8 ----
    print(" SR8")
    report(at(s243, 72).startswith("#define BTRFS_ATTR_RW(_prefix, _name, _show, _store)"),
           "SR8 BTRFS_ATTR_RW declared at sysfs.c:72", at(s243, 72))
    report(at(s243, 74) == "__INIT_KOBJ_ATTR(_name, 0644, _show, _store)",
           "SR8 mode 0644 built at sysfs.c:74", at(s243, 74))
    report(at(s243, 2028) == 'return sysfs_emit(buf, "%llu\\n", READ_ONCE(device->scrub_speed_max));',
           "SR8 decimal + newline read at sysfs.c:2028", at(s243, 2028))
    store = find(s243, r"^static ssize_t btrfs_devinfo_scrub_speed_max_store\(")
    mem = find(s243, r"limit = memparse\(buf, &endptr\);", store)
    skip = find(s243, r"endptr = skip_spaces\(endptr\);", mem)
    einv = find(s243, r"return -EINVAL;", skip)
    report(mem == 2040 and skip == 2042 and einv == 2044,
           "SR8 store order memparse -> skip_spaces -> -EINVAL",
           f"memparse@{mem} skip_spaces@{skip} EINVAL@{einv}")
    report(at(s243, 2043).startswith("if (*endptr != 0)"),
           "SR8 'rejects anything else after the number' at sysfs.c:2043", at(s243, 2043))
    report(at(s243, 2048) == "BTRFS_ATTR_RW(devid, scrub_speed_max, btrfs_devinfo_scrub_speed_max_show,",
           "SR8 attribute registration at sysfs.c:2048", at(s243, 2048))
    thr = find(s242, r"^static void scrub_throttle_dev_io\(")
    rd = find(s242, r"bwlimit = READ_ONCE\(device->scrub_speed_max\);", thr)
    zero = find(s242, r"if \(bwlimit == 0\)", rd)
    ret0 = find(s242, r"^\s*return;$", zero)
    report(thr is not None and rd == 1380 and zero == 1381 and ret0 == 1382,
           "SR8 throttle reads scrub_speed_max and returns at once when 0",
           f"fn@{thr} read@{rd} zero@{zero} return@{ret0}")

    # ---- SR9 ----
    print(" SR9")
    report(at(pkgsrc, 100) == 'install -Dm644 btrfs-scrub@.service "${pkgdir}/usr/lib/systemd/system/btrfs-scrub@.service"',
           "SR9 PKGBUILD:100 installs the service", at(pkgsrc, 100))
    report(at(pkgsrc, 101) == 'install -Dm644 btrfs-scrub@.timer "${pkgdir}/usr/lib/systemd/system/btrfs-scrub@.timer"',
           "SR9 PKGBUILD:101 installs the timer", at(pkgsrc, 101))
    case_b = find(s237, r"^\s*case 'B':")
    nb = find(s237, r"^\s*case 'd':", case_b)
    report(case_b is not None
           and find(s237, r"do_background = false;", case_b) < nb
           and find(s237, r"do_print = true;", case_b) < nb,
           "SR9 '-B' keeps foreground (do_background=false) and sets do_print",
           f"case 'B'@{case_b}..{nb - 1}")
    handler = find(s237, r"^static int scrub_handle_sigint_child\(int fd\)")
    sig = find(s237, r"scrub_sigint_record_progress", handler)
    report(handler is not None and sig == 439,
           "SR9 SIGINT handler installed by scrub_handle_sigint_child", f"scrub.c:{sig}")
    rec = find(s237, r"^static void scrub_sigint_record_progress\(int signal\)")
    ioctl_line = find(s237, r"BTRFS_IOC_SCRUB_CANCEL", rec)
    report(ioctl_line == 421, "SR9 handler issues BTRFS_IOC_SCRUB_CANCEL", f"scrub.c:{ioctl_line}")
    bg = find(s237, r"^\s*if \(do_background\) \{")
    fg_call = find(s237, r"scrub_handle_sigint_child\(fdmnt\);")
    bg_end = find(s237, r"^\s*scrub_handle_sigint_child\(-1\);")
    report(bg is not None and fg_call == 1546 and fg_call > bg and fg_call < bg_end,
           "SR9 foreground start calls scrub_handle_sigint_child(fdmnt)",
           f"do_background@{bg} fg call@{fg_call} background call@{bg_end}")
    one_dev = find(s237, r"^static void \*scrub_one_dev\(")
    io = find(s237, r"ret = ioctl\(sp->fd, BTRFS_IOC_SCRUB, &sp->scrub_args\);", one_dev)
    cancel = find(s237, r"sp->stats.canceled = !!ret;", io)
    report(cancel == 969 and io < cancel and cancel - io <= 4,
           "SR9 canceled set from the scrub ioctl return", f"ioctl@{io} canceled@{cancel}")


def pass_c():
    """Extra: the `capture.txt:N` pointers in the three Host reading cells."""
    print("\n== pass C (extra): Host reading cell pointers into capture.txt ==")
    cap = slines(os.path.join(HOST, "capture.txt"))
    report(len(cap) >= 9, "capture.txt has at least 9 lines", f"{len(cap)} lines")
    report("uid=1000" in at(cap, 1) and "CapEff=0000000000000000" in at(cap, 1),
           "capture.txt:1 'no effective capabilities'", at(cap, 1))
    report("mode=644" in at(cap, 4) and "owner=root" in at(cap, 4) and "value=0" in at(cap, 4)
           and "/devinfo/1/scrub_speed_max" in at(cap, 4),
           "capture.txt:4 devid 1 scrub_speed_max mode=644 owner=root value=0", at(cap, 4))
    report(at(cap, 5) == "wants_btrfs_scrub_instances 0",
           "capture.txt:5 no timers.target.wants link", at(cap, 5))
    report(at(cap, 6) == "is_enabled_btrfs-scrub@-.timer disabled",
           "capture.txt:6 instance disabled", at(cap, 6))
    report(at(cap, 7).startswith("installed_unit 9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad")
           and at(cap, 8).startswith("installed_unit eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252"),
           "capture.txt:7,8 installed units byte-identical to the pinned digests",
           at(cap, 7)[:40] + " / " + at(cap, 8)[:40])
    report("owned by btrfs-progs 7.1-1" in at(cap, 9),
           "capture.txt:9 package ownership", at(cap, 9))


def pass_d():
    """Extra: function-name and path claims named in the Statement cells."""
    print("\n== pass D (extra): function names and sysfs path named in the statements ==")
    s242 = slines(os.path.join(R44, "scrub.c"))
    s243 = slines(os.path.join(R44, "sysfs.c"))
    s237 = slines(os.path.join(R42, "scrub.c"))
    s240 = slines(os.path.join(R43, "ioctl.c"))

    report(find(s242, r"^int btrfs_scrub_dev\(") == 3079,
           "name btrfs_scrub_dev defined", f"scrub.c:{find(s242, r'^int btrfs_scrub_dev\(')}")
    report(find(s242, r"^int btrfs_scrub_progress\(") == 3321,
           "name btrfs_scrub_progress defined", f"scrub.c:{find(s242, r'^int btrfs_scrub_progress\(')}")
    sig = find(s242, r"^int btrfs_scrub_dev\(")
    report(find(s242, r"bool readonly, bool is_dev_replace\)", sig) == 3081,
           "SR7 'its is_dev_replace argument' in the signature", f"scrub.c:3081")
    uses = [i for i in range(sig, find(s242, r"^}", 3230)) if "is_dev_replace" in s242[i - 1]]
    report(len(uses) >= 2, "SR7 'serves both a scrub and a device replace' — is_dev_replace branches in the body",
           f"{len(uses)} uses: lines {uses}")
    fn = find(s237, r"^static int is_scrub_running_in_kernel\(int fd,")
    io = find(s237, r"ret = ioctl\(fd, BTRFS_IOC_SCRUB_PROGRESS, &sp.scrub_args\);", fn)
    report(fn == 1190 and io == 1200 and at(s237, 1201) == "if (!ret)" and at(s237, 1202) == "return 1;",
           "SR7's SR6 referent is_scrub_running_in_kernel answers 1 on the first 0",
           f"fn@{fn} ioctl@{io} -> return 1")
    report(find(s243, r"^#define BTRFS_ATTR_RW") == 72, "name BTRFS_ATTR_RW defined", "sysfs.c:72")
    report(find(s243, r"memparse\(buf, &endptr\)") == 2040, "name memparse used", "sysfs.c:2040")
    report(find(s243, r"skip_spaces\(endptr\)") == 2042, "name skip_spaces used", "sysfs.c:2042")
    report(find(s237, r"BTRFS_IOC_SCRUB_CANCEL") == 421, "name BTRFS_IOC_SCRUB_CANCEL used", "r42 scrub.c:421")
    # sysfs path: devinfo_kobj <- devid_kobj named "%llu"; fsid_kobj is the /sys/fs/btrfs/<fsid> node
    report(at(s243, 2165).strip() == "ret = kobject_init_and_add(&device->devid_kobj, &devid_ktype,"
           and at(s243, 2166).strip() == 'devinfo_kobj, "%llu", device->devid);'
           and at(s243, 36).strip() == "* devid_attrs				/sys/fs/btrfs/<uuid>/devinfo/<devid>",
           "SR8 'devinfo/<devid>/scrub_speed_max under /sys/fs/btrfs/<fsid>/'",
           "sysfs.c:36, 2165-2166")


def main():
    verify_digests()
    doc = load_doc()
    print(f"\ndoc {DOC}@{REV[:12]}: {len(doc)} lines")
    pass_a(doc)
    pass_b()
    pass_c()
    pass_d()
    print(f"\nRESULT: {'ALL CHECKS PASS' if fail == 0 else str(fail) + ' CHECK(S) FAILED'}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
```

## Appendix B — the output

The script checks only what the frozen snapshots can settle, so its `RESULT: ALL CHECKS PASS` and this report's
`VERDICT: defect-found` are not in conflict: F1 lives in a file that is not in the frozen set and was found by the
separate live fetch recorded in `live-aux.txt`.

```
== pass 0: digest verification ==
  PASS  .ufo/waves/round-44/frozen/src/scrub.c  | expected f347931b795c738d… got f347931b795c738d…
  PASS  .ufo/waves/round-44/frozen/src/sysfs.c  | expected ce146120f29ac29c… got ce146120f29ac29c…
  PASS  .ufo/waves/round-44/frozen/src/btrfs-scrub@.timer  | expected 9a0b6cc23f7bd97b… got 9a0b6cc23f7bd97b…
  PASS  .ufo/waves/round-44/frozen/src/btrfs-scrub@.service  | expected eaa7af92d28bfa89… got eaa7af92d28bfa89…
  PASS  .ufo/waves/round-44/frozen/src/PKGBUILD  | expected 3b803e8b05d84900… got 3b803e8b05d84900…
  PASS  .ufo/waves/round-42/frozen/src/scrub.c  | expected 48df2e2f468f7db7… got 48df2e2f468f7db7…
  PASS  .ufo/waves/round-42/frozen/src/CHANGES  | expected bd881ab899ba4f4f… got bd881ab899ba4f4f…
  PASS  .ufo/waves/round-43/frozen/src/ioctl.c  | expected 7b3488f2f8356313… got 7b3488f2f8356313…
  info  .ufo/waves/round-44/frozen/hostcap/capture.txt sha256 efb523889035cba62235d904b9e254068a7083dd07e7bb338ce2a803a3e84900

doc corpus/knowledge/btrfs-scrub-record-r44.md@7e081698d4fc: 145 lines

== pass A: every **Quote.** line against its snapshot ==
  PASS  doc:30 S242 scrub.c:3081
  PASS  doc:32 S242 scrub.c:3147
  PASS  doc:34 S242 scrub.c:3153
  PASS  doc:36 S242 scrub.c:3159
  PASS  doc:38 S242 scrub.c:3222
  PASS  doc:40 S242 scrub.c:3321
  PASS  doc:42 S242 scrub.c:3331
  PASS  doc:44 S242 scrub.c:3333
  PASS  doc:46 S242 scrub.c:3336
  PASS  doc:48 S240 ioctl.c:3139
  PASS  doc:50 S240 ioctl.c:3141
  PASS  doc:65 S243 sysfs.c:72
  PASS  doc:67 S243 sysfs.c:74
  PASS  doc:69 S243 sysfs.c:2028
  PASS  doc:71 S243 sysfs.c:2040
  PASS  doc:73 S243 sysfs.c:2042
  PASS  doc:75 S243 sysfs.c:2044
  PASS  doc:77 S243 sysfs.c:2048
  PASS  doc:79 S242 scrub.c:1380
  PASS  doc:81 S242 scrub.c:1381
  PASS  doc:98 S244 PKGBUILD:100
  PASS  doc:100 S244 PKGBUILD:101
  PASS  doc:102 S244 btrfs-scrub@.timer:5
  PASS  doc:104 S244 btrfs-scrub@.timer:7
  PASS  doc:106 S244 btrfs-scrub@.timer:8
  PASS  doc:108 S244 btrfs-scrub@.timer:11
  PASS  doc:110 S244 btrfs-scrub@.service:9
  PASS  doc:112 S244 btrfs-scrub@.service:10
  PASS  doc:114 S237 scrub.c:1293
  PASS  doc:116 S237 scrub.c:1295
  PASS  doc:118 S237 scrub.c:421
  PASS  doc:120 S237 scrub.c:1546
  PASS  doc:122 S237 scrub.c:969
  note  doc:65 S243 sysfs.c:72 quote is a strict prefix of the line (dropped tail '\t\t\t\\', no ellipsis)
  PASS  quote line count = 33 (doc has 33)

== pass B: Statement-cell line/function claims ==
 SR7
  PASS  SR7 'refuses ... when dev->scrub_ctx is already set' guard at scrub.c:3147  | if (dev->scrub_ctx ||
  PASS  SR7 -EINPROGRESS at scrub.c:3153 inside that guard  | guard 3147..3154
  PASS  SR7 function btrfs_scrub_dev defined  | scrub.c:3079
  PASS  SR7 'attaches its own context before the scrub starts'  | attach scrub.c:3159 < first scrub work scrub.c:3193
  PASS  SR7 'sets dev->scrub_ctx back to NULL when it ends'  | detach scrub.c:3222 > last scrub work scrub.c:3215
  PASS  SR7 'looks the requested devid up under device_list_mutex'  | progress@3321 lock@3328 find@3329 unlock@3334
  PASS  SR7 'copies that context's stat' at scrub.c:3333  | memcpy(progress, &sctx->stat, sizeof(*progress));
  PASS  SR7 0/-ENOTCONN/-ENODEV return at scrub.c:3336  | return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;
  PASS  SR7 ioctl handler: CAP_SYS_ADMIN gate before the call  | handler@3126 gate@3132 call@3139 copy_to_user@3141
  PASS  SR7 'copies the arguments back only when it is 0' at ioctl.c:3141  | if (ret == 0 && copy_to_user(arg, sa, sizeof(*sa)))
 SR8
  PASS  SR8 BTRFS_ATTR_RW declared at sysfs.c:72  | #define BTRFS_ATTR_RW(_prefix, _name, _show, _store)			\
  PASS  SR8 mode 0644 built at sysfs.c:74  | __INIT_KOBJ_ATTR(_name, 0644, _show, _store)
  PASS  SR8 decimal + newline read at sysfs.c:2028  | return sysfs_emit(buf, "%llu\n", READ_ONCE(device->scrub_speed_max));
  PASS  SR8 store order memparse -> skip_spaces -> -EINVAL  | memparse@2040 skip_spaces@2042 EINVAL@2044
  PASS  SR8 'rejects anything else after the number' at sysfs.c:2043  | if (*endptr != 0)
  PASS  SR8 attribute registration at sysfs.c:2048  | BTRFS_ATTR_RW(devid, scrub_speed_max, btrfs_devinfo_scrub_speed_max_show,
  PASS  SR8 throttle reads scrub_speed_max and returns at once when 0  | fn@1371 read@1380 zero@1381 return@1382
 SR9
  PASS  SR9 PKGBUILD:100 installs the service  | install -Dm644 btrfs-scrub@.service "${pkgdir}/usr/lib/systemd/system/btrfs-scrub@.service"
  PASS  SR9 PKGBUILD:101 installs the timer  | install -Dm644 btrfs-scrub@.timer "${pkgdir}/usr/lib/systemd/system/btrfs-scrub@.timer"
  PASS  SR9 '-B' keeps foreground (do_background=false) and sets do_print  | case 'B'@1292..1296
  PASS  SR9 SIGINT handler installed by scrub_handle_sigint_child  | scrub.c:439
  PASS  SR9 handler issues BTRFS_IOC_SCRUB_CANCEL  | scrub.c:421
  PASS  SR9 foreground start calls scrub_handle_sigint_child(fdmnt)  | do_background@1512 fg call@1546 background call@1710
  PASS  SR9 canceled set from the scrub ioctl return  | ioctl@965 canceled@969

== pass C (extra): Host reading cell pointers into capture.txt ==
  PASS  capture.txt has at least 9 lines  | 9 lines
  PASS  capture.txt:1 'no effective capabilities'  | captured 2026-10-26T23:53:22Z uid=1000 CapEff=0000000000000000
  PASS  capture.txt:4 devid 1 scrub_speed_max mode=644 owner=root value=0  | scrub_speed_max 1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/scrub_speed_max mode=644 owner=root value=0
  PASS  capture.txt:5 no timers.target.wants link  | wants_btrfs_scrub_instances 0
  PASS  capture.txt:6 instance disabled  | is_enabled_btrfs-scrub@-.timer disabled
  PASS  capture.txt:7,8 installed units byte-identical to the pinned digests  | installed_unit 9a0b6cc23f7bd97b83b6c38dd / installed_unit eaa7af92d28bfa8940bb55156
  PASS  capture.txt:9 package ownership  | pacman_owner /usr/lib/systemd/system/btrfs-scrub@.timer is owned by btrfs-progs 7.1-1

== pass D (extra): function names and sysfs path named in the statements ==
  PASS  name btrfs_scrub_dev defined  | scrub.c:3079
  PASS  name btrfs_scrub_progress defined  | scrub.c:3321
  PASS  SR7 'its is_dev_replace argument' in the signature  | scrub.c:3081
  PASS  SR7 'serves both a scrub and a device replace' — is_dev_replace branches in the body  | 7 uses: lines [3081, 3109, 3121, 3127, 3148, 3180, 3217]
  PASS  SR7's SR6 referent is_scrub_running_in_kernel answers 1 on the first 0  | fn@1190 ioctl@1200 -> return 1
  PASS  name BTRFS_ATTR_RW defined  | sysfs.c:72
  PASS  name memparse used  | sysfs.c:2040
  PASS  name skip_spaces used  | sysfs.c:2042
  PASS  name BTRFS_IOC_SCRUB_CANCEL used  | r42 scrub.c:421
  PASS  SR8 'devinfo/<devid>/scrub_speed_max under /sys/fs/btrfs/<fsid>/'  | sysfs.c:36, 2165-2166

RESULT: ALL CHECKS PASS
```
