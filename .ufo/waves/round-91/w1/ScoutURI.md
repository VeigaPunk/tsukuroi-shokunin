# ScoutURI — round 91 w1, C2 sources (URI-resolution half)

Lane revision measured: `master` = **2d7e09e101996cc1ac5836c6d635f3f608453ac5** (frozen battery
`tools/limine-pin-battery-r91.py` sha256 `655ee8f3d0942e958cc853deb2d16abcd2d16ae2823ca6548f2a53991b4901b9`,
matching the spec). Landed gate `tools/check-limine-pins.py` sha256
`62bb06c997fb99a9fd811ec97440eebe2dafa7e63c4f21f43aa0ead9af7da737`.

Seat dir: `.ufo/waves/round-91/w1/ScoutURI/`. **No lane file was edited.** Read-only; no sudo; no host
write. Nothing was booted.

## Verdict per check

| Check | Verdict |
|---|---|
| C2 (exploratory, depth 8): `uri_resolve` on the host's line-72 shape | **met** — the mechanism is established and measured |
| C2 sub-question: what `uri_open` does with the result | **met** — `NULL` for a shape failure, opens-with-no-hash-check for the absent-hash case |
| C2 sub-question: `uri_open_optional` vs `uri_open`, and whether the optional path changes the failure mode | **met** — two call sites, and the optional path only converts `URI_ERROR` from panic to print |
| Pinned snapshot byte-identical to upstream v12.9.4 and to a fresh tag clone | **met** — three-way sha256 match |
| Host receipt line 72 read (read-only) | **met** — but see the truncation finding below |

## What the source says, measured

I compiled `uri_resolve` (pinned `uri.c` raw lines 32-107, verbatim) with upstream's `URI_ERROR`/`panic`
semantics and ran it. The decisive result for C2:

- **Exactly three of `uri_resolve`'s failures are message-free** — no `(` (line 49), no `):/` (line 62),
  empty path (line 74). No `URI_ERROR`, no panic at that layer.
- **A value with shape but no `#` is not a failure.** The host's line 72 value
  `boot():/EFI/BOOT/BOOTX64.EFI` resolves to resource `boot`, root ``, path `EFI/BOOT/BOOTX64.EFI`,
  **hash `NULL`** — `ret=true`. The hash loop simply never matches and the function falls through to
  `return true` (line 106).
- **A malformed hash is loud, not silent.** `URI_ERROR("Blake2b hash must be 128 characters long")` →
  `panic` on a required key (harness prints `PANIC(...)`, exits 7). Same for a non-hex character.

So the "no URI shape at all" wording in the C2 brief covers three cases; the host's line 72 is a *fourth*
case (shaped, unhashed) that is **not** in that set and does not fail to resolve. It fails later, or
rather it does not fail at all: with `hash == NULL` no hash filter is installed (line 483) and the final
comparison is guarded by `hash_fh != NULL` (line 663), so there is **no comparison to mismatch**. The
Secure-Boot-unhashed rule (line 372) cannot fire for it either, because `chainload` clears
`secure_boot_active` around the `uri_open` call (chainload.c 426-427) — the firmware's `LoadImage` verifies
the signature instead (chainload.c 423-425).

## Gate behaviour (landed gate, fixtures in `receipt-gate-observations.txt`)

- The host's line-72 shape → `unverified_image_lines [3]`, `verdict HEALTHY`, `rc 0`, `pins []`.
- The **same** efi entry with a hash, file absent from the ESP → `LP-MISSING` / `panic`, `DEGRADED` rc 1.
  With the hash removed → `HEALTHY` rc 0, `unverified [3]`. The unhashed form **hides a missing-file
  condition** the hashed form surfaces.
- Same for a bad resource: unhashed `bogus():/p` → `unverified [3]` / `HEALTHY`; hashed
  `bogus():/p#<128 hex>` → `LP-BAD-RESOURCE` / `panic` / `DEGRADED`.
