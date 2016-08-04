#!/usr/bin/env python
# coding: utf-8
import codecs
from ctypes import *
import getpass
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

# import jieba
from PIL import Image


# def corpus_list(pattern):
#     segments = map(lambda x: x.lstrip('(').split('|') if x.startswith('(') else ['']+x.lstrip('[').split('|'),
#                    re.split('[\])]', pattern.replace(' ', ''))[:-1])
#
#     # print str(segments).decode('string_escape')
#
#     cp_list = ['']
#     for seg in segments:
#         new_list = []
#         for word in seg:
#             for cp in cp_list:
#                 new_list.append(cp+word)
#         cp_list = new_list
#     return cp_list
#
#
# def generate_corpus(in_file, out_file, repeat_min=1, repeat_max=1, prop=0.15):
#     with open(in_file, 'r') as i_f, open(out_file, 'w') as o_f:
#         for line in i_f:
#             cls = corpus_list(line.strip())
#             cls = random.sample(cls, int(len(cls) * prop))
#             for cl in cls:
#                 for _ in xrange(random.randint(repeat_min, repeat_max)):
#                     o_f.write(cl+'\n')
#     i_f.close()
#     o_f.close()
# import codecs
#
# sym_reg = ur'[\u3002|\uff1f|\uff01|\uff0c|\u3001]'
#
# chn_reg = ur'[^\u4E00-\u9FA5]'
#
# new_file = codecs.open("songci2.txt", "w", "utf-8")
#
# i, c = 0, 0
# for line in codecs.open('songci.txt', 'r', 'utf-8'):
#     i += 1
#     # print i
#     # print line
#     if i == 3 or i == 4:
#         # print line
#
#         words = re.split(sym_reg, line.strip())
#
#         for word in words[0:-1]:
#             t = re.sub(chn_reg, '', word)
#             print t
#             new_file.write(t+'\n')
#
#     if line == '\r\n':
#         new_file.write('\n')
#         c += 1
#         i = 0
#
# print c
# new_file.close()









# if __name__ == '__main__':
    # generate_corpus('pattern.txt', 'pa.txt')

    # print map(lambda x: x.lstrip('(').split('|') if x.startswith('(') else ['']+x.lstrip('[').split('|'), re.split('[\])]', "[a|b][c|d](e|f)".replace(' ', ''))[:-1])
    # print corpus_list("[a][c|r](e)")

    # f = open('ts.txt', 'w')
    # f.write('a'+'\t'+'b')
    # print 'Hi'

    # str = u'连续降雨让长江南京段水位也升至高点，扬子晚报记者昨天沿江探访，整个滨江风光带的亲水步道基本都已经没入江水中，江面与防洪堤也已经非常接近。在青奥公园内有一组雕塑，记录了百年来南京长江江面水位的历史，每一根钢柱代表一年的水位高度。在现场，江面已经几乎将这组雕塑淹没，仅剩1957年等几个年份的刻度仍然能看到。'
    # base_dir =  os.path.dirname(os.getcwd())+'\\static\\ws\\'
    # from time import clock
    # start=clock()
    #
    #
    # end = clock()
    # print (end-start), 'dll'
    # start=clock()
    # # seg_list = jieba.cut(str, cut_all=False)
    # # print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
    # end = clock()
    # print (end-start)
    # def hex_to_rgb(value):
    #     value = value.lstrip('#')
    #     lv = len(value)
    #     return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))
    #
    # img = Image.new('RGB', (200, 200), hex_to_rgb('#3498db'))
    # img.save('a.png')



# import codecs
#
# sym_reg = ur'[\u3002|\uff1f|\uff01|\uff0c|\u3001]'
#
# chn_reg = ur'[^\u4E00-\u9FA5]'
#
# new_file = codecs.open("quansongci2.txt", "w", "utf-8")
#
# i, c, last_line = False, 0, ''
# for line in codecs.open('quansongci.txt', 'r', 'utf-8'):
#
#     if line == '':
#         i = True
#         continue
#
#     words = re.split(sym_reg, line.strip())
#
#     if len(words) < 2:
#
#         if not i:
#             c += 1
#             new_file.write('\n')
#         i = True
#         continue
#
#     for word in words[0:-1]:
#         t = re.sub(chn_reg, '', word)
#         # print t
#         new_file.write(t+'\n')
#
#     i = False
#
#
# print c
# new_file.close()
#
endfile = codecs.open("nu_rnn_sample_all.txt", "w", "utf-8")


for d in os.listdir('rnn_sample'):
    if d.endswith('txt'):
        f = codecs.open('rnn_sample/'+d, "r", "utf-8")
        endfile.writelines(f.readlines()[1:-1])

endfile.close()




