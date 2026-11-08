#!/usr/bin/env python3
"""Round-92 battery for a Limine path-pin gate (tsukuroi lane; successor of the r91 battery).

What it decides: whether a gate `GATE --conf FILE --esp DIR [--secure-boot-enforced 0|1]
[--tpm-present 0|1] [--limine-version X.Y.Z]` follows the Limine pin rule set R1-R7 and R9-R10
below, the reporting contracts R8 (optional fields), V1 (global-section visibility of
`hash_mismatch_panic` and `measured_boot`), V2 (the version-selected visibility rule: pre-12.9.5 vs
12.9.5+) and U1 (`unverified_image_lines` reporting), for each of the families in FAMILY_ROSTER, on
fixtures generated fresh per run with OS-entropy names, bytes and layouts, the whole case list
shuffled per run; every case must return exactly the expected (rc, verdict, sorted per-pin (line,
status, consequence), on_panic, unverified_image_lines) within 20 s, plus R8's optional fields.
Verdict `met` only when every family in the literal FAMILY_ROSTER passed every case.

Round-92 claims (C1 and C2, SCORECARD.md "Round 92 — declaration"). C1 (operability): the r91
battery launched the gate with `argv = [sys.executable, gate, ...]`, so a `tools/`-resident gate had
the battery's own directory as `sys.path[0]` and could import the judge's `Case` oracle — the r91
wave measured a gate that models none of R6/R9/R10/V1/U1 and still reads 82/82 met
(`.ufo/waves/round-91/w1/ScribeLesson.md` M1, QUALITY 132). r92 launches every gate through
ISOLATION below. C2 (depth): the r91 V1 rule is v12.9.4's; upstream v12.9.5 rewrote the parser and
removed the first-line-is-entry exception (`.ufo/waves/round-91/w1/ScoutDrift.md`; v12.9.6 raw
328-330, 362-365), so the gate takes `--limine-version` and V2 selects the era.

ISOLATION (C1; the contract a control must be measured against): the battery copies the gate's bytes
into a private directory that holds nothing else, then runs it as `bwrap --unshare-all
--die-with-parent --new-session --clearenv` with only `/usr` and `/etc` read-only, a fresh `/dev`, a
fresh `/proc`, a fresh `/tmp`, the case directory read-only and the gate-copy read-only mounted, cwd
set to the case directory, `PATH=/usr/bin HOME=/tmp LC_ALL=C TMPDIR=/tmp`, and `python3 -I` (isolated
mode: no script directory on sys.path, PYTHON* variables ignored). The sandbox therefore exposes no
path to the battery's source, to the lane tree or to the caller's environment; `--isolation-check`
prints what a probe process actually sees. A missing `bwrap` is `could-not-evaluate` (exit 2), never
a silent unsandboxed run.

RULE SET (the r87 frozen R1-R7 as r90 stated them, with the r90 and r91 changes marked; sources
.ufo/waves/round-90/before/src/, Limine tag v12.9.4, re-pinned byte-identical in
.ufo/waves/round-91/before/src/):
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
  R4 resolution (uri.c raw 344-366): ONE leading '$' (gzip marker) is dropped from the resource;
     the resource name is then compared case-sensitively (strcmp). r90: a name that is not exactly
     one of hdd, odd, boot, guid, uuid, fslabel, tftp (an empty name, `$boot` left by `$$boot`,
     `BOOT`, `Boot`, `bootx`) is not a resource: URI_ERROR "Resource ... not valid" (raw 364) ->
     LP-BAD-RESOURCE. Of the seven names only `boot` with an empty root resolves, to ESP/path; a
     valid name with any other root (boot(2), guid(...), uuid(...), fslabel(...), hdd, odd, tftp)
     -> LP-UNRESOLVED.
  R5 comparison (uri.c raw 378-383, 403-470, 483-487, 662-664; CONFIG.md raw 458-462): no regular
     file at ESP/path (absent, or the path names a directory such as the ESP itself) -> LP-MISSING;
     otherwise BLAKE2b-512 of the file's raw bytes as stored (gzip files are NOT decompressed)
     compared with the hash case-insensitively -> OK or LP-MISMATCH.
  R6 consequence per pin (uri.c raw 18-26, 301-319, 693-710; common/menu.c raw 1711-1717;
     CONFIG.md raw 152-156): OK -> `none`; LP-UNRESOLVED -> `not-modelled`; r90: LP-MISSING ->
     `panic` when the pin's line is the image line of an efi chainload entry (R9), else
     `not-modelled`; for LP-MISMATCH, LP-HASH-FORMAT and (r90) LP-BAD-RESOURCE: key `wallpaper` or
     `term_font`, matched case-insensitively like every key (optional resources) -> `skip`; else
     LP-HASH-FORMAT and LP-BAD-RESOURCE -> `panic`; else LP-MISMATCH -> `panic` when
     --secure-boot-enforced 1, else `prompt` when the FIRST VISIBLE `hash_mismatch_panic` key
     line in the global section (V1, R1 rules) has a value equal to `no` case-insensitively,
     else `panic`.
  R7 verdict: any LP-MISMATCH, LP-MISSING, LP-HASH-FORMAT or (r90) LP-BAD-RESOURCE -> DEGRADED
     rc 1; else any LP-UNRESOLVED -> CANNOT-EVALUATE rc 2; else HEALTHY rc 0 (also when the file
     holds no pin at all). An unreadable --conf (absent, a directory, or unreadable for any OS
     reason) -> CANNOT-EVALUATE rc 2 with an empty pin list. `--secure-boot-enforced 0` and an
     absent flag both mean "not enforced".
  R8 reporting contract (the lane gate's own output, not Limine behaviour): a pin record MAY
     carry "entry"; when it does, it equals the label of the nearest preceding entry line (a
     line whose first non-blank character is '/'; label = the line without its leading '/'
     characters, then without a leading '+' (no fixture starts a label with '++'), then trimmed of
     spaces/tabs at both ends; a trailing '+' stays), or null before any entry line. The top-level object MAY carry
     "hash_mismatch_panic"; when it does, it is null if no VISIBLE `hash_mismatch_panic` key line
     exists (V1, R1 rules), else {"line": the 1-based line of the FIRST such key line in the
     global section, "value": its R1 value, i.e. without leading or trailing blanks} (value
     compared case-insensitively).
  R9 efi image line (r90; common/menu.c raw 2429-2468 dispatch on the entry's PROTOCOL by strcmp;
     common/protos/chainload.c raw 414-435 reads PATH, then IMAGE_PATH, and panics "Failed to open
     image" when uri_open returns NULL; common/lib/config.c raw 686-720 entry body, raw 778-818 first
     matching key wins): an entry line is a line whose first non-blank character is '/'; its body
     is the physical lines after it up to the next entry line (or the end of the file); lines
     before the first entry line belong to no entry. An entry is an efi chainload entry when the
     FIRST key line (R1 rules) of its body whose key is `protocol` (key case-insensitive) has a
     value exactly `efi`, `uefi` or `efi_chainload` (case-sensitive; `efi_boot_entry`, `EFI`,
     `linux`, `limine` are not). Its image line is the FIRST key line of its body whose key is
     `path`; when the body has none, the FIRST key line whose key is `image_path`. The image line
     need not be a pin; only a pin on it gets R6's missing -> panic.
  R10 on_panic (r90; common/menu.c raw 1719-1728; common/lib/panic.s2.c raw 24-28, 70-78, 98): the
     top-level object MUST carry "on_panic" (not checked when --conf is unreadable). r91 (V1):
     measured boot is requested when the FIRST VISIBLE `measured_boot` key line in the global
     section (R1 rules, key case-insensitive) has a value exactly `yes` (strcmp,
     case-sensitive), or when --secure-boot-enforced 1. Not requested -> "menu" (a panic prints
     and returns to the menu on a key press). Requested: --tpm-present 1 -> "halt" ("System
     halted."); --tpm-present 0 -> "menu" (Limine forces measured boot off without a TPM/CC
     interface); flag absent -> "halt-if-tpm".

  V1 global-section visibility (r91; common/lib/config.c raw 642-650, 527-551): the config buffer
     Limine hands to config_get_value is cut at the newline before the first entry line — the first
     physical line whose first non-blank character is '/' (leading spaces/tabs allowed) — and the
     byte before that line is overwritten with NUL. The guard `c > config_addr` means that when
     that first '/'-line is ALSO the first physical line of the file (no bytes precede it), no cut
     happens and the WHOLE file stays visible to config_get_value. Therefore `hash_mismatch_panic`
     (R6) and `measured_boot` (R10) are read only from the "global section": every physical line
     before the first entry line, EXCEPT when that entry line is the file's first line, in which
     case every physical line is in the global section. "FIRST ... key line" in R6/R10/R8 means the
     first matching key line WITHIN THAT SECTION. r91 reverses r90's whole-file reading; a
     `hash_mismatch_panic` or `measured_boot` key line inside an entry body (or after the first
     entry line in general) is INVISIBLE to Limine and must not be read. A config whose first line
     is blank (spaces/tabs) before the first '/'-line keeps the cut (the '/'-line is not the first
     physical line): the global section is those blank lines only.
  V2 version-selected visibility (r92; sources .ufo/waves/round-92/before/src/): the rule above is
     v12.9.4's. Upstream v12.9.5 rewrote `create_menu_tree()` to parse in place (v12.9.5 == v12.9.6
     in this region, ChangeLog 12.9.5 "Parse the config in linear time"): it cuts before the first
     entry line (v12.9.6 raw 328-330 `if (p > config_addr) { *(p - 1) = '\\0'; }`) and then NULs the
     end of every entry label line (raw 362-365), so `config_addr` ends at the first entry's label.
     The first-line-is-entry exception is GONE: when line 1 is an entry line the global section is
     EMPTY and both keys are invisible. The gate selects the era from `--limine-version X.Y.Z`
     (default `12.9.4`): a version < 12.9.5 keeps V1, >= 12.9.5 applies this rule; an unknown or
     malformed version is a usage error (rc 64, no verdict). The battery passes the case's version
     (ERA-DEFAULT omits the flag and expects the 12.9.4 answers). The non-first-line cases answer
     identically in both eras.
  U1 unverified_image_lines (r91; uri.c raw 46-63 uri_resolve returns false without a message when
     the value has no '(' or no '):/', raw 28-104; chainload.c raw 414-435 still uri_opens PATH then
     IMAGE_PATH): the image line of an efi chainload entry (R9's first `path` else first
     `image_path` key line) whose value Limine still hands to uri_open but which carries no URI
     shape at all (no `(`, or no `):/` after the `(`) or no `#` hash after `):/` is an
     "unverified image line". The gate MUST carry a top-level "unverified_image_lines" array: the
     sorted (ascending) list of the 1-based physical line numbers of every image line whose value
     is not a parseable `[$]resource(root):/path#hash` pin (R2). It is a REPORTING contract like
     R8: it changes no pin verdict, status, consequence or rc. A gate that omits the field, or
     returns a different list, fails U1 families; a value that IS a pin (valid or invalid hash,
     bad resource, unresolved) is NOT in the list even when its pin status is a fault.

GATE OUTPUT CONTRACT (stdout, one JSON object): {"verdict": str, "rc": int, "on_panic": str,
  "pins": [{"line": int (1-based physical line), "status": str, "consequence": str, ...}, ...]}.
  The process exit code must equal "rc". Other extra keys are allowed and ignored.

Not modelled (limits, not families): macro expansion (`${NAME}`), Secure Boot's "unhashed path
panics" rule, a missing file on any line other than an efi image line (linux, limine, multiboot
protocols; modules; optional keys), whether a valid resource other than empty-root `boot()`
resolves (boot(N) range and strtoui parse, volume lookups), menu hierarchy validity (a parentless
child), BIOS builds, a cmdline value that is itself URI-shaped, a gate that behaves differently on
its own bytes or file name, a version string outside `X.Y.Z` (refused as usage, not modelled), and
upstream releases after v12.9.6 (V2 maps every version >= 12.9.5 to the create_menu_tree rule the
two pinned releases share).

Fixtures carry no answer: random file and directory names (history names too: no content digest
in any name), no expected value on disk; the conf lives outside the ESP directory; the gate runs
with cwd set to the fixture directory, inside the ISOLATION sandbox.

Usage: limine-pin-battery-r92.py --gate PATH [--runs N>=1] [--work DIR] [--json OUT]
       limine-pin-battery-r92.py --selftest [--reference GATE]
       limine-pin-battery-r92.py --isolation-check [--work DIR]
Exit: 0 met; 1 unmet; 2 usage/could-not-evaluate (also: FAMILIES differs from FAMILY_ROSTER,
      or bwrap is absent).
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
VALID_RESOURCES = ("hdd", "odd", "boot", "guid", "uuid", "fslabel", "tftp")   # uri.c raw 349-366
EFI_PROTOCOLS = ("efi", "uefi", "efi_chainload")                              # menu.c raw 2456-2458
OPTIONAL = ("wallpaper", "term_font")


def r1_key(raw):
    """R1: (key_lower, value) for a key line, else None."""
    line = raw.replace("\r", "").strip(" \t")
    if not line or line[0] == "#":
        return None
    i = 0
    while i < len(line) and (line[i].isascii() and (line[i].isalpha() or line[i] == "_")):
        i += 1
    if i == 0 or i >= len(line) or line[i] != ":":
        return None
    return line[:i].lower(), line[i + 1:].lstrip(" \t")


def resource_name(resource, gz):
    """R4: the resource name as Limine compares it (text before the first '(', one '$' dropped)."""
    name = ("$" if gz else "") + resource.split("(", 1)[0]
    return name[1:] if name.startswith("$") else name


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
        self.tpm = None          # None: --tpm-present absent; "0"/"1": passed explicitly
        self.tpm_fixed = False   # True: the family chose tpm (R10 families); else drawn in build()
        self.version = "12.9.4"  # V2: the Limine version this case is modelled against
        self.pass_version = True # False: the battery omits --limine-version (ERA-DEFAULT)

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
        """V1: R1 scan for the FIRST VISIBLE hash_mismatch_panic key line in the global section:
        (line, value) or None."""
        visible = self.global_lines()
        for n, raw in enumerate(self.lines, 1):
            if n not in visible:
                continue
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

    def era_b(self):
        """V2: the create_menu_tree() cut applies from 12.9.5 on (no first-line exception)."""
        return tuple(int(p) for p in self.version.split(".")) >= (12, 9, 5)

    def global_lines(self):
        """V1/V2: the physical lines in the global section. Before 12.9.5: every line before the
        first entry line, unless that first entry line is the file's FIRST physical line, in which
        case every line. From 12.9.5 on: every line before the first entry line, with no
        exception (line 1 is an entry line -> empty section)."""
        first_entry = None
        for n, raw in enumerate(self.lines, 1):
            if raw.replace("\r", "").strip(" \t").startswith("/"):
                first_entry = n
                break
        if first_entry is None:
            return set(range(1, len(self.lines) + 1))
        if first_entry == 1 and not self.era_b():
            return set(range(1, len(self.lines) + 1))
        return set(range(1, first_entry))

    def r1_first_visible(self, key):
        """V1: the FIRST key line with this key within the global section: (line, value) or None."""
        visible = self.global_lines()
        for n, raw in enumerate(self.lines, 1):
            if n not in visible:
                continue
            kv = r1_key(raw)
            if kv is not None and kv[0] == key:
                return n, kv[1]
        return None

    def want_unverified(self):
        """U1: sorted physical lines of image lines whose value is not a parseable pin (R2).
        Pin shape (uri_resolve raw 32-107): a '(' , later a '):/', a non-empty path, and a '#'
        after '):/'. A '#' with no 128-hex hash is still a pin (LP-HASH-FORMAT), so the shape check
        here is structural only — '#' present, path non-empty."""
        images = self.r9_image_lines()
        out = []
        for ln in sorted(images):
            kv = r1_key(self.lines[ln - 1])
            if kv is None:
                continue
            val = kv[1]
            try:
                i_paren = val.index("(")
            except ValueError:
                out.append(ln)
                continue
            rest = val[i_paren + 1:]
            try:
                i_close = rest.index("):/")
            except ValueError:
                out.append(ln)
                continue
            tail = rest[i_close + 3:]
            if tail == "" or "#" not in tail:
                out.append(ln)
        return sorted(out)

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
        elif status in ("LP-UNRESOLVED", "LP-BAD-RESOURCE"):
            h = good
            # r90 R4: a name outside VALID_RESOURCES is LP-BAD-RESOURCE, whatever the family asked for
            status = ("LP-BAD-RESOURCE" if resource_name(resource, gz) not in VALID_RESOURCES
                      else "LP-UNRESOLVED")
        else:
            raise ValueError(status)
        if hashfmt is not None and status != "LP-HASH-FORMAT":
            h = hashfmt(h) if callable(hashfmt) else hashfmt
        uri = "%s%s:/%s#%s" % ("$" if gz else "", resource, rel, h)
        ln = self.add("%s%s: %s" % (indent, key, uri))
        self.expect.append([ln, status, key])
        return ln

    def r1_first(self, key):
        """V1: R1 scan of the GLOBAL SECTION for the FIRST key line with this key: (line, value)
        or None. Supersedes the r90 whole-file read."""
        return self.r1_first_visible(key)

    def r9_image_lines(self):
        """R9: the set of physical lines that are the image line of an efi chainload entry."""
        bodies, cur = [], None
        for n, raw in enumerate(self.lines, 1):
            if raw.replace("\r", "").strip(" \t").startswith("/"):
                cur = []
                bodies.append(cur)
            elif cur is not None:
                cur.append(n)
        out = set()
        for body in bodies:
            keys = [(n, r1_key(self.lines[n - 1])) for n in body]
            keys = [(n, kv) for n, kv in keys if kv is not None]
            proto = next((kv[1] for n, kv in keys if kv[0] == "protocol"), None)
            if proto not in EFI_PROTOCOLS:
                continue
            img = next((n for n, kv in keys if kv[0] == "path"), None)
            if img is None:
                img = next((n for n, kv in keys if kv[0] == "image_path"), None)
            if img is not None:
                out.add(img)
        return out

    def want_on_panic(self):
        """R10."""
        mb = self.r1_first("measured_boot")
        requested = (mb is not None and mb[1] == "yes") or self.sb
        if not requested:
            return "menu"
        return {"1": "halt", "0": "menu"}.get(self.tpm, "halt-if-tpm")

    def finish(self):
        out = []
        images = self.r9_image_lines()
        for ln, status, key in self.expect:
            optional = key.lower() in OPTIONAL
            if status == "OK":
                cons = "none"
            elif status == "LP-UNRESOLVED":
                cons = "not-modelled"
            elif status == "LP-MISSING":
                cons = "panic" if ln in images else "not-modelled"
            elif status in ("LP-HASH-FORMAT", "LP-BAD-RESOURCE"):
                cons = "skip" if optional else "panic"
            else:
                cons = self.mismatch_consequence(key)
            out.append((ln, status, cons))
        statuses = {s for _, s, _ in out}
        if self.conf_missing or self.conf_dir:
            return 2, "CANNOT-EVALUATE", []
        if statuses & {"LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT", "LP-BAD-RESOURCE"}:
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
    decoy(c, "  path = boot():/%s#%s")
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

# ---- round-90 families (each certifies an r90 clause: R4/R6/R7 bad resource, R6/R9 efi image
# missing, R10 on_panic; finite sets are enumerated inside each case, QUALITY 128) ----

def efi_entry(c, protocol="efi", label=None):
    """An entry line and (unless protocol is None) one protocol key line with random blanks."""
    c.add("/%s" % (label or rname(c.rng, "")))
    if protocol is not None:
        c.add("%sprotocol:%s%s%s" % (c.rng.choice(["", "  ", "\t"]), c.rng.choice([" ", "\t", "  "]),
                                     protocol, c.rng.choice(["", " ", "\t"])))


def set_tpm(c, value):
    c.tpm = value
    c.tpm_fixed = True


def fam_efi_image_missing(c):
    """R6/R9: a missing pin on the image line of an efi chainload entry is `panic`; every case writes
    all three chainload protocol names and the IMAGE_PATH-only form."""
    c.header()
    for proto in EFI_PROTOCOLS:
        efi_entry(c, proto)
        c.pin("LP-MISSING")
    efi_entry(c, c.rng.choice(EFI_PROTOCOLS))
    c.pin("LP-MISSING", key="image_path")
    efi_entry(c)
    c.pin("OK")


def fam_non_efi_missing(c):
    """R9: the protocol is compared with strcmp against efi, uefi, efi_chainload only; a missing
    `path` pin in a linux, limine or efi_boot_entry entry, in an entry whose protocol is a case
    variant of a chainload name, or in an entry with no protocol line stays `not-modelled`."""
    c.header()
    for proto in ("linux", "limine", "efi_boot_entry",
                  c.rng.choice(["EFI", "Efi", "UEFI", "Uefi", "EFI_CHAINLOAD", "Efi_Chainload"]), None):
        efi_entry(c, proto)
        c.pin("LP-MISSING")
    efi_entry(c)
    c.pin("OK")


def fam_path_precedence(c):
    """R9: PATH is read before IMAGE_PATH whatever the line order. Every case: path OK then a missing
    image_path (not-modelled); a missing image_path written before a path OK line (not-modelled);
    image_path alone and missing (panic); path missing with image_path OK (panic on path)."""
    c.header()
    efi_entry(c)
    c.pin("OK")
    c.pin("LP-MISSING", key="image_path")
    efi_entry(c)
    c.pin("LP-MISSING", key="image_path")
    c.pin("OK")
    efi_entry(c)
    c.pin("LP-MISSING", key="image_path")
    efi_entry(c)
    c.pin("LP-MISSING")
    c.pin("OK", key="image_path")


def fam_first_path(c):
    """R9: the FIRST `path` key line (key case-insensitive) is the image line. Every case: first OK,
    second missing (second not-modelled); first missing in another key case, second OK (first
    panics); a non-pin first `path:` line (no hash) before a missing pin (not-modelled)."""
    c.header()
    efi_entry(c)
    c.pin("OK")
    c.pin("LP-MISSING", key=c.rng.choice(["path", "PATH", "Path"]))
    efi_entry(c)
    c.pin("LP-MISSING", key=c.rng.choice(["PATH", "Path", "pAth"]))
    c.pin("OK")
    efi_entry(c)
    c.add("  path: boot():/%s" % c.newfile())
    c.pin("LP-MISSING")


def fam_first_protocol(c):
    """R9: the FIRST protocol key line of the body decides (key case-insensitive). Every case: efi
    then linux (panic) and linux then efi (not-modelled)."""
    c.header()
    efi_entry(c, None)
    c.add("  %s: efi" % c.rng.choice(["PROTOCOL", "Protocol", "protocol"]))
    c.add("  protocol: linux")
    c.pin("LP-MISSING")
    efi_entry(c, None)
    c.add("  protocol: linux")
    c.add("  %s: efi" % c.rng.choice(["PROTOCOL", "Protocol", "protocol"]))
    c.pin("LP-MISSING")


def fam_entry_scope(c):
    """R9: a body ends at the next entry line, and lines before the first entry line belong to no
    entry. Every case: a global `protocol: efi` with a missing global path pin (not-modelled); an
    efi entry without a path followed by a protocol-less entry with a missing path (not-modelled);
    an efi parent whose child line `//name` carries only a missing path (not-modelled); an efi
    entry with an OK path followed by a protocol-less entry with only a missing image_path."""
    c.header()
    c.add("protocol: efi")
    c.pin("LP-MISSING", indent="")
    efi_entry(c)
    c.add("  cmdline: quiet")
    efi_entry(c, None)
    c.pin("LP-MISSING")
    efi_entry(c)
    c.add("  //%s" % rname(c.rng, ""))
    c.pin("LP-MISSING")
    efi_entry(c)
    c.pin("OK")
    efi_entry(c, None)
    c.pin("LP-MISSING", key="image_path")


def fam_protocol_decoy(c):
    """R9 with R1: `#protocol: efi`, `comment: protocol: efi`, `protocol = efi` and `protocol : efi`
    are not protocol key lines; an entry holding only those is not an efi entry. Every case writes
    all four in one entry, then an efi entry with a missing path (panic)."""
    c.header()
    efi_entry(c, None)
    c.add("  #protocol: efi")
    c.add("  comment: protocol: efi")
    c.add("  protocol = efi")
    c.add("  protocol : efi")
    c.pin("LP-MISSING")
    efi_entry(c)
    c.pin("LP-MISSING")


BAD_CASE = ("BOOT", "Boot", "GUID", "Uuid", "HDD", "FsLabel", "TFTP", "Odd")
BAD_OTHER = ("efi", "esp", "disk", "part", "nvme", "file")


def bad_names(c):
    """One of each kind of invalid name: empty, a case variant, a valid name with a suffix, another word."""
    return ["", c.rng.choice(BAD_CASE), c.rng.choice(VALID_RESOURCES) + c.rng.choice(["x", "2", "_", "s"]),
            c.rng.choice(BAD_OTHER)]


def fam_bad_resource(c):
    """R4/R6/R7: a resource name outside the seven is LP-BAD-RESOURCE, `panic`, DEGRADED. Every case
    writes an empty name, a case variant of a valid name, a valid name with a suffix and another
    word, each with or without the '$' marker (dropped before the compare)."""
    c.header()
    for name in bad_names(c):
        efi_entry(c)
        c.pin("LP-BAD-RESOURCE", key=c.rng.choice(["path", "kernel_path", "module_path"]),
              resource="%s(%s)" % (name, c.rng.choice(["", "1"])), gz=c.rng.random() < 0.5)
    efi_entry(c)
    c.pin("OK")


def fam_bad_resource_optional(c):
    """R6: LP-BAD-RESOURCE on wallpaper and term_font (key case varies) is `skip`; both every case."""
    c.header()
    for key in ("wallpaper", "term_font"):
        k = c.rng.choice([key, key.upper(), key.capitalize()])
        c.pin("LP-BAD-RESOURCE", key=k, indent="", resource="%s()" % c.rng.choice(bad_names(c)))
    efi_entry(c)
    c.pin("OK")


def fam_valid_resources(c):
    """R4: each of the seven valid names other than empty-root `boot` (hdd, odd, guid, uuid, fslabel,
    tftp, boot(N)), with or without '$', is LP-UNRESOLVED, never LP-BAD-RESOURCE; all seven every case."""
    c.header()
    for res in ("hdd(1:%d)" % c.rng.randint(1, 4), "odd(1:1)", "guid(%s)" % secrets.token_hex(4),
                "uuid(%s)" % secrets.token_hex(4), "fslabel(%s)" % rname(c.rng, ""), "tftp()",
                "boot(%d)" % c.rng.randint(1, 9)):
        efi_entry(c)
        c.pin("LP-UNRESOLVED", resource=res, gz=c.rng.random() < 0.5)


def fam_bad_over_unresolved(c):
    """R7: LP-BAD-RESOURCE is a fault: beside an LP-UNRESOLVED pin the verdict is DEGRADED rc 1."""
    c.header()
    efi_entry(c)
    c.pin("LP-UNRESOLVED", resource="guid(%s)" % secrets.token_hex(4))
    efi_entry(c)
    c.pin("LP-BAD-RESOURCE", resource="%s()" % c.rng.choice(bad_names(c)))


def fam_format_before_bad(c):
    """R3 before R4: a bad hash on an invalid resource name is LP-HASH-FORMAT."""
    c.header()
    efi_entry(c)
    c.pin("LP-HASH-FORMAT", resource="%s()" % c.rng.choice(bad_names(c)), hashfmt=bad_hash(c))
    efi_entry(c)
    c.pin("OK")


def measured(c, value="yes", indent=""):
    c.add("%s%s: %s" % (indent, c.rng.choice(["measured_boot", "MEASURED_BOOT", "Measured_Boot"]), value))


def panic_pins(c):
    efi_entry(c)
    c.pin("LP-MISSING")
    efi_entry(c)
    c.pin("OK")


def fam_measured_tpm(c, tpm):
    """R10: `measured_boot: yes` (key case varies) requests measured boot; --tpm-present 1 -> halt,
    0 -> menu, absent -> halt-if-tpm (one family per tpm state)."""
    c.header()
    measured(c)
    set_tpm(c, tpm)
    panic_pins(c)


def fam_measured_sb(c):
    """R10: --secure-boot-enforced 1 requests measured boot without any measured_boot key (or with
    `measured_boot: no`); --tpm-present 1 -> halt."""
    c.sb = True
    c.header()
    if c.rng.random() < 0.5:
        measured(c, "no")
    set_tpm(c, "1")
    panic_pins(c)


def fam_measured_value_case(c):
    """R10: the value is compared with strcmp; `Yes`, `YES`, `yEs` do not request (tpm 1 -> menu)."""
    c.header()
    measured(c, c.rng.choice(["Yes", "YES", "yEs", "yeS"]))
    set_tpm(c, "1")
    panic_pins(c)


def fam_measured_first(c):
    """R10: the FIRST measured_boot key line wins (tpm 1): `no` then `yes` -> menu, or `yes` then
    `no` -> halt; either order kills a last-wins gate."""
    c.header()
    first, second = ("no", "yes") if c.rng.random() < 0.5 else ("yes", "no")
    measured(c, first)
    set_tpm(c, "1")
    efi_entry(c)
    measured(c, second, indent="  ")
    c.pin("LP-MISSING")


def fam_measured_decoy(c):
    """R10 with R1: `# measured_boot: yes`, `comment: measured_boot: yes`, `measured-boot: yes`,
    `measured_boot = yes` and a cmdline carrying `measured_boot: yes` are not measured_boot key
    lines (tpm 1 -> menu); all five every case."""
    c.header()
    c.add("# measured_boot: yes")
    c.add("comment: measured_boot: yes")
    c.add("measured-boot: yes")
    c.add("measured_boot = yes")
    set_tpm(c, "1")
    efi_entry(c)
    c.add("  cmdline: quiet measured_boot: yes")
    c.pin("LP-MISSING")


def fam_measured_in_entry(c):
    """V1/R10: a `measured_boot` key line INSIDE an entry body is INVISIBLE to Limine (config.c
    cuts the buffer before the first '/' line). With --tpm-present 1 the measured_boot in the body
    must NOT request measured boot -> "menu"; the r90 whole-file read would say "halt"."""
    c.header()
    set_tpm(c, "1")
    efi_entry(c)
    measured(c, indent="  ")
    c.pin("LP-MISSING")
    efi_entry(c)
    c.pin("OK")

# ---- round-90 repairs of r89 routed defect 2 (clauses no r89 family drew; R89-R3, R89-R4) ----

def fam_large_file(c):
    """R5: the hash covers every stored byte; files of 1.1-2.5 MiB (above a 1 MiB read size), one OK
    and one whose pinned hash differs only in its LAST byte's content (r89 MutHeldOut survivors)."""
    c.header()
    big = c.blob(c.rng.randint(1153434, 2621440))
    efi_entry(c)
    c.pin("OK", data=big)
    efi_entry(c)
    data = c.blob(c.rng.randint(1153434, 2621440))
    rel = c.newfile(data)
    h = b2(data[:-1] + bytes([data[-1] ^ 0xFF]))
    ln = c.add("  path: boot():/%s#%s" % (rel, h))
    c.expect.append([ln, "LP-MISMATCH", "path"])


