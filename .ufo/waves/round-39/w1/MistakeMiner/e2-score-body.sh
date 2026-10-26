#!/usr/bin/env bash
set -euo pipefail
S=$1
score() {
  local label=$1 counter=$2 rev out
  rev=deadbeef
  out=$(TMPDIR=$S python3 "$counter" --repo x --revision "$rev" 2>/dev/null || true)
  OUT_JSON=$out python3 - "$label" "$counter" "$rev" "sha" <<'EOF'
import json, sys
label, counter, rev, sha = sys.argv[1:5]
import os
r = json.loads(os.environ['OUT_JSON'])
keep = {k: r.get(k) for k in ('hidden_matched', 'views_matched', 'fixtures_matched', 'live_match', 'six_planes_all',
                              'rules_verified', 'duplicate_rows', 'duplicate_headings', 'source_ok', 'counts_ok',
