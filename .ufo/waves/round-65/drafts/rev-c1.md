# REV-C1 — attack on claim C1 (round 65 w1) — seat R1RevC1, 2026-11-03

**Verdict: AGREE-WITH-ADMISSION.** C1's evidence survives every attack I ran: the S282
capture is live-identical (third independent fetch), the Gate quote is verbatim-faithful and
23 words, the do-nothing control cannot reach the target, and the SY4 applicability verdict
repelled all four falsification readings I tried. Five findings below are integration-time
fixes (none verdict-flipping); two predicates are executable only at round end.

## 1. S282 live re-open — PASS

- URL from `before/s282-open-receipt.txt`: `https://api.github.com/repos/systemd/systemd/releases/tags/v262`.
  My refetch: HTTP 200, 55194 bytes, sha256 `008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b`
  — byte-identical to the before capture and to S1Scout's 19:39:10Z refetch (three fetches, one day, one hash).
  `tag_name` v262 / `name` "systemd v262" / `published_at` 2026-09-22T13:19:16Z all match the receipt.
- Gate quote `The UKI must also embed a signed PCR policy that is bound to the initrd boot phase and
  with the "initrd" policy reference.` → `wc -w` = **23** (≤ 25 ✓). Present in the live body
  whitespace-normalized ×1 (strict single-line grep 0 — the source's own CRLF wrap; sentence spans
  body lines 444-446). SY1's 3-sentence 49-word quote also normalized-present ×1; the bullet's first
  sentence `The way that NvPCRs are anchored has been improved.` is strict single-line ×1.
- Location: heading at body line 437 is `##` + **9 spaces** + `Changes in the TPM Subsystem:`
  (24 `##` sections; exactly one TPM section). The quote is inside the first bullet of that section
  (bullet spans lines 439-452). The note's in-table citation is by title ("Changes in the TPM
  Subsystem") and is exact; only the header `source:` line's `"## Changes…"` string (1 space) is a
  normalized, not byte, form (finding R3).
- v262.1 (what Arch ships) carries only a 76-char changelog-link tag note — the v262 body is the
  substantive notes and the right anchor. My live copy kept at
  `.ufo/waves/round-65/w1/seats/R1RevC1-s282-live.json`.

## 2. Do-nothing control — CONFIRMED (cannot reach target)

- `git cat-file -e 1bd8e196:corpus/knowledge/systemd262-uki-pcr-r65.md` → **rc 128** (path absent at
  base; 1bd8e196 verified = 37c74e27^, both commits).
- `git grep -c S282 1bd8e196 -- corpus/SOURCES.md` → **rc 1, 0 matches**. Base S28x rows = 2
  (S280 line 290, S281 line 291); worktree SOURCES.md = 281 rows (census-before receipt rc 0,
  `rows: 281`). A do-nothing round leaves note absent ∧ SY-count 0 ∧ SOURCES 281 — no predicate
  clause met. Control sound.
- Scope note: repo-wide `grep INITRAMFS` at base has 11 hits under `.ufo/waves/round-17/`; the
  receipt's C2 control is correctly scoped to `tools/tsukuroi-census.sh` (0 there). No contradiction.

## 3. Applicability attack (SY4 falsification attempt) — NO falsifying reading found; SY4 stands

