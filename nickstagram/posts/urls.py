from django.urls import path
from nickstagram.posts.views import CreatePostView, PostDetailsView, EditPostView, DeletePostView

urlpatterns = [
    path('create/', CreatePostView.as_view(), name='create post page'),
    path('details/<int:pk>/', PostDetailsView.as_view(), name='post details page'),
    path('edit/<int:pk>/', EditPostView.as_view(), name='post edit page'),
    path('delete/<int:pk>', DeletePostView.as_view(), name='post delete page')
]