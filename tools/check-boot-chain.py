#!/usr/bin/env python3
"""Read-only round-17 next-boot verdict gate for the limine entry corpus.

Binds corpus/knowledge/boot-chain-r17.json (schema tsukuroi-boot-chain-v2)
and its .md twin to the four pinned L1 read-only captures named by the
JSON's `captures` map, and re-derives every entry's verdict from that
entry's own fields with the corpus's ordered rule table (first match):

  1 mkinitcpio_version is null -> NOT-A-KERNEL-ENTRY
  2 selected_this_boot, image sha256 equal to the /boot image whose uname
    is the running kernel, efi_path equal to that image's extraction
    block, uname and rootflags equal to the boot block, and a cited
    "no newer boot-chain input" witness -> BOOTED-OBSERVED
  3 snapshot is null and selected_this_boot is false -> UNTESTED
  4 /sysroot init, image_new_root 'symlink->sysroot', both hook_roots
    '/new_root' -> PATH-ALIASED-EMULATED
  5 /new_root init, image_new_root 'directory', both hook_roots
    '/new_root' -> CONSISTENT-PRE42
  6 otherwise -> UNTESTED

Every cited `capture_path:line` evidence ref must resolve against the
pinned capture map and contain the claimed sha256, uname, mkinitcpio
VERSION, init root-reference counts, btrfs-overlayfs root_mnt, plymouth
--new-root-dir and rootflags strings; the b2sum prefix must equal the
`path:` #hash of the entry's own limine.conf line; each kernel entry must
also agree with its own `### <efi_path>` image-extraction block. The boot
block's evidence must witness running_kernel, boot_start,
cmdline_rootflags and loader_entry_selected. The MD must carry
source:/verified-at:/recheck:, the headings ## Decision table, ##
Falsifier, ## QUALITY check and ## Sources, and every entry id inside
## Decision table.

--revision admits only an explicit 7-64 hex commit and binds it to
refs/heads/<--branch> (default master) and, when that ref exists, to
refs/remotes/origin/<branch>: HEAD, @, @- and ref names are rejected
because under jj colocation HEAD is @-, not the branch tip. Exit 0 clean,
1 failed, 2 could-not-evaluate. Reads immutable git objects only; no
writes, no network, no host queries, no boot/package/service action.
"""
from __future__ import annotations
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, namedtuple
from pathlib import Path

PASS, FAIL, CANNOT = 0, 1, 2
ROOT = Path(__file__).resolve().parents[1]
JSON17 = "corpus/knowledge/boot-chain-r17.json"
MD17 = "corpus/knowledge/boot-chain-r17.md"
SCHEMA = "tsukuroi-boot-chain-v2"
CAPTURES = {
    "boot": ".ufo/waves/round-17/l1-capture/boot-chain-capture.txt",
    "fresh": ".ufo/waves/round-17/l1-capture/fresh-capture.txt",
    "emulation": ".ufo/waves/round-17/l1-capture/overlay-emulation.txt",
    "supplement": ".ufo/waves/round-17/l1-capture/supplement-capture.txt",
}
NOT_KERNEL = "NOT-A-KERNEL-ENTRY"
RULE_TABLE = ((1, "NOT-A-KERNEL-ENTRY"), (2, "BOOTED-OBSERVED"),
              (3, "UNTESTED"), (4, "PATH-ALIASED-EMULATED"),
              (5, "CONSISTENT-PRE42"), (6, "UNTESTED"))
ENTRY_KEYS = ("id", "limine_label", "efi_path", "sha256", "b2sum_prefix",
              "uname", "mkinitcpio_version", "init_sysroot_refs",
              "init_new_root_refs", "image_new_root", "hook_roots",
              "rootflags", "snapshot", "snapshot_ro", "selected_this_boot",
              "verdict", "evidence", "note")
ENTRY_SPEC = (("id", "str"), ("limine_label", "str"), ("efi_path", "str"),
              ("sha256", "str?"), ("b2sum_prefix", "str?"), ("uname", "str?"),
              ("mkinitcpio_version", "str?"), ("init_sysroot_refs", "int?"),
              ("init_new_root_refs", "int?"), ("image_new_root", "str?"),
              ("hook_roots", "dict"), ("rootflags", "str?"),
              ("snapshot", "int?"), ("snapshot_ro", "bool?"),
              ("selected_this_boot", "bool?"), ("verdict", "str"),
              ("evidence", "list"), ("note", "str"))
TOP_KEYS = ("schema", "captured_at", "captures", "boot", "verdict_rules",
            "entries", "superseded", "authority")
BOOT_KEYS = ("running_kernel", "boot_start", "cmdline_rootflags",
             "loader_entry_selected", "evidence")
HOOKS = ("btrfs-overlayfs", "plymouth")
MD_HEADINGS = ("## Decision table", "## Falsifier", "## QUALITY check",
               "## Sources")
MD_HEADER = ("source:", "verified-at:", "recheck:")
REV = re.compile(r"^[0-9a-fA-F]{7,64}$")
# refs/heads/<branch> is always built explicitly, so a branch name can
# never be parsed as a git option.
BRANCH = re.compile(r"^(?!-)(?!.*\.\.)(?!.*//)[A-Za-z0-9._/-]{1,255}$")
B2_PATH = re.compile(r"path:\s*(?P<path>\S+)#(?P<hash>[0-9a-f]{16,})")
BLOCK_SHA = re.compile(r"^sha256 (?P<v>[0-9a-f]{64})\s*$")
BLOCK_UNAME = re.compile(r"^uname\s+(?P<v>\S+)\s*$")
BLOCK_VERSION = re.compile(r"^VERSION\s+(?P<v>\S+)\s*$")
BLOCK_REFS = re.compile(r"^init /sysroot refs (?P<s>\d+) ; /new_root refs "
                        r"(?P<n>\d+)\s*$")
BLOCK_ROOT_MNT = re.compile(r'root_mnt="(?P<v>[^"]*)"')
BLOCK_NEW_ROOT = re.compile(r"--new-root-dir=(?P<v>\S+)")

Finding = namedtuple("Finding", "id site detail")
DocSet = namedtuple("DocSet", "json17 md17 captures")
Result = namedtuple("Result", "code findings verdicted entries")


class Cannot(Exception):
    def __init__(self, fid, site, detail):
        super().__init__(detail)
        self.fid, self.site, self.detail = fid, site, detail


def as_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def type_ok(value, spec):
    if spec == "str":
        return isinstance(value, str)
    if spec == "str?":
        return value is None or isinstance(value, str)
    if spec == "int?":
        return value is None or as_int(value)
    if spec == "bool?":
        return value is None or isinstance(value, bool)
    if spec == "list":
        return isinstance(value, list)
    if spec == "dict":
        return isinstance(value, dict)
    return False


def extraction_blocks(lines):
    """`### <efi_path>` image-extraction blocks keyed by the exact path."""
    blocks, current = {}, None
    for line in lines:
        if line.startswith("### "):
            current = {"path": line[4:].strip(), "sha256": None, "uname": None,
                       "version": None, "refs": None, "root_mnt": None,
                       "new_root_dir": None}
            blocks[current["path"]] = current
            continue
        if current is None:
            continue
        if line.startswith("$ "):
            current = None
            continue
        for key, pattern in (("sha256", BLOCK_SHA), ("uname", BLOCK_UNAME),
                             ("version", BLOCK_VERSION)):
            match = pattern.match(line)
            if match and current[key] is None:
                current[key] = match.group("v")
        match = BLOCK_REFS.match(line)
        if match and current["refs"] is None:
            current["refs"] = (int(match.group("s")), int(match.group("n")))
        match = BLOCK_ROOT_MNT.search(line)
        if match and current["root_mnt"] is None:
            current["root_mnt"] = match.group("v")
        match = BLOCK_NEW_ROOT.search(line)
        if match and current["new_root_dir"] is None:
            current["new_root_dir"] = match.group("v")
    return blocks


