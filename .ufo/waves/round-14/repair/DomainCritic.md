# DomainCritic — R14-VALUE-DOMAIN adversarial review (report only)

Axes: depth (source fidelity of the corrected domain), calibration (no new closure). No R14 MD/JSON draft existed at review time
(`glob **/*r14*` empty), so the attack targets the dispatched intent "documented domain boolean/full/strict; mechanism examples non-exhaustive".

## Primary source reopened (2026-10-20)
- https://man.archlinux.org/man/systemd.exec.5 (.raw sha256 4e7a79b3…016c, `.TH … "systemd 262.1"`), § ProtectSystem= (SANDBOXING), raw L1830-1833:
  `Takes a boolean argument or the special values "full" or "strict".` — 11 words; HTML renders straight ASCII quotes.
- Host /usr/share/man/man5/systemd.exec.5.gz (`.TH … "systemd 261.2"`): ProtectSystem paragraph byte-identical to the 262.1 paragraph (diff = window offset only).
- systemd.syntax(7) (host): booleans "1, yes, true and on" / "0, no, false and off" are equivalent.
- Code at tag https://github.com/systemd/systemd/tree/v261.2 (host package 261.2-1): src/basic/parse-util.c `parse_boolean`
  (STRCASE_IN_SET 1/yes/y/true/t/on, 0/no/n/false/f/off); src/basic/string-table.c `string_table_lookup_from_string_with_boolean`
  (boolean first, then case-sensitive `streq_ptr`); src/core/namespace.c:4116-4123 table no/yes/full/strict + `DEFINE_STRING_TABLE_LOOKUP_WITH_BOOLEAN(…, PROTECT_SYSTEM_YES)`;
  src/core/unit.c:4505 `ec->protect_system = PROTECT_SYSTEM_STRICT` under DynamicUser; src/core/dbus-execute.c:1343 property type "s".

## Verdict on the core correction
`boolean or "full"/"strict"` is the correct, source-exact documented domain; r13 MD:97 "the value set is not exhaustive" is wrong.
The correction is safe **only** if it quotes the domain and does not re-enumerate it. Counterexamples below are closure/confusion risks.

## Findings (counterexample → evidence → smallest safe correction)
1. **Lexical-alias closure (high if written).** Any phrasing "accepts no/yes/full/strict", "four values", or a closed spelling list
   (e.g. 1/yes/true/on/0/no/false/off/full/strict) is contradicted: v261.2 also accepts `y`,`t`,`n`,`f` and any-case booleans (`TRUE`),
   while `Full`/`STRICT` are rejected (case-sensitive table) — parse error, setting ignored (`log_syntax_parse_error`, critical=false); empty `ProtectSystem=` is likewise a parse error, not a reset.
   Docs (syntax(7)) list 8 boolean spellings; code accepts 12, case-insensitively. Fix: state the domain only by the verbatim quote;
   if modes are named, say "four resulting modes no/yes/full/strict (the canonical tokens `systemctl show` prints)" and explicitly
   "boolean spellings follow systemd.syntax(7); not enumerated here". Do not add synonyms (agrees with DomainSource brief).
2. **Existing r13 table conflates spelling with mode.** r13 MD:37-42 / JSON:32-60 rows `no`, `yes`/`true`, `full`, `strict` — asymmetric
   aliases (`true` listed, `false`/`on`/`1` not). Not false, but a reader of a "closed domain" correction will treat the rows as the
   complete lexicon. Fix (in R14 text, r13 bytes untouched): one sentence "r13 table rows are the four modes; `yes`/`true` is an example spelling, not a lexicon."
3. **Quote/anchor collision.** The prefix "Takes a boolean argument or the special values" occurs 3× in systemd.exec(5)
   (ProtectSystem L1830, ProtectHome L1877 "read-only"/"tmpfs", ProtectControlGroups L3053 "private"/"strict"). `"strict"` alone is
   ProtectControlGroups' value too (a read-only /sys/fs/cgroup mechanism). Fix: quote must contain `"full"`; location must be
   "§ ProtectSystem= (SANDBOXING)"; checker must match the whole 11-word string, never a bare `strict`/prefix substring, and normalise `\"`→`"`.
