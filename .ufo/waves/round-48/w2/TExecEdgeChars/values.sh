# name|value ; values are read with IFS='|'
S=/fast/scratch/hyaku/tsukuroi-r48/TExecEdgeChars
vals=(
  "e1tab|$S/e1tab"$'\t'"x"
  "e2nl|$S/e2nl"$'\n'"x"
  "e3sq|$S/e3sq'uote"
  "e4dq|$S/e4dq\"uote"
  "e5dollar|$S/e5\$HOME"
  "e6btick|$S/e6\`bt"
  "e7star|$S/e7st*ar"
  "e8dash|$S/e8/-x"
  "e9eq|$S/e9eq=1"
  "e10slash|$S/e10slash/"
  "e11link|$S/e11link"
  "e12rel|e12 rel dir"
  "e13long|$S/e13$(printf 'a%.0s' $(seq 200))"
  "e14uni|$S/e14üñí"
  "e15relclean|e13relclean"
)
