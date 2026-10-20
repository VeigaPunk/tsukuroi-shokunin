# SafetyCredentials — planned gate credential/agent-db risk (static)

Status: `tools/check-section-citations.py` and `corpus/knowledge/section-citation-errata-r16.json` absent; nothing evaluated.

Baseline clean: tools/ has zero `.omp`/`agent.db`/credential/`expanduser` refs; no repo symlinks; `.git/config` has no fsmonitor/filter/helper/include/promisor keys; no `.gitattributes`. Template `git()` (check-locator-clarification.py:439-448) uses argv list, `--no-pager`, strips `GIT_*`; `REV` regex (:30) plus resolved-SHA `{sha}:{path}` (:452) blocks option injection.

**HIGH (planned) — record-controlled `path`.** Contract gives each correction a `path`. Template worktree read `ROOT / path` (:432) becomes the bare absolute path when `path` is absolute (`/home/vgpnk/.omp/agent/agent.db`); `../` also escapes. Text credential files decode; findings detail could echo bytes to stdout/reports.
Fix: exact allowlist `{corpus/knowledge/host-health-report-r3.md, corpus/knowledge/update-safety-v3.md}` → fixed finding id; never put file text in `detail`.

**LOW** — env keeps HOME/global gitconfig (not inspected; out of scope). Optional: set `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_NO_LAZY_FETCH=1`.

Installs: none.
