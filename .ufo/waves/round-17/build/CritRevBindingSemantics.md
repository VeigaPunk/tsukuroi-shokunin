# CritRevBindingSemantics — C3 attack (R17)

Axes: C3 operability, provenance.

1. [obs] Ancestor of master yet unlanded: jj-lane moves the bookmark (`scripts/hyaku/jj-lane.sh:649`) before pushing; failure exits 3 keeping it (`:9,660`); recovery rewrites it (`:307-321`). Only the origin check catches this, skipped when the origin ref is absent (`check-section-citations.py:468-469`, fail-open, fixable: emit `remote_tip`, null rejectable). Tracking ref ≠ `ls-remote` (`jj-lane.sh:228`) [inf: stale after foreign force-push; tradeoff].
2. [obs] `--branch` admits any name (`check-section-citations.py:64`): a seat-made `refs/heads/x` certifies unlanded commits. Fix: consumers require JSON `branch == master`.
3. [inf, git ref-over-abbrev rule, unverified] a 7–39-hex ref name shadows the object. Fix: resolved sha must start with input.
4. [obs] HEAD rejection breaks no LOG command (`LOG.md:553-554,729,901` use `<commit>`); `SKILL.md:1818-1819` document REV=`HEAD`, needs appended correction. [unk] cited hashes `9574a189` (`round-13/correction/CorrectionCheck.md:73`), `8606bad4`/`9dd82bce` (`round-14/repair/verification.json:14,20`), `db68e62`, `0db618a` still ancestors.
5. [obs] Count gameable: BOUND (`spec.json:55`) passes stubs S1 equality-only (breaks all historical reproductions), S2 no origin check, S3 literal-`HEAD`-only reject. Sandbox clone's origin = lane local master, so NOT-PUSHED never fires. Fixed `total:5` ignores four new `--revision` gates.

Falsifier: `--selftest` must score S1–S3 UNBOUND; live adds landed non-tip ancestor accepted, sandbox origin=`tip^` → NOT-PUSHED, `@-`/`master` → INVALID, abbreviated tip → full-sha `revision`; denominator = tools defining `--revision`; bind `--tools-revision`.

Scope: executed=none
