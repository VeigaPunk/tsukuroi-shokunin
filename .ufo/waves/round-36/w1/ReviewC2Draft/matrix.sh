probe() { desc="$1"; shift; out=$("$@" 2>&1 >/dev/null); rc=$?; printf '%-42s rc=%-3s %s\n' "$desc" "$rc" "$(printf '%s' "$out" | head -1)"; }
F=-F; FLD=_TRANSPORT
probe "baseline -F _TRANSPORT"            journalctl $F $FLD
probe "-F --since"                        journalctl $F $FLD --since "1 hour ago"
probe "-F -S (short)"                     journalctl $F $FLD -S "1 hour ago"
probe "-F --until"                        journalctl $F $FLD --until "1 hour ago"
probe "-F -n 1"                           journalctl $F $FLD -n 1
probe "-F -b"                             journalctl $F $FLD -b
probe "-F -b -1"                          journalctl $F $FLD -b -1
probe "-F -k"                             journalctl $F $FLD -k
probe "-F -u systemd-journald"            journalctl $F $FLD -u systemd-journald
probe "-F -t kernel"                      journalctl $F $FLD -t kernel
probe "-F -p err"                         journalctl $F $FLD -p err
probe "-F -g pattern"                     journalctl $F $FLD -g xyzzy
probe "-F --facility"                     journalctl $F $FLD --facility 0
probe "-F --grep"                         journalctl $F $FLD --grep xyzzy
probe "-F --after-cursor"                 journalctl $F $FLD --after-cursor=s=deadbeef
probe "-F --cursor"                       journalctl $F $FLD --cursor=s=deadbeef
probe "-F --invocation"                   journalctl $F $FLD --invocation=deadbeef
probe "-F -D /var/log/journal"            journalctl $F $FLD -D /var/log/journal
probe "-F --file"                         journalctl $F $FLD --file /nonexistent
probe "-F --root"                         journalctl $F $FLD --root /
probe "-F --namespace"                    journalctl $F $FLD --namespace=x
probe "-F --system"                       journalctl $F $FLD --system
probe "-F --user"                         journalctl $F $FLD --user
probe "-F --user-unit"                    journalctl $F $FLD --user-unit=x
probe "-F --machine"                      journalctl $F $FLD -M x
probe "-F --image"                        journalctl $F $FLD --image=x
probe "-F --slice"                        journalctl $F $FLD --slice=x
probe "-F --no-pager (non-limiting)"      journalctl $F $FLD --no-pager
probe "-F -q (non-limiting)"              journalctl $F $FLD -q
probe "-F -o json (non-limiting)"         journalctl $F $FLD -o json
probe "-F --boot=0"                       journalctl $F $FLD --boot=0
echo "--- -N variants ---"
probe "-N baseline"                       journalctl -N
probe "-N --since"                        journalctl -N --since "1 hour ago"
probe "-N -n 1"                           journalctl -N -n 1
probe "-N -p err"                         journalctl -N -p err
probe "-N --fields=_TRANSPORT --since"    journalctl --fields=_TRANSPORT --since "1 hour ago"
