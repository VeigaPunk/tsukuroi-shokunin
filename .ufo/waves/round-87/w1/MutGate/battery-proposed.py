#!/usr/bin/env python3
"""Round-87 frozen battery for a Limine v12.9.4 path-pin gate (tsukuroi lane).

PREDICATE (the same sentence in SCORECARD.md "Round 87 — declaration" and in every receipt):
  `tools/check-limine-pins.py --conf FILE --esp DIR [--secure-boot-enforced 1]` implements the
  frozen Limine v12.9.4 pin rule set R1-R7 below: for each of 22 families, on fixtures generated
  fresh per run with OS-entropy names, bytes and layouts, with the whole case list shuffled per
  run, every case returns exactly the expected (rc, verdict, sorted per-pin (line, status,
  consequence)) within 20 s.
TARGET: 22 of 22 families (`verdict: met`, rc 0) in each of three consecutive runs at the landed tip.
KILL RULE: unmet if any of the three runs reads below 22/22; void if this file's bytes differ
  from `.ufo/waves/round-87/before/freeze-manifest.sha256`.

FROZEN RULE SET (sources pinned in .ufo/waves/round-87/before/src/, Limine tag v12.9.4):
  R1 key lines (common/lib/config.c raw 527-551 strip CR and leading/trailing blanks per line;
     config_get_value raw 778-818 matches a key case-insensitively, only at the start of a line,
     followed directly by ':' and skips blanks after ':'): a line is `KEY: value` when, after
     removing leading spaces/tabs, it starts with letters/underscores then ':'. A line whose
     first non-blank character is '#' is not a key line. The value is the rest of the line with
     leading spaces/tabs removed and trailing spaces/tabs/CR removed.
  R2 pins (common/lib/uri.c uri_resolve raw 28-104; CONFIG.md raw 111-113, 134, 210, 295-308,
     330-350 name the path-valued keys): a key line whose key is one of path, kernel_path,
     image_path, module_path, dtb_path, global_dtb, wallpaper, term_font (case-insensitive) is a
     pin when its value has the URI form `[$]resource(root):/path#hash` - a '(' then, later, '):/'
     then, later, a '#'. The hash is the text after the LAST '#'; the path is the text between
     the first '):/' and that '#'. Any other key, a value with no '#' after '):/', or a value
     with no URI form, is not a pin and is ignored.
  R3 hash format (uri.c raw 89-101): the hash must be exactly 128 characters of [0-9a-fA-F];
     otherwise status LP-HASH-FORMAT (checked before resolution).
  R4 resolution (uri.c raw 344-362): a leading '$' (gzip marker) is dropped from the resource;
     resource `boot` with an empty root resolves to ESP/path. Any other resource, or a non-empty
     root (boot(2), guid(...), uuid(...), fslabel(...), hdd, odd, tftp) -> LP-UNRESOLVED.
  R5 comparison (uri.c raw 378-383, 403-470, 483-487, 662-664; CONFIG.md raw 458-462): the file
     absent -> LP-MISSING; otherwise BLAKE2b-512 of the file's raw bytes as stored (gzip files
     are NOT decompressed) compared with the hash case-insensitively -> OK or LP-MISMATCH.
  R6 consequence per pin (uri.c raw 18-26, 301-319, 693-710; common/menu.c raw 1711-1717;
     CONFIG.md raw 152-156): OK -> `none`; LP-MISSING and LP-UNRESOLVED -> `not-modelled`;
     for LP-MISMATCH and LP-HASH-FORMAT: key `wallpaper` or `term_font` (optional resources)
     -> `skip`; else LP-HASH-FORMAT -> `panic`; else LP-MISMATCH -> `panic` when
     --secure-boot-enforced 1, else `prompt` when the FIRST `hash_mismatch_panic` key line in
     the whole file (R1 rules) has a value equal to `no` case-insensitively, else `panic`.
  R7 verdict: any LP-MISMATCH, LP-MISSING or LP-HASH-FORMAT -> DEGRADED rc 1; else any
     LP-UNRESOLVED -> CANNOT-EVALUATE rc 2; else HEALTHY rc 0. An unreadable --conf ->
     CANNOT-EVALUATE rc 2 with an empty pin list.

GATE OUTPUT CONTRACT (stdout, one JSON object): {"verdict": str, "rc": int,
  "pins": [{"line": int (1-based physical line), "status": str, "consequence": str, ...}, ...]}.
  The process exit code must equal "rc". Extra keys are allowed and ignored.

Not modelled (limits, not families): macro expansion (`${NAME}`), Secure Boot's "unhashed path
panics" rule, per-protocol behaviour of a missing file, a cmdline value that is itself URI-shaped.

Fixtures carry no answer: random file and directory names, no expected value on disk; the conf
lives outside the ESP directory; the gate runs with cwd set to the fixture directory.

Usage: limine-pin-battery-r87.py --gate PATH [--runs N] [--work DIR] [--json OUT]
       limine-pin-battery-r87.py --selftest
Exit: 0 met; 1 unmet; 2 usage/could-not-evaluate.
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
        self.eol = "\n"
        self.conf_missing = False
        self.panic_value = None  # value of first hash_mismatch_panic, None = absent
        self.meta = {}           # extra assertions: "entries" {line: entry}, "panic" {line, value}

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

    def mismatch_consequence(self, key):
        if key.lower() in ("wallpaper", "term_font"):
            return "skip"
        if self.sb:
            return "panic"
        if self.panic_value is not None and self.panic_value.lower() == "no":
            return "prompt"
        return "panic"

    def pin(self, status, key="path", indent="  ", resource="boot()", data=None, hashfmt=None,
            rel=None, gz=False, entry=None):
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
        if entry is not None:
            self.meta.setdefault("entries", {})[ln] = entry
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
        if self.conf_missing:
            return 2, "CANNOT-EVALUATE", []
        if statuses & {"LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT"}:
            rc, verdict = 1, "DEGRADED"
        elif "LP-UNRESOLVED" in statuses:
            rc, verdict = 2, "CANNOT-EVALUATE"
        else:
            rc, verdict = 0, "HEALTHY"
        return rc, verdict, sorted(out)


def set_panic(c, value, indent=""):
    ln = c.add("%shash_mismatch_panic: %s" % (indent, value))
    if c.panic_value is None:
        c.panic_value = value.strip()
        c.meta["panic"] = {"line": ln, "value": value.strip()}


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
    if c.rng.random() < 0.6:
        c.eol = "\r\n"


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
    """The host's limine.conf shape at the freeze (receipt .ufo/waves/round-87/before/host/): one
    global hash_mismatch_panic: no, two kernel entries whose pins mismatch, a Snapshots directory
    with three history pins that match, and an unhashed fallback EFI path."""
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
        name = "omarchy_linux.efi_sha256_%s" % hashlib.sha256(data).hexdigest()
        rel = "%s/limine_history/%s" % (mid, name)
        c.files[rel] = data
        c.pin("OK", rel=rel, indent="     ")
    c.add("/EFI fallback")
    c.add("protocol: efi")
    c.add("path: boot():/EFI/BOOT/%s" % c.newfile(sub=["EFI", "BOOT"]).split("/")[-1])


def fam_paren_path(c):
    """R2: the resource ends at the FIRST '('; a stored path may itself contain '(' and ')'."""
    c.header()
    label = rname(c.rng, "")
    c.entry(label)
    rel = "EFI/Linux/%s(%d).efi" % (rname(c.rng, ""), c.rng.randrange(10))
    c.files[rel] = c.blob()
    c.pin("OK", rel=rel)
    c.pin("LP-MISMATCH", key="kernel_path", rel=rel)


def fam_entry_label(c):
    """The per-pin entry label is reported; sibling entries must not be confused."""
    c.header()
    for label in (rname(c.rng, ""), "EFI fallback", rname(c.rng, "")):
        c.entry(label)
        c.pin(c.rng.choice(["OK", "LP-MISMATCH"]), entry=label)


def fam_panic_metadata(c):
    """The reported hash_mismatch_panic record names the first occurrence's line and value."""
    c.header()
    set_panic(c, c.rng.choice(["no", "NO", "No"]), indent="  ")
    c.entry()
    c.pin("LP-MISMATCH")


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
    "PAREN-PATH": fam_paren_path,
    "ENTRY-LABEL": fam_entry_label,
    "PANIC-METADATA": fam_panic_metadata,
}
CASES_PER_FAMILY = 4


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
    if not c.conf_missing:
        with open(conf, "w", newline="") as f:
            f.write(c.eol.join(c.lines) + c.eol)
    return c, d, conf, esp


