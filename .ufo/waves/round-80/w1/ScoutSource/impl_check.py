#!/usr/bin/env python3
"""Cross-check the frozen matrix against systemd v262's OWN implementation.

The man page table is documentation; src/core/service.c service_shall_restart()
is the behaviour. This script encodes the implementation's six restart
predicates verbatim (v262 src/core/service.c, service_shall_restart) and
evaluates them against the ServiceResult enum (v262 src/core/service.h), then
compares the resulting per-cause restart sets against the frozen matrix.

Implementation (verbatim from v262 src/core/service.c):
    NO:          return false;
    ALWAYS:      return s->result != SERVICE_SKIP_CONDITION;
    ON_SUCCESS:  return s->result == SERVICE_SUCCESS;
    ON_FAILURE:  return !IN_SET(s->result, SERVICE_SUCCESS, SERVICE_SKIP_CONDITION);
    ON_ABNORMAL: return !IN_SET(s->result, SERVICE_SUCCESS, SERVICE_FAILURE_EXIT_CODE,
                                SERVICE_SKIP_CONDITION);
    ON_WATCHDOG: return s->result == SERVICE_FAILURE_WATCHDOG;
    ON_ABORT:    return IN_SET(s->result, SERVICE_FAILURE_SIGNAL, SERVICE_FAILURE_CORE_DUMP);

Cause -> ServiceResult mapping (v262 service.h ServiceResult enum):
    Clean exit code or signal  -> SERVICE_SUCCESS
    Unclean exit code          -> SERVICE_FAILURE_EXIT_CODE
    Unclean signal             -> SERVICE_FAILURE_SIGNAL
    Timeout                    -> SERVICE_FAILURE_TIMEOUT
    Watchdog                   -> SERVICE_FAILURE_WATCHDOG
    Termination due to OOM     -> SERVICE_FAILURE_OOM_KILL
"""
import json
import sys

CAUSE_RESULT = {
    "Clean exit code or signal": "SERVICE_SUCCESS",
    "Unclean exit code": "SERVICE_FAILURE_EXIT_CODE",
    "Unclean signal": "SERVICE_FAILURE_SIGNAL",
    "Timeout": "SERVICE_FAILURE_TIMEOUT",
    "Watchdog": "SERVICE_FAILURE_WATCHDOG",
    "Termination due to OOM": "SERVICE_FAILURE_OOM_KILL",
}


def IN_SET(x, *vals):
    return x in vals


def restarts(setting, result):
    if setting == "no":
        return False
    if setting == "always":
        return result != "SERVICE_SKIP_CONDITION"
    if setting == "on-success":
        return result == "SERVICE_SUCCESS"
    if setting == "on-failure":
        return not IN_SET(result, "SERVICE_SUCCESS", "SERVICE_SKIP_CONDITION")
    if setting == "on-abnormal":
        return not IN_SET(result, "SERVICE_SUCCESS", "SERVICE_FAILURE_EXIT_CODE",
                          "SERVICE_SKIP_CONDITION")
    if setting == "on-watchdog":
        return result == "SERVICE_FAILURE_WATCHDOG"
    if setting == "on-abort":
        return IN_SET(result, "SERVICE_FAILURE_SIGNAL", "SERVICE_FAILURE_CORE_DUMP")
    raise ValueError(setting)


matrix = json.load(open(sys.argv[1]))
settings = matrix["settings"]
rows = {r["cause"]: r["restart"] for r in matrix["rows"]}

mismatches = []
for cause, table_row in rows.items():
    result = CAUSE_RESULT[cause]
    for i, setting in enumerate(settings):
        impl = restarts(setting, result)
        tbl = table_row[i]
        if impl != tbl:
            mismatches.append((cause, setting, tbl, impl, result))
        print(f"{'ok ' if impl == tbl else 'MISMATCH'} {cause:28s} {setting:12s} "
              f"table={str(tbl):5s} impl={str(impl):5s} ({result})")

print()
print(f"cells compared: {len(rows)*len(settings)}   mismatches: {len(mismatches)}")
for m in mismatches:
    print("  MISMATCH", m)
sys.exit(1 if mismatches else 0)
