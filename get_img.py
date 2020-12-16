from selenium import webdriver
import func
import os
import shutil

for i in range(100):
    driver = webdriver.Chrome()
    driver.get("https://caselearn2.fju.edu.tw/cas/login?service=https%3A//elearn2.fju.edu.tw/course/184586/content&locale=zh_TW&ts=1608096105.607027#/")
    func.get_captcha(driver)
    guess = func.number()

    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    captcha = driver.find_element_by_id("captcha")

    username.send_keys("408040143")
    password.send_keys("sandy010419")
    captcha.send_keys(guess)

    driver.find_element_by_class_name("btn-submit").click()

    title = driver.title
    guess = guess+".png"
    if title == "天主教輔仁大學 - 登入 Tronclass":
        print("fail")
        os.rename("captcha.png", guess)
        shutil.move(guess, "./wrong")
    else:
        print("成功")
        os.rename("captcha.png", guess)
        shutil.move(guess, "./robot_got_img")
    driver.close()