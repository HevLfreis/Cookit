import random
from django.http import HttpResponse
from django.shortcuts import render
from django.core.servers.basehttp import FileWrapper

# Create your views here.
from NLU.constants import NLU_TOPIC
from NLU.methods import init, get_corpus_file

init()

print NLU_TOPIC


def index(request):

    domains = sorted(NLU_TOPIC.keys())
    return render(request, 'NLU/data.html', {'domains': domains, 'topics': NLU_TOPIC})


def downcorpus(request):

    if request.is_ajax():

        # request.session['id'] = random.randint(10000, 99999)
        try:
            topics = request.POST.get('topics')

            corpus_file = get_corpus_file(topics, random.randint(10000, 99999))
        except Exception, e:
            print e

        # for line in corpus_file:
        #     print line

        # response = HttpResponse(FileWrapper(corpus_file.getvalue()), content_type='application/zip')
        # response['Content-Disposition'] = 'attachment; filename=myfile.zip'
        return HttpResponse(corpus_file)

