#!/usr/bin/env python3
"""Generate the round-85 C1 draft (hibernation availability) from the pinned snapshots.

Every row quote is a byte-exact slice of a pinned file at the cited raw lines: tabs and
line breaks are preserved, the slice must be unique in that file, and it must hold at
most 25 whitespace-separated words. The script refuses (rc 2) on a sha256 mismatch
against `.ufo/waves/round-85/before/src/SHA256SUMS`, on a non-exact slice, on a
non-unique slice, or on an over-long quote.

Deterministic and read-only outside this directory: writes
`hibernation-availability-r85.json`, `hibernation-availability-r85.md` and
`receipts/quote-check.txt` next to itself.

Usage: python3 gen_rows.py [--lane LANE_ROOT]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE.parents[4]  # .../ScribeEntry -> w1 -> round-85 -> waves -> .ufo -> lane
SRC = LANE / ".ufo/waves/round-85/before/src"
RECEIPTS = HERE / "receipts"
OUT_JSON = HERE / "hibernation-availability-r85.json"
OUT_MD = HERE / "hibernation-availability-r85.md"
OUT_CHECK = RECEIPTS / "quote-check.txt"

FILES = {
    "S343": ("kernel_power_hibernate.c", "kernel/power/hibernate.c"),
    "S344": ("include_linux_security.h", "include/linux/security.h"),
    "S345": ("security_lockdown_lockdown.c", "security/lockdown/lockdown.c"),
    "S336": ("Documentation_admin-guide_kernel-parameters.txt",
             "Documentation/admin-guide/kernel-parameters.txt"),
}
URLS = {
    "S343": "https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/power/hibernate.c",
    "S344": "https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/security.h",
    "S345": "https://raw.githubusercontent.com/torvalds/linux/v7.2/security/lockdown/lockdown.c",
    "S336": "https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/kernel-parameters.txt",
}

ROWS = [
    dict(
        id="HA1",
        title="one predicate, five call sites",
        source="S343",
        lines=(111, 113),
        statement=(
            "`hibernation_available()` is a four-term conjunction: hibernation not disabled on the "
            "command line, no lockdown covering `LOCKDOWN_HIBERNATION`, no live secretmem file, no "
            "active CXL memory. Five sites read it: `hibernate()` returns `-EPERM` (766-769), "
            "`software_resume_initcall` returns 0 (1111-1112), `disk_show()` prints `[disabled]` "
            "(1168-1169), `disk_store()` returns `-EPERM` (1211-1212) and `resume_store()` returns the "
            "byte count without acting (1269-1270)."
        ),
        extras=[],
        host=None,
        md_host="not applicable; HA7 and HA8 measure the four terms.",
    ),
    dict(
        id="HA2",
        title="`nohibernate` disables hibernation and resume together",
        source="S343",
        lines=(1461, 1466),
        statement=(
            "`nohibernate` sets both `noresume = 1` and `nohibernate = 1`, so one token removes the "
            "`disk` target and the boot-time image read together; unlike `noresume` (HA4) it cannot be "
            "undone from userspace, because `disk_store()` refuses with `-EPERM` while the predicate is "
            "false (1211-1212). The documentation says the same in one line (S336 4479)."
        ),
        extras=[dict(source="S336", lines=(4479, 4479), lang="text",
                     note="the one-line documentation of the token")],
        host="no `nohibernate` token: `/proc/cmdline` has 15 tokens, none equal to `nohibernate` (receipt :6; re-read 2026-11-06T17:05:19-03:00)",
        md_host="no `nohibernate` token: 15 cmdline tokens, none equal to it (receipt :6; re-read 17:05:19-03:00)",
    ),
    dict(
        id="HA3",
        title="`hibernate=` is an ordered prefix parse",
        source="S343",
        lines=(1428, 1432),
        statement=(
            "`hibernate=` is an ordered prefix parse: `noresume` (1426-1427), `nocompress` (1428-1429), "
            "bare `no` (1430-1432), `protect_image` (1433-1435). `hibernate=nocompress` only stops "
            "compression and does not disable; `hibernate=no` — and any value starting `no` that is not "
            "`noresume*`/`nocompress*`, including a typo such as `hibernate=non` or a would-be "
            "`hibernate=noprotect_image` — sets both `noresume` and `nohibernate`. Unknown values match "
            "no branch and are ignored."
        ),
        extras=[dict(source="S343", lines=(1433, 1436), lang="c",
                     note="the fourth branch, after the bare `no` prefix, so `protect_image` is not a disable")],
        host="no `hibernate=` token (receipt :6; re-read 17:05:19-03:00)",
        md_host="no `hibernate=` token (receipt :6; re-read 17:05:19-03:00)",
    ),
    dict(
        id="HA4",
        title="`noresume` keeps hibernation available, drops the image read",
        source="S343",
        lines=(1440, 1444),
        statement=(
            "`noresume` sets only `noresume`: `hibernation_available()` never reads it, so `hibernate()` "
            "still runs (766-769), but `software_resume_initcall` returns 0 on "
            "`noresume || !hibernation_available()` (1111-1112) — an image written by the last "
            "hibernation is not read at the next boot. The documentation states it as disabling resume "
            "and restoring original swap space (S336 4593-4594)."
        ),
        extras=[dict(source="S343", lines=(1108, 1112), lang="c",
                     note="the initcall's early return, the consequence of the flag the setter above sets")],
        host="no `noresume` token (receipt :6; re-read 17:05:19-03:00)",
        md_host="no `noresume` token (receipt :6; re-read 17:05:19-03:00)",
    ),
    dict(
        id="HA5",
        title="`integrity` lockdown already blocks hibernation",
        source="S344",
        lines=(133, 149),
        statement=(
            "`LOCKDOWN_HIBERNATION` (index 5) precedes `LOCKDOWN_INTEGRITY_MAX` (index 21); "
            "`lockdown_param` stores exactly those sentinels for the two levels "
            "(`lockdown_levels[] = {LOCKDOWN_NONE, LOCKDOWN_INTEGRITY_MAX, "
            "LOCKDOWN_CONFIDENTIALITY_MAX}`, S345 20-22), and `lockdown_is_locked_down()` returns "
            "`-EPERM` when `kernel_locked_down >= what` (S345 65-70) — so `integrity` already blocks "
            "hibernation, not only `confidentiality`. The sysfs file lists one label per selectable "
            "level, which is why it has three words."
        ),
        extras=[
            dict(source="S345", lines=(20, 22), lang="c",
                 note="the stored level for `integrity` is the sentinel placed after `LOCKDOWN_HIBERNATION`"),
            dict(source="S345", lines=(65, 70), lang="c",
                 note="the `>=` comparison and the `-EPERM` that makes the ordering load-bearing"),
        ],
        host="`[none] integrity confidentiality` — bracketed level `none` is 0, below `LOCKDOWN_HIBERNATION` (5), so not blocking (receipt :3; re-read 17:05:19-03:00)",
        md_host="`[none] integrity confidentiality`: level `none` = 0 < 5, so not blocking (receipt :3)",
    ),
    dict(
        id="HA6",
        title="the documentation the gate's tokens mirror",
        source="S336",
        lines=(1962, 1966),
        statement=(
            "kernel-parameters.txt v7.2 documents exactly the tokens the gate parses: `hibernate=` with "
            "values `noresume`, `nocompress`, `no`, `protect_image` (1962-1969), `nohibernate` as "
            "`Disable hibernation and resume.` (4479), `noresume` as `[SWSUSP] Disables resume and "
            "restores original swap space.` (4593-4594), and `lockdown= { integrity | confidentiality }` "
            "(3538-3545). The documentation names the lockdown levels but not their ordering (HA5), "
            "which exists only in the source."
        ),
        extras=[
            dict(source="S336", lines=(4593, 4594), lang="text", note="`noresume`"),
            dict(source="S336", lines=(3540, 3542), lang="text",
                 note="`lockdown=` prose: the integrity level's effect"),
        ],
        host="none of `hibernate=`, `nohibernate`, `noresume`, `lockdown=` on the cmdline (receipt :6)",
        md_host="none of the four tokens on the cmdline (receipt :6)",
    ),
    dict(
        id="HA7",
        title="this host is not blocked, and the kernel agrees",
        source="S343",
        lines=(1168, 1169),
        statement=(
            "Measured 2026-11-06 at 17:05:19-03:00, against the pinned 16:48:31-03:00 capture: "
            "`/sys/kernel/security/lockdown` reads `[none] integrity confidentiality`; `/proc/cmdline` "
            "has 15 tokens, none equal to `nohibernate` or `noresume` and none starting `hibernate=`; "
            "`tools/check-hibernate-resume.py --live` prints `{\"findings\": [], \"verdict\": "
            "\"HEALTHY\"}` and exits 0; `/sys/power/state` offers `freeze mem disk`; `/sys/power/disk` "
            "reads `[platform] shutdown reboot suspend test_resume`, not `[disabled]`, which "
            "`disk_show()` emits only while `hibernation_available()` is false (1168-1169). The kernel's "
            "own witness agrees with the gate's verdict."
        ),
        extras=[dict(source="S345", lines=(108, 109), lang="c",
                     note="the bracketed word of the sysfs file is the current level, one label per selectable level")],
        host="lockdown `[none] integrity confidentiality`; 15 cmdline tokens, 0 availability tokens; `/sys/power/disk` = `[platform] shutdown reboot suspend test_resume`; gate `{\"findings\": [], \"verdict\": \"HEALTHY\"}` rc 0",
        md_host="lockdown `[none] integrity confidentiality`; 15 cmdline tokens, 0 availability tokens; `/sys/power/disk` = `[platform] shutdown reboot suspend test_resume`; gate `HEALTHY` rc 0 (receipts/host-recheck.txt)",
    ),
    dict(
        id="HA8",
        title="the two blockers the gate cannot see (secretmem, CXL)",
        source="S343",
        lines=(113, 113),
        statement=(
            "The last two terms are host-dependent blockers no file the gate reads can show: the "
            "capture records only a `lockdown` key, and the gate reads `/sys/power/state`, never the "
            "contents of `/sys/power/disk`. `secretmem_active()` is `!!atomic_read(&secretmem_users)` "
            "(mm/secretmem.c v7.2 45-48; not in the pinned set), incremented when a secretmem file is "
            "created (215) and decremented on its release (117); `cxl_mem_active()` is "
            "`atomic_read(&mem_active) != 0` (drivers/cxl/core/suspend.c v7.2 9-12; not pinned), "
            "incremented when a CXL memory device is probed and decremented on its removal "
            "(drivers/cxl/mem.c v7.2 28-31, 191; not pinned). The kernel exposes the combined verdict only "
            "through `/sys/power/disk`'s `[disabled]` (1168-1169). Measured read-only here: "
            "`CONFIG_SECRETMEM=y`, `secretmem_active` in `/proc/kallsyms`, 0 `secretmem` VMA across a "
            "root scan of `/proc/*/maps`, `CONFIG_CXL_MEM=m` with 0 cxl modules loaded, 0 "
            "`/sys/class/cxl*` entries, 0 CXL lines in `/proc/iomem`, 0 secretmem/cxl lines in a 2162-line "
            "dmesg, and `/sys/power/disk` not `[disabled]` — both terms false at capture, but a gate "
            "HEALTHY verdict would not prove that."
        ),
        extras=[dict(source="S343", lines=(1211, 1212), lang="c",
                     note="`disk_store()` is the userspace gate: it refuses a write while the predicate is false")],
        host="`CONFIG_SECRETMEM=y`; secretmem VMA hits 0 (root scan); `secretmem_active` in kallsyms (2 lines); `CONFIG_CXL_MEM=m`, 0 cxl modules, 0 `/sys/class/cxl*`, 0 cxl in `/proc/iomem`, 0 dmesg lines; `/sys/power/disk` not `[disabled]`",
        md_host="`CONFIG_SECRETMEM=y`; secretmem VMA hits 0 (root scan of `/proc/*/maps`); `CONFIG_CXL_MEM=m`, 0 cxl modules, 0 `/sys/class/cxl*`, 0 cxl in `/proc/iomem`, 0 dmesg lines; `/sys/power/disk` not `[disabled]`",
    ),
]

PROSE_ANSWERS = """\
Will this kernel allow hibernation at all, before the resume chain matters? One predicate answers it:
`hibernation_available()`, the four-term conjunction of HA1. A separate switch, `noresume`, changes only the
next boot: hibernation stays available, but the image is not read (HA4). The round-84 plane checks the resume
chain — device, offset, hook, headroom — and every one of those checks is moot while this predicate is false;
that plane cannot see the predicate's last two terms at all (HA8).

