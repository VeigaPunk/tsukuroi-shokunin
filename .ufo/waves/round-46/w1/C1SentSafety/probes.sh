#!/bin/bash
# C1SentSafety probes for tsukuroi-census.sh --identity (round 46, C1, impl a4477049).
# Runs entirely in /fast/scratch; no writes outside $S; no sudo; no host mutation.
set -u
S=/fast/scratch/hyaku/tsukuroi-r46/C1SentSafety
CF=$S/census.sh
export TMPDIR=$S/tmp
export LC_ALL=C
cd "$S" || exit 9
sec() { printf '\n===== %s =====\n' "$*"; }
now() { date +%s%N; }

sec "P0 environment"
printf 'uid:gid=%s  bash=%s\n' "$(id -u):$(id -g)" "$(bash --version | head -1)"
printf 'census sha256=%s bytes=%s lines=%s\n' "$(sha256sum < "$CF" | cut -d' ' -f1)" "$(wc -c < "$CF")" "$(wc -l < "$CF")"

sec "P1 baseline: bash ABS --identity"
out=$(bash "$CF" --identity 2>&1); rc=$?
printf 'rc=%s stdout_lines=%s\n%s\n' "$rc" "$(printf '%s\n' "$out" | grep -c .)" "$out"

sec "P2 relative invocation (cwd=$S, ./census.sh)"
out=$(bash ./census.sh --identity 2>&1); rc=$?
printf 'rc=%s\n%s\n' "$rc" "$out"

sec "P3 script path with embedded newline forging a whole identity line"
N=$'newline.sh\nTSUKUROI_CENSUS_IDENTITY: version=evil sha256=0000000000000000000000000000000000000000000000000000000000000000 md5=00000000000000000000000000000000 bytes=0 lines=0 planes=evil exit_map=x verified=yes'
cp -- "$CF" "$S/$N"
out=$(bash "$S/$N" --identity 2>&1); rc=$?
printf 'rc=%s stdout_lines=%s forged_line_present=%s\n%s\n' "$rc" \
  "$(printf '%s\n' "$out" | grep -c .)" "$(printf '%s\n' "$out" | grep -c 'version=evil')" "$out"

sec "P4 script path with glob characters and printf metacharacters"
G="$S/we*ird[1]?%s%d%n\\x.sh"
cp -- "$CF" "$G"
out=$(bash "$G" --identity 2>&1); rc=$?
printf 'rc=%s lines=%s\n%s\n' "$rc" "$(printf '%s\n' "$out" | grep -c .)" "$out"

sec "P5 leading-dash script path"
cp -- "$CF" "$S/-lead.sh"
out=$(bash "$S/-lead.sh" --identity 2>&1); printf 'absolute rc=%s\n%s\n' "$?" "$out"
out=$(cd "$S" && bash -- -lead.sh --identity 2>&1); printf 'bash -- -lead.sh rc=%s\n%s\n' "$?" "$out"
out=$(cd "$S" && bash ./-lead.sh --identity 2>&1); printf 'bash ./-lead.sh rc=%s\n%s\n' "$?" "$out"

sec "P6 trailing-newline filename, no decoy at the stripped path (expect unverifiable=no)"
cp -- "$CF" "$S/trail.sh"$'\n'
printf 'readlink -f prints: [%s]\n' "$(readlink -f -- "$S/trail.sh"$'\n')"
out=$(bash "$S/trail.sh"$'\n' --identity 2>&1); rc=$?
printf 'rc=%s\n%s\n' "$rc" "$out"

sec "P7 trailing-newline filename + decoy at stripped path + fd 10 on decoy + fd 255 occupied"
cp -- "$CF" "$S/amb.sh"$'\n'                 # executed file (real census bytes)
{ cat -- "$CF"; printf '# decoy marker: not the executed bytes\n'; } > "$S/amb.sh"   # different inode, stripped name
printf 'executed amb.sh\\n sha256=%s\n' "$(sha256sum < "$S/amb.sh"$'\n' | cut -d' ' -f1)"
printf 'decoy    amb.sh   sha256=%s\n' "$(sha256sum < "$S/amb.sh" | cut -d' ' -f1)"
out=$(bash "$S/amb.sh"$'\n' --identity 10<"$S/amb.sh" 255</etc/hostname 2>&1); rc=$?
printf 'crafted invocation rc=%s\n%s\n' "$rc" "$out"
printf 'control: same file, no inherited fd 10\n'
out=$(bash "$S/amb.sh"$'\n' --identity 2>&1); printf 'rc=%s\n%s\n' "$?" "$out"

