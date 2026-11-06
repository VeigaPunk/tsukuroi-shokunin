#!/usr/bin/env python3
# Near-miss: literal rule 7 without its "swaps non-empty" antecedent.
exec(open(__file__.replace("n-nearmiss", "l-literal")).read().replace(
 'if len(f["swaps"]) > 0:\n    free', 'if True:\n    free'))
