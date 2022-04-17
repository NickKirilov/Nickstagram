from django.urls import path
from nickstagram.comments.views import CreateCommentView, EditCommentView, delete_comment


urlpatterns = [
    path('create/<int:pk>', CreateCommentView.as_view(), name='comment post page'),
    path('edit/<int:pk>', EditCommentView.as_view(), name='edit comment page'),
    path('delete/<int:pk>', delete_comment, name='delete comment page'),
]