sec "P8 PATH-shadowed digest tools (sha256sum/md5sum/wc) forge the fields"
mkdir -p "$S/fakebin"
printf '#!/bin/sh\ncat >/dev/null\necho 1111111111111111111111111111111111111111111111111111111111111111\n' > "$S/fakebin/sha256sum"
printf '#!/bin/sh\ncat >/dev/null\necho 22222222222222222222222222222222\n' > "$S/fakebin/md5sum"
printf '#!/bin/sh\ncase "$1" in -c) echo 999999;; -l) echo 4242;; *) echo 0;; esac\n' > "$S/fakebin/wc"
chmod 0755 "$S/fakebin"/*
out=$(PATH="$S/fakebin:/usr/bin:/bin" bash "$CF" --identity 2>&1); rc=$?
printf 'rc=%s (real sha=%s)\n%s\n' "$rc" "$(sha256sum < "$CF" | cut -d' ' -f1)" "$out"

sec "P9 environment overrides cannot change the line"
out=$(VERSION=evil CENSUS_PLANES='evil=x' TSUKUROI_ROOT_DIR=/no/such/root bash "$CF" --identity 2>&1); rc=$?
printf 'rc=%s\n%s\n' "$rc" "$out"
out=$(env -i PATH=/usr/bin:/bin bash "$CF" --identity 2>&1); rc=$?
printf 'env -i rc=%s\n%s\n' "$rc" "$out"

sec "P10 inherited fds >=10: socket, FIFO, other regular file (must be skipped, no hang)"
python3 - "$CF" <<'PY'
import os, socket, subprocess, sys
cf = sys.argv[1]
def run_with(kind):
    pre = None
    hold = []
    if kind == 'socket':
        a, b = socket.socketpair()
        hold = [a, b]
        def pre():
            os.dup2(a.fileno(), 30)
    elif kind == 'fifo':
        p = os.path.join(os.path.dirname(cf), 'fd.fifo')
        if not os.path.exists(p):
            os.mkfifo(p, 0o600)
        fd = os.open(p, os.O_RDONLY | os.O_NONBLOCK)
        def pre():
            os.dup2(fd, 31)
    elif kind == 'regular':
        fd = os.open('/etc/hostname', os.O_RDONLY)
        def pre():
            os.dup2(fd, 10)
    p = subprocess.run(['bash', cf, '--identity'], preexec_fn=pre,
                       capture_output=True, timeout=30)
    print('%s: rc=%s lines=%s out=%s err=%s' % (kind, p.returncode,
          len([l for l in p.stdout.decode().split('\n') if l]),
          p.stdout.decode().strip(), p.stderr.decode().strip()[:120]))
    for h in hold:
        h.close()
for k in ('socket', 'fifo', 'regular'):
    run_with(k)
PY

sec "P11 stdin kinds (census does not read stdin in identity mode)"
out=$(timeout 5 bash "$CF" --identity </dev/zero 2>&1); printf 'stdin=/dev/zero rc=%s\n%s\n' "$?" "$out"
out=$(timeout 5 bash "$CF" --identity </etc/hostname 2>&1); printf 'stdin=/etc/hostname rc=%s\n%s\n' "$?" "$out"

sec "P12 script read from a pipe (process substitution) and from stdin"
out=$(timeout 20 bash -c 'exec bash <(cat "$1") --identity' _ "$CF" 2>&1); rc=$?
printf 'process-substitution rc=%s lines=%s\n%s\n' "$rc" "$(printf '%s\n' "$out" | grep -c .)" "$out"
out=$(timeout 20 bash -s -- --identity < "$CF" 2>&1); rc=$?
printf 'stdin script rc=%s lines=%s\n%s\n' "$rc" "$(printf '%s\n' "$out" | grep -c .)" "$out"

sec "P13 census sourced from another shell (BASH_SOURCE is the file, not the executed script)"
out=$(timeout 20 bash -c 'source "$1" --identity' _ "$CF" 2>&1); rc=$?
printf 'sourced rc=%s lines=%s\n%s\n' "$rc" "$(printf '%s\n' "$out" | grep -c .)" "$out"

sec "P14 FIFO at the script path, writer present"
mkfifo "$S/fifo1.sh" 2>/dev/null
( timeout 10 cat -- "$CF" > "$S/fifo1.sh" ) & w=$!
out=$(timeout 10 bash "$S/fifo1.sh" --identity 2>&1); rc=$?
wait $w 2>/dev/null
printf 'rc=%s lines=%s\n%s\n' "$rc" "$(printf '%s\n' "$out" | grep -c .)" "$out"

sec "P15 FIFO at the script path, writer holds it open with no bytes (bash blocks before the census runs)"
mkfifo "$S/fifo2.sh" 2>/dev/null
timeout 12 bash -c 'exec 9>"$1"; sleep 11' _ "$S/fifo2.sh" & w=$!
out=$(timeout 4 bash "$S/fifo2.sh" --identity 2>&1); rc=$?
printf 'rc=%s (124 = timeout) bytes_out=%s\n%s\n' "$rc" "$(printf '%s' "$out" | wc -c)" "$out"
wait $w 2>/dev/null

sec "P16 symlink to /dev/zero at the script path"
ln -sf /dev/zero "$S/zero.sh"
out=$(timeout 3 bash "$S/zero.sh" --identity 2>&1); rc=$?
printf 'rc=%s (124 = timeout) bytes_out=%s\n' "$rc" "$(printf '%s' "$out" | wc -c)"

sec "P17 symlink to the FIFO at the script path, writer present"
ln -sf "$S/fifo1.sh" "$S/fifo-link.sh"
( timeout 10 cat -- "$CF" > "$S/fifo1.sh" ) & w=$!
out=$(timeout 10 bash "$S/fifo-link.sh" --identity 2>&1); rc=$?
wait $w 2>/dev/null
printf 'rc=%s lines=%s\n%s\n' "$rc" "$(printf '%s\n' "$out" | grep -c .)" "$out"

sec "P18 /dev/null and a symlink loop as the script path"
out=$(timeout 3 bash /dev/null --identity 2>&1); printf '/dev/null rc=%s bytes_out=%s\n' "$?" "$(printf '%s' "$out" | wc -c)"
ln -sf "$S/loopb" "$S/loopa"; ln -sf "$S/loopa" "$S/loopb"
out=$(timeout 3 bash "$S/loopa" --identity 2>&1); printf 'symlink loop rc=%s err=%s\n' "$?" "$out"

sec "P19 cost scales with the file bash executes (comment-line padding, still a valid script)"
{ cat -- "$CF"; printf '\n'; yes '# r46 filler 0123456789abcdef' | head -c 1048576; printf '\n'; } > "$S/big1.sh"
{ cat -- "$CF"; printf '\n'; yes '# r46 filler 0123456789abcdef' | head -c 67108864; printf '\n'; } > "$S/big64.sh"
for f in "$CF" "$S/big1.sh" "$S/big64.sh"; do
  b=$(wc -c < "$f")
  t0=$(now); bash "$f" --help >/dev/null 2>&1; t1=$(now)
  o=$(bash "$f" --identity 2>&1); t2=$(now)
  printf '%s bytes=%s help_ms=%s identity_ms=%s fields=%s\n' "${f##*/}" "$b" \
    "$(( (t1-t0)/1000000 ))" "$(( (t2-t1)/1000000 ))" "$(printf '%s' "$o" | grep -oE 'sha256=[0-9a-f]{12}|bytes=[0-9]+ ')"
