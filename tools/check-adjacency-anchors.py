#!/usr/bin/env python3
"""Read-only verifier for round-19 portable adjacency anchors."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import re
import subprocess
import sys
sys.dont_write_bytecode = True
import tempfile
from collections import Counter, namedtuple
from pathlib import Path

from _revision import E_GIT, RevisionError, bind, clean_env

PASS, FAIL, CANNOT = 0, 1, 2
BASELINE = "452a054677f6b18284917d7c08c45361f91c25ac"
SCHEMA = "tsukuroi-adjacency-anchors-r19-v1"
CENSUS_SCHEMA = "tsukuroi-adjacency-pointers-r19-v1"
DEFAULT_REGISTRY = "corpus/knowledge/adjacency-anchors-r19.json"
DEFAULT_CENSUS = ".ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json"
DEFAULT_KNOWLEDGE = "corpus/knowledge/adjacency-anchors-r19.md"
PROVINCE_SECTION = "## Adjacent — portable ownership anchors (round 19)"
DEFAULT_SIBLINGS_ROOT = "/home/vgpnk/Projects/shokunin"
ROOT = Path(__file__).resolve().parents[1]
OUTBOUND_FIELDS = frozenset((
    "id", "province_pointer", "sibling", "sibling_path", "sibling_commit",
    "sibling_blob_sha256", "snapshot", "heading", "quote", "quote_line",
    "proposition"))
INBOUND_FIELDS = frozenset((
    "id", "sibling", "sibling_path", "sibling_line", "pointer", "target_path",
    "target_ranges", "scope", "classification", "evidence_quote", "found_line",
    "relied_on", "note"))
ID_OUT = re.compile(r"^OUT-[0-9]{3}$")
ID_IN = re.compile(r"^IN-[0-9]{3}$")
HEX40 = re.compile(r"^[0-9a-fA-F]{40}$")
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")
ATX_RE = re.compile(r"^ {0,3}(#{1,6})[\t ]+.+?(?:[\t ]+#+[\t ]*)?$")
OWNERSHIP_HEADING = "## R20 ownership clarification — OUT-009"
OWNERSHIP_CORRECTION = (
    "R20-OUT009: OUT-009 is Revenger's sibling declaration of reverse engineering of "
    "shipped artifacts — native binaries, managed assemblies, Electron/JavaScript packages, "
    "Android APKs, archives, firmware, browser/Electron runtime evidence. It is not a tsukuroi "
    "grant of ownership. Kaidoku/Revenger arbitration remains unresolved; ask the protocol "
    "integrator before an internals handoff. No configuration, service, package, boot or "
    "sibling-file write is authorized.")
OWNERSHIP_CORRECTION_FILE = ".ufo/waves/round-20/ownership-correction.txt"
OWNERSHIP_CORRECTION_TEXT_SHA256 = "23289c7a8fa558c0249ff56b53ccddf9dcae522ef6dcd3064dc3ce607453fc2a"
OWNERSHIP_EXPLANATION = (
    "This explicitly supersedes only the OUT-009 proposition's unqualified “Revenger owns” "
    "wording and its broad “packages” paraphrase. The original quoted declaration and pinned "
    "bytes remain historical evidence; “Electron/JavaScript packages” is the precise package "
    "scope, not arbitrary packages. ADJ-06's unresolved recipient and Frontier arbitration "
    "remain controlling. The other nine locators and all prepared/acknowledged handoff states "
    "are unchanged. Source: the pinned Revenger snapshot in "
    "`corpus/knowledge/adjacency-anchors-r19.json`; recheck: "
    "`python3 tools/check-adjacency-anchors.py --revision <REV> --ownership-corrections`.")
OWNERSHIP_SECTION_LINES = (
    OWNERSHIP_HEADING, "", OWNERSHIP_CORRECTION, "", OWNERSHIP_EXPLANATION)
OWNERSHIP_ARBITRATION_LINES = (
    "- Kaidoku and revenger both declare shipped-artifact RE. The integrator must",
    "  arbitrate this shared scope; tsukuroi neither picks an owner nor absorbs it.")
OWNERSHIP_BASELINE = "0cbc34dd6b20896085a8fb07943e3ea4027d8472"
OWNERSHIP_BASELINE_FIXTURE = (
    "# Fixture Province\n"
    "## Frontier\n"
    f"{OWNERSHIP_ARBITRATION_LINES[0]}\n"
    f"{OWNERSHIP_ARBITRATION_LINES[1]}\n"
    "\n"
    "## Adjacent — portable ownership anchors (round 19)\n"
    "| OUT-008 | ADJ-06 | fixture |\n"
    "| OUT-009 | ADJ-06 | fixture |\n"
)

OWNERSHIP_PIN = {
    "id": "OUT-009",
    "province_pointer": "../revenger-shokunin/PROVINCE.md:3-7,19-25",
    "sibling": "revenger",
    "sibling_path": "PROVINCE.md",
    "sibling_commit": "cf02419276e5dd8aafb6fe09d4e9aaa6bcb78c97",
    "sibling_blob_sha256": "63acc3d033869f93f3e13da79e35023d86baa60b3f1d3b52861b019183b4b19f",
    "snapshot": ".ufo/waves/round-19/l1-capture/siblings/revenger/cf02419276e5/PROVINCE.md",
    "heading": "# revenger province",
    "quote": "Owns: reverse engineering of shipped artifacts",
    "quote_line": 3,
    "proposition": ("Revenger owns shipped-artifact reverse engineering (binaries, packages, "
                    "APKs) with an observation/inference/unknown evidence ledger; tsukuroi tracks state only."),
}
OWNERSHIP_CENSUS_PIN = {
    "id": "OUT-009",
    "pointer": "../revenger-shokunin/PROVINCE.md:3-7,19-25",
    "sibling": "revenger",
    "sibling_path": "PROVINCE.md",
    "ranges": [[3, 7], [19, 25]],
    "sibling_commit": "cf02419276e5dd8aafb6fe09d4e9aaa6bcb78c97",
    "sibling_blob_sha256": "63acc3d033869f93f3e13da79e35023d86baa60b3f1d3b52861b019183b4b19f",
    "snapshot": ".ufo/waves/round-19/l1-capture/siblings/revenger/cf02419276e5/PROVINCE.md",
}
OWNERSHIP_SNAPSHOT_FIXTURE = (
    "# revenger province\n"
    "\n"
    "Owns: reverse engineering of shipped artifacts — native binaries, managed\n"
    "assemblies, Electron/JavaScript packages, Android APKs, archives, firmware,\n"
    "browser/Electron runtime evidence — using the REA skill and its toolset,\n"
    "with an evidence-ledger discipline: every conclusion separates observation,\n"
    "inference, and unknown, and cites Evidence IDs.\n"
    "\n"
    "Sources (read-only):\n"
    "- REA skill: ~/.agents/skills/reverse-engineer-anything/ (SKILL.md +\n"
    "  references/; instructions only — server registration and engines are the\n"
    "  lane's readiness domain)\n"
    "- REA package: `rea` CLI when installed, else `npx -y rea-agents@6.4.0`\n"
    "  within authorized scope (setup never installs unrelated software)\n"
    "- Host engines as they become available (caller-supplied per REA: Ghidra,\n"
    "  IDA, JADX, Binwalk/Unblob, pwntools) — census in corpus/knowledge/seed.md\n"
    "- Demand context: ~/Projects/gamez/research/ (incl. decomp/recomp interest)\n"
    "\n"
    "Refuses: live-target execution beyond the declared target and lifecycle\n"
    "(REA runtime discipline); DRM circumvention or piracy facilitation;\n"
    "publishing reversed code; asset rights claims (art-east-asian-design);\n"
    "harness/evidence auditing (harness-integrity, gate-evidence, rlm-dispatch);\n"
    "game mechanics verification (game-dev-2d); narrative canon (lore).\n"
    "\n"
    "Writes only this `revenger-shokunin/` repository under the current interactive\n"
    "dispatch. Reports, continuation evidence and L0 requests stay in its own\n"
    "`.ufo/`; the fleet integrator alone copies them to shared ledgers/report paths.\n"
    "Domain source checkouts, shared fleet state and sibling repositories remain\n"
    "read-only. No push, global routing changes or substrate/package remediation.\n"
    "Historical `.shokunin/revenger/**` paths identify imported evidence, not the\n"
    "current write scope. The r55–r57 replay repair checks this domain's saved\n"
    "PE evidence ledger; it does not take ownership of generic harness gates.\n")

def _ownership_correction_source_matches():
    path = Path(__file__).resolve().parents[1] / OWNERSHIP_CORRECTION_FILE
    if path.is_symlink() or not path.is_file():
        return False
    try:
        data = path.read_bytes()
    except OSError:
        return False
    expected = (OWNERSHIP_CORRECTION + "\n").encode("utf-8")
    return (data == expected
            and hashlib.sha256(data).hexdigest() == OWNERSHIP_CORRECTION_TEXT_SHA256)

def _ownership_correction(province_text, registry_doc, census_doc,
                          registry_revision, reader, revision=None):
    """Count only the exact R20 clarification over the original pinned declaration."""
    def invalid(detail):
        return 0, [_finding("OWNERSHIP-CORRECTION-INVALID", "OUT-009", detail)]
    if not _ownership_correction_source_matches():
        return invalid("the checked-in correction text differs from its fixed digest")
    if revision is not None and registry_revision != revision:
        return invalid("registry evidence must come from the corrected PROVINCE revision")
    outbound = registry_doc.get("outbound") if isinstance(registry_doc, dict) else None
    records = [item for item in outbound if isinstance(item, dict)
               and item.get("id") == "OUT-009"] if isinstance(outbound, list) else []
    if len(records) != 1:
        return invalid("OUT-009 must remain a unique registry record")
    record = records[0]
    if any(record.get(key) != value for key, value in OWNERSHIP_PIN.items()):
        return invalid("OUT-009 no longer matches its original pinned Revenger declaration")
    census_outbound = census_doc.get("outbound") if isinstance(census_doc, dict) else None
    census_records = [item for item in census_outbound if isinstance(item, dict)
                      and item.get("id") == "OUT-009"] if isinstance(census_outbound, list) else []
    if (len(census_records) != 1
            or any(census_records[0].get(key) != value
                   for key, value in OWNERSHIP_CENSUS_PIN.items())):
        return invalid("OUT-009 pointer census no longer matches the pinned sibling source")

    baseline = reader.read(OWNERSHIP_BASELINE, "PROVINCE.md")
    if baseline.issue is not None or baseline.data is None:
        raise RevisionError("E-OWNERSHIP-BASELINE", "PROVINCE.md",
                            "R20 baseline PROVINCE.md is absent or unsafe")
    current_data = province_text.encode("utf-8")
    baseline_data = baseline.data
    lines = province_text.splitlines()
    headings = [index for index, line in enumerate(lines) if line == OWNERSHIP_HEADING]
    if not headings:
        if current_data == baseline_data:
            return 0, [_finding("OWNERSHIP-CORRECTION-MISSING", "OUT-009",
                                "the exact R20 ownership clarification is absent")]
        return invalid("PROVINCE.md differs from the R20 baseline without the exact correction")
    if len(headings) != 1:
        return invalid("the R20 ownership clarification heading must be unique")
    if not current_data.startswith(baseline_data):
        return invalid("PROVINCE.md no longer preserves the exact R20 baseline prefix")
    expected_suffix = ("\n" + "\n".join(OWNERSHIP_SECTION_LINES) + "\n").encode("utf-8")
    if current_data[len(baseline_data):] != expected_suffix:
        return invalid("the OUT-009 clarification is not an exact append after the baseline")


    loaded = reader.read(registry_revision, OWNERSHIP_PIN["snapshot"])
    if (loaded.issue is not None or loaded.data is None
            or hashlib.sha256(loaded.data).hexdigest() != OWNERSHIP_PIN["sibling_blob_sha256"]):
        return invalid("the original Revenger snapshot is absent or its pinned digest differs")
    try:
        source_lines = loaded.data.decode("utf-8", "strict").splitlines()
    except UnicodeDecodeError:
        return invalid("the pinned Revenger snapshot is not UTF-8 text")
    quote_line = OWNERSHIP_PIN["quote_line"]
    if (not _heading_section_contains(source_lines, OWNERSHIP_PIN["heading"], quote_line)
            or quote_line > len(source_lines)
            or OWNERSHIP_PIN["quote"] not in source_lines[quote_line - 1]):
        return invalid("the pinned Revenger heading or exact quote is absent")

    if (any(line not in lines for line in OWNERSHIP_ARBITRATION_LINES)
            or "| OUT-008 | ADJ-06 |" not in province_text
            or "| OUT-009 | ADJ-06 |" not in province_text):
        return invalid("the original ADJ-06 arbitration context was removed or changed")
    return 1, []


Finding = namedtuple("Finding", "id site detail")
Loaded = namedtuple("Loaded", "data issue")
Result = namedtuple("Result", "code findings counts")


class DuplicateJSONKey(ValueError):
    pass


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJSONKey(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _finding(fid, site, detail):
    return Finding(str(fid), str(site), str(detail)[:240])


def _dedupe(findings):
    seen, result = set(), []
    for item in findings:
        key = (item.id, item.site, item.detail)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def _safe_path(path):
    """Accept a repository-relative path without traversal or git path tricks."""
    if not isinstance(path, str) or not path or path.startswith("/") or "\\" in path or "\0" in path:
        return False
    return all(part not in ("", ".", "..") for part in path.split("/"))


def _safe_sibling(name):
    return isinstance(name, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name) is not None


def _git(root, *args):
    try:
        return subprocess.run(["git", "--no-pager", "-C", str(root), *args],
                              stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, env=clean_env(), timeout=60)
    except subprocess.TimeoutExpired as exc:
        raise RevisionError(E_GIT, "git", f"git {args[0]} exceeded 60s") from exc
    except OSError as exc:
        raise RevisionError(E_GIT, "git", str(exc)[:120]) from exc


def _git_detail(proc):
    return proc.stderr.decode("utf-8", "replace").strip()[:120] or f"exit={proc.returncode}"


class GitReader:
    """Read regular committed blobs only; never follow working-tree symlinks."""

    def __init__(self, root):
        self.root = Path(root)
        self.cache = {}

    def read(self, revision, path):
        key = (revision, path)
        if key in self.cache:
            return self.cache[key]
        if not _safe_path(path):
            loaded = Loaded(None, "unsafe")
        else:
            listing = _git(self.root, "ls-tree", "-z", "--full-tree", revision, "--", path)
            if listing.returncode:
                raise RevisionError(E_GIT, path, "git ls-tree failed: " + _git_detail(listing))
            entries = []
            for item in listing.stdout.split(b"\0"):
                if not item:
                    continue
                try:
                    metadata, name = item.split(b"\t", 1)
                    mode, kind, _oid = metadata.split(b" ", 2)
                except ValueError as exc:
                    raise RevisionError(E_GIT, path, "git ls-tree returned malformed entry") from exc
                if name.decode("utf-8", "replace") == path:
                    entries.append((mode, kind))
            if not entries:
                loaded = Loaded(None, "missing")
            elif (len(entries) != 1 or entries[0][0] not in (b"100644", b"100755")
                  or entries[0][1] != b"blob"):
                loaded = Loaded(None, "unsafe")
            else:
                shown = _git(self.root, "show", f"{revision}:{path}")
                if shown.returncode:
                    raise RevisionError(E_GIT, path, "git show failed: " + _git_detail(shown))
                loaded = Loaded(shown.stdout, None)
        self.cache[key] = loaded
        return loaded



def _text(reader, revision, path, missing=""):
    loaded = reader.read(revision, path)
    if loaded.issue == "missing":
        return missing
    if loaded.issue is not None or loaded.data is None:
        raise RevisionError("E-OBJECT-UNSAFE", path,
                            "committed path is not a readable regular blob")
    try:
        return loaded.data.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise RevisionError("E-OBJECT-UTF8", path, "committed text is not UTF-8") from exc


def _json_document(data, site):
    try:
        return json.loads(data.decode("utf-8", "strict"), object_pairs_hook=_unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError, DuplicateJSONKey, ValueError) as exc:
        raise RevisionError("E-REGISTRY-PARSE", site, str(exc)[:120]) from exc


def _ranges_valid(ranges):
    if not isinstance(ranges, list) or not ranges:
        return False
    for item in ranges:
        if (not isinstance(item, list) or len(item) != 2
                or any(type(value) is not int or value < 1 for value in item)
                or item[0] > item[1]):
            return False
    return True


def _line_in_ranges(line, ranges):
    return any(start <= line <= end for start, end in ranges)


def _word_count(text):
    return len(text.split())


def _heading_section_contains(lines, heading, quote_line):
    """Whether heading precedes quote_line before a same/higher ATX heading."""
    if type(quote_line) is not int or quote_line < 1 or quote_line > len(lines):
        return False
    positions = [index for index, line in enumerate(lines) if line == heading]
    for start in positions:
        match = ATX_RE.fullmatch(lines[start])
        if match is None:
            continue
        level = len(match.group(1))
        quote_index = quote_line - 1
        if quote_index <= start:
            continue
        ended = False
        for pos in range(start + 1, quote_index + 1):
            found = ATX_RE.fullmatch(lines[pos])
            if found and len(found.group(1)) <= level:
                ended = True
                break
        if not ended:
            return True
    return False


def _empty_counts():
    return {
        "outbound_total": 0,
        "outbound_portable": 0,
        "inbound_total": 0,
        "inbound_classified": 0,
        "inbound_by_class": {"RESOLVES": 0, "DRIFTED": 0, "UNRESOLVABLE": 0},
        "inbound_by_scope": {"operative": 0, "historical": 0},
        "live_object_checked": 0,
        "live_object_match": 0,
    }






def _result(code, findings, counts=None):
    return Result(code, _dedupe(findings), counts if counts is not None else _empty_counts())


def _outbound_publication(lines, section_heading, record):
    """An anchor is published only when the section carries all four portable fields.

    id+quote identify the row; id+commit and id+sha256 bind the published
    locator to the pinned bytes; the heading must appear in the published
    region too. Round-19 falsify seats (FxProvinceSection, FxOut001/002/004/
    005/007/008/009/010) showed the id+quote-only check passed a table with no
    digest and no full commit.
    """
    anchor_id = record.get("id")
    quote = record.get("quote")
    if not isinstance(anchor_id, str) or not isinstance(quote, str):
        return False
    section_positions = [i for i, line in enumerate(lines) if line == section_heading]
    commit = record.get("sibling_commit")
    digest = record.get("sibling_blob_sha256")
    heading = record.get("heading")
    for start in section_positions:
        region = lines[start + 1:]
        if not any(anchor_id in line and quote in line for line in region):
            continue
        if not (isinstance(commit, str) and commit
                and any(anchor_id in line and commit in line for line in region)):
            continue
        if not (isinstance(digest, str) and digest
                and any(anchor_id in line and digest in line for line in region)):
            continue
        if not (isinstance(heading, str) and heading
                and any(heading in line for line in region)):
            continue
        return True
    return False


def _inbound_identity(record, census):
    """Check pointer provenance fields and the draft's derived scope."""
    equal_fields = ("sibling", "sibling_path", "sibling_line", "pointer",
                    "target_path", "target_ranges")
    mismatches = [field for field in equal_fields if record.get(field) != census.get(field)]
    expected_scope = "historical" if str(census.get("sibling_path", "")).startswith(".ufo/") else "operative"
    if record.get("scope") != expected_scope:
        mismatches.append("scope")
    return mismatches


