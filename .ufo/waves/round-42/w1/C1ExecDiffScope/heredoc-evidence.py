import sys, datetime
import diffscope as d
bl=d.load("base.sh"); il=d.load("impl.sh")
fb,hb=d.scan(bl); fi,hi=d.scan(il)
chg=[692,693,694,695,697,1624,1638,1639,1644,1645,1655]+list(range(2350,2360))+list(range(2556,2568))
print("## heredoc-vs-changed-line check", datetime.datetime.utcnow().isoformat()+"Z")
print("changed impl lines that are heredoc content:", [n for n in chg if n in hi] or "none")
print("changed base lines that are heredoc content:", [n for n in [692,694,1621,1635,1636,1641,1642,1652] if n in hb] or "none")
print("impl run_selftest span:", [f for f in fi if f[0]=="run_selftest"])
print("impl probe_storage_arm span:", [f for f in fi if f[0]=="probe_storage_arm"])
print("heredoc content line count:", len(hi))
ln=[l for l in il]
import re
print("dispatch heredoc opener line:", [i+1 for i,l in enumerate(ln) if "cat > \"$bin/.dispatch\"" in l])
print("line 2013 repr:", repr(ln[2012]))
print("rc_of/out_of lines:", [i+1 for i,l in enumerate(ln) if re.match(r"^(rc_of|out_of)\(\)", l)])
