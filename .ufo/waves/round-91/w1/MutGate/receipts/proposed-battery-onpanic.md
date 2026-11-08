# Proposed battery amendment for survivor S4 (`CONF-a-onpanic-menu`)

Gap: `tools/limine-pin-battery-r91.py` never constrains `on_panic` for an unreadable conf.

Current code (`run_battery`, around line 1696):

```python
want_op = None if (c.conf_missing or c.conf_dir) else c.want_on_panic()
ok = (got is not None and got[0] == want[0] and got[3] == want[0] and got[1] == want[1]
      and [list(x) for x in got[2]] == [list(x) for x in want[2]] and r8_ok(c, got)
      and u1_ok(c, got)
      and (want_op is None or got[6] == want_op))
```

Because `want_op` is `None`, any `on_panic` value passes — a gate that reports `"menu"` (or `"halt"`) after failing to read the conf is not caught, even though it has read no `measured_boot` and no Secure Boot state.

Proposed patch (two lines; `"null"` is a sentinel distinct from "not checked"):

```python
want_op = "null" if (c.conf_missing or c.conf_dir) else c.want_on_panic()
ok = (got is not None and got[0] == want[0] and got[3] == want[0] and got[1] == want[1]
      and [list(x) for x in got[2]] == [list(x) for x in want[2]] and r8_ok(c, got)
      and u1_ok(c, got)
      and (want_op is None or (got[6] is None if want_op == "null" else got[6] == want_op)))
```

Kills mutant `CONF-a-onpanic-menu` (`"on_panic": None` → `"menu"` in the `OSError` return) while leaving the pristine gate `met`: `CONF-UNREADABLE` / `MALFORMED-INPUT` already set `conf_missing` or `conf_dir`, and the pristine gate returns `on_panic: None` there (probe `receipts/probe-CONF-a-onpanic-menu.json`).

No new family is needed; only the expectation is missing. This is a battery change, so it is proposed only — not applied (leaf seat, lane read-only).
