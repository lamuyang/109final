from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from django.views.generic import TemplateView


import numpy as np
from tensorflow.keras import models
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img

from selenium import webdriver
from time import sleep
import pandas as pd
import csv

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

def login(driver, ac, pa):
    driver.find_element_by_id("username").clear()
    driver.find_element_by_id("password").clear()
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    username.send_keys(ac)
    password.send_keys(pa)

def capt(driver):
    get_captcha(driver)
    guess = number()
    driver.find_element_by_id("captcha").clear()
    captcha = driver.find_element_by_id("captcha")
    captcha.send_keys(guess)
    driver.find_element_by_class_name("btn-submit").click()
name = ""
pwd = ""

def reg(request):
    if request.method == 'POST':
      global name,pwd
      name=request.POST.get('account')
      pwd=request.POST.get('YourPassword')
    print(name,pwd)
    return render(request,'done.html')


 



from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    FlexSendMessage
)
import random,string

def GenPassword(length):
  numOfNum = random.randint(1,length-1) 
  numOfLetter = length - numOfNum 
  #選中numOfNum個數字 
  slcNum = [random.choice(string.digits) for i in range(numOfNum)] 
  #選中numOfLetter個字母 
  slcLetter = [random.choice(string.ascii_letters) for i in range(numOfLetter)] 
  #打亂這個組合 
  slcChar = slcNum + slcLetter 
  random.shuffle(slcChar) 
  #生成密碼 
  genPwd = ''.join([i for i in slcChar]) 
  return genPwd 

























line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
            
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件

                if event.message.text == "查詢公告":
                    flex_message = FlexSendMessage(
                        alt_text='hello',
                        contents={
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "要開始查詢嗎？",
        "weight": "bold",
        "size": "xxl",
        "margin": "md"
      },
      {
        "type": "separator",
        "margin": "xxl"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "margin": "md",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "要",
              "text": "開始查詢"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "不用",
              "text": "沒事"
            },
            "position": "relative"
          }
        ]
      }
    ]
  },
  "styles": {
    "footer": {
      "separator": True
    }
  }
}
                    )
                    line_bot_api.reply_message(event.reply_token, flex_message)

                elif event.message.text == "沒事":
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text="那就好")
                    )
                elif event.message.text == "取得id":
                  id = GenPassword(4)
                  user_id = event.source.user_id
                  print(user_id)
                  line_bot_api.reply_message(  # 回復傳入的訊息文字
                      event.reply_token,
                      TextSendMessage(text=f"你的使用者ｉｄ是：{id}")
                      
                    )
                elif event.message.text == "開始查詢":
                  global name,pwd
                  ac,pa = name,pwd
                  login(driver, ac, pa)
                  capt(driver)

                  title = driver.title
                  times = 0
                  while title == "天主教輔仁大學 - 登入 Tronclass":
                      if times <= 2:
                          login(driver, ac, pa)
                          capt(driver)
                      else:
                          ac,pa = name,pwd
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
                  anouce = pd.DataFrame(info_dic)
                  anouce.to_csv("./anouce.csv")
                  print("11")



                  line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text="開始")
                  )
                else:
                  line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                  )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def get_Password(request):
  return render(request, 'login.html')

def done(request):
  return render(request,"done.html")