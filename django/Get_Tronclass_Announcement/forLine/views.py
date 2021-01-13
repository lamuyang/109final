from typing import Text
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import pandas as pd
from django.views.generic import TemplateView
import os

name = ""
pwd = ""

def reg(request):
    if request.method == 'POST':
      global name,pwd
      name=request.POST.get('account')
      pwd=request.POST.get('YourPassword')    
    print(name,pwd,file=open('file.txt', 'w'))
    return render(request,'done.html')


 



from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    FlexSendMessage,
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
        "size": "xl",
        "margin": "md"
      },
      {
        "type": "text",
        "text": "(查詢需等待10-15秒)",
        "size": "xs",
        "color": "#aaaaaa",
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
                elif event.message.text == "開始查詢":
                  os.system("python3 -W ignore /Users/yangsicheng/Desktop/109final/main.py")
                  print("123")
                  line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text="查詢完成")
                  )
                elif event.message.text == "查詢結果":
                  global name,pwd
                  for i in range(10):
                    df = pd.read_csv('./anouce.csv')
                    # print(df)
                    TText = f"\n===============\n第1筆資料：\n課程名稱：{df.iloc[0,2]}\n公告標題：{df.iloc[0,1]}\n公告內文：{df.iloc[0,3]}\n===============\n第2筆資料：\n課程名稱：{df.iloc[1,2]}\n公告標題：{df.iloc[1,1]}\n公告內文：{df.iloc[1,3]}\n===============\n第3筆資料：\n課程名稱：{df.iloc[2,2]}\n公告標題：{df.iloc[2,1]}\n公告內文：{df.iloc[2,3]}\n===============\n第4筆資料：\n課程名稱：{df.iloc[3,2]}\n公告標題：{df.iloc[3,1]}\n公告內文：{df.iloc[3,3]}\n===============\n第5筆資料：\n課程名稱：{df.iloc[4,2]}\n公告標題：{df.iloc[4,1]}\n公告內文：{df.iloc[4,3]}\n===============\n第6筆資料：\n課程名稱：{df.iloc[5,2]}\n公告標題：{df.iloc[5,1]}\n公告內文：{df.iloc[5,3]}\n===============\n第7筆資料：\n課程名稱：{df.iloc[6,2]}\n公告標題：{df.iloc[6,1]}\n公告內文：{df.iloc[6,3]}\n===============\n第8筆資料：\n課程名稱：{df.iloc[7,2]}\n公告標題：{df.iloc[7,1]}\n公告內文：{df.iloc[7,3]}\n===============\n第9筆資料：\n課程名稱：{df.iloc[8,2]}\n公告標題：{df.iloc[8,1]}\n公告內文：{df.iloc[8,3]}\n===============\n第10筆資料：\n課程名稱：{df.iloc[9,2]}\n公告標題：{df.iloc[9,1]}\n公告內文：{df.iloc[9,3]}"
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                      event.reply_token,
                      TextSendMessage(text=TText)
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