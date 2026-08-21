import os
import json
import requests

os.makedirs("assets", exist_ok=True)

for json_file in ["1.json", "2.json", "3.json", "4.json"]:
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        url = item.get("asset")

        if not url:
            continue

        ext = os.path.splitext(url.split("?")[0])[1] or ".png"
        filename = f"{os.path.basename(json_file).split('.')[0]}_{data.index(item) + 1}{ext}"
        path = os.path.join("assets", filename)

        response = requests.get(url)
        response.raise_for_status()

        with open(path, "wb") as f:
            f.write(response.content)

        item["asset"] = path.replace("\\", "/")

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)