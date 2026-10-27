ROW GR3 VERDICT: holds
SECTION SHA256: 8fa626768b49a98186b5a03fbc348175e5ed73484648b6e68a4277c6907a2800

- Unit selects SIGINT and invokes foreground `btrfs scrub start -B`: `btrfs-scrub@.service:9-10` directly supports both clauses.
- Default control-group applies and sends signal to every remaining process: `systemd.kill.xml:68-70,101` supports service control-group behavior and default. `capture.txt:3` confirms effective host KillMode=control-group.
- SIGCONT follows the initial stop signal: `systemd.kill.xml:114-115` explicitly says systemd always sends SIGCONT right after configured signal.
- Final SIGKILL after TimeoutStopSec if processes remain, subject to SendSIGKILL: `systemd.kill.xml:91-98` supports the conditional repeated termination request and configured FinalKillSignal; `capture.txt:3` confirms host FinalKillSignal=9 and SendSIGKILL=yes.
- Host timeout is 5 seconds, sourced from system default drop-in rather than unit override: `capture.txt:3-5` gives TimeoutStopUSec=5s, DefaultTimeoutStopSec=5s, and drop-in owner none; `btrfs-scrub@.service:6-10` contains no TimeoutStopSec directive.
- SIGINT cancellation invokes scrub cancel ioctl: `scrub.c:412-423` identifies the SIGINT handler and its `BTRFS_IOC_SCRUB_CANCEL` ioctl. The statement does not claim the handler itself writes the record.
- Cancellation record timing remains unestablished and explicitly marked inference: `scrub.c:412-414` says the cancel operation makes the master process record progress before exiting, but does not establish completion within 5 seconds or behavior after SIGKILL; the row correctly limits its inference to a killed process potentially leaving the last-written record.
- Snapshot digests verified against the manifests: round-45 `systemd.kill.xml` SHA256 448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72; round-44 service SHA256 eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252; round-42 `scrub.c` SHA256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801; host capture SHA256 f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70. Hash command printed the expected GR3 section hash above.
- Limits context: the entry explicitly bounds GR3 to documented systemd behavior plus effective host values, not a trace of a real stop; the row likewise states no unit was started or stopped (`Limits` section; `capture.txt:2-5`).
