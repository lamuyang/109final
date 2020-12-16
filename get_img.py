from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import time
import numpy as np
import shutil
import os
import sys
from tensorflow.keras import models
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
# 取消彈出視窗
# options = Options()
# options.add_argument("--disable-notifications")
 # chrome = webdriver.Chrome('./chromedriver', chrome_options=options)

def get_captcha(driver):
    element = driver.find_elements_by_tag_name("img")
    img = element[1]
    img.screenshot("captcha.png")
    # driver.save_screenshot("screenshot.png")

for i in range(100):
    driver = webdriver.Chrome()
    # driver.set_window_size(0.1 ,0.05)
    # driver.maximize_window()
    driver.get("https://caselearn2.fju.edu.tw/cas/login?service=https%3A//elearn2.fju.edu.tw/course/184586/content&locale=zh_TW&ts=1608096105.607027#/")
    get_captcha(driver)

    img_rows = None
    img_cols = None
    digits_in_img = 4
    model = None
    np.set_printoptions(suppress=True, linewidth=150, precision=9, formatter={'float': '{: 0.9f}'.format})

    def split_digits_in_img(img_array):
        x_list = list()
        for i in range(digits_in_img):
            step = img_cols // digits_in_img
            x_list.append(img_array[:, i * step:(i + 1) * step] / 255)
        return x_list

    if os.path.isfile('cnn_model.h5'):
        model = models.load_model('cnn_model.h5')
    else:
        print('No trained model found.')
        exit(-1)

    img_filename = './captcha.png'
    img = load_img(img_filename, color_mode='grayscale')
    img_array = img_to_array(img)
    img_rows, img_cols, _ = img_array.shape
    x_list = split_digits_in_img(img_array)

    varification_code = list()
    for i in range(digits_in_img):
        confidences = model.predict(np.array([x_list[i]]), verbose=0)
        result_class = model.predict_classes(np.array([x_list[i]]), verbose=0)
        varification_code.append(result_class[0])
        # print('Digit {0}: Confidence=> {1}    Predict=> {2}'.format(i + 1, np.squeeze(confidences), np.squeeze(result_class)))
    # print('Predicted varification code:', varification_code)
    guass = ""
    for i in varification_code:
        guass = guass+str(i)

    print(guass)



    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    captcha = driver.find_element_by_id("captcha")

    username.send_keys("408040143")
    password.send_keys("sandy010419")
    captcha.send_keys(guass)

    driver.find_element_by_class_name("btn-submit").click()

    # title = driver.find_elements_by_tag_name("title")
    title = driver.title
    print(title)
    guass = guass+".png"
    if title == "天主教輔仁大學 - 登入 Tronclass":
        print("fail")
        os.rename("captcha.png",guass)
        shutil.move(guass, "./wrong")

    else:
        print("成功")
        os.rename("captcha.png",guass)
        shutil.move(guass, "./robot_got_img")

    driver.close() 
