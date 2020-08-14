# tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory
from hatch_blog_posts import views
from rest_framework.test import APIClient



factory = APIRequestFactory()
request = factory.get('/api/ping/', {"success": "true"}, format='json')
response = views(request)

class TestViews(unittest.TestCase)
    def setUp(self):
        self.client = APIClient()

    def test_ping(self):
        res = self.client.get()