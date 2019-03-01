from flask import Flask, render_template
from serv import content, get_set_anything, users, devices, friend, chat
from settings import IP_ADDR

app = Flask(__name__)

app.register_blueprint(content.content)
app.register_blueprint(get_set_anything.gsa)
app.register_blueprint(users.users)
app.register_blueprint(devices.devices)
app.register_blueprint(friend.friend)
app.register_blueprint(chat.chat)

@app.route('/')
def toy():
    return render_template('toy.html',ip_addr=IP_ADDR)

if __name__ == '__main__':
    app.run('0.0.0.0',8000,debug=True)