4. **Mode ≠ assignment (mode/mechanism confusion).** systemd.exec(5) L1855-1856 "This setting is implied if DynamicUser= is set";
   unit.c:4505 assigns STRICT unconditionally (overrides an explicit `ProtectSystem=no`). So "closed value domain" must not become
   "the mode is set only by ProtectSystem=". `systemctl show` reports the manager's post-patch context, `systemctl cat` file text [INFERENCE: show reads patched ExecContext via D-Bus offsetof]. Fix: no new claim needed; avoid the sentence form "ProtectSystem=no means no ProtectSystem effect from any setting".
5. **Mode ≠ applied mount.** SANDBOXING L1813-1814: ProtectSystem "has no effect if the kernel is built without file system namespacing"
   or in such containers; L1818-1820 not available in user services. A domain correction must not imply a value guarantees a mount. Fix: keep r13 "configured text, live namespace unobserved".
6. **Exception list is documentation-level, not implementation-closed.** v261.2 namespace.c strict table marks `/home`, `/run/user`,
   `/root` READ_WRITE_IMPLICIT (left to ProtectHome=), beyond the doc's /dev /proc /sys. `/` remains read-only, so r13 B2 logic is
   unaffected. Fix: R14 should say "subject to its documented exceptions", not restate the three-path list as complete. Lead only; out of R14 scope.
7. **Code trap that re-closes mechanisms.** namespace.c `root_read_only()` returns true only for STRICT or ReadOnlyPaths containing `/`.
   It is used solely to decide read-only image dissection (L2599-2603), ignoring BindReadOnlyPaths/TemporaryFileSystem/RootImage.
   Fix: if any seat cites code, forbid using this helper as evidence that the mechanism set is closed (would resurrect the r12 universal).
8. **Sibling ambiguity to sweep.** r13 JSON:120 replacement: "Among ProtectSystem= values, only `strict` … ; the option set is not an
   exhaustive list of unit-side read-only mechanisms" — "option set" right after "values" can be misread as the value domain (same defect class as MD:97).
   Fix: R14 supersession notice should name it and gloss "option set" = mechanisms (ProtectSystem=, ReadOnlyPaths=, …), not values.
9. **Checker scoping.** R14 MD must itself say "non-exhaustive" for mechanisms; a whole-file "no `not exhaustive`" predicate would
   false-fail, and a bare "contains boolean" predicate would pass "boolean values true/false only". Mutants to require red:
   (a) "the value set is not exhaustive" in R14 section; (b) "four values: no, yes, full, strict" as the domain; (c) quote with `"private" or "strict"`;
   (d) mechanism list called exhaustive. Bounded conformance, not source truth.

## Recommended minimal R14-VALUE-DOMAIN text
- quote: `Takes a boolean argument or the special values "full" or "strict".` (11 words) — url https://man.archlinux.org/man/systemd.exec.5, location § ProtectSystem= (SANDBOXING).
- replacement: "The documented ProtectSystem= domain is a boolean or the special values "full" or "strict"; among them only strict covers the
  hierarchy, subject to its documented exceptions. Non-exhaustiveness applies to unit-side read-only mechanisms, not to this value domain;
  boolean spellings follow systemd.syntax(7) and are not enumerated."
- supersedes: r13 MD:97 phrase "the value set is not exhaustive" (historical bytes retained) and note JSON:120 "option set" gloss.

## Impacted axes
depth: positive if F1/F3 avoided; harmed if any closed spelling/mode-source list ships. calibration: F4-F7 prevent new over-claim. No host-cause or capability claim touched.

## Limitations
No R14 draft to inspect; findings are pre-landing. Code reads are v261.2 tag (matches host 261.2-1); man page 262.1 web vs 261.2 host
paragraph identical. Did not inspect Arch patches to systemd (unverified none touch parse_boolean). No commands from sources executed;
no tests/build/checkers run; scratch downloads only under /tmp/dc-*.

## Tooling
Installed/updated: none. Used curl, zcat, grep/awk/sed/diff, python3 (read-only parsing).
