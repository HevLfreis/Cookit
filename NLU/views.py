import json
import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import get_template

from NLU.constants import NLU_TOPIC
from NLU.methods import init, get_corpus_file

init()

# print NLU_TOPIC


def index(request):

    domains = sorted(NLU_TOPIC.keys())
    return render(request, 'NLU/data.html', {'domains': domains, 'topics': NLU_TOPIC})


def downcorpus(request):
    if request.is_ajax():

        # request.session['id'] = random.randint(10000, 99999)
        try:
            topics = request.POST.get('topics')

            res = get_corpus_file(topics, random.randint(10000, 99999))
        except Exception, e:
            print e
            res = None

        # for line in corpus_file:
        #     print line

        # response = HttpResponse(FileWrapper(corpus_file.getvalue()), content_type='application/zip')
        # response['Content-Disposition'] = 'attachment; filename=myfile.zip'
        # return HttpResponse(json.dumps(res))
        t = get_template('NLU/data_res.html')
        html = t.render(res['topics'])
        return JsonResponse({'filename': res['filename'], 'html': html}, safe=False)