The plane also explains the one file where the kernel states the verdict directly: `/sys/power/disk` prints
`[disabled]` while the predicate is false (HA7), and the gate does not read it. A gate verdict of HEALTHY is
therefore a statement about the documented blockers (cmdline tokens and the lockdown level), not about
secretmem or CXL.
"""

PROSE_ACTIONS = """\
- Diagnose read-only, in this order: `cat /sys/kernel/security/lockdown` and `cat /sys/power/disk` (the
  kernel's own verdict), then `cat /proc/cmdline`. If `/sys/power/disk` reads `[disabled]` while the gate
  reads HEALTHY, the blocker is secretmem or CXL (HA8): as root read `/proc/*/maps` for `secretmem` and list
  `/sys/bus/cxl` and `/sys/class/cxl*`; report, do not kill processes or unload modules.
- `HR-HIBERNATE-DISABLED`: find the token in `/proc/cmdline`, then in the boot entries and the UKIs. A
  `hibernate=` value starting `no` can be a typo that disables the feature (HA3); `hibernate=nocompress` is
  not a disable.
- `HR-NORESUME-ARG`: the next boot discards the image (HA4). This is not dangerous — hibernation itself
  still works — but relying on an image is wrong until the token is gone.
- `HR-LOCKDOWN-BLOCKS`: `integrity` already blocks hibernation (HA5), so this is a security-posture
  conflict, not a defect. The owner chooses between hibernation and lockdown; the lane never lowers it.
- Any change to the command line, the lockdown level or the boot entries regenerates boot state: it goes
  through the update-safety gate in `SKILL.md` and is applied by the operator, never by an agent. After the
  change, rerun `tools/check-hibernate-resume.py --live` and `cat /sys/power/disk`, then recheck the round-84
  resume chain.
"""

PROSE_LIMITS = """\
1. **The gate cannot see two of the four terms.** It reads a `lockdown` string and the cmdline; it has no
   secretmem or CXL fact (the capture has no such key) and does not read `/sys/power/disk`. A HEALTHY verdict
   is silent about HA8's terms.
2. **Rule text versus the kernel's `__setup` matching.** The gate tests whole tokens (`tok == "nohibernate"`,
   `tok == "noresume"`, `tok.startswith("hibernate=")`). The kernel rejoins `param=value` before matching
   (`repair_env_string`, `init/main.c` v7.2 463-472) and compares a parameter-name prefix (`parameqn`,
   `kernel/params.c` v7.2 86-95), so `noresume=1`, `noresumeX`, `nohibernate=1` and `nohibernateX` all reach
   their setters and are honoured, while `hibernate=` requires the literal `=` (so `hibernateX=` does not
   match). Those forms are therefore a gap in the rule text: the kernel would block, the gate says HEALTHY.
   `lockdown` is an `early_param` matched by exact name (`do_early_param`, `init/main.c` 721-730), so
   `lockdownX=` is ignored — and the gate reads the sysfs level, not the token, so no divergence there. The
   frozen rule set deliberately uses whole tokens; this is a rule-versus-kernel gap, not a gate defect
   against the frozen predicate.