def _live_object_hash(root, record):
    sibling = record.get("sibling")
    path = record.get("sibling_path")
    commit = record.get("sibling_commit")
    if not (_safe_sibling(sibling) and _safe_path(path)
            and isinstance(commit, str) and HEX40.fullmatch(commit)):
        return None
    repo = Path(root) / f"{sibling}-shokunin"
    try:
        proc = subprocess.run(["git", "--no-pager", "-C", str(repo), "show",
                               f"{commit}:{path}"],
                              stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, env=clean_env(), timeout=60)
    except (subprocess.TimeoutExpired, OSError):
        return None
    if proc.returncode:
        return None
    return hashlib.sha256(proc.stdout).hexdigest()


def evaluate(registry_bytes, revision, registry_revision, reader, siblings_root=None,
             registry_path=DEFAULT_REGISTRY, ownership_corrections=False):
    """Evaluate a parsed registry and the immutable lane objects it names."""
    counts = _empty_counts()
    doc = _json_document(registry_bytes, registry_path)
    top_fields = frozenset(("schema", "baseline", "province_section", "knowledge_entry",
                            "pointer_census", "outbound", "inbound"))
    if (not isinstance(doc, dict) or set(doc) != top_fields
            or doc.get("schema") != SCHEMA or doc.get("baseline") != BASELINE
            or doc.get("province_section") != PROVINCE_SECTION
            or doc.get("knowledge_entry") != DEFAULT_KNOWLEDGE
            or doc.get("pointer_census") != DEFAULT_CENSUS
            or not isinstance(doc.get("outbound"), list)
            or not isinstance(doc.get("inbound"), list)):
        raise RevisionError("E-REGISTRY-SCHEMA", registry_path,
                            "registry must use the exact round-19 schema, baseline and paths")

    census_bytes = reader.read(registry_revision, doc["pointer_census"])
    if census_bytes.issue == "missing":
        raise RevisionError("E-CENSUS-MISSING", doc["pointer_census"],
                            "pointer census is absent at the registry revision")
    if census_bytes.issue is not None or census_bytes.data is None:
        raise RevisionError("E-CENSUS-UNSAFE", doc["pointer_census"],
                            "pointer census is not a regular committed file")
    census_doc = _json_document(census_bytes.data, doc["pointer_census"])
    if (not isinstance(census_doc, dict) or census_doc.get("schema") != CENSUS_SCHEMA
            or not isinstance(census_doc.get("outbound"), list)
            or not isinstance(census_doc.get("inbound"), list)):
        raise RevisionError("E-CENSUS-SCHEMA", doc["pointer_census"],
                            "pointer census must contain round-19 outbound and inbound arrays")

    province_text = _text(reader, revision, "PROVINCE.md")
    knowledge_text = _text(reader, revision, doc["knowledge_entry"])
    province_lines = province_text.splitlines()
    findings = []

    # A census entry is the captured source list: prevent silently dropping an
    # ownership pointer from the gate's outbound coverage.
    census_outbound = {}
    for index, item in enumerate(census_doc["outbound"]):
        site = f"{doc['pointer_census']}:outbound[{index}]"
        if (not isinstance(item, dict) or not isinstance(item.get("id"), str)
                or not ID_OUT.fullmatch(item["id"])
                or not isinstance(item.get("pointer"), str) or not item["pointer"]):
            raise RevisionError("E-CENSUS-SCHEMA", site, "outbound census record lacks id or pointer")
        if item["id"] in census_outbound:
            raise RevisionError("E-CENSUS-SCHEMA", site, f"duplicate census id {item['id']}")
        census_outbound[item["id"]] = item

    inbound_census = {}
    for index, item in enumerate(census_doc["inbound"]):
        site = f"{doc['pointer_census']}:inbound[{index}]"
        required = (isinstance(item, dict) and isinstance(item.get("id"), str)
                    and ID_IN.fullmatch(item["id"])
                    and isinstance(item.get("sibling"), str)
                    and isinstance(item.get("sibling_path"), str)
                    and _safe_path(item.get("sibling_path"))
                    and type(item.get("sibling_line")) is int and item["sibling_line"] > 0
                    and isinstance(item.get("pointer"), str) and bool(item["pointer"])
                    and isinstance(item.get("target_path"), str)
                    and _safe_path(item.get("target_path"))
                    and _ranges_valid(item.get("target_ranges")))
        if not required:
            raise RevisionError("E-CENSUS-SCHEMA", site,
                                "inbound census record lacks valid pointer/target fields")
        if item["id"] in inbound_census:
            raise RevisionError("E-CENSUS-SCHEMA", site, f"duplicate census id {item['id']}")
        inbound_census[item["id"]] = item

    counts["outbound_total"] = len(doc["outbound"])
    counts["inbound_total"] = len(inbound_census)
    outbound_seen = Counter()
    portable_ids = set()

    for index, record in enumerate(doc["outbound"]):
        site = f"{registry_path}:outbound[{index}]"
        if not isinstance(record, dict) or set(record) != OUTBOUND_FIELDS:
            findings.append(_finding("OUTBOUND-FIELDS", site,
                                     "record must have exactly the declared outbound keys"))
            continue
        anchor_id = record["id"]
        valid = True
        if not isinstance(anchor_id, str) or not ID_OUT.fullmatch(anchor_id):
            findings.append(_finding("OUTBOUND-ID", site, "id must be OUT-NNN"))
            valid = False
        else:
            outbound_seen[anchor_id] += 1
            if outbound_seen[anchor_id] > 1:
                portable_ids.discard(anchor_id)
                findings.append(_finding("OUTBOUND-DUPLICATE", site,
                                         f"duplicate outbound id {anchor_id}"))
                valid = False
        fields_ok = (
            isinstance(record["province_pointer"], str) and bool(record["province_pointer"])
            and _safe_sibling(record["sibling"])
            and _safe_path(record["sibling_path"])
            and isinstance(record["sibling_commit"], str) and HEX40.fullmatch(record["sibling_commit"])
            and isinstance(record["sibling_blob_sha256"], str) and HEX64.fullmatch(record["sibling_blob_sha256"])
            and _safe_path(record["snapshot"])
            and isinstance(record["heading"], str) and bool(record["heading"])
            and isinstance(record["quote"], str) and bool(record["quote"]) and "\n" not in record["quote"]
            and type(record["quote_line"]) is int and record["quote_line"] > 0
            and isinstance(record["proposition"], str) and bool(record["proposition"]))
        if not fields_ok:
            findings.append(_finding("OUTBOUND-FIELDS", site,
                                     "outbound values must be nonempty and use safe paths/pins"))
            valid = False
        if isinstance(record["proposition"], str) and _word_count(record["proposition"]) > 25:
            findings.append(_finding("OUTBOUND-PROPOSITION-TOO-LONG", site,
                                     "proposition exceeds the 25-word maximum"))
            valid = False
        census_item = census_outbound.get(anchor_id) if isinstance(anchor_id, str) else None
        if census_item is None:
            findings.append(_finding("OUTBOUND-CENSUS-UNKNOWN", site,
                                     f"{anchor_id!r} is absent from the outbound pointer census"))
            valid = False
        elif record["province_pointer"] != census_item["pointer"]:
            findings.append(_finding("OUTBOUND-POINTER-MISMATCH", site,
                                     "province_pointer differs from the captured pointer census"))
            valid = False

        snapshot_text = None
        snapshot = reader.read(registry_revision, record["snapshot"]) if _safe_path(record["snapshot"]) else Loaded(None, "unsafe")
        if snapshot.issue == "missing":
            findings.append(_finding("ANCHOR-SNAPSHOT-TAMPERED", site,
                                     "committed sibling snapshot is missing at the registry revision"))
            valid = False
        elif snapshot.issue is not None or snapshot.data is None:
            raise RevisionError("E-SNAPSHOT-UNSAFE", record["snapshot"],
                                "sibling snapshot is not a regular committed file")
        else:
            digest = hashlib.sha256(snapshot.data).hexdigest()
            if digest != record["sibling_blob_sha256"]:
                findings.append(_finding("ANCHOR-SNAPSHOT-TAMPERED", site,
                                         f"snapshot sha256 {digest} differs from pinned sibling_blob_sha256"))
                valid = False
            try:
                snapshot_text = snapshot.data.decode("utf-8", "strict")
            except UnicodeDecodeError as exc:
                raise RevisionError("E-SNAPSHOT-UTF8", record["snapshot"],
                                    "sibling snapshot is not UTF-8 text") from exc

        if snapshot_text is not None:
            snapshot_lines = snapshot_text.splitlines()
            heading_ok = (isinstance(record["heading"], str)
                          and _heading_section_contains(snapshot_lines, record["heading"],
                                                        record["quote_line"]))
            if not heading_ok:
                findings.append(_finding("ANCHOR-HEADING-MISSING", site,
                                         "heading is absent or does not contain quote_line in its section"))
                valid = False
            quote = record["quote"]
            quote_line = record["quote_line"]
            exact_quote = (isinstance(quote, str) and type(quote_line) is int
                           and 1 <= quote_line <= len(snapshot_lines)
                           and quote in snapshot_lines[quote_line - 1])
            if not exact_quote:
                findings.append(_finding("ANCHOR-QUOTE-MISSING", site,
                                         "quote is not an exact substring of the cited snapshot line"))
                valid = False
            if isinstance(quote, str) and _word_count(quote) > 25:
                findings.append(_finding("ANCHOR-QUOTE-TOO-LONG", site,
                                         f"quote has {_word_count(quote)} words; maximum is 25"))
                valid = False

        pointer_present = (isinstance(record["province_pointer"], str)
                           and record["province_pointer"] in province_text)
        if not pointer_present:
            findings.append(_finding("ANCHOR-POINTER-MISSING", site,
                                     "province_pointer does not appear in PROVINCE.md at --revision"))
            valid = False
        published = (isinstance(anchor_id, str) and isinstance(record["quote"], str)
                     and _outbound_publication(province_lines, doc["province_section"],
                                               record))
        if not published:
            findings.append(_finding("ANCHOR-UNPUBLISHED", site,
                                     "published section lacks the anchor's id+quote, id+full commit, "
                                     "id+blob sha256, or the heading"))
            valid = False

        if siblings_root is not None:
            live_digest = _live_object_hash(siblings_root, record)
            if live_digest is not None:
                counts["live_object_checked"] += 1
                if live_digest == record["sibling_blob_sha256"]:
                    counts["live_object_match"] += 1

        if valid:
            portable_ids.add(anchor_id)

    for anchor_id in census_outbound:
        if outbound_seen[anchor_id] == 0:
            findings.append(_finding("OUTBOUND-CENSUS-INCOMPLETE", doc["pointer_census"],
                                     f"no portable anchor record for census id {anchor_id}"))
    counts["outbound_portable"] = len(portable_ids)

    inbound_by_id = Counter()
    for record in doc["inbound"]:
        if isinstance(record, dict) and isinstance(record.get("id"), str):
            inbound_by_id[record["id"]] += 1
    for inbound_id, count in inbound_by_id.items():
        if count > 1:
            findings.append(_finding("INBOUND-DUPLICATE", f"{registry_path}:inbound:{inbound_id}",
                                     f"inbound id occurs {count} times"))
    for inbound_id in inbound_census:
        if inbound_by_id[inbound_id] == 0:
            findings.append(_finding("CENSUS-INCOMPLETE", doc["pointer_census"],
                                     f"no inbound classification for census id {inbound_id}"))
    for inbound_id in inbound_by_id:
        if inbound_id not in inbound_census:
            findings.append(_finding("INBOUND-CENSUS-UNKNOWN", f"{registry_path}:inbound:{inbound_id}",
                                     "inbound id is absent from the pointer census"))

    classifications = {"RESOLVES", "DRIFTED", "UNRESOLVABLE"}
    scope_counts = Counter()
    class_counts = Counter()
    target_texts = {}
    for index, record in enumerate(doc["inbound"]):
        site = f"{registry_path}:inbound[{index}]"
        if not isinstance(record, dict) or set(record) != INBOUND_FIELDS:
            findings.append(_finding("INBOUND-FIELDS", site,
                                     "record must have exactly the declared inbound keys"))
            continue
        inbound_id = record["id"]
        if not isinstance(inbound_id, str) or not ID_IN.fullmatch(inbound_id):
            findings.append(_finding("INBOUND-FIELDS", site, "id must be IN-NNN"))
            continue
        if (not isinstance(record["evidence_quote"], str)
                or "\n" in record["evidence_quote"]
                or type(record["found_line"]) is not int or record["found_line"] < 0
                or not isinstance(record["classification"], str)
                or record["classification"] not in classifications
                or record["scope"] not in ("operative", "historical")
                or not isinstance(record["relied_on"], str)
                or not isinstance(record["note"], str)):
            findings.append(_finding("INBOUND-FIELDS", site,
                                     "classification, scope, quote, found_line or notes are malformed"))
            continue
        census_item = inbound_census.get(inbound_id)
        consistent = True
        if census_item is None:
            consistent = False
        else:
            mismatches = _inbound_identity(record, census_item)
            if mismatches:
                findings.append(_finding("INBOUND-POINTER-MISMATCH", site,
                                         "census fields differ: " + ", ".join(mismatches)))
                consistent = False

        quote = record["evidence_quote"]
        found_line = record["found_line"]
        classification_ok = False
        limits_ok = True
        if quote and _word_count(quote) > 25:
            findings.append(_finding("INBOUND-QUOTE-TOO-LONG", site,
                                     f"evidence_quote has {_word_count(quote)} words; maximum is 25"))
            limits_ok = False
        if record["relied_on"] and _word_count(record["relied_on"]) > 20:
            findings.append(_finding("INBOUND-RELIED-ON-TOO-LONG", site,
                                     "relied_on exceeds the 20-word maximum"))
            limits_ok = False
        if census_item is not None and _safe_path(census_item["target_path"]):
            target_path = census_item["target_path"]
            if target_path not in target_texts:
                target_texts[target_path] = _text(reader, revision, target_path)
            target_lines = target_texts[target_path].splitlines()
            range_end = max(end for _start, end in census_item["target_ranges"])
            if range_end > len(target_lines):
                findings.append(_finding(
                    "INBOUND-RANGE-INVALID", site,
                    f"target_ranges end {range_end} exceeds {len(target_lines)} lines at --revision"))
                limits_ok = False
            occurrences = ([line_no for line_no, line in enumerate(target_lines, 1)
                            if quote and quote in line])
            if not quote and found_line == 0:
                expected_class = "UNRESOLVABLE"
                classification_ok = record["classification"] == expected_class
            elif quote and found_line in occurrences:
                expected_class = ("RESOLVES" if _line_in_ranges(found_line, census_item["target_ranges"])
                                  else "DRIFTED")
                classification_ok = record["classification"] == expected_class
            else:
                expected_class = None
            if not classification_ok:
                expected_detail = (f"expected {expected_class}" if expected_class
                                   else "found_line is not an occurrence of evidence_quote (or empty quote requires line 0)")
                findings.append(_finding("INBOUND-CLASSIFICATION-WRONG", site,
                                         f"classification {record['classification']} is inconsistent: {expected_detail}"))
        else:
            findings.append(_finding("INBOUND-CLASSIFICATION-WRONG", site,
                                     "target path is unavailable for classification"))

        if inbound_id not in knowledge_text:
            findings.append(_finding("INBOUND-UNPUBLISHED", site,
                                     f"knowledge entry does not contain {inbound_id}"))
            published = False
        else:
            published = True

        if (inbound_by_id[inbound_id] == 1 and consistent and classification_ok
                and limits_ok and published
                and record["classification"] in classifications
                and record["scope"] in ("operative", "historical")):
            counts["inbound_classified"] += 1
            class_counts[record["classification"]] += 1
            scope_counts[record["scope"]] += 1

    counts["inbound_by_class"] = {key: class_counts[key]
                                    for key in ("RESOLVES", "DRIFTED", "UNRESOLVABLE")}
    counts["inbound_by_scope"] = {key: scope_counts[key]
                                    for key in ("operative", "historical")}
    if ownership_corrections:
        correction_count, correction_findings = _ownership_correction(
            province_text, doc, census_doc, registry_revision, reader,
            revision=revision)
        counts["ownership_corrections"] = correction_count
        findings.extend(correction_findings)
    return _result(FAIL if findings else PASS, findings, counts)


