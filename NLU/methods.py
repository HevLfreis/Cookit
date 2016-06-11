#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2016/6/10 
# Time: 18:21
#
import StringIO
import codecs
import os
import datetime
import zipfile
import thread
from NLU.constants import NLU_TOPIC, STATIC_FOLDER
from NLU.models import Corpus


def init():
    cs = Corpus.objects.all()
    for c in cs:
        domain, topic = c.topic.split('.', 1)

        if domain not in NLU_TOPIC:
            NLU_TOPIC[domain] = [topic, ]
        elif topic not in NLU_TOPIC[domain]:
            NLU_TOPIC[domain].append(topic)


def get_corpus_file(topics, sessionid):

    topics = topics.strip().rstrip(';').split(';')

    print topics

    now = datetime.datetime.now()
    filename = str(sessionid)+'_'+now.strftime('%Y-%m-%d_%H-%M-%S')
    filepath = os.path.join(STATIC_FOLDER, 'temp\\' + filename)
    print filepath

    # thread.start_new_thread(create_file, (topics, filepath))
    create_file(topics, filepath)
    return filename


def create_file(topics, filepath):
    txt = codecs.open(filepath+'.txt', 'w+', 'utf-8')
    #
    for topic in topics:
        cps = Corpus.objects.filter(topic=topic)
        for cp in cps:
            # print cp.topic+'\t'+cp.content
            txt.write(cp.topic+'\t'+cp.content+'\n')

    txt.close()

    f = zipfile.ZipFile(filepath+'.zip', 'w', zipfile.ZIP_DEFLATED)
    f.write(filepath+'.txt')
    f.close()



