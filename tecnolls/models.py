from __future__ import unicode_literals
from django.db import models
from mongoengine import *
import datetime
from mongoengine.django.auth import User

# Create your models here.

class DomainTag(EmbeddedDocument):
    uri= URLField(max_length=250)
    label= StringField(max_length=200)

class LessonRate(EmbeddedDocument):
    user= ReferenceField(User)
    date= DateTimeField(default=datetime.datetime.now, help_text='date rated')
    rate= DecimalField(precision=1)

class Lesson(Document):
    number= SequenceField(unique=True)
    project= StringField(max_length=200)
    leader= StringField(max_length=200)
    pub_date = DateTimeField(default=datetime.datetime.now, help_text='date published')
    author = ReferenceField(User)
    role= StringField(max_length=200)
    title= StringField(max_length=400)
    problem= StringField()
    context= StringField()
    solution= StringField()
    tags = ListField(EmbeddedDocumentField(DomainTag))
    rates = ListField(EmbeddedDocumentField(LessonRate))

    @property
    def rate_avg(self):
        return  sum([r.rate for r in self.rates])/ len(self.rates) if len(self.rates)>0 else None

class LessonResult(Document):
    number= IntField()
    pub_date = DateTimeField(default=datetime.datetime.now, help_text='date published')
    author = ReferenceField(User)
    title= StringField(max_length=400)
    problem= StringField()
    tags = ListField(EmbeddedDocumentField(DomainTag))
    hits = ListField(StringField())
    hits_count = IntField();
    rate_avg= DecimalField(precision=1)