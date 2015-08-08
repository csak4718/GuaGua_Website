# -*- coding: utf-8 -*-
from django.shortcuts import render

from django.http import HttpResponse

import json,httplib,urllib
from django.template import RequestContext, loader
from .models import Question

import datetime

from django.utils.dateparse import parse_datetime
import pytz

from django.utils import timezone


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
def results(request, question_id):
    global prayer_idx
    comments_list = [] # comments dictionary of a post
    commenters_list = []

    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('GET', '/1/classes/Prayer', '', {
       "X-Parse-Application-Id": "iMyUdfPQnXeU1bTHi3f8jhRw5oCx40UxvMfcicno",
       "X-Parse-REST-API-Key": "9CuCkIj1wCODNiCpj9lOT8LfvOTKduf5fJeQa9lc"
     })
    prayer = json.loads(connection.getresponse().read())

    params = urllib.urlencode({"order":"createdAt"})
    connection.request('GET', '/1/classes/Comments?%s'% params, '', {
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
            comments['results'][i]['createdAtInLocalTime'] = getRelativeDateTime(comments['results'][i]['createdAt'])
            comments_list.append(comments['results'][i])

    for i in range(0, len(comments_list)):
        connection.request('GET', '/1/users/'+comments_list[i]['userId'], '', {
        "X-Parse-Application-Id": "iMyUdfPQnXeU1bTHi3f8jhRw5oCx40UxvMfcicno",
        "X-Parse-REST-API-Key": "9CuCkIj1wCODNiCpj9lOT8LfvOTKduf5fJeQa9lc"
        })
        commenters_list.append(json.loads(connection.getresponse().read()))

    if prayer['results'][prayer_idx]['A'] == 0 and prayer['results'][prayer_idx]['B'] == 0:
        percentA = 0
        percentB = 0
    else:
        percentA = 100* prayer['results'][prayer_idx]['A'] / (prayer['results'][prayer_idx]['A']+prayer['results'][prayer_idx]['B'])
        percentB = 100* prayer['results'][prayer_idx]['B'] / (prayer['results'][prayer_idx]['A']+prayer['results'][prayer_idx]['B'])

    grouped_list = zip(commenters_list, comments_list)


    posterId = prayer['results'][prayer_idx]['user']['objectId']
    connection.request('GET', '/1/users/'+posterId, '', {
    "X-Parse-Application-Id": "iMyUdfPQnXeU1bTHi3f8jhRw5oCx40UxvMfcicno",
    "X-Parse-REST-API-Key": "9CuCkIj1wCODNiCpj9lOT8LfvOTKduf5fJeQa9lc"
    })
    poster = json.loads(connection.getresponse().read())

    postRelativeDateTime = getRelativeDateTime(prayer['results'][prayer_idx]['createdAt'])

    context = {
            'post': prayer['results'][prayer_idx],
            'postRelativeDateTime': postRelativeDateTime,
            'poster': poster,

            'progressA': percentA,
            'progressB': percentB,

            'comments_list_size': len(comments_list), # hasn't be used in html so far
            'comments_list': comments_list, # hasn't be used in html so far
            'commenters_list': commenters_list, # hasn't be used in html so far
            'grouped_list': grouped_list,

            }
    return render(request, 'guagua/results.html', context)

def getRelativeDateTime(mDate):
    taipei_tz = pytz.timezone('Asia/Taipei')
    nowInUTC = datetime.datetime.now()

    # correct way to show time string in Local (Taiwan) time
    nowInLocalTime = datetime.datetime.now(taipei_tz)

    dateInUTC = parse_datetime(mDate).replace(tzinfo=None)

    timeDelta = nowInUTC - dateInUTC
    dateInLocalTime = nowInLocalTime - timeDelta

    diff = nowInLocalTime - dateInLocalTime
    s = diff.seconds
    if diff.days > 7 or diff.days < 0:
        return dateInLocalTime.strftime('%-m 月 %-d 日 %H:%M')
    elif diff.days == 1:
        return '1 天前'
    elif diff.days > 1:
        return '{} 天前'.format(diff.days)
    elif s <= 1:
        return 'Just now' # To do: translate to Chinese
    elif s < 60:
        return '{} 秒前'.format(s)
    elif s < 120:
        return '1 分鐘前'
    elif s < 3600:
        return '{} 分鐘前'.format(s/60)
    elif s < 7200:
        return '1 小時前'
    else:
        return '{} 小時前'.format(s/3600)







    #response = "You're looking at the results of question %s."
    #return HttpResponse(response % question_id)
