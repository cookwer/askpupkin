from django.db import models
from django.contrib.auth.models import User
from djangosphinx.models import SphinxSearch


class Tag(models.Model):
    name = models.CharField(max_length=32, db_index=True)

    def __unicode__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=2048)
    author = models.ForeignKey(User)
    date = models.DateTimeField()

    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField()
    search = SphinxSearch(
        index='questions',
        weights={
            'title': 100,
            'content': 40,
        }
    )

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    content = models.CharField(max_length=1024)
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
    date = models.DateTimeField()
    right = models.BooleanField()
    rating = models.IntegerField()
    search = SphinxSearch(
        index='answers',
        weights={
            'content': 100,
        }
    )

    def __unicode__(self):
        return self.content


class QuestionVote(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    value = models.SmallIntegerField()


class AnswerVote(models.Model):
    answer = models.ForeignKey(Answer)
    user = models.ForeignKey(User)
    value = models.SmallIntegerField()
