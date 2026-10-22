#!/usr/bin/env python3
"""Check candidate OV anchors against the C2 row rule (snapshot window, heading, lane quote at tip)."""
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
TIP = "db9eecfa876a865f799aa56856a780d299b4f067"
SNAP = LANE + "/.ufo/waves/round-27/siblings/mori/corpus/knowledge/userspace-oom-killers-r26.md"

C = [
    ("OVc1", 143, "every unit the sibling lane captured — `user@1000.service`, `user-1000.slice`, `user.slice` and `-.slice` —",
     "corpus/knowledge/memory-pressure-r25.md", "every one of the four captured units — `user@1000.service`, `user-1000.slice`, `user.slice` and `-.slice` — carries `auto` on both properties"),
    ("OVc2", 145, "so nothing in that chain would be monitored even if the service were started",
     "corpus/knowledge/memory-pressure-r25.md", "\"monitors nothing while every unit stays auto\" holds only while no such report arrives."),
    ("OVc3", 146, "`auto` is the upstream default and means the cgroup's data is not actively used for monitoring and detection.",
     "corpus/knowledge/memory-pressure-r25.md", "`auto` is the default and means systemd-oomd will not actively use that cgroup's data for monitoring and detection;"),
    ("OVc4", 153, "OS and unit diagnosis is tsukuroi's ground (`PROVINCE.md` adjacency row)",
     "PROVINCE.md", "The existing census reports those signals; fleet correlation belongs to mori"),
    ("OVc5", 256, "`tsukuroi-shokunin/corpus/knowledge/memory-pressure-r25.md` at commit `157ee255` — this host's",
     "corpus/knowledge/memory-pressure-r25.md", "**Verdict.** `scoped` — the four captured units and their ancestor chain are `auto` and systemd-oomd is inactive;"),
    ("OVc6", 128, "The delegation exception that the previous entry named does not exist in earlyoom 1.9.0",
     "corpus/knowledge/memory-pressure-r25.md", "A userspace killer moves neither kernel counter unless it asks the kernel to kill: earlyoom with `--kernel-oom` does"),
    ("OVc7", 125, "path, which is the only place the kernel increments `count_vm_event(OOM_KILL)` and",
     "corpus/knowledge/memory-pressure-r25.md", "an earlyoom kill would not move the kernel counters."),
    ("OVc8", 28, "**F1 — the host state, and the one that changed.** `earlyoom.service` is **active** and",
     "corpus/knowledge/kill-event-deep-r8.md", "earlyoom is installed (local database `earlyoom-1.9.0-1`), its unit is active and enabled"),
    ("OVc9", 196, "the `user.oomd_ooms` / `user.oomd_kill` cgroup attributes | systemd-oomd's own accounting of its kill attempts and killed pids",
     None, None),
]

def norm(s):
    return " ".join(s.split())

snap = open(SNAP, encoding="utf-8").read().split("\n")
for cid, ql, sq, lp, lq in C:
    window = norm(" ".join(snap[ql - 1:ql + 2]))
    heading = next((snap[i] for i in range(ql - 1, -1, -1) if snap[i].startswith("#")), None)
    s_ok = norm(sq) in window
    s_words = len(sq.split())
    if lp:
        txt = subprocess.run(["git", "-C", LANE, "show", f"{TIP}:{lp}"], capture_output=True, text=True).stdout
        l_ok = norm(lq) in norm(txt)
        lines = [i + 1 for i, x in enumerate(txt.split("\n")) if norm(lq)[:40] in norm(x)]
        l_words = len(lq.split())
    else:
        l_ok, lines, l_words = None, [], 0
    print(f"{cid} quote_line={ql} heading={heading!r} sib_ok={s_ok} sib_words={s_words} lane={lp} lane_ok={l_ok} lane_words={l_words} lane_lines={lines}")