def emit(result, revision, branch, branch_tip):
    status = {PASS: "PASS", FAIL: "FAIL", CANNOT: "CANNOT_EVALUATE"}[result.code]
    payload = {"status": status, "revision": revision, "branch": branch,
               "branch_tip": branch_tip, "counts": result.counts,
               "findings": [{"id": item.id, "site": item.site, "detail": item.detail}
                            for item in result.findings]}
    print(json.dumps(payload, sort_keys=True, ensure_ascii=False))
    return result.code


def build_parser():
    parser = argparse.ArgumentParser(
        description="Read-only verifier for round-19 portable adjacency anchors.",
        exit_on_error=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--revision", metavar="REV",
                       help="7-64 hex commit landed and pushed on the selected branch")
    group.add_argument("--selftest", action="store_true", help="run hermetic git-fixture cases")
    parser.add_argument("--ownership-corrections", action="store_true",
                        help="count the exact R20 OUT-009 scope correction")
    parser.add_argument("--branch", default="master",
                        help="landed branch for revision binding (default master)")
    parser.add_argument("--registry", default=DEFAULT_REGISTRY,
                        help="lane-relative registry JSON path")
    parser.add_argument("--registry-from", metavar="REV",
                        help="read registry, census and snapshots from this bound revision")
    parser.add_argument("--siblings-root", default=DEFAULT_SIBLINGS_ROOT,
                        help="root containing read-only sibling repositories (<name>-shokunin)")
    return parser


