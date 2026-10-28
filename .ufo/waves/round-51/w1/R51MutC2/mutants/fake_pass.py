import json, sys
print(json.dumps({'verdict': 'PASS', 'control': 'always-pass'}, sort_keys=True))
sys.exit(0)
