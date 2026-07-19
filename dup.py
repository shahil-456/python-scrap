import json

with open("abs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

seen = set()
unique = []

for item in data:
    if item["url"] in seen:
        continue
    seen.add(item["url"])
    unique.append(item)

with open("abs.json", "w", encoding="utf-8") as f:
    json.dump(unique, f, indent=4, ensure_ascii=False)

print(f"Removed {len(data) - len(unique)} duplicates.")
print(f"Remaining {len(unique)} records.")