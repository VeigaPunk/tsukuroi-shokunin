#!/usr/bin/env python3
"""Narrow, read-only round-14 source-scope correction conformance gate.

Not a semantic proof: bounded conformance for the two named corrections,
retained historical defect phrases with preceding supersession notices, and the
S042 / appended S045 registry relation. Exit 0 clean, 1 failed, 2 cannot
evaluate. No writes, no network; --selftest uses in-memory literals only.
"""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys
from collections import namedtuple
from pathlib import Path

PASS, FAIL, CANNOT = 0, 1, 2
ROOT = Path(__file__).resolve().parents[1]
R13_MD = "corpus/knowledge/root-dac-correction-r13.md"
LESSON = "corpus/lessons/round-13.md"
SOURCES = "corpus/SOURCES.md"
R14_MD = "corpus/knowledge/source-scope-correction-r14.md"
R14_JSON = "corpus/knowledge/source-scope-correction-r14.json"
FILES = (R14_MD, R14_JSON, R13_MD, LESSON, SOURCES)
SCHEMA = "tsukuroi-source-scope-correction-v1"
VALUE_ID, ATTR_ID = "R14-VALUE-DOMAIN", "R14-COMMENT-ATTRIBUTION"
VALUE_URL = "https://man.archlinux.org/man/systemd.exec.5"
ATTR_URL = "https://api.github.com/repos/omacom/omarchy/issues/comments/6071740243"
REV = re.compile(r"^(?:HEAD|[0-9a-fA-F]{4,64})$")
DOMAIN_BAD = re.compile(r"value\s+set\s+(?:is\s+|are\s+)?not\s+(?:exhaustive|closed|the\s+only)"
                        r"|values\s+(?:are|is)\s+not\s+(?:exhaustive|closed)", re.I)
ATTR_BAD = re.compile(r"self-described[^.]{0,100}(?:model[- ]generated|automated\s+triage)"
                      r"|(?:model[- ]generated|automated\s+triage)[^.]{0,100}self-described", re.I)
ATTR_HIST = re.compile(r"self-described model-generated triage from\s+an API account", re.I)
THEOREM = re.compile(r"\b(?:proves?|proven|theorem|guarantees?|establishes)\b[^.\n]{0,80}"
                     r"\b(?:general\s+)?(?:correctness|security|host\s+cause|read-only)\b", re.I)
MECH = re.compile(r"(?:non-exhaustive|not exhaustive|not closed)[^.]{0,100}"
                  r"(?:mechanism|unit-side|examples?)|(?:mechanism|unit-side|examples?)"
                  r"[^.]{0,100}(?:non-exhaustive|not exhaustive|not closed)", re.I)
HEADS = ("## R14-VALUE-DOMAIN", "## R14-COMMENT-ATTRIBUTION", "## QUALITY check")
REQUIRED = ("id", "supersedes", "source_id", "url", "location", "quote", "replacement")
Finding = namedtuple("Finding", "id site detail")
DocSet = namedtuple("DocSet", "md14 json14 md13 lesson sources")
Result = namedtuple("Result", "code findings count")


class Cannot(Exception):
    def __init__(self, fid, site, detail):
        super().__init__(detail)
        self.fid, self.site, self.detail = fid, site, detail


def plain(text):
    return " ".join(str(text).replace("`", "").split())


def section(text, heading):
    lines = [line.rstrip() for line in text.splitlines()]
    if heading not in lines:
        return None
    start = lines.index(heading)
    body = []
    for line in text.splitlines()[start + 1:]:
        if line.startswith("## "):
            break
        body.append(line)
    return "\n".join(body)


def negated(text, match):
    window = text[max(0, match.start() - 48):match.start()]
    return bool(re.search(r"\b(?:not|no|never|cannot|nonexistent|unsupported|incorrect|absent)\s*$", window)
                or re.search(r"(?:does not|do not|doesn't|don't)\s*$", window))


def active_restore(text, pattern):
    for block in re.split(r"\n\s*\n", text):
        if pattern.search(plain(block)) and not re.search(
                r"supersed|replac|no longer|historical|retired|quoted|says", block, re.I):
            return True
    return False


def theorem_hit(text):
    low = plain(text).lower()
    return any(not negated(low, m) for m in THEOREM.finditer(low))


