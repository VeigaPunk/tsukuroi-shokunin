#!/usr/bin/env bash
# recheck-drift-r54 — one committed read-only command that re-verifies the drift register
# (corpus/knowledge/host-transition-drift-r53.md, rows D1-D12, observed 2026-10-31) against the
# live host. Rounds 1-53 carried the recheck loop only as prose in the register's `recheck:` line,
# the PROVINCE host-transition record and the SKILL round-53 section; this script is that loop,
# executable (AXES operability signal) in service of freshness.
#
# Usage: bash tools/recheck-drift-r54.sh [--receipt PATH] [--budget SECONDS]
#   Emits one line per register row:  D<k> match|drift|doc-row <evidence>
#   Rollup:  RECHECK_DRIFT: PASS (12 rows, H host-probed match, DOC doc rows, 0 drift)  rc 0
#            RECHECK_DRIFT: FAIL  (N drift)                                            rc 1
#   A drift line is honest output, not a crash: it owes an appended register correction next.
#   --budget SECONDS (round 56): the D7 leg's wall-clock budget; default 90 (the register's
#   recorded class). The 420 s class runs without editing this script; the D7 match predicate
#   is budget-independent (the old census selftest does not complete: rc 124, 0 FAIL, no
#   summary at either budget — .ufo/waves/round-54/d7-receipts/).
#
# Read-only: every probe is command -v / version / grep / the census path plane. The D7 leg runs
# the old census selftest under `timeout <budget>` (GNU coreutils) with output to a temp file that
# is deleted; its durable 90 s/420 s receipts live at .ufo/waves/round-54/d7-receipts/ (round-54
# re-derivation). --receipt writes the output copy to a lane-tree path; nothing else is written.
# Spell `python`, not `python3` (register D8). Owner: tsukuroi.
set -u
cd "$(dirname "$0")/.." || exit 2
REG=corpus/knowledge/host-transition-drift-r53.md
PROV=PROVINCE.md
receipt=""
budget=90
while [ $# -gt 0 ]; do
  case "$1" in
    --receipt) receipt="${2:?--receipt needs a path}"; shift 2 ;;
    --budget)  budget="${2:?--budget needs seconds}"; shift 2 ;;
    *) echo "usage: recheck-drift-r54.sh [--receipt PATH] [--budget SECONDS]" >&2; exit 2 ;;
  esac
done
case "$budget" in ''|*[!0-9]*|0) echo "--budget needs a positive integer (seconds)" >&2; exit 2 ;; esac

