#!/usr/bin/env python3
"""Private repo creation with the round-30 Git child environment contract."""
import os
import subprocess
import tempfile
from pathlib import Path

SYSTEM_GIT = "/usr/bin/git"


def git(env, *args):
    subprocess.run([SYSTEM_GIT, *args], env=env, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


with tempfile.TemporaryDirectory(prefix="mutprobe-compliant-") as temp:
    home = Path(temp) / "home"
    (home / ".config").mkdir(parents=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"PATH": "/usr/bin:/bin", "HOME": str(home),
                "XDG_CONFIG_HOME": str(home / ".config"),
                "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_CONFIG_SYSTEM": os.devnull,
                "GIT_CEILING_DIRECTORIES": os.path.dirname(temp),
                "TMPDIR": temp})
    repo = Path(temp) / "repo"
    git(env, "init", "-q", "-b", "fixture", str(repo))
    (repo / "fixture.txt").write_text("fixture\n", encoding="utf-8")
    git(env, "-C", str(repo), "add", "fixture.txt")
    git(env, "-C", str(repo), "-c", "user.name=fixture",
        "-c", "user.email=fixture@invalid", "-c", "commit.gpgsign=false",
        "commit", "-qm", "fixture")