def all_blocks(lines_by_path):
    merged = {}
    for lines in lines_by_path.values():
        for path, block in extraction_blocks(lines).items():
            merged.setdefault(path, block)
    return merged


def parse_evidence(value, lines_by_path, site):
    """Resolve `capture_path:line` refs to (ref, line) pairs."""
    if not isinstance(value, list):
        return [Finding("BOOTCHAIN-EVIDENCE-LINE", site,
                        "evidence must be an array")], []
    out, cited = [], []
    for ref in value:
        if not isinstance(ref, str) or ":" not in ref:
            out.append(Finding("BOOTCHAIN-EVIDENCE-LINE", site,
                               f"evidence ref {ref!r} is not `capture_path:line`"))
            continue
        path, _, tail = ref.rpartition(":")
        number = int(tail) if tail.isdigit() else -1
        lines = lines_by_path.get(path)
        if lines is None:
            out.append(Finding("BOOTCHAIN-EVIDENCE-PATH", site,
                               f"capture {path!r} not in the captures map"))
            continue
        if not 1 <= number <= len(lines):
            out.append(Finding("BOOTCHAIN-EVIDENCE-LINE", site,
                               f"{ref!r} outside {path} 1-{len(lines)}"))
            continue
        cited.append((ref, lines[number - 1]))
    return out, cited


def context(doc, lines_by_path):
    """The boot identity a verdict may be re-derived against."""
    boot = doc.get("boot") if isinstance(doc.get("boot"), dict) else {}
    blocks = all_blocks(lines_by_path)
    running = boot.get("running_kernel")
    booted = [b for b in blocks.values()
              if b["path"].startswith("/boot/EFI/Linux/") and b["sha256"]
              and b["uname"] == running]
    return {"running": running,
            "booted_sha": booted[0]["sha256"] if len(booted) == 1 else None,
            "booted_path": booted[0]["path"] if len(booted) == 1 else None,
            "rootflags": boot.get("cmdline_rootflags"),
            "blocks": blocks}


def no_newer_witness(cited):
    return any("none newer" in line or line.strip() == "0"
               for _, line in cited)


def derive(entry, ctx, cited):
    if entry.get("mkinitcpio_version") is None:
        return NOT_KERNEL
    hooks = entry.get("hook_roots") if isinstance(entry.get("hook_roots"),
                                                  dict) else {}
    if (entry.get("selected_this_boot") is True
            and ctx["booted_sha"] is not None
            and entry.get("sha256") == ctx["booted_sha"]
            and entry.get("efi_path") == ctx["booted_path"]
            and entry.get("uname") == ctx["running"]
            and entry.get("rootflags") == ctx["rootflags"]
            and no_newer_witness(cited)):
        return "BOOTED-OBSERVED"
    if entry.get("snapshot") is None and entry.get("selected_this_boot") is False:
        return "UNTESTED"
    sysroot, new_root = entry.get("init_sysroot_refs"), entry.get("init_new_root_refs")
    both_new_root = (hooks.get("btrfs-overlayfs") == "/new_root"
                     and hooks.get("plymouth") == "/new_root")
    if (as_int(sysroot) and sysroot > 0 and new_root == 0
            and entry.get("image_new_root") == "symlink->sysroot"
            and both_new_root):
        return "PATH-ALIASED-EMULATED"
    if (as_int(new_root) and new_root > 0 and sysroot == 0
            and entry.get("image_new_root") == "directory"
            and both_new_root):
        return "CONSISTENT-PRE42"
    return "UNTESTED"


def block_issue(entry, blocks):
    """The entry must agree with its own `### <efi_path>` extraction block."""
    if entry.get("mkinitcpio_version") is None:
        return None
    path, eid = entry.get("efi_path"), entry.get("id")
    block = blocks.get(path)
    if block is None:
        return Finding("BOOTCHAIN-BLOCK", eid,
                       f"no `### {path}` extraction block in the captures")
    for field, want in (("sha256", entry.get("sha256")),
                        ("uname", entry.get("uname")),
                        ("version", entry.get("mkinitcpio_version"))):
        if want is not None and block[field] != want:
            return Finding("BOOTCHAIN-BLOCK", eid,
                           f"{field} block={block[field]!r} entry={want!r}")
    refs = (entry.get("init_sysroot_refs"), entry.get("init_new_root_refs"))
    if as_int(refs[0]) and as_int(refs[1]) and block["refs"] != refs:
        return Finding("BOOTCHAIN-BLOCK", eid,
                       f"init refs block={block['refs']!r} entry={refs!r}")
    hooks = entry.get("hook_roots") if isinstance(entry.get("hook_roots"),
                                                  dict) else {}
    if (isinstance(hooks.get("btrfs-overlayfs"), str)
            and block["root_mnt"] != hooks["btrfs-overlayfs"]):
        return Finding("BOOTCHAIN-BLOCK", eid,
                       f"root_mnt block={block['root_mnt']!r}")
    if (isinstance(hooks.get("plymouth"), str)
            and block["new_root_dir"] != hooks["plymouth"]):
        return Finding("BOOTCHAIN-BLOCK", eid,
                       f"--new-root-dir block={block['new_root_dir']!r}")
    return None


def b2sum_issue(entry, lines_by_path):
    prefix = entry.get("b2sum_prefix")
    if prefix is None:
        return None
    want = "boot():" + str(entry.get("efi_path", "")).removeprefix("/boot")
    for lines in lines_by_path.values():
        for line in lines:
            match = B2_PATH.search(line)
            if match and match.group("path") == want \
                    and match.group("hash").startswith(prefix):
                return None
    return Finding("BOOTCHAIN-B2SUM", entry.get("id"),
                   f"no `path: {want}#{prefix}…` limine.conf line in the captures")


TYPED_DIR = re.compile(r"^d[rwx-]{9}\s+(?:\S+\s+)*new_root\s*$")


def typed_root_findings(entry, cited, eid):
    """R17-TYPE-BLIND: the image's /new_root kind must be typed by a cited line.

    A name-only listing (`dirs: new_root sysroot`) cannot tell a directory from a
    symlink, so it never witnesses the kind (QUALITY 25)."""
    kind = entry.get("image_new_root")
    if entry.get("mkinitcpio_version") is None:
        if kind is not None:
            return [Finding("BOOTCHAIN-FIELD", eid,
                            "image_new_root must be null for a non-kernel entry")]
        return []
    if kind not in ("symlink->sysroot", "directory"):
        return [Finding("BOOTCHAIN-FIELD", eid,
                        f"image_new_root {kind!r} not in symlink->sysroot|directory")]
    lines = [line.strip() for _, line in cited]
    if kind == "symlink->sysroot":
        typed = any("new_root -> sysroot" in line for line in lines)
    else:
        typed = any(TYPED_DIR.match(line) for line in lines)
    if typed:
        return []
    return [Finding("BOOTCHAIN-UNTYPED", eid,
                    f"no cited line types /new_root as {kind}; a name-only "
                    "listing is not a witness")]


