#!/usr/bin/env python
# coding: utf-8
import os
import random
import re

import sys


# Create your tests here.


# import time, sched
#
#
# def event_func(msg):
#     print "Current Time:",time.time(),'msg:',msg
#
# if __name__ == "__main__":
#
#     s = sched.scheduler(time.time, time.sleep)
#
#     s.enter(8, 2,event_func,("Small event.",))
#     s.enter(2,1,event_func,("Big event.",))
#     s.run()
from os.path import dirname, abspath

def corpus_list(pattern):
    segments = map(lambda x: x.lstrip('(').split('|') if x.startswith('(') else ['']+x.lstrip('[').split('|'),
                   re.split('[\])]', pattern.replace(' ', ''))[:-1])

    # print str(segments).decode('string_escape')

    cp_list = ['']
    for seg in segments:
        new_list = []
        for word in seg:
            for cp in cp_list:
                new_list.append(cp+word)
        cp_list = new_list
    return cp_list


def generate_corpus(in_file, out_file, repeat_min=1, repeat_max=1, prop=0.15):
    with open(in_file, 'r') as i_f, open(out_file, 'w') as o_f:
        for line in i_f:
            cls = corpus_list(line.strip())
            cls = random.sample(cls, int(len(cls) * prop))
            for cl in cls:
                for _ in xrange(random.randint(repeat_min, repeat_max)):
                    o_f.write(cl+'\n')
    i_f.close()
    o_f.close()


if __name__ == '__main__':
    # generate_corpus('pattern.txt', 'pa.txt')

    # print map(lambda x: x.lstrip('(').split('|') if x.startswith('(') else ['']+x.lstrip('[').split('|'), re.split('[\])]', "[a|b][c|d](e|f)".replace(' ', ''))[:-1])
    # print corpus_list("[a|b][c|d](e|f)")

    # f = open('ts.txt', 'w')
    # f.write('a'+'\t'+'b')
    PROJECT_DIR = dirname(dirname(abspath(__file__)))
    sys.path.append(PROJECT_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Cookit.settings")

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

    from django.contrib.auth.models import User
    #
    user = User.objects.create_user(username='test',
                                    email='test@123.com',
                                    password='123456')




