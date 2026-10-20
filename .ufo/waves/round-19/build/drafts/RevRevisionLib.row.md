# Draft registry row — shared revision binding library

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| shared-revision-binding | library | Imported Python API: `from _revision import bind, RevisionError, Binding`; standalone: `python3 tools/_revision.py --selftest` | `bind` returns `Binding` or raises one typed `RevisionError`; selftest 0 pass / 1 fail; invalid argv 64 | `python3 tools/_revision.py --selftest` | Branch syntax before revision; 7–64 hex commit; local ancestry and optional origin ancestry; `Binding(sha, branch, branch_tip, origin_tip)` | Binding reads Git only; selftest writes in a temporary Git repository, removed on exit | tsukuroi |

Evidence: API/fields/error shape `tools/_revision.py:50-58,134-154`; validation order `tools/_revision.py:134-153`; CLI/selftest exit and tally `tools/_revision.py:239-252`; read-only binding note `tools/_revision.py:26-28`; selftest temporary repo and Git writes `tools/_revision.py:180-189,220-234`.