def fam_non_utf8(c):
    """R1/R7: a conf that is not valid UTF-8 (raw 0xff/0xfe/0xc3 bytes in a comment and a cmdline) is
    still read; its pins are judged as usual (r89 MutHeldOut survivors)."""
    c.header()
    c.add("# \udcff\udcfe %s" % secrets.token_hex(3))
    efi_entry(c)
    c.add("  cmdline: quiet x=\udcc3( \udcff")
    c.pin("OK")
    efi_entry(c)
    c.pin("LP-MISMATCH")


def fam_panic_after_pin(c):
    """V1/R6: a `hash_mismatch_panic: no` key line written AFTER the first entry line is INVISIBLE
    to Limine (config.c cuts the buffer before the first '/' line). A mismatch pin must get
    `panic`, not `prompt` — the r90 whole-file read would say `prompt`. The OK pin after it stays
    `none`; the mismatch forces DEGRADED."""
    c.header()
    efi_entry(c)
    c.pin("LP-MISMATCH")
    efi_entry(c)
    c.pin("OK")
    set_panic(c, c.rng.choice(["no", "No", "NO"]), indent="  ")

# ---- round-91 families (V1 global-section visibility; U1 unverified image lines) ----

def fam_global_vs_entry(c):
    """V1: `hash_mismatch_panic` and `measured_boot` are read only from the global section (lines
    before the first '/' entry line). A global `hash_mismatch_panic: no` + a `measured_boot: yes`
    inside an entry body: the panic setting IS visible (prompt), the measured_boot is NOT
    (on_panic stays "menu" even with --tpm-present 1). Kills a gate that reads either key
    whole-file."""
    c.header()
    set_panic(c, "no")
    efi_entry(c)
    c.pin("LP-MISMATCH")   # consequence prompt (global panic=no, no sb)
    measured(c, indent="  ")  # invisible: on_panic must stay "menu"
    set_tpm(c, "1")
    efi_entry(c)
    c.pin("OK")


