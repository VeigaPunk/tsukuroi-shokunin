# Proposed entry patch — hibernate-resume-plane-r84.md Limits (defect R84-SCRIBE-F1)

Owner: lane L1 (this seat does not edit lane files). Target:
`corpus/knowledge/hibernate-resume-plane-r84.md:50-52`. Class: missing observable, not a false statement.

## What is wrong

The Limits bullet says "no resume was exercised" and cites only that no hibernation entry or exit exists.
The chain's boot-time image lookup **is** exercised on every retained boot and its failure is logged:

- `journalctl -b -g 'Image not found'` → `Nov 02 12:07:17 plazir27 kernel: PM: Image not found (code -22)`, rc 0.
- `journalctl --no-pager -g 'hibernation entry|hibernation exit'` → two boot-separator lines and `-- No entries --`.
- Same pair already recorded at `corpus/knowledge/journal-boot-plane.md:64` and `:249-252` (`PM: Image not
  found (code -22)` exactly once per retained boot except the −12 live ISO).

The entry and the README row therefore claim less evidence than the host actually gives: the configured
chain is reached at boot, and what is absent is an image, not a resume path.

## Proposed text (append one Limit bullet after line 52; nothing above is rewritten)

```
- [observed] The boot-time image lookup runs and fails for a known reason on every retained boot:
  `journalctl -b -g 'Image not found'` → `Nov 02 12:07:17 plazir27 kernel: PM: Image not found (code -22)`,
  and `journalctl --no-pager -g 'hibernation entry|hibernation exit'` prints boot separators and
  `-- No entries --` (same pair as `journal-boot-plane.md:64`, `:249-252`). This shows the kernel reached
  its image read; it does not show that the read used the btrfs swap header (HR2/HR3) or that a hibernation
  image was ever written.
```

## Why it is not a claim of success

`-22` (`EINVAL`) is what swsusp logs when no image signature is found. It is consistent with a correct
configuration and with a broken one, so it adds a bounded observation, not a pass. It also names the one
surface a future frontend measurement can use: the position of the `-22` record among initramfs steps
(`journal-boot-plane.md:357` still lists that writer/phase question as open).

## Alternatives considered

- Rewriting the "silent until first resume" sentence at `:12-13`: rejected, because the sentence is about
  the absence of a *success* signal and stays true; only the Limits enumeration is incomplete.
