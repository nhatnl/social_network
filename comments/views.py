
from django.shortcuts import render

from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from comments.serializers import CommentSerializer
from comments.models import Comments, CanDelComment, IsOwner
class CommentsListCreate(ListCreateAPIView):
    model = Comments
    lookup_url_kwarg = 'comment_pk'
    lookup_url_kwarg_post_pk = 'post_pk'
    def get_serializer_class(self):
        return CommentSerializer
    
    def get_queryset(self):
        return self.model.objects.filter(post_id = self.kwargs[self.lookup_url_kwarg_post_pk])

class UpdateDeleteComment(RetrieveUpdateDestroyAPIView):
    model = Comments
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'comment_pk'
    lookup_url_kwarg_post_pk = 'post_pk'
    def get_queryset(self):
        return self.model.objects

    def get_serializer_class(self):
        return CommentSerializer
    
    def get_object(self):
        if self.request.method == 'DELETE':
            self.permission_classes.append(CanDelComment)
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            self.permission_classes.append(IsOwner)

        return super().get_object()
    def perform_destroy(self, instance):
        sub_comments = self.model.objects.filter(parent_id = instance.id)
        if sub_comments:
            for comment in sub_comments:
                self.perform_destroy(comment)
        instance.delete()

class ListSubComment(ListAPIView):
    model = Comments
    lookup_url_kwarg = 'comment_pk'
    lookup_url_kwarg_post_pk = 'post_pk'
    def get_serializer_class(self):
        return CommentSerializer
    def get_queryset(self):
        return self.model.objects.filter(
            post_id = self.kwargs[self.lookup_url_kwarg_post_pk],
            parent_id = self.kwargs[self.lookup_url_kwarg]
            )
