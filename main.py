from datetime import date, datetime
from time import time, localtime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_id2 = os.environ["USER_ID2"]
template_id = os.environ["TEMPLATE_ID"]

def get_today():
  week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
  year = localtime().tm_year
  month = localtime().tm_mon
  day = localtime().tm_mday
  today = datetime.date(datetime(year=year, month=month, day=day))
  week = week_list[today.isoweekday() % 7]
  return "{} {}".format(today, week)

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), math.floor(weather['low']), math.floor(weather['high'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_wordsdujitang():
  words = requests.get("http://api.tianapi.com/dujitang/index?key=de2db404877a219544ae3ab78dc4e8a5")
  if words.status_code != 200:
    return get_wordsdujitang()
  return words.json()['newslist'][0]['content']

def get_caihongpi():
  words = requests.get("http://api.tianapi.com/caihongpi/index?key=de2db404877a219544ae3ab78dc4e8a5")
  if words.status_code != 200:
    return get_caihongpi()
  return words.json()['newslist'][0]['content']

def get_qinghua():
  words = requests.get("http://api.tianapi.com/saylove/index?key=de2db404877a219544ae3ab78dc4e8a5")
  if words.status_code != 200:
    return get_qinghua()
  return words.json()['newslist'][0]['content']

def get_shunkouliu():
  words = requests.get("http://api.tianapi.com/skl/index?key=de2db404877a219544ae3ab78dc4e8a5")
  if words.status_code != 200:
    return get_shunkouliu()
  return words.json()['newslist'][0]['content']

def get_xiaohua():
  words = requests.get("http://api.tianapi.com/joke/index?key=de2db404877a219544ae3ab78dc4e8a5&num=4")
  if words.status_code != 200:
    return get_xiaohua()
  return words.json()['newslist'][0]['title'],words.json()['newslist'][0]['content'],words.json()['newslist'][1]['title'],words.json()['newslist'][1]['content'],words.json()['newslist'][2]['title'],words.json()['newslist'][2]['content'],words.json()['newslist'][3]['title'],words.json()['newslist'][3]['content']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature,low,high = get_weather()
title1,content1,title2,content2,title3,content3,title4,content4 = get_xiaohua()
data = {"date":{"value":get_today(), "color":get_random_color()},"city":{"value":city, "color":get_random_color()},"low":{"value":str(low)+"℃", "color":get_random_color()},"high":{"value":str(high)+"℃", "color":get_random_color()},"weather":{"value":wea, "color":get_random_color()},"temperature":{"value":temperature, "color":get_random_color()},"love_days":{"value":get_count(), "color":get_random_color()},"birthday":{"value":get_birthday(), "color":get_random_color()},"words":{"value":get_words(), "color":get_random_color()},"dujitang":{"value":get_wordsdujitang(), "color":get_random_color()},"caihongpi":{"value":get_caihongpi(), "color":get_random_color()},"qinghua":{"value":get_qinghua(), "color":get_random_color()},"shunkouliu":{"value":get_shunkouliu(), "color":get_random_color()},"title1":{"value":title1, "color":get_random_color()},"title2":{"value":title2, "color":get_random_color()},"title3":{"value":title3, "color":get_random_color()},"title4":{"value":title4, "color":get_random_color()},"content1":{"value":content1, "color":get_random_color()},"content2":{"value":content2, "color":get_random_color()},"content3":{"value":content3, "color":get_random_color()},"content4":{"value":content4, "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
res2 = wm.send_template(user_id2, template_id, data)
print(res)
print(res2)
