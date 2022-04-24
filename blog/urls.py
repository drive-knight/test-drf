from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('api/article/add/', create_article),
    path('api/articles/', list_article, name='article-list'),
    path('api/comment/add/', create_comment),
    path('api/comments/', list_comment, name='comment-list'),
    path('api/comment_reply/<int:pk>/', reply_comment),
    path('api/comment/comments/<int:pk>/', list_comment_lvlthree),

]