def fam_first_line_entry(c):
    """V1 exception: when the FIRST physical line of the file is itself an entry line ('/...'),
    config.c's `c > config_addr` guard skips the cut and the WHOLE file stays visible — a
    `hash_mismatch_panic: no` or `measured_boot: yes` later in the file DOES count. This family
    puts the entry line first, then a global-looking panic key and a measured_boot, and expects
    prompt + halt-if-tpm/hal. Kills a gate that always cuts at the first '/' line."""
    c.header()
    # first physical line is an entry line (no header, no global keys before it)
    c.lines = []  # reset: header() already added lines; rebuild from scratch
    c.add("/%s" % rname(c.rng, ""))
    c.add("  protocol: efi")
    c.pin("LP-MISMATCH", indent="  ")
    # now a "global-looking" key AFTER the entry body — still visible because no cut happened
    set_panic(c, "no", indent="")
    measured(c, "yes", indent="")
    set_tpm(c, "1")
    efi_entry(c)
    c.pin("OK")


def fam_panic_global_only(c):
    """V1: a `hash_mismatch_panic: no` in the global section and ANOTHER `hash_mismatch_panic: yes`
    inside an entry body — only the global one counts (first visible wins; the entry one is
    invisible). Mismatch -> prompt. Kills a gate that reads the entry-body key or last-wins."""
    c.header()
    set_panic(c, "no")
    efi_entry(c)
    c.pin("LP-MISMATCH")
    set_panic(c, "yes", indent="  ")  # invisible
    efi_entry(c)
    c.pin("OK")


