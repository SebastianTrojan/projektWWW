from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Article, Message
from .serializers import ArticleSerializer, MessageSerializer
from base.api import serializers


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/articles',
        'GET /api/articles/:id',
        'GET /api/messages',
        'GET /api/messages/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getArticles(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getArticle(request, pk):
    message = Article.objects.get(id=pk)
    serializer = MessageSerializer(message, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getMessages(request):
    messages = Message.objects.all()
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getMessage(request, pk):
    article = Message.objects.get(id=pk)
    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data)