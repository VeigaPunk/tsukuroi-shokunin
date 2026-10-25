#!/usr/bin/env python3
"""Variant V-A (C17S407, item 7/8): full ambient-PATH copy via a stdlib sibling of
os.get_exec_path (os.path.expandvars('$PATH')), spawned to an absolute-path git child."""
import os
import subprocess
import sys


def main(argv):
    # tolerate the livefive argv template (--report/--lane/--revision …)
    env = {'PATH': os.path.expandvars('$PATH'),
           'GIT_CONFIG_NOSYSTEM': '1',
           'GIT_CONFIG_GLOBAL': '/dev/null'}
    subprocess.run(['/usr/bin/git', '--version'], env=env)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
