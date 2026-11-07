# Proposed patch: r89 counter cannot bind its AF_UNIX launcher socket at the documented scratch path
# File: tools/battery-discrimination-r89.py (frozen; proposed only, not applied)
# Measured at lane master 665408cc45a88ed49717e22f4593e8e6152ac665, counter sha256 c666323a35e736fc534634b6b826313e5ff2895dff9d3df3f8bd8c1cd0c9a0e5
#
# Evidence (seat MutBattery, 2026-11-06): the counting command of the r89 claim
#   python3 tools/battery-discrimination-r89.py --battery tools/limine-pin-battery-r89.py --runs 3 --scratch "$S/work"
# with S=/fast/scratch/hyaku/tsukuroi-r89/MutBattery dies before the first gate:
#   File ".../tools/battery-discrimination-r89.py", line 216, in one
#     sock.bind(sp)
#   OSError: AF_UNIX path too long
#   EXIT=1
# The exception is uncaught: the process exits 1 (the same code the KILL RULE uses for `unmet`),
# writes no --json receipt, and never reaches the could-not-evaluate (exit 3) path that the KILL
# RULE reserves for "any row of any run is an error row".
#
# Arithmetic (sun_path is 108 bytes including NUL, so <= 107 bytes; measured boundary 107 ok / 108 fail):
#   scratch          = $S/work = 48 bytes
#   outer mkdtemp    = 48 + 1 + 35 (prefix 27 + 8)                 = 84   (line 297)
#   case mkdtemp d   = 84 + 1 + 11 (prefix "bd-" 3 + 8)            = 96   (line 206)
#   socket path      = 96 + 1 + 1 + 12 (token_hex(6))              = 110  (line 215)
# 110 > 107 -> bind fails. In general socket = len(--scratch) + 62, so the counter only binds when
# --scratch is at most 45 bytes. $S/work = 38 + len(seat) is 48 at this seat root
# (/fast/scratch/hyaku/tsukuroi-r89/MutBattery), i.e. it needs a seat name of at most 7 characters.
# Measured: --scratch "$S/c" (45 bytes) -> socket 107 -> binds; --scratch "$S/pf" (46) -> 108 -> fails;
# --scratch "$S/work" (48) -> 110 -> fails; --scratch "$S/work-baseline" (57) -> 119 -> fails.
# A shorter --scratch is not a fix the frozen counting command can carry: the claim names "$S/work".
#
# Proposed change (shorten the socket name; d is already unique, so the 12-byte nonce is redundant;
# convert an over-long path into an error row instead of a crash):
--- a/tools/battery-discrimination-r89.py
+++ b/tools/battery-discrimination-r89.py
@@ -212,8 +212,11 @@ def one(battery, gate, scratch):
         for extra in gate.get("support", []):
             shutil.copy(os.path.join(ROSTER_DIR, extra), os.path.join(gd, extra))
-        sp = os.path.join(d, "s" + secrets.token_hex(6))
-        sock.bind(sp)
+        sp = os.path.join(d, "s")  # d is unique; sun_path holds 108 bytes incl NUL
+        if len(sp.encode()) > 107:
+            return "error:socket path %d bytes > 107 (shorten --scratch)" % len(sp.encode()), None
+        sock.bind(sp)
         sock.listen(16)
         th = threading.Thread(target=serve, args=(sock, gate_path, gd, d, stop), daemon=True)
         th.start()
#
# With the patch the same command at $S/work binds a 96-byte path, and any future over-long path
# is reported as an error row, which the KILL RULE turns into could-not-evaluate (exit 3), never
# into a `met` or a bare `unmet` exit 1. Full 3-run re-measurement of C1 is the L1's call.
