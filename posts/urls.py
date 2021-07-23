
from django.urls.conf import include, path
from django.conf.urls import url

from .views import CreatePostView, ListPostView, RetrieveUpdateDeletePostView, LikeView

urlpatterns = [
    path('', ListPostView.as_view(), name='list_post'),
    path('create/', CreatePostView.as_view(), name='create_post'),
    path('<int:post_pk>/',RetrieveUpdateDeletePostView.as_view(), name='detail_update_delete_post'),
    path('<int:post_pk>/like/',LikeView.as_view(), name='like_dislike_listLike'),
    path('<int:post_pk>/comment/',include('comments.urls'), name='comments_post'),
]