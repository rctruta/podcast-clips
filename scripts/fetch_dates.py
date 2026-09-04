"""Pull upload dates + titles for the L&L episode list via yt-dlp metadata only.

No caption/subtitle download here -- just --print fields from the player
response, which is a separate, lighter-weight request than subtitle content.
"""

import csv
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT = ROOT / "ll_episode_dates.csv"

VIDEO_IDS = [
    "TXNIkzYhPL4", "6sQhn90C3CA", "6DPtNstP-XE", "8Bj4Z0kgySQ", "ACOMAyOEFYU",
    "_1W0kA_XWLQ", "POJzaaMoS-U", "VXFx47EkmEY", "YcF_ggeg-K4", "NbnEVFAtx9o",
    "dJXSzcjGx20", "N_wH8GSByj0", "cqOgt0JZLQY", "aDfppkj9iVg", "It2bUYFUptM",
    "FRhaCRiMbAk", "X4B2rBFABIU", "kcctcQhlxOw", "OVT6ixYenVM",
]

rows = []
for i, vid in enumerate(VIDEO_IDS):
    try:
        r = subprocess.run(
            ["yt-dlp", "--skip-download", "--print",
             "%(upload_date)s|||%(title)s|||%(duration>%H:%M:%S)s",
             f"https://www.youtube.com/watch?v={vid}"],
            capture_output=True, text=True, timeout=30,
        )
        line = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
        parts = line.split("|||")
        if len(parts) == 3:
            upload_date, title, duration = parts
            rows.append({"id": vid, "upload_date": upload_date, "title": title, "duration": duration})
            print(f"{i+1}/{len(VIDEO_IDS)} {vid} {upload_date} {title[:50]}")
        else:
            print(f"{i+1}/{len(VIDEO_IDS)} {vid} PARSE_FAIL: {r.stdout!r} {r.stderr[-200:]!r}")
    except Exception as e:
        print(f"{i+1}/{len(VIDEO_IDS)} {vid} ERROR {e}")
    time.sleep(1.5)

with OUT.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["id", "upload_date", "title", "duration"])
    w.writeheader()
    w.writerows(rows)

print(f"\nwrote {len(rows)}/{len(VIDEO_IDS)} rows to {OUT}")
