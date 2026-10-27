VERDICT: supports

Item C2-4 — mutation test of the C2 fix (fixture-base guard + two R47-C2 pinning cases) in
tools/tsukuroi-census.sh, per the frozen counting-command shape
(`env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$S/t 2" bash <copy> --selftest`, S under
/fast/scratch/hyaku/tsukuroi-r47/C2MutFix/<mutant>). All runs on scratch copies; the lane
file was never written (sha256 before and after: adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41;
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain -- tools/` empty).

Detector note: PASS lines and the TSUKUROI_CENSUS_SELFTEST trailer print to stdout; per-case
FAIL lines print to stderr. Receipts: .ufo/waves/round-47/w1/C2MutFix/<run>/{run.out,run.err,run.rc}
plus run-summary.txt, pristine-hashes.txt, mutant-hashes.txt.

Kill matrix (space TMPDIR = "$S/t 2" unless noted):

| run   | bytes changed                                   | TMPDIR | detector result                                          | verdict |
|-------|-------------------------------------------------|--------|----------------------------------------------------------|---------|
| base  | none (pristine copy)                            | space  | rc=0, PASS (164 cases, 164 passed, 0 failed)             | control |
| m1    | (a) st_base guard removed, both R47-C2 cases kept | space | rc=1, FAIL (164 cases, 14 passed, 150 failed); stderr last line: `FAIL selftest: the fixture base must classify absolute under a dirty TMPDIR (R47-C2)` | KILLED, legibly |
| m2    | (b) guard kept, fallback made unsafe: st_base=/nonexistent | space | rc=1, stdout EMPTY (no trailer), stderr: `mktemp: failed to create directory via template '/nonexistent/tsukuroi-r3-2-selftest.XXXXXX': No such file or directory` | KILLED at setup |
| m2ctl | m2 bytes                                        | clean  | rc=0, PASS (164/164)                                     | control: failure is fallback-specific |
| m3    | (c-i) R47-C2 unsafe-pin removed, guard intact   | space  | rc=0, PASS (163 cases, 163 passed, 0 failed)             | SURVIVED (intended) |
| m3b   | m3 + guard removed                              | space  | rc=1, FAIL (163 cases, 13 passed, 150 failed); stderr: `FAIL selftest: the fixture base must classify absolute under a dirty TMPDIR (R47-C2)` | KILLED by the one remaining case |
| m4    | (c-iii) R47-C2 absolute-pin removed, guard intact | space | rc=0, PASS (163 cases, 163 passed, 0 failed)             | SURVIVED but HOLLOW (contract unpinned) |
| m4b   | m4 + guard removed                              | space  | rc=1, FAIL (163 cases, 14 passed, 149 failed); ZERO R47-C2 lines in stderr; all 149 fails are generic fixture-arm reds | KILLED only indirectly; illegible |

(a) Guard removed, cases kept — do the cases FAIL as designed? YES.
m1 receipts: m1/run.out, m1/run.err, m1/run.rc. Of 150 failures, exactly 149 are the
fixture-arm reds the guard exists to prevent (script comment at tools/tsukuroi-census.sh:2054
"a caller's dirty TMPDIR must not turn 149 cases red (round-46 w1/C1ExecRerunB)") plus the
one named R47-C2 pin. The unsafe-pin case 2 PASSED even in the mutant (under m1, $work
itself contains a space, so "$work/fx/sp dir/root" is trivially 'unsafe') — confirming case 2
is a classifier-behavior pin, not a guard pin; it cannot detect a missing guard.

(b) Fallback made unsafe (/nonexistent) — is the failure mode legible? LOUD BUT NOT IN THE
HARNESS'S VOICE. m2 receipts: m2/run.{out,err,rc}. set -e aborts at the mktemp assignment
before any fixture or trailer prints: rc=1, stdout empty, stderr carries mktemp's own
`failed to create directory via template '/nonexistent/...': No such file or directory`.
A human sees the broken fallback path; but (1) the TSUKUROI_CENSUS_SELFTEST trailer never
prints, so a parser keying on it sees nothing; (2) rc=1 is indistinguishable from an
ordinary verdict FAIL; (3) nothing explains that a dirty TMPDIR triggered the fallback.
Control m2ctl (clean TMPDIR, m2/run-clean.*): PASS 164/164 rc=0 — the failure is specific
to dirty-TMPDIR + broken-fallback, never a silent pass. No lane change is proposed: this
legibility gap exists only under a hypothetical broken fallback; the shipped fallback is /tmp.

(c) One R47-C2 case removed — does PASS still mean the contract is covered?
- Remove the unsafe-pin (m3): PASS 163/163. Then remove the guard too (m3b, hash
  02156fae4c0cf872266fdd8198b0748760add492906ddde4e7ef79990b61e338): the remaining
  absolute-pin fires by name — `FAIL selftest: the fixture base must classify absolute
  under a dirty TMPDIR (R47-C2)` (m3/run-m3b.err). So with the unsafe-pin gone, PASS stays
  meaningful: the absolute-pin alone kills a guard breach. The unsafe-pin is redundant
  w.r.t. the guard, but see m4b — it is not redundant for legibility of the classifier
  half of the contract.
- Remove the absolute-pin (m4): PASS 163/163 — and now NOTHING pins "the fixture base
  classifies absolute under a dirty TMPDIR". Then remove the guard too (m4b, hash
  56b1ff0b2e5d67075a31e6b16c811960ca8468c547e56f2878880490806c8612): the run FAILs
  (rc=1, 149 failed) but no R47-C2 line names the cause; a reader sees only generic
  fixture-arm BLOCKED reds (m4/run-m4b.err head: `FAIL healthy: all planes pass: exit 2
  wanted 0; output: SCRUB btrfs-scrub-record state=NONE ... TSUKUROI_CENSUS: BLOCKED
  (packages=BLOCKED ...)`). Compare m1, where the same breach produced one named line.

Conclusion: both R47-C2 cases earn their keep. Case 1 ("absolute under a dirty TMPDIR") is
the operative detection pin for the guard; case 2 ("a space in a root override stays
unsafe") does not detect the guard at all (it passed in m1 and m4b) but pins the
classifier's refusal behavior independently of TMPDIR state. Removing either case leaves
PASS green while silently dropping half the pinned contract (hollow PASS, m4); only the
combination gives a named, actionable kill. The C2 fix as frozen kills every applied mutant
that the harness can reach: (a) killed legibly, (b) killed at setup, (c) each case shown
load-bearing. No defect in the shipped bytes; claim C2's kill rules and the 164-case count
are corroborated on pristine bytes (base run).

Byte-level evidence:
- pristine/lane sha256: adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41
- m1 sha256: 92a61f54d806e4d96761f84c038cfb6d5a0a7e9b02e5a3e4f2c906cdf3f8a83d (guard removal only)
- m2 sha256: 4f62fd1d5700c6f16ef5228e89a72058be74af7e459d776873147abd770dcc97 (fallback=/nonexistent only)
- m3 sha256: 6dfc3003cf5953be688eedc844e0ba6b647999c15f12295f959d71c5f7257986 (unsafe-pin removal only);
  m3b sha256: 02156fae4c0cf872266fdd8198b0748760add492906ddde4e7ef79990b61e338 (m3 + guard removal)
- m4 sha256: d5db78861cd10cc3f7cebb91751da5b06c3d0b24624466f16f491649197e8614 (absolute-pin removal only);
  m4b sha256: 56b1ff0b2e5d67075a31e6b16c811960ca8468c547e56f2878880490806c8612 (m4 + guard removal)
- Diff of each single-mutant vs pristine: see below (identical to the mutations named above).
- Restoration: the lane file was never mutated (hash identical before/after; lane git status
  clean). The scratch copies are the disposable artifacts this item assigns ("mutation-test
  the C2 fix on a scratch copy"); per the seat rule the scratch dir
  /fast/scratch/hyaku/tsukuroi-r47/C2MutFix was removed after receipts were copied, with
  before/after hashes recorded here and in mutant-hashes.txt / pristine-hashes.txt.

Not done: no mutation of root_locator_class itself (out of item scope); no reruns under
TMPDIR with tabs/newlines (the charset guard treats them identically to space — same
character-class branch); no concurrency (selftests serialized, one at a time, per seat cost rule).

Mutant diffs (vs pristine, from `diff -u`):

m1:
-  local st_base=${TMPDIR:-/tmp}
-  case "$st_base" in
-    *[!A-Za-z0-9._/+-]*) st_base=/tmp ;;
-  esac
-  work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")
+  work=$(mktemp -d "${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX")

m2:
-    *[!A-Za-z0-9._/+-]*) st_base=/tmp ;;
+    *[!A-Za-z0-9._/+-]*) st_base=/nonexistent ;;

m3:
-  mkdir -p "$work/fx/sp dir/root"
-  [ "$(root_locator_class "$work/fx/sp dir/root")" = 'unsafe' ] \
-    && ok 'selftest: a space in a root override stays unsafe by design (R47-C2)' \
-    || bad 'selftest: root_locator_class must refuse whitespace overrides (R47-C2)'

m4:
-  [ "$(root_locator_class "$work")" = 'absolute' ] \
-    && ok 'selftest: the fixture base classifies absolute even when TMPDIR contains a space (R47-C2)' \
-    || bad 'selftest: the fixture base must classify absolute under a dirty TMPDIR (R47-C2)'
