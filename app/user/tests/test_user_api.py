# Test the userApi.
from rest_framework import status
from rest_framework.test import APICLient
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase


CREATE_USER_URL = reverse('user:create')
