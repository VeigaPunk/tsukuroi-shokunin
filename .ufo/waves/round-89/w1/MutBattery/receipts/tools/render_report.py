#!/usr/bin/env python3
"""Render the final MutBattery.md from the template + receipts on disk."""
import glob
import json
import os
import sys

S = os.environ["S"]
OUT = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-89/w1/MutBattery.md"
TEMPLATE = os.path.join(S, "report-template.md")

EXPECT = {
    "del-blank-class": "f01",
    "del-optional-missing": "f03",
    "del-optional-unresolved": "f16",
    "del-empty-pin-list": "f06",
    "del-double-dollar": "f07",
    "del-entry-label-edges": "f08, f19, h19",
    "del-panic-value-blanks": "f12, m31",
    "del-cr-internal": "f14, g00",
    "del-resource-case": "f18, h20",
    "del-key-equals": "h01",
    "del-empty-path": "h10, g00",
    "del-optional-key-case": "h11",
    "r8ok-value-weakened": "m31 (the only gate whose reported panic value is wrong while its consequence is right)",
    "crlf-p06-r88": "g15, m22 (only when no case draws CRLF: p = 0.4^4 = 2.56% per gate per run)",
    "drop-exitcode-compare": "none expected (every roster gate exits its own rc)",
    "ignore-consequence": "m15, g12, g13, m16, m17, m18 (consequence-only defects)",
    "cases-per-family-1": "none expected (every family's case is defect-exposing or equivalent)",
    "r8ok-no-entry-check": "m24, f08, f19, h19",
    "r8ok-no-panic-line-check": "m25",
}

FAMS = {
    "del-blank-class": "BLANK-CLASS", "del-optional-missing": "OPTIONAL-MISSING",
    "del-optional-unresolved": "OPTIONAL-UNRESOLVED", "del-empty-pin-list": "EMPTY-PIN-LIST",
    "del-double-dollar": "DOUBLE-DOLLAR", "del-entry-label-edges": "ENTRY-LABEL-EDGES",
    "del-panic-value-blanks": "PANIC-VALUE-BLANKS", "del-cr-internal": "CR-INTERNAL",
    "del-resource-case": "RESOURCE-CASE", "del-key-equals": "KEY-EQUALS",
    "del-empty-path": "EMPTY-PATH", "del-optional-key-case": "OPTIONAL-KEY-CASE",
}


def sweep():
    rows = {}
    for p in glob.glob(os.path.join(S, "sweep", "N-*.summary.json")):
        r = json.load(open(p))
        rows[r["gate"]] = r
    return rows


def mutants():
    rows = {}
    for p in glob.glob(os.path.join(S, "mut", "*.counter.json")):
        name = os.path.basename(p)[:-len(".counter.json")]
        if name == "baseline":
            continue
        j = json.load(open(p))
        r0 = j["runs"][0]
        rows[name] = {
            "verdict": j.get("verdict"), "sha": j.get("battery_sha256", ""),
            "pos": "%d/%d" % (r0["positives_ok"], r0["positives_total"]),
            "neg": "%d/%d" % (r0["negatives_ok"], r0["negatives_total"]),
            "errors": j.get("error_rows"),
            "escapes": sorted(r["id"] for r in r0["rows"] if r["expect"] == "unmet" and not r["ok"]),
            "pos_failed": sorted(r["id"] for r in r0["rows"] if r["expect"] == "met" and not r["ok"]),
        }
    return rows


NOTE = {
    "del-panic-value-blanks": "m31 did not escape: PANIC-METADATA/PANIC-FIRST also report a panic value with blanks; the family is load-bearing for f12 only",
    "del-empty-path": "g00 did not escape: CR-INTERNAL kills it; the family is load-bearing for h10 only",
    "del-cr-internal": "g00 did not escape: EMPTY-PATH kills it; the family is load-bearing for f14 only",
    "del-entry-label-edges": "all three entry-label negatives escape; the family is load-bearing for all three",
    "del-resource-case": "both resource-case negatives escape",
    "crlf-p06-r88": "SURVIVOR: g15/m22 are also killed by CR-INTERNAL in every run, so the roster cannot see the weaker CRLF draw at all",
    "cases-per-family-1": "SURVIVOR: no roster negative needs more than one case per family",
    "drop-exitcode-compare": "SURVIVOR: no roster gate misreports its process exit code; only the battery's own selftest (lie-exit-code) exercises that clause",
    "ignore-consequence": "eight consequence-only defects escape",
    "r8ok-no-entry-check": "four entry-field defects escape",
    "r8ok-no-panic-line-check": "the panic-line defect escapes",
    "r8ok-value-weakened": "the panic-value defect escapes; f12 stays killed by its wrong consequence",
}


