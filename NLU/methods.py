#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2016/6/10 
# Time: 18:21
#
import codecs
import datetime
import os
import sched
import shutil
import thread
import time
import zipfile
from ctypes import cdll
from os.path import basename

from Cookit.settings import BASE_DIR
from NLU.constants import NLU_COP_TOPIC, TEMP_PATH, NLU_HRL_TOPIC, NLU_PAT_TOPIC, HYBRID_MODEL_FILE, HYBRID_DLL, CRF_DLL, \
    CRF_MODEL_FILE
from NLU.enlu import ENLU_init, ENLU_Process, ENLU_Uninit, Word_segment_init, Word_segment_for_string, \
    Word_segment_uninit
from NLU.models import Corpus, Hrl, Pattern


def init():
    for c in Corpus.objects.all():
        domain, topic = c.topic.split('.', 1)

        if domain not in NLU_COP_TOPIC:
            NLU_COP_TOPIC[domain] = [topic, ]
        elif topic not in NLU_COP_TOPIC[domain]:
            NLU_COP_TOPIC[domain].append(topic)

    for h in Hrl.objects.all():
        domain, topic = h.topic.split('_')[1:3]
        if domain not in NLU_HRL_TOPIC:
            NLU_HRL_TOPIC[domain] = [topic, ]
        elif topic not in NLU_HRL_TOPIC[domain]:
            NLU_HRL_TOPIC[domain].append(topic)

    for p in Pattern.objects.all():
        domain, topic = p.topic.split('.', 1)
        if domain not in NLU_PAT_TOPIC:
            NLU_PAT_TOPIC[domain] = [topic, ]
        elif topic not in NLU_PAT_TOPIC[domain]:
            NLU_PAT_TOPIC[domain].append(topic)

    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH)

    else:
        shutil.rmtree(TEMP_PATH)
        os.makedirs(TEMP_PATH)

    ENLU_init(HYBRID_DLL, HYBRID_MODEL_FILE, 1)
    Word_segment_init(CRF_DLL, CRF_MODEL_FILE)


def create_zipfile(topics, sessionid, context='corpus'):

    topics = topics.strip().rstrip(';').split(';')

    print topics

    now = datetime.datetime.now()
    filename = str(sessionid)+'_'+now.strftime('%Y-%m-%d_%H-%M-%S')
    filepath = os.path.join(TEMP_PATH, filename)
    print filepath

    if context == 'cop':
        rtopics = create_corpus_file(topics, filepath)
    elif context == 'hrl':
        rtopics = create_hrl_file(topics, filepath)
    elif context == 'pat':
        rtopics = create_pattern_file(topics, filepath)

    print rtopics, 'r'

    thread.start_new_thread(do_clean_up_sched, (filepath,))
    return {'filename': filename, 'topics': rtopics}


def create_corpus_file(topics, filepath):

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

    zip_file(filepath, '.txt')

    return {'success': topic_success, 'errors': topic_failed}


def create_hrl_file(topics, filepath):

    txt = codecs.open(filepath+'.hrl', 'w+', 'utf-8')

    topic_success, topic_failed, top_dict = [], [], {}

    hrl_head = '#head;hrl;2.0;utf-8\n' \
               '#ref#speechfile#speaker#gender#reference word sequence#topic#;slot names#;slot values\n' \
               'head\n'

    txt.write(hrl_head)

    for topic in topics:

        t = topic.replace('.', '_')

        if Hrl.objects.filter(topic__contains=t).exists() and topic not in top_dict:
            top_dict[topic] = 1
            topic_success.append(topic.strip().split('.', 1))
            hrls = Hrl.objects.filter(topic__contains=t)
            for hrl in hrls:
                # print cp.topic+'\t'+cp.content
                gender = 'female' if hrl.gender else 'male'
                txt.write('ref#'+hrl.speech_file+'#'+hrl.speaker+'#'+gender+'#'+hrl.reference_word_sequence+
                          '#'+hrl.topic+'#'+hrl.slot_names+'#'+hrl.slot_values+'\n')
        else:
            topic_failed.append(topic.strip().split('.', 1))

    txt.close()

    zip_file(filepath, '.hrl')

    return {'success': topic_success, 'errors': topic_failed}


def create_pattern_file(topics, filepath):

    txt = codecs.open(filepath+'.pat', 'w+', 'utf-8')

    topic_success, topic_failed, top_dict = [], [], {}
    #
    for topic in topics:
        if Pattern.objects.filter(topic__exact=topic).exists() and topic not in top_dict:
            top_dict[topic] = 1
            topic_success.append(topic.strip().split('.', 1))
            ps = Pattern.objects.filter(topic__exact=topic)
            for p in ps:
                # print cp.topic+'\t'+cp.content
                txt.write(p.topic+'    '+p.content+'\n')
        else:
            topic_failed.append(topic.strip().split('.', 1))

    txt.close()

    zip_file(filepath, '.pat')

    return {'success': topic_success, 'errors': topic_failed}


def zip_file(filepath, suffix):
    f = zipfile.ZipFile(filepath+'.zip', 'w', zipfile.ZIP_DEFLATED)
    f.write(filepath+suffix, basename(filepath+suffix))
    f.close()


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


def hybrid_nlu(words):

    res = ENLU_Process(HYBRID_DLL, words)
    # ENLU_Uninit(dll)

    return res


def ws_nlu(words):
    res = Word_segment_for_string(CRF_DLL, words)
    # Word_segment_uninit(dll)
    return res





