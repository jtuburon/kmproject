from __future__ import unicode_literals
from django.db import models
from mongoengine import *
import datetime
from mongoengine.django.auth import User


class DomainTag(EmbeddedDocument):
    uri= URLField(max_length=250)
    label= StringField(max_length=200)

# Create your models here.
class Lesson(Document):
    number= SequenceField(unique=True)
    project= StringField(max_length=200)
    leader= StringField(max_length=200)
    pub_date = DateTimeField(default=datetime.datetime.now, help_text='date published')
    #author= StringField(max_length=200)
    author = ReferenceField(User)
    role= StringField(max_length=200)
    title= StringField(max_length=400)
    problem= StringField()
    context= StringField()
    solution= StringField()
    tags = ListField(EmbeddedDocumentField(DomainTag))
    


class LessonResult(Document):
    number= IntField()
    pub_date = DateTimeField(default=datetime.datetime.now, help_text='date published')
    author= StringField(max_length=200)
    title= StringField(max_length=400)
    problem= StringField()
    tags = ListField(EmbeddedDocumentField(DomainTag))
    hits = ListField(StringField())
    hits_count = IntField();