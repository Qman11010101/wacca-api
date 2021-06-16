import json

from selenium import webdriver
from selenium.webdriver.common.by import By

# 定数
URL_WACCA = "https://wacca.marv.jp/music/"
browser = webdriver.Firefox(executable_path="./geckodriver.exe")

browser.get(URL_WACCA)
browser.find_element(By.XPATH, '//a[@class="genre" and text()="すべて"]').click()
browser.quit()
