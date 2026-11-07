FIXTURES 25
| mutant | gate:line | rule (mutated clause) | probe fixture that differs | r87 families_passed (3 runs) | r88 families_passed (3 runs) | r87 | r88 | equivalent? | r88 families that failed (union) |
|---|---|---|---|---|---|---|---|---|---|
| `h01-key-sep-equals` | 53 | R1 key directly followed by ':' | key-eq-sep | 22, 22, 22 | 38, 38, 38 | SURVIVED | SURVIVED | yes | - |
| `h02-keychars-digits` | 40 | R1 key charset letters/underscore | **none — EQUIVALENT** | 22, 22, 22 | 38, 38, 38 | SURVIVED | SURVIVED | EQ | - |
| `h03-value-lstrip-spaces-only` | 55 | R1 skip blanks (space+tab) after ':' | value-tab | 21, 21, 21 | 37, 37, 37 | killed | killed | yes | WHITESPACE-CRLF |
| `h04-strip-spaces-only` | 47 | R1 strip leading/trailing space+tab per line | indent-tab | 21, 21, 21 | 37, 37, 37 | killed | killed | yes | WHITESPACE-CRLF |
| `h05-hash-empty-ignored` | 119 | R2/R3 an empty hash is still a pin (LP-HASH-FORMAT) | empty-hash | 21, 21, 21 | 37, 38, 37 | killed | killed | yes | OPTIONAL-HASH-FORMAT |
| `h06-hash-len-at-least` | 127 | R3 hash exactly 128 characters | hash-129 | 21, 22, 22 | 38, 36, 36 | killed | killed | yes | FORMAT-BEFORE-RESOLVE, HASH-LENGTH, OPTIONAL-HASH-FORMAT |
| `h07-hash-prefix-64` | 156 | R5 full-digest comparison | hash-prefix-late-flip, optional-upper-wallpaper | 11, 11, 12 | 18, 17, 17 | killed | killed | yes | 21 families (ALL-PIN-KEYS, ENTRY-LABEL, FIRST-URI-SEP, ...) |
| `h08-dollar-kept` | 132 | R4 leading '$' gzip marker dropped from the resource | gz-marker | 21, 21, 21 | 37, 37, 37 | killed | killed | yes | GZ-RAW |
| `h09-root-ignored-on-boot` | 133 | R4 boot with a NON-empty root is LP-UNRESOLVED | root-on-boot2, resource-upper | 21, 21, 22 | 35, 35, 36 | killed | killed | yes | EMPTY-ROOT-RESOURCE, ROOT-ON-BOOT, UNRESOLVED |
| `h10-empty-path-pin-ignored` | 119 | R2 a pin with an empty path is still a pin | empty-path | 22, 22, 22 | 38, 38, 38 | SURVIVED | SURVIVED | yes | - |
| `h11-optional-case-sensitive` | 125 | R6 optional keys matched per R1 (case-insensitive) | optional-upper-wallpaper | 22, 22, 22 | 38, 38, 38 | SURVIVED | SURVIVED | yes | - |
| `h12-format-optional-panic` | 128 | R6 LP-HASH-FORMAT on wallpaper/term_font -> skip | optional-format-wallpaper | 22, 22, 22 | 37, 37, 37 | SURVIVED | killed | yes | OPTIONAL-HASH-FORMAT |
| `h13-panic-key-case` | 115 | R1/R6 hash_mismatch_panic key case-insensitive | panic-key-upper | 22, 22, 22 | 37, 37, 37 | SURVIVED | killed | yes | PANIC-KEY-CASE |
| `h14-sb-zero-inverted` | 269 | R6/R7 --secure-boot-enforced 0 means not enforced | sb-flag-zero | 21, 21, 21 | 33, 32, 34 | killed | killed | yes | 7 families (HOST-SHAPE, PANIC-FIRST, PANIC-KEY-CASE, ...) |
| `h15-panic-startswith-no` | 121 | R6 panic value equal to 'no' (not a prefix) | panic-value-nope | 22, 22, 22 | 37, 36, 37 | SURVIVED | killed | yes | PANIC-NO-ONLY, PANIC-NON-NO |
| `h16-missing-consequence-none` | 146 | R6 LP-MISSING -> not-modelled | empty-path, missing-file | 20, 20, 20 | 36, 36, 36 | killed | killed | yes | MISSING, MULTI-FAULT |
| `h17-hash-nonhex-skipped` | 127 | R3 hash must be hex | hash-nonhex-128 | 21, 21, 21 | 35, 35, 35 | killed | killed | yes | FORMAT-BEFORE-RESOLVE, HASH-NONHEX, OPTIONAL-HASH-FORMAT |
| `h18-cr-split-lines` | 106 | R7/R8 1-based PHYSICAL line numbering | crlf | 21, 21, 21 | 37, 37, 37 | killed | killed | yes | WHITESPACE-CRLF |
| `h19-entry-plus-kept` | 109 | R8 entry label strips one leading '+' | entry-plus | 22, 22, 22 | 38, 38, 38 | SURVIVED | SURVIVED | yes | - |
| `h20-resource-case-insensitive` | 133 | R4 resource names are case-sensitive | resource-upper | 22, 22, 22 | 38, 38, 38 | SURVIVED | SURVIVED | yes | - |
| `h21-conf-except-filenotfound` | 101 | R7 any unreadable --conf -> CANNOT-EVALUATE | conf-dir | 22, 22, 22 | 37, 37, 37 | SURVIVED | killed | yes | CONF-UNREADABLE |
| `h22-first-uri-sep-rfind` | 63 | R2 path starts after the FIRST '):/' | first-uri-sep | 22, 22, 22 | 37, 37, 37 | SURVIVED | killed | yes | FIRST-URI-SEP |
| `h23-key-lookup-as-written` | 117 | R1/R2 pin keys matched case-insensitively | optional-upper-wallpaper, key-upper | 21, 21, 21 | 37, 37, 37 | killed | killed | yes | KEY-CASE |
| `h24-term-font-dropped` | 38 | R6 term_font is an optional key | optional-mismatch-term-font | 21, 21, 21 | 35, 35, 35 | killed | killed | yes | ALL-PIN-KEYS, OPTIONAL-HASH-FORMAT, OPTIONAL-SKIP |
