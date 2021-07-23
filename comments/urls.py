
from django.urls.conf import include, path
from django.conf.urls import url

from .views import CommentsListCreate, UpdateDeleteComment, ListSubComment

urlpatterns = [
    path('', CommentsListCreate.as_view(), name='create_comments'),
    path('<int:comment_pk>/',UpdateDeleteComment.as_view(), name='detail_update_delete_post'),
    path('<int:comment_pk>/sub/', ListSubComment.as_view(), name='list_sub_comments' )
]