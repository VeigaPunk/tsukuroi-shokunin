import re
src=open('matcher.py').read()
ns={}
exec("import re\n"+src[src.index("IDIOM_RE = "):src.index("SUMMARY_RE")], ns)
exec(src[src.index("def strip_comment"):src.index("def selftest")], ns)
IDIOM_RE=ns['IDIOM_RE']; strip=ns['strip_comment']
frozen=open('census-frozen.sh',encoding='utf-8').read()
print('BAD count', frozen.count("  bad() { FAIL=$((FAIL + 1)); printf 'FAIL %s\\n' \"$*\" >&2; }"))
print('ARM count', frozen.count("    elif ! out_has 'host=fixture-host'; then"))
print('needle M1', frozen.count('  roll=$(worse "$roll" "$OOM_V")\n'), 'M2', frozen.count('    DEGRADED) exit 1 ;;\n'))
print('OOM_V occurrences', frozen.count('OOM_V'))
cases = {
 'bare printf|grep -q': "printf '%s\\n' \"$out\" | grep -q 'x'",
 'grep -E -q (flag order)': "printf '%s\\n' \"$out\" | grep -E -q 'x'",
 'grep -m1 (no -q)': "printf '%s\\n' \"$out\" | grep -m1 'x' >/dev/null",
 'positional $1 producer': "printf '%s\\n' \"$1\" | grep -q 'x'",
 '|| producer': "out_has() { false || printf '%s\\n' \"$out\" | grep -q 'x'; }",
 'else producer': "if false; then :; else printf '%s\\n' \"$out\" | grep -q 'x'; fi",
 'case ) producer': "case $k in a) printf '%s\\n' \"$out\" | grep -q 'x' ;; esac",
 'command printf': "command printf '%s\\n' \"$out\" | grep -q 'x'",
 'escaped-quote then fake comment': "    elif ! printf '%s\\n' \"a\\\" #\" \"$out\" | grep -q 'host=fixture-host'; then",
 '${v/ #/} unquoted with space-hash': "    elif ! printf '%s\\n' ${out/ #/} | grep -q 'host=fixture-host'; then",
 '${#out} (must be a site)': "    elif ! printf '%s\\n' \"${#out}\" | grep -q 'x'; then",
 '$# in test (must not be a site)': "[ $# -eq 0 ] && printf '%s\\n' \"$out\" | grep -q x",
 'backslash-continuation': "    elif ! printf '%s\\n' \"$out\" \\\n      | grep -q 'x'; then",
 'F2 braced-spell': "    elif ! printf '%s\\n' \"${out}\" | grep -q 'host=fixture-host'; then",
 'F3 echo-spell': "    elif ! echo \"$out\" | grep -q 'host=fixture-host'; then",
}
for k,v in cases.items():
    print(f'{k:36s} sites={1 if IDIOM_RE.search(strip(v)) else 0}')
# broad scan of frozen census: any producer/early-exit pipe, whatever the consumer spelling
broad=re.compile(r'\b(printf|echo|cat)\b[^|\n]*\|\s*(grep|head|awk|sed|tr|cut)\b[^\n]*')
print('--- frozen broad producer|consumer lines (producer uses $) ---')
for i,l in enumerate(frozen.split('\n'),1):
    s=strip(l)
    m=broad.search(s)
    if m and '$' in m.group(0) and re.search(r'grep\s+-\S*q|grep\s+-[a-zA-Z]*m|head|-m\s*1|grep\s+-[A-Za-z]+\s+-q|-e\b',m.group(0)):
        print(i, l.strip()[:150])