def entry_findings(entry, lines_by_path, ctx):
    out = []
    eid = entry.get("id") if isinstance(entry.get("id"), str) else "entry"
    issues, cited = parse_evidence(entry.get("evidence"), lines_by_path, eid)
    out += issues
    for field, fid in (("sha256", "BOOTCHAIN-SHA256"),
                       ("uname", "BOOTCHAIN-UNAME"),
                       ("rootflags", "BOOTCHAIN-ROOTFLAGS")):
        value = entry.get(field)
        if isinstance(value, str) and not any(value in line for _, line in cited):
            out.append(Finding(fid, eid,
                               f"claimed {field} {value!r} appears in no cited line"))
    version = entry.get("mkinitcpio_version")
    if isinstance(version, str) and not any(
            f"VERSION {version}" in line for _, line in cited):
        out.append(Finding("BOOTCHAIN-VERSION", eid,
                           f"claimed VERSION {version} appears in no cited line"))
    sysroot, new_root = entry.get("init_sysroot_refs"), entry.get("init_new_root_refs")
    if as_int(sysroot) and as_int(new_root) and not any(
            f"init /sysroot refs {sysroot} ; /new_root refs {new_root}" in line
            for _, line in cited):
        out.append(Finding("BOOTCHAIN-INIT-REFS", eid,
                           f"claimed init refs {sysroot}/{new_root} appear in no "
                           "cited line"))
    hooks = entry.get("hook_roots") if isinstance(entry.get("hook_roots"),
                                                  dict) else {}
    for hook, needle in (("btrfs-overlayfs", 'root_mnt="{}"'),
                         ("plymouth", "--new-root-dir={}")):
        value = hooks.get(hook)
        if isinstance(value, str) and not any(
                needle.format(value) in line for _, line in cited):
            out.append(Finding("BOOTCHAIN-HOOK-ROOT", eid,
                               f"claimed {hook} {value} appears in no cited line"))
    out += typed_root_findings(entry, cited, eid)
    issue = b2sum_issue(entry, lines_by_path)
    if issue:
        out.append(issue)
    issue = block_issue(entry, ctx["blocks"])
    if issue:
        out.append(issue)
    derived = derive(entry, ctx, cited)
    if entry.get("verdict") != derived:
        out.append(Finding("BOOTCHAIN-VERDICT", eid,
                           f"recorded={entry.get('verdict')!r} derived={derived}"))
    return out, derived


def doc_findings(doc):
    """Top-level, rule-table, entry-shape and id findings plus the entries."""
    if not isinstance(doc, dict):
        return [Finding("BOOTCHAIN-SCHEMA", JSON17, "top-level object required")], []
    out = []
    extra = sorted(key for key in doc if key not in TOP_KEYS)
    missing = [key for key in TOP_KEYS if key not in doc]
    if extra:
        out.append(Finding("BOOTCHAIN-SCHEMA", JSON17,
                           "extra top-level keys=" + ",".join(extra)))
    if missing:
        out.append(Finding("BOOTCHAIN-SCHEMA", JSON17,
                           "missing top-level keys=" + ",".join(missing)))
    if doc.get("schema") != SCHEMA:
        out.append(Finding("BOOTCHAIN-SCHEMA", JSON17,
                           f"schema={doc.get('schema')!r} != {SCHEMA}"))
    if doc.get("captures") != CAPTURES:
        out.append(Finding("BOOTCHAIN-CAPTURE-PATH", "captures",
                           f"capture map {doc.get('captures')!r} != pinned"))
    authority = doc.get("authority")
    if not isinstance(authority, str) or "authorizes no" not in authority.lower():
        out.append(Finding("BOOTCHAIN-SCHEMA", JSON17,
                           "authority must state that it authorizes no action"))
    superseded = doc.get("superseded")
    if not isinstance(superseded, str) or not superseded.strip():
        out.append(Finding("BOOTCHAIN-SCHEMA", JSON17,
                           "superseded must be a non-empty string"))
    rules = doc.get("verdict_rules")
    table = None
    if isinstance(rules, list) and all(isinstance(r, dict) for r in rules):
        table = [(r.get("order"), r.get("verdict")) for r in rules]
    if table != list(RULE_TABLE):
        out.append(Finding("BOOTCHAIN-RULES", "verdict_rules",
                           f"order/verdict table={table!r} != {list(RULE_TABLE)!r}"))
    entries = doc.get("entries")
    if not isinstance(entries, list) or not entries:
        out.append(Finding("BOOTCHAIN-SCHEMA", JSON17, "entries array required"))
        return out, []
    kept = []
    for index, entry in enumerate(entries):
        site = f"entries[{index}]"
        if not isinstance(entry, dict):
            out.append(Finding("BOOTCHAIN-SCHEMA", site, "object required"))
            continue
        kept.append(entry)
        absent = [key for key in ENTRY_KEYS if key not in entry]
        if absent:
            out.append(Finding("BOOTCHAIN-SCHEMA", site,
                               "missing keys=" + ",".join(absent)))
        present = sorted(key for key in entry if key not in ENTRY_KEYS)
        if present:
            out.append(Finding("BOOTCHAIN-SCHEMA", site,
                               "extra keys=" + ",".join(present)))
        for key, spec in ENTRY_SPEC:
            if key in entry and not type_ok(entry[key], spec):
                out.append(Finding("BOOTCHAIN-SCHEMA", f"{site}.{key}",
                                   f"{entry[key]!r} is not {spec}"))
        hooks = entry.get("hook_roots")
        if isinstance(hooks, dict):
            if sorted(hooks) != sorted(HOOKS):
                out.append(Finding("BOOTCHAIN-SCHEMA", f"{site}.hook_roots",
                                   "keys must be exactly " + ",".join(HOOKS)))
            for hook in HOOKS:
                if hook in hooks and not type_ok(hooks[hook], "str?"):
                    out.append(Finding("BOOTCHAIN-SCHEMA",
                                       f"{site}.hook_roots.{hook}",
                                       f"{hooks[hook]!r} is not str?"))
    ids = [entry.get("id") for entry in kept]
    for eid in ids:
        if not isinstance(eid, str) or not eid.strip():
            out.append(Finding("BOOTCHAIN-ENTRY-ID", JSON17,
                               f"blank or non-string id {eid!r}"))
    for eid, count in sorted(Counter(x for x in ids
                                     if isinstance(x, str)).items()):
        if count > 1:
            out.append(Finding("BOOTCHAIN-ENTRY-ID", eid,
                               f"duplicate id x{count}"))
    return out, kept


def boot_findings(doc, lines_by_path):
    boot = doc.get("boot")
    if not isinstance(boot, dict):
        return [Finding("BOOTCHAIN-SCHEMA", "boot", "object required")]
    out = []
    absent = [key for key in BOOT_KEYS if key not in boot]
    if absent:
        out.append(Finding("BOOTCHAIN-SCHEMA", "boot",
                           "missing keys=" + ",".join(absent)))
    issues, cited = parse_evidence(boot.get("evidence"), lines_by_path, "boot")
    out += issues
    for field in ("running_kernel", "boot_start", "cmdline_rootflags",
                  "loader_entry_selected"):
        value = boot.get(field)
        if not isinstance(value, str) or not any(value in line for _, line in cited):
            out.append(Finding("BOOTCHAIN-BOOT-EVIDENCE", "boot",
                               f"{field} {value!r} appears in no cited line"))
    return out


