from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth import get_user_model

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .serializers import UserSerializer, PostSerializer
from .models import Post
from .permissions import IsAdminOrCreateOnly


User = get_user_model()


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



@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def analitics_likes(request):

    likes_per_post = []
    total = []
    posts = Post.objects.all()

    # get date params from request if it exist
    if request.GET.get('from_date') and request.GET.get('to_date'):
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        posts = Post.objects.filter(created__range=[from_date, to_date])
    
    for post in posts:
        likes_per_post.append({str(post.created)+' '+post.title:post.likes.count()})
        total.append(post.likes.count())
    
    sum_of_likes = sum(total)

    # return total count of likes for queryset 
    # and likes for every post in queryset with date when post was created
    analitics = {
        'Total likes': sum_of_likes,
        'Likes per post': likes_per_post
    }

    return Response(analitics)



@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def analitics_users(request):

    analitics = []

    for user in User.objects.all():
        analitics.append({user.username:{
            'Last Login': user.last_login,
            'Last Request Time': user.last_request_time,
            'Date Joined': user.date_joined
        }})

    return Response(analitics)