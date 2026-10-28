import re
exec(open('proposed.py').read().split("import sys")[0].replace("IDIOM2 = re.compile(", "IDIOM2_OLD = re.compile("))
IDIOM2 = re.compile(
    r'(?:^|[;&(){}!|]|\$\(|\b(?:if|elif|then|else|do|while|until|case|time)\b)\s*!?\s*'
    r'(?:command\s+|builtin\s+)?(?:printf|echo|cat)\b[^|\n]*\$(?:\{(?!#)|\(|[A-Za-z0-9_@*?!$-])[^|\n]*'
    r'\|\s*(?:grep\b[^|\n]*?\s(?:-[A-Za-z]*q[A-Za-z]*\b|--quiet\b|--silent\b|-[A-Za-z]*m\s*\d+\b|--max-count(?:=|\s+)\d+\b)'
    r'|head\s+(?:-n\s*1\b|-1\b|-n1\b))')
def sites(text):
    joined = re.sub(r'\\\n', ' ', text)
    return sum(1 for ln in joined.split('\n') if IDIOM2.search(strip_comment(ln)))
for name in ['census-frozen.sh','census-base.sh','census-r50.sh']:
    t=open(name,encoding='utf-8',errors='replace').read()
    print(name, 'new', sites(t))
tests = {
 'grep -m1 (must 1)': "printf '%s\\n' \"$out\" | grep -m1 'x' >/dev/null",
 'grep -m 1 (must 1)': "printf '%s\\n' \"$out\" | grep -m 1 'x' >/dev/null",
 'backslash continuation (must 1)': "    elif ! printf '%s\\n' \"$out\" \\\n      | grep -q 'x'; then",
 'F2 (must 1)': "    elif ! printf '%s\\n' \"${out}\" | grep -q 'host=fixture-host'; then",
 'grep -c (must 0)': "n=$(printf '%s\\n' \"$out\" | grep -c .)",
 'head -n6 (must 0)': "x=$(printf '%s\\n' \"$CAP_OUT\" | grep '^?' | head -n6)",
}
for k,v in tests.items(): print(f'{k:34s} {sites(v)}')
