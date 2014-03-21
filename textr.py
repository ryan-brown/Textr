import smtplib
import datetime

class Textr:
 
    def __init__(self):
        self.me = 'delayedmailman@gmail.com'
        self.password = 'Qwerty1993'

    def send(self, text):
        self.server = smtplib.SMTP('smtp.gmail.com:587')
        self.server.starttls()
        self.server.login(self.me, self.password)
        self.server.sendmail(self.me, text.you, '\n' + text.message + '\n\nSent via Textr\nVisit us at textr.info')
        
        f = open('log', 'a+')
        logtext = 'SENT  : ' + str(datetime.datetime.now()) + ' - ' + str(text)
        f.write(logtext+'\n')
        f.close()

        self.server.close()