def parse_rows(text):
    rows = {}
    for line in text.splitlines():
        match = re.match(r"\|\s*(S\d{3,})\s*\|", line)
        if match:
            rows[match.group(1)] = [c.strip() for c in line.strip().strip("|").split("|")]
    return rows


def domain_site(text):
    for index, line in enumerate(text.splitlines()):
        if line.strip().startswith("| r12 MD:41-42") and DOMAIN_BAD.search(line):
            return index
    return None


def md13_notice_ok(text):
    low, row = plain(text).lower(), domain_site(text)
    marker = next((i for i, line in enumerate(text.splitlines())
                   if "r14-value-domain" in line.lower()), None)
    return (row is not None and marker is not None and marker < row
            and re.search(r"\b97\b|r12\s+md:41-42", low) is not None
            and re.search(r"supersed|replac|withdraw|correct", low) is not None
            and ("value set" in low or "option domain" in low or "non-exhaustive" in low))


def lesson_notice_ok(text):
    low, site = plain(text).lower(), ATTR_HIST.search(plain(text).lower())
    denial = re.search(r"(?:does not|do not|doesn't|not|no|never|nonexistent|unsupported|incorrect|absent)"
                       r"[^.!?]{0,80}self[- ]descri[bp]|self[- ]descri[bp]\w*[^.!?]{0,60}"
                       r"(?:is|was|remains)\s+(?:absent|unsupported|incorrect|nonexistent)", low)
    return (site is not None and 0 <= low.find("r14-comment-attribution") < site.start()
            and "s042" in low and "s045" in low and denial is not None
            and re.search(r"supersed|withdraw|correct|replac|notice", low) is not None)


def value_rep_missing(rep):
    low = plain(rep).lower()
    return [name for name, ok in (
        ("protectsystem", "protectsystem" in low),
        ("domain", re.search(r"documented\s+values?|value\s+(?:set|domain)|domain", low) is not None),
        ("boolean", "boolean" in low),
        ("full", "full" in low),
        ("strict", "strict" in low),
        ("mechanism-scope", MECH.search(low) is not None),
    ) if not ok]


def attr_rep_missing(rep):
    low = plain(rep).lower()
    return [name for name, ok in (
        ("issue", any(token in low for token in ("8047", "s042", "6071740243"))),
        ("user", re.search(r"\buser\b", low) is not None),
        ("collaborator", "collaborator" in low),
        ("unverified", re.search(r"unverified|not verified|no verified", low) is not None),
        ("second-opinion", "second opinion" in low),
        ("maintainer", "maintainer" in low and re.search(r"defer|decid|wait", low) is not None),
        ("host-cause", re.search(r"(?:reject|not|no)[^.]{0,60}host[- ]cause|"
                                 r"host[- ]cause[^.]{0,60}(?:reject|unknown|not\s+(?:established|proven))",
                                 low) is not None),
        ("codex", "codex" in low),
    ) if not ok]


def md14_issues(text):
    out = []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    heads = [line.lower() for line in lines[:3]]
    if not (len(heads) == 3 and heads[0].startswith("source:") and heads[1].startswith("verified-at:")
            and heads[2].startswith("recheck:") and not any(line.startswith("#") for line in lines[:3])):
        out.append(Finding("R14-MD-OPENERS", R14_MD, "source:/verified-at:/recheck: first"))
    stripped = [line.rstrip() for line in text.splitlines()]
    if not all(head in stripped for head in HEADS):
        out.append(Finding("R14-MD-HEADING", R14_MD, "named headings absent"))
    value = plain(section(text, HEADS[0]) or "").lower()
    if not all(t in value for t in ("s044", "97", "boolean", "full", "strict", "mechanism")) or not (
            "non-exhaustive" in value or "not exhaustive" in value):
        out.append(Finding("R14-MD-VALUE-DOMAIN", R14_MD, "value-domain pins absent"))
    attr = plain(section(text, HEADS[1]) or "").lower()
    if not all(t in attr for t in ("s045", "8047", "user", "collaborator", "unverified",
                                   "second opinion", "maintainer")):
        out.append(Finding("R14-MD-COMMENT-ATTRIBUTION", R14_MD, "attribution pins absent"))
    if len(plain(section(text, HEADS[2]) or "")) < 40:
        out.append(Finding("R14-MD-QUALITY", R14_MD, "QUALITY check absent or empty"))
    for line in text.splitlines():
        if line.strip().lower().startswith("recheck:") and re.search(
                r"\b(?:snapper|sudo|systemctl|journalctl|pacman)\b", line, re.I):
            out.append(Finding("R14-MD-RECHECK", R14_MD, "recheck line names a host command"))
    if theorem_hit(text):
        out.append(Finding("R14-OVERCLAIM", R14_MD, "unnegated proof/guarantee language"))
    if active_restore(text, DOMAIN_BAD):
        out.append(Finding("R14-VALUE-DOMAIN-RESTORED", R14_MD, "old domain phrase active"))
    if active_restore(text, ATTR_BAD):
        out.append(Finding("R14-COMMENT-ATTRIBUTION-RESTORED", R14_MD, "old attribution active"))
    return out


