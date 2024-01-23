from rest_framework.serializers import ModelSerializer
from base.models import Article, Message


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
