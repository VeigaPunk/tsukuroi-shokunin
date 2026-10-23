#!/bin/bash
# Verbatim commands from C2-correction-block-draft.md (ScribeC2Remnants), each followed by rc echo.
set -u
echo '== boot equivalence: --boot=0 vs list-boots =='
timeout 30 journalctl --list-boots --no-pager -q | tail -2
timeout 30 journalctl --boot=0 --no-pager -q -n1 --output=json | jq -r '._BOOT_ID'
echo '== draft cmd 1 =='
timeout 120 bash -o pipefail -c "journalctl --boot=0 --priority=err --no-pager --output=json --output-fields=SYSLOG_IDENTIFIER,MESSAGE_ID,MESSAGE,PRIORITY SYSLOG_IDENTIFIER=systemd-coredump MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1 | jq -s '{summary_records:length, null_message:map(select(.MESSAGE == null))|length, printed_message:map(select(.MESSAGE != null))|length}'"
echo "rc1=$?"
echo '== draft cmd 2 =='
timeout 120 bash -o pipefail -c "journalctl --boot=0 --priority=err --all --no-pager --output=json --output-fields=SYSLOG_IDENTIFIER,MESSAGE_ID,MESSAGE,PRIORITY SYSLOG_IDENTIFIER=systemd-coredump MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1 | jq -s '{summary_records:length, dumped_core:map(select((.MESSAGE // \"\" | split(\"\\n\")[0]) | contains(\"dumped core.\")))|length, no_core_written:map(select((.MESSAGE // \"\" | split(\"\\n\")[0]) | contains(\"terminated abnormally without generating a coredump.\")))|length, null_message:map(select(.MESSAGE == null))|length}'"
echo "rc2=$?"
echo '== draft cmd 3 =='
timeout 120 bash -o pipefail -c "journalctl --boot=0 --priority=err --all --no-pager --output=json --output-fields=SYSLOG_IDENTIFIER,MESSAGE_ID,MESSAGE,PRIORITY SYSLOG_IDENTIFIER=systemd-coredump | jq -s '{identifier_entries:length, summary_id:map(select(.MESSAGE_ID == \"fc2e22bc6ee647b6b90729ab34a250b1\"))|length, handler_no_message_id:map(select((.MESSAGE_ID // \"\") == \"\"))|length, other_message_id:map(select((.MESSAGE_ID // \"\") != \"\" and .MESSAGE_ID != \"fc2e22bc6ee647b6b90729ab34a250b1\"))|length}'"
echo "rc3=$?"
echo '== draft cmd 4 =='
timeout 120 bash -o pipefail -c "coredumpctl --quiet --no-pager --json=short list | jq -s 'if length == 1 and (.[0] | type) == \"array\" then .[0] else . end | {records:length, first_keys:(.[0] | keys), corefile_states:(map(.corefile // .COREFILE // \"MISSING\") | group_by(.) | map({state:.[0], count:length}))}'"
echo "rc4=$?"
echo '== coredumpctl json=short raw shape (first 400 bytes) =='
timeout 60 coredumpctl --quiet --no-pager --json=short list 2>/dev/null | head -c 400; echo
echo '== keys of one journalctl json record with --output-fields =='
timeout 60 journalctl --boot=0 --no-pager -q -n1 --output=json --output-fields=SYSLOG_IDENTIFIER,MESSAGE_ID,MESSAGE,PRIORITY SYSLOG_IDENTIFIER=systemd-coredump | jq -c 'keys'
