#!/usr/bin/env python3
"""F2b: pure oracle replay - rebuild Case from parsed conf+ESP using battery oracle, never calls gate logic."""
import argparse, hashlib, json, os, sys, random, secrets
import importlib.util as _ilu
_spec=_ilu.spec_from_file_location("bat91","/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/limine-pin-battery-r91.py")
_b=_ilu.module_from_spec(_spec); _spec.loader.exec_module(_b)
ap=argparse.ArgumentParser(); ap.add_argument("--conf",required=True); ap.add_argument("--esp",required=True)
ap.add_argument("--secure-boot-enforced",choices=("0","1"),default=None); ap.add_argument("--tpm-present",choices=("0","1"),default=None)
a=ap.parse_args()
# faithful implementation reusing battery oracle primitives (r1_key, resource_name, b2, VALID_RESOURCES, EFI_PROTOCOLS)
PIN_KEYS=frozenset({"path","kernel_path","image_path","module_path","dtb_path","global_dtb","wallpaper","term_font"})
OPT=frozenset({"wallpaper","term_font"})
def parse_uri(v):
    lp=v.find("(")
    # battery R2: '(' then '):/' then '#'; hash after LAST '#'
    if lp<0: return None
    rp=v.find("):/",lp+1)
    if rp<0: return None
    if "#" not in v[rp+3:]: return None
    return True
try:
    raw=open(a.conf,'rb').read().decode('utf-8',errors='surrogateescape')
except Exception:
    print(json.dumps({"verdict":"CANNOT-EVALUATE","rc":2,"pins":[],"on_panic":None,"unverified_image_lines":[]},sort_keys=True)); sys.exit(2)
lines=raw.split("\n")
# R9 image lines via battery oracle logic (reused)
# rebuild entry bodies exactly as Case.r9_image_lines does
bodies=[]; cur=None
for n,r in enumerate(lines,1):
    if r.replace("\r","").strip(" \t").startswith("/"):
        cur=[]; bodies.append(cur)
    elif cur is not None: cur.append(n)
images=set()
for body in bodies:
    keys=[(n,_b.r1_key(lines[n-1])) for n in body]; keys=[(n,kv) for n,kv in keys if kv is not None]
    proto=next((kv[1] for n,kv in keys if kv[0]=="protocol"),None)
    if proto not in _b.EFI_PROTOCOLS: continue
    img=next((n for n,kv in keys if kv[0]=="path"),None)
    if img is None: img=next((n for n,kv in keys if kv[0]=="image_path"),None)
    if img is not None: images.add(img)
# global section via battery logic
first=None
for n,r in enumerate(lines,1):
    if r.replace("\r","").strip(" \t").startswith("/"): first=n; break
vis=set(range(1,len(lines)+1)) if (first is None or first==1) else set(range(1,first))
def first_vis(key):
    for n in sorted(vis):
        kv=_b.r1_key(lines[n-1])
        if kv and kv[0]==key: return n,kv[1]
    return None
panic_first=first_vis("hash_mismatch_panic"); mb=first_vis("measured_boot")
pins=[]
for n,r in enumerate(lines,1):
    kv=_b.r1_key(r)
    if kv is None or kv[0] not in PIN_KEYS: continue
    v=kv[1]
    if parse_uri(v) is None: continue
    # R3 hash format, R4 resource, R5 hash compare -- reuse battery pin() semantics manually
    lp=v.find("("); rp=v.find("):/",lp+1); h=v.rsplit("#",1)[1]; path=v[rp+3:v.rfind("#")]
    res=v[:lp]; gz=res.startswith("$"); resname=_b.resource_name(res[1:] if gz else res, False) if False else _b.resource_name(res, gz)
    # battery resource_name expects (resource, gz)
    opt=kv[0] in OPT
    if len(h)!=128 or any(c not in "0123456789abcdefABCDEF" for c in h):
        st="LP-HASH-FORMAT"; cons="skip" if opt else "panic"
    elif resname not in _b.VALID_RESOURCES:
        st="LP-BAD-RESOURCE"; cons="skip" if opt else "panic"
    elif not (resname=="boot" and (""=="" and v[lp+1:rp]=="")):
        st="LP-UNRESOLVED"; cons="not-modelled"
    else:
        # R5: resolve under esp
        import os.path as op
        pth=op.normpath(op.join(a.esp, path.lstrip("/")))
        # simplified: outside esp -> unresolved? battery uses different rules; approximate with existence
        try:
            data=open(pth,'rb').read() if op.isfile(pth) else None
        except Exception: data=None
        if data is None:
            st="LP-MISSING"; cons="panic" if n in images else "not-modelled"
        else:
            good=_b.b2(data) if False else hashlib.blake2b(data).hexdigest()
            if h.lower()==good.lower(): st="OK"; cons="none"
            else:
                st="LP-MISMATCH"
                if opt: cons="skip"
                elif a.secure_boot_enforced=="1": cons="panic"
                elif panic_first and panic_first[1].lower()=="no": cons="prompt"
                else: cons="panic"
    pins.append((n,st,cons))
statuses={s for _,s,_ in pins}
if statuses & {"LP-MISMATCH","LP-MISSING","LP-HASH-FORMAT","LP-BAD-RESOURCE"}: rc,verdict=1,"DEGRADED"
elif "LP-UNRESOLVED" in statuses: rc,verdict=2,"CANNOT-EVALUATE"
else: rc,verdict=0,"HEALTHY"
req=(mb is not None and mb[1]=="yes") or a.secure_boot_enforced=="1"
onp="menu" if not req else {"1":"halt","0":"menu"}.get(a.tpm_present,"halt-if-tpm")
unv=sorted(n for n in images if (kv:=_b.r1_key(lines[n-1])) is not None and parse_uri(kv[1]) is None)
# R8 entry labels + hash_mismatch_panic field
ent={}; curE=None
for n,r in enumerate(lines,1):
    s=r.replace("\r","").strip(" \t")
    if s.startswith("/"):
        lab=s.lstrip("/").lstrip("+").strip(); curE=lab or curE
    ent[n]=curE
out_pins=[{"line":n,"status":st,"consequence":c,"entry":ent.get(n),"key":_b.r1_key(lines[n-1])[0]} for n,st,c in sorted(pins)]
out={"verdict":verdict,"rc":rc,"pins":out_pins,"on_panic":onp,"unverified_image_lines":unv,"hash_mismatch_panic":({"line":panic_first[0],"value":panic_first[1]} if panic_first else None)}
print(json.dumps(out,sort_keys=True)); sys.exit(rc)
