#!/usr/bin/env python3
"""Narrow, read-only round-15 locator/positive-domain clarification gate.

Bounded named-defect conformance, never source truth: two corrections, S046 and
the positive ProtectSystem= definition, a stable SANDBOXING > ProtectSystem=
location, no renderer-dependent line number in locator-bearing fields, exact
preservation of the r14 original bytes/values, and both r14 supersession
notices. On baseline the actual bare "rendered lines 1266-1267" locator and the
unswept "documents no further values" absence are named defects, not merely a
missing new file. Exit 0 clean, 1 failed, 2 cannot evaluate. No writes, no
network; --selftest uses in-memory fixtures plus a throwaway mktemp git repo.

Revision-bound mode delegates branch, revision, landing, and push validation to
`tools/_revision.py`; worktree mode reads no git.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile
sys.dont_write_bytecode = True  # read-only shared-module import
import _revision
from collections import namedtuple
from pathlib import Path

PASS, FAIL, CANNOT = 0, 1, 2
ROOT = Path(__file__).resolve().parents[1]
MD15 = "corpus/knowledge/source-locator-clarification-r15.md"
JSON15 = "corpus/knowledge/source-locator-clarification-r15.json"
MD14 = "corpus/knowledge/source-scope-correction-r14.md"
JSON14 = "corpus/knowledge/source-scope-correction-r14.json"
FILES = (MD15, JSON15, MD14, JSON14)
SCHEMA, LOC_ID, POS_ID = "tsukuroi-locator-clarification-v1", "R15-LOCATOR", "R15-POSITIVE-DOMAIN"
URL = "https://man.archlinux.org/man/systemd.exec.5"
QUOTE = 'Takes a boolean argument or the special values "full" or "strict".'
HEADS = ("## R15-LOCATOR", "## R15-POSITIVE-DOMAIN", "## QUALITY check")
REQUIRED = ("id", "source_id", "url", "location", "quote", "replacement", "supersedes")
# 0db618a r14 originals, as exact bytes (MD prefix, JSON minus the additive key).
MD14_SHA = "9f7cc3cf0ad75824d39cf73a2789d4acfc411386f81b01d1058ea3557ca8dc04"
JSON14_SHA = "1a4cccacac86f6c88f2b470219935de0d1dfc9aeab8f1f7ddedae7a86dfeffb5"
LOC_NUM = re.compile(r"\brendered\s+lines?\s*\d{2,4}(?:\s*[-\u2013\u2014]\s*\d{2,4})?"
                     r"|\blines?\s*\d{2,4}(?:\s*[-\u2013\u2014]\s*\d{2,4})?|\bL\d{2,4}\b"
                     r"|\b\d{3,4}\s*[-\u2013\u2014]\s*\d{3,4}\b|\b\d{3,4}\s+to\s+\d{3,4}\b", re.I)
WITHDRAW = re.compile(r"withdraw|supersed|not (?:an? )?(?:active )?locator|reader-dependent|"
                      r"renderer-dependent|unqualified|no longer (?:a locator|used)", re.I)
ABSENCE = re.compile(r"document(?:s|ed)?\s+no\s+(?:further|other|additional|more)\s+values?"
                     r"|no\s+(?:further|other|additional|more)\s+(?:documented\s+)?values?"
                     r"|value\s+set\s+is\s+(?:closed|exhaustive)"
                     r"|\bonly\s+(?:these\s+|the\s+)?(?:documented\s+)?values\b"
                     r"|\b(?:complete|entire|whole|full)\s+documented\s+(?:value\s+domain|values?)"
                     r"|\b(?:and|are|is)\s+only\s+these\b", re.I)
NEG_PRE = re.compile(r"(?:does not|do not|did not|is not|no)\s+(?:claim|assert|establish|state|evidence)"
                     r"[^.!?]{0,50}$", re.I)
NEG_POST = re.compile(r"^\s*(?:is|was|remains|has been)\s+(?:unsupported|withdrawn|superseded|not claimed)",
                      re.I)
Finding = namedtuple("Finding", "id site detail")
DocSet = namedtuple("DocSet", "md15 json15 md14 json14 digests")
Result = namedtuple("Result", "code findings count")


class Cannot(Exception):
    def __init__(self, fid, site, detail):
        super().__init__(detail)
        self.fid, self.site, self.detail = fid, site, detail


def norm(text):
    return " ".join(str(text).replace("\u201c", '"').replace("\u201d", '"').split())


def plain(text):
    return norm(str(text).replace("`", ""))


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def section(text, heading):
    lines = [line.rstrip() for line in text.splitlines()]
    if heading not in lines:
        return None
    body = []
    for line in text.splitlines()[lines.index(heading) + 1:]:
        if line.startswith("## "):
            break
        body.append(line)
    return "\n".join(body)


def sentence_at(flat, start):
    left = max(flat.rfind(". ", 0, start), flat.rfind("! ", 0, start), flat.rfind("? ", 0, start))
    rights = [x for x in (flat.find(". ", start), flat.find("! ", start), flat.find("? ", start)) if x != -1]
    return flat[left + 2:min(rights) if rights else len(flat)], left + 2


def line_hits(text):
    return [m.group(0) for m in LOC_NUM.finditer(norm(text))]


def locator_sites(text):
    flat, out = norm(text), []
    for match in LOC_NUM.finditer(flat):
        sent, offset = sentence_at(flat, match.start())
        quoted = flat[offset:match.start()].count('"') % 2 == 1
        if quoted and "1266-1267" in match.group(0) and WITHDRAW.search(sent):
            continue
        out.append(sent[:120])
    return out


def absence_sites(text):
    flat, out = norm(text), []
    for match in ABSENCE.finditer(flat):
        sent, offset = sentence_at(flat, match.start())
        rel = match.start() - offset
        quoted = flat[offset:match.start()].count('"') % 2 == 1
        marker = re.search(r"supersed|withdraw|unsupported|unqualified|negative sentence|not claimed",
                           sent, re.I)
        if (quoted and marker) or NEG_PRE.search(sent[:rel]) or NEG_POST.search(sent[rel:]):
            continue
        out.append(sent[:120])
    return out


def leaves(obj, prefix=""):
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield from leaves(value, f"{prefix}.{key}" if prefix else str(key))
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            yield from leaves(value, f"{prefix}[{index}]")
    elif isinstance(obj, str):
        yield prefix, obj


def md15_issues(text):
    out, lines = [], [line.strip() for line in text.splitlines() if line.strip()]
    trio = [line.lower() for line in lines[:3]]
    if not (len(trio) == 3 and trio[0].startswith("source:") and trio[1].startswith("verified-at:")
            and trio[2].startswith("recheck:") and not any(line.startswith("#") for line in lines[:3])):
        out.append(Finding("R15-MD-OPENERS", MD15, "source:/verified-at:/recheck: first"))
    if not all(head in lines for head in HEADS):
        out.append(Finding("R15-MD-HEADING", MD15, "named headings absent"))
    loc = plain(section(text, HEADS[0]) or "").lower()
    if not all(t in loc for t in ("s046", "sandboxing", "protectsystem=", "1266")) or not (
            re.search(r"reader|renderer", loc) and re.search(r"stable|heading", loc)
            and re.search(r"withdraw|supersed|not a locator", loc)):
        out.append(Finding("R15-MD-LOCATOR", MD15, "stable/withdrawn locator pins absent"))
    pos = plain(section(text, HEADS[1]) or "").lower()
    if not all(t in pos for t in ("s046", "boolean", "full", "strict")) or QUOTE.lower() not in pos:
        out.append(Finding("R15-MD-POSITIVE", MD15, "positive-domain pins absent"))
    if len(plain(section(text, HEADS[2]) or "")) < 40:
        out.append(Finding("R15-MD-QUALITY", MD15, "QUALITY check absent or empty"))
    out += [Finding("LOCATOR_UNQUALIFIED", MD15, hit) for hit in locator_sites(text)]
    for line in text.splitlines():
        if re.match(r"\s*(?:\*\*|__)?\s*(?:active locator|location|source object)\s*(?:\*\*|__)?\s*:",
                    line, re.I):
            out += [Finding("LOCATOR_UNQUALIFIED", MD15, line.strip()[:120])
                    for _ in line_hits(line)]
    out += [Finding("NEGATIVE_DOMAIN_UNSWEPT", MD15, hit) for hit in absence_sites(text)]
    return out


def token_issues(kind, obj):
    out, loc = [], plain(obj.get("location", "")).lower()
    rep, sup = plain(obj.get("replacement", "")).lower(), plain(obj.get("supersedes", "")).lower()
    prefix = "LOCATOR" if kind == LOC_ID else "POSITIVE"

    def add(fid, detail):
        out.append(Finding(fid, f"{JSON15}:{kind}", detail))

    if not ("sandboxing" in loc and "protectsystem=" in loc):
        add(f"R15-{prefix}-PIN", "stable heading tokens absent")
    if kind == LOC_ID:
        if not ("source-scope-correction-r14" in sup and re.search(r"1266|render|locator|location", sup)):
            add("R15-LOCATOR-SUPERSEDES", "r14 locator pointer absent")
        if not ("sandboxing" in rep and "protectsystem=" in rep and re.search(r"stable|heading", rep)
                and re.search(r"reader|renderer", rep)
                and re.search(r"withdraw|supersed|not a locator", rep)):
            add("R15-LOCATOR-PIN", "stable/withdrawn replacement tokens absent")
    else:
        if not ("source-scope-correction-r14" in sup
                and re.search(r"no further values|negative|absence|exhaustive", sup)):
            add("R15-POSITIVE-SUPERSEDES", "r14 negative pointer absent")
        if not ("boolean" in rep and "full" in rep and "strict" in rep
                and re.search(r"positive|takes a boolean|documented (?:domain|input|values)", rep)):
            add("R15-POSITIVE-PIN", "positive boolean/full/strict tokens absent")
    return out


def json15_scan(doc, owners):
    out, bad = [], set()
    for path, text in leaves(doc):
        key = path.rsplit(".", 1)[-1]
        index = re.match(r"corrections\[(\d+)\]", path)
        owner = owners.get(int(index.group(1))) if index else (
            LOC_ID if path.startswith("sources[") and key == "anchor" else "GLOBAL")
        hits = line_hits(text)
        if key in ("location", "anchor", "active_locator", "quote") and hits:
            out.append(Finding("LOCATOR_UNQUALIFIED", f"{JSON15}:{owner}", hits[0]))
            bad.add(owner)
        elif key in ("supersedes", "superseded_text"):
            if any("1266-1267" not in hit for hit in hits):
                out.append(Finding("LOCATOR_UNQUALIFIED", f"{JSON15}:{owner}",
                                   "non-historical line number in supersession pointer"))
                bad.add(owner)
        else:
            for hit in locator_sites(text):
                out.append(Finding("LOCATOR_UNQUALIFIED", f"{JSON15}:{owner}", hit))
                bad.add(owner)
        if key not in ("supersedes", "superseded_text"):
            for hit in absence_sites(text):
                out.append(Finding("NEGATIVE_DOMAIN_UNSWEPT", f"{JSON15}:{owner}", hit))
                bad.add(owner)
    return out, bad


def json15_issues(doc):
    out, valid = [], {LOC_ID: True, POS_ID: True}
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA:
        out.append(Finding("R15-JSON-SCHEMA", JSON15, "schema tsukuroi-locator-clarification-v1 required"))
        valid = {LOC_ID: False, POS_ID: False}
    if isinstance(doc, dict):
        extra = sorted(set(doc) - {"schema", "corrections"})
        if extra:
            out.append(Finding("R15-JSON-SCHEMA", JSON15, "extra top-level keys=" + ",".join(extra)))
            valid = {LOC_ID: False, POS_ID: False}
    corrections = doc.get("corrections") if isinstance(doc, dict) else None
    if not isinstance(corrections, list):
        out.append(Finding("R15-JSON-SCHEMA", JSON15, "corrections array required"))
        return out, {LOC_ID: False, POS_ID: False}
    if len(corrections) != 2:
        out.append(Finding("R15-CORRECTION-COUNT", JSON15, f"corrections={len(corrections)}"))
        valid = {LOC_ID: False, POS_ID: False}
    by_id, owners = {}, {}
    for index, obj in enumerate(corrections):
        cid = obj.get("id") if isinstance(obj, dict) else None
        owners[index] = cid if cid in (LOC_ID, POS_ID) else "GLOBAL"
        if cid not in (LOC_ID, POS_ID):
            out.append(Finding("R15-CORRECTION-ID", JSON15, f"unexpected id={cid!r}"))
            valid = {LOC_ID: False, POS_ID: False}
        elif cid in by_id:
            out.append(Finding("R15-CORRECTION-ID", JSON15, f"duplicate id={cid}"))
            valid[cid] = False
        else:
            by_id[cid] = obj
    for kind in (LOC_ID, POS_ID):
        prefix = "LOCATOR" if kind == LOC_ID else "POSITIVE"
        obj = by_id.get(kind)
        if obj is None:
            out.append(Finding("R15-CORRECTION-ID", JSON15, f"missing id={kind}"))
            valid[kind] = False
            continue
        missing = [f for f in REQUIRED if not isinstance(obj.get(f), str) or not obj[f].strip()]
        extra = sorted(set(obj) - set(REQUIRED))
        if missing or extra:
            out.append(Finding(f"R15-{prefix}-FIELD", f"{JSON15}:{kind}",
                               ("missing=" + ",".join(missing) if missing else "")
                               + (" extra=" + ",".join(extra) if extra else "")))
            valid[kind] = False
        if obj.get("source_id") != "S046" or obj.get("url") != URL:
            out.append(Finding(f"R15-{prefix}-SOURCE", f"{JSON15}:{kind}", "S046 + systemd.exec.5 required"))
            valid[kind] = False
        count = len(norm(obj.get("quote")).split()) if isinstance(obj.get("quote"), str) else 0
        if not 1 <= count <= 25:
            out.append(Finding(f"R15-{prefix}-QUOTE-WORDS", f"{JSON15}:{kind}", f"words={count}"))
            valid[kind] = False
        elif kind == POS_ID and norm(obj.get("quote")) != QUOTE:
            out.append(Finding("R15-POSITIVE-QUOTE", f"{JSON15}:{kind}", "exact definition sentence required"))
            valid[kind] = False
        pins = token_issues(kind, obj)
        out += pins
        if pins:
            valid[kind] = False
    issues, bad = json15_scan(doc, owners)
    out += issues
    for owner in bad:
        if owner in valid:
            valid[owner] = False
        else:
            valid = {LOC_ID: False, POS_ID: False}
    return out, valid


def md14_notice_ok(text):
    match = re.search(r"(?m)^## R15 supersession\b.*$", text)
    if not match:
        return False
    body = re.split(r"(?m)^## ", text[match.end():])[0]
    low = plain(body).lower()
    return all(token in low for token in (
        "r15-locator", "r15-positive-domain", "rendered lines 1266-1267",
        "documents no further values for this option", "corrections[0].location",
        "sources[0].anchor", "corrections[0].replacement", "source-locator-clarification-r15.md",
        "tsukuroi-locator-clarification-v1")) and re.search(r"supersed|withdraw", low) is not None


def json14_notice_ok(doc):
    item = doc.get("r15_supersession") if isinstance(doc, dict) else None
    if not isinstance(item, dict) or item.get("round") != "round-15":
        return False
    pair = item.get("canonical_pair")
    if not isinstance(pair, dict) or pair.get("schema") != SCHEMA \
            or not str(pair.get("md", "")).endswith("source-locator-clarification-r15.md") \
            or not str(pair.get("json", "")).endswith("source-locator-clarification-r15.json") \
            or set(pair.get("correction_ids") or []) != {LOC_ID, POS_ID}:
        return False
    notices = {n.get("id"): n for n in item.get("notices") or [] if isinstance(n, dict)}
    loc, pos = notices.get(LOC_ID), notices.get(POS_ID)
    if not all(isinstance(n, dict) for n in (loc, pos)):
        return False
    fields_ok = all(isinstance(n.get(f), str) and n[f].strip() for n in (loc, pos)
                    for f in ("supersedes", "superseded_text", "reason", "preserved"))
    loc_sup, pos_sup = plain(loc.get("supersedes")).lower(), plain(pos.get("supersedes")).lower()
    loc_active = plain(loc.get("active_locator")).lower()
    return fields_ok and isinstance(loc.get("active_locator"), str) \
        and "1266-1267" in str(loc.get("superseded_text")) \
        and "corrections[0].location" in loc_sup and "sources[0].anchor" in loc_sup \
        and "sandboxing" in loc_active and "protectsystem=" in loc_active \
        and "corrections[0].replacement" in pos_sup \
        and "documents no further values" in plain(pos.get("superseded_text")).lower()


def json14_notice_scan(doc):
    item = doc.get("r15_supersession") if isinstance(doc, dict) else None
    out = []
    if not isinstance(item, dict):
        return out
    for path, text in leaves(item):
        key, hits = path.rsplit(".", 1)[-1], line_hits(text)
        if key == "active_locator" and hits:
            out.append(Finding("LOCATOR_UNQUALIFIED", f"{JSON14}:r15_supersession", hits[0]))
        elif key in ("supersedes", "superseded_text") and any("1266-1267" not in hit for hit in hits):
            out.append(Finding("LOCATOR_UNQUALIFIED", f"{JSON14}:r15_supersession", hits[0]))
    return out


def history_issues(md14, doc14, digests):
    out = []
    heading = re.search(r"(?m)^## R15 supersession\b", md14)
    prefix = md14[:heading.start()] if heading else md14
    if digest(prefix.rstrip()) != digests[0]:
        out.append(Finding("R15-HISTORY-REWRITTEN", MD14, "original bytes changed before r15 notice"))
    original = {k: v for k, v in doc14.items() if k != "r15_supersession"} if isinstance(doc14, dict) else {}
    if digest(canon(original)) != digests[1]:
        out.append(Finding("R15-HISTORY-REWRITTEN", JSON14, "original JSON values changed"))
    return out


def md14_defects(text, notice_ok):
    if notice_ok:
        return []
    text = section(text, "## R14-VALUE-DOMAIN") or ""
    return [Finding("LOCATOR_UNQUALIFIED", MD14, hit) for hit in locator_sites(text)] + [
        Finding("NEGATIVE_DOMAIN_UNSWEPT", MD14, hit) for hit in absence_sites(text)]


def json14_defects(doc, notice_ok):
    if notice_ok or not isinstance(doc, dict):
        return []
    out = []
    for correction in doc.get("corrections") or []:
        if isinstance(correction, dict):
            out += [Finding("LOCATOR_UNQUALIFIED", JSON14, hit)
                    for hit in line_hits(correction.get("location", ""))]
            out += [Finding("NEGATIVE_DOMAIN_UNSWEPT", JSON14, hit)
                    for hit in absence_sites(correction.get("replacement", ""))]
    for source in doc.get("sources") or []:
        if isinstance(source, dict):
            out += [Finding("LOCATOR_UNQUALIFIED", JSON14, hit)
                    for hit in line_hits(source.get("anchor", ""))]
    return out


def evaluate(docs):
    findings = []
    for path, field, fid in ((MD15, "md15", "R15-MD-MISSING"), (JSON15, "json15", "R15-JSON-MISSING"),
                             (MD14, "md14", "R15-HISTORY-MISSING"), (JSON14, "json14", "R15-HISTORY-MISSING")):
        if docs._asdict()[field] is None:  # round-34 C1: a plain field read, no getattr
            findings.append(Finding(fid, path, "file absent"))
    try:
        doc15 = json.loads(docs.json15) if docs.json15 is not None else None
    except json.JSONDecodeError as exc:
        return Result(CANNOT, [Finding("E-R15-JSON-PARSE", JSON15, str(exc)[:120])], 0)
    try:
        doc14 = json.loads(docs.json14) if docs.json14 is not None else None
    except json.JSONDecodeError as exc:
        return Result(CANNOT, [Finding("E-R15-JSON14-PARSE", JSON14, str(exc)[:120])], 0)
    valid = {LOC_ID: False, POS_ID: False}
    if doc15 is not None:
        issues, valid = json15_issues(doc15)
        findings += issues
    if docs.md15 is not None:
        findings += md15_issues(docs.md15)
    has_new = docs.md15 is not None or docs.json15 is not None
    md_notice = md14_notice_ok(docs.md14 or "") if has_new else False
    json_notice = json14_notice_ok(doc14) if has_new else False
    if has_new and docs.md14 is not None and not md_notice:
        findings.append(Finding("R15-R14-MD-NOTICE", MD14, "r15 supersession section absent"))
    if has_new and doc14 is not None and not json_notice:
        findings.append(Finding("R15-R14-JSON-NOTICE", JSON14, "r15_supersession notice absent"))
    if docs.md14 is not None and doc14 is not None:
        findings += md14_defects(docs.md14, md_notice)
        findings += json14_defects(doc14, json_notice)
        findings += json14_notice_scan(doc14)
        findings += history_issues(docs.md14, doc14, docs.digests)
    findings = [Finding(*key) for key in sorted({(f.id, f.site, f.detail) for f in findings})]
    common = {"R15-MD-MISSING", "R15-JSON-MISSING", "R15-HISTORY-MISSING", "R15-MD-OPENERS",
              "R15-MD-HEADING", "R15-MD-QUALITY", "R15-R14-MD-NOTICE", "R15-R14-JSON-NOTICE",
              "R15-HISTORY-REWRITTEN", "R15-JSON-SCHEMA", "R15-CORRECTION-COUNT", "R15-CORRECTION-ID"}
    loc_block = common | {"R15-LOCATOR-FIELD", "R15-LOCATOR-SOURCE", "R15-LOCATOR-PIN",
                          "R15-LOCATOR-SUPERSEDES", "R15-LOCATOR-QUOTE-WORDS",
                          "LOCATOR_UNQUALIFIED", "R15-MD-LOCATOR"}
    pos_block = common | {"R15-POSITIVE-FIELD", "R15-POSITIVE-SOURCE", "R15-POSITIVE-QUOTE",
                          "R15-POSITIVE-PIN", "R15-POSITIVE-SUPERSEDES",
                          "R15-POSITIVE-QUOTE-WORDS", "NEGATIVE_DOMAIN_UNSWEPT", "R15-MD-POSITIVE"}
    def blocked(kind, ids):
        other = POS_ID if kind == LOC_ID else LOC_ID
        return any(f.id in ids and f.site != f"{JSON15}:{other}" for f in findings)
    count = int(valid.get(LOC_ID) and not blocked(LOC_ID, loc_block))
    count += int(valid.get(POS_ID) and not blocked(POS_ID, pos_block))
    return Result(FAIL if findings else PASS, findings, count)


def payload(result, revision, branch="master", branch_tip=None):
    return {"status": {PASS: "PASS", FAIL: "FAIL", CANNOT: "CANNOT_EVALUATE"}[result.code],
            "revision": revision, "branch": branch, "branch_tip": branch_tip,
            "correction_count": result.count,
            "findings": [{"id": f.id, "site": f.site, "detail": f.detail} for f in result.findings]}


def emit(result, revision, branch="master", branch_tip=None):
    print(json.dumps(payload(result, revision, branch, branch_tip), sort_keys=True))
    return result.code


def read_tree(path):
    target = ROOT / path
    try:
        return target.read_bytes().decode("utf-8") if target.is_file() else None
    except (OSError, UnicodeDecodeError) as exc:
        raise Cannot("E-READ-FAILED", path, str(exc)[:120])


def git(*args, repo=None):
    env = {"PATH": "/usr/bin:/bin", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}  # round-34 C1: fixed allow-list, no ambient copy
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat", "LC_ALL": "C"})
    try:
        return subprocess.run(["git", "--no-pager", "-C", str(repo or ROOT), *args],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=30)
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


def build_parser():
    parser = argparse.ArgumentParser(description="Narrow read-only round-15 locator clarification gate.",
                                     exit_on_error=False)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--revision", metavar="REV",
                       help="hex commit, bound to --branch; reads immutable objects only")
    group.add_argument("--selftest", action="store_true", help="in-memory fixture suite")
    parser.add_argument("--branch", metavar="BRANCH", default="master",
                        help="branch --revision must be landed on (default master)")
    return parser


def cli_finding(argv):
    try:
        build_parser().parse_args(argv)
        return None
    except (argparse.ArgumentError, SystemExit):
        return "E-CLI"


BASE_MD14 = ("# r14 corrections\n## R14-VALUE-DOMAIN\nSource object: S044, `systemd.exec(5)` § ProtectSystem= "
             "(under SANDBOXING),\nrendered lines 1266-1267, page footer systemd 262.1, opened 2026-10-20.\n"
             "**Proposition supported:** The opened revision documents no further values for `ProtectSystem=`.\n"
             "**Replacement:** the opened revision documents no further values for this option.\n")
APPENDIX = ("\n## R15 supersession (2026-10-20) — locator and positive-domain notices\n\n"
            "`corpus/knowledge/source-locator-clarification-r15.md` / `.json`\n"
            "(schema `tsukuroi-locator-clarification-v1`) supersede only the supplemental locator\n"
            "\"rendered lines 1266-1267\" as unqualified historical text, and the negative sentence\n"
            "\"documents no further values for this option\" as unsupported absence. R15-LOCATOR and\n"
            "R15-POSITIVE-DOMAIN supply the stable SANDBOXING > ProtectSystem= heading and the positive\n"
            "option definition. Sources: corrections[0].location; sources[0].anchor; corrections[0].replacement.\n")
BASE_JSON14 = {"schema": "tsukuroi-source-scope-correction-v1", "corrections": [
    {"id": "R14-VALUE-DOMAIN", "location": "systemd.exec(5) § ProtectSystem= (SANDBOXING), "
     "rendered lines 1266-1267; page footer systemd 262.1", "quote": QUOTE,
     "replacement": "The opened revision documents no further values for this option."},
    {"id": "R14-COMMENT-ATTRIBUTION", "location": "comment 6071740243, body first sentence",
     "quote": "I tried this on a stock Omarchy worker VM"}],
    "sources": [{"source_id": "S044", "url": URL, "anchor":
                 "§ ProtectSystem= (SANDBOXING), rendered lines 1266-1267; footer systemd 262.1"}]}
NOTICE14 = {"round": "round-15", "canonical_pair": {"md": MD15, "json": JSON15, "schema": SCHEMA,
                                                    "correction_ids": [LOC_ID, POS_ID]},
            "notices": [
                {"id": LOC_ID, "supersedes": "corrections[0].location; sources[0].anchor (S044)",
                 "superseded_text": "rendered lines 1266-1267", "reason": "renderer-dependent "
                 "supplemental locator", "active_locator": "stable SANDBOXING > ProtectSystem= "
                 "heading plus page footer", "preserved": "old bytes unchanged"},
                {"id": POS_ID, "supersedes": "corrections[0].replacement negative sentence",
                 "superseded_text": "documents no further values for this option", "reason":
                 "unsupported exhaustive absence", "preserved": "old bytes unchanged"}]}
MD15_CLEAN = ("source: S046 — https://man.archlinux.org/man/systemd.exec.5; reopened 2026-10-20, "
              "footer systemd 262.1.\nverified-at: 2026-10-20\nrecheck: on systemd.exec(5) revision "
              "change; no host command.\n\n# Locator clarification (round 15)\n\n## R15-LOCATOR\n"
              "S046 locator is the stable § SANDBOXING > ProtectSystem= heading, not any renderer's line\n"
              "numbers. The historical \"rendered lines 1266-1267\" is reader-dependent supplemental text\n"
              "and withdrawn as a locator; the quote is not false.\n\n## R15-POSITIVE-DOMAIN\n"
              "S046 defines the option positively: Takes a boolean argument or the special values\n"
              "\"full\" or \"strict\". The documented domain is boolean, full and strict; this correction\n"
              "does not assert an exhaustive absence.\n\n## QUALITY check\nBounded conformance over named\n"
              "headings, two corrections, quote words and notices.\n")
JSON15_CLEAN = {"schema": SCHEMA, "corrections": [
    {"id": LOC_ID, "source_id": "S046", "url": URL, "location":
     "systemd.exec(5) § SANDBOXING > ProtectSystem= (stable heading), page footer systemd 262.1",
     "quote": "ProtectSystem=", "replacement": "The active locator is the stable SANDBOXING > "
     "ProtectSystem= heading; the historical \"rendered lines 1266-1267\" are reader-dependent "
     "supplemental text and withdrawn as a locator.",
     "supersedes": "corpus/knowledge/source-scope-correction-r14.json corrections[0].location "
     "rendered lines 1266-1267"},
    {"id": POS_ID, "source_id": "S046", "url": URL, "location":
     "systemd.exec(5) § SANDBOXING > ProtectSystem= first definition", "quote": QUOTE,
     "replacement": "The documented ProtectSystem= domain is positive: a boolean argument or the "
     "special values full and strict. This correction does not assert an exhaustive absence of "
     "undocumented values.",
     "supersedes": "corpus/knowledge/source-scope-correction-r14.md R14-VALUE-DOMAIN negative "
     "absence proposition"}]}


def fixtures():
    doc14 = json.loads(json.dumps(BASE_JSON14))
    doc14["r15_supersession"] = NOTICE14
    digests = (digest(BASE_MD14.rstrip()), digest(canon(BASE_JSON14)))
    return DocSet(MD15_CLEAN, json.dumps(JSON15_CLEAN), BASE_MD14 + APPENDIX, json.dumps(doc14), digests)


BINDING_WANTS = {
    "binding-landed-tip-accepted": "OK",
    "binding-head-rejected": _revision.E_INVALID,
    "binding-invalid-branch-range": _revision.E_BRANCH_INVALID,
    "binding-invalid-branch-slash": _revision.E_BRANCH_INVALID,
    "binding-invalid-branch-space": _revision.E_BRANCH_INVALID,
    "binding-invalid-branch-head": _revision.E_BRANCH_INVALID,
    "binding-branch-first": _revision.E_BRANCH_INVALID,
    "binding-invalid-revision-before-missing": _revision.E_INVALID,
    "binding-missing-branch": _revision.E_BRANCH_MISSING,
    "binding-missing-nested-branch": _revision.E_BRANCH_MISSING,
    "binding-unlanded-rejected": _revision.E_NOT_LANDED,
    "binding-not-pushed-rejected": _revision.E_NOT_PUSHED,
    "binding-git-failed": _revision.E_GIT,
    "binding-main-single-id": "OK",
}


def binding_cases():
    """Exercise shared revision binding in a throwaway repo; the lane repo is untouched."""
    global ROOT
    tmp = tempfile.mkdtemp(prefix="locator-clarification-")
    env = {"PATH": "/usr/bin:/bin", "GIT_CONFIG_NOSYSTEM": "1"}  # round-34 C1: fixed allow-list, no ambient copy
    env.update({"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull,
                "GIT_TERMINAL_PROMPT": "0", "GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat",
                "LC_ALL": "C", "GIT_AUTHOR_NAME": "gate", "GIT_AUTHOR_EMAIL": "gate@example.invalid",
                "GIT_COMMITTER_NAME": "gate", "GIT_COMMITTER_EMAIL": "gate@example.invalid"})

    def run(*args):
        proc = subprocess.run(["git", "-C", tmp, *args], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, env=env, timeout=30)
        if proc.returncode != 0:
            raise RuntimeError(f"{args[0]}: {proc.stderr.decode('utf-8', 'replace').strip()[:80]}")
        return proc.stdout.decode("ascii", "replace").strip()

    def check(name, rev, tip, branch="master"):
        try:
            binding = _revision.bind(tmp, rev, branch)
            got = ("OK" if binding.sha == rev and binding.branch == branch
                   and binding.branch_tip == tip else "MISMATCH")
        except _revision.RevisionError as exc:
            got = exc.fid if exc.site and isinstance(exc.detail, str) else "MISMATCH"
        except Exception as exc:
            got = "ERROR:" + type(exc).__name__
        return name, got, BINDING_WANTS[name]

    try:
        run("init", "-q", "-b", "master")
        Path(tmp, "a.txt").write_text("one\n", encoding="utf-8")
        run("add", "a.txt")
        run("commit", "-q", "-m", "c0")
        first = run("rev-parse", "HEAD")
        Path(tmp, "a.txt").write_text("two\n", encoding="utf-8")
        run("commit", "-q", "-a", "-m", "c1")
        tip = run("rev-parse", "HEAD")
        run("checkout", "-q", "-b", "side")
        Path(tmp, "a.txt").write_text("three\n", encoding="utf-8")
        run("commit", "-q", "-a", "-m", "c2")
        side = run("rev-parse", "HEAD")
        run("checkout", "-q", "master")
        out = [check("binding-landed-tip-accepted", tip, tip),
               check("binding-head-rejected", "HEAD", tip)]
        for label, branch in (("range", "a..b"), ("slash", "master/"),
                              ("space", "bad branch"), ("head", "HEAD")):
            out.append(check(f"binding-invalid-branch-{label}", tip, tip, branch))
        out.extend([
            check("binding-branch-first", "HEAD", tip, "a..b"),
            check("binding-invalid-revision-before-missing", "HEAD", None, "nosuch"),
            check("binding-missing-branch", tip, None, "nosuch"),
            check("binding-missing-nested-branch", tip, None, "feature/x"),
            check("binding-unlanded-rejected", side, tip),
        ])
        run("update-ref", "refs/remotes/origin/master", first)
        out.append(check("binding-not-pushed-rejected", tip, tip))
        Path(tmp, "blob.txt").write_text("not a commit\n", encoding="utf-8")
        blob = run("hash-object", "-w", "blob.txt")
        run("update-ref", "refs/remotes/origin/master", blob)
        out.append(check("binding-git-failed", tip, tip))
        run("update-ref", "refs/remotes/origin/master", tip)

        import contextlib, io
        original_root = ROOT
        try:
            ROOT = Path(tmp)
            with contextlib.redirect_stdout(io.StringIO()) as captured:
                code = main(["--revision", "HEAD", "--branch", "a..b"])
            doc = json.loads(captured.getvalue())
            findings = doc.get("findings")
            ids = [item.get("id") for item in findings if isinstance(item, dict)] \
                if isinstance(findings, list) else []
            got = ("OK" if code == CANNOT and ids == [_revision.E_BRANCH_INVALID]
                   else "MISMATCH")
            out.append(("binding-main-single-id", got, BINDING_WANTS["binding-main-single-id"]))
        finally:
            ROOT = original_root
        return out, None
    except Exception as exc:
        return ([(name, "setup:" + type(exc).__name__, want)
                 for name, want in BINDING_WANTS.items()],
                f"{type(exc).__name__}: {exc}"[:120])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def selftest():
    base = fixtures()
    clean_json, clean14 = JSON15_CLEAN, json.loads(base.json14)
    cases = [("clean", base, PASS, set(), 2),
             ("baseline", DocSet(None, None, BASE_MD14, json.dumps(BASE_JSON14), base.digests), FAIL,
              {"R15-MD-MISSING", "R15-JSON-MISSING", "LOCATOR_UNQUALIFIED", "NEGATIVE_DOMAIN_UNSWEPT"}, 0)]
    doc = json.loads(json.dumps(clean_json))
    doc["corrections"][0]["location"] = ("systemd.exec(5) § ProtectSystem= (SANDBOXING), "
                                         "rendered lines 1266-1267")
    cases.append(("restored-locator-json", base._replace(json15=json.dumps(doc)), FAIL,
                  {"LOCATOR_UNQUALIFIED"}, 1))
    for name, extra in (("restored-locator-md-url", "Source object: S046, https://man.archlinux.org/"
                         "man/systemd.exec.5 § SANDBOXING > ProtectSystem=, rendered lines 1266-1267."),
                        ("restored-locator-md-1272", "Active locator: rendered lines 1272-1273 in the "
                         "closure reader."),
                        ("historical-active-locator", "The historical source lists rendered lines 1266-1267.")):
        cases.append((name, base._replace(md15=MD15_CLEAN.replace("Bounded conformance", extra +
                                                                       "\nBounded conformance")),
                      FAIL, {"LOCATOR_UNQUALIFIED"}, 1))
    for name, prose in (("restored-negative-md", "The opened revision documents no further values; "
                         "this is historical."),
                        ("split-negative-md", "The opened revision documents no\nfurther values."),
                        ("only-values-md", "Only documented values are possible.")):
        cases.append((name, base._replace(md15=MD15_CLEAN.replace(
            "does not assert an exhaustive absence.", "does not assert an exhaustive absence. " + prose)),
            FAIL, {"NEGATIVE_DOMAIN_UNSWEPT"}, 1))
    doc = json.loads(json.dumps(clean_json))
    doc["corrections"][1]["replacement"] += " Only documented values exist."
    cases.append(("only-values-json", base._replace(json15=json.dumps(doc)), FAIL,
                  {"NEGATIVE_DOMAIN_UNSWEPT"}, 1))
    doc = json.loads(json.dumps(clean_json))
    doc["sources"] = [{"anchor": "§ ProtectSystem= (SANDBOXING), rendered lines 1266-1267"}]
    cases.append(("extra-anchor-json15", base._replace(json15=json.dumps(doc)), FAIL,
                  {"R15-JSON-SCHEMA", "LOCATOR_UNQUALIFIED"}, 0))
    doc = json.loads(json.dumps(clean_json))
    doc["corrections"][1]["replacement"] += " Active locator: line 1272."
    cases.append(("locator-1272-json", base._replace(json15=json.dumps(doc)), FAIL,
                  {"LOCATOR_UNQUALIFIED"}, 1))
    moved = json.loads(json.dumps(clean14))
    moved["relocated"] = moved.pop("r15_supersession")
    cases.append(("notices-moved", base._replace(md14=BASE_MD14, json14=json.dumps(moved),
                                                 md15=MD15_CLEAN + APPENDIX), FAIL,
                  {"R15-R14-MD-NOTICE", "R15-R14-JSON-NOTICE", "R15-HISTORY-REWRITTEN",
                   "LOCATOR_UNQUALIFIED", "NEGATIVE_DOMAIN_UNSWEPT"}, 0))
    cases.append(("notice-absent-md", base._replace(md14=BASE_MD14), FAIL,
                  {"R15-R14-MD-NOTICE", "LOCATOR_UNQUALIFIED", "NEGATIVE_DOMAIN_UNSWEPT"}, 0))
    cases.append(("notice-absent-json", base._replace(json14=json.dumps(BASE_JSON14)), FAIL,
                  {"R15-R14-JSON-NOTICE", "LOCATOR_UNQUALIFIED", "NEGATIVE_DOMAIN_UNSWEPT"}, 0))
    doc = json.loads(json.dumps(clean14))
    doc["r15_supersession"]["notices"][0]["active_locator"] = ("SANDBOXING > ProtectSystem= stable "
                                                               "heading at lines 1266-1267")
    cases.append(("notice-active-locator-number", base._replace(json14=json.dumps(doc)), FAIL,
                  {"LOCATOR_UNQUALIFIED"}, 1))
    doc = json.loads(json.dumps(clean14))
    doc["r15_supersession"]["notices"][0]["supersedes"] = "corrections[0].location"
    cases.append(("anchor-uncovered", base._replace(json14=json.dumps(doc)), FAIL,
                  {"R15-R14-JSON-NOTICE", "LOCATOR_UNQUALIFIED", "NEGATIVE_DOMAIN_UNSWEPT"}, 0))
    cases.append(("delete-original-md", base._replace(md14=APPENDIX), FAIL,
                  {"R15-HISTORY-REWRITTEN"}, 0))
    doc = json.loads(json.dumps(clean14))
    doc["corrections"][0]["replacement"] = "The opened revision takes a boolean argument."
    cases.append(("delete-original-json", base._replace(json14=json.dumps(doc)), FAIL,
                  {"R15-HISTORY-REWRITTEN"}, 0))
    doc = json.loads(json.dumps(clean_json))
    doc["corrections"][1]["quote"] = " ".join(f"word{i}" for i in range(26))
    cases.append(("oversized-quote", base._replace(json15=json.dumps(doc)), FAIL,
                  {"R15-POSITIVE-QUOTE-WORDS"}, 1))
    cases.append(("malformed-json", base._replace(json15="{"), CANNOT, {"E-R15-JSON-PARSE"}, 0))
    passed, failures = 0, []
    for name, docs, code, want, count in cases:
        result = evaluate(docs)
        got = {f.id for f in result.findings}
        problems = []
        if result.code != code:
            problems.append(f"exit={result.code}/{code}")
        if got != want:
            problems.append("ids=" + ",".join(sorted(got)) + " want=" + ",".join(sorted(want)))
        if result.count != count:
            problems.append(f"count={result.count}/{count}")
        if problems:
            failures.append(f"{name}: " + "; ".join(problems))
        else:
            passed += 1
    for name, got, want in (("invalid-cli", cli_finding(["--bogus"]), "E-CLI"),):
        if got == want:
            passed += 1
        else:
            failures.append(f"{name}: id={got}/{want}")
    binding, binding_error = binding_cases()
    for name, got, want in binding:
        if got == want:
            passed += 1
        else:
            failures.append(f"{name}: id={got}/{want}")
    doc = payload(Result(PASS, [], 2), "a" * 40, "master", "b" * 40)
    shape = sorted(doc)
    if shape == ["branch", "branch_tip", "correction_count", "findings", "revision", "status"] \
            and doc["branch"] == "master" and doc["branch_tip"] == "b" * 40:
        passed += 1
    else:
        failures.append("payload-shape: keys=" + ",".join(shape))
    if binding_error:
        failures.append("binding-sandbox: " + binding_error)
    total = len(cases) + 2 + len(binding)
    if failures:
        print(f"CHECK_LOCATOR_CLARIFICATION_SELFTEST: FAIL ({total} cases, {passed} passed)")
        print("\n".join("  " + item for item in failures))
        return FAIL
    print(f"CHECK_LOCATOR_CLARIFICATION_SELFTEST: PASS ({total} cases, {passed} passed, 0 failed)")
    return PASS


def main(argv=None):
    try:
        args = build_parser().parse_args(argv)
    except (argparse.ArgumentError, SystemExit) as exc:
        if isinstance(exc, SystemExit) and not exc.code:
            return 0
        return emit(Result(CANNOT, [Finding("E-CLI", "cli", "invalid arguments")], 0), "worktree")
    if args.selftest:
        return selftest()
    branch, tip, revision = args.branch, None, "worktree"
    try:
        if args.revision is not None:
            try:
                binding = _revision.bind(ROOT, args.revision, branch)
            except _revision.RevisionError as exc:
                tip = _revision.branch_tip(ROOT, branch)
                revision = args.revision
                raise Cannot(exc.fid, exc.site, exc.detail) from exc
            revision, tip = binding.sha, binding.branch_tip
            docs = DocSet(*[read_git(revision, path) for path in FILES], (MD14_SHA, JSON14_SHA))
        else:
            docs = DocSet(*[read_tree(path) for path in FILES], (MD14_SHA, JSON14_SHA))
    except Cannot as exc:
        return emit(Result(CANNOT, [Finding(exc.fid, exc.site, exc.detail)], 0),
                    revision, branch, tip)
    except Exception as exc:  # no traceback exit 1: unreadable input is CANNOT
        return emit(Result(CANNOT, [Finding("E-INTERNAL", "gate", str(exc)[:120])], 0), revision,
                    branch, tip)
    try:
        result = evaluate(docs)
    except Exception as exc:
        return emit(Result(CANNOT, [Finding("E-INTERNAL", "gate", str(exc)[:120])], 0), revision,
                    branch, tip)
    return emit(result, revision, branch, tip)


if __name__ == "__main__":
    sys.exit(main())
