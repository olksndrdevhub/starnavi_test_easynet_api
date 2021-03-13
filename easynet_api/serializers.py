from enum import auto
from django.contrib.auth.models import User
from django.db.models import fields

from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'password',]
        
    # custom create method to creaute new users via API
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class PostSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Post
        fields = ['id', 'title', 'body', 'likes', 'author',]

    # get author of post for GET methods
    def get_author(self, obj):
        return obj.get_author
    
    # custom create method to set author of post as current user
    def create(self, validated_data):

        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        validated_data['author']=user
        post = super(PostSerializer, self).create(validated_data)
        post.save()
        return post
        

        