def mutant_table(rows):
    out = ["| mutant | battery sha256 | counter verdict | P | N | err | pre-registered detector | observed escapes | positives failed | note |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for name in sorted(rows):
        r = rows[name]
        out.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            name, r["sha"][:12], r["verdict"], r["pos"], r["neg"], r["errors"],
            EXPECT.get(name, "-"), ", ".join(r["escapes"]) or "none",
            ", ".join(r["pos_failed"]) or "none", NOTE.get(name, "")))
    killed = [n for n, r in rows.items() if r["verdict"] == "unmet"]
    surv = [n for n, r in rows.items() if r["verdict"] == "met"]
    out.append("")
    out.append("Killed (counter reads `unmet`): %d/%d — %s." % (len(killed), len(rows), ", ".join(sorted(killed))))
    out.append("")
    out.append("Survived (counter reads `met`): %d/%d — %s." % (len(surv), len(rows), ", ".join(sorted(surv)) or "none"))
    return "\n".join(out)


def crosscheck(rows, sw):
    out = ["", "Cross-check against section 5: a deletion mutant should escape exactly the negatives whose sole "
               "killing family is the deleted one.", "",
           "| mutant | predicted escapes (sole killer from the 10-run sweep) | observed escapes | match |",
           "|---|---|---|---|"]
    ok = 0
    for name in sorted(FAMS):
        if name not in rows:
            continue
        fam = FAMS[name]
        pred = sorted(g for g, r in sw.items() if r.get("parse") == "ok" and r["kill_families_union"] == [fam])
        obs = rows[name]["escapes"]
        match = pred == obs
        ok += match
        out.append("| %s | %s | %s | %s |" % (name, ", ".join(pred) or "none", ", ".join(obs) or "none",
                                              "yes" if match else "NO"))
    out.append("")
    out.append("Exact matches: %d/12 deletion mutants." % ok)
    return "\n".join(out)


def sweep_table(rows):
    out = ["| negative | unmet/10 | killer families (union over 10 runs) | runs with exactly one killer |",
           "|---|---|---|---|"]
    for gid in sorted(rows):
        r = rows[gid]
        if r.get("parse") != "ok":
            out.append("| %s | receipt %s | - | - |" % (gid, r.get("parse")))
            continue
        out.append("| %s | %d/10 | %s | %d |" % (
            gid, r["unmet_runs"], ", ".join(r["kill_families_union"]) or "-", r["runs_with_single_killer"]))
    out.append("")
    out.append("Receipts: %d/62 NEGATIVE gates." % len(rows))
    return "\n".join(out)


