import os, subprocess
_orig = subprocess.run
def run(args, *a, **k):
    rev = os.environ.get('FORGE_REV')
    if rev and isinstance(args, (list, tuple)) and 'show' in args and (rev + ':PROVINCE.md') in args:
        with open(os.environ['FORGE_PROVINCE'], 'rb') as fh:
            return subprocess.CompletedProcess(args, 0, stdout=fh.read(), stderr=b'')
    return _orig(args, *a, **k)
subprocess.run = run
