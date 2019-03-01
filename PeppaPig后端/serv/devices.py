from flask import Blueprint, jsonify, request
from settings import MONGO_DB, RET
from bson import ObjectId

devices = Blueprint('devices',__name__)

@devices.route('/validate_code',methods =['POST'] )
def validate_code():
    code = request.form.to_dict()
    res = MONGO_DB.devices.find_one(code,{'_id':0})
    if res:
        RET['code'] = 0
        RET['msg'] = '设备已授权,开启绑定'
        RET['data'] = res
    else:
        RET['code'] = 2
        RET['msg'] = '非授权设备'
        RET['data'] = {}

    return jsonify(RET)


@devices.route('/bind_toy',methods=['POST'])
def bind_toy():
    toy_info = request.form.to_dict()

    chat_window = MONGO_DB.chats.insert_one({'user_list':[],'chat_list':[]})

    user_info = MONGO_DB.users.find_one({'_id':ObjectId(toy_info['user_id'])})

    toy_info['bind_user'] = toy_info.pop('user_id')
    toy_info['avatar'] = 'toy.jpg'
    toy_info['friend_list'] = [
        {
            'friend_id':toy_info['bind_user'],
            'friend_name':user_info['nickname'],
            'friend_nick':toy_info.pop('remark'),
            'friend_avatar':user_info['avatar'],
            'friend_type':'app',
            'friend_chat':str(chat_window.inserted_id)
        }
    ]

    toy = MONGO_DB.toys.insert_one(toy_info)

    user_info['bind_toy'].append(str(toy.inserted_id))
    user_add_toy = {
        'friend_id':str(toy.inserted_id),
        'friend_name':toy_info.get('toy_name'),
        'friend_nick':toy_info.get('baby_name'),
        'friend_avatar':toy_info.get('avatar'),
        'friend_type':'toy',
        'friend':str(chat_window.inserted_id)
    }

    user_info['friend_list'].append(user_add_toy)

    MONGO_DB.users.update_one({'_id':user_info['_id']},{'$set':user_info})
    MONGO_DB.chats.update_one({'_id':chat_window.inserted_id},{'$set':{'user_list':[str(toy.inserted_id),str(user_info.get('_id'))]}})

    RET['code'] = 0
    RET['msg'] = '绑定玩具成功'
    RET['data'] = {}

    return jsonify(RET)


@devices.route('/toy_list',methods=['POST'])
def toy_list():
    user_id = request.form.get('_id')
    print('123',user_id)
    user_info = MONGO_DB.users.find_one({'_id':ObjectId(user_id)})
    print('456',user_info)
    user_bind_toy = user_info['bind_toy']

    for index, item in enumerate(user_bind_toy):
        user_bind_toy[index] = ObjectId(item)

    toy_list = list(MONGO_DB.toys.find({'_id':{"$in":user_bind_toy}}))

    for index, toy in enumerate(toy_list):
        toy_list[index]['_id'] = str(toy.get("_id"))

    RET['code'] = 0
    RET['msg'] = '查看所有绑定玩具'
    RET['data'] = toy_list

    return jsonify(RET)


@devices.route('/device_login',methods=['POST'])
def device_login():
    dev_info = request.form.to_dict()
    dev = MONGO_DB.devices.find_one(dev_info)
    if dev:
        toy = MONGO_DB.toys.find_one(dev_info)
        if toy:
            return jsonify({'music':'welcome.mp3','info':str(toy.get('_id'))})
        return jsonify({'info':'no_bind.mp3'})
    else:
        return jsonify({'info':'no_lic.mp3'})