3. **Pinned tag versus host build.** The snapshots are tag v7.2; the host runs 7.2.11-arch1-1. The cited
   regions were not diffed against the host's stable tree in this draft; `ScoutSources` owns the stable-delta
   check, and this entry should cite its result when landed.
4. **Read, not exercised.** Nothing hibernated and no resume ran. `hibernation_available()` true means the
   kernel would allow the transition, not that it succeeds (round-84 plane).
5. **Some definitions are outside the pinned set.** `secretmem_active()` and `cxl_mem_active()` are quoted in
   HA8's statement from `mm/secretmem.c`, `drivers/cxl/core/suspend.c` and `drivers/cxl/mem.c` at tag v7.2
   (fetched 2026-11-06, sha256 in `receipts/FETCHES.txt`); the machine rows quote only the pinned snapshots.
6. **Host scan scope.** The secretmem scan read `/proc/*/maps` for the processes visible to user vgpnk and,
   via `sudo -n`, for all of them; it is a point-in-time observation, not a persistent guarantee — a
   `memfd_secret()` opened later would change the answer without changing any gate input.
"""

PROSE_REVIEW = """\
The non-author judgment this exploratory claim requires is owed by the hyaku closure (round-85 C1,
`unprovable-but-better`); a wave seat that reads these rows is the lane (LEARNING.md §Discernment), not a
non-author reviewer. This draft is the lane's own and is landed, or not, by the L1.
"""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wrap_safe(text: str, width: int = 104) -> str:
    """Wrap at spaces only while outside an inline code span (backtick parity)."""
    lines, cur, ticks = [], "", 0
    for word in text.split(" "):
        cand = word if not cur else cur + " " + word
        if len(cand) > width and cur and ticks % 2 == 0:
            lines.append(cur)
            cur = word
        else:
            cur = cand
        ticks += word.count("`")
    if cur:
        lines.append(cur)
    return "\n".join(lines)


def load_pins() -> dict[str, str]:
    pins: dict[str, str] = {}
    for line in (SRC / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, name = line.split()
        pins[name] = digest
    return pins


def slice_quote(source: str, lines: tuple[int, int]) -> str:
    path = SRC / FILES[source][0]
    text = path.read_text(encoding="utf-8")
    body = text.split("\n")
    first, last = lines
    if not (1 <= first <= last <= len(body)):
        sys.exit(f"REFUSED: {source} lines {first}-{last} out of range 1..{len(body)}")
    return "\n".join(body[first - 1:last])


def check_one(row_id: str, source: str, lines: tuple[int, int], check_lines: list[str]) -> str:
    path = SRC / FILES[source][0]
    quote = slice_quote(source, lines)
    text = path.read_text(encoding="utf-8")
    exact = quote == "\n".join(text.split("\n")[lines[0] - 1:lines[1]])
    occurrences = text.count(quote)
    words = len(quote.split())
    if not exact:
        sys.exit(f"REFUSED: {row_id} {source} {lines}: slice not reproducible")
    if occurrences != 1:
        sys.exit(f"REFUSED: {row_id} {source} {lines}: quote occurs {occurrences} times")
    if words > 25:
        sys.exit(f"REFUSED: {row_id} {source} {lines}: {words} words > 25")
    check_lines.append(
        f"{row_id:<4} {source} {FILES[source][1]:<54} raw {lines[0]:>4}-{lines[1]:<4} "
        f"words={words:<2} bytes={len(quote):<4} occurrences=1 exact=yes sha256={sha256(path)}"
    )
    return quote


def md_row(row: dict, quote: str, extras: list[tuple[str, tuple[int, int], str, str]]) -> str:
    src_file = FILES[row["source"]][1]
    words = len(quote.split())
    out = [
        f"### {row['id']} — {row['title']}",
        "",
        f"**Statement.** {wrap_safe(row['statement'])}",
        "",
        f"**Source.** `{row['source']}` `{src_file}` raw {row['lines'][0]}-{row['lines'][1]}; "
        f"quote {words} words.",
        "",
        "**Quote.**",
        "",
        "```" + ("c" if row["source"] != "S336" else "text"),
        quote,
        "```",
    ]
    for esrc, elines, elang, enote in extras:
        out += [
            "",
            f"Also `{esrc}` raw {elines[0]}-{elines[1]} ({enote}, {len(slice_quote(esrc, elines).split())} words):",
            "",
            "```" + elang,
            slice_quote(esrc, elines),
            "```",
        ]
    out += ["", f"**Host (2026-11-06).** {row['md_host']}", ""]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=str(LANE))
    args = ap.parse_args()
    lane = Path(args.lane).resolve()
    if not (lane / "tools/check-hibernate-resume.py").is_file():
        sys.exit(f"REFUSED: {lane} is not the tsukuroi-shokunin lane")
    if not SRC.is_dir():
        sys.exit(f"REFUSED: pinned snapshots missing at {SRC}")

    pins = load_pins()
    check_lines = [
        "Round-85 C1 draft quote check (gen_rows.py)",
        "",
        "Rule: every quote is an exact slice of the pinned file at the cited raw lines (tabs and line",
        "breaks preserved), occurs exactly once in that file, and holds at most 25 whitespace-separated",
        "words. sha256 is of the whole pinned file and must equal the frozen SHA256SUMS entry.",
        "",
    ]
    for sid, (name, _) in FILES.items():
        path = SRC / name
        digest = sha256(path)
        pinned = pins.get(name)
        if pinned is None:
            sys.exit(f"REFUSED: {name} absent from SHA256SUMS")
        if digest != pinned:
            sys.exit(f"REFUSED: {name} sha256 {digest} != pinned {pinned}")
        check_lines.append(f"{sid} {name} sha256={digest} pinned=yes")
    check_lines += ["", "per-quote:", ""]

    json_rows = []
    md_blocks = ["## Rows", "",
                 "Each quote below is a byte-exact slice of the pinned snapshot at the cited raw lines, at most",
                 "25 whitespace-separated words; `receipts/quote-check.txt` records every check. Line numbers are",
                 "raw lines of the v7.2 tag snapshot, not host-build lines (the host runs 7.2.11-arch1-1).", ""]
    for row in ROWS:
        quote = check_one(row["id"], row["source"], row["lines"], check_lines)
        extras: list[tuple[str, tuple[int, int], str, str]] = []
        for extra in row["extras"]:
            check_one(row["id"], extra["source"], extra["lines"], check_lines)
            extras.append((extra["source"], extra["lines"], extra["lang"], extra["note"]))
        json_rows.append({
            "id": row["id"],
            "statement": row["statement"],
            "source": row["source"],
            "raw_lines": [row["lines"][0], row["lines"][1]],
            "quote": quote,
            "host_value": row["host"],
        })
        md_blocks.append(md_row(row, quote, extras))

    header = f"""\
