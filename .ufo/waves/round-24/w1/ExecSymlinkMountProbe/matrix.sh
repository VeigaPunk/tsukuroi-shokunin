BASE=/fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe/m
rm -rf "$BASE"; mkdir -p "$BASE"
run() {  # $1=name $2=target-kind(sym|plain) $3=low-kind(plain|mount) $4=up-work-kind(plain|tmpfs)
  local n=$1 tk=$2 lk=$3 uw=$4
  local d="$BASE/$n"; mkdir -p "$d"/{low,up,work,sysroot,tgt}
  ln -s sysroot "$d/new_root"
  local tgt="$d/tgt"
  [ "$tk" = sym ] && tgt="$d/new_root"
  if [ "$lk" = mount ]; then mount -t tmpfs tmpfs "$d/low"; else :; fi
  if [ "$uw" = tmpfs ]; then mkdir -p "$d/ram/upper" "$d/ram/work"; mount -t tmpfs tmpfs "$d/ram"; local up="$d/ram/upper" wk="$d/ram/work"; else local up="$d/up" wk="$d/work"; fi
  printf '%-28s target=%-5s low=%-5s up/w=%-6s -> ' "$n" "$tk" "$lk" "$uw"
  out=$(mount -t overlay overlay -o "lowerdir=$d/low,upperdir=$up,workdir=$wk" "$tgt" 2>&1); rc=$?
  printf 'exit=%d %s\n' "$rc" "$(echo "$out" | head -1)"
}
run a_sym_plain_plain sym plain plain
run b_plain_plain_plain plain plain plain
run c_sym_mount_plain sym mount plain
run d_sym_plain_tmpfs sym plain tmpfs
run e_sym_mount_tmpfs sym mount tmpfs
run f_plain_mount_plain plain mount plain
run g_plain_plain_tmpfs plain plain tmpfs
run h_plain_mount_tmpfs plain mount tmpfs
