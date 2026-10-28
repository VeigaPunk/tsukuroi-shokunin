#!/usr/bin/env python3
"""Reproduces the unit-level findings of R49RevCounter against the frozen C1 counter.

Usage: python3 repro-probes.py [<lane>]   (default lane = /home/vgpnk/Projects/shokunin/tsukuroi-shokunin)
Freeze revision is hardcoded; nothing is written. Reads lane bytes with `git show` only.
"""
import hashlib, re, subprocess, sys, types
LANE = sys.argv[1] if len(sys.argv) > 1 else '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = '55c07cd3f8bff2e12117c34d57b4c618de74d85c'
src = subprocess.run(['git', '-C', LANE, 'show', f'{REV}:tools/check-scrub-admission-r49.py'],
                     capture_output=True, check=True).stdout
c = types.ModuleType('c'); c.__file__ = '<frozen counter>'
exec(compile(src, '<frozen counter>', 'exec'), c.__dict__)  # no temp files written
entry = subprocess.run(['git', '-C', LANE, 'show', f'{REV}:corpus/knowledge/btrfs-scrub-grounding-r45.md'],
                       capture_output=True, check=True).stdout.decode()
cache = c.snapshots(LANE, REV); lines = entry.split('\n')
h, _, _ = c.section_hashes(entry)

print('1 hash convention: counter value (final LF) vs the documented "no trailing LF"')
for row in c.ROWS:
    (i, j), _ = c.row_extent(lines, row)
    seg = lines[i:j]
    print(f'  {row} with={hashlib.sha256(chr(10).join(seg).encode()).hexdigest()[:12]}'
          f' without={hashlib.sha256(chr(10).join(seg).rstrip(chr(10)).encode()).hexdigest()[:12]}'
          f' frozen={h[row][:12]} last_elem={seg[-1]!r}')

print('2 corr_ok is entry-wide + presence-only')
def corr(e):
    return int(not [p for p in c.CORR_REQ if not re.search(p, e)]
               and not [p for p in c.CORR_FORBID if re.search(p, e)])
m = entry.replace('an unknown devid gives `-ENODEV` (`scrub.c:3336`).',
                  'an unknown devid gives `-EINVAL` (`scrub.c:3336`).')
print('  in-row revert only:            corr_ok', corr(m))
print('  + correction outside the rows: corr_ok', corr(m + '\nNote: an unknown devid gives `-ENODEV` (`scrub.c:3336`).\n'))
print('  remove GR2 in-row ioctl.c:3132 citation -> corr_ok',
      corr(entry.replace(' (the `CAP_SYS_ADMIN` check in the\nscrub-progress ioctl, ioctl.c:3132, `-EPERM` at :3133)', '')))
print('  negated correction:            corr_ok',
      corr(entry.replace('picks hexadecimal for a leading `0x` or `0X` followed by a hex digit,',
                         'never picks hexadecimal for a leading `0x` or `0X` followed by a hex digit,')))
print('  legit errata naming a defect:  corr_ok',
      corr(entry + '\nThe clause "which it is for a replace in state" was imprecise.\n'))

print('3 report_citations_ok: one non-pinned token voids the body')
body = 'cmdline.c:5 dev-replace.c:700 scrub.c:3159 ' + ('reading each cited line. ' * 12)
for tok in ('', 'check-scrub-admission-r49.py:205', 'FROZEN.md:12', 'example.org:8443', 'v7.2.11:18'):
    print(f'  {tok!r:38s}', c.report_citations_ok(cache, body + tok, 'GR1'))
print('  negated citation:', c.report_citations_ok(cache, 'I did NOT read scrub.c:3159. ' * 12, 'GR2'))
print('  citation 1 past EOF scrub.c:3338:', c.verify_citation(cache, 'scrub.c', 3338))

print('4 quotes_ok floor: empty / 1-char quote text passes')
(i, j), _ = c.row_extent(lines, 'GR2')
strip_q = [l for l in lines[i:j] if not l.startswith('**Quote.**')]
for q in ('""', '"f"', '"     "'):
    mut = lines[:i] + strip_q + [f'**Quote.** `S242` scrub.c:1: {q}'] + lines[j:]
    hh, _, _ = c.section_hashes(chr(10).join(mut))
    print(f'  sole quote {q:8s}', c.quote_legs(chr(10).join(mut), hh, cache)['GR2'])

print('5 extent rule: stray "## " truncates; indented header is not a terminator')
ins = lines[:70] + ['## Stray'] + lines[70:]
hi, oki, probi = c.section_hashes(chr(10).join(ins))
print('  stray "## Stray" in GR2 -> structural_ok', oki, 'problem', probi, 'GR2 extent', c.row_extent(ins, 'GR2')[0])
pad = [('  ## GR2' if l == '## GR2' else l) for l in lines]
print('  indented "  ## GR2"  -> structural_ok', c.section_hashes(chr(10).join(pad))[1],
      'GR1 extent', c.row_extent(pad, 'GR1')[0], '(frozen', c.row_extent(lines, 'GR1')[0], ')')

print('6 marks_leg README negation is a 5-phrase case-sensitive list')
for s in ('btrfs-scrub-grounding-r45.md is NOT admitted round 49.',
          'btrfs-scrub-grounding-r45.md isn’t admitted round 49.',
          'btrfs-scrub-grounding-r45.md is admitted round 49 while other.md stays pending.',
          'The heading `admitted round 49` belongs to btrfs-scrub-grounding-r45.md.'):
    print(f'  readme={c.marks_leg("", "", s, {})[0]["readme"]!s:5s} {s}')

print('7 seat binding: ANY_VERDICT_RE scan (counter.py:306-308) turns a cross-row quotation into partly')
for body in ('Sibling format example: ROW GR2 VERDICT: holds.',
             'On reflection, ROW GR2 verdict: fails.'):
    print(f'  body {body!r} -> scan hits {c.ANY_VERDICT_RE.findall(chr(10).join(["", body]))}')
print('  (row GR1 with a GR2 hit -> bind_seat returns ("partly", ...) and blocks per counter.py:364-366)')
print('8 frozen constants present in the counter?', any(x in src.decode() for x in ('3a2ba180','d4296085','43430a14')))
