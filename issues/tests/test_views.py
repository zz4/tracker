import json
from datetime import datetime

from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Issue, State, Category
from ..serializers import IssueSerializer, UserSerializer, StateSerializer,CategorySerializer


# initialize the APIClient app
client = Client()