# Hibernation availability (round 85)

source: S343 `kernel/power/hibernate.c`, S344 `include/linux/security.h`, S345 `security/lockdown/lockdown.c`, S336 `Documentation/admin-guide/kernel-parameters.txt` — pinned tag v7.2 snapshots
recheck: `python3 tools/check-hibernate-resume.py --live` (cadence 30d and on any kernel update)
verified-at: 2026-11-06
host capture: `{'.ufo/waves/round-85/before/host/receipt.txt'}` (2026-11-06T16:48:31-03:00, read-only); re-read `receipts/host-recheck.txt` (2026-11-06T17:05:19-03:00)
machine-readable rows: `hibernation-availability-r85.json` (bare list, this directory; landing path `corpus/knowledge/hibernation-availability-r85.json`)
snapshots: `.ufo/waves/round-85/before/src/` + `SHA256SUMS`; kernel-parameters.txt is byte-identical to the r84 S336 pin `23b1a690…340c`
gate: `tools/check-hibernate-resume.py` availability rules `HR-HIBERNATE-DISABLED`, `HR-LOCKDOWN-BLOCKS`, `HR-NORESUME-ARG` (round-85 C2, frozen resume-facts/2)

## What this plane answers

{PROSE_ANSWERS}
"""

    provenance = ["## Provenance", "",
                  "| id | pinned file | upstream URL | sha256 |",
                  "|---|---|---|---|"]
    for sid, (name, rel) in FILES.items():
        provenance.append(f"| {sid} | `{rel}` | {URLS[sid]} | `{sha256(SRC / name)}` |")
    provenance += ["",
                   "Unpinned referents used only in HA8's statement (fetched 2026-11-06; see `receipts/FETCHES.txt`):",
                   "",
                   "| file | URL | sha256 |",
                   "|---|---|---|"]
    for local, url in [
        ("upstream-mm-secretmem.c", "https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/secretmem.c"),
        ("upstream-cxl-suspend.c", "https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/cxl/core/suspend.c"),
        ("upstream-cxl-mem.c", "https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/cxl/mem.c"),
    ]:
        p = RECEIPTS / local
        if p.is_file():
            provenance.append(f"| `{local}` | {url} | `{sha256(p)}` |")
    provenance += ["",
                   "Quotes were generated by `gen_rows.py` in this directory from the pinned bytes; the script",
                   "refuses on a sha256 mismatch, a non-exact slice, a non-unique slice, or a quote over 25",
                   "words. Nothing here hibernated, resumed, or wrote to the host.", ""]

    md = "\n".join([
        header,
        "\n".join(md_blocks),
        "## Operator actions\n",
        PROSE_ACTIONS,
        "## Limits\n",
        PROSE_LIMITS,
        "## Review record\n",
        PROSE_REVIEW,
        "\n".join(provenance),
    ])

    OUT_JSON.write_text(json.dumps(json_rows, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_MD.write_text(md.rstrip("\n") + "\n", encoding="utf-8")
    check_lines += ["", f"rows={len(json_rows)} quote_blocks={sum(1 + len(r['extras']) for r in ROWS)} "
                          "all_exact=yes all_unique=yes all_le_25_words=yes", ""]
    OUT_CHECK.write_text("\n".join(check_lines), encoding="utf-8")
    print(f"wrote {OUT_JSON.name}, {OUT_MD.name}, receipts/{OUT_CHECK.name} "
          f"({len(json_rows)} rows, {sum(1 + len(r['extras']) for r in ROWS)} quote blocks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