def run_gate(gate, conf, esp, sb, cwd):
    argv = [sys.executable, gate, "--conf", conf, "--esp", esp]
    if sb:
        argv += ["--secure-boot-enforced", "1"]
    try:
        p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return None, "timeout"
    try:
        out = json.loads(p.stdout)
        pins = sorted((int(x["line"]), str(x["status"]), str(x["consequence"])) for x in out["pins"])
        entries = {int(x["line"]): ("entry" in x, x.get("entry")) for x in out["pins"]}
        got = (p.returncode, out["verdict"], pins, out["rc"], entries, out.get("hash_mismatch_panic"))
    except Exception as e:  # noqa: BLE001 - any malformed output is a failed case
        return None, "bad-output: %s rc=%s stderr=%s" % (type(e).__name__, p.returncode, p.stderr[-300:])
    return got, None


def run_battery(gate, work):
    rng = random.Random(secrets.randbits(64))
    root = tempfile.mkdtemp(prefix="limine-battery-r87-", dir=work)
    try:
        plan = [f for f in FAMILIES for _ in range(CASES_PER_FAMILY)]
        rng.shuffle(plan)
        log = []
        for fam in plan:
            c, d, conf, esp = build(fam, rng, root)
            want = c.finish()
            got, err = (None, "gate absent") if not os.path.isfile(gate) else run_gate(gate, conf, esp, c.sb, d)
            ok = got is not None and got[0] == want[0] and got[3] == want[0] and got[1] == want[1] and [list(x) for x in got[2]] == [list(x) for x in want[2]]
            if ok and "entries" in c.meta:
                ok = all((not got[4].get(ln, (False, None))[0]) or got[4][ln][1] == e
                         for ln, e in c.meta["entries"].items())
            if ok and "panic" in c.meta:
                pm = got[5]
                ok = not isinstance(pm, dict) or (
                    pm.get("line") == c.meta["panic"]["line"]
                    and str(pm.get("value", "")).strip().lower() == c.meta["panic"]["value"].lower())
            log.append({"family": fam, "passed": ok,
                        "want": [want[0], want[1], [list(x) for x in want[2]]],
                        "got": None if got is None else [got[0], got[1], [list(x) for x in got[2]], got[3]],
                        "error": err})
            shutil.rmtree(d, ignore_errors=True)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    fams = {}
    for e in log:
        fams.setdefault(e["family"], []).append(e["passed"])
    passed = sorted(f for f, v in fams.items() if all(v))
    failed = sorted(f for f, v in fams.items() if not all(v))
    met = len(passed) == len(FAMILIES)
    return {"schema": "tsukuroi-limine-pin-battery-r87-v1", "gate": gate,
            "families_total": len(FAMILIES), "families_passed": len(passed),
            "failed_families": failed, "cases": len(log), "verdict": "met" if met else "unmet",
            "case_log": log}


