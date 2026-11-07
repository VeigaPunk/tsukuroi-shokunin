#!/usr/bin/env python3
"""Round-89 battery for a Limine v12.9.4 path-pin gate (tsukuroi lane; successor of the r88 battery).

What it decides: whether a gate `GATE --conf FILE --esp DIR [--secure-boot-enforced 0|1]` follows
the Limine v12.9.4 pin rule set R1-R7 below and the reporting contract R8, for each of the
families in FAMILY_ROSTER, on fixtures generated fresh per run with OS-entropy names, bytes and
layouts, the whole case list shuffled per run; every case must return exactly the expected
(rc, verdict, sorted per-pin (line, status, consequence)) within 20 s, plus R8's optional fields.
Verdict `met` only when every family in the literal FAMILY_ROSTER passed every case.

Round-89 claim (C1, SCORECARD.md "Round 89 — declaration"; surface: battery calibration of the
`limine-pins` gate): this battery is judged by the frozen counter tools/battery-discrimination-r89.py
over a frozen roster of 3 correct and 62 deviant gates, each handed over as an opaque launcher. The
r88 families stay; the twelve added in r89 each certify a written clause the r88 battery left
unexercised (r88 lesson routed R88-R2, R88-R3, R88-R5; CriticForgers f01 f03 f06 f07 f08 f12 f14 f16
f18 f19, MutHeldOut h01 h10 h11 h19 h20, r88 g00, m31): BLANK-CLASS, OPTIONAL-MISSING,
OPTIONAL-UNRESOLVED, EMPTY-PIN-LIST, DOUBLE-DOLLAR, ENTRY-LABEL-EDGES, PANIC-VALUE-BLANKS,
CR-INTERNAL, RESOURCE-CASE, KEY-EQUALS, EMPTY-PATH, OPTIONAL-KEY-CASE. WHITESPACE-CRLF now writes
CRLF in every case (r88 drew it with p 0.6, so a CR-blind gate escaped a run with p ~2.6 %), and
the selftest adds a one-field lie on hash_mismatch_panic.value (r88 MutBattery M18).

RULE SET (the r87 frozen R1-R7, unchanged in substance; r89 states explicitly what the r88 text
left implicit, each from the same pinned lines; sources .ufo/waves/round-87/before/src/, Limine tag
v12.9.4, byte-identical to the v12.9.4 tag clone re-opened in r89):
  R1 key lines (common/lib/config.c raw 527-551 remove EVERY CR anywhere in the file and the
     leading/trailing blanks of each line, blanks being space and tab only; config_get_value raw
     778-818 matches a key case-insensitively, only at the start of a line, followed directly by
     ':' and skips blanks after ':'): a line is `KEY: value` when, after removing every CR and the
     leading spaces/tabs, it starts with letters/underscores then ':' (not '=', not a blank). A
     line whose first non-blank character is '#' is not a key line; a line that starts with any
     other character (a form feed, a vertical tab) is not a key line either. The value is the rest
     of the line with leading spaces/tabs removed and trailing spaces/tabs removed; any other
     trailing character (a vertical tab, a form feed) stays in the value.
  R2 pins (common/lib/uri.c uri_resolve raw 28-104; CONFIG.md raw 111-113, 134, 210, 295-308,
     330-350 name the path-valued keys): a key line whose key is one of path, kernel_path,
     image_path, module_path, dtb_path, global_dtb, wallpaper, term_font (case-insensitive) is a
     pin when its value has the URI form `[$]resource(root):/path#hash` - a '(' then, later, '):/'
     then, later, a '#'. The hash is the text after the LAST '#'; the path is the text between
     the first '):/' and that '#' and may be empty (an empty path is still a pin). Any other key,
     a value with no '#' after '):/', or a value with no URI form, is not a pin and is ignored.
  R3 hash format (uri.c raw 89-101): the hash must be exactly 128 characters of [0-9a-fA-F];
     otherwise status LP-HASH-FORMAT (checked before resolution).
  R4 resolution (uri.c raw 344-362): ONE leading '$' (gzip marker) is dropped from the resource;
     the resource name is then compared case-sensitively (strcmp): only `boot` with an empty root
     resolves, to ESP/path. Any other resource (`$boot` left by `$$boot`, `BOOT`, `Boot`), or a
     non-empty root (boot(2), guid(...), uuid(...), fslabel(...), hdd, odd, tftp) -> LP-UNRESOLVED.
  R5 comparison (uri.c raw 378-383, 403-470, 483-487, 662-664; CONFIG.md raw 458-462): no regular
     file at ESP/path (absent, or the path names a directory such as the ESP itself) -> LP-MISSING;
     otherwise BLAKE2b-512 of the file's raw bytes as stored (gzip files are NOT decompressed)
     compared with the hash case-insensitively -> OK or LP-MISMATCH.
  R6 consequence per pin (uri.c raw 18-26, 301-319, 693-710; common/menu.c raw 1711-1717;
     CONFIG.md raw 152-156): OK -> `none`; LP-MISSING and LP-UNRESOLVED -> `not-modelled`;
     for LP-MISMATCH and LP-HASH-FORMAT: key `wallpaper` or `term_font`, matched case-insensitively
     like every key (optional resources)
     -> `skip`; else LP-HASH-FORMAT -> `panic`; else LP-MISMATCH -> `panic` when
     --secure-boot-enforced 1, else `prompt` when the FIRST `hash_mismatch_panic` key line in
     the whole file (R1 rules) has a value equal to `no` case-insensitively, else `panic`.
  R7 verdict: any LP-MISMATCH, LP-MISSING or LP-HASH-FORMAT -> DEGRADED rc 1; else any
     LP-UNRESOLVED -> CANNOT-EVALUATE rc 2; else HEALTHY rc 0 (also when the file holds no pin at
     all). An unreadable --conf (absent, a directory, or unreadable for any OS reason) ->
     CANNOT-EVALUATE rc 2 with an empty pin list. `--secure-boot-enforced 0` and an absent flag
     both mean "not enforced".
  R8 reporting contract (the lane gate's own output, not Limine behaviour): a pin record MAY
     carry "entry"; when it does, it equals the label of the nearest preceding entry line (a
     line whose first non-blank character is '/'; label = the line without its leading '/'
     characters, then without a leading '+' (no fixture starts a label with '++'), then trimmed of
     spaces/tabs at both ends; a trailing '+' stays), or null before any entry line. The top-level object MAY carry
     "hash_mismatch_panic"; when it does, it is null if no `hash_mismatch_panic` key line exists
     (R1 rules), else {"line": the 1-based line of the FIRST such key line, "value": its R1 value,
     i.e. without leading or trailing blanks} (value compared case-insensitively).

GATE OUTPUT CONTRACT (stdout, one JSON object): {"verdict": str, "rc": int,
  "pins": [{"line": int (1-based physical line), "status": str, "consequence": str, ...}, ...]}.
  The process exit code must equal "rc". Other extra keys are allowed and ignored.

Not modelled (limits, not families): macro expansion (`${NAME}`), Secure Boot's "unhashed path
panics" rule, per-protocol behaviour of a missing file, a cmdline value that is itself URI-shaped,
a gate that behaves differently on its own bytes or file name.

Fixtures carry no answer: random file and directory names (history names too: no content digest
in any name), no expected value on disk; the conf lives outside the ESP directory; the gate runs
with cwd set to the fixture directory.

Usage: limine-pin-battery-r89.py --gate PATH [--runs N] [--work DIR] [--json OUT]
       limine-pin-battery-r89.py --selftest
Exit: 0 met; 1 unmet; 2 usage/could-not-evaluate (also: FAMILIES differs from FAMILY_ROSTER).
"""
import argparse
import gzip
import hashlib
import json
import os
import random
import secrets
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TIMEOUT = 20
HEX = "0123456789abcdef"


