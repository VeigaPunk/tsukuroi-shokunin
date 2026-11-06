import json, sys

AVAIL=["HR-HIBERNATE-DISABLED","HR-LOCKDOWN-BLOCKS","HR-NORESUME-ARG"]
IDS=AVAIL+["HR-NO-RESUME-ARG","HR-OFFSET-MISSING","HR-OFFSET-MISMATCH","HR-SWAPFILE-COW",
 "HR-NO-ACTIVE-SWAP","HR-SYSFS-DEVICE-MISMATCH","HR-SYSFS-OFFSET-MISMATCH","HR-NO-RESUME-HOOK",
 "HR-HOOK-BEFORE-ENCRYPT","HR-SWAP-TOO-SMALL","HR-NO-DISK-STATE"]

def norm(s): return s.replace('-','_')
def matches(t,S): return len(t)>=len(S) and norm(t[:len(S)])==norm(S)

def need(cond):  # CANNOT-EVALUATE guard
    if not cond: raise ValueError

def is_int(v): return isinstance(v,int) and not isinstance(v,bool)
def is_str(v): return isinstance(v,str)
def opt(pred):
    return lambda v: v is None or pred(v)

REQ={"schema":is_str,"cmdline":is_str,"swaps":lambda v:isinstance(v,list),
 "resume_swapfile":opt(is_str),"map_swapfile_offset":opt(is_int),
 "swapfile_attrs":opt(is_str),"resume_dev_majmin":opt(is_str),
 "sys_power_resume":opt(is_str),"sys_power_resume_offset":opt(is_int),
 "sys_power_state":is_str,"image_size":is_int,"hooks":lambda v:isinstance(v,list),
 "lockdown":opt(is_str)}

def evaluate(f):
    try:
        need(f.get("schema")=="resume-facts/2")
        for k,p in REQ.items():
            need(k in f)
            need(p(f[k]))
        for sw in f["swaps"]:
            need(isinstance(sw,dict) and is_int(sw.get("size_kib")) and is_int(sw.get("used_kib")))
        for h in f["hooks"]: need(is_str(h))
        lock=f["lockdown"]
        if lock is not None:
            words=lock.split()
            br=[w for w in words if len(w)>=3 and w[0]=='[' and w[-1]==']']
            need(len(br)==1)
    except (ValueError,TypeError):
        return (2,"CANNOT-EVALUATE",[])

    toks=f["cmdline"].split()
    finds=set()
    hib=[]  # A1
    # collect
    nohib_token=any(matches(t,"nohibernate") for t in toks)
    hibval=[t[len("hibernate="):] for t in toks if matches(t,"hibernate=")]
    nores_token=any(matches(t,"noresume") for t in toks)
    a1 = nohib_token or any(v.startswith("no") and not (v.startswith("noresume") or v.startswith("nocompress")) for v in hibval)
    if a1: finds.add("HR-HIBERNATE-DISABLED")
    lock=f["lockdown"]
    if lock is not None:
        for w in lock.split():
            if w.startswith("[") and w.endswith("]") and w[1:-1] in ("integrity","confidentiality"):
                finds.add("HR-LOCKDOWN-BLOCKS")
    a3tok = nores_token or any(v.startswith("noresume") for v in hibval)
    if a3tok and not a1: finds.add("HR-NORESUME-ARG")

    res=[t[len("resume="):] for t in toks if matches(t,"resume=")]
    r = res[-1] if res else None
    offs=[t[len("resume_offset="):] for t in toks if matches(t,"resume_offset=") and t[len("resume_offset="):len("resume_offset=")+1].isdigit()]
    o = int(''.join(c for c in offs[-1] if c.isdigit())) if offs else None
    # leading decimal digits only
    if offs:
        digits=[]
        for c in offs[-1]:
            if c.isdigit(): digits.append(c)
            else: break
        o=int(''.join(digits))

    if r is None or r=="":
        finds.add("HR-NO-RESUME-ARG")
    else:
        sf=f["resume_swapfile"]
        if sf is not None:
            if o is None: finds.add("HR-OFFSET-MISSING")
            if o is not None and f["map_swapfile_offset"] is not None and o!=f["map_swapfile_offset"]:
                finds.add("HR-OFFSET-MISMATCH")
            attrs=f["swapfile_attrs"]
            if attrs is not None and 'C' not in attrs: finds.add("HR-SWAPFILE-COW")
        if not f["swaps"]: finds.add("HR-NO-ACTIVE-SWAP")
        if f["resume_dev_majmin"] is not None and f["resume_dev_majmin"]!=f["sys_power_resume"]:
            finds.add("HR-SYSFS-DEVICE-MISMATCH")
        if o is not None and o!=f["sys_power_resume_offset"]:
            finds.add("HR-SYSFS-OFFSET-MISMATCH")
        hooks=f["hooks"]
        def has(h): return any(h in x for x in hooks)
        if not has("resume") and not has("systemd"): finds.add("HR-NO-RESUME-HOOK")
        if has("resume") and has("encrypt"):
            ri=[i for i,x in enumerate(hooks) if "resume" in x]
            ei=[i for i,x in enumerate(hooks) if "encrypt" in x]
            if ri and ei and min(ri)<min(ei): finds.add("HR-HOOK-BEFORE-ENCRYPT")
        if f["swaps"] and sum((s["size_kib"]-s["used_kib"])*1024 for s in f["swaps"]) < f["image_size"]:
            finds.add("HR-SWAP-TOO-SMALL")
        if "disk" not in f["sys_power_state"].split(): finds.add("HR-NO-DISK-STATE")
    fl=sorted(finds)
    return (1,"DEGRADED",fl) if fl else (0,"HEALTHY",[])

if __name__=="__main__":
    d=json.load(open(sys.argv[1]))
    bad=[]
    for c in d["case_log"]:
        got=evaluate(c["facts"]); want=c["want"]
        if list(got)!=list(want): bad.append((c["base"],c["family"],c["facts"]["cmdline"],want,got))
    print(f"cases={len(d['case_log'])} disagreements={len(bad)}")
    import collections
    print(collections.Counter(b[1] for b in bad))
    for b in bad[:15]: print(json.dumps(b)[:400])
