# tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory


factory = APIRequestFactory()
request = factory.get('/api/ping/', {"success": "true"}, format='json')
