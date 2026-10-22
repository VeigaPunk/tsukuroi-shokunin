#!/usr/bin/env python3
"""Intentionally inherits PATH and Git user configuration."""
import os
import subprocess
import tempfile
from pathlib import Path


def git(args, cwd):
    subprocess.run(["git", *args], cwd=cwd, env=os.environ, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


with tempfile.TemporaryDirectory(prefix="mutprobe-path-user-") as temp:
    repo = Path(temp) / "repo"
    repo.mkdir()
    git(["init", "-q"], repo)
    (repo / "fixture.txt").write_text("fixture\n", encoding="utf-8")
    git(["-c", "core.excludesFile=/dev/null", "add", "fixture.txt"], repo)
    git(["-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
         "-c", "commit.gpgsign=false", "commit", "-qm", "fixture"], repo)
