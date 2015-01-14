import sys, os
import datetime
sys.path.append('/home/costa/askpupkin/askpupkin')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings
from ask.models import *
from django.contrib.auth.models import User
import random
from random_words import *
from django.test import Client
import time

c = Client()

response = c.post('/login/', {'username': 'ask_user', 'password': 'ask_pwd'})
if response.status_code == 302:
    print "Logged in"
else:
    print "Unable to log in"

rw = RandomWords()
rc = LoremIpsum()

tags = rw.random_words(None, 25)

while True:
    time.sleep(3)

    title = rc.get_sentence()
    content = rc.get_sentences(random.randint(5, 10))
    tags_str = ''
    tags_count = random.randint(1, 3)
    for i in range(0, tags_count):
        tags_str = tags_str + tags[random.randint(0, len(tags) - 1)] + ', '

    response = c.post('/', {'title': title, 'content': content, 'tags': tags_str, 'type': 'question'})
    print response.status_code
