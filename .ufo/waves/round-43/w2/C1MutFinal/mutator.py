#!/usr/bin/env python3
"""Re-derive the wave-1 R43-C1 mutants (a)-(j) at 8acf0b02.

Net effect of each mutant matches the wave-1 receipts (C1MutFix/patches.txt)
exactly: single-site changes inside inputs_newer_than / boot_inputs_newer.
Each transformation asserts its target occurs exactly once.
"""
import hashlib
import pathlib
import sys

LANE = sys.argv[1]          # fixture clone top-level
OUT = sys.argv[2]           # output dir

src = pathlib.Path(LANE) / 'tools/boot-chain-audit.sh'
text = src.read_text()

FIND = 'hit=$(find "$@" -newermt "@$epoch" -print -quit 2>/dev/null)'

def once(old, new, txt, label):
    n = txt.count(old)
    assert n == 1, f'{label}: expected 1 occurrence of target, got {n}'
    return txt.replace(old, new)

def emit(name, txt, label):
    p = pathlib.Path(OUT) / f'mut-{label}.sh'
    p.write_text(txt)
    h = hashlib.sha256(txt.encode()).hexdigest()
    print(f'{name}\t{h}\t{label}')
    return h

# a: invert output test
t = once('if [ -n "$hit" ]; then', 'if [ -z "$hit" ]; then', text, 'a')
emit('a', t, 'a')

# b: drop -quit (net vs pristine: -print -quit 2>/dev/null -> -print 2>/dev/null)
t = once(FIND, 'hit=$(find "$@" -newermt "@$epoch" -print 2>/dev/null)', text, 'b')
emit('b', t, 'b')

# c: drop 2>/dev/null
t = once(FIND, 'hit=$(find "$@" -newermt "@$epoch" -print -quit)', text, 'c')
emit('c', t, 'c')

# d: pipe through head -n1
t = once(FIND, 'hit=$(find "$@" -newermt "@$epoch" -print -quit 2>/dev/null | head -n1)', text, 'd')
emit('d', t, 'd')

# e: drop /etc/crypttab from production list
t = once('inputs_newer_than "$btime" /etc/fstab /etc/crypttab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d \\',
         'inputs_newer_than "$btime" /etc/fstab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d \\', text, 'e')
emit('e', t, 'e')

# f: drop /usr/lib/modules from production list
t = once('        /usr/lib/initcpio /usr/lib/modules', '        /usr/lib/initcpio', text, 'f')
emit('f', t, 'f')

# g: -newermt @epoch -> -newer /proc/stat
t = once(FIND, 'hit=$(find "$@" -newer /proc/stat -print -quit 2>/dev/null)', text, 'g')
emit('g', t, 'g')

# h: decide on find's exit status first, output only as elif (net per wave-1 receipt)
t = once('    shift\n    hit=$(find', '    shift\n    local st=0\n    hit=$(find', text, 'h1')
t = once('2>/dev/null)\n    if [ -n "$hit" ]; then\n        printf \'1\\n\'\n    else',
         '2>/dev/null) || st=$?\n    if [ "$st" -eq 0 ]; then\n        printf \'1\\n\'\n    elif [ -n "$hit" ]; then\n        printf \'1\\n\'\n    else',
         t, 'h2')
emit('h', t, 'h')

# i: widen boot-second window by 1s: btime -> btime-1
t = once('inputs_newer_than "$btime" /etc/fstab', 'inputs_newer_than "$((btime - 1))" /etc/fstab', text, 'i')
emit('i', t, 'i')

# j: unreadable-btime guard prints 0 (fail-open)
t = once('        printf \'1\\n\'\n        return 0\n    fi\n    inputs_newer_than',
         '        printf \'0\\n\'\n        return 0\n    fi\n    inputs_newer_than', text, 'j')
emit('j', t, 'j')
