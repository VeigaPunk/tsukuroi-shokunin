VERDICT: holds
ROW: PA8
lines checked: frozen/src/version.c:39-255

Adversarial re-read of PA8 at 9cc9aa77e30e0e23de2d4d2697b3b218ada02969. I looked for a reading under which the
rule cell is false, overstated or short of a condition, and found none that survives the code. The two
precision gaps I did find are recorded under "Residuals" and do not make the cell false; if the row is ever
edited, they are the smallest safe wording changes.

## 1. The cell against the code (lines are the pinned snapshot)

Snapshot provenance: `sha256sum -c SHA256SUMS` in `.ufo/waves/round-41/frozen/src/` returns `version.c: OK`
(and OK for all eight other files), so the file I compiled is the pinned artifact; the counter's frozen digest
`fa769e30…ab833` (`tools/check-package-anatomy-r41.py:73`) matches that file.

- Split into three fields, absent epoch = 0: `version.c:49-64` — `while (*s && isdigit(*s)) s++;` then
  `if(*s == ':') { epoch = evr; … } else { /* different from RPM- always assume 0 epoch */ epoch = "0"; }`.
  The quoted source text of the cell ("/* different from RPM- always assume 0 epoch */") is `version.c:61`,
  inside the cited range. An *empty* epoch (`":1.0"`) is also made `"0"` at `version.c:57-59`.
- Release split at the last dash, `NULL` when absent: `version.c:65-70`.
- Three steps with fall-through and the release gate: `version.c:249-255`

  ```
  ret = rpmvercmp(epoch1, epoch2);
  if(ret == 0) {
      ret = rpmvercmp(ver1, ver2);
      if(ret == 0 && rel1 && rel2) {
          ret = rpmvercmp(rel1, rel2);
      }
  }
  ```

  That is exactly the value cell `epoch, then version, then release when both carry one`: the epoch
  comparison short-circuits the other two, and the release string is consulted only when both `rel` pointers
  are non-`NULL`.

## 2. Both derivations in the cell tested against the compiled comparator

I built the pinned `version.c` verbatim (only a stub `util.h` supplying `SYMEXPORT` and `<stdlib.h>`;
`gcc -O1 -o vc drv.c version.c`) and drove it through `alpm_pkg_vercmp`, comparing each result with this host's
`/usr/bin/vercmp`. Receipts: `.ufo/waves/round-41/w1/C2RevPA8b/matrix.txt` (30 pairs, library column and CLI
column), `…/fuzz.txt` (2 300 randomised pairs), `…/drv.c`, `…/util.h`.

- Epoch dominance — "any epoch 1 build outranks every epoch 0 build": analytic (the epoch `ret` short-circuits
  at `version.c:249-250`, so the version and release never enter) and empirical. `1:0` vs
  `0:999999999999999999999999` → `1`; `1:1.0` vs `0` → `1`; `10:1` vs `9:9` → `1`. Randomised: 1 200 triples
  of the form `1:<body>` vs `0:<y>` / bare `<y>` (and the reverse expecting `-1`), 0 failures.
- `1.0` equals `1.0-5`: `1.0` vs `1.0-5` → `0`, and the reverse → `0`; `1.0` vs `1.0-` → `0`; `1.0-` vs `1.0-5`
  → `-1` (the empty release is a release, non-`NULL` at `version.c:67`, and loses to `5`). Randomised: 800
  pairs `<v>` vs `<v>-<rel>` expecting `0`, 0 failures. `0:<v>` vs `<v>` → `0` in 300 further pairs, i.e.
  the absent epoch really is 0.
- The release branch really decides when both carry one: `1.0-1` vs `1.0-2` → `-1`, `1.0-9` vs `1.0-10` →
  `-1`, `1:1.0-1` vs `1:1.0-2` → `-1`, `1.0-1` vs `1.0-1.0` → `-1`.
- Leading zeros are normalised rather than compared as text: `01:1.0` vs `1:1.0` → `0`, `000:5` vs `0:9` →
  `-1` (epochs equal, then version 5 < 9). This narrows "epoch first" but does not contradict it: equal epochs
  fall through, as the cell's "then" says.
- Library and CLI agreed on all 30 pairs (no divergence), so the row's host column is evidence about the same
  comparator the rule describes.

## 3. Host column reproduced

