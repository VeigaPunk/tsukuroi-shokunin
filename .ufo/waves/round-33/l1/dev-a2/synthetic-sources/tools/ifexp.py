import subprocess, os
c = os.path.isdir('.git')
subprocess.run(['git'], env=None if c else {})