| # | counter-reading tried | evidence | result |
|---|---|---|---|
| CR1 | "systemd-tpm2-setup-early.service (claimed shipped by mkinitcpio 42.2) runs with no TPM2 and fails at boot" | `pacman -Ql mkinitcpio \| grep -iE 'tpm\|pcr\|ukify'` → rc 1 (zero files): mkinitcpio ships none host-side. The unit is owned by **systemd 262.1-1**, statically wanted (`sysinit.target.wants/systemd-tpm2-setup-early.service`), but `ConditionSecurity=measured-os` + `ConditionPathExists=!/run/systemd/tpm2-srk-public-key.pem` (unit lines 17-18) skip it: journalctl -b (Nov 02 boot) shows `Early TPM SRK Setup skipped, unmet condition check ConditionSecurity=measured-os`; `journalctl -b -p err \| grep -ic tpm` → **0**; `systemctl is-system-running` → `running` | **REFUTED as a failure reading** — wanted-but-skipped, zero boot failures |
| CR2 | initrd-phase NvPCR separator binds the host | `systemd-pcrnvdone.service` ("TPM PCR NvPCR Initialization Separator") has `ConditionSecurity=measured-os` + `ConditionPathExists=/etc/initrd-release` → skipped in real root (journal confirms, description matches); dormant in the real root, double-gated in an initrd | no reachable failure |
| CR3 | runtime extend path reaches lazy-init failure | `systemd-pcrextend.socket` disabled/disabled in list-unit-files → no socket-activation path today | no reachable failure |
| CR4 | "UKIs exist on this host, so the v262 UKI requirement binds" | TRUE the host boots UKIs: limine 12.9.4 → `/EFI/Linux/omarchy_linux.efi`, Current Stub **systemd-stub 262.1-1-arch** (bootctl). But `TPM2 Support: no`, `Measured UKI: no`, `Secure Boot: disabled`, `/dev/tpm*` absent (ls rc 2), `/sys/class/tpm{,rm}` empty → whether the UKIs embed the defs is unobservable and no NvPCR can be extended — exactly SY4's reading. Latent gap sharpened: `systemd-ukify` not installed, `command -v ukify` rc 1 → the host **cannot produce the required signed initrd PCR policy at all today**; a firmware TPM2 appearance fires SY4's named falsifier | SY4 verdict CONFIRMED (exposure real but latent) |

Corroboration detail: shipped `hardware.nvpcr` carries `"orderly": false`, matching the body's later
bullet (body lines 466-467: `…TPMA_NV_ORDERLY flag (which remains enabled by default). The
"hardware" NvPCR will now disable by default…`). The note quotes it with single quotes ('hardware')
— words identical, quote-mark style differs (finding R4, info).

## 4. Row shape + receipting — PASS with fixes

- Planned S282 row (scout-s282.md §5.1 primary, full line read raw): `awk -F'|'` → **NF 13, 11
  cells, zero pipes inside any cell**; kind docs / tier A / status queued (house has 5 queued,
  253 mined, 23 rejected — enum valid) / opened 2026-11-03 / recheck on-release / used-by the note
  path. House form consistent: new source (no supersedes — that form is for re-pins like
  S280→S021/S281→S022); the S279 cross-link lives in the note, as the house does for new sources.
- **Independent fleet-validator run** (my fixture, my scratch): real `corpus/SOURCES.md` + row
  inserted directly after S281 (line 292) + full `corpus/ tools/ SKILL.md` →
  `sources-census.sh validate --today 2026-11-03` → **rc 0, 0 E-codes, 282 rows, final line `ok`**.
  EOF-append control → **E12 "S282 row outside Registry section", rc 1** — insertion at line 292 is
  required and verified; appending at EOF is a real routed hazard (S1Scout's §5.4 confirmed
  independently).
- Note draft: `grep -c '^| SY'` = **5** (≥ 5 ✓). Header `source:` / `verified-at: 2026-11-03` /
  `recheck: on-release…` all at column 0, no fences → knowledge-header gate rules
  (tools/check-knowledge-header.py: MISSING/VALUE, column-0 + fence-aware) predict **PASS**. The
  gate reads `corpus/knowledge/` at a git revision, so the actual PASS executes at the work revision
  after landing — not runnable pre-landing from this read-only seat.