def b2(data):
    return hashlib.blake2b(data).hexdigest()


def rname(rng, ext=".efi"):
    return "".join(rng.choice("abcdefghijklmnopqrstuvwxyz0123456789_-") for _ in range(rng.randint(5, 14))) + ext


def flip_last(h):
    c = h[-1]
    return h[:-1] + ("0" if c != "0" else "1")


def flip_first(h):
    c = h[0]
    return ("f" if c != "f" else "e") + h[1:]


class Case:
    """A fixture under construction: conf lines, ESP files, expected pins."""

    def __init__(self, family, rng):
        self.family = family
        self.rng = rng
        self.lines = []          # physical lines (without newline)
        self.files = {}          # relpath -> bytes
        self.expect = []         # (line, status, consequence)
        self.sb = False
        self.sbflag = None       # None: flag absent; "0"/"1": passed explicitly (sb mirrors "1")
        self.eol = "\n"
        self.conf_missing = False
        self.conf_dir = False    # --conf names a directory (unreadable as a file)
        self.panic_value = None  # value of first hash_mismatch_panic, None = absent

    def add(self, text):
        self.lines.append(text)
        return len(self.lines)

    def blob(self, n=None):
        return secrets.token_bytes(n or self.rng.randint(64, 4096))

    def newfile(self, data=None, sub=None):
        rng = self.rng
        parts = [rname(rng, "") for _ in range(rng.randint(0, 2))] if sub is None else sub
        rel = "/".join(parts + [rname(rng)])
        self.files[rel] = data if data is not None else self.blob()
        return rel

    def header(self):
        rng = self.rng
        self.add("timeout: %d" % rng.randint(0, 9))
        if rng.random() < 0.5:
            self.add("### generated header %s" % secrets.token_hex(4))

    def entry(self, label=None, depth=1):
        self.add("%s%s%s" % ("  " * (depth - 1), "/" * depth, label or rname(self.rng, "")))
        self.add("%sprotocol: efi" % ("  " * (depth - 1)))

    def r1_panic(self):
        """R1 scan for the FIRST hash_mismatch_panic key line: (line, value) or None."""
        for n, raw in enumerate(self.lines, 1):
            line = raw.replace("\r", "").strip(" \t")
            if not line or line[0] == "#":
                continue
            i = 0
            while i < len(line) and (line[i].isascii() and (line[i].isalpha() or line[i] == "_")):
                i += 1
            if i == 0 or i >= len(line) or line[i] != ":":
                continue
            if line[:i].lower() == "hash_mismatch_panic":
                return n, line[i + 1:].lstrip(" \t")
        return None

    def r8_entries(self):
        """R8: label of the nearest preceding entry line for every physical line."""
        out, cur = {}, None
        for n, raw in enumerate(self.lines, 1):
            s = raw.replace("\r", "").strip(" \t")
            if s.startswith("/"):
                label = s.lstrip("/").lstrip("+").strip()
                cur = label or cur
            out[n] = cur
        return out

    def mismatch_consequence(self, key):
        if key.lower() in ("wallpaper", "term_font"):
            return "skip"
        if self.sb:
            return "panic"
        p = self.r1_panic()
        if p is not None and p[1].lower() == "no":
            return "prompt"
        return "panic"

    def pin(self, status, key="path", indent="  ", resource="boot()", data=None, hashfmt=None,
            rel=None, gz=False):
        """Append one pin line; record its expectation (consequence resolved at finish())."""
        if rel is None:
            rel = self.newfile(data)
        content = self.files.get(rel)
        good = b2(content) if content is not None else secrets.token_hex(64)
        if status == "OK":
            h = good
        elif status == "LP-MISMATCH":
            h = flip_last(good) if self.rng.random() < 0.5 else flip_first(good)
        elif status == "LP-MISSING":
            h = good
            self.files.pop(rel, None)
        elif status == "LP-HASH-FORMAT":
            h = hashfmt
        elif status == "LP-UNRESOLVED":
            h = good
        else:
            raise ValueError(status)
        if hashfmt is not None and status != "LP-HASH-FORMAT":
            h = hashfmt(h) if callable(hashfmt) else hashfmt
        uri = "%s%s:/%s#%s" % ("$" if gz else "", resource, rel, h)
        ln = self.add("%s%s: %s" % (indent, key, uri))
        self.expect.append([ln, status, key])
        return ln

    def finish(self):
        out = []
        for ln, status, key in self.expect:
            if status == "OK":
                cons = "none"
            elif status in ("LP-MISSING", "LP-UNRESOLVED"):
                cons = "not-modelled"
            elif status == "LP-HASH-FORMAT":
                cons = "skip" if key.lower() in ("wallpaper", "term_font") else "panic"
            else:
                cons = self.mismatch_consequence(key)
            out.append((ln, status, cons))
        statuses = {s for _, s, _ in out}
        if self.conf_missing or self.conf_dir:
            return 2, "CANNOT-EVALUATE", []
        if statuses & {"LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT"}:
            rc, verdict = 1, "DEGRADED"
        elif "LP-UNRESOLVED" in statuses:
            rc, verdict = 2, "CANNOT-EVALUATE"
        else:
            rc, verdict = 0, "HEALTHY"
        return rc, verdict, sorted(out)

    def meta(self):
        """R8 expectations: {line: entry label} for every expected pin, and the first panic line."""
        ent = self.r8_entries()
        return {ln: ent.get(ln) for ln, _, _ in self.expect}, self.r1_panic()


