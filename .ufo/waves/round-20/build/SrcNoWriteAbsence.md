# Rule 4 / 09:08:04 source finding

**Accessed:** 2026-10-21 (read-only). Sources below are local files; there is no public source URL for these captured records.

## Located evidence

- **Operator rule 4:** `file:///home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/boot-writers-r19.md:93`, `## Operator decision rule`, item 4. Exact quote (13 words): “No write: a snapper-cleanup run with no `Updated:` line is not a write.” It makes a categorical no-write inference from the missing log message.
- **Qualification:** same file, `## Falsify qualifications`, line 164. Exact quote (10 words): ‘Absence of `Updated:` is not proof of "not a write"’. The line further states the tool's message has no content hash, a silent/no-change path is not excluded, and the 09:08:04 cause stays `[unk]`.
- **Named supersession:** same file, `## R20-RULE4 — named supersession of Operator decision rule item 4`, lines 168–170. Exact quote (11 words): “This block supersedes only item 4 under `## Operator decision rule`”. It controls the contradiction narrowly: no captured `Updated:` line means no captured matching log event, not proof of no write or unchanged contents. It preserves the unresolved 09:08:04 cause and authorizes no host action.
- **Captured event:** `file:///home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:45-58` (bounded journal query; capture accessed 2026-10-21). Lines 47–56 show the 09:08:04 cleanup start and `home`/`root` cleanup messages; line 57 says “snapper-cleanup.service: Deactivated successfully.” No `Updated:` line appears in this excerpt.

## Interpretation and limits

The capture supports that the bounded journal excerpt records a snapper cleanup run at 09:08:04 and contains no `Updated:` message. The named R20-RULE4 block explicitly supersedes **only** operator decision-rule item 4: retain the missing-message observation, reject its conversion into “not a write.” These sources do **not** establish whether `/boot/limine.conf` or any other boot file was written, whether contents changed, why no sync message appears, or whether wiring, a lock skip, successful silent sync, or failure caused the event. No exhaustive filesystem audit or content hash is supplied.

## Candidate row recommendation

**A — admit** a bounded correction/evidence row recording the event and qualification; **reject** the historical item-4 no-write inference. Reason: the primary record supports only absence of a matching log line in its bounded excerpt, and the named qualification expressly denies that this proves no write. Flip the rejection of the no-write conclusion only if independent, exact-window exhaustive write evidence or a before/after content comparison establishes that no write occurred; absent that, keep the event cause unknown.

Scope: executed=none