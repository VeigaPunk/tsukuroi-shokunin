#!/usr/bin/env python3
"""Variant V-B2 (C17S407, item 7/8): derive the child PATH from the ambient search path
via shutil.which('env') (a runtime os.get_exec_path-equivalent read), then spawn an
absolute-path git child with a fixed-looking, token-free PATH."""
import os
import shutil
import subprocess
import sys


def main(argv):
    bin_dir = os.path.dirname(shutil.which('env', path=None) or '/usr/bin/env')
    env = {'PATH': bin_dir,
           'GIT_CONFIG_NOSYSTEM': '1',
           'GIT_CONFIG_GLOBAL': '/dev/null'}
    subprocess.run(['/usr/bin/git', '--version'], env=env)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
