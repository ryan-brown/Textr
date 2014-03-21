from flask import Flask
from flask import request
from flask import send_from_directory
import pickle
import math
import os
from time import sleep
import datetime
import thread
from text import Text
from textr import Textr

app = Flask(__name__, static_url_path='')

htmltop = '<html><head><title>Textr</title></head><body>'
htmlbot = '</body></html>'

params = ['to', 'provider', 'message', 'date', 'validate']

#texts = [Text('2394041933', 'verizon', 'Server starting', datetime.datetime.now())]
texts = []
textr = Textr()

@app.route('/', methods=['GET', 'POST'])
def hello():
    return app.send_static_file('index.html')

@app.route('/text', methods=['POST'])
def text():
    global params
    if not all(key in request.form for key in params):
        return htmltop + "Error 400 - Invalid params" + htmlbot

    to = request.form["to"]
    provider = request.form["provider"]
    message = request.form["message"]
    dateraw = request.form["date"]
    validate = request.form["validate"]

    return generate_text(to, provider, message, dateraw, validate)

def generate_text(to, provider, message, dateraw, validate):
    if validate != "":
        return htmltop + "Stahp it bots." + htmlbot

    try:
        year, month, day, hour, minute, second = map(int, dateraw.split())
        date = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
    except:
        return htmltop + "Error 400 - Invalid date format. <br/>use: 'year month day hour minute'<br/>For example '2014 7 5 15 35 15' for July 5, 2014 at 3:35PM and 15 seconds" + htmlbot

    message_len = len(message)
    if message_len > 100:
        num_txts = int(math.ceil(float(message_len)/100))
        new_txts = []
    
        f = open('log', 'a+')
        for i in range(num_txts):
            start = i*100
            new_message = '(' + str(i+1) + '/' + str(num_txts) + ')\n' + message[start:start+100]
            text = Text(to, provider, new_message, date + datetime.timedelta(0,10*i))
            new_txts.append(text)
         
            logtext = 'QUEUED: ' + str(request.remote_addr) + ' - ' + str(datetime.datetime.now()) + ' - ' + str(text)
            f.write(logtext+'\n')
        f.close()
        texts.extend(new_txts)
    else:
        text = Text(to, provider, message, date)

        f = open('log', 'a+')
        logtext='QUEUED: ' + str(request.remote_addr) + ' - ' + str(datetime.datetime.now()) + ' - ' + str(text)
        f.write(logtext+'\n')
        f.close()
        texts.append(text)

    return htmltop + 'Success!<br/><a href="/">Back</a>' + htmlbot

def text_runner(delay):
    global texts
    
    sendtexts = [text for text in texts if text.ready() == True]
    texts = [text for text in texts if text not in sendtexts]

    f = open('texts.pickle', 'wb+')
    pickle.dump(texts, f)
    f.close()

    for text in sendtexts:
        textr.send(text)
    
    sleep(delay)
    text_runner(delay)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

def load_texts():
    global texts
    if os.path.isfile('texts.pickle'):
        f = open('texts.pickle', 'rb')
        texts = pickle.load(f)
        f.close()

if __name__ == '__main__':
    load_texts()
    thread.start_new_thread(text_runner, (5,))
    app.run('0.0.0.0', 80)
