# DomainSource — ProtectSystem= Value Domain & Boolean Parsing Evidence

source: `systemd.exec(5)` (Arch manual pages); `systemd.syntax(7)` (Arch manual pages)
verified-at: 2026-10-20
recheck: on-release

## Axes
- **depth**: Distinguishes the closed documented option domain from configuration boolean spellings, and isolates the source conflation where unit-side mechanism non-exhaustiveness was misattributed to `ProtectSystem=`'s value set.
- **calibration**: Exact primary quotes (<=25 words) and located URLs without adding unneeded synonyms or asserting ungrounded option values.

## 1. Documented Value Domain vs Lexical Spellings
- **Primary Option Definition**: `systemd.exec(5)` defines `ProtectSystem=` as:
  “Takes a boolean argument or the special values "full" or "strict".” (11 words)
- **Domain Values (4 Semantic Modes)**:
  1. Negative boolean (`off`, default): protection disabled.
  2. Positive boolean (`true`): mounts `/usr/`, `/boot`, `/efi` read-only.
  3. Special value `"full"`: positive boolean scope plus `/etc/` read-only.
  4. Special value `"strict"`: entire hierarchy read-only except `/dev/`, `/proc/`, `/sys/`.
- **Parsing Spellings vs Domain**: `systemd.syntax(7)` documents configuration parsing formats:
  - Positive booleans: `1`, `yes`, `true`, `on`.
  - Negative booleans: `0`, `no`, `false`, `off`.
  These are parser-level lexical aliases for the boolean domain argument, not distinct option modes. No other strings or synonyms are recognized.
- **Source of R13 Factual Defect (MD:97)**:
  r13 MD:97 stated “the value set is not exhaustive”. The source domain for `ProtectSystem=` is strictly closed. Non-exhaustiveness belongs exclusively to the open set of *unit-side read-only mechanisms* (`ProtectSystem=`, `ReadOnlyPaths=`, `BindReadOnlyPaths=`, `TemporaryFileSystem=:ro`, etc.), as correctly distinguished in r13 JSON.

## 2. Located Primary Quotes (≤25 words each)
| Source | Section / Anchor | URL | Located Quote (≤25 words) |
|---|---|---|---|
| `systemd.exec(5)` | § ProtectSystem= (SANDBOXING) | https://man.archlinux.org/man/systemd.exec.5 | “Takes a boolean argument or the special values "full" or "strict".” (11 words) |
| `systemd.exec(5)` | § ProtectSystem= (SANDBOXING) | https://man.archlinux.org/man/systemd.exec.5 | “If true, mounts the /usr/ and the boot loader directories (/boot and /efi) read-only for processes invoked by this unit.” (20 words) |
| `systemd.syntax(7)` | § INTRODUCTION (Booleans) | https://man.archlinux.org/man/systemd.syntax.7 | “Boolean arguments used in configuration files can be written in various formats. For positive settings the strings 1, yes, true and on are equivalent.” (22 words) |
| `systemd.syntax(7)` | § INTRODUCTION (Booleans) | https://man.archlinux.org/man/systemd.syntax.7 | “For negative settings, the strings 0, no, false and off are equivalent.” (11 words) |

## 3. Concrete Recommendations for R14-VALUE-DOMAIN
1. **Target Correction ID**: `R14-VALUE-DOMAIN` (source ID: `S044`, tier A docs).
2. **Superseded Locus**: `corpus/knowledge/root-dac-correction-r13.md:97` phrase “the value set is not exhaustive”.
3. **Exact Minimal Quote**: “Takes a boolean argument or the special values "full" or "strict".” (11 words; `https://man.archlinux.org/man/systemd.exec.5`).
4. **Recommended Replacement Text**:
   “the documented ProtectSystem= value domain consists of a boolean argument or the special values "full" or "strict"; non-exhaustiveness applies to unit-side read-only mechanisms, not the option domain”
5. **Registry Entry (S044)**:
   - URL: `https://man.archlinux.org/man/systemd.exec.5`
   - Anchor: `§ ProtectSystem=`
   - Teaches: `ProtectSystem= takes a boolean argument or "full" or "strict"; its value domain is closed, while unit-side read-only mechanisms remain non-exhaustive.`

## 4. Limitations & Tooling Record
- **Limitations**: Examines documented option interface and parser syntax from authoritative documentation; does not probe kernel runtime namespaces or execute systemd services.
- **Tooling Record**: Tools installed or updated: none.
