from rest_framework import serializers
from .models import Article, Comment


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content')


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all(), required=False)
    parent = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=Comment.objects.all(), required=False)

    class Meta:
        model = Comment
        fields = ('post', 'id', 'name', 'email', 'body', 'parent', 'level')

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


