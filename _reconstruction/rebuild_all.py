#!/usr/bin/env python3
"""Re-run every per-post reconstruction script.

Each script writes its figures straight into wp-content/uploads and asserts
the post's own arithmetic on the way, so this doubles as the regression test:
if a shared change in figstyle breaks a claim, the run stops here.
"""
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
scripts = sorted(glob.glob(os.path.join(HERE, "posts", "p*.py")))
failed = []
for s in scripts:
    r = subprocess.run([sys.executable, s], capture_output=True, text=True)
    tail = [l for l in r.stdout.splitlines() if "figures written" in l]
    if r.returncode:
        failed.append(os.path.basename(s))
        print(f"FAILED {os.path.basename(s)}")
        print(r.stdout[-800:], r.stderr[-800:])
    else:
        print(tail[0] if tail else f"  {os.path.basename(s)}: ok")
print(f"\n{len(scripts) - len(failed)}/{len(scripts)} scripts ok")
sys.exit(1 if failed else 0)
