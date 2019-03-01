from flask import Blueprint, jsonify, send_file, request
from settings import MONGO_DB, RET, MUSIC_PATH, IMAGE_PATH, CHATS_PATH
from redismsg import get_redis_one, get_redis_all

chat = Blueprint('chat',__name__)

@chat.route('/recv_msg',methods=['POST'])
def recv_msg():
    to_user = request.form.get('to_user')
    from_user = request.form.get('from_user')
    print('to_user',to_user,'from_user',from_user)
    count = get_redis_one(to_user,from_user)
    print('count',count)
    chat_window = MONGO_DB.chats.find_one({'user_list':{'$all':[to_user,from_user]}})

    chat_list = []

    for chat in reversed(chat_window.get('chat_list')):
        if chat.get('sender') != from_user:
            continue
        chat_list.append(chat)
        if len(chat_list) == count:
            break
    chat_list.reverse()
    print('chat_list',chat_list)
    return jsonify(chat_list)

@chat.route('/chat_list',methods=['POST'])
def chat_list():
    to_user = request.form.get('to_user')
    from_user = request.form.get('from_user')
    chat_window = MONGO_DB.chats.find_one({'user_list': {'$all': [to_user, from_user]}})
    print('chat_window',chat_window,to_user,from_user)

    RET['code'] = 0
    RET['msg'] = '查询聊天内容'
    RET['data'] = chat_window.get('chat_list')[-10:]

    return jsonify(RET)


@chat.route('/chat_count',methods=['POST'])
def chat_count():
    user_id = request.form.get('user_id')
    to_user_msg = get_redis_all(user_id)

    RET['code'] = 0
    RET['msg'] = '查询未读消息'
    RET['data'] = to_user_msg

    print('chat_count',RET)

    return jsonify(RET)


