import os
import subprocess

base_dir = os.path.join(os.getcwd(), "videos")

for folder in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder)

    if not os.path.isdir(folder_path):
        continue

    ts_files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith(".ts")]
    )

    if not ts_files:
        continue

    list_file = os.path.join(folder_path, "files.txt")

    with open(list_file, "w", encoding="utf-8") as f:
        for ts in ts_files:
            f.write(f"file '{ts}'\n")

    output = os.path.join(folder_path, "output.mp4")

    subprocess.run([
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        output
    ], cwd=folder_path)

    os.remove(list_file)

print("Done.")