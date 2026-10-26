import sys
CASE = """  # The -Sup-sourced name list is the second extraction the R42 pipeline fix touched; it is reached
  # only when -Qu is empty or short of -Sup (R42-C1).
  case_home='degraded-update-sup-names-large'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 1 > "$FX/qu.rc"; : > "$FX/qu"
  { printf 'fixture/alpha 1.1-1\\nextra/beta 2.1-1\\nextra/gamma 3.1-1\\n'
    awk 'BEGIN { for (i = 0; i < 4000; i++) printf "extra/pad%05d 1.0-2\\n", i }'; } > "$FX/sup"
  check 'degraded: a 4003-line -Sup list keeps its names (R42-C1)' 1 DEGRADED \\
    '^PLANE update-safety: DEGRADED \\(status=REQUIRES-PREP; pending=REQUIRES-PREP\\(candidates=4003 join_behind=0 names=\\[alpha,beta,gamma\\]\\); qu=rc=1/0; sup=4003 '

"""
anchor = "  case_home='blocked-update-qu';"
for src, dst in (("impl-census.sh", "impl-plus-case.sh"), ("v4-sup-census.sh", "v4-plus-case.sh")):
    text = open(src).read()
    assert text.count(anchor) == 1, src
    open(dst, "w").write(text.replace(anchor, CASE + anchor, 1))
    print("wrote", dst)
