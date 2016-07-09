import random

# import jieba
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import get_template

from NLU.constants import NLU_COP_TOPIC, PROJECT_NAME, NLU_HRL_TOPIC, NLU_PAT_TOPIC
from NLU.methods import init, create_zipfile, hybrid_nlu, ws_nlu

init()

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
                   'p_domains': p_domains, 'p_topics': NLU_PAT_TOPIC, 'project_name': PROJECT_NAME})


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

        # seg_list = jieba.cut(words, cut_all=False)

        # return HttpResponse('|'.join(seg_list))
        return HttpResponse('No')
    return render(request, 'NLU/wseg.html', {'project_name': PROJECT_NAME})


def model_test(request):

    if request.is_ajax():
        words = request.POST.get('words').encode('utf-8')

        res = hybrid_nlu(words)
        new_words = ws_nlu(words).split('|')

        # for i, nw in enumerate(new_words):
        #     if nw in res['slot']:
        #         new_words.insert(i, '@'+res['slot'][nw])

        for slot in res['slot']:
            idx = words.find(slot)
            words = words[:idx]+'@'+res['slot'][slot]+'='+slot+'@'+words[idx+len(slot):]

        word_list = words.split('@')

        for i, word in enumerate(word_list):
            if '>=' in word:
                word_list[i] = word.split('=')
            else:
                word_list[i] = [word]

        print str(word_list).decode('string_escape')
        return render(request, 'NLU/mt_res.html', {'domain': res['domain'], 'words': word_list})
    return render(request, 'NLU/mtest.html', {'project_name': PROJECT_NAME})


