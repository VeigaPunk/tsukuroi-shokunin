import re
IDIOM2 = re.compile(
    r'(?:^|[;&(){}!|]|\$\(|\b(?:if|elif|then|else|do|while|until|case|time)\b)\s*!?\s*'
    r'(?:command\s+|builtin\s+)?(?:printf|echo|cat)\b[^|\n]*\$(?:\{(?!#)|\(|[A-Za-z0-9_@*?!$-])[^|\n]*'
    r'\|\s*(?:grep\b[^|\n]*?\s-[A-Za-z]*[qm][A-Za-z]*\b|grep\b[^|\n]*?\s--(?:quiet|silent|max-count)\b'
    r'|head\s+(?:-n\s*1\b|-1\b|-n1\b))')
def strip_comment(ln):
    if ln.lstrip().startswith('#'):
        return ''
    q = None; depth = 0; i = 0
    while i < len(ln):
        ch = ln[i]
        if q == "'":
            if ch == "'":
                q = None
        elif ch == '\\':
            i += 2; continue
        elif q == '"':
            if ch == '"':
                q = None
        elif ch in '"\'':
            q = ch
        elif ch == '$' and i + 1 < len(ln) and ln[i + 1] == '{':
            depth += 1; i += 2; continue
        elif ch == '}' and depth:
            depth -= 1
        elif ch == '#' and depth == 0 and (i == 0 or ln[i - 1].isspace()):
            return ln[:i]
        i += 1
    return ln
def sites(text, strip, rx):
    return sum(1 for ln in text.split('\n') if rx.search(strip(ln)))
import sys
ns={}
src=open('matcher.py').read()
exec('import re\n'+src[src.index('IDIOM_RE = '):src.index('SUMMARY_RE')],ns)
OLD_RE=ns['IDIOM_RE']
exec(src[src.index('def strip_comment'):src.index('def selftest')],ns)
OLD_STRIP=ns['strip_comment']
for name in ['census-frozen.sh','census-base.sh','census-r50.sh']:
    t=open(name,encoding='utf-8',errors='replace').read()
    print(name, 'old', sites(t,OLD_STRIP,OLD_RE), 'new', sites(t,strip_comment,IDIOM2))
cases = {
 'bare printf|grep -q (must 1)': "printf '%s\\n' \"$out\" | grep -q 'x'",
 'F2 braced (must 1)': "    elif ! printf '%s\\n' \"${out}\" | grep -q 'host=fixture-host'; then",
 'F3 echo (must 1)': "    elif ! echo \"$out\" | grep -q 'host=fixture-host'; then",
 'grep -E -q (must 1)': "printf '%s\\n' \"$out\" | grep -E -q 'x'",
 'grep -m1 (must 1)': "printf '%s\\n' \"$out\" | grep -m1 'x' >/dev/null",
 'positional $1 (must 1)': "printf '%s\\n' \"$1\" | grep -q 'x'",
 '|| producer (must 1)': "out_has() { false || printf '%s\\n' \"$out\" | grep -q 'x'; }",
 'else producer (must 1)': "if false; then :; else printf '%s\\n' \"$out\" | grep -q 'x'; fi",
 'case ) producer (must 1)': "case $k in a) printf '%s\\n' \"$out\" | grep -q 'x' ;; esac",
 'command printf (must 1)': "command printf '%s\\n' \"$out\" | grep -q 'x'",
 'escaped-quote fake comment (must 1)': "    elif ! printf '%s\\n' \"a\\\" #\" \"$out\" | grep -q 'host=fixture-host'; then",
 'unquoted ${v/ #/} (must 1)': "    elif ! printf '%s\\n' ${out/ #/} | grep -q 'host=fixture-host'; then",
 'backslash continuation (must 1)': "    elif ! printf '%s\\n' \"$out\" \\\n      | grep -q 'x'; then",
 '${#out} length (must 0)': "    elif ! printf '%s\\n' \"${#out}\" | grep -q 'x'; then",
 '$# count (must 0)': "[ $# -eq 0 ] && printf '%s\\n' \"$out\" | grep -q x",
 'head -n6 bounded (must 0)': "x=$(printf '%s\\n' \"$CAP_OUT\" | grep '^?' | head -n6)",
 'grep -c (must 0)': "n=$(printf '%s\\n' \"$out\" | grep -c .)",
 'here-string grep -q (must 0)': "grep -qE -- \"$re\" <<<\"$out\" || miss=1",
}
for k,v in cases.items():
    print(f'{k:40s} old={1 if OLD_RE.search(OLD_STRIP(v)) else 0} new={1 if IDIOM2.search(strip_comment(v)) else 0}')
