# #!/usr/bin/env python
# # coding: utf-8
# import codecs
# from ctypes import *
# import getpass
# import os
# import random
# import re
#
# import sys
#
#
# # Create your tests here.
#
#
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
#         for l in i_f:
#             cls = corpus_list(l.strip())
#             cls = random.sample(cls, int(len(cls) * prop))
#             for cl in cls:
#                 for _ in xrange(random.randint(repeat_min, repeat_max)):
#                     o_f.write(cl+'\n')
#     i_f.close()
#     o_f.close()
#
#
# #######################################################################
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
#
# import codecs
#
# import re
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
#         i = False
#
#
# print c
# new_file.close()
#
# endfile = codecs.open("nu_rnn_sample_all.txt", "w", "utf-8")
#
#
# for d in os.listdir('rnn_sample'):
#     if d.endswith('txt'):
#         f = codecs.open('rnn_sample/'+d, "r", "utf-8")
#         endfile.writelines(f.readlines()[1:-1])
#
# endfile.close()
#
#
#
#
# import codecs
# import os
#
# news_dir = 'd://temp/nuance/news/'
#
# news = codecs.open(news_dir+'all.txt', 'w', 'utf-8')
#
# # for i, l in enumerate(news):
# #     print l
# #     if i > 1000:
# #         break
#
#
# for i, d in enumerate(os.listdir(news_dir)):
#     if d == 'all.txt' or i > 20:
#         continue
#     print d
#
#     for l in codecs.open(news_dir+d, 'r', 'gb18030'):
#         # print l
#         if l.startswith('<contenttitle>'):
#             n_l = l.strip().lstrip('<contenttitle>').rstrip('</contenttitle>')
#             # print n_l
#             if n_l == '':
#                 continue
#             news.write(n_l+'\n')
#         elif l.startswith('<content>'):
#             n_l = l.strip().lstrip('<content>').rstrip('</content>')
#             # print n_l
#             if n_l == '':
#                 continue
#             news.write(n_l+'\n\n')
#
# news.close()



# import time
#
# a = set([x for x in xrange(10000000)])
# b = set([x for x in xrange(10000000) if x % 2 == 0])
#
# start_time = time.time()
#
# c = a - b
#
# print("--- %s seconds ---" % (time.time() - start_time))
#
# start_time = time.time()
#
# c = set([])
# for x in a:
#     if x not in b:
#         c.add(x)
#
# print("--- %s seconds ---" % (time.time() - start_time))'
# import codecs
# import random
#
# with codecs.open('no_db_close_test_result.txt', 'r', 'utf-8') as i_f \
#         , codecs.open('result.txt', 'w', 'utf-8') as r_f\
#         , codecs.open('output.txt', 'r', 'utf-8') as o_f:
#
#     og = {}
#
#     for l in o_f:
#         spl = l.split()
#         if spl[0] in og:
#             og[spl[0]].append(spl[1])
#         else:
#             og[spl[0]] = [spl[1]]
#
#     tmp = {}
#     for i, line in enumerate(i_f):
#
#         print i
#         if i < 3:
#             continue
#         splits = line.split('%%')
#         a, b = splits[0].split('#')[2], splits[1].split(';')[0]
#         if a == b:
#             if a in tmp:
#                 tmp[a].append(splits[0].split('#')[0])
#             else:
#                 tmp[a] = [splits[0].split('#')[0]]
#
#     tmp = sorted(tmp.items(), key=lambda x: x[0])
#
#     for a, b in tmp:
#         if a in og:
#             c = list(set(b) - set(og[a]))
#             sam = random.sample(c, 10)
#             for o in og[a]:
#                 r_f.write(a+'\t'+o+'\n')
#             for s in sam:
#                 r_f.write(a+'\t'+s.rstrip(u'。').replace(' ', '')+'\n')

