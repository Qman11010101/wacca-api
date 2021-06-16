from selenium import webdriver
import json

# 定数
URL_WACCA = "https://wacca.marv.jp/music/"
browser = webdriver.Firefox()

browser.get(URL_WACCA)