def set_panic(c, value, indent="", key="hash_mismatch_panic"):
    c.add("%s%s: %s" % (indent, key, value))
    if c.panic_value is None:
        c.panic_value = value.strip()


def fam_positive(c):
    c.header()
    for _ in range(c.rng.randint(2, 5)):
        c.entry()
        c.pin("OK")
        c.add("  cmdline: quiet root=UUID=%s" % secrets.token_hex(8))


def fam_mismatch(c, late):
    c.header()
    n = c.rng.randint(2, 4)
    bad = c.rng.randrange(n)
    for i in range(n):
        c.entry()
        if i == bad:
            rel = c.newfile()
            good = b2(c.files[rel])
            h = flip_last(good) if late else flip_first(good)
            ln = c.add("  path: boot():/%s#%s" % (rel, h))
            c.expect.append([ln, "LP-MISMATCH", "path"])
        else:
            c.pin("OK")


def fam_missing(c):
    c.header()
    c.entry()
    c.pin("OK")
    c.entry()
    c.pin("LP-MISSING")


def fam_hash_short(c):
    c.header()
    c.entry()
    c.pin("OK")
    c.entry()
    n = c.rng.choice([127, 129, 64, 0])
    c.pin("LP-HASH-FORMAT", hashfmt=secrets.token_hex(65)[:n])


def fam_hash_nonhex(c):
    c.header()
    c.entry()
    h = list(secrets.token_hex(64))
    h[c.rng.randrange(128)] = c.rng.choice("gxzG -_")
    c.pin("LP-HASH-FORMAT", hashfmt="".join(h))
    c.entry()
    c.pin("OK")


def fam_hash_upper(c):
    c.header()
    for _ in range(c.rng.randint(1, 3)):
        c.entry()
        c.pin("OK", hashfmt=lambda h: h.upper() if c.rng.random() < 0.5 else
              "".join(ch.upper() if c.rng.random() < 0.5 else ch for ch in h))


def fam_comment_decoy(c):
    c.header()
    c.entry()
    rel = c.newfile()
    c.add("#path: boot():/%s#%s" % (rel, flip_last(b2(c.files[rel]))))
    c.add("  # path: boot():/%s#%s" % (rel, secrets.token_hex(64)))
    c.add("\t#module_path: boot():/%s#%s" % (c.newfile(), secrets.token_hex(64)))
    c.pin("OK", rel=rel)
    c.add("comment: path: boot():/%s#%s" % (rname(c.rng), secrets.token_hex(64)))


def fam_key_case(c):
    c.header()
    c.entry()
    c.pin("LP-MISMATCH", key=c.rng.choice(["PATH", "Path", "pAtH"]))
    c.entry()
    c.pin("OK", key=c.rng.choice(["MODULE_PATH", "Module_Path", "KERNEL_PATH", "Image_Path", "DTB_path"]))
    c.entry()
    c.pin("LP-MISMATCH", key=c.rng.choice(["kernel_path", "image_path", "dtb_path", "global_dtb"]))


def fam_whitespace(c):
    c.header()
    c.entry()
    rel = c.newfile()
    ln = c.add("\t \tpath:\t  boot():/%s#%s \t " % (rel, b2(c.files[rel])))
    c.expect.append([ln, "OK", "path"])
    c.entry()
    rel2 = c.newfile()
    ln = c.add("path:boot():/%s#%s  " % (rel2, flip_last(b2(c.files[rel2]))))
    c.expect.append([ln, "LP-MISMATCH", "path"])
    c.eol = "\r\n"  # r89: every case (r88 drew CRLF with p 0.6; routed R88-R2)


def fam_last_hash(c):
    c.header()
    c.entry()
    rel = "%s#%s" % (rname(c.rng, ""), rname(c.rng))
    c.files[rel] = c.blob()
    c.pin("OK", rel=rel)
    c.entry()
    rel2 = "%s#x/%s" % (rname(c.rng, ""), rname(c.rng))
    c.files[rel2] = c.blob()
    c.pin("LP-MISMATCH", rel=rel2)


def fam_gz_raw(c):
    c.header()
    c.entry()
    payload = c.blob(c.rng.randint(200, 2000))
    rel = c.newfile(gzip.compress(payload, mtime=0))
    c.pin("OK", key="module_path", rel=rel, gz=True)
    c.entry()
    rel2 = c.newfile(gzip.compress(c.blob(300), mtime=0))
    # pinned to the hash of the DECOMPRESSED bytes: Limine hashes stored bytes, so this mismatches
    ln = c.add("  module_path: $boot():/%s#%s" % (rel2, b2(gzip.decompress(c.files[rel2]))))
    c.expect.append([ln, "LP-MISMATCH", "module_path"])


def fam_unresolved(c):
    c.header()
    c.entry()
    c.pin("OK")
    c.entry()
    res = c.rng.choice(["boot(2)", "guid(%s)" % secrets.token_hex(4), "uuid(%s)" % secrets.token_hex(4),
                        "fslabel(ESP)", "hdd(1:2)", "odd(1:1)"])
    c.pin("LP-UNRESOLVED", resource=res)


def fam_panic_default(c):
    c.header()
    c.entry()
    c.pin("LP-MISMATCH")
    c.entry()
    c.pin("OK")


def fam_panic_no_only(c):
    c.header()
    yes_no = c.rng.random() < 0.5
    val = c.rng.choice(["no", "No", "NO", "nO"]) if yes_no else c.rng.choice(["off", "false", "0", "nope", "yes", "n"])
    set_panic(c, val)
    c.entry()
    c.pin("LP-MISMATCH")
    c.entry()
    c.pin("OK")


def fam_panic_first(c):
    c.header()
    first = c.rng.choice(["no", "yes"])
    set_panic(c, first)
    c.entry()
    set_panic(c, "yes" if first == "no" else "no", indent="  ")
    c.pin("LP-MISMATCH")


def fam_secureboot(c):
    c.sb = True
    c.header()
    set_panic(c, "no")
    c.entry()
    c.pin("LP-MISMATCH")
    c.entry()
    c.pin("OK")


def fam_optional_skip(c):
    c.header()
    set_panic(c, c.rng.choice(["yes", "no"]))
    key = c.rng.choice(["wallpaper", "term_font"])
    rel = c.newfile()
    ln = c.add("%s: boot():/%s#%s" % (key, rel, flip_last(b2(c.files[rel]))))
    c.expect.append([ln, "LP-MISMATCH", key])
    c.add("backdrop: 1a1b26")
    c.entry()
    c.pin("OK")


