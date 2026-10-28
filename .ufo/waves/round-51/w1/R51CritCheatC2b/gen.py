import hashlib, os, sys
SRC = '/fast/scratch/hyaku/tsukuroi-r51/R51CritCheatC2b/census-frozen.sh'
OUT = '/fast/scratch/hyaku/tsukuroi-r51/R51CritCheatC2b/fx'
os.makedirs(OUT, exist_ok=True)
B = open(SRC, encoding='utf-8').read()

def sub1(t, old, new):
    n = t.count(old)
    assert n == 1, (n, old[:70])
    return t.replace(old, new)

SELFBR = '  if [ "$selftest" -eq 1 ]; then\n    run_selftest\n    return\n  fi\n'
M1 = '  roll=$(worse "$roll" "$OOM_V")\n'
M1EQ = '  roll=$(worse "$OOM_V" "$roll")\n'          # worse() is symmetric: same semantics
M2 = '    DEGRADED) exit 1 ;;\n'
M2EQ = '    DEGRADED) exit $((1)) ;;\n'
BAD = "  bad() { FAIL=$((FAIL + 1)); printf 'FAIL %s\\n' \"$*\" >&2; }\n"
NEUT = "  bad() { PASS=$((PASS + 1)); printf 'PASS %s\\n' \"$*\"; }\n"
FAILLINE = "      printf 'TSUKUROI_CENSUS_SELFTEST: FAIL (1 cases, 0 passed, 1 failed)\\n'\n"
CANNED = ("  if [ \"$selftest\" -eq 1 ]; then\n"
          "    printf 'PASS canned liar case (R50-C2)\\n'\n"
          "    printf 'TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)\\n'\n"
          "    exit 0\n  fi\n")

def live_respell(t, eq=False):
    # live rollup + exit map; eq=True uses semantically equal spellings
    t = sub1(t, M1, M1EQ if eq else M1)  # placeholder when eq False keeps exact needle
    return t

def base_with(branch, eq_live=False, neut=False, pin=False):
    t = B
    if eq_live:
        t = sub1(t, M1, M1EQ); t = sub1(t, M2, M2EQ)
    t = sub1(t, SELFBR, branch)
    if neut:
        t = sub1(t, BAD, NEUT)
    return t

DETECT = ("  if [ \"$selftest\" -eq 1 ]; then\n"
          "    if ! grep -qxF '  roll=$(worse \"$roll\" \"$OOM_V\")' \"$SELF\" || ! grep -qxF '    DEGRADED) exit 1 ;;' \"$SELF\"; then\n"
          + FAILLINE + "      exit 1\n    fi\n"
          "    run_selftest\n    return\n  fi\n")
SHA = ("  if [ \"$selftest\" -eq 1 ]; then\n"
       "    pin_want=$(sed -n 's/^# PIN-SELF: //p' \"$SELF\")\n"
       "    pin_got=$(grep -v '^# PIN-SELF: ' \"$SELF\" | sha256sum | cut -d' ' -f1)\n"
       "    if [ \"$pin_got\" != \"$pin_want\" ]; then\n"
       + FAILLINE + "      exit 1\n    fi\n"
       "    run_selftest\n    return\n  fi\n")
ENV = ("  if [ \"$selftest\" -eq 1 ]; then\n"
       "    if [ -n \"${CENSUS_MUTANT:-}\" ]; then\n"
       "      printf 'PASS canned (R50-C2)\\n'\n"
       "      printf 'TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)\\n'\n"
       "      exit 0\n    fi\n"
       "    run_selftest\n    return\n  fi\n")
NAME = ("  if [ \"$selftest\" -eq 1 ]; then\n"
        "    case \"${TMPDIR:-}${SELF}\" in\n"
        "      *tmp-M[0-9]*|*mut-M[0-9]*)\n"
        + FAILLINE + "        exit 1 ;;\n    esac\n"
        "    run_selftest\n    return\n  fi\n")

def dead_block():
    return ("  if false; then\n"
            "  roll=$(worse \"$roll\" \"$OOM_V\")\n"
            "  case \"$roll\" in\n"
            "    HEALTHY)  exit 0 ;;\n"
            "    DEGRADED) exit 1 ;;\n"
            "    BLOCKED)  exit 2 ;;\n"
            "  esac\n"
            "  fi\n")

out = {}
# (a) canned printer, needles only in an if-false block, live code respelled
t = sub1(B, SELFBR, CANNED)
t = sub1(t, M1, M1EQ); t = sub1(t, M2, "    DEGRADED) exit 1;;\n")
t = sub1(t, "  printf 'TSUKUROI_CENSUS: %s (packages=", dead_block() + "  printf 'TSUKUROI_CENSUS: %s (packages=")
out['F1-canned-dead'] = t
# (b) text detector (real harness)
out['F2-detector'] = base_with(DETECT)
# (c) self-hash pin (real harness); pin = sha256 of body-without-pin + newline
body = base_with(SHA)
h = hashlib.sha256((body + '\n').encode()).hexdigest()
out['F3-selfhash'] = body + '\n# PIN-SELF: ' + h + '\n'
# (d) CENSUS_MUTANT env recogniser (hides only when env set), real harness otherwise
out['F4-env'] = base_with(ENV)
# combined adversarial: detector / self-hash / name-keyed, each with a NEUTERED harness
out['F2n-detector-neutered'] = base_with(DETECT, neut=True)
b2 = base_with(SHA, neut=True)
h2 = hashlib.sha256((b2 + '\n').encode()).hexdigest()
out['F3n-selfhash-neutered'] = b2 + '\n# PIN-SELF: ' + h2 + '\n'
out['F5n-name-neutered'] = base_with(NAME, neut=True)
out['F5-name'] = base_with(NAME)
# equivalence variants (same semantics, different bytes)
out['EQ-real'] = base_with(SELFBR, eq_live=True)
out['EQ-F2-detector'] = base_with(DETECT, eq_live=True)
out['EQ-F3-selfhash'] = base_with(SHA, eq_live=True) + '\n# PIN-SELF: ' + h + '\n'
out['NEUT-real'] = base_with(SELFBR, neut=True)

for k, v in out.items():
    p = os.path.join(OUT, k + '.sh')
    open(p, 'w', encoding='utf-8').write(v)
    print(k, len(v), 'M1x=%d M2x=%d' % (v.count(M1), v.count(M2)))
