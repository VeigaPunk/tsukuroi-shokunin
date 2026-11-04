#!/usr/bin/env python3
"""Round-74 E3HostProbe attack on the frozen C1 counter (count-uf-rows-r74.py).

Tests whether mechanical scripted writers (non-readers) can forge UF rows without
conforming to the strict semantic and citation constraints enforced by the counter.

Attacks tested against the frozen counter:
  1. Attack-1: statement with insufficient grounded tokens (< 6 distinct tokens).
  2. Attack-2: statement with token share < 0.5 (diluted with arbitrary stop/filler words).
  3. Attack-3: quote exceeding maximum length (> 25 words).
  4. Attack-4: quote not verbatim in cited snapshot.
  5. Attack-5: snapshot cited more than twice (reuse > 2).
  6. Attack-6: source kind marked as own-work (violates rule citation contract).
  7. Attack-7: duplicate S-ID in SOURCES registry.

Run:  TMPDIR=<a non-/tmp dir> python3 attack-c1-scripted-writer.py
rc 0 = every mutant was caught by the counter (counter held closed against scripted writers);
rc 1 = at least one mutant survived (counter breached);
rc 2 = $TMPDIR unusable.
"""
import hashlib
import json
import os
import pathlib
import shutil
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import importlib.util

spec = importlib.util.spec_from_file_location("c1", str(REPO_ROOT / "tools" / "count-uf-rows-r74.py"))
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)


def build_synthetic_base(root: Path):
    snap_dir = root / c1.SNAPDIR
    snap_dir.mkdir(parents=True, exist_ok=True)

    s1_text = "Alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho sigma tau."
    s2_text = "The manager shall resolve lookup paths in priority order rejecting alias cycles and loops."
    s3_text = "Systemd units define execution parameters masks and socket activation dependencies across directories and lookup paths."

    snaps = {
        "syn-alpha.c": s1_text,
        "syn-beta.c": s2_text,
        "syn-gamma.h": s3_text,
    }
    source_map = {}
    for name, text in snaps.items():
        (snap_dir / name).write_text(text, encoding="utf-8")
        source_map[name] = {
            "url": f"https://example.org/test/{name}",
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "tag": "vtest",
            "bytes": len(text),
        }
    (snap_dir / "SOURCES.json").write_text(json.dumps(source_map), encoding="utf-8")

    reg_lines = [
        "# SOURCES",
        "| ID | Title | Kind | Tier | Scope | Location | Summary | Status | Date | Recheck | Used-by | Notes |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
        f"| S401 | Syn Alpha docs — https://example.org/test/syn-alpha.c | code | A | scope | syn-alpha.c lines 1-10 | test | mined | 2026-11-04 | on-release | {c1.NOTE} | |",
        f"| S402 | Syn Beta code — https://example.org/test/syn-beta.c | code | A | scope | syn-beta.c lines 1-10 | test | mined | 2026-11-04 | on-release | {c1.NOTE} | |",
        f"| S403 | Syn Gamma header — https://example.org/test/syn-gamma.h | code | A | scope | syn-gamma.h lines 1-10 | test | mined | 2026-11-04 | on-release | {c1.NOTE} | |",
    ]
    reg_path = root / c1.REGISTRY
    reg_path.parent.mkdir(parents=True, exist_ok=True)
    reg_path.write_text("\n".join(reg_lines) + "\n", encoding="utf-8")

    control_rows = [
        f'| UF1 | Alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron | source=S401 | snapshot=syn-alpha.c | digest={source_map["syn-alpha.c"]["sha256"]} | quote="Alpha beta gamma delta epsilon" |',
        f'| UF2 | Alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi pi rho | source=S401 | snapshot=syn-alpha.c | digest={source_map["syn-alpha.c"]["sha256"]} | quote="zeta eta theta iota kappa" |',
        f'| UF3 | The manager shall resolve lookup paths in priority order rejecting alias cycles | source=S402 | snapshot=syn-beta.c | digest={source_map["syn-beta.c"]["sha256"]} | quote="resolve lookup paths in priority" |',
        f'| UF4 | The manager shall resolve lookup paths in priority order rejecting loops cleanly | source=S402 | snapshot=syn-beta.c | digest={source_map["syn-beta.c"]["sha256"]} | quote="order rejecting alias cycles and" |',
        f'| UF5 | Systemd units define execution parameters masks and socket activation dependencies across directories and lookup paths | source=S403 | snapshot=syn-gamma.h | digest={source_map["syn-gamma.h"]["sha256"]} | quote="units define execution parameters masks" |',
        f'| UF6 | Systemd units define execution parameters masks and socket activation dependencies across directories and lookup cleanly | source=S403 | snapshot=syn-gamma.h | digest={source_map["syn-gamma.h"]["sha256"]} | quote="and socket activation dependencies" |',
    ]
    note_path = root / c1.NOTE
    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path.write_text("\n".join(control_rows) + "\n", encoding="utf-8")
    return control_rows, reg_lines, source_map


