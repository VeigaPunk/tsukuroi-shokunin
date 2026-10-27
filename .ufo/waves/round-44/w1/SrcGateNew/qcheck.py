import re,hashlib
base="/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/w1/SrcGateNew/fetched/"
def L(f,n):
    return open(base+f,encoding='utf-8',errors='replace').read().splitlines()[n-1]
# verify each gate quote string against the fetched file at the given line
checks=[('scrub.c',3081,'bool readonly, bool is_dev_replace)'),
 ('scrub.c',3147,'if (dev->scrub_ctx ||'),
 ('scrub.c',3153,'ret = -EINPROGRESS;'),
 ('scrub.c',3159,'dev->scrub_ctx = sctx;'),
 ('scrub.c',3222,'dev->scrub_ctx = NULL;'),
 ('scrub.c',3331,'sctx = dev->scrub_ctx;'),
 ('scrub.c',3336,'return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;'),
 ('scrub.c',1381,'if (bwlimit == 0)'),
 ('scrub.c',1382,'return;'),
 ('sysfs.c',74,'__INIT_KOBJ_ATTR(_name, 0644, _show, _store)'),
 ('sysfs.c',2028,'return sysfs_emit(buf, "%llu\\n", READ_ONCE(device->scrub_speed_max));'),
 ('sysfs.c',2040,'limit = memparse(buf, &endptr);'),
 ('sysfs.c',2042,'endptr = skip_spaces(endptr);'),
 ('sysfs.c',2043,'if (*endptr != 0)'),
 ('sysfs.c',2044,'return -EINVAL;'),
 ('sysfs.c',2113,'BTRFS_ATTR_PTR(devid, scrub_speed_max),'),
 ('btrfs-scrub@.timer',5,'OnCalendar=monthly'),
 ('btrfs-scrub@.timer',8,'Persistent=true'),
 ('btrfs-scrub@.timer',11,'WantedBy=timers.target'),
 ('btrfs-scrub@.service',9,'KillSignal=SIGINT'),
 ('btrfs-scrub@.service',10,'ExecStart=/usr/bin/btrfs scrub start -B %f'),
 ('PKGBUILD',100,'install -Dm644 btrfs-scrub@.service "${pkgdir}/usr/lib/systemd/system/btrfs-scrub@.service"'),
 ('PKGBUILD',101,'install -Dm644 btrfs-scrub@.timer "${pkgdir}/usr/lib/systemd/system/btrfs-scrub@.timer"'),
]
bad=0
for f,n,exp in checks:
    got=L(f,n)
    ok = got.strip()==exp
    if not ok: bad+=1
    print(('OK  ' if ok else 'FAIL'), f'{f}:{n}', '|', got.strip()[:90] if got else '<missing>')
print('mismatches',bad)