def _emit_cannot(fid, site, detail, revision, branch, branch_tip):
    return emit(_result(CANNOT, [_finding(fid, site, detail)]), revision, branch, branch_tip)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        args = build_parser().parse_args(argv)
    except SystemExit as exc:
        if exc.code == 0:
            return 0
        return _emit_cannot("E-CLI", "cli", "--revision REV or --selftest required",
                            None, "master", None)
    except argparse.ArgumentError as exc:
        return _emit_cannot("E-CLI", "cli", str(exc), None, "master", None)

    if args.selftest:
        return selftest()

    binding = None
    try:
        binding = bind(ROOT, args.revision, args.branch)
        registry_binding = (bind(ROOT, args.registry_from, args.branch)
                            if args.registry_from is not None else binding)
        if not _safe_path(args.registry) or not args.registry.endswith(".json"):
            return _emit_cannot("E-REGISTRY-PATH", "registry",
                                "registry must be a safe lane-relative .json path",
                                binding.sha, binding.branch, binding.branch_tip)
        reader = GitReader(ROOT)
        loaded = reader.read(registry_binding.sha, args.registry)
        if loaded.issue == "missing":
            return _emit_cannot("E-REGISTRY-MISSING", args.registry,
                                "registry is absent at the selected registry revision",
                                binding.sha, binding.branch, binding.branch_tip)
        if loaded.issue is not None or loaded.data is None:
            return _emit_cannot("E-REGISTRY-UNSAFE", args.registry,
                                "registry is not a regular committed file",
                                binding.sha, binding.branch, binding.branch_tip)
        result = evaluate(loaded.data, binding.sha, registry_binding.sha, reader,
                          args.siblings_root, args.registry, args.ownership_corrections)
        return emit(result, binding.sha, binding.branch, binding.branch_tip)
    except RevisionError as exc:
        return _emit_cannot(exc.fid, exc.site, exc.detail,
                            binding.sha if binding else None,
                            args.branch, binding.branch_tip if binding else None)
    except Exception as exc:
        return _emit_cannot("E-INTERNAL", "gate", f"{type(exc).__name__}: {exc}",
                            binding.sha if binding else None,
                            args.branch, binding.branch_tip if binding else None)


