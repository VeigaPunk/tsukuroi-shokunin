# SrcPlymouthUpdateRootFs

Opened 2026-10-20, `main` @ `03fe0c1f`, base `https://gitlab.freedesktop.org/plymouth/plymouth/-/raw/main/`.

[obs] `--new-root-dir` is client-only (`src/client/plymouth.c:952-959`); daemon options have no root flag, `src/main.c` only runs `plymouthd_run`. Man page: `"Root filesystem is about to change"` (`docs/plymouth1.xml:194-204`). Client sends NEWROOT then SYSTEM_INITIALIZED with `--read-write` (`plymouth.c:739-751`); server ACKs unconditionally (`src/ply-boot-server.c:787-790,821-823`), so bad paths report success.

[obs] `plymouthd_handle_newroot` (`src/daemon/plymouthd-actions.c:205-231`): `chdir (root_dir); chroot ("."); chdir ("/");`, returns ignored, no stat/statvfs/mountpoint test. Only `/run/initramfs` is special-cased (:216-220).

[obs] Existing empty dir: chroot succeeds and all later absolute paths resolve inside it; progress-cache load fails silently (`src/libply/ply-progress.c:167-169`). boot.log opens only at SYSTEM_INITIALIZED to `/var/log/boot.log` (`src/daemon/plymouthd-logging.c:114`, `O_CREAT|O_APPEND` `src/libply/ply-logger.c:43`); failure only traces `"failed to open log: %m"` (:189) — no boot.log, no spool. Missing dir: [inf] `chroot (".")` re-roots to cwd. An already-open log fd survives chroot; the client sends NEWROOT before SYSTEM_INITIALIZED in one call.

[obs] Splash: only `ply_boot_splash_root_mounted` (:229-231; NULL guard `src/libply-splash-core/ply-boot-splash.c:630-635`); two-step/space-flares set an unread `root_is_mounted`; details/text/tribar/fade-throbber/console-viewer implement nothing; script themes dispatch a callback. Newroot never hides the splash.

Does not establish: host hook's NEW_ROOT; whether this host's `/new_root` is empty (`RevNewRootDir`: 42.2 symlinks to `/sysroot`); boot.log presence; Arch package behavior; plugin sweep file-by-file (blob search HTTP 401).

Scope: executed=none
