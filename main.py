from selenium import webdriver
import func
from time import sleep

driver = webdriver.Chrome()
driver.get("https://caselearn2.fju.edu.tw/cas/login?service=https%3A//elearn2.fju.edu.tw/login%3Fnext%3D/user/index&locale=zh_TW&ts=1607908465.74927")

func.get_captcha(driver)
guess = func.number()

username = driver.find_element_by_id("username")
password = driver.find_element_by_id("password")
captcha = driver.find_element_by_id("captcha")

username.send_keys("")
password.send_keys("")
captcha.send_keys(guess)
driver.find_element_by_class_name("btn-submit").click()

driver.get("https://elearn2.fju.edu.tw/bulletin-list/")

sleep(5)

info_dic = {"title":[], "class":[], "content":[]}

title_class = driver.find_elements_by_css_selector("span.ng-binding")
title_class.insert(23, "")
for i in range(3,47):
    if title_class[i] == "" or title_class[i].text == "":
        continue
    if i % 4 == 3:
        # print("標題：",title_class[i].text)
        info_dic["title"].append(title_class[i].text)
    elif i % 4 == 0:
        # print("課程：",title_class[i].text)
        info_dic["class"].append(title_class[i].text)

op = driver.find_elements_by_css_selector("div.bulletin-update-info")
for i in op:
    i.click()

contents = driver.find_elements_by_css_selector("div.content-review.ng-isolate-scope")
for content in contents:
    # print("內文"：content.text)
    info_dic["content"].append(content.text)

print(info_dic)
driver.close()