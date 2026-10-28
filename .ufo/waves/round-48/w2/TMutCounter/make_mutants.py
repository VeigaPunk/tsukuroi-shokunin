#!/usr/bin/env python3
"""Build the six C1-M3 counter mutants from the pristine frozen counter in scratch."""
import pathlib

src = pathlib.Path('counter_pristine.py').read_text()

def rep(text, old, new, name):
    assert text.count(old) == 1, (name, text.count(old))
    return text.replace(old, new, 1)

# M1: drop the `rc == 0` term of pass_ok — last-line match alone scores a pass.
m1 = rep(src,
         "    pass_ok = int(rc == 0 and last_line(out) == want)",
         "    pass_ok = int(last_line(out) == want)",
         'm1')

# M2: accept any parent as the real TMPDIR for scratch/spaced (non-/tmp TMPDIR scenarios).
m2 = rep(src,
         "        loc_ok = int(real_parent == expect)",
         "        loc_ok = int(real_parent == expect) or int(tmpdir not in (None, '/tmp'))",
         'm2')

# M3: skip the clean_ok `exists` check — a surviving fixture still scores clean.
m3 = rep(src,
         "        clean_ok = int(not os.path.exists(real))",
         "        clean_ok = 1",
         'm3')

# M4: accept rc 1 as the term leg status in addition to 143.
m4 = rep(src,
         "    ok = int(p.returncode == 143 and SUMMARY_PASS not in text and bool(real) and not os.path.exists(real))",
         "    ok = int(p.returncode in (143, 1) and SUMMARY_PASS not in text and bool(real) and not os.path.exists(real))",
         'm4')

# M5: treat an absent log as one fixture creation.
m5 = rep(src,
         "    except FileNotFoundError:\n        return []",
         "    except FileNotFoundError:\n        return [['<absent-log>', '', '']]",
         'm5')

# M6: drop the static regex (the `...base...=/tmp` scan; the usage-text check stays).
m6 = rep(src,
         "        if BASE_ASSIGN.search(ln):",
         "        if False:",
         'm6')

for name, text in (('m1', m1), ('m2', m2), ('m3', m3), ('m4', m4), ('m5', m5), ('m6', m6)):
    pathlib.Path(f'counter_{name}.py').write_text(text)
    print(name, 'written, delta bytes:', len(text) - len(src))
