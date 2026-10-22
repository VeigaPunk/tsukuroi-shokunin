#!/bin/sh
# Before-state of check-self-assessment --selftest under the probe's path-wrapper and
# user-files channels, run from a clone (has .git) so the export harness error is avoided.
S=/fast/scratch/hyaku/tsukuroi-r30/CritClaimFraming
R=$S/repo
W=$S/sa
rm -rf "$W"; mkdir -p "$W/home-clean/.config" "$W/tmp" "$W/bin" "$W/home/.config/git" "$W/hooks"
base() { env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_CONFIG_NOSYSTEM=1 LC_ALL=C TMPDIR="$W/tmp" "$@"; }
printf '#!/bin/sh\nprintf "%%s\\n" "$*" >> "%s/wrap.log"\nexec /usr/bin/git "$@"\n' "$W" > "$W/bin/git"; chmod +x "$W/bin/git"
for h in pre-commit post-commit post-checkout; do printf '#!/bin/sh\necho "%s $PWD" >> "%s/hook.log"\nexit 0\n' "$h" "$W" > "$W/hooks/$h"; chmod +x "$W/hooks/$h"; done
printf '[core]\n\thooksPath = %s\n' "$W/hooks" | tee "$W/home/.gitconfig" > "$W/home/.config/git/config"
echo '*' > "$W/home/.config/git/ignore"; echo '* -text -diff' > "$W/home/.config/git/attributes"
cd "$R"
base HOME="$W/home-clean" XDG_CONFIG_HOME="$W/home-clean/.config" python3 tools/check-self-assessment.py --selftest > "$W/ctl.out" 2>&1; echo "control rc=$?"
base HOME="$W/home-clean" XDG_CONFIG_HOME="$W/home-clean/.config" PATH="$W/bin:$PATH" python3 tools/check-self-assessment.py --selftest > "$W/wrap.out" 2>&1; echo "path-wrapper rc=$? log_lines=$(cat "$W/wrap.log" 2>/dev/null | wc -l)"
base HOME="$W/home" XDG_CONFIG_HOME="$W/home/.config" python3 tools/check-self-assessment.py --selftest > "$W/uf.out" 2>&1; echo "user-files rc=$? hook_lines=$(cat "$W/hook.log" 2>/dev/null | wc -l)"
head -c 300 "$W/wrap.log"; echo; grep -m3 -E '"selftest"|failures' "$W/uf.out"
