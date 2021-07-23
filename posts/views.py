
import re
from django.db import models
from django.shortcuts import get_object_or_404, render
from django.db.models.signals import post_save
from django.dispatch import receiver


from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Posts
from .serializers import PostSerializer, LikeSerializer
from custom_user.models import CustomUser
from comments.models import IsOwner
class CreatePostView(CreateAPIView):
    model = Posts
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        return PostSerializer
    

class ListPostView(ListAPIView):
    model = Posts
    permission_classes = [AllowAny]
    def get_serializer_class(self):
        return PostSerializer
    def get_queryset(self):
        return self.model.objects



class RetrieveUpdateDeletePostView(RetrieveUpdateDestroyAPIView):
    model = Posts
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'post_pk'
    def get_queryset(self):
        return self.model
    def get_serializer_class(self):
        return PostSerializer
    
    

        

class LikeView(ListCreateAPIView, DestroyAPIView):
    model = Posts
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'post_pk'
    def get_serializer_class(self):
        return LikeSerializer
    def get_queryset(self):
        return self.model.objects.filter(id = self.kwargs[self.lookup_url_kwarg])
    
    def get_object(self):
        return get_object_or_404(Posts, id = self.kwargs[self.lookup_url_kwarg])

    def perform_destroy(self, instance):
        user = self.request.user
        instance.likes.remove(user)