def fam_measured_global_only(c):
    """V1: `measured_boot: yes` in the global section requests measured boot; a `measured_boot: no`
    inside an entry body is invisible and must not veto it. --tpm-present 1 -> halt. Kills a gate
    that reads the entry-body key or last-wins."""
    c.header()
    measured(c, "yes")
    set_tpm(c, "1")
    efi_entry(c)
    measured(c, "no", indent="  ")  # invisible
    c.pin("LP-MISSING")
    efi_entry(c)
    c.pin("OK")


def fam_unverified_image(c):
    """U1: an efi entry's image line whose value has no URI shape (no '(' or no '):/') or no '#'
    hash is reported in unverified_image_lines and does NOT change any pin verdict. Every case
    writes a no-'(' value, a no-'):' value, a no-'#' value, and a valid pin — the first three land
    in the list, the pin does not."""
    c.header()
    efi_entry(c)
    ln1 = c.add("  path: %s" % rname(c.rng, ".efi"))  # no '(' at all
    efi_entry(c)
    ln2 = c.add("  path: boot()%s" % rname(c.rng, ".efi"))  # '(' but no '):/'
    efi_entry(c)
    ln3 = c.add("  path: boot():/%s" % rname(c.rng, ".efi"))  # '):/' but no '#'
    efi_entry(c)
    c.pin("OK")
    # record the three unverified lines as expectations via a side channel: they are image lines
    # with non-pin values, so want_unverified() picks them up automatically.
    return ln1, ln2, ln3