def fam_multi(c):
    c.header()
    if c.rng.random() < 0.5:
        set_panic(c, "no")
    kinds = ["LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT", "LP-UNRESOLVED", "OK", "LP-MISMATCH"]
    c.rng.shuffle(kinds)
    for k in kinds:
        c.entry()
        if k == "LP-HASH-FORMAT":
            c.pin(k, hashfmt=secrets.token_hex(32))
        elif k == "LP-UNRESOLVED":
            c.pin(k, resource="guid(%s)" % secrets.token_hex(4))
        else:
            c.pin(k)


def fam_unhashed_decoys(c):
    c.header()
    c.entry()
    c.add("  path: boot():/%s" % c.newfile())
    c.add("  cmdline: root=/dev/x foo#%s rd.x=%s" % (secrets.token_hex(64), secrets.token_hex(3)))
    c.add("  comment: see %s#%s" % (rname(c.rng), secrets.token_hex(64)))
    c.add("  image_path: %s#%s" % (rname(c.rng), secrets.token_hex(64)))
    c.add("  kernel_cmdline: x=boot():/%s#%s" % (rname(c.rng), secrets.token_hex(64)))
    c.add("  %s: boot():/%s#%s" % (c.rng.choice(["module_string", "comment", "backdrop"]),
                                   rname(c.rng), secrets.token_hex(64)))
    c.pin("OK")
    c.entry()
    c.add("  module_path: boot():/%s" % c.newfile())


def fam_malformed_input(c):
    c.header()
    c.entry()
    c.pin("OK")
    c.conf_missing = True


HOST_TEMPLATE = None


def fam_host_shape(c):
    """The host's limine.conf shape at the r87 freeze (receipt .ufo/waves/round-87/before/host/):
    one global hash_mismatch_panic: no, two kernel entries whose pins mismatch, a Snapshots
    directory with three history pins (OK, or a stale copied pin: r88 C2), and an unhashed
    fallback EFI path."""
    rng = c.rng
    set_panic(c, "no")
    c.add("default_entry: 2")
    c.add("interface_branding: Omarchy Bootloader")
    c.add("/+Omarchy")
    c.add("comment: machine-id=%s order-priority=50" % secrets.token_hex(16))
    for k in ("linux", "linux-lts"):
        c.add("  //%s" % k)
        c.add("  comment: kernel-id=%s" % k)
        c.add("  protocol: efi")
        c.pin("LP-MISMATCH", rel=c.newfile(sub=["EFI", "Linux"]))
        c.add("  cmdline: resume=/dev/mapper/root resume_offset=%d quiet" % rng.randint(1, 10 ** 7))
    c.add("    //Snapshots")
    mid = secrets.token_hex(16)
    for _ in range(3):
        c.add("     ///2026-10-20 09:%02d:%02d" % (rng.randrange(60), rng.randrange(60)))
        c.add("     ////linux")
        c.add("     protocol: efi")
        data = c.blob()
        # r87 routed R87-R2: the host names history files by content digest; here the digest
        # field is random, so a name never carries the answer.
        name = "omarchy_linux.efi_sha256_%s" % secrets.token_hex(32)
        rel = "%s/limine_history/%s" % (mid, name)
        c.files[rel] = data
        c.pin(c.rng.choice(["OK", "OK", "LP-MISMATCH"]), rel=rel, indent="     ")
    c.add("/EFI fallback")
    c.add("protocol: efi")
    c.add("path: boot():/EFI/BOOT/%s" % c.newfile(sub=["EFI", "BOOT"]).split("/")[-1])


def bad_hash(c):
    """A hash that fails R3: wrong length (127, 129, 64, 0) or a non-hex character."""
    if c.rng.random() < 0.5:
        return secrets.token_hex(65)[:c.rng.choice([127, 129, 64, 0])]
    h = list(secrets.token_hex(64))
    h[c.rng.randrange(128)] = c.rng.choice("gxzG-_")
    return "".join(h)


def decoy(c, fmt):
    """Add a non-pin line naming a real file with a wrong hash (a gate that takes it as a pin errs)."""
    rel = c.newfile()
    c.add(fmt % (rel, flip_last(b2(c.files[rel]))))


def fam_key_spacing(c):
    """R1: the key is letters/underscores followed DIRECTLY by ':'; blanks before ':', digits or
    '-' make the line a non-key line (r87 forger g01)."""
    c.header()
    c.entry()
    decoy(c, "  path : boot():/%s#%s")
    decoy(c, "  module_path\t: boot():/%s#%s")
    decoy(c, "  kernel-path: boot():/%s#%s")
    decoy(c, "  path2: boot():/%s#%s")
    c.pin("OK")
    c.entry()
    c.pin("LP-MISMATCH")


def fam_no_paren(c):
    """R2: a value without '(' ... '):/' is not a URI, so not a pin (r87 forger g02)."""
    c.header()
    c.entry()
    decoy(c, "  path: boot:/%s#%s")
    decoy(c, "  module_path: $boot:/%s#%s")
    decoy(c, "  image_path: boot)/:/%s#%s")
    c.pin("OK")


def fam_format_before_resolve(c):
    """R3 before R4: a bad hash on an unresolvable resource is LP-HASH-FORMAT (r87 forger g03)."""
    c.header()
    c.entry()
    res = c.rng.choice(["boot(2)", "guid(%s)" % secrets.token_hex(4), "uuid(%s)" % secrets.token_hex(4),
                        "fslabel(ESP)", "hdd(1:2)", "odd()"])
    c.pin("LP-HASH-FORMAT", resource=res, hashfmt=bad_hash(c))
    c.entry()
    c.pin("OK")


def fam_optional_hash_format(c):
    """R6: wallpaper/term_font with an LP-HASH-FORMAT hash -> skip, not panic (r87 forger g04)."""
    c.header()
    set_panic(c, c.rng.choice(["yes", "no"]))
    for key in ("wallpaper", "term_font"):
        c.pin("LP-HASH-FORMAT", key=key, indent="", hashfmt=bad_hash(c))
    c.entry()
    c.pin("OK")


def fam_first_uri_sep(c):
    """R2: the path starts after the FIRST '):/' (a stored path may contain '):/') (r87 forger g05)."""
    c.header()
    for status in ("OK", "LP-MISMATCH"):
        c.entry()
        rel = "%s):/%s" % (rname(c.rng, ""), rname(c.rng))
        c.files[rel] = c.blob()
        c.pin(status, rel=rel)


def fam_paren_path(c):
    """R2: the resource ends at the FIRST '('; a stored path may contain '(' and ')' (r87 MutGate m05)."""
    c.header()
    for status, key in (("OK", "path"), ("LP-MISMATCH", "kernel_path")):
        c.entry()
        rel = "EFI/Linux/%s(%d).efi" % (rname(c.rng, ""), c.rng.randrange(10))
        c.files[rel] = c.blob()
        c.pin(status, key=key, rel=rel)