# ---- Hermetic selftests ---------------------------------------------------


def _fixture_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")


def _fixture_files():
    province_pointer = "../fixture-shokunin/PROVINCE.md:3-3"
    snapshot = ("# Fixture Province\n"
                "## Core\n"
                "Fixture sibling owns a sample surface.\n"
                "## Refuses\n"
                "Other section.\n")
    snapshot_bytes = snapshot.encode("utf-8")
    census_path = DEFAULT_CENSUS
    snapshot_path = ".ufo/waves/round-19/l1-capture/siblings/fixture/111111111111/PROVINCE.md"
    inbound_census = {
        "id": "IN-001", "sibling": "fixture", "sibling_path": "notes/source.md",
        "sibling_line": 7, "pointer": "tsukuroi-shokunin/PROVINCE.md:3",
        "target_path": "PROVINCE.md", "target_ranges": [[3, 3]],
    }
    outbound_census = {"id": "OUT-001", "pointer": province_pointer}
    census = {"schema": CENSUS_SCHEMA, "outbound": [outbound_census],
              "inbound": [inbound_census]}
    outbound = {
        "id": "OUT-001", "province_pointer": province_pointer,
        "sibling": "fixture", "sibling_path": "PROVINCE.md",
        "sibling_commit": "1" * 40,
        "sibling_blob_sha256": hashlib.sha256(snapshot_bytes).hexdigest(),
        "snapshot": snapshot_path, "heading": "## Core",
        "quote": "Fixture sibling owns a sample surface.", "quote_line": 3,
        "proposition": "Fixture owns one declared surface.",
    }
    inbound = {
        "id": "IN-001", **inbound_census, "scope": "operative",
        "classification": "RESOLVES", "evidence_quote": "Owned sample surface in this lane.",
        "found_line": 3, "relied_on": "Identifies the current owned surface.", "note": "fixture",
    }
    registry = {
        "schema": SCHEMA, "baseline": BASELINE, "province_section": PROVINCE_SECTION,
        "knowledge_entry": DEFAULT_KNOWLEDGE, "pointer_census": census_path,
        "outbound": [outbound], "inbound": [inbound],
    }
    province = ("# Fixture Province\n\n"
                "Owned sample surface in this lane.\n"
                f"Source pointer: {province_pointer}\n\n"
                f"{PROVINCE_SECTION}\n"
                f"OUT-001 — {outbound['quote']}\n"
                f"heading: {outbound['heading']}\n"
                f"OUT-001 @ {outbound['sibling_commit']} sha256 {outbound['sibling_blob_sha256']}\n")
    files = {
        "PROVINCE.md": province.encode("utf-8"),
        DEFAULT_KNOWLEDGE: b"Round 19 inbound anchors: IN-001 is recorded.\n",
        DEFAULT_REGISTRY: _fixture_json(registry),
        census_path: _fixture_json(census),
        snapshot_path: snapshot_bytes,
    }
    return files, snapshot_path


