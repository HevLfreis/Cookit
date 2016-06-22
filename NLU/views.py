import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import get_template

from NLU.constants import NLU_CORPUS_TOPIC, PROJECT_NAME, NLU_HRL_TOPIC
from NLU.methods import init, create_zipfile

init()

# print NLU_HRL_TOPIC


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
def corpus(request):

    domains = sorted(NLU_CORPUS_TOPIC.keys())
    return render(request, 'NLU/corpus.html', {'domains': domains, 'topics': NLU_CORPUS_TOPIC, 'project_name': PROJECT_NAME})


@login_required
def downcorpus(request):
    if request.is_ajax():

        try:
            topics = request.POST.get('topics')

            res = create_zipfile(topics, request.session.get('id'), 'corpus')
        except Exception, e:
            print e
            res = None

        t = get_template('NLU/dl_res.html')
        html = t.render(res['topics'])
        return JsonResponse({'filename': res['filename'], 'html': html}, safe=False)


@login_required
def hrl(request):
    domains = sorted(NLU_HRL_TOPIC.keys())
    return render(request, 'NLU/hrl.html', {'domains': domains, 'topics': NLU_HRL_TOPIC, 'project_name': PROJECT_NAME})


@login_required
def downhrl(request):
    if request.is_ajax():

        try:
            topics = request.POST.get('topics')

            res = create_zipfile(topics, request.session.get('id'), 'hrl')
        except Exception, e:
            print e
            res = None

        # for line in corpus_file:
        #     print line

        t = get_template('NLU/dl_res.html')
        html = t.render(res['topics'])
        return JsonResponse({'filename': res['filename'], 'html': html}, safe=False)

