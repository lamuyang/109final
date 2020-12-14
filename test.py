from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time

# 取消彈出視窗
# options = Options()
# options.add_argument("--disable-notifications")
# chrome = webdriver.Chrome('./chromedriver', chrome_options=options)

def get_captcha(driver):
    element = driver.find_elements_by_tag_name("img")
    img = element[1]
    img.screenshot("captcha.png")



driver = webdriver.Chrome()
driver.set_window_size(1024, 960)
# driver.maximize_window()
driver.get("https://caselearn2.fju.edu.tw/cas/login?service=https%3A//elearn2.fju.edu.tw/login%3Fnext%3D/user/index&locale=zh_TW&ts=1607908465.74927")
get_captcha(driver)

username = driver.find_element_by_id("username")
password = driver.find_element_by_id("password")
captcha = driver.find_element_by_id("captcha")

