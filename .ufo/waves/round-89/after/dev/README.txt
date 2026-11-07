First candidate score (development, uncommitted battery bytes sha256 fae9c65bd8f4ca9ee260138e4d5c6a4fbea6ae469b50c59902d7b986b72d39bb, canonical layout, counter at freeze fba764ca), 2026-11-06T22:15:28-03:00
selftest PASS 15/15; counter: run1 3/3 62/62; run2 3/3 61/62 failures N-h01-key-sep-equals; run3 3/3 62/62; verdict unmet rc 1
cause: KEY-EQUALS drew 'path =' (blank before '=') with p 0.5 per case; h01 accepts '=' only when it directly follows the key, so with the blank it behaves correctly and escapes; 0.5^4 = 1/16 per run.
fix: KEY-EQUALS always writes 'path=' (key touching '='); the blank-before-'=' variant is KEY-SPACING's ground already. Predicate, counter and roster unchanged.
