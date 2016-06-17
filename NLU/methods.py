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
import sched
import shutil
import zipfile
import time
import thread
from NLU.constants import NLU_TOPIC, STATIC_FOLDER, TEMP_PATH
from NLU.models import Corpus
from os.path import basename


def init():
    cs = Corpus.objects.all()
    for c in cs:
        domain, topic = c.topic.split('.', 1)

        if domain not in NLU_TOPIC:
            NLU_TOPIC[domain] = [topic, ]
        elif topic not in NLU_TOPIC[domain]:
            NLU_TOPIC[domain].append(topic)

    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH)

    else:
        shutil.rmtree(TEMP_PATH)
        os.makedirs(TEMP_PATH)


def get_corpus_file(topics, sessionid):

    topics = topics.strip().rstrip(';').split(';')

    print topics

    now = datetime.datetime.now()
    filename = str(sessionid)+'_'+now.strftime('%Y-%m-%d_%H-%M-%S')
    filepath = os.path.join(TEMP_PATH, filename)
    print filepath

    rtopics = create_temp_file(topics, filepath)
    thread.start_new_thread(do_clean_up_sched, (filepath,))
    return {'filename': filename, 'topics': rtopics}


def create_temp_file(topics, filepath):

    txt = codecs.open(filepath+'.txt', 'w+', 'utf-8')

    topic_success, topic_failed, top_dict = [], [], {}
    #
    for topic in topics:
        if Corpus.objects.filter(topic__exact=topic).exists() and topic not in top_dict:
            top_dict[topic] = 1
            topic_success.append(topic.strip().split('.', 1))
            cps = Corpus.objects.filter(topic__exact=topic)
            for cp in cps:
                # print cp.topic+'\t'+cp.content
                txt.write(cp.topic+'    '+cp.content+'\n')
        else:
            topic_failed.append(topic.strip().split('.', 1))

    txt.close()

    f = zipfile.ZipFile(filepath+'.zip', 'w', zipfile.ZIP_DEFLATED)
    f.write(filepath+'.txt', basename(filepath+'.txt'))
    f.close()

    return {'success': topic_success, 'errors': topic_failed}


def do_clean_up_sched(filepath):
    s = sched.scheduler(time.time, time.sleep)
    s.enter(120, 1, do_clean_up, (filepath,))
    s.run()


def do_clean_up(filepath):

    try:
        os.remove(filepath+'.txt')
        os.remove(filepath+'.zip')

        print 'Clean up:', filepath
    except Exception, e:
        print e




