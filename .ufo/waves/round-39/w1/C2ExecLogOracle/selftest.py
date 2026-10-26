import importlib.util, os, shutil, sys, tempfile
spec=importlib.util.spec_from_file_location('oracle', os.path.join(os.path.dirname(os.path.abspath(__file__)),'oracle.py'))
o=importlib.util.module_from_spec(spec); spec.loader.exec_module(o)
CAP='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/pacman.log'
S=os.path.dirname(os.path.abspath(__file__))
T='[2026-01-01T00:00:00+0000] '
fx=[
 T+"[PACMAN] Running 'pacman -Syu'",            # window 1
 T+"[ALPM] running 'pre.hook'",                 # pre (outside)
 T+"[ALPM-SCRIPTLET] pre hook output",          # outside
 T+"[ALPM] transaction started",                # commit open
 T+"[ALPM] installed pkgA (1-1)",               # add
 T+"[ALPM] running 'inside.hook'",              # INSIDE -> violation
 T+"[ALPM-SCRIPTLET] inside output",            # inside
 T+"[ALPM] removed pkgX (0.9-1)",               # removed inside
 T+"[ALPM] upgraded pkgB (1-1 -> 2-1)",         # add
 T+"[ALPM] transaction completed",              # close
 T+"[ALPM] running 'post.hook'",                # post
 T+"[ALPM-SCRIPTLET] post output",              # outside
 T+"[PACMAN] Running 'pacman -Q'",              # window 2 (no transaction)
 T+"[PACMAN] Running 'pacman -R pkgY'",         # window 3
 T+"[ALPM] transaction started",                # commit open 2
 T+"[ALPM] removed pkgY (1-1)",                 # removed
 T+"[ALPM] transaction interrupted",            # close
 T+"[ALPM-SCRIPTLET] after interrupt",          # outside
]
p=os.path.join(S,'fixture.log'); open(p,'w').write('\n'.join(fx)+'\n')
r=o.parse(p); s=o.summary(r)
exp=dict(W_command_windows=3,T_transactions_started=2,R_hook_running_lines=3,R_in_commit=1,R_out_commit=2,
         S_scriptlet_lines=4,S_in_commit=1,S_out_commit=3,D_removed_lines=2,MIX_transactions_removed_and_added=[1])
bad=[]
for k,v in exp.items():
    if s[k]!=v: bad.append((k,s[k],v))
print('FIXTURE self-test', 'PASS' if not bad else 'FAIL '+str(bad))
print('  fixture:', {k:s[k] for k in ('W_command_windows','T_transactions_started','R_in_commit','R_out_commit','S_scriptlet_lines','S_in_commit','S_out_commit','D_removed_lines','MIX_transactions_removed_and_added')})
print('  closers:', s['tx_closed_by'])

base=o.parse(CAP); bs=o.summary(base)
def mutate(name, fn):
    d=os.path.join(S,'mut'); os.makedirs(d,exist_ok=True)
    q=os.path.join(d,name+'.log'); lines=open(CAP).read().splitlines(); lines=fn(lines)
    open(q,'w').write('\n'.join(lines)+'\n')
    return o.summary(o.parse(q))
def inject_running(lines):
    i=next(n for n,l in enumerate(lines) if l.endswith('[ALPM] transaction started'))
    return lines[:i+1]+['[2026-10-03T20:41:58+0000] [ALPM] running \'injected.hook\'']+lines[i+1:]
def flip_closer(lines):
    return [l.replace('transaction completed','transaction interrupted') if 'transaction completed' in l else l for l in lines]
def drop_window(lines):
    i=next(n for n,l in enumerate(lines) if '[PACMAN] Running ' in l)
    return lines[:i]+lines[i+1:]
def move_closer(lines):
    # remove the first 'transaction completed' -> the phase stays open, swallowing the rest
    i=next(n for n,l in enumerate(lines) if l.endswith('[ALPM] transaction completed'))
    return lines[:i]+lines[i+1:]
m1=mutate('injrun',inject_running); m2=mutate('flip',flip_closer)
m3=mutate('dropwin',drop_window); m4=mutate('unclosed',move_closer)
print('MUTANT inject-running-inside : R_in %d (base %d), S_in %d (base %d), R total %d (base %d)'%(m1['R_in_commit'],bs['R_in_commit'],m1['S_in_commit'],bs['S_in_commit'],m1['R_hook_running_lines'],bs['R_hook_running_lines']))
print('MUTANT flip-closers         : closers %s (base %s), S_out %d (base %d)'%(m1 and m2['tx_closed_by'],bs['tx_closed_by'],m2['S_out_commit'],bs['S_out_commit']))
print('MUTANT drop-one-window      : W %d (base %d), T %d (base %d)'%(m3['W_command_windows'],bs['W_command_windows'],m3['T_transactions_started'],bs['T_transactions_started']))
print('MUTANT drop-first-closer    : unclosed %d (base %d), R_in %d (base %d), S_in %d (base %d)'%(m4['unclosed_transactions'],bs['unclosed_transactions'],m4['R_in_commit'],bs['R_in_commit'],m4['S_in_commit'],bs['S_in_commit']))
ok = (m1['R_in_commit']==1 and m1['S_in_commit']==bs['S_in_commit'] and m2['tx_closed_by'].get('transaction interrupted')==60 and m3['W_command_windows']==85 and m4['R_in_commit']>0 and m4['nested_transaction_started']>0)
print('SENSITIVITY', 'PASS' if ok else 'FAIL')
