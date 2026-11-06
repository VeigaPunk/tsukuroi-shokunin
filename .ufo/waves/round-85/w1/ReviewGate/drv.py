import copy, json, os, subprocess, sys, tempfile
GATE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-hibernate-resume.py"
BASE = json.load(open("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-85/before/host/facts-v2.json"))
S = os.environ["S"]

def run(doc, tag, expect):
    d = tempfile.mkdtemp(dir=S + "/fx"); p = os.path.join(d, "f.json")
    with open(p, "w") as fh: json.dump(doc, fh)
    r = subprocess.run([sys.executable, GATE, "--facts", p], capture_output=True, text=True)
    got = (r.returncode, r.stdout.strip())
    mark = "OK " if expect in r.stdout and (r.returncode == int(expect.split("(")[0]) if expect.startswith("rc") else True) else "?? "
    print(f"{tag:38} rc={r.returncode} {r.stdout.strip()}")

def t(tag, cmdline=None, lockdown="__keep__", drop_lockdown=False, expect=""):
    f = copy.deepcopy(BASE)
    if cmdline is not None: f["cmdline"] = cmdline
    if drop_lockdown: f.pop("lockdown")
    elif lockdown != "__keep__": f["lockdown"] = lockdown
    run(f, tag, expect)

CL = BASE["cmdline"]
def plus(*toks): return CL + " " + " ".join(toks)
def noresume_tok(): return " ".join(x for x in CL.split() if not x.startswith("resume="))

t("T1  +nohibernate",             plus("nohibernate"),           expect="HR-HIBERNATE-DISABLED")
t("T2  +nohibernate +noresume",   plus("nohibernate", "noresume"),expect="HR-HIBERNATE-DISABLED")
t("T3  +hibernate=no",            plus("hibernate=no"),          expect="HR-HIBERNATE-DISABLED")
t("T4  +hibernate=nocompress",    plus("hibernate=nocompress"),  expect='"findings": [], "verdict": "HEALTHY"')
t("T5  +hibernate=noresume",      plus("hibernate=noresume"),    expect="HR-NORESUME-ARG")
t("T6  +hibernate=noresumeX",     plus("hibernate=noresumeX"),   expect="HR-NORESUME-ARG")
t("T7  +hibernate=nofoobar",      plus("hibernate=nofoobar"),    expect="HR-HIBERNATE-DISABLED")
t("T8  +noresume",                plus("noresume"),              expect="HR-NORESUME-ARG")
t("T9  +noresume=1  [L1]",        plus("noresume=1"),            expect='"findings": [], "verdict": "HEALTHY"')
t("T10 +nohibernate=1 [L1]",      plus("nohibernate=1"),         expect='"findings": [], "verdict": "HEALTHY"')
t("T11 +noresumefoo [L1]",        plus("noresumefoo"),           expect='"findings": [], "verdict": "HEALTHY"')
t("T12 lockdown [integrity]",     lockdown="none [integrity] confidentiality", expect="HR-LOCKDOWN-BLOCKS")
t("T13 lockdown [confidentiality]",lockdown="none integrity [confidentiality]", expect="HR-LOCKDOWN-BLOCKS")
t("T14 lockdown null",            lockdown=None,                 expect='"findings": [], "verdict": "HEALTHY"')
t("T15a lockdown 0",              lockdown=0,                    expect="CANNOT-EVALUATE")
t("T15b lockdown [\"none\"]",     lockdown=["none"],             expect="CANNOT-EVALUATE")
t("T15c lockdown true",           lockdown=True,                 expect="CANNOT-EVALUATE")
t("T15d lockdown \"\"",           lockdown="",                   expect="CANNOT-EVALUATE")
t("T15e lockdown unbracketed",    lockdown="none integrity confidentiality", expect="CANNOT-EVALUATE")
t("T15f lockdown two brackets",   lockdown="[none] [integrity] confidentiality", expect="CANNOT-EVALUATE")
t("T15g lockdown [none]",         lockdown="[none]",             expect='"findings": [], "verdict": "HEALTHY"')
t("T15h lockdown key dropped",    drop_lockdown=True,            expect="CANNOT-EVALUATE")
t("T16 resume= empty [L3]",       CL.replace("resume=/dev/mapper/root ", "resume= ", 1), expect='"findings": [], "verdict": "HEALTHY"')
t("T17 no-resume + noresume",     noresume_tok() + " noresume",  expect="HR-NO-RESUME-ARG")
t("T18 dup resume_offset last wins", "resume_offset=1 " + CL,    expect='"findings": [], "verdict": "HEALTHY"')
t("T19 resume_offset=abc",        CL.replace("resume_offset=3795013", "resume_offset=abc"), expect="CANNOT-EVALUATE")
t("T20 noresume + no resume= + [integrity]", noresume_tok() + " noresume", lockdown="none [integrity] confidentiality", expect="HR-LOCKDOWN-BLOCKS")
