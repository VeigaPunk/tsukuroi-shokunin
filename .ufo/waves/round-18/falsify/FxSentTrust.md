# FxSentTrust — final local-gate security review

**Disposition: SURVIVES, bounded to reviewed local code.** Axes: process isolation, Git configuration, claim accuracy.

**Severity: Low (configuration-isolation consistency); informational for clone isolation.**

**Exploit path / evidence:** `tools/check-revision-binding.py:101-113` removes inherited `GIT_*`, disables system/global config, and applies `core.hooksPath=/dev/null` to the judge's own Git calls. `:314-325` runs each candidate Python gate in the clone with that sanitized environment and a 60-second timeout. But `tools/_revision.py:62-72` subsequently removes all `GIT_*` variables again and invokes Git without a hooks-path override; its `:88-90,97-122` callsites are `check-ref-format`, `rev-parse`, and `merge-base`. **[INFERENCE, untested]** ambient global/system config may affect nested binding observations. No current hook-triggering Git operation was found; this is not evidence of hook execution.

**Impact:** The outer judge's Git configuration/hook suppression is implemented, but does not fully propagate into the shared helper. The candidate processes otherwise retain caller filesystem/network authority: the judge explicitly says at `check-revision-binding.py:49-53` “not OS process isolation” and “retain the caller's user-level filesystem/network authority.” A malicious/unreviewed reachable revision could therefore read or alter user-accessible files, use the network, or leave descendants; clone and timeout do not prevent that. The stated reviewed-code-only boundary is essential, not a sandbox guarantee.

**Smallest remediation:** Preserve `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=os.devnull` in `_revision.clean_env()` (and explicitly set `core.hooksPath` for its Git calls) if uniform nested Git isolation is required. Keep refusing unreviewed candidate code; genuine untrusted execution requires an OS-level sandbox/least-privilege account. No execution or runtime containment test was performed.

Scope: executed=none