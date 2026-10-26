#!/bin/bash
printf 'PLANE packages: PROBE id=%s euid=%s tsk_vars=%s home=%s tmpdir=%s cwd=%s nenv=%s sh=%s\n' \
  "$(id -u)" "$EUID" "$(env | grep -c '^TSUKUROI_' || true)" "${HOME:-unset}" "${TMPDIR:-unset}" "$PWD" "$(env | wc -l)" "$0"
