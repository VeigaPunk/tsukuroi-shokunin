# FxAuditPrivilege — tools/boot-chain-audit.sh privilege/read-only contract

**Escalation: SURVIVES. Read-only guarantee (:124-126): FAILS. `sudo -n stat`: privilege-safe.**

What holds [obs]: there are three sudo argvs, all fixed (:252, :420, :1245). Paths must match `^boot\(\):/[A-Za-z0-9._/-]+` with no `..` (:527-528). Every redirect is opened by the user shell. bsdcpio rejects symlink, absolute and `..` paths unless `--insecure`, and lsinitcpio never passes it (bsdcpio.1:150-156). The stat output is regex-gated before use (:737).

Findings:
1. **MED [obs]: booted-bytes binding.** stat (:420) is a fresh path lookup made after objcopy and lsinitcpio. It is not tied to the copy made at :252, and no before/after check exists. limine-snapper-sync is enabled (build/SentHostSafety.md:7). The live BOOTED-OBSERVED row (audit-live.txt:5) rests on this binding. Fix: run `stat -L` before and after the cat and require the two values to match.
2. **LOW [obs]: lsinitcpio writes outside $WORK.** It always creates `mktemp -d --tmpdir` (lsinitcpio:392), and the tool never sets `TMPDIR` (asked for in SentHostSafety.md:8). Fix: run it with `TMPDIR=$WORK`.
3. **LOW [inf]: possible ESP write.** /boot is vfat `relatime` (supplement-capture.txt:144), so the root cat may update FAT access dates.
4. **LOW [obs]: analyze_tree follows symlinks in the extracted tree** (:345-363). A crafted `hooks -> /usr/lib/initcpio/hooks` makes it report host bytes as image bytes.
5. **LOW [obs]: cleanup can leave files behind.** `chmod -R u+w` (:159) cannot open dirs that have mode 0, and rm failures are ignored. Fix: `u+rwX`.
6. **LOW [obs]: conf text is globbed.** `for tok in $cmdline` (:207) expands glob characters taken from limine.conf.

Not verified [unk]: sudoers secure_path, the real FAT atime behaviour, and which partition limine actually booted from.

Scope: executed=command -v lsinitcpio,command -v bsdtar cpio
