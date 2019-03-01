from flask import Blueprint, jsonify, send_file, request
from settings import MONGO_DB, RET, MUSIC_PATH, IMAGE_PATH, CHATS_PATH
import os, time
from uuid import uuid4
from ai.baidu import audio2text, my_nlp

gsa = Blueprint('gsa',__name__)

@gsa.route('/get_image/<filename>')
def get_image(filename):
    file_path = os.path.join(IMAGE_PATH,filename)
    print('file_path',file_path)
    return send_file(file_path)


@gsa.route('/get_music/<filename>')
def get_music(filename):
    file_path = os.path.join(MUSIC_PATH,filename)
    print('file_path_music', file_path)
    return send_file(file_path)


@gsa.route('/get_chat/<filename>')
def get_chat(filename):
    file_path = os.path.join(CHATS_PATH,filename)
    print('filepath',file_path)
    return send_file(file_path)


@gsa.route('/uploader',methods=['POST'])
def uploader():
    audio = request.files.get("recorder")
    to_user = request.form.get('to_user')
    from_user = request.form.get('from_user')
    print('to_user',to_user,'from_user',from_user)
    path = os.path.join(CHATS_PATH,audio.filename)
    audio.save(path)
    os.system(f'ffmpeg -i {path} {path}.mp3')

    msg_dict = {
        'sender': from_user,
        'msg': f'{audio.filename}.mp3',
        'createtime': time.time()
    }
    ret0 = MONGO_DB.chats.find_one({'user_list': {'$all': [to_user, from_user]}})
    print('ret0',ret0['chat_list'])

    ret = MONGO_DB.chats.update_one({'user_list': {'$all': [to_user, from_user]}}, {'$push': {'chat_list': msg_dict}})
    ret1 = MONGO_DB.chats.find_one({'user_list': {'$all': [to_user, from_user]}})
    print('ret1',ret1['chat_list'])

    RET['code'] = 0
    RET['msg'] = '上传视频文件'
    RET['data'] = {'filename':f"{audio.filename}.mp3"}
    print(RET)

    return jsonify(RET)

@gsa.route('/toy_uploader',methods=['POST'])
def toy_uploader():
    audio = request.files.get("record")
    to_user = request.form.get('to_user')
    from_user = request.form.get('from_user')
    filename = f'{uuid4()}.wav'
    path = os.path.join(CHATS_PATH,filename)
    audio.save(path)

    msg_dict = {
        'sender':from_user,
        'msg':filename,
        'createtime':time.time()
    }

    MONGO_DB.chats.update_one({'user_list':{'$all':[to_user,from_user]}},{'$push':{'chat_list':msg_dict}})

    return jsonify({
         'code':0,
        'filename':filename
        })


@gsa.route('/ai_uploader',methods=['POST'])
def ai_uploader():
    audio = request.files.get("record")
    to_user = request.form.get('to_user')
    from_user = request.form.get('from_user')
    print('to_user',to_user,'from_user',from_user)
    filename = f'{uuid4()}.wav'
    path = os.path.join(CHATS_PATH,filename)
    audio.save(path)

    Q =audio2text(path)
    ret = my_nlp(Q,from_user)

    return jsonify(ret)