SELFTEST_GATES = {
    # name: (source, must_meet)
    "absent": (None, False),
    "constant-healthy": ('import json,sys\nprint(json.dumps({"verdict":"HEALTHY","rc":0,"pins":[]}))\n', False),
    "non-json": ('print("hello")\n', False),
    "constant-degraded": ('import json,sys\nprint(json.dumps({"verdict":"DEGRADED","rc":1,"pins":[]}))\nsys.exit(1)\n', False),
}


def selftest():
    """Negative controls must read unmet; the positive control (the committed reference gate the
    freeze names, controls/ref-gate-r87.py, never the candidate) must read met. Paths resolve from
    this file, not the cwd; the run happens from an unrelated cwd."""
    results = []
    work = tempfile.mkdtemp(prefix="limine-battery-selftest-")
    old = os.getcwd()
    try:
        os.chdir(work)
        for name, (src, must) in SELFTEST_GATES.items():
            g = os.path.join(work, name + ".py")
            if src is not None:
                with open(g, "w") as f:
                    f.write(src)
            r = run_battery(g, work)
            results.append((name, r["verdict"] == ("met" if must else "unmet"), r["families_passed"]))
        lane = os.path.dirname(HERE)
        ref = os.path.join(lane, ".ufo", "waves", "round-87", "before", "controls", "ref-gate-r87.py")
        if os.path.isfile(ref):
            r = run_battery(ref, work)
            results.append(("reference-gate", r["verdict"] == "met", r["families_passed"]))
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