def fam_unverified_mixed(c):
    """U1: unverified_image_lines lists ONLY image lines with non-pin values. A missing pin
    (LP-MISSING, has '#'), a bad-resource pin, an unresolved pin, and a hash-format pin are all
    parseable pins and must NOT appear; only the no-'#' image line does. The verdicts stay
    DEGRADED/CANNOT-EVALUATE as R7 says."""
    c.header()
    efi_entry(c)
    c.pin("LP-MISSING")          # pin, not unverified
    efi_entry(c)
    c.pin("LP-BAD-RESOURCE", resource="bogus()")  # pin, not unverified
    efi_entry(c)
    c.pin("LP-UNRESOLVED", resource="guid(%s)" % secrets.token_hex(4))  # pin, not unverified
    efi_entry(c)
    c.pin("LP-HASH-FORMAT", hashfmt="xyz")  # pin, not unverified
    efi_entry(c)
    c.add("  path: boot():/%s" % rname(c.rng, ".efi"))  # no '#' -> unverified
    efi_entry(c)
    c.pin("OK")


def fam_unverified_non_efi(c):
    """U1: unverified_image_lines applies ONLY to efi chainload entries (R9). A `path:` with no
    URI shape in a linux or protocol-less entry is NOT an image line and must NOT be listed."""
    c.header()
    efi_entry(c, "linux")
    c.add("  path: %s" % rname(c.rng, ".efi"))  # non-efi, no URI shape -> not listed
    efi_entry(c, None)  # no protocol line
    c.add("  path: %s" % rname(c.rng, ".efi"))  # no protocol -> not listed
    efi_entry(c)
    c.add("  path: boot():/%s" % rname(c.rng, ".efi"))  # efi, no '#' -> listed
    efi_entry(c)
    c.pin("OK")


