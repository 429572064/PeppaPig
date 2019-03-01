from settings import SPEECH, VOICE, CHATS_PATH, MONGO_DB
from uuid import uuid4
from bson import ObjectId
from ai.to_tuling import tuling
import os


def text2audio(text):
    filename = f'{uuid4()}.mp3'
    result = SPEECH.synthesis(text,'zh',1,VOICE)
    file_path = os.path.join(CHATS_PATH,filename)

    if not isinstance(result,dict):
        with open(file_path,'wb') as f:
            f.write(result)

    return filename


def get_file_content(filepath):
    os.system(f'ffmpeg -y -i {filepath} -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {filepath}.pcm')
    with open(f'{filepath}.pcm', 'rb') as fp:
        return fp.read()


def audio2text(filepath):
    res = SPEECH.asr(get_file_content(filepath),'pcm',16000,{'<dev_pid></dev_pid>':1536})
    print('123',filepath,res)
    print(res.get('result')[0])

    return res.get('result')[0]


def my_nlp(Q,nid):
    # Q = '我要给爸爸发消息'
    if '发消息' in Q:
        print('nid',nid)
        toy = MONGO_DB.toys.find_one({'_id':ObjectId(nid)})
        print('toy',toy)
        for friend in toy.get('friend_list'):
            print('friend',friend)
            if friend.get('friend_nick') in Q or friend.get('friend_name') in Q:
                msg = f"可以按消息键给{friend.get('friend_nick')}发消息了"
                filename = text2audio(msg)
                return {'chat':filename,'from_user':str(friend.get('friend_id'))}

    #  Q = '我要听小毛驴'
    if '我要听' in Q or '我想听' in Q or '播放' in Q:
        content_list = MONGO_DB.content.find({})
        for content in content_list:
            if content.get('title') in Q:
                return {'music':content.get('audio'),'from_user':'ai'}

    text = tuling(Q,nid)
    filename = text2audio(text)

    return {'chat':filename,'from_user':'ai'}


