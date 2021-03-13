from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

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



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def like_unlike_post(request, id):

    user = request.user
    post = Post.objects.get(id=id)
    serializer = PostSerializer(post)

    if user not in post.likes.all():
        post.like_post(user)
        serializer = PostSerializer(post)
        return Response(serializer.data)
        
    elif user in post.likes.all():
        post.unlike_post(user)
        serializer = PostSerializer(post)
        return Response(serializer.data)