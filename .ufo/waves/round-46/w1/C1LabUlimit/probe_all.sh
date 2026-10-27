#!/usr/bin/env bash
# C1LabUlimit probe driver: descriptor edge cases of tsukuroi-census.sh --identity
# Everything runs under $S (scratch); no host mutation, no lane write.
set +e
S=/fast/scratch/hyaku/tsukuroi-r46/C1LabUlimit
cd "$S" || exit 9
REAL_SHA=$(sha256sum census.sh | cut -d' ' -f1)
REAL_MD5=$(md5sum census.sh | cut -d' ' -f1)
REAL_B=$(wc -c < census.sh)
REAL_L=$(wc -l < census.sh)
line() { printf '%s\n' "$*"; }
run() { # run LABEL EXPECT_VERDICT -- command...
  local label=$1 exp=$2; shift 3
  local out rc
  out=$("$@" 2>&1); rc=$?
  line "### $label"
  line "cmd: $*"
  line "rc: $rc"
  line "out: $out"
  line ""
}
verdict() { # verdict LABEL OUT
  local out=$1 v=correct
  case "$out" in
    *"sha256=$REAL_SHA"*"md5=$REAL_MD5"*"bytes=$REAL_B"*"lines=$REAL_L"*"verified=yes"*) v=correct ;;
    *"sha256=unverifiable"*"verified=no"*) v=unverifiable ;;
    *"sha256="*) v=WRONG ;;
    *) v=other ;;
  esac
  line "verdict($2): $v"
}

line "== ground truth for census.sh (a4477049 tools/tsukuroi-census.sh) =="
line "sha256=$REAL_SHA md5=$REAL_MD5 bytes=$REAL_B lines=$REAL_L"
line "bash=$(bash --version | head -1)"
line "sh=$(readlink -f /bin/sh)  kernel=$(uname -r)  ulimit_n=$(ulimit -n)"
line ""

# ---- 1 baseline
o=$(bash census.sh --identity 2>&1); line "### baseline (cwd, relative)"
line "out: $o"; verdict "$o" baseline

# ---- 2 absolute from /
o=$(cd / && bash "$S/census.sh" --identity 2>&1); line "### absolute from /"
line "out: $o"; verdict "$o" abs-from-root

# ---- 3 relative from sibling cwd
o=$(cd /fast/scratch/hyaku/tsukuroi-r46 && bash C1LabUlimit/census.sh --identity 2>&1)
line "### relative from sibling cwd (/fast/scratch/hyaku/tsukuroi-r46, 'C1LabUlimit/census.sh')"
line "out: $o"; verdict "$o" rel-sibling

# ---- 4 ./
o=$(cd "$S" && bash ./census.sh --identity 2>&1); line "### ./census.sh"
line "out: $o"; verdict "$o" dot-slash

# ---- 5 sh
o=$(cd "$S" && sh census.sh --identity 2>&1); line "### sh census.sh ( /bin/sh -> $(readlink -f /bin/sh) )"
line "out: $o"; verdict "$o" sh

# ---- 6 bash -x
o=$(cd "$S" && bash -x census.sh --identity 2>/dev/null); line "### bash -x (stdout only)"
line "out: $o"; verdict "$o" bash-x

# ---- 7 env -i
o=$(cd "$S" && env -i bash census.sh --identity 2>&1); line "### env -i"
line "out: $o"; verdict "$o" env-i

# ---- 8 symlink to file
rm -rf lk; mkdir -p lk; ln -sf "$S/census.sh" lk/link.sh
o=$(bash "$S/lk/link.sh" --identity 2>&1); line "### symlink invocation"
line "out: $o"; verdict "$o" symlink-file

# ---- 9 hardlink
rm -rf hl; mkdir -p hl; cp census.sh hl/a.sh; ln hl/a.sh hl/b.sh
o=$(bash "$S/hl/b.sh" --identity 2>&1); line "### hardlink invocation (same inode, other name)"
line "out: $o"; verdict "$o" hardlink

# ---- 10 symlinked directory
rm -rf sd; mkdir -p sd/real; cp census.sh sd/real/c.sh; ln -sfn real sd/link
o=$(bash "$S/sd/link/c.sh" --identity 2>&1); line "### invoked through a symlinked directory"
line "out: $o"; verdict "$o" symlink-dir

