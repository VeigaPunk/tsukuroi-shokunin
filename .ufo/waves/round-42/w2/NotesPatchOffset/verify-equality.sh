#!/usr/bin/env bash
# F-15 corrected equality battery: pin-range -> built-range text identity.
set -u
S=/fast/scratch/hyaku/tsukuroi-r42/NotesPatchOffset
D=$(cut -d= -f2 "$S/fixture.path")
A=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/src/add.c
U=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/src/util.c
M=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-41/frozen/src/makepkg.sh.in
K=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-41/frozen/src/PKGBUILD.5.asciidoc
AB=$D/lib/libalpm/add.c; UB=$D/lib/libalpm/util.c; MB=$D/scripts/makepkg.sh.in; KB=$D/doc/PKGBUILD.5.asciidoc
pass=0; fail=0
# eq <label> <pinfile> <pinrange> <builtfile> <builtrange>
eq() {
  local label=$1 pf=$2 pr=$3 bf=$4 br=$5
  if diff -q <(sed -n "${pr}p" "$pf") <(sed -n "${br}p" "$bf") >/dev/null; then
    pass=$((pass+1)); printf 'PASS %-34s pin:%s == built:%s\n' "$label" "$pr" "$br"
  else
    fail=$((fail+1)); printf 'FAIL %-34s pin:%s != built:%s\n' "$label" "$pr" "$br"
  fi
}
echo "== add.c (r39 note; +23 after pin 414)"
eq add.c:466-474_to_489-497 "$A" 466,474 "$AB" 489,497
eq add.c:468-469_to_491-492 "$A" 468,469 "$AB" 491,492
eq add.c:470-474_to_493-497 "$A" 470,474 "$AB" 493,497
eq add.c:616-636_to_639-659 "$A" 616,636 "$AB" 639,659
eq add.c:616-648_to_639-671 "$A" 616,648 "$AB" 639,671
eq add.c:630_to_653         "$A" 630,630  "$AB" 653,653
eq add.c:638-647_to_661-670 "$A" 638,647 "$AB" 661,670
eq add.c:639-640_to_662-663 "$A" 639,640 "$AB" 662,663
eq add.c:669-688_to_692-711 "$A" 669,688 "$AB" 692,711
eq add.c:676-692_to_699-715 "$A" 676,692 "$AB" 699,715
echo "== util.c (r39 note; +5 after pin 675)"
eq util.c:677-687_to_682-692 "$U" 677,687 "$UB" 682,692
eq util.c:688-698_to_693-703 "$U" 688,698 "$UB" 693,703
eq util.c:698-700_to_703-705 "$U" 698,700 "$UB" 703,705
echo "== makepkg.sh.in (r41 note; +118 after pin 511)"
eq makepkg:560-569_to_678-687 "$M" 560,569 "$MB" 678,687
eq makepkg:565_to_683         "$M" 565,565  "$MB" 683,683
eq makepkg:615-620_to_733-738 "$M" 615,620 "$MB" 733,738
echo "== PKGBUILD.5.asciidoc (r41 note; +9 after pin 234)"
eq pkgb5:345-377_to_354-386 "$K" 345,377 "$KB" 354,386
eq pkgb5:400-404_to_409-413 "$K" 400,404 "$KB" 409,413
eq pkgb5:439-441_to_448-450 "$K" 439,441 "$KB" 448,450
echo "== spot: the mapped built text carries the cited statements"
sed -n '489,497p' "$AB" | head -9
echo "--"
sed -n '678,687p' "$MB"
echo "--"
sed -n '354,356p' "$KB"
echo "== summary: pass=$pass fail=$fail"
