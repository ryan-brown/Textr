from flask import Flask
from flask import request
from flask import send_from_directory
import os
from time import sleep
import datetime
import thread
from text import Text
from textr import Textr

app = Flask(__name__, static_url_path='')

htmltop = '<html><head><title>Textr</title></head><body>'
htmlbot = '</body></html>'

#texts = [Text('2394041933', 'verizon', 'Server starting', datetime.datetime.now())]
texts = []
textr = Textr()

@app.route('/', methods=['GET', 'POST'])
def hello():
    return app.send_static_file('index.html')

@app.route('/text', methods=['POST'])
def text():
    to = request.form["to"]
    provider = request.form["provider"]
    message = request.form["message"]
    dateraw = request.form["date"]
    validate = request.form["validate"]
    if validate != "":
        return "Stahp it bots."

    year, month, day, hour, minute = map(int, dateraw.split())

    date = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
    texts.append(Text(to, provider, message, date))

    return htmltop + 'Success!<br/><a href="/">Back</a>' + htmlbot

def text_runner(delay):
    global texts
    
    sendtexts = [text for text in texts if text.ready() == True]
    texts = [text for text in texts if text not in sendtexts]

    f = open('texts', 'w+')
    for text in texts:
        f.write(text.encode()+'\n')
    f.close()

    for text in sendtexts:
        textr.send(text)
    
    sleep(delay)
    text_runner(delay)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

def load_texts():
    if os.path.isfile('texts'):
        lines = [line.strip('\n') for line in open('texts', 'r')]
        for line in lines:
            texts.append(Text.decode(line))

if __name__ == '__main__':
    load_texts()
    thread.start_new_thread(text_runner, (10,))
    app.run('0.0.0.0', 80)
