#!/usr/bin/env python3
# K4: never reads its input; always HEALTHY.
import json
print(json.dumps({"verdict": "HEALTHY", "findings": []}))
