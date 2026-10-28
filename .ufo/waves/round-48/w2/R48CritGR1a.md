ROW GR1 VERDICT: partly
SECTION SHA256: fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8
Seat R48CritGR1a (critic), claim C2, row GR1, revision ae99f021b76f8eb1c8805d32d80644464afb1ff6.

Hash: the frozen counter's --section-hash printed GR1 fe77ac76...badf9ca8 (same as expected, structural_ok 1, problems []).
I did not re-derive it by an independent sha256 over the joined lines; I used the counter value.
Snapshots: sha256sum of cmdline.c (1af5ad98...), vsprintf.c (cabb648a...), kstrtox.c (0c52ae02...) and sysfs.c (ce146120...)
each equal their SHA256SUMS lines (round-45 and round-44 frozen/src). capture.txt digest not re-checked.

Quotes: all 13 Quote lines sit on their cited lines (checked by grep -n): cmdline.c:147, 156, 159, 189, 191, 192;
vsprintf.c:86; kstrtox.c:29, 30, 33; sysfs.c:2040, 2043. Text matches.

Clauses verified from the bytes:
- memparse calls simple_strtoull with base 0: cmdline.c:156. simple_strtoull calls simple_strntoull (vsprintf.c:112-114),
  which calls _parse_integer_fixup_radix at vsprintf.c:86.
- Fixup: kstrtox.c:29 leading '0'; kstrtox.c:30 hex when s[1] is x and s[2] is a hex digit; kstrtox.c:33 otherwise octal;
  kstrtox.c:35 decimal when no leading 0. The 0x prefix is then skipped at kstrtox.c:37.
- At most one suffix: single switch on *endptr at cmdline.c:160, cases E..K with shl += 10 at cmdline.c:163, 167, 171, 175,
  179, 183 (cascading, so K is 10 bits = 1024); both cases listed (cmdline.c:161, 181-182). Only one endptr++ at cmdline.c:193.
- Needs a preceding digit: cmdline.c:189 (ptr != endptr). Overflow to ULLONG_MAX: cmdline.c:191-192.
- Store: memparse at sysfs.c:2040, skip_spaces at sysfs.c:2042, EINVAL unless *endptr == 0 at sysfs.c:2043.
- Examples: 100M and 100m = 100<<20 = 104857600 OK; 010 -> base 8 = 8 OK; 0x10 -> 16 OK; 10MB: suffix eaten, 'B' remains,
  EINVAL OK; "10 M": no suffix at the blank, skip_spaces leaves 'M', EINVAL OK; "-1": simple_strntoull has no sign
  handling (vsprintf.c:78-96), zero digits, endptr stays on '-', EINVAL OK; bare newline: no digits, 0, skip_spaces
  reaches NUL, accepted with 0 OK. The "0 means no limit" part rests on SR8 (another entry) and scrub.c:1381 in the
  round-44 snapshot (bwlimit == 0 returns); that is outside the quoted lines but the row cites SR8 for it.
- Host reading: capture.txt:8 shows value=0 mode=644 owner=root; capture.txt:1 shows uid=1000 CapEff=0; capture.txt:9 devids=1. OK.

DEFECT (the reason for partly): the fixup clause "hexadecimal for a leading `0x` followed by a hex digit, octal for any
other leading `0`" is imprecise. The pinned test at kstrtox.c:30 is _tolower(s[1]) == 'x', so uppercase "0X10" is also
hexadecimal (16). Read literally, "any other leading 0" would send "0X10" to octal, where it would stop at the X and be
rejected with EINVAL. That is false: the code accepts 0X10 as 16. The row itself says "in either case" for suffix letters
but not for the prefix, and the Quote at kstrtox.c:30 is the very line that shows the case-insensitivity.
Core of the row (parse chain, suffix rules, store check, examples, host reading) is right, so not `fails`.

Exact replacement text for the clause: "which picks hexadecimal for a leading `0x` or `0X` followed by a hex digit, octal for
any other leading `0`, and decimal otherwise."

Minor, not by itself blocking: the Host reading clause "this caller cannot write one" is a kernel permission inference
(mode 644, owner root, uid 1000, no capabilities; ACLs and LSM rules are not in the capture) and carries no [inference]
mark. Suggested wording: "so this caller [inference: by ordinary file-mode checks, which the capture does not exercise]
cannot write one." The quotes also do not cover the shl += 10 lines or sysfs.c:2042 that the Statement relies on; the
lines exist in the snapshot, so this is a completeness note only.

Not done: no sysfs write or kernel run to test the parse (read-only, no privilege); no independent sha256 re-derivation.
