from selenium import webdriver
import func

driver = webdriver.Chrome()
driver.get("https://caselearn2.fju.edu.tw/cas/login?service=https%3A//elearn2.fju.edu.tw/login%3Fnext%3D/user/index&locale=zh_TW&ts=1607908465.74927")

func.get_captcha(driver)
guess = func.number()

username = driver.find_element_by_id("username")
password = driver.find_element_by_id("password")
captcha = driver.find_element_by_id("captcha")

username.send_keys("408040143")
password.send_keys("sandy010419")
captcha.send_keys(guess)
driver.find_element_by_class_name("btn-submit").click()

driver.close()