def json14_issues(doc):
    out, valid = [], {VALUE_ID: True, ATTR_ID: True}
    global_ok = isinstance(doc, dict) and doc.get("schema") == SCHEMA
    if not global_ok:
        out.append(Finding("R14-JSON-SCHEMA", R14_JSON, "schema tsukuroi-source-scope-correction-v1 required"))
    corrections = doc.get("corrections") if isinstance(doc, dict) else None
    if not isinstance(corrections, list):
        out.append(Finding("R14-JSON-SCHEMA", R14_JSON, "corrections array required"))
        corrections, global_ok = [], False
    if len(corrections) != 2:
        out.append(Finding("R14-CORRECTION-COUNT", R14_JSON, f"corrections={len(corrections)}"))
        global_ok = False
    by_id = {}
    for obj in corrections:
        if not isinstance(obj, dict) or obj.get("id") not in (VALUE_ID, ATTR_ID):
            out.append(Finding("R14-CORRECTION-ID", R14_JSON,
                               f"unexpected id={str(obj.get('id') if isinstance(obj, dict) else obj)[:120]!r}"))
        elif obj["id"] in by_id:
            out.append(Finding("R14-CORRECTION-ID", R14_JSON, f"duplicate id={obj['id']}"))
            valid[obj["id"]] = False
        else:
            by_id[obj["id"]] = obj
    for cid in (VALUE_ID, ATTR_ID):
        if cid not in by_id:
            out.append(Finding("R14-CORRECTION-ID", R14_JSON, f"missing id={cid}"))
            valid[cid] = False
            continue
        obj, site = by_id[cid], f"{R14_JSON}:{cid}"

        def add(fid, detail):
            out.append(Finding(fid, site, detail))
            valid[cid] = False

        for field in REQUIRED:
            if not isinstance(obj.get(field), str) or not obj[field].strip():
                add("R14-JSON-SCHEMA", f"field={field}")
        words = len(obj.get("quote").split()) if isinstance(obj.get("quote"), str) else 0
        if not 1 <= words <= 25:
            add("R14-QUOTE-WORDS", f"words={words}")
        sup = obj.get("supersedes")
        sup = " ".join(map(str, sup)) if isinstance(sup, list) else (sup if isinstance(sup, str) else "")
        rep = obj.get("replacement") if isinstance(obj.get("replacement"), str) else ""
        if cid == VALUE_ID:
            if obj.get("source_id") != "S044" or obj.get("url") != VALUE_URL:
                add("R14-SOURCE-ID", "S044 + systemd.exec.5 required")
            if "root-dac-correction-r13.md" not in sup or re.search(r"\b97\b", sup) is None:
                add("R14-SUPERSEDES", "r13 MD:97 pointer required")
            missing = value_rep_missing(rep)
            if missing:
                add("R14-VALUE-DOMAIN-PIN", ",".join(missing))
            if DOMAIN_BAD.search(plain(rep)):
                add("R14-VALUE-DOMAIN-RESTORED", "old phrase restored")
        else:
            if obj.get("source_id") != "S045" or obj.get("url") != ATTR_URL:
                add("R14-SOURCE-ID", "S045 + comment endpoint required")
            if "S042" not in sup.upper():
                add("R14-SUPERSEDES", "S042 required")
            missing = attr_rep_missing(rep)
            if missing:
                add("R14-COMMENT-ATTRIBUTION-PIN", ",".join(missing))
            if ATTR_BAD.search(plain(rep)):
                add("R14-COMMENT-ATTRIBUTION-RESTORED", "old attribution restored")
            if re.search(r"nothing was run", rep, re.I):
                add("R14-DISCLAIMER-TRANSFER", "#6629 disclaimer must not transfer")
    if not global_ok:
        valid = {VALUE_ID: False, ATTR_ID: False}
    return out, valid