The three quoted lines are byte-exact in `.ufo/waves/round-41/frozen/hostcap/vercmp.txt` (produced live by
`capture.sh:29` `printf 'vercmp %s %s = %s\n' "$1" "$2" "$(vercmp "$1" "$2")"`, entry list at
`capture.sh:27`). I re-ran the same six pairs with `/usr/bin/vercmp` on this host and got
`1`, `0`, `-1`, `0`, `-1`, `1` — identical to the capture, including the row's `vercmp 1:1.0-1 2.0-1 = 1`,
`vercmp 0:2.0-1 2.0-1 = 0`, `vercmp 1.0 1.0-5 = 0`. No read-only pacman query was needed and none was run.

## 4. Counterexamples attempted and why they fail

1. *Release compared when only one string carries one?* No — `rel1 && rel2` at `version.c:252`; tested.
2. *Epoch 1 beaten by an epoch 0 build with a huge version?* No — short-circuit; tested with a 24-digit
   version body.
3. *An "epoch" that is not a number bypassing the epoch step?* `a:1.0` vs `1.0` → `-1`: the `':'` branch needs a
   digit prefix, so such a string is version text, which is what "absent epoch counting as 0" predicts.
4. *Empty epoch not counting as 0?* `:1.0` vs `1.0` → `0`; `version.c:57-59` sets `"0"`.
5. *A caller that bypasses the comparator?* The two consumers in the snapshot are
   `add.c:85` and `add.c:436`, both through `_alpm_pkg_compare_versions`, not through a second comparator; and
   the only local-version-versus-target decision is `cmp == 0 → "up to date -- reinstalling"` (`add.c:87-91`),
   `cmp < 0 → "downgrading package"` (`add.c:97-99`) — the epoch outcome propagates unchanged. No `strcmp`
   on package version strings anywhere in `add.c`: the only `strcmp` calls there are archive-entry names
   (`add.c:173-177`) and file hashes (`add.c:365-383`), the rest being log lines.
6. *A different comparator in libalpm?* `grep -n 'parseEVR\|rpmvercmp\|alpm_pkg_vercmp' *.c` in the snapshot
   returns only `version.c` definitions plus the two `_alpm_pkg_compare_versions` call sites.

## 5. Residuals (non-falsifying; wording only)

- The third step's gate is `ret == 0 && rel1 && rel2` (`version.c:252`), i.e. the release is consulted only
  when the *versions* also compared equal. The cell's "the release **only when** both strings carry one" states
  the necessary condition and the "then … then" wording carries the sequencing, so the literal cell is not
  contradicted; a reader who drops the sequencing could over-read it. Counterexample to that over-reading, not
  to the cell: `1.0-1` vs `1.1-0` → `-1` with both releases present and never compared (`matrix.txt`). Smallest
  safe hardening if the row is touched: "…then the version, and last the release, only when the versions are
  equal and both carry one".
- "`1.0` equals `1.0-5`" is a comparator-level fact, not a package-plane one: `be_package.c:613-614` refuses a
  version without a dash (`_("invalid package version in %s\n")`) and `PKGBUILD.5.asciidoc:439-441` defines the
  full version string as 'pkgver-pkgrel' or 'epoch:pkgver-pkgrel', so two *loaded* packages always both carry a
  release and the skip branch is unreachable between them. This is consistent with PA2 in the same entry, and
  the row does not claim a package may have version `1.0`; it is a scope note for a future edit, not a defect.
- The cell does not mention the `NULL` handling above the three steps (`version.c:227-233`: `(NULL,NULL) → 0`,
  one `NULL` → `∓1`). Callers pass `pkg->version` after `be_package.c:609-614` has rejected a null/empty
  version, so the omission cannot mislead about package comparison.

## What I did not do

- I did not read `_alpm_pkg_compare_versions` itself: it is not in the frozen snapshot (only the six `.c` files
  listed in `FETCH.txt`/`SHA256SUMS` are), so the "caller" claim above is limited to the two call sites and to
  the absence of any second comparator in the snapshot. The rule cell does not depend on that wrapper for its
  three steps.
- I did not fetch upstream, run the counter, or touch the lane, host, or any pacman transaction. Scratch was
  `/fast/scratch/hyaku/tsukuroi-r41/C2RevPA8b` and has been removed after copying receipts. No tool was
  installed or upgraded.
