from multiprocessing import Process

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, )

import Data_analy as data
from DataBase.DB_apps import DB

# import
DB = DB()

app = Flask(__name__)




CHANNEL_ACCESS_TOKEN="3iBqJ7ksu2x9V9UPKCwuF0ehKxDb179IPMnQfjmHEiXS8wfssR0KArebG4ejuCntaa8JWWk4IErucKC5tns1gqWag9ockxqjLtMffrVZzgwxwm7VDy7IYdTCq8Vj9nDlasp6TclYX0f5Bwe+YDVYkAdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET="2afd619d959438ef78d81efc81f4d354"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
GropeDict = {}
import queue

q = queue.Queue()

@app.route("/")
def hello_world():
    return "THIS IS LINE BOT"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# import web_api.weather
import requests

def get_today_Weather(**kwargs)->str:
    id="280010"
    url = f'http://weather.livedoor.com/forecast/webservice/json/v1?city={id}'
    api_data = requests.get(url).json()
    #print(api_data['title'])
    ## for weather in api_data['forecasts']:
    #     weather_date = weather['dateLabel']
    #     weather_forecasts = weather['telop']
    #     print(weather_date + ':' + weather_forecasts)
    weather=max_temp=min_temp=None
    try:
        weather=api_data["forecasts"][0]["telop"]
        max_temp=api_data["forecasts"][0]["temperature"]["max"]["celsius"]
        min_temp = api_data["forecasts"][0]["temperature"]["min"]["celsius"]
    except:
        pass
    finally:
        return weather,max_temp,min_temp

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # group か　個人かを判定
    isGroup = (event.source.type == "group")
    print(isGroup)
    print(event)
    user_id = event.source.user_id
    if isGroup:
        msg_t = str(event.message.text)
        GroupId = event.source.group_id

        global GropeDict
        try:
            GropeDict[GroupId] += [user_id]
            GropeDict[GroupId] = list(set(GropeDict[GroupId]))

        except:
            GropeDict[GroupId] = [user_id]

        # リクエストか
        if msg_t in ["リクエスト", "バルス"]:

            GroupId = event.source.group_id
            print(GroupId)
            # グループの各ユーザIDを取得
            #     users=line_bot_api.get_group_member_ids(GroupId)
            ##現在把握している（発言した）ユーザの趣向を出す。
            # print(type(users),users)
            userhobby = []
            ##DBに一人のユーザ趣向を問い合わせ
            for u in GropeDict[GroupId]:
                userhobby.append(DB.get_talk_his_table_from_userId(u))

            userhobby = list(set(userhobby))
            print("userhobby::", userhobby)
            userhobby = ",".join(userhobby)
            LineSender(line_bot_api).sendMessage(text=userhobby, user_id=GroupId)



    msg_t = str(event.message.text)
    #print(msg_t)
    # print(type(event))
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)

    # status = (profile.status_message)
    
    print(profile.display_name,msg_t)

    # msg = TextMessage(text=f"name::{profile.display_name}\n"
    # f"status_message::{status}")
    # weather,max_temp,min_temp=get_today_Weather()
    # msg=f"今日の天気は,{weather}\n" \
    #     f"最高気温は{max_temp}℃です。\n" \
    #     f"最低気温は{min_temp}℃です." \

    user=LineUser(userId=user_id)
    DB.set_new_user(user_id,user.name)
    words = data.analy(msg_t)
    DB.set_talk_history(user_id, text=words)
    msg = "DBに保存しました"
    # LineSender(line_bot_api).sendMessage(str(user),user)


    msg_t=TextMessage(text=msg)
    # msg2=TextMessage(text=str(user))
    # for r in range(10):
    line_bot_api.push_message(user_id, msg_t)
    # line_bot_api.push_message(user_id, msg2)
    # line_bot_api.push_message(user_id, msg_t)


def q_put(q, msg):
    q.put(msg)


def _args():
    app.run(debug=False, host='0.0.0.0', port=5000)


def start():
    s = Process(target=_args)
    s.start()
    return q




class LineUser:
    def __init__(self,reply=None,userId=None):
        '''line のユーザ情報クラス　ここではreplayからUserIdを取得することも
            できるし、そのままuserIdを入力できる。
            そこからLine APIを通して、名前と　ひとこと（status message）を取得する。
        '''

        #reply か　userIdどちらも情報がない場合,userIdはNone とする。
        if  (reply or userId):
            ##replyからuserIdを取得
            if reply:
                self.userId = reply.source.user_id
            else:
                self.userId=userId
            #replyから名前とひとことを取得
            profile = line_bot_api.get_profile(self.userId)
            self.status = (profile.status_message)
            self.name=profile.display_name
        else:
            self.userId=None
            self.name=None
            self.status=None

    def __eq__(self, other):
        if type(other)==LineUser:
            return self.userId == other.userId
        else:
            return self.userId== other

    def __str__(self):
        return f"userId::{self.userId}\n" \
               f"userName::{self.name}\n" \
               f"userStatus::{self.status}"


class LineSender:
    def __init__(self,lineins:LineBotApi):
        self.line_bot_api=lineins

    def sendMessage(self,text:str,user_id:LineUser):
        if isinstance(user_id,LineUser):
            user_id=user_id.userId
        msg=TextMessage(text=text)
        self.line_bot_api.push_message(to=user_id,messages=msg)


if __name__ == "__main__":
    q = start()

    # # app.run(debug=True, host='0.0.0.0', port=5000)
    # userId="U8c8b0e06213c94bc4c7f42cac57cf1a7"
    # user=LineUser(userId=userId)
    # sender=LineSender(line_bot_api)

    while 1:
    #     sender.sendMessage(text=str(user),user_id=user)
    #
    pass