def section(lines, heading):
    start = None
    for index, line in enumerate(lines):
        if line.rstrip() == heading:
            start = index
            break
    if start is None:
        return None
    for end in range(start + 1, len(lines)):
        if lines[end].startswith("## "):
            return lines[start + 1:end]
    return lines[start + 1:]


def md_findings(text, entries):
    out = []
    lines = text.splitlines()
    for token in MD_HEADER:
        if not any(line.startswith(token) and len(line.strip()) > len(token)
                   for line in lines):
            out.append(Finding("BOOTCHAIN-MD-HEADER", MD17,
                               f"provenance header `{token}` absent or empty"))
    for heading in MD_HEADINGS:
        if not any(line.rstrip() == heading for line in lines):
            out.append(Finding("BOOTCHAIN-MD-HEADING", MD17,
                               f"heading `{heading}` absent"))
    table = section(lines, "## Decision table")
    table_text = "\n".join(table) if table is not None else None
    for entry in entries:
        eid = entry.get("id")
        if table_text is None:
            break
        if isinstance(eid, str) and f"`{eid}`" not in table_text:
            out.append(Finding("BOOTCHAIN-MD-ENTRY", eid,
                               "id absent from ## Decision table"))
    return out


def evaluate(docs):
    findings = []
    for path, text in ((JSON17, docs.json17), (MD17, docs.md17)):
        if text is None:
            findings.append(Finding("BOOTCHAIN-MISSING", path,
                                    "file absent at this revision"))
    lines_by_path = {}
    for name, path in CAPTURES.items():
        text = docs.captures.get(name)
        if text is None:
            findings.append(Finding("BOOTCHAIN-MISSING", path,
                                    "file absent at this revision"))
        else:
            lines_by_path[path] = text.splitlines()
    if findings:
        return Result(FAIL, findings, 0, 0)
    try:
        doc = json.loads(docs.json17)
    except json.JSONDecodeError as exc:
        return Result(CANNOT, [Finding("E-JSON-PARSE", JSON17,
                                       str(exc)[:100])], 0, 0)
    issues, entries = doc_findings(doc)
    findings += issues
    findings += boot_findings(doc, lines_by_path)
    ctx = context(doc, lines_by_path)
    verdicted = 0
    for entry in entries:
        issues, derived = entry_findings(entry, lines_by_path, ctx)
        findings += issues
        if derived != NOT_KERNEL and entry.get("verdict") == derived:
            verdicted += 1
    findings += md_findings(docs.md17, entries)
    findings = [Finding(*key) for key in
                sorted({(f.id, f.site, f.detail) for f in findings})]
    return Result(FAIL if findings else PASS, findings, verdicted, len(entries))


def emit(result, revision, branch="master", branch_tip=None):
    status = {PASS: "PASS", FAIL: "FAIL", CANNOT: "CANNOT_EVALUATE"}[result.code]
    payload = {"status": status,
               "revision": revision,
               "branch": branch,
               "branch_tip": branch_tip,
               "verdicted_kernel_entries": result.verdicted,
               "entry_count": result.entries,
               "scope": "next-boot verdict conformance for the limine entry "
                        "corpus only; no boot, package, service or initramfs action",
               "findings": [{"id": f.id, "site": f.site, "detail": f.detail}
                            for f in result.findings]}
    print(json.dumps(payload, sort_keys=True))
    return result.code


