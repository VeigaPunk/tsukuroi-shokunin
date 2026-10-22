# Mutant diffs (each against the pristine probe `b168b9b8…`)

### M01-drop-parity-check
sha256 4cdb2c344ee79b6f0e113615189d5746ba5a877bf8edb5573efc045d883cd9da

```diff
--- /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo/tools/probe-git-child-env-r31.py	2026-10-22 19:59:53.031856020 -0300
+++ /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/mutants/M01-drop-parity-check.py	2026-10-22 20:02:39.087446812 -0300
@@ -239,7 +239,7 @@
 
 def parity(a, b):
     diffs = []
-    for k in ('rc', 'stdout_sha256', 'git_execs'):
+    for k in ():
         if a.get(k) != b.get(k):
             diffs.append('%s %s differs from control %s' % (k, b.get(k), a.get(k)))
     return diffs
```

### M02-drop-stdout-comparison
sha256 d30901feb52ba7a60b3f50ee8662d93ed3c546b9593126e6dd4ccfcccc33d972

```diff
--- /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo/tools/probe-git-child-env-r31.py	2026-10-22 19:59:53.031856020 -0300
+++ /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/mutants/M02-drop-stdout-comparison.py	2026-10-22 20:02:39.132955527 -0300
@@ -239,7 +239,7 @@
 
 def parity(a, b):
     diffs = []
-    for k in ('rc', 'stdout_sha256', 'git_execs'):
+    for k in ('rc', 'git_execs'):
         if a.get(k) != b.get(k):
             diffs.append('%s %s differs from control %s' % (k, b.get(k), a.get(k)))
     return diffs
```

### M03-drop-git-exec-count
sha256 3ca8987ceb04bf2a7fef679e6968ea4a0b47be13bb6e8b027841fe3569e08e7f

```diff
--- /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo/tools/probe-git-child-env-r31.py	2026-10-22 19:59:53.031856020 -0300
+++ /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/mutants/M03-drop-git-exec-count.py	2026-10-22 20:02:39.186801899 -0300
@@ -239,7 +239,7 @@
 
 def parity(a, b):
     diffs = []
-    for k in ('rc', 'stdout_sha256', 'git_execs'):
+    for k in ('rc', 'stdout_sha256'):
         if a.get(k) != b.get(k):
             diffs.append('%s %s differs from control %s' % (k, b.get(k), a.get(k)))
     return diffs
```

### M04-skip-first-exec-exclusion
sha256 fbb00bb91f008a50a9577fb848b2db2249beb9a227e46e3d3f98570e74d27a69

```diff
--- /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo/tools/probe-git-child-env-r31.py	2026-10-22 19:59:53.031856020 -0300
+++ /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/mutants/M04-skip-first-exec-exclusion.py	2026-10-22 20:02:39.240551960 -0300
@@ -332,7 +332,7 @@
                          'LD_LIBRARY_PATH': inject, 'PYTHONPATH': inject}
                 r = one_run(root, f'{ch}-{i}', tree, tool, args, extra_env=extra)
                 res.update({'channel_rc': r['rc'], 'git_execs': r['git_execs']})
-                carried = [e for e in r['execs'][1:] if any(inject in x for x in e[3])]
+                carried = [e for e in r['execs'] if any(inject in x for x in e[3])]
                 if carried:
                     evidence.append('%d descendant execs carry the injection path' % len(carried))
                     res['sample'] = {'exec': carried[0][1], 'argv_head': carried[0][2][:4]}
```

### M05-injection-by-variable-name
sha256 f7d3f756ec8be79c42198cb9f7fc9e5a201eb0b8100a23a565dbd29c2430555a

```diff
--- /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo/tools/probe-git-child-env-r31.py	2026-10-22 19:59:53.031856020 -0300
+++ /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/mutants/M05-injection-by-variable-name.py	2026-10-22 20:02:39.291824212 -0300
@@ -332,7 +332,7 @@
                          'LD_LIBRARY_PATH': inject, 'PYTHONPATH': inject}
                 r = one_run(root, f'{ch}-{i}', tree, tool, args, extra_env=extra)
                 res.update({'channel_rc': r['rc'], 'git_execs': r['git_execs']})
-                carried = [e for e in r['execs'][1:] if any(inject in x for x in e[3])]
+                carried = [e for e in r['execs'][1:] if any(x.split('=', 1)[0] in ('LD_PRELOAD', 'LD_LIBRARY_PATH', 'PYTHONPATH') for x in e[3])]
                 if carried:
                     evidence.append('%d descendant execs carry the injection path' % len(carried))
                     res['sample'] = {'exec': carried[0][1], 'argv_head': carried[0][2][:4]}
```

