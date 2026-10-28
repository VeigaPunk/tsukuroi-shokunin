import subprocess,os,time,signal
S='/fast/scratch/hyaku/tsukuroi-r48/TRevCounterA'
p=subprocess.Popen(['python3',S+'/counter.py','--census',S+'/e6/longrun.sh','--work',S+'/e6work'],stdin=subprocess.DEVNULL)
time.sleep(8); os.path.exists(S+'/e6work') and None
p.send_signal(signal.SIGTERM); p.wait()
print('counter rc:',p.returncode,'work exists:',os.path.exists(S+'/e6work'),'contents:',os.listdir(S+'/e6work') if os.path.exists(S+'/e6work') else None)
