from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
import pytesseract
import cv2

# 取消彈出視窗
# options = Options()
# options.add_argument("--disable-notifications")
# chrome = webdriver.Chrome('./chromedriver', chrome_options=options)

def get_captcha(driver):
    element = driver.find_elements_by_tag_name("img")
    img = element[1]
    img.screenshot("captcha.png")
    # img = Image.open("captcha.png")
    # pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    # text = pytesseract.image_to_string(img, lang='eng')
    # print(type(text))
    # print(text+"?")
    img = cv2.imread("captcha.png", 0)
    img = cv2.medianBlur(img, 5)
    cv2.imshow("newimg", img)
    cv2.waitKey(0)
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    text = pytesseract.image_to_string(img, lang="eng")
    print(text)

driver = webdriver.Chrome()
driver.get("https://caselearn2.fju.edu.tw/cas/login?service=https%3A//elearn2.fju.edu.tw/login%3Fnext%3D/user/index&locale=zh_TW&ts=1607908465.74927")
get_captcha(driver)

username = driver.find_element_by_id("username")
password = driver.find_element_by_id("password")
captcha = driver.find_element_by_id("captcha")
