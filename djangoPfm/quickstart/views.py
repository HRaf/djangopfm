from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.utils import json
from .serializers import NewsSerializer
from .models import News
from django.http import HttpResponse, request
from .training import TrainingModels
from .analysentiment import analysentiment
from nltk.tokenize import word_tokenize
import re


class NewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # permission_classes = [permissions.IsAuthenticated]


@api_view(['GET', 'POST', 'DELETE'])
@parser_classes([JSONParser])
def check_st_news(request):
    try:
        if request.method == 'POST':
            news_data = json.loads(request.body)
            # title = news_data['title']
            content = news_data['content']
            prediction = TrainingModels.predict(content)
            if prediction[0] == 0:
                return HttpResponse('خبر صحيح  ✅')
            else:
                HttpResponse('خبر زائف ❌')

        # result_st=predict(news_data)
        '''if title == 'Fake':
            return HttpResponse("Fake news")

        else:
            return HttpResponse(title)'''
    except:
        return HttpResponse('nothing')

#Analyse des sentiments
@api_view(['GET', 'POST', 'DELETE'])
@parser_classes([JSONParser])
def analysentiment_function(request):
    try:
        if request.method=='POST':
            feeling_data = json.loads(request.body)
            feeling_text = feeling_data['content']
            prediction=analysentiment(feeling_text)
            if prediction>0:
               return HttpResponse("Sentiment +")
            elif prediction<0:
                return HttpResponse("Sentiment -")
            else:
                return HttpResponse("Neutre")
    except:
        return HttpResponse('Error')




# Tokenization
@api_view(['GET', 'POST', 'DELETE'])
@parser_classes([JSONParser])
def tokenization(request):
    try:
        if request.method == 'POST':
            nlp_data = json.loads(request.body)
            nlp_text = nlp_data['content']
            #nlp_text=nlp_text.replace("\"","")
            nlp_text= re.sub(r"[-()\"#/@;:<>{}=~|.?,]", "", nlp_text)
            nlp_result = word_tokenize(nlp_text)
            return HttpResponse(','.join(nlp_result))
    except:
        return HttpResponse('Error')