### M06-no-LD_LIBRARY_PATH-in-injection
sha256 835c574ff8aa93dd3de572dd08a0483a1510ff4069c95e57c17a8754b17606c1

```diff
--- /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo/tools/probe-git-child-env-r31.py	2026-10-22 19:59:53.031856020 -0300
+++ /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/mutants/M06-no-LD_LIBRARY_PATH-in-injection.py	2026-10-22 20:02:39.350741480 -0300
@@ -329,7 +329,7 @@
                     res['sample'] = sample
             elif ch == 'loader-env':
                 extra = {'LD_PRELOAD': os.path.join(inject, 'libprobe-inject.so'),
-                         'LD_LIBRARY_PATH': inject, 'PYTHONPATH': inject}
+                         'PYTHONPATH': inject}
                 r = one_run(root, f'{ch}-{i}', tree, tool, args, extra_env=extra)
                 res.update({'channel_rc': r['rc'], 'git_execs': r['git_execs']})
                 carried = [e for e in r['execs'][1:] if any(inject in x for x in e[3])]
```

### M07-no-PYTHONPATH-in-injection
sha256 d927e8084d335240cad318a0475a028271dab7af82fa8fb4fd851df1c0977838

```diff
--- /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo/tools/probe-git-child-env-r31.py	2026-10-22 19:59:53.031856020 -0300
+++ /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/mutants/M07-no-PYTHONPATH-in-injection.py	2026-10-22 20:02:39.419899623 -0300
@@ -329,7 +329,7 @@
                     res['sample'] = sample
             elif ch == 'loader-env':
                 extra = {'LD_PRELOAD': os.path.join(inject, 'libprobe-inject.so'),
-                         'LD_LIBRARY_PATH': inject, 'PYTHONPATH': inject}
+                         'LD_LIBRARY_PATH': inject}
                 r = one_run(root, f'{ch}-{i}', tree, tool, args, extra_env=extra)
                 res.update({'channel_rc': r['rc'], 'git_execs': r['git_execs']})
                 carried = [e for e in r['execs'][1:] if any(inject in x for x in e[3])]
```

### M08-drop-control-B-determinism-check
sha256 238b5a67aa2e084ae65977a10ade1c3c5cc4708b8f116f74a041c75145f41d38

```diff
--- /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo/tools/probe-git-child-env-r31.py	2026-10-22 19:59:53.031856020 -0300
+++ /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/mutants/M08-drop-control-B-determinism-check.py	2026-10-22 20:02:39.486991797 -0300
@@ -297,8 +297,6 @@
         herr = None
         if ca['rc'] != 0:
             herr = 'control run failed rc %s: %s' % (ca['rc'], ca.get('stderr_tail', ''))
-        elif parity(ca, cb):
-            herr = 'control runs disagree: ' + '; '.join(parity(ca, cb))
         elif ca['git_execs'] < 1:
             herr = 'control run started no git child'
         if herr:
```

### M09-no-require-git-child
sha256 493614c4c41c9a28f3ed59a80e9f93752e9fb30802f4479d937905a21fb8423d

```diff
--- /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo/tools/probe-git-child-env-r31.py	2026-10-22 19:59:53.031856020 -0300
+++ /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/mutants/M09-no-require-git-child.py	2026-10-22 20:02:39.538546130 -0300
@@ -299,8 +299,6 @@
             herr = 'control run failed rc %s: %s' % (ca['rc'], ca.get('stderr_tail', ''))
         elif parity(ca, cb):
             herr = 'control runs disagree: ' + '; '.join(parity(ca, cb))
-        elif ca['git_execs'] < 1:
-            herr = 'control run started no git child'
         if herr:
             res = {'tool': tool, 'argv': args, 'harness_error': herr}
             errors.append(tool)
```

### M10-supplementary-drop-stdout-and-exec-count
sha256 79a3135f917df33da12a1a6265ac3af628014805ade063be80e122a2b03e6589

```diff
--- /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo/tools/probe-git-child-env-r31.py	2026-10-22 19:59:53.031856020 -0300
+++ /fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/mutants/M10-supplementary-drop-stdout-and-exec-count.py	2026-10-22 20:02:39.584511285 -0300
@@ -239,7 +239,7 @@
 
 def parity(a, b):
     diffs = []
-    for k in ('rc', 'stdout_sha256', 'git_execs'):
+    for k in ('rc',):
         if a.get(k) != b.get(k):
             diffs.append('%s %s differs from control %s' % (k, b.get(k), a.get(k)))
     return diffs
```
