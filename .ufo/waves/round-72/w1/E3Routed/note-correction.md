## Correction (round-72 C3; appended — the filed MP5 sentence is quoted, not edited)

R71-NOTE-MODPROBE-COUNT. The MP5 host-applicability paragraph above files the count as
"the three `/etc/modprobe.d` plus four `/usr/lib/modprobe.d` paths are recorded by path and
mode only". The superseded figure is **four**; the committed capture
`.ufo/waves/round-71/before/host.txt` lists **five** names under `/usr/lib/modprobe.d`:

- `/usr/lib/modprobe.d/README`
- `/usr/lib/modprobe.d/bluetooth-usb.conf`
- `/usr/lib/modprobe.d/gsr-nvidia.conf`
- `/usr/lib/modprobe.d/nvidia-utils.conf`
- `/usr/lib/modprobe.d/systemd.conf`

The three `/etc/modprobe.d` names are unchanged (`disable-usb-autosuspend.conf`,
`hid_apple.conf`, `nvidia.conf`), so the capture holds 3 + 5 = 8 modprobe.d paths, not 3 + 4.
The path-and-mode-only boundary and the blacklist conclusion of MP5 are unaffected; only the
figure and its enumeration are corrected here, by append, with the filed sentence left in place.