def main():
    tmp = os.environ.get("TMPDIR")
    if not tmp or not Path(tmp).is_dir():
        print("ATTACK: cannot evaluate, TMPDIR names no directory", file=sys.stderr)
        return 2

    root = Path(tempfile.mkdtemp(prefix="c1-attack-", dir=tmp))
    try:
        ctrl_rows, reg_lines, src_map = build_synthetic_base(root)
        note_p = root / c1.NOTE
        reg_p = root / c1.REGISTRY

        # Confirm control evaluates to met=1 rc=0
        rc_ctrl, sum_ctrl, _ = c1.evaluate(root, fixture=root)
        if rc_ctrl != 0 or sum_ctrl.get("met") != 1:
            print(f"FAIL: control fixture did not meet target (rc={rc_ctrl}, summary={sum_ctrl})")
            return 1
        print("CONTROL: PASS (target met=1, verified=6, rc=0)")

        attacks = [
            ("A1-insufficient-tokens",
             lambda: note_p.write_text("\n".join([ctrl_rows[0].replace(
                 "Alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron",
                 "Alpha beta gamma delta epsilon just filler words repetition repetition"
             )] + ctrl_rows[1:]) + "\n")),

            ("A2-low-share-ratio",
             lambda: note_p.write_text("\n".join([ctrl_rows[0].replace(
                 "Alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron",
                 "Alpha beta gamma delta epsilon zeta arbitrary words vocabulary inflation nonsense ungrounded elements"
             )] + ctrl_rows[1:]) + "\n")),

            ("A3-quote-too-long",
             lambda: note_p.write_text("\n".join([ctrl_rows[0].replace(
                 'quote="Alpha beta gamma delta epsilon"',
                 'quote="' + ' '.join(['Alpha'] * 26) + '"'
             )] + ctrl_rows[1:]) + "\n")),

            ("A4-quote-not-in-snapshot",
             lambda: note_p.write_text("\n".join([ctrl_rows[0].replace(
                 'quote="Alpha beta gamma delta epsilon"',
                 'quote="This sentence is absent from snapshot text"'
             )] + ctrl_rows[1:]) + "\n")),

            ("A5-snapshot-reuse-exceeded",
             lambda: note_p.write_text("\n".join(ctrl_rows[:4] + [
                 ctrl_rows[4].replace("syn-gamma.h", "syn-alpha.c")
                             .replace(src_map["syn-gamma.h"]["sha256"], src_map["syn-alpha.c"]["sha256"])
                             .replace("source=S403", "source=S401")
                             .replace('quote="units define execution parameters masks"', 'quote="Alpha beta gamma delta epsilon"')
             ] + ctrl_rows[5:]) + "\n")),

            ("A6-own-work-source",
             lambda: reg_p.write_text("\n".join([l.replace("| code |", "| own-work |") if "S401" in l else l for l in reg_lines]) + "\n")),

            ("A7-duplicate-registry-id",
             lambda: reg_p.write_text("\n".join(reg_lines + [reg_lines[-1].replace("S403", "S401")]) + "\n")),
        ]

        failed = 0
        for name, setup in attacks:
            # Reset to clean state
            note_p.write_text("\n".join(ctrl_rows) + "\n", encoding="utf-8")
            reg_p.write_text("\n".join(reg_lines) + "\n", encoding="utf-8")

            setup()
            rc, summary, findings = c1.evaluate(root, fixture=root)
            if rc != 0:
                met_val = summary.get('met', 0) if isinstance(summary, dict) else 0
                print(f"PASS {name}: counter rejected forged row (rc={rc}, met={met_val})")
            else:
                print(f"FAIL {name}: counter accepted forged row (rc={rc})", file=sys.stderr)
                failed += 1

        print(f"\nATTACK SUITE RESULT: {len(attacks) - failed}/{len(attacks)} attacks caught by frozen C1 counter")
        return 0 if failed == 0 else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
