"""Scan every video on the Joe Reis channel for caption mentions of Ramona.

Uses yt-dlp for caption fetch (youtube-transcript-api hit an IP block on
2026-09-03 and yt-dlp's caption-content endpoint has its own separate,
stricter rate limit -- pace this deliberately). Captions only, no video
download. Writes matches incrementally to appearances_found.jsonl so a
partial run is usable, logs every video to scan_log.txt.
"""

import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from podcast_clips.captions import get_transcript
from podcast_clips.turns import build_turns

ROOT = Path(__file__).parent.parent
LISTING = ROOT / "channel_listing_raw.txt"
OUT = ROOT / "appearances_found.jsonl"
LOG = ROOT / "scan_log.txt"
TMPDIR = ROOT / "raw_captions" / "_scan_tmp"


def fetch_vtt(video_id: str) -> Path | None:
    """Try manual (live-captioner) track first, fall back to plain ASR."""
    out_prefix = TMPDIR / video_id
    subprocess.run(
        [
            "yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs",
            "--sub-langs", "en.*", "--sub-format", "vtt",
            "-o", str(out_prefix), f"https://www.youtube.com/watch?v={video_id}",
        ],
        capture_output=True, text=True, timeout=60,
    )
    candidates = list(TMPDIR.glob(f"{video_id}.*.vtt"))
    return candidates[0] if candidates else None


def main():
    TMPDIR.mkdir(parents=True, exist_ok=True)
    video_ids, titles = [], {}
    for line in LISTING.read_text().splitlines():
        parts = line.split(" | ")
        if len(parts) >= 2 and re.match(r"^[\w-]{11}$", parts[0]):
            video_ids.append(parts[0])
            titles[parts[0]] = parts[1]

    print(f"scanning {len(video_ids)} videos via yt-dlp", flush=True)
    found = []
    with OUT.open("w") as out_f, LOG.open("w") as log_f:
        for i, vid in enumerate(video_ids):
            try:
                vtt = fetch_vtt(vid)
                if vtt is None:
                    log_f.write(f"{i+1}/{len(video_ids)} no-captions {vid}\n")
                    log_f.flush()
                    time.sleep(1.5)
                    continue
                transcript = get_transcript(vtt)
                vtt.unlink()
                full = " ".join(line for _, line in transcript)
                if "ramona" in full.lower():
                    turns = build_turns(transcript)
                    tags = sorted({t.speaker for t in turns})
                    rec = {"id": vid, "title": titles[vid], "speaker_tags": tags}
                    found.append(rec)
                    out_f.write(json.dumps(rec) + "\n")
                    out_f.flush()
                    log_f.write(f"{i+1}/{len(video_ids)} MATCH {vid} {titles[vid]}\n")
                else:
                    log_f.write(f"{i+1}/{len(video_ids)} no-match {vid}\n")
            except subprocess.TimeoutExpired:
                log_f.write(f"{i+1}/{len(video_ids)} TIMEOUT {vid}\n")
            except Exception as e:
                log_f.write(f"{i+1}/{len(video_ids)} ERROR {vid} {e}\n")
            log_f.flush()
            time.sleep(1.5)

    print(f"done. matches={len(found)}", flush=True)


if __name__ == "__main__":
    main()
