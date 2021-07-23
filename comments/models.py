from django.db import models


from posts.models import Posts
from custom_user.models import CustomUser

from rest_framework.permissions import BasePermission
class Comments(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null= True, blank= True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.email + ':'+ self.content

    

class CanDelComment(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        comment = view.get_object()
        post = Posts.objects.filter(id = comment.post_id.id)
        if user == comment.user or user == post.user:
            return True
        else:
            return False
class IsOwner(BasePermission):
    def has_permission(self, request, view):

        user = request.user
        obj = view.get_object()
        if user == obj.user:
            return True
        else:
            return False