def fam_empty_root_resource(c):
    """R4: only resource `boot` resolves; another resource with an EMPTY root is LP-UNRESOLVED
    (r87 forger g06)."""
    c.header()
    c.entry()
    c.pin("LP-UNRESOLVED", resource=c.rng.choice(["hdd()", "odd()", "guid()", "uuid()", "fslabel()",
                                                  "tftp()", "bootx()", "Boot2()"]))
    c.entry()
    c.pin("OK")


def fam_root_on_boot(c):
    """R4: resource `boot` with a NON-empty root is LP-UNRESOLVED, gzip marker or not (r87 MutGate m10)."""
    c.header()
    c.entry()
    c.pin("LP-UNRESOLVED", resource="boot(%d)" % c.rng.randint(1, 9), gz=c.rng.random() < 0.5)
    c.entry()
    c.pin("OK")


def fam_panic_key_case(c):
    """R1/R6: the hash_mismatch_panic key matches case-insensitively (r87 forger g07)."""
    c.header()
    set_panic(c, c.rng.choice(["no", "NO", "No"]),
              key=c.rng.choice(["HASH_MISMATCH_PANIC", "Hash_Mismatch_Panic", "hash_MISMATCH_panic"]))
    c.entry()
    c.pin("LP-MISMATCH")
    c.entry()
    c.pin("OK")


def fam_sb_flag_zero(c):
    """R6/R7: `--secure-boot-enforced 0` is not enforcement (r87 forger g08)."""
    c.sbflag = "0"
    c.header()
    set_panic(c, "no")
    c.entry()
    c.pin("LP-MISMATCH")
    c.entry()
    c.pin("OK")


def fam_panic_raw_decoy(c):
    """R6: only a KEY LINE sets hash_mismatch_panic; a '#' line or another key's value does not
    (r87 forger g10)."""
    c.header()
    c.add(c.rng.choice(["# hash_mismatch_panic: no", "  #hash_mismatch_panic: no"]))
    c.add("comment: hash_mismatch_panic: no")
    if c.rng.random() < 0.5:
        set_panic(c, "yes")
    c.entry()
    c.add("  cmdline: quiet hash_mismatch_panic: no")
    c.pin("LP-MISMATCH")


def fam_conf_unreadable(c):
    """R7: a --conf that exists but cannot be read as a file (a directory) is CANNOT-EVALUATE rc 2
    (r87 forger g14)."""
    c.header()
    c.entry()
    c.pin("OK")
    c.conf_dir = True


def fam_all_pin_keys(c):
    """R2: every one of the eight path keys is a pin, every run (r87 g16's sampled `global_dtb`,
    MutGate m26/m27)."""
    c.header()
    if c.rng.random() < 0.5:
        set_panic(c, c.rng.choice(["yes", "no"]))
    keys = ["path", "kernel_path", "image_path", "module_path", "dtb_path", "global_dtb", "wallpaper",
            "term_font"]
    c.rng.shuffle(keys)
    for key in keys:
        c.entry()
        c.pin(c.rng.choice(["OK", "LP-MISMATCH"]), key=key)


def fam_panic_non_no(c):
    """R6: any value other than `no` keeps the panic, every run (r87 PANIC-NO-ONLY sampled it;
    forger g12)."""
    c.header()
    set_panic(c, c.rng.choice(["off", "false", "0", "nope", "n", "disabled", "none", "no-", "noo"]))
    c.entry()
    c.pin("LP-MISMATCH")
    c.entry()
    c.pin("OK")


def fam_entry_label(c):
    """R8: a reported entry label is the nearest preceding entry line's (r87 MutGate m24)."""
    c.header()
    c.add("/+%s" % rname(c.rng, ""))
    for label, depth in ((rname(c.rng, ""), 2), ("EFI fallback", 1), (rname(c.rng, ""), 3),
                         ("%s %s" % (rname(c.rng, ""), rname(c.rng, "")), 2)):
        c.entry(label, depth)
        c.pin(c.rng.choice(["OK", "LP-MISMATCH"]))


def fam_panic_metadata(c):
    """R8: a reported hash_mismatch_panic names the FIRST key line and its value (r87 MutGate m25)."""
    c.header()
    for _ in range(c.rng.randint(0, 3)):
        c.add("# %s" % secrets.token_hex(4))
    set_panic(c, c.rng.choice(["no", "NO", "No", "yes"]), indent="  ")
    c.entry()
    set_panic(c, "no", indent="  ")
    c.pin("LP-MISMATCH")

# ---- round-89 families (each certifies a clause the r88 battery left unexercised) ----

CONTROL_WS = ("\x0b", "\x0c", "\x1c", "\x1d", "\x1e", "\x1f")


def fam_blank_class(c):
    """R1: blanks are space and tab only. A line led by another whitespace character is not a key
    line, and such a character after the hash stays in the value (129 characters ->
    LP-HASH-FORMAT) (r88 CriticForgers f01)."""
    c.header()
    c.entry()
    rel = c.newfile()
    c.add("%s  path: boot():/%s#%s" % (c.rng.choice(CONTROL_WS), rel, flip_last(b2(c.files[rel]))))
    c.pin("OK")
    c.entry()
    rel2 = c.newfile()
    ln = c.add("  path: boot():/%s#%s%s" % (rel2, b2(c.files[rel2]), c.rng.choice(CONTROL_WS)))
    c.expect.append([ln, "LP-HASH-FORMAT", "path"])


def fam_optional_missing(c):
    """R6: LP-MISSING on wallpaper/term_font is `not-modelled`, not `skip` (r88 CriticForgers f03)."""
    c.header()
    c.pin("LP-MISSING", key=c.rng.choice(["wallpaper", "term_font"]), indent="")
    c.entry()
    c.pin("OK")


def fam_optional_unresolved(c):
    """R6: LP-UNRESOLVED on wallpaper/term_font is `not-modelled`, not `skip` (r88 CriticForgers f16)."""
    c.header()
    c.pin("LP-UNRESOLVED", key=c.rng.choice(["wallpaper", "term_font"]), indent="",
          resource=c.rng.choice(["guid(%s)" % secrets.token_hex(4), "fslabel(%s)" % rname(c.rng, ""),
                                 "boot(%d)" % c.rng.randint(1, 9), "hdd(1:%d)" % c.rng.randint(1, 4)]))
    c.entry()
    c.pin("OK")


def fam_empty_pin_list(c):
    """R7: a file with no pin at all is HEALTHY rc 0 with an empty pin list (r88 CriticForgers f06)."""
    c.header()
    if c.rng.random() < 0.5:
        set_panic(c, c.rng.choice(["yes", "no"]))
    for _ in range(c.rng.randint(1, 3)):
        c.entry()
        c.add("  path: boot():/%s" % c.newfile())
        c.add("  cmdline: quiet rw")


