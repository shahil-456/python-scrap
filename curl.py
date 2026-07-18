import subprocess

import subprocess

subprocess.run([
    "py", "-m", "yt_dlp",
    "--cookies", "cookies.txt",
    "--add-header", "Referer:https://video.arrs.org/player/embed?videoId=arrs-2026-ocmbm&partnerId=arrs&liveBadge=off&autoplay=1&muted=1",
    "--add-header", "User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "https://video.arrs.org/vod/published/trusted-b561e0e0154c9c3cbc8da2b9/normalized/master_720p.m3u8"
], check=True)