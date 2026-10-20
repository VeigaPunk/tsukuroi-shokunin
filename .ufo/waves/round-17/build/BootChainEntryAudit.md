# BootChainEntryAudit — boot-chain-r17.md v2

v2 symlink chain (md:45–48; E:5/E:8/E:10; S057) verified.

1. md:71–73; JSON `verdict_rules[2]`/`linux.note`: "no /etc or /usr input newer" overstates B:256's nine paths; /boot/limine.conf changed (B:106, S:118–122) outside the rule. Fix: enumerate; bind via S:113–115 + S:34/B:172.
2. md:64–65; JSON `linux`/`linux-lts` evidence: symlink cell uncited — B:181/197 are type-blind `dirs:`, lts cites no E. Fix: add E:5/E:8/E:10.
3. md:45: "every 42.2 image" observes one; universal is `functions:1212–1213` (E:9–10). Fix: split obs/inf (Q17/19).
4. md:29–30,33–34,102–103: `[obs]` asserts copier, "cause", "same menu" — inferences. Fix: split `[inf]` (Q3).
5. md:43–44: "byte-identical … upstream" unsupported; hashes prove image=installed only (B:183–184=B:252–253). Fix: reword (Q19).
6. md:3: "only privileged step is `sudo -n cat`" false; tool runs `sudo -n` sha256sum/b2sum/stat/objcopy/`btrfs property get`/find (`tools/boot-chain-audit.sh:60–66,193–349`). Fix: use its $WORK guarantee.
7. md:145/154/155: Q2 false (md:113–115 LUKS; md:132 `ls -d`); Q10 misses `arch-news-gate-2026.md:21` (mkinitcpio 41.1 "current", no R17 notice; registry covers 5 files); Q11: no round-17 LOG entry (LOG.md:907–927). Fix: anchor/add notice/mark pending.
8. md:157/160: Q14 circular, skips 13/15–18/20; "25" is not a criterion. Fix: evaluate/N-A; drop 25.
9. JSON `captured_at`: "13:0x" placeholder (E:2 13:02:39; S:2 13:03:06). Fix: exact.
10. md:86–87/132: B:157 is a command with a summarized token; "0 of 58674" mixes 9-path/3-tree scopes; `dirs:` "came from `ls -d`" unrecorded (B:169). Fix: reword.

Deviation: read-only bash text inspection; no host probe/write.

Scope: executed=grep,ls,sed,tail,head,wc,find,nl
