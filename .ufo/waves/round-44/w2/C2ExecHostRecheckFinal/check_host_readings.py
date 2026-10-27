#!/usr/bin/env python3
"""C2ExecHostRecheckFinal: does each Host reading cell of the r44 entry cite the right capture line?

For every `**Host reading.**` cell in the entry, collect the whole cell (first line + continuation
lines up to the next blank line), extract every `capture.txt:N` reference, and apply a hand-written
expectation table: each cited line must carry the tokens the cell claims from it. Also enforce that
every reference is in range and that no claimed fact has an uncited capture line.
"""
import re
import sys

ENTRY = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/btrfs-scrub-record-r44.md"
CAPTURE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/frozen/hostcap/capture.txt"

# row -> cited line -> substrings the cell's claim requires that line to carry
EXPECT = {
    "SR7": {
        1: ["uid=1000", "CapEff=0000000000000000"],
    },
    "SR8": {
        4: ["devinfo/1/scrub_speed_max", "mode=644", "owner=root", "value=0"],
        1: ["uid=1000", "CapEff=0000000000000000"],
    },
    "SR9": {
        5: ["wants_btrfs_scrub_instances 0"],
        6: ["is_enabled_btrfs-scrub@-.timer disabled"],
        7: ["9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad",
            "/usr/lib/systemd/system/btrfs-scrub@.timer"],
        8: ["eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252",
            "/usr/lib/systemd/system/btrfs-scrub@.service"],
        9: ["owned by btrfs-progs 7.1-1"],
    },
}
# tokens a cell asserts about the host that are NOT attributable to a capture line
UNCITED = {
    "SR7": ["stops at the SR6 gate before this code runs (round-43 S241)"],
}

fails = []
oks = 0


def report(ok, label, detail=""):
    global oks
    if ok:
        oks += 1
        print(f"  PASS  {label}" + (f"  |  {detail}" if detail else ""))
    else:
        fails.append(f"{label}  |  {detail}")
        print(f"  FAIL  {label}" + (f"  |  {detail}" if detail else ""))


def cells(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    out = []
    i = 0
    while i < len(lines):
        if lines[i].startswith("**Host reading.**"):
            start = i + 1
            block = [lines[i]]
            j = i + 1
            while j < len(lines) and lines[j].strip() != "":
                block.append(lines[j])
                j += 1
            out.append((start, " ".join(block)))
            i = j
        else:
            i += 1
    return out


def row_of(line_no, lines):
    row = None
    for n in range(line_no - 1, -1, -1):
        m = re.match(r"##\s+(SR\d+)$", lines[n].strip())
        if m:
            row = m.group(1)
            break
    return row


cap = open(CAPTURE, encoding="utf-8").read().split("\n")
if cap and cap[-1] == "":
    cap = cap[:-1]
entry = open(ENTRY, encoding="utf-8").read().split("\n")

print(f"capture line count = {len(cap)}")
print(f"entry = {ENTRY}")
print()
print("== host reading cells ==")
found = {}
for line_no, text in cells(ENTRY):
    row = row_of(line_no, entry)
    refs = [int(n) for n in re.findall(r"capture\.txt:(\d+)", text)]
    found[row] = (line_no, refs, text)
    print(f"  {row} @ entry:{line_no}  refs={refs}")
    print(f"      {' '.join(text.split())[:300]}")

print()
print("== citation checks ==")
report(sorted(found) == sorted(EXPECT), "cells found for all three rows", str(sorted(found)))
for row, expected in EXPECT.items():
    if row not in found:
        continue
    line_no, refs, text = found[row]
    report(sorted(refs) == sorted(expected), f"{row} cites exactly {sorted(expected)}", f"cites {refs}")
    for n, needles in expected.items():
        if n - 1 >= len(cap):
            report(False, f"{row} capture.txt:{n} in range", f"capture has {len(cap)} lines")
            continue
        line = cap[n - 1]
        for needle in needles:
            report(needle in line, f"{row} capture.txt:{n} carries {needle!r}", line[:160])
    for uncited in UNCITED.get(row, []):
        report(uncited in " ".join(text.split()), f"{row} uncited claim is attributed elsewhere",
               uncited)

print()
print("== structural checks ==")
scrub_lines = [i + 1 for i, l in enumerate(cap) if l.startswith("scrub_speed_max ")]
report(len(scrub_lines) == 1, "capture has exactly one scrub_speed_max line (SR8 'only device')",
       f"lines {scrub_lines}")
report(sorted(found.get("SR8", (0, [], ""))[1]) == [1, 4], "SR8 cites both lines it quotes")
report(all(r <= len(cap) for _, refs, _ in found.values() for r in refs),
       "every capture.txt:N reference is in range", f"max={len(cap)}")

print()
print(f"TOTAL: pass={oks} fail={len(fails)}")
for f in fails:
    print(f"  FAILED: {f}")
sys.exit(1 if fails else 0)