def git(*args, repo=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat", "LC_ALL": "C"})
    try:
        return subprocess.run(["git", "--no-pager", "-C", str(repo or ROOT), *args],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=env, timeout=30)
    except subprocess.TimeoutExpired:
        raise Cannot("E-GIT-TIMEOUT", "git", "git command exceeded 30s")
    except OSError as exc:
        raise Cannot("E-GIT-FAILED", "git", str(exc)[:120])


def read_git(commit, path):
    proc = git("show", f"{commit}:{path}")
    if proc.returncode == 0:
        try:
            return proc.stdout.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise Cannot("E-READ-FAILED", path, str(exc)[:120])
    error = proc.stderr.decode("utf-8", "replace")
    if re.search(r"does not exist|exists on disk, but not in|not in '", error, re.I):
        return None
    raise Cannot("E-GIT-READ-FAILED", path, error.strip()[:120])


def resolve(rev, repo=None):
    proc = git("rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}", repo=repo)
    if proc.returncode != 0:
        raise Cannot("E-REVISION-INVALID", "revision",
                     "7-64 hex commit required; HEAD/@/@-/refs are not revisions")
    return proc.stdout.decode("ascii", "replace").strip()


def ref_sha(ref, repo=None):
    proc = git("rev-parse", "--verify", "--quiet", ref, repo=repo)
    return proc.stdout.decode("ascii", "replace").strip() if proc.returncode == 0 else None


def is_ancestor(sha, ref, repo=None):
    proc = git("merge-base", "--is-ancestor", sha, ref, repo=repo)
    if proc.returncode == 0:
        return True
    if proc.returncode == 1:
        return False
    raise Cannot("E-GIT-FAILED", ref,
                 proc.stderr.decode("utf-8", "replace").strip()[:120])


def bind_revision(sha, branch, repo=None):
    """Require sha on refs/heads/<branch> and, when it exists, on origin's."""
    local = f"refs/heads/{branch}"
    tip = ref_sha(local, repo)
    if tip is None:
        raise Cannot("E-REVISION-NOT-LANDED", sha,
                     f"{local} absent, so the revision is not a landed branch commit")
    if not is_ancestor(sha, local, repo):
        raise Cannot("E-REVISION-NOT-LANDED", sha,
                     f"{sha[:12]} is not an ancestor of {local}")
    remote = f"refs/remotes/origin/{branch}"
    if ref_sha(remote, repo) is not None and not is_ancestor(sha, remote, repo):
        raise Cannot("E-REVISION-NOT-PUSHED", sha,
                     f"{sha[:12]} is not an ancestor of {remote}")
    return tip


def revision_finding(rev):
    return None if isinstance(rev, str) and REV.fullmatch(rev) else "E-REVISION-INVALID"


def branch_finding(branch):
    return None if isinstance(branch, str) and BRANCH.fullmatch(branch) else "E-BRANCH-INVALID"


def build_parser():
    parser = argparse.ArgumentParser(
        description="Read-only round-17 next-boot verdict gate for the limine "
                    "entry corpus.",
        exit_on_error=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--revision", metavar="REV",
                       help="7-64 hex commit only; HEAD/@/@-/ref names are rejected "
                            "(under jj, HEAD is @-) and the commit must be an "
                            "ancestor of refs/heads/<BRANCH>")
    group.add_argument("--selftest", action="store_true",
                       help="in-memory fixture suite plus a mktemp git binding sandbox")
    parser.add_argument("--branch", default="master", metavar="BRANCH",
                        help="refs/heads/<BRANCH> and refs/remotes/origin/<BRANCH> "
                             "(when present) must contain the revision; default master")
    return parser


def cli_finding(argv):
    try:
        build_parser().parse_args(argv)
        return None
    except (argparse.ArgumentError, SystemExit):
        return "E-CLI"


# --- hermetic fixtures -----------------------------------------------------
S1, S2, S3 = "a" * 64, "b" * 64, "c" * 64
B1, B2 = "1" * 128, "2" * 128


def boot_lines():
    return [
        "# fixture capture",
        "$ uname -r",
        "7.2.11-fixture",
        "$ journalctl --list-boots --no-pager | tail -3",
        " 0 abcdef Tue 2026-10-20 09:57:09 -03 Tue 2026-10-20 12:00:00 -03",
        "$ cat /proc/cmdline",
        "resume=/dev/mapper/root root=/dev/mapper/root rootflags=subvol=@ rw",
        "$ find boot-chain inputs -newermt \"2026-10-20 09:57:09\"",
        "(rc=0 ; empty = none newer)",
        "$ sudo grep -nE limine",
        "3:default_entry: 2",
        "25:  //fix",
        f"30:  path: boot():/EFI/Linux/fix.efi#{B1}",
        "31:  cmdline: resume=/dev/mapper/root rootflags=subvol=@ rw",
        "44:     ///2026-10-20 09:29:19",
        "46:     ////fixsnap",
        f"50:     path: boot():/history/fixsnap.efi_sha256_{S2}#{B2}",
        "51:     cmdline: resume=/dev/mapper/root rootflags=subvol=/@/.snapshots/2/snapshot rw",
        "$ sudo btrfs property get -t subvol /.snapshots/{1,2}/snapshot ro",
        "#2 ro=true",
        "### /boot/EFI/Linux/fix.efi",
        f"sha256 {S1}",
        "uname  7.2.11-fixture",
        "VERSION 42.2",
        "init /sysroot refs 7 ; /new_root refs 0",
        "hooks/btrfs-overlayfs:4:\troot_mnt=\"/new_root\"",
        "hooks/plymouth:11:  plymouth update-root-fs --new-root-dir=/new_root",
        "dirs: new_root sysroot ",
        f"### /boot/history/fixsnap.efi_sha256_{S2}",
        f"sha256 {S2}",
        "uname  7.2.11-fixture",
        "VERSION 42.2",
        "init /sysroot refs 7 ; /new_root refs 0",
        "hooks/btrfs-overlayfs:4:\troot_mnt=\"/new_root\"",
        "hooks/plymouth:11:  plymouth update-root-fs --new-root-dir=/new_root",
        "dirs: new_root sysroot ",
        "71:/EFI fallback",
        "72:path: boot():/EFI/BOOT/BOOTX64.EFI",
    ]


def supplement_lines():
    return [
        "# fixture supplement",
        "$ for v in /sys/firmware/efi/efivars/Loader*; do echo; done",
        "LoaderEntrySelected-4a67b082-0a4c-41cf-b6c7: Omarchy.linux",
        "LoaderInfo-4a67b082-0a4c-41cf-b6c7: Limine 12.9.3",
        "LimineLastBootedEntry-513ee0d0-6e43-cb05: Omarchy/linux",
        "$ sudo -n sha256sum /boot/EFI/BOOT/BOOTX64.EFI /boot/EFI/limine/limine_x64.efi",
        f"{S3}  /boot/EFI/BOOT/BOOTX64.EFI",
        f"{S3}  /boot/EFI/limine/limine_x64.efi",
    ]


def emulation_lines():
    return [
        "# fixture emulation",
        "lrwxrwxrwx  1 vgpnk vgpnk     7 Oct 20 12:33 new_root -> sysroot",
        "step3 overlay mount rc=0",
        "new_root -> sysroot",
    ]


def fresh_lines():
    return ["# fixture fresh"]


def ref(name, number):
    return f"{CAPTURES[name]}:{number}"


def line_no(rows, text):
    return rows.index(text) + 1


def fixture_json():
    rows, supp = boot_lines(), supplement_lines()
    fix_start = line_no(rows, "### /boot/EFI/Linux/fix.efi")
    snap_start = line_no(rows, f"### /boot/history/fixsnap.efi_sha256_{S2}")
    fix_evidence = sorted({line_no(rows, "7.2.11-fixture"),
                           line_no(rows, "resume=/dev/mapper/root root=/dev/mapper/"
                                         "root rootflags=subvol=@ rw"),
                           line_no(rows, "(rc=0 ; empty = none newer)"),
                           line_no(rows, f"30:  path: boot():/EFI/Linux/fix.efi#{B1}")}
                          | set(range(fix_start, fix_start + 8)))
    snap_evidence = sorted({line_no(rows, "#2 ro=true"),
                            line_no(rows, f"50:     path: boot():/history/fixsnap."
                                          f"efi_sha256_{S2}#{B2}"),
                            line_no(rows, "51:     cmdline: resume=/dev/mapper/root "
                                          "rootflags=subvol=/@/.snapshots/2/snapshot rw")}
                           | set(range(snap_start, snap_start + 8)))
    fix_evidence = ([ref("boot", n) for n in fix_evidence] + [ref("supplement", 3)]
                    + [ref("emulation", 2)])
    snap_evidence = [ref("boot", n) for n in snap_evidence] + [ref("emulation", 2)]
    prose = ("efi_path is not a kernel UKI (mkinitcpio_version is null)",
             "selected_this_boot is true, the image sha256 equals the file that "
             "booted, and no /etc or /usr boot-chain input is newer than boot start",
             "snapshot is null and selected_this_boot is false",
             "init_sysroot_refs>0 and init_new_root_refs==0 and "
             "image_new_root=='symlink->sysroot' and both hook_roots=='/new_root'",
             "init_new_root_refs>0 and init_sysroot_refs==0 and "
             "image_new_root=='directory' and both hook_roots=='/new_root'",
             "otherwise")
    rules = [{"order": order, "if": text, "verdict": verdict}
             for (order, verdict), text in zip(RULE_TABLE, prose)]
    entries = [
        {"id": "fix", "limine_label": "//fix", "efi_path": "/boot/EFI/Linux/fix.efi",
         "sha256": S1, "b2sum_prefix": B1[:20], "uname": "7.2.11-fixture",
         "mkinitcpio_version": "42.2", "init_sysroot_refs": 7,
         "init_new_root_refs": 0, "image_new_root": "symlink->sysroot",
         "hook_roots": {"btrfs-overlayfs": "/new_root", "plymouth": "/new_root"},
         "rootflags": "subvol=@", "snapshot": None, "snapshot_ro": None,
         "selected_this_boot": True, "verdict": "BOOTED-OBSERVED",
         "evidence": fix_evidence, "note": "fixture"},
        {"id": "snap",
         "limine_label": "///2026-10-20 09:29:19 ////fixsnap",
         "efi_path": f"/boot/history/fixsnap.efi_sha256_{S2}", "sha256": S2,
         "b2sum_prefix": B2[:20], "uname": "7.2.11-fixture",
         "mkinitcpio_version": "42.2", "init_sysroot_refs": 7,
         "init_new_root_refs": 0, "image_new_root": "symlink->sysroot",
         "hook_roots": {"btrfs-overlayfs": "/new_root", "plymouth": "/new_root"},
         "rootflags": "subvol=/@/.snapshots/2/snapshot", "snapshot": 2,
         "snapshot_ro": True, "selected_this_boot": False,
         "verdict": "PATH-ALIASED-EMULATED", "evidence": snap_evidence,
         "note": "fixture"},
        {"id": "firmware", "limine_label": "/EFI fallback",
         "efi_path": "/boot/EFI/BOOT/BOOTX64.EFI", "sha256": S3,
         "b2sum_prefix": None, "uname": None, "mkinitcpio_version": None,
         "init_sysroot_refs": None, "init_new_root_refs": None,
         "image_new_root": None,
         "hook_roots": {"btrfs-overlayfs": None, "plymouth": None},
         "rootflags": None, "snapshot": None, "snapshot_ro": None,
         "selected_this_boot": False, "verdict": NOT_KERNEL,
         "evidence": [ref("supplement", line_no(supp, f"{S3}  /boot/EFI/BOOT/"
                                                      "BOOTX64.EFI")),
                      ref("boot", line_no(rows, "71:/EFI fallback")),
                      ref("boot", line_no(rows,
                                          "72:path: boot():/EFI/BOOT/BOOTX64.EFI"))],
         "note": "fixture"},
    ]
    return {"schema": SCHEMA,
            "captured_at": "2026-10-20T12:35:07-03:00",
            "captures": dict(CAPTURES),
            "boot": {"running_kernel": "7.2.11-fixture",
                     "boot_start": "2026-10-20 09:57:09 -03",
                     "cmdline_rootflags": "subvol=@",
                     "loader_entry_selected": "Omarchy.linux",
                     "evidence": [ref("boot", line_no(rows, "7.2.11-fixture")),
                                  ref("boot", line_no(rows, " 0 abcdef Tue 2026-10-20 "
                                                            "09:57:09 -03 Tue 2026-10-20 "
                                                            "12:00:00 -03")),
                                  ref("boot", line_no(rows, "resume=/dev/mapper/root "
                                                            "root=/dev/mapper/root "
                                                            "rootflags=subvol=@ rw")),
                                  ref("supplement", line_no(supp, "LoaderEntrySelected"
                                                                  "-4a67b082-0a4c-41cf-b6c7: "
                                                                  "Omarchy.linux"))]},
            "verdict_rules": rules, "entries": entries,
            "superseded": "fixture superseded line",
            "authority": "Read-only observation; authorizes no package, service, "
                         "initramfs or bootloader action."}


MD_CLEAN = (
    "source: S051 fixture capture 2026-10-20T12:35 -03\n"
    "verified-at: 2026-10-20 (fixture)\n"
    "recheck: on-release; re-run after any mkinitcpio or kernel change\n\n"
    "# Fixture boot chain\n\n"
    "## What ran\n\nNothing; fixture.\n\n"
    "## Decision table\n\n"
    "| entry | image sha256 | VERSION | init root | hook roots | root | verdict | "
    "evidence lines |\n"
    "|---|---|---|---|---|---|---|---|\n"
    "| `fix` | `aaaaaaaa…` | 42.2 | /sysroot | /new_root, /new_root | `subvol=@` | "
    "**BOOTED-OBSERVED** | boot:2–19 |\n"
    "| `snap` | `bbbbbbbb…` | 42.2 | /sysroot | /new_root, /new_root | "
    "`/@/.snapshots/2/snapshot`, ro=true | **PATH-ALIASED-EMULATED** | boot:28–35 |\n"
    "| `firmware` | — | — | — | — | — | NOT-A-KERNEL-ENTRY | boot:37–38 |\n\n"
    "## Falsifier\n\nFixture falsifier.\n\n"
    "## QUALITY check\n\nFixture quality.\n\n"
    "## Sources\n\n- **S051** — fixture capture.\n")


def fixture(**over):
    captures = {"boot": "\n".join(boot_lines()),
                "supplement": "\n".join(supplement_lines()),
                "emulation": "\n".join(emulation_lines()),
                "fresh": "\n".join(fresh_lines())}
    docs = {"json17": json.dumps(fixture_json()), "md17": MD_CLEAN,
            "captures": captures}
    docs.update(over)
    return DocSet(**docs)


def mutate_json(key, value):
    doc = json.loads(json.dumps(fixture_json()))
    doc[key] = value
    return json.dumps(doc)


def mutate_entries(fn):
    doc = json.loads(json.dumps(fixture_json()))
    fn(doc["entries"])
    return json.dumps(doc)


def _swap_rules():
    doc = json.loads(json.dumps(fixture_json()))
    doc["verdict_rules"][2], doc["verdict_rules"][3] = (
        doc["verdict_rules"][3], doc["verdict_rules"][2])
    return doc


def _rewrite_rule():
    doc = json.loads(json.dumps(fixture_json()))
    doc["verdict_rules"][1]["verdict"] = "UNTESTED"
    return doc


def selftest():
    fix_sha_line = line_no(boot_lines(), f"sha256 {S1}")
    cases = [
        ("clean", fixture(), PASS, set(), 2),
        ("json-missing", fixture(json17=None), FAIL, {"BOOTCHAIN-MISSING"}, 0),
        ("md-missing", fixture(md17=None), FAIL, {"BOOTCHAIN-MISSING"}, 0),
        ("capture-missing", fixture(captures={"boot": None,
                                              "supplement": "\n",
                                              "emulation": "\n",
                                              "fresh": "\n"}),
         FAIL, {"BOOTCHAIN-MISSING"}, 0),
        ("json-malformed", fixture(json17="{"), CANNOT, {"E-JSON-PARSE"}, 0),
        ("schema-wrong", fixture(json17=mutate_json("schema", "tsukuroi-x-v1")),
         FAIL, {"BOOTCHAIN-SCHEMA"}, 2),
        ("captures-map-wrong",
         fixture(json17=mutate_json("captures", {"boot": CAPTURES["boot"]})),
         FAIL, {"BOOTCHAIN-CAPTURE-PATH"}, 2),
        ("authority-removed",
         fixture(json17=mutate_json("authority", "Read-only observation.")),
         FAIL, {"BOOTCHAIN-SCHEMA"}, 2),
        ("superseded-removed",
         fixture(json17=mutate_json("superseded", "")),
         FAIL, {"BOOTCHAIN-SCHEMA"}, 2),
        ("rules-order-swapped", fixture(json17=json.dumps(_swap_rules())),
         FAIL, {"BOOTCHAIN-RULES"}, 2),
        ("rules-verdict-rewritten", fixture(json17=json.dumps(_rewrite_rule())),
         FAIL, {"BOOTCHAIN-RULES"}, 2),
        ("duplicate-id", fixture(json17=mutate_entries(
            lambda es: es[1].update(id="fix"))),
         FAIL, {"BOOTCHAIN-ENTRY-ID"}, 2),
        ("entry-key-missing", fixture(json17=mutate_entries(
            lambda es: es[0].pop("note"))),
         FAIL, {"BOOTCHAIN-SCHEMA"}, 2),
        ("entry-sha-type", fixture(json17=mutate_entries(
            lambda es: es[0].update(sha256=1))),
         FAIL, {"BOOTCHAIN-SCHEMA", "BOOTCHAIN-BLOCK", "BOOTCHAIN-VERDICT"}, 1),
        ("verdict-wrong", fixture(json17=mutate_entries(
            lambda es: es[0].update(verdict="UNTESTED"))),
         FAIL, {"BOOTCHAIN-VERDICT"}, 1),
        ("restored-defect-snapshot-booted", fixture(json17=mutate_entries(
            lambda es: es[1].update(verdict="BOOTED-OBSERVED"))),
         FAIL, {"BOOTCHAIN-VERDICT"}, 1),
        ("restored-defect-nonuki", fixture(json17=mutate_entries(
            lambda es: es[2].update(verdict="UNTESTED"))),
         FAIL, {"BOOTCHAIN-VERDICT"}, 2),
        ("derivation-selected-false", fixture(json17=mutate_entries(
            lambda es: es[0].update(selected_this_boot=False))),
         FAIL, {"BOOTCHAIN-VERDICT"}, 1),
        ("derivation-image-dir", fixture(json17=mutate_entries(
            lambda es: es[1].update(image_new_root="directory"))),
         FAIL, {"BOOTCHAIN-UNTYPED", "BOOTCHAIN-VERDICT"}, 1),
        ("restored-defect-type-blind", fixture(json17=mutate_entries(
            lambda es: es[1].update(image_new_root="directory", verdict="UNTESTED",
                                    evidence=[r for r in es[1]["evidence"]
                                              if not r.startswith(CAPTURES["emulation"])]
                                    + [ref("boot", line_no(boot_lines(),
                                                           "dirs: new_root sysroot "))]))),
         FAIL, {"BOOTCHAIN-UNTYPED"}, 2),
        ("restored-defect-degraded", fixture(json17=mutate_entries(
            lambda es: es[1].update(verdict="DEGRADED-PREDICTED"))),
         FAIL, {"BOOTCHAIN-VERDICT"}, 1),
        ("untyped-symlink-claim", fixture(json17=mutate_entries(
            lambda es: es[1].update(evidence=[r for r in es[1]["evidence"]
                                              if not r.startswith(CAPTURES["emulation"])]))),
         FAIL, {"BOOTCHAIN-UNTYPED"}, 2),
        ("image-kind-enum", fixture(json17=mutate_entries(
            lambda es: es[1].update(image_new_root="dir"))),
         FAIL, {"BOOTCHAIN-FIELD", "BOOTCHAIN-VERDICT"}, 1),
        ("nonkernel-kind-set", fixture(json17=mutate_entries(
            lambda es: es[2].update(image_new_root="directory"))),
         FAIL, {"BOOTCHAIN-FIELD"}, 2),
        ("pre42-guard", fixture(json17=mutate_entries(
            lambda es: es[1].update(init_sysroot_refs=0, init_new_root_refs=7,
                                    verdict="CONSISTENT-PRE42"))),
         FAIL, {"BOOTCHAIN-BLOCK", "BOOTCHAIN-INIT-REFS", "BOOTCHAIN-VERDICT"}, 1),
        ("evidence-line-zero", fixture(json17=mutate_entries(
            lambda es: es[0]["evidence"].append(ref("boot", 0)))),
         FAIL, {"BOOTCHAIN-EVIDENCE-LINE"}, 2),
        ("derivation-no-newer-witness", fixture(json17=mutate_entries(
            lambda es: es[0]["evidence"].remove(
                ref("boot", line_no(boot_lines(),
                                    "(rc=0 ; empty = none newer)"))))),
         FAIL, {"BOOTCHAIN-VERDICT"}, 1),
        ("sha256-not-cited", fixture(json17=mutate_entries(
            lambda es: es[0]["evidence"].remove(ref("boot", fix_sha_line)))),
         FAIL, {"BOOTCHAIN-SHA256"}, 2),
        ("sha256-mismatch", fixture(json17=mutate_entries(
            lambda es: es[0].update(sha256="d" * 64))),
         FAIL, {"BOOTCHAIN-SHA256", "BOOTCHAIN-BLOCK", "BOOTCHAIN-VERDICT"}, 1),
        ("uname-mismatch", fixture(json17=mutate_entries(
            lambda es: es[0].update(uname="9.9-fixture"))),
         FAIL, {"BOOTCHAIN-UNAME", "BOOTCHAIN-BLOCK", "BOOTCHAIN-VERDICT"}, 1),
        ("rootflags-mismatch", fixture(json17=mutate_entries(
            lambda es: es[0].update(rootflags="subvol=@other"))),
         FAIL, {"BOOTCHAIN-ROOTFLAGS", "BOOTCHAIN-VERDICT"}, 1),
        ("b2sum-prefix-wrong", fixture(json17=mutate_entries(
            lambda es: es[0].update(b2sum_prefix="f" * 20))),
         FAIL, {"BOOTCHAIN-B2SUM"}, 2),
        ("version-mismatch", fixture(json17=mutate_entries(
            lambda es: es[0].update(mkinitcpio_version="41.1"))),
         FAIL, {"BOOTCHAIN-VERSION", "BOOTCHAIN-BLOCK"}, 2),
        ("init-refs-mismatch", fixture(json17=mutate_entries(
            lambda es: es[0].update(init_sysroot_refs=0, init_new_root_refs=7))),
         FAIL, {"BOOTCHAIN-INIT-REFS", "BOOTCHAIN-BLOCK"}, 2),
        ("hook-root-mismatch", fixture(json17=mutate_entries(
            lambda es: es[0]["hook_roots"].update(plymouth="/sysroot"))),
         FAIL, {"BOOTCHAIN-HOOK-ROOT", "BOOTCHAIN-BLOCK"}, 2),
        ("evidence-line-outside", fixture(json17=mutate_entries(
            lambda es: es[0]["evidence"].append(ref("boot", 999)))),
         FAIL, {"BOOTCHAIN-EVIDENCE-LINE"}, 2),
        ("evidence-path-unknown", fixture(json17=mutate_entries(
            lambda es: es[0]["evidence"].append("elsewhere.txt:1"))),
         FAIL, {"BOOTCHAIN-EVIDENCE-PATH"}, 2),
        ("evidence-malformed", fixture(json17=mutate_entries(
            lambda es: es[0]["evidence"].append("nocolon"))),
         FAIL, {"BOOTCHAIN-EVIDENCE-LINE"}, 2),
        ("block-path-renamed", fixture(captures={
            "boot": "\n".join(boot_lines()).replace(
                "### /boot/EFI/Linux/fix.efi", "### /boot/EFI/Linux/other.efi"),
            "supplement": "\n".join(supplement_lines()),
            "emulation": "\n".join(emulation_lines()),
            "fresh": "\n".join(fresh_lines())}),
         FAIL, {"BOOTCHAIN-BLOCK", "BOOTCHAIN-VERDICT"}, 1),
        ("boot-start-uncited", fixture(json17=mutate_json(
            "boot", {"running_kernel": "7.2.11-fixture",
                     "boot_start": "2026-10-20 09:00:00 -03",
                     "cmdline_rootflags": "subvol=@",
                     "loader_entry_selected": "Omarchy.linux",
                     "evidence": [ref("boot", 2), ref("boot", 4),
                                  ref("boot", 6), ref("supplement", 3)]})),
         FAIL, {"BOOTCHAIN-BOOT-EVIDENCE"}, 2),
        ("loader-not-cited", fixture(json17=mutate_json(
            "boot", {"running_kernel": "7.2.11-fixture",
                     "boot_start": "2026-10-20 09:57:09 -03",
                     "cmdline_rootflags": "subvol=@",
                     "loader_entry_selected": "Other.entry",
                     "evidence": [ref("boot", 2), ref("boot", 4),
                                  ref("boot", 6), ref("supplement", 3)]})),
         FAIL, {"BOOTCHAIN-BOOT-EVIDENCE"}, 2),
        ("md-header-missing", fixture(md17=MD_CLEAN.replace(
            "recheck: on-release; re-run after any mkinitcpio or kernel change\n",
            "")),
         FAIL, {"BOOTCHAIN-MD-HEADER"}, 2),
        ("md-heading-missing", fixture(md17=MD_CLEAN.replace(
            "## Falsifier\n", "## Renamed\n")),
         FAIL, {"BOOTCHAIN-MD-HEADING"}, 2),
        ("md-entry-missing", fixture(md17="\n".join(
            line for line in MD_CLEAN.splitlines() if "`snap`" not in line)),
         FAIL, {"BOOTCHAIN-MD-ENTRY"}, 2),
    ]
    passed, failures = 0, []
    for name, docs, code, want, count in cases:
        try:
            result = evaluate(docs)
        except Exception as exc:  # a fixture must never crash the gate
            failures.append(f"{name}: raised {type(exc).__name__}: {exc}")
            continue
        got = {f.id for f in result.findings}
        problems = []
        if result.code != code:
            problems.append(f"exit={result.code}/{code}")
        if got != want:
            problems.append("ids=" + ",".join(sorted(got))
                            + " want=" + ",".join(sorted(want)))
        if result.verdicted != count:
            problems.append(f"verdicted={result.verdicted}/{count}")
        if problems:
            failures.append(f"{name}: " + "; ".join(problems))
        else:
            passed += 1
    for name, got, want in (
            ("revision-head", revision_finding("HEAD"), "E-REVISION-INVALID"),
            ("revision-at", revision_finding("@"), "E-REVISION-INVALID"),
            ("revision-at-parent", revision_finding("@-"), "E-REVISION-INVALID"),
            ("revision-ref", revision_finding("refs/heads/master"),
             "E-REVISION-INVALID"),
            ("revision-short", revision_finding("abc"), "E-REVISION-INVALID"),
            ("revision-hex", revision_finding("6923fe0"), None),
            ("branch-bad", branch_finding("--exec"), "E-BRANCH-INVALID"),
            ("branch-ok", branch_finding("master"), None),
            ("cli-unknown", cli_finding(["--bogus"]), "E-CLI"),
            ("cli-both-modes", cli_finding(["--selftest", "--revision", "6923fe0"]),
             "E-CLI"),
            ("cli-no-mode", cli_finding([]), "E-CLI")):
        if got == want:
            passed += 1
        else:
            failures.append(f"{name}: id={got}/{want}")
    # main() must route --revision through bind_revision (mutation FxGateMutants :1115)
    global resolve, bind_revision
    saved = (resolve, bind_revision)
    def _stub_resolve(rev, repo=None):
        return "f" * 40
    def _stub_bind(sha, branch, repo=None):
        raise Cannot("E-REVISION-NOT-LANDED", sha, "selftest stub")
    resolve, bind_revision = _stub_resolve, _stub_bind
    try:
        import contextlib, io
        with contextlib.redirect_stdout(io.StringIO()) as buf:
            code = main(["--revision", "f" * 40])
        out = json.loads(buf.getvalue() or "{}")
        ids = {f.get("id") for f in out.get("findings", [])}
    except Exception as exc:  # pragma: no cover - reported as failure
        code, ids = None, {repr(exc)}
    finally:
        resolve, bind_revision = saved
    if code == CANNOT and ids == {"E-REVISION-NOT-LANDED"}:
        passed += 1
    else:
        failures.append(f"cli-binds-revision: exit={code} ids={sorted(map(str, ids))}")
    total = len(cases) + 12
    bound, bind_failures = binding_cases()
    passed += bound
    total += 5
    failures += bind_failures
    if failures:
        print(f"CHECK_BOOT_CHAIN_SELFTEST: FAIL ({total} cases, {passed} passed)")
        print("\n".join("  " + item for item in failures))
        return FAIL
    print(f"CHECK_BOOT_CHAIN_SELFTEST: PASS ({total} cases, {passed} passed, 0 failed)")
    return PASS


def _git_commit(repo, message):
    proc = git("-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid",
               "commit", "-q", "-m", message, repo=repo)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace")[:200])
    return ref_sha("HEAD", repo)


def _expect_cannot(fn, want):
    try:
        fn()
    except Cannot as exc:
        return None if exc.fid == want else exc.fid
    return "no-Cannot"


def binding_cases():
    """Real binding vectors in a throwaway mktemp git sandbox."""
    passed, failures = 0, []
    tmp = Path(tempfile.mkdtemp(prefix="boot-chain-gate-"))

    def check(name, got, want):
        nonlocal passed
        if got == want:
            passed += 1
        else:
            failures.append(f"{name}: {got}/{want}")

    try:
        git("init", "-q", repo=tmp)
        git("symbolic-ref", "HEAD", "refs/heads/master", repo=tmp)
        (tmp / "a.txt").write_text("a\n")
        git("add", "-A", repo=tmp)
        first = _git_commit(tmp, "first")
        check("bind-landed", bind_revision(first, "master", repo=tmp), first)
        git("update-ref", "refs/remotes/origin/master", first, repo=tmp)
        (tmp / "b.txt").write_text("b\n")
        git("add", "-A", repo=tmp)
        second = _git_commit(tmp, "second")
        check("bind-not-pushed", _expect_cannot(
            lambda: bind_revision(second, "master", repo=tmp),
            "E-REVISION-NOT-PUSHED"), None)
        check("bind-pushed-ancestor",
              bind_revision(first, "master", repo=tmp), second)
        git("checkout", "-q", "--detach", first, repo=tmp)
        (tmp / "c.txt").write_text("c\n")
        git("add", "-A", repo=tmp)
        third = _git_commit(tmp, "third")
        check("bind-not-landed", _expect_cannot(
            lambda: bind_revision(third, "master", repo=tmp),
            "E-REVISION-NOT-LANDED"), None)
        git("update-ref", "-d", "refs/remotes/origin/master", repo=tmp)
        check("bind-no-origin", bind_revision(second, "master", repo=tmp), second)
    except Exception as exc:  # a sandbox must never crash the gate
        failures.append(f"binding-sandbox: {type(exc).__name__}: {exc}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return passed, failures


def main(argv=None):
    branch = "master"
    try:
        args = build_parser().parse_args(argv)
    except (argparse.ArgumentError, SystemExit) as exc:
        if isinstance(exc, SystemExit) and not exc.code:
            return 0
        return emit(Result(CANNOT, [Finding("E-CLI", "cli",
                                            "--revision REV or --selftest required")],
                           0, 0), "unbound", branch, None)
    if args.selftest:
        return selftest()
    revision, branch_tip = "unbound", None
    try:
        finding = branch_finding(args.branch)
        if finding:
            raise Cannot(finding, "branch",
                         "branch must match [A-Za-z0-9._/-], no leading dash, "
                         "'..' or '//'")
        branch = args.branch
        finding = revision_finding(args.revision)
        if finding:
            raise Cannot(finding, "revision",
                         "7-64 hex commit required; HEAD/@/@-/refs are rejected")
        revision = resolve(args.revision)
        branch_tip = bind_revision(revision, branch)
        docs = DocSet(read_git(revision, JSON17), read_git(revision, MD17),
                      {name: read_git(revision, path)
                       for name, path in CAPTURES.items()})
    except Cannot as exc:
        return emit(Result(CANNOT, [Finding(exc.fid, exc.site, exc.detail)], 0, 0),
                    revision, branch, branch_tip)
    except Exception as exc:  # no traceback: unreadable input is CANNOT
        return emit(Result(CANNOT, [Finding("E-INTERNAL", "gate", str(exc)[:120])],
                           0, 0), revision, branch, branch_tip)
    try:
        result = evaluate(docs)
    except Exception as exc:
        return emit(Result(CANNOT, [Finding("E-INTERNAL", "gate", str(exc)[:120])],
                           0, 0), revision, branch, branch_tip)
    return emit(result, revision, branch, branch_tip)


if __name__ == "__main__":
    sys.exit(main())
