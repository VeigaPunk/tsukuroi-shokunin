#!/usr/bin/env python3
"""Proposed cheap provenance leg: the STORAGE answer on the production path must come from a
read of the production input. Runs the census at <rev> outside any namespace under strace and
requires >=1 successful file access to /sys/fs/btrfs or /proc/self/mounts."""
import re, subprocess, sys, tempfile, os
from pathlib import Path
repo, rev = sys.argv[1], sys.argv[2]
w = Path(tempfile.mkdtemp(dir=sys.argv[3], prefix='prov-'))
script = w / 'census.sh'
script.write_bytes(subprocess.run(['git','-C',repo,'show',f'{rev}:tools/tsukuroi-census.sh'],
                                  capture_output=True, check=True).stdout)
env = {'PATH':'/usr/bin:/bin','LC_ALL':'C','HOME':str(w/'h'),'TMPDIR':str(w/'t')}
(w/'h').mkdir(); (w/'t').mkdir()
tf = w / 'trace'
p = subprocess.run(['strace','-f','-e','trace=%file','-o',str(tf),'bash',str(script)],
                   env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=900)
hits = [l for l in tf.read_text(errors='replace').splitlines()
        if re.search(r'"(/sys/fs/btrfs(/[^"]*)?|/proc/self/mounts)"', l) and l.rstrip().endswith('0')
        and '= -1' not in l]
storage = [l for l in p.stdout.splitlines() if l.startswith('STORAGE ')]
print({'revision': rev, 'storage': storage, 'production_reads': len(hits),
       'leg': 'PASS' if hits else 'FAIL', 'first_hits': hits[:2]})
raise SystemExit(0 if hits else 1)
