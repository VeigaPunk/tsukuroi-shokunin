# FxFresh16 — C3 update-safety-v2 review

Axes: evidence fidelity; same-premise coverage; bounded unknowns.

**LSP:** unavailable (`read xd://lsp` returned “No such tool”; no status/references/definition/diagnostics). Findings below are literal source review, not semantic proof.

**Records:** Content-valid: `R18-FRESH-SUPPLEMENT-16`, `-20`, `-21`, `-22`, `-23`, `-24`. `-16` correctly supersedes the 41.1-installed/42.2-pending premise with local-db 42.2 at capture :34; pending remains unknown. `-20` distinguishes configured snapper names (:75-80) from unverified snapshots/restoration. `-21` correctly leaves checkupdates unverified; `-22` separates running kernel from package inventory; `-23` prevents replay of stale DKMS removal; `-24` correctly treats `.db.sig` presence (:54) as no signature validation.

**Invalid as recorded:**
- `R18-FRESH-SUPPLEMENT-15`: “after later transactions” overstates capture :65, which is a `pacman -D` invocation, not completion. Replace with “later invocation logged; R18 ran no pending query; current count UNKNOWN.” Do not infer transaction completion.
- `R18-FRESH-SUPPLEMENT-25`: :54 (`openai-chatgpt.db.sig`) alone cannot establish `offline.db` absence. Cite complete `ls` command/output/status, capture :48-55. Its bounded “absent from captured sync-directory listing” and unknown cache/reachability claims are otherwise appropriate.

**Locator fixes:** `-20` → :75-80; `-21` → :36 and :82-86 (paccache); `-22` → :6 and :32-33 (package directories); `-23` → :92-96 (complete DKMS output/no 7.1.4 row). `-24` :54 suffices. All seven JSON `reason` fields are identical boilerplate; make each state its specific stale premise/evidence rather than only “correction sweep found” it.

Same-premise notices cover U1, U2, U3, U4 (including rank-3 repeat), and offline-exile reachability; historical §1/§4 measurements remain dated. No config→rollback or enabled→active inference: line208 explicitly says enabled + inactive. Residual: appended recheck line417 calls filesystem mtime an “upstream stamp”; capture :42-46 establishes mtimes only. Replace with “filesystem mtime; does not establish acquisition/refresh.” No pending count, snapshot/restore capability, checkupdates availability, or repository reachability is established by R18.

Scope: executed=none