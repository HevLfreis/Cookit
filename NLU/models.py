from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Corpus(models.Model):
    topic = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    md5 = models.CharField(max_length=50)
    last_modified = models.DateTimeField()


class Pattern(models.Model):
    topic = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    md5 = models.CharField(max_length=50)
    last_modified = models.DateTimeField()
    md8 = models.CharField(max_length=50)


class Hrl(models.Model):
    speech_file = models.CharField(max_length=100)
    speaker = models.CharField(max_length=50)
    gender = models.BooleanField()
    reference_word_sequence = models.CharField(max_length=200)
    topic = models.CharField(max_length=100)
    slot_names = models.CharField(max_length=1000)
    slot_values = models.CharField(max_length=1000)
    last_modified = models.DateTimeField()


class ModelValidate(models.Model):
    words = models.CharField(max_length=200)
    result = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField()
    created_time = models.DateTimeField()
