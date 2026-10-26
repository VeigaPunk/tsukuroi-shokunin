import re,subprocess,html,sys
rows={
"S201":("https://man.archlinux.org/man/alpm-hooks.5",["Hooks are run in alphabetical order of their file name, where the ordering ignores the suffix.","AbortOnFail (Optional, PreTransaction only)","Causes the transaction to be aborted if the hook exits"]),
"S202":("https://devblog.archlinux.page/2026/on-scripts-and-hooks/",["As hooks are read from the target system's filesystem, pre-transaction tasks are only available and run once the package is installed, that provides them.","A post-transaction task is only available and run as long as the package is installed, that provides it.","we are missing a documented ordering system for alpm-hooks(5) in the distribution to establish ranges of number prefixes for specific tasks"]),
"S209":("https://man.archlinux.org/man/alpm-install-scriptlet.5",["The shell functions are executed in the root (/) of the system, so all paths inside of it must be absolute.","Such files are located at the root of ALPM packages and are named .INSTALL.","No shebang is used in the script and the decision on which shell to use for running it is not based on a package's metadata"]),
"S212":("https://wiki.archlinuxcn.org/wiki/Pacman",["pacman可以在处理前后，运行/usr/share/libalpm/hooks/文件夹下的hooks","Hook文件必须以'.hook'为后缀。Pacman hooks不是交互式的。","如果'pacman'PostTransaction钩子可执行，执行这些钩子"]),
"S215":("https://man.archlinux.org/man/alpm-package.7",["Optionally, an alpm-install-scriptlet named .INSTALL may be present at the root of an ALPM based package.","All existing data files of a package are extracted to the root directory of a target system upon installation of the package.","it is best practice to never package files in directories that contain user data"]),
"S217":("https://man.archlinux.org/man/PKGBUILD.5",["Note that during an upgrade operation, none of the install or remove functions will be called.","The mandatory fields for a minimally functional PKGBUILD are pkgname, pkgver, pkgrel and arch.","An array of file names, without preceding slashes, that should be backed up if the package is removed or upgraded."]),
}
def norm(t):
    t=html.unescape(re.sub(r'<[^>]+>','',t)); t=t.replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"').replace('\u00a0',' ')
    return re.sub(r'\s+','',t)
for k,(u,qs) in rows.items():
    r=subprocess.run(["curl","-sSL","--max-time","40","-A","Mozilla/5.0",u],capture_output=True)
    t=r.stdout.decode('utf8','replace'); n=norm(t)
    print(k,u,"rc",r.returncode,"bytes",len(t))
    for q in qs: print("  ",("PRESENT" if norm(q) in n else "ABSENT"),q[:70])