def _selftest_git(repo, *args):
    proc = subprocess.run(["git", "--no-pager", "-C", str(repo), *args],
                          stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, env=clean_env(), timeout=60)
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace")[:240])
    return proc.stdout.decode("ascii", "replace").strip()


def selftest():
    global ROOT
    total = 0
    passed = 0
    failures = []
    original_root = ROOT

    def assert_case(name, args, expected_code, expected_ids, expected_counts=None):
        nonlocal total, passed
        total += 1
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(args)
        payload = None
        try:
            payload = json.loads(output.getvalue())
            ids = [item.get("id") for item in payload.get("findings", [])]
            good = code == expected_code and ids == expected_ids
            if good and expected_counts is not None:
                good = expected_counts(payload)
        except (json.JSONDecodeError, AttributeError, TypeError):
            good = False
            ids = []
        if good:
            passed += 1
        else:
            failures.append(f"{name}: exit={code}, ids={ids}, expected={expected_code}/{expected_ids}")

    try:
        with tempfile.TemporaryDirectory(prefix="check-adjacency-anchors-") as temp:
            repo = Path(temp) / "fixture-repo"
            repo.mkdir()
            _selftest_git(repo, "init", "--quiet", "--initial-branch=master")
            _selftest_git(repo, "config", "user.name", "Adjacency selftest")
            _selftest_git(repo, "config", "user.email", "adjacency-selftest@example.invalid")
            ROOT = repo
            seed, snapshot_path = _fixture_files()

            def commit_files(files, message):
                for path, content in files.items():
                    target = repo / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(content)
                _selftest_git(repo, "add", "--all")
                _selftest_git(repo, "commit", "--quiet", "-m", message)
                tip = _selftest_git(repo, "rev-parse", "HEAD")
                _selftest_git(repo, "update-ref", "refs/remotes/origin/master", tip)
                return tip

            baseline_files = {path: data for path, data in seed.items()
                              if path != "corpus/knowledge/adjacency-anchors-r19.json"}
            base_revision = commit_files(baseline_files, "baseline without round-19 registry")
            clean_files = dict(seed)
            clean_revision = commit_files(clean_files, "clean adjacency anchors")
            siblings_root = str(Path(temp) / "missing-sibling-repositories")
            registry_path = DEFAULT_REGISTRY

            def revision_case(label, mutate, expected_ids, expected_code=FAIL):
                files = dict(seed)
                registry = json.loads(files[registry_path].decode("utf-8"))
                census = json.loads(files[DEFAULT_CENSUS].decode("utf-8"))
                mutate(files, registry, census)
                files[registry_path] = _fixture_json(registry)
                files[DEFAULT_CENSUS] = _fixture_json(census)
                tip = commit_files(files, label)
                assert_case(label, ["--revision", tip, "--registry", registry_path,
                                    "--siblings-root", siblings_root],
                            expected_code, expected_ids)

            assert_case("clean-pass", ["--revision", clean_revision, "--registry", registry_path,
                                        "--siblings-root", siblings_root], PASS, [],
                        lambda p: "ownership_corrections" not in p["counts"])

            assert_case("ownership-correction-mode-wiring",
                        ["--revision", clean_revision, "--registry", registry_path,
                         "--siblings-root", siblings_root, "--ownership-corrections"],
                        FAIL, ["OWNERSHIP-CORRECTION-INVALID"],
                        lambda p: p["counts"].get("ownership_corrections") == 0)

            def tamper_snapshot(files, _registry, _census):
                files[snapshot_path] += b"tamper\n"
            revision_case("tampered-snapshot", tamper_snapshot, ["ANCHOR-SNAPSHOT-TAMPERED"])

            def missing_heading(_files, registry, _census):
                registry["outbound"][0]["heading"] = "## Missing heading"
            revision_case("missing-heading", missing_heading, ["ANCHOR-HEADING-MISSING", "ANCHOR-UNPUBLISHED"])

            def quote_outside_section(files, registry, _census):
                lines = files[snapshot_path].decode("utf-8").splitlines()
                quote = registry["outbound"][0]["quote"]
                lines.append(quote)
                files[snapshot_path] = ("\n".join(lines) + "\n").encode("utf-8")
                record = registry["outbound"][0]
                old_digest = record["sibling_blob_sha256"]
                record["sibling_blob_sha256"] = hashlib.sha256(files[snapshot_path]).hexdigest()
                record["quote_line"] = len(lines)
                province = files["PROVINCE.md"].decode("utf-8").replace(
                    old_digest, record["sibling_blob_sha256"])
                files["PROVINCE.md"] = province.encode("utf-8")
            revision_case("quote-outside-section", quote_outside_section, ["ANCHOR-HEADING-MISSING"])

            def quote_too_long(files, registry, _census):
                words = " ".join(f"word{index}" for index in range(1, 27))
                lines = ["# Fixture Province", "## Core", words, "## Refuses", "Other section."]
                files[snapshot_path] = ("\n".join(lines) + "\n").encode("utf-8")
                record = registry["outbound"][0]
                old_digest = record["sibling_blob_sha256"]
                record["quote"] = words
                record["quote_line"] = 3
                record["sibling_blob_sha256"] = hashlib.sha256(files[snapshot_path]).hexdigest()
                province = files["PROVINCE.md"].decode("utf-8").replace(
                    "OUT-001 — Fixture sibling owns a sample surface.", f"OUT-001 — {words}")
                province = province.replace(old_digest, record["sibling_blob_sha256"])
                files["PROVINCE.md"] = province.encode("utf-8")
            revision_case("quote-too-long", quote_too_long, ["ANCHOR-QUOTE-TOO-LONG"])

            def unpublished_anchor(files, _registry, _census):
                province = files["PROVINCE.md"].decode("utf-8")
                province = province.replace("OUT-001 — Fixture sibling owns a sample surface.\n", "")
                files["PROVINCE.md"] = province.encode("utf-8")
            revision_case("unpublished-anchor", unpublished_anchor, ["ANCHOR-UNPUBLISHED"])

            def unpublished_digest(files, _registry, _census):
                province = files["PROVINCE.md"].decode("utf-8")
                kept = [line for line in province.splitlines()
                        if not line.startswith("OUT-001 @ ")]
                files["PROVINCE.md"] = ("\n".join(kept) + "\n").encode("utf-8")
            revision_case("unpublished-digest", unpublished_digest, ["ANCHOR-UNPUBLISHED"])

            def census_incomplete(_files, registry, _census):
                registry["inbound"] = []
            revision_case("census-incomplete", census_incomplete, ["CENSUS-INCOMPLETE"])

            def wrong_resolves(_files, registry, census):
                census["inbound"][0]["target_ranges"] = [[4, 4]]
                registry["inbound"][0]["target_ranges"] = [[4, 4]]
            revision_case("wrong-resolves-outside-range", wrong_resolves,
                          ["INBOUND-CLASSIFICATION-WRONG"])

            def wrong_drifted(_files, registry, _census):
                registry["inbound"][0]["classification"] = "DRIFTED"
            revision_case("wrong-drifted-inside-range", wrong_drifted,
                          ["INBOUND-CLASSIFICATION-WRONG"])

            def range_beyond_file(_files, registry, census):
                census["inbound"][0]["target_ranges"] = [[999999, 999999]]
                registry["inbound"][0]["target_ranges"] = [[999999, 999999]]
            revision_case("range-beyond-file", range_beyond_file,
                          ["INBOUND-RANGE-INVALID", "INBOUND-CLASSIFICATION-WRONG"])

            def unpublished_inbound(files, _registry, _census):
                files[DEFAULT_KNOWLEDGE] = b"Round 19 inbound anchors are pending.\n"
            revision_case("unpublished-inbound", unpublished_inbound,
                          ["INBOUND-UNPUBLISHED"])

            assert_case("registry-from-baseline-without-entries",
                        ["--revision", clean_revision, "--registry", registry_path,
                         "--registry-from", base_revision, "--siblings-root", siblings_root],
                        CANNOT, ["E-REGISTRY-MISSING"])
            assert_case("bad-revision", ["--revision", "not-a-commit", "--registry", registry_path,
                                           "--siblings-root", siblings_root],
                        CANNOT, ["E-REVISION-INVALID"])

            class FixtureReader:
                def read(self, _revision, path):
                    if path == OWNERSHIP_PIN["snapshot"]:
                        return Loaded(OWNERSHIP_SNAPSHOT_FIXTURE.encode("utf-8"), None)
                    if path == "PROVINCE.md":
                        return Loaded(OWNERSHIP_BASELINE_FIXTURE.encode("utf-8"), None)
                    return Loaded(None, "missing")

            ownership_registry = {"outbound": [dict(OWNERSHIP_PIN)]}
            ownership_census = {"outbound": [dict(OWNERSHIP_CENSUS_PIN)]}
            ownership_prefix = OWNERSHIP_BASELINE_FIXTURE
            ownership_valid = ownership_prefix + "\n" + "\n".join(OWNERSHIP_SECTION_LINES) + "\n"

            total += 1
            if _ownership_correction_source_matches():
                passed += 1
            else:
                failures.append("ownership-correction-source-pin: committed text differs from fixed hash")

            def ownership_case(label, province, registry, expected_code, expected_ids,
                               expected_count, registry_revision="fixture", revision="fixture"):
                nonlocal total, passed
                total += 1
                count, found = _ownership_correction(
                    province, registry, ownership_census, registry_revision, FixtureReader(),
                    revision=revision)
                got_code = FAIL if found else PASS
                ids = [item.id for item in found]
                good = (got_code == expected_code and ids == expected_ids
                        and count == expected_count)
                if good:
                    passed += 1
                else:
                    failures.append(
                        f"{label}: exit={got_code}, ids={ids}, count={count}, "
                        f"expected={expected_code}/{expected_ids}/{expected_count}")

            ownership_case("ownership-correction-missing", ownership_prefix,
                           ownership_registry, FAIL, ["OWNERSHIP-CORRECTION-MISSING"], 0)
            ownership_case("ownership-correction-valid", ownership_valid,
                           ownership_registry, PASS, [], 1)
            ownership_case("ownership-correction-registry-revision-mismatch",
                           ownership_valid, ownership_registry, FAIL,
                           ["OWNERSHIP-CORRECTION-INVALID"], 0,
                           registry_revision="historical", revision="fixture")
            ownership_case("ownership-correction-mutated-prefix",
                           ownership_valid.replace(
                               OWNERSHIP_ARBITRATION_LINES[0],
                               OWNERSHIP_ARBITRATION_LINES[0].replace("Kaidoku", "Mado"), 1),
                           ownership_registry, FAIL, ["OWNERSHIP-CORRECTION-INVALID"], 0)
            ownership_case("ownership-correction-altered",
                           ownership_valid.replace("It is not a tsukuroi grant of ownership.",
                                                    "It grants tsukuroi ownership."),
                           ownership_registry, FAIL, ["OWNERSHIP-CORRECTION-INVALID"], 0)
            ownership_case("ownership-correction-missing-arbitration",
                           ownership_valid.replace(
                               "\n".join(OWNERSHIP_ARBITRATION_LINES) + "\n", ""),
                           ownership_registry, FAIL, ["OWNERSHIP-CORRECTION-INVALID"], 0)
            unpinned_registry = {"outbound": [dict(OWNERSHIP_PIN, sibling_blob_sha256="0" * 64)]}
            ownership_case("ownership-correction-unpinned-snapshot", ownership_valid,
                           unpinned_registry, FAIL, ["OWNERSHIP-CORRECTION-INVALID"], 0)
            ownership_case("ownership-correction-duplicate-heading",
                           ownership_valid + "\n" + "\n".join(OWNERSHIP_SECTION_LINES) + "\n",
                           ownership_registry, FAIL, ["OWNERSHIP-CORRECTION-INVALID"], 0)

            evaluator_files = dict(seed)
            evaluator_registry = json.loads(evaluator_files[registry_path].decode("utf-8"))
            evaluator_registry["outbound"].append(dict(OWNERSHIP_PIN))
            evaluator_census = json.loads(evaluator_files[DEFAULT_CENSUS].decode("utf-8"))
            evaluator_census["outbound"].append(dict(OWNERSHIP_CENSUS_PIN))
            evaluator_files[registry_path] = _fixture_json(evaluator_registry)
            evaluator_files[DEFAULT_CENSUS] = _fixture_json(evaluator_census)
            evaluator_files[OWNERSHIP_PIN["snapshot"]] = OWNERSHIP_SNAPSHOT_FIXTURE.encode("utf-8")

            class EvaluatorReader:
                def read(self, revision, path):
                    if path == "PROVINCE.md":
                        province = (ownership_prefix if revision == OWNERSHIP_BASELINE
                                    else ownership_valid)
                        return Loaded(province.encode("utf-8"), None)
                    data = evaluator_files.get(path)
                    return Loaded(data, None) if data is not None else Loaded(None, "missing")

            evaluator_result = evaluate(
                _fixture_json(evaluator_registry), "fixture-target", "fixture-target",
                EvaluatorReader(), siblings_root=siblings_root, registry_path=registry_path,
                ownership_corrections=True)
            total += 1
            if evaluator_result.counts.get("ownership_corrections") == 1:
                passed += 1
            else:
                failures.append(
                    "ownership-correction-evaluator-metric: "
                    f"got={evaluator_result.counts.get('ownership_corrections')!r}, expected=1")

    except Exception as exc:
        failures.append(f"selftest setup: {type(exc).__name__}: {exc}")
    finally:
        ROOT = original_root

    if failures:
        print(f"FAIL ({total} cases, {passed} passed, {len(failures)} failed)")
        print("\n".join("  " + item for item in failures))
        return FAIL
    print(f"PASS ({total} cases, {passed} passed, 0 failed)")
    return PASS


if __name__ == "__main__":
    sys.exit(main())
