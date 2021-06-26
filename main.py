import json

import requests
from bs4 import BeautifulSoup

# 定数
with open("pathSetting.json", encoding="utf-8_sig") as j:
    PATHJSON = json.load(j)
API_PATH = PATHJSON["export_path"] + "wacca_all.json"
API_KEYS = PATHJSON["api_keys"]
REQ_STR = """%7BrenderType%3A%22plainText%22%2CoutputAsJson%3Atrue%2CoverseerScript%3A%27await+page.goto%28%22https%3A%2F%2Fwacca.marv.jp%2Fmusic%2F%22%29%3Bpage.click%28%22a%5Bdata-s%3Dall%5D%22%29%3Bawait+page.waitForNavigation%28%29%3B%27%7D"""
for key in API_KEYS:
    r = requests.get(f"https://phantomjscloud.com/api/browser/v2/{key}/?request={REQ_STR}").json()
    try:
        source = r["pageResponses"][0]["frameData"]["content"]
    except:
        pass
    else:
        break
html = BeautifulSoup(source, "html.parser")
musics = [m for m in html.find_all("div", {"class": "song"})]
music_json = []
for m in musics:
    title = m.find_all("div", {"class": "data_name"})[0].get_text()
    artist = m.find_all("dd")[0].get_text()
    category = m.find_all("div", {"class": "data_cat"})[0].get_text()
    lvs = m.find_all("div", {"class": "level_value"})
    has_inf = True if len(lvs) == 4 else False
    has_mv = True if len(m.find_all("div", {"class": "data_movie"})) else False
    if (ctx := m.find_all("div", {"class": "song_copy"})[0].get_text()) != "":
        copy = ctx
    else:
        copy = None
    lv_nor = lvs[0].get_text().strip()
    lv_har = lvs[1].get_text().strip()
    lv_exp = lvs[2].get_text().strip()
    lv_inf = lvs[3].get_text().strip() if has_inf else None
    tempobj = {
        "meta": {
            "title": title,
            "artist": artist,
            "category": category,
            "has_inferno": has_inf,
            "has_movie": has_mv,
            "copyright": copy
        },
        "level": {
            "nor": lv_nor,
            "har": lv_har,
            "exp": lv_exp
        }
    }
    if has_inf:
        tempobj["level"]["inf"] = lv_inf
    music_json.append(tempobj)
with open(API_PATH, "w", encoding="utf-8_sig") as api:
    json.dump(music_json, api, ensure_ascii=False)