# ---- 11 path with spaces / newline
rm -rf sp; mkdir -p sp; cp census.sh "sp/cen sus copy.sh"; cp census.sh "$(printf 'sp/census\nnl.sh')"
o=$(bash "$S/sp/cen sus copy.sh" --identity 2>&1); line "### path with spaces"
line "out: $o"; verdict "$o" spaces
o=$(bash "$S/$(printf 'sp/census\nnl.sh')" --identity 2>&1); line "### path with a newline"
line "out: $o"; verdict "$o" newline

# ---- 12 descriptor-limit sweep, with the script descriptor located
line "== descriptor-limit sweep (bash -c 'ulimit -n N; exec bash probe_fd.sh --identity') =="
{ printf 'printf "FDSCAN: %%s\\n" "$(cd /proc/$$/fd && for f in *; do printf "%%s=%%s " "$f" "$(readlink "$f")"; done)" >&2\n'
  cat census.sh; } > probe_fd.sh
P_FD_SHA=$(sha256sum probe_fd.sh | cut -d' ' -f1)
line "probe_fd.sh sha256=$P_FD_SHA bytes=$(wc -c < probe_fd.sh) lines=$(wc -l < probe_fd.sh) (copy with one prepended FDSCAN line)"
for n in 1024 64 20 16 12 11 10 8; do
  out=$(cd "$S" && bash -c "ulimit -n $n; exec bash probe_fd.sh --identity" 2>&1)
  fdscan=$(printf '%s\n' "$out" | sed -n 's/^FDSCAN://p')
  idline=$(printf '%s\n' "$out" | grep '^TSUKUROI_CENSUS_IDENTITY:')
  scriptfd=$(printf '%s\n' "$fdscan" | tr ' ' '\n' | grep '=.*probe_fd\.sh$' | cut -d= -f1)
  line "--- ulimit -n $n: script fd=${scriptfd:-none}"
  line "    fdscan: $fdscan"
  line "    id: $idline"
  case "$idline" in
    *"sha256=$P_FD_SHA"*"verified=yes"*) line "    verdict: correct" ;;
    *"sha256=unverifiable"*"verified=no"*) line "    verdict: unverifiable" ;;
    *) line "    verdict: WRONG" ;;
  esac
done
line ""

# ---- 13 descriptor 255 pre-occupied
o=$(cd "$S" && bash -c 'exec 255</dev/null; exec bash census.sh --identity' 2>&1)
line "### parent occupies fd 255"; line "out: $o"; verdict "$o" fd255-occupied
o=$(cd "$S" && bash -c 'exec 255</dev/null; exec 254</dev/null; exec bash census.sh --identity' 2>&1)
line "### parent occupies fd 255 and 254"; line "out: $o"; verdict "$o" fd255-and-254
o=$(cd "$S" && bash -c 'exec 255<argfile 2>/dev/null; exec 10</dev/null; exec bash census.sh --identity' 2>&1)
line "### parent supplies fd 10 on /dev/null"; line "out: $o"; verdict "$o" fd10-devnull

# ---- 14 BASH_ENV variants
rm -rf be; mkdir -p be; cp census.sh be/census.sh
cp census.sh be/other.sh
printf 'exec 10</dev/null\n' > be/benv_null.sh
printf 'exec 10<"$R46_OTHER"\n' > be/benv_other.sh
o=$(cd "$S" && BASH_ENV="$S/be/benv_null.sh" bash "$S/be/census.sh" --identity 2>&1)
line "### BASH_ENV opens fd 10 on /dev/null"; line "out: $o"; verdict "$o" benv-null
o=$(cd "$S" && R46_OTHER="$S/be/other.sh" BASH_ENV="$S/be/benv_other.sh" bash "$S/be/census.sh" --identity 2>&1)
line "### BASH_ENV opens fd 10 on a different file at a different path"; line "out: $o"; verdict "$o" benv-otherpath