def fam_unverified_image_path(c):
    """U1/R9: the image line is the FIRST `path` else FIRST `image_path` key line. An efi entry
    with no `path` but an `image_path` carrying no URI shape -> that image_path line is listed.
    A second `path` line (not the image line) with no URI shape is NOT listed."""
    c.header()
    efi_entry(c)
    c.add("  image_path: boot():/%s" % rname(c.rng, ".efi"))  # image_path, no '#' -> listed
    c.add("  path: %s" % rname(c.rng, ".efi"))  # not image line (image_path won? no — path wins)
    # NOTE: R9 says image line = FIRST `path` else FIRST `image_path`. With BOTH present, `path`
    # wins, so the `path` line (no URI shape) is the image line and IS listed; image_path is not.
    efi_entry(c)
    c.add("  image_path: %s" % rname(c.rng, ".efi"))  # no path -> image_path is image line, no '(' -> listed
    efi_entry(c)
    c.pin("OK")


def fam_unverified_sorted(c):
    """U1: unverified_image_lines is sorted ascending by physical line number regardless of the
    order the entries appear. Six unverified image lines interleaved with OK pins and non-efi
    entries still sort; a gate that returns set-iteration order fails."""
    c.header()
    for i in range(6):
        efi_entry(c)
        if i % 2 == 0:
            c.add("  path: boot():/%s" % rname(c.rng, ".efi"))   # unverified (no '#')
        else:
            c.pin("OK")                                          # pin, not unverified
    efi_entry(c, "linux")
    c.add("  path: %s" % rname(c.rng, ".efi"))                    # non-efi, not listed
    efi_entry(c)
    c.pin("OK")


# ---- round-92 families (V2 version-selected visibility; pre-12.9.5 vs 12.9.5+) ----

def _era_first_line_panic(c, version, pass_version=True):
    """V2: the file's FIRST physical line is an entry line and its body carries a mismatch pin and,
    after the body, a `hash_mismatch_panic: no`. Pre-12.9.5 the cut is skipped (no bytes precede
    the '/') so the key IS visible -> `prompt`; from 12.9.5 on the label-end NUL leaves the global
    section empty so the key is INVISIBLE -> `panic`."""
    c.version = version
    c.pass_version = pass_version
    c.add("/%s" % rname(c.rng, ""))
    c.add("  protocol: efi")
    c.pin("LP-MISMATCH", indent="  ")
    set_panic(c, c.rng.choice(["no", "No", "NO"]), indent="")
    efi_entry(c)
    c.pin("OK")


def _era_first_line_measured(c, version):
    """V2: first line an entry, `measured_boot: yes` after its body, --tpm-present 1.
    Pre-12.9.5 the key is visible -> `halt`; from 12.9.5 on it is invisible -> `menu`."""
    c.version = version
    c.add("/%s" % rname(c.rng, ""))
    c.add("  protocol: efi")
    c.pin("OK", indent="  ")
    measured(c, "yes", indent="")
    set_tpm(c, "1")
    efi_entry(c)
    c.pin("OK")


def _era_global_key(c, version):
    """V2 control: a `hash_mismatch_panic: no` in a real global section (a header line precedes the
    first entry) answers `prompt` in BOTH eras — the era flag must not move a non-first-line case."""
    c.version = version
    c.header()
    set_panic(c, "no")
    efi_entry(c)
    c.pin("LP-MISMATCH")
    efi_entry(c)
    c.pin("OK")


def fam_era_fle_panic_a(c):
    _era_first_line_panic(c, "12.9.4")


def fam_era_fle_panic_b(c):
    _era_first_line_panic(c, "12.9.6")


def fam_era_fle_measured_a(c):
    _era_first_line_measured(c, "12.9.4")


def fam_era_fle_measured_b(c):
    _era_first_line_measured(c, "12.9.6")


def fam_era_global_key_a(c):
    _era_global_key(c, "12.9.5")


def fam_era_global_key_b(c):
    _era_global_key(c, "12.9.6")


def fam_era_default(c):
    """V2: with `--limine-version` omitted the gate applies the 12.9.4 rule (the host package), so
    the first-line-entry key is visible -> `prompt`. Kills a gate whose default is the new era."""
    _era_first_line_panic(c, "12.9.4", pass_version=False)


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
    "EFI-IMAGE-MISSING": fam_efi_image_missing,
    "NON-EFI-MISSING": fam_non_efi_missing,
    "PATH-PRECEDENCE": fam_path_precedence,
    "FIRST-PATH": fam_first_path,
    "FIRST-PROTOCOL": fam_first_protocol,
    "ENTRY-SCOPE": fam_entry_scope,
    "PROTOCOL-DECOY": fam_protocol_decoy,
    "BAD-RESOURCE": fam_bad_resource,
    "BAD-RESOURCE-OPTIONAL": fam_bad_resource_optional,
    "VALID-RESOURCES": fam_valid_resources,
    "BAD-OVER-UNRESOLVED": fam_bad_over_unresolved,
    "FORMAT-BEFORE-BAD": fam_format_before_bad,
    "MEASURED-TPM1": lambda c: fam_measured_tpm(c, "1"),
    "MEASURED-TPM0": lambda c: fam_measured_tpm(c, "0"),
    "MEASURED-TPM-ABSENT": lambda c: fam_measured_tpm(c, None),
    "MEASURED-SB": fam_measured_sb,
    "MEASURED-VALUE-CASE": fam_measured_value_case,
    "MEASURED-FIRST": fam_measured_first,
    "MEASURED-DECOY": fam_measured_decoy,
    "MEASURED-IN-ENTRY": fam_measured_in_entry,
    "LARGE-FILE": fam_large_file,
    "NON-UTF8": fam_non_utf8,
    "PANIC-AFTER-PIN": fam_panic_after_pin,
    "GLOBAL-VS-ENTRY": fam_global_vs_entry,
    "FIRST-LINE-ENTRY": fam_first_line_entry,
    "PANIC-GLOBAL-ONLY": fam_panic_global_only,
    "MEASURED-GLOBAL-ONLY": fam_measured_global_only,
    "UNVERIFIED-IMAGE": fam_unverified_image,
    "UNVERIFIED-MIXED": fam_unverified_mixed,
    "UNVERIFIED-NON-EFI": fam_unverified_non_efi,
    "UNVERIFIED-IMAGE-PATH": fam_unverified_image_path,
    "UNVERIFIED-SORTED": fam_unverified_sorted,
    "ERA-FLE-PANIC-A": fam_era_fle_panic_a,
    "ERA-FLE-PANIC-B": fam_era_fle_panic_b,
    "ERA-FLE-MEASURED-A": fam_era_fle_measured_a,
    "ERA-FLE-MEASURED-B": fam_era_fle_measured_b,
    "ERA-GLOBAL-KEY-A": fam_era_global_key_a,
    "ERA-GLOBAL-KEY-B": fam_era_global_key_b,
    "ERA-DEFAULT": fam_era_default,
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
    "EFI-IMAGE-MISSING", "NON-EFI-MISSING", "PATH-PRECEDENCE", "FIRST-PATH", "FIRST-PROTOCOL",
    "ENTRY-SCOPE", "PROTOCOL-DECOY", "BAD-RESOURCE", "BAD-RESOURCE-OPTIONAL", "VALID-RESOURCES",
    "BAD-OVER-UNRESOLVED", "FORMAT-BEFORE-BAD", "MEASURED-TPM1", "MEASURED-TPM0",
    "MEASURED-TPM-ABSENT", "MEASURED-SB", "MEASURED-VALUE-CASE", "MEASURED-FIRST", "MEASURED-DECOY",
    "MEASURED-IN-ENTRY", "LARGE-FILE", "NON-UTF8", "PANIC-AFTER-PIN",
    "GLOBAL-VS-ENTRY", "FIRST-LINE-ENTRY", "PANIC-GLOBAL-ONLY", "MEASURED-GLOBAL-ONLY",
    "UNVERIFIED-IMAGE", "UNVERIFIED-MIXED", "UNVERIFIED-NON-EFI", "UNVERIFIED-IMAGE-PATH",
    "UNVERIFIED-SORTED",
    "ERA-FLE-PANIC-A", "ERA-FLE-PANIC-B", "ERA-FLE-MEASURED-A", "ERA-FLE-MEASURED-B",
    "ERA-GLOBAL-KEY-A", "ERA-GLOBAL-KEY-B", "ERA-DEFAULT",
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
        with open(conf, "w", newline="", encoding="utf-8", errors="surrogateescape") as f:
            f.write(c.eol.join(c.lines) + c.eol)
    if not c.sb and c.sbflag is None and rng.random() < 0.3:
        c.sbflag = "0"
    if not c.tpm_fixed:
        c.tpm = rng.choice([None, "0", "1"])
    return c, d, conf, esp


