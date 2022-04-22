from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .serializers import *


class CommentSerializerTestCase(TestCase):
    def test(self):
        post1 = Article.objects.create(title='Статья1', content='Контент1')
        post2 = Article.objects.create(title='Статья2', content='Контент2')

        comment1 = Comment.objects.create(name='Лия1', email='qwerty1@gmail.com', body='интересно1', parent=None,

                                          level=0, post_id=post1.id)
        comment2 = Comment.objects.create(name='Лия2', email='qwerty2@gmail.com', body='интересно2', parent=None,
                                          level=0, post_id=post2.id)

        data = CommentSerializer([comment1, comment2], many=True).data
        expected_data = [
            {
                'post': post1.id,
                'id': comment1.id,
                'name': 'Лия1',
                'body': 'интересно1',
                'email': 'qwerty1@gmail.com',
                'parent': None,
                'level': 0
            },
            {
                'post': post2.id,
                'id': comment2.id,
                'name': 'Лия2',
                'body': 'интересно2',
                'email': 'qwerty2@gmail.com',
                'parent': None,
                'level': 0
            },
        ]
        self.assertEqual(expected_data, data)


class ApiTestCase(APITestCase):
    def test(self):
        article = Article.objects.create(title='Статья1', content='Контент1')
        url = reverse('api:article-list')
        response = self.client.get(url)
        data = ArticleSerializer([article], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data, response.data)

