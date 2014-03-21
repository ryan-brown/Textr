import smtplib

class Textr:
 
    def __init__(self):
        self.me = 'delayedmailman@gmail.com'
        self.password = 'Qwerty1993'

        self.server = smtplib.SMTP('smtp.gmail.com:587')
        self.server.starttls()
        self.server.login(self.me, self.password)

    def send(self, text):
        self.server.sendmail(self.me, text.you, '\n'+text.message)

    def destroy(self):
        self.server.close()

