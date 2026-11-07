Proposed docstring-only patch (CriticForgers, round 89 wave w1).

Target: tsukuroi-shokunin/tools/limine-pin-battery-r89.py, module docstring.

(a) R1 paragraph, line 29 (the sentence "a line is `KEY: value` when, after removing every CR
and the leading spaces/tabs, it starts with letters/underscores then ':' (not '=', not a
blank).") — append:

    The key charset is observable only through the enumerated keys: no path-valued key (R2)
    and no `hash_mismatch_panic` key (R6/R8) contains a digit, so whether the charset admits
    digits changes no output and the battery does not certify this clause.

(b) Alternative (or in addition), "Not modelled (limits, not families)" list, line 76 — add:

    the R1 key charset beyond letters/underscores (unobservable: no enumerated key contains a
    digit)

Rationale: forger fx_f04_digits_in_key.py (base.py with KEYCHARS = letters + underscore +
digits) reads 50/50 met in 12/12 runs, and a 1200-case differential probe of base.py vs
fx_f04_digits_in_key.py found 0 differences in (stdout, rc). The clause is inert, not
under-tested; the docstring should say so rather than let a `met` verdict be read as
certifying it. No battery family can be added to close it.
