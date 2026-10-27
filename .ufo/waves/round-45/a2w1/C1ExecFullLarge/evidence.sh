#!/usr/bin/env bash
# Evidence dump for the C1-10 report: every line below is a command's observed output.
set +e
S=/fast/scratch/hyaku/tsukuroi-r45/C1ExecFullLarge
cd "$S"
echo '## census revisions under test'
sha256sum rev/base/tools/tsukuroi-census.sh rev/impl/tools/tsukuroi-census.sh
echo '## base reader line numbers (5bbd5ff5)'
grep -n "state=\$(printf\|r=\$(printf\|driver=\$(printf\|t_word=\$(printf" rev/base/tools/tsukuroi-census.sh
echo '## stub output size at PAD_LINES=4000 (systemctl --user is-system-running)'
FX=$S/fx PAD_LINES=4000 "$S/bin/systemctl" --user is-system-running --no-pager | wc -c
echo '## stub output at PAD_LINES=0'
FX=$S/fx PAD_LINES=0 "$S/bin/systemctl" --user is-system-running --no-pager | od -c | head -1
echo '## run exit codes'
for f in base-large base-small impl-large impl-small impl-small2 base-large-calls impl-large-calls; do
  printf '%-18s rc=%s stdout_bytes=%s stderr_bytes=%s\n' "$f" "$(cat $f.rc)" "$(wc -c < $f.out)" "$([ -f $f.err ] && wc -c < $f.err || echo 0)"
done
echo '## base-large stdout (whole)'
cat base-large.out
echo '## base-large stderr (whole)'
cat base-large.err
echo '## impl-large PLANE/HANDOFF/DRIFT/STORAGE/SCRUB/rollup lines'
grep -E '^(PLANE|HANDOFF|DRIFT|STORAGE|SCRUB|TSUKUROI_CENSUS)' impl-large.out
echo '## diff impl-large vs impl-small, body only (header timestamp line 1 dropped)'
diff <(tail -n +2 impl-large.out) <(tail -n +2 impl-small.out) && echo 'IDENTICAL_BODY'
echo '## diff impl-small vs impl-small2, body only (live-drift repeat check)'
diff <(tail -n +2 impl-small.out) <(tail -n +2 impl-small2.out) && echo 'IDENTICAL_BODY_REPEAT'
echo '## diff base-small vs impl-large, body only'
diff <(tail -n +2 base-small.out) <(tail -n +2 impl-large.out) && echo 'SAME_OUTPUT_BASE_VS_IMPL'
echo '## stub calls, base run (PAD 4000)'
cat calls-base.log
echo '## stub calls, impl run (PAD 4000)'
cat calls-impl.log
echo '## per-site probe (264 KB CAP_OUT, base statement vs impl statement)'
cat siteprobe.out
echo '## SIGPIPE threshold sweep (base S1 statement)'
cat threshold.out
echo '## base xtrace: line numbers reached, last trace line'
grep -oE 'rev/base/tools/tsukuroi-census\.sh:[0-9]+:' base-large-xtrace.trace | sort -u | tail -3
tail -1 base-large-xtrace.trace | cut -c1-200
