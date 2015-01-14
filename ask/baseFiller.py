import sys, os
import datetime

sys.path.append('/home/costa/askpupkin/askpupkin')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings
from ask.models import *
from django.contrib.auth.models import User
import random

from random_words import *


def has_user(username):
    if len(User.objects.filter(username__exact=username)):
        return True

    return False


def has_tag(tags, tagname):
    for t in tags:
        if t.name == tagname:
            return True

    return False

rw = RandomWords()
re = RandomEmails()
rn = RandomNicknames()
rc = LoremIpsum()

tags = []

for i in range(0, 100):
    tagname = rw.random_word()
    while has_tag(tags, tagname):
        tagname = rw.random_word()

    tag = Tag(name=tagname)
    tag.save()
    tags.append(tag)

print "Tags added"

user_ids = []

for i in range(0, 10000):
    username = rn.random_nick(gender='u')

    while has_user(username):
        username = rn.random_nick(gender='u') + str(random.randint(10, 999))

    user = User.objects.create_user(username=username, email=re.randomMail(),
                                    first_name=rn.random_nick(gender='u'), last_name=rn.random_nick(gender='u'))
    user.set_password(rw.random_word())
    user.save()
    user_ids.append(user.id)

print "Users added"

question_ids = []

for i in range(0, 100000):
    title = rc.get_sentence()
    if len(title) > 100:
        title = title[0:99]
    q_title = title[0:len(title)-1]

    quest = Question(title=q_title+"?", author_id=user_ids[random.randint(0, len(user_ids)-1)],
                     content=rc.get_sentences(random.randint(5, 10)), date=datetime.datetime.today())

    #generate votes
    up_votes_count = random.randint(0, 99)

    # reduce votes count
    if up_votes_count > 50 and random.randint(0, 1) == 0:
        up_votes_count /= 3

    down_votes_count = random.randint(0, 10)

    quest.rating = up_votes_count - down_votes_count
    quest.save()

    group_start = random.randint(0, len(user_ids) - (up_votes_count + down_votes_count))

    voted_user_ids = user_ids[group_start:group_start + up_votes_count + down_votes_count]

    for j, user_id in enumerate(voted_user_ids):
        if j <= up_votes_count:
            vote = QuestionVote(question_id=quest.id, user_id=user_id, value=1)
            vote.save()
        else:
            vote = QuestionVote(question_id=quest.id, user_id=user_id, value=-1)
            vote.save()

    #add tags
    for j in range(0, random.randint(0, 3)):
        quest.tags.add(tags[random.randint(0, len(tags)-1)])

    quest.save()

    question_ids.append(quest.id)

print "Questions added"

for i in range(0, 1000000):
    answer = Answer(author_id=user_ids[random.randint(0, len(user_ids)-1)],
                    question_id=question_ids[random.randint(0, len(question_ids)-1)],
                    right=random.choice([False, True, False, False, False]),
                    content=rc.get_sentences(random.randint(1, 5)),
                    date=datetime.datetime.today())

    #generate votes
    up_votes_count = random.randint(0, 15)

    # reduce votes count
    if up_votes_count > 10 and random.randint(0, 1) == 0:
        up_votes_count /= 2

    down_votes_count = random.randint(0, 5)

    answer.rating = up_votes_count - down_votes_count
    answer.save()

    group_start = random.randint(0, len(user_ids) - (up_votes_count + down_votes_count))

    voted_user_ids = user_ids[group_start:group_start + up_votes_count + down_votes_count]

    for j, user_id in enumerate(voted_user_ids):
        if j <= up_votes_count:
            vote = AnswerVote(answer_id=answer.id, user_id=user_id, value=1)
            vote.save()
        else:
            vote = AnswerVote(answer_id=answer.id, user_id=user_id, value=-1)
            vote.save()

print "Answers added"
