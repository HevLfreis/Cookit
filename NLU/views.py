#!/usr/bin/env python
# coding: utf-8
import random
import re
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from django.template.loader import get_template
from django.utils import timezone

from NLU.constants import NLU_COP_TOPIC, PROJECT_NAME, NLU_HRL_TOPIC, NLU_PAT_TOPIC, MODELS, HYBRID_DLL
from NLU.enlu import ENLU_init, ENLU_Uninit
from NLU.methods import init, create_zipfile, hybrid_nlu, ws_nlu
from NLU.models import ModelValidate

# Create your views here.
# init()

# print NLU_PAT_TOPIC


def redirect2main(request):
    return redirect('home')


def home(request):
    if request.is_ajax():

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['id'] = random.randint(10000, 99999)
                return HttpResponse(1)
            else:
                return HttpResponse(-1)
        else:
            return HttpResponse(-1)

    else:
        return render(request, 'NLU/home.html', {'project_name': PROJECT_NAME})


def check_login(request):
    return HttpResponse(request.user.is_authenticated())


@login_required
def download(request):

    c_domains = sorted(NLU_COP_TOPIC.keys())
    h_domains = sorted(NLU_HRL_TOPIC.keys())
    p_domains = sorted(NLU_PAT_TOPIC.keys())
    return render(request, 'NLU/download.html',
                  {'c_domains': c_domains, 'c_topics': NLU_COP_TOPIC,
                   'h_domains': h_domains, 'h_topics': NLU_HRL_TOPIC,
                   'p_domains': p_domains, 'p_topics': NLU_PAT_TOPIC,
                   'project_name': PROJECT_NAME})


@login_required
def get_data(request):
    if request.is_ajax():

        try:
            topics = request.POST.get('topics')
            t = request.POST.get('t')

            print t

            if 'cop' in t:
                res = create_zipfile(topics, request.session.get('id'), 'cop')
            elif 'hrl' in t:
                res = create_zipfile(topics, request.session.get('id'), 'hrl')
            elif 'pat' in t:
                res = create_zipfile(topics, request.session.get('id'), 'pat')
            else:
                res = None

        except Exception, e:
            print e
            res = None

        t = get_template('NLU/dl_res.html')
        html = t.render(res['topics'])
        return JsonResponse({'filename': res['filename'], 'html': html}, safe=False)


@login_required
def word_segment(request):

    if request.is_ajax():

        words = request.POST.get('words')

        algo_type = request.POST.get('type')

        print algo_type

        if not words:
            return HttpResponse('')

        return HttpResponse(ws_nlu(words.encode('utf-8'), algo_type))
    
    return render(request, 'NLU/wseg.html', {'project_name': PROJECT_NAME})


@login_required
def model_test(request):

    if request.method == 'GET':
        return render(request, 'NLU/mtest.html', {'project_name': PROJECT_NAME, 'models': MODELS})

    elif request.is_ajax():

        row = request.POST.get('row')
        previd = request.POST.get('previd')

        if not previd:

            words = request.POST.get('words')
            mode = request.POST.get('mode')

            if words == '':
                return HttpResponse(0)

            # print MODELS[mode]

            ENLU_init(HYBRID_DLL, MODELS[mode], 1)

            words_list = filter(None, re.split(ur'[\n\u3002]', words))

            # print str(words_list).decode('string_escape')

            request.session['proc_words'] = {request.session.session_key: words_list}
            request.session['proc_idx'] = 0
            request.session['proc_len'] = float(len(words_list))
            idx = 0
            words = request.session['proc_words'][request.session.session_key][idx].encode('utf-8')

        else:

            idx = request.session['proc_idx']

            # print previd, idx
            words = request.session['proc_words'][request.session.session_key][idx-1]
            mt = ModelValidate.objects.get(id=previd, creator=request.user)

            # print words, mt.words

            if mt.words == words:
                mt.status = -1 if row == '0' else 1
                mt.save()
            else:
                return HttpResponse(-1)

            if idx >= request.session.get('proc_len'):

                del request.session['proc_words']
                del request.session['proc_idx']
                del request.session['proc_len']

                ENLU_Uninit(HYBRID_DLL)

                proc = 100

                t = get_template('NLU/mt_comp.html')
                html = t.render()

                return JsonResponse({'html': html, 'proc': proc})

            words = request.session['proc_words'][request.session.session_key][idx].encode('utf-8')

        # print words

        res = nlu_process(request, words)
        # print res

        request.session['proc_idx'] += 1
        proc = float(idx) / request.session.get('proc_len') * 100.0

        # print str(res['words']).decode('string_escape')

        t = get_template('NLU/mt_res.html')
        html = t.render({'domain': res['domain'], 'words': res['words'], 'wid': res['id']})

        return JsonResponse({'html': html, 'proc': proc})

    else:
        return HttpResponse(status=403)


def nlu_process(request, words):

    res_dict = hybrid_nlu(words)

    # print res_dict

    res = words
    for slot in res_dict['slot']:
        idx = words.find(slot)
        res = words[:idx]+'@'+res_dict['slot'][slot]+'='+slot+'@'+words[idx+len(slot):]

    if re.match("^.*[@].*[@].*$", res):
        word_list = res.split('@')[:-1]
    else:
        word_list = [res]

    mv = ModelValidate(words=words,
                       result=res,
                       creator=request.user,
                       status=0,
                       created_time=timezone.now())
    mv.save()

    for i, word in enumerate(word_list):
        if '>=' in word:
            word_list[i] = word.split('=')
        else:
            word_list[i] = [word]

    return {'domain': res_dict['domain'], 'words': word_list, 'id': mv.id}