BWRAP = shutil.which("bwrap")


def sandbox_argv(gate, case_dir, inner):
    """C1 ISOLATION: wrap `inner` (the gate argv) in the bwrap allowlist described in the module
    docstring. Only /usr, /etc, a fresh /dev, /proc, /tmp, the gate-copy file and the case directory
    are visible; the caller's environment is cleared."""
    return [BWRAP, "--unshare-user", "--unshare-uts", "--unshare-cgroup", "--unshare-ipc",
            "--unshare-net", "--die-with-parent", "--new-session", "--clearenv",
            "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp",
            "--ro-bind", "/usr", "/usr", "--ro-bind", "/etc", "/etc",
            "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
            "--symlink", "usr/bin", "/bin", "--symlink", "usr/bin", "/sbin",
            "--ro-bind", gate, gate, "--ro-bind", case_dir, case_dir,
            "--chdir", case_dir, "--setenv", "PATH", "/usr/bin", "--setenv", "HOME", "/tmp",
            "--setenv", "LC_ALL", "C", "--setenv", "TMPDIR", "/tmp", "--"] + inner


def copy_gate(gate, work):
    """C1: the gate runs from a private directory that holds nothing but the gate's bytes, so a
    sibling-path lookup for the battery finds nothing."""
    d = tempfile.mkdtemp(prefix="gate-", dir=work)
    dst = os.path.join(d, "gate.py")
    shutil.copyfile(gate, dst)
    return d, dst


def run_gate(gate, conf, esp, c, cwd):
    inner = [sys.executable, "-I", gate, "--conf", conf, "--esp", esp]
    if c.pass_version:
        inner += ["--limine-version", c.version]
    if c.sb:
        inner += ["--secure-boot-enforced", "1"]
    elif c.sbflag is not None:
        inner += ["--secure-boot-enforced", c.sbflag]
    if c.tpm is not None:
        inner += ["--tpm-present", c.tpm]
    argv = sandbox_argv(gate, cwd, inner)
    try:
        p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return None, "timeout"
    try:
        out = json.loads(p.stdout)
        pins = sorted((int(x["line"]), str(x["status"]), str(x["consequence"])) for x in out["pins"])
        entries = {int(x["line"]): x["entry"] for x in out["pins"] if "entry" in x}
        panic = ("present", out["hash_mismatch_panic"]) if "hash_mismatch_panic" in out else ("absent", None)
        got = (p.returncode, out["verdict"], pins, out["rc"], entries, panic, out.get("on_panic"),
               out.get("unverified_image_lines"))
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

def u1_ok(c, got):
    """U1: unverified_image_lines, when the conf is readable, must equal the expected sorted list.
    Absent field or unreadable conf -> not checked here."""
    if c.conf_missing or c.conf_dir:
        return True
    want = c.want_unverified()
    got_list = got[7]
    if got_list is None:
        return False
    try:
        got_sorted = [int(x) for x in got_list]
        return got_sorted == want and got_sorted == sorted(got_sorted)
    except Exception:
        return False


