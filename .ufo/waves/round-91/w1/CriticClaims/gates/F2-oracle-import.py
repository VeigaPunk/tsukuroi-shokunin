#!/usr/bin/env python3
import argparse, hashlib, json, os, sys
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools")
# import battery helpers (oracle): r1_key, resource_name, b2, VALID_RESOURCES, EFI_PROTOCOLS, OPTIONAL
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("bat91", "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/limine-pin-battery-r91.py")
_b = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_b)
# reuse gate's split_key/parse_uri/on_panic etc by executing candidate gate as module (not subprocess)
_spec2 = _ilu.spec_from_file_location("gate", "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-limine-pins.py")
_g = _ilu.module_from_spec(_spec2); _spec2.loader.exec_module(_g)
ap = argparse.ArgumentParser()
ap.add_argument("--conf", required=True); ap.add_argument("--esp", required=True)
ap.add_argument("--secure-boot-enforced", choices=("0","1"), default=None)
ap.add_argument("--tpm-present", choices=("0","1"), default=None)
a = ap.parse_args()
r = _g.check(a.conf, a.esp, a.secure_boot_enforced=="1", a.tpm_present)
print(json.dumps(r, sort_keys=True))
sys.exit(r["rc"])
