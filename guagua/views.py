from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


import json,httplib,urllib
from django.template import RequestContext, loader
from .models import Question


def index(request):
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('GET', '/1/classes/Prayer', '', {
       "X-Parse-Application-Id": "iMyUdfPQnXeU1bTHi3f8jhRw5oCx40UxvMfcicno",
       "X-Parse-REST-API-Key": "9CuCkIj1wCODNiCpj9lOT8LfvOTKduf5fJeQa9lc"
     })
    prayer = json.loads(connection.getresponse().read())
    context = {'question': prayer['results']}
    print prayer['results'][0]
    return HttpResponse("Hello, world. You're at the guagua index.")

prayer_idx=0
# comment_idx=0

def results(request, question_id):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    global prayer_idx
    comments_list = [] # comments dictionary of a post
    # messages=[]
    # global comment_idx
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('GET', '/1/classes/Prayer', '', {
       "X-Parse-Application-Id": "iMyUdfPQnXeU1bTHi3f8jhRw5oCx40UxvMfcicno",
       "X-Parse-REST-API-Key": "9CuCkIj1wCODNiCpj9lOT8LfvOTKduf5fJeQa9lc"
     })
    prayer = json.loads(connection.getresponse().read())

    connection.request('GET', '/1/classes/Comments', '', {
       "X-Parse-Application-Id": "iMyUdfPQnXeU1bTHi3f8jhRw5oCx40UxvMfcicno",
       "X-Parse-REST-API-Key": "9CuCkIj1wCODNiCpj9lOT8LfvOTKduf5fJeQa9lc"
    })
    comments = json.loads(connection.getresponse().read())



    # params = urllib.urlencode({"include":"comments"})
    # connection.request('GET', '/1/classes/Prayer/'+question_id+'?%s' % params, '', {
    #    "X-Parse-Application-Id": "iMyUdfPQnXeU1bTHi3f8jhRw5oCx40UxvMfcicno",
    #    "X-Parse-REST-API-Key": "9CuCkIj1wCODNiCpj9lOT8LfvOTKduf5fJeQa9lc"
    # })


    # params = urllib.urlencode({"where":json.dumps({
    #    "PostId": {
    #      "__type": "Pointer",
    #      "className": "Prayer",
    #      "objectId": "uMNQvwpBr5"
    #    }
    # })})
    # connection.request('GET', '/1/classes/Comments?%s' % params, '', {
    #    "X-Parse-Application-Id": "iMyUdfPQnXeU1bTHi3f8jhRw5oCx40UxvMfcicno",
    #    "X-Parse-REST-API-Key": "9CuCkIj1wCODNiCpj9lOT8LfvOTKduf5fJeQa9lc"
    #  })

    # comments = json.loads(connection.getresponse().read())


    for i in range(0, len(prayer['results'])):
        if (prayer['results'][i]['objectId']==question_id):
            prayer_idx=i

    # Get the comments dictionary of a post
    for i in range(0, len(comments['results'])):
        if (comments['results'][i]['PostId']==question_id):
            comments_list.append(comments['results'][i])

    if prayer['results'][prayer_idx]['A'] == 0 and prayer['results'][prayer_idx]['B'] == 0:
        percentA = 0
        percentB = 0
    else:
        percentA = 100* prayer['results'][prayer_idx]['A'] / (prayer['results'][prayer_idx]['A']+prayer['results'][prayer_idx]['B'])
        percentB = 100* prayer['results'][prayer_idx]['B'] / (prayer['results'][prayer_idx]['A']+prayer['results'][prayer_idx]['B'])

    # # get messages out of comments dictionary
    # for i in range(0, len(comments_list)):
    #     messages.append(comments_list[i]['msg'])

    context = {
            'numA': prayer['results'][prayer_idx]['A'],
            'numB': prayer['results'][prayer_idx]['B'],
            'progressA': percentA,
            'progressB': percentB,
            'choiceA': prayer['results'][prayer_idx]['QA'],
            'choiceB': prayer['results'][prayer_idx]['QB'],
            'title': prayer['results'][prayer_idx]['prayer'],
            # 'tag': prayer['results'][prayer_idx]['tag'],
            'createdAt': prayer['results'][prayer_idx]['createdAt'],
            'updatedAt': prayer['results'][prayer_idx]['updatedAt'],

            'comments_list_size': len(comments_list),
            'comments_list': comments_list,
            # 'messages': messages,
            }



    # for i in range(0, len(comments_list)):
    #     print 'msg'+str(i)
    #     context['comments_msg'+str(i)] = comments_list[i]['msg']



    return render(request, 'guagua/results.html', context)







    #response = "You're looking at the results of question %s."
    #return HttpResponse(response % question_id)
