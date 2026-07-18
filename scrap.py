from bs4 import BeautifulSoup
import requests
import os
import time
from playwright.sync_api import sync_playwright
import subprocess
import sys
import json
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://apps.arrs.org/",
}


cookies = {
        "_fbp": "fb.1.1784266287793.913685236107844828",
		"_ga": "GA1.1.1876688536.1784266660",
		"_ga_HSL9VJ48WH": "GS2.1.s1784266679$o1$g1$t1784266948$j60$l0$h0",
		"_ga_HWLMFBNLQN": "GS2.1.s1784266660$o1$g1$t1784266676$j56$l0$h0",
		"_ga_LTFCHBS130": "GS2.1.s1784277829$o2$g1$t1784278965$j45$l0$h0",
		"_gcl_au": "1.1.1487417827.1784266679.1343847666.1784266692.1784266692.1984379585.1784266692.1784266692",
		".refreshtoken": "388065CC9BBE3B3D9A18EC3E56033D767440EDED4265CC20B449D2DF9EDCE5E5DF64B577DEE74BA12B13174BC19CB2989AA72D598AECD9BABB62098207575A79842F98DC3714657E552A16DE6D005FDA11A2232992C0764987BDDD32137851E39DE6C27565E56EA92E767EFC3F8C1A36D88E783B",
		"AMP26": "42CF203C0587F6E12C6FAACFF939CB230B53258A3BA183B22A0CC10E252878AB49BD48EA6EA1BC5C190D3859FE44A793BB0711F77A059688EE1E8711784637EDB499A0CA09E2F5586C60FF28FE176FEA15E2EFE6A439CD121D7AE07CAE0CF705DDFD147F853CAB5D6697D421178BA577364B4C76",
		"bitmovin_analytics_uuid": "8fd06bac-37ea-4238-8b38-a31db5d56e9c",
		"CloudFront-Key-Pair-Id": "K3LFK811YWDLL2",
		"CloudFront-Policy": "eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly92aWRlby5hcnJzLm9yZy8qIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzg0Mjc5MzE4fX19XX0_",
		"CloudFront-Signature": "sL4tbMBMEqHUO4rhdALIQSbbWcb32i-VgvwF8HaA9-TAMnmqlJf2fAwU6slu1FZSGt5ISI4va5zRVjL5gn5tdWsXsIVcjkN6QQ2OyisM9MALUoVb996OPNOLI4xrbqVpjyXmVgZgCbYMNHX4fOLKHAtM24P9K2-n-a16aG5n4kovOVmWXgGAYFVU-xGoWI3DqI8zKhFDGF3NYxmzVdo0okdLhZX1~ViiW1DksyDVrSbKuJIll68idbBvg-PnC9wXH0d1rSmLiTqc4hdhBKbjGoVixmDaTbTOHSNf0gpq7E4UNjXRSBSlWQdO9yg6eupbA5BgvHeGKZeMgCrOy-0syg__",
		"Embed-Context": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXAiOiJlbWJlZC1jb250ZXh0IiwiYXVkIjoicGxheWJhY2stc2Vzc2lvbiIsInBhcnRuZXJJZCI6ImFycnMiLCJ2aWRlb0lkIjoiYXJycy0yMDI2LW9jbWJtIiwiaG9zdCI6InZpZGVvLmFycnMub3JnIiwibm9uY2UiOiI3MzZkM2FkYS05MmIzLTQyYmQtOWYwMC1lOWUyMmY0NjdhMGUiLCJpYXQiOjE3ODQyNzkwNzgsImV4cCI6MTc4NDI3OTM3OH0.iSta8TGrNVhDKIfCYbNITtCZAMjh-g2TQOCRHGzss4Y",
		"login": "AD769C1D41E2B8D5BF17474F7BDC78DEE54765457F6EEB6AB713F7BAAE3D60EAEDD651042914313FBAA0FC4A21D56E149F3BD2F2DC09DC3A20BD513A9D93E17ECAAE75A7BBB13FB5764C6450958483A65186D9A3E6B79E5FD460B61A815CC7D2ADAAB93B407EE2AA324E918182DBA846F79A2A194FED44942EB2832A6551181199481E81D94D3F62DF29F46A264271C096710289A5159487D6A15A4DC0C079592796BC0CBDEEB75DFF37CAFAB38BF347B810A3B510A9AE83F1FB5B70D10243152969491C30C2D0BBCEE7A4142A794A71C3FD19D8A5D8CAF112A9FB1891BFA84C187A6BF88785896EEF23BB47888A822378E202858DB4E226DA71F6CFB8D7A3A5BB0A4A7BE4298AD8BA0E839BA7F6CC7BC97552FAB65848B40868503C8D32EBCCCDF871475ED2BA87E7558FFB28DA85B7C5C14D2D747022F2A82F9FC6E0B08FED7C9EBAD8C66E1FB2637F588783AC32343BFA9051DB83A5CEFBE35B46CB01B8DD6B5D456C471CD69FBD73B62CBD71969AB531DB4A51C60622AE2447B81D5F670FCDE663764DA0BADFC0B8305A7C7DD8DAA90C0FB12625DC95A8F88EA6F724A2E944A41975C82B919C7F47A40C5C7142FC84083657424213BC0A3AB3AB71846A48B7C119A4DBB4EC15368D66E7ED41BB46"
}

