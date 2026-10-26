VERDICT: draft

# P-5 — round-38 `## Gate` rows for S208–S212

Scope: the five draft rows only. No lane file was edited. URL/path cells are reproduced from `corpus/SOURCES.md:217-221`; each quoted string is literal text in the committed snapshot or capture, verified with `grep -n` and pasted below. Access date 2026-10-26 is supported by the row cells (`corpus/SOURCES.md:217-221`), by `capture-meta.txt:1` (`# captured 2026-10-26T04:11:58Z`) and by `sources/SHA256SUMS:1` (`# fetched 2026-10-26T04:20:21Z`).

## Proposed `## Gate` table

| Row | Source URL/path and opened date | Located quote (≤25 words) | Location | Decision |
|---|---|---|---|---|
| S208 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/hook.c — opened 2026-10-26 | “return l1 < l2 ? -1 : 1;” | `_alpm_hook_cmp`, hook.c:452 (tie-break; suffix exclusion :449, `strncmp` :450; reverse directory walk :540; first-file-wins skip :588-590) | admit, mined, tier A |
| S209 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/doc/alpm-hooks.5.asciidoc — opened 2026-10-26 | “alphabetical order of their file name, where the ordering ignores the suffix.” | `DESCRIPTION`, alpm-hooks.5.asciidoc:39 (order rule; AbortOnFail PreTransaction-only scope :87-89) | admit, mined, tier A |
| S210 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/trans.c — opened 2026-10-26 | “if(!(trans->flags & ALPM_TRANS_FLAG_NOHOOKS) && _alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0) { RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1);” | `_alpm_trans_commit`, trans.c:201-203 (Post phase after a completed commit, result discarded :237-239) | admit, mined, tier A |
| S211 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/alpm.c — opened 2026-10-26 | “myhandle->hookdirs = alpm_list_add(NULL, hookdir);” | `alpm_initialize`, alpm.c:62 (system dir assembled :56-62 and installed as list head) | admit, mined, tier A |
| S212 | `.ufo/waves/round-38/frozen/hooks-capture/` (own-work) — opened 2026-10-26 | “# captured 2026-10-26T04:11:58Z host=plazir27 read-only” | capture-meta.txt:1 (version `pacman 7.1.0.r9.g54d9411-3` :3; `HookDir` :4-5); MANIFEST.sha256:1-70 — 70 entries: 67 under `usr-share-libalpm-hooks/`, 3 under `etc-pacman.d-hooks/`, `90-mkinitcpio-install.hook` in both | admit, mined, tier A, own-work |

Quote word counts (whitespace split): S208 8, S209 12, S210 12, S211 4, S212 5 — all ≤25.

## Quote verification — pasted `grep -n` output

Snapshot digests first (`sha256sum -c`), because the quotes are only evidence if the snapshot is the cited commit:

```
$ cd .ufo/waves/round-38/sources && sha256sum -c SHA256SUMS
hook.c: OK
alpm-hooks.5.asciidoc: OK
trans.c: OK
alpm.c: OK
```

```
$ grep -n 'l1 < l2 ? -1 : 1' sources/hook.c
452:		return l1 < l2 ? -1 : 1;
```

```
$ grep -n 'alphabetical order of their file name, where the ordering ignores the suffix' sources/alpm-hooks.5.asciidoc
39:alphabetical order of their file name, where the ordering ignores the suffix.
```

```
$ grep -n -B1 -A2 'ALPM_HOOK_PRE_TRANSACTION) != 0' sources/trans.c
201-	if(!(trans->flags & ALPM_TRANS_FLAG_NOHOOKS) &&
202:			_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0) {
203-		RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1);
204-	}
```

```
$ grep -n 'hookdirs = alpm_list_add' sources/alpm.c
62:	myhandle->hookdirs = alpm_list_add(NULL, hookdir);
```

```
$ grep -n 'captured 2026-10-26T04:11:58Z' frozen/hooks-capture/capture-meta.txt
1:# captured 2026-10-26T04:11:58Z host=plazir27 read-only
```

Secondary anchors named in the Location cells:

```
$ grep -n 'applies to PreTransaction hooks' sources/alpm-hooks.5.asciidoc
89:	applies to PreTransaction hooks.

$ grep -n 'skipping overridden hook' sources/hook.c
589:				_alpm_log(handle, ALPM_LOG_DEBUG, "skipping overridden hook %s\n", path);

$ grep -n '_alpm_hook_run(handle, ALPM_HOOK_POST_TRANSACTION)' sources/trans.c
238:			_alpm_hook_run(handle, ALPM_HOOK_POST_TRANSACTION);
```