def fam_double_dollar(c):
    """R4: exactly ONE leading '$' is dropped; `$$boot()` leaves resource `$boot`, which is
    LP-UNRESOLVED (r88 CriticForgers f07)."""
    c.header()
    c.entry()
    c.pin("OK", key="module_path", data=gzip.compress(c.blob(300), mtime=0), gz=True)
    c.entry()
    c.pin("LP-UNRESOLVED", resource="$boot()", gz=True)


def fam_entry_label_edges(c):
    """R8: the label drops the leading '/' run and a leading '+', is trimmed at both ends, and keeps
    a trailing '+' (r88 CriticForgers f08, f19; MutHeldOut h19). Every case draws all three."""
    c.header()
    forms = [lambda n: "/+%s" % n, lambda n: "/%s+" % n,
             lambda n: "/%s%s%s %s" % (c.rng.choice(["", "+"]), c.rng.choice([" ", "\t", "  \t"]), n, rname(c.rng, ""))]
    c.rng.shuffle(forms)
    for form in forms:
        depth = c.rng.randint(1, 3)
        c.add("  " * (depth - 1) + "/" * (depth - 1) + form(rname(c.rng, "")))
        c.add("%sprotocol: efi" % ("  " * (depth - 1)))
        c.pin(c.rng.choice(["OK", "LP-MISMATCH"]))


def fam_panic_value_blanks(c):
    """R1/R6/R8: the hash_mismatch_panic value loses its leading and trailing blanks, so
    `no` followed by blanks still prompts, and a reported value is the trimmed one (r88 CriticForgers
    f12; r88 MutBattery M18 / roster m31)."""
    c.header()
    v = c.rng.choice(["no", "No", "NO"])
    c.add("hash_mismatch_panic:%s%s%s" % (c.rng.choice([" ", "\t", "  "]), v,
                                          c.rng.choice([" ", "\t", " \t ", "   "])))
    c.panic_value = v
    c.entry()
    c.pin("LP-MISMATCH")
    c.entry()
    c.pin("OK")


def fam_cr_internal(c):
    """R1: config.c removes EVERY CR, not only a trailing one: a CR inside a key or inside a hash
    is dropped before the key and the hash are read (r88 CriticForgers f14, r88 g00)."""
    c.header()
    c.entry()
    rel = c.newfile()
    k = c.rng.choice(["path", "kernel_path", "image_path"])
    i = c.rng.randint(1, len(k) - 1)
    ln = c.add("  %s\r%s: boot():/%s#%s" % (k[:i], k[i:], rel, flip_last(b2(c.files[rel]))))
    c.expect.append([ln, "LP-MISMATCH", k])
    c.entry()
    rel2 = c.newfile()
    good = b2(c.files[rel2])
    j = c.rng.randint(1, 127)
    ln = c.add("  path: boot():/%s#%s\r%s" % (rel2, good[:j], good[j:]))
    c.expect.append([ln, "OK", "path"])


def fam_resource_case(c):
    """R4: the resource name is compared case-sensitively; `BOOT()` does not resolve (r88
    CriticForgers f18, MutHeldOut h20)."""
    c.header()
    c.entry()
    c.pin("OK")
    c.entry()
    c.pin("LP-UNRESOLVED", resource=c.rng.choice(["BOOT()", "Boot()", "bOOT()", "boOt()"]),
          gz=c.rng.random() < 0.5)


def fam_key_equals(c):
    """R1: a key is followed directly by ':'; `path=` (the key's last letter touching '=') is not a key
    line (r88 MutHeldOut h01). Every case writes the touching form; `path =` was drawn with p 0.5 in the
    first candidate and a gate that accepts '=' escaped one run of three (r89 dev receipt), the R88-R2
    class, so the blank-before-'=' variant is no longer drawn."""
    c.header()
    c.entry()
    rel = c.newfile()
    c.add("  path=%sboot():/%s#%s" % (c.rng.choice(["", " ", "\t"]), rel, flip_last(b2(c.files[rel]))))
    c.pin("OK")


def fam_empty_path(c):
    """R2/R5: `boot():/#hash` has an empty path; it is still a pin, and ESP/'' is the ESP directory,
    not a regular file -> LP-MISSING (r88 MutHeldOut h10, r88 g00)."""
    c.header()
    c.entry()
    ln = c.add("  %s: boot():/#%s" % (c.rng.choice(["path", "kernel_path"]), secrets.token_hex(64)))
    c.expect.append([ln, "LP-MISSING", "path"])
    c.entry()
    c.pin("OK")


def fam_optional_key_case(c):
    """R6: `WALLPAPER`/`Term_Font` are the optional keys too (keys match case-insensitively), so a
    mismatch there is `skip` (r88 MutHeldOut h11)."""
    c.header()
    if c.rng.random() < 0.5:
        set_panic(c, c.rng.choice(["yes", "no"]))
    key = c.rng.choice(["WALLPAPER", "Wallpaper", "wallPaper", "TERM_FONT", "Term_Font", "term_FONT"])
    rel = c.newfile()
    ln = c.add("%s: boot():/%s#%s" % (key, rel, flip_last(b2(c.files[rel]))))
    c.expect.append([ln, "LP-MISMATCH", key])
    c.entry()
    c.pin("OK")



