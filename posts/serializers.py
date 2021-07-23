
from django.db import models
from django.db.models import fields
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Posts
from custom_user.serializers import UserSerializer, CustomUser
from comments.serializers import CommentSerializer, Comments

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Posts
        fields = ['content', 'mode', 'create_at', 'likes', 'comments']
        extra_kwargs = {
            'content': {'required': True},
            'create_at':{'read_only': True},
            'likes':{
                'required': False,
                'default':[]
            },
            'mode':{
                'default':'PB'
            }
        }
    def save(self, **kwargs):
        content = self.validated_data['content']
        user = self.context.get('request').user
        mode = self.validated_data['mode']
        post = Posts(
            content=content,
            user=user,
            mode=mode
        )
        post.save()
        return post

    def get_current_post(self):
        post_id = self.context.get('view').kwargs[self.context.get('view').lookup_url_kwarg]
        post = get_object_or_404(Posts, id = post_id)
        return post

    def get_comments(self, obj):
        obj.comments = Comments.objects.filter(post_id = self.get_current_post().id)
        return obj.comments

class LikeSerializer(serializers.ModelSerializer):
    # fields = ['likes', 'count']
    likes = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Posts
        fields = ['likes']
    
    def is_liked(self, user = None):
        if user is None:
            user = self.context.get('request').user
        post = get_object_or_404(Posts, id = self.context.get('view').kwargs[self.context.get('view').lookup_url_kwarg])
        if post.likes.filter(id=user.id):
            return True
        else:
            return False
    
    def save(self, **kwargs):
        user = self.context.get('request').user
        post = get_object_or_404(Posts, id = self.context.get('view').kwargs[self.context.get('view').lookup_url_kwarg])
        if self.is_liked(user=user):
            pass
        else:
            post.likes.add(user)
            post.save()
        return post