## Provenance and capture cross-checks

- Digest equality with the SOURCES cells (`corpus/SOURCES.md:217-220`): `hook.c` `99f1044badd36f83bb781d9d59409b0cdff0f26e1aa95ebd88d0f25f776b199a`, `alpm-hooks.5.asciidoc` `2970cb35115a32a5d8a9652dfd795ad535d9354c36039fcc0d25929d9c3493d3`, `trans.c` `637c1165790ddd1c9d80bb0bfed9d85b1f5baa9b8e5a2e323243c5764ac4ed07`, `alpm.c` `8bbb0a3c90f23d8904a78faaf907a645e9329ddd05652c2b410d695f18f0834a` (`sha256sum hook.c alpm-hooks.5.asciidoc trans.c alpm.c`, output identical). `sources/SHA256SUMS:1` records the fetch from `https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/<path>` — the same commit as the row URLs.
- Capture: `sha256sum MANIFEST.sha256` = `da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd`, equal to the S212 row cell (`corpus/SOURCES.md:221`); `wc -l MANIFEST.sha256` = 70; `sha256sum -c MANIFEST.sha256` → `exit=0` with 70 lines matching `: OK$` (observed: `exit=0`, `70`). Directory counts: `ls usr-share-libalpm-hooks | wc -l` = 67; `ls etc-pacman.d-hooks | wc -l` = 3. The same-name pair is exactly one: `join -j 1 <(ls usr-share-libalpm-hooks | sort) <(ls etc-pacman.d-hooks | sort)` → `90-mkinitcpio-install.hook`.
- Live read-only recheck (no transaction, no mutation): `hostname` → `plazir27`; `pacman -Q pacman` → `pacman 7.1.0.r9.g54d9411-3`; `ls /usr/share/libalpm/hooks | wc -l` → 67; `ls /etc/pacman.d/hooks | wc -l` → 3.

## Findings

1. **S208–S211 `teaches` cells in SOURCES.md are paraphrases, not located quotes.** `corpus/SOURCES.md:217` (“Hooks sort by name without the .hook suffix…”), `:218` (“The manual states the suffix-ignoring alphabetical order…, so S208 and S209 agree”), `:219` (“A Pre-phase error stops the transaction…”) and `:220` (“The system hook directory is the list head…”) read as restated propositions, and `:218` is commentary about the pair rather than manual text. The Gate table therefore supplies fresh literal strings; the lesson must not re-present the `teaches` cells as quotations. This is a presentation defect, not a coverage one: the propositions are supported by the snapshot lines cited above.
2. **S212's `teaches` cell (“read without running pacman”, `corpus/SOURCES.md:221`) is contradicted by its own capture.** `capture-meta.txt:2` is `$ pacman -Q pacman` and `:4` is `$ pacman-conf HookDir`; pacman and pacman-conf were invoked (read-only queries), and `capture-meta.txt:1` says only `read-only`. No transaction or hook was run, which is the defensible claim. Recommend the lesson say “captured by reading the hook files, with `pacman -Q`/`pacman-conf` queries only; no transaction or hook run” instead of “read without running pacman”.
3. **The “70 files / 67 system / 3 operator / one same-name pair” count is derived, not quoted.** `capture-meta.txt` never states a count; the numbers come from the 70-line `MANIFEST.sha256` and the two directory listings (commands above). A Gate quote cannot literally carry that proposition, so the S212 row quotes capture provenance and puts the computed counts in Location. If the Gate convention requires the quote itself to prove the count, S212 fails that convention; I did not fabricate a capture line to fix it. Flag to the closure reviewer.
4. **Tier call.** All five rows retain tier A as declared in `corpus/SOURCES.md:217-221`; S208–S211 are primary upstream source at the installed commit, S212 is own-work host capture, matching the round-37 own-work precedent (`corpus/lessons/round-37.md:17-18`, S206/S207 “admit, mined, tier A, own-work”).

## Not done

- The four GitLab URLs were not re-fetched; provenance rests on `sources/SHA256SUMS:1` plus digest equality, so no URL-liveness claim is made.
- No lesson file was assembled and no lane file touched; the two C2 counters were not run (outside this item).
- No scratch directory was needed; nothing under `/fast/scratch` was created.
