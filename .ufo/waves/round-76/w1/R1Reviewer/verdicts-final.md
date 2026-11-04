Verdict: JD1–JD8 HOLD against committed note b698d13d63a56e47bc5e6e0de63fe793b2d8b96d. Recommendation only, not admission.
Residual unchecked: live cached metrics/min_use; Arch binary equivalence; actual vacuum behavior. None is presented as measured by the corrected note.
Axes: depth, C1 source truth, attack.

## Scope and evidence

Read the exact revision with `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show b698d13d63a56e47bc5e6e0de63fe793b2d8b96d:corpus/knowledge/journald-retention-plane-r76.md`. Re-read pinned source ranges below, including the newly referenced vacuum caller. This final report supersedes the initial note-specific JD3 FAIL/JD7 PARTLY verdicts for this revision only. It does not retroactively change the frozen draft or declaration. Stale-carrier final errata are outside this requested recheck. LSP remains unavailable as previously recorded; evidence is direct textual source inspection, not semantic-reference proof. No note/registry/instrument edits, commits, installation, counter runs or live host operations.

## Per-row entailment

All source names below are under .ufo/waves/round-76/before/src/.

| Row | Verdict | Checked source | Entailment and scope attack |
|---|---|---|---|
| JD1 | HOLD | journald.conf.xml:77–108 | :84–86 says auto behaves like persistent when the directory exists, volatile otherwise. :81–84 permits early-boot/unwritable fallback; :92–95 gives flush transition; :102–108 gives namespace directory-creation caveat. The row says 'like persistent', not always disk, and final prose preserves fallback and compilation-dependent default. |
| JD2 | HOLD | journald.conf.xml:274–298 | :283–285 gives 10%/15%, each capped 4G. :274–281 supplies both constraints/smaller permitted allowance. :285–298 gives startup and active-file caveats. Final explanatory paragraph explicitly says 'subject to the startup floor'; no unqualified guarantee of physical usage at/below MaxUse is inferred. |
| JD3 | HOLD | journald-manager.c:143–173 | :168 is LESS_BY(vfs_avail,keep_free), :170 CLAMP(vfs_used+avail,min_use,max_use), :171 saturated available growth. Corrected row states subtraction floored zero, not minimum. Final paragraph's extra manager_do_vacuum reference was checked at :796–814: :807–809 passes space limit, file-count limit and max_retention_usec into journal_directory_vacuum. |
| JD4 | HOLD | journald-manager.c:176–186 | Comment :179–183 states startup/first open and restart reset; :185 uses MAX. Corrected 'at least current' preserves existing larger minimum. Another caller at :1656–1668, already inspected in initial review, reapplies the patch during full rotate; row does not claim startup is the only invocation. Prose explicitly disclaims never deleting old archives under other constraints. |
| JD5 | HOLD | journald.conf.xml:300–309 | :302–305 supports one-eighth capped 128M, 'usually seven', compact mode 4G. :308–309 supports synchronous extension enforcement. Final prose distinguishes usual history from guarantee and compact ceiling from default. |
| JD6 | HOLD | journald.conf.xml:311–318 | :313–315 exempts active files from count-limit deletion; :316–318 allows excess total and gives default 100. 'Only' is scoped to archived deletions for this count reduction, not all possible file removal. |
| JD7 | HOLD | journald-config.c:24–27,39–68,106–142 | Constants all hold at :24–27. Initializer assigns rate pair at :51–52; MERGE_NON_ZERO at :106–111 implements fallback precedence; manager_merge_configs applies sync at :133 and max-file at :142. Corrected row now names the right functions; prose distinguishes compiled defaults from live/service-effective configuration. Quote cell joins two adjacent macro lines with whitespace, so it is a normalized multiline excerpt, not one physical source line; no source-semantic defect remains. |
| JD8 | HOLD | journalctl.xml:941–985 | :943–944 includes archived and active usage; :954–957 gives oldest-archive size vacuum; :969–973 gives indirect effect and active exemption; :975–979 covers combined and zero limits; :981–985 covers rotate first. No promise that vacuum alone clears active data. |

## Host derivation and Limits block

**HOLD as derived configuration limits, not a live state measurement.** The final note explicitly says the result is not a direct read of running cached state or startup min_use. This repairs the earlier unconditional live-limit concern by narrowing what effective_limit means in this note. It does not prove live min_use<=256MiB.

Frozen before/host.txt:60–63 supplies SystemMaxUse=256M/RuntimeMaxUse=64M; :35–42 shows no explicit KeepFree or per-file override. Receipt :72 gives filesystem size 998037782528 and available 764239769600 bytes; :76 independently yields 4096*186581975=764239769600 from bavail.

- Uncapped 10% and 15% defaults both exceed 4GiB; KeepFree therefore defaults to 4294967296 bytes, while explicit MaxUse wins at 268435456 bytes.
- Correct avail=764239769600−4294967296=759944802304 bytes. The final note's 'remaining allowance' description is consistent with this subtraction; the earlier wrong min expression is removed.
- With min_use<=268435456, clamp(used+759944802304,min_use,268435456)=268435456=256MiB. Without that startup metric, actual cached limit is not independently established; final text explicitly disclaims that observation.
- Derived per-file default=min(268435456/8,134217728)=33554432=32MiB. This remains a default derivation under pinned mechanism, not installed runtime proof.
- Receipt :66–68 directly reports 'Archived and active journals take up 148.6M in the file system.' :84–86 separately reports 13 files and 209715200 bytes=200MiB apparent-length sum. Final note correctly avoids equating file lengths with allocated-block disk usage and does not assert precise implementation equivalence between manager and journalctl.

Limits block correctly states upstream v262 versus installed 262.1-1 gap; no vacuum/rotation/flush/restart/configuration write; inventory is not rotation-schedule/seven-file/count-bound evidence; counter is not semantic entailment or daemon-state proof. Earlier unsupported birth timestamp and drop-in/storm causal history are removed. No actionable source-entailment defect remains in these eight rows and the qualified host/limits text.

## Residual risk and verification gaps

The unchanged frozen declaration/draft's wrong arithmetic remains historical and is not silently vindicated by this revision's correction. Live cached min_use and installed binary equivalence remain unmeasured, as the note acknowledges. This review provides no runtime admission, saturation measurement, rerouting or resume-continuity claim. The recheck uses previously recomputed integer values, re-read source contexts, and exact committed note content; no counter or live experiment was run. Existing scratch was already deleted; none recreated.

Self-evaluation: accuracy 4/5 (upstream-only implementation and unmeasured live minimum are explicit); completeness 5/5 (eight rows plus host and Limits checked); clarity 4/5 (separates configured bound from cached state); actionability 5/5 (exact revision and source ranges); conciseness 4/5 (detailed evidence retained for audit). Overall 4.4/5.
