import json, os, shutil, socket, subprocess, sys, stat
spec = json.load(sys.stdin)
def sh(*a):
    subprocess.run(list(a), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
sh('mount', '-t', 'tmpfs', '-o', 'mode=755', 'r44lib', '/mnt')
os.mkdir('/mnt/home'); os.chmod('/mnt/home', 0o1777)
ROOTS = ['/sys/fs/btrfs', '/var/lib', '/etc/systemd/system']
for d in ROOTS:
    sh('mount', '-t', 'tmpfs', '-o', 'mode=755', 'r44view', d)
# plant fixtures exactly like materialize(): live fsid devinfo + scrub_speed_max, record file
import uuid as uuidmod
fid = '1d02a454-c549-4a35-b567-89d60902af8e'
os.makedirs('/sys/fs/btrfs/'+fid+'/devinfo/1', exist_ok=True)
open('/sys/fs/btrfs/'+fid+'/devinfo/1/scrub_speed_max','w').write('0\n')
os.makedirs('/var/lib/btrfs', exist_ok=True)
open('/var/lib/btrfs/scrub.status.'+fid,'w').write('scrub status:1\n')
os.chmod('/var/lib/btrfs/scrub.status.'+fid, 0o644)
os.makedirs('/etc/systemd/system/timers.target.wants', exist_ok=True)
os.symlink('/usr/lib/systemd/system/btrfs-scrub@.timer', '/etc/systemd/system/timers.target.wants/btrfs-scrub@home.timer')
env = spec['env']
pre = ['setpriv', '--reuid=%d' % spec['uid'], '--regid=%d' % spec['gid'], '--clear-groups']
def dump(tag, cmd):
    p = subprocess.run(pre + ['bash', '-c', cmd], env=env, capture_output=True, text=True, timeout=60, cwd='/mnt/home')
    return p.stdout
print('=== NS-STATE (python, ns-root) ===')
print('uid_map:', open('/proc/self/uid_map').read().strip().replace('\n',' | '))
print('gid_map:', open('/proc/self/gid_map').read().strip().replace('\n',' | '))
out = subprocess.run(['bash','-c','grep -E "r44lib|r44view" /proc/self/mountinfo; echo ---; stat -f -c "%n %T" /sys/fs/btrfs /var/lib /etc/systemd/system /mnt; echo ---; readlink /proc/self/ns/user /proc/self/ns/mnt; echo ---; ps -o cmd= -p $PPID'], capture_output=True, text=True)
print(out.stdout)
print('=== CENSUS-PROC (after setpriv reuid=1000 regid=1000 clear-groups) ===')
print(dump('id', 'id -u; id -g; id -G'))
print('status:', dump('ok', "grep -E '^(Uid|Gid|Groups):' /proc/self/status"))
print('pwd:', dump('pwd', 'pwd; printf "HOME=%s PWD=%s SHLVL=%s _=%s\\n" "$HOME" "$PWD" "$SHLVL" "$_"; echo; echo "argv0=$0"; echo "BASH_SOURCE0=${BASH_SOURCE[0]}"'))
print('stdin:', dump('stdin', 'if read -t 0.2 x; then echo "stdin: data=$x"; else echo "stdin: EOF-or-empty"; fi'))
print('owner:', dump('owner', 'stat -c "%n uid=%u gid=%g mode=%a" /var/lib/btrfs/scrub.status.'+fid+' /sys/fs/btrfs/'+fid+'/devinfo/1/scrub_speed_max; ls -l /var/lib/btrfs | head -3'))
print('nslinks:', dump('ns', 'readlink /proc/self/ns/user /proc/self/ns/mnt'))
print('parent:', dump('par', 'ps -o cmd= -p $PPID | head -c 200'))
print('mountcnt:', dump('mc', 'grep -c "" /proc/self/mountinfo'))
