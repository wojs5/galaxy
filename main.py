import os
import math
import json
import random
import requests
import datetime
import time
import hmac
import hashlib
import base64
import urllib.parse


# 获取天气和温度
# https://dev.qweather.com/ 和风天气开发服务
def get_weather():
    url = "https://devapi.qweather.com/v7/weather/now?key=" + weather_key + "&location=" + city
    res = requests.get(url).json()
    if(res['code']!='200'):
        return "天气数据请求错误",res['code']
    weather = res['now']
    return weather['text'], weather['temp']


# 每日一句
def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


# 字体随机颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


def send_msg(token_dd, msg, at_all=False):
    """
    通过钉钉机器人发送内容
    @param date_str:
    @param msg:
    @param at_all:
    @return:
    """
    timestamp,sign = dd_code()
    url = 'https://oapi.dingtalk.com/robot/send?access_token=' + token_dd + '&timestamp=' + timestamp + '&sign=' + sign
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    content_str = "早安！\n\n{0}\n".format(msg)

    data = {
        "msgtype": "text",
        "text": {
            "content": content_str
        },
        "at": {
            "isAtAll": at_all
        },
    }
    res = requests.post(url, data=json.dumps(data), headers=headers)
    print(res.text)

    return res.text

def dd_code():
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret_dd.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret_dd)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp,sign


if __name__ == '__main__':
    city = os.environ['CITY']
    token_dd = os.environ['TOKEN_DD']
    secret_dd = os.environ['SECRET_DD']
    weather_key = os.environ['WEATHER_KEY']
    #weather_key = ''
    #secret_dd = ''
    #city = "101210101"
    #token_dd = '你自己的webhook后面的access_token复制在此'
    wea, temperature = get_weather()

    note_str = "当前城市：{0}\n今日天气：{1}\n当前温度：{2}\n{3}".format("杭州", wea, temperature, get_words())

    send_msg(token_dd, note_str, True)
