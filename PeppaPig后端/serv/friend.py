from flask import Blueprint, request, jsonify
from settings import MONGO_DB, RET
from bson import ObjectId


friend = Blueprint('friend',__name__)

@friend.route('/friend_list',methods=['POST'])
def friend_list():
    print(request.form.get('user_id'))
    user_id = ObjectId(request.form.get('user_id'))
    user_info = MONGO_DB.users.find_one({'_id':user_id})

    RET['code'] = 0
    RET['msg'] = '好友列表查看'
    RET['data'] = user_info.get('friend_list')

    return jsonify(RET)