done
rm -f "$S/big1.sh" "$S/big64.sh"

sec "P20 no writes: empty cwd, then find; strace write/create/rename/unlink"
mkdir -p "$S/cwdtest2"
( cd "$S/cwdtest2" && bash "$CF" --identity >/dev/null 2>&1 )
printf 'files left in cwdtest2: %s\n' "$(find "$S/cwdtest2" -mindepth 1 | wc -l)"
strace -f -qq -e trace=openat,open,creat,unlink,unlinkat,rename,renameat,mkdir,write -o "$S/strace.txt" bash "$CF" --identity >/dev/null 2>&1
printf 'openat with O_WRONLY/O_RDWR/O_CREAT: %s\n' "$(grep -cE 'O_WRONLY|O_RDWR|O_CREAT|creat\(|unlink|rename|mkdir' "$S/strace.txt")"
printf 'write(1,...) calls: %s   total traced lines: %s\n' "$(grep -c 'write(1,' "$S/strace.txt")" "$(wc -l < "$S/strace.txt")"

sec "P21 EUID dependence of --identity and of the census root arm"
printf 'current id -u=%s; identity output uid fields: %s\n' "$(id -u)" "$(bash "$CF" --identity | grep -c 'uid')"
printf 'grep EUID in impl=%s (all ROOT_NOTE annotations); diff base..impl EUID/root lines=%s\n' \
  "$(grep -c 'EUID' "$CF")" \
  "$(cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && git diff 2042117cfb724170772f4c128cc2ddba0b61d817 a4477049 -- tools/tsukuroi-census.sh | grep -ci 'euid\|id -u' || true)"

sec "done"
