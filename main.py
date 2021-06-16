import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# 定数
with open("pathSetting.json", encoding="utf-8_sig") as j:
    PATHJSON = json.load(j)
URL_WACCA = "https://wacca.marv.jp/music/"
API_PATH = PATHJSON["export_path"] + "wacca_all.json"

options = Options()
options.add_argument('--headless') # ヘッドレス
driver = webdriver.Firefox(options=options, executable_path="./geckodriver")

driver.get(URL_WACCA)

ms_count_check = 0
wait_time = 10

while ms_count_check < 100:
    driver.find_element(By.XPATH, '//a[@class="genre" and text()="すべて"]').click()
    time.sleep(wait_time)
    source = driver.page_source

    html = BeautifulSoup(source, "html.parser")
    musics = [m for m in html.find_all("div", {"class": "song"})]
    ms_count_check = len(musics)
    wait_time += 5

music_json = []
for m in musics:
    title = m.find_all("div", {"class": "data_name"})[0].get_text()
    artist = m.find_all("dd")[0].get_text()
    category = m.find_all("div", {"class": "data_cat"})[0].get_text()
    lvs = m.find_all("div", {"class": "level_value"})
    has_inf = True if len(lvs) == 4 else False
    lv_nor = lvs[0].get_text().strip()
    lv_har = lvs[1].get_text().strip()
    lv_exp = lvs[2].get_text().strip()
    lv_inf = lvs[3].get_text().strip() if has_inf else None
    tempobj = {
        "meta": {
            "title": title,
            "artist": artist,
            "category": category
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
