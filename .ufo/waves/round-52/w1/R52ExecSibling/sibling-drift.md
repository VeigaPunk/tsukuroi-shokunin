# OUT-row sibling pin drift receipt

Observed using `git -C <sibling> rev-parse HEAD`, `git -C <sibling> cat-file -e <pin>^{commit}`, and, for moved tips, `git -C <sibling> grep -F '<first eight words>' HEAD -- PROVINCE.md`. Every pin exists; every live HEAD has moved. Quote status is literal fixed-string grep against the indicated file at HEAD.

| OUT row | Sibling | Pinned commit | Pin exists? | Live HEAD | Moved? | Quote at live tip? |
|---|---|---|---|---|---|---|
| OUT-001 | mori | `91940fa339e38006f8db5bd7d78bb6f037f4d016` | yes | `7370a731abcafc4c803111de7c22cd6264d63be1` | yes | absent |
| OUT-002 | kama | `e75cf680b53484a61709ee1b2787d8dbc6419f74` | yes | `361c620c33edf8d19ec63b287250287f34f95484` | yes | absent |
| OUT-003 | kagi | `c2cab35bc92e57e39e5489bac3386db078345b3f` | yes | `c49023b773b69de983f0e6eb7e5867ceb5c2c634` | yes | present |
| OUT-004 | mado | `a4046a8216080d4004de3f268c62cf142095ac07` | yes | `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` | yes | absent |
| OUT-005 | mori | `91940fa339e38006f8db5bd7d78bb6f037f4d016` | yes | `7370a731abcafc4c803111de7c22cd6264d63be1` | yes | present |
| OUT-006 | kumitate | `1770305fae20826b39905a8251ddeca6b4957ac4` | yes | `14057f3e3899180c95713bace088fb9c0d0046e3` | yes | present |
| OUT-007 | mori | `91940fa339e38006f8db5bd7d78bb6f037f4d016` | yes | `7370a731abcafc4c803111de7c22cd6264d63be1` | yes | present |
| OUT-008 | kaidoku | `d1d981d2cc041dda4656c5b01d2c8445d8d17124` | yes | `39f41d4f15a87689a41c16c5c17ed885fbfb7da3` | yes | present |
| OUT-009 | revenger | `cf02419276e5dd8aafb6fe09d4e9aaa6bcb78c97` | yes | `abe4276bfb6efd37405c6845ea88c786267cd675` | yes | present |
| OUT-010 | tameshi | `01d586ddbc5fcd78659557c4e93a6ee8517b87d1` | yes | `2c51affd37e15cd7cd258d76ba0f5f73ff235924` | yes | present |

Raw command outputs are retained in `drift.tsv` alongside this report.