FAMILIES = {
    "POSITIVE": fam_positive,
    "MISMATCH-EARLY": lambda c: fam_mismatch(c, False),
    "MISMATCH-LATE": lambda c: fam_mismatch(c, True),
    "MISSING": fam_missing,
    "HASH-LENGTH": fam_hash_short,
    "HASH-NONHEX": fam_hash_nonhex,
    "HASH-UPPER": fam_hash_upper,
    "COMMENT-DECOY": fam_comment_decoy,
    "KEY-CASE": fam_key_case,
    "WHITESPACE-CRLF": fam_whitespace,
    "LAST-HASH": fam_last_hash,
    "GZ-RAW": fam_gz_raw,
    "UNRESOLVED": fam_unresolved,
    "PANIC-DEFAULT": fam_panic_default,
    "PANIC-NO-ONLY": fam_panic_no_only,
    "PANIC-FIRST": fam_panic_first,
    "SECUREBOOT": fam_secureboot,
    "OPTIONAL-SKIP": fam_optional_skip,
    "MULTI-FAULT": fam_multi,
    "UNHASHED-DECOYS": fam_unhashed_decoys,
    "MALFORMED-INPUT": fam_malformed_input,
    "HOST-SHAPE": fam_host_shape,
    "KEY-SPACING": fam_key_spacing,
    "NO-PAREN": fam_no_paren,
    "FORMAT-BEFORE-RESOLVE": fam_format_before_resolve,
    "OPTIONAL-HASH-FORMAT": fam_optional_hash_format,
    "FIRST-URI-SEP": fam_first_uri_sep,
    "PAREN-PATH": fam_paren_path,
    "EMPTY-ROOT-RESOURCE": fam_empty_root_resource,
    "ROOT-ON-BOOT": fam_root_on_boot,
    "PANIC-KEY-CASE": fam_panic_key_case,
    "SB-FLAG-ZERO": fam_sb_flag_zero,
    "PANIC-RAW-DECOY": fam_panic_raw_decoy,
    "CONF-UNREADABLE": fam_conf_unreadable,
    "ALL-PIN-KEYS": fam_all_pin_keys,
    "PANIC-NON-NO": fam_panic_non_no,
    "ENTRY-LABEL": fam_entry_label,
    "PANIC-METADATA": fam_panic_metadata,
    "BLANK-CLASS": fam_blank_class,
    "OPTIONAL-MISSING": fam_optional_missing,
    "OPTIONAL-UNRESOLVED": fam_optional_unresolved,
    "EMPTY-PIN-LIST": fam_empty_pin_list,
    "DOUBLE-DOLLAR": fam_double_dollar,
    "ENTRY-LABEL-EDGES": fam_entry_label_edges,
    "PANIC-VALUE-BLANKS": fam_panic_value_blanks,
    "CR-INTERNAL": fam_cr_internal,
    "RESOURCE-CASE": fam_resource_case,
    "KEY-EQUALS": fam_key_equals,
    "EMPTY-PATH": fam_empty_path,
    "OPTIONAL-KEY-CASE": fam_optional_key_case,
}
CASES_PER_FAMILY = 4
# r87 routed R87-R1: the verdict is computed against this literal roster, not len(FAMILIES);
# a FAMILIES table that differs from it is a usage error (exit 2), never a verdict.
FAMILY_ROSTER = (
    "POSITIVE", "MISMATCH-EARLY", "MISMATCH-LATE", "MISSING", "HASH-LENGTH", "HASH-NONHEX",
    "HASH-UPPER", "COMMENT-DECOY", "KEY-CASE", "WHITESPACE-CRLF", "LAST-HASH", "GZ-RAW",
    "UNRESOLVED", "PANIC-DEFAULT", "PANIC-NO-ONLY", "PANIC-FIRST", "SECUREBOOT", "OPTIONAL-SKIP",
    "MULTI-FAULT", "UNHASHED-DECOYS", "MALFORMED-INPUT", "HOST-SHAPE",
    "KEY-SPACING", "NO-PAREN", "FORMAT-BEFORE-RESOLVE", "OPTIONAL-HASH-FORMAT", "FIRST-URI-SEP",
    "PAREN-PATH", "EMPTY-ROOT-RESOURCE", "ROOT-ON-BOOT", "PANIC-KEY-CASE", "SB-FLAG-ZERO",
    "PANIC-RAW-DECOY", "CONF-UNREADABLE", "ALL-PIN-KEYS", "PANIC-NON-NO", "ENTRY-LABEL",
    "PANIC-METADATA",
    "BLANK-CLASS", "OPTIONAL-MISSING", "OPTIONAL-UNRESOLVED", "EMPTY-PIN-LIST", "DOUBLE-DOLLAR",
    "ENTRY-LABEL-EDGES", "PANIC-VALUE-BLANKS", "CR-INTERNAL", "RESOURCE-CASE", "KEY-EQUALS",
    "EMPTY-PATH", "OPTIONAL-KEY-CASE",
)


def build(fam, rng, root):
    c = Case(fam, rng)
    FAMILIES[fam](c)
    d = tempfile.mkdtemp(prefix="c", dir=root)
    esp = os.path.join(d, rname(rng, ""))
    os.makedirs(esp)
    for rel, data in c.files.items():
        p = os.path.join(esp, *rel.split("/"))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(data)
    conf = os.path.join(d, rname(rng, ".conf"))
    if c.conf_dir:
        os.makedirs(conf)
    elif not c.conf_missing:
        with open(conf, "w", newline="") as f:
            f.write(c.eol.join(c.lines) + c.eol)
    if not c.sb and c.sbflag is None and rng.random() < 0.3:
        c.sbflag = "0"
    return c, d, conf, esp


def run_gate(gate, conf, esp, c, cwd):
    argv = [sys.executable, gate, "--conf", conf, "--esp", esp]
    if c.sb:
        argv += ["--secure-boot-enforced", "1"]
    elif c.sbflag is not None:
        argv += ["--secure-boot-enforced", c.sbflag]
    try:
        p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return None, "timeout"
    try:
        out = json.loads(p.stdout)
        pins = sorted((int(x["line"]), str(x["status"]), str(x["consequence"])) for x in out["pins"])
        entries = {int(x["line"]): x["entry"] for x in out["pins"] if "entry" in x}
        panic = ("present", out["hash_mismatch_panic"]) if "hash_mismatch_panic" in out else ("absent", None)
        got = (p.returncode, out["verdict"], pins, out["rc"], entries, panic)
    except Exception as e:  # noqa: BLE001 - any malformed output is a failed case
        return None, "bad-output: %s rc=%s stderr=%s" % (type(e).__name__, p.returncode, p.stderr[-300:])
    return got, None


def r8_ok(c, got):
    """R8: optional fields, when present, must be right (pins already matched exactly)."""
    want_entries, want_panic = c.meta()
    for ln, label in got[4].items():
        if ln not in want_entries or label != want_entries[ln]:
            return False
    state, pm = got[5]
    if state == "absent" or c.conf_missing or c.conf_dir:
        return True
    if want_panic is None:
        return pm is None
    return (isinstance(pm, dict) and pm.get("line") == want_panic[0]
            and str(pm.get("value", "")).lower() == want_panic[1].lower())


