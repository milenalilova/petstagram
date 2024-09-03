from django.urls import path
from petstagram.common.views import index, like_photo, share_photo, add_comment

urlpatterns = [
    path('', index, name='index'),
    path('like/<int:photo_id>', like_photo, name='like photo'),
    path('share/<int:photo_id>', share_photo, name='share photo'),
    path('comment/<int:photo_id>/', add_comment, name='add comment')
]
