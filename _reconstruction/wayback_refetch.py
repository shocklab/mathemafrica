#!/usr/bin/env python3
"""Refetch archived Mathemafrica images from the Wayback Machine."""
import json, os, subprocess, sys, time

SP = "."  # paths were session-local; set before rerunning
R  = "/Users/jonathanshock/Cursor folders/Mathemafrica"
STATUS = SP + "/fetch_status.txt"

MAGIC = {b"\xff\xd8\xff": "jpg", b"\x89PNG": "png", b"GIF8": "gif",
         b"RIFF": "webp", b"%PDF": "pdf", b"BM": "bmp", b"II*\x00": "tif",
         b"MM\x00*": "tif", b"<svg": "svg", b"<?xm": "svg"}

def looks_like_media(b):
    return any(b.startswith(m) for m in MAGIC)

def main():
    jobs = json.load(open(SP + "/jobs.json"))
    open(STATUS, "w").write(f"STARTED {os.getpid()} jobs={len(jobs)}\n")
    log = open(SP + "/fetch.log", "w", buffering=1)
    ok = skip = fail = 0
    for i, j in enumerate(jobs, 1):
        dest = os.path.join(R, j["dest"])
        if os.path.exists(dest):
            skip += 1; continue
        url = f"https://web.archive.org/web/{j['ts']}id_/{j['url']}"
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        tmp = dest + ".part"
        rc = subprocess.run(["curl", "-sL", "-m", "120", "--retry", "3",
                             "--retry-delay", "10", "--retry-all-errors",
                             "-o", tmp, url], capture_output=True).returncode
        good = False
        if rc == 0 and os.path.exists(tmp) and os.path.getsize(tmp) > 200:
            with open(tmp, "rb") as fh:
                good = looks_like_media(fh.read(8))
        if good:
            os.replace(tmp, dest); ok += 1
            log.write(f"OK   {os.path.getsize(dest):>9} {j['dest']}\n")
        else:
            if os.path.exists(tmp): os.remove(tmp)
            fail += 1
            log.write(f"FAIL rc={rc} {j['dest']}  <- {url}\n")
        if i % 10 == 0:
            open(STATUS, "a").write(f"PROGRESS {i}/{len(jobs)} ok={ok} fail={fail}\n")
        time.sleep(1.5)
    log.write(f"\nok={ok} skipped={skip} failed={fail}\n")
    open(STATUS, "a").write(f"ENDED rc=0 ok={ok} skipped={skip} failed={fail}\n")

main()
