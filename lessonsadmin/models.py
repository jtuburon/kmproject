from __future__ import unicode_literals
from django.db import models
from mongoengine import *
import datetime

class DomainTag(Document):
	uri= URLField(max_length=250, unique=True)
	label= StringField(max_length=200, unique=True)

# Create your models here.
class Lesson(Document):
    number= SequenceField(unique=True)
    project= StringField(max_length=200)
    leader= StringField(max_length=200)
    pub_date = DateTimeField(default=datetime.datetime.now, help_text='date published')
    author= StringField(max_length=200)
    role= StringField(max_length=200)
    title= StringField(max_length=400)
    problem= StringField()
    context= StringField()
    solution= StringField()
    tags = ListField(DomainTag)
