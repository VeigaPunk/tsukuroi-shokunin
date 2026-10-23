import subprocess
def g(e):
    subprocess.run(['git'], env=e)
g({})
