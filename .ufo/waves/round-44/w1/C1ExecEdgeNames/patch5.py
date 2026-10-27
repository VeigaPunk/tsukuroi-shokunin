import sys
src = open(sys.argv[1]).read()
old = '''        v=\'\' nl=0
        while IFS= read -r line || [ -n "$line" ]; do nl=$((nl + 1)); v=$line; done < "$f"
        if [ "$nl" -ne 1 ] || ! [[ $v =~ ^[0-9]+$ ]]; then
          blocked=1; detail+="$fs8:${dev##*/}:speed-malformed,"; continue
        fi
'''
new = '''        v=\'\' rest=\'\'
        { IFS= read -r -n 33 v || [ -n "$v" ] || true          # bounded: 20 digits + \\n + slack
          IFS= read -r -N 1 rest || [ -n "$rest" ] || true; } < "$f"   # any further byte = not one number
        if [ "${#v}" -ge 33 ] || [ -n "$rest" ] || ! [[ $v =~ ^[0-9]+$ ]]; then
          blocked=1; detail+="$fs8:${dev##*/}:speed-malformed,"; continue
        fi
'''
assert src.count(old) == 1, src.count(old)
open(sys.argv[2], 'w').write(src.replace(old, new))
print("patched")