- Receipting: every live value the note cites has a `probes/` file (10 present; cited: r65-bootctl,
  r65-tpm2-units, r65-limine-conf, r65-boot-inventory, r65-ukify, r65-nvpcr, r65-mkinitcpio-conf;
  r65-versions covers systemd 262.1-1 / mkinitcpio 42.2-1 / limine 12.9.4-1 / kernel 7.2.11-arch1-1).
  I re-derived: /etc/mkinitcpio.d/ empty ✓, 4 conf.d drop-ins ✓, `/usr/lib/initcpio/hooks` = 12 with
  exactly btrfs-overlayfs + plymouth naming /new_root ✓ (SY3's "12 hooks, 2 name /new_root").
  "Committed with-or-before the citing commit" is pending round end (probes/ untracked today).

## Findings (fix at integration; none verdict-flipping)

- **R1 (low, note):** SY table header declares 4 columns `| id | row | ground | receipt |` (NF 6)
  but all five SY rows carry **3 cells** (NF 5) — receipt paths render into the ground column and
  receipt stays empty. Fix header to 3 columns or split cells before landing.
- **R2 (low, note):** SY3 "images built 2026-10-20 (the mkinitcpio-42.2 upgrade day), 281-290 MB
  each" — the note's own receipt (r65-boot-inventory.txt) shows the **live**
  `/boot/EFI/Linux/omarchy_linux{,-lts}.efi` are dated **2026-10-29 03:45** (284447744 / 281338880
  bytes); only the `limine_history/` snapshot copies are 2026-10-20 (290422784 / 284439552 /
  281318912 bytes). Reword to split live-vs-snapshot dates (the 281-290 MB span remains true).
- **R3 (info, note):** header line 1 `source:` cites the section as `"## Changes in the TPM
  Subsystem:"` (1 space); the stored heading has 9 spaces after `##`. Title-only citation (as SY1
  uses in-table) is exact — drop the byte-claim or note the byte form.
- **R4 (info, note):** SY1 quote-mark style: body wraps "hardware" in double quotes; note writes
  'hardware'. Words identical; optional normalization.
- **R5 (info, wording):** SY1's "mkinitcpio v42.2 ships systemd-tpm2-setup-early.service +
  systemd-pcrnvdone.service" is S279's installer-side wording carried as a quote; host-side both
  units are `pacman -Qo`-owned by systemd 262.1-1 (both rc 0). No change required.

Pending at round end (not defects): note lands at `corpus/knowledge/systemd262-uki-pcr-r65.md`;
SOURCES row inserts at line 292 (never EOF → E12); probes/ + note + row committed with-or-before
the citing commit; knowledge-header gate runs at the work revision; round-end census rc 0
(before receipt rc 0, rows 281 already on file).

## Residual risk / verification gaps

- Round-end predicates (census rc 0 at 282 rows, header gate at work revision, commit ordering) are
  executable only post-landing; predicted PASS on today's evidence.
- `/boot/limine.conf` mtime **2026-11-03 16:19:30 -03:00**, ~20 min before the probe receipt
  (limine-snapper-sync 1.32.1-2 installed; no attribution attempted, read-only round). The note
  quotes limine.conf via r65-limine-conf.txt taken after that mtime; a recheck should re-read if it
  changes again.
- GitHub API byte-identity is observed (16:33 + 19:39 + my fetch, same day), not guaranteed;
  ETag `W/"fb5e0d08…"` + Last-Modified 2026-09-23T14:57:45Z recorded in scout §1 as recheck handles.

## Commands run (all rc)

| command | rc |
|---|---|
| `mkdir -p /fast/scratch/hyaku/tsukuroi-r65/R1RevC1` | 0 |
| `ls -la` before/probes/drafts/w1/w1-seats | 0 |
| `git -C <lane> status --porcelain` (M tools/tsukuroi-census.sh; wave dirs untracked) | 0 |
| `git -C <lane> rev-parse HEAD` / `cat-file -t 37c74e27` / `rev-parse 37c74e27^` / `cat-file -t 1bd8e196` | 0 (1bd8e196 = 37c74e27^, commits) |
| `git -C <lane> cat-file -e 1bd8e196:corpus/knowledge/systemd262-uki-pcr-r65.md` | **128** (absent — control) |
| `git -C <lane> grep -c S282 1bd8e196 -- corpus/SOURCES.md` | **1** (0 matches — control) |
| `git -C <lane> grep -c '^| SY' 1bd8e196 -- corpus/knowledge/` | 1 (0) |
| `git -C <lane> show 1bd8e196:corpus/SOURCES.md \| grep -cE '^\| S28[0-9]'` | 0 (count 2) |
| `git -C <lane> grep -c INITRAMFS 1bd8e196` | 0 (11 hits, .ufo/waves/round-17 only; C2 control scoped to the census script = 0) |
| `pacman -Q systemd systemd-ukify mkinitcpio` | systemd 262.1-1, mkinitcpio 42.2-1; systemd-ukify not found |
| `systemctl --version \| head -2` | 0 (systemd 262 (262.1-1-arch)) |
| `ls -la /sys/class/tpm /sys/class/tpmrm` | 0 (both empty) |
| `systemctl list-unit-files \| grep -iE 'tpm\|measure\|pcr'` | 0 (tpm2-setup-early static/wanted; pcrextend.socket disabled) |
| `bootctl status --no-pager` | 0 (Secure Boot disabled; TPM2 Support no; Measured UKI no; Limine 12.9.4; stub 262.1-1-arch) |
| `journalctl -b --no-pager \| grep -inE 'tpm'` | 0 (all hits = "skipped, unmet condition" + 1 chromium tmpfiles path; zero failures) |
| `journalctl -b --no-pager \| grep tpm2-setup/srk/nvpcr minus skips` | 0 (no lines) |
| `journalctl -b -p err \| grep -icE 'tpm'` | 0 (count 0) |
| `systemctl is-system-running` | 0 (running) |
| `cat /proc/cmdline` | 0 |
| `pacman -Ql systemd \| grep -iE 'ukify\|tpm2-setup\|pcr'` | 0 (nvpcr defs + units; no ukify) |
| `pacman -Ql mkinitcpio \| grep -iE 'tpm\|pcr\|ukify'` | **1** (none) |
| `ls -la /usr/bin/ukify /usr/lib/systemd/system/systemd-tpm2-setup*.service` | units present; ukify No such file (2) |
| `grep -rln 'NvPCR' /usr/lib/systemd/system/*.service` + Description/Condition greps | 0 |
| `pacman -Qo /usr/lib/systemd/system/systemd-pcrnvdone.service` | 0 (owned by systemd 262.1-1) |
| `ls -la /etc/mkinitcpio.d/` / `ls -la /etc/mkinitcpio.conf.d/` / `ls /etc/initcpio/hooks \| wc -l` | 0 / 0 (4 drop-ins) / 0 (count 0) |
| `ls /usr/lib/initcpio/hooks \| wc -l` + `grep -l /new_root /usr/lib/initcpio/hooks/*` | 0 (12; exactly btrfs-overlayfs + plymouth) |
| `ls -la /dev/tpm*` | **2** (No such file) |
| `uname -r` / `hostname` | 7.2.11-arch1-1 / plazir27 |
| `grep -n '^| S28' corpus/SOURCES.md \| tail -6`; header; `grep -cE '^\| S[0-9]'`; S281 NF | 0 (S280@290, S281@291; 281 rows; NF 13) |
| `cat before/s282-sha256.txt`; `sha256sum` both captures | 0 (008e1265… + body cb2d1416…) |
| `curl -sS -o $S/s282-live.json <S282 URL> -w …` | 0 (HTTP 200, 55194 B) |
| `sha256sum $S/s282-live.json` + tag/name/published greps | 0 (**== 008e1265…**) |
| python quote checks on live body (gate quote words/in-body; q2; q3; hardware bullet) | 0 (23 / True / True / True; 'hardware' single-quote variant False → double-quote form confirmed at body lines 466-467) |
| `awk -F'\|'` NF scan of note draft + `wc -l`; `printf '%s' '<gate quote>' \| wc -w` | 0 (SY rows 5 @ NF 5; header/sep NF 6; 26 lines; 23 words) |
| `awk -F'\|'` on scout line 144 (planned row) | 0 (NF 13, cells 11, no pipe-in-cell) |
| python fixture build (fxint minimal) + `sources-census.sh validate` | 1 (fixture-artifact E11s only; **no E-code on S282**) |
| python fixture build (fxeof, row at EOF) + validate \| grep E12 | **E12 present, rc 1** |
| python fixture build (fxint2: full corpus/tools/SKILL.md, row at 292) + validate | **0 (0 E-codes, 282 rows, ok)** |
| reads: note draft, scout-s282.md, before/* receipts, probes/* receipts, LOG.md 2844+, SCORECARD.md 4789+, tools/check-knowledge-header.py head, scripts/sources-census.sh head | 0 |

No sudo used (bootctl and all probes ran unprivileged; no /boot reads by this seat). No tool
installs. No mutating git/jj command anywhere. No writes outside: drafts/rev-c1.md,
w1/seats/R1RevC1.md, w1/R1RevC1.md, w1/seats/R1RevC1-s282-live.json, and scratch
/fast/scratch/hyaku/tsukuroi-r65/R1RevC1/ (removed before yield; live JSON copied out first).