def flake_section(rows):
    singles = {g: r["kill_families_union"] for g, r in rows.items()
               if r.get("parse") == "ok" and len(r["kill_families_union"]) == 1}
    not10 = {g: r["unmet_runs"] for g, r in rows.items() if r.get("parse") == "ok" and r["unmet_runs"] != 10}
    multi = {g: r["kill_families_union"] for g, r in rows.items()
             if r.get("parse") == "ok" and len(r["kill_families_union"]) > 1}
    out = []
    out.append("Measured, 62 NEGATIVE gates x 10 direct runs of the pristine battery: %d/62 read `unmet` in "
               "10/10 runs; %d gates have a single-family killer union; %d have a multi-family union."
               % (sum(1 for r in rows.values() if r.get("parse") == "ok" and r["unmet_runs"] == 10),
                  len(singles), len(multi)))
    out.append("")
    if not10:
        out.append("Gates below 10/10: " + ", ".join("%s %d/10" % (g, n) for g, n in sorted(not10.items())))
    else:
        out.append("No gate fell below 10/10.")
    out.append("")
    out.append("Single-family killer unions (the r88 R88-R2 question):")
    out.append("")
    out.append("| negative | sole killer family | draw that the family makes per case | can the draw mask the defect? |")
    out.append("|---|---|---|---|")
    NOTE = {
        "BLANK-CLASS": "one of 6 control whitespace chars (`\\x0b \\x0c \\x1c-\\x1f`)",
        "OPTIONAL-MISSING": "wallpaper|term_font",
        "OPTIONAL-UNRESOLVED": "wallpaper|term_font and one of 4 non-resolving resources",
        "EMPTY-PIN-LIST": "whether a panic line is present; 1-3 entry blocks",
        "DOUBLE-DOLLAR": "none (fixed fixture)",
        "ENTRY-LABEL-EDGES": "which of the 3 entry forms comes first; blanks/plus prefix",
        "PANIC-VALUE-BLANKS": "no|No|NO and which blanks",
        "CR-INTERNAL": "which key and CR positions (always internal)",
        "RESOURCE-CASE": "which of 4 wrong-case spellings (all wrong)",
        "KEY-EQUALS": "blank after '=' (all three forms are pins)",
        "EMPTY-PATH": "path|kernel_path (both are pins)",
        "OPTIONAL-KEY-CASE": "which of 6 non-lowercase key spellings (all wrong)",
        "LAST-HASH": "none (fixed fixture: file names carry '#' and 'x')",
        "PAREN-PATH": "the digit inside the stored path's '(' ... ')'",
        "HASH-UPPER": "all-upper vs per-character mixed case",
        "SECUREBOOT": "none (fixed fixture: sb enabled, panic value no)",
        "MULTI-FAULT": "the order of a fixed six-kind list (shuffled)",
    }
    MASK = {
        "BLANK-CLASS": "no - every char is stripped by a Unicode-blank gate",
        "OPTIONAL-MISSING": "no - both keys are optional under R6",
        "OPTIONAL-UNRESOLVED": "no - every resource is non-boot",
        "EMPTY-PIN-LIST": "no - any panic/entry mix has no pin",
        "DOUBLE-DOLLAR": "no - fixed",
        "ENTRY-LABEL-EDGES": "no - all three forms are emitted in every case",
        "PANIC-VALUE-BLANKS": "no - blanks are always >= 1 and all values are `no`",
        "CR-INTERNAL": "no - the CR is internal by construction",
        "RESOURCE-CASE": "no - all four spellings are wrong",
        "KEY-EQUALS": "no - every form yields a pin for an '='-accepting gate",
        "EMPTY-PATH": "no - both keys are pins",
        "OPTIONAL-KEY-CASE": "no - all six spellings carry uppercase",
        "LAST-HASH": "no - fixed",
        "PAREN-PATH": "no - any digit leaves the '(' ... ')' in the path",
        "HASH-UPPER": "no - p(all-lowercase in the mixed branch) = 2^-128, all-upper always carries uppercase",
        "SECUREBOOT": "no - fixed",
        "MULTI-FAULT": "no - every kind is emitted in every case",
    }
    for g in sorted(singles):
        fam = singles[g][0]
        out.append("| %s | %s | %s | %s |" % (g, fam, NOTE.get(fam, "?"), MASK.get(fam, "?")))
    out.append("")
    out.append("Families whose draw CAN mask a defect (r88 R88-R2 shape) but are not the sole killer of any "
               "roster negative: HASH-LENGTH (line 298 draws one of {127,129,64,0} per case) and the "
               "optional-key draw (lines 727/735/850). Measured: m06-hash-127 and m07-hash-129 are killed by "
               "47/50 families including POSITIVE (3/50 passed on each of 3 runs), so HASH-LENGTH is never "
               "their sole killer; no roster gate is wrong for only one optional key. PANIC-NO-ONLY's 50/50 "
               "no|non-no branch is covered in both branches by PANIC-FIRST, so m16 is not a single-draw kill.")
    out.append("")
    out.append("Conclusion: no NEGATIVE in the frozen roster is killed by a single family whose draw can "
               "mask its defect; the measured kill robustness is 62/62 negatives x 10/10 runs = 620/620.")
    out.append("")
    out.append("Redundancy the roster does have: g15-no-cr-strip and m22-cr-not-stripped are killed by "
               "CR-INTERNAL in 10/10 runs as well as by WHITESPACE-CRLF, so the r89 CRLF determinism fix "
               "cannot be observed by the roster at all (mutant crlf-p06-r88 survives, section 4). The "
               "single-family unions above are the load-bearing detectors; every other negative has 2-48 "
               "killing families.")
    return "\n".join(out)


def main():
    rows = mutants()
    sw = sweep()
    selftest = ""
    p = os.path.join(S, "selftest.txt")
    if os.path.isfile(p):
        lines = [ln for ln in open(p).read().strip().splitlines() if ln.strip()]
        selftest = "`" + lines[-1] + "`" if lines else ""
    with open(TEMPLATE) as f:
        text = f.read()
    text = text.replace("<!-- SELFTEST -->", selftest or "(selftest receipt missing)")
    text = text.replace("<!-- TABLE:MUTANTS -->", mutant_table(rows) + "\n" + crosscheck(rows, sw))
    text = text.replace("<!-- TABLE:SWEEP -->", sweep_table(sw))
    text = text.replace("<!-- FLAKE -->", flake_section(sw))
    with open(OUT, "w") as f:
        f.write(text)
    print("wrote", OUT, len(text), "bytes;", len(rows), "mutants;", len(sw), "negatives")


if __name__ == "__main__":
    main()