# ---- 15 the item's scenario: parent fd>=10 on a different file at the SAME path (rename before exec)
rm -rf fx1; mkdir -p fx1
cp census.sh fx1/P.sh
{ printf '# decoy head\n'; cat census.sh; printf '\n# decoy tail\n'; } > fx1/decoy.sh
line "before-exec fixture: P.sh sha256=$(sha256sum fx1/P.sh|cut -d' ' -f1) bytes=$(wc -c <fx1/P.sh); decoy.sh sha256=$(sha256sum fx1/decoy.sh|cut -d' ' -f1) bytes=$(wc -c <fx1/decoy.sh)"
out=$(P=$S/fx1/P.sh Q=$S/fx1/decoy.sh bash -c 'exec 10<"$P"; printf "pre-exec fd10=%s\n" "$(readlink /proc/$$/fd/10)"; mv -f -- "$Q" "$P"; printf "after-rename fd10=%s\n" "$(readlink /proc/$$/fd/10)"; exec bash "$P" --identity' 2>&1); rc=$?
line "### item scenario: parent fd10 on old inode, rename over path BEFORE exec"
line "rc: $rc"; line "out: $out"
case "$out" in
  *"sha256=$(sha256sum fx1/P.sh|cut -d' ' -f1)"*"verified=yes"*) line "verdict(item-before-exec): correct (line names the decoy inode, which is the file bash executes)" ;;
  *) line "verdict(item-before-exec): inspect" ;;
esac

# ---- 16 adversarial: fd>=10 on a decoy inode + BASH_ENV that relinks the path AFTER bash opened the script
rm -rf fx2; mkdir -p fx2
cp census.sh fx2/P.sh
{ printf 'printf "DECOY_EXECUTED\\n" >&2\n'; cat census.sh; printf '\n# decoy tail\n'; } > fx2/decoy.sh
cat > fx2/benv.sh <<'EOS'
exec 10<"$R46_Q"
trap '[ -n "$R46_ARMED" ] || { R46_ARMED=1; mv -f -- "$R46_Q" "$R46_P"; printf "FDLINKS:255=%s 10=%s\n" "$(readlink /proc/$$/fd/255)" "$(readlink /proc/$$/fd/10)" >&2; }' DEBUG
EOS
DEC_SHA=$(sha256sum fx2/decoy.sh | cut -d' ' -f1); DEC_B=$(wc -c < fx2/decoy.sh)
line "adversarial fixture: executed file P.sh sha256=$REAL_SHA bytes=$REAL_B; decoy sha256=$DEC_SHA bytes=$DEC_B"
out=$(R46_Q=$S/fx2/decoy.sh R46_P=$S/fx2/P.sh BASH_ENV=$S/fx2/benv.sh bash "$S/fx2/P.sh" --identity 2>&1); rc=$?
line "### adversarial BASH_ENV (fd 10 on decoy + DEBUG relink after open)"
line "rc: $rc"; line "out: $out"
if printf '%s' "$out" | grep -q 'DECOY_EXECUTED'; then
  line "verdict(adversarial): the decoy was executed (consistent)"
elif printf '%s' "$out" | grep -q "sha256=$DEC_SHA" && printf '%s' "$out" | grep -q 'verified=yes'; then
  line "verdict(adversarial): WRONG -- line reports the decoy's bytes ($DEC_SHA) with verified=yes, but the executed file was $REAL_SHA and DECOY_EXECUTED never printed"
else
  line "verdict(adversarial): inspect"
fi

# ---- 17 stdin and process substitution
o=$(cd "$S" && bash -s -- --identity < census.sh 2>&1); line "### stdin (bash -s -- --identity < census.sh)"
line "out: $o"; verdict "$o" stdin
o=$(cd "$S" && bash <(cat census.sh) --identity 2>&1); line "### process substitution (bash <(cat census.sh) --identity)"
line "out: $o"; verdict "$o" procsubst

# ---- 18 cli
o=$(cd "$S" && bash census.sh --identity --selftest 2>&1); rc=$?
line "### --identity with a second flag"; line "rc: $rc"; line "out(head2): $(printf '%s\n' "$o" | head -2 | tr '\n' '|')"

# ---- 19 writes check in identity mode
rm -rf wr; mkdir -p wr; cp census.sh wr/c.sh
before=$(ls -A wr | wc -l)
(cd "$S/wr" && bash c.sh --identity >/dev/null 2>&1)
after=$(ls -A wr | wc -l)
line "### identity mode writes nothing: entries before=$before after=$after"
line "== end =="