def source_issues(rows):
    out, row42, row45 = [], rows.get("S042"), rows.get("S045")
    if row42 is None or len(row42) < 11:
        out.append(Finding("R14-SOURCES-IMMUTABLE", SOURCES, "S042 row absent or malformed"))
    else:
        teaches = plain(row42[6]).lower()
        if not ("8047" in row42[1] and "6071740243" in plain(row42[5])
                and "self-described model-generated automated triage" in teaches
                and "supersedes s036" in teaches and "reject" in teaches):
            out.append(Finding("R14-SOURCES-IMMUTABLE", SOURCES, "S042 historical fields changed"))
    if row45 is None or len(row45) < 11:
        out.append(Finding("R14-SOURCES-SUPERSESSION", SOURCES, "S045 row absent or malformed"))
    else:
        teaches, low = plain(row45[6]).lower(), " ".join(row45).lower()
        denial = re.search(r"(?:does not|do not|doesn't|not|no|never|nonexistent|unsupported|incorrect|absent)"
                           r"[^.!?]{0,80}self[- ]descri[bp]|self[- ]descri[bp]\w*[^.!?]{0,60}"
                           r"(?:is|was|remains)\s+(?:absent|unsupported|incorrect|nonexistent)", teaches)
        distinguish = "unverified" in low and ("second opinion" in low or "codex" in low)
        host = re.search(r"(?:reject|unknown|unsupported|not\s+(?:established|proven))[^.!?]{0,80}host[- ]cause|"
                         r"host[- ]cause[^.!?]{0,80}(?:reject|unknown|unsupported|not\s+(?:established|proven))",
                         low)
        if not (re.match(r"supersedes\s+s042\b", teaches, re.I) and row45[3] == "C"
                and row45[7].lower() == "rejected" and "6071740243" in low
                and denial is not None and distinguish and host is not None):
            out.append(Finding("R14-SOURCES-SUPERSESSION", SOURCES, "S045 supersession fields absent"))
    return out


def evaluate(docs):
    findings = []
    for path, value in ((R13_MD, docs.md13), (LESSON, docs.lesson), (SOURCES, docs.sources)):
        if value is None:
            findings.append(Finding("R14-HISTORY-MISSING", path, "preserved history file absent"))
    md13, lesson = docs.md13 or "", docs.lesson or ""
    rows = parse_rows(docs.sources or "")
    if docs.sources is not None:
        findings += source_issues(rows)
    domain_kept = domain_site(md13) is not None
    attr_kept = bool(ATTR_HIST.search(plain(lesson)))
    if docs.md13 is not None and not domain_kept:
        findings.append(Finding("R14-HISTORY-REWRITTEN", R13_MD, "r13 value-domain phrase removed"))
    if docs.lesson is not None and not attr_kept:
        findings.append(Finding("R14-LESSON-HISTORY-REWRITTEN", LESSON, "lesson attribution phrase removed"))
    value_bad, comment_bad = domain_kept, attr_kept or bool(
        rows.get("S042") and len(rows["S042"]) >= 7 and ATTR_BAD.search(plain(rows["S042"][6])))
    vnotice, cnotice = md13_notice_ok(md13), lesson_notice_ok(lesson)
    valid = {}
    if docs.json14 is None:
        findings.append(Finding("R14-JSON-MISSING", R14_JSON, "correction JSON absent"))
    else:
        try:
            j14 = json.loads(docs.json14)
        except json.JSONDecodeError as exc:
            return Result(CANNOT, [Finding("E-R14-JSON-PARSE", R14_JSON, str(exc)[:120])], 0)
        issues, valid = json14_issues(j14)
        findings += issues
    if docs.md14 is None:
        findings.append(Finding("R14-MD-MISSING", R14_MD, "correction MD absent"))
    else:
        findings += md14_issues(docs.md14)
    if not vnotice:
        findings.append(Finding("R14-MD-NOTICE-MISSING", R13_MD, "R14-VALUE-DOMAIN notice absent"))
    if not cnotice:
        findings.append(Finding("R14-LESSON-NOTICE-MISSING", LESSON, "R14-COMMENT-ATTRIBUTION notice absent"))
    if value_bad and not vnotice:
        findings.append(Finding("VALUE_DOMAIN_OVERCLAIM", R13_MD, "documented value set called non-exhaustive"))
    if comment_bad and not cnotice:
        findings.append(Finding("COMMENT_ATTRIBUTION_OVERCLAIM", f"{LESSON};{SOURCES}",
                                "unsupported model-generated self-description active"))
    failed = {f.id for f in findings}
    common = {"R14-MD-MISSING", "R14-MD-HEADING", "R14-MD-OPENERS", "R14-MD-QUALITY",
              "R14-OVERCLAIM", "R14-HISTORY-MISSING"}
    count = int(bool(valid.get(VALUE_ID)) and vnotice and domain_kept
                and not (common | {"R14-MD-VALUE-DOMAIN", "R14-HISTORY-REWRITTEN",
                                   "R14-VALUE-DOMAIN-RESTORED"}).intersection(failed))
    count += int(bool(valid.get(ATTR_ID)) and cnotice and attr_kept
                 and not (common | {"R14-MD-COMMENT-ATTRIBUTION", "R14-SOURCES-SUPERSESSION",
                                    "R14-SOURCES-IMMUTABLE", "R14-LESSON-HISTORY-REWRITTEN",
                                    "R14-COMMENT-ATTRIBUTION-RESTORED"}).intersection(failed))
    return Result(FAIL if findings else PASS, findings, count)


