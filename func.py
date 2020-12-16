import numpy as np
from tensorflow.keras import models
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img

digits_in_img = 4
img_rows = None
img_cols = None

def get_captcha(driver):
    element = driver.find_elements_by_tag_name("img")
    img = element[1]
    img.screenshot("captcha.png")

def split_digits_in_img(img_array, img_rows, img_cols):
    x_list = []
    for i in range(digits_in_img):
        step = img_cols // digits_in_img
        x_list.append(img_array[:, i * step:(i + 1) * step] / 255)
    return x_list

def number():
    np.set_printoptions(suppress=True, linewidth=150, precision=9, formatter={'float': '{: 0.9f}'.format})
    model = models.load_model('cnn_model.h5')
    img_filename = './captcha.png'
    img = load_img(img_filename, color_mode='grayscale')
    img_array = img_to_array(img)
    img_rows, img_cols, _ = img_array.shape
    x_list = split_digits_in_img(img_array, img_rows, img_cols)
    varification_code = []
    for i in range(digits_in_img):
        confidences = model.predict(np.array([x_list[i]]), verbose=0)
        result_class = model.predict_classes(np.array([x_list[i]]), verbose=0)
        varification_code.append(result_class[0])
        guess = ""
    for i in varification_code:
        guess = guess+str(i)
    return guess