# Round 19 boot-writer gate

`tools/check-boot-writers.py` verifies that every `/boot/limine.conf` update
reported by the declared capture probes has one exact, evidenced writer
attribution, and that every registry event is backed by those probe outputs.
It reads committed blobs only; it does not inspect the host or perform writes.

## Invocation

```text
python3 tools/check-boot-writers.py --revision <hex> [--branch master]
  [--registry corpus/knowledge/boot-writers-r19.json]
  [--registry-from <hex>]
python3 tools/check-boot-writers.py --selftest
```

The target revision supplies the knowledge entry. The registry revision is
`--registry-from` when supplied, otherwise `--revision`; captures and
`corpus/SOURCES.md` are read from that same registry revision. Both revisions
must pass the shared landed-revision binding. Exit codes are 0 (pass), 1
(registry/evidence failure), and 2 (cannot evaluate, including capture digest
mismatch). `--help` prints argparse help.

The single JSON result is key-sorted and contains `status`, `revision`,
`branch`, `branch_tip`, `counts`, and sorted `findings`. Counts mean:

- `events_total`: distinct capture-line locations enumerated by the declared
  probe/pattern pairs, between each exact `$ <probe>` and its next `[rc=` line.
- `attributed_events`: enumerated locations with exactly one claim whose quote,
  writer signature, mechanism/source evidence, and writer/event publication
  checks all pass.
- `writer_classes`: published writers with at least one mechanism reference.
- `writers_with_events`: declared writer IDs used by at least one event.
- `unattributed`: enumerated lines lacking exactly one fully valid claim.

`--selftest` uses an isolated temporary Git fixture under the sandbox clone and
prints its case summary; it performs no network access and always cleans up.
