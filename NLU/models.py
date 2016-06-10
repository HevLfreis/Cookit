from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Corpus(models.Model):
    topic = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    md5 = models.CharField(max_length=50)
    last_modified = models.DateTimeField()
    last_modified_backup = models.CharField(max_length=200)
