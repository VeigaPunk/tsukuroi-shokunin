import json, sys
print(json.dumps({'verdict': 'FAIL', 'control': 'always-fail'}, sort_keys=True))
sys.exit(1)
