import json

from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import ArticleSerializer, CommentSerializer
from .models import Article, Comment
from rest_framework import status
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from mptt.templatetags.mptt_tags import cache_tree_children


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def create_article(request):
    serializer = ArticleSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def list_article(request):
    arts = Article.objects.all()
    serializer = ArticleSerializer(arts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def create_comment(request):
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(parent=None)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def reply_comment(request, pk):
    if request.method == 'POST':
        serializer_post = CommentSerializer(data=request.data)
        if serializer_post.is_valid():
            comm = Comment.objects.get(id=pk)
            post = Article.objects.get(pk=comm.post.id)
            serializer_post.save(parent=comm, post=post)
            return Response(serializer_post.data, status=status.HTTP_201_CREATED)
        return Response(serializer_post.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        comm = Comment.objects.get(id=pk)
        serializer = CommentSerializer(comm, many=False)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def list_comment(request):
    comms = Comment.objects.filter(post_id__in=[i['id'] for i in Article.objects.values('id')])
    serializer = CommentSerializer(comms, many=True, source='parent.name')
    return Response(serializer.data)


"""@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def list_comment_lvlthree(request, pk):
    condition1 = Q(id=pk)
    condition2 = Q(level=3)
    condition4 = (~Q(level=3))
    comm = Comment.objects.get(condition1 & condition2)
    condition3 = Q(tree_id=comm.tree_id)
    comms = Comment.objects.filter(condition3 & condition4).values('id', 'name', 'body',
                                                                   'email', 'parent', 'level')
    serializer1 = CommentSerializer(comm, many=False)
    serializer2 = CommentSerializer(comms, many=True)
    content = {
        'comment': serializer1.data,
        'childrens': serializer2.data,
    }
    return Response(content, status=status.HTTP_200_OK)"""


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def list_comment_lvlthree(request, pk):

    def serialization_func(com):
        data = [{
            'name': com.name,
            'body': com.body,
            'email': com.email,
            'level': com.level,
            'children': [serialization_func(child) for child in com.get_children()]
        }]
        return data

    comment = Comment.objects.get(id=pk)
    content = serialization_func(comment)
    return Response(content, status=status.HTTP_200_OK)