session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://apps.arrs.org/",
})

session.cookies.update({
    "_fbp": "fb.1.1784266287793.913685236107844828",
		"_ga": "GA1.1.1876688536.1784266660",
		"_ga_HSL9VJ48WH": "GS2.1.s1784266679$o1$g1$t1784266948$j60$l0$h0",
		"_ga_HWLMFBNLQN": "GS2.1.s1784266660$o1$g1$t1784266676$j56$l0$h0",
		"_ga_LTFCHBS130": "GS2.1.s1784277829$o2$g1$t1784278965$j45$l0$h0",
		"_gcl_au": "1.1.1487417827.1784266679.1343847666.1784266692.1784266692.1984379585.1784266692.1784266692",
		".refreshtoken": "388065CC9BBE3B3D9A18EC3E56033D767440EDED4265CC20B449D2DF9EDCE5E5DF64B577DEE74BA12B13174BC19CB2989AA72D598AECD9BABB62098207575A79842F98DC3714657E552A16DE6D005FDA11A2232992C0764987BDDD32137851E39DE6C27565E56EA92E767EFC3F8C1A36D88E783B",
		"AMP26": "42CF203C0587F6E12C6FAACFF939CB230B53258A3BA183B22A0CC10E252878AB49BD48EA6EA1BC5C190D3859FE44A793BB0711F77A059688EE1E8711784637EDB499A0CA09E2F5586C60FF28FE176FEA15E2EFE6A439CD121D7AE07CAE0CF705DDFD147F853CAB5D6697D421178BA577364B4C76",
		"bitmovin_analytics_uuid": "8fd06bac-37ea-4238-8b38-a31db5d56e9c",
		"CloudFront-Key-Pair-Id": "K3LFK811YWDLL2",
		"CloudFront-Policy": "eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly92aWRlby5hcnJzLm9yZy8qIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzg0Mjc5MzE4fX19XX0_",
		"CloudFront-Signature": "sL4tbMBMEqHUO4rhdALIQSbbWcb32i-VgvwF8HaA9-TAMnmqlJf2fAwU6slu1FZSGt5ISI4va5zRVjL5gn5tdWsXsIVcjkN6QQ2OyisM9MALUoVb996OPNOLI4xrbqVpjyXmVgZgCbYMNHX4fOLKHAtM24P9K2-n-a16aG5n4kovOVmWXgGAYFVU-xGoWI3DqI8zKhFDGF3NYxmzVdo0okdLhZX1~ViiW1DksyDVrSbKuJIll68idbBvg-PnC9wXH0d1rSmLiTqc4hdhBKbjGoVixmDaTbTOHSNf0gpq7E4UNjXRSBSlWQdO9yg6eupbA5BgvHeGKZeMgCrOy-0syg__",
		"Embed-Context": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXAiOiJlbWJlZC1jb250ZXh0IiwiYXVkIjoicGxheWJhY2stc2Vzc2lvbiIsInBhcnRuZXJJZCI6ImFycnMiLCJ2aWRlb0lkIjoiYXJycy0yMDI2LW9jbWJtIiwiaG9zdCI6InZpZGVvLmFycnMub3JnIiwibm9uY2UiOiI3MzZkM2FkYS05MmIzLTQyYmQtOWYwMC1lOWUyMmY0NjdhMGUiLCJpYXQiOjE3ODQyNzkwNzgsImV4cCI6MTc4NDI3OTM3OH0.iSta8TGrNVhDKIfCYbNITtCZAMjh-g2TQOCRHGzss4Y",
		"login": "AD769C1D41E2B8D5BF17474F7BDC78DEE54765457F6EEB6AB713F7BAAE3D60EAEDD651042914313FBAA0FC4A21D56E149F3BD2F2DC09DC3A20BD513A9D93E17ECAAE75A7BBB13FB5764C6450958483A65186D9A3E6B79E5FD460B61A815CC7D2ADAAB93B407EE2AA324E918182DBA846F79A2A194FED44942EB2832A6551181199481E81D94D3F62DF29F46A264271C096710289A5159487D6A15A4DC0C079592796BC0CBDEEB75DFF37CAFAB38BF347B810A3B510A9AE83F1FB5B70D10243152969491C30C2D0BBCEE7A4142A794A71C3FD19D8A5D8CAF112A9FB1891BFA84C187A6BF88785896EEF23BB47888A822378E202858DB4E226DA71F6CFB8D7A3A5BB0A4A7BE4298AD8BA0E839BA7F6CC7BC97552FAB65848B40868503C8D32EBCCCDF871475ED2BA87E7558FFB28DA85B7C5C14D2D747022F2A82F9FC6E0B08FED7C9EBAD8C66E1FB2637F588783AC32343BFA9051DB83A5CEFBE35B46CB01B8DD6B5D456C471CD69FBD73B62CBD71969AB531DB4A51C60622AE2447B81D5F670FCDE663764DA0BADFC0B8305A7C7DD8DAA90C0FB12625DC95A8F88EA6F724A2E944A41975C82B919C7F47A40C5C7142FC84083657424213BC0A3AB3AB71846A48B7C119A4DBB4EC15368D66E7ED41BB46"
})



downloaded = False
browser = None

page = None

ts_urls = []

os.makedirs("videos", exist_ok=True)

count = 0


def download_video(url, name):
    global count

    folder = os.path.join("videos", name)
    os.makedirs(folder, exist_ok=True)

    if url.endswith(".m3u8"):
        base = url.replace("master.m3u8", "master_1080p_")

        for i in range(1, 1700):
            ts_url = f"{base}{i:05d}.ts"

            # if i > 2:
            #     browser.close()

            print("Downloading:", ts_url)
            time.sleep(0.8)
            response = page.request.get(ts_url)

            if response.ok:
                filename = os.path.join(folder, f"{count:05d}.ts")

                with open(filename, "wb") as f:
                    f.write(response.body())

                print("Saved:", filename)
                count += 1
            else:
                print("Failed:", response.status)
                if i > 25:
                    browser.close()
                    return

                break



def handle_request(request,name):
    print(request.url)
    # print(name)
    # return
    global count
    if "0001" in request.url:
        return
    if request.url.endswith(".ts") or request.url.endswith(".m3u8"):
        print("REQUEST:", request.url)
        download_video(request.url,name)
        # response = page.request.get('request.url')

        # if response.ok:
        #     ext = ".m3u8" if request.url.endswith(".m3u8") else ".ts"
        #     filename = f"videos/{count:05d}{ext}"

        #     with open(filename, "wb") as f:
        #         f.write(response.body())

        #     print("Saved:", filename)
        #     count += 1
        # else:
        #     print("Failed:", response.status)


def handle_response(response):
    if response.url.endswith(".ts"):
        if response.url not in ts_urls:
            ts_urls.append(response.url)

def download_and_merge(ts_urls, output="video.mp4"):
    os.makedirs("temp_ts", exist_ok=True)

    filelist = []

    for i, url in enumerate(ts_urls):
        filename = f"temp_ts/{i:05d}.ts"

        r = requests.get(url, stream=True)
        r.raise_for_status()

        with open(filename, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                f.write(chunk)

        filelist.append(filename)

    with open("temp_ts/list.txt", "w") as f:
        for file in filelist:
            f.write(f"file '{os.path.abspath(file)}'\n")

    subprocess.run([
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", "temp_ts/list.txt",
        "-c", "copy",
        output
    ], check=True)

    print("Saved:", output)


def start_browser(name1,video_url):
    global browser, page

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)

            context = browser.new_context(
                extra_http_headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    "Referer": "https://apps.arrs.org/",
                    "Accept": "*/*",
                }
            )

            cookie_list = []

            for name, value in cookies.items():
                cookie_list.append({
                    "name": str(name),
                    "value": str(value),
                    "domain": "apps.arrs.org",
                    "path": "/"
                })

            context.add_cookies(cookie_list)

            page = context.new_page()

            page.on("request", lambda request: handle_request(request, name1))
            # page.on("response", handle_response)

            page.goto(
                video_url,
                wait_until="commit",
                timeout=120000
            )

            page.wait_for_timeout(50000)  

            print("Reached here")

            page.wait_for_selector("#videowatch")

            frame = next(f for f in page.frames if "video.arrs.org" in f.url)

            if frame.locator("video").count() > 0:
                frame.locator("video").click(force=True)
            else:
                print("Video not found")

            for f in page.frames:
                print(f.url)


            # frame = page.frame_locator("#videowatch")

            # frame.locator("video").click()

            page.wait_for_timeout(30000000)

            # download_and_merge(ts_urls, "output.mp4")


    except Exception as e:
        print(e)




with open("urls.json", "r", encoding="utf-8") as f:
    urls = json.load(f)


urls = [item for item in urls if not item["saved"]]

random.shuffle(urls)

for item in urls:
    name = item["name"]
    url = item["url"]

    try:
        print("Starting:", name)
        start_browser(name, url)
        item["saved"] = True
        with open("urls.json", "w", encoding="utf-8") as f:
            json.dump(urls, f, indent=4, ensure_ascii=False)


    except Exception as e:
        print("Error:", name, e)

    time.sleep(4.5)


# start_browser('name2',"https://apps.arrs.org/vam26/ondemand/demand?functioncode=OCMBM")
