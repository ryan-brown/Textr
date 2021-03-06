import datetime

class Text:

    providers = {
        'verizon' : '@vtext.com',
        'att' : '@txt.att.net',
        'alltell' : '@message.alltel.com',
        'boost' : '@myboostmobile.com',
        'comcast' : '@comcastpcs.textmsg.com',
        'metropcs' : '@mymetropcs.com',
        'sprint' : '@messaging.sprintpcs.com',
        'tmobile' : '@tmomail.net',
        'virgin' : '@vmobl.com'}

    def __init__(self, to, provider, message, time):
        self.to = to
        self.provider = provider
        self.you = to + self.providers[provider]
        self.message = message
        self.time = time

    def ready(self):
        return datetime.datetime.now() > self.time

    def __str__(self):
        return '|'.join(map(str, [self.to, self.provider, self.message, self.time]))

    def __eq__(self, other):
        return (self.you == other.you and self.message == other.message and self.time == other.time)
