from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from .serializers import UserSerializer, PostSerializer
from .models import Post
from .permissions import IsAdminOrCreateOnly

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrCreateOnly]



class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


def index(request):
    return HttpResponse('<h1>Go to <a href="/api/v1/">/api/v1/</a> URI</h1>')


def like_post(request):
    user = request.user
    print(request)
    return HttpResponse('hi')