## Corrections after wave 2 — C2 remnants (draft, appended 2026-10-23)

This is an append-only correction block for `corpus/knowledge/coredump-count-unit-r34.md`; it is not applied to that note. The body and its existing corrections remain unchanged.

- **Correction to body line 11:** “Before this note, no lane entry said what one counted entry is” is withdrawn. `kill-oom-boundary-r33.md` and `journal-boot-plane.md:79-106` already described the census unit as entries by identifier. The round-34 note adds the sourced split of those entries into two summary wordings and handler-error records; it did not first state the unit. This restates the correction already appended at body line 77, which the body sentence still contradicts.
- **Correction to body line 15:** “One summary record per crash” is too broad. S186 does not establish exactly one record for every crash: the handler may return before building the summary, and journal submission may fail. Read the existing narrower correction at body line 72: at most one summary for a crash the handler processes to the relevant point; the wording split applies to the summary path, not every crash.
- **Correction to body line 59:** “mori's scope is quoted” is inaccurate. The sentence at body line 42 paraphrases and cites Mori's scoped catalog-ID record counts; it does not reproduce a direct quotation. Read: “Mori's scope is referenced, not changed.”
- **Replacement for the header `recheck:` procedure at body line 5:** the old default-JSON first-line pipeline cannot reproduce the split: default JSON can encode the oversized `MESSAGE` as `null`, and the pipeline does not select the summary `MESSAGE_ID` or count handler records separately. The following read-only checks supersede it. They select the summary identifier explicitly, compare default JSON against `--all`, count identifier entries without a `MESSAGE_ID`, and check coredump status through `coredumpctl list`.

  1. Count summary records and null-vs-printed `MESSAGE` using default JSON (without `--all`):

     ```sh
     timeout 60 bash -o pipefail -c "journalctl --boot=0 --priority=err --no-pager --output=json --output-fields=SYSLOG_IDENTIFIER,MESSAGE_ID,MESSAGE,PRIORITY SYSLOG_IDENTIFIER=systemd-coredump MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1 | jq -s '{summary_records:length, null_message:map(select(.MESSAGE == null))|length, printed_message:map(select(.MESSAGE != null))|length}'"
     ```

  2. Select the same `MESSAGE_ID` with `--all` and count the two summary wordings:

     ```sh
     timeout 60 bash -o pipefail -c "journalctl --boot=0 --priority=err --all --no-pager --output=json --output-fields=SYSLOG_IDENTIFIER,MESSAGE_ID,MESSAGE,PRIORITY SYSLOG_IDENTIFIER=systemd-coredump MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1 | jq -s '{summary_records:length, dumped_core:map(select((.MESSAGE // \"\" | split(\"\\n\")[0]) | contains(\"dumped core.\")))|length, no_core_written:map(select((.MESSAGE // \"\" | split(\"\\n\")[0]) | contains(\"terminated abnormally without generating a coredump.\")))|length, null_message:map(select(.MESSAGE == null))|length}'"
     ```

  3. Count all identifier entries and the records with no summary `MESSAGE_ID`:

     ```sh
     timeout 60 bash -o pipefail -c "journalctl --boot=0 --priority=err --all --no-pager --output=json --output-fields=SYSLOG_IDENTIFIER,MESSAGE_ID,MESSAGE,PRIORITY SYSLOG_IDENTIFIER=systemd-coredump | jq -s '{identifier_entries:length, summary_id:map(select(.MESSAGE_ID == \"fc2e22bc6ee647b6b90729ab34a250b1\"))|length, handler_no_message_id:map(select((.MESSAGE_ID // \"\") == \"\"))|length, other_message_id:map(select((.MESSAGE_ID // \"\") != \"\" and .MESSAGE_ID != \"fc2e22bc6ee647b6b90729ab34a250b1\"))|length}'"
     ```

  4. For stored-core status, `coredumpctl list`'s human-readable table exposes `COREFILE`; its v262 manual defines `-`, `none`, `present`, `journal`, `truncated`, `error`, and `missing`. For reliable counts use the same `list` command in JSON mode and group its `corefile` field, rather than splitting the formatted table on whitespace:

     ```sh
     timeout 60 bash -o pipefail -c "coredumpctl --quiet --no-pager --json=short list | jq -s 'if length == 1 and (.[0] | type) == \"array\" then .[0] else . end | {records:length, first_keys:(.[0] | keys), corefile_states:(map(.corefile // .COREFILE // \"MISSING\") | group_by(.) | map({state:.[0], count:length}))}'"
     ```

[obs] On 2026-10-23 the read-only host checks returned: default selected summary JSON, 1,689 records / 81 `MESSAGE=null` / 1,608 printed `MESSAGE` (exit 0, explicitly echoed); selected `MESSAGE_ID` with `--all`, 1,689 summaries / 306 “dumped core” / 1,383 “terminated abnormally without generating a coredump” / 0 null; all identifier entries with `--all`, 1,693 entries / 1,689 summary IDs / 4 without a `MESSAGE_ID` / 0 other IDs. The latter two calls returned normal output; their numeric rc was not echoed, so exit 0 is [inf], not a separately captured status. `coredumpctl --json=short list` returned 1,827 total / 1,776 `none` / 50 `missing` / 1 `present` / 0 other states (exit 0, explicitly echoed). The coredumpctl list covers all records it returned, not just the journal query's current boot; do not equate those totals. [inf] The four no-ID rows match the handler-error class described by S189 and the earlier capture; this current query counts absent IDs but does not inspect their message text.

  A plain table-column parse was also tried once: `coredumpctl --quiet --no-pager list | awk ...` returned 1,827 rows but zero for each tested state; those state counts are invalid and discarded. Use the JSON query above for automated counts, with the documented `COREFILE` column as the human-readable view.

- **v262 option/source check:** the downloaded `journalctl(1)` source documents `FIELD=VALUE` matching, `--boot`, `--priority`, JSON output, `--output-fields`, `--all`, and `--no-pager` at lines 44-45, 284-300, 414-425, 492-497, 585-593, 667-677, 765-770 and 825. The v262 `coredumpctl(1)` source documents `list` and its `COREFILE` table at lines 49-56 and 92-104, and includes the JSON/no-pager standard options at lines 175-179; the included JSON definition is `standard-options.xml:84-90`. Host `journalctl --version`, `coredumpctl --version` and `pacman -Q systemd` identify systemd `262-1` (`262-1-arch`).
