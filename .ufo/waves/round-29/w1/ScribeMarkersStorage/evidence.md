# Evidence for the O09 to O12 draft (ScribeMarkersStorage, round 29 wave 1)

All commands run from the seat clone `/fast/scratch/hyaku/tsukuroi-r29/ScribeMarkersStorage/repo`, a
`git clone --no-local` of the lane checked out at `81a061a67466c5e1be812814a895a4b5ed89b4ff`, with
`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE` on every git call. No network read was needed.

## 1. Anchors at the pinned revision

`git show 81a061a:corpus/knowledge/storage-health-r26.json | grep -cF "<anchor>"` for the four frozen
`ITEMS` anchors of `tools/check-owed-statements-r29.py`:

```
1	under shorter names (write_errs, read_errs, flush_errs, corruption_errs, generation_errs)
1	systemd sets that attribute on journal files by default
1	No scrub record exists on this host
1	FAILED! otherwise
```

`git show 81a061a:corpus/knowledge/storage-health-r26.json | grep -c corrections_r29` → `0`
(no marker array before this draft).

## 2. Correction prose lines at the pinned revision

`git show 81a061a:corpus/knowledge/storage-health-r26.md | sed -n '128p;129p;133p;135p' | cut -c1-200`;
the file has 135 lines, so line 135 is its last line:

```
128: - SH1 names, corrected (RevS133): only write, read and flush have shorter names in sysfs (`write_errs` against `write_io_errs`); `corruption_errs` and `generation_errs` are the same in both views. The
129: - SH5 wording (RevRowSH5): "FAILED! otherwise" and the SKILL row's "exactly when" hold only after a successful SMART log read; with no `-H`, a failed Identify Controller or a failed log read, smartctl
133: - SH4 scope and action (RevRowSH4): "no scrub record exists on this host" is narrowed to what was read: no status file and no `scrub: started` or `finished` kernel line in the six retained boots (live
135: - SH3, late wave-2 corrections (RevRowSH3): "systemd sets that attribute on journal files by default" is stale for systemd 262. Since systemd 220 the NOCOW flag comes from the tmpfiles snippet `journa
```

## 3. Registry cells for the two cited sources

`git show 81a061a:corpus/SOURCES.md | grep -n '^| S13[34] |'` → lines 139 (S133) and 140 (S134). Cell 11
(used-by) of both is exactly `corpus/knowledge/storage-health-r26.md`; status cell 8 is `mined`, opened
cell 9 is `2026-10-22` (parsed with the same cell split the counter uses).

R3 predicate of `tools/check-storage-health.py`, evaluated on both cell forms:

```
'corpus/knowledge/storage-health-r26.md' -> True
'corpus/knowledge/storage-health-r26.md, corpus/knowledge/storage-health-r26.json' -> True
```

## 4. Counter runs

Declared command, `python3 tools/check-owed-statements-r29.py --revision <REV> --lane .`, from the
clone:

- `--revision 81a061a67466c5e1be812814a895a4b5ed89b4ff` → last line
  `{"revision": "81a061a...", "items": 12, "marked": 0, "unmarked": ["O01",...,"O12"], "counter_sha256": "5b6cf227580ff26e47db5888001febc7ff38b97322bd496121a6aa84c2dc6375"}`,
  process exit 1.
- final block plus used-by cells, scratch commit `c4e4173f5db7671cbf2cc4a85ec356e69bfb87c1` (the
  delivered `draft.md` block, inserted verbatim into the `81a061a` entry; the sandbox commit earlier
  named `b13b1f7b...` carries the same block before the O09 `now` gained its snapshot sentence) →
  `marked` 4, unmarked `["O01","O02","O03","O04","O05","O06","O07","O08"]`, exit 1
  (`git diff --stat 81a061a HEAD`: `corpus/SOURCES.md` 4 ++--, `corpus/knowledge/storage-health-r26.json`
  6 ++++++, 8 insertions, 2 deletions). Item lines:

```
{"basis": {"paths": ["corpus/knowledge/storage-health-r26.md:128"], "sources": ["S133"], "unresolved": []}, "file": "corpus/knowledge/storage-health-r26.json", "id": "O09", "ok": true, "verdict": "corrected"}
{"basis": {"paths": ["corpus/knowledge/storage-health-r26.md:135"], "sources": [], "unresolved": []}, "file": "corpus/knowledge/storage-health-r26.json", "id": "O10", "ok": true, "verdict": "corrected"}
{"basis": {"paths": ["corpus/knowledge/storage-health-r26.md:133"], "sources": [], "unresolved": []}, "file": "corpus/knowledge/storage-health-r26.json", "id": "O11", "ok": true, "verdict": "qualified"}
{"basis": {"paths": ["corpus/knowledge/storage-health-r26.md:129"], "sources": ["S134"], "unresolved": []}, "file": "corpus/knowledge/storage-health-r26.json", "id": "O12", "ok": true, "verdict": "qualified"}
```

- draft without the used-by cells, scratch commit `6a331d943889bba7d4e85fbc2a0fd5d95e3c1b69` →
  `marked` 4, exit 1; O09 and O12 `ok` with `"sources": []` and `"unresolved": ["S133"]` /
  `["S134"]`.

## 5. Entry parse under the storage-health tool's loader

`json.loads(text, object_pairs_hook=<the tool's duplicate-key hook>)` on the patched entry:
`schema = tsukuroi-storage-health-r26-v1`, `rows = 6` (`SH1` to `SH6`), `corrections_r29 = 4`.

`tools/check-storage-health.py --revision b13b1f7b... --repo .` returned exit 2 with
`{"status": "CANNOT_EVALUATE", "findings": [{"id": "E-REVISION-NOT-PUSHED", "site": "refs/remotes/origin/master"}]}`;
the tool binds the measured revision to a pushed ref, and pushing is outside this seat's bounds, so no
end-to-end run of that tool is claimed for the draft.

## 6. Bytes

Sandbox tree after the draft (`sha256sum` in the clone):

```
cdcdf617f530c82b1328eb2ae33899df0455239f64bb51db1b7e4618db7153f6  corpus/knowledge/storage-health-r26.json
ec1fe77360c34fae5e8a5d549c510feab888f03830c88d8f8dce2a68db0a9e00  corpus/SOURCES.md
```

Seat deliverables:

```
0ae269dbc233f32ba34ce66475ee8f71528a9e5845214241a22f9786592cba50  draft.md   (bytes as first written)
b5cc6babab3e0a6c0321032d4ba0f5eba1add1e7cd4fb1c39b55a8c831a253fc  corrections_r29.json
```

`draft.md` was edited after that first hash (two wording edits), so its current digest is the one in the
report, not the value above.
