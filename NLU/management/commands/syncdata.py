#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2016/7/22
# Time: 9:28
import codecs
import datetime
import glob
import hashlib
import sys

from django.core.management import BaseCommand
from os.path import basename

from django.utils import timezone

from Cookit.settings import BASE_DIR
from NLU.models import Corpus, Pattern, Hrl


class Command(BaseCommand):
    help = 'Sync data to db'

    def handle(self, *args, **options):
        now = timezone.now()

        for filename in glob.iglob(BASE_DIR+'/static/data/*.cop'):
            print 'Corpus file: '+basename(filename)

            cops = []
            for i, line in enumerate(codecs.open(filename, 'r', 'utf-8')):
                line = line.strip()

                t = line.split('\t')
                md5 = hashlib.md5(line.encode('utf-8')).hexdigest()
                cop = Corpus(topic=t[0],
                             content=t[1],
                             md5=md5,
                             last_modified=now)
                cops.append(cop)

                print('\rImporting... '+str(i)),
            print '\nSaving...'
            # Corpus.objects.bulk_create(cops, 1000)
            print 'Saved\n'

        for filename in glob.iglob(BASE_DIR+'/static/data/*.hrl'):
            print 'Hrl file: '+basename(filename)

            hrls = []
            for i, line in enumerate(codecs.open(filename, 'r', 'utf-8')):
                if i < 3:
                    continue
                line = line.strip()

                t = line.split('#')
                # print t
                hrl = Hrl(speech_file=t[1],
                          speaker=t[2],
                          gender=False if t[3] == 'male' else True,
                          reference_word_sequence=t[4],
                          topic=t[5],
                          slot_names=t[6],
                          slot_values=t[7],
                          last_modified=now)

                hrls.append(hrl)

                print('\rImporting... '+str(i)),
            print '\nSaving...'
            # Hrl.objects.bulk_create(pats, 1000)
            print 'Saved\n'

        for filename in glob.iglob(BASE_DIR+'/static/data/*.pat'):
            print 'Pattern file: '+basename(filename)

            pats = []
            for i, line in enumerate(codecs.open(filename, 'r', 'utf-8')):
                line = line.strip()

                t = line.split('\t')
                if len(t) != 2:
                    t = line.split(' ', 1)
                if len(t) != 2:
                    t = line.split('  ', 1)
                if len(t) != 2:
                    continue
                md5 = hashlib.md5(line.encode('utf-8')).hexdigest()
                pat = Pattern(topic=t[0],
                              content=t[1],
                              md5=md5,
                              last_modified=now)

                pats.append(pat)

                print('\rImporting... '+str(i)),
            print '\nSaving...'
            # Pattern.objects.bulk_create(pats, 1000)
            print 'Saved\n\nAll Completed'




