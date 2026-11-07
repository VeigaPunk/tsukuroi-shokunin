# HASH-LENGTH draw: considered, measured NOT a roster flake risk (optional hardening only)
# File: tools/limine-pin-battery-r89.py (frozen candidate; nothing applied)
# Measured at lane master 665408cc45a88ed49717e22f4593e8e6152ac665, battery sha256 3bae11e939cf6900fd29bb24033e6d134de8bf0ae7069cdec3f12f716e8df7f8
#
# The family draws ONE bad length per case from {127, 129, 64, 0} (line 298) with CASES_PER_FAMILY = 4
# (line 911), so a gate could in principle escape if the length that exposes it is never drawn
# ((3/4)^4 = 31.6% per run). The roster does not contain such a gate:
#   m06-hash-127 is `if len(h) != 127 or not set(h) <= HEXDIGITS` -> rejects every ordinary 128-hex
#   hash, and m07-hash-129 is `if len(h) != 129 ...` -> rejects every ordinary 128-hex hash. Both are
#   therefore killed by every family that presents a 128-hex hash.
# Measured (pristine battery, <roster>/m06-hash-127.py and m07-hash-129.py, --runs 3 each):
#   families_passed 3/50, failed 47 families including POSITIVE, MISMATCH-EARLY/LATE, MISSING,
#   HASH-NONHEX, HASH-UPPER, OPTIONAL-SKIP, ... on all 3 runs for both gates.
# So the HASH-LENGTH draw cannot mask a roster defect, and no roster negative has HASH-LENGTH as its
# sole killer (section 5 of the report: every negative's killer union is larger than {HASH-LENGTH}).
#
# Optional hardening (not required by any measured risk; only worth taking if the family is meant to
# certify each boundary rather than one boundary per case):
--- a/tools/limine-pin-battery-r89.py
+++ b/tools/limine-pin-battery-r89.py
@@ -293,10 +293,11 @@ def fam_hash_short(c):
 def fam_hash_short(c):
     c.header()
     c.entry()
     c.pin("OK")
-    c.entry()
-    n = c.rng.choice([127, 129, 64, 0])
-    c.pin("LP-HASH-FORMAT", hashfmt=secrets.token_hex(65)[:n])
+    for n in (127, 129, 64, 0):
+        c.entry()
+        c.pin("LP-HASH-FORMAT", hashfmt=secrets.token_hex(65)[:n])
#
# The same consideration applies to PANIC-NO-ONLY's 50/50 no|non-no branch (line 399): the only roster
# gate whose exposure depends on that branch is m16-panic-no-inverted, and PANIC-FIRST (line 410) puts
# the first key at no and yes on alternate cases, so m16 is killed in every case of every run by
# PANIC-FIRST. Measured killer unions for m16 (section 5) do not rest on PANIC-NO-ONLY alone.
