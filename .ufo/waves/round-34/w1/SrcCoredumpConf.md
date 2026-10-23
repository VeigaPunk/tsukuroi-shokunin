Depth/source verdict: systemd v262 distinguishes permanent core storage from processing and logging; the host’s parsed on-disk configuration sets `Storage=none`. This seat did not score a C1 control.

1. [obs] Source provenance: systemd v262 `man/coredump.conf.xml`, fetched from `https://raw.githubusercontent.com/systemd/systemd/v262/man/coredump.conf.xml` on 2026-10-23 with `curl -sL --fail`; unchanged bytes are saved at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/SrcCoredumpConf/coredump.conf.xml`, SHA-256 `b1c2eeee292175ff687fc428635bb25c7908ed14143a3cfc34016ba78278a39d`.

2. [obs] The source’s storage and logging distinctions are (each quotation is under 25 words): `Storage=`: “Controls where to store cores.” (source lines 77); with `Storage=none`, “the core dumps may be logged (including the backtrace if possible), but not stored permanently.” (lines 78–80). Processing may still use a temporary or unlinked disk file: the source says “the core will be written to /var/lib/systemd/coredump/ either way” (lines 89–92), and “Storage= thus only controls whether to leave it there even after it was processed.” (lines 92–93).

3. [obs] `ProcessSizeMax=` bounds processing, not storage: “The maximum size in bytes of a core which will be processed.” (lines 110–113); oversized cores “may be stored, but the stack trace will not be generated.” (lines 112–113). The source specifically says “Setting Storage=none and ProcessSizeMax=0 disables all coredump handling except for a log entry.” (lines 117–118). [inf] Thus a log entry remains even in that no-processing/no-permanent-storage case; for `Storage=none` alone, log messages and a backtrace are possible, not guaranteed for every crash.

4. [obs] `ExternalSizeMax=` is the per-core saved-size cap for external files: “The maximum (compressed or uncompressed) size in bytes of a coredump to be saved in separate files on disk” (lines 158–163; the same entry separately describes `JournalSizeMax=` for journal storage). `MaxUse=` makes “old core dumps [be] removed as soon as the total disk space taken up by core dumps grows beyond this limit” (lines 177–183). `KeepFree=` “controls how much disk space to keep free at least” (lines 184–186). These are limits on externally stored cores; the source notes usage can temporarily exceed them during processing and that `MaxUse=` takes precedence (lines 177–188).

5. [obs] Host version and effective parsed configuration: `systemd-analyze --version` reported `systemd 262 (262-1-arch)`. `systemd-analyze cat-config systemd/coredump.conf` exited 0 and printed `/etc/systemd/coredump.conf` plus the following drop-ins. The base file’s shown directives are comments, including `#ProcessSizeMax=32G` and `#ExternalSizeMax=32G`; the active non-comment lines read from the drop-ins are:

`/etc/systemd/coredump.conf.d/limit.conf`
```
[Coredump]
MaxUse=512M
KeepFree=8G
```

`/etc/systemd/coredump.conf.d/storage.conf`
```
[Coredump]
Storage=none
```

[obs] Reading `/usr/lib/systemd/coredump.conf.d` returned “Path ... not found”; no vendor drop-in path was present there. [inf] On the parsed file configuration, cores are not kept permanently under `Storage=none`; processing can still write a temporary core, and the source permits logging (including a backtrace if possible). The active `MaxUse` and `KeepFree` values govern externally stored cores, not whether the crash is logged.

6. [obs] Registry comparison: the exact source URL and fetched SHA-256 were each searched in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`; neither matched. S177 is a related but distinct source (`systemd-coredump.xml`), not this `coredump.conf.xml`. No duplicate by registered URL or recorded digest was found.

7. Draft `corpus/SOURCES.md` row, text only (proposed S186; 11 cells; not inserted):

`| S186 | systemd v262 — coredump.conf(5) — https://raw.githubusercontent.com/systemd/systemd/v262/man/coredump.conf.xml | docs | A | systemd v262 coredump storage, processing-size, external-size and external-disk-space semantics; documentation, not host-state evidence | tag v262; man/coredump.conf.xml lines 77–93, 110–118, 158–168, 174–191; raw bytes SHA-256 b1c2eeee292175ff687fc428635bb25c7908ed14143a3cfc34016ba78278a39d; snapshot .ufo/waves/round-34/w1/SrcCoredumpConf/coredump.conf.xml; fetched with curl -sL --fail on 2026-10-23 | Storage=none may log a crash but does not keep its core permanently; processing and saved-core size/space limits are distinct | mined | 2026-10-23 | on-release | .ufo/waves/round-34/w1/SrcCoredumpConf.md |`

8. [unk] `systemd-analyze cat-config` establishes the parsed on-disk configuration, not whether the running coredump handler has reloaded it or whether any particular crash was logged. This seat did not inspect journal entries or reconcile the census `coredump=` count with ADJ-04; those are outside this source/config item. The source’s “may be logged” wording does not promise a backtrace for every event.

Execution record: first, `timeout 300 git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 6de666c427ba9aa6b4350561980bde8d0e7c261d:SCORECARD.md` exited 0 and supplied the round-34 declaration. The initial chained host command created the seat directory, then `timeout 300 systemd --version` failed with exit 127 (`systemd: command not found`), so later steps in that chain did not run. I then ran `timeout 300 systemd-analyze --version` and `timeout 300 systemd-analyze cat-config systemd/coredump.conf` (both exit 0), and separately `timeout 300 curl -sL --fail https://raw.githubusercontent.com/systemd/systemd/v262/man/coredump.conf.xml --output /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/SrcCoredumpConf/coredump.conf.xml` followed by `timeout 300 sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/SrcCoredumpConf/coredump.conf.xml` (exit 0; digest above). No C1 probe, receipt, journal count, or install was run.

Scope: read=round-34 declaration in SCORECARD.md; systemd v262 coredump.conf.xml; SOURCES.md rows/URL/digest; systemd-analyze effective config; /etc and /usr/lib coredump drop-in paths; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/SrcCoredumpConf/coredump.conf.xml, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/SrcCoredumpConf.md; executed=git show declaration; mkdir seat directory; systemd --version attempt (exit 127); systemd-analyze --version; systemd-analyze cat-config systemd/coredump.conf; curl -sL --fail v262 source URL; sha256sum saved source.
Model: openai-codex/gpt-6-luna
Installs: none