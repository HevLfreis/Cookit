# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Corpus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=200)),
                ('md5', models.CharField(max_length=50)),
                ('last_modified', models.DateTimeField()),
                ('last_modified_backup', models.CharField(max_length=200)),
            ],
        ),
    ]