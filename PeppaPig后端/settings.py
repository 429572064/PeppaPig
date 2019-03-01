# 目录配置
import os

MUSIC_PATH = 'Music'
IMAGE_PATH = 'Image'
CHATS_PATH = 'Chats'

QRCODE_PATH = 'QRcode'

IP_ADDR = '192.168.13.172'

# 数据库配置
import pymongo
client = pymongo.MongoClient(host='127.0.0.1',port=27017)
MONGO_DB = client['PeppaPig']

from redis import Redis
REDIS_DB = Redis(host='127.0.0.1',port=6379,db=10 )

#Rest-API
RET = {
    'code':0,
    'msg':'',
    'data':{}
}

# 联图配置
LT_URL = "http://qr.liantu.com/api.php?text=%s"

# 百度AI配置
from aip import AipSpeech, AipNlp

APP_ID = '15483561'
API_KEY ='PGop0sbEIlUd7fjP6ZEI4G0k'
SECRET_KEY = 'BAsacHXVOgbh7c7Gncatx0XSObyicOdU'

NLP = AipNlp(APP_ID, API_KEY, SECRET_KEY)
SPEECH = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

VOICE = {
    'vol':5,
    'spd':4,
    'pit':6,
    'per':3
}

# 图灵配置
TULING_STR =   args = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": '%s'
            }
        },
        "userInfo": {
            "apiKey": "d44ab919f21a4877a03aa042a291cd0e",
            "userId": "%s"
        }
    }

TULING_URL = 'http://openapi.tuling123.com/openapi/api/v2'