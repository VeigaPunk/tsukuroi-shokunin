#!/usr/bin/env bash
# F-15 NotesPatchOffset-3: verify Round-42 packaging-offset note numbers against a
# faithful reconstruction of the Arch build tree (pin 54d9411 + PKGBUILD patch order).
set -u
S=/fast/scratch/hyaku/tsukuroi-r42/NotesPatchOffset
D=$(cut -d= -f2 "$S/fixture.path")
F39=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/src
F41=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-41/frozen/src
pass=0; fail=0
ok()  { pass=$((pass+1)); printf 'PASS %s\n' "$1"; }
bad() { fail=$((fail+1)); printf 'FAIL %s\n' "$1"; }

# eq <label> <pinned-file> <a-b> <built-file> <c-d>: text of pin[a-b] == built[c-d]
eq() {
  local label=$1 pin=$2 ar=$3 bui=$4 br=$5
  if diff -q <(sed -n "${ar}p" "$pin") <(sed -n "${br}p" "$bui") >/dev/null; then
    ok "$label: pin :$ar == built :$br"
  else
    bad "$label: pin :$ar != built :$br"
    diff <(sed -n "${ar}p" "$pin") <(sed -n "${br}p" "$bui") | head -6
  fi
}

echo "== 1. line counts (pin -> built)"
for f in "add.c:$F39/add.c:$D/lib/libalpm/add.c" "makepkg.sh.in:$F41/makepkg.sh.in:$D/scripts/makepkg.sh.in" "PKGBUILD.5.asciidoc:$F41/PKGBUILD.5.asciidoc:$D/doc/PKGBUILD.5.asciidoc" "util.c:$F39/util.c:$D/lib/libalpm/util.c"; do
  IFS=: read -r n p b <<<"$f"
  printf '%-20s pin=%s built=%s delta=%s\n' "$n" "$(wc -l <"$p")" "$(wc -l <"$b")" "$(( $(wc -l <"$b") - $(wc -l <"$p") ))"
done

echo "== 2. diff hunk headers (pin numbering, u=0)"
for f in "add.c:$F39/add.c:$D/lib/libalpm/add.c" "makepkg.sh.in:$F41/makepkg.sh.in:$D/scripts/makepkg.sh.in" "PKGBUILD.5.asciidoc:$F41/PKGBUILD.5.asciidoc:$D/doc/PKGBUILD.5.asciidoc" "util.c:$F39/util.c:$D/lib/libalpm/util.c"; do
  IFS=: read -r n p b <<<"$f"
  echo "-- $n"; diff -U0 "$p" "$b" | grep '^@@'
done

echo "== 3. add.c cited ranges (r39 note)"
A=$F39/add.c; AB=$D/lib/libalpm/add.c
eq add.c:168-189-still-168-189 "$A" 168,189 "$AB" 168,189
eq 'add.c:466-474->489-497'   "$A" 466,474 "$AB" 489,497
eq 'add.c:468-469->491-492'   "$A" 468,469 "$AB" 491,492
eq 'add.c:470-474->493-497'   "$A" 470,474 "$AB" 493,497
eq 'add.c:616-636->639-659'   "$A" 616,636 "$AB" 639,659
eq 'add.c:616-648->639-671'   "$A" 616,648 "$AB" 639,671
eq 'add.c:630->653' "$A" 630,630  "$AB" 653,653
eq 'add.c:638-647->661-670'   "$A" 638,647 "$AB" 661,670
eq 'add.c:639-640->662-663'   "$A" 639,640 "$AB" 662,663
eq 'add.c:669-688->692-711'   "$A" 669,688 "$AB" 692,711
eq 'add.c:676-692->699-715'   "$A" 676,692 "$AB" 699,715
eq add.c:412-417-hunk-context-unmoved "$A" 412,417 "$AB" 412,417
eq add.c:415-417-shifted-to-438-440   "$A" 415,417 "$AB" 438,440

echo "== 4. util.c cited ranges (r39 note)"
U=$F39/util.c; UB=$D/lib/libalpm/util.c
eq util.c:521-528-unshifted "$U" 521,528 "$UB" 521,528
eq util.c:665-666-unshifted "$U" 665,666 "$UB" 665,666
eq util.c:675-unshifted     "$U" 675,675 "$UB" 675,675
eq 'util.c:677-687->682-692' "$U" 677,687 "$UB" 682,692
eq 'util.c:688-698->693-703' "$U" 688,698 "$UB" 693,703
eq 'util.c:698-700->703-705' "$U" 698,700 "$UB" 703,705

echo "== 5. makepkg.sh.in cited ranges (r41 note)"
M=$F41/makepkg.sh.in; MB=$D/scripts/makepkg.sh.in
eq makepkg:192-unshifted   "$M" 192,192  "$MB" 192,192
eq makepkg:414-unshifted   "$M" 414,414  "$MB" 414,414
eq 'makepkg:560-569->678-687' "$M" 560,569 "$MB" 678,687
eq makepkg:565     '->683'     "$M" 565,565  "$MB" 683,683
eq 'makepkg:615-620->733-738' "$M" 615,620 "$MB" 733,738
echo "-- evidence.txt anchors in built makepkg"
sed -n '472p;537p;628,629p' "$MB"

echo "== 6. PKGBUILD.5.asciidoc cited ranges (r41 note)"
K=$F41/PKGBUILD.5.asciidoc; KB=$D/doc/PKGBUILD.5.asciidoc
eq pkgb5:51-56-unshifted  "$K" 51,56   "$KB" 51,56
eq pkgb5:67-74-unshifted  "$K" 67,74   "$KB" 67,74
eq 'pkgb5:345-377->354-386' "$K" 345,377 "$KB" 354,386
eq 'pkgb5:400-404->409-413' "$K" 400,404 "$KB" 409,413
eq 'pkgb5:439-441->448-450' "$K" 439,441 "$KB" 448,450

echo "== 7. first shifted pin line per file (boundary facts)"
firstshift() { # pin, built, label
  local p=$1 b=$2 n=$3 i=1
  while :; do
    if ! diff -q <(sed -n "${i}p" "$p") <(sed -n "${i}p" "$b") >/dev/null; then echo "$n: first differing prefix line = $i"; break; fi
    i=$((i+1))
  done
}
firstshift "$A" "$AB" add.c
firstshift "$U" "$UB" util.c
firstshift "$M" "$MB" makepkg.sh.in
firstshift "$K" "$KB" PKGBUILD.5.asciidoc

echo "== 8. summary: pass=$pass fail=$fail"
