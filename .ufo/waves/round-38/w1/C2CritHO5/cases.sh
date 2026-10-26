#!/bin/bash
# C2CritHO5 case driver v3 — canonical run. Everything under $S (scratch); no host mutation.
# Note: a hook file with NO [Trigger] short-circuits _alpm_hook_validate (hook.c:119-123),
# so every "broken" case below carries a valid [Trigger] block unless it is testing that rule.
set -u
S=/fast/scratch/hyaku/tsukuroi-r38/C2CritHO5
export TMPDIR=$S
cd "$S" || exit 1
TPL=$S/tpl
PKG=which

TRIG='[Trigger]
Operation = Upgrade
Type = Package
Target = nosuchpkg
'

mkroot() {
	local R=$S/run/$1
	rm -rf "$R"
	mkdir -p "$R"
	cp -a "$TPL/." "$R/"
	mkdir -p "$R/etc/pacman.d/hooks" "$R/usr/share/libalpm/hooks" "$R/var/log"
	echo "$R"
}

run() {
	local name=$1 R=$S/run/$1
	printf '=== %s\n' "$name"
	rm -f "$R/var/lib/pacman/db.lck"
	: > "$R/var/log/pacman.log"
	"$S/fx" "$R/" "$R/var/lib/pacman/" "$R/etc/pacman.d/hooks" "$PKG" \
		"$R/var/log/pacman.log" 2> "$S/log/$name.err" > "$S/log/$name.out"
	grep -E '^(HOOKDIRS|RESULT)' "$S/log/$name.out"
	grep -E "parsing hook file .* failed|could not open directory|could not stat file|could not read directory|Missing |invalid |overwriting|AbortOnFail set|skipping overridden|skipping directory|skipping non-hook|error while reading hook" \
		"$S/log/$name.err" | sed "s#$R##g; s/^/    /"
	grep -E "running '" "$R/var/log/pacman.log" | sed "s#$R##g; s/^/    LOG: /"
	echo
}