- A value with a `#` inside the resource name (`boot#x():/p`) resolves in Limine to resource `boot#x`,
  which is not one of the seven known resources, so Limine would panic — but the gate reports it as
  merely `unverified`.

These are **observations of the frozen rule set's behaviour**, not a proposal to re-scope it. U1 is a
reporting contract ("changes no pin verdict, status, consequence or rc") and I did not touch it.

## Defect found (read-only report; L1 decides)

**The r91 host receipt's `path:` lines are truncated at 140 columns**, so the hash status of five of the
six efi image lines is unknowable from it. Lines 30 and 38 show 93 and 89 hash characters where a real
blake2b hash needs 128; lines 50/56/64 show no `#` only because the line is cut. **Only line 72
(37 columns) is complete.** The r90 receipt's `LP-MISMATCH line 30` / `LP-MISMATCH line 38` findings
require a hash to compare against, so the real lines 30/38 do carry hashes; the two receipts disagree on
their face purely because of the truncation. The r91 receipt is frozen in the manifest
(sha256 `10914f675f2778c91315b5c3fdc06165bf0a681fb8e53828bcc8eef94410c77a`), so this seat changed
nothing — but any C2 text that says "line 72 is the only unhashed image line" should be read as "line 72
is the only image line whose value the receipt shows **in full**".

## Deliverables

- `.ufo/waves/round-91/w1/ScoutURI/proposed-rows.md` — 29 candidate rows (UR1-UR29) for
  `corpus/knowledge/limine-unverified-image-r91.md`, each labelled `[src]`/`[obs]`/`[inf]` with file:raw
  lines, a ≤25-word verbatim quote, and the host value.
- `.ufo/waves/round-91/w1/ScoutURI/proposed-sources.md` — three SOURCES row drafts (S377-S379, ids TBD;
  the registry's highest used id is S376) plus a note that `common/entry.s3.c` is **not pinned** this
  round and needs pinning before a row may cite it.
- `.ufo/waves/round-91/w1/ScoutURI/receipt-uri-resolve.txt` — the three-way sha256 identity check and
  both harness outputs.
- `.ufo/waves/round-91/w1/ScoutURI/receipt-gate-observations.txt` — the landed-gate fixture runs and the
  receipt-truncation arithmetic.
- `.ufo/waves/round-91/w1/ScoutURI/receipt-quote-verification.txt` — machine check that all 28 quotes are
  substrings of their named raw line ranges and ≤25 words (`ALL_OK`).
- `.ufo/waves/round-91/w1/ScoutURI/uri_resolve_probe.c`, `uri_resolve_probe_argv.c` — the harness sources.

## Refused / not done

- Did not boot Limine, did not run `limine`, did not touch `/boot`, `/efi`, `/etc`, `/usr`, `/var`, did
  not use `sudo`. The host statements come from the committed receipt only.
- Did not edit `corpus/SOURCES.md`, `corpus/knowledge/limine-unverified-image-r91.md`,
  `tools/check-limine-pins.py` or the frozen battery. The three claims above are candidate rows and
  drafts only.
- Did not read `/boot/limine.conf` directly (permission denied); the receipt's truncation is the
  reason the host's hash status cannot be established here.
- No subagents spawned (leaf seat). No model passed or chosen.
- Tooling: no install was needed — `gcc` (present at `/usr/bin/gcc`), `git` and `python3` were already
  on the host. No pacman transaction was run.
- Scratch `/fast/scratch/hyaku/tsukuroi-r91/ScoutURI/` was removed after the receipts were copied into
  the wave dir.

## Remaining unknowns

- Whether the six host efi image lines other than 72 carry hashes — needs the untruncated `/boot/limine.conf`
  (operator-side, read-only).
- Whether `common/entry.s3.c` will be pinned for round 91 (needed for the S378 row).
- The `uri_open` dispatch and the `chainload` wrapper were **read**, not executed: the harness exercises
  `uri_resolve` alone. The dispatch and wrapper claims are `[src]`, not `[obs]`.
