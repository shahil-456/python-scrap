import json

key_name = "2026 AHFTC Board Review OnDemand Presentations"
name = "test1-ha1aaa"



def save_video_if_not_found(key_name, name):
    with open("full.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for site in data["sites"]:
        if site["key_name"] == key_name:
            for video in site.get("videos", []):
                if video["name"] == name:
                    return

            site["videos"].append({
                "name": name,
                "saved": False
            })

            with open("full.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return




save_video_if_not_found(key_name,name)






# key_name = "2026 AHFTC Board Review OnDemand Presentations"
# name = "test1-ha"

# with open("full.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# found = False

# for site in data["sites"]:
#     if site["key_name"] == key_name:
#         for video in site.get("videos", []):
#             if video["name"] == name:
#                 found = True
#                 break

#         if not found:
#             site["videos"].append({
#                 "name": name,
#                 "saved": False
#             })
#             with open("full.json", "w", encoding="utf-8") as f:
#                 json.dump(data, f, indent=2, ensure_ascii=False)

#         break

# count = 0

# for site in data["sites"]:
#     if site["key_name"] == key_name:
#         count = len(site.get("videos", []))
#         break

# print(count)