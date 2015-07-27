from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


import json,httplib
from django.template import RequestContext, loader
from .models import Question


def index(request):
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('GET', '/1/classes/Prayer', '', {
       "X-Parse-Application-Id": "iMyUdfPQnXeU1bTHi3f8jhRw5oCx40UxvMfcicno",
       "X-Parse-REST-API-Key": "9CuCkIj1wCODNiCpj9lOT8LfvOTKduf5fJeQa9lc"
     })
    r = json.loads(connection.getresponse().read())
    context = {'question': r['results']}
    print r['results'][0]
    return HttpResponse("Hello, world. You're at the guagua index.")
    
idx=0    
def results(request, question_id):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    global idx
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('GET', '/1/classes/Prayer', '', {
       "X-Parse-Application-Id": "iMyUdfPQnXeU1bTHi3f8jhRw5oCx40UxvMfcicno",
       "X-Parse-REST-API-Key": "9CuCkIj1wCODNiCpj9lOT8LfvOTKduf5fJeQa9lc"
     })
    r = json.loads(connection.getresponse().read())

    for i in range(0, len(r['results'])):
        if (r['results'][i]['objectId']==question_id):
            idx=i

    context = {
            'numA': r['results'][idx]['A'],
            'numB': r['results'][idx]['B'],
            'choiceA': r['results'][idx]['QA'],
            'choiceB': r['results'][idx]['QB'], 
            'title': r['results'][idx]['prayer'],
            # 'tag': r['results'][idx]['tag'],
            'createdAt': r['results'][idx]['createdAt'],
            'updatedAt': r['results'][idx]['updatedAt'],  
            }            
    return render(request, 'guagua/results.html', context)
            
            
            
            
    
    
    
    #response = "You're looking at the results of question %s."
    #return HttpResponse(response % question_id)