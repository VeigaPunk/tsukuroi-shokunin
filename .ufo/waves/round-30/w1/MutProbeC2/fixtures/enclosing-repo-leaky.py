#!/usr/bin/env python3
"""Discover/refuse an enclosing repo; optional mode isolates its fingerprint signal."""
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def clean_git_env(home):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"PATH": "/usr/bin:/bin", "HOME": home,
                "XDG_CONFIG_HOME": os.path.join(home, ".config"),
                "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_CONFIG_SYSTEM": os.devnull})
    return env


def make_private_repo(temp, env):
    repo = Path(temp) / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], env=env, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    (repo / "fixture.txt").write_text("fixture\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "-c", "core.excludesFile=/dev/null",
                    "add", "fixture.txt"], env=env, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=fixture",
                    "-c", "user.email=fixture@invalid", "-c", "commit.gpgsign=false",
                    "commit", "-qm", "fixture"], env=env, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


mode = sys.argv[1] if len(sys.argv) > 1 else "fail-on-discovery"
with tempfile.TemporaryDirectory(prefix="mutprobe-enclosing-") as temp:
    home = Path(temp) / "home"
    (home / ".config").mkdir(parents=True)
    env = clean_git_env(str(home))
    discovery = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                               cwd=os.getcwd(), env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    if discovery.returncode == 0 and mode != "--fingerprint-only":
        print("unexpected enclosing repository", file=sys.stderr)
        sys.exit(42)
    if discovery.returncode == 0:
        top = Path(discovery.stdout.decode().strip())
        marker = top / "MUTPROBE_FINGERPRINT.txt"
        marker.write_text("enclosing repo write\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(top), "add", marker.name], env=env,
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "-C", str(top), "-c", "user.name=fixture",
                        "-c", "user.email=fixture@invalid", "-c", "commit.gpgsign=false",
                        "commit", "-qm", "fixture enclosing write"], env=env, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    make_private_repo(temp, env)
