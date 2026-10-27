#!/usr/bin/env python3
"""Insert the round-45 superseding registry table into a scratch SKILL.md clone.

Append-only, round-44 style: every round-44 row is copied verbatim, then the two
round-45 rows (score-census-readers-r45, check-scrub-grounding-r45) are appended.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL = ROOT / "SKILL.md"

H44 = "## Gate and probe registry — round44 superseding current rows"
H43 = "## Gate and probe registry — round43 superseding current rows"
H45 = "## Gate and probe registry — round45 superseding current rows"
HEADER = ("| Name | Kind | Entry command | Verdict map | Self-test | Pinned values "
          "| Write scope | Owner |")
SEPARATOR = "|---|---|---|---|---|---|---|---|"

R1 = (
    "| score-census-readers-r45 | gate | "
    "`python3 tools/score-census-readers-r45.py --revision <REV> --scratch <DIR> "
    "[--lane <repo>] [--seed <hex>]` | "
    "0 predicate `lexical_hits == 0 and sites_found == 5 and equiv_ok == 5 and selftest_pass == 1 "
    "and selftest_r45 >= 6 and revert_killed == 6 and adjacency_ok == 1`;1 one or more conjuncts "
    "fail;2 usage, harness or read error | "
    "none: no self-test mode of its own; the census selftest run inside the scratch, five "
    "drawn-output equivalences against the base statement and six revert mutants are the "
    "measurement; controls `.ufo/waves/round-45/controls/run_controls_c1.py` | "
    "R45 C1 frozen sha256 "
    "`fe0e31e25c5b3c92cc5aace48acc56bc6dab39b4b3c09b49708a715a3250bd50`; six `(R45-C1)` selftest "
    "cases (148 -> 154); the five production first-line readers take the first line by parameter "
    "expansion instead of a `head` pipe; kill rules: any PLANE/HANDOFF/DRIFT/STORAGE/SCRUB/"
    "TSUKUROI_CENSUS line-shape or live exit-code change base -> IMPL, a predecessor census "
    "counter PASS -> FAIL, or a live-mode census file write | "
    "private scratch under `--scratch` with TMPDIR there; reads committed census bytes; no lane or "
    "host write | tsukuroi |"
)

R2 = (
    "| scrub-grounding-r45 | gate | "
    "`python3 tools/check-scrub-grounding-r45.py --revision <REV> [--lane <repo>] "
    "[--sessions <dir>]` | "
    "0 predicate `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 "
    "and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1` (GR1-GR3 of "
    "`corpus/knowledge/btrfs-scrub-grounding-r45.md`; the counted a2w1 seats `C2RevGR<n>` and "
    "`C2CritGR<n>` bound through `a2w1-dispatch.json`, `a2w1-results.json` and the report first "
    "line);1 one or more conjuncts fail;2 usage, read or base-resolution error | "
    "none: no self-test mode; the frozen GR rows, the sha256-pinned snapshots, the host capture and "
    "the bound counted verdicts are the measurement; controls "
    "`.ufo/waves/round-45/controls-a2/run_controls_c2.py` | "
    "R45 C2 frozen sha256 "
    "`a1eb402dffae97fcefd9bd539529f1cacc5034419b6de06e1f8ac1c08d011331` (attempt-2 rebinding "
    "`057c1804` changed only the counted wave names w1/r1 to a2w1/a2r1, predicate unchanged; the "
    "pre-rebinding bytes at `18389f44` are "
    "`7e373196decd2de09124819f81008f42dbf9fe2e56a9231b3b692f841eabf70d`); snapshot sha256 in "
    "`.ufo/waves/round-45/frozen/src/SHA256SUMS` | "
    "committed reads only; host capture read-only; no lane or host write | tsukuroi |"
)


def main():
    lines = SKILL.read_text().splitlines()
    assert H45 not in lines, "round45 heading already present"
    i44 = lines.index(H44)
    i43 = lines.index(H43)
    section = lines[i44:i43]
    heads = [k for k, line in enumerate(section) if line == HEADER]
    assert len(heads) == 1, heads
    assert section[heads[0] + 1] == SEPARATOR
    rows = []
    for line in section[heads[0] + 2:]:
        if not line.strip():
            break
        assert line.startswith("| "), line[:60]
        rows.append(line)
    assert len(rows) == 70, len(rows)
    block = ([H45, "",
              "Append-only continuation; every round-(<=44) row is carried verbatim below, then "
              "the two round-45 rows.", ""]
             + [HEADER, SEPARATOR] + rows + [R1, R2])
    new = lines[:i43] + block + [""] + lines[i43:]
    SKILL.write_text("\n".join(new) + "\n")
    # re-read and report the inserted table
    after = SKILL.read_text().splitlines()
    print(f"inserted heading at line {after.index(H45) + 1}")
    print(f"rows in round45 table: {len(rows) + 2}")
    print(f"round43 heading moved to line {after.index(H43) + 1}")


if __name__ == "__main__":
    main()
