from selenium import webdriver
import func
from time import sleep
import gui
import pandas as pd
import csv

def login(driver, ac, pa):
    driver.find_element_by_id("username").clear()
    driver.find_element_by_id("password").clear()
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    username.send_keys(ac)
    password.send_keys(pa)

def capt(driver):
    func.get_captcha(driver)
    guess = func.number()
    driver.find_element_by_id("captcha").clear()
    captcha = driver.find_element_by_id("captcha")
    captcha.send_keys(guess)
    driver.find_element_by_class_name("btn-submit").click()

options = webdriver.ChromeOptions()
options.add_argument("--headless")
# driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
driver = webdriver.Chrome(chrome_options=options)
driver.get("https://caselearn2.fju.edu.tw/cas/login?service=https%3A//elearn2.fju.edu.tw/login%3Fnext%3D/user/index&locale=zh_TW&ts=1607908465.74927")

ac, pa = gui.start()
login(driver, ac, pa)
capt(driver)

title = driver.title
times = 0
while title == "天主教輔仁大學 - 登入 Tronclass":
    if times <= 2:
        login(driver, ac, pa)
        capt(driver)
    else:
        ac, pa = gui.start()
        login(driver, ac, pa)
        capt(driver)
    title = driver.title
    times += 1

driver.get("https://elearn2.fju.edu.tw/bulletin-list/")

sleep(5)

info_dic = {"title":[], "class":[], "content":[]}

title_class = driver.find_elements_by_css_selector("span[ng-bind='bulletin.title']")
for i in title_class:
    info_dic["title"].append(i.text)

class_name = driver.find_elements_by_css_selector("span[ng-bind='getCourseName(bulletin.course_id)']")
for i in class_name:
    info_dic["class"].append(i.text)

op = driver.find_elements_by_css_selector("div.bulletin-update-info")
for i in op:
    i.click()
contents = driver.find_elements_by_css_selector("div.content-review.ng-isolate-scope")
for content in contents:
    info_dic["content"].append(content.text)

driver.close()

check = gui.save_page(info_dic)
if check == True:
    anouce = pd.DataFrame(info_dic)
    anouce.to_csv("./anouce.csv")
    print("11")