#!/usr/bin/python3
"""Bounded direct invocation of the actual boot-chain git child builder."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--tool', required=True)
parser.add_argument('--repo', required=True)
parser.add_argument('--stage', required=True)
args = parser.parse_args()
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(args.tool).parent))
spec = importlib.util.spec_from_file_location('c08_boot_chain', args.tool)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
proc = module.git('--version', repo=args.repo)
print(json.dumps({'stage': args.stage, 'cwd': os.getcwd(), 'file': module.__file__,
                  'tool_sha256': hashlib.sha256(Path(args.tool).read_bytes()).hexdigest(),
                  'git_exit': proc.returncode, 'git_stdout': proc.stdout.decode().strip(),
                  'ambient_marker_at_parent': os.environ.get('ZZ_R34_AMBIENT')}))
sys.exit(proc.returncode)