drift=0; matched=0; docrows=0
lines_out=""
emit() { lines_out="${lines_out}${1}
"; }

# D1-D6: Linux-class tools absent here
i=1
for t in pacman systemctl journalctl btrfs nvidia-smi jq; do
  if command -v "$t" >/dev/null 2>&1; then
    emit "D$i drift ($t now resolves)"; drift=$((drift+1))
  else
    emit "D$i match ($t absent)"; matched=$((matched+1))
  fi
  i=$((i+1))
done

# D7: old census selftest does not complete under the budget (timeout, partial PASS list, no summary)
tmp7="$(mktemp "${TMPDIR:-/tmp}/recheck-d7.XXXXXX")"
timeout "$budget" bash tools/tsukuroi-census.sh --selftest >"$tmp7" 2>&1
rc7=$?
pass7=$(grep -c "^PASS " "$tmp7")
fail7=$(grep -c "^FAIL " "$tmp7")
summ7=$(grep -c "SELFTEST: PASS (" "$tmp7")
rm -f "$tmp7"
if [ "$rc7" -eq 124 ] && [ "$fail7" -eq 0 ] && [ "$summ7" -eq 0 ]; then
  emit "D7 match (timeout rc 124, partial: ${pass7} PASS / 0 FAIL / no summary line; budget ${budget}s; durable receipts .ufo/waves/round-54/d7-receipts/)"; matched=$((matched+1))
else
  emit "D7 drift (rc=$rc7 pass=$pass7 fail=$fail7 summary=$summ7 — register recorded rc 124 partial at the 90s/420s classes)"; drift=$((drift+1))
fi

# D8: python3 is the Store alias stub (nonzero rc), python is real
if command -v python3 >/dev/null 2>&1; then
  python3 --version >/dev/null 2>&1; p3rc=$?
else
  p3rc=127
fi
python --version > /tmp/r54-pyv 2>&1; pyrc=$?
pyv="$(cat /tmp/r54-pyv 2>/dev/null || true)"; rm -f /tmp/r54-pyv
if [ "$p3rc" -ne 0 ] && [ "$pyrc" -eq 0 ] && printf '%s' "$pyv" | grep -q "Python 3\.13"; then
  emit "D8 match (python3 rc ${p3rc} stub-class, python: ${pyv})"; matched=$((matched+1))
else
  emit "D8 drift (python3 rc=$p3rc python rc=$pyrc: $pyv — register recorded stub rc 49 + Python 3.13)"; drift=$((drift+1))
fi

# D9: census path plane still DEGRADED (register: 51 entries, 3 missing, 5 dup values, fnm entry)
# census line format: "PLANE path DEGRADED entries=51 missing=3 dup_values=5 empty=0" (no key=value pair)
census_line="$(python tools/win-host-census-r53.py 2>/dev/null | grep '^PLANE path')"
case "$census_line" in
  *" path DEGRADED "*) emit "D9 match (${census_line})"; matched=$((matched+1)) ;;
  *" path GREEN "*|*" path BLOCKED "*) emit "D9 drift (${census_line} — register recorded DEGRADED)"; drift=$((drift+1)) ;;
  *) emit "D9 drift (census path plane line not recognized: '${census_line}' — register recorded PLANE path DEGRADED)"; drift=$((drift+1)) ;;
esac

# D10: PROVINCE carries the dated host-transition record (doc row)
if grep -q "Round-53 host transition" "$PROV" && grep -q "^| D10" "$REG"; then
  emit "D10 doc-row (PROVINCE host-transition record + register row present)"; docrows=$((docrows+1))
else
  emit "D10 drift (PROVINCE record or register row missing)"; drift=$((drift+1))
fi

# D11: index-free plumbing binding recorded (doc row)
if grep -q "treecommit.py" "$REG"; then
  emit "D11 doc-row (register row names the plumbing helper; contract §0 binding unchanged this round)"; docrows=$((docrows+1))
else
  emit "D11 drift (register row lost the helper name)"; drift=$((drift+1))
fi

# D12: node resolves into a per-session fnm_multishells directory
nodep="$(command -v node 2>/dev/null || true)"
case "$nodep" in
  *fnm_multishells*) emit "D12 match (node: ${nodep})"; matched=$((matched+1)) ;;
  "") emit "D12 drift (node no longer resolves)"; drift=$((drift+1)) ;;
  *) emit "D12 drift (node now resolves elsewhere: ${nodep} — register recorded fnm_multishells)"; drift=$((drift+1)) ;;
esac

rollup="RECHECK_DRIFT: PASS (12 rows, ${matched} host-probed match, ${docrows} doc rows, 0 drift)"
rc=0
if [ "$drift" -ne 0 ]; then
  rollup="RECHECK_DRIFT: FAIL (${drift} drift)"
  rc=1
fi
out="${lines_out}${rollup}
"
printf '%s' "$out"
if [ -n "$receipt" ]; then
  mkdir -p "$(dirname "$receipt")"
  printf 'recheck_drift_r54=1\ndate_utc=%s\nbudget_s=%s\nhost_probes_matched=%s\ndoc_rows=%s\ndrift=%s\n---\n%s' \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$budget" "$matched" "$docrows" "$drift" "$out" > "$receipt" \
    || { echo "cannot write receipt $receipt" >&2; exit 2; }
fi
exit $rc
