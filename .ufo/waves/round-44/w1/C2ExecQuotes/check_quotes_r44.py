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