def emit(result, revision):
    status = {PASS: "PASS", FAIL: "FAIL", CANNOT: "CANNOT_EVALUATE"}[result.code]
    payload = {"status": status, "revision": revision, "correction_count": result.count,
               "findings": [{"id": f.id, "site": f.site, "detail": f.detail}
                            for f in sorted(result.findings, key=lambda f: (f.id, f.site, f.detail))]}
    print(json.dumps(payload, sort_keys=True))
    return result.code


def read_tree(repo, path):
    target = repo / path
    try:
        return target.read_bytes().decode("utf-8") if target.is_file() else None
    except (OSError, UnicodeDecodeError) as exc:
        raise Cannot("E-READ-FAILED", path, str(exc)[:120])


def git(repo, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat", "LC_ALL": "C"})
    try:
        return subprocess.run(["git", "--no-pager", "-C", str(repo), *args],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=30)
    except subprocess.TimeoutExpired:
        raise Cannot("E-GIT-TIMEOUT", "git", "git command exceeded 30s")
    except OSError as exc:
        raise Cannot("E-GIT-FAILED", "git", str(exc)[:120])


def read_git(repo, commit, path):
    proc = git(repo, "show", f"{commit}:{path}")
    if proc.returncode == 0:
        try:
            return proc.stdout.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise Cannot("E-READ-FAILED", path, str(exc)[:120])
    error = proc.stderr.decode("utf-8", "replace")
    if re.search(r"does not exist|exists on disk, but not in|not in '", error, re.I):
        return None
    raise Cannot("E-GIT-READ-FAILED", path, error.strip()[:120])


def resolve(repo, rev):
    proc = git(repo, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    if proc.returncode != 0:
        raise Cannot("E-REVISION-INVALID", "revision", "HEAD or hex commit required")
    return proc.stdout.decode("ascii", "replace").strip()


BASELINE_MD13 = ("# r13\n| r12 MD:41-42 | hierarchy text attributed read-only coverage to strict alone | "
                 "among `ProtectSystem=` values, `strict` covers the hierarchy; "
                 "the value set is not exhaustive |\n")
VALUE_NOTICE = ("\n## R14-VALUE-DOMAIN supersession\nR14-VALUE-DOMAIN supersedes "
                "corpus/knowledge/root-dac-correction-r13.md:97. The documented domain is a boolean "
                "argument or full/strict; non-exhaustive applies to unit-side mechanisms.\n")
BASELINE_LESSON = ("| S042 | comment6071740243 |\nBot comments are self-described model-generated "
                   "triage from an API account, not maintainer acceptance.\n")
LESSON_NOTICE = ("\n## Round-14 attribution notice\nR14-COMMENT-ATTRIBUTION supersedes the S042 "
                 "collective claim; S045 corrects the nonexistent self-description. The #8047 comment "
                 "does not self-describe as model-generated automated triage.\n")
BASELINE_SOURCES = (
    "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|\n"
    "| S042 | issue #8047 https://github.com/omacom/omarchy/issues/8047 | community | C | authority | "
    "comment6071740243 | supersedes S036 — REJECTED: self-described model-generated automated triage "
    "by omarchybot | rejected | 2026-10-20 | 90d | — |\n")
S045_ROW = (
    "| S045 | issue #8047 https://api.github.com/repos/omacom/omarchy/issues/comments/6071740243 | "
    "community | C | authority correction | comment6071740243 login omarchybot | supersedes S042 — "
    "REJECTED: the comment does not self-describe as model-generated automated triage; the VM "
    "assertion is unverified, Codex Medium is a second opinion, host cause unsupported | rejected | "
    "2026-10-20 | 90d | corpus/knowledge/source-scope-correction-r14.md |\n")
MD14 = ("source: S044\nverified-at: 2026-10-20\nrecheck: 90d\n"
        "## R14-VALUE-DOMAIN\nS044 r13:97 ProtectSystem= boolean full strict; non-exhaustive mechanism "
        "examples.\n## R14-COMMENT-ATTRIBUTION\nS045 #8047 6071740243 User COLLABORATOR unverified; "
        "Codex Medium second opinion; #6634 maintainer decision; #8047 reporter wait; host cause rejected.\n"
        "## QUALITY check\nBounded conformance only; no semantic theorem.\n")
JSON14 = {"schema": SCHEMA, "corrections": [
    {"id": VALUE_ID, "supersedes": "corpus/knowledge/root-dac-correction-r13.md:97", "source_id": "S044",
     "url": VALUE_URL, "location": "ProtectSystem= paragraph",
     "quote": 'Takes a boolean argument or the special values "full" or "strict".',
     "replacement": "The documented ProtectSystem= value domain is boolean or full and strict; "
                    "non-exhaustive applies to unit-side mechanism examples, not the documented values."},
    {"id": ATTR_ID, "supersedes": "S042", "source_id": "S045", "url": ATTR_URL,
     "location": "comment 6071740243 body", "quote": "I tried this on a stock Omarchy worker VM",
     "replacement": "Comment 6071740243 verified API fields: User and COLLABORATOR login omarchybot. "
                    "The VM assertion is unverified; Codex Medium is a second opinion; the maintainer-"
                    "decision sentence concerns #6634; #8047 waits on an answer. Host-cause use is "
                    "rejected; it does not self-describe as model-generated automated triage."}]}


def clean_docs():
    return DocSet(MD14, json.dumps(JSON14), VALUE_NOTICE + BASELINE_MD13,
                  LESSON_NOTICE + BASELINE_LESSON, BASELINE_SOURCES + S045_ROW)


def selftest():
    base, cases = clean_docs(), []

    def mutant(name, fn, ids, count=1):
        doc = json.loads(json.dumps(JSON14))
        fn(doc["corrections"])
        cases.append((name, base._replace(json14=json.dumps(doc)), FAIL, set(ids), count))

    cases.append(("baseline", DocSet(None, None, BASELINE_MD13, BASELINE_LESSON, BASELINE_SOURCES), FAIL,
                  {"R14-MD-MISSING", "R14-JSON-MISSING", "R14-MD-NOTICE-MISSING",
                   "R14-LESSON-NOTICE-MISSING", "R14-SOURCES-SUPERSESSION",
                   "VALUE_DOMAIN_OVERCLAIM", "COMMENT_ATTRIBUTION_OVERCLAIM"}, 0))
    cases.append(("clean", base, PASS, set(), 2))
    cases.append(("self-description-denial", base._replace(
        sources=base.sources.replace("does not self-describe", "contains no self-description")),
        PASS, set(), 2))
    mutant("restored-domain", lambda c: c[0].__setitem__(
        "replacement", "Among ProtectSystem= values strict covers the hierarchy; the value set is not exhaustive."),
        {"R14-VALUE-DOMAIN-PIN", "R14-VALUE-DOMAIN-RESTORED"})
    mutant("restored-attribution", lambda c: c[1].__setitem__(
        "replacement", "The #8047 comment is self-described model-generated automated triage "
                       "(API type User, not API type Bot and not maintainer acceptance)."),
        {"R14-COMMENT-ATTRIBUTION-PIN", "R14-COMMENT-ATTRIBUTION-RESTORED"})
    cases.append(("missing-notice", base._replace(md13=BASELINE_MD13, lesson=BASELINE_LESSON), FAIL,
                  {"VALUE_DOMAIN_OVERCLAIM", "COMMENT_ATTRIBUTION_OVERCLAIM",
                   "R14-MD-NOTICE-MISSING", "R14-LESSON-NOTICE-MISSING"}, 0))
    cases.append(("malformed-json", base._replace(json14="{"), CANNOT, {"E-R14-JSON-PARSE"}, 0))
    mutant("oversized-quote", lambda c: c[0].__setitem__(
        "quote", " ".join(f"word{i}" for i in range(26))), {"R14-QUOTE-WORDS"})
    cases.append(("sources-immutable", base._replace(sources=BASELINE_SOURCES.replace(
        "self-described model-generated automated triage", "maintainer confirmation") + S045_ROW),
        FAIL, {"R14-SOURCES-IMMUTABLE"}, 1))
    cases.append(("wrong-id", base._replace(json14=json.dumps({"schema": SCHEMA, "corrections": [
        dict(JSON14["corrections"][0], id="R14-OTHER"), JSON14["corrections"][1]]})),
        FAIL, {"R14-CORRECTION-ID"}, 1))
    cases.append(("top-level-array", base._replace(json14="[]"), FAIL,
                  {"R14-JSON-SCHEMA", "R14-CORRECTION-COUNT", "R14-CORRECTION-ID"}, 0))
    cases.append(("recheck-host-command", base._replace(
        md14=MD14.replace("recheck: 90d", "recheck: snapper list-configs")),
        FAIL, {"R14-MD-RECHECK"}, 2))
    cases.append(("history-domain-rewritten", base._replace(
        md13=VALUE_NOTICE + BASELINE_MD13.replace("the value set is not exhaustive", "the domain is closed")),
        FAIL, {"R14-HISTORY-REWRITTEN", "R14-MD-NOTICE-MISSING"}, 1))
    cases.append(("history-lesson-rewritten", base._replace(
        lesson=LESSON_NOTICE + BASELINE_LESSON.replace("self-described model-generated triage", "model triage")),
        FAIL, {"R14-LESSON-HISTORY-REWRITTEN", "R14-LESSON-NOTICE-MISSING",
               "COMMENT_ATTRIBUTION_OVERCLAIM"}, 1))
    cases.append(("notice-after-site", base._replace(md13=BASELINE_MD13 + VALUE_NOTICE),
                  FAIL, {"R14-MD-NOTICE-MISSING", "VALUE_DOMAIN_OVERCLAIM"}, 1))
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
    if failures:
        print(f"CHECK_SOURCE_SCOPE_CORRECTION_SELFTEST: FAIL ({len(cases)} cases, {passed} passed)")
        print("\n".join("  " + item for item in failures))
        return FAIL
    print(f"CHECK_SOURCE_SCOPE_CORRECTION_SELFTEST: PASS ({len(cases)} cases, {passed} passed, 0 failed)")
    return PASS


def main(argv=None):
    parser = argparse.ArgumentParser(description="Narrow read-only round-14 source-scope correction gate.",
                                     exit_on_error=False)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--revision", metavar="REV", help="HEAD or a 4-64 hex commit")
    group.add_argument("--selftest", action="store_true", help="in-memory fixture suite")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        if not exc.code:
            return 0
        return emit(Result(CANNOT, [Finding("E-CLI", "cli", "invalid arguments")], 0), "worktree")
    except argparse.ArgumentError:
        return emit(Result(CANNOT, [Finding("E-CLI", "cli", "invalid arguments")], 0), "worktree")
    if args.selftest:
        return selftest()
    revision = "worktree"
    try:
        if args.revision:
            if not REV.fullmatch(args.revision):
                raise Cannot("E-REVISION-INVALID", "revision", "HEAD or hex commit required")
            revision = resolve(ROOT, args.revision)
            docs = DocSet(*[read_git(ROOT, revision, path) for path in FILES])
        else:
            docs = DocSet(*[read_tree(ROOT, path) for path in FILES])
    except Cannot as exc:
        return emit(Result(CANNOT, [Finding(exc.fid, exc.site, exc.detail)], 0), revision)
    except Exception as exc:  # no traceback exit 1: unreadable/invalid input is CANNOT
        return emit(Result(CANNOT, [Finding("E-INTERNAL", "gate", str(exc)[:120])], 0), revision)
    try:
        result = evaluate(docs)
    except Exception as exc:
        return emit(Result(CANNOT, [Finding("E-INTERNAL", "gate", str(exc)[:120])], 0), revision)
    return emit(result, revision)


if __name__ == "__main__":
    sys.exit(main())