mkdir -p "$S/log" "$S/run"
rm -f "$S/log"/*

# T0 control: valid, never-triggered Post hook in the system dir
R=$(mkroot T0)
printf '%s\n[Action]\nDescription = control\nWhen = PostTransaction\nExec = /bin/true\n' "$TRIG" \
	> "$R/usr/share/libalpm/hooks/50-valid.hook"
run T0

# T1 broken PostTransaction-only hook (valid trigger, no Exec) in /etc
R=$(mkroot T1)
printf '%s\n[Action]\nDescription = bad post\nWhen = PostTransaction\n' "$TRIG" \
	> "$R/etc/pacman.d/hooks/50-bad-post.hook"
run T1

# T2 broken PreTransaction hook (valid trigger, no Exec) in /etc
R=$(mkroot T2)
printf '%s\n[Action]\nDescription = bad pre\nWhen = PreTransaction\n' "$TRIG" \
	> "$R/etc/pacman.d/hooks/50-bad-pre.hook"
run T2

# T2b missing When only (valid trigger + Exec)
R=$(mkroot T2b)
printf '%s\n[Action]\nDescription = no when\nExec = /bin/true\n' "$TRIG" \
	> "$R/etc/pacman.d/hooks/50-no-when.hook"
run T2b

# T3 /etc hookdir unreadable (EACCES); system dir holds one valid hook
R=$(mkroot T3)
printf '%s\n[Action]\nWhen = PostTransaction\nExec = /bin/true\n' "$TRIG" \
	> "$R/usr/share/libalpm/hooks/50-valid.hook"
chmod 0000 "$R/etc/pacman.d/hooks"
run T3
chmod 0755 "$R/etc/pacman.d/hooks"

# T4 dangling symlink named *.hook in /etc (stat ENOENT)
R=$(mkroot T4)
ln -s /nonexistent/target.hook "$R/etc/pacman.d/hooks/50-dangling.hook"
run T4

# T5 broken hook only in the system dir
R=$(mkroot T5)
printf '%s\n[Action]\nWhen = PostTransaction\n' "$TRIG" \
	> "$R/usr/share/libalpm/hooks/50-bad-sys.hook"
run T5

# T6 broken file in the system dir shadowed by a valid same-name file in /etc
R=$(mkroot T6)
printf '%s\n[Action]\nWhen = PostTransaction\n' "$TRIG" \
	> "$R/usr/share/libalpm/hooks/90-shadow.hook"
printf '%s\n[Action]\nWhen = PostTransaction\nExec = /bin/true\n' "$TRIG" \
	> "$R/etc/pacman.d/hooks/90-shadow.hook"
run T6

# T7 triggerless mask, no Exec, no When (HO3 semantics)
R=$(mkroot T7)
printf '[Action]\nDescription = mask only\n' > "$R/etc/pacman.d/hooks/50-mask.hook"
run T7

# T8 AbortOnFail on a PostTransaction hook (man page: PreTransaction only)
R=$(mkroot T8)
printf '%s\n[Action]\nWhen = PostTransaction\nExec = /bin/true\nAbortOnFail\n' "$TRIG" \
	> "$R/etc/pacman.d/hooks/50-abort-post.hook"
run T8

# T9 bad trigger value (Type = Bogus), valid When/Exec
R=$(mkroot T9)
printf '[Trigger]\nOperation = Install\nType = Bogus\nTarget = *\n\n[Action]\nWhen = PostTransaction\nExec = /bin/true\n' \
	> "$R/etc/pacman.d/hooks/50-bad-trigger.hook"
run T9

# T10 unknown section
R=$(mkroot T10)
printf '[Bogus]\nkey = value\n\n[Action]\nWhen = PostTransaction\nExec = /bin/true\n' \
	> "$R/etc/pacman.d/hooks/50-bad-section.hook"
run T10

# T11 unreadable .hook file (fopen EACCES)
R=$(mkroot T11)
printf '%s\n[Action]\nWhen = PostTransaction\nExec = /bin/true\n' "$TRIG" \
	> "$R/etc/pacman.d/hooks/50-unreadable.hook"
chmod 0000 "$R/etc/pacman.d/hooks/50-unreadable.hook"
run T11
chmod 0644 "$R/etc/pacman.d/hooks/50-unreadable.hook"

# T12 a directory named *.hook
R=$(mkroot T12)
mkdir "$R/etc/pacman.d/hooks/50-isdir.hook"
run T12

# T13 non-.hook garbage file
R=$(mkroot T13)
printf 'not ini at all [\n' > "$R/etc/pacman.d/hooks/50-bad.txt"
run T13

# T14 valid matched Pre hook + broken PostTransaction-only file in the system dir
R=$(mkroot T14)
printf '[Action]\nDescription = probe\nWhen = PreTransaction\nExec = /bin/true\n\n[Trigger]\nOperation = Remove\nType = Package\nTarget = which\n' \
	> "$R/etc/pacman.d/hooks/10-runme.hook"
printf '%s\n[Action]\nWhen = PostTransaction\n' "$TRIG" \
	> "$R/usr/share/libalpm/hooks/zz-bad.hook"
run T14

# T15 control: same matched Pre hook, clean tree
R=$(mkroot T15)
printf '[Action]\nDescription = probe\nWhen = PreTransaction\nExec = /bin/true\n\n[Trigger]\nOperation = Remove\nType = Package\nTarget = which\n' \
	> "$R/etc/pacman.d/hooks/10-runme.hook"
run T15

# T16 /etc hookdir replaced by a regular file (ENOTDIR) — the root-reachable form of the
# non-ENOENT opendir branch at hook.c:554-562 (root bypasses the DAC EACCES of T3)
R=$(mkroot T16)
rmdir "$R/etc/pacman.d/hooks"
printf 'not a directory\n' > "$R/etc/pacman.d/hooks"
printf '%s\n[Action]\nWhen = PostTransaction\nExec = /bin/true\n' "$TRIG" \
	> "$R/usr/share/libalpm/hooks/50-valid.hook"
run T16