def run_battery(gate, work):
    rng = random.Random(secrets.randbits(64))
    root = tempfile.mkdtemp(prefix="limine-battery-r89-", dir=work)
    try:
        plan = [f for f in FAMILY_ROSTER for _ in range(CASES_PER_FAMILY)]
        rng.shuffle(plan)
        log = []
        for fam in plan:
            c, d, conf, esp = build(fam, rng, root)
            want = c.finish()
            got, err = (None, "gate absent") if not os.path.isfile(gate) else run_gate(gate, conf, esp, c, d)
            ok = (got is not None and got[0] == want[0] and got[3] == want[0] and got[1] == want[1]
                  and [(x[0], x[1]) for x in got[2]] == [(x[0], x[1]) for x in want[2]] and r8_ok(c, got))
            log.append({"family": fam, "passed": ok, "sbflag": "1" if c.sb else c.sbflag,
                        "want": [want[0], want[1], [list(x) for x in want[2]]],
                        "got": None if got is None else [got[0], got[1], [list(x) for x in got[2]], got[3]],
                        "error": err})
            shutil.rmtree(d, ignore_errors=True)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    fams = {f: [] for f in FAMILY_ROSTER}
    for e in log:
        fams[e["family"]].append(e["passed"])
    passed = sorted(f for f, v in fams.items() if len(v) == CASES_PER_FAMILY and all(v))
    failed = sorted(f for f in FAMILY_ROSTER if f not in passed)
    met = len(passed) == len(FAMILY_ROSTER) and len(log) == len(FAMILY_ROSTER) * CASES_PER_FAMILY
    return {"schema": "tsukuroi-limine-pin-battery-r89-v1", "gate": gate,
            "families_total": len(FAMILY_ROSTER), "families_passed": len(passed),
            "failed_families": failed, "cases": len(log), "verdict": "met" if met else "unmet",
            "case_log": log}


# One-field lie wrappers (r87 routed R87-R1): each runs the positive gate and falsifies exactly one
# field of its answer; a battery that misses any of them does not check that field.
LIE_WRAPPER = '''import json, subprocess, sys
p = subprocess.run([sys.executable, %r] + sys.argv[1:], capture_output=True, text=True)
out = json.loads(p.stdout)
rc = p.returncode
KIND = %r
pins = out.get("pins", [])
if KIND == "exit-code" and pins:
    rc = 1 - rc if rc in (0, 1) else 0
elif KIND == "rc-field" and pins:
    out["rc"] = 1 - out["rc"] if out["rc"] in (0, 1) else 0
elif KIND == "line" and pins:
    pins[-1]["line"] += 1
elif KIND == "consequence":
    for x in pins:
        if x["consequence"] == "prompt":
            x["consequence"] = "panic"
elif KIND == "status":
    for x in pins:
        if x["status"] == "LP-MISSING":
            x["status"] = "LP-UNRESOLVED"
elif KIND == "verdict" and out.get("verdict") == "CANNOT-EVALUATE" and pins:
    out["verdict"] = "HEALTHY"
elif KIND == "entry":
    for x in pins[:1]:
        x["entry"] = "lie"
elif KIND == "panic-line" and isinstance(out.get("hash_mismatch_panic"), dict):
    out["hash_mismatch_panic"]["line"] += 1
elif KIND == "panic-value" and isinstance(out.get("hash_mismatch_panic"), dict):
    out["hash_mismatch_panic"]["value"] = " " + str(out["hash_mismatch_panic"]["value"]) + " "
print(json.dumps(out))
sys.exit(rc)
'''
LIE_KINDS = ("exit-code", "rc-field", "line", "consequence", "status", "verdict", "entry", "panic-line",
             "panic-value")

SELFTEST_GATES = {
    # name: (source, must_meet)
    "absent": (None, False),
    "constant-healthy": ('import json,sys\nprint(json.dumps({"verdict":"HEALTHY","rc":0,"pins":[]}))\n', False),
    "non-json": ('print("hello")\n', False),
    "constant-degraded": ('import json,sys\nprint(json.dumps({"verdict":"DEGRADED","rc":1,"pins":[]}))\nsys.exit(1)\n', False),
}


def selftest():
    """The literal roster equals FAMILIES; negative controls and one-field lies must read unmet; the
    positive control (the r87 landed gate copied at the r89 freeze, never the candidate) must read
    met with every roster family run CASES_PER_FAMILY times. Paths resolve from this file, not the
    cwd; the run happens from an unrelated cwd."""
    results = [("roster-literal", tuple(FAMILIES) == FAMILY_ROSTER, len(FAMILY_ROSTER))]
    work = tempfile.mkdtemp(prefix="limine-battery-selftest-")
    old = os.getcwd()
    lane = os.path.dirname(HERE)
    ref = os.path.join(lane, ".ufo", "waves", "round-89", "before", "roster", "pos-landed-gate-3ba37eb0.py")
    try:
        os.chdir(work)
        for name, (src, must) in SELFTEST_GATES.items():
            g = os.path.join(work, name + ".py")
            if src is not None:
                with open(g, "w") as f:
                    f.write(src)
            r = run_battery(g, work)
            results.append((name, r["verdict"] == ("met" if must else "unmet"), r["families_passed"]))
        if os.path.isfile(ref):
            r = run_battery(ref, work)
            counts = {}
            for e in r["case_log"]:
                counts[e["family"]] = counts.get(e["family"], 0) + 1
            full = all(counts.get(f) == CASES_PER_FAMILY for f in FAMILY_ROSTER)
            results.append(("reference-gate", r["verdict"] == "met" and full, r["families_passed"]))
            for kind in LIE_KINDS:
                g = os.path.join(work, "lie-%s.py" % kind)
                with open(g, "w") as f:
                    f.write(LIE_WRAPPER % (ref, kind))
                r = run_battery(g, work)
                results.append(("lie-" + kind, r["verdict"] == "unmet", r["families_passed"]))
        else:
            results.append(("reference-gate", False, "missing " + ref))
    finally:
        os.chdir(old)
        shutil.rmtree(work, ignore_errors=True)
    ok = all(x[1] for x in results)
    for name, good, n in results:
        print("%-18s %s families_passed=%s" % (name, "PASS" if good else "FAIL", n))
    print("selftest %s %d/%d" % ("PASS" if ok else "FAIL", sum(x[1] for x in results), len(results)))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--gate")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--work", default=os.environ.get("TMPDIR"))
    ap.add_argument("--json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if tuple(FAMILIES) != FAMILY_ROSTER:
        print("FAMILIES differs from FAMILY_ROSTER", file=sys.stderr)
        return 2
    if a.selftest:
        return selftest()
    if not a.gate:
        ap.print_usage(sys.stderr)
        return 2
    gate = os.path.abspath(a.gate)
    work = a.work or tempfile.gettempdir()
    os.makedirs(work, exist_ok=True)
    runs = [run_battery(gate, work) for _ in range(a.runs)]
    if a.json:
        with open(a.json, "w") as f:
            json.dump(runs if a.runs > 1 else runs[0], f, indent=1)
    for r in runs:
        print("families_passed %d/%d verdict %s failed %s" % (r["families_passed"], r["families_total"],
                                                             r["verdict"], ",".join(r["failed_families"]) or "-"))
    return 0 if all(r["verdict"] == "met" for r in runs) else 1


if __name__ == "__main__":
    sys.exit(main())