def run_battery(gate, work):
    rng = random.Random(secrets.randbits(64))
    root = tempfile.mkdtemp(prefix="limine-battery-r92-", dir=work)
    gdir = gpath = None
    try:
        if os.path.isfile(gate):
            gdir, gpath = copy_gate(gate, root)
        plan = [f for f in FAMILY_ROSTER for _ in range(CASES_PER_FAMILY)]
        rng.shuffle(plan)
        log = []
        for fam in plan:
            c, d, conf, esp = build(fam, rng, root)
            want = c.finish()
            got, err = ((None, "gate absent") if gpath is None
                        else run_gate(gpath, conf, esp, c, d))
            want_op = None if (c.conf_missing or c.conf_dir) else c.want_on_panic()
            ok = (got is not None and got[0] == want[0] and got[3] == want[0] and got[1] == want[1]
                  and [list(x) for x in got[2]] == [list(x) for x in want[2]] and r8_ok(c, got)
                  and u1_ok(c, got)
                  and (want_op is None or got[6] == want_op))
            log.append({"family": fam, "passed": ok, "sbflag": "1" if c.sb else c.sbflag, "tpm": c.tpm,
                        "want": [want[0], want[1], [list(x) for x in want[2]], want_op],
                        "got": None if got is None else [got[0], got[1], [list(x) for x in got[2]], got[3],
                                                         got[6]],
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
    return {"schema": "tsukuroi-limine-pin-battery-r92-v1", "gate": gate,
            "families_total": len(FAMILY_ROSTER), "families_passed": len(passed),
            "failed_families": failed, "cases": len(log), "verdict": "met" if met else "unmet",
            "case_log": log}


# One-field lie wrappers (r87 routed R87-R1): each runs the positive gate and falsifies exactly one
# field of its answer; a battery that misses any of them does not check that field.
LIE_WRAPPER = '''import json, os, subprocess, sys, tempfile
GATE_SRC = %r
d = tempfile.mkdtemp(prefix="lie-", dir="/tmp")
g = os.path.join(d, "gate.py")
with open(g, "w") as f:
    f.write(GATE_SRC)
p = subprocess.run([sys.executable, "-I", g] + sys.argv[1:], capture_output=True, text=True)
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
elif KIND == "on-panic" and "on_panic" in out:
    out["on_panic"] = {"menu": "halt", "halt": "menu", "halt-if-tpm": "halt"}.get(out["on_panic"], "menu")
elif KIND == "bad-resource":
    for x in pins:
        if x["status"] == "LP-BAD-RESOURCE":
            x["status"] = "LP-UNRESOLVED"
elif KIND == "missing-panic":
    for x in pins:
        if x["status"] == "LP-MISSING" and x["consequence"] == "panic":
            x["consequence"] = "not-modelled"
print(json.dumps(out))
sys.exit(rc)
'''
LIE_KINDS = ("exit-code", "rc-field", "line", "consequence", "status", "verdict", "entry", "panic-line",
             "panic-value", "on-panic", "bad-resource", "missing-panic")

SELFTEST_GATES = {
    # name: (source, must_meet)
    "absent": (None, False),
    "constant-healthy": ('import json,sys\nprint(json.dumps({"verdict":"HEALTHY","rc":0,"pins":[]}))\n', False),
    "non-json": ('print("hello")\n', False),
    "constant-degraded": ('import json,sys\nprint(json.dumps({"verdict":"DEGRADED","rc":1,"pins":[]}))\nsys.exit(1)\n', False),
}


def selftest(ref=None):
    """The literal roster equals FAMILIES; negative controls must read unmet. With --reference GATE
    (a gate the round has scored `met`), that gate must read met with every roster family run
    CASES_PER_FAMILY times and each one-field lie wrapped around it must read unmet; without it the
    reference leg is reported as `skipped`, never as a pass. Paths resolve from this file, not the
    cwd; the run happens from an unrelated cwd."""
    results = [("roster-literal", tuple(FAMILIES) == FAMILY_ROSTER, len(FAMILY_ROSTER))]
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
        if ref is not None and os.path.isfile(ref):
            r = run_battery(ref, work)
            counts = {}
            for e in r["case_log"]:
                counts[e["family"]] = counts.get(e["family"], 0) + 1
            full = all(counts.get(f) == CASES_PER_FAMILY for f in FAMILY_ROSTER)
            results.append(("reference-gate", r["verdict"] == "met" and full, r["families_passed"]))
            with open(ref, "r", encoding="utf-8", errors="surrogateescape") as f:
                gate_src = f.read()
            for kind in LIE_KINDS:
                g = os.path.join(work, "lie-%s.py" % kind)
                with open(g, "w") as f:
                    f.write(LIE_WRAPPER % (gate_src, kind))
                r = run_battery(g, work)
                results.append(("lie-" + kind, r["verdict"] == "unmet", r["families_passed"]))
        elif ref is not None:
            results.append(("reference-gate", False, "missing " + ref))
        else:
            print("reference-gate      skipped (no --reference)")
    finally:
        os.chdir(old)
        shutil.rmtree(work, ignore_errors=True)
    ok = all(x[1] for x in results)
    for name, good, n in results:
        print("%-18s %s families_passed=%s" % (name, "PASS" if good else "FAIL", n))
    print("selftest %s %d/%d" % ("PASS" if ok else "FAIL", sum(x[1] for x in results), len(results)))
    return 0 if ok else 1


PROBE_SRC = '''import json, os, sys
print(json.dumps({
    "cwd": os.getcwd(),
    "root": sorted(os.listdir("/")),
    "cwd_entries": sorted(os.listdir(os.getcwd())),
    "sibling_files": sorted(os.listdir(os.path.dirname(os.path.abspath(__file__)))),
    "lane_visible": os.path.exists("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"),
    "battery_visible": os.path.exists(
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/limine-pin-battery-r92.py"),
    "env": dict(os.environ),
    "pids": sorted(p for p in os.listdir("/proc") if p.isdigit()),
    "sys_path": sys.path,
}))
'''


def isolation_check(work):
    """Print what a probe process sees under the ISOLATION launcher: the receipt that the sandbox
    binds only /usr, /etc, /dev, /proc, /tmp, the gate copy and the case directory."""
    os.makedirs(work, exist_ok=True)
    root = tempfile.mkdtemp(prefix="limine-iso-", dir=work)
    try:
        probe = os.path.join(root, "probe.py")
        with open(probe, "w") as f:
            f.write(PROBE_SRC)
        _gdir, gpath = copy_gate(probe, root)
        case = os.path.join(root, "case")
        os.makedirs(case)
        inner = [sys.executable, "-I", gpath]
        p = subprocess.run(sandbox_argv(gpath, case, inner), cwd=case, capture_output=True,
                           text=True, timeout=TIMEOUT)
        print(p.stdout.strip())
        if p.returncode != 0:
            print("isolation-check exit %d stderr=%s" % (p.returncode, p.stderr[-500:]),
                  file=sys.stderr)
        return 0 if p.returncode == 0 else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


def usage_check(gate, work):
    """V2 refusal contract: `--limine-version` outside X.Y.Z is a usage error (rc 64), never a
    silent default, and an accepted value on a healthy fixture is rc 0. Runs through the same
    ISOLATION launcher; prints one JSON object; exit 0 iff every expectation held."""
    os.makedirs(work, exist_ok=True)
    root = tempfile.mkdtemp(prefix="limine-usage-", dir=work)
    try:
        _gdir, gpath = copy_gate(os.path.abspath(gate), root)
        case = os.path.join(root, "case")
        esp = os.path.join(case, "esp")
        os.makedirs(os.path.join(esp, "EFI", "Linux"))
        data = b"usage-check"
        with open(os.path.join(esp, "EFI", "Linux", "a.efi"), "wb") as f:
            f.write(data)
        h = hashlib.blake2b(data).hexdigest()
        conf = os.path.join(case, "limine.conf")
        with open(conf, "w") as f:
            f.write("/e\npath: boot():/EFI/Linux/a.efi#%s\n" % h)
        cases = [("12.9", 64), ("abc", 64), ("12.9.6.1", 64), ("", 64),
                 ("12.9.4", 0), ("12.9.5", 0), ("13.0.0", 0), (None, 0)]
        rows = []
        for version, want in cases:
            inner = [sys.executable, "-I", gpath, "--conf", conf, "--esp", esp]
            if version is not None:
                inner += ["--limine-version", version]
            p = subprocess.run(sandbox_argv(gpath, case, inner), cwd=case, capture_output=True,
                               text=True, timeout=TIMEOUT)
            rows.append({"version": version, "want_rc": want, "rc": p.returncode,
                         "ok": p.returncode == want})
        ok = all(r["ok"] for r in rows)
        print(json.dumps({"schema": "tsukuroi-limine-pins-usage-r92-v1", "gate": os.path.abspath(gate),
                          "cases": rows, "verdict": "met" if ok else "unmet"}, indent=1))
        return 0 if ok else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--gate")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--work", default=os.environ.get("TMPDIR"))
    ap.add_argument("--json")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--reference")
    ap.add_argument("--isolation-check", action="store_true")
    ap.add_argument("--usage-check", action="store_true")
    a = ap.parse_args()
    if tuple(FAMILIES) != FAMILY_ROSTER:
        print("FAMILIES differs from FAMILY_ROSTER", file=sys.stderr)
        return 2
    if a.selftest:
        return selftest(os.path.abspath(a.reference) if a.reference else None)
    if not BWRAP:
        print("bwrap not found: the isolation launcher is required (see ISOLATION)", file=sys.stderr)
        return 2
    if a.isolation_check:
        return isolation_check(a.work or tempfile.gettempdir())
    if a.usage_check:
        if not a.gate:
            ap.print_usage(sys.stderr)
            return 2
        return usage_check(a.gate, a.work or tempfile.gettempdir())
    if not a.gate or a.runs < 1:
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
