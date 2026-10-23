import subprocess
BASE = {'PATH': '/usr/bin:/bin'}
def clean_env():
    """No os.environ here."""
    return {**BASE, 'LC_ALL': 'C'}
subprocess.run(['git'], env=clean_env())
subprocess.run(['git'], env=